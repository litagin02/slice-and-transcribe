# TTS のためのデータセット作りをするやつ

音声ファイルたちから、

1. [slice.py](slice.py): 発話区間を 2-12 秒に収まるように分割 ([Silero VAD](https://github.com/snakers4/silero-vad)を使用)
2. [transcribe.py](transcribe.py): 分割したファイルからテキストを書き起こして保存([Faster Whisper](https://github.com/SYSTRAN/faster-whisper)を使用)

をするやつです。

[Bert-VITS2](https://github.com/fishaudio/Bert-VITS2/) で使うために作りました。

## 導入

**ffmpeg のインストールが別途必要です**、「Couldn't find ffmpeg」とか怒られたら、「Windows ffmpeg インストール」等でググって別途インストールしてください。

```
git clone https://github.com/litagin02/slice-and-transcribe.git
cd slice_and_transcribe
python -m venv venv
venv\Scripts\activate
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

## 音声分割

`inputs`フォルダを作り、そこに wav ファイルたちを入れてください。

```bash
python slice.py
```

スライスされた結果が`raw`ディレクトリに保存されます。

デフォルトは 2 秒から 12 秒の発話のみが保存されます。

パラメータ：

- `--max_sec`, `-M`: 最大秒数、デフォルトは 12 秒
- `--min_sec`, `-m`: 最小秒数、デフォルトは 2 秒
- `--min_silence_dur_ms`, `-s`: 無音とみなす秒数の長さ（ミリ秒）、デフォルトは 700ms。 このミリ秒数以上を無音だと判断する。逆に、この秒数以下の無音区間では区切られない。小さくすると、音声がぶつ切りに小さくなりすぎ、大きくすると音声一つ一つが長くなりすぎる。

例：

```bash
python slice.py -M 15 -m 3 -s 1000
```


## 書き起こし

`raw`ディレクトリにある wav ファイルからテキストを書き起こし、`text.list`に保存します。

```bash
python transcribe.py speaker_name
```

書き起こし形式は、

```
Data/{speaker_name}/audios/wavs/{file_name}|{speaker_name}|JP|{text}
```

という形です（Bert-VITS2 ですぐ使える形にしている）ので、必要なら適宜 [transcribe.py](transcribe.py) を書き換えてください。
