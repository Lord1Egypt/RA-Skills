#!/usr/bin/env python3
"""
Local QR code generate & decode skill for OpenClaw.
本地二维码生成与识别，不依赖外部 HTTP 接口。
"""

import json
import os
import sys
from typing import Any, Dict


def _normalize_local_path(user_path: str, field: str) -> Dict[str, Any]:
    """
    规范化并限制本地文件路径，只允许在当前工作目录及其子目录内读写。
    禁止绝对路径和目录穿越（包含 ..）。
    """
    if not user_path:
        return {
            "error": "invalid_param",
            "message": f"field '{field}' is empty",
        }

    # 禁止绝对路径
    if os.path.isabs(user_path):
        return {
            "error": "invalid_path",
            "message": f"Absolute path is not allowed for '{field}'",
        }

    # 规范化并检查目录穿越
    norm = os.path.normpath(user_path)
    if norm.startswith("..") or norm == "..":
        return {
            "error": "invalid_path",
            "message": f"Path traversal is not allowed for '{field}'",
        }

    base = os.getcwd()
    full = os.path.join(base, norm)
    return {"error": None, "path": full, "relative": norm}


def _encode_qr(req: Dict[str, Any]) -> Dict[str, Any]:
    try:
        import qrcode
        from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
    except ImportError:
        return {
            "error": "missing_dependency",
            "message": "Python package 'qrcode' (with Pillow) is required. Please install via: pip install \"qrcode[pil]\"",
        }

    text = req.get("text") or req.get("data") or req.get("url")
    if not text:
        return {"error": "missing_param", "message": "text (or data/url) is required"}

    out_raw = req.get("out") or "qrcode.png"
    version = req.get("version")
    box_size = int(req.get("box_size", 10))
    border = int(req.get("border", 4))
    ec = str(req.get("error_correction", "M")).upper()

    ec_map = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H,
    }
    ec_const = ec_map.get(ec, ERROR_CORRECT_M)

    qr = qrcode.QRCode(
        version=None if version in (None, "", 0) else int(version),
        error_correction=ec_const,
        box_size=box_size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)

    fill_color = req.get("fill_color", "black")
    back_color = req.get("back_color", "white")

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    safe = _normalize_local_path(out_raw, "out")
    if safe["error"]:
        return safe

    out = safe["path"]
    out_dir = os.path.dirname(out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    try:
        img.save(out)
    except Exception as e:
        return {"error": "save_failed", "message": str(e), "path": out}

    return {
        "path": safe["relative"],
        "text": text,
        "error_correction": ec,
        "box_size": box_size,
        "border": border,
    }


def _decode_qr(req: Dict[str, Any]) -> Dict[str, Any]:
    try:
        import cv2
    except ImportError:
        return {
            "error": "missing_dependency",
            "message": "Python package 'opencv-python' is required for decode. Please install via: pip install opencv-python",
        }

    path_raw = req.get("path") or req.get("image") or req.get("file")
    if not path_raw:
        return {"error": "missing_param", "message": "path (or image/file) is required"}

    safe = _normalize_local_path(path_raw, "path")
    if safe["error"]:
        return safe

    path = safe["path"]
    if not os.path.isfile(path):
        return {"error": "file_not_found", "message": f"File not found: {safe['relative']}"}

    img = cv2.imread(path)
    if img is None:
        return {"error": "load_failed", "message": f"Cannot read image: {safe['relative']}"}

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)
    if not data:
        return {
            "error": "decode_failed",
            "message": "No QR code detected or decode failed.",
            "path": safe["relative"],
        }

    return {
        "text": data,
        "points": points.tolist() if points is not None else None,
        "path": safe["relative"],
    }


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  qrcode2.py encode '{\"text\":\"https://www.jisuapi.com\",\"out\":\"out/qrcode.png\"}'\n"
            "  qrcode2.py decode '{\"path\":\"out/qrcode.png\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    cmd = sys.argv[1].strip().lower()

    req: Dict[str, Any] = {}
    if len(sys.argv) >= 3 and sys.argv[2].strip():
        raw = sys.argv[2]
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(obj, dict):
            print("Error: JSON body must be an object.", file=sys.stderr)
            sys.exit(1)
        req = obj

    if cmd == "encode":
        result = _encode_qr(req)
    elif cmd == "decode":
        result = _decode_qr(req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
QR code generate & decode skill for OpenClaw.
本地二维码生成与识别，不依赖外部 HTTP 接口。
"""

import json
import os
import sys
from typing import Any, Dict


def _encode_qr(req: Dict[str, Any]) -> Dict[str, Any]:
    try:
        import qrcode
        from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
    except ImportError:
        return {
            "error": "missing_dependency",
            "message": "Python package 'qrcode' (with Pillow) is required. Please install via: pip install \"qrcode[pil]\"",
        }

    text = req.get("text") or req.get("data") or req.get("url")
    if not text:
        return {"error": "missing_param", "message": "text (or data/url) is required"}

    out_raw = req.get("out") or "qrcode.png"
    version = req.get("version")
    box_size = int(req.get("box_size", 10))
    border = int(req.get("border", 4))
    ec = str(req.get("error_correction", "M")).upper()

    ec_map = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H,
    }
    ec_const = ec_map.get(ec, ERROR_CORRECT_M)

    qr = qrcode.QRCode(
        version=None if version in (None, "", 0) else int(version),
        error_correction=ec_const,
        box_size=box_size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)

    fill_color = req.get("fill_color", "black")
    back_color = req.get("back_color", "white")

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    safe = _normalize_local_path(out_raw, "out")
    if safe["error"]:
        return safe

    out = safe["path"]
    out_dir = os.path.dirname(out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    try:
        img.save(out)
    except Exception as e:
        return {"error": "save_failed", "message": str(e), "path": out}

    return {
        "path": safe["relative"],
        "text": text,
        "error_correction": ec,
        "box_size": box_size,
        "border": border,
    }


def _decode_qr(req: Dict[str, Any]) -> Dict[str, Any]:
    try:
        import cv2
    except ImportError:
        return {
            "error": "missing_dependency",
            "message": "Python package 'opencv-python' is required for decode. Please install via: pip install opencv-python",
        }

    path_raw = req.get("path") or req.get("image") or req.get("file")
    if not path_raw:
        return {"error": "missing_param", "message": "path (or image/file) is required"}

    safe = _normalize_local_path(path_raw, "path")
    if safe["error"]:
        return safe

    path = safe["path"]
    if not os.path.isfile(path):
        return {"error": "file_not_found", "message": f"File not found: {safe['relative']}"}

    img = cv2.imread(path)
    if img is None:
        return {"error": "load_failed", "message": f"Cannot read image: {safe['relative']}"}

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)
    if not data:
        return {
            "error": "decode_failed",
            "message": "No QR code detected or decode failed.",
            "path": safe["relative"],
        }

    return {
        "text": data,
        "points": points.tolist() if points is not None else None,
        "path": safe["relative"],
    }


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  qrcode.py encode '{\"text\":\"https://www.jisuapi.com\",\"out\":\"out/qrcode.png\"}'\n"
            "  qrcode.py decode '{\"path\":\"out/qrcode.png\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    cmd = sys.argv[1].strip().lower()

    req: Dict[str, Any] = {}
    if len(sys.argv) >= 3 and sys.argv[2].strip():
        raw = sys.argv[2]
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(obj, dict):
            print("Error: JSON body must be an object.", file=sys.stderr)
            sys.exit(1)
        req = obj

    if cmd == "encode":
        result = _encode_qr(req)
    elif cmd == "decode":
        result = _decode_qr(req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

