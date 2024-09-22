
import os
import argparse
from google.cloud import texttospeech

# 命令參數宣告
parser = argparse.ArgumentParser(description="Google WaveNet TTS 示例")
parser.add_argument("--credential_path", required=True, help="Google Cloud 憑證文件的路徑")
parser.add_argument("--mp3_out", required=True, help="tts mp3 輸出檔案")
 # 解析命令行參數
args = parser.parse_args()

# 設定 Google Cloud 認證（路徑為你下載的 JSON 憑證檔）
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.credential_path

# 初始化客戶端
client = texttospeech.TextToSpeechClient()

# 設定合成的文本
text = "你好，歡迎使用 Google WaveNet 文字轉語音服務。"

# 設定語音請求內容
synthesis_input = texttospeech.SynthesisInput(text=text)

# 設定語音參數
voice = texttospeech.VoiceSelectionParams(
    language_code="cmn-TW",  # 中文
    name="cmn-TW-Standard-A",  # 使用 輸出檔案WaveNet 模型
)

# 設定音頻配置
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3  # 音頻格式為 MP3
)

# 發送請求進行合成
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# 將合成的音頻寫入文件
with open(args.mp3_out, "wb") as out:
    out.write(response.audio_content)
    print("音頻內容已寫入 ",args.mp3_out)
