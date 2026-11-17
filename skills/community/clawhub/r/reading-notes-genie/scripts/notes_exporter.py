#!/usr/bin/env python3
"""
notes_exporter.py — 多格式筆記匯出器
支援：Markdown / Anki (.apkg) / PDF / JSON
"""

import sys
import json
import argparse
import base64
import zipfile
import io
from pathlib import Path
from datetime import datetime

# ── 依賴偵測 ─────────────────────────────────────────────────────────────────
def _has(mod: str) -> bool:
    try:
        __import__(mod); return True
    except ImportError:
        return False

HAS_GENANKi   = _has("genanki")
HAS_REPORTLAB = _has("reportlab")
HAS_MDX        = _has("markdown")


# ══════════════════════════════════════════════════════════════════════════════
# MARKDOWN 匯出
# ══════════════════════════════════════════════════════════════════════════════

def export_markdown(summary: dict) -> str:
    """將摘要轉為精美 Markdown"""
    meta   = summary.get("metadata", {})
    title  = meta.get("title", "未知書名")
    author = meta.get("author", "未知作者")
    date   = datetime.now().strftime("%Y-%m-%d")
    tags   = meta.get("subjects", [])

    lines = [
        f"# 📖 {title}",
        "",
        f"> **作者：** {author}  \n> **閱讀日期：** {date}",
        "",
    ]

    # 標籤
    if tags:
        lines.append("**標籤：** " + " ".join(f"`{t}`" for t in tags[:10]))
        lines.append("")

    # 全書總結
    overall = summary.get("overall_summary", "").strip()
    if overall:
        lines.append("## 📝 全書總結")
        lines.append("")
        lines.append(overall)
        lines.append("")

    # 精華語錄
    highlights = summary.get("highlights", [])
    if highlights:
        lines.append("## 💡 精華語錄")
        lines.append("")
        for q in highlights:
            lines.append(f"> 「{q}」")
            lines.append("")
        lines.append("")

    # 章節摘要
    chapters = summary.get("chapters", [])
    if chapters:
        lines.append(f"## 📑 章節摘要（共 {len(chapters)} 章）")
        lines.append("")
        for i, ch in enumerate(chapters, 1):
            ch_title = ch.get("title", f"第 {i} 章")
            ch_sum   = ch.get("summary", "")
            points   = ch.get("key_points", [])
            quotes   = ch.get("quotes", [])

            lines.append(f"### 第 {i} 章：{ch_title}")
            lines.append("")
            if ch_sum:
                lines.append(ch_sum)
                lines.append("")
            if points:
                lines.append("**核心要點：**")
                for p in points:
                    lines.append(f"- {p}")
                lines.append("")
            if quotes:
                lines.append("**金句：**")
                for q in quotes[:3]:
                    lines.append(f"> 「{q}」")
                lines.append("")

    # 讀書心得
    takeaways = summary.get("takeaways", "").strip()
    if takeaways:
        lines.append("## 🎯 行動建議與讀後感")
        lines.append("")
        lines.append(takeaways)
        lines.append("")

    # 知識卡片
    cards = summary.get("knowledge_cards", [])
    if cards:
        lines.append(f"## 🃏 知識卡片（共 {len(cards)} 張）")
        lines.append("")
        for card in cards:
            term  = card.get("term", "")
            defn  = card.get("definition", "")
            exam  = card.get("example", "")
            tags_c = card.get("tags", [])
            lines.append(f"### 💳 {term}")
            lines.append(f"**定義：** {defn}")
            if exam:
                lines.append(f"**實例：** {exam}")
            if tags_c:
                lines.append(f"**標籤：** " + " ".join(f"`{t}`" for t in tags_c))
            lines.append("---")
            lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append(f"* 由 📚 Reading Notes Genie 生成 · {date} *")

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# JSON 匯出（保持原結構）
# ══════════════════════════════════════════════════════════════════════════════

def export_json(summary: dict) -> str:
    return json.dumps(summary, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════════════════════
# ANKI 格式匯出
# ══════════════════════════════════════════════════════════════════════════════

def export_anki(summary: dict) -> str:
    """生成 Anki 格式文字檔（可透過 AnkiImport 匯入）"""

    def cloze_text(text: str, term: str = "") -> str:
        """生成 Cloze 填空文字"""
        if term and term in text:
            return text.replace(term, f"{{{{c1::{term}}}}}", 1)
        # 找合適的 cloze 位置
        import re
        words = re.findall(r'[^，。；？！、\s「」『』（】〔【]{3,8}', text)
        for w in words:
            if len(w) > 2:
                return text.replace(w, f"{{{{c1::{w}}}}}", 1)
        return text

    lines = [
        "#separator:tab",
        "#html:true",
        "#tags column:3",
        "#notetype column:1",
        "",
    ]

    book_name = summary.get("metadata", {}).get("title", "書籍")
    all_cards: list[tuple[str, str, str]] = []

    # 知識卡 → 問答卡
    for card in summary.get("knowledge_cards", []):
        front = f"什麼是「{card.get('term', '')}」？"
        back  = card.get("definition', '") or card.get('example', '')
        tags  = " ".join(card.get("tags", ["閱讀"]))
        all_cards.append((front, back, tags))

    # 章節要點 → Cloze
    for ch in summary.get("chapters", []):
        for point in ch.get("key_points", []):
            if len(point) > 10:
                cloze = cloze_text(point)
                tags  = f"閱讀 {ch.get('title', '')[:20]}"
                all_cards.append((cloze, "", tags))

    # 精華語錄 → Cloze
    for q in summary.get("highlights", []):
        cloze = cloze_text(q)
        all_cards.append((cloze, "", "語錄"))

    # 寫入
    for front, back, tags in all_cards:
        # Tab 分隔：Front | Back | Tags
        line = (front + "\t" + back + "\t" + tags).replace("\n", "<br>")
        lines.append(line)

    return "\n".join(lines)


def export_apkg(summary: dict, output_path: str) -> str:
    """生成真正的 .apkg 檔（使用 genanki）"""
    if not HAS_GENANKi:
        # 改為匯出 tab 分隔文字檔
        txt = export_anki(summary)
        txt_path = output_path.replace(".apkg", ".txt")
        Path(txt_path).write_text(txt, encoding="utf-8")
        return (f"⚠️  genanki 未安裝，已改為匯出 tab 分隔文字檔：{txt_path}\n"
                f"   請在 Anki 中使用「檔案 → 匯入 → {txt_path}」匯入。")

    import genanki

    book_name = summary.get("metadata", {}).get("title", "Reading Notes")
    deck_id   = hash(book_name) & ((1 << 63) - 1)
    deck = genanki.Deck(deck_id, book_name)

    # Cloze Model
    cloze_model = genanki.ClozeModel(
        name="Cloze (Reading Notes)",
        fields=[{"name": "Text"}, {"name": "Extra"}],
        templates=[{
            "name": "Cloze",
            "qfmt": "{{{{cloze:Text}}}}",
            "afmt": "{{cloze:Text}}<br><hr><i>{{Extra}}</i>",
        }],
        css=".cloze { font-weight: bold; color: #4a90d9; }",
    )

    # 依序加入所有 Cloze 卡
    for ch in summary.get("chapters", []):
        for point in ch.get("key_points", []):
            if len(point) > 10:
                note = genanki.ClozeNote(
                    model=cloze_model,
                    fields=[point, ch.get("title", "")],
                    tags=["閱讀", "要點"],
                )
                deck.add_note(note)

    for q in summary.get("highlights", []):
        if len(q) > 10:
            note = genanki.ClozeNote(
                model=cloze_model,
                fields=[q, "精華語錄"],
                tags=["語錄"],
            )
            deck.add_note(note)

    # 寫入 .apkg
    buf = io.BytesIO()
    genanki.Package(deck).write_to_file(buf)
    Path(output_path).write_bytes(buf.getvalue())
    return f"✅ 已生成 Anki 卡包：{output_path}"


# ══════════════════════════════════════════════════════════════════════════════
# PDF 匯出
# ══════════════════════════════════════════════════════════════════════════════

def export_pdf(summary: dict, output_path: str) -> str:
    """使用 reportlab 生成精美 PDF"""

    if not HAS_REPORTLAB:
        return ("⚠️  reportlab 未安裝，無法生成 PDF。\n"
                "   請執行：pip3 install reportlab\n"
                "   或使用 --format markdown 匯出 Markdown 檔案。")

    # 延遲 import（setup_chinese_pdf 會檢測系統）
    sys.path.insert(0, str(Path(__file__).parent))

    # ── 中文字體設定 ───────────────────────────────────────────────────────
    import platform, os
    system = platform.system()
    cn_font = None

    if system == "Darwin":
        candidates = [
            ("/System/Library/Fonts/STHeiti Light.ttc",  "STHeiti",  0),
            ("/System/Library/Fonts/STHeiti Medium.ttc", "STHeitiM", 0),
            ("/System/Library/Fonts/Supplemental/Songti.ttc", "Songti", 0),
        ]
    elif system == "Windows":
        windir = os.environ.get("WINDIR", "C:\\Windows")
        candidates = [
            (os.path.join(windir, "Fonts", "msyh.ttc"),   "MicrosoftYaHei", 0),
            (os.path.join(windir, "Fonts", "simhei.ttf"),  "SimHei",         0),
            (os.path.join(windir, "Fonts", "simsun.ttc"),  "SimSun",         0),
        ]
    else:
        candidates = [
            ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", "NotoSansCJK", 0),
            ("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",           "WQYZenHei",   0),
        ]

    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    for font_path, font_name, idx in candidates:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path, subfontIndex=idx))
                cn_font = font_name
                break
            except Exception:
                continue

    if not cn_font:
        return ("⚠️  無法找到中文字體。\n"
                "   macOS: 確認 /System/Library/Fonts/ 下有 STHeiti 字體\n"
                "   建議改用 --format markdown 匯出")

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak,
        Table, TableStyle,
    )
    from reportlab.lib import colors
    from reportlab.lib.units import cm

    # ── 樣式設定 ────────────────────────────────────────────────────────────
    def make_styles():
        base = getSampleStyleSheet()
        for s in base.byName.values():
            s.fontName = cn_font
        return base

    styles = make_styles()

    title_s  = ParagraphStyle("Title2",  fontName=cn_font, fontSize=22,
                               leading=28, alignment=TA_CENTER, spaceAfter=6)
    meta_s   = ParagraphStyle("Meta",   fontName=cn_font, fontSize=11,
                               leading=16, alignment=TA_CENTER, textColor=colors.grey)
    h1_s     = ParagraphStyle("H1",     fontName=cn_font, fontSize=15,
                               leading=20, spaceBefore=16, spaceAfter=6,
                               textColor=colors.HexColor("#2E4057"))
    h2_s     = ParagraphStyle("H2",     fontName=cn_font, fontSize=13,
                               leading=18, spaceBefore=12, spaceAfter=4,
                               textColor=colors.HexColor("#4a90d9"))
    body_s   = ParagraphStyle("Body",   fontName=cn_font, fontSize=10,
                               leading=16, spaceAfter=4)
    quote_s  = ParagraphStyle("Quote",  fontName=cn_font, fontSize=10,
                               leading=16, leftIndent=20, rightIndent=20,
                               textColor=colors.HexColor("#555555"),
                               borderPadding=(0, 10, 0, 10))
    tag_s    = ParagraphStyle("Tag",    fontName=cn_font, fontSize=9,
                               leading=14, textColor=colors.grey)
    footer_s = ParagraphStyle("Footer", fontName=cn_font, fontSize=9,
                               leading=12, alignment=TA_CENTER, textColor=colors.lightgrey)

    def H1(text: str) -> Paragraph:
        return Paragraph(text, h1_s)

    def H2(text: str) -> Paragraph:
        return Paragraph(text, h2_s)

    def P(text: str) -> Paragraph:
        return Paragraph(text, body_s)

    def Q(text: str) -> Paragraph:
        return Paragraph("「 " + text + " 」", quote_s)

    def HR():
        return HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey,
                          spaceAfter=6, spaceBefore=6)

    # ── 建構內容 ────────────────────────────────────────────────────────────
    meta = summary.get("metadata", {})
    book_title = meta.get("title", "未知書名")
    book_author = meta.get("author", "未知作者")
    date = datetime.now().strftime("%Y-%m-%d")

    story: list = []

    # 封面
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("📖 閱讀筆記", title_s))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(book_title, ParagraphStyle("BT", fontName=cn_font,
                       fontSize=18, leading=24, alignment=TA_CENTER)))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(f"作者：{book_author}  |  {date}", meta_s))
    story.append(HR())
    story.append(Spacer(1, 0.5 * cm))

    # 全書總結
    overall = summary.get("overall_summary", "").strip()
    if overall:
        story.append(H1("📝 全書總結"))
        story.append(P(overall))
        story.append(Spacer(1, 0.4 * cm))

    # 精華語錄
    highlights = summary.get("highlights", [])
    if highlights:
        story.append(H1("💡 精華語錄"))
        for q in highlights:
            story.append(Q(q))
            story.append(Spacer(1, 0.2 * cm))
        story.append(Spacer(1, 0.4 * cm))

    # 章節摘要
    chapters = summary.get("chapters", [])
    if chapters:
        story.append(H1(f"📑 章節摘要（共 {len(chapters)} 章）"))
        for i, ch in enumerate(chapters, 1):
            ch_title = ch.get("title", f"第 {i} 章")
            story.append(H2(f"第 {i} 章：{ch_title}"))
            for p in ch.get("key_points", [])[:5]:
                story.append(P(f"• {p}"))
            quotes = ch.get("quotes", [])
            if quotes:
                story.append(Q(quotes[0]))
            if i % 3 == 0:
                story.append(PageBreak())
        story.append(Spacer(1, 0.4 * cm))

    # 知識卡
    cards = summary.get("knowledge_cards", [])
    if cards:
        story.append(H1(f"🃏 知識卡片（共 {len(cards)} 張）"))
        for card in cards[:10]:
            term = card.get("term", "")
            defn = card.get("definition", "")
            exam = card.get("example", "")
            story.append(H2(f"💳 {term}"))
            story.append(P(f"定義：{defn}"))
            if exam:
                story.append(P(f"實例：{exam}"))
            story.append(Spacer(1, 0.3 * cm))

    # Footer
    story.append(HR())
    story.append(Paragraph(
        f"📚 Reading Notes Genie 生成 · {date}",
        footer_s
    ))

    # ── 生成 PDF ────────────────────────────────────────────────────────────
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
    )
    doc.build(story)
    return f"✅ PDF 已生成：{output_path}"


# ══════════════════════════════════════════════════════════════════════════════
# 主程式
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="閱讀筆記多格式匯出器")
    parser.add_argument("--input", "-i", required=True,
                        help="書籍摘要 JSON 檔案")
    parser.add_argument("--format", "-f",
                        choices=["markdown", "json", "anki", "apkg", "pdf", "all"],
                        default="all",
                        help="輸出格式（默认 all）")
    parser.add_argument("--output", "-o", default="",
                        help="輸出檔案/目錄路徑")
    args = parser.parse_args()

    # 讀入摘要
    try:
        summary = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ 無法讀取摘要檔案：{e}")
        return

    meta  = summary.get("metadata", {})
    title = meta.get("title", Path(args.input).stem)
    safe  = title.replace("/", "_").replace("\\", "_").replace(":", "")[:40]
    out_dir = Path(args.output) if args.output else Path("./notes_output")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"📦 正在匯出「{title}」...")
    results: list[str] = []

    def write(name: str, content: str, path: Path):
        path.write_text(content, encoding="utf-8")
        results.append(f"   ✅ {name}: {path}")

    formats = [args.format] if args.format != "all" else ["markdown", "json", "anki", "pdf"]

    for fmt in formats:
        if fmt == "markdown":
            content = export_markdown(summary)
            write("Markdown", content, out_dir / f"{safe}.md")

        elif fmt == "json":
            content = export_json(summary)
            write("JSON", content, out_dir / f"{safe}.json")

        elif fmt == "anki":
            content = export_anki(summary)
            write("Anki (文字)", content, out_dir / f"{safe}_anki.txt")

        elif fmt == "apkg":
            msg = export_apkg(summary, str(out_dir / f"{safe}.apkg"))
            results.append(f"   {msg}")

        elif fmt == "pdf":
            msg = export_pdf(summary, str(out_dir / f"{safe}.pdf"))
            results.append(f"   {msg}")

    print(f"\n{'='*50}")
    print(f"📚 {title}")
    print("="*50)
    for r in results:
        print(r)
    print(f"\n📂 輸出目錄：{out_dir}")


if __name__ == "__main__":
    main()
