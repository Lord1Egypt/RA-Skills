#!/usr/bin/env python3
"""xAI Studio — generate and edit images and videos via the xAI API.

Subcommands
----------
Image:
    generate         Create images from a text prompt (single or batch).
    edit             Edit existing image(s) with a text prompt.
    concurrent       Apply multiple style prompts to one image in parallel.
    multi-turn       Chain sequential edits — each output feeds into the next.

Video:
    video-generate   Create a video from text or a still image.
    video-edit       Edit an existing video with a text prompt.
    video-concurrent Apply multiple edit prompts to one video in parallel.

Examples
--------
    python3 run.py generate --prompt "A futuristic cityscape at dawn"
    python3 run.py edit --prompt "Make it a watercolor" --image photo.png
    python3 run.py concurrent --image photo.png --prompt "oil painting" --prompt "pencil sketch"
    python3 run.py multi-turn --image photo.png --prompt "Add clouds" --prompt "Make it sunset"
    python3 run.py video-generate --prompt "A rocket launching from Mars" --duration 10
    python3 run.py video-edit --prompt "Add a necklace" --video source.mp4
    python3 run.py video-concurrent --video clip.mp4 --prompt "Add hat" --prompt "Change outfit"
"""

import argparse
import asyncio
import base64
import sys

from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse
from urllib.request import urlretrieve

try:
    import xai_sdk

    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False

# ---------------------------------------------------------------------------
# Constants & configuration
# ---------------------------------------------------------------------------

DEFAULT_MODEL = "grok-imagine-image"
DEFAULT_VIDEO_MODEL = "grok-imagine-video"
DEFAULT_OUT_DIR = "media/xai-output"

MIME_MAP: dict[str, str] = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}


def _ensure_sdk() -> bool:
    """Return True if the xAI SDK is available, printing an error otherwise."""
    if not SDK_AVAILABLE:
        print(
            "Error: xai_sdk is not installed.\n"
            " → activate the venv first, or run: pip install xai-sdk",
            file=sys.stderr,
        )
        return False
    return True


def _prepare_out_dir(path: str) -> Path:
    """Create ``<path>/<YYYY-MM-DD>/`` and return the resulting :class:`Path`."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = Path(path) / today
    out.mkdir(parents=True, exist_ok=True)
    return out


def _make_stem(prefix: str, index: int) -> str:
    """Build a descriptive file stem: ``<prefix>_<NNN>_<HHMMSS>``."""
    ts = datetime.now(timezone.utc).strftime("%H%M%S")
    return f"{prefix}_{index:03d}_{ts}"


def _infer_ext(url: str) -> str:
    """Derive a file extension from *url*, defaulting to ``.png``."""
    path = PurePosixPath(urlparse(url).path)
    ext = path.suffix.lower()
    if ext in MIME_MAP:
        return ext
    return ".png"


def _detect_ext(data: bytes) -> str:
    """Sniff the image format from the first few magic bytes of *data*."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if data[:2] == b"\xff\xd8":
        return ".jpg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    if data[:4] in (b"GIF8",):
        return ".gif"
    return ".png"


def _encode_image(img_path: str) -> str:
    """Return a base64 data-URI for a local file, or pass *img_path* through as a URL."""
    p = Path(img_path)
    if p.is_file():
        mime = MIME_MAP.get(p.suffix.lower(), "image/png")
        b64 = base64.b64encode(p.read_bytes()).decode()
        return f"data:{mime};base64,{b64}"
    return img_path


def _encode_video(video_path: str) -> str:
    """Return a base64 data-URI for a local video file, or pass through as URL."""
    p = Path(video_path)
    if p.is_file():
        mime = "video/mp4"  # assume mp4 for now
        b64 = base64.b64encode(p.read_bytes()).decode()
        return f"data:{mime};base64,{b64}"
    return video_path


def _save_response(response, stem: str, out_dir: Path) -> Path | None:
    """Save an image response to disk and return the written path.

    Supports both base64-encoded data and URL responses. The file
    extension is detected from magic bytes (base64) or the URL path.
    Returns ``None`` when the response contains no usable data.
    """
    filepath: Path | None = None

    if hasattr(response, "image") and response.image:
        # base64 mode — detect the real format from magic bytes
        ext = _detect_ext(response.image)
        filepath = out_dir / f"{stem}{ext}"
        with open(filepath, "wb") as f:
            f.write(response.image)
    elif hasattr(response, "url") and response.url:
        ext = _infer_ext(response.url)
        filepath = out_dir / f"{stem}{ext}"
        urlretrieve(response.url, str(filepath))
    else:
        print(f"Warning: no image data in response for {stem}", file=sys.stderr)
        return None

    try:
        url_info = response.url or "base64"
    except (ValueError, AttributeError):
        url_info = "base64"
    moderation = ""
    if hasattr(response, "respect_moderation"):
        moderation = " ✓ moderation" if response.respect_moderation else " ⚠ filtered"
    model_info = ""
    if hasattr(response, "model") and response.model:
        model_info = f" [{response.model}]"
    print(f" Saved: {filepath} ({url_info}{model_info}{moderation})")
    return filepath


def _save_async_image(image_bytes: bytes, stem: str, out_dir: Path) -> Path:
    """Save pre-resolved image bytes (from an async response) to disk."""
    ext = _detect_ext(image_bytes)
    filepath = out_dir / f"{stem}{ext}"
    with open(filepath, "wb") as f:
        f.write(image_bytes)
    print(f" Saved: {filepath}")
    return filepath


def _build_common_image_kwargs(
    args: argparse.Namespace, overrides: dict = None
) -> dict:
    """Build common kwargs for image.sample calls to reduce repetition."""
    if overrides is None:
        overrides = {}
    kwargs = {
        "model": args.model,
        **overrides,
    }
    if getattr(args, "aspect_ratio", None) and args.aspect_ratio != "1:1":
        kwargs["aspect_ratio"] = args.aspect_ratio
    if getattr(args, "resolution", None):
        kwargs["resolution"] = args.resolution
    if getattr(args, "format", None) == "base64":
        kwargs["image_format"] = "base64"
    return kwargs


def _build_common_video_kwargs(
    args: argparse.Namespace, overrides: dict = None
) -> dict:
    """Build common kwargs for video calls to reduce repetition."""
    if overrides is None:
        overrides = {}
    kwargs = {
        "model": args.model,
        **overrides,
    }
    if getattr(args, "aspect_ratio", None):
        kwargs["aspect_ratio"] = args.aspect_ratio
    if getattr(args, "resolution", None):
        kwargs["resolution"] = args.resolution
    if getattr(args, "timeout", None):
        kwargs["timeout"] = timedelta(seconds=args.timeout)
    if getattr(args, "poll_interval", None):
        kwargs["interval"] = timedelta(seconds=args.poll_interval)
    return kwargs


# ---------------------------------------------------------------------------
# Image subcommands
# ---------------------------------------------------------------------------


def cmd_generate(args: argparse.Namespace) -> int:
    """Generate one or more images from a text prompt."""
    if not _ensure_sdk():
        return 1

    out_dir = _prepare_out_dir(args.out_dir)
    client = xai_sdk.Client()

    kwargs = _build_common_image_kwargs(
        args, {"prompt": args.prompt, "aspect_ratio": args.aspect_ratio}
    )

    count = args.count
    print(
        f"Generating {count} image(s) — model={args.model}, ratio={args.aspect_ratio}"
    )

    if count == 1:
        response = client.image.sample(**kwargs)
        _save_response(response, _make_stem("generate", 1), out_dir)
    else:
        responses = client.image.sample_batch(**kwargs, n=count)
        for i, resp in enumerate(responses, 1):
            _save_response(resp, _make_stem("generate", i), out_dir)

    print(f"Done. Output in {out_dir}")
    return 0


def cmd_edit(args: argparse.Namespace) -> int:
    """Edit one or more source images with a text prompt."""
    if not _ensure_sdk():
        return 1

    out_dir = _prepare_out_dir(args.out_dir)
    client = xai_sdk.Client()

    # Encode local files as data-URIs; URLs pass through unchanged
    image_uris = [_encode_image(img) for img in args.image]

    kwargs = _build_common_image_kwargs(args, {"prompt": args.prompt})

    # The API uses singular vs plural key depending on image count
    if len(image_uris) == 1:
        kwargs["image_url"] = image_uris[0]
    else:
        kwargs["image_urls"] = image_uris

    print(f"Editing {len(image_uris)} image(s) — model={args.model}")
    response = client.image.sample(**kwargs)
    _save_response(response, _make_stem("edit", 1), out_dir)

    print(f"Done. Output in {out_dir}")
    return 0


def cmd_concurrent(args: argparse.Namespace) -> int:
    """Apply multiple style prompts to one image concurrently via ``AsyncClient``."""
    if not _ensure_sdk():
        return 1

    out_dir = _prepare_out_dir(args.out_dir)
    source_uri = _encode_image(args.image)

    # Common kwargs for all concurrent calls
    common = {
        "model": args.model,
        "image_url": source_uri,
    }
    if args.aspect_ratio and args.aspect_ratio != "1:1":
        common["aspect_ratio"] = args.aspect_ratio
    if args.resolution:
        common["resolution"] = args.resolution
    # Force base64 so we can resolve image bytes in-process
    common["image_format"] = "base64"

    async def _run() -> list[tuple[int, bytes]]:
        sem = asyncio.Semaphore(4)

        async def _one(idx: int, prompt: str) -> tuple[int, bytes]:
            async with sem:
                async with xai_sdk.AsyncClient() as client:
                    resp = await client.image.sample(prompt=prompt, **common)
                    img = await resp.image
                    return (idx, img)

        tasks = [_one(i, p) for i, p in enumerate(args.prompt, 1)]
        return await asyncio.gather(*tasks)

    print(
        f"Running {len(args.prompt)} concurrent style transfer(s) — model={args.model}"
    )
    results = asyncio.run(_run())

    for idx, img_bytes in results:
        _save_async_image(img_bytes, _make_stem("style", idx), out_dir)

    print(f"Done. Output in {out_dir}")
    return 0


def cmd_multiturn(args: argparse.Namespace) -> int:
    """Chain multiple edits sequentially, feeding each output into the next step."""
    if not _ensure_sdk():
        return 1

    out_dir = _prepare_out_dir(args.out_dir)
    client = xai_sdk.Client()

    # Begin with the user-supplied source image
    current_uri = _encode_image(args.image)

    for i, prompt in enumerate(args.prompt, 1):
        print(f" Step {i}/{len(args.prompt)}: {prompt}")

        kwargs = _build_common_image_kwargs(
            args, {"prompt": prompt, "image_url": current_uri}
        )
        # Force base64 for intermediates so chaining works without re-downloading
        kwargs["image_format"] = "base64"

        response = client.image.sample(**kwargs)
        saved = _save_response(response, _make_stem("step", i), out_dir)

        # Re-encode the output as the next input
        if saved and hasattr(response, "image") and response.image:
            b64 = base64.b64encode(response.image).decode()
            current_uri = f"data:image/png;base64,{b64}"
        elif hasattr(response, "url") and response.url:
            current_uri = response.url
        else:
            print(
                "Error: could not chain — no output from previous step", file=sys.stderr
            )
            return 1

    print(f"Done. {len(args.prompt)} step(s) completed. Output in {out_dir}")
    return 0


# ---------------------------------------------------------------------------
# Video subcommands
# ---------------------------------------------------------------------------


def _save_video_response(response, stem: str, out_dir: Path) -> Path | None:
    """Download a video response and return the saved ``.mp4`` path."""
    if not (hasattr(response, "url") and response.url):
        print(f"Warning: no video URL in response for {stem}", file=sys.stderr)
        return None

    filepath = out_dir / f"{stem}.mp4"
    urlretrieve(response.url, str(filepath))

    duration = getattr(response, "duration", "?")
    moderation = ""
    if hasattr(response, "respect_moderation"):
        moderation = " ✓ moderation" if response.respect_moderation else " ⚠ filtered"
    model_info = ""
    if hasattr(response, "model") and response.model:
        model_info = f" [{response.model}]"
    print(f" Saved: {filepath} ({duration}s{model_info}{moderation})")
    return filepath


def cmd_video_generate(args: argparse.Namespace) -> int:
    """Generate a video from a text prompt, optionally animating a still image."""
    if not _ensure_sdk():
        return 1

    out_dir = _prepare_out_dir(args.out_dir)
    client = xai_sdk.Client()

    kwargs = _build_common_video_kwargs(
        args, {"prompt": args.prompt, "duration": args.duration}
    )

    # Image-to-video when a source image is provided
    if args.image:
        kwargs["image_url"] = _encode_image(args.image)
        print(
            f"Generating video from image — model={args.model}, duration={args.duration}s"
        )
    else:
        print(f"Generating video — model={args.model}, duration={args.duration}s")

    response = client.video.generate(**kwargs)
    _save_video_response(response, _make_stem("video", 1), out_dir)

    print(f"Done. Output in {out_dir}")
    return 0


def cmd_video_edit(args: argparse.Namespace) -> int:
    """Edit an existing video using a text prompt."""
    if not _ensure_sdk():
        return 1

    out_dir = _prepare_out_dir(args.out_dir)
    client = xai_sdk.Client()

    video_uri = _encode_video(args.video)
    kwargs = _build_common_video_kwargs(
        args, {"prompt": args.prompt, "video_url": video_uri}
    )

    print(f"Editing video — model={args.model}")
    response = client.video.generate(**kwargs)
    _save_video_response(response, _make_stem("video_edit", 1), out_dir)

    print(f"Done. Output in {out_dir}")
    return 0


def cmd_video_concurrent(args: argparse.Namespace) -> int:
    """Apply multiple edit prompts to one video concurrently via ``AsyncClient``."""
    if not _ensure_sdk():
        return 1

    out_dir = _prepare_out_dir(args.out_dir)

    video_uri = _encode_video(args.video)
    common = _build_common_video_kwargs(args, {"video_url": video_uri})

    async def _run() -> list:
        sem = asyncio.Semaphore(4)

        async def _one(prompt: str):
            async with sem:
                async with xai_sdk.AsyncClient() as client:
                    return await client.video.generate(prompt=prompt, **common)

        tasks = [_one(p) for p in args.prompt]
        return await asyncio.gather(*tasks)

    print(f"Running {len(args.prompt)} concurrent video edit(s) — model={args.model}")
    results = asyncio.run(_run())

    for i, resp in enumerate(results, 1):
        _save_video_response(resp, _make_stem("video_style", i), out_dir)

    print(f"Done. Output in {out_dir}")
    return 0


# ---------------------------------------------------------------------------
# CLI parser
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Construct the CLI parser with image and video subcommands."""
    parser = argparse.ArgumentParser(
        prog="xai-studio",
        description="xAI Studio — generate and edit images and videos via the xAI API",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- Image flags -----------------------------------------------------------
    def add_common_flags(p: argparse.ArgumentParser) -> None:
        """Register flags shared across all image subcommands."""
        p.add_argument(
            "--model",
            default=DEFAULT_MODEL,
            help=f"Model name (default: {DEFAULT_MODEL})",
        )
        p.add_argument(
            "--aspect-ratio",
            default="1:1",
            help="Aspect ratio, e.g. 16:9 (default: 1:1)",
        )
        p.add_argument(
            "--resolution",
            choices=["1k", "2k"],
            default=None,
            help="Output resolution (default: API default)",
        )
        p.add_argument(
            "--format",
            choices=["url", "base64"],
            default="base64",
            help="Response format (default: base64)",
        )
        p.add_argument(
            "--out-dir",
            default=DEFAULT_OUT_DIR,
            help=f"Output directory (default: {DEFAULT_OUT_DIR})",
        )

    # -- generate --------------------------------------------------------------
    gen = sub.add_parser("generate", help="Generate images from a text prompt")
    gen.add_argument("--prompt", required=True, help="Image generation prompt")
    gen.add_argument(
        "--count", type=int, default=1, help="Number of images (default: 1, max: 10)"
    )
    add_common_flags(gen)
    gen.set_defaults(func=cmd_generate)

    # -- edit ------------------------------------------------------------------
    edit = sub.add_parser("edit", help="Edit existing image(s) with a text prompt")
    edit.add_argument("--prompt", required=True, help="Edit instruction prompt")
    edit.add_argument(
        "--image",
        required=True,
        action="append",
        help="Source image path or URL (repeat up to 3x)",
    )
    add_common_flags(edit)
    edit.set_defaults(func=cmd_edit)

    # -- concurrent ------------------------------------------------------------
    conc = sub.add_parser(
        "concurrent", help="Parallel style transfers on a source image"
    )
    conc.add_argument("--image", required=True, help="Source image path or URL")
    conc.add_argument(
        "--prompt",
        required=True,
        action="append",
        help="Style prompt (repeat for each variation)",
    )
    add_common_flags(conc)
    conc.set_defaults(func=cmd_concurrent)

    # -- multi-turn ------------------------------------------------------------
    mt = sub.add_parser(
        "multi-turn", help="Iterative edit chaining — each output feeds into the next"
    )
    mt.add_argument("--image", required=True, help="Starting image path or URL")
    mt.add_argument(
        "--prompt",
        required=True,
        action="append",
        help="Edit prompt (applied sequentially)",
    )
    add_common_flags(mt)
    mt.set_defaults(func=cmd_multiturn)

    # -- Video flags -----------------------------------------------------------
    def add_video_flags(p: argparse.ArgumentParser) -> None:
        """Register flags shared across all video subcommands."""
        p.add_argument(
            "--model",
            default=DEFAULT_VIDEO_MODEL,
            help=f"Model name (default: {DEFAULT_VIDEO_MODEL})",
        )
        p.add_argument(
            "--aspect-ratio",
            default=None,
            help="Aspect ratio (default: 16:9 for text, source for editing)",
        )
        p.add_argument(
            "--resolution",
            choices=["480p", "720p"],
            default=None,
            help="Output resolution (default: 480p)",
        )
        p.add_argument(
            "--out-dir",
            default=DEFAULT_OUT_DIR,
            help=f"Output directory (default: {DEFAULT_OUT_DIR})",
        )
        p.add_argument(
            "--timeout",
            type=int,
            default=None,
            help="Max wait in seconds (default: 600)",
        )
        p.add_argument(
            "--poll-interval",
            type=int,
            default=None,
            help="Poll interval in seconds (default: SDK default)",
        )

    # -- video-generate --------------------------------------------------------
    vgen = sub.add_parser("video-generate", help="Generate video from text or image")
    vgen.add_argument("--prompt", required=True, help="Video generation prompt")
    vgen.add_argument(
        "--duration", type=int, default=5, help="Duration in seconds, 1-15 (default: 5)"
    )
    vgen.add_argument(
        "--image", default=None, help="Optional source image for image-to-video"
    )
    add_video_flags(vgen)
    vgen.set_defaults(func=cmd_video_generate)

    # -- video-edit ------------------------------------------------------------
    vedit = sub.add_parser(
        "video-edit", help="Edit an existing video with a text prompt"
    )
    vedit.add_argument("--prompt", required=True, help="Edit instruction prompt")
    vedit.add_argument("--video", required=True, help="Source video URL")
    add_video_flags(vedit)
    vedit.set_defaults(func=cmd_video_edit)

    # -- video-concurrent ------------------------------------------------------
    vconc = sub.add_parser(
        "video-concurrent", help="Parallel video edits with multiple prompts"
    )
    vconc.add_argument("--video", required=True, help="Source video URL")
    vconc.add_argument(
        "--prompt",
        required=True,
        action="append",
        help="Edit prompt (repeat for each variation)",
    )
    add_video_flags(vconc)
    vconc.set_defaults(func=cmd_video_concurrent)

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    """Parse arguments and dispatch to the selected subcommand."""
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
