# TTSのためのデータセット作りをするやつ

音声ファイルたちから、
1. [slice.py](slice.py): 発話区間を2-10秒に収まるように分割 ([Silero VAD](https://github.com/snakers4/silero-vad)を使用)
2. [transcribe.py](transcribe.py): 分割したファイルからテキストを書き起こして保存([Faster Whisper](https://github.com/SYSTRAN/faster-whisper)を使用)

をするやつです。

[Bert-VITS2](https://github.com/fishaudio/Bert-VITS2/) で使うために作りました。

## 導入

**ffmpegのインストールが別途必要です**、「Couldn't find ffmpeg」とか怒られたら、「Windows ffmpeg インストール」等でググって別途インストールしてください。

```
git clone https://github.com/litagin02/slice-and-transcribe.git
cd slice_and_transcribe
python -m venv venv
venv\Scripts\activate
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

## 音声分割

wavファイルを`inputs`ディレクトリに入れてください。
```
python slice.py
```
スライスされた結果が`raw`ディレクトリに保存されます。

デフォルトは2秒から10秒の発話のみが保存されます。気になる人は [slice.py](slice.py) を見て各種パラメータ（他にも無音とみなす秒数の長さやらマージンやら）をデータセットに応じて調整してください。

## 書き起こし

`raw`ディレクトリにあるwavファイルからテキストを書き起こし、`text.list`に保存します。
```
python transcribe.py speaker_name
```
書き起こし形式は、
```
Data/{speaker_name}/audios/wavs/{file_name}|{speaker_name}|JP|{text}
```
という形です（Bert-VITS2ですぐ使える形にしている）ので、必要なら適宜 [transcribe.py](transcribe.py) を書き換えてください。
