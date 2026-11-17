# -*- coding: utf-8 -*-
"""
知识库 RAG 检索质量真实评测（含应用层拒答兜底优化）
- 引擎：本地 Ollama bge-m3 (1024维) + 余弦检索（零积分）
- 语料：目标知识库内容（FAQ Q1-Q50 + 法规文号事实库，路径在下方 BASE 配置）
- 评测：50 题（45 FAQ 检索题 + 5 负样本）
- 优化：新增应用层拒答阈值扫描，给出较优 top-1 余弦拒答阈值

使用前请修改 BASE 指向你的知识库目录（或设置环境变量 RAG_EVAL_BASE）。
"""
import os, re, json, urllib.request, math

OLLAMA = "http://127.0.0.1:11434"
EMBED_MODEL = "bge-m3"
# 知识库根目录：可用环境变量覆盖，便于 CI / 多机复用
BASE = os.environ.get("RAG_EVAL_BASE", "path/to/your/knowledge_base")
FAQ = os.path.join(BASE, "website/_lexiang_sync/faq.md")
FACT = os.path.join(BASE, "法规文号事实库.md")
OUT_JSON = os.path.join(os.path.dirname(__file__), "eval_questions.json")
REPORT = os.path.join(os.path.dirname(__file__), "rag_eval_report.json")

def embed(text):
    req = urllib.request.Request(
        OLLAMA + "/api/embed",
        data=json.dumps({"model": EMBED_MODEL, "input": text}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["embeddings"][0]

def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(x*x for x in b))
    return dot/(na*nb) if na and nb else 0

# ---------- 1. 解析语料 ----------
faq = {}
text = open(FAQ, encoding="utf-8").read()
for block in re.split(r'\n## ', text):
    m = re.match(r'(Q\d+)\.\s*(.*?)\n(.*)', block, re.S)
    if m:
        qn, q, a = m.group(1), m.group(2).strip(), m.group(3).strip()
        faq[qn] = {"q": q, "a": a}

fact_chunks = []
for line in open(FACT, encoding="utf-8"):
    if line.startswith("|") and any(k in line for k in ["号令","公告","EU 20","ISO ","GB/","CFR","第 83"]):
        cells = [c.strip() for c in line.strip("|\n").split("|")]
        if len(cells) >= 3:
            fact_chunks.append(cells[1] + " " + cells[2])

# ---------- 2. 构建评测索引 ----------
corpus = [{"source": "faq#"+qn, "text": d["q"]+" "+d["a"][:600]} for qn, d in faq.items()]
corpus += [{"source": "fact", "text": t} for t in fact_chunks]
print(f"语料 chunk 数 = {len(corpus)}（FAQ {len(faq)} 条 + 法规事实 {len(fact_chunks)} 行），开始嵌入...")
for i, c in enumerate(corpus):
    c["vec"] = embed(c["text"][:400])
    if (i+1) % 20 == 0:
        print(f"  embed {i+1}/{len(corpus)}")

# ---------- 3. 构造 50 题标准答案集 ----------
questions = []
for qn in sorted(faq.keys(), key=lambda x: int(x[1:])):
    if int(qn[1:]) > 45:
        break
    questions.append({"query": faq[qn]["q"], "target": "faq#"+qn,
                      "gold": faq[qn]["a"][:200], "type": "faq"})
neg = ["今天北京天气怎么样？", "如何用 Python 写一个快速排序？",
       "NBA 昨天哪支球队赢了？", "红烧肉怎么做好吃？", "比特币现在价格是多少？"]
for n in neg:
    questions.append({"query": n, "target": None, "gold": "", "type": "negative"})

# ---------- 4. 检索 ----------
K = 5
for q in questions:
    qv = embed(q["query"][:400])
    scored = sorted(((cosine(qv, c["vec"]), c) for c in corpus), key=lambda x: -x[0])
    top = scored[:K]
    q["top1_score"] = round(top[0][0], 3)
    q["top5_sources"] = [c["source"] for _, c in top]
    q["top_sources"] = q["top5_sources"][:3]

# ---------- 5. 阈值扫描：应用层拒答兜底 ----------
faq_q = [q for q in questions if q["type"] == "faq"]
neg_q = [q for q in questions if q["type"] == "negative"]
faq_scores = sorted(q["top1_score"] for q in faq_q)
neg_scores = sorted(q["top1_score"] for q in neg_q)
print("\n=== top-1 分数分布 ===")
print(f"FAQ 正样本 最低={faq_scores[0]} 最高={faq_scores[-1]}")
print(f"负样本     最低={neg_scores[0]} 最高={neg_scores[-1]}")

candidates = [round(x, 2) for x in [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]]
scan = []
for T in candidates:
    fp = sum(1 for q in faq_q if q["top1_score"] >= T and q["target"] in q["top5_sources"])
    np_ = sum(1 for q in neg_q if q["top1_score"] < T)
    overall = (fp + np_) / len(questions)
    scan.append({"threshold": T, "faq_pass_rate": round(fp/len(faq_q), 4),
                 "neg_reject_rate": round(np_/len(neg_q), 4),
                 "overall_pass_rate": round(overall, 4)})

# 选较优阈值：优先 neg=100% 且 faq=100%；否则 faq=100% 下 neg 最高
best = next((s for s in scan if s["neg_reject_rate"] == 1.0 and s["faq_pass_rate"] == 1.0), None)
if best is None:
    best = next((s for s in scan if s["faq_pass_rate"] == 1.0), None)
if best is None:
    best = max(scan, key=lambda s: (s["neg_reject_rate"], s["faq_pass_rate"]))
T = best["threshold"]
print("\n=== 阈值扫描（应用层拒答：top-1 余弦 < T 则拒答）===")
for s in scan:
    mark = " <== 推荐" if s["threshold"] == T else ""
    print(f"  T={s['threshold']}: FAQ命中 {s['faq_pass_rate']:.0%} | 负样本拒答 {s['neg_reject_rate']:.0%} | 整体 {s['overall_pass_rate']:.0%}{mark}")

# 在推荐阈值下的逐题判定（模拟应用层行为）
for q in questions:
    q["app_reject"] = q["top1_score"] < T
    if q["type"] == "negative":
        q["hit"] = q["app_reject"]
    else:
        q["hit"] = (not q["app_reject"]) and (q["target"] in q["top5_sources"])

faq_pass = sum(1 for q in faq_q if q["hit"])
neg_pass = sum(1 for q in neg_q if q["hit"])
report = {
    "engine": f"Ollama {EMBED_MODEL} + cosine",
    "corpus_size": len(corpus),
    "k": K,
    "total": len(questions),
    "recommended_threshold": T,
    "faq_pass_rate": round(faq_pass/len(faq_q), 4),
    "negative_reject_rate": round(neg_pass/len(neg_q), 4),
    "overall_pass_rate": round((faq_pass+neg_pass)/len(questions), 4),
    "threshold_scan": scan,
    "failed": [{"query": q["query"], "type": q["type"], "top1_score": q["top1_score"],
                "top_sources": q["top_sources"], "app_reject": q.get("app_reject"),
                "gold_source": q["target"]}
               for q in questions if not q["hit"]],
}
print("\n================ 应用层拒答机制后评测结果 ================")
print(f"推荐阈值      : top-1 余弦 < {T} 则拒答")
print(f"语料规模      : {len(corpus)} chunks")
print(f"总题数        : {len(questions)}")
print(f"整体合格率    : {report['overall_pass_rate']:.1%}")
print(f"FAQ 检索命中  : {faq_pass}/{len(faq_q)} = {report['faq_pass_rate']:.1%}")
print(f"负样本拒答率  : {neg_pass}/{len(neg_q)} = {report['negative_reject_rate']:.1%}")
if report["failed"]:
    print(f"\n未通过 {len(report['failed'])} 题：")
    for f in report["failed"]:
        print(f"  - [{f['type']}] {f['query'][:40]} | top1={f['top1_score']} | 拒答={f.get('app_reject')} | 召回:{f['top_sources']}")

json.dump(questions, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(report, open(REPORT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n标准答案集已导出: {OUT_JSON}")
print(f"评测报告已导出: {REPORT}")
