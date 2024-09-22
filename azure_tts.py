
import os
import argparse
import azure.cognitiveservices.speech as speechsdk

# 命令參數宣告
parser = argparse.ArgumentParser(description="AZURE TTS 示例")
parser.add_argument("--voice_model", required=True, help="Voice Model")
parser.add_argument("--sub_key", required=True, help="subscription key")
parser.add_argument("--region", required=True, help="region")
args = parser.parse_args()


# 设置 Azure 语音服务的订阅密钥和服务区域
subscription_key = args.sub_key
region = args.region  # 如 "eastus"

def text_to_speech(text):
    # 创建语音配置对象
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    
    # 设置语音合成的语言（可根据需求更改语言和语音类型）
    speech_config.speech_synthesis_voice_name = args.voice_model  # 中文女性语音

    # 创建语音合成器对象(僅音源輸出)
    #audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    #用於輸出mp3
    audio_config = speechsdk.audio.AudioOutputConfig(filename='test.mp3')

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    #speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav"))


    # 合成文本到语音
    result = speech_synthesizer.speak_text_async(text).get()

    # 检查合成结果
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("语音合成成功!")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"语音合成取消: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"错误详情: {cancellation_details.error_details}")

if __name__ == "__main__":
    text = "你好，这是一个 Azure 文本转语音的测试程序。"
    text_to_speech(text)
