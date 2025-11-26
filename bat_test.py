import socket
import struct
import json
import time

HOST = "192.168.31.97"   # Server IP
PORT = 3333              # Server Port
OUTPUT_FILE = "d://log.jsonl"  # JSONL 格式（每行一筆 JSON，適合接資料）

def bytes_to_hex(b: bytes) -> str:
    return b.hex(" ").upper()   # 每 byte 以空白分隔並轉大寫

def write_to_file(data: dict):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")  # JSONL格式，每筆一行

def parse_packet(data: bytes) -> dict | None:
    # 至少要有 14 bytes 才能解析
    if len(data) < 14:
        return None

    # 過濾條件：byte1 == 0x02 且 byte2 == 0x47
    if not (data[1] == 0x02 and data[2] == 0x47):
        return None

    # 解析 IEEE754 float (little-endian)
    col0 = struct.unpack('<f', data[4:8])[0]     # byte4–7
    col1 = struct.unpack('<f', data[8:12])[0]    # byte8–11

    # byte12、byte13 十進制
    col2 = data[12]
    col3 = data[13]

  # 新增：column4 = byte14–byte17 (IEEE754 float)
    col4 = struct.unpack('<f', data[14:18])[0]   # byte14–17

  # 新增：column5 = byte18–byte21 (IEEE754 float)
    col5 = struct.unpack('<f', data[18:22])[0]   # byte18–21

    epoch = time.time()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(epoch))
    return {
        "timestamp": timestamp,
        "Min_Bat_Vol": col0,
        "Max_Bat_Vol": col1,
        "Chrg_Status": col2,
        "batt_percentage_local": col3,
        "vol": col4,
        "bq_bat_vol": col5
    }

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # <── 讓 recv 不會永遠卡住
            s.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT}")

            while True:
                try:
                    data = s.recv(80)
                except socket.timeout:
                    continue  # 超時就再試一次（讓 Ctrl+C 有機會觸發）

                if not data:
                    print("Server closed the connection.")
                    break

                #print("HEX:", bytes_to_hex(data))
                #print("-------------------------")
                parsed = parse_packet(data)
                if parsed:
                    #print("JSON:", json.dumps(parsed, ensure_ascii=False))
                    #print("=========================")
		    # 寫入檔案
                    write_to_file(parsed)
            print("while True: end")

    except KeyboardInterrupt:
        print("\n[User Exit] Connection closed by user.")
    except Exception as e:
        print(f"[Error] {e}")

if __name__ == "__main__":
    main()
