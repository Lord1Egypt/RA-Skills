#!/usr/bin/env python3
"""
小红书笔记发布脚本 - 增强版
使用 xhs 库直接发布（本地签名）。
"""

import argparse
import contextlib
import glob
import io
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

def parse_cookie(cookie_string: str) -> Dict[str, str]:
    """解析 Cookie 字符串为字典。"""
    cookies = {}
    for item in cookie_string.split(";"):
        item = item.strip()
        if "=" in item:
            key, value = item.split("=", 1)
            cookies[key.strip()] = value.strip()
    return cookies


def load_cookie() -> str:
    """从环境变量 XHS_COOKIE 加载 Cookie。"""
    cookie = os.getenv("XHS_COOKIE")
    if not cookie:
        print("❌ 错误: 未找到 XHS_COOKIE")
        print("请通过环境变量配置：export XHS_COOKIE=\"your_cookie_string\"")
        print("\nCookie 获取方式：")
        print("1. 在浏览器中登录小红书（https://www.xiaohongshu.com）")
        print("2. 打开开发者工具（F12）")
        print("3. 在 Network 标签中查看任意请求的 Cookie 头")
        print("4. 复制完整的 cookie 字符串")
        sys.exit(1)

    return cookie


def validate_cookie(cookie_string: str) -> bool:
    """验证 Cookie 是否包含必要字段。"""
    cookies = parse_cookie(cookie_string)
    required_fields = ["a1", "web_session"]
    missing = [field for field in required_fields if field not in cookies]

    if missing:
        print(f"⚠️ Cookie 可能不完整，缺少字段: {', '.join(missing)}")
        print("这可能导致签名失败，请确保 Cookie 包含 a1 和 web_session 字段")
        return False

    return True


def validate_images(image_paths: List[str]) -> List[str]:
    """验证图片文件是否存在。"""
    valid_images = []
    for path in image_paths:
        if os.path.exists(path):
            valid_images.append(os.path.abspath(path))
        else:
            print(f"⚠️ 警告: 图片不存在 - {path}")

    if not valid_images:
        print("❌ 错误: 没有有效的图片文件")
        sys.exit(1)

    return valid_images


def natural_sort_key(text: str):
    """用于对 card_1/card_2/... 做自然排序。"""
    return [int(tok) if tok.isdigit() else tok.lower() for tok in re.split(r"(\d+)", text)]


def load_desc(desc: str, desc_file: Optional[str]) -> str:
    """从参数或文件加载描述，保留真实换行。"""
    if desc and desc_file:
        print("❌ 错误: 不能同时使用 --desc 和 --desc-file")
        sys.exit(1)
    if desc_file:
        path = Path(desc_file)
        if not path.exists():
            print(f"❌ 错误: 描述文件不存在 - {desc_file}")
            sys.exit(1)
        return path.read_text(encoding="utf-8")
    return desc or ""


def load_images(images: List[str], images_glob: Optional[str]) -> List[str]:
    """从显式路径或 glob 加载图片列表，并做自然排序。"""
    if images and images_glob:
        print("❌ 错误: 不能同时使用 --images 和 --images-glob")
        sys.exit(1)
    if images_glob:
        matched = sorted(glob.glob(images_glob), key=natural_sort_key)
        if not matched:
            print(f"❌ 错误: images glob 未匹配到文件 - {images_glob}")
            sys.exit(1)
        return matched
    return images


@contextlib.contextmanager
def maybe_suppress_output(verbose: bool):
    """默认隐藏第三方库输出，避免噪音和潜在敏感信息泄露。"""
    if verbose:
        yield
        return
    with io.StringIO() as _out, io.StringIO() as _err:
        with contextlib.redirect_stdout(_out), contextlib.redirect_stderr(_err):
            yield


class LocalPublisher:
    """本地发布模式：直接使用 xhs 库。"""

    def __init__(self, cookie: str, *, verbose: bool = False):
        self.cookie = cookie
        self.verbose = verbose
        self.client = None

    def init_client(self):
        """初始化 xhs 客户端。"""
        try:
            from xhs import XhsClient
            from xhs.help import sign as local_sign
        except ImportError:
            print("❌ 错误: 缺少 xhs 库")
            print("请运行: pip install xhs")
            sys.exit(1)

        cookies = parse_cookie(self.cookie)
        a1 = cookies.get("a1", "")
        b1 = cookies.get("b1", "")

        def sign_func(uri, data=None, **kwargs):
            """
            xhs 库对 sign 回调的调用参数在不同版本间可能不同。
            用 **kwargs 兼容，并优先使用 Cookie 中解析出的 a1/b1。
            """
            return local_sign(
                uri,
                data,
                ctime=kwargs.get("ctime"),
                a1=a1 or kwargs.get("a1", ""),
                b1=b1 or kwargs.get("b1", ""),
            )

        self.client = XhsClient(cookie=self.cookie, sign=sign_func)

    def publish(
        self,
        title: str,
        desc: str,
        images: List[str],
        is_private: bool = False,
        post_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        """发布图文笔记。"""
        print("\n🚀 准备发布笔记（本地模式）...")
        print(f"  📌 标题: {title}")
        print(f"  📝 描述: {desc[:50]}..." if len(desc) > 50 else f"  📝 描述: {desc}")
        print(f"  🖼️ 图片数量: {len(images)}")
        print(f"  🔒 私密: {is_private}")

        try:
            with maybe_suppress_output(self.verbose):
                result = self.client.create_image_note(
                    title=title,
                    desc=desc,
                    files=images,
                    is_private=is_private,
                    post_time=post_time,
                )

            print("\n✨ 笔记发布成功！")
            if isinstance(result, dict):
                note_id = result.get("note_id") or result.get("id")
                if note_id:
                    print(f"  📎 笔记ID: {note_id}")
                    print(f"  🔗 链接: https://www.xiaohongshu.com/explore/{note_id}")

            return result
        except Exception as exc:
            error_msg = str(exc)
            print(f"\n❌ 发布失败: {error_msg}")
            if "sign" in error_msg.lower() or "signature" in error_msg.lower():
                print("\n💡 签名错误排查建议：")
                print("1. 确保 Cookie 包含有效的 a1 和 web_session 字段")
                print("2. Cookie 可能已过期，请重新获取")
            elif "cookie" in error_msg.lower():
                print("\n💡 Cookie 错误排查建议：")
                print("1. 确保 Cookie 格式正确")
                print("2. Cookie 可能已过期，请重新获取")
                print("3. 确保 Cookie 来自已登录的小红书网页版")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="将图片发布为小红书笔记",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--title", "-t", required=True, help="笔记标题（不超过20字）")
    parser.add_argument("--desc", "-d", default="", help="笔记描述/正文内容")
    parser.add_argument("--desc-file", default=None, help="从 UTF-8 文件读取笔记描述/正文")
    parser.add_argument("--images", "-i", nargs="+", default=[], help="图片文件路径")
    parser.add_argument("--images-glob", default=None, help="使用 glob 匹配图片，会按自然序排序")
    parser.add_argument("--require-image-count", type=int, default=None, help="要求图片数量必须等于该值")

    visibility_group = parser.add_mutually_exclusive_group()
    visibility_group.add_argument("--private", dest="private", action="store_true", help="设为私密笔记（默认）")
    visibility_group.add_argument("--public", dest="private", action="store_false", help="设为公开笔记")
    parser.set_defaults(private=True)

    parser.add_argument("--post-time", default=None, help="定时发布时间（格式：2024-01-01 12:00:00）")
    parser.add_argument("--dry-run", action="store_true", help="仅验证，不实际发布")
    parser.add_argument("--verbose", action="store_true", help="显示底层库输出")
    parser.add_argument("--debug-json", default=None, help="将最终发布结果写入 JSON 文件")
    parser.add_argument("--yes", "-y", action="store_true", help="兼容旧参数；当前脚本不再交互确认")

    args = parser.parse_args()

    if len(args.title) > 20:
        print("⚠️ 警告: 标题超过20字，将被截断")
        args.title = args.title[:20]

    cookie = load_cookie()
    validate_cookie(cookie)

    desc = load_desc(args.desc, args.desc_file)
    image_inputs = load_images(args.images, args.images_glob)
    if not image_inputs:
        print("❌ 错误: 必须提供图片（--images 或 --images-glob）")
        sys.exit(1)

    valid_images = validate_images(image_inputs)
    if args.require_image_count is not None and len(valid_images) != args.require_image_count:
        print(f"❌ 错误: 图片数量不符合要求：期望 {args.require_image_count}，实际 {len(valid_images)}")
        sys.exit(1)

    if args.dry_run:
        print("\n🔍 验证模式 - 不会实际发布")
        print(f"  📌 标题: {args.title}")
        print(f"  📝 描述: {desc}")
        print(f"  🖼️ 图片: {valid_images}")
        print(f"  🔒 私密: {args.private}")
        print(f"  ⏰ 定时: {args.post_time or '立即发布'}")
        print("  📡 模式: 本地")
        print("\n✅ 验证通过，可以发布")
        return

    publisher = LocalPublisher(cookie, verbose=args.verbose)
    publisher.init_client()

    try:
        result = publisher.publish(
            title=args.title,
            desc=desc,
            images=valid_images,
            is_private=args.private,
            post_time=args.post_time,
        )
        if args.debug_json:
            Path(args.debug_json).write_text(
                json.dumps(result, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
