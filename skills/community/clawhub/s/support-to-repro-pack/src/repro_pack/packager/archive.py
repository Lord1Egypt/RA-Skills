"""Archive creation — bundle outputs into distributable zip."""

from __future__ import annotations

import os
import zipfile


def create_archive(
    source_dir: str,
    output_path: str,
    formats: list[str] | None = None,
) -> str:
    """Create a zip archive of the output directory.

    Args:
        source_dir: Directory containing output files.
        output_path: Path for the archive file (e.g., 'repro-pack.zip').
        formats: Optional list of file extensions to include. None = all files.

    Returns:
        Absolute path to the created archive.
    """
    output_path = os.path.abspath(output_path)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(source_dir):
            for fname in files:
                if formats and not any(fname.endswith(ext) for ext in formats):
                    continue
                fpath = os.path.join(root, fname)
                arcname = os.path.relpath(fpath, source_dir)
                zf.write(fpath, arcname)

    return output_path
