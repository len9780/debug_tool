# ESP crash stack trace
Usage: python script.py <elf_file> <addresses_file>
# google wavenet tts test tool
用"google_wavenet_tts.py"需先安裝以下python packet
```python=
pip install google-cloud-texttospeech
```
## 使用方式
```bash=
python google_wavenet_tts.py
```
Ps. 相對的參數會透過上述命令顯示出來，按照填寫參數的內容即可。
# azure tts test tool
用"azure_tts.py"需先安裝以下python packet
```python=
pip install azure-cognitiveservices-speech
```
## 使用方式
```bash=
python azure_tts.py --voice_model $voice_model
```
voice_model內容可參照: https://github.com/jsbxyyx/tts_java
Ps. 相對的參數會透過上述命令顯示出來，按照填寫參數的內容即可。
