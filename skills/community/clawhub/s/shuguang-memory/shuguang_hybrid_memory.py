# -*- coding: utf-8 -*-
"""
曙光混合记忆引擎 v1.0
掠夺来源: memory-lancedb-pro v1.1.0-beta.8
核心技术:
  1. 混合检索: 向量语义 + BM25关键词 (0.7/0.3权重)
  2. Weibull衰减: Core/Working/Peripheral三层生命周期
  3. 自改进治理: 自动提取教训 + WAL集成
"""

import os, json, math, re, hashlib, time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

@dataclass
class MemoryEntry:
    id: str
    text: str
    category: str  # preference|fact|decision|entity|reflection|other
    importance: float  # 0.0-1.0
    timestamp: float
    vector: Optional[List[float]] = None
    scope: str = "global"  # global|agent|project|user
    l0_abstract: str = ""  # 一句话摘要
    l1_overview: str = ""  # 一段话概述
    l2_detail: str = ""    # 完整细节
    access_count: int = 0
    last_access: float = 0.0
    
    def to_dict(self) -> Dict:
        d = asdict(self)
        return d
    
    @staticmethod
    def from_dict(d: Dict) -> "MemoryEntry":
        return MemoryEntry(**d)


class WeibullDecay:
    """
    Weibull衰减模型 — 三层记忆生命周期
    
    来源: memory-lancedb-pro 生命周期管理
    公式: S(t) = exp(-(t/λ)^k)
      t: 记忆年龄(天)
      λ: 特征寿命(半衰期)
      k: 形状参数
    """
    
    TIERS = {
        "core": {"beta": 0.8, "half_life_days": 90, "importance_threshold": 0.8, "access_threshold": 10},
        "working": {"beta": 1.0, "half_life_days": 30, "importance_threshold": 0.4, "access_threshold": 3},
        "peripheral": {"beta": 1.3, "half_life_days": 7, "importance_threshold": 0.0, "access_threshold": 0},
    }
    
    @classmethod
    def compute_strength(cls, entry: MemoryEntry) -> float:
        """计算记忆当前强度 (0.0-1.0)"""
        age_days = (time.time() - entry.timestamp) / 86400
        access_boost = 1 + cls.TIERS["core"]["beta"] * min(entry.access_count / 10, 2.0)
        
        # 确定层级
        tier = cls._classify_tier(entry)
        half_life = cls.TIERS[tier]["half_life_days"]
        
        # Weibull: S(t) = exp(-(t/λ)^k), k=1.5
        k = 1.5
        lambda_val = half_life / (math.log(2) ** (1/k))
        decay = math.exp(-((age_days / lambda_val) ** k))
        
        # 综合: 衰减 × 重要性 × 访问强化
        strength = decay * entry.importance * access_boost
        return min(strength, 1.0)
    
    @classmethod
    def _classify_tier(cls, entry: MemoryEntry) -> str:
        """分类记忆层级"""
        if entry.importance >= cls.TIERS["core"]["importance_threshold"] or \
           entry.access_count >= cls.TIERS["core"]["access_threshold"]:
            return "core"
        elif entry.importance >= cls.TIERS["working"]["importance_threshold"] or \
             entry.access_count >= cls.TIERS["working"]["access_threshold"]:
            return "working"
        return "peripheral"
    
    @classmethod
    def should_forget(cls, entry: MemoryEntry) -> bool:
        """判断是否应该遗忘"""
        strength = cls.compute_strength(entry)
        tier = cls._classify_tier(entry)
        thresholds = {"core": 0.15, "working": 0.10, "peripheral": 0.05}
        return strength < thresholds.get(tier, 0.05)


class BM25Index:
    """
    BM25关键词索引 — 轻量级全文检索
    
    来源: memory-lancedb-pro hybrid retrieval
    无需外部依赖，纯Python实现
    """
    
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: Dict[str, Dict] = {}  # id -> {tokens, length}
        self.idf: Dict[str, float] = {}
        self.avg_doc_len = 0.0
        self.N = 0
    
    def _tokenize(self, text: str) -> List[str]:
        """简单分词：中文按字，英文按词"""
        # 中文：保留中文字符作为token
        chinese = re.findall(r'[\u4e00-\u9fff]', text)
        # 英文：提取单词
        english = re.findall(r'[a-zA-Z]+', text.lower())
        return chinese + english
    
    def add_document(self, doc_id: str, text: str):
        """添加文档到索引"""
        tokens = self._tokenize(text)
        self.documents[doc_id] = {
            "tokens": tokens,
            "length": len(tokens),
            "freq": {}
        }
        for t in tokens:
            self.documents[doc_id]["freq"][t] = self.documents[doc_id]["freq"].get(t, 0) + 1
        self.N = len(self.documents)
        self._update_stats()
    
    def _update_stats(self):
        """更新IDF和平均文档长度"""
        total_len = sum(d["length"] for d in self.documents.values())
        self.avg_doc_len = total_len / max(self.N, 1)
        
        # 计算IDF
        df = {}
        for doc in self.documents.values():
            for token in set(doc["tokens"]):
                df[token] = df.get(token, 0) + 1
        
        for token, freq in df.items():
            self.idf[token] = math.log((self.N - freq + 0.5) / (freq + 0.5) + 1)
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """BM25搜索，返回 (doc_id, score) 列表"""
        tokens = self._tokenize(query)
        scores = {}
        
        for doc_id, doc in self.documents.items():
            score = 0.0
            for token in tokens:
                if token not in doc["freq"]:
                    continue
                idf = self.idf.get(token, 0)
                tf = doc["freq"][token]
                denom = tf + self.k1 * (1 - self.b + self.b * doc["length"] / max(self.avg_doc_len, 1))
                score += idf * (tf * (self.k1 + 1)) / max(denom, 1e-6)
            scores[doc_id] = score
        
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]


class HybridMemoryEngine:
    """
    曙光混合记忆引擎
    
    结合向量语义检索 + BM25关键词检索 + Weibull衰减 + 三层分级
    """
    
    VECTOR_WEIGHT = 0.7
    BM25_WEIGHT = 0.3
    MIN_SCORE = 0.3
    HARD_MIN_SCORE = 0.35
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace", "memory", "hybrid")
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self.entries: Dict[str, MemoryEntry] = {}
        self.bm25 = BM25Index()
        self.decay = WeibullDecay()
        
        self._load()
    
    def _load(self):
        """从磁盘加载记忆"""
        path = os.path.join(self.data_dir, "memory_store.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for d in data:
                    entry = MemoryEntry.from_dict(d)
                    self.entries[entry.id] = entry
                    self.bm25.add_document(entry.id, entry.text)
    
    def _save(self):
        """保存到磁盘"""
        path = os.path.join(self.data_dir, "memory_store.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.entries.values()], f, ensure_ascii=False, indent=2)
    
    def _hash_text(self, text: str) -> str:
        """生成记忆ID"""
        return hashlib.md5(f"{text}:{time.time()}".encode()).hexdigest()[:16]
    
    def _simple_vectorize(self, text: str, dim: int = 384) -> List[float]:
        """
        简单向量生成（无外部embedding模型时）
        使用字符级n-gram哈希作为fallback
        
        生产环境应替换为: jina-embeddings-v5-text-small / text-embedding-3-small
        """
        # 基于字符哈希的简单向量（用于演示和fallback）
        vec = [0.0] * dim
        tokens = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z]+', text)
        for i, token in enumerate(tokens[:50]):
            h = int(hashlib.md5(token.encode()).hexdigest(), 16)
            for j in range(dim):
                vec[j] += math.sin(h * (j + 1) / dim) * (1.0 / (i + 1))
        # 归一化
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """计算余弦相似度"""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        return dot / (norm_a * norm_b + 1e-6)
    
    def store(self, text: str, category: str = "fact", importance: float = 0.5,
              scope: str = "global", vector: Optional[List[float]] = None) -> str:
        """
        存储记忆
        
        自动执行:
          1. 生成ID和向量
          2. 提取L0/L1/L2摘要（简化版）
          3. 加入BM25索引
          4. WAL写入磁盘
        """
        entry_id = self._hash_text(text)
        now = time.time()
        
        # 简单摘要提取（生产环境用LLM）
        l0 = text[:50] + "..." if len(text) > 50 else text
        l1 = text[:200] + "..." if len(text) > 200 else text
        
        if vector is None:
            vector = self._simple_vectorize(text)
        
        entry = MemoryEntry(
            id=entry_id,
            text=text,
            category=category,
            importance=importance,
            timestamp=now,
            vector=vector,
            scope=scope,
            l0_abstract=l0,
            l1_overview=l1,
            l2_detail=text,
            access_count=0,
            last_access=now
        )
        
        self.entries[entry_id] = entry
        self.bm25.add_document(entry_id, text)
        self._save()
        
        return entry_id
    
    def recall(self, query: str, top_k: int = 5, scope: Optional[str] = None) -> List[Dict]:
        """
        混合检索回忆
        
        流程:
          1. 向量搜索 (语义相似度)
          2. BM25搜索 (关键词匹配)
          3. 分数融合 (0.7*向量 + 0.3*BM25)
          4. Weibull衰减加权
          5. 过滤低分记忆
        """
        query_vec = self._simple_vectorize(query)
        
        # 1. 向量搜索
        vector_scores = {}
        for eid, entry in self.entries.items():
            if scope and entry.scope != scope:
                continue
            if entry.vector:
                sim = self._cosine_similarity(query_vec, entry.vector)
                vector_scores[eid] = sim
        
        # 2. BM25搜索
        bm25_results = self.bm25.search(query, top_k=max(top_k * 3, 20))
        bm25_scores = {eid: score for eid, score in bm25_results}
        
        # 3. 分数融合 + 衰减加权
        combined = {}
        all_ids = set(vector_scores.keys()) | set(bm25_scores.keys())
        
        for eid in all_ids:
            entry = self.entries.get(eid)
            if not entry:
                continue
            
            v_score = vector_scores.get(eid, 0.0)
            b_score = bm25_scores.get(eid, 0.0)
            
            # 归一化BM25分数
            max_bm25 = max(bm25_scores.values()) if bm25_scores else 1.0
            b_norm = b_score / max_bm25 if max_bm25 > 0 else 0.0
            
            # 混合融合
            fused = self.VECTOR_WEIGHT * v_score + self.BM25_WEIGHT * b_norm
            
            # Weibull衰减加权
            strength = self.decay.compute_strength(entry)
            final_score = fused * strength
            
            combined[eid] = final_score
        
        # 4. 排序过滤
        results = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        filtered = [(eid, score) for eid, score in results if score >= self.MIN_SCORE]
        
        # 更新访问计数
        output = []
        for eid, score in filtered[:top_k]:
            entry = self.entries[eid]
            entry.access_count += 1
            entry.last_access = time.time()
            output.append({
                "id": eid,
                "text": entry.text,
                "category": entry.category,
                "importance": entry.importance,
                "score": round(score, 4),
                "tier": self.decay._classify_tier(entry),
                "strength": round(self.decay.compute_strength(entry), 4),
                "timestamp": entry.timestamp
            })
        
        self._save()
        return output
    
    def forget(self, entry_id: str) -> bool:
        """主动遗忘某条记忆"""
        if entry_id in self.entries:
            del self.entries[entry_id]
            self._save()
            return True
        return False
    
    def cleanup(self) -> int:
        """
        清理过期记忆
        返回清理数量
        """
        to_remove = []
        for eid, entry in self.entries.items():
            if self.decay.should_forget(entry):
                to_remove.append(eid)
        
        for eid in to_remove:
            del self.entries[eid]
        
        if to_remove:
            self._save()
        
        return len(to_remove)
    
    def stats(self) -> Dict:
        """统计信息"""
        tiers = {"core": 0, "working": 0, "peripheral": 0}
        categories = {}
        for entry in self.entries.values():
            tier = self.decay._classify_tier(entry)
            tiers[tier] += 1
            categories[entry.category] = categories.get(entry.category, 0) + 1
        
        return {
            "total": len(self.entries),
            "tiers": tiers,
            "categories": categories,
            "avg_strength": round(sum(self.decay.compute_strength(e) for e in self.entries.values()) / max(len(self.entries), 1), 4),
            "data_dir": self.data_dir
        }


class SelfImprovementGovernance:
    """
    曙光自改进治理系统
    
    掠夺来源: memory-lancedb-pro 自改进治理
    核心:
      - 自动从失败中提取教训
      - LEARNINGS.md / ERRORS.md 自动治理
      - WAL协议集成 (先写再答)
    """
    
    def __init__(self, workspace_dir: str = None):
        if workspace_dir is None:
            workspace_dir = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace")
        self.workspace = workspace_dir
        os.makedirs(os.path.join(workspace_dir, "memory"), exist_ok=True)
    
    def _get_path(self, filename: str) -> str:
        return os.path.join(self.workspace, "memory", filename)
    
    def log_error(self, context: str, error: str, attempted_solutions: List[str], 
                  final_solution: str = ""):
        """
        记录错误到 ERRORS.md
        
        触发条件:
          - 工具调用失败
          - 用户纠正
          - 预期输出不匹配
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = f"""
## [{timestamp}] {context}
**错误**: {error}
**尝试方案**:
"""
        for i, sol in enumerate(attempted_solutions, 1):
            entry += f"  {i}. {sol}\n"
        
        entry += f"**最终方案**: {final_solution if final_solution else '未解决'}\n\n"
        
        path = self._get_path("ERRORS.md")
        with open(path, "a", encoding="utf-8") as f:
            f.write(entry)
        
        return True
    
    def log_learning(self, trigger: str, insight: str, action: str, 
                     category: str = "general"):
        """
        记录学习到 LEARNINGS.md
        
        触发条件:
          - 用户明确教导
          - 成功解决困难问题
          - 发现新工具/方法
          - 修正错误后
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = f"""
## [{timestamp}] {category.upper()}: {trigger}
**触发**: {trigger}
**洞察**: {insight}
**行动**: {action}
**验证**: [待验证/已验证/持续观察]

"""
        
        path = self._get_path("LEARNINGS.md")
        with open(path, "a", encoding="utf-8") as f:
            f.write(entry)
        
        # 同时存入混合记忆引擎
        engine = HybridMemoryEngine()
        engine.store(
            text=f"[{category}] {trigger}: {insight} → {action}",
            category="reflection",
            importance=0.85,
            scope="global"
        )
        
        return True
    
    def wal_sync(self, fact_type: str, content: str, target_file: str = "session-state.json"):
        """
        WAL协议同步
        
        触发时:
          1. 写入目标文件
          2. 记录到learning日志
          3. 存入混合记忆
        
        fact_type: preference|decision|correction|fact|entity
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. 更新学习日志
        self.log_learning(
            trigger=f"WAL:{fact_type}",
            insight=content,
            action=f"已同步到 {target_file}",
            category="wal"
        )
        
        # 2. 存入混合记忆
        engine = HybridMemoryEngine()
        engine.store(
            text=f"[{timestamp}] {fact_type}: {content}",
            category=fact_type if fact_type in ["preference","fact","decision","entity"] else "other",
            importance=0.9 if fact_type in ["preference", "decision"] else 0.7,
            scope="global"
        )
        
        return True
    
    def review_and_extract(self, period: str = "daily") -> List[Dict]:
        """
        定期审查提取可复用模式
        
        从 LEARNINGS.md + ERRORS.md 中提取可复用技能
        返回待结晶的技能列表
        """
        learnings_path = self._get_path("LEARNINGS.md")
        errors_path = self._get_path("ERRORS.md")
        
        patterns = []
        
        # 读取LEARNINGS
        if os.path.exists(learnings_path):
            with open(learnings_path, "r", encoding="utf-8") as f:
                content = f.read()
            # 简单提取：找重复出现的insight模式
            insights = re.findall(r'\*\*洞察\*\*: (.+)', content)
            from collections import Counter
            freq = Counter(insights)
            for insight, count in freq.most_common(5):
                if count >= 2:
                    patterns.append({
                        "type": "pattern",
                        "content": insight,
                        "frequency": count,
                        "source": "LEARNINGS.md"
                    })
        
        # 读取ERRORS
        if os.path.exists(errors_path):
            with open(errors_path, "r", encoding="utf-8") as f:
                content = f.read()
            # 提取常见错误模式
            errors = re.findall(r'\*\*错误\*\*: (.+)', content)
            from collections import Counter
            freq = Counter(errors)
            for err, count in freq.most_common(3):
                if count >= 2:
                    patterns.append({
                        "type": "anti-pattern",
                        "content": err,
                        "frequency": count,
                        "source": "ERRORS.md"
                    })
        
        return patterns


# === 便捷函数 ===

def store_memory(text: str, category: str = "fact", importance: float = 0.5, 
                 scope: str = "global") -> str:
    """便捷存储记忆"""
    engine = HybridMemoryEngine()
    return engine.store(text, category, importance, scope)

def recall_memory(query: str, top_k: int = 5) -> List[Dict]:
    """便捷检索记忆"""
    engine = HybridMemoryEngine()
    return engine.recall(query, top_k)

def log_learning(trigger: str, insight: str, action: str, category: str = "general"):
    """便捷记录学习"""
    gov = SelfImprovementGovernance()
    return gov.log_learning(trigger, insight, action, category)

def wal_log(fact_type: str, content: str):
    """便捷WAL记录"""
    gov = SelfImprovementGovernance()
    return gov.wal_sync(fact_type, content)


if __name__ == "__main__":
    # 自测
    print("[OK] 曙光混合记忆引擎加载成功")
    print(f"[INFO] 数据目录: {os.path.join(os.path.expanduser('~'), '.openclaw', 'workspace', 'memory', 'hybrid')}")
    
    # 测试存储
    engine = HybridMemoryEngine()
    eid = engine.store("曙光使用双策略V2.5进行股票选股", "fact", 0.9)
    print(f"[STORE] {eid}")
    
    # 测试检索
    results = engine.recall("股票选股策略", top_k=3)
    print(f"[RECALL] 找到 {len(results)} 条")
    for r in results:
        print(f"  - {r['text'][:40]}... (score={r['score']}, tier={r['tier']})")
    
    # 测试统计
    stats = engine.stats()
    print(f"[STATS] 总记忆: {stats['total']}, 层级: {stats['tiers']}")
    
    print("[OK] 所有测试通过")
