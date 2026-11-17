#!/usr/bin/env python3
"""generate_xhs — content-engine 生成 mode (v2.0 M1) 的一键编排脚本。

输入 XHS 链接 + 我方品牌输入 → 输出我方版本的脚本 / 文案 / 标签 / Seedance prompt
（M1：文本类 only。M2 加 Nano Banana 出图，v2.1 加 Seedance 真生视频。）

工作区结构：
    docs/deconstructions/AIC-xxx-slug.md (v1 拆解卡)
    docs/deconstructions/AIC-xxx-slug-generated/   ← v2 产出
    └── GEN-260427-001-video/
        ├── script.md
        ├── caption.txt
        ├── cover.txt
        ├── desc.txt
        ├── tags.txt
        └── seedance-prompt.md  (仅 video 类型)

Usage:
    python3 generate_xhs.py <link> --type video --count 1
    python3 generate_xhs.py <link> --type image --count 8 --product-imgs ./photos/
    python3 generate_xhs.py <link> --type script --count 1
    python3 generate_xhs.py --check                # 仅环境检查
"""

from __future__ import annotations
import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

# Python 版本守卫
if sys.version_info < (3, 10):
    print(
        f"❌ Python {sys.version_info.major}.{sys.version_info.minor} 不支持。"
        f" 本 skill 需要 Python 3.10+。",
        file=sys.stderr,
    )
    sys.exit(2)

sys.path.insert(0, str(Path(__file__).parent))

from content_engine import __version__
from content_engine.generate import generate, GenerateInput
from content_engine.llm import OfoxError


def log(msg: str) -> None:
    """所有进度信息走 stderr，stdout 只输出最终 JSON 摘要。"""
    print(msg, file=sys.stderr, flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("link", nargs="?", help="XHS 链接（短链/长链/note_id/分享口令）")
    ap.add_argument(
        "--type",
        choices=["video", "image", "script"],
        default="video",
        help="生成类型（默认 video）",
    )
    ap.add_argument(
        "--count",
        type=int,
        default=1,
        help="生成数量（视频时长档/图片张数，默认 1）",
    )
    ap.add_argument(
        "--product-imgs",
        type=Path,
        help="我方产品图目录或单张路径",
    )
    ap.add_argument(
        "--product-usp",
        default="",
        help="我方产品卖点（材质/工艺/价格带）",
    )
    ap.add_argument("--out", type=Path, help="自定义输出目录")
    ap.add_argument("--fresh", action="store_true", help="强制重拆解（绕开缓存）")
    ap.add_argument("--check", action="store_true", help="仅环境检查（含 OFOX_API_KEY）")
    ap.add_argument(
        "--no-real-video", action="store_true",
        help="(video 类型) 跳过 Seedance 真生视频，仅出 prompt（节省成本）",
    )
    ap.add_argument(
        "--async", dest="async_video", action="store_true",
        help="(video 类型) 仅提交 Seedance 任务不轮询，立即返回 task_id",
    )
    ap.add_argument(
        "--no-confirm", action="store_true",
        help="(video 类型) 跳过 3 秒成本确认倒数",
    )
    ap.add_argument("--version", action="version", version=f"content-engine {__version__}")
    args = ap.parse_args()

    # ─── Preflight 检查 ───
    from content_engine import preflight
    workspace_for_check = args.out.expanduser().resolve() if args.out else None
    checks = preflight.run_all(workspace=workspace_for_check)

    if args.check:
        return preflight.print_report(checks)

    # 阻断检查 + Ofox 必需检查（generate 用）
    fatal_failures = [c for c in checks if not c.ok and c.fatal]
    if fatal_failures:
        log("❌ 环境检查未通过：")
        for c in fatal_failures:
            log(f"   - {c.name}: {c.message}")
        return 2

    # generate mode 必须有 OFOX_API_KEY（preflight 标 fatal=False，这里强制）
    ofox_check = next((c for c in checks if "OFOX" in c.name), None)
    if ofox_check and not ofox_check.ok:
        log("❌ generate mode 必需 OFOX_API_KEY：")
        log(f"   {ofox_check.fix}")
        return 2

    if not args.link:
        ap.error("缺少 link 参数（除非用 --check）")
        return 2

    # ─── 收集产品图列表 ───
    product_imgs: list[Path] = []
    if args.product_imgs:
        p = args.product_imgs.expanduser().resolve()
        if p.is_file():
            product_imgs = [p]
        elif p.is_dir():
            product_imgs = sorted(
                f for f in p.iterdir()
                if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
            )
        else:
            log(f"⚠️ --product-imgs 路径不存在：{p}（继续，但视觉风格可能飘）")

    # ─── 调主流程 ───
    input_ = GenerateInput(
        link=args.link,
        type=args.type,
        count=args.count,
        product_imgs=product_imgs,
        product_usp=args.product_usp,
        out_dir=args.out.expanduser().resolve() if args.out else None,
        fresh=args.fresh,
        real_video=not args.no_real_video,
        async_video=args.async_video,
        cost_confirm_seconds=0 if args.no_confirm else 3,
    )

    try:
        output = generate(input_, log=log)
    except OfoxError as e:
        log(f"❌ Ofox API 错误：{e}")
        return 2
    except (ValueError, RuntimeError) as e:
        log(f"❌ 生成失败：{e}")
        return 1

    # ─── 输出 stdout 结构化 summary ───
    summary = {
        "note_id": output.note_id,
        "card_path": str(output.card_path.absolute()),
        "gen_dir": str(output.gen_dir.absolute()),
        "type": output.type,
        "count": output.count,
        "files": output.files,
        "duration_seconds": output.duration_seconds,
        "llm_calls": output.llm_calls,
        "next": "Read gen_dir/script.md and other files; review and adjust before publishing.",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
