import subprocess
from pathlib import Path
import wave



def _synthesize_mock(text: str, output_wav: Path) -> Path:
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_wav), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(22050)
        wav_file.writeframes(b"\x00\x00" * 22050)
    return output_wav



def synthesize_with_piper(
    text: str,
    output_wav: Path,
    model_path: Path,
    piper_binary: str = "piper",
    backend: str = "piper",
) -> Path:
    if backend == "mock":
        return _synthesize_mock(text, output_wav)

    command = [
        piper_binary,
        "--model",
        str(model_path),
        "--output_file",
        str(output_wav),
    ]

    subprocess.run(
        command,
        input=text.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return output_wav
