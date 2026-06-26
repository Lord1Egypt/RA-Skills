#!/usr/bin/env python3
"""Camera snapshot utility - part of the camsnap skill."""

from __future__ import annotations

import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import cv2

__all__ = ["take_snapshot"]

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def _validate_output_path(output_path: str) -> Path:
    """Validate and normalise an output path, raising on unsafe values."""
    p = Path(output_path).resolve()
    ext = p.suffix.lower()
    if ext and ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported image extension: {ext!r}. Allowed: {sorted(ALLOWED_EXTENSIONS)}")
    if p.exists():
        raise FileExistsError(f"File already exists: {p}")
    return p


def take_snapshot(
    output_path: Optional[str] = None,
    show_preview: bool = False,
    output_dir: str = "snapshots",
) -> Optional[str]:
    """Take a snapshot from the default webcam.

    Args:
        output_path: Optional explicit path to save the image.
        show_preview: Whether to display a preview window.
        output_dir: Directory for auto-generated filenames when
            *output_path* is not provided.

    Returns:
        Absolute path to the saved image, or ``None`` on failure.
    """
    # --- resolve destination ---
    if output_path:
        dest = _validate_output_path(output_path)
    else:
        dir_path = Path(output_dir).resolve()
        dir_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%M%S")
        dest = dir_path / f"snapshot_{timestamp}.jpg"

    # --- capture ---
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("Could not access webcam")
        return None

    try:
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to capture frame")
            return None

        # Ensure parent directory exists
        dest.parent.mkdir(parents=True, exist_ok=True)

        ok = cv2.imwrite(str(dest), frame)
        if not ok:
            logger.error("cv2.imwrite failed for %s", dest)
            return None

        logger.info("Snapshot saved to: %s", dest)
    finally:
        cap.release()

    # --- preview ---
    if show_preview:
        cv2.imshow("Snapshot Preview", frame)  # type: ignore[possibly-undefined]
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return str(dest)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="Take webcam snapshot")
    parser.add_argument("output_path", nargs="?", help="Path to save the snapshot")
    parser.add_argument("--preview", action="store_true", help="Show preview window")
    parser.add_argument("--output-dir", default="./snapshots", help="Directory for auto-generated filenames")

    cli_args = parser.parse_args()

    try:
        result = take_snapshot(cli_args.output_path, cli_args.preview, cli_args.output_dir)
    except (ValueError, FileExistsError) as exc:
        parser.error(str(exc))
