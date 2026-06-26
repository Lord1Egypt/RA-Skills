from __future__ import annotations

import os
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile


class ConversionError(RuntimeError):
    pass


WORD_FORMAT_DOCX = 16
WORD_FORMAT_PDF = 17
WORD_TIMEOUT_SECONDS = int(os.environ.get("LATEX_CONVERT_WORD_TIMEOUT", "45"))


def ensure_docx(input_path: Path, work_dir: Path, engine: str = "auto") -> tuple[Path, str]:
    input_path = input_path.resolve()
    suffix = input_path.suffix.lower()
    if suffix == ".docx":
        return input_path, "already-docx"
    if suffix not in {".doc", ".wps"}:
        raise ConversionError(f"Unsupported input extension: {suffix}")
    work_dir.mkdir(parents=True, exist_ok=True)
    output_path = work_dir / f"{input_path.stem}.docx"
    errors: list[str] = []
    engines = [engine] if engine != "auto" else ["word", "libreoffice"]
    for candidate in engines:
        try:
            if candidate == "word":
                convert_with_word(input_path, output_path)
            elif candidate == "libreoffice":
                convert_with_libreoffice(input_path, output_path)
            else:
                raise ConversionError(f"Unknown conversion engine: {candidate}")
            if output_path.exists() and output_path.stat().st_size > 0:
                return output_path, candidate
            errors.append(f"{candidate}: output was not created")
        except subprocess.TimeoutExpired:
            errors.append(f"{candidate}: timed out after {WORD_TIMEOUT_SECONDS}s")
        except Exception as exc:
            errors.append(f"{candidate}: {exc}")
    raise ConversionError("; ".join(errors))


def convert_with_word(input_path: Path, output_path: Path) -> None:
    system = platform.system().lower()
    if system == "darwin":
        _convert_with_word_mac(input_path, output_path)
        return
    if system == "windows":
        _convert_with_word_windows(input_path, output_path)
        return
    raise ConversionError("Microsoft Word automation is only implemented for macOS and Windows")


def convert_docx_to_pdf(input_path: Path, output_path: Path, engine: str = "auto") -> tuple[Path, str]:
    input_path = input_path.resolve()
    output_path = output_path.resolve()
    if input_path.suffix.lower() != ".docx":
        raise ConversionError(f"PDF preview requires a DOCX input, got: {input_path.suffix}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    engines = [engine] if engine != "auto" else ["word", "libreoffice"]
    for candidate in engines:
        try:
            if candidate == "word":
                _export_pdf_with_word(input_path, output_path)
            elif candidate == "libreoffice":
                _export_pdf_with_libreoffice(input_path, output_path)
            else:
                raise ConversionError(f"Unknown preview engine: {candidate}")
            if output_path.exists() and output_path.stat().st_size > 0:
                return output_path, candidate
            errors.append(f"{candidate}: PDF output was not created")
        except subprocess.TimeoutExpired:
            errors.append(f"{candidate}: timed out after {WORD_TIMEOUT_SECONDS}s")
        except Exception as exc:
            errors.append(f"{candidate}: {exc}")
    raise ConversionError("; ".join(errors))


def _convert_with_word_mac(input_path: Path, output_path: Path) -> None:
    if not Path("/Applications/Microsoft Word.app").exists():
        raise ConversionError("Microsoft Word.app was not found in /Applications")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="latex-convert-word-", dir=_word_mac_work_root()) as tmp:
        tmp_dir = Path(tmp)
        local_input = tmp_dir / input_path.name
        local_output = tmp_dir / output_path.name
        shutil.copy2(input_path, local_input)
        _run_word_mac_save_as(local_input, local_output)
        if not local_output.exists():
            raise ConversionError("Microsoft Word did not create the DOCX")
        shutil.copy2(local_output, output_path)


def _export_pdf_with_word(input_path: Path, output_path: Path) -> None:
    system = platform.system().lower()
    if system == "darwin":
        _export_pdf_with_word_mac(input_path, output_path)
        return
    if system == "windows":
        _export_pdf_with_word_windows(input_path, output_path)
        return
    raise ConversionError("Microsoft Word PDF export is only implemented for macOS and Windows")


def _export_pdf_with_word_mac(input_path: Path, output_path: Path) -> None:
    if not Path("/Applications/Microsoft Word.app").exists():
        raise ConversionError("Microsoft Word.app was not found in /Applications")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="latex-convert-word-pdf-", dir=_word_mac_work_root()) as tmp:
        tmp_dir = Path(tmp)
        local_input = tmp_dir / input_path.name
        local_output = tmp_dir / output_path.name
        shutil.copy2(input_path, local_input)
        _run_word_mac_export_pdf(local_input, local_output)
        if not local_output.exists():
            raise ConversionError("Microsoft Word did not create the PDF")
        shutil.copy2(local_output, output_path)


def _word_mac_work_root() -> str | None:
    """Prefer Word's own sandbox container to avoid macOS file-access prompts."""
    configured = os.environ.get("LATEX_CONVERT_WORD_WORKDIR")
    candidates = [
        Path(configured).expanduser() if configured else None,
        Path.home() / "Library/Containers/com.microsoft.Word/Data/tmp",
        Path.home() / "Library/Containers/com.microsoft.Word/Data/Documents",
    ]
    for candidate in candidates:
        if candidate is None:
            continue
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".latex_convert_probe"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink(missing_ok=True)
            return str(candidate)
        except OSError:
            continue
    return None


def _run_word_mac_save_as(input_path: Path, output_path: Path) -> None:
    script = f'''
set inFile to POSIX file "{_escape_applescript(str(input_path))}"
set outFile to POSIX file "{_escape_applescript(str(output_path))}"
tell application "Microsoft Word"
    set wasVisible to visible
    set oldAlerts to display alerts
    try
        set visible to false
        set display alerts to alerts none
        open inFile
        set activeDoc to active document
        save as activeDoc file name outFile file format format document default
        close activeDoc saving no
        set display alerts to oldAlerts
        set visible to wasVisible
    on error errMsg number errNum
        try
            if (count of documents) > 0 then close active document saving no
        end try
        set display alerts to oldAlerts
        set visible to wasVisible
        error errMsg number errNum
    end try
end tell
'''
    result = subprocess.run(
        ["osascript", "-e", script],
        text=True,
        capture_output=True,
        timeout=WORD_TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        raise ConversionError(_short_process_error(result))


def _run_word_mac_export_pdf(input_path: Path, output_path: Path) -> None:
    script = f'''
set inFile to POSIX file "{_escape_applescript(str(input_path))}"
set outFile to POSIX file "{_escape_applescript(str(output_path))}"
tell application "Microsoft Word"
    set wasVisible to visible
    set oldAlerts to display alerts
    try
        set visible to false
        set display alerts to alerts none
        open inFile
        set activeDoc to active document
        save as activeDoc file name outFile file format format PDF
        close activeDoc saving no
        set display alerts to oldAlerts
        set visible to wasVisible
    on error errMsg number errNum
        try
            if (count of documents) > 0 then close active document saving no
        end try
        set display alerts to oldAlerts
        set visible to wasVisible
        error errMsg number errNum
    end try
end tell
'''
    result = subprocess.run(
        ["osascript", "-e", script],
        text=True,
        capture_output=True,
        timeout=WORD_TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        raise ConversionError(_short_process_error(result))


def _convert_with_word_windows(input_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    code = f"""
import pythoncom
import win32com.client

input_path = {json.dumps(str(input_path))}
output_path = {json.dumps(str(output_path))}
word = None
doc = None
pythoncom.CoInitialize()
try:
    word = win32com.client.DispatchEx('Word.Application')
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        word.AutomationSecurity = 3
    except Exception:
        pass
    doc = word.Documents.Open(
        FileName=input_path,
        ConfirmConversions=False,
        ReadOnly=True,
        AddToRecentFiles=False,
        Visible=False,
        NoEncodingDialog=True,
    )
    doc.SaveAs2(FileName=output_path, FileFormat={WORD_FORMAT_DOCX}, AddToRecentFiles=False)
finally:
    if doc is not None:
        doc.Close(False)
    if word is not None:
        word.Quit()
    pythoncom.CoUninitialize()
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        text=True,
        capture_output=True,
        timeout=WORD_TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        raise ConversionError(_short_process_error(result))


def _export_pdf_with_word_windows(input_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    code = f"""
import pythoncom
import win32com.client

input_path = {json.dumps(str(input_path))}
output_path = {json.dumps(str(output_path))}
word = None
doc = None
pythoncom.CoInitialize()
try:
    word = win32com.client.DispatchEx('Word.Application')
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        word.AutomationSecurity = 3
    except Exception:
        pass
    doc = word.Documents.Open(
        FileName=input_path,
        ConfirmConversions=False,
        ReadOnly=True,
        AddToRecentFiles=False,
        Visible=False,
        NoEncodingDialog=True,
    )
    doc.ExportAsFixedFormat(OutputFileName=output_path, ExportFormat={WORD_FORMAT_PDF}, OpenAfterExport=False)
finally:
    if doc is not None:
        doc.Close(False)
    if word is not None:
        word.Quit()
    pythoncom.CoUninitialize()
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        text=True,
        capture_output=True,
        timeout=WORD_TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        raise ConversionError(_short_process_error(result))


def convert_with_libreoffice(input_path: Path, output_path: Path) -> None:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise ConversionError("LibreOffice/soffice was not found")
    with tempfile.TemporaryDirectory(prefix="latex-convert-lo-") as tmp:
        tmp_path = Path(tmp)
        env = os.environ.copy()
        env["HOME"] = str(tmp_path / "home")
        env["UserInstallation"] = f"file://{tmp_path / 'profile'}"
        result = subprocess.run(
            [
                soffice,
                "--headless",
                f"-env:UserInstallation={(tmp_path / 'profile').as_uri()}",
                "--convert-to",
                "docx",
                "--outdir",
                str(output_path.parent),
                str(input_path),
            ],
            text=True,
            capture_output=True,
            timeout=180,
            env=env,
        )
    generated = output_path.parent / f"{input_path.stem}.docx"
    if result.returncode != 0:
        raise ConversionError(_short_process_error(result))
    if generated != output_path and generated.exists():
        generated.replace(output_path)
    if not output_path.exists():
        raise ConversionError(_short_process_error(result) or "LibreOffice did not create a DOCX")


def _export_pdf_with_libreoffice(input_path: Path, output_path: Path) -> None:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise ConversionError("LibreOffice/soffice was not found")
    with tempfile.TemporaryDirectory(prefix="latex-convert-lo-pdf-") as tmp:
        tmp_path = Path(tmp)
        env = os.environ.copy()
        env["HOME"] = str(tmp_path / "home")
        env["UserInstallation"] = f"file://{tmp_path / 'profile'}"
        result = subprocess.run(
            [
                soffice,
                "--headless",
                f"-env:UserInstallation={(tmp_path / 'profile').as_uri()}",
                "--convert-to",
                "pdf",
                "--outdir",
                str(output_path.parent),
                str(input_path),
            ],
            text=True,
            capture_output=True,
            timeout=240,
            env=env,
        )
    generated = output_path.parent / f"{input_path.stem}.pdf"
    if result.returncode != 0:
        raise ConversionError(_short_process_error(result))
    if generated != output_path and generated.exists():
        generated.replace(output_path)
    if not output_path.exists():
        raise ConversionError(_short_process_error(result) or "LibreOffice did not create a PDF")


def _escape_applescript(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _short_process_error(result: subprocess.CompletedProcess[str]) -> str:
    text = (result.stderr or result.stdout or "").strip()
    return text[-1000:] if text else f"process exited with {result.returncode}"
