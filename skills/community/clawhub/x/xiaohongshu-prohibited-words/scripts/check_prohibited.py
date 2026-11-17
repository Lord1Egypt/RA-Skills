#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书「免费课程/证书」笔记 离线违禁词扫描器

不依赖付费 API，纯离线。扫描标题/正文/标签文本，分级输出命中结果。

**词库与解析逻辑都来自同级模块 `wordlist.py`**（词库单一真相源在
`references/prohibited-words.md`，段落级别配置在 `references/sections.json`）。
本脚本**不再内嵌任何词条副本** —— 内嵌副本正是漂移的来源：2026-09-19 实测发现
脚本与词库文档已经不一致（文档标为 P0 的「免费（全文≥2次）」与
「答案+PDF+主页群」，脚本一个都没拦住）。

用法:
  python3 check_prohibited.py "标题文本" "正文文本" "标签文本"
  python3 check_prohibited.py --file 笔记终稿.md    # 从 markdown 提取并扫描

退出码: 0=无P0硬词(PASS)  1=发现P0硬词(需改)  2=运行错误  3=依赖缺失(fail-closed)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wordlist  # noqa: E402  同目录模块

BUCKETS = [
    ("P0", "P0 硬词（必改，否则可能限流）"),
    ("P1", "P1 极限词/营销诱导（建议改）"),
    ("P2", "P2 账号级禁区词（建议改）"),
]


def extract_section(content, section_name):
    """从 markdown 提取指定标题段落内容（到下一个同级标题为止）"""
    result, in_section = [], False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("## "):
            in_section = (stripped[3:].strip() == section_name.lstrip("# ").strip() or
                          stripped.startswith(section_name))
            if in_section:
                continue
        elif stripped.startswith("# "):
            if in_section:
                break
        if in_section:
            result.append(line)
    return "\n".join(result).strip()


def main():
    args = sys.argv[1:]
    if not args:
        print("用法: check_prohibited.py '标题' '正文' '标签'  或  --file 笔记.md")
        return 2

    title, body, tags = "", "", ""
    if args[0] == "--file":
        if len(args) < 2:
            print("用法: check_prohibited.py --file 笔记.md")
            return 2
        try:
            content = Path(args[1]).read_text(encoding="utf-8")
        except Exception as e:
            print("读取失败: {0}".format(e))
            return 2
        # 只提取「## 标题」「## 正文」「## 标签」三段，跳过「违禁词审查记录/checklist/发布建议」
        # 等元信息段，否则审查记录里"旧版用了白嫖→已删"这类对照词会被误报
        title = extract_section(content, "## 标题")
        body = extract_section(content, "## 正文")
        tags = extract_section(content, "## 标签")
        if not title and not body:
            # 没找到标准段落，退回整篇（纯文案文件场景）
            title = body = content
    else:
        title = args[0] if len(args) > 0 else ""
        body = args[1] if len(args) > 1 else ""
        tags = args[2] if len(args) > 2 else ""

    try:
        rules, notices, stats, errors = wordlist.load()
    except Exception as e:
        print("✗ 词库加载失败：{0}".format(e), file=sys.stderr)
        return 3
    if errors or not rules:
        for e in (errors or ["词库解析出 0 条可匹配规则"]):
            print("✗ {0}".format(e), file=sys.stderr)
        print("✗ fail-closed：拿不到词库就不判定「通过」", file=sys.stderr)
        return 3

    all_text = "\n".join([title, body, tags])
    hits = wordlist.collect(rules, all_text)

    by_level = {lv: [] for lv, _ in BUCKETS}
    for h in hits:
        by_level.setdefault(h["level"], []).append(h)

    print("=" * 50)
    print("违禁词离线扫描结果")
    print("=" * 50)
    print("词库：{0}（载入 {1} 条）".format(wordlist.find_wordlist(), sum(stats.values())))

    for level, label in BUCKETS:
        rows = by_level.get(level, [])
        if rows:
            total = sum(r.get("count", 1) for r in rows)
            print("\n【{0}】命中 {1} 处:".format(label, total))
            for h in rows:
                n = h.get("count", 1)
                times = "（×{0}）".format(n) if n > 1 else ""
                print("  - [{0}] 「{1}」{2} → {3}；建议：{4}".format(
                    level, h["matched"], times, h["why"], h["suggest"]))
        else:
            print("\n【{0}】未命中".format(label))

    if notices:
        print("\n【须逐条核对的平台强制标注项】")
        for n in notices:
            print("  - {0}".format(n["text"]))

    print("\n" + "=" * 50)
    p0 = by_level.get("P0", [])
    if p0:
        total = sum(r.get("count", 1) for r in p0)
        print("结论：❌ 有 {0} 处 P0 硬词，需修改后再发布".format(total))
        return 1
    print("结论：✅ 无 P0 硬词，可发布（P1/P2 若命中建议顺手改）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
