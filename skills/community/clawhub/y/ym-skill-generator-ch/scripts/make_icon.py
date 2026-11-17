"""技能图标：生成提示词 → 居中裁切 → 清生成标 → 512×512 / ≤500KB → 上传前自查。

    # ① 先拿 ImageGen 用的提示词（按本技能 SKILL.md 的展示名与描述拼，贴合技能身份）
    python scripts/make_icon.py --prompt [--lang en]

    # ② 生成图后处理（默认开启居中裁切与清生成标）
    python scripts/make_icon.py <图片...> [--out <目录>] [--name <技能名>]
                                [--no-center] [--no-clean] [--fmt png|jpg]
                                [--size 512] [--max-kb 500] [--dry-run]

    # ③ 上传前自查（只校验，不改动文件）
    python scripts/make_icon.py --check <图片...>

平台硬性要求：**512×512、PNG 或 JPG、单张 ≤ 500KB**。

为什么默认要裁切和清标（两个真实踩过的坑）：
  · ImageGen 出的是「1024×1024 圆角方块 + 外圈留白」，主体常偏一侧。
    整图缩放会带着不对称留白；随手按固定框硬切（如 `(0,0,900,900)`）会
    「一边内容被截、另一边留白」。—— `--center` 按圆角方块真实边界取正方形，四边等距。
  · 生成图右下角带「AI生成 / WORKBUDDY」标，落在圆角方块**外侧**的背景上。
    —— `--clean` 用周围背景平滑重建那一小块，不碰主体；检测不到就不动。

⚠️ 图标必须落在**技能目录之外**（默认 ~/.workbuddy/skill-icons/，可用 --out 或
   环境变量 SKILLHUB_ICON_DIR 覆盖）。技能目录通常同时是 GitHub 仓库，而 SkillHub
   绑定仓库发布时按「文件类型白名单」过滤，裸 .png 会被直接拒收（报「不支持的
   文件类型」）。图标本来就该走平台图标入口单独提交，不要塞进技能包。

依赖 Pillow（可选）。未安装时给出提示，不会擅自安装。
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
from _paths import platform_sub  # noqa: E402
SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
ICON_SIZE = 512
MAX_KB = 500

# 图标默认落到**技能目录之外**。原因：技能目录通常同时是 GitHub 仓库，而 SkillHub
# 绑定仓库发布时按「文件类型白名单」过滤文件，裸 .png 会被直接拒收
# （报「不支持的文件类型: icons/xxx-icon.png」）。图标本来就该走平台图标入口
# 单独提交，放在技能目录里只会把发布卡住。
DEFAULT_ICON_DIRNAME = "skill-icons"
ICON_DIR_ENV = "SKILLHUB_ICON_DIR"


def default_icon_dir() -> Path:
    """图标默认输出目录：环境变量 SKILLHUB_ICON_DIR 优先，否则平台根下的 skill-icons。"""
    env = os.environ.get(ICON_DIR_ENV, "").strip()
    if env:
        return Path(env).expanduser()
    return platform_sub(DEFAULT_ICON_DIRNAME, fallback_home=True)


def use_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def read_frontmatter(path: Path) -> dict:
    """读 SKILL.md 的 frontmatter（够用即可，不引第三方库）。

    支持 YAML 折叠块（`>-` / `|`）—— description 常这么写，只认单行标量会读成空串。
    """
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    data: dict = {}
    key = None
    for line in m.group(1).splitlines():
        if re.match(r"^[A-Za-z0-9_.-]+\s*:", line):
            k, _, v = line.partition(":")
            key, v = k.strip(), v.strip().strip("\"'")
            data[key] = "" if v in (">", "|", ">-", "|-") else v
        elif key and line.strip().startswith("- "):
            data.setdefault("__list_" + key, []).append(line.strip()[2:].strip().strip("\"'"))
        elif key and line[:1] in (" ", "\t") and line.strip():
            data[key] = (str(data.get(key, "")) + " " + line.strip()).strip()
    return data


# --------------------------------------------------------------------------- #
# ① 提示词构建
# --------------------------------------------------------------------------- #

def build_prompt(lang: str = "zh") -> str:
    fm = read_frontmatter(SKILL_ROOT / "SKILL.md")
    name = fm.get("name") or SKILL_ROOT.name
    disp = fm.get("display_name") or name
    desc = re.sub(r"\s+", " ", fm.get("description") or fm.get("description_zh") or "")
    # 只取能力描述：触发词那串是给模型判断触发用的，不是给画图看的
    purpose = re.split(r"当用户|也适用于|亦适用于|触发词|使用场景", desc)[0]
    purpose = purpose.strip().rstrip("。.；;，, ")
    if len(purpose) > 150:
        purpose = purpose[:149].rstrip() + "…"

    if lang == "en":
        return "\n".join([
            f'Design a professional app icon for a WorkBuddy skill named "{disp}" ({name}).',
            f"What it does: {purpose}",
            "Subject (YOU decide): 1–2 concrete objects that visually express the above.",
            "Style: minimal geometric, modern tech, flat with a subtle 3D touch, "
            "professional software-marketplace icon.",
            "Composition: single centered subject on a rounded-square tile, light background, "
            "still recognizable when shrunk to 64px.",
            "Do NOT include: text, letters, numbers, logos, watermarks, dense detail, "
            "collage of many objects.",
            "Output: 1024×1024 PNG.",
        ])

    return "\n".join([
        f"为 WorkBuddy 技能「{disp}」（{name}）设计一个专业应用图标。",
        f"这个技能做什么：{purpose}",
        "视觉主体（**由你决定**）：用 1~2 个具象物件表达上面这件事，",
        "                不要出现任何文字、字母、数字。",
        "风格：简洁几何、现代科技感、扁平微立体，专业软件市场图标的气质。",
        "构图：单一主体居中，铺在圆角方形底上；浅色背景；缩小到 64px 仍能认出。",
        "禁止：文字 / 字母 / 数字 / logo / 水印、密集碎细节、多物件拼贴。",
        "输出：1024×1024 PNG。",
    ])


# --------------------------------------------------------------------------- #
# ② 图像处理（仅用 Pillow，不引入 numpy）
# --------------------------------------------------------------------------- #

def _content_mask(img, threshold: int = 8):
    """与最外圈背景色差异明显的区域（= 圆角方块本身）。

    PIL 没有现成的「批量算色差」，用 ImageChops 组合：
    sat = max(RGB) - min(RGB)，dark = 255 - min(RGB)，两者取大再阈值化。
    """
    from PIL import ImageChops, ImageOps

    rgb = img.convert("RGB")
    r, g, b = rgb.split()
    mx = ImageChops.lighter(ImageChops.lighter(r, g), b)
    mn = ImageChops.darker(ImageChops.darker(r, g), b)
    sat = ImageChops.difference(mx, mn)
    dark = ImageOps.invert(mn)
    return ImageChops.lighter(sat, dark).point(lambda v: 255 if v > threshold else 0)


def detect_watermark(img, box=None) -> bool:
    """右下角是否真的有 AI 生成标：与「局部平滑背景」差异明显即算有。"""
    from PIL import Image, ImageChops

    w, h = img.size
    if box is None:
        box = (int(w * 0.84), int(h * 0.89), w, h)
    region = img.convert("RGB").crop(box)
    if region.width < 8 or region.height < 8:
        return False
    smooth = region.resize((6, 6), Image.BOX).resize(region.size, Image.BICUBIC)
    diff = ImageChops.difference(region, smooth).convert("L")
    return diff.getextrema()[1] > 18


def clean_mark(img, box=None, feather_ratio: float = 0.22):
    """用背景平滑重建覆盖右下角小矩形，靠主体一侧羽化，避免接缝。

    该矩形必须整块落在圆角方块**之外**的背景里（默认右下角 16%×11%），
    这样重建不会侵蚀图标主体。
    """
    from PIL import Image, ImageChops

    w, h = img.size
    if box is None:
        box = (int(w * 0.84), int(h * 0.89), w, h)
    x0, y0, x1, y1 = box
    region = img.convert("RGB").crop(box)
    rw, rh = region.size

    smooth = region.resize((6, 6), Image.BOX).resize((rw, rh), Image.BICUBIC)

    feather = max(4, int(min(rw, rh) * feather_ratio))
    lut = [min(255, int(255 * i / feather)) for i in range(256)]
    ramp_down = Image.linear_gradient("L").resize((rw, rh)).point(lut)
    ramp_right = ramp_down.rotate(-90, expand=True).resize((rw, rh)).point(lut)
    mask = ImageChops.darker(ramp_down, ramp_right)

    out = img.convert("RGB").copy()
    out.paste(smooth, (x0, y0), mask)
    return out


def center_crop(img):
    """按圆角方块的真实边界取正方形、四边等距地裁切。"""
    w, h = img.size
    bbox = _content_mask(img).getbbox()
    if not bbox:
        return img, None
    x0, y0, x1, y1 = bbox
    side = min(max(x1 - x0, y1 - y0), w, h)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    left = max(0, min(cx - side // 2, w - side))
    top = max(0, min(cy - side // 2, h - side))
    return img.crop((left, top, left + side, top + side)), (left, top, side)


def _save(img, path: Path, fmt: str, quality=None) -> float:
    from PIL import Image

    if fmt == "jpg":
        img.convert("RGB").save(path, format="JPEG", quality=quality, optimize=True,
                                progressive=True)
    elif fmt == "png8":
        img.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=256).save(
            path, format="PNG", optimize=True, compress_level=9)
    else:
        img.save(path, format="PNG", optimize=True, compress_level=9)
    return path.stat().st_size / 1024


def fit_size_limit(img, base: Path, max_kb: int, fmt: str):
    """按「PNG → JPEG 降质 → 调色板 PNG」的顺序压到 max_kb 以内。

    返回 (最终路径, 格式标签, KB)；全都不达标时返回最小的那个，由调用方提示。
    """
    order = [("png", 0), ("jpg", 92), ("jpg", 85), ("jpg", 76), ("png8", 0)]
    if fmt == "jpg":
        order = [("jpg", 92), ("jpg", 85), ("jpg", 76), ("png", 0), ("png8", 0)]
    made: list[Path] = []
    last = None
    for name, quality in order:
        path = base.with_suffix(".jpg" if name == "jpg" else ".png")
        kb = _save(img, path, name, quality or None)
        made.append(path)
        last = (path, name, kb)
        if kb <= max_kb:
            for other in set(made):
                if other != path:
                    other.unlink(missing_ok=True)
            return path, name, kb
    for other in set(made):
        if other != last[0] and other.exists():
            other.unlink(missing_ok=True)
    return last


# --------------------------------------------------------------------------- #
# ③ 合规检查
# --------------------------------------------------------------------------- #

def check_image(path: Path, size: int, max_kb: int) -> tuple[bool, str]:
    from PIL import Image

    try:
        with Image.open(path) as img:
            fmt, dims = (img.format or "?"), img.size
    except Exception as exc:                       # 不是图片 / 读不了
        return False, f"无法读取（{exc}）"
    kb = path.stat().st_size / 1024
    problems = []
    if dims != (size, size):
        problems.append(f"尺寸是 {dims[0]}×{dims[1]}，要求 {size}×{size}")
    if fmt not in ("PNG", "JPEG"):
        problems.append(f"格式是 {fmt}，只收 PNG / JPG")
    if kb > max_kb:
        problems.append(f"{kb:.0f}KB 超 {max_kb}KB")
    detail = f"{dims[0]}×{dims[1]}  {fmt}  {kb:.1f}KB"
    return (not problems), (detail + ("  合规" if not problems else "  ← " + "；".join(problems)))


# --------------------------------------------------------------------------- #

def main() -> int:
    use_utf8_stdout()
    import argparse

    ap = argparse.ArgumentParser(
        prog="make_icon.py",
        description="技能图标：提示词构建 / 居中裁切 + 清生成标 + 512×512 + ≤500KB / 上传前自查")
    ap.add_argument("images", nargs="*", help="待处理的生成图（默认开启裁切与清标）")
    ap.add_argument("--prompt", action="store_true", help="只打印给 ImageGen 用的提示词")
    ap.add_argument("--lang", choices=("zh", "en"), default="zh", help="提示词语言（默认 zh）")
    ap.add_argument("--check", action="store_true", help="只校验合规性，不改动文件")
    ap.add_argument("--out", default=None,
                    help=f"输出目录（默认 {default_icon_dir()}，可用环境变量 {ICON_DIR_ENV} 覆盖）")
    ap.add_argument("--name", default=None, help="输出文件名前缀（默认取 SKILL.md 的 name）")
    ap.add_argument("--fmt", choices=("png", "jpg"), default="png", help="优先输出的格式")
    ap.add_argument("--size", type=int, default=ICON_SIZE, help=f"目标边长（默认 {ICON_SIZE}）")
    ap.add_argument("--max-kb", type=int, default=MAX_KB, help=f"体积上限 KB（默认 {MAX_KB}）")
    ap.add_argument("--no-center", action="store_true", help="不做居中裁切")
    ap.add_argument("--no-clean", action="store_true", help="不清右下角生成标")
    ap.add_argument("--dry-run", action="store_true", help="只说明会怎么处理，不落盘")
    if len(sys.argv) == 1:
        print(__doc__.strip())
        return 0
    args = ap.parse_args()

    size, max_kb, fmt = args.size, args.max_kb, args.fmt
    out_dir = Path(args.out).expanduser() if args.out else default_icon_dir()
    icon_name = args.name or (read_frontmatter(SKILL_ROOT / "SKILL.md").get("name")
                              or SKILL_ROOT.name)

    # ---- ① 提示词 ----
    if args.prompt:
        print("把下面这段交给 ImageGen（size 用 1024x1024，生成后回到本脚本后处理）：\n")
        print(build_prompt(args.lang))
        print("\n拿到图之后：")
        print(f"  python scripts/make_icon.py <生成图>            # 默认输出到 {out_dir}")
        return 0

    images = [Path(t).expanduser() for t in args.images]
    for p in [p for p in images if not p.is_file()]:
        print(f"[!] 跳过（不存在）：{p}")
    images = [p for p in images if p.is_file()]

    # ---- ③ 只校验 ----
    if args.check:
        if not images:
            print("[!] 没有可校验的图片。用法：make_icon.py --check <图片...>")
            return 1
        bad = 0
        print(f"图标合规检查（要求 {size}×{size}、PNG/JPG、≤{max_kb}KB）\n")
        for p in images:
            ok, detail = check_image(p, size, max_kb)
            print(f"  {'[OK]' if ok else '[X] '} {p.name}  {detail}")
            bad += 0 if ok else 1
        print(f"\n{len(images) - bad}/{len(images)} 张合规。")
        return 1 if bad else 0

    if not images:
        print("[!] 没有可处理的图片。")
        print("    先跑 `python scripts/make_icon.py --prompt` 拿提示词，再传生成图进来。")
        return 1

    try:
        from PIL import Image
    except ImportError:
        print("[X] 未安装 Pillow，无法处理图标。")
        print("    安装：python scripts/setup.py --install-pillow")
        print("    或手动：python -m pip install Pillow")
        return 1

    do_center = not args.no_center
    do_clean = not args.no_clean
    dry_run = args.dry_run

    print(f"处理 {len(images)} 张 → {size}×{size}、≤{max_kb}KB"
          f"{'，居中裁切' if do_center else ''}{'，清生成标' if do_clean else ''}")
    print(f"输出目录：{out_dir}（在技能目录之外，不会被发布校验扫到）\n")

    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for path in images:
        before_kb = path.stat().st_size / 1024
        with Image.open(path) as img:
            dims = img.size
            if dry_run:
                print(f"  · {path.name}  {dims[0]}×{dims[1]} {before_kb:.0f}KB  → 会重新裁切/压缩")
                continue

            work = img.convert("RGB")
            notes = []
            if do_clean and detect_watermark(work):
                work = clean_mark(work)
                notes.append("已清生成标")
            if do_center:
                cropped, info = center_crop(work)
                if info:
                    work = cropped
                    notes.append(f"居中裁切 {info[2]}px")
            if work.size != (size, size):
                work = work.resize((size, size), Image.LANCZOS)

            base = out_dir / f"{icon_name}-icon"
            target, used_fmt, kb = fit_size_limit(work, base, max_kb, fmt)

        ok, _ = check_image(target, size, max_kb)
        results.append((target, ok))
        note = f"  [{'; '.join(notes)}]" if notes else ""
        warn = "" if ok else "  ← 仍不达标，需手工处理"
        print(f"  · {path.name}  {dims[0]}×{dims[1]} {before_kb:.0f}KB → "
              f"{target.name}  {size}×{size} {used_fmt.upper()} {kb:.1f}KB{warn}{note}")

    if dry_run:
        print("\n[dry-run] 未落盘。")
        return 0

    print()
    for target, ok in results:
        print(f"  {'[OK]' if ok else '[X] '} {target}")
    print(f"\n提醒：图标落在技能目录之外（{out_dir}），不会污染技能仓库。")
    print(f"     想固定到自己的目录：设环境变量 {ICON_DIR_ENV}，或每次传 --out。")
    print("     上传技能时，在平台「图标」处单独提交上面这个文件，不要塞进技能包。")
    return 0 if all(ok for _, ok in results) else 1


if __name__ == "__main__":
    code = main()
    if code:
        print("    退出码 1：图标处理未完成 —— 按上面的提示处理后再跑一次。")
    raise SystemExit(code)
