#!/usr/bin/env python3
"""
book_summarizer.py — AI 書籍摘要核心引擎
支援：OpenAI / Anthropic / 本地模型（Ollama）
輸入：書名 / PDF 路徑 / EPUB 路徑
輸出：章節摘要、精華語錄、讀書心得（JSON 結構）
"""

import sys
import json
import os
import argparse
import subprocess
import textwrap
from pathlib import Path
from typing import Optional

# ── 設定 ──────────────────────────────────────────────────────────────────────
DEFAULT_MODEL  = "gpt-4o-mini"
DEFAULT_PROVIDER = "openai"

MAX_CHUNK_CHARS = 8000   # 單次送入模型的字符上限
OVERLAP_CHARS    = 500    # 段落間重疊

# ── API 包裝 ──────────────────────────────────────────────────────────────────

class LLMClient:
    """統一介面：自動偵測可用模型"""

    def __init__(self, provider: str = "", model: str = ""):
        self.provider = provider or self._detect_provider()
        self.model    = model    or self._default_model()
        self._client  = None

    def _detect_provider(self) -> str:
        if os.environ.get("ANTHROPIC_API_KEY"):
            return "anthropic"
        if os.environ.get("OPENAI_API_KEY"):
            return "openai"
        if os.environ.get("LOCAL_MODEL_URL"):
            return "local"
        return "offline"

    def _default_model(self) -> str:
        if self.provider == "anthropic": return "claude-sonnet-4-20250514"
        if self.provider == "openai":    return DEFAULT_MODEL
        if self.provider == "local":     return os.environ.get("LOCAL_MODEL", "llama3")
        return "offline"

    def _init_client(self):
        if self.provider == "openai":
            import openai
            self._client = openai.OpenAI()
        elif self.provider == "anthropic":
            import anthropic
            self._client = anthropic.Anthropic()
        # local: 不需要 client，直接 curl

    # ── 訊息建構 ──────────────────────────────────────────────────────────────

    def _system_prompt(self) -> str:
        return textwrap.dedent("""\
            你是一個專業的閱讀教練與書籍分析師。
            你的任務是深入分析輸入的書籍內容，生成高價值的閱讀筆記。
            請用繁體中文輸出（保留必要的繁體詞彙如「習慣」「定義」「章節」等）。

            輸出格式：嚴格 JSON，無任何額外文字。
            {
              "chapters": [
                {
                  "title": "章節標題",
                  "summary": "章節核心摘要（150-300字）",
                  "key_points": ["要點1", "要點2", "要點3"],
                  "quotes": ["精華語錄1", "精華語錄2"]
                }
              ],
              "highlights": ["全書最重要3-5個語錄"],
              "takeaways": "讀書心得與行動建議（300字）",
              "knowledge_cards": [
                {
                  "term": "核心概念",
                  "definition": "定義說明",
                  "example": "實例",
                  "tags": ["標籤1", "標籤2"]
                }
              ],
              "overall_summary": "全書總結（200字）"
            }
        """)

    def _chapter_prompt(self, chapter_num: int, title: str) -> str:
        return textwrap.dedent(f"""\
            請分析以下章節內容，生成結構化筆記。

            章節 {chapter_num}：{title}

            === 書籍內容 ===
            {{content}}
            ===

            請以 JSON 格式輸出，包含：
            - summary：章節摘要（150-300字）
            - key_points：3-5個核心要點
            - quotes：2-4句精華語錄（原句引用，無誤）
        """)

    def _book_prompt(self, book_name: str, metadata: dict) -> str:
        return textwrap.dedent(f"""\
            請為以下書籍生成完整的閱讀筆記結構。
            書名：{book_name}
            作者：{metadata.get('author', metadata.get('creator', '未知'))}
            === 書籍內容 ===
            {{content}}
            ===

            請嚴格以 JSON 輸出完整結構（包含 chapters、highlights、takeaways、knowledge_cards、overall_summary）。
        """)

    # ── 呼叫模型 ──────────────────────────────────────────────────────────────

    def _call_openai(self, system: str, user: str, max_tokens: int = 4096) -> str:
        import openai
        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ],
            max_tokens=max_tokens,
            temperature=0.3,
        )
        return resp.choices[0].message.content or ""

    def _call_anthropic(self, system: str, user: str, max_tokens: int = 4096) -> str:
        import anthropic
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model=self.model,
            system=system,
            messages=[{"role": "user", "content": user}],
            max_tokens=max_tokens,
        )
        return resp.content[0].text

    def _call_local(self, system: str, user: str, max_tokens: int = 4096) -> str:
        url = os.environ.get("LOCAL_MODEL_URL", "http://localhost:11434/api/generate")
        model = os.environ.get("LOCAL_MODEL", "llama3")
        payload = {
            "model": model,
            "prompt": f"<system>\n{system}\n</system>\n\n<user>\n{user}\n</user>",
            "stream": False,
            "options": {"num_predict": max_tokens},
        }
        try:
            import urllib.request, json as _json
            data = _json.dumps(payload).encode()
            req = urllib.request.Request(url, data=data,
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                resp = _json.loads(r.read())
            return resp.get("response", "")
        except Exception as e:
            return f"[LOCAL_MODEL_ERROR: {e}]"

    def call(self, system: str, user: str, max_tokens: int = 4096) -> str:
        if self.provider == "offline":
            return self._offline_summary(user)
        try:
            if self.provider == "openai":
                return self._call_openai(system, user, max_tokens)
            elif self.provider == "anthropic":
                return self._call_anthropic(system, user, max_tokens)
            elif self.provider == "local":
                return self._call_local(system, user, max_tokens)
        except Exception as e:
            print(f"⚠️  {self.provider} 呼叫失敗：{e}", file=sys.stderr)
            return self._offline_summary(user)
        return self._offline_summary(user)

    # ── 離線 fallback ─────────────────────────────────────────────────────────

    def _offline_summary(self, content: str) -> str:
        """無 API Key 時：依賴關鍵字萃取生成簡化摘要"""
        # 找引號內的句子當語錄
        import re
        raw_quotes = re.findall(r'["""「『]([^"""「」』]{20,80})["""「」』]', content)
        quotes = list(dict.fromkeys(raw_quotes))[:8]

        # 取第一段當概述
        paras = [p.strip() for p in content.split("\n\n") if len(p.strip()) > 30]
        overview = paras[0][:300] if paras else "（無內容）"

        return json.dumps({
            "chapters": [{
                "title": "章節摘要",
                "summary": overview,
                "key_points": ["請連接網路以獲得完整 AI 分析"],
                "quotes": quotes[:4],
            }],
            "highlights": quotes[:3],
            "takeaways": "請設定 OPENAI_API_KEY 或 ANTHROPIC_API_KEY 以啟用 AI 摘要功能。",
            "knowledge_cards": [],
            "overall_summary": overview,
        }, ensure_ascii=False)


# ── 書籍摘要器 ────────────────────────────────────────────────────────────────

class BookSummarizer:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def summarize_chapters(self, chapters: list[dict]) -> list[dict]:
        """對每章呼叫 LLM 生成摘要"""
        results = []
        total   = len(chapters)

        for i, ch in enumerate(chapters, 1):
            title   = ch.get("title", f"第 {i} 章")
            content = ch.get("content", "")

            if not content.strip():
                results.append({"title": title, "summary": "", "key_points": [], "quotes": []})
                continue

            # 分 chunk 處理長內容
            chunks = self._chunk_text(content)
            chapter_notes = []

            for chunk_idx, chunk in enumerate(chunks):
                prompt = self.llm._chapter_prompt(i, title)
                user   = prompt.format(content=chunk)
                raw    = self.llm.call(self.llm._system_prompt(), user, max_tokens=2048)
                parsed = self._parse_json(raw)
                if parsed:
                    chapter_notes.append(parsed)

                # 進度
                pct = (i / total) * 100
                print(f"\r   📖 [{i}/{total}] 章節處理中... {pct:.0f}%", end="", flush=True)

            # 合併多 chunk 結果
            merged = self._merge_chapter_notes(chapter_notes, title)
            results.append(merged)

        print()  # 換行
        return results

    def _chunk_text(self, text: str) -> list[str]:
        """將長文字分段（考慮段落邊界）"""
        if len(text) <= MAX_CHUNK_CHARS:
            return [text]

        chunks = []
        paras  = text.split("\n\n")
        cur    = ""

        for para in paras:
            if len(cur) + len(para) + 2 <= MAX_CHUNK_CHARS:
                cur += "\n\n" + para
            else:
                if cur:
                    chunks.append(cur.strip())
                # 保留 overlap
                cur = para[max(0, len(para) - OVERLAP_CHARS):]

        if cur.strip():
            chunks.append(cur.strip())
        return chunks

    def _merge_chapter_notes(self, notes: list[dict], fallback_title: str) -> dict:
        """合併多段解析結果"""
        if not notes:
            return {"title": fallback_title, "summary": "", "key_points": [], "quotes": []}
        if len(notes) == 1:
            notes[0]["title"] = fallback_title
            return notes[0]

        all_points = []
        all_quotes: list[str] = []
        summaries  = []

        for n in notes:
            if n.get("summary"):
                summaries.append(n["summary"])
            all_points.extend(n.get("key_points", []))
            all_quotes.extend(n.get("quotes", []))

        # 去重
        seen_q = set()
        uniq_q = []
        for q in all_quotes:
            if q not in seen_q:
                seen_q.add(q); uniq_q.append(q)

        return {
            "title":      fallback_title,
            "summary":    " ".join(summaries[:3]),
            "key_points": list(dict.fromkeys(all_points))[:8],
            "quotes":     uniq_q[:5],
        }

    def _parse_json(self, raw: str) -> Optional[dict]:
        """從 LLM 回覆中解析 JSON"""
        import re
        # 找 ```json ... ``` 或直接 { ... }
        m = re.search(r"```json\s*(.+?)```", raw, re.DOTALL)
        if not m:
            m = re.search(r"```\s*(.+?)```", raw, re.DOTALL)
        if not m:
            m = re.search(r"(\{[\s\S]+\})", raw)
        if not m:
            return None
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            return None

    def generate_highlights(self, chapters: list[dict], book_name: str) -> dict:
        """從所有章節萃取全書精華"""
        # 收集所有語錄
        all_quotes: list[tuple[str, int]] = []
        for ch in chapters:
            for q in ch.get("quotes", []):
                all_quotes.append((q, len(q)))

        # 按長度排序（中等長度最可能是有意義的語錄）
        all_quotes.sort(key=lambda x: abs(x[1] - 60))
        highlights = [q for q, _ in all_quotes[:10]]

        all_takeaways: list[str] = []
        for ch in chapters:
            all_takeaways.extend(ch.get("key_points", []))

        return {
            "highlights": highlights[:5],
            "takeaways": "；".join(list(dict.fromkeys(all_takeaways))[:10]),
            "knowledge_cards": self._extract_knowledge_cards(chapters),
        }

    def _extract_knowledge_cards(self, chapters: list[dict]) -> list[dict]:
        """從摘要萃知識點卡片"""
        # 取前3章最有價值的要點當知識卡
        cards = []
        seen  = set()
        for ch in chapters:
            for point in ch.get("key_points", []):
                key = point[:10]
                if key not in seen:
                    seen.add(key)
                    cards.append({
                        "term":      point[:50],
                        "definition": point,
                        "example":   "",
                        "tags":      ["閱讀", "知識"],
                    })
                if len(cards) >= 8:
                    break
            if len(cards) >= 8:
                break
        return cards


# ── 整合入口 ─────────────────────────────────────────────────────────────────

def summarize_by_bookname(book_name: str, llm: LLMClient) -> dict:
    """從書名出發：搜尋網路取得書籍內容摘要"""
    try:
        # 用 openalex / openlibrary API 拿書籍基本資訊
        import urllib.request, json as _json
        # Open Library Search
        q = urllib.parse.quote(book_name) if True else book_name
        url = f"https://openlibrary.org/search.json?q={q}&fields=title,author_name,subject,first_sentence&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "reading-notes-genie/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = _json.loads(r.read())

        docs = data.get("docs", [])
        if not docs:
            return _empty_result(book_name)

        doc = docs[0]
        authors = ", ".join(doc.get("author_name", ["未知"]))
        subjects = doc.get("subject", [])[:5]

        # 用 subject/description 作為摘要素材
        content = "\n".join(subjects)
        if not content.strip():
            return _empty_result(book_name)

        s    = BookSummarizer(llm)
        note = llm.call(
            llm._system_prompt(),
            llm._book_prompt(book_name, {"author": authors}),
            max_tokens=4096,
        )
        parsed = s._parse_json(note) or {}
        parsed["metadata"] = {
            "title":   doc.get("title", book_name),
            "author":  authors,
            "source":  "Open Library",
            "subjects": subjects,
        }
        return parsed

    except Exception as e:
        return _empty_result(book_name, error=str(e))


def _empty_result(name: str, error: str = "") -> dict:
    return {
        "metadata": {"title": name, "author": "未知", "source": "N/A"},
        "chapters": [],
        "highlights": [],
        "takeaways": (
            f"無法獲取「{name}」的摘要（{error}）"
            if error
            else f"無法獲取「{name}」的摘要，請確認網路連線。"
        ),
        "knowledge_cards": [],
        "overall_summary": "",
    }


def summarize_file(file_path: str, llm: LLMClient) -> dict:
    """從 PDF / EPUB 檔案出發"""
    path = Path(file_path)

    if path.suffix.lower() == ".epub":
        sys.path.insert(0, str(Path(__file__).parent))
        from epub_parser import EPUBBook
        book = EPUBBook(str(path))
        book.parse()
        chapters = book.chapters

    elif path.suffix.lower() == ".pdf":
        sys.path.insert(0, str(Path(__file__).parent))
        from pdf_extractor import extract_pdf
        result = extract_pdf(str(path))
        # 將每頁合併為若干區塊當「章節」
        pages   = result.pages
        chapters = []
        chunk_pages = 10  # 每10頁一組
        for i in range(0, len(pages), chunk_pages):
            chunk = pages[i:i+chunk_pages]
            text  = "\n\n".join(p.get("text", "") for p in chunk)
            chapters.append({
                "title":   f"第 {i//chunk_pages + 1} 部分（頁 {i+1}–{min(i+chunk_pages, len(pages))}）",
                "content": text,
            })
        if not chapters:
            chapters = [{"title": "全書", "content": ""}]

    else:
        return _empty_result(path.stem, error="不支援的檔案格式")

    s    = BookSummarizer(llm)
    note = s.summarize_chapters(chapters)

    # 全書精華
    highlights = s.generate_highlights(note, path.stem)

    # 合併
    for ch in note:
        if "title" not in ch or not ch["title"]:
            ch["title"] = chapters[note.index(ch)].get("title", "")

    return {
        "metadata": {
            "title":    path.stem,
            "source":   f"local:{path.suffix}",
            "chapters": len(chapters),
        },
        "chapters": note,
        "highlights":     highlights["highlights"],
        "takeaways":      highlights["takeaways"],
        "knowledge_cards": highlights["knowledge_cards"],
        "overall_summary": " ".join(c.get("summary", "") for c in note[:3]),
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    import urllib.parse
    parser = argparse.ArgumentParser(description="AI 書籍摘要生成器")
    parser.add_argument("--book",  help="書名（AI 網路查詢）")
    parser.add_argument("--file",  help="PDF 或 EPUB 檔案路徑")
    parser.add_argument("--output", "-o", default="./notes",
                        help="輸出目錄（預設 ./notes）")
    parser.add_argument("--provider", choices=["openai", "anthropic", "local", "offline"],
                        default="", help="模型供應商（預設自動偵測）")
    parser.add_argument("--model",  default="", help="模型名稱")
    args = parser.parse_args()

    if not args.book and not args.file:
        parser.print_help()
        return

    llm  = LLMClient(provider=args.provider, model=args.model)
    print(f"🤖 使用：{llm.provider} / {llm.model}")

    if args.book:
        print(f"📚 正在為「{args.book}」生成摘要...")
        result = summarize_by_bookname(args.book, llm)
    else:
        print(f"📄 正在分析：{args.file}")
        result = summarize_file(args.file, llm)

    # 寫入 JSON
    out_dir  = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_name = (result.get("metadata", {}).get("title", "notes")
                 .replace("/", "_").replace("\\", "_")[:50])
    out_file = out_dir / f"{safe_name}.json"
    out_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 已寫入：{out_file}")

    # 彩色預覽
    print("\n" + "─" * 50)
    meta = result.get("metadata", {})
    print(f"📖 {meta.get('title', '未知書名')} — {meta.get('author', '未知作者')}")
    print(f"\n💡 精華語錄：")
    for q in result.get("highlights", [])[:3]:
        print(f"   「{q[:80]}{'…' if len(q)>80 else ''}」")
    print(f"\n📝 核心心得：")
    print(f"   {result.get('takeaways', '')[:200]}…")


if __name__ == "__main__":
    main()
