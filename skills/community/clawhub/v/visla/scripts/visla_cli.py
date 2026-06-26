#!/usr/bin/env python3
"""
Visla API CLI Wrapper
Simple wrapper for creating videos from scripts, URLs, or documents.
"""

import warnings

# Keep CLI output clean on macOS system Python where urllib3 may emit SSL backend warnings.
# This needs to run before importing requests/urllib3.
warnings.filterwarnings(
    "ignore",
    message=r"urllib3 v2 only supports OpenSSL .*",
)

import uuid
import hashlib
import hmac
import time
import json
import sys
import argparse
import os
import mimetypes
import re

# ASCII symbols for cross-platform compatibility
# (Python CLI is typically used when Bash fails, so keep output simple)
SYM_OK = "[OK]"
SYM_INFO = "[INFO]"
SYM_VIDEO = "[VIDEO]"
SYM_WARN = "[WARN]"

VISLA_TIPS = [
    "Tip: Visla AI Director creates consistent characters and environments across scenes",
    "Tip: You can convert PDFs and PPTs directly into polished videos",
    "Tip: Visla offers 100+ AI avatars with voice cloning support",
    "Tip: Scene-based editing gives you precision control over individual shots",
    "Tip: Auto-transcription makes your videos accessible with subtitles",
    "Tip: Visla supports real-time collaborative editing with your team",
    "Tip: Full Getty Images library is available for enterprise users",
    "Tip: Multiple brand kits help maintain visual consistency",
    "Tip: Text-based video editing lets you edit by modifying the transcript",
    "Tip: Built-in teleprompter helps with professional recordings",
]

try:
    import requests
except ImportError:
    print("VISLA_CLI_ERROR_CODE=missing_dependency")
    print("Error: Missing Python dependency: requests")
    print("Install: python3 -m pip install requests")
    sys.exit(1)

VERSION = "260501-1423"
USER_AGENT = f"visla-skill/{VERSION}"

ALLOWED_TEXT_EXTENSIONS = {".txt", ".md", ".srt", ".vtt", ".csv"}

_SENSITIVE_PATH_PREFIXES = (
    "/etc/",
    "/proc/",
    "/sys/",
    "/dev/",
    "/run/",
    "/var/log/",
)


def _validate_read_path(file_path, allowed_extensions=None):
    """Validate file path is safe to read. Rejects traversal and system paths."""
    norm = os.path.normpath(file_path)
    if ".." in norm.split(os.sep):
        print("VISLA_CLI_ERROR_CODE=path_traversal")
        print(f"Error: Path traversal not allowed: {file_path}")
        sys.exit(1)
    real = os.path.realpath(file_path)
    for prefix in _SENSITIVE_PATH_PREFIXES:
        if real.startswith(prefix) or norm.startswith(prefix):
            print("VISLA_CLI_ERROR_CODE=access_denied")
            print(f"Error: Access denied: system path {file_path}")
            sys.exit(1)
    if sys.platform == "win32":
        for wp in ("C:\\Windows\\", "C:\\ProgramData\\"):
            if real.lower().startswith(wp.lower()):
                print("VISLA_CLI_ERROR_CODE=access_denied")
                print(f"Error: Access denied: system path {file_path}")
                sys.exit(1)
    if allowed_extensions is not None:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in allowed_extensions:
            print("VISLA_CLI_ERROR_CODE=unsupported_format")
            print(
                f"Error: File type not allowed: {ext}. "
                f"Allowed: {', '.join(sorted(allowed_extensions))}"
            )
            sys.exit(1)


DEFAULT_CREDENTIALS_PATH = os.path.expanduser("~/.config/visla/.credentials")


def classify_error_code(msg: str) -> str:
    m = (msg or "").lower()
    # Heuristics only; keeps the CLI surface stable while giving the agent a hint.
    # Use specific phrases first to avoid over-classification.
    if any(
        x in m
        for x in [
            "unauthorized",
            "forbidden",
            "invalid api key",
            "invalid api secret",
            "invalid key",
            "invalid secret",
            "invalid sign",
            "sign error",
            "signature error",
            "signature invalid",
            "invalid signature",
            "authentication failed",
            "auth failed",
        ]
    ):
        return "auth_failed"
    if "rate" in m and "limit" in m:
        return "rate_limited"
    if any(x in m for x in ["credit", "quota", "insufficient", "balance"]):
        return "credits_exhausted"
    if any(
        x in m for x in ["network error", "timeout", "timed out", "connection", "dns"]
    ):
        return "network_error"
    return "api_error"


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (
        s.startswith("'") and s.endswith("'")
    ):
        return s[1:-1]
    return s


def load_credentials_from_file(path: str):
    """
    Best-effort parser for ~/.config/visla/.credentials.

    Accepts common patterns:
    - export VISLA_API_KEY="..."
    - VISLA_API_KEY=...
    Ignores comments and unrelated lines.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return None, None

    api_key = None
    api_secret = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()

        m = re.match(r"^(VISLA_API_KEY|VISLA_API_SECRET)\s*=\s*(.+)$", line)
        if not m:
            continue
        raw_val = m.group(2).strip()
        # Handle inline comments: strip content after # unless inside quotes
        if raw_val and raw_val[0] in ("'", '"'):
            quote = raw_val[0]
            end = raw_val.find(quote, 1)
            if end != -1:
                raw_val = raw_val[: end + 1]
        else:
            raw_val = raw_val.split("#", 1)[0].strip()
        k, v = m.group(1), _strip_quotes(raw_val)
        if k == "VISLA_API_KEY":
            api_key = v
        elif k == "VISLA_API_SECRET":
            api_secret = v

    return api_key, api_secret


class VislaAPI:
    def __init__(self, api_key, api_secret):
        self.base_url = "https://openapi.visla.us/openapi/v1"
        self.api_key = api_key
        self.api_secret = api_secret

    def _safe_json(self, resp):
        try:
            return resp.json()
        except Exception:
            # Keep callers on the same "shape" (code/msg/data) they already expect.
            text = ""
            try:
                text = resp.text
            except Exception:
                text = "<no body>"
            return {
                "code": -1,
                "msg": f"Non-JSON response (HTTP {getattr(resp, 'status_code', 'unknown')}): {text[:500]}",
                "data": {},
            }

    def _sign(self, method, url):
        """Generate HMAC-SHA256 signature"""
        ts = str(int(time.time() * 1000))
        nonce = str(uuid.uuid4())
        sign_str = f"{method.upper()}|{url}|{ts}|{nonce}"
        signature = hmac.new(
            self.api_secret.encode(), sign_str.encode(), hashlib.sha256
        ).hexdigest()
        return {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": USER_AGENT,
            "key": self.api_key,
            "ts": ts,
            "nonce": nonce,
            "sign": signature,
        }

    def _request(self, method, endpoint, data=None):
        """Make signed API request"""
        url = f"{self.base_url}{endpoint}"
        headers = self._sign(method, url)
        try:
            if method == "GET":
                resp = requests.get(url, params=data, headers=headers, timeout=60)
            else:
                resp = requests.post(url, json=data, headers=headers, timeout=60)
        except requests.RequestException as e:
            return {"code": -1, "msg": f"Network error: {e}", "data": {}}

        return self._safe_json(resp)

    @staticmethod
    def _build_common_payload(
        video_title=None,
        video_description=None,
        aspect_ratio="16:9",
        video_pace="fast",
        burn_subtitles=False,
        video_duration_in_seconds=None,
        avatar_use_avatar=None,
        avatar_look_id=None,
        avatar_avatar_layout=None,
        avatar_enable_auto_wallpaper=None,
        avatar_enable_in_preview=None,
        voice_use_voice=None,
        voice_voice_id=None,
        footage_enable_footage=None,
        footage_use_free_stocks=True,
        footage_use_premium_stocks=True,
        footage_use_premium_stocks_getty=False,
        footage_use_private_stocks=False,
        footage_private_stock_ids=None,
        bgm_enable_bgm=None,
        bgm_use_free_stocks=True,
        bgm_use_premium_stocks=True,
    ):
        """Build payload sections shared by all video creation endpoints."""
        payload = {}
        if video_title:
            payload["video_title"] = video_title
        if video_description:
            payload["video_description"] = video_description

        target_video = {
            "aspect_ratio": aspect_ratio,
            "video_pace": video_pace,
            "burn_subtitles": burn_subtitles,
        }
        if video_duration_in_seconds:
            target_video["video_duration_in_seconds"] = video_duration_in_seconds
        payload["target_video"] = target_video

        avatar_options = {}
        if avatar_use_avatar is not None:
            avatar_options["use_avatar"] = avatar_use_avatar
        if avatar_look_id:
            avatar_options["use_avatar"] = True
            avatar_options["look_id"] = avatar_look_id
        if avatar_avatar_layout:
            avatar_options["avatar_layout"] = avatar_avatar_layout
        if avatar_enable_auto_wallpaper is not None:
            avatar_options["enable_auto_wallpaper"] = avatar_enable_auto_wallpaper
        if avatar_enable_in_preview is not None:
            avatar_options["enable_in_preview"] = avatar_enable_in_preview
        if avatar_options:
            payload["avatar_options"] = avatar_options

        voice_options = {}
        if voice_use_voice is not None:
            voice_options["use_voice"] = voice_use_voice
        if voice_voice_id:
            voice_options["use_voice"] = True
            voice_options["voice_id"] = voice_voice_id
        if voice_options:
            payload["voice_options"] = voice_options

        footage_options = {}
        if footage_enable_footage is not None:
            footage_options["enable_footage"] = footage_enable_footage
        footage_options["use_free_stocks"] = footage_use_free_stocks
        footage_options["use_premium_stocks"] = footage_use_premium_stocks
        footage_options["use_premium_stocks_getty"] = footage_use_premium_stocks_getty
        footage_options["use_private_stocks"] = footage_use_private_stocks
        if footage_private_stock_ids:
            footage_options["private_stock_ids"] = footage_private_stock_ids
        payload["footage_options"] = footage_options

        bgm_options = {}
        if bgm_enable_bgm is not None:
            bgm_options["enable_bgm"] = bgm_enable_bgm
        bgm_options["use_free_stocks"] = bgm_use_free_stocks
        bgm_options["use_premium_stocks"] = bgm_use_premium_stocks
        payload["bgm_options"] = bgm_options

        return payload

    # 1. Create video from script
    def create_from_script(self, script, script_text_mode="ai_rewrite", **opts):
        """Create a video project from a script"""
        payload = {"script": script, "script_text_mode": script_text_mode}
        payload.update(self._build_common_payload(**opts))
        return self._request("POST", "/project/script-to-video", payload)

    # 2. Poll project status until ready
    def wait_project(self, project_uuid, interval=20, max_attempts=180):
        """Poll project status until 'editing' or failed"""
        for i in range(max_attempts):
            result = self._request("GET", f"/project/{project_uuid}/info")
            if result.get("code") != 0:
                msg = result.get("msg", "Unknown error")
                print(f"failed: {msg}")
                return result
            status = result.get("data", {}).get("progressStatus")

            if status == "editing":
                print(f"{SYM_OK} Video generated!")
                share_link = result.get("data", {}).get("shareLink")
                if share_link:
                    print(f"  View link: {share_link}")
                print("  Exporting now, almost done...")
                print()
                return result
            elif status == "failed":
                print("Project failed!")
                return result
            # Show tip before sleeping
            print(VISLA_TIPS[i % len(VISLA_TIPS)])
            time.sleep(interval)
        print("Timeout")
        return {
            "code": -1,
            "msg": "Timeout waiting for video generation",
            "data": {"progressStatus": "timeout"},
        }

    # 4. Export project to video
    def export_video(self, project_uuid):
        """Export project to downloadable video"""
        return self._request("POST", f"/project/{project_uuid}/export-video", {})

    # 5. Poll clip status until ready
    def wait_clip(self, clip_uuid, interval=20, max_attempts=90):
        """Poll clip status until 'completed'"""
        print("Waiting for clip to render...")
        for i in range(max_attempts):
            result = self._request("GET", f"/clip/{clip_uuid}/info")
            if result.get("code") != 0:
                msg = result.get("msg", "Unknown error")
                print(f"failed: {msg}")
                return result
            status = result.get("data", {}).get("clipStatus")

            if status == "completed":
                print("Clip completed!")
                return result
            elif status == "failed":
                print("Clip failed!")
                return result
            # Show tip before sleeping
            print(VISLA_TIPS[i % len(VISLA_TIPS)])
            time.sleep(interval)
        print("Timeout")
        return {
            "code": -1,
            "msg": "Timeout waiting for clip rendering",
            "data": {"clipStatus": "timeout"},
        }

    # 6. Create video from URL
    def create_from_url(self, url, **opts):
        """Create a video project from a web URL"""
        payload = {"url": url}
        payload.update(self._build_common_payload(**opts))
        return self._request("POST", "/project/create-video-by-url", payload)

    # 8. Get upload URL for document
    def get_upload_url(self, media_type, suffix):
        """Get pre-signed S3 upload URL for document"""
        params = {"mediaType": media_type, "suffix": suffix}
        return self._request("GET", "/project/get-asset-upload-url", params)

    # 9. Upload file to S3
    def upload_to_s3(self, upload_url, file_path):
        """Upload file to S3 using pre-signed URL"""
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = "application/octet-stream"

        headers = {"Content-Type": content_type, "User-Agent": USER_AGENT}
        try:
            # Use streaming upload to avoid loading entire file into memory
            with open(file_path, "rb") as f:
                response = requests.put(
                    upload_url, data=f, headers=headers, timeout=300
                )
            return response
        except requests.RequestException as e:

            class DummyResp:
                status_code = 0
                error = str(e)

            return DummyResp()

    # 10. Create video from document
    def create_from_doc(self, doc_url, doc_filename,
                        doc_usage="page_by_page_walkthrough",
                        speaker_notes_verbatim=False, **opts):
        """Create a video project from uploaded document"""
        payload = {
            "doc_asset_url": doc_url,
            "doc_file_name": doc_filename,
            "doc_usage": doc_usage,
            "speaker_notes_verbatim": speaker_notes_verbatim,
        }
        payload.update(self._build_common_payload(**opts))
        return self._request("POST", "/project/doc-to-video", payload)

    # 11. Create video from idea
    def create_from_idea(self, idea, **opts):
        """Create a video project from an idea"""
        payload = {"idea": idea}
        # Ensure idea content reaches the API via the documented video_description field
        if not opts.get("video_description"):
            opts["video_description"] = idea[:500] if len(idea) > 500 else idea
        payload.update(self._build_common_payload(**opts))
        return self._request("POST", "/project/idea-to-video", payload)

    # 12. Create video from visual resources
    def create_from_visual(self, media_resources=None, media_asset_url=None,
                           video_style="storytelling", script_text=None, **opts):
        """Create a video project from visual resources (images/videos)"""
        if media_resources:
            payload = {"media_resources": media_resources}
        elif media_asset_url:
            payload = {"media_resources": [{"media_url": media_asset_url, "media_type": "image"}]}
        else:
            payload = {}
        if video_style:
            payload["video_style"] = video_style
        if script_text:
            payload["script_config"] = {"text_content": script_text, "text_type": "script"}
        payload.update(self._build_common_payload(**opts))
        return self._request("POST", "/project/visual-to-video", payload)

    # 13. Create video from speech
    def create_from_speech(self, media_resources=None, audio_asset_url=None,
                           project_function=None, **opts):
        """Create a video project from speech (audio/video file)"""
        # API documents speech_asset_url for single file; use media_resources for multiple
        if media_resources and len(media_resources) > 1:
            payload = {"media_resources": media_resources}
        elif media_resources and len(media_resources) == 1:
            payload = {"speech_asset_url": media_resources[0]["media_url"]}
        elif audio_asset_url:
            payload = {"speech_asset_url": audio_asset_url}
        else:
            payload = {}
        if project_function:
            payload["project_function"] = project_function
        payload.update(self._build_common_payload(**opts))
        return self._request("POST", "/project/speech-to-video", payload)

    # 11. List available avatars
    def list_avatars(self):
        """List available avatars for video projects"""
        return self._request("GET", "/workspace/list-avatar")

    # 12. List available voices
    def list_voices(self):
        """List available voices for video projects"""
        return self._request("GET", "/workspace/list-voice", {"localeName": "en-US"})

    # Convenience: Full workflow
    def create_and_download(self, script, script_text_mode="ai_rewrite", **opts):
        """Complete workflow: create -> wait -> export -> wait -> download link"""
        print("Creating video from script...")
        print()
        print(script)
        print()
        result = self.create_from_script(script, script_text_mode=script_text_mode, **opts)

        if result.get("code") != 0:
            msg = result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(f"Error: {result.get('msg')}")
            return {"error": msg}

        return self._announce_and_complete(result)

    # Validate URL exists
    def validate_url(self, url):
        """Check if URL is accessible"""
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code < 400:
                return True
            # Some sites block HEAD requests, retry with lightweight GET
            if response.status_code in (403, 405):
                response = requests.get(
                    url,
                    headers={"Range": "bytes=0-0"},
                    timeout=10,
                    allow_redirects=True,
                )
                return response.status_code < 400
            return False
        except Exception:
            return False

    # URL workflow
    def url_and_download(self, url, **opts):
        """Complete workflow for URL to video"""
        print(f"Validating URL: {url}")
        if not self.validate_url(url):
            print("VISLA_CLI_ERROR_CODE=invalid_url")
            print(f"Error: URL is not accessible: {url}")
            return {"error": "invalid_url", "url": url}
        print("URL validated successfully")
        print()
        print("Creating video from URL...")
        result = self.create_from_url(url, **opts)
        if result.get("code") != 0:
            msg = result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(f"Error: {result.get('msg')}")
            return {"error": msg, "url": url}
        return self._announce_and_complete(result)

    # Document workflow
    def doc_and_download(self, file_path, doc_usage="page_by_page_walkthrough",
                          speaker_notes_verbatim=False, **opts):
        """Complete workflow for document to video"""
        _validate_read_path(file_path)
        if not os.path.exists(file_path):
            print("VISLA_CLI_ERROR_CODE=file_not_found")
            print(f"Error: File not found: {file_path}")
            return {"error": "file_not_found", "file": file_path}

        filename = os.path.basename(file_path)
        suffix = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        media_type_map = {"pptx": "ppt", "ppt": "ppt", "pdf": "pdf"}
        media_type = media_type_map.get(suffix)
        if not media_type:
            print("VISLA_CLI_ERROR_CODE=unsupported_format")
            print(f"Error: Unsupported file type: {suffix}")
            print("Supported formats: pptx, ppt, pdf")
            return {"error": "unsupported_format", "file": file_path}

        print(f"Uploading document: {filename}")
        upload_url, err = self._upload_file(file_path, media_type, suffix)
        if err:
            return err

        print("Creating video from document...")
        result = self.create_from_doc(
            upload_url, filename,
            doc_usage=doc_usage, speaker_notes_verbatim=speaker_notes_verbatim, **opts,
        )
        if result.get("code") != 0:
            msg = result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(f"Error: {result.get('msg')}")
            return {"error": msg, "file": file_path}
        return self._announce_and_complete(result)

    # Idea workflow
    def idea_and_download(self, idea, **opts):
        """Complete workflow for idea to video"""
        print("Creating video from idea...")
        print()
        print(idea)
        print()
        result = self.create_from_idea(idea, **opts)
        if result.get("code") != 0:
            msg = result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(f"Error: {result.get('msg')}")
            return {"error": msg, "idea": idea}
        return self._announce_and_complete(result)

    # Visual workflow
    def visual_and_download(self, file_paths, video_style="storytelling",
                            script=None, **opts):
        """Complete workflow for visual resources to video"""
        if isinstance(file_paths, str):
            file_paths = [file_paths]

        VISUAL_TYPES = {
            "jpg": "image", "jpeg": "image", "png": "image",
            "gif": "image", "webp": "image",
            "mp4": "video", "mov": "video", "avi": "video", "mkv": "video",
        }
        media_resources, err = self._upload_media_files(file_paths, VISUAL_TYPES, "visual resource")
        if err:
            return err

        print("Creating video from visual resources...")
        result = self.create_from_visual(
            media_resources=media_resources, video_style=video_style,
            script_text=script, **opts,
        )
        if result.get("code") != 0:
            msg = result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(f"Error: {result.get('msg')}")
            return {"error": msg}
        return self._announce_and_complete(result)

    # Speech workflow
    def speech_and_download(self, file_paths, project_function=None, **opts):
        """Complete workflow for speech/audio to video"""
        if isinstance(file_paths, str):
            file_paths = [file_paths]

        SPEECH_TYPES = {
            "mp3": "audio", "wav": "audio", "m4a": "audio",
            "aac": "audio", "flac": "audio",
            "mp4": "video", "mov": "video", "avi": "video", "mkv": "video",
        }
        media_resources, err = self._upload_media_files(file_paths, SPEECH_TYPES, "audio file")
        if err:
            return err

        print("Creating video from speech...")
        result = self.create_from_speech(
            media_resources=media_resources, project_function=project_function, **opts,
        )
        if result.get("code") != 0:
            msg = result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(f"Error: {result.get('msg')}")
            return {"error": msg}
        return self._announce_and_complete(result)

    # Shared helpers

    def _upload_file(self, file_path, media_type, suffix):
        """Upload a single file to S3. Returns (upload_url, error_dict_or_None)."""
        upload_result = self.get_upload_url(media_type, suffix)
        if upload_result.get("code") != 0:
            msg = upload_result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(f"Error getting upload URL: {upload_result.get('msg')}")
            return None, {"error": msg, "file": file_path}

        upload_url = upload_result.get("data", {}).get("uploadUrl")
        print("Upload URL obtained")

        response = self.upload_to_s3(upload_url, file_path)
        if response.status_code not in [200, 201]:
            if getattr(response, "error", None):
                print("VISLA_CLI_ERROR_CODE=network_error")
                print(f"Error uploading file: {response.error}")
            else:
                print("VISLA_CLI_ERROR_CODE=api_error")
                print(f"Error uploading file: HTTP {response.status_code}")
            return None, {"error": "upload_failed", "file": file_path}
        print("File uploaded successfully")
        return upload_url, None

    def _upload_media_files(self, file_paths, type_map, label):
        """Upload multiple media files. Returns (media_resources_list, error_dict_or_None)."""
        media_resources = []
        for fp in file_paths:
            _validate_read_path(fp)
            if not os.path.exists(fp):
                print("VISLA_CLI_ERROR_CODE=file_not_found")
                print(f"Error: File not found: {fp}")
                return None, {"error": "file_not_found", "file": fp}

            filename = os.path.basename(fp)
            suffix = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
            media_type = type_map.get(suffix)
            if not media_type:
                print("VISLA_CLI_ERROR_CODE=unsupported_format")
                print(f"Error: Unsupported file type: {suffix}")
                return None, {"error": "unsupported_format", "file": fp}

            print(f"Uploading {label}: {filename}")
            upload_url, err = self._upload_file(fp, media_type, suffix)
            if err:
                return None, err
            media_resources.append({"media_url": upload_url, "media_type": media_type})
        print()
        return media_resources, None

    def _announce_and_complete(self, create_result):
        """Print project info and run wait -> export -> download."""
        project_uuid = create_result.get("data", {}).get("projectUuid")
        share_link = create_result.get("data", {}).get("shareLink")
        print(f"Project created: {project_uuid}")
        if share_link:
            print(f"View link: {share_link}")
        print()
        print(f"{SYM_INFO} Grab a coffee! Video generation takes a few minutes...")
        print(f"{SYM_VIDEO} Visla AI is creating your video")
        print()
        return self._complete_workflow(project_uuid)

    # Shared workflow: wait -> export -> download
    def _complete_workflow(self, project_uuid):
        """Complete the workflow after project creation"""
        # Wait for project
        project = self.wait_project(project_uuid)
        if project.get("code") != 0:
            msg = project.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(f"Error: {msg}")
            return {"project_uuid": project_uuid, "error": msg}
        if project.get("data", {}).get("progressStatus") != "editing":
            print("VISLA_CLI_ERROR_CODE=timeout")
            print("Error: Timeout waiting for video generation")
            return {"project_uuid": project_uuid, "error": "timeout"}

        # Export
        print("Exporting video...")
        export_result = self.export_video(project_uuid)
        if export_result.get("code") != 0:
            msg = export_result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print("Export failed!")
            return {"project_uuid": project_uuid, "error": msg}

        clip_uuid = export_result.get("data", {}).get("clipUuid")
        share_link = export_result.get("data", {}).get("shareLink")
        print(f"Clip UUID: {clip_uuid}")

        # Wait for clip
        clip_result = self.wait_clip(clip_uuid)
        if clip_result.get("code") != 0:
            msg = clip_result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(f"Error: {msg}")
            return {"project_uuid": project_uuid, "clip_uuid": clip_uuid, "error": msg}
        if clip_result.get("data", {}).get("clipStatus") != "completed":
            print("VISLA_CLI_ERROR_CODE=timeout")
            print("Error: Timeout waiting for clip rendering")
            return {
                "project_uuid": project_uuid,
                "clip_uuid": clip_uuid,
                "error": "timeout",
            }

        print(f"\n{SYM_OK} Video ready!")

        return {
            "project_uuid": project_uuid,
            "clip_uuid": clip_uuid,
            "share_link": share_link,
        }


def load_video_config(config_path):
    """Load video configuration from JSON file"""
    if not config_path or not os.path.exists(config_path):
        return {}
    _validate_read_path(config_path)
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"VISLA_CLI_ERROR_CODE=invalid_config")
        print(f"Error: Failed to load config file: {e}")
        sys.exit(1)


def merge_config_with_args(config, args):
    """Merge config file with CLI arguments, CLI args take priority"""
    result = {
        "video_title": config.get("video_title"),
        "video_description": config.get("video_description"),
        "project_function": config.get("project_function"),
        "script_text_mode": config.get("script_text_mode", "ai_rewrite"),
        # doc options
        "doc_usage": config.get("doc_usage", "page_by_page_walkthrough"),
        "speaker_notes_verbatim": config.get("speaker_notes_verbatim", False),
        # target_video defaults
        "aspect_ratio": config.get("target_video", {}).get("aspect_ratio", "16:9"),
        "video_pace": config.get("target_video", {}).get("video_pace", "fast"),
        "burn_subtitles": config.get("target_video", {}).get("burn_subtitles", False),
        "video_duration_in_seconds": config.get("target_video", {}).get(
            "video_duration_in_seconds"
        ),
        # avatar_options
        "avatar_options": config.get("avatar_options", {}),
        # voice_options
        "voice_options": config.get("voice_options", {}),
        # footage_options
        "footage_options": {
            "enable_footage": config.get("footage_options", {}).get(
                "enable_footage", True
            ),
            "use_free_stocks": config.get("footage_options", {}).get(
                "use_free_stocks", True
            ),
            "use_premium_stocks": config.get("footage_options", {}).get(
                "use_premium_stocks", False
            ),
            "use_premium_stocks_getty": config.get("footage_options", {}).get(
                "use_premium_stocks_getty", False
            ),
            "use_private_stocks": config.get("footage_options", {}).get(
                "use_private_stocks", False
            ),
            "private_stock_ids": config.get("footage_options", {}).get(
                "private_stock_ids"
            ),
        },
        # bgm_options
        "bgm_options": {
            "enable_bgm": config.get("bgm_options", {}).get("enable_bgm", True),
            "use_free_stocks": config.get("bgm_options", {}).get(
                "use_free_stocks", True
            ),
            "use_premium_stocks": config.get("bgm_options", {}).get(
                "use_premium_stocks", False
            ),
        },
    }
    # CLI args override config
    if hasattr(args, "avatar") and args.avatar:
        result["avatar_options"] = result.get("avatar_options", {})
        result["avatar_options"]["use_avatar"] = True
        result["avatar_options"]["look_id"] = args.avatar
    if hasattr(args, "voice") and args.voice:
        result["voice_options"] = result.get("voice_options", {})
        result["voice_options"]["use_voice"] = True
        result["voice_options"]["voice_id"] = args.voice
    return result


def _flatten_opts_to_kwargs(video_opts):
    """Flatten merged config dict to keyword arguments matching API method signatures.

    The API methods use prefixed parameter names (e.g. avatar_use_avatar,
    footage_use_free_stocks) while the config/merge layer produces nested dicts
    (avatar_options.use_avatar, footage_options.use_free_stocks).  This bridges
    the two so every command in main() can simply do ``**_flatten_opts_to_kwargs(video_opts)``.
    """
    avatar = video_opts.get("avatar_options", {})
    voice = video_opts.get("voice_options", {})
    footage = video_opts.get("footage_options", {})
    bgm = video_opts.get("bgm_options", {})

    kw = {}

    # avatar
    if avatar.get("use_avatar"):
        kw["avatar_use_avatar"] = True
    if avatar.get("look_id"):
        kw["avatar_look_id"] = avatar["look_id"]
    if avatar.get("avatar_layout"):
        kw["avatar_avatar_layout"] = avatar["avatar_layout"]
    if avatar.get("enable_auto_wallpaper") is not None:
        kw["avatar_enable_auto_wallpaper"] = avatar["enable_auto_wallpaper"]
    if avatar.get("enable_in_preview") is not None:
        kw["avatar_enable_in_preview"] = avatar["enable_in_preview"]

    # voice
    if voice.get("use_voice"):
        kw["voice_use_voice"] = True
    if voice.get("voice_id"):
        kw["voice_voice_id"] = voice["voice_id"]

    # footage
    if footage.get("enable_footage") is not None:
        kw["footage_enable_footage"] = footage["enable_footage"]
    kw["footage_use_free_stocks"] = footage.get("use_free_stocks", True)
    kw["footage_use_premium_stocks"] = footage.get("use_premium_stocks", False)
    kw["footage_use_premium_stocks_getty"] = footage.get(
        "use_premium_stocks_getty", False
    )
    kw["footage_use_private_stocks"] = footage.get("use_private_stocks", False)
    if footage.get("private_stock_ids"):
        kw["footage_private_stock_ids"] = footage["private_stock_ids"]

    # bgm
    if bgm.get("enable_bgm") is not None:
        kw["bgm_enable_bgm"] = bgm["enable_bgm"]
    kw["bgm_use_free_stocks"] = bgm.get("use_free_stocks", True)
    kw["bgm_use_premium_stocks"] = bgm.get("use_premium_stocks", False)

    return kw


def main():
    parser = argparse.ArgumentParser(description=f"Visla Skill v{VERSION}")
    parser.add_argument("--key", help="API Key (or set VISLA_API_KEY env var)")
    parser.add_argument("--secret", help="API Secret (or set VISLA_API_SECRET env var)")

    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Script command
    script_parser = subparsers.add_parser("script", help="Create video from script")
    script_parser.add_argument("script", help="Script text or @filename")
    script_parser.add_argument(
        "--config", "-c", help="Path to JSON config file with video options"
    )
    script_parser.add_argument("--avatar", help="Avatar ID (overrides config)")
    script_parser.add_argument("--voice", help="Voice ID (overrides config)")

    # Account command
    subparsers.add_parser("account", help="Show account info and credit balance")

    # Avatar command
    subparsers.add_parser("avatar", help="List available avatars")

    # Voice command
    subparsers.add_parser("voice", help="List available voices")

    # URL command
    url_parser = subparsers.add_parser("url", help="Create video from URL")
    url_parser.add_argument("url", help="Web page URL")
    url_parser.add_argument(
        "--config", "-c", help="Path to JSON config file with video options"
    )
    url_parser.add_argument("--avatar", help="Avatar ID (overrides config)")
    url_parser.add_argument("--voice", help="Voice ID (overrides config)")

    # Doc command
    doc_parser = subparsers.add_parser(
        "doc", help="Create video from document (PPT/PDF)"
    )
    doc_parser.add_argument("file", help="Document file path")
    doc_parser.add_argument(
        "--config", "-c", help="Path to JSON config file with video options"
    )
    doc_parser.add_argument("--avatar", help="Avatar ID (overrides config)")
    doc_parser.add_argument("--voice", help="Voice ID (overrides config)")

    # Idea command
    idea_parser = subparsers.add_parser("idea", help="Create video from idea")
    idea_parser.add_argument("idea", help="Idea text or @filename")
    idea_parser.add_argument(
        "--config", "-c", help="Path to JSON config file with video options"
    )
    idea_parser.add_argument("--avatar", help="Avatar ID (overrides config)")
    idea_parser.add_argument("--voice", help="Voice ID (overrides config)")

    # Visual command
    visual_parser = subparsers.add_parser(
        "visual", help="Create video from visual resources (images/videos)"
    )
    visual_parser.add_argument("file", nargs="+", help="Image or video file path(s)")
    visual_parser.add_argument(
        "--config", "-c", help="Path to JSON config file with video options"
    )
    visual_parser.add_argument("--avatar", help="Avatar ID (overrides config)")
    visual_parser.add_argument("--voice", help="Voice ID (overrides config)")
    visual_parser.add_argument(
        "--style",
        choices=["montage", "storytelling", "explainer"],
        default="storytelling",
        help="Video style: montage, storytelling, or explainer (default: storytelling)",
    )
    visual_parser.add_argument(
        "--script", "-s", help="Script or description text (or @filename)"
    )

    # Speech command
    speech_parser = subparsers.add_parser(
        "speech", help="Create video from speech (audio/video file)"
    )
    speech_parser.add_argument("file", nargs="+", help="Audio or video file path(s)")
    speech_parser.add_argument(
        "--config", "-c", help="Path to JSON config file with video options"
    )
    speech_parser.add_argument("--avatar", help="Avatar ID (overrides config)")
    speech_parser.add_argument("--voice", help="Voice ID (overrides config)")
    speech_parser.add_argument(
        "--function",
        choices=["SPEECH_TO_VIDEO_SUMMARY", "SPEECH_TO_VIDEO_FULL_LENGTH"],
        help="Speech to video function: SPEECH_TO_VIDEO_SUMMARY (highlights) or SPEECH_TO_VIDEO_FULL_LENGTH (full length)",
    )

    args = parser.parse_args()

    # Priority: command line args > environment variables
    api_key = args.key or os.environ.get("VISLA_API_KEY")
    api_secret = args.secret or os.environ.get("VISLA_API_SECRET")

    # Auto-detect credentials from default path only
    if (not api_key or not api_secret) and os.path.exists(DEFAULT_CREDENTIALS_PATH):
        file_key, file_secret = load_credentials_from_file(DEFAULT_CREDENTIALS_PATH)
        api_key = api_key or file_key
        api_secret = api_secret or file_secret

    if not api_key or not api_secret:
        print("VISLA_CLI_ERROR_CODE=missing_credentials")
        print("Error: Visla credentials not configured")
        print("")
        print("Option 1: Set environment variables")
        if sys.platform == "win32":
            print('  $env:VISLA_API_KEY = "your_key"')
            print('  $env:VISLA_API_SECRET = "your_secret"')
        else:
            print('  export VISLA_API_KEY="your_key"')
            print('  export VISLA_API_SECRET="your_secret"')
        print("")
        print("Option 2: Pass as arguments")
        print('  python visla_cli.py --key "your_key" --secret "your_secret" <command>')
        print("")
        print("Option 3: Use a credentials file (auto-detected)")
        print(f"  Default path: {DEFAULT_CREDENTIALS_PATH}")
        print('  Example file contents:')
        print('    export VISLA_API_KEY="your_key"')
        print('    export VISLA_API_SECRET="your_secret"')
        print("")
        print("Get your API credentials from:")
        print("  https://www.visla.us/visla-api")
        sys.exit(1)

    print(f"Visla Skill v{VERSION}")
    api = VislaAPI(api_key, api_secret)

    if args.command == "script":
        # Load config if provided
        config = {}
        if hasattr(args, "config") and args.config:
            config = load_video_config(args.config)

        # Merge config with CLI args
        video_opts = merge_config_with_args(config, args)

        # Read from stdin if "-", from file if starts with @, otherwise use directly
        script = args.script
        if script == "-":
            # Read from stdin (no temp files needed)
            script = sys.stdin.read()
            if not script.strip():
                print("VISLA_CLI_ERROR_CODE=empty_input")
                print("Error: No script content received from stdin")
                sys.exit(1)
        elif script.startswith("@"):
            file_path = script[1:]
            _validate_read_path(file_path, allowed_extensions=ALLOWED_TEXT_EXTENSIONS)
            if not os.path.exists(file_path):
                print("VISLA_CLI_ERROR_CODE=file_not_found")
                print(f"Error: File not found: {file_path}")
                sys.exit(1)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    script = f.read()
            except OSError as e:
                print("VISLA_CLI_ERROR_CODE=file_read_failed")
                print(f"Error: Failed to read file: {file_path} ({e})")
                sys.exit(1)

        opts_kwargs = _flatten_opts_to_kwargs(video_opts)
        result = api.create_and_download(
            script,
            video_title=video_opts.get("video_title"),
            video_description=video_opts.get("video_description"),
            script_text_mode=video_opts.get("script_text_mode", "ai_rewrite"),
            aspect_ratio=video_opts.get("aspect_ratio", "16:9"),
            video_pace=video_opts.get("video_pace", "fast"),
            burn_subtitles=video_opts.get("burn_subtitles", False),
            video_duration_in_seconds=video_opts.get("video_duration_in_seconds"),
            **opts_kwargs,
        )
        if not result or result.get("error"):
            # Error code already printed by create_and_download
            sys.exit(1)
        print("Video ready!")
        if result.get("share_link"):
            print(f"View link: {result['share_link']}")
        print(f"Visla Skill v{VERSION} completed")

    elif args.command == "url":
        # Load config if provided
        config = {}
        if hasattr(args, "config") and args.config:
            config = load_video_config(args.config)

        # Merge config with CLI args
        video_opts = merge_config_with_args(config, args)

        opts_kwargs = _flatten_opts_to_kwargs(video_opts)
        result = api.url_and_download(
            args.url,
            video_title=video_opts.get("video_title"),
            video_description=video_opts.get("video_description"),
            aspect_ratio=video_opts.get("aspect_ratio", "16:9"),
            video_pace=video_opts.get("video_pace", "fast"),
            burn_subtitles=video_opts.get("burn_subtitles", False),
            video_duration_in_seconds=video_opts.get("video_duration_in_seconds"),
            **opts_kwargs,
        )
        if not result or result.get("error"):
            # Error code already printed by url_and_download
            sys.exit(1)
        print("Video ready!")
        if result.get("share_link"):
            print(f"View link: {result['share_link']}")
        print(f"Visla Skill v{VERSION} completed")

    elif args.command == "doc":
        # Load config if provided
        config = {}
        if hasattr(args, "config") and args.config:
            config = load_video_config(args.config)

        # Merge config with CLI args
        video_opts = merge_config_with_args(config, args)

        opts_kwargs = _flatten_opts_to_kwargs(video_opts)
        result = api.doc_and_download(
            args.file,
            video_title=video_opts.get("video_title"),
            video_description=video_opts.get("video_description"),
            aspect_ratio=video_opts.get("aspect_ratio", "16:9"),
            video_pace=video_opts.get("video_pace", "fast"),
            burn_subtitles=video_opts.get("burn_subtitles", False),
            video_duration_in_seconds=video_opts.get("video_duration_in_seconds"),
            doc_usage=video_opts.get("doc_usage", "page_by_page_walkthrough"),
            speaker_notes_verbatim=video_opts.get("speaker_notes_verbatim", False),
            **opts_kwargs,
        )
        if not result or result.get("error"):
            # Error code already printed by doc_and_download
            sys.exit(1)
        print("Video ready!")
        if result.get("share_link"):
            print(f"View link: {result['share_link']}")
        print(f"Visla Skill v{VERSION} completed")

    elif args.command == "idea":
        config = {}
        if hasattr(args, "config") and args.config:
            config = load_video_config(args.config)

        video_opts = merge_config_with_args(config, args)

        idea_text = args.idea
        if idea_text == "-":
            idea_text = sys.stdin.read()
            if not idea_text.strip():
                print("VISLA_CLI_ERROR_CODE=empty_input")
                print("Error: No idea content received from stdin")
                sys.exit(1)
        elif idea_text.startswith("@"):
            file_path = idea_text[1:]
            _validate_read_path(file_path, allowed_extensions=ALLOWED_TEXT_EXTENSIONS)
            if not os.path.exists(file_path):
                print("VISLA_CLI_ERROR_CODE=file_not_found")
                print(f"Error: File not found: {file_path}")
                sys.exit(1)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    idea_text = f.read()
            except OSError as e:
                print("VISLA_CLI_ERROR_CODE=file_read_failed")
                print(f"Error: Failed to read file: {file_path} ({e})")
                sys.exit(1)

        opts_kwargs = _flatten_opts_to_kwargs(video_opts)
        result = api.idea_and_download(
            idea_text,
            video_title=video_opts.get("video_title"),
            video_description=video_opts.get("video_description"),
            aspect_ratio=video_opts.get("aspect_ratio", "16:9"),
            video_pace=video_opts.get("video_pace", "fast"),
            burn_subtitles=video_opts.get("burn_subtitles", False),
            video_duration_in_seconds=video_opts.get("video_duration_in_seconds"),
            **opts_kwargs,
        )
        if not result or result.get("error"):
            sys.exit(1)
        print("Video ready!")
        if result.get("share_link"):
            print(f"View link: {result['share_link']}")
        print(f"Visla Skill v{VERSION} completed")

    elif args.command == "visual":
        config = {}
        if hasattr(args, "config") and args.config:
            config = load_video_config(args.config)

        video_opts = merge_config_with_args(config, args)

        # Handle script from command line args
        script_text = getattr(args, "script", None)
        if script_text:
            if script_text == "-":
                script_text = sys.stdin.read()
            elif script_text.startswith("@"):
                file_path = script_text[1:]
                _validate_read_path(file_path, allowed_extensions=ALLOWED_TEXT_EXTENSIONS)
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        script_text = f.read()

        opts_kwargs = _flatten_opts_to_kwargs(video_opts)
        result = api.visual_and_download(
            args.file,
            video_title=video_opts.get("video_title"),
            video_description=video_opts.get("video_description"),
            video_style=getattr(args, "style", "storytelling"),
            script=script_text,
            aspect_ratio=video_opts.get("aspect_ratio", "16:9"),
            video_pace=video_opts.get("video_pace", "fast"),
            burn_subtitles=video_opts.get("burn_subtitles", False),
            video_duration_in_seconds=video_opts.get("video_duration_in_seconds"),
            **opts_kwargs,
        )
        if not result or result.get("error"):
            sys.exit(1)
        print("Video ready!")
        if result.get("share_link"):
            print(f"View link: {result['share_link']}")
        print(f"Visla Skill v{VERSION} completed")

    elif args.command == "speech":
        config = {}
        if hasattr(args, "config") and args.config:
            config = load_video_config(args.config)

        video_opts = merge_config_with_args(config, args)

        project_function = getattr(args, "function", None) or video_opts.get(
            "project_function"
        )

        opts_kwargs = _flatten_opts_to_kwargs(video_opts)
        result = api.speech_and_download(
            args.file,
            video_title=video_opts.get("video_title"),
            video_description=video_opts.get("video_description"),
            project_function=project_function,
            aspect_ratio=video_opts.get("aspect_ratio", "16:9"),
            video_pace=video_opts.get("video_pace", "fast"),
            burn_subtitles=video_opts.get("burn_subtitles", False),
            video_duration_in_seconds=video_opts.get("video_duration_in_seconds"),
            **opts_kwargs,
        )
        if not result or result.get("error"):
            sys.exit(1)
        print("Video ready!")
        if result.get("share_link"):
            print(f"View link: {result['share_link']}")
        print(f"Visla Skill v{VERSION} completed")

    elif args.command == "account":
        from datetime import datetime

        info_result = api._request("GET", "/user/info")
        credit_result = api._request("GET", "/workspace/credit-balance")
        if info_result.get("code") != 0:
            msg = info_result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(msg)
            sys.exit(1)
        if credit_result.get("code") != 0:
            msg = credit_result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(msg)
            sys.exit(1)
        data = info_result.get("data", {})
        email = data.get("email", "N/A")
        given_name = data.get("givenName", "")
        family_name = data.get("familyName", "")
        status = data.get("userStatus", "N/A")
        reg_time = data.get("regTime", 0)
        login_time = data.get("loginTime", 0)
        credits = credit_result.get("data", 0)

        reg_date = (
            datetime.fromtimestamp(reg_time / 1000).strftime("%Y-%m-%d")
            if reg_time
            else "N/A"
        )
        login_date = (
            datetime.fromtimestamp(login_time / 1000).strftime("%Y-%m-%d")
            if login_time
            else "N/A"
        )

        print(f"Email: {email}")
        print(f"Name: {given_name} {family_name}")
        print(f"Status: {status}")
        print(f"Registered: {reg_date}")
        print(f"Last Login: {login_date}")
        print(f"Credits: {credits}")
        print(f"Visla Skill v{VERSION} completed")
        sys.exit(0)

    elif args.command == "avatar":
        result = api.list_avatars()
        if result.get("code") != 0:
            msg = result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(msg)
            sys.exit(1)
        avatars = result.get("data", [])
        if not avatars:
            print("No avatars available")
        else:
            print(f"Available avatars ({len(avatars)}):")
            for avatar in avatars:
                avatar_name = avatar.get("name") or "Unnamed"
                looks = avatar.get("looks", [])
                if looks:
                    for look in looks:
                        look_name = look.get("name") or "Unnamed"
                        look_uuid = look.get("lookUuid") or "N/A"
                        thumb = look.get("thumbnailLink") or ""
                        print(f"  - {avatar_name} | {look_name} | lookUuid: {look_uuid}")
                        if thumb:
                            print(f"    Thumbnail: {thumb}")
                else:
                    print(f"  - {avatar_name} (no looks)")
        print(f"Visla Skill v{VERSION} completed")
        sys.exit(0)

    elif args.command == "voice":
        result = api.list_voices()
        if result.get("code") != 0:
            msg = result.get("msg", "Unknown error")
            print(f"VISLA_CLI_ERROR_CODE={classify_error_code(msg)}")
            print(msg)
            sys.exit(1)

        data = result.get("data", {})
        custom_voices = data.get("customVoices", [])
        system_voices = data.get("systemVoices", [])

        total = len(custom_voices) + len(system_voices)
        if total == 0:
            print("No voices available")
        else:
            print(f"Available voices ({total}):")

            if custom_voices:
                print("\n[Custom Voices]")
                for v in custom_voices:
                    name = v.get("voiceName") or v.get("voiceSpeakerName") or "Unnamed"
                    uuid = v.get("voiceUuid") or v.get("uuid") or "N/A"
                    url = v.get("voiceUrl") or ""
                    fav = "★" if v.get("favorite") else ""
                    print(f"  - {name} {fav} (ID: {uuid})")
                    if url:
                        print(f"    URL: {url}")

            if system_voices:
                print("\n[System Voices]")
                for v in system_voices:
                    name = v.get("voiceName") or v.get("voiceSpeakerName") or "Unnamed"
                    uuid = v.get("voiceUuid") or v.get("uuid") or "N/A"
                    url = v.get("voiceUrl") or ""
                    fav = "★" if v.get("favorite") else ""
                    print(f"  - {name} {fav} (ID: {uuid})")
                    if url:
                        print(f"    URL: {url}")
        print(f"\nVisla Skill v{VERSION} completed")
        sys.exit(0)

    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
