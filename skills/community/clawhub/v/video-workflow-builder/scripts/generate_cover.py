#!/usr/bin/env python3
"""
用 gpt-image-2 生成视频封面（走 B站 LLM 网关）。

两种模式：
    1. 纯文生图（默认）：只给 --prompt，模型凭描述生成整张封面。
       适合无「标准答案」的主体——泛指类别（一般会谈场景/城市/港口）、抽象概念（博弈/脱钩/焦虑）。
    2. 参考图生图（给 --reference-image 时自动启用）：把一张真实素材图喂给模型，
       让它在这个具体主体上重打光、重建背景，主体不溶解。
       适合有「标准答案」、观众会拿去和现实核对的具名实体——具体某位政要本人、某款武器型号、某座地标。
       注意：图生图是「忠实渲染器」，喂错就把错误也精美地还原，参考图务必先核验是不是对的那一个。

用法:
    python3 generate_cover.py --platform bilibili --prompt "封面画面描述" --output cover_bilibili.png
    python3 generate_cover.py --platform douyin   --prompt "..."        --output cover_douyin.png
    python3 generate_cover.py --platform bilibili --prompt "..." --reference-image 真人照.jpg --output cover.png

API key 与网关地址读取顺序（均：环境变量 > skill 目录 .env）:
    1. LLM_GATEWAY_API_KEY —— LLM 网关密钥（必填）
    2. LLM_GATEWAY_BASE_URL —— LLM 网关 base（OpenAI 兼容接口，必填），未配置则报错退出
    .env 已在 .gitignore 中，不会被提交。

依赖:
    pip install openai
"""

import argparse
import base64
import os
import sys

MODEL = "gpt-image-2"

# 平台 -> 画幅尺寸。取最接近目标比例的档位：
#   bilibili / baijiahao 4:3 横版  -> 1024x768
#   douyin / xiaohongshu / shipinhao 3:4 竖版 -> 768x1024
PLATFORM_SIZES = {
    "douyin": "768x1024",
    "bilibili": "1024x768",
    "xiaohongshu": "768x1024",
    "shipinhao": "768x1024",
    "baijiahao": "1024x768",
}


def _load_api_key():
    """按优先级读取 API key：环境变量 > skill 目录下的 .env。"""
    key = os.environ.get("LLM_GATEWAY_API_KEY")
    if key:
        return key.strip()
    # 兜底：读取 skill 根目录（本脚本上一级）下的 .env
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                name, _, value = line.partition("=")
                if name.strip() == "LLM_GATEWAY_API_KEY":
                    return value.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return None


def _load_base_url():
    """按优先级读取网关 base：环境变量 > skill 目录下的 .env。未配置返回 None。"""
    val = os.environ.get("LLM_GATEWAY_BASE_URL")
    if val:
        return val.strip()
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                name, _, value = line.partition("=")
                if name.strip() == "LLM_GATEWAY_BASE_URL":
                    return value.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return None


def resolve_size(platform, override):
    """手动指定 --size 时优先使用，否则按平台取默认画幅。"""
    if override:
        return override
    return PLATFORM_SIZES[platform]


def main():
    parser = argparse.ArgumentParser(description="生成视频封面 (gpt-image-2)")
    parser.add_argument(
        "--platform",
        required=True,
        choices=list(PLATFORM_SIZES.keys()),
        help="目标平台，决定画幅比例",
    )
    parser.add_argument("--prompt", required=True, help="封面画面描述提示词")
    parser.add_argument("--output", required=True, help="输出文件路径 (.png)")
    parser.add_argument(
        "--reference-image",
        default=None,
        help="可选，真实素材参考图路径。给了就走图生图（images.edit），"
        "让模型在这张真实主体上重打光重建背景——适合具名实体（政要本人/武器型号/地标）。"
        "务必先核验这张图确实是对的那一个（图生图会忠实还原你喂的错误）。不给则纯文生图。",
    )
    parser.add_argument(
        "--size",
        default=None,
        help="可选，手动指定尺寸如 1024x768，覆盖平台默认值",
    )
    args = parser.parse_args()

    api_key = _load_api_key()
    if not api_key:
        print(
            "错误：未找到 LLM_GATEWAY_API_KEY。\n"
            "请二选一：export LLM_GATEWAY_API_KEY=你的key，"
            "或在 skill 目录下的 .env 里写入 LLM_GATEWAY_API_KEY=你的key。",
            file=sys.stderr,
        )
        return 1

    try:
        import openai
    except ImportError:
        print("错误：未安装 openai 库。请运行:  pip install openai", file=sys.stderr)
        return 1

    base_url = _load_base_url()
    if not base_url:
        print(
            "错误：未找到 LLM_GATEWAY_BASE_URL。\n"
            "请二选一：export LLM_GATEWAY_BASE_URL=你的LLM网关base，"
            "或在 skill 目录下的 .env 里写入 LLM_GATEWAY_BASE_URL=你的LLM网关base。",
            file=sys.stderr,
        )
        return 1

    size = resolve_size(args.platform, args.size)
    client = openai.OpenAI(base_url=base_url, api_key=api_key)

    ref = args.reference_image
    if ref:
        if not os.path.isfile(ref):
            print("错误：参考图不存在：" + ref, file=sys.stderr)
            return 1
        print("正在用参考图生成 " + args.platform + " 封面 (" + size + ") ...", file=sys.stderr)
        print("参考图：" + ref + "（务必已确认这张确实是对的那一个）", file=sys.stderr)
        try:
            with open(ref, "rb") as img_f:
                result = client.images.edit(
                    model=MODEL,
                    image=img_f,
                    prompt=args.prompt,
                    size=size,
                    n=1,
                )
        except Exception as e:
            print("图生图失败：" + str(e), file=sys.stderr)
            return 1
    else:
        print("正在生成 " + args.platform + " 封面 (" + size + ") ...", file=sys.stderr)
        try:
            result = client.images.generate(
                model=MODEL,
                prompt=args.prompt,
                size=size,
                n=1,
            )
        except Exception as e:
            print("生成失败：" + str(e), file=sys.stderr)
            return 1

    data = result.data[0]
    image_bytes = None

    # 网关可能返回 base64 或 url，两种都兼容
    b64 = getattr(data, "b64_json", None)
    if b64:
        image_bytes = base64.b64decode(b64)
    else:
        url = getattr(data, "url", None)
        if not url:
            print("生成失败：返回结果中既无 b64_json 也无 url。", file=sys.stderr)
            return 1
        import urllib.request

        with urllib.request.urlopen(url) as resp:
            image_bytes = resp.read()

    with open(args.output, "wb") as f:
        f.write(image_bytes)

    print("已保存封面：" + args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
