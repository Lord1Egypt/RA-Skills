#!/usr/bin/env python3
"""
knowledge_card.py — 知識點卡片生成器
從書籍摘要萃取可複習的知識點，支援：
- 獨立知識卡（Term + Definition + Example）
- Anki Cloze 填空卡
- Anki 問答卡（Q&A）
- Markdown 格式導出
"""

import sys
import json
import argparse
import random
from pathlib import Path
from typing import Optional

# ── 卡片模板 ──────────────────────────────────────────────────────────────────

TEMPLATES = {
    # ── Cloze 填空 ────────────────────────────────────────────────────────
    "cloze": """\
<!-- {tags} -->
{c1::{term}}
{cloze}
<!-- /{id} -->
""",

    # ── 問答卡 ────────────────────────────────────────────────────────────
    "qa": """\
Q：{question}

A：{answer}

Tags: {tags}
ID: {id}
""",

    # ── Markdown 卡片 ────────────────────────────────────────────────────
    "markdown": """\
## {term}

**定義：** {definition}

**實例：** {example}

**標籤：** {tags}

---
""",
}


# ── 知識卡生成器 ──────────────────────────────────────────────────────────────

class KnowledgeCardGenerator:
    def __init__(self):
        self.cards: list[dict] = []

    def load_from_summary(self, summary: dict):
        """從書籍摘要 JSON 載入知識卡"""
        self.cards = []

        # 優先用 summary 中的 knowledge_cards
        for card in summary.get("knowledge_cards", []):
            self.cards.append(self._normalize(card))

        # 從章節要點萃知識卡
        for ch in summary.get("chapters", []):
            for point in ch.get("key_points", []):
                if len(point) > 15:
                    self.cards.append(self._from_point(point))

        # 從精華語錄生成語錄卡
        for quote in summary.get("highlights", []):
            self.cards.append(self._from_quote(quote))

    def _normalize(self, card: dict) -> dict:
        return {
            "id":       self._gen_id(),
            "term":     card.get("term",     card.get("definition", ""))[:80],
            "definition": card.get("definition", card.get("term", "")),
            "example":  card.get("example",  ""),
            "tags":     card.get("tags",     ["閱讀"]),
            "source":   "book",
        }

    def _from_point(self, point: str) -> dict:
        """將章節要點轉為知識卡"""
        # 嘗試找「：」「是」「稱為」等分隔符
        for sep in ("：", "：", "稱為", "是", "＝", " = "):
            if sep in point:
                parts = point.split(sep, 1)
                term  = parts[0].strip()
                defn  = parts[1].strip()
                if len(term) > 3 and len(defn) > 5:
                    return {
                        "id": self._gen_id(), "term": term, "definition": defn,
                        "example": "", "tags": ["閱讀", "要點"], "source": "chapter_point",
                    }

        return {
            "id": self._gen_id(),
            "term":     point[:50],
            "definition": point,
            "example":  "",
            "tags":     ["閱讀", "要點"],
            "source":   "chapter_point",
        }

    def _from_quote(self, quote: str) -> dict:
        """將語錄轉為 Cloze 卡片"""
        # 找第一個實體名詞（heuristic）
        words = quote.split()
        highlight_word = ""
        for w in words[2:]:
            if len(w) >= 2 and w[0].isupper():
                highlight_word = w
                break

        return {
            "id":         self._gen_id(),
            "type":       "cloze",
            "cloze_text": quote,
            "cloze_word": highlight_word or words[min(3, len(words)-1)],
            "quote":      quote,
            "tags":       ["語錄", "金句"],
            "source":     "quote",
        }

    def _gen_id(self) -> str:
        return f"kc_{random.randint(10000, 99999)}"

    # ── 格式化輸出 ──────────────────────────────────────────────────────────

    def to_cloze_cards(self) -> str:
        """生成 Anki Cloze 格式文字"""
        lines = []
        lines.append("# Anki Cloze 格式卡片")
        lines.append("# 由 Reading Notes Genie 生成")
        lines.append("")

        for card in self.cards:
            if card.get("type") == "cloze" or "cloze_text" in card:
                text = card["cloze_text"]
                cloze_word = card.get("cloze_word", "")
                # 隨機 cloze 位置
                if cloze_word and cloze_word in text:
                    cloze = text.replace(cloze_word, f"{{{{c1::{cloze_word}}}}}", 1)
                else:
                    # 找第一個名詞短語 cloze
                    import re
                    noun = re.findall(r'[^，。；？！\s]{4,10}', text)
                    if noun:
                        cloze = text.replace(noun[0], f"{{{{c1::{noun[0]}}}}}", 1)
                    else:
                        cloze = text

                tags_str = " ".join(f"#{t}" for t in card.get("tags", []))
                lines.append(f"<!-- {tags_str} -->")
                lines.append(cloze)
                lines.append("")
            else:
                # 從 definition cloze
                term     = card["term"]
                defn     = card["definition"]
                cloze    = f"{term}：{{{{c1::{defn[:30]}}}}}"
                tags_str = " ".join(f"#{t}" for t in card.get("tags", []))
                lines.append(f"<!-- {tags_str} -->")
                lines.append(cloze)
                lines.append("")

        return "\n".join(lines)

    def to_qa_cards(self) -> str:
        """生成 Anki 問答格式"""
        lines = []
        lines.append("# Anki Q&A 格式卡片")
        lines.append("# 由 Reading Notes Genie 生成")
        lines.append("")

        for card in self.cards:
            q = f"什麼是「{card['term']}」？"
            a = card.get("definition", "")
            if card.get("example"):
                a += f"\n\n例：{card['example']}"
            tags_str = "、".join(card.get("tags", []))
            lines.append(f"Q：{q}")
            lines.append(f"A：{a}")
            lines.append(f"標籤：{tags_str}  ID：{card['id']}")
            lines.append("")

        return "\n".join(lines)

    def to_markdown(self) -> str:
        """生成 Markdown 格式（可存入 Obsidian / Notion）"""
        lines = []
        lines.append("# 📚 閱讀知識卡")
        lines.append("")

        # Group by tag
        by_tag: dict[str, list[dict]] = {}
        for card in self.cards:
            for tag in card.get("tags", ["未分類"]):
                by_tag.setdefault(tag, []).append(card)

        for tag, tagged in by_tag.items():
            lines.append(f"## 🏷 {tag}（{len(tagged)} 張）")
            lines.append("")
            for card in tagged:
                term  = card.get("term", "")
                defn  = card.get("definition", "")
                exam  = card.get("example", "")
                # 語錄卡
                if card.get("source") == "quote":
                    lines.append(f"> 「{card.get('cloze_text', card.get('quote', ''))}」")
                    lines.append("")
                else:
                    lines.append(f"### {term}")
                    lines.append(f"**定義：** {defn}")
                    if exam:
                        lines.append(f"**實例：** {exam}")
                    lines.append("")

        return "\n".join(lines)

    def to_flashcards_json(self) -> str:
        """生成 JSON 格式（供 AnkiConnect 讀取）"""
        out: list[dict] = []
        for card in self.cards:
            out.append({
                "id":    card["id"],
                "type":  card.get("type", "basic"),
                "front": card.get("term", card.get("cloze_text", "")),
                "back":  card.get("definition", card.get("quote", "")),
                "tags":  card.get("tags", []),
                "source": card.get("source", ""),
            })
        return json.dumps(out, ensure_ascii=False, indent=2)

    def stats(self) -> str:
        """統計摘要"""
        by_type: dict[str, int] = {}
        for c in self.cards:
            t = c.get("type", c.get("source", "normal"))
            by_type[t] = by_type.get(t, 0) + 1
        total = len(self.cards)
        lines = [
            f"📇 知識卡統計（共 {total} 張）",
        ]
        for t, n in by_type.items():
            icon = "💡" if t == "normal" else "🔑" if t == "cloze" else "❓" if t == "qa" else "📝"
            lines.append(f"   {icon} {t}: {n} 張")
        return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="知識點卡片生成器")
    parser.add_argument("summary_file", help="書籍摘要 JSON 檔案")
    parser.add_argument("--format", "-f", choices=["cloze", "qa", "markdown", "json", "all"],
                        default="all", help="輸出格式")
    parser.add_argument("--output", "-o", help="輸出檔案路徑（預設印到標準輸出）")
    args = parser.parse_args()

    # 讀取摘要
    try:
        summary = json.loads(Path(args.summary_file).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ 無法讀取摘要檔案：{e}")
        return

    gen = KnowledgeCardGenerator()
    gen.load_from_summary(summary)
    print(gen.stats())

    outputs: dict[str, str] = {}
    if args.format in ("cloze", "all"):
        outputs["cloze"]   = gen.to_cloze_cards()
    if args.format in ("qa", "all"):
        outputs["qa"]      = gen.to_qa_cards()
    if args.format in ("markdown", "all"):
        outputs["markdown"] = gen.to_markdown()
    if args.format in ("json", "all"):
        outputs["json"]    = gen.to_flashcards_json()

    if args.output:
        # 根據格式分檔
        out_dir = Path(args.output)
        if out_dir.suffix:
            # 單檔：選第一個
            name = list(outputs.keys())[0]
            out_dir.write_text(outputs[name], encoding="utf-8")
            print(f"\n✅ 已寫入：{args.output}")
        else:
            out_dir.mkdir(parents=True, exist_ok=True)
            for fmt, content in outputs.items():
                fp = out_dir / f"cards.{fmt}"
                fp.write_text(content, encoding="utf-8")
                print(f"   ✅ {fmt}: {fp}")
    else:
        for fmt, content in outputs.items():
            print("\n" + "=" * 50)
            print(f"📦 格式：{fmt}")
            print("=" * 50)
            print(content[:2000])


if __name__ == "__main__":
    main()
