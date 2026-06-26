#!/usr/bin/env python3
"""
xqximage.py - Ark (火山引擎豆包) 文生图
调用火山方舟 /images/generations API；成功时将图片 URL 写到标准输出返回调用方，不下载图片文件。
"""

import json
import os
import re
import sys
import urllib.request

# 默认配置
API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
DEFAULT_SIZE = "2K"
SIZE_OPTIONS = ["2K", "4K","1456x816", "2048x2048", "2560x1440", "1440x2560", "2304x1728", "1728x2304"]
_SIZE_WH = re.compile(r"^\d+x\d+$")
# OpenClaw 工作目录下固定路径：Agent 须先将用户提示词写入该文件，再在本目录为 cwd 时执行 --file（见 SKILL.md）
PROMPT_FILE_PARTS = ("wdatas", "xqx-img-prompt.txt")

# Fix Windows encoding
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def load_api_key() -> str:
    """从环境变量读取 ARK_API_KEY（由外部调用方设置）"""
    return os.environ.get("ARK_API_KEY", "")


def load_image_model() -> str:
    """从环境变量读取 ARK_IMAGE_MODEL（必填，无默认值）"""
    return (os.environ.get("ARK_IMAGE_MODEL") or "").strip()


def prompt_file_path() -> str:
    """当前工作目录下的 wdatas/xqx-img-prompt.txt（由 Agent 写入，路径不可配置）"""
    return os.path.join(os.getcwd(), *PROMPT_FILE_PARTS)


def load_prompt_from_wdatas() -> str:
    path = prompt_file_path()
    if not os.path.isfile(path):
        print(f"Error: 未找到 {path}，请在工作目录的 wdatas/xqx-img-prompt.txt 写入提示词")
        raise SystemExit(1)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.strip():
        print(f"Error: {path} 为空")
        raise SystemExit(1)
    return text


def parse_size_only_args(rest: list[str], mode_label: str) -> str:
    """--file 模式下仅允许可选的 size 参数"""
    size = DEFAULT_SIZE
    unknown: list[str] = []
    for a in rest:
        if a in SIZE_OPTIONS or _SIZE_WH.match(a):
            size = a
        else:
            unknown.append(a)
    if unknown:
        print(f"Error: {mode_label} 下仅可额外传入尺寸，无法识别: {' '.join(unknown)}")
        raise SystemExit(1)
    return size


def generate_image(
    prompt: str,
    api_key: str,
    model: str,
    size: str = DEFAULT_SIZE,
    watermark: bool = False,
    response_format: str = "url",
) -> str | None:
    """调用 Ark API 生成图片，返回图片 URL"""
    body = json.dumps({
        "model": model,
        "prompt": prompt,
        "sequential_image_generation": "disabled",
        "response_format": response_format,
        "size": size,
        "stream": False,
        "watermark": watermark,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())

    urls = data.get("data", [])
    if urls and len(urls) > 0:
        return urls[0].get("url")
    return None


def print_usage() -> None:
    """打印用法"""
    print("用法:")
    print("  xqximage.py <prompt> [size]")
    print("  xqximage.py --file | -f [size]   # 从工作目录 wdatas/xqx-img-prompt.txt 读入提示词")
    print("")
    print("参数说明:")
    print("  prompt  : 图片描述（必填，短文案可用命令行）")
    print("  --file  : 长文案请写入 ./wdatas/xqx-img-prompt.txt（相对当前工作目录），再使用本选项")
    print("  size    : 尺寸，如 2K、4K、2560x1440（默认 2K）")
    print("")
    print("环境变量:")
    print("  ARK_API_KEY     : API Key（必填）")
    print("  ARK_IMAGE_MODEL : 模型/端点 ID（必填，无默认值）")
    print("")
    print("示例:")
    print('  xqximage.py "星际穿越，黑洞，电影大片"')
    print('  xqximage.py "可爱的猫咪" 4K')
    print('  xqximage.py "风景照" 2560x1440')
    print("  xqximage.py --file")
    print("  xqximage.py -f 4K")


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print_usage()
        return 0 if not args else 1

    if args[0] in ("--file", "-f"):
        prompt = load_prompt_from_wdatas()
        size = parse_size_only_args(args[1:], "--file")
    else:
        prompt = args[0]
        size = DEFAULT_SIZE
        for a in args[1:]:
            if a in SIZE_OPTIONS or _SIZE_WH.match(a):
                size = a

    api_key = load_api_key()
    if not api_key:
        print("Error: 请由调用方设置 ARK_API_KEY 环境变量")
        return 1

    model = load_image_model()
    if not model:
        print("Error: 请设置 ARK_IMAGE_MODEL 环境变量（方舟模型/推理端点 ID，无默认值）")
        return 1

    print("========== XQX Ark 文生图 ==========")
    print(f"描述: {prompt}")
    print(f"尺寸: {size}")
    print("====================================")
    print("")
    print("生成中...")

    try:
        image_url = generate_image(prompt, api_key, model=model, size=size)
    except Exception as e:
        print(f"Error: {e}")
        return 1

    if not image_url:
        print("Error: 生成失败，未返回图片 URL")
        return 1

    print("")
    print("========== 完成 ==========")
    print(f"图片URL: {image_url}")
    print("=========================")

    print(image_url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
