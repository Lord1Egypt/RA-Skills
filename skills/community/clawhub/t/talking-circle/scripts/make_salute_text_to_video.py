#!/usr/bin/env python3
"""One-shot: SaluteSpeech TTS (Sber) + animated circle avatar video."""
import argparse
import os
import subprocess
import tempfile
import uuid
from pathlib import Path

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(str(c) for c in cmd)}\n{result.stderr}")
    return result


def ensure_runtime_python() -> str:
    """Return python path with required video deps for make_talking_circle_video.py."""
    venv_dir = Path("/tmp/talking-circle-venv")
    py = venv_dir / "bin" / "python"
    if py.exists():
        return str(py)

    subprocess.run(["python3", "-m", "venv", str(venv_dir)], check=True)
    pip = venv_dir / "bin" / "pip"
    req = Path(__file__).resolve().parents[1] / "requirements.txt"
    subprocess.run([str(pip), "install", "--quiet", "-r", str(req)], check=True)
    return str(py)


def get_salute_token(auth_key: str, scope: str) -> str:
    """Get OAuth token from SaluteSpeech API. Token is valid for 30 minutes."""
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
        "Authorization": f"Basic {auth_key}",
    }
    r = requests.post(url, headers=headers, data={"scope": scope}, timeout=30, verify=False)
    r.raise_for_status()
    return r.json()["access_token"]


def synthesize_salute(token: str, text: str, voice: str, audio_format: str) -> bytes:
    """Synthesize speech via SaluteSpeech REST API."""
    url = "https://smartspeech.sber.ru/rest/v1/text:synthesize"
    params = {"format": audio_format, "voice": voice}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/text",
    }
    r = requests.post(url, headers=headers, params=params, data=text.encode("utf-8"), timeout=90, verify=False)
    if r.status_code == 401:
        raise SystemExit("SaluteSpeech auth failed (401). Check your SALUTE_SPEECH_AUTH key.")
    if r.status_code == 429:
        raise SystemExit("SaluteSpeech rate limit (429). Try again later.")
    r.raise_for_status()
    return r.content


def main():
    p = argparse.ArgumentParser(description="One-shot: SaluteSpeech TTS + animated circle avatar video")
    p.add_argument("--text", required=True)
    p.add_argument("--out", required=True)

    p.add_argument("--neutral", required=True)
    p.add_argument("--slight", required=True)
    p.add_argument("--wide", required=True)
    p.add_argument("--blink", required=True)

    # SaluteSpeech auth
    p.add_argument("--auth-key", default=os.getenv("SALUTE_SPEECH_AUTH"),
                    help="Base64-encoded client_id:client_secret (or set SALUTE_SPEECH_AUTH)")
    p.add_argument("--scope", default="SALUTE_SPEECH_PERS",
                    choices=["SALUTE_SPEECH_PERS", "SALUTE_SPEECH_CORP"],
                    help="OAuth scope (default: SALUTE_SPEECH_PERS)")

    # Voice settings
    p.add_argument("--voice", default="Bys_24000",
                    help="SaluteSpeech voice (default: Bys_24000). "
                         "Options: Nec_24000 (Natalia), Bys_24000 (Boris), "
                         "May_24000 (Martha), Tur_24000 (Taras), "
                         "Ost_24000 (Alexandra), Pon_24000 (Sergey), "
                         "Kin_24000 (Kira, en-US)")
    p.add_argument("--audio-format", default="wav16", choices=["opus", "wav16", "pcm16"],
                    help="Audio output format (default: wav16)")

    # Video settings
    p.add_argument("--size", type=int, default=720)
    p.add_argument("--diameter", type=int, default=640)
    p.add_argument("--fps", type=int, default=30)

    p.add_argument("--blink-start", type=float, default=1.1)
    p.add_argument("--blink-every", type=float, default=3.8)
    p.add_argument("--blink-duration-frames", type=int, default=4)

    p.add_argument("--amp-low", type=int, default=1200)
    p.add_argument("--amp-high", type=int, default=2600)

    args = p.parse_args()

    if not args.auth_key:
        raise SystemExit(
            "Missing SaluteSpeech auth key. Set SALUTE_SPEECH_AUTH or pass --auth-key.\n"
            "To get the key: encode your client_id:client_secret in Base64.\n"
            "Register at https://developers.sber.ru/portal/products/smartspeech"
        )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    neutral = Path(args.neutral)
    slight = Path(args.slight)
    wide = Path(args.wide)
    blink = Path(args.blink)
    for f in [neutral, slight, wide, blink]:
        if not f.exists():
            raise SystemExit(f"Missing frame file: {f}")

    log_path = out.with_suffix(".build.log")

    # Get OAuth token
    token = get_salute_token(args.auth_key, args.scope)

    # Map format to file extension
    ext_map = {"opus": ".opus", "wav16": ".wav", "pcm16": ".pcm"}
    audio_ext = ext_map.get(args.audio_format, ".wav")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        audio = td / f"speech{audio_ext}"

        # Synthesize speech
        audio_bytes = synthesize_salute(token, args.text, args.voice, args.audio_format)
        audio.write_bytes(audio_bytes)

        script = Path(__file__).with_name("make_talking_circle_video.py")
        runtime_python = ensure_runtime_python()
        cmd = [
            runtime_python,
            str(script),
            "--neutral", str(neutral),
            "--slight", str(slight),
            "--wide", str(wide),
            "--blink", str(blink),
            "--audio", str(audio),
            "--out", str(out),
            "--blink-start", str(args.blink_start),
            "--blink-every", str(args.blink_every),
            "--blink-duration-frames", str(args.blink_duration_frames),
            "--size", str(args.size),
            "--diameter", str(args.diameter),
            "--fps", str(args.fps),
            "--amp-low", str(args.amp_low),
            "--amp-high", str(args.amp_high),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        log_path.write_text(
            f"RC={result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\n"
        )

        if result.returncode != 0:
            raise SystemExit(
                f"Animated video build failed.\n{result.stderr}\nSee build log: {log_path}"
            )

    if not out.exists() or out.stat().st_size == 0:
        raise RuntimeError("Output video is missing or empty")

    print(str(out))


if __name__ == "__main__":
    main()
