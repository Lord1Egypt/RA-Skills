#!/usr/bin/env python3
"""
Smart Photo Editor - Unified Entry Point

Provides a unified interface for all photo editing operations:
- Object removal (Seedream AI + OpenCV fallback)
- Background removal (rembg + ImageMagick fallback)
- Old photo restoration (Seedream AI)
- Basic editing (ImageMagick)

Usage:
    ./edit.py --task remove-object --image input.jpg --prompt "Remove the person" --output output.jpg
    ./edit.py --task restore --image old.jpg --output restored.jpg
    ./edit.py --task remove-background --image portrait.jpg --output no_bg.png
    ./edit.py --task resize --image photo.jpg --output small.jpg --width 800 --height 600
    ./edit.py --json < tasks.json   # Batch mode with JSON input

JSON batch format:
    {
      "operations": [
        {"task": "remove-object", "image": "a.jpg", "prompt": "...", "output": "a_out.jpg"},
        {"task": "restore", "image": "b.jpg", "output": "b_out.jpg"}
      ]
    }
"""
import argparse
import json
import os
import sys
import subprocess
import time
import traceback
from typing import Any, Dict, List, Optional

# Try to import optional dependencies
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_API_DIM = 2048  # Seedream API limit


class SmartPhotoEditor:
    """Unified photo editing engine with automatic tool selection."""

    def __init__(self, venv_python: str = None, json_output: bool = False):
        self.json_output = json_output
        # Auto-detect venv Python: prefer sys.executable (shebang-driven),
        # fall back to known venv locations if needed
        if venv_python:
            self.venv_python = venv_python
        elif sys.executable and "venv-clawd" in sys.executable:
            self.venv_python = sys.executable
        else:
            # Fallback: try known venv locations
            import glob
            venv_root = os.path.expanduser("~/.openclaw")
            candidates = glob.glob(f"{venv_root}/venv*/bin/python")
            if candidates:
                self.venv_python = candidates[0]
            else:
                # Last resort: use the Python running this script
                self.venv_python = sys.executable
        self.results: List[Dict] = []

    def _log(self, message: str, level: str = "info"):
        """Log message to stderr or output JSON."""
        if self.json_output:
            print(json.dumps({"log": message, "level": level}), file=sys.stderr)
        else:
            print(f"[{level.upper()}] {message}", file=sys.stderr)

    def _error(self, message: str):
        self._log(message, "error")

    def _warn(self, message: str):
        self._log(message, "warning")

    def _result(self, success: bool, operation: str, output: str = None,
                elapsed_ms: int = 0, error: str = None, **extra):
        """Record a result."""
        result = {
            "success": success,
            "operation": operation,
            "elapsed_ms": elapsed_ms,
        }
        if output:
            result["output"] = output
        if error:
            result["error"] = error
        result.update(extra)
        self.results.append(result)

        if self.json_output:
            print(json.dumps(result), file=sys.stdout)
        else:
            status = "✓" if success else "✗"
            print(f"{status} {operation}" + (f": {output}" if output else ""), file=sys.stderr)
            if error:
                print(f"  Error: {error}", file=sys.stderr)

        return success

    def _validate_path(self, path: str, must_exist: bool = False,
                      allow_outside_cwd: bool = False) -> tuple:
        """
        Validate a file path for security (path traversal prevention).
        Returns (is_valid, resolved_path, error_message).
        """
        if not path:
            return False, None, "Empty path"

        # Check for path traversal attempts
        normalized = os.path.normpath(path)
        if '..' in normalized.split(os.sep):
            return False, None, f"Path traversal not allowed: {path}"

        # Check must-exist constraint
        if must_exist and not os.path.exists(path):
            return False, None, f"File does not exist: {path}"

        # For output paths, ensure it's a reasonable location
        # (not system directories like /etc, /sys, /proc)
        if not must_exist:
            resolved = os.path.abspath(path)
            forbidden = ['/etc', '/sys', '/proc', '/boot', '/dev']
            for forbidden_dir in forbidden:
                if resolved.startswith(forbidden_dir + os.sep):
                    return False, None, f"Output path not allowed: {path}"

        resolved = os.path.abspath(path) if os.path.exists(path) else path
        return True, resolved, None

    def _check_image(self, path: str) -> tuple:
        """Check if image exists and return (valid, resolved_path, error)."""
        if not os.path.exists(path):
            return False, None, f"File not found: {path}"
        # Try to read it to verify it's a valid image
        if OPENCV_AVAILABLE:
            img = cv2.imread(path)
            if img is None:
                return False, None, f"Could not read image: {path}"
            return True, path, None
        elif PIL_AVAILABLE:
            try:
                with Image.open(path) as img:
                    img.verify()
                return True, path, None
            except Exception as e:
                return False, None, f"Invalid image: {e}"
        # No image library available — just check existence
        return True, path, None

    def _resize_for_api(self, image_path: str, max_dim: int = MAX_API_DIM) -> tuple:
        """Resize image if needed, return (temp_path, was_resized)."""
        valid, resolved, err = self._check_image(image_path)
        if not valid:
            return image_path, False

        # Read image to get dimensions
        if OPENCV_AVAILABLE:
            img = cv2.imread(resolved)
            if img is None:
                return image_path, False
            height, width = img.shape[:2]
        elif PIL_AVAILABLE:
            with Image.open(resolved) as img:
                width, height = img.size
        else:
            return image_path, False
        if max(width, height) <= max_dim:
            return image_path, False

        # Need to resize
        if OPENCV_AVAILABLE:
            img = cv2.imread(image_path)
            if height > width:
                new_h, new_w = max_dim, int(width * max_dim / height)
            else:
                new_w, new_h = max_dim, int(height * max_dim / width)
            resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            temp_path = image_path + ".resized.jpg"
            cv2.imwrite(temp_path, resized)
            return temp_path, True
        elif PIL_AVAILABLE:
            with Image.open(image_path) as img:
                img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
                temp_path = image_path + ".resized.jpg"
                img.save(temp_path)
                return temp_path, True
        return image_path, False

    def _cleanup_temp(self, path: str, was_temp: bool):
        """Remove temporary file if it was created."""
        if was_temp and path and path.endswith(".resized.jpg"):
            try:
                os.remove(path)
            except OSError:
                pass

    # R2 / Cloudflare uploader
    _R2_SIZE_THRESHOLD = 1_500_000  # bytes

    def _r2_upload(self, file_path: str):
        """Upload a file to R2 via a Cloudflare Worker.

        Returns (url, None) on success, (None, error_message) on failure.
        The caller MUST fall back to base64 data URI on failure.

        Requires BOTH env vars to be set (no built-in defaults):
          SEEDREAM_UPLOAD_TOKEN       - Bearer token for the worker
          SEEDREAM_UPLOAD_WORKER_URL  - Worker base URL
        """
        import mimetypes, urllib.request, urllib.error, json as _json

        worker_url = os.environ.get("SEEDREAM_UPLOAD_WORKER_URL", "")
        upload_token = os.environ.get("SEEDREAM_UPLOAD_TOKEN", "")
        if not upload_token:
            return None, "SEEDREAM_UPLOAD_TOKEN not set"
        if not worker_url:
            return None, "SEEDREAM_UPLOAD_WORKER_URL not set"

        filename = os.path.basename(file_path)
        mime, _ = mimetypes.guess_type(file_path)
        mime = mime or "image/jpeg"

        try:
            with open(file_path, "rb") as fh:
                data = fh.read()
        except OSError as e:
            return None, "Could not read " + file_path + ": " + str(e)

        req = urllib.request.Request(
            worker_url.rstrip("/") + "/" + filename,
            data=data, method="PUT",
        )
        req.add_header("Authorization", "Bearer " + upload_token)
        req.add_header("Content-Type", mime)
        req.add_header("User-Agent", "Mozilla/5.0")

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = resp.read().decode()
                result = _json.loads(body)
                url = result.get("url", "")
                if url:
                    return url, None
                return None, "Worker returned empty URL"
        except urllib.error.HTTPError as e:
            eb = e.read().decode()
            return None, "R2 upload HTTP " + str(e.code) + ": " + eb[:200]
        except Exception as e:
            return None, "R2 upload failed: " + str(e)

    # ─────────────────────────────────────────────────────────────
    # Tool: Seedream (AI via image_generate tool)
    # ─────────────────────────────────────────────────────────────

    def _seedream_available(self) -> bool:
        """Check if Seedream skill is available."""
        seedream_skill = os.path.expanduser("~/.openclaw/skills/byted-ark-seedream-skill/SKILL.md")
        return os.path.exists(seedream_skill)

    def _call_seedream(self, image_path: str = None, prompt: str = "",
                       reference_strength: float = 0.85,
                       output_path: str = None,
                       reference_images: list = None,
                       watermark: bool = False) -> tuple:
        """
        Call Seedream via its installed Node CLI (scripts/generate.js).

        The Seedream skill ships a single Node entry-point and emits a JSON
        envelope on stdout containing each generated image's local path.
        We parse that envelope, locate the first successful local file, and
        copy it to output_path so the caller sees a normal output file.

        Args:
            image_path:       Single reference image (legacy single-image path).
                               Kept for backward compatibility with op_remove_object
                               and op_restore. If `reference_images` is also given,
                               `reference_images` wins.
            prompt:           Generation prompt.
            reference_strength: 0..1, how strongly Seedream must preserve the
                               reference image(s).
            output_path:      Where to stage the final image.
            reference_images: Optional list of file paths. When given, this is
                               passed to Seedream's --reference_images as a
                               JSON-array of data URIs (Seedream's validator
                               only accepts HTTP URLs or base64 data URIs).
            watermark:        If True, pass --watermark true to Seedream.
                               Default False (most product / academic uses
                               should not be watermarked).

        Returns (success, output_path, error).
        """
        if not self._seedream_available():
            return False, None, (
                "Seedream skill not found. Install it from ClawHub:\n"
                "  openclaw skills install byted-ark-seedream-skill\n"
                "Or set up a Volcengine Ark account and configure ARK_API_KEY."
            ), None

        import base64
        import mimetypes
        import shutil
        import subprocess

        skill_dir = os.path.expanduser("~/.openclaw/skills/byted-ark-seedream-skill")
        generate_js = os.path.join(skill_dir, "scripts", "generate.js")
        if not os.path.exists(generate_js):
            return False, None, f"Seedream entry-point not found: {generate_js}", None

        # Resolve the final list of reference images.
        # Priority: explicit reference_images > single image_path > empty.
        if reference_images:
            ref_paths = list(reference_images)
        elif image_path:
            ref_paths = [image_path]
        else:
            return False, None, "No reference image provided", None

        for p in ref_paths:
            if not os.path.exists(p):
                return False, None, f"Reference image not found: {p}", None

        # Default output_path: derive from the first reference image if not given.
        if output_path is None:
            first = ref_paths[0]
            output_path = first.rsplit('.', 1)[0] + "_seedream.jpg"
        # Build reference image list for Seedream.
        # Strategy:
        #   small file (<1.5 MB) -> base64 data URI  (no extra round-trip)
        #   large file           -> upload to R2       (avoids CLI ARG_MAX limit)
        ref_arg_items = []
        for p in ref_paths:
            size = os.path.getsize(p)
            if size < self._R2_SIZE_THRESHOLD:
                mime, _ = mimetypes.guess_type(p)
                mime = mime or "image/jpeg"
                try:
                    with open(p, "rb") as fh:
                        b64 = base64.b64encode(fh.read()).decode("ascii")
                    ref_arg_items.append("data:" + mime + ";base64," + b64)
                except OSError as e:
                    return False, None, "Could not read reference image " + p + ": " + str(e), None
            else:
                url, err = self._r2_upload(p)
                if url:
                    ref_arg_items.append(url)
                else:
                    # R2 unavailable or failed — fall back to base64 data URI.
                    # This may exceed CLI arg limits for very large files, but
                    # it is better than hard-failing for users without R2.
                    import sys as _sys
                    print("Warning: R2 upload unavailable (" + str(err) + "), "
                          "falling back to data URI for " + p, file=_sys.stderr)
                    try:
                        with open(p, "rb") as fh:
                            b64 = base64.b64encode(fh.read()).decode("ascii")
                        ref_arg_items.append("data:" + mime + ";base64," + b64)
                    except OSError as e2:
                        return False, None, "Could not read " + p + ": " + str(e2), None
        ref_arg = json.dumps(ref_arg_items)

        cmd = [
            "node", generate_js,
            "--prompt", prompt,
            "--mode", "image-to-image",
            "--reference_images", ref_arg,
            "--reference_strength", str(reference_strength),
            "--optimize", "false",  # we already wrote a precise prompt
            "--watermark", "true" if watermark else "false",
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
                cwd=skill_dir,
            )
        except subprocess.TimeoutExpired:
            return False, None, "Seedream timeout (180s)", None
        except FileNotFoundError:
            return False, None, "`node` runtime not on PATH (Seedream needs Node 18+)", None
        except Exception as e:
            return False, None, f"Seedream invocation failed: {e}", None

        # Try to parse the JSON envelope first — Seedream emits it on stdout for
        # both success and failure paths. If parsing fails, fall back to the
        # last stderr line so the caller still sees a readable error.
        payload = None
        generation_time = None
        if result.stdout:
            try:
                payload = json.loads(result.stdout.strip())
            except (json.JSONDecodeError, ValueError):
                payload = None

        if result.returncode != 0 and not (payload and payload.get("success")):
            err_msg = (payload or {}).get("error")
            if not err_msg:
                tail = (result.stderr or "").strip().splitlines()
                err_msg = tail[-1].strip() if tail else "Seedream returned non-zero exit"
            return False, None, err_msg, None

        if not payload:
            return False, None, "Could not parse Seedream output (empty stdout)", None
        if not payload.get("success"):
            return False, None, payload.get("error") or "Seedream reported failure", None

        # Capture generation_time from metadata (for quota tracking).
        meta = payload.get("metadata") or {}
        if "generation_time" in meta:
            try:
                generation_time = float(meta["generation_time"])
            except (TypeError, ValueError):
                generation_time = None

        # Find the first successfully-downloaded local image.
        images = payload.get("images") or []
        local = next((img.get("local_path") for img in images
                      if img.get("download_success") and img.get("local_path")), None)
        if not local or not os.path.exists(local):
            return False, None, "Seedream produced no local image file", None

        # Guard against copying a file onto itself (would truncate to zero)
        if os.path.abspath(local) == os.path.abspath(output_path):
            return True, output_path, None, {"generation_time": generation_time}

        # Copy into the caller's requested output_path.
        try:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
            shutil.copyfile(local, output_path)
        except OSError as e:
            return False, None, f"Failed to stage Seedream output: {e}", None

        return True, output_path, None, {"generation_time": generation_time}

    # ─────────────────────────────────────────────────────────────
    # Operations
    # ─────────────────────────────────────────────────────────────

    def op_remove_object(self, image: str, prompt: str, output: str,
                         tool: str = "auto") -> bool:
        """Remove object using AI (Seedream) by default; fall back to a hint
        for the geometric-only inpaint.py path when Seedream is unavailable.

        Tool selection policy (`--tool auto`):
          1. Seedream first — it handles arbitrary natural-language object
             removal (people, vehicles, watermarks, complex scenes) and
             produces high-resolution AI-aware fills.
          2. OpenCV fallback — only when Seedream is not installed/available.
             For geometric primitives with known coordinates (wires, dust
             spots, exact rectangles) the user should call inpaint.py
             directly; this branch surfaces that hint so the unified entry
             still gives an actionable next step.

        Override with --tool seedream (force AI) or --tool opencv (force the
        inpaint.py redirect).
        """
        start = time.time()

        # Check input
        if not os.path.exists(image):
            return self._result(False, "remove-object", error=f"Input not found: {image}")

        # Validate prompt
        if not prompt or len(prompt.strip()) < 3:
            return self._result(False, "remove-object", error="Prompt too short")

        # Auto-route: Seedream first when available, else fall back to the
        # OpenCV/inpaint.py hint. Earlier versions tried to keyword-sniff the
        # prompt for words like "wire" or "cable" and route to OpenCV, but
        # the OpenCV branch is just a redirect to inpaint.py, so that
        # routing turned reasonable AI-suitable prompts into silent failures.
        if tool == "auto":
            tool = "seedream" if self._seedream_available() else "opencv"

        if tool == "seedream" and self._seedream_available():
            self._log(f"Using Seedream AI for object removal...")

            # Resize if needed
            working_img, was_resized = self._resize_for_api(image)

            success, result_path, error, _meta = self._call_seedream(
                working_img, prompt, reference_strength=0.85, output_path=output
            )

            self._cleanup_temp(working_img, was_resized)

            elapsed = int((time.time() - start) * 1000)
            return self._result(success, "remove-object", output=output,
                              elapsed_ms=elapsed, tool="seedream", error=error)

        elif tool == "opencv" and OPENCV_AVAILABLE:
            self._log("OpenCV object removal needs explicit geometry; redirecting to inpaint.py...")
            # Geometric primitives belong in inpaint.py (it accepts exact
            # coordinates). edit.py's --task remove-object is the AI path.
            return self._result(False, "remove-object", error=(
                "OpenCV object removal requires explicit geometry. "
                "For geometric primitives with known coordinates, call "
                "./scripts/inpaint.py directly (e.g. --type spot --x ... --y ..., "
                "--type wire --y ..., --type rect --x ... --y ... --w ... --h ...). "
                "For natural-language object removal, use --tool seedream "
                "(install the byted-ark-seedream-skill if missing)."
            ))

        else:
            return self._result(False, "remove-object", error=(
                "No suitable tool available. Install the Seedream skill for AI "
                "object removal, or use ./scripts/inpaint.py directly with "
                "explicit coordinates."
            ))

    def op_restore(self, image: str, output: str, prompt: str = None) -> bool:
        """Restore old photo using Seedream AI."""
        start = time.time()

        if not os.path.exists(image):
            return self._result(False, "restore", error=f"Input not found: {image}")

        if not self._seedream_available():
            return self._result(False, "restore", error=(
                "Seedream skill not found. Install from ClawHub:\n"
                "  openclaw skills install byted-ark-seedream-skill"
            ))

        default_prompt = (
            "Restore this old photo. Remove all scratches, dust spots, and damage. "
            "Enhance clarity and contrast. Restore natural, vivid colors while "
            "preserving the original photo's character. Do not change the composition."
        )
        prompt = prompt or default_prompt

        # Resize if needed
        working_img, was_resized = self._resize_for_api(image)

        success, result_path, error, _meta = self._call_seedream(
            working_img, prompt, reference_strength=0.7, output_path=output
        )

        self._cleanup_temp(working_img, was_resized)

        elapsed = int((time.time() - start) * 1000)
        return self._result(success, "restore", output=output,
                          elapsed_ms=elapsed, tool="seedream", error=error)

    # ─────────────────────────────────────────────────────────────
    # 11. Scene Replacement (Seedream multi-reference fusion)
    # ─────────────────────────────────────────────────────────────

    def op_replace_scene(self, subject: str, output: str,
                         scene: str = None, scene_prompt: str = None,
                         subject_type: str = "auto",
                         prompt: str = None,
                         reference_strength: float = None,
                         position: str = "center", scale: str = "medium",
                         watermark: bool = False,
                         output_format: str = None) -> bool:
        """
        Place a subject (portrait / pet / product) into a new scene using
        Seedream's multi-reference image fusion.

        Subject + (scene image OR scene text description) → composed output.

        Requires the byted-ark-seedream-skill. No deterministic fallback —
        scene replacement is fundamentally an AI task.

        Args:
            subject:           Path to the subject image.
            scene:             Path to the target scene image (mutually
                               exclusive with scene_prompt).
            scene_prompt:      Text description of the target scene
                               (mutually exclusive with scene).
            subject_type:      'auto' | 'portrait' | 'pet' | 'product'.
                               Selects the prompt template + reference_strength.
            prompt:            Override the default prompt built from the
                               template. If given, the template is ignored.
            reference_strength: 0..1, how strongly Seedream must preserve
                               the subject. Default depends on subject_type.
            position:          'left' | 'center' | 'right' (placement hint).
            scale:             'close' | 'medium' | 'full' (subject size).
            watermark:         Add Seedream watermark. Default False.
            output_format:     'jpeg' | 'png' | 'webp'. Default: follow
                               subject's file extension.
        """
        start = time.time()

        # ── Validate inputs ──────────────────────────────────────────
        if not subject or not os.path.exists(subject):
            return self._result(False, "replace-scene",
                                error=f"Subject not found: {subject}")

        if not self._seedream_available():
            return self._result(False, "replace-scene", error=(
                "replace-scene requires the byted-ark-seedream-skill.\n"
                "Install from ClawHub: openclaw skills install byted-ark-seedream-skill"
                "Install it first (see SKILL.md in that skill)."
            ))

        if scene and scene_prompt:
            return self._result(False, "replace-scene", error=(
                "Use only one of --scene <image> or --scene-prompt <description>, "
                "not both."
            ))
        if not scene and not scene_prompt:
            return self._result(False, "replace-scene", error=(
                "Provide either --scene <image> or --scene-prompt <description>."
            ))
        if scene_prompt and len(scene_prompt.strip()) < 3:
            return self._result(False, "replace-scene", error=(
                "--scene-prompt must be at least 3 characters."
            ))
        if scene and not os.path.exists(scene):
            return self._result(False, "replace-scene",
                                error=f"Scene image not found: {scene}")

        # ── Auto-detect subject_type if needed ──────────────────────
        if subject_type == "auto":
            subject_type = self._detect_subject_type(subject)
        if subject_type not in ("portrait", "pet", "product"):
            subject_type = "portrait"  # safe default

        # ── Resolve reference_strength if not given ────────────────
        if reference_strength is None:
            reference_strength = 0.90 if subject_type == "product" else 0.85
        reference_strength = max(0.0, min(1.0, reference_strength))

        # ── Build prompt from template (or use override) ──────────
        if not prompt:
            prompt = self._build_replace_scene_prompt(
                subject_type=subject_type,
                scene=scene,
                scene_prompt=scene_prompt,
                position=position,
                scale=scale,
            )

        # ── Build reference_images list (in order: subject, then scene) ──
        ref_paths = [subject]
        ref_working_paths = []  # for cleanup
        try:
            # Resize subject if needed (Seedream API limit ~2048px)
            subj_working, subj_resized = self._resize_for_api(subject)
            ref_paths[0] = subj_working
            if subj_resized:
                ref_working_paths.append(subj_working)

            if scene:
                scene_working, scene_resized = self._resize_for_api(scene)
                ref_paths.append(scene_working)
                if scene_resized:
                    ref_working_paths.append(scene_working)

            # ── Call Seedream ─────────────────────────────────────
            success, result_path, error, meta = self._call_seedream(
                prompt=prompt,
                reference_strength=reference_strength,
                output_path=output,
                reference_images=ref_paths,
                watermark=watermark,
            )
        finally:
            for p in ref_working_paths:
                self._cleanup_temp(p, was_temp=True)

        elapsed = int((time.time() - start) * 1000)

        info = {
            "subject_type": subject_type,
            "reference_strength": reference_strength,
            "position": position,
            "scale": scale,
            "watermark": watermark,
        }
        if meta and meta.get("generation_time") is not None:
            info["generation_time_s"] = meta["generation_time"]

        # ── Enforce output_format if specified ───────────────────────
        # Seedream always outputs a file (its default format). If the user
        # passed --output-format, convert the file to match.
        if success and output_format is not None and output:
            ext_map = {"jpeg": ".jpg", "png": ".png", "webp": ".webp"}
            expected_ext = ext_map.get(output_format.lower().replace("-", ""))
            if expected_ext and not output.lower().endswith(expected_ext):
                # Target extension differs → re-save with PIL in the right format
                if PIL_AVAILABLE:
                    try:
                        final_path = output.rsplit(".", 1)[0] + expected_ext
                        with Image.open(output) as img:
                            # PNG supports alpha; JPEG does not
                            if output_format.lower() in ("jpeg", "jpg"):
                                img = img.convert("RGB")
                            img.save(final_path)
                        # Remove the Seedream intermediate now that conversion succeeded
                        if os.path.exists(final_path):
                            os.remove(output)
                            output = final_path
                            info["output_format_applied"] = output_format
                    except Exception:
                        pass  # Non-fatal: return the original Seedream file

        return self._result(success, "replace-scene", output=output,
                            elapsed_ms=elapsed, tool="seedream",
                            error=error, **info)

    def _detect_subject_type(self, image_path: str) -> str:
        """
        Heuristic subject-type detection when user passes --subject-type auto.

        Strategy (in priority order):
        1. Filename keyword (pet/cat/dog/animal/portrait/selfie/headshot
           → pet or portrait; product/item/obj/thing → product)
        2. Background solidity check (PIL corner sampling) — flat
           single-color backgrounds typically indicate product photos
        3. Fall back to "portrait" (most common case)

        Heuristic, not a guarantee. Users can always pass --subject-type
        explicitly for certainty.
        """
        import re

        name = os.path.basename(image_path).lower()
        if re.search(r"(pet|cat|dog|kitten|puppy|animal|horse|rabbit|bird)", name):
            return "pet"
        if re.search(r"(portrait|selfie|headshot|face|person|people|human|avatar)", name):
            return "portrait"
        if re.search(r"(product|item|obj|object|merch|goods|sku|package|bottle|box)", name):
            return "product"

        # Try corner solidity check (PIL).
        if PIL_AVAILABLE:
            try:
                with Image.open(image_path) as img:
                    w, h = img.size
                    if w < 20 or h < 20:
                        return "portrait"
                    # Convert to RGB first so getpixel always returns (R,G,B)
                    # rather than a palette index for P-mode (palette) images.
                    img = img.convert("RGB")
                    corners = [
                        img.getpixel((5, 5)),
                        img.getpixel((w - 5, 5)),
                        img.getpixel((5, h - 5)),
                        img.getpixel((w - 5, h - 5)),
                    ]
                    # If all 4 corners are very similar (max color distance < 15),
                    # it's likely a product shot on a flat-color backdrop.
                    max_dist = 0
                    for i in range(len(corners)):
                        for j in range(i + 1, len(corners)):
                            c1 = corners[i][:3]
                            c2 = corners[j][:3]
                            d = max(abs(a - b) for a, b in zip(c1, c2))
                            max_dist = max(max_dist, d)
                    if max_dist < 15:
                        return "product"
            except Exception:
                pass

        return "portrait"  # safe default

    def _build_replace_scene_prompt(self, subject_type: str, scene: str,
                                    scene_prompt: str, position: str,
                                    scale: str) -> str:
        """Build the default prompt for a given subject type + scene input."""

        if scene:
            scene_ref = "Image 2"
        else:
            scene_ref = f'the following scene: "{scene_prompt}"'

        position_map = {
            "left": "slightly left of center",
            "center": "at center",
            "right": "slightly right of center",
        }
        scale_map = {
            "close": "in close-up",
            "medium": "as a medium shot",
            "full": "as a full-body figure",
        }
        pos_hint = position_map.get(position, position_map["center"])
        scale_hint = scale_map.get(scale, scale_map["medium"])

        if subject_type == "product":
            return (
                f"Place the product from Image 1 into the usage scene from "
                f"{scene_ref}. Preserve the product's exact appearance, "
                f"branding, label text, and surface details. Adapt the "
                f"lighting to match the scene naturally — the product "
                f"should appear as if physically present, with realistic "
                f"shadows, reflections, and contact. Do not distort the "
                f"product, warp its shape, or change its branding. "
                f"Position the product {pos_hint} at {scale_hint}."
            )

        # portrait and pet share a template
        subject_noun = {
            "portrait": "person",
            "pet": "animal",
        }.get(subject_type, "subject")

        return (
            f"Place the {subject_noun} from Image 1 naturally into the "
            f"scene from {scene_ref}. Preserve the subject's exact "
            f"appearance, features, and identity. Match the scene's "
            f"lighting direction, color temperature, and perspective. "
            f"Keep the subject sharp with subtle edge blending. Do not "
            f"alter the subject's pose or expression. "
            f"Position the subject {pos_hint}. Frame the subject at "
            f"{scale_hint} in the final composition."
        )

    def op_remove_background(self, image: str, output: str,
                             tool: str = "auto") -> bool:
        """Remove background using rembg or ImageMagick."""
        start = time.time()

        if not os.path.exists(image):
            return self._result(False, "remove-background", error=f"Input not found: {image}")

        # Method 1: rembg (AI)
        rembg_cmd = None
        # Build rembg candidates: try PATH first, then venv-relative path
        venv_rembg = self.venv_python.replace("/bin/python", "/bin/rembg")
        for cmd_candidate in ["rembg", venv_rembg]:
            try:
                subprocess.run([cmd_candidate, "--help"],
                             capture_output=True, timeout=5)
                rembg_cmd = cmd_candidate
                break
            except (subprocess.TimeoutExpired, OSError, FileNotFoundError):
                pass

        if rembg_cmd and tool in ("auto", "rembg"):
            try:
                self._log("Using rembg for background removal...")
                result = subprocess.run(
                    [rembg_cmd, "i", image, output],
                    capture_output=True, text=True, timeout=60
                )
                if result.returncode == 0:
                    elapsed = int((time.time() - start) * 1000)
                    return self._result(True, "remove-background", output=output,
                                      elapsed_ms=elapsed, tool="rembg")
                else:
                    self._warn(f"rembg failed: {result.stderr}")
            except Exception as e:
                self._warn(f"rembg error: {e}")

        # Method 2: ImageMagick (solid backgrounds)
        im_cmd = None
        for cmd_candidate in ["magick", "convert"]:
            try:
                subprocess.run([cmd_candidate, "--version"],
                             capture_output=True, timeout=5)
                im_cmd = cmd_candidate
                break
            except (subprocess.TimeoutExpired, OSError):
                pass

        if im_cmd and tool in ("auto", "imagemagick"):
            try:
                self._log("Using ImageMagick for background removal...")
                # Auto-detect background color from corners and make it transparent
                if PIL_AVAILABLE:
                    with Image.open(image) as img:
                        w, h = img.size
                        corners = [
                            img.getpixel((5, 5)),
                            img.getpixel((w-5, 5)),
                            img.getpixel((5, h-5)),
                            img.getpixel((w-5, h-5)),
                        ]
                        from collections import Counter
                        bg_color = Counter(corners).most_common(1)[0][0]
                        if len(bg_color) == 4:
                            bg_color = bg_color[:3]
                        bg_hex = '#%02x%02x%02x' % bg_color

                    # Make detected background color transparent
                    result = subprocess.run(
                        [im_cmd, image, "-fuzz", "20%", "-transparent", bg_hex, output],
                        capture_output=True, text=True, timeout=30
                    )
                    if result.returncode == 0:
                        elapsed = int((time.time() - start) * 1000)
                        return self._result(True, "remove-background", output=output,
                                          elapsed_ms=elapsed, tool="imagemagick-transparent")
            except Exception as e:
                self._warn(f"ImageMagick error: {e}")

        elapsed = int((time.time() - start) * 1000)
        return self._result(False, "remove-background", elapsed_ms=elapsed, error=
            "No background removal tool available. Install rembg: "
            "pip install rembg")

    def op_resize(self, image: str, output: str,
                  width: int = None, height: int = None,
                  max_dim: int = None, maintain_aspect: bool = True) -> bool:
        """Resize image using ImageMagick or OpenCV."""
        start = time.time()

        if not os.path.exists(image):
            return self._result(False, "resize", error=f"Input not found: {image}")

        if not width and not height and not max_dim:
            return self._result(False, "resize", error="Specify width, height, or max_dim")

        # Use ImageMagick
        im_cmd = None
        for cmd_candidate in ["magick", "convert"]:
            try:
                subprocess.run([cmd_candidate, "--version"],
                             capture_output=True, timeout=5)
                im_cmd = cmd_candidate
                break
            except (subprocess.TimeoutExpired, OSError):
                pass

        if im_cmd:
            try:
                args = [im_cmd, image]

                if max_dim:
                    if maintain_aspect:
                        args.extend(["-resize", f"{max_dim}x{max_dim}>"])
                    else:
                        args.extend(["-resize", f"{max_dim}x{max_dim}!"])
                else:
                    if maintain_aspect:
                        if width and height:
                            args.extend(["-resize", f"{width}x{height}>"])
                        elif width:
                            args.extend(["-resize", str(width)])
                        else:
                            args.extend(["-resize", f"x{height}"])
                    else:
                        if width and height:
                            args.extend(["-resize", f"{width}x{height}!"])
                        elif width:
                            args.extend(["-resize", f"{width}x{width}!"])
                        else:
                            args.extend(["-resize", f"x{height}x{height}!"])

                args.append(output)

                result = subprocess.run(
                    args,
                    capture_output=True, text=True, timeout=30
                )

                if result.returncode == 0:
                    elapsed = int((time.time() - start) * 1000)
                    return self._result(True, "resize", output=output,
                                      elapsed_ms=elapsed, tool="imagemagick")
            except Exception as e:
                pass

        # Fallback to OpenCV
        if OPENCV_AVAILABLE:
            try:
                img = cv2.imread(image)
                h, w = img.shape[:2]

                if max_dim:
                    if max(w, h) > max_dim:
                        scale = max_dim / max(w, h)
                        new_w, new_h = int(w * scale), int(h * scale)
                        img = cv2.resize(img, (new_w, new_h))
                elif width and height:
                    if maintain_aspect:
                        img = cv2.resize(img, (width, height),
                                       interpolation=cv2.INTER_AREA)
                    else:
                        img = cv2.resize(img, (width, height))
                elif width:
                    scale = width / w
                    img = cv2.resize(img, (width, int(h * scale)))
                elif height:
                    scale = height / h
                    img = cv2.resize(img, (int(w * scale), height))

                cv2.imwrite(output, img)
                elapsed = int((time.time() - start) * 1000)
                return self._result(True, "resize", output=output,
                                  elapsed_ms=elapsed, tool="opencv")
            except Exception as e:
                return self._result(False, "resize", error=str(e))

        return self._result(False, "resize", error="No resize tool available")

    def op_crop(self, image: str, output: str,
                x: int = None, y: int = None,
                width: int = None, height: int = None) -> bool:
        """Crop image using ImageMagick or OpenCV."""
        start = time.time()

        if not os.path.exists(image):
            return self._result(False, "crop", error=f"Input not found: {image}")

        if None in (x, y, width, height):
            return self._result(False, "crop", error="Specify x, y, width, height")

        # Use ImageMagick
        im_cmd = None
        for cmd_candidate in ["magick", "convert"]:
            try:
                subprocess.run([cmd_candidate, "--version"],
                             capture_output=True, timeout=5)
                im_cmd = cmd_candidate
                break
            except (subprocess.TimeoutExpired, OSError):
                pass

        if im_cmd:
            try:
                result = subprocess.run(
                    [im_cmd, image, "-crop", f"{width}x{height}+{x}+{y}",
                     "+repage", output],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    elapsed = int((time.time() - start) * 1000)
                    return self._result(True, "crop", output=output,
                                      elapsed_ms=elapsed, tool="imagemagick")
            except Exception as e:
                pass

        # Fallback to OpenCV
        if OPENCV_AVAILABLE:
            try:
                img = cv2.imread(image)
                h, w = img.shape[:2]

                x1, y1 = max(0, min(x, w-1)), max(0, min(y, h-1))
                x2, y2 = min(x + width, w), min(y + height, h)

                cropped = img[y1:y2, x1:x2]
                cv2.imwrite(output, cropped)

                elapsed = int((time.time() - start) * 1000)
                return self._result(True, "crop", output=output,
                                  elapsed_ms=elapsed, tool="opencv")
            except Exception as e:
                return self._result(False, "crop", error=str(e))

        return self._result(False, "crop", error="No crop tool available")

    def op_color_adjust(self, image: str, output: str,
                        brightness: float = None,
                        contrast: float = None,
                        saturation: float = None,
                        grayscale: bool = False) -> bool:
        """Adjust color using ImageMagick."""
        start = time.time()

        if not os.path.exists(image):
            return self._result(False, "color-adjust", error=f"Input not found: {image}")

        im_cmd = None
        for cmd_candidate in ["magick", "convert"]:
            try:
                subprocess.run([cmd_candidate, "--version"],
                             capture_output=True, timeout=5)
                im_cmd = cmd_candidate
                break
            except (subprocess.TimeoutExpired, OSError):
                pass

        if not im_cmd:
            return self._result(False, "color-adjust", error="ImageMagick not found")

        try:
            args = [im_cmd, image]

            if grayscale:
                args.extend(["-colorspace", "Gray"])

            if saturation is not None:
                # Modulate: brightness,saturation,hue
                # 100 = no change, >100 = increase
                sat_val = 100 + (saturation * 100) if saturation != 0 else 100
                args.extend(["-modulate", f"100,{sat_val},100"])

            if brightness is not None or contrast is not None:
                # Brightness: -100 to 100 (0 = no change)
                # Contrast: -100 to 100 (0 = no change)
                b = brightness if brightness is not None else 0
                c = contrast if contrast is not None else 0
                args.extend(["-brightness-contrast", f"{b}x{c}"])

            args.append(output)

            result = subprocess.run(args, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                elapsed = int((time.time() - start) * 1000)
                return self._result(True, "color-adjust", output=output,
                                  elapsed_ms=elapsed, tool="imagemagick")
            else:
                return self._result(False, "color-adjust", error=result.stderr)

        except Exception as e:
            return self._result(False, "color-adjust", error=str(e))

    # ─────────────────────────────────────────────────────────────
    # 7. Perspective Correction
    # ─────────────────────────────────────────────────────────────

    def op_perspective_correct(self, image: str, output: str,
                                corners: str = None,
                                **kwargs) -> bool:
        """
        Auto-detect and correct perspective distortion (e.g. document scan).

        Args:
            corners: Optional CSV of 8 ints: x1,y1,x2,y2,x3,y3,x4,y4
                     (top-left, top-right, bottom-right, bottom-left).
                     If omitted, auto-detects largest quadrilateral.
        """
        if not OPENCV_AVAILABLE:
            return self._result(False, "perspective-correct",
                                error="OpenCV not available")

        valid, resolved, err = self._check_image(image)
        if not valid:
            return self._result(False, "perspective-correct", error=err)

        try:
            img = cv2.imread(resolved)
            if img is None:
                return self._result(False, "perspective-correct",
                                    error=f"Could not read: {image}")

            h, w = img.shape[:2]
            src_pts = None

            if corners:
                # Manual corners provided as "x1,y1,x2,y2,x3,y3,x4,y4"
                try:
                    coords = [int(x.strip()) for x in corners.split(",")]
                    if len(coords) != 8:
                        raise ValueError()
                    src_pts = np.array([
                        [coords[0], coords[1]],
                        [coords[2], coords[3]],
                        [coords[4], coords[5]],
                        [coords[6], coords[7]],
                    ], dtype='float32')
                except Exception:
                    return self._result(False, "perspective-correct",
                                        error="Invalid corners format; expected 8 CSV ints")
            else:
                # Auto-detect document border via edge detection + contour analysis
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Blur to reduce noise
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                # Adaptive threshold for document-like contrast
                thresh = cv2.adaptiveThreshold(
                    blurred, 255,
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY, 11, 2
                )
                # Morphological close to join edges
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

                contours, _ = cv2.findContours(
                    thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
                )

                # Sort by area, keep largest quadrilaterals
                contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

                best_cnt = None
                for cnt in contours:
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                    if len(approx) == 4 and cv2.contourArea(approx) > (w * h * 0.05):
                        best_cnt = approx
                        break

                if best_cnt is None:
                    return self._result(False, "perspective-correct",
                                        error="No document-like quadrilateral detected. "
                                               "Try specifying corners manually.")

                # Order points: TL, TR, BR, BL
                def order_pts(pts):
                    pts = pts.reshape(4, 2)
                    s = pts.sum(axis=1)
                    tl, br = pts[np.argmin(s)], pts[np.argmax(s)]
                    diff = np.diff(pts, axis=1)
                    tr = pts[np.argmin(diff)]
                    bl = pts[np.argmax(diff)]
                    return np.array([tl, tr, br, bl], dtype='float32')

                src_pts = order_pts(best_cnt)

            # Compute output dimensions based on detected edges
            (tl, tr, br, bl) = src_pts
            max_width = int(max(np.linalg.norm(tr - tl), np.linalg.norm(bl - br)))
            max_height = int(max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl)))

            dst_pts = np.array([
                [0, 0],
                [max_width - 1, 0],
                [max_width - 1, max_height - 1],
                [0, max_height - 1],
            ], dtype='float32')

            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            corrected = cv2.warpPerspective(img, M, (max_width, max_height),
                                            borderMode=cv2.BORDER_REPLICATE)

            cv2.imwrite(output, corrected)
            elapsed = 0  # placeholder
            return self._result(True, "perspective-correct", output=output,
                                elapsed_ms=elapsed)

        except Exception as e:
            return self._result(False, "perspective-correct", error=str(e))

    # ─────────────────────────────────────────────────────────────
    # 8. Intelligent / Smart Compression
    # ─────────────────────────────────────────────────────────────

    def op_smart_compress(self, image: str, output: str,
                          target_kb: int = None,
                          quality: int = None,
                          format: str = None,
                          **kwargs) -> bool:
        """
        Intelligently compress an image with content-aware quality selection.

        Uses image entropy, edge density, and color variance to choose the
        best format (JPEG/PNG/WebP) and quality level.

        Args:
            target_kb:  Target file size in KB (approximate).
            quality:    Manual quality 1-100 (overrides auto-decision).
            format:     Force output format: jpeg | png | webp.
        """
        if not OPENCV_AVAILABLE:
            return self._result(False, "smart-compress",
                                error="OpenCV not available")

        valid, resolved, err = self._check_image(image)
        if not valid:
            return self._result(False, "smart-compress", error=err)

        try:
            img = cv2.imread(resolved)
            if img is None:
                return self._result(False, "smart-compress",
                                    error=f"Could not read: {image}")

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            h, w = img.shape[:2]

            # ── Feature extraction for content analysis ──────────────

            # 1. Entropy (information complexity)
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            hist = hist.flatten() / hist.sum()
            entropy = -np.sum(hist * np.log2(hist + 1e-10))

            # 2. Edge density (high edges → needs JPEG quality)
            edges = cv2.Canny(gray, 50, 150)
            edge_density = edges.sum() / (h * w * 255)

            # 3. Color variance (photos vs graphics)
            channels = cv2.split(img)
            color_var = np.mean([np.var(c) for c in channels])

            # ── Format selection ────────────────────────────────────
            if format is None:
                has_alpha = img.shape[2] == 4 if len(img.shape) == 3 else False
                if has_alpha:
                    fmt = "png"
                elif entropy > 6.5 and edge_density > 0.08:
                    # Complex photo: JPEG
                    fmt = "jpeg"
                elif color_var < 500 and edge_density < 0.05:
                    # Flat/vector-like graphic: PNG
                    fmt = "png"
                else:
                    fmt = "jpeg"  # default
            else:
                fmt = format.lower().replace("-", "")
                if fmt not in ("jpeg", "png", "webp"):
                    return self._result(False, "smart-compress",
                                        error=f"Unsupported format: {format}")

            # ── Quality selection ────────────────────────────────────
            if quality is None:
                if target_kb:
                    # Binary search quality to hit target KB
                    lo, hi = 10, 100
                    best_q, best_size = 85, float("inf")
                    # Use a real format extension on the probe file so cv2.imwrite
                    # can pick the correct codec (it infers format from the suffix).
                    probe_ext = {"jpeg": ".jpg", "png": ".png", "webp": ".webp"}.get(fmt, ".jpg")
                    for _ in range(6):  # 6 iterations ≈ 1% precision
                        mid = (lo + hi) // 2
                        tmp_path = output + f".q{mid}{probe_ext}"
                        ok = self._save_with_quality(img, tmp_path, fmt, mid)
                        if not ok or not os.path.exists(tmp_path):
                            # Probe write failed; bail out of the search and
                            # fall back to a sensible default quality.
                            best_q, best_size = 85, 0
                            break
                        size_kb = os.path.getsize(tmp_path) // 1024
                        try:
                            os.remove(tmp_path)
                        except OSError:
                            pass
                        if abs(size_kb - target_kb) < abs(best_size - target_kb):
                            best_q, best_size = mid, size_kb
                        if size_kb > target_kb:
                            hi = mid - 1
                        else:
                            lo = mid + 1
                    quality = best_q
                else:
                    # Auto quality based on content complexity
                    if entropy > 7.0:
                        quality = 92
                    elif entropy > 5.5:
                        quality = 85
                    elif entropy > 3.5:
                        quality = 75
                    else:
                        quality = 65

            # ── Save ─────────────────────────────────────────────────
            if fmt == "jpeg":
                ext = ".jpg"
            elif fmt == "png":
                ext = ".png"
            else:
                ext = ".webp"

            out_path = output if output else \
                os.path.splitext(image)[0] + f".{fmt}_q{quality}" + ext

            saved_ok = self._save_with_quality(img, out_path, fmt, quality)
            if not saved_ok:
                return self._result(False, "smart-compress",
                                    error=f"Failed to save {fmt} image")

            size_kb = os.path.getsize(out_path) // 1024
            return self._result(True, "smart-compress", output=out_path,
                                elapsed_ms=0,
                                info={
                                    "format": fmt,
                                    "quality": quality,
                                    "entropy": round(float(entropy), 2),
                                    "edge_density": round(float(edge_density), 3),
                                    "size_kb": size_kb,
                                    "dimensions": f"{w}x{h}"
                                })

        except Exception as e:
            return self._result(False, "smart-compress", error=str(e))

    # ─────────────────────────────────────────────────────────────
    # 10. HDR / Tonemapping
    # ─────────────────────────────────────────────────────────────

    def op_hdr_tonemap(self, image: str, output: str,
                       mode: str = "auto",
                       strength: float = None,
                       gamma: float = None,
                       **kwargs) -> bool:
        """
        HDR-style tone mapping to enhance dynamic range on single images.

        Applies multi-scale tone mapping using bilateral-filter decomposition:
        decomposes the image into a base layer (illumination) and detail layer,
        compresses the base layer's dynamic range, then recombines.

        Also supports shadow/highlight recovery as an alternative mode.

        Args:
            mode:       "auto" | "bilateral" | "log" | "shadows" | "highlight"
                        auto = bilateral (detail-preserving) for most images
            strength:   Compression/enhancement strength 0.1–2.0 (default 1.0)
            gamma:      Gamma for log mode (default 2.2)
        """
        if not OPENCV_AVAILABLE:
            return self._result(False, "hdr-tonemap",
                                error="OpenCV not available")

        valid, resolved, err = self._check_image(image)
        if not valid:
            return self._result(False, "hdr-tonemap", error=err)

        try:
            img = cv2.imread(resolved)
            if img is None:
                return self._result(False, "hdr-tonemap",
                                    error=f"Could not read: {image}")

            if img.dtype != np.dtype('float32'):
                img = img.astype('float32')

            # Auto-select mode based on image characteristics
            if mode == "auto":
                gray = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2GRAY)
                # High contrast range → bilateral; otherwise log
                dark_pct = (gray < 50).sum() / gray.size
                bright_pct = (gray > 200).sum() / gray.size
                has_shadow = dark_pct > 0.05
                has_highlight = bright_pct > 0.05
                if has_shadow and has_highlight:
                    mode = "bilateral"
                elif has_shadow:
                    mode = "shadows"
                elif has_highlight:
                    mode = "highlight"
                else:
                    mode = "bilateral"

            strength = strength if strength is not None else 1.0
            strength = max(0.1, min(2.0, strength))
            gamma = gamma if gamma is not None else 2.2

            if mode == "bilateral":
                # Multi-scale bilateral decomposition tone mapping
                result = self._tonemap_bilateral(img, strength)

            elif mode == "log":
                # Log-domain tone mapping (fast, global)
                result = self._tonemap_log(img, gamma, strength)

            elif mode == "shadows":
                # Shadow recovery: lighten shadows, preserve highlights
                result = self._tonemap_shadows(img, strength)

            elif mode == "highlight":
                # Highlight recovery: compress highlights, preserve shadows
                result = self._tonemap_highlights(img, strength)

            else:
                return self._result(False, "hdr-tonemap",
                                    error=f"Unknown mode: {mode}")

            # Clip and convert back to uint8
            result = np.clip(result, 0, 255).astype(np.uint8)

            cv2.imwrite(output, result)
            return self._result(True, "hdr-tonemap", output=output,
                                elapsed_ms=0,
                                info={"mode": mode, "strength": strength})

        except Exception as e:
            return self._result(False, "hdr-tonemap", error=str(e))

    def _tonemap_bilateral(self, img: np.ndarray, strength: float) -> np.ndarray:
        """
        Multi-scale bilateral tone mapping.

        Decomposes into base/detail using bilateral filter.
        Compresses base (illumination) layer, preserves detail layer.
        """
        # Normalize to [0, 1]
        img_norm = img / 255.0

        # Estimate illumination with bilateral filter (edge-preserving blur)
        # Using large sigmaColor to capture global illumination structure
        base = np.zeros_like(img_norm)
        for c in range(img_norm.shape[2]):
            base[:, :, c] = cv2.bilateralFilter(
                img_norm[:, :, c].astype('float32'),
                d=9,
                sigmaColor=0.05 * 255,
                sigmaSpace=9
            )

        # Detail layer = original - base
        detail = img_norm - base

        # Compress base layer with S-curve
        k = 6.0 * strength  # stronger = more compression
        base_compressed = 1.0 / (1.0 + np.exp(-k * (base - 0.5)))
        blend = min(strength, 1.0)
        base_compressed = base * (1 - blend) + base_compressed * blend

        result = base_compressed + detail * strength

        # Adaptive saturation boost via proper BGR→HSV conversion
        result_uint8 = np.clip(result * 255.0, 0, 255).astype(np.uint8)
        hsv = cv2.cvtColor(result_uint8, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        # Boost saturation slightly (10–15%)
        s = np.clip(s.astype(np.float32) * 1.12, 0, 255).astype(np.uint8)
        hsv = cv2.merge([h, s, v])
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR).astype(np.float32) / 255.0

        return result * 255.0

    def _tonemap_log(self, img: np.ndarray, gamma: float, strength: float) -> np.ndarray:
        """Log-domain tone mapping: compress dynamic range in log space."""
        img_norm = img / 255.0
        # Avoid log(0)
        img_safe = np.clip(img_norm, 1e-8, 1.0)
        log_img = np.log10(img_safe + 1)
        log_max = np.log10(1.0 + 1)
        log_min = np.log10(1.0 + 1e-8)
        # Normalize log to [0, 1]
        log_norm = (log_img - log_min) / (log_max - log_min + 1e-10)
        # Apply gamma curve
        gamma_inv = 1.0 / max(gamma, 0.1)
        log_gamma = np.power(log_norm, gamma_inv)
        # Compress back and restore
        result = log_gamma * 255.0
        return np.clip(result, 0, 255)

    def _tonemap_shadows(self, img: np.ndarray, strength: float) -> np.ndarray:
        """Shadow recovery: lighten dark regions, preserve highlights."""
        img_norm = img / 255.0
        # CLAHE on luminance
        lab = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0 * strength,
                                tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return result.astype(np.float32)

    def _tonemap_highlights(self, img: np.ndarray, strength: float) -> np.ndarray:
        """Highlight recovery: compress blown highlights, preserve shadows."""
        img_norm = img / 255.0
        # Invert, apply shadow recovery, invert back
        inv = 1.0 - img_norm
        inv_bgr = (inv * 255).astype(np.uint8)
        lab = cv2.cvtColor(inv_bgr, cv2.COLOR_BGR2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0 * strength,
                                tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        recovered = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        result = 255.0 - recovered.astype(np.float32)
        return np.clip(result, 0, 255)

    def _save_with_quality(self, img: np.ndarray, path: str,
                           fmt: str, quality: int) -> bool:
        """Save image with format-specific quality settings."""
        try:
            # Derive actual format from file extension to avoid codec/params
            # mismatch (e.g. user gives --output foo.webp but --format png).
            ext = os.path.splitext(path)[1].lower().lstrip(".")
            ext_to_fmt = {"jpg": "jpeg", "jpeg": "jpeg",
                          "png": "png", "webp": "webp"}
            actual_fmt = ext_to_fmt.get(ext, fmt)

            if actual_fmt == "jpeg":
                params = [cv2.IMWRITE_JPEG_QUALITY, quality]
            elif actual_fmt == "png":
                # PNG compression level: 0=none … 9=maximum
                png_quality = max(0, min(9, 9 - int(quality / 12)))
                params = [cv2.IMWRITE_PNG_COMPRESSION, png_quality]
            elif actual_fmt == "webp":
                params = [cv2.IMWRITE_WEBP_QUALITY, quality]
            else:
                params = []

            ok = cv2.imwrite(path, img, params)
            return ok
        except Exception:
            return False

    # ─────────────────────────────────────────────────────────────
    # Dispatch
    # ─────────────────────────────────────────────────────────────

    def process(self, task: str, image: str = None, output: str = None,
                prompt: str = None, tool: str = "auto",
                subject: str = None, scene: str = None, scene_prompt: str = None,
                subject_type: str = "auto",
                reference_strength: float = None,
                position: str = "center", scale: str = "medium",
                watermark: bool = False, output_format: str = None,
                **kwargs) -> bool:
        """Process a single editing task.

        Most tasks use `image=` as the primary input. The `replace-scene`
        task uses `subject=` (and accepts `image=` as a synonym for
        backward compat with batch input).
        """
        # replace-scene: 'subject' is the primary input; fall back to 'image'
        if task == "replace-scene":
            primary = subject or image
            if not primary:
                return self._result(False, task, error=(
                    "replace-scene requires --subject <image>."
                ))
            return self.op_replace_scene(
                subject=primary, output=output, scene=scene,
                scene_prompt=scene_prompt, subject_type=subject_type,
                prompt=prompt, reference_strength=reference_strength,
                position=position, scale=scale,
                watermark=watermark, output_format=output_format,
            )

        # All other tasks: `image` is required (existing path).
        if not image:
            return self._result(False, task, error=(
                f"--image is required for task '{task}'."
            ))

        # JSON batch goes through process_batch, which normalizes dashed
        # keys (--scene-prompt → scene_prompt). The no-maintain-aspect
        # flag has inverted semantics (presence=True means maintain=False);
        # CLI's main() does this translation explicitly. Mirror it here so
        # JSON batch behaves identically. We also pop the original key from
        # kwargs so it doesn't leak into op_resize as an unexpected kwarg.
        if kwargs.get("no_maintain_aspect"):
            kwargs["maintain_aspect"] = False
            kwargs.pop("no_maintain_aspect", None)

        # Validate input path
        valid, resolved, err = self._validate_path(image, must_exist=True)
        if not valid:
            return self._result(False, task, error=err)

        # Validate output path
        if output:
            valid, resolved, err = self._validate_path(output, must_exist=False)
            if not valid:
                return self._result(False, task, error=err)

        # Default output: input_name.task.jpg
        if output is None:
            base = os.path.splitext(image)[0]
            ext = os.path.splitext(image)[1] or ".jpg"
            output = f"{base}.{task}{ext}"

        # Route to operation
        if task == "remove-object":
            return self.op_remove_object(image, prompt, output, tool)
        elif task == "restore":
            return self.op_restore(image, output, prompt)
        elif task == "remove-background":
            return self.op_remove_background(image, output, tool)
        elif task == "resize":
            return self.op_resize(image, output, **kwargs)
        elif task == "crop":
            return self.op_crop(image, output, **kwargs)
        elif task == "color-adjust":
            return self.op_color_adjust(image, output, **kwargs)
        elif task == "perspective-correct":
            return self.op_perspective_correct(image, output, **kwargs)
        elif task == "smart-compress":
            return self.op_smart_compress(image, output, **kwargs)
        elif task == "hdr-tonemap":
            return self.op_hdr_tonemap(image, output, **kwargs)
        else:
            return self._result(False, task, error=f"Unknown task: {task}")

    def process_batch(self, operations: List[Dict]) -> Dict:
        """Process multiple operations."""
        total_start = time.time()
        success_count = 0
        failure_count = 0

        for op in operations:
            op_name = op.get("task", "unknown")
            # Normalize dashed keys: CLI uses --scene-prompt / --target-kb /
            # --no-maintain-aspect / --subject-type (with dashes), but the
            # function signatures accept Python identifiers (underscores).
            # Without this normalization, **op would silently drop dashed
            # keys into the trailing **kwargs and the real parameter would
            # receive its default value — a very confusing failure mode.
            normalized = {k.replace('-', '_'): v for k, v in op.items()}
            success = self.process(**normalized)
            if success:
                success_count += 1
            else:
                failure_count += 1

        total_elapsed = int((time.time() - total_start) * 1000)

        summary = {
            "total": len(operations),
            "success": success_count,
            "failed": failure_count,
            "total_elapsed_ms": total_elapsed
        }

        if self.json_output:
            print(json.dumps(summary), file=sys.stdout)
        else:
            print(f"\n{'='*50}", file=sys.stderr)
            print(f"Batch complete: {success_count}/{len(operations)} succeeded "
                  f"in {total_elapsed}ms", file=sys.stderr)

        return summary


def main():
    parser = argparse.ArgumentParser(
        description="Smart Photo Editor - Unified photo editing tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --task remove-object --image photo.jpg --prompt "Remove the person" --output out.jpg
  %(prog)s --task restore --image old.jpg --output restored.jpg
  %(prog)s --task remove-background --image portrait.png --output no_bg.png
  %(prog)s --task resize --image photo.jpg --output small.jpg --width 800
  %(prog)s --task crop --image photo.jpg --output crop.jpg --x 100 --y 100 --width 400 --height 300
  %(prog)s --task color-adjust --image photo.jpg --output bright.jpg --brightness 20 --saturation 30
  %(prog)s --task perspective-correct --image doc.jpg --output flat.jpg
  %(prog)s --task perspective-correct --image doc.jpg --output flat.jpg --corners "100,50,600,50,600,800,100,800"
  %(prog)s --task smart-compress --image photo.jpg --output optimized.jpg
  %(prog)s --task smart-compress --image photo.jpg --output optimized.jpg --target-kb 200
  %(prog)s --task smart-compress --image photo.jpg --output optimized.webp --format webp --quality 85
  %(prog)s --task hdr-tonemap --image photo.jpg --output hdr_enhanced.jpg
  %(prog)s --task hdr-tonemap --image photo.jpg --output hdr_enhanced.jpg --mode bilateral --strength 1.2
  %(prog)s --task hdr-tonemap --image photo.jpg --output hdr_enhanced.jpg --mode shadows
  %(prog)s --json < tasks.json   # Batch mode from JSON file
  %(prog)s --json --batch tasks.json
        """
    )

    parser.add_argument("--task", choices=[
        "remove-object", "remove-background", "restore",
        "resize", "crop", "color-adjust",
        "perspective-correct", "smart-compress", "hdr-tonemap",
        "replace-scene"
    ], help="Editing task type")
    parser.add_argument("--image", "-i", help="Input image path (or subject image for replace-scene)")
    parser.add_argument("--subject", "-S",
                       help="Subject image path (replace-scene only). Overrides --image for this task.")
    parser.add_argument("--scene",
                       help="Target scene image path (replace-scene only). Mutually exclusive with --scene-prompt.")
    parser.add_argument("--scene-prompt",
                       help="Target scene text description (replace-scene only). Mutually exclusive with --scene.")
    parser.add_argument("--subject-type",
                       choices=["auto", "portrait", "pet", "product"],
                       default="auto",
                       help="Subject type (replace-scene only). Selects prompt template + reference_strength.")
    parser.add_argument("--reference-strength", type=float,
                       help="Subject preservation strength 0.0-1.0 (replace-scene; default depends on --subject-type)")
    parser.add_argument("--position",
                       choices=["left", "center", "right"],
                       default="center",
                       help="Subject placement hint (replace-scene only)")
    parser.add_argument("--scale",
                       choices=["close", "medium", "full"],
                       default="medium",
                       help="Subject size hint (replace-scene only)")
    parser.add_argument("--watermark", action="store_true",
                       help="Add Seedream watermark (replace-scene only, default OFF)")
    parser.add_argument("--output-format",
                       choices=["jpeg", "png", "webp"],
                       help="Output format (replace-scene only, default: follow subject extension)")
    parser.add_argument("--output", "-o", help="Output image path")
    parser.add_argument("--prompt", "-p", help="Description/prompt for AI operations")
    parser.add_argument("--tool", "-t", default="auto",
                       choices=["auto", "seedream", "opencv", "imagemagick", "rembg"],
                       help="Force specific tool (default: auto)")

    # Resize/crop options
    parser.add_argument("--width", "-w", type=int, help="Target width")
    parser.add_argument("--height", "-H", type=int, help="Target height")
    parser.add_argument("--max-dim", type=int, help="Max dimension (maintains aspect)")
    parser.add_argument("--no-maintain-aspect", action="store_true",
                       help="Allow stretching/distortion during resize "
                            "(resize only, default: preserve aspect ratio)")
    parser.add_argument("--x", type=int, help="X offset for crop")
    parser.add_argument("--y", type=int, help="Y offset for crop")

    # Color adjust options
    parser.add_argument("--brightness", type=float, help="Brightness adjustment (-100 to 100)")
    parser.add_argument("--contrast", type=float, help="Contrast adjustment (-100 to 100)")
    parser.add_argument("--saturation", type=float, help="Saturation adjustment (-1 to 1)")
    parser.add_argument("--grayscale", action="store_true", help="Convert to grayscale")

    # Perspective correction options
    parser.add_argument("--corners",
                       help="4 points as CSV: x1,y1,x2,y2,x3,y3,x4,y4 (TL,TR,BR,BL)")

    # Smart compression options
    parser.add_argument("--target-kb", type=int,
                       help="Target file size in KB (approximate, enables binary-search quality)")
    parser.add_argument("--quality", type=int,
                       help="Output quality 1-100 (jpeg/webp). Ignored when --target-kb is set.")
    parser.add_argument("--format",
                       choices=["jpeg", "png", "webp"],
                       help="Force output format")

    # HDR / Tonemapping options
    parser.add_argument("--mode",
                       choices=["auto", "bilateral", "log", "shadows", "highlight"],
                       default="auto",
                       help="Tone mapping mode (default: auto)")
    parser.add_argument("--strength", type=float,
                       help="Enhancement strength 0.1–2.0 (default: 1.0)")
    parser.add_argument("--gamma", type=float,
                       help="Gamma value for log mode (default: 2.2)")

    # Batch/JSON mode
    parser.add_argument("--json", action="store_true",
                       help="Emit a JSON result envelope on stdout. Also enables JSON\n"
                            "batch input when combined with --batch or piped to stdin.")
    parser.add_argument("--batch", "-b", help="JSON file with batch operations")

    args = parser.parse_args()

    # JSON batch mode is selected when --batch is provided, OR when --json is
    # set together with piped stdin (no --task on the command line). A bare
    # --json on a single-operation invocation only switches the result
    # envelope to JSON; it must NOT block waiting for stdin.
    use_batch = bool(args.batch) or (args.json and not args.task and not sys.stdin.isatty())
    if use_batch:
        editor = SmartPhotoEditor(json_output=True)

        if args.batch:
            with open(args.batch) as f:
                data = json.load(f)
        else:
            data = json.load(sys.stdin)

        operations = data.get("operations", [])
        if not operations:
            print(json.dumps({"error": "No operations found"}), file=sys.stdout)
            sys.exit(1)

        editor.process_batch(operations)
        sys.exit(0)

    # Single operation mode
    # For replace-scene: --subject is the primary input, --image is optional
    # (used as fallback). For all other tasks: --image is required.
    if not args.task:
        parser.print_help()
        sys.exit(1)
    if args.task == "replace-scene":
        if not args.subject and not args.image:
            print("Error: --subject (or --image as fallback) is required for replace-scene.", file=sys.stderr)
            sys.exit(1)
    elif not args.image:
        parser.print_help()
        sys.exit(1)

    editor = SmartPhotoEditor(json_output=args.json)

    kwargs = {}
    if args.subject is not None:
        kwargs["subject"] = args.subject
    if args.scene is not None:
        kwargs["scene"] = args.scene
    if args.scene_prompt is not None:
        kwargs["scene_prompt"] = args.scene_prompt
    if args.subject_type is not None:
        kwargs["subject_type"] = args.subject_type
    if args.reference_strength is not None:
        kwargs["reference_strength"] = args.reference_strength
    if args.position is not None:
        kwargs["position"] = args.position
    if args.scale is not None:
        kwargs["scale"] = args.scale
    if args.watermark:
        kwargs["watermark"] = True
    if args.output_format is not None:
        kwargs["output_format"] = args.output_format
    if args.width is not None:
        kwargs["width"] = args.width
    if args.height is not None:
        kwargs["height"] = args.height
    if args.max_dim is not None:
        kwargs["max_dim"] = args.max_dim
    if args.x is not None:
        kwargs["x"] = args.x
    if args.y is not None:
        kwargs["y"] = args.y
    if args.brightness is not None:
        kwargs["brightness"] = args.brightness
    if args.contrast is not None:
        kwargs["contrast"] = args.contrast
    if args.saturation is not None:
        kwargs["saturation"] = args.saturation
    if args.grayscale:
        kwargs["grayscale"] = True
    if args.corners is not None:
        kwargs["corners"] = args.corners
    if args.target_kb is not None:
        kwargs["target_kb"] = args.target_kb
    if args.quality is not None:
        kwargs["quality"] = args.quality
    if args.format is not None:
        kwargs["format"] = args.format
    # Only forward --mode for tasks that accept it. argparse sets default="auto"
    # so args.mode is never None; gating on the task prevents leaking the kwarg
    # into op_resize/op_crop/op_color_adjust which have explicit signatures.
    if args.mode is not None and args.task in ("hdr-tonemap",):
        kwargs["mode"] = args.mode
    if args.strength is not None:
        kwargs["strength"] = args.strength
    if args.gamma is not None:
        kwargs["gamma"] = args.gamma

    # Non-proportional resize override
    if args.no_maintain_aspect:
        kwargs["maintain_aspect"] = False

    success = editor.process(
        task=args.task,
        image=args.image,
        output=args.output,
        prompt=args.prompt,
        tool=args.tool,
        **kwargs
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
