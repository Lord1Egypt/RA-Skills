#!/usr/bin/env python3
"""
Document parsing MCP client.

Usage:
    python docparse.py <input_file> [output_file]

Environment:
    DOCPARSE_MCP_URL  - Document parsing MCP server URL (required)
    DOCPARSE_API_KEY  - Document parsing API key (optional)
    DOCPARSE_TIMEOUT  - MCP client timeout in seconds (default: 7200)

Config priority (highest to lowest):
    1. Process environment variables (os.environ)
    2. openclaw.json mcp.servers.docparse.env
    3. Skill directory .env file
    Values from higher priority sources override lower ones.

Exit codes:
    0   - success
    11  - file not found (F001)
    12  - file not readable (F002)
    13  - unsupported format (F003)
    21  - config missing (C001)
    22  - MCP connection/auth error (A001/N001)
    31  - service returned empty (S001)
    32  - response parse error (S002)
    33  - service returned error JSON (S003)
    41  - output directory not writable (O001)
    42  - output file write failed (O002)
"""

import os
import sys
import json
import base64
import asyncio
import mimetypes
from pathlib import Path
from urllib.parse import urlparse

from fastmcp import Client

# Location of this script (for resolving relative .env paths)
_SCRIPT_DIR = Path(__file__).resolve().parent

# openclaw.json location (one level above skills/)
_OPENCLAW_CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"


def _load_openclaw_config() -> dict:
    """Load environment variables from openclaw.json MCP config.

    Reads mcp.servers.docparse.env section.
    Returns a dict of key=value pairs, or empty dict if unavailable.
    """
    if not _OPENCLAW_CONFIG_PATH.is_file():
        return {}
    try:
        with open(_OPENCLAW_CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        mcp_env = (
            config
            .get("mcp", {})
            .get("servers", {})
            .get("docparse", {})
            .get("env", {})
        )
        # Filter to only DOCPARSE_ prefixed keys
        return {
            k: v for k, v in mcp_env.items()
            if isinstance(k, str) and k.startswith("DOCPARSE_") and isinstance(v, str)
        }
    except (json.JSONDecodeError, OSError, TypeError, AttributeError):
        return {}


def _load_env_file() -> dict:
    """Load .env file from the skill directory (parent of mcp/).

    Searches for .env in:
      1. <skill_dir>/.env  (i.e. the directory containing mcp/)

    Returns a dict of key=value pairs, ignoring comments and blank lines.
    """
    skill_dir = _SCRIPT_DIR.parent  # mcp/ to docparse/
    env_path = skill_dir / ".env"
    env_vars = {}

    if env_path.is_file():
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith("#"):
                        continue
                    # Parse KEY=VALUE (support both quoted and unquoted)
                    if "=" in line:
                        key, _, value = line.partition("=")
                        key = key.strip()
                        value = value.strip()
                        # Remove surrounding quotes
                        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                            value = value[1:-1]
                        env_vars[key] = value
        except (OSError, UnicodeDecodeError):
            pass  # Silently ignore unreadable .env files

    return env_vars


def _get_config() -> tuple[str | None, str | None, int]:
    """Get DOCPARSE_MCP_URL, DOCPARSE_API_KEY, and DOCPARSE_TIMEOUT with priority:

      1. os.environ (process environment variables -- highest priority)
      2. openclaw.json mcp.servers.docparse.env
      3. .env file in skill directory
      4. None (caller should raise C001 if URL is missing)

    Returns: (mcp_url, api_key, timeout)
    """
    # Load all config sources
    openclaw_vars = _load_openclaw_config()
    env_file_vars = _load_env_file()

    # os.environ > openclaw.json > .env file
    # For URL and API_KEY: use first non-empty value
    mcp_url = (
        os.environ.get("DOCPARSE_MCP_URL")
        or openclaw_vars.get("DOCPARSE_MCP_URL")
        or env_file_vars.get("DOCPARSE_MCP_URL")
    )
    api_key = (
        os.environ.get("DOCPARSE_API_KEY")
        or openclaw_vars.get("DOCPARSE_API_KEY")
        or env_file_vars.get("DOCPARSE_API_KEY")
    )

    # Parse timeout with fallback to 7200 seconds (2 hours)
    timeout_str = (
        os.environ.get("DOCPARSE_TIMEOUT")
        or openclaw_vars.get("DOCPARSE_TIMEOUT")
        or env_file_vars.get("DOCPARSE_TIMEOUT")
    )
    if timeout_str:
        try:
            timeout = int(timeout_str)
        except ValueError:
            timeout = 7200
    else:
        timeout = 7200

    return mcp_url, api_key, timeout


# Supported MIME types and extensions
SUPPORTED_MIME = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/bmp",
    "image/webp",
    "image/tiff",
}
SUPPORTED_EXT = {".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff"}


class DocparseError(Exception):
    """文档解析异常，携带错误代号。"""
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


def error(code: str, message: str) -> None:
    """Print error and exit with appropriate code."""
    print(f"[{code}] {message}", file=sys.stderr)
    sys.exit(int(code[1:]) if code[1:].isdigit() else 1)


def _check_file(file_path: str) -> tuple[bool, dict | str]:
    """Validate input file without exiting.

    Returns (ok, resolved_path_or_error_dict).
    """
    path = Path(file_path)
    if not path.exists():
        return False, {"code": "F001", "message": "解析失败：未找到待解析文件。建议：请确认文件是否已上传，或检查文件路径是否正确。"}
    if not path.is_file() or not os.access(path, os.R_OK):
        return False, {"code": "F002", "message": "解析失败：当前文件无法读取。建议：请检查文件权限后重试。"}
    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXT:
        mime, _ = mimetypes.guess_type(str(path))
        if mime not in SUPPORTED_MIME:
            return False, {"code": "F003", "message": "解析失败：当前文件格式不支持文档解析。支持格式：PDF、PNG、JPG、JPEG、BMP、WEBP、TIFF。建议：请先将文件转换为 PDF 后重试。"}
    return True, str(path.resolve())


def check_file(file_path: str) -> str:
    """Validate input file: exists, readable, supported format. (CLI version, exits on error)"""
    ok, result = _check_file(file_path)
    if not ok:
        error(result["code"], result["message"])
    return result


def get_output_path(input_path: str, output_path: str | None) -> Path:
    """Determine output file path."""
    if output_path:
        out = Path(output_path)
    else:
        inp = Path(input_path)
        out = inp.parent / f"{inp.stem}.md"

    # Auto-increment if exists
    counter = 1
    original = out
    while out.exists():
        out = original.parent / f"{original.stem}_{counter}{original.suffix}"
        counter += 1

    # Ensure parent directory exists and is writable
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        error("O001", f"解析失败：无法写入输出目录。建议：请更换输出路径或检查目录权限。")

    return out


def extract_result(data: dict, output_format: str) -> tuple[str, dict]:
    """Extract result from document parsing response.

    Returns:
        (content_str, metadata_dict)
    """
    if not isinstance(data, dict):
        error("S002", "解析失败：文档结果解析异常。建议：请稍后重试，或联系管理员检查解析服务。")

    # Check for top-level error
    if "error" in data or "error_code" in data or "errcode" in data:
        error("S003", "解析失败：文档解析服务返回异常。建议：请稍后重试，或联系管理员检查解析服务。")

    # Handle wrapped response: {"success": true, "result": {...}}
    result = data.get("result", data)

    # Check for error inside result
    if isinstance(result, dict):
        if "error" in result or "error_code" in result or "errcode" in result:
            error("S003", "解析失败：文档解析服务返回异常。建议：请稍后重试，或联系管理员检查解析服务。")

    # Build output based on format
    outputs = {}
    if isinstance(result, dict):
        if "markdown_result" in result and result["markdown_result"]:
            outputs["markdown"] = str(result["markdown_result"])
        if "json_result" in result and result["json_result"]:
            outputs["json"] = json.dumps(result["json_result"], ensure_ascii=False, indent=2)

    # Priority extraction for single-format requests
    if output_format == "markdown" and "markdown" in outputs:
        return outputs["markdown"], {"format": "markdown"}
    if output_format == "json" and "json" in outputs:
        return outputs["json"], {"format": "json"}

    # Both: prefer markdown if available, else json, else fallback
    if "markdown" in outputs:
        return outputs["markdown"], {"format": "markdown"}
    if "json" in outputs:
        return outputs["json"], {"format": "json"}

    # Legacy fallback: direct field extraction from result
    if isinstance(result, dict):
        for key in ("markdown", "content", "text", "result"):
            if key in result and result[key]:
                return str(result[key]), {"format": "markdown"}

    # Final fallback: pretty-print entire response
    return json.dumps(data, ensure_ascii=False, indent=2), {"format": "json"}


async def parse_document(
    input_file: str,
    output_file: str | None = None,
    output_format: str = "markdown",
) -> None:
    """Parse document via document parsing MCP server (CLI entry, exits on error)."""
    result = await parse_document_return(input_file, output_file, output_format)
    if result["success"]:
        r = result["result"]
        print(f"✅ 解析完成！")
        print(f"输出文件：{r['output_path']}")
        print(f"文件大小：{r['size_kb']:.1f} KB")
        print(f"输出格式：{r['format']}")
        print(f"内容摘要：{r['summary']}...")
    else:
        err = result["error"]
        error(err["code"], err["message"])


async def parse_document_return(
    input_file: str,
    output_file: str | None = None,
    output_format: str = "markdown",
) -> dict:
    """Parse document via document parsing MCP server.

    Returns a dict:
      - On success:
        {
          "success": True,
          "result": {
            "output_path": str,
            "size_kb": float,
            "format": str,
            "summary": str,
            "content": str,
          }
        }
      - On failure:
        {
          "success": False,
          "error": {
            "code": str,      # e.g. "F001", "C001", "S001" ...
            "message": str,   # user-friendly Chinese message
          }
        }
    """
    # ---- input validation ----
    ok, check_result = _check_file(input_file)
    if not ok:
        return {"success": False, "error": check_result}
    input_path = check_result

    if output_format not in ("markdown", "json", "both"):
        output_format = "markdown"

    # ---- config ----
    mcp_url, api_key, timeout = _get_config()
    if not mcp_url:
        return {"success": False, "error": {"code": "C001", "message": "解析失败：文档解析服务当前不可用。建议：请联系管理员检查解析服务配置后重试。"}}

    try:
        parsed = urlparse(mcp_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URL")
    except Exception:
        return {"success": False, "error": {"code": "C001", "message": "解析失败：文档解析服务当前不可用。建议：请联系管理员检查解析服务配置后重试。"}}

    # ---- output path ----
    if output_file:
        out = Path(output_file)
    else:
        inp = Path(input_path)
        out = inp.parent / f"{inp.stem}.md"
    counter = 1
    original = out
    while out.exists():
        out = original.parent / f"{original.stem}_{counter}{original.suffix}"
        counter += 1
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        return {"success": False, "error": {"code": "O001", "message": "解析失败：无法写入输出目录。建议：请更换输出路径或检查目录权限。"}}
    output_path = out

    # ---- read file ----
    try:
        with open(input_path, "rb") as f:
            file_b64 = base64.b64encode(f.read()).decode("utf-8")
    except OSError:
        return {"success": False, "error": {"code": "F002", "message": "解析失败：当前文件无法读取。建议：请检查文件权限后重试。"}}

    # ---- call MCP ----

    try:
        client_kwargs = {"timeout": timeout}
        if api_key:
            client_kwargs["auth"] = api_key
        client = Client(mcp_url, **client_kwargs)
        async with client:
            result = await client.call_tool(
                "docparse",
                {
                    "file_content_base64": file_b64,
                    "file_name": Path(input_path).name,
                    "output_format": output_format,
                },
            )
    except Exception:
        return {"success": False, "error": {"code": "A001", "message": "解析失败：文档解析服务当前不可用。建议：请联系管理员检查解析服务配置后重试。"}}

    # ---- parse response ----
    try:
        if hasattr(result, "content") and result.content:
            response_text = result.content[0].text
        else:
            response_text = str(result)
        data = json.loads(response_text)
    except (json.JSONDecodeError, IndexError, AttributeError):
        return {"success": False, "error": {"code": "S002", "message": "解析失败：文档结果解析异常。建议：请稍后重试，或联系管理员检查解析服务。"}}

    if isinstance(data, dict) and "call_result" in data:
        data = data["call_result"]

    content, meta = extract_result(data, output_format)
    if not content or not content.strip():
        return {"success": False, "error": {"code": "S001", "message": "解析失败：文档解析服务未返回有效内容。建议：请确认文件内容清晰后重试。"}}

    # ---- write output ----
    try:
        output_path.write_text(content, encoding="utf-8")
    except OSError:
        return {"success": False, "error": {"code": "O002", "message": "解析失败：无法写入输出文件。建议：请更换输出路径或检查目录权限。"}}

    if output_path.stat().st_size == 0:
        return {"success": False, "error": {"code": "O002", "message": "解析失败：无法写入输出文件。建议：请更换输出路径或检查目录权限。"}}

    size_kb = output_path.stat().st_size / 1024
    summary = content[:200].replace("\n", " ")
    return {
        "success": True,
        "result": {
            "output_path": str(output_path),
            "size_kb": size_kb,
            "format": meta.get("format", "unknown"),
            "summary": summary,
            "content": content,
        }
    }


def main() -> None:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Document parser client via MCP.")
    parser.add_argument("input_file", help="Path to the document/image to parse")
    parser.add_argument("output_file", nargs="?", default=None, help="Output file path (optional)")
    parser.add_argument(
        "--output", choices=["markdown", "json", "both"], default="markdown",
        help="Output format (default: markdown)"
    )
    args = parser.parse_args()

    asyncio.run(parse_document(args.input_file, args.output_file, args.output))


if __name__ == "__main__":
    main()
