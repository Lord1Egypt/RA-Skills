"""gugu-gaga 产物校验脚本
Usage:
  python validate.py <stem> --step page-plan [--dir <dir>]     # 校验页数计划
  python validate.py <stem> --step layout-plan [--dir <dir>]   # 校验布局分配
  python validate.py <stem> --step 4 [--dir <dir>]             # 校验 5 个独立分析文件
  python validate.py <stem> --step 5 [--dir <dir>]             # 校验 HTML + class 白名单
"""
import sys, re
from pathlib import Path


def check_analysis_files(stem: str, directory: Path) -> dict:
    """检查 5 个独立分析文件（{stem}_4.N_*.md）是否存在且内容有效"""
    files = [
        ("4.1 元素采集",  f"{stem}_4.1_元素采集.md"),
        ("4.2 定性",      f"{stem}_4.2_定性.md"),
        ("4.3 重点内容",  f"{stem}_4.3_重点内容.md"),
        ("4.4 生命周期图", f"{stem}_4.4_生命周期图.md"),
        ("4.5 红黄绿蓝灯", f"{stem}_4.5_红黄绿蓝灯.md"),
    ]

    results = {}
    for name, fname in files:
        fp = directory / fname
        if not fp.exists():
            results[name] = "FAIL 文件不存在"
            continue
        text = fp.read_text(encoding="utf-8")
        stripped = re.sub(r"[#*\-\|\s]", "", text)
        if len(stripped) < 10:
            results[name] = "FAIL 内容为空或过短"
        else:
            results[name] = f"OK 内容 {len(text)} 字符"

    all_pass = all(v.startswith("OK") for v in results.values())
    return {"pass": all_pass, "sections": results}


def check_html(filepath: Path) -> dict:
    """检查 HTML 文件是否存在且 slide ≥ 8"""
    if not filepath.exists():
        return {"pass": False, "error": f"文件不存在: {filepath}"}

    text = filepath.read_text(encoding="utf-8")
    slides = re.findall(r'<section[^>]*class="[^"]*slide[^"]*"', text)
    count = len(slides)

    if count >= 8:
        return {"pass": True, "count": count, "status": f"OK {count} slides"}
    else:
        return {"pass": False, "count": count, "status": f"FAIL {count} slides（预期 >= 8）"}


def check_page_plan(stem: str, directory: Path) -> dict:
    """检查 {stem}_page-plan.md 存在且页数 >= 6"""
    fp = directory / f"{stem}_page-plan.md"
    if not fp.exists():
        return {"pass": False, "error": f"文件不存在: {fp.name}"}
    text = fp.read_text(encoding="utf-8")
    rows = len(re.findall(r'^\|', text, re.MULTILINE))
    # 减去表头分隔行（|---|），实际数据行
    data_rows = max(0, rows - 2)
    if data_rows < 6:
        return {"pass": False, "error": f"页数不足: {data_rows}（预期 >= 6：封面+4 份内容+结束页）"}
    return {"pass": True, "status": f"OK {data_rows} 页"}


def check_layout_plan(stem: str, directory: Path) -> dict:
    """检查 {stem}_layout-plan.md 存在且与 page-plan 行数匹配"""
    fp = directory / f"{stem}_layout-plan.md"
    if not fp.exists():
        return {"pass": False, "error": f"文件不存在: {fp.name}"}
    text = fp.read_text(encoding="utf-8")
    rows = len(re.findall(r'^\|', text, re.MULTILINE))
    data_rows = max(0, rows - 2)
    if data_rows < 6:
        return {"pass": False, "error": f"行数不足: {data_rows}"}
    # 与 page-plan 比对行数
    pp = directory / f"{stem}_page-plan.md"
    if pp.exists():
        pp_text = pp.read_text(encoding="utf-8")
        pp_rows = max(0, len(re.findall(r'^\|', pp_text, re.MULTILINE)) - 2)
        if data_rows != pp_rows:
            return {"pass": False, "error": f"行数不匹配: layout-plan {data_rows} != page-plan {pp_rows}"}
    return {"pass": True, "status": f"OK {data_rows} 行，与 page-plan 匹配"}


def check_html_classes(filepath: Path) -> dict:
    """检查 HTML 中所有 class 是否在白名单内"""
    PPTX_WHITELIST = {
        "slide", "is-active", "skip",
        "deck", "tpl-pptx-model",
        "ts-stripe", "ts-stripe-b", "ts-chrome", "ts-alert-tag", "ts-page",
        "ts-h1", "ts-h2", "ts-kicker", "ts-sub",
        "ts-alert-box", "ts-card", "ts-grid-2", "ts-grid-3", "ts-grid-4",
        "ts-codebox", "ts-checklist", "ts-check", "ts-footer",
        "strike", "red", "ts-highlight-red",
        "amber", "green", "ok",
    }
    PDF_WHITELIST = {
        "slide", "is-active", "skip",
        "deck", "tpl-pdf-model",
        "page-dot", "sticker", "hand-box", "bottom-bar", "cover-title",
        "num-circle", "tag-row", "ht", "stack", "avatar", "big-emoji",
        "lede", "h1", "h2", "h3",
        "pink", "yellow", "blue", "green",
    }

    whitelist = PPTX_WHITELIST if "pptx" in filepath.name else PDF_WHITELIST
    text = filepath.read_text(encoding="utf-8")
    classes = set()
    for m in re.finditer(r'class="([^"]*)"', text):
        for c in m.group(1).split():
            classes.add(c.strip())
    # 也检查 class='...'（单引号）
    for m in re.finditer(r"class='([^']*)'", text):
        for c in m.group(1).split():
            classes.add(c.strip())

    unknown = classes - whitelist
    if unknown:
        return {"pass": True, "status": f"WARNING 非白名单 class: {', '.join(sorted(unknown))}"}
    return {"pass": True, "status": "OK 全部 class 在白名单内"}


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate.py <stem> --step <4|5> [--dir <dir>]")
        sys.exit(1)

    stem = sys.argv[1]
    step = None
    directory = Path.cwd()

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--step" and i + 1 < len(sys.argv):
            step = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--dir" and i + 1 < len(sys.argv):
            directory = Path(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    all_pass = True

    if step == "4":
        print(f"校验 5 个独立分析文件（{stem}_4.N_*.md）")
        result = check_analysis_files(stem, directory)
        ok_count = 0
        fail_count = 0
        if "sections" in result:
            for name, status in result["sections"].items():
                print(f"  {name}: {status}")
                if status.startswith("OK"):
                    ok_count += 1
                else:
                    fail_count += 1
        print(f"  总计: {ok_count}/5 OK" + (f", {fail_count} FAIL" if fail_count else ""))
        if not result["pass"]:
            sys.exit(1)
        else:
            print("  PASS")

    elif step == "page-plan":
        print(f"校验: {stem}_page-plan.md")
        result = check_page_plan(stem, directory)
        print(f"  {result.get('status', result.get('error', '?'))}")
        if not result["pass"]:
            sys.exit(1)

    elif step == "layout-plan":
        print(f"校验: {stem}_layout-plan.md")
        result = check_layout_plan(stem, directory)
        print(f"  {result.get('status', result.get('error', '?'))}")
        if not result["pass"]:
            sys.exit(1)

    elif step == "5":
        # 根据用户选择仅校验对应格式
        for model in ["pptx-model", "pdf-model"]:
            html_file = directory / f"{stem}_{model}.html"
            # 跳过不存在的文件（用户只选了其中一种格式）
            if not html_file.exists():
                continue
            print(f"校验: {html_file.name}")
            result = check_html(html_file)
            print(f"  {result.get('status', result.get('error', '?'))}")
            if not result["pass"]:
                all_pass = False
            # class 白名单检查（仅 WARNING，不阻塞）
            cls_result = check_html_classes(html_file)
            print(f"  {cls_result['status']}")

    else:
        print("--step 须为 page-plan / layout-plan / 4 / 5")
        sys.exit(1)

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
