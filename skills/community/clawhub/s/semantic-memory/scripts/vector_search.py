#!/usr/bin/env python3
"""
混合搜索 v5 — Semantic Memory 核心检索脚本
依赖：chromadb, jieba
用法：python3 vector_search.py "你的查询" [topk]
"""
import chromadb, os, pickle, math
from collections import Counter
import jieba
jieba.setLogLevel(20)

# ── 配置 ──────────────────────────────────────────────────────────
CLIENT_HOST = os.environ.get('CHROMA_HOST', 'localhost')
CLIENT_PORT = int(os.environ.get('CHROMA_PORT', '8000'))
CACHE_DIR   = os.environ.get('TFIDF_CACHE', './tfidf_cache')
os.makedirs(CACHE_DIR, exist_ok=True)

client = chromadb.HttpClient(host=CLIENT_HOST, port=CLIENT_PORT)

# ── Agent 路由 ────────────────────────────────────────────────────
AGENT_KEYWORDS = {
    '狗蛋':    ['狗蛋', 'goudan', 'CSI', '跌倒', '产品规划', 'ESP32', '硬件', '老人监测'],
    '狗学术':  ['狗学术', 'gouxueshu', '学术', '论文', '引用', '文献', '查重'],
    '百晓生':  ['百晓生', '用户调研', '配置'],
}
AGENT_COLLECTION = {'狗蛋': 'projects', '狗学术': 'knowledge', '百晓生': 'memories'}

def detect_agent(query):
    q = query.lower()
    return next((a for a, kws in AGENT_KEYWORDS.items()
                 if any(kw.lower() in q for kw in kws)), None)

def get_collection_order(query):
    agent = detect_agent(query)
    order = ['memories', 'knowledge', 'projects']
    if agent:
        coll = AGENT_COLLECTION[agent]
        order = [coll] + [c for c in order if c != coll]
    return order

# ── Tokenizer ─────────────────────────────────────────────────────
def tokenize(text):
    return [t for t in jieba.cut(text.lower()) if len(t) >= 2]

# ── TF-IDF Index ─────────────────────────────────────────────────
class TFIDFIndex:
    def __init__(self):
        self.docs, self.vectors, self.doc_norms = [], [], []

    def build(self, docs):
        self.docs = docs
        N = len(docs)
        df_global = Counter()
        for doc in docs:
            df_global.update(set(tokenize(doc)))
        self.df_global = df_global
        self.N = N
        self.vectors, self.doc_norms = [], []
        for doc in docs:
            tf = Counter(tokenize(doc))
            vec = {}
            for token, freq in tf.items():
                idf = math.log((N + 1) / (df_global.get(token, 0) + 1)) + 1
                vec[token] = freq * idf
            self.vectors.append(vec)
            norm = math.sqrt(sum(v**2 for v in vec.values()))
            self.doc_norms.append(norm if norm > 0 else 1.0)

    def compute_query_vec(self, query):
        tf = Counter(tokenize(query))
        q_vec = {}
        for token, freq in tf.items():
            idf = math.log((self.N + 1) / (self.df_global.get(token, 0) + 1)) + 1
            q_vec[token] = freq * idf
        q_norm = math.sqrt(sum(v**2 for v in q_vec.values()))
        return q_vec, q_norm

    def fast_scores(self, query):
        q_vec, q_norm = self.compute_query_vec(query)
        if q_norm == 0:
            return [(0.0, i) for i in range(len(self.docs))]
        results = []
        for i, (vec, norm) in enumerate(zip(self.vectors, self.doc_norms)):
            dot = sum(q_vec.get(t, 0) * vec.get(t, 0) for t in set(q_vec) & set(vec))
            results.append((dot / (q_norm * norm), i))
        results.sort(reverse=True)
        return results

    def search(self, query, topk=None):
        topk = topk or len(self.docs)
        tokens = tokenize(query)
        if not tokens:
            return [(0.0, i, self.docs[i]) for i in range(min(topk, len(self.docs)))]
        scored = self.fast_scores(query)
        return [(s, i, self.docs[i]) for s, i in scored[:topk]]

# ── Collection 加载（带缓存）─────────────────────────────────────
def load_collection(name):
    cache_path = os.path.join(CACHE_DIR, f'{name}.pkl')
    col = client.get_collection(name)
    count = col.count()

    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 100:
        try:
            with open(cache_path, 'rb') as f:
                cached = pickle.load(f)
            if cached.get('count') == count:
                print(f"  📦 TF-IDF缓存命中: {name} ({count}条)")
                return cached['docs'], cached['metas'], cached['index']
        except: pass

    print(f"  🔨 构建TF-IDF索引: {name} ({count}条)...")
    results = col.get(include=['documents', 'metadatas'])
    docs = results['documents']
    metas = results.get('metadatas') or [{}] * len(docs)
    idx = TFIDFIndex()
    idx.build(docs)
    with open(cache_path, 'wb') as f:
        pickle.dump({'docs': docs, 'metas': metas, 'index': idx, 'count': count}, f)
    print(f"  💾 TF-IDF缓存已保存")
    return docs, metas, idx

# ── 单 collection 搜索 ────────────────────────────────────────────
def search_collection(name, query, topk=20):
    docs, metas, idx = load_collection(name)
    if not docs:
        return []

    tfidf_results = idx.search(query, topk=topk)
    max_tfidf = tfidf_results[0][0] if tfidf_results else 1.0
    q_vec, q_norm = idx.compute_query_vec(query)

    vec_r = client.get_collection(name).query(
        query_texts=[query], n_results=topk,
        include=['documents', 'metadatas', 'distances']
    )
    vec_map = {}
    if vec_r['documents'] and vec_r['documents'][0]:
        for doc, meta, dist in zip(vec_r['documents'][0],
                                     vec_r['metadatas'][0] or [],
                                     vec_r['distances'][0]):
            key = doc[:60]
            sim = 1 - (dist / 2) if dist is not None else 0
            if key not in vec_map or sim > vec_map[key][0]:
                vec_map[key] = (sim, doc, meta)

    results = []
    seen = set()
    for tfidf_sim, i, doc in tfidf_results:
        key = doc[:60]
        if key in seen:
            continue
        seen.add(key)
        tfidf_norm = tfidf_sim / max_tfidf if max_tfidf > 0 else 0
        vec_sim = vec_map.get(key, (0, None, None))[0]
        src = (metas[i] or {}).get('source', '') or ''
        boost = sum(0.4 for t in tokenize(query) if t in src.lower())
        combined = 0.45 * vec_sim + 0.55 * tfidf_norm + boost
        results.append((combined, vec_sim, tfidf_sim, doc, metas[i]))

    seen_keys = {d[:60] for _, _, _, d, _ in results}
    for key, (vec_sim, doc, meta) in vec_map.items():
        if key not in seen_keys:
            seen_keys.add(key)
            doc_idx = next((j for j, d in enumerate(docs) if d[:60] == key), None)
            if doc_idx is not None:
                dot = sum(q_vec.get(t, 0) * idx.vectors[doc_idx].get(t, 0)
                          for t in set(q_vec) & set(idx.vectors[doc_idx]))
                tfidf_sim = dot / (q_norm * idx.doc_norms[doc_idx]) if q_norm > 0 and idx.doc_norms[doc_idx] > 0 else 0
                tfidf_norm = tfidf_sim / max_tfidf if max_tfidf > 0 else 0
            else:
                tfidf_sim, tfidf_norm = 0, 0
            src = (meta or {}).get('source', '') or ''
            boost = sum(0.4 for t in tokenize(query) if t in src.lower())
            combined = 0.45 * vec_sim + 0.55 * tfidf_norm + boost
            results.append((combined, vec_sim, tfidf_sim, doc, meta))

    results.sort(reverse=True)
    return results[:topk]

# ── 全局搜索 ─────────────────────────────────────────────────────
def search(query, topk=6):
    collection_order = get_collection_order(query)
    agent = detect_agent(query)
    boost = 1.3 if agent else 1.0

    all_results = []
    for coll in collection_order:
        for combined, vec_sim, tfidf_sim, doc, meta in search_collection(coll, query, topk=topk):
            if agent and coll == AGENT_COLLECTION.get(agent):
                combined *= boost
            all_results.append({
                'doc': doc, 'meta': meta,
                'combined': combined,
                'vector_sim': vec_sim,
                'tfidf_sim': tfidf_sim,
                'source': (meta or {}).get('source', '?'),
                'agent': (meta or {}).get('agent', '?'),
                'collection': coll,
            })

    all_results.sort(key=lambda x: x['combined'], reverse=True)
    return all_results[:topk]

# ── CLI ──────────────────────────────────────────────────────────
if __name__ == '__main__':
    import sys, time
    query = sys.argv[1] if len(sys.argv) > 1 else '狗蛋产品功能'
    agent = detect_agent(query)
    t0 = time.time()
    results = search(query)
    elapsed = time.time() - t0
    note = f" | Agent路由: {agent}→{AGENT_COLLECTION.get(agent,'')}" if agent else ""
    print(f"\n🔍 Semantic Memory: \"{query}\" ({elapsed:.2f}秒){note}")
    print("=" * 60)
    for i, r in enumerate(results):
        print(f"\n【{i+1}】综合:{r['combined']:.3f} | 向量:{r['vector_sim']:.2f} | TF-IDF:{r['tfidf_sim']:.3f}")
        print(f"  [{r['collection']}] {r['source']} ({r['agent']})")
        print(f"  → {r['doc'][:150]}...")
