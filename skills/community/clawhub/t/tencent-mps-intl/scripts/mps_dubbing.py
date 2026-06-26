#!/usr/bin/env python3
"""
Tencent Cloud MPS Voice Synthesis and Voice Cloning Script

Features:
  AI-powered voice cloning and speech synthesis for audiobooks, podcasts,
  audio/video dubbing, and more. Supports 40+ languages including Chinese,
  English, Japanese, Korean, and others. Provides rich system voices and
  high-fidelity voice cloning.

  Modes (specified via --mode):

  ● clone        Voice cloning (synchronous)
                 Submit a cloning audio; returns a VoiceId.
                 Recommended audio: 10–20 seconds, single speaker, clear voice.

  ● tts          Short-text speech synthesis (synchronous)
                 Submit text + VoiceId; returns synthesized WAV audio.
                 Texts up to 2000 characters use the sync API; longer texts
                 are automatically switched to async-tts (no manual action needed).

  ● async-tts    Long-text to speech (asynchronous, TextToSpeech)
                 Submits an async task via ProcessMedia; supports very long texts;
                 output audio written to COS.

  ● async-sts    Speech-to-speech (asynchronous, SpeechToSpeech)
                 Submits an async task via ProcessMedia; replaces the voice of
                 the input audio/video; output written to COS.

COS Storage Convention:
  The COS bucket is specified via the TENCENTCLOUD_COS_BUCKET environment variable.
  - Default output path: {TENCENTCLOUD_COS_BUCKET}/output/dubbing/

Usage:
  # Voice cloning (local audio file)
  python mps_dubbing.py --mode clone --audio-file /path/to/voice.wav

  # Voice cloning (audio URL)
  python mps_dubbing.py --mode clone --audio-url https://example.com/voice.mp4

  # Short-text TTS (system voice ID)
  python mps_dubbing.py --mode tts --text "Hello, welcome to Tencent Cloud!" --voice-id s1_2GSzVAf00hl

  # Short-text TTS (save to file)
  python mps_dubbing.py --mode tts --text "Hello, welcome!" --voice-id s1_xxx --output /tmp/output.wav

  # Clone + TTS workflow (clone first, then synthesize)
  python mps_dubbing.py --mode clone --audio-file /path/to/voice.wav
  python mps_dubbing.py --mode tts --text "Hello" --voice-id <VoiceId from previous step>

  # Long-text TTS (async, specify voice ID)
  python mps_dubbing.py --mode async-tts \\
      --text "This is a very long text..." --voice-id clone_v1_Q03FBduA

  # Long-text TTS (async, clone from video URL)
  python mps_dubbing.py --mode async-tts \\
      --text "This is a very long text..." \\
      --clone-video-url https://example.com/train.mp4

  # Speech-to-speech (async, replace voice)
  python mps_dubbing.py --mode async-sts \\
      --url https://example.com/video.mp4 \\
      --clone-video-url https://example.com/train.mp4

  # Speech-to-speech (async, system voice ID)
  python mps_dubbing.py --mode async-sts \\
      --url https://example.com/video.mp4 --voice-id s1_2GSzVAf00hl

  # Dry Run (print request parameters only, no API call)
  python mps_dubbing.py --mode tts --text "Hello" --voice-id s1_xxx --dry-run

Environment Variables:
  TENCENTCLOUD_SECRET_ID   - Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  - Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET  - COS bucket name (required for async modes)
  TENCENTCLOUD_COS_REGION  - COS bucket region (required for async modes)
"""

import argparse
import base64
import json
import os
import sys
from mps_auto_upgrade import check_sdk_version
import time
import urllib.request

# Helper modules in the same directory
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False

try:
    from mps_poll_task import poll_video_task, auto_download_outputs
    _POLL_AVAILABLE = True
except ImportError:
    _POLL_AVAILABLE = False

check_sdk_version()
try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.mps.v20190612 import mps_client, models
except ImportError:
    print("Error: Please install the Tencent Cloud SDK first: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# Constants
# =============================================================================

# SyncDubbing API endpoint (for international: set TENCENTCLOUD_MPS_ENDPOINT=mps.intl.tencentcloudapi.com)
MPS_ENDPOINT = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")

# Async dubbing definition ID (TextToSpeech / SpeechToSpeech)
ASYNC_DUBBING_DEFINITION = 36

# Supported languages
SUPPORTED_LANGS = {
    "zh": "Chinese",
    "en": "English",
    "ja": "Japanese",
    "de": "German",
    "fr": "French",
    "ko": "Korean",
    "ru": "Russian",
    "uk": "Ukrainian",
    "pt": "Portuguese",
    "it": "Italian",
    "es": "Spanish",
    "id": "Indonesian",
    "nl": "Dutch",
    "tr": "Turkish",
    "fil": "Filipino",
    "ms": "Malay",
    "el": "Greek",
    "fi": "Finnish",
    "hr": "Croatian",
    "sk": "Slovak",
    "pl": "Polish",
    "sv": "Swedish",
    "hi": "Hindi",
    "bg": "Bulgarian",
    "ro": "Romanian",
    "ar": "Arabic",
    "cs": "Czech",
    "da": "Danish",
    "ta": "Tamil",
    "hun": "Hungarian",
    "vi": "Vietnamese",
    "no": "Norwegian",
    "yue": "Cantonese",
    "th": "Thai",
    "he": "Hebrew",
    "ca": "Catalan",
    "nn": "Nynorsk",
    "af": "Afrikaans",
    "fa": "Persian",
    "sl": "Slovenian",
}

# Supported sample rates
SUPPORTED_SAMPLE_RATES = [8000, 16000, 22050, 32000, 44100]

# Mode descriptions
MODES = {
    "clone":     "Voice cloning (sync) — submit cloning audio, returns VoiceId",
    "tts":       "Short-text TTS (sync) — submit text + VoiceId, returns WAV audio",
    "async-tts": "Long-text TTS (async TextToSpeech) — submit long text, output to COS",
    "async-sts": "Speech-to-speech (async SpeechToSpeech) — replace voice in audio/video, output to COS",
}

# Max text length for sync TTS (auto-switch to async if exceeded)
TTS_SYNC_MAX_CHARS = 2000


# =============================================================================
# Utility Functions
# =============================================================================

def get_cos_bucket():
    """Get COS bucket name from environment variable."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """Get COS bucket region from environment variable."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def get_credentials():
    """Get Tencent Cloud credentials from environment variables."""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        print("❌ TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY not found", file=sys.stderr)
        print("   Please configure them in ~/.env or <SKILL_DIR>/.env and retry", file=sys.stderr)
        if _LOAD_ENV_AVAILABLE:
            from mps_load_env import _print_setup_hint
            _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
        sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def create_mps_client(cred, region):
    """Create an MPS client."""
    http_profile = HttpProfile()
    http_profile.endpoint = MPS_ENDPOINT
    http_profile.reqMethod = "POST"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return mps_client.MpsClient(cred, region or "", client_profile)


def load_audio_base64(audio_file):
    """Read a local audio file and encode it as base64."""
    if not os.path.isfile(audio_file):
        print(f"❌ Audio file not found: {audio_file}", file=sys.stderr)
        sys.exit(1)
    with open(audio_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")


def _ensure_wav_ext(path):
    """Append .wav extension if the path does not end with it."""
    if not path.lower().endswith(".wav"):
        path = path + ".wav"
    return path


def _truncate_audio_data(d):
    """Truncate AudioData field in a dict to avoid flooding output with base64 content."""
    return {
        k: (v[:40] + "...(truncated)" if k == "AudioData" and isinstance(v, str) and len(v) > 40 else v)
        for k, v in d.items()
    }


def save_audio_output(audio_base64, output_path):
    """Decode base64-encoded WAV audio and save to a local file."""
    output_path = _ensure_wav_ext(output_path)
    audio_bytes = base64.b64decode(audio_base64)
    # Simple validation: WAV header starts with RIFF....WAVE
    if len(audio_bytes) >= 12 and audio_bytes[:4] == b"RIFF" and audio_bytes[8:12] == b"WAVE":
        fmt = "WAV"
    else:
        fmt = "unknown"
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    size_kb = len(audio_bytes) / 1024
    print(f"✅ Audio saved to: {output_path}  [{fmt}, {size_kb:.1f} KB]")
    return output_path


def download_audio_from_url(url, output_path):
    """Download audio from a URL and save to a local file."""
    output_path = _ensure_wav_ext(output_path)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    print(f"⬇️  Downloading audio from URL...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "mps-syncdubbing/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            audio_bytes = resp.read()
    except Exception as e:
        print(f"❌ Failed to download audio: {e}", file=sys.stderr)
        return None
    if len(audio_bytes) >= 12 and audio_bytes[:4] == b"RIFF" and audio_bytes[8:12] == b"WAVE":
        fmt = "WAV"
    else:
        fmt = "unknown"
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    size_kb = len(audio_bytes) / 1024
    print(f"✅ Audio saved to: {output_path}  [{fmt}, {size_kb:.1f} KB]")
    return output_path


# =============================================================================
# SyncDubbing — Synchronous API (clone / tts)
# =============================================================================

def build_sync_params(args):
    """
    Build request parameters for SyncDubbing.

    Two scenarios:
    - clone:  pass AudioData/AudioUrl to clone voice; returns VoiceId
    - tts:    pass Text + VoiceId to synthesize speech; returns audio
    """
    params = {}

    mode = args.mode

    # ---- Text parameters + VoiceId (tts) ----
    if mode == "tts":
        if not args.text:
            print(f"❌ --mode {mode} requires --text", file=sys.stderr)
            sys.exit(1)
        params["Text"] = args.text
        if args.text_lang:
            params["TextLang"] = args.text_lang

        if not args.voice_id:
            print("❌ --mode tts requires --voice-id", file=sys.stderr)
            sys.exit(1)
        params["VoiceId"] = args.voice_id

    # ---- Cloning audio (clone) ----
    if mode == "clone":
        if args.audio_file:
            params["AudioData"] = load_audio_base64(args.audio_file)
        elif args.audio_url:
            params["AudioUrl"] = args.audio_url
        else:
            print(f"❌ --mode {mode} requires --audio-file or --audio-url", file=sys.stderr)
            sys.exit(1)
        if args.audio_lang:
            params["AudioLang"] = args.audio_lang

    # ---- Extended parameters (synExt / cloneExt) ----
    ext_param = {}
    syn_ext = {}
    clone_ext = {}

    if args.sample_rate is not None:
        if args.sample_rate not in SUPPORTED_SAMPLE_RATES:
            print(f"❌ Unsupported sample rate {args.sample_rate}. Supported: {SUPPORTED_SAMPLE_RATES}", file=sys.stderr)
            sys.exit(1)
        syn_ext["sampleRate"] = args.sample_rate

    if args.pitch is not None:
        if not (-12 <= args.pitch <= 12):
            print(f"❌ Pitch must be in range [-12, 12], got: {args.pitch}", file=sys.stderr)
            sys.exit(1)
        syn_ext["pitch"] = args.pitch

    if args.duration is not None:
        if args.duration <= 0:
            print(f"❌ Duration must be greater than 0", file=sys.stderr)
            sys.exit(1)
        syn_ext["duration"] = args.duration

    if args.time_ranges:
        ranges = []
        for tr in args.time_ranges:
            parts = tr.split(",")
            if len(parts) != 2:
                print(f"❌ Invalid time range format '{tr}', expected start,end (seconds, e.g. 5.2,20)", file=sys.stderr)
                sys.exit(1)
            try:
                start, end = float(parts[0]), float(parts[1])
            except ValueError:
                print(f"❌ Time range values must be numeric: '{tr}'", file=sys.stderr)
                sys.exit(1)
            ranges.append([start, end])
        clone_ext["timeRanges"] = ranges

    if syn_ext:
        ext_param["synExt"] = syn_ext
    if clone_ext:
        ext_param["cloneExt"] = clone_ext
    if ext_param:
        params["ExtParam"] = json.dumps(ext_param, ensure_ascii=False)

    # ---- Output options ----
    # Default: return base64 audio; set OutputType=URL if --output-url is specified
    if getattr(args, "output_url", False):
        params["Output"] = {"OutputType": "URL"}

    # ---- Resource ID ----
    if getattr(args, "resource_id", None):
        params["ResourceId"] = args.resource_id

    return params


def run_sync_dubbing(args):
    """Execute synchronous dubbing/cloning task (SyncDubbing API)."""
    region = getattr(args, "region", None) or os.environ.get("TENCENTCLOUD_API_REGION", "")

    cred = get_credentials()
    client = create_mps_client(cred, region)

    params = build_sync_params(args)

    if args.dry_run:
        print("=" * 60)
        print("[Dry Run] Printing request parameters only — API not called")
        print("=" * 60)
        print(json.dumps(_truncate_audio_data(params), ensure_ascii=False, indent=2))
        return

    if args.verbose:
        print("Request parameters:")
        print(json.dumps(_truncate_audio_data(params), ensure_ascii=False, indent=2))
        print()

    try:
        req = models.SyncDubbingRequest()
        req.from_json_string(json.dumps(params))

        resp = client.SyncDubbing(req)
        result = json.loads(resp.to_json_string())

        error_code = result.get("ErrorCode", -1)
        msg = result.get("Msg", "")
        request_id = result.get("RequestId", "N/A")

        if error_code != 0:
            print(f"❌ API returned error [{error_code}]: {msg}", file=sys.stderr)
            if args.verbose:
                print("Full response:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(1)

        print("✅ Task completed!")
        print(f"   RequestId: {request_id}")

        mode = args.mode

        # Output VoiceId
        voice_id = result.get("VoiceId")
        if voice_id:
            print(f"   VoiceId: {voice_id}")

        # Output audio duration (ExtInfo)
        ext_info_str = result.get("ExtInfo")
        if ext_info_str:
            try:
                ext_info = json.loads(ext_info_str)
                if isinstance(ext_info, dict):
                    duration = ext_info.get("duration")
                    if duration is not None:
                        print(f"   Audio duration: {duration:.3f}s")
            except (json.JSONDecodeError, TypeError):
                pass

        # Determine local output path
        output_path = getattr(args, "output", None)
        if not output_path:
            output_path = _auto_output_name(args)

        # Save synthesized audio (clone mode does not produce audio)
        if mode != "clone":
            audio_data = result.get("AudioData")
            audio_url = result.get("AudioUrl")

            if audio_data:
                # Prefer writing from base64 data directly (no network request)
                save_audio_output(audio_data, output_path)
            elif audio_url:
                # API returned URL (--output-url was used, or server chose URL output)
                print(f"   AudioUrl: {audio_url}")
                download_audio_from_url(audio_url, output_path)
            else:
                print("⚠️  Response contains no AudioData / AudioUrl — cannot save audio", file=sys.stderr)
        else:
            # clone mode: print AudioUrl only (if present)
            audio_url = result.get("AudioUrl")
            if audio_url:
                print(f"   AudioUrl: {audio_url}")

        if args.verbose:
            print("\nFull response:")
            print(json.dumps(_truncate_audio_data(result), ensure_ascii=False, indent=2))

        return result

    except TencentCloudSDKException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def _auto_output_name(args):
    """Auto-generate an output filename based on the mode."""
    ts = int(time.time())
    mode = args.mode
    if mode == "tts":
        name = f"tts_{ts}.wav"
    else:
        name = f"dubbing_{ts}.wav"
    return name


# =============================================================================
# Async API — Long text (async-tts / async-sts, ProcessMedia API)
# =============================================================================

def build_async_input_info(args):
    """
    Build async task input information.

    async-tts mode: InputInfo can be any accessible media URL (not billed by duration);
                    use a placeholder URL if no real input exists.
    async-sts mode: InputInfo must be the real audio/video to replace the voice in.
    """
    mode = args.mode

    if mode == "async-tts":
        # TextToSpeech mode: InputInfo is a placeholder — any accessible URL works
        url = getattr(args, "url", None) or getattr(args, "placeholder_url", None)
        if not url:
            # Fallback to a public COS test resource
            url = "https://mps-1300828900.cos.ap-guangzhou.myqcloud.com/test/silent_1s.mp4"
        return {"Type": "URL", "UrlInputInfo": {"Url": url}}

    # async-sts mode: real input source
    if args.url:
        return {"Type": "URL", "UrlInputInfo": {"Url": args.url}}

    cos_input_key = getattr(args, "cos_input_key", None)
    if cos_input_key:
        bucket = getattr(args, "cos_input_bucket", None) or get_cos_bucket()
        region = getattr(args, "cos_input_region", None) or get_cos_region()
        if not bucket:
            print("❌ COS input requires a bucket. Set --cos-input-bucket or TENCENTCLOUD_COS_BUCKET",
                  file=sys.stderr)
            sys.exit(1)
        return {
            "Type": "COS",
            "CosInputInfo": {
                "Bucket": bucket,
                "Region": region,
                "Object": cos_input_key if cos_input_key.startswith("/") else f"/{cos_input_key}",
            },
        }

    print("❌ async-sts mode requires an input source: --url or --cos-input-key", file=sys.stderr)
    sys.exit(1)


def build_async_extended_param(args):
    """
    Build the ExtendedParameter JSON string.

    TextToSpeech:
      {"dubbing": {"dubbingType": "TextToSpeech", "text": "...", "voiceId": "...", ...}}

    SpeechToSpeech:
      {"dubbing": {"dubbingType": "SpeechToSpeech", "cloneVideoUrl": "...", "voiceId": "...", ...}}
    """
    mode = args.mode
    dubbing = {}

    if mode == "async-tts":
        dubbing["dubbingType"] = "TextToSpeech"

        if not args.text:
            print("❌ --mode async-tts requires --text", file=sys.stderr)
            sys.exit(1)
        dubbing["text"] = args.text

        if args.text_lang:
            dubbing["textLang"] = args.text_lang
        if args.voice_id:
            dubbing["voiceId"] = args.voice_id
        if getattr(args, "clone_video_url", None):
            dubbing["cloneVideoUrl"] = args.clone_video_url
        if getattr(args, "clone_video_lang", None):
            dubbing["cloneVideoLang"] = args.clone_video_lang
        if getattr(args, "output_pattern", None):
            dubbing["outputPattern"] = args.output_pattern

    elif mode == "async-sts":
        dubbing["dubbingType"] = "SpeechToSpeech"

        if not args.voice_id and not getattr(args, "clone_video_url", None):
            print("❌ --mode async-sts requires --voice-id or --clone-video-url", file=sys.stderr)
            sys.exit(1)

        if args.voice_id:
            dubbing["voiceId"] = args.voice_id
        if getattr(args, "clone_video_url", None):
            dubbing["cloneVideoUrl"] = args.clone_video_url
        if getattr(args, "clone_video_lang", None):
            dubbing["cloneVideoLang"] = args.clone_video_lang
        if getattr(args, "src_lang", None):
            dubbing["srcLang"] = args.src_lang
        if getattr(args, "output_pattern", None):
            dubbing["outputPattern"] = args.output_pattern

    # extraPara.synExt (shared by both async modes)
    syn_ext = {}
    if args.pitch is not None:
        syn_ext["pitch"] = args.pitch
    if mode == "async-tts" and args.sample_rate is not None:
        if args.sample_rate not in SUPPORTED_SAMPLE_RATES:
            print(f"❌ Unsupported sample rate {args.sample_rate}. Supported: {SUPPORTED_SAMPLE_RATES}", file=sys.stderr)
            sys.exit(1)
        syn_ext["sampleRate"] = args.sample_rate
    if syn_ext:
        dubbing["extraPara"] = {"synExt": syn_ext}

    ext_param_obj = {"dubbing": dubbing}
    return json.dumps(ext_param_obj, ensure_ascii=False)


def build_async_output_storage(args):
    """Build async task output storage configuration."""
    bucket = getattr(args, "output_bucket", None) or get_cos_bucket()
    region = getattr(args, "output_region", None) or get_cos_region()

    if not bucket:
        print("❌ Async mode requires an output COS bucket (--output-bucket or TENCENTCLOUD_COS_BUCKET)",
              file=sys.stderr)
        sys.exit(1)
    return {
        "Type": "COS",
        "CosOutputStorage": {
            "Bucket": bucket,
            "Region": region,
        },
    }


def build_async_request_params(args):
    """Build the complete ProcessMedia request parameters."""
    params = {}

    # Input
    params["InputInfo"] = build_async_input_info(args)

    # Output storage
    params["OutputStorage"] = build_async_output_storage(args)

    # Output directory (API requires trailing slash)
    output_dir = getattr(args, "output_dir", None) or "/output/dubbing/"
    if not output_dir.endswith("/"):
        output_dir += "/"
    params["OutputDir"] = output_dir

    # AI analysis task (voice synthesis, Definition=36)
    extended_param = build_async_extended_param(args)
    params["AiAnalysisTask"] = {
        "Definition": ASYNC_DUBBING_DEFINITION,
        "ExtendedParameter": extended_param,
    }

    # Callback configuration
    notify_url = getattr(args, "notify_url", None)
    if notify_url:
        params["TaskNotifyConfig"] = {
            "NotifyType": "URL",
            "NotifyUrl": notify_url,
        }

    return params


def run_async_dubbing(args):
    """Execute async TTS/STS task (ProcessMedia API)."""
    region = getattr(args, "region", None) or os.environ.get("TENCENTCLOUD_API_REGION", "")

    cred = get_credentials()
    client = create_mps_client(cred, region)

    params = build_async_request_params(args)

    if args.dry_run:
        print("=" * 60)
        print("[Dry Run] Printing request parameters only — API not called")
        print("=" * 60)
        print(json.dumps(params, ensure_ascii=False, indent=2))
        return

    if args.verbose:
        print("Request parameters:")
        print(json.dumps(params, ensure_ascii=False, indent=2))
        print()

    try:
        req = models.ProcessMediaRequest()
        req.from_json_string(json.dumps(params))

        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get("TaskId", "N/A")
        print("✅ Async task submitted successfully!")
        print(f"## TaskId: {task_id}")
        print(f"   RequestId: {result.get('RequestId', 'N/A')}")

        mode = args.mode
        mode_desc = MODES.get(mode, mode)
        print(f"   Mode: {mode_desc}")

        extended_param = params.get("AiAnalysisTask", {}).get("ExtendedParameter", "")
        if extended_param and args.verbose:
            print(f"   ExtendedParameter: {extended_param}")

        out_storage = params.get("OutputStorage", {}).get("CosOutputStorage", {})
        out_dir = params.get("OutputDir", "")
        if out_storage:
            print(f"   Output: COS - {out_storage.get('Bucket')}:{out_dir} "
                  f"(region: {out_storage.get('Region')})")

        if args.verbose:
            print("\nFull response:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        # Auto-poll (unless --no-wait is specified)
        no_wait = getattr(args, "no_wait", False)
        if not no_wait and _POLL_AVAILABLE and task_id != "N/A":
            poll_interval = getattr(args, "poll_interval", 10)
            max_wait = getattr(args, "max_wait", 3600)
            task_result = poll_video_task(task_id, region=region, interval=poll_interval,
                                         max_wait=max_wait, verbose=args.verbose)
            # Auto-download
            download_dir = getattr(args, "download_dir", None)
            if download_dir and task_result and _POLL_AVAILABLE:
                auto_download_outputs(task_result, download_dir=download_dir)
        else:
            print(f"\nNote: Task is processing in the background. Query status with:")
            print(f"  python scripts/mps_get_video_task.py --task-id {task_id}")

        return result

    except TencentCloudSDKException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)


# =============================================================================
# Entry Point
# =============================================================================

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Voice Synthesis & Voice Cloning — ideal for audiobooks, podcasts, dubbing; 40+ languages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes (--mode):
  clone       Voice cloning (sync) — returns VoiceId
  tts         TTS — returns WAV audio (≤2000 chars uses sync; longer auto-switches to async)
  async-tts   Long-text TTS (async) — TextToSpeech, output to COS
  async-sts   Speech-to-speech (async) — SpeechToSpeech, replace voice, output to COS

⚡ Auto mode upgrade: in tts mode, if text exceeds 2000 characters, the script
   automatically switches to async-tts — no need to manually specify --mode async-tts.

Examples:
  # Voice cloning (local audio, recommended 10–20s clear single-speaker audio)
  python mps_dubbing.py --mode clone --audio-file /path/to/voice.wav

  # Voice cloning (audio URL)
  python mps_dubbing.py --mode clone --audio-url https://example.com/voice.mp4

  # Short-text TTS (system voice ID)
  python mps_dubbing.py --mode tts --text "Hello, welcome to Tencent Cloud!" --voice-id s1_2GSzVAf00hl

  # Short-text TTS (custom sample rate + pitch + output file)
  python mps_dubbing.py --mode tts --text "Hello!" --voice-id s1_xxx \\
      --sample-rate 44100 --pitch 2 --output /tmp/out.wav

  # Clone + TTS workflow
  python mps_dubbing.py --mode clone --audio-file voice.wav
  python mps_dubbing.py --mode tts --text "Hello" --voice-id <VoiceId from previous step>

  # Long-text TTS (async, specify voice ID)
  python mps_dubbing.py --mode async-tts \\
      --text "A very long text exceeding 2000 characters..." --voice-id clone_v1_Q03FBduA

  # Long-text TTS (async, clone from video URL)
  python mps_dubbing.py --mode async-tts \\
      --text "Long text..." --clone-video-url https://example.com/train.mp4

  # Speech-to-speech (async, replace voice)
  python mps_dubbing.py --mode async-sts \\
      --url https://example.com/video.mp4 \\
      --clone-video-url https://example.com/train.mp4

  # Speech-to-speech (async, use specified voice ID)
  python mps_dubbing.py --mode async-sts \\
      --url https://example.com/video.mp4 --voice-id s1_2GSzVAf00hl

  # Dry Run
  python mps_dubbing.py --mode tts --text "Hello" --voice-id s1_xxx --dry-run

Supported languages (--text-lang / --audio-lang / --src-lang / --clone-video-lang):
  zh=Chinese  en=English  ja=Japanese  ko=Korean  de=German  fr=French
  es=Spanish  it=Italian  ru=Russian  pt=Portuguese  ar=Arabic  hi=Hindi
  th=Thai  vi=Vietnamese  ...  (40+ total)

Environment Variables:
  TENCENTCLOUD_SECRET_ID   Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET  COS bucket name (required for async modes)
  TENCENTCLOUD_COS_REGION  COS bucket region (required for async modes)
        """
    )

    # ---- Mode ----
    parser.add_argument(
        "--mode", type=str, required=True, choices=list(MODES.keys()),
        metavar="MODE",
        help=(
            "Operation mode (required): "
            "clone=voice cloning | "
            "tts=speech synthesis | "
            "async-tts=long-text TTS | "
            "async-sts=speech-to-speech"
        )
    )

    # ---- Text parameters ----
    text_group = parser.add_argument_group("Text parameters (tts / async-tts modes)")
    text_group.add_argument("--text", type=str,
                            help="Text to synthesize. tts mode: ≤2000 chars uses sync API; "
                                 "longer text auto-switches to async (no need to specify async-tts manually)")
    text_group.add_argument(
        "--text-lang", type=str, metavar="LANG",
        choices=list(SUPPORTED_LANGS.keys()),
        help="Text language (default: zh). E.g. en/ja/ko/fr/de/..."
    )

    # ---- Voice parameters ----
    voice_group = parser.add_argument_group("Voice parameters")
    voice_group.add_argument("--voice-id", type=str,
                             help="Voice ID (system voice or cloned voice). Used by tts/async-tts/async-sts modes")

    # ---- Clone audio parameters ----
    clone_group = parser.add_argument_group("Clone audio parameters (clone mode only)")
    clone_group.add_argument("--audio-file", type=str,
                             help="Local cloning audio file (WAV/MP3/MP4 etc.). Recommended: 10–20s, single speaker, clear voice")
    clone_group.add_argument("--audio-url", type=str,
                             help="Cloning audio URL (used when --audio-file is not specified)")
    clone_group.add_argument(
        "--audio-lang", type=str, metavar="LANG",
        choices=list(SUPPORTED_LANGS.keys()),
        help="Cloning audio language (default: zh)"
    )
    clone_group.add_argument("--time-ranges", type=str, action="append",
                             metavar="START,END",
                             help="Time range(s) for cloning audio (seconds, e.g. 5.2,20). Can be specified multiple times")

    # ---- Async clone video parameters ----
    async_clone_group = parser.add_argument_group("Async mode clone video parameters (async-tts / async-sts)")
    async_clone_group.add_argument("--clone-video-url", type=str,
                                   help="Video/audio URL to clone voice from (min 5 seconds, single speaker)")
    async_clone_group.add_argument(
        "--clone-video-lang", type=str, metavar="LANG",
        choices=list(SUPPORTED_LANGS.keys()),
        help="Language of the clone video/audio (default: zh)"
    )
    async_clone_group.add_argument(
        "--src-lang", type=str, metavar="LANG",
        choices=list(SUPPORTED_LANGS.keys()),
        help="Language of the source video/audio (async-sts mode)"
    )

    # ---- Async task input source ----
    input_group = parser.add_argument_group("Async task input source (async-tts / async-sts)")
    input_group.add_argument("--url", type=str,
                             help="Input video/audio URL. "
                                  "async-tts: any accessible URL (acts as placeholder); async-sts: required real input")
    input_group.add_argument("--cos-input-bucket", type=str,
                             help="Input COS bucket name (used with --cos-input-key)")
    input_group.add_argument("--cos-input-region", type=str,
                             help="Input COS bucket region")
    input_group.add_argument("--cos-input-key", type=str,
                             help="Input COS object key (e.g. /input/video.mp4)")

    # ---- Audio quality parameters ----
    quality_group = parser.add_argument_group("Audio quality parameters (optional)")
    quality_group.add_argument("--sample-rate", type=int,
                               metavar="RATE",
                               choices=SUPPORTED_SAMPLE_RATES,
                               help=f"Output audio sample rate. Supported: {SUPPORTED_SAMPLE_RATES} (default: 16000)")
    quality_group.add_argument("--pitch", type=int,
                               metavar="[-12,12]",
                               help="Pitch adjustment, range [-12, 12], default 0 (original)")
    quality_group.add_argument("--duration", type=float,
                               help="Target audio duration in seconds (e.g. 5.2). Sync mode only")

    # ---- Async task output configuration ----
    output_group = parser.add_argument_group("Async task output configuration (async-tts / async-sts)")
    output_group.add_argument("--output-bucket", type=str,
                              help="Output COS bucket (default: TENCENTCLOUD_COS_BUCKET env var)")
    output_group.add_argument("--output-region", type=str,
                              help="Output COS bucket region (default: TENCENTCLOUD_COS_REGION env var)")
    output_group.add_argument("--output-dir", type=str,
                              help="Output directory (default: /output/dubbing/), must start and end with /")
    output_group.add_argument("--output-pattern", type=str,
                              help="Output filename prefix; supports placeholders {taskType}, {timestamp}")

    # ---- Sync task output ----
    sync_output_group = parser.add_argument_group("Sync task output (clone / tts)")
    sync_output_group.add_argument("--output", "-o", type=str,
                                   help="Local path to save synthesized audio (e.g. /tmp/output.wav). "
                                        "Auto-generated filename if not specified")
    sync_output_group.add_argument("--output-url", action="store_true",
                                   help="Request the API to return an audio URL (valid 24h) instead of base64 data")

    # ---- Other configuration ----
    other_group = parser.add_argument_group("Other configuration")
    other_group.add_argument("--region", type=str,
                             help="MPS service region (not required for sync API; recommended for async)")
    other_group.add_argument("--resource-id", type=str,
                             help="Resource ID (defaults to the account's primary resource ID)")
    other_group.add_argument("--notify-url", type=str,
                             help="Callback URL for async task completion")
    other_group.add_argument("--no-wait", action="store_true",
                             help="Submit async task only, do not wait for result (default: auto-poll until done)")
    other_group.add_argument("--poll-interval", type=int, default=10,
                             help="Polling interval in seconds (default: 10)")
    other_group.add_argument("--max-wait", type=int, default=3600,
                             help="Maximum wait time in seconds (default: 3600 = 1 hour)")
    other_group.add_argument("--download-dir", type=str, default=None,
                             help="Auto-download results to this local directory when async task completes")
    other_group.add_argument("--verbose", "-v", action="store_true",
                             help="Output verbose information")
    other_group.add_argument("--dry-run", action="store_true",
                             help="Print request parameters only, do not call the API")

    args = parser.parse_args()

    # Load environment variables from .env file if available
    if _LOAD_ENV_AVAILABLE:
        _ensure_env_loaded()

    # ---- Validation ----
    mode = args.mode

    # ---- Auto-detect: switch to async if text exceeds limit ----
    # SyncDubbing max text length is TTS_SYNC_MAX_CHARS; auto-switch to async if exceeded.
    _auto_upgraded = False
    _orig_mode = None
    _text_len = None
    if mode == "tts" and args.text:
        _text_len = len(args.text)
        if _text_len > TTS_SYNC_MAX_CHARS:
            _orig_mode = mode
            _auto_upgraded = True
            mode = "async-tts"
            args.mode = mode

    # Sync modes cannot use async-only parameters
    if mode in ("clone", "tts"):
        async_only = [
            (getattr(args, "clone_video_url", None), "--clone-video-url"),
            (getattr(args, "clone_video_lang", None), "--clone-video-lang"),
            (getattr(args, "src_lang", None), "--src-lang"),
            (getattr(args, "output_bucket", None), "--output-bucket"),
            (getattr(args, "output_dir", None), "--output-dir"),
            (getattr(args, "output_pattern", None), "--output-pattern"),
            (getattr(args, "notify_url", None), "--notify-url"),
            (getattr(args, "no_wait", False) and True, "--no-wait"),
            (getattr(args, "download_dir", None), "--download-dir"),
        ]
        used = [name for val, name in async_only if val]
        if used:
            parser.error(f"Parameter(s) {', '.join(used)} are only supported in async modes (async-tts / async-sts)")

    # async-tts requires --text
    if mode == "async-tts" and not args.text:
        parser.error("--mode async-tts requires --text")

    # async-sts requires --voice-id or --clone-video-url
    if mode == "async-sts":
        if not args.voice_id and not getattr(args, "clone_video_url", None):
            parser.error("--mode async-sts requires --voice-id or --clone-video-url")

    # tts requires --text and --voice-id
    if mode == "tts" and not args.text:
        parser.error("--mode tts requires --text")
    if mode == "tts" and not args.voice_id:
        parser.error("--mode tts requires --voice-id")

    # clone requires --audio-file or --audio-url
    if mode == "clone":
        if not args.audio_file and not args.audio_url:
            parser.error("--mode clone requires --audio-file or --audio-url")

    # Print execution info
    print("=" * 60)
    if _auto_upgraded:
        print(f"⚡ Auto-detected: text is {_text_len} chars > sync limit {TTS_SYNC_MAX_CHARS}")
        print(f"   Auto-switched: {_orig_mode} (sync) → async-tts (async TextToSpeech)")
    print(f"Tencent Cloud MPS Voice Synthesis & Cloning — {MODES.get(mode, mode)}")
    print("=" * 60)

    if mode in ("clone", "tts"):
        if mode == "tts":
            text_preview = (args.text[:30] + "...") if args.text and len(args.text) > 30 else args.text
            print(f"Text: {text_preview}")
        if args.voice_id:
            print(f"Voice ID: {args.voice_id}")
        if args.audio_file:
            print(f"Clone audio: {args.audio_file}")
        elif args.audio_url:
            print(f"Clone audio: {args.audio_url}")
    else:
        if args.url:
            print(f"Input: {args.url}")
        elif getattr(args, "cos_input_key", None):
            bucket = getattr(args, "cos_input_bucket", None) or get_cos_bucket()
            print(f"Input: COS - {bucket}:{args.cos_input_key}")
        if args.text:
            text_preview = (args.text[:50] + "...") if len(args.text) > 50 else args.text
            print(f"Text: {text_preview}")
        if args.voice_id:
            print(f"Voice ID: {args.voice_id}")
        if getattr(args, "clone_video_url", None):
            print(f"Clone video: {args.clone_video_url}")
        out_bucket = getattr(args, "output_bucket", None) or get_cos_bucket() or "not set"
        out_dir = getattr(args, "output_dir", None) or "/output/dubbing/"
        print(f"Output: COS - {out_bucket}:{out_dir}")

        # Async mode: check COS bucket
        if not get_cos_bucket() and not getattr(args, "output_bucket", None) and not args.dry_run:
            print("❌ TENCENTCLOUD_COS_BUCKET is not set. Please configure it and retry.", file=sys.stderr)
            sys.exit(1)

    print("-" * 60)

    # ---- Execute ----
    if mode in ("clone", "tts"):
        run_sync_dubbing(args)
    else:
        run_async_dubbing(args)


if __name__ == "__main__":
    main()
