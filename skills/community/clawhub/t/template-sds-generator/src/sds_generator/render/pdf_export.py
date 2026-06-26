from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from sds_generator.models import ChecklistBucket, ReviewNote, ReviewSeverity, ReviewStatus


def _warning(message: str) -> ReviewNote:
    return ReviewNote(
        field_path="render.pdf_export",
        severity=ReviewSeverity.MINOR,
        status=ReviewStatus.WARNING,
        why=message,
        checklist_bucket=ChecklistBucket.LAYOUT_BRANDING_QA,
    )


def _user_installation_uri(path: Path) -> str:
    return path.resolve().as_uri()


def _libreoffice_command(binary: str, docx_path: Path, output_dir: Path, profile_dir: Path) -> list[str]:
    return [
        binary,
        "--headless",
        f"-env:UserInstallation={_user_installation_uri(profile_dir)}",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_dir),
        str(docx_path),
    ]


def export_docx_to_pdf(docx_path: Path, output_dir: Path) -> tuple[Path | None, list[ReviewNote]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    last_error: str | None = None
    for binary in ("soffice", "libreoffice"):
        if shutil.which(binary):
            with tempfile.TemporaryDirectory(prefix="sds-lo-") as temp_dir:
                temp_root = Path(temp_dir)
                profile_dir = temp_root / "profile"
                config_dir = temp_root / "config"
                cache_dir = temp_root / "cache"
                runtime_dir = temp_root / "runtime"
                for directory in (profile_dir, config_dir, cache_dir, runtime_dir):
                    directory.mkdir(parents=True, exist_ok=True)

                command = _libreoffice_command(binary, docx_path, output_dir, profile_dir)
                env = os.environ.copy()
                env.update(
                    {
                        "HOME": str(temp_root),
                        "XDG_CONFIG_HOME": str(config_dir),
                        "XDG_CACHE_HOME": str(cache_dir),
                        "XDG_RUNTIME_DIR": str(runtime_dir),
                    }
                )
                result = subprocess.run(command, capture_output=True, text=True, check=False, env=env)

            pdf_path = output_dir / f"{docx_path.stem}.pdf"
            if result.returncode == 0 and pdf_path.exists():
                return pdf_path, []
            last_error = result.stderr.strip() or result.stdout.strip() or "unknown error"

    try:
        from docx2pdf import convert  # type: ignore[import-not-found]
    except ImportError:
        if last_error is not None:
            return None, [_warning(f"PDF export via LibreOffice failed: {last_error}")]
        return None, [_warning("No PDF export engine available; kept DOCX output only.")]

    pdf_path = output_dir / f"{docx_path.stem}.pdf"
    try:
        convert(str(docx_path), str(pdf_path))
    except Exception as exc:  # pragma: no cover
        return None, [_warning(f"docx2pdf export failed: {exc}")]
    return (pdf_path if pdf_path.exists() else None), []
