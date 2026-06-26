#!/usr/bin/env python3
import subprocess
import sys
import wave
from pathlib import Path


def is_silk(path: Path) -> bool:
    head = path.read_bytes()[:16]
    return b'#!SILK_V3' in head


def decode_silk_to_wav(src: Path, wav: Path, sample_rate: int = 24000) -> None:
    import pysilk

    pcm_path = wav.with_suffix('.pcm')
    with src.open('rb') as fi, pcm_path.open('wb') as fo:
        pysilk.decode(fi, fo, sample_rate)

    raw = pcm_path.read_bytes()
    with wave.open(str(wav), 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(raw)

    pcm_path.unlink(missing_ok=True)


def decode_to_wav(src: Path, wav: Path) -> None:
    if is_silk(src):
        decode_silk_to_wav(src, wav)
    else:
        subprocess.run(
            ['ffmpeg', '-y', '-i', str(src), str(wav)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def transcribe(wav: Path) -> str:
    from faster_whisper import WhisperModel

    model = WhisperModel('base', device='cpu', compute_type='int8')
    segments, info = model.transcribe(str(wav), language='zh', vad_filter=False, beam_size=5)
    texts = [seg.text.strip() for seg in segments if seg.text.strip()]
    return '\n'.join(texts)


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: transcribe_wechat_voice.py <audio_path> [wav_out]', file=sys.stderr)
        raise SystemExit(2)

    src = Path(sys.argv[1])
    wav = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('/tmp/wechat-voice-decoded.wav')
    decode_to_wav(src, wav)
    text = transcribe(wav)
    print(text if text else 'NO_SEGMENTS')


if __name__ == '__main__':
    main()
