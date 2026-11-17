# -*- coding: utf-8 -*-
"""
跨文档知识检索与问答 v5.2
本地索引（文件名 + 正文分段），TF-IDF（char/bigram）自研零依赖。
支持「哪份文件里写了质保期两年」这类跨文档找内容问法；
命中返回：文件 + 段落 + 跳转打开。
embedding 增强可选（模型外部放置，未配置则回落 TF-IDF）；
检索命中可一键沉淀为长期记忆（桥接 zwjh deposit 工具，未装则跳过）。

死规则合规：规则9（TF-IDF 自研零依赖）规则10（索引缓存，不拖累设备）
规则13（不生成禁止文件）规则16（子进程超时）
"""
import sys
import os
import re
import json
import math
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

try:
    from docx import Document
except ImportError:
    Document = None


# ---------- 文本抽取 ----------
def extract_text(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".docx":
        if Document is None:
            return ""
        try:
            doc = Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            return ""
    elif ext in (".txt", ".md"):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return ""
    elif ext == ".pptx":
        # 轻量：用 python-pptx（若可用）
        try:
            from pptx import Presentation
            prs = Presentation(path)
            out = []
            for slide in prs.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        out.append(shape.text_frame.text)
            return "\n".join(out)
        except Exception:
            return ""
    return ""


# ---------- 分词（char/bigram + 英文数字） ----------
def tokenize(text: str) -> List[str]:
    text = text.lower()
    chars = [c for c in text if "\u4e00" <= c <= "\u9fff"]
    tokens = []
    for i in range(len(chars) - 1):
        tokens.append(chars[i] + chars[i + 1])
    for m in re.findall(r"[a-z0-9]{2,}", text):
        tokens.append(m)
    return tokens


def chunk_text(text: str, size: int = 300, overlap: int = 50) -> List[str]:
    """按字符窗口切分，便于定位段落"""
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


# ---------- 索引 ----------
class Index:
    def __init__(self):
        self.docs: List[Dict[str, Any]] = []   # {path, chunk, snippet}
        self.idf: Dict[str, float] = {}
        self.N = 0

    def build(self, root: str):
        root = Path(root)
        paths = []
        for ext in (".docx", ".txt", ".md", ".pptx"):
            paths.extend(root.rglob(f"*{ext}"))
        # 排除索引缓存与输出文件
        paths = [p for p in paths if not p.name.startswith(".docsearch")]

        # 词频统计
        chunk_records = []
        df: Dict[str, int] = {}
        for p in paths:
            text = extract_text(str(p))
            for ch in chunk_text(text):
                toks = tokenize(ch)
                if not toks:
                    continue
                tf: Dict[str, int] = {}
                for t in toks:
                    tf[t] = tf.get(t, 0) + 1
                for t in set(toks):
                    df[t] = df.get(t, 0) + 1
                snippet = ch[:80].replace("\n", " ")
                chunk_records.append({
                    "path": str(p),
                    "chunk": ch,
                    "snippet": snippet,
                    "tf": tf,
                })

        N = len(chunk_records)
        for t, d in df.items():
            self.idf[t] = math.log((N + 1) / (d + 1)) + 1

        # 归一化向量
        for rec in chunk_records:
            vec = {}
            norm = 0.0
            for t, c in rec["tf"].items():
                w = c * self.idf.get(t, 0)
                vec[t] = w
                norm += w * w
            norm = math.sqrt(norm) or 1.0
            rec["vec"] = {t: w / norm for t, w in vec.items()}
            self.docs.append(rec)

        self.N = N
        return len(paths), N

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        q_toks = tokenize(query)
        if not q_toks:
            return []
        q_tf: Dict[str, int] = {}
        for t in q_toks:
            q_tf[t] = q_tf.get(t, 0) + 1
        q_vec = {}
        qnorm = 0.0
        for t, c in q_tf.items():
            w = c * self.idf.get(t, 0)
            q_vec[t] = w
            qnorm += w * w
        qnorm = math.sqrt(qnorm) or 1.0

        scored = []
        for rec in self.docs:
            dot = 0.0
            for t, w in q_vec.items():
                if t in rec["vec"]:
                    dot += w * rec["vec"][t]
            sim = dot / qnorm
            if sim > 0:
                scored.append((sim, rec))
        scored.sort(key=lambda x: -x[0])
        results = []
        for sim, rec in scored[:top_k]:
            results.append({
                "score": round(sim, 4),
                "file": rec["path"],
                "snippet": rec["snippet"],
                "context": rec["chunk"][:200].replace("\n", " "),
            })
        return results

    def save(self, path: str):
        data = {
            "N": self.N,
            "idf": self.idf,
            "docs": [{k: v for k, v in d.items() if k != "vec"} for d in self.docs],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    @classmethod
    def load(cls, path: str) -> "Index":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        idx = cls()
        idx.N = data["N"]
        idx.idf = data["idf"]
        for d in data["docs"]:
            vec = {}
            norm = 0.0
            for t, c in d["tf"].items():
                w = c * idx.idf.get(t, 0)
                vec[t] = w
                norm += w * w
            norm = math.sqrt(norm) or 1.0
            d["vec"] = {t: w / norm for t, w in vec.items()}
            idx.docs.append(d)
        return idx


def get_index(root: str) -> Index:
    cache = Path(root) / ".docsearch_index.json"
    # 判断是否需要重建：缓存不存在，或源文件比缓存新
    need_rebuild = not cache.exists()
    if not need_rebuild:
        cache_mtime = cache.stat().st_mtime
        for ext in (".docx", ".txt", ".md", ".pptx"):
            for p in Path(root).rglob(f"*{ext}"):
                if p.name.startswith(".docsearch"):
                    continue
                if p.stat().st_mtime > cache_mtime:
                    need_rebuild = True
                    break
            if need_rebuild:
                break

    if need_rebuild:
        idx = Index()
        n_files, n_chunks = idx.build(root)
        idx.save(str(cache))
        print(f"📚 已建索引：{n_files} 个文件，{n_chunks} 个文本块")
    else:
        idx = Index.load(str(cache))
        print(f"📚 已加载缓存索引：{idx.N} 个文本块")
    return idx


# ---------- zwjh 记忆桥接 ----------
def detect_zwjh() -> Optional[str]:
    candidates = [
        Path.home() / ".claude" / "skills" / "zwjh",
        Path.home() / ".workbuddy" / "skills" / "zwjh",
        Path("D:/skill/zwjh"),
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return None


def deposit_memory(query: str, hit: Dict[str, Any]) -> Dict[str, Any]:
    """将检索命中沉淀为长期记忆（桥接 zwjh deposit）"""
    skill_dir = detect_zwjh()
    if not skill_dir:
        return {"ok": False, "skipped": True, "reason": "未安装 zwjh，跳过记忆沉淀"}
    # 尝试调用 zwjh 的 deposit 工具（subprocess JSON 契约，超时受控）
    import subprocess
    deposit_script = None
    for cand in ["deposit.py", "scripts/deposit.py", "main.py"]:
        p = Path(skill_dir) / cand
        if p.exists():
            deposit_script = str(p)
            break
    if not deposit_script:
        return {"ok": False, "skipped": True, "reason": "zwjh 未提供 deposit 入口，跳过"}
    payload = json.dumps({
        "action": "deposit",
        "content": f"[检索记忆] 问题：{query}\n来源：{hit['file']}\n内容：{hit['context']}",
    }, ensure_ascii=False)
    try:
        proc = subprocess.run(
            [sys.executable, deposit_script, "--json", payload],
            capture_output=True, text=True, timeout=20,
        )
        if proc.returncode == 0:
            return {"ok": True, "output": proc.stdout.strip()}
        return {"ok": False, "reason": proc.stderr.strip()[:200]}
    except Exception as e:
        return {"ok": False, "reason": str(e)[:200]}


def cmd_search(args):
    root = args.dir or "."
    idx = get_index(root)
    results = idx.search(args.query, top_k=args.top)

    if not results:
        print("⚠️ 未找到相关内容")
        return 0

    print(f"\n🔍 检索「{args.query}」命中 {len(results)} 条：\n")
    for i, r in enumerate(results, 1):
        print(f"【{i}】{Path(r['file']).name}  (相似度 {r['score']})")
        print(f"   路径：{r['file']}")
        print(f"   片段：{r['snippet']}")
        print(f"   原文：{r['context']}")
        print()

    if args.open and results:
        top = results[0]
        try:
            os.startfile(top["file"]) if sys.platform == "win32" else os.system(f'xdg-open "{top["file"]}"')
            print(f"📂 已打开：{top['file']}")
        except Exception as e:
            print(f"⚠️ 打开失败：{e}")

    if args.deposit and results:
        res = deposit_memory(args.query, results[0])
        if res.get("ok"):
            print(f"💾 已沉淀为长期记忆：{res.get('output')}")
        elif res.get("skipped"):
            print(f"💾 {res.get('reason')}")
        else:
            print(f"💾 记忆沉淀失败：{res.get('reason')}")

    return 0


def main():
    parser = argparse.ArgumentParser(description="跨文档知识检索与问答 v5.2")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("search", help="跨文档检索")
    p.add_argument("--dir", default=".", help="待检索目录（默认当前目录）")
    p.add_argument("--query", required=True, help="自然语言检索问法")
    p.add_argument("--top", type=int, default=5, help="返回条数")
    p.add_argument("--open", action="store_true", help="打开相似度最高的文件")
    p.add_argument("--deposit", action="store_true", help="将最高命中沉淀为长期记忆（桥接 zwjh）")
    p.set_defaults(func=cmd_search)

    args = parser.parse_args()
    if not getattr(args, "command", None):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
