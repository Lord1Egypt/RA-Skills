#!/usr/bin/env python3
"""
翔云通用文档/表格识别脚本
支持：识别单张/批量图片，可选导出为 Excel/Word/Markdown/PDF/TXT/OFD

使用方法:
    # 识别单张图片（仅识别，结果打印到控制台）
    python recognize_table.py --image <路径>

    # 识别并立即导出为 Excel
    python recognize_table.py --image <路径> --export xls

    # 批量识别目录下所有图片
    python recognize_table.py --dir <目录路径>

    # 仅下载已识别结果（已有 consumeId）
    python recognize_table.py --download --consume-id <id> --num 1-1 --type xls --output result.xls

凭据加载顺序：命令行参数 > ./config.json > 环境变量 NETOCR_KEY/NETOCR_SECRET
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.parse
from pathlib import Path

try:
    import requests
except ImportError:
    print("缺少依赖，请先执行：pip install requests")
    sys.exit(1)

try:
    from PIL import Image as _PILImage
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False

# ──────────────────────────────────────────────
# API 配置
# ──────────────────────────────────────────────
API_RECOG_BASE64 = "https://netocr.com/api/recog_table_base64"
API_RECOG_FILE   = "https://netocr.com/api/recog_table_file"
API_DOWNLOAD     = "https://netocr.com/api/download_file"

SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".ofd", ".pdf"}

# 需要先转换为 JPG 再发送的格式（平台 typeId=3050 对这些格式返回 -8 产品类型错误）
CONVERT_TO_JPG_EXTS = {".tif", ".tiff", ".webp"}

EXPORT_EXT_MAP = {
    "xls":       ".xls",
    "flowWord":  ".docx",
    "boxWord":   ".docx",
    "md":        ".md",
    "pdf":       ".pdf",
    "txt":       ".txt",
    "ofd":       ".ofd",
}


# ──────────────────────────────────────────────
# 凭据加载（三级优先）
# ──────────────────────────────────────────────
def load_credentials(key=None, secret=None):
    """
    加载顺序：命令行参数 > ./config.json（Skill 自目录）> 环境变量
    config.json 路径为脚本同级目录下的 config.json
    """
    # 1. 命令行参数优先
    if key and secret:
        return key, secret

    # 2. Skill 自目录配置文件（./config.json，Skill 根目录下）
    # 脚本在 scripts/ 子目录，需要往上一级找 Skill 根目录
    skill_root = Path(__file__).parent.parent.resolve()
    config_path = skill_root / "config.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        k = cfg.get("key", "").strip()
        s = cfg.get("secret", "").strip()
        if k and s:
            return k, s

    # 3. 环境变量兜底
    return os.environ.get("NETOCR_KEY", "").strip(), os.environ.get("NETOCR_SECRET", "").strip()


# ──────────────────────────────────────────────
# 格式转换：TIF/WEBP → JPG（平台不支持时预处理）
# ──────────────────────────────────────────────
def convert_to_jpg(image_path):
    """
    将 TIF/WEBP 等平台不支持的格式转换为临时 JPG 文件。
    返回 (jpg_path, is_temp)：
      - jpg_path  : 转换后的 JPG 路径（或原路径，若无需转换）
      - is_temp   : True 表示是临时文件，调用方负责识别后删除
    """
    path = Path(image_path)
    if path.suffix.lower() not in CONVERT_TO_JPG_EXTS:
        return str(path), False   # 无需转换

    if not _PIL_AVAILABLE:
        print("  [WARN] Pillow 未安装，无法转换格式，跳过此文件")
        print("         请执行：pip install Pillow")
        return None, False

    tmp_path = path.with_suffix(".___tmp_converted.jpg")
    try:
        img = _PILImage.open(str(path))
        # TIF 可能是多帧（多页），只取第一帧
        if hasattr(img, "n_frames") and img.n_frames > 1:
            img.seek(0)
        # 转为 RGB（去除 alpha/调色板，确保 JPEG 兼容）
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        img.save(str(tmp_path), "JPEG", quality=95)
        print(f"  [CONV] {path.suffix.upper()} -> JPG ({tmp_path.name})")
        return str(tmp_path), True
    except Exception as e:
        print(f"  [WARN] Format conversion failed: {e}")
        return None, False


# ──────────────────────────────────────────────
# 图片转 Base64
# ──────────────────────────────────────────────
def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ──────────────────────────────────────────────
# 表格识别（Base64）
# ──────────────────────────────────────────────
def recognize_by_base64(image_path, key, secret, options=None):
    img_b64 = image_to_base64(image_path)
    payload = {
        "img": img_b64,
        "key": key,
        "secret": secret,
        "typeId": 3050,
        "format": "json",
    }
    if options:
        payload.update(options)
    resp = requests.post(API_RECOG_BASE64, data=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


# ──────────────────────────────────────────────
# 表格识别（File 上传）
# ──────────────────────────────────────────────
def recognize_by_file(image_path, key, secret, options=None):
    with open(image_path, "rb") as f:
        files = {"file": f}
        data = {
            "key": key,
            "secret": secret,
            "typeId": 3050,
            "format": "json",
        }
        if options:
            data.update(options)
        resp = requests.post(API_RECOG_FILE, files=files, data=data, timeout=60)
    resp.raise_for_status()
    return resp.json()


# ──────────────────────────────────────────────
# 下载导出文件（两步：获取 OSS URL → 下载实际文件）
# ──────────────────────────────────────────────
def download_file(consume_id, num, file_type, save_path):
    """
    consume_id : 识别返回的唯一 ID
    num        : 页范围，如 "1-1" / "1-5"
    file_type  : xls / flowWord / boxWord / md / pdf / txt / ofd
    save_path  : 本地保存路径

    注意：下载接口返回的是预签名 OSS URL，需要再请求该 URL 获取实际文件。
    翔云 OSS 返回 http:// URL（服务端对 http 传输有内容截断限制），
    改用 https 直连阿里云 OSS 获取完整文件。
    """
    payload = {
        "consumeId": consume_id,
        "num": num,
        "type": file_type,
    }
    resp = requests.post(API_DOWNLOAD, data=payload, timeout=60)

    # 解析 OSS URL（响应格式：{"message": {"status": 0, "value": "http://..."}}）
    try:
        result = resp.json()
        msg = result.get("message", {})
        oss_url = msg.get("value", "")
    except Exception:
        oss_url = ""

    if not oss_url or not oss_url.startswith("http"):
        # 直接返回内容（兜底）
        if resp.status_code == 200 and len(resp.content) > 1000:
            with open(save_path, "wb") as f:
                f.write(resp.content)
            return True, str(save_path)
        return False, f"HTTP {resp.status_code}: {resp.text[:200]}"

    # 从 OSS URL 下载实际文件
    # 翔云返回 http://product.netocr.com/... 预签名 URL，http 传输服务端截断不完整。
    # product.netocr.com 是阿里云 OSS cn-beijing 的 CNAME，
    # 直接请求 https://oss-cn-beijing.aliyuncs.com/... 并附带 Host 头，证书完全合法。
    try:
        parsed = urllib.parse.urlparse(oss_url)
        original_host = parsed.hostname  # product.netocr.com
        # 换用阿里云 OSS 官方域名（包含在证书 SAN 中），标准 https 无需任何 ssl 调整
        oss_https = oss_url.replace("http://", "https://").replace(
            original_host, "oss-cn-beijing.aliyuncs.com"
        )
        resp = requests.get(
            oss_https,
            headers={"Host": original_host},
            timeout=60,
        )
        if resp.status_code == 200 and len(resp.content) > 1000:
            with open(save_path, "wb") as f:
                f.write(resp.content)
            return True, str(save_path)
        return False, f"OSS download failed: HTTP {resp.status_code}"
    except Exception as e:
        return False, f"OSS request error: {e}"


# ──────────────────────────────────────────────
# 格式化并渲染识别结果（Markdown 表格）
# ──────────────────────────────────────────────
def format_result(result):
    # API 响应格式：
    # {
    #   "message": {"status": 0, "value": "识别完成"},
    #   "info": {
    #     "result": [...],       # HTML 表格内容
    #     "num": "1-1",
    #     "consumeId": "...",
    #     "typeId": 3050
    #   }
    # }
    msg = result.get("message", {})
    status = msg.get("status", -1)

    if str(status) != "0":
        return f"\n[FAIL] Recognition failed (status={status}): {msg.get('value', '')}\n"

    info = result.get("info", {})
    consume_id = info.get("consumeId", "N/A")
    num_pages = info.get("num", "N/A")
    html_tables = info.get("result", [])

    lines = [
        f"\n[OK] Recognition succeeded",
        f"   consumeId : {consume_id}",
        f"   pages      : {num_pages}",
        f"   HTML tables: {len(html_tables)} block(s)",
    ]

    return "\n".join(lines)


# ──────────────────────────────────────────────
# 识别单张图片
# ──────────────────────────────────────────────
def process_single(image_path, key, secret, export_type=None, options=None):
    image_path = Path(image_path)
    print(f"\n[FILE] {image_path.name}")

    # 格式转换：TIF/WEBP 先转为临时 JPG
    actual_path, is_temp = convert_to_jpg(str(image_path))
    if actual_path is None:
        # 转换失败（Pillow 缺失或异常），跳过
        return False

    # 优先 Base64，失败后降级到 File 方式
    try:
        try:
            result = recognize_by_base64(actual_path, key, secret, options)
        except Exception as e:
            print(f"  Base64 failed ({e}), trying File upload...")
            result = recognize_by_file(actual_path, key, secret, options)
    finally:
        # 清理临时转换文件
        if is_temp:
            try:
                Path(actual_path).unlink()
            except Exception:
                pass

    print(format_result(result))

    # 检查识别是否成功（status=0）
    msg = result.get("message", {})
    if str(msg.get("status", -1)) != "0":
        return False  # 识别失败

    # 保存原始 JSON
    json_path = image_path.with_suffix(".table_result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  [SAVE] JSON saved: {json_path}")

    # 按需导出
    if export_type:
        info = result.get("info", {})
        consume_id = info.get("consumeId")
        total_pages = info.get("num", "1-1")
        if not consume_id:
            print("  [WARN] No consumeId, cannot export")
            return result

        ext = EXPORT_EXT_MAP.get(export_type, f".{export_type}")
        save_path = image_path.with_suffix(ext)
        num_str = f"1-{total_pages}"
        ok, msg = download_file(consume_id, num_str, export_type, str(save_path))
        if ok:
            print(f"  [EXPORT] {export_type.upper()} -> {save_path}")
        else:
            print(f"  [FAIL] Export failed: {msg}")

    return result


# ──────────────────────────────────────────────
# 批量处理目录
# ──────────────────────────────────────────────
def process_directory(dir_path, key, secret, export_type=None, options=None):
    dir_path = Path(dir_path)
    image_files = [
        f for f in dir_path.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTS
    ]
    if not image_files:
        print(f"[WARN] No supported images found: {dir_path}")
        return

    print(f"\n[DIR] {dir_path}")
    print(f"   共找到 {len(image_files)} 个文件\n")

    success, failed = 0, 0
    for img in image_files:
        try:
            ok = process_single(str(img), key, secret, export_type, options)
            if ok is not False:
                success += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  [FAIL] {img.name} -> {e}")
            failed += 1
        time.sleep(0.5)  # 防止请求频率过高

    print(f"\n[DONE] Success: {success}, Failed: {failed}")


# ──────────────────────────────────────────────
# 主入口
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="翔云通用表格识别工具")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--image", help="单张图片路径")
    group.add_argument("--dir",   help="批量识别目录路径")
    group.add_argument("--download", action="store_true", help="仅下载已识别结果")

    parser.add_argument("--key",    default="", help="OCR Key（可省略，从配置文件读取）")
    parser.add_argument("--secret", default="", help="OCR Secret（可省略，从配置文件读取）")
    parser.add_argument("--export", default="md",
                        choices=list(EXPORT_EXT_MAP.keys()),
                        help="识别后立即导出的格式（默认：md）")

    # 下载专用参数
    parser.add_argument("--consume-id", help="识别结果的唯一 ID（下载模式必填）")
    parser.add_argument("--num",        default="1-1", help="页范围，如 1-1 / 1-5（下载模式）")
    parser.add_argument("--type",       help="导出格式（下载模式必填）")
    parser.add_argument("--output",     help="导出文件保存路径（下载模式）")

    # 可选识别参数
    parser.add_argument("--language",          type=int, default=0)
    parser.add_argument("--auto-rotation",     type=int, default=1)
    parser.add_argument("--incline-correct",   type=int, default=0)
    parser.add_argument("--remove-watermark",  type=int, default=0)
    parser.add_argument("--layout",            type=int, default=1)

    args = parser.parse_args()

    # 加载凭据
    key, secret = load_credentials(args.key, args.secret)
    if not key or not secret:
        skill_root = Path(__file__).parent.parent.resolve()
        config_path = skill_root / "config.json"
        print("\n[ERROR] 未找到 OCR 凭据")
        print(f"  请创建配置文件：{config_path}")
        print('  内容：{"key": "你的Key", "secret": "你的Secret"}')
        print("  或设置环境变量：NETOCR_KEY / NETOCR_SECRET")
        print("  或传入参数：--key <key> --secret <secret>")
        sys.exit(1)

    if not _PIL_AVAILABLE:
        print("[WARN] Pillow 未安装，TIF/WEBP 格式将无法自动转换为 JPG")
        print("       如需处理此类格式，请执行：pip install Pillow")

    options = {
        "nLanguage":    args.language,
        "autoRotation": args.auto_rotation,
        "layout":       args.layout,
    }

    # 执行对应模式
    if args.download:
        # 仅下载模式
        if not args.consume_id or not args.type:
            print("[FAIL] Download mode requires --consume-id and --type")
            sys.exit(1)
        output = args.output or f"result{EXPORT_EXT_MAP.get(args.type, '.bin')}"
        ok, msg = download_file(args.consume_id, args.num, args.type, output)
        if ok:
            print(f"\n[OK] Downloaded: {msg}")
        else:
            print(f"\n[FAIL] Download failed: {msg}")

    elif args.image:
        if not os.path.exists(args.image):
            print(f"[FAIL] File not found: {args.image}")
            sys.exit(1)
        process_single(args.image, key, secret, args.export, options)

    elif args.dir:
        if not os.path.isdir(args.dir):
            print(f"[FAIL] Directory not found: {args.dir}")
            sys.exit(1)
        process_directory(args.dir, key, secret, args.export, options)


if __name__ == "__main__":
    main()
