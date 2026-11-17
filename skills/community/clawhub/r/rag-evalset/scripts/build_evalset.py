#!/usr/bin/env python3
"""构建生产级 RAG 评估集：问题 + 参考答案 + gold chunk ID。

两种语料入口（二选一）：
  位置参数 docs          .txt/.md 目录或文件，由本脚本切块（Markdown 标题感知）
  --chunks-from 文件     外部切块器输出（例如你自己的索引器），每行格式：
                         {"chunk_id": "...", "text": "...", "source": "..."}

产出到 --out-dir：
  evalset.jsonl  query_id、query、reference_answer、gold_chunk_ids、元信息
  chunks.jsonl   实际喂给 ragas 的语料（让被测系统索引这批块，保证 ID 对齐）
  review.jsonl   需要人工补标 gold 的样本
  manifest.json  溯源：参数、语料统计、回填率、版本号

需要环境变量 OPENAI_API_KEY；可选 OPENAI_BASE_URL（或 --base-url）指向任意
OpenAI 兼容端点（支持 Dashscope/Qwen）。
"""
import argparse
import hashlib
import json
import os
import random
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

WS_RE = re.compile(r"\s+")


def norm(s: str) -> str:
    return WS_RE.sub(" ", unicodedata.normalize("NFKC", s)).strip()


def split_paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def split_sentences(text):
    parts = re.split(r"(?<=[。！？.!?；;\n])", text)
    return [p for p in parts if p.strip()]


def tail_overlap(chunk_text: str, overlap: int):
    """返回 chunk_text 句子对齐的尾部片段，最多 overlap 个字符。"""
    if overlap <= 0:
        return ""
    out = ""
    for s in reversed(split_sentences(chunk_text)):
        cand = s + out
        if len(cand) > overlap:
            break
        out = cand
    if not out:  # 单句就超过 overlap：退化为按字符切
        out = chunk_text[-overlap:]
    return out


def pack(paragraphs, max_chars, overlap):
    chunks, buf = [], ""
    for para in paragraphs:
        pieces = [para] if len(para) <= max_chars else None
        if pieces is None:
            if buf:
                chunks.append(buf)
                buf = tail_overlap(buf, overlap)
            sentences, acc = split_sentences(para), ""
            for s in sentences:
                if acc and len(acc) + len(s) > max_chars:
                    chunks.append(acc)
                    acc = tail_overlap(acc, overlap)
                acc += s
            if acc:
                buf = (buf + "\n" + acc).strip() if buf else acc
            continue
        if buf and len(buf) + 1 + len(para) > max_chars:
            chunks.append(buf)
            buf = (tail_overlap(buf, overlap) + "\n" + para).strip()
        else:
            buf = (buf + "\n" + para).strip() if buf else para
    if buf:
        chunks.append(buf)
    return chunks


def merge_short(chunks, min_chars=80):
    """过短块（如纯标题行）并入下一块，避免无语料价值的碎块稀释检索与评估。"""
    merged = []
    carry = ""
    for c in chunks:
        piece = (carry + "\n" + c).strip() if carry else c
        if len(piece) < min_chars:
            carry = piece
            continue
        merged.append(piece)
        carry = ""
    if carry:
        if merged:
            merged[-1] = (merged[-1] + "\n" + carry).strip()
        else:
            merged.append(carry)
    return merged


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def chunk_md_file(path, max_chars, overlap):
    """标题切分：## 是硬边界；标题行留在所属小节内，让块文本自带结构上下文。
    代码围栏内的 # 不视为标题；跨小节的过短块向前合并。"""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    sections, body = [], []
    in_fence = False

    def flush():
        paras = split_paragraphs("\n".join(body))
        if paras:
            sections.append(paras)

    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            body.append(line)
            continue
        if not in_fence and HEADING_RE.match(line):
            flush()
            body = [line]
        else:
            body.append(line)
    flush()

    raw = []
    for paras in sections:
        raw.extend(pack(paras, max_chars, overlap))
    seen, final, i = set(), [], 0
    for c in merge_short(raw):
        key = norm(c)
        if not key or key in seen:
            continue
        seen.add(key)
        final.append({"chunk_id": f"{path.stem}-{i:04d}", "source": path.name, "text": c})
        i += 1
    return final


def chunk_plain_file(path, max_chars, overlap):
    paras = split_paragraphs(path.read_text(encoding="utf-8", errors="replace"))
    return [
        {"chunk_id": f"{path.stem}-{i:04d}", "source": path.name, "text": c}
        for i, c in enumerate(merge_short(pack(paras, max_chars, overlap)))
    ]


def read_external_chunks(path):
    corpus, ids = [], set()
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError as e:
            sys.exit(f"{path}:{n}: JSON 格式错误：{e}")
        cid, text = r.get("chunk_id"), r.get("text")
        if not cid or not norm(str(text or "")):
            sys.exit(f"{path}:{n}: 必须有 chunk_id 和非空 text")
        if cid in ids:
            sys.exit(f"{path}:{n}: chunk_id 重复：{cid!r}——生成前必须先修复")
        ids.add(cid)
        corpus.append({"chunk_id": cid, "source": r.get("source", ""), "text": text})
    if not corpus:
        sys.exit(f"{path}: 没有找到任何块")
    return corpus


def build_corpus(a):
    docs = Path(a.docs)
    corpus = []
    files = [docs] if docs.is_file() else sorted(
        p for p in docs.rglob("*") if p.suffix.lower() in {".txt", ".md", ".markdown"})
    for f in files:
        if f.suffix.lower() in {".md", ".markdown"}:
            corpus.extend(chunk_md_file(f, a.chunk_chars, a.overlap))
        else:
            corpus.extend(chunk_plain_file(f, a.chunk_chars, a.overlap))
    return corpus


def backfill_gold(ctxs, text2ids):
    """两级回填：精确匹配 -> 包含匹配（概括跨多块 / 引用被截断）。"""
    gold, unmatched = [], []
    for ctx in ctxs:
        n = norm(ctx)
        ids = text2ids.get(n)
        if ids is None:
            ids = [i for frag, idlist in text2ids.items() for i in idlist
                   if (frag in n or (len(n) > 40 and n in frag))]
            ids = sorted(set(ids))
        if ids:
            gold.extend(ids)
        else:
            unmatched.append(ctx)
    return sorted(set(gold)), unmatched


def merge_review(a):
    """把人工补标好的 review 文件合并回 evalset.jsonl（幂等，可多次执行）。"""
    out = Path(a.out_dir)
    es_path = out / "evalset.jsonl"
    if not es_path.exists():
        sys.exit(f"{es_path} 不存在——--merge-review 需要在生成完成后使用")
    rows = {r["query_id"]: r for r in
            (json.loads(l) for l in es_path.read_text(encoding="utf-8").splitlines() if l.strip())}
    fixed = skipped = 0
    for r in (json.loads(l) for l in Path(a.merge_review).read_text(encoding="utf-8").splitlines() if l.strip()):
        qid, gold = r.get("query_id"), r.get("gold_chunk_ids") or []
        if qid not in rows:
            skipped += 1
            continue
        unknown = [g for g in gold if g not in {c["chunk_id"] for c in
                   (json.loads(l) for l in (out / "chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}]
        if unknown:
            sys.exit(f"{qid}: gold 含未知 chunk_id {unknown[:3]}——必须来自 chunks.jsonl")
        rows[qid]["gold_chunk_ids"] = sorted(set(gold))
        rows[qid]["needs_review"] = False
        fixed += 1
    es_path.write_text("".join(json.dumps(rows[q], ensure_ascii=False) + "\n" for q in sorted(rows)),
                       encoding="utf-8")
    print(f"合并完成：修正 {fixed} 条，忽略不在 evalset 的 {skipped} 条 -> {es_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docs", nargs="?", help="待切块的 .txt/.md 目录或文件")
    ap.add_argument("--chunks-from", help="外部切块 jsonl（{chunk_id,text,source?}），跳过内置切块")
    ap.add_argument("--out-dir", default="evalset")
    ap.add_argument("--size", type=int, default=50, help="生成问题数")
    ap.add_argument("--chunk-chars", type=int, default=600, help="单块最大字符数（>=100）")
    ap.add_argument("--overlap", type=int, default=100, help="块间重叠字符数（默认 100）")
    ap.add_argument("--llm-model", default="gpt-4o-mini")
    ap.add_argument("--embed-model", default="text-embedding-3-small")
    ap.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL"), help="OpenAI 兼容端点")
    ap.add_argument("--model-kwargs", default=None, help='透传给 chat 模型的 JSON，如 {"temperature":0.3}')
    ap.add_argument("--cache-dir", default=None, help="LLM+向量磁盘缓存目录（跨次运行复用）")
    ap.add_argument("--seed", type=int, default=None, help="随机种子，保证可复现")
    ap.add_argument("--workers", type=int, default=32, help="transform/采样并发数（实测端点 32 并发无线性衰减）")
    ap.add_argument("--transform-model", default=None, help="图谱 transform 用更快模型（如 qwen-turbo），问题生成仍用 --llm-model")
    ap.add_argument("--kg-cache", default=None, help="知识图谱 JSON 缓存路径；同语料重跑跳过全部 transform（最大加速项）")
    ap.add_argument("--single-hop", type=float, default=None, help="单跳具体问题权重（如 0.5）")
    ap.add_argument("--multi-hop-specific", type=float, default=None, help="多跳具体问题时权重")
    ap.add_argument("--multi-hop-abstract", type=float, default=None, help="多跳概括/抽象问题时权重")
    ap.add_argument("--dry-run", action="store_true", help="只产出 chunks.jsonl 和 manifest，不调 LLM")
    ap.add_argument("--query-language", default=None, help='问题/参考答案语言，如 zh、en（默认由模型自决）')
    ap.add_argument("--llm-context", default=None, help='附加生成指导（字符串或 @文件路径），如"多生成对比类问题"；与 --query-language 合并')
    ap.add_argument("--personas", default=None, help='自定义 persona JSON 文件（[{name,role_description}]），控制问题前缀人物语言与视角；缺省由 LLM 生成')
    ap.add_argument("--merge-review", default=None, metavar="FILE",
                    help="把人工补标后的 review 文件合并回 <out-dir>/evalset.jsonl 后退出（幂等）")
    a = ap.parse_args()

    if a.merge_review:
        merge_review(a)
        return

    if not a.docs and not a.chunks_from:
        ap.error("必须提供 docs 位置参数或 --chunks-from 之一")
    if a.docs and a.chunks_from:
        ap.error("docs 位置参数与 --chunks-from 互斥，只能选一个")
    if a.size < 1:
        ap.error("--size 必须 >= 1")
    if a.chunk_chars < 100:
        ap.error("--chunk-chars 必须 >= 100")
    dist_flags = {"--single-hop": a.single_hop, "--multi-hop-specific": a.multi_hop_specific,
                  "--multi-hop-abstract": a.multi_hop_abstract}
    if any(v is not None for v in dist_flags.values()) and any(v is None for v in dist_flags.values()):
        ap.error("问题分布三个权重（--single-hop/--multi-hop-specific/--multi-hop-abstract）需同时给出")
    if None not in dist_flags.values() and abs(sum(dist_flags.values()) - 1.0) > 1e-6:
        ap.error(f"分布权重之和须为 1，当前 {sum(dist_flags.values()):.4f}")

    sys.stdout.reconfigure(line_buffering=True)  # 实时日志：逐阶段刷新，便于用户感知进度
    if a.seed is not None:
        random.seed(a.seed)
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    timings, _prev = {}, [time.time()]

    def stage(name):
        timings[name] = round(time.time() - _prev[0], 1)
        _prev[0] = time.time()

    print("【1/6 构建语料】")
    corpus = read_external_chunks(Path(a.chunks_from)) if a.chunks_from else build_corpus(a)
    if not corpus:
        sys.exit("没有产出任何可用块——检查输入或 --chunk-chars")
    (out / "chunks.jsonl").write_text(
        "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in corpus), encoding="utf-8")

    text2ids = {}
    for c in corpus:
        text2ids.setdefault(norm(c["text"]), []).append(c["chunk_id"])
    id2source = {c["chunk_id"]: c["source"] for c in corpus}
    print(f"语料：{len(corpus)} 块，共 {sum(len(c['text']) for c in corpus)} 字符 -> {out/'chunks.jsonl'}")
    stage("1_corpus")

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "entry_mode": "external" if a.chunks_from else "internal",
        "params": {k: getattr(a, k) for k in
                   ("size", "chunk_chars", "overlap", "llm_model", "embed_model", "base_url",
                    "model_kwargs", "cache_dir", "seed", "workers", "transform_model", "kg_cache",
                    "query_language", "llm_context", "personas",
                    "single_hop", "multi_hop_specific", "multi_hop_abstract")},
        "corpus_stats": {"num_chunks": len(corpus),
                         "num_sources": len({c["source"] for c in corpus if c["source"]})},
    }

    if a.dry_run:
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print("dry-run：跳过 TestsetGenerator；manifest 已写出")
        return

    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("未设置 OPENAI_API_KEY——生成评估集必需")

    print("【2/6 加载 ragas 与 LLM 客户端】")
    try:
        from openai import AsyncOpenAI
        from ragas import __version__ as ragas_version
        from ragas.llms import llm_factory
        from ragas.embeddings import OpenAIEmbeddings
        from ragas.run_config import RunConfig
        from ragas.testset import TestsetGenerator
        from ragas.dataset_schema import SingleTurnSample
    except ImportError as e:
        sys.exit(f"缺少依赖（{e}）——需要：pip install 'ragas>=0.4' openai")

    manifest["ragas_version"] = ragas_version

    cache = None
    if a.cache_dir:
        from ragas.cache import DiskCacheBackend
        cache = DiskCacheBackend(cache_dir=a.cache_dir)

    client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url=a.base_url or None)
    extra = json.loads(a.model_kwargs) if a.model_kwargs else {}
    guidance_parts = []
    if a.query_language:
        guidance_parts.append(f"所有生成的问题（query）与参考答案（reference answer）必须使用{a.query_language}撰写。")
    if a.llm_context:
        raw = a.llm_context
        guidance_parts.append(Path(raw[1:]).read_text(encoding="utf-8").strip() if raw.startswith("@") else raw)
    guidance = "\n".join(guidance_parts) or None
    personas = None
    if a.personas:
        from ragas.testset.persona import Persona
        data = json.loads(Path(a.personas).read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else [data]
        personas = [Persona(name=p["name"], role_description=p["role_description"]) for p in items]
        if not personas:
            sys.exit("--personas 文件解析后为空")
        print(f"使用自定义 persona {len(personas)} 个（跳过 LLM 生成，问题语言不再受英文 persona 污染）")
    gen = TestsetGenerator(
        llm=llm_factory(a.llm_model, client=client, cache=cache, **extra),
        embedding_model=OpenAIEmbeddings(client=client, model=a.embed_model, cache=cache),
        llm_context=guidance,
        persona_list=personas,
    )
    stage("2_load_client")
    from ragas.testset.graph import KnowledgeGraph, Node, NodeType
    from ragas.testset.transforms import apply_transforms, default_transforms_for_prechunked
    rc = RunConfig(max_workers=a.workers)
    n_chunks = len(corpus)
    tlm = llm_factory(a.transform_model, client=client, cache=cache, **extra) if a.transform_model else gen.llm

    # 知识图谱：命中缓存则秒过 transform（最大加速杠杆）
    fingerprint = hashlib.sha256(
        ("\n".join(norm(c["text"]) for c in corpus) + f"|{a.transform_model or a.llm_model}").encode()
    ).hexdigest()[:16]
    kg, kg_reused = None, False
    if a.kg_cache and Path(a.kg_cache).exists() and Path(a.kg_cache + ".meta.json").exists():
        try:
            if json.loads(Path(a.kg_cache + ".meta.json").read_text()).get("fingerprint") == fingerprint:
                kg = KnowledgeGraph.load(a.kg_cache)
                kg_reused = True
                print(f"【3/6 复用知识图谱缓存】{a.kg_cache}（跳过全部 transform，预计省 6-8 分钟）")
            else:
                print("! 知识图谱缓存与当前语料指纹不符（内容或模型已变），将重建")
        except Exception as e:
            print(f"! 知识图谱缓存读取失败（{type(e).__name__}: {e}），将重建")

    if kg is None:
        print(f"【3/6 构建知识图谱】{n_chunks} 块，transform 每块约 3 次 LLM 调用"
              f"（transform 模型：{a.transform_model or a.llm_model}，并发 {a.workers}）")
        kg = KnowledgeGraph(nodes=[
            Node(type=NodeType.CHUNK, properties={
                "page_content": c["text"],
                "document_metadata": {"chunk_id": c["chunk_id"], "source": c["source"]},
            }) for c in corpus])
        apply_transforms(kg, default_transforms_for_prechunked(llm=tlm,
                                                               embedding_model=gen.embedding_model),
                         run_config=rc)
        if a.kg_cache:
            kg.save(a.kg_cache)
            Path(a.kg_cache + ".meta.json").write_text(json.dumps(
                {"fingerprint": fingerprint, "num_chunks": n_chunks,
                 "transform_model": a.transform_model or a.llm_model}))
            print(f"   知识图谱已缓存 -> {a.kg_cache}（下次同语料重跑直接复用）")

    query_distribution = None
    stage("3_knowledge_graph")
    if a.single_hop is not None:
        from ragas.testset.synthesizers import (
            MultiHopAbstractQuerySynthesizer,
            MultiHopSpecificQuerySynthesizer,
            SingleHopSpecificQuerySynthesizer,
        )
        pairs = [(SingleHopSpecificQuerySynthesizer, a.single_hop, "单跳具体问题"),
                 (MultiHopSpecificQuerySynthesizer, a.multi_hop_specific, "多跳具体问题"),
                 (MultiHopAbstractQuerySynthesizer, a.multi_hop_abstract, "多跳概括问题")]
        usable = []
        for cls, w, label in pairs:
            if w <= 0:
                continue
            inst = cls(llm=gen.llm, llm_context=guidance)
            try:
                has_clusters = bool(inst.get_node_clusters(kg))
            except Exception:
                has_clusters = False
            if has_clusters:
                usable.append((inst, w))
            else:
                print(f"! 预检：语料跨块关系不足以支撑「{label}」，该类权重已剔除并重新分配（语料偏小或段落独立性强）")
        if not usable:
            sys.exit("语料过小或缺乏跨块关联，显式分布无任何一类可满足——请扩大语料或去掉分布参数改用默认混合")
        total = sum(w for _, w in usable)
        query_distribution = [(inst, w / total) for inst, w in usable]
        dist_note = f"实际分布 {[(type(i).__name__, round(w, 2)) for i, w in query_distribution]}"
    else:
        dist_note = "默认混合分布（ragas 自动选择语料支持的类型）"
    gen.knowledge_graph = kg
    print(f"【4/6 TestsetGenerator 生成中】{a.size} 个问题，{dist_note}")
    testset = gen.generate(testset_size=a.size, query_distribution=query_distribution,
                           run_config=rc)
    stage("4_generate_queries")

    print("【5/6 回填 gold chunk ID】")
    records, review = [], []
    for i, ts in enumerate(testset.samples, 1):
        s = ts.eval_sample
        if not isinstance(s, SingleTurnSample) or not s.user_input:
            continue
        gold, unmatched = backfill_gold(s.reference_contexts or [], text2ids)
        rec = {
            "query_id": f"q{i:04d}",
            "query": s.user_input,
            "reference_answer": s.reference,
            "gold_chunk_ids": gold,
            "gold_sources": sorted({id2source.get(g, "") for g in gold}),
            "reference_contexts": s.reference_contexts or [],
            "synthesizer": ts.synthesizer_name,
            "needs_review": bool(unmatched),
            "unmatched_reference_contexts": unmatched,
        }
        records.append(rec)
        if unmatched or not gold:
            review.append(rec)

    print("【6/6 写出结果】")
    stage("5_backfill")
    write_jsonl(out / "evalset.jsonl", records)
    write_jsonl(out / "review.jsonl", review)
    stage("6_write")
    with_gold = sum(1 for r in records if r["gold_chunk_ids"])
    by_synth = {}
    for r in records:
        by_synth[r["synthesizer"]] = by_synth.get(r["synthesizer"], 0) + 1
    manifest["results"] = {"num_queries": len(records), "gold_matched": with_gold,
                           "needs_review": len(review), "by_synthesizer": by_synth}
    manifest["stage_seconds"] = timings
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"评估集：{len(records)} 个问题 | gold 回填 {with_gold}/{len(records)} | 待人工复核 {len(review)}")
    print(f"合成器分布：{by_synth}")
    print(f"-> {out/'evalset.jsonl'}（溯源：{out/'manifest.json'}）")
    if review:
        print(f"! {len(review)} 条在 {out/'review.jsonl'}：人工补标 gold_chunk_ids 后合并回 evalset.jsonl；"
              f"不补也可以——这些样本不参与 IR 层统计，仍可用于 ragas 层")


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


if __name__ == "__main__":
    main()
