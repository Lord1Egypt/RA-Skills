#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD AIGC Audio Generation Task Script
Uses the CreateAigcAudioTask API to create AIGC audio generation tasks.
Supported capabilities:
  - Text-to-sound-effect / Video-to-sound-effect (Kling, SceneType=sfx)
  - Text-to-music (MiniMaxMusic / GL(Google Lyria), SceneType=music)
"""

import os
import sys
import json
import argparse
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vod_auto_upgrade import check_sdk_version

# Soft dependency: vod_load_env, used to fall back to loading from ~/.env or other dotenv files when credentials are missing
try:
    from vod_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False

check_sdk_version()

try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.vod.v20180717 import vod_client, models
except ImportError:
    print("Error: please install the Tencent Cloud SDK first: python3 -m pip install tencentcloud-sdk-python")
    sys.exit(1)

def get_credential():
    """Get Tencent Cloud credentials. Falls back to loading from a dotenv file if env vars are missing."""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        # Fallback: try to load from ~/.env or other dotenv files
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] Environment variables not set, trying to auto-load from a dotenv file...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    # Check all required variables (SECRET_ID/KEY/SUB_APP_ID)
    if _LOAD_ENV_AVAILABLE:
        from vod_load_env import check_required_vars, _print_setup_hint
        missing = check_required_vars()
        if missing:
            _print_setup_hint(missing)
            sys.exit(1)
    elif not secret_id or not secret_key:
        print("Error: please set the TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY environment variables", file=sys.stderr)
        sys.exit(1)

    return credential.Credential(secret_id, secret_key)

def get_client(region="ap-guangzhou"):
    """Get the VOD client"""
    cred = get_credential()
    http_profile = HttpProfile()
    http_profile.endpoint = "vod.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return vod_client.VodClient(cred, region, client_profile)

# ── Model/scene mapping (doc 3.13.1 model overview) ──────────────────────────
# Module              ModelName        ModelVersion            SceneType
# Text-to-sfx         Kling            empty (unset)           sfx
# Video-to-sfx        Kling            empty (unset)           sfx
# Text-to-music       MiniMaxMusic     2.0/2.5/2.6/3.0          music
# Text-to-music       GL               3.0-clip/3.0-pro         music
MODEL_VERSIONS = {
    "Kling": [],  # Leave ModelVersion unset to use the system's default stable version
    "MiniMaxMusic": ["2.0", "2.5", "2.6", "3.0"],
    "GL": ["3.0-clip", "3.0-pro"],
}

# Valid SceneType per model (used for validation, to avoid an API error from a wrong scene)
MODEL_SCENE_TYPES = {
    "Kling": ["sfx"],
    "MiniMaxMusic": ["music"],
    "GL": ["music"],
}

def validate_model_scene(args):
    """Validate the ModelName/SceneType combination (doc 3.13.1 model overview)."""
    if not args.model:
        return
    valid_scenes = MODEL_SCENE_TYPES.get(args.model)
    if valid_scenes is None:
        return
    if args.scene_type and args.scene_type not in valid_scenes:
        print(f"Error: model {args.model} does not support scene {args.scene_type}, "
              f"available scenes: {valid_scenes}")
        sys.exit(1)
    if args.model in ("MiniMaxMusic", "GL") and args.model_version:
        allowed = MODEL_VERSIONS.get(args.model, [])
        if allowed and args.model_version not in allowed:
            print(f"Error: model {args.model} does not support version {args.model_version}, "
                  f"available versions: {allowed}")
            sys.exit(1)
    if args.model == "Kling" and args.model_version:
        print("Note: for Kling sound-effect/music scenes, ModelVersion is recommended to be left unset "
              "(uses the system's default stable version), as shown empty in the doc examples")

def create_audio_task(args):
    """Create an AIGC audio generation task (CreateAigcAudioTask)"""
    client = get_client(args.region)

    validate_model_scene(args)

    req = models.CreateAigcAudioTaskRequest()

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id

    if args.model:
        req.ModelName = args.model
    if args.model_version:
        req.ModelVersion = args.model_version
    if args.scene_type:
        req.SceneType = args.scene_type
    if args.prompt:
        req.Prompt = args.prompt

    # Reference video info (VideoInfos, used in the video-to-sound-effect scenario)
    if args.video_id or args.video_url:
        video_info = models.AigcAudioReferenceVideoInfo()
        if args.video_id:
            video_info.Type = "File"
            video_info.FileId = args.video_id
        elif args.video_url:
            video_info.Type = "Url"
            video_info.Url = args.video_url
        req.VideoInfos = [video_info]
    elif args.video_infos:
        try:
            video_infos_data = json.loads(args.video_infos)
            video_infos = []
            for vi in video_infos_data:
                video_info = models.AigcAudioReferenceVideoInfo()
                video_info.Type = vi.get("Type", "Url")
                if vi.get("FileId"):
                    video_info.FileId = vi["FileId"]
                if vi.get("Url"):
                    video_info.Url = vi["Url"]
                video_infos.append(video_info)
            req.VideoInfos = video_infos
        except json.JSONDecodeError as e:
            print(f"Error: --video-infos parameter has invalid JSON format: {e}")
            sys.exit(1)

    # Reference audio info (AudioInfos, used e.g. when generating music from an input audio)
    if args.audio_id or args.audio_url:
        audio_info = models.AigcAudioReferenceAudioInfo()
        if args.audio_id:
            audio_info.Type = "File"
            audio_info.FileId = args.audio_id
        elif args.audio_url:
            audio_info.Type = "Url"
            audio_info.Url = args.audio_url
        req.AudioInfos = [audio_info]
    elif args.audio_infos:
        try:
            audio_infos_data = json.loads(args.audio_infos)
            audio_infos = []
            for ai in audio_infos_data:
                audio_info = models.AigcAudioReferenceAudioInfo()
                audio_info.Type = ai.get("Type", "Url")
                if ai.get("FileId"):
                    audio_info.FileId = ai["FileId"]
                if ai.get("Url"):
                    audio_info.Url = ai["Url"]
                audio_infos.append(audio_info)
            req.AudioInfos = audio_infos
        except json.JSONDecodeError as e:
            print(f"Error: --audio-infos parameter has invalid JSON format: {e}")
            sys.exit(1)

    # Output config (OutputConfig)
    if any([args.output_storage_mode, args.output_media_name, args.output_class_id,
            args.output_expire_time, args.output_duration is not None, args.output_audio_format]):
        output_config = models.AigcAudioOutputConfig()
        if args.output_storage_mode:
            output_config.StorageMode = args.output_storage_mode
        if args.output_media_name:
            output_config.MediaName = args.output_media_name
        if args.output_class_id is not None:
            output_config.ClassId = args.output_class_id
        if args.output_expire_time:
            output_config.ExpireTime = args.output_expire_time
        if args.output_duration is not None:
            output_config.Duration = args.output_duration
        if args.output_audio_format:
            output_config.OutputAudioFormat = args.output_audio_format
        req.OutputConfig = output_config

    # Build AdditionalParameters
    # Priority: --bgm-prompt/--asmr-mode/--lyrics (dedicated convenience params, merged into the same JSON)
    #           > --additional-parameters (raw JSON passed through by the user, merged in; dedicated params take precedence)
    additional = {}
    if args.additional_parameters:
        try:
            additional.update(json.loads(args.additional_parameters))
        except json.JSONDecodeError as e:
            print(f"Error: --additional-parameters parameter has invalid JSON format: {e}")
            sys.exit(1)
    if args.bgm_prompt:
        additional["bgm_prompt"] = args.bgm_prompt
    if args.asmr_mode:
        additional["asmr_mode"] = args.asmr_mode == "true"
    if args.lyrics:
        additional["lyrics"] = args.lyrics

    if additional:
        req.AdditionalParameters = json.dumps(additional, ensure_ascii=False)

    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return

    try:
        resp = client.CreateAigcAudioTask(req)
        result = json.loads(resp.to_json_string())

        print("AIGC audio generation task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), the task is still running")
                print(f"📋 You can check it later: python3 scripts/vod_describe_task.py --task-id {result['TaskId']}")
            else:
                print_task_outputs(wait_result)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"Failed to create audio generation task: {e}")
        sys.exit(1)

def print_task_outputs(result):
    """Extract and print output artifacts (audio/video URL or FileId) from the task result.

    Compatible with two response shapes:
    - The root object returned by DescribeTaskDetail (containing an AigcAudioTask sub-object)
    - An already-unwrapped AigcAudioTask object
    """
    if not result:
        return
    task = result.get('AigcAudioTask') or result
    output = task.get('Output') or {}
    audio_infos = output.get('AudioInfos') or []
    video_infos = output.get('VideoInfos') or []

    if not audio_infos and not video_infos:
        err_msg = task.get('Message') or task.get('ErrCodeExt')
        if err_msg:
            print(f"⚠️  Error message: {err_msg}")
        return

    if audio_infos:
        print(f"\n🎵 Audio output ({len(audio_infos)} file(s)):")
        for i, fi in enumerate(audio_infos, 1):
            _print_output_file_info(fi, i, len(audio_infos))

    if video_infos:
        print(f"\n🎬 Video output ({len(video_infos)} file(s)):")
        for i, fi in enumerate(video_infos, 1):
            _print_output_file_info(fi, i, len(video_infos))

def _print_output_file_info(fi, index, total):
    """Print a single output file's info (FileUrl/FileId/Duration)."""
    url = fi.get('FileUrl') or ''
    fid = fi.get('FileId') or ''
    duration = fi.get('Duration')
    prefix = f"  [{index}]" if total > 1 else "  •"
    if fid:
        print(f"{prefix} FileId : {fid}")
        print(f"     URL    : {url}")
    else:
        print(f"{prefix} URL: {url}")
    if duration:
        print(f"     Duration: {duration}s")

def wait_for_task(client, task_id, sub_app_id=None, max_wait=600):
    """Wait for the task to complete"""
    print(f"\nWaiting for the task to complete (TaskId: {task_id})...")
    start_time = time.time()

    while time.time() - start_time < max_wait:
        req = models.DescribeTaskDetailRequest()
        req.TaskId = task_id
        if sub_app_id:
            req.SubAppId = sub_app_id

        try:
            resp = client.DescribeTaskDetail(req)
            result = json.loads(resp.to_json_string())

            status = result.get('Status', 'PROCESSING')
            print(f"  Current status: {status}")

            if status == 'FINISH':
                print("Task completed!")
                return result
            elif status == 'FAIL':
                print("Task failed!")
                return result

            time.sleep(5)
        # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
        except Exception as e:
            print(f"Failed to query task status: {e}")
            time.sleep(5)

    print(f"⏱️ Wait timed out ({max_wait}s), the task is still running")
    return None

def list_models(args):
    """List the supported models and scenes"""
    print("Supported models and versions:")
    print("  Kling: leave ModelVersion unset (uses the system's default stable version)")
    print(f"  MiniMaxMusic: versions {MODEL_VERSIONS['MiniMaxMusic']}")
    print(f"  GL: versions {MODEL_VERSIONS['GL']}")
    print("\nSceneType to model mapping:")
    print("  sfx (sound effect, text-to-sfx / video-to-sfx): Kling")
    print("  music (music, text-to-music)                 : MiniMaxMusic, GL")

def main():
    # Load .env first, ensuring env vars are ready before argparse `default=os.environ.get(...)` is evaluated
    if _LOAD_ENV_AVAILABLE:
        try:
            _ensure_env_loaded(verbose=False)
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description='VOD AIGC audio generation task tool (CreateAigcAudioTask)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Text-to-sound-effect (Kling, SceneType=sfx)
  python3 vod_aigc_audio.py create --model Kling --scene-type sfx \\
      --prompt "fireworks sound during Chinese New Year celebration" --output-duration 6 \\
      --output-storage-mode Temporary

  # Video-to-sound-effect (Kling, reference video URL, with BGM + ASMR mode)
  python3 vod_aigc_audio.py create --model Kling --scene-type sfx \\
      --video-url "https://example.com/ref.mp4" \\
      --prompt "gentle wind sound, distant bird calls, occasional footsteps, page turning, rain hitting the window" \\
      --bgm-prompt "healing piano music, soft string accompaniment, warm and soothing melody" \\
      --asmr-mode true \\
      --output-duration 6

  # Text-to-music (MiniMaxMusic, with lyrics)
  python3 vod_aigc_audio.py create --model MiniMaxMusic --model-version 2.0 \\
      --scene-type music --prompt "a joyful song" \\
      --lyrics "the ocean is full of water, the horse has four legs" \\
      --output-audio-format mp3

  # Text-to-music (GL/Google Lyria, style + lyrics need to be concatenated into the prompt)
  python3 vod_aigc_audio.py create --model GL --model-version 3.0-clip \\
      --scene-type music \\
      --prompt "upbeat folk style\\n\\nLyrics:\\nthe ocean is full of water, the horse has four legs" \\
      --output-audio-format mp3

  # List supported models
  python3 vod_aigc_audio.py models

  # Preview request parameters
  python3 vod_aigc_audio.py create --model Kling --scene-type sfx --prompt "test" --dry-run
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='Subcommand')

    # ---- create subcommand ----
    create_parser = subparsers.add_parser('create', help='Create an AIGC audio generation task')

    create_parser.add_argument('--model', choices=list(MODEL_VERSIONS.keys()),
                               help='Model name: Kling (sound effect) / MiniMaxMusic / GL (music)')
    create_parser.add_argument('--model-version',
                               help='Model version; recommended to leave unset for Kling (uses the system default stable version), '
                                    'MiniMaxMusic supports 2.0/2.5/2.6/3.0, GL supports 3.0-clip/3.0-pro')
    create_parser.add_argument('--scene-type', choices=['sfx', 'music'],
                               help='Scene type: sfx (sound effect, Kling) / music (music, MiniMaxMusic/GL)')
    create_parser.add_argument('--prompt', help='Description (prompt) of the audio to generate')

    # Reference video (video-to-sound-effect scenario)
    create_parser.add_argument('--video-id', help='VOD FileId of the reference video (video-to-sound-effect scenario)')
    create_parser.add_argument('--video-url', help='URL of the reference video (video-to-sound-effect scenario)')
    create_parser.add_argument('--video-infos',
                               help='JSON array of multiple reference videos, format: [{"Type":"Url","Url":"..."}]')

    # Reference audio (e.g. generating music from an input audio)
    create_parser.add_argument('--audio-id', help='VOD FileId of the reference audio')
    create_parser.add_argument('--audio-url', help='URL of the reference audio')
    create_parser.add_argument('--audio-infos',
                               help='JSON array of multiple reference audios, format: [{"Type":"Url","Url":"..."}]')

    # AdditionalParameters convenience params (common fields for video-to-sfx/text-to-music)
    create_parser.add_argument('--bgm-prompt', help='BGM generation prompt (video-to-sound-effect scenario, Kling), merged into AdditionalParameters')
    create_parser.add_argument('--asmr-mode', choices=['true', 'false'],
                               help='Whether to enable ASMR mode (enhances detailed sound effects, good for highly immersive content), merged into AdditionalParameters')
    create_parser.add_argument('--lyrics', help='Lyrics content (text-to-music scenario, MiniMaxMusic), merged into AdditionalParameters')
    create_parser.add_argument('--additional-parameters',
                               help='Reserved field, special scenario parameters as a JSON string, e.g. {"camera_control":{"type":"simple"}}; '
                                    'merged with --bgm-prompt/--asmr-mode/--lyrics (the latter take precedence)')

    # Output config
    create_parser.add_argument('--output-storage-mode', choices=['Permanent', 'Temporary'],
                               help='Storage mode: Permanent / Temporary (default)')
    create_parser.add_argument('--output-media-name', help='Output file name, up to 64 characters')
    create_parser.add_argument('--output-class-id', type=int, help='Output file class ID, default 0')
    create_parser.add_argument('--output-expire-time', help='Output file expiration time, ISO 8601 format')
    create_parser.add_argument('--output-duration', type=int,
                               help='Duration of the generated audio (seconds), range [0, 60], unset by default')
    create_parser.add_argument('--output-audio-format', help='Output audio format, e.g. wav, mp3, unset by default')

    create_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                               help='Sub-application ID, required for customers who activated VOD after 2023-12-25')
    create_parser.add_argument('--region', default=os.getenv('TENCENTCLOUD_REGION', 'ap-guangzhou'), help='Region, default ap-guangzhou')
    create_parser.add_argument('--no-wait', action='store_true', help='Only submit the task, do not wait for the result')
    create_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds), default 600')
    create_parser.add_argument('--json', action='store_true', help='Output the full response in JSON format')
    create_parser.add_argument('--dry-run', action='store_true', help='Preview the request parameters without executing')

    # ---- models subcommand ----
    _ = subparsers.add_parser('models', help='List supported models and scenes')

    args = parser.parse_args()

    if args.command == 'create':
        create_audio_task(args)
    elif args.command == 'models':
        list_models(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
