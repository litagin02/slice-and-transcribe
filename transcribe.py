import os
import sys

from faster_whisper import WhisperModel
from tqdm import tqdm

model = WhisperModel("large-v3", device="cuda", compute_type="float16")


def transcribe(wav_path, initial_prompt=None):
    segments, _ = model.transcribe(
        wav_path, beam_size=5, language="ja", initial_prompt=initial_prompt
    )
    texts = [segment.text for segment in segments]
    return "".join(texts)


if __name__ == "__main__":
    wav_dir = "raw"
    output_file = "text.list"
    initial_prompt = "こんにちは。元気、ですかー？私はちゃんと元気だよ。"

    wav_files = [
        os.path.join(wav_dir, f) for f in os.listdir(wav_dir) if f.endswith(".wav")
    ]
    if os.path.exists(output_file):
        print(f"{output_file}が存在するので、バックアップを{output_file}.bakに作成します。")
        if os.path.exists(output_file + ".bak"):
            print(f"{output_file}.bakも存在するので、削除します。")
            os.remove(output_file + ".bak")
        os.rename(output_file, output_file + ".bak")

    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <speaker_name>")
        sys.exit(1)
    speaker_name = sys.argv[1]

    with open(output_file, "w", encoding="utf-8") as f:
        for wav_file in tqdm(wav_files):
            file_name = os.path.basename(wav_file)
            text = transcribe(wav_file, initial_prompt=initial_prompt)
            f.write(
                f"Data/{speaker_name}/audios/wavs/{file_name}|{speaker_name}|JP|{text}\n"
            )
