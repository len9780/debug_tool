# 操作命令: python.exe C:\Users\yesid\Desktop\watchdog_backtrace.py .\build\play_and_save.elf C:\Users\yesid\Desktop\address.txt

import subprocess
import sys

def addr2line(elf_file, addresses):
    # Command template
    command = ["xtensa-esp32-elf-addr2line.exe", "-pfiaC", "-e", elf_file]

    # Run addr2line for each address
    results = []
    for address in addresses:
        try:
            result = subprocess.run(command + [address], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            results.append(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            results.append(f"Error: {e.stderr.strip()}")
    
    return results

def read_addresses_from_file(file_path):
    with open(file_path, 'r') as f:
       content = f.read().strip()
    addresses = content.split()
    return addresses

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <elf_file> <addresses_file>")
        sys.exit(1)
    
    elf_file = sys.argv[1]
    addresses_file = sys.argv[2]
    
    addresses = read_addresses_from_file(addresses_file)
    
    results = addr2line(elf_file, addresses)
    
    for result in results:
        print(result)
