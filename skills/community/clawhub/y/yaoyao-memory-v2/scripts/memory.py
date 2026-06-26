#!/usr/bin/env python3
"""yaoyao-memory 核心记忆脚本 v2.0 - 全优化版"""
import argparse
import json
import os
import re
import sys
import uuid
import hashlib
from datetime import datetime, timedelta
sys.path.insert(0, str(__file__).rsplit("/", 1)[0])
try:
    from audit import log
except:
    def log(*args, **kwargs): pass  # fallback if audit not available
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import threading
# 向量存储（ChromaDB）
try:
    from vector_store import VectorStore
    _vs = VectorStore()
except:
    _vs = None
try:
    from feature_flag import FeatureFlag
    _ff = FeatureFlag()
except:
    _ff = None
def _is_enabled(flag, default=True):
    """检查feature flag是否启用"""
    if _ff is None:
        return default
    try:
        return _ff.is_enabled(flag)
    except:
        return default
# Embedding缓存(进程内)+ 持久化
_embedding_cache = {}
_embedding_cache_size = 200  # 最多缓存200条
_embedding_verbose = False  # 静默模式（避免每次初始化打印日志）
_embedding_persist_file = Path(__file__).parent.parent / "config" / "embeddings_cache.json"
_embedding_failure_count = 0  # 连续失败计数
_embedding_failure_threshold = 3  # 连续失败3次后暂时禁用
_embedding_last_success = None  # 上次成功时间
# Embedding配置（支持多种Provider）
_embedding_config = None
def _load_embedding_config():
    """加载embedding配置（优先级：llm_config.json > 环境变量 > secrets.env）"""
    global _embedding_config
    if _embedding_config is not None:
        return _embedding_config
    
    config = {
        "api_key": None,
        "endpoint": "https://ai.gitee.com/v1/embeddings",
        "model": "Qwen3-Embedding-8B",
        "dimensions": 1024,
    }
    
    # 1. 从 llm_config.json 加载
    config_file = Path(__file__).parent.parent / "config" / "llm_config.json"
    if config_file.exists():
        try:
            with open(config_file) as f:
                cfg = json.load(f)
            emb = cfg.get("embedding", {})
            if emb.get("api_key"):
                config["api_key"] = emb.get("api_key")
            if emb.get("base_url"):
                config["endpoint"] = emb.get("base_url")
            if emb.get("model"):
                config["model"] = emb.get("model")
            if emb.get("dimensions"):
                config["dimensions"] = emb.get("dimensions")
        except:
            pass
    
    # 2. 从环境变量加载（覆盖）
    if os.environ.get("EMBEDDING_API_KEY"):
        config["api_key"] = os.environ.get("EMBEDDING_API_KEY")
    if os.environ.get("EMBEDDING_API"):
        config["endpoint"] = os.environ.get("EMBEDDING_API")
    if os.environ.get("EMBEDDING_MODEL"):
        config["model"] = os.environ.get("EMBEDDING_MODEL")
    
    # 3. 从 secrets.env 加载（兼容旧配置）
    if not config["api_key"]:
        secrets_file = Path.home() / ".openclaw" / "credentials" / "secrets.env"
        if secrets_file.exists():
            for line in secrets_file.read_text().splitlines():
                if line.startswith("GITEE_EMBED_API_KEY="):
                    config["api_key"] = line.split("=", 1)[1].strip()
                    break
                if line.startswith("EMBEDDING_API_KEY="):
                    config["api_key"] = line.split("=", 1)[1].strip()
                    break
    
    _embedding_config = config
    return config
def _load_embedding_cache():
    """加载持久化的embedding缓存（静默模式）"""
    global _embedding_cache, _embedding_verbose
    if not _embedding_verbose:
        # 静默模式：不打印加载信息
        if _embedding_persist_file.exists():
            try:
                data = json.loads(_embedding_persist_file.read_text())
                _embedding_cache = data
            except:
                pass
        return
    
    # 详细模式
    if _embedding_persist_file.exists():
        try:
            data = json.loads(_embedding_persist_file.read_text())
            _embedding_cache = data
            print(f"[embedding] Loaded {len(_embedding_cache)} cached embeddings")
        except:
            pass
def _save_embedding_cache():
    """保存embedding缓存到磁盘"""
    try:
        _embedding_persist_file.parent.mkdir(parents=True, exist_ok=True)
        _embedding_persist_file.write_text(json.dumps(_embedding_cache))
    except:
        pass
# 启动时加载缓存
_load_embedding_cache()
def _get_embedding(text, model=None, dimensions=None):
    """获取文本embedding向量（带持久化缓存+稳定性方案）"""
    global _embedding_failure_count, _embedding_last_success
    
    if not _is_enabled("memory.vector_search", True):
        return None
    
    # 连续失败后暂时禁用
    if _embedding_failure_count >= _embedding_failure_threshold:
        return None
    
    # 加载配置
    cfg = _load_embedding_config()
    api_key = cfg["api_key"]
    endpoint = cfg["endpoint"]
    default_model = cfg["model"]
    default_dims = cfg["dimensions"]
    
    # 使用传入参数或默认值
    model = model or default_model
    dimensions = dimensions or default_dims
    
    # 检查缓存
    cache_key = f"{model}:{dimensions}:{text}"
    if cache_key in _embedding_cache:
        return _embedding_cache[cache_key]
    
    if not api_key:
        return None
    
    import urllib.request
    import urllib.error
    import time
    data = json.dumps({
        "model": model,
        "input": text,
        "dimensions": dimensions
    }).encode("utf-8")
    
    # 重试机制：最多3次
    for attempt in range(3):
        req = urllib.request.Request(
            endpoint,
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                emb = result.get("data", [{}])[0].get("embedding", None)
                
                # 成功：重置失败计数
                _embedding_failure_count = 0
                _embedding_last_success = time.time()
                
                # 缓存结果（持久化）
                if emb:
                    if len(_embedding_cache) < _embedding_cache_size:
                        _embedding_cache[cache_key] = emb
                    _save_embedding_cache()
                return emb
                
        except urllib.error.HTTPError as e:
            # HTTP错误，不重试
            _embedding_failure_count += 1
            return None
            
        except (urllib.error.URLError, TimeoutError) as e:
            # 网络错误，重试
            if attempt < 2:
                time.sleep(0.5 * (attempt + 1))  # 指数退避
                continue
            else:
                _embedding_failure_count += 1
                return None
                
        except Exception as e:
            _embedding_failure_count += 1
            return None
    
    return None
def _reset_embedding_failures():
    """重置失败计数（手动调用或定时）"""
    global _embedding_failure_count
    _embedding_failure_count = 0
def preheat_embeddings(items, model="Qwen3-Embedding-8B", dimensions=1024):
    """预热embedding缓存 - 为记忆项预计算embeddings"""
    count = 0
    for item in items:
        title = item.get("title", "")
        if title:
            emb = _get_embedding(title, model, dimensions)
            if emb:
                count += 1
    if count > 0:
        _save_embedding_cache()
        print(f"[embedding] Preheated {count} embeddings")
    return count
IMPORTANCE = {"c": "Critical", "h": "High", "n": "Normal", "l": "Low"}
class MemoryCache:
    """多级缓存系统"""
    _cache = {}
    _lock = threading.Lock()
    @classmethod
    def get(cls, key, ttl=60):
        with cls._lock:
            if key in cls._cache:
                entry = cls._cache[key]
                if (datetime.now() - entry["time"]).total_seconds() < ttl:
                    return entry["data"]
                del cls._cache[key]
        return None
    @classmethod
    def set(cls, key, data):
        with cls._lock:
            cls._cache[key] = {"data": data, "time": datetime.now()}
    @classmethod
    def clear(cls):
        with cls._lock:
            cls._cache.clear()
class Memory:
    """记忆系统 - 全优化版"""
    def __init__(self):
        self.ws = Path.home() / ".openclaw" / "workspace"
        self.mem_dir = self.ws / "memory"
        self.meta_file = self.mem_dir / ".meta.json"
        self._meta = self._load_meta()
        self._ensure_wal_mode()  # 自动启用WAL模式
        self._pending_save = False  # 写合并标记
        self.load()
    
    def _ensure_wal_mode(self):
        """确保WAL模式已启用"""
        import sqlite3
        db_path = self.mem_dir / "memory.db"
        if db_path.exists():
            try:
                conn = sqlite3.connect(str(db_path))
                cursor = conn.execute("PRAGMA journal_mode")
                mode = cursor.fetchone()[0]
                if mode.upper() != "WAL":
                    conn.execute("PRAGMA journal_mode=WAL")
                    conn.execute("PRAGMA synchronous=NORMAL")
                    conn.execute("PRAGMA wal_autocheckpoint=1000")
                    conn.commit()
                conn.close()
            except Exception as e:
                pass  # WAL启用失败不影响主流程
    def _load_meta(self):
        if self.meta_file.exists():
            try:
                return json.loads(self.meta_file.read_text(encoding="utf-8"))
            except Exception as e:
                pass  # 损坏的meta文件会被重建
        return {"index": [], "last_load": None, "cache": {}}
    def _save_meta(self, immediate=False):
        """保存元数据（支持写合并）"""
        import time
        if not immediate:
            self._pending_save = True
            # 延迟写入，合并多次修改
            if not hasattr(self, '_save_timer'):
                self._save_timer = time.time()
                # 异步保存（如果已有待保存的，直接返回）
                import threading
                if not hasattr(self, '_save_thread'):
                    self._save_thread = threading.Timer(0.5, self._flush_save)
                    self._save_thread.daemon = True
                    self._save_thread.start()
            return
        
        try:
            self.meta_file.parent.mkdir(parents=True, exist_ok=True)
            self.meta_file.write_text(json.dumps(self._meta, ensure_ascii=False), encoding="utf-8")
            self._pending_save = False
        except:
            pass
    
    def _flush_save(self):
        """flush待保存的修改"""
        if self._pending_save:
            self._save_meta(immediate=True)
    # ========== 自动分类引擎 v5 ==========
    TYPE_PRIORITY = {
        "security": 1, "error": 2, "decision": 3, "preference": 4,
        "learning": 5, "task": 6, "progress": 7,
    }
    IMPORTANCE_PRIORITY = {"Critical": 1, "High": 2, "Low": 3}
    TYPE_PATTERNS = {
        "decision": ["决定采用", "决定用", "采用", "选择", "实施", "配置变更", "迁移到", "切换到", "敲定", "拍板", "决策", "不应该", "不该"],
        "preference": ["喜欢", "偏好", "倾向", "更愿意", "习惯", "不喜欢", "不要", "钟爱", "偏爱"],
        "learning": ["学会", "理解", "发现", "学到", "认识到", "掌握", "了解", "熟悉", "学会了"],
        "task": ["需要做", "需要修复", "计划", "下一步", "待处理", "TODO", "将要做", "待办", "要做", "应该做"],
        "error": ["错误", "失败", "bug", "修复", "异常", "失效", "崩溃", "报错", "严重错误", "严重bug"],
        "progress": ["完成", "达成", "里程碑", "实现", "已成功", "搞定", "结束", "收工", "完成了"],
        "security": ["安全漏洞", "注入漏洞", "安全问题", "安全风险", "泄露", "密码", "密钥", "Token", "权限", "认证", "漏洞", "注入"],
    }
    IMPORTANCE_PATTERNS = {
        "Critical": ["永远记住", "永远不忘", "绝不", "绝对不能", "永久", "致命"],
        "High": ["重要", "关键", "必须", "紧急", "优先", "主要", "重大", "严重"],
        "Low": ["试试", "可能", "随便", "临时", "暂且", "不重要", "不太重要"],
    }
    def _flatten_patterns(self, patterns_dict, priority_dict):
        items = []
        for ptype, words in patterns_dict.items():
            priority = priority_dict.get(ptype, 999)
            for word in words:
                items.append((word, ptype, priority))
        items.sort(key=lambda x: (-len(x[0]), x[2]))
        return items
    def _classify(self, text_lower, patterns_dict, priority_dict):
        for word, ptype, _ in self._flatten_patterns(patterns_dict, priority_dict):
            if word in text_lower:
                return ptype
        return None
    def _auto_classify(self, text):
        text_lower = text.lower()
        mem_type = self._classify(text_lower, self.TYPE_PATTERNS, self.TYPE_PRIORITY) or "info"
        importance = self._classify(text_lower, self.IMPORTANCE_PATTERNS, self.IMPORTANCE_PRIORITY) or "Normal"
        return mem_type, importance
    def load(self, force=False):
        now = datetime.now()
        if not force and self._meta.get("last_load"):
            last = datetime.fromisoformat(self._meta["last_load"])
            if (now - last).total_seconds() < 60:
                return
        self._meta["last_load"] = now.isoformat()
        self._meta["index"] = []
        for f in self.mem_dir.glob("*.md"):
            if f.name == "archive" or f.name.startswith("."):
                continue
            try:
                content = f.read_text(encoding="utf-8")
                for block in re.split(r"\n## ", content):
                    lines = block.split("\n", 1)
                    if len(lines) > 1 and lines[0].strip():
                        title = lines[0].strip()[:50]
                        body = lines[1][:200] if len(lines) > 1 else ""
                        # 自动分类
                        combined = title + " " + body
                        mem_type, importance = self._auto_classify(combined)
                        self._meta["index"].append({
                            "id": str(uuid.uuid4())[:8],
                            "title": title,
                            "type": mem_type,
                            "importance": importance,
                            "file": f.name
                        })
            except:
                pass
        self._save_meta()
    # ========== 搜索核心优化 ==========
    def _vector_search(self, query, limit=3):
        """向量搜索 - 使用真实embedding(带缓存+降级)"""
        # 获取query embedding
        query_emb = _get_embedding(query)
        if not query_emb:
            # 降级到FTS
            return self._fts_search(query, limit)
        # 限制搜索范围:只处理前30项(按相关度预估)
        index = self._meta.get("index", [])[:30]
        results = []
        for item in index:
            title = item.get("title", "")
            if not title:
                continue
            # 简单的相关性预过滤
            q_lower = query.lower()
            title_lower = title.lower()
            if q_lower in title_lower:
                # 精确匹配给予高分
                results.append({"s": title, "score": 0.95, "type": item.get("type", "info")})
                continue
            # 获取标题embedding(慢,只对候选项)
            title_emb = _get_embedding(title)
            if not title_emb:
                continue
            score = self._cosine_sim(query_emb, title_emb)
            if score > 0.5:
                results.append({"s": title, "score": score, "type": item.get("type", "info")})
        # 按分数排序
        results.sort(key=lambda x: -x["score"])
        return results[:limit]
    def _cosine_sim(self, a, b):
        """计算余弦相似度"""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0
    def _fts_search(self, query, limit=3):
        """全文搜索"""
        q_lower = query.lower()
        results = []
        for item in self._meta.get("index", []):
            if q_lower in item.get("title", "").lower():
                results.append({"s": item.get("title", ""), "score": 0.8, "type": item.get("type", "info")})
        return results[:limit]
    def _parallel_search(self, query, limit=3):
        """并行搜索 - 多策略并发"""
        with ThreadPoolExecutor(max_workers=3) as executor:
            v_future = executor.submit(self._vector_search, query, limit)
            f_future = executor.submit(self._fts_search, query, limit)
            v_results = v_future.result()
            f_results = f_future.result()
        return v_results, f_results
    def _rrf_rank(self, results_list, k=60):
        """RRF排名算法"""
        scores = {}
        for results in results_list:
            for i, r in enumerate(results):
                key = r["s"]
                score = scores.get(key, 0) + 1 / (k + i + 1)
                scores[key] = score
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
    def hybrid_search(self, query, limit=3):
        """混合搜索 - 向量+FTS+RRF"""
        cache_key = f"hybrid_{query}_{limit}"
        cached = MemoryCache.get(cache_key, 60)
        if cached:
            return cached
        v_results, f_results = self._parallel_search(query, limit)
        rrf_results = self._rrf_rank([v_results, f_results])
        output = [{"title": title, "score": score} for title, score in rrf_results[:limit]]
        MemoryCache.set(cache_key, output)
        return output
    
    def chroma_hybrid_search(self, query, limit=3):
        """ChromaDB混合搜索 - 本地向量+Gitee API重排序"""
        if _vs is None:
            return self.hybrid_search(query, limit)
        
        cache_key = f"chroma_{query}_{limit}"
        cached = MemoryCache.get(cache_key, 60)
        if cached:
            return cached
        
        # 使用ChromaDB混合搜索
        results = _vs.hybrid_search(query, _get_embedding, n_results=limit)
        
        # 格式化结果
        output = []
        if results.get('ids') and results['ids'][0]:
            for i, doc_id in enumerate(results['ids'][0]):
                output.append({
                    "s": results['documents'][0][i],
                    "score": 1 - results['distances'][0][i] if results.get('distances') else 0,
                    "type": results['metadatas'][0][i].get('type', 'info') if results.get('metadatas') else 'info'
                })
        
        MemoryCache.set(cache_key, output)
        return output
    # ========== 缓存优化 ==========
    def get_cached(self, key):
        """预计算缓存获取"""
        return MemoryCache.get(f"cached_{key}", 300)
    def set_cached(self, key, data):
        """预计算缓存设置"""
        MemoryCache.set(f"cached_{key}", data)
    def clear_cache(self):
        """清理缓存"""
        MemoryCache.clear()
    # ========== LLM增强 ==========
    def rerank_results(self, results, query):
        """重排序 - 基于query权重"""
        if not results:
            return results
        query_words = set(query.lower().split())
        for r in results:
            title_words = set(r.get("title", "").lower().split())
            overlap = len(query_words & title_words)
            r["rerank_score"] = r.get("score", 0.5) * (1 + overlap * 0.1)
        return sorted(results, key=lambda x: x.get("rerank_score", 0), reverse=True)
    def summarize_results(self, results, max_chars=100):
        """结果摘要"""
        if not results:
            return []
        for r in results:
            title = r.get("title", "")
            if len(title) > max_chars:
                r["summary"] = title[:max_chars] + "..."
            else:
                r["summary"] = title
        return results
    # ========== 智能路由 ==========
    # 搜索路由配置 - 关键词集合
    _FTS_KEYWORDS = frozenset([
        # 操作类
        "配置", "设置", "状态", "规则", "推送", "记忆", "用户", "系统", "决策",
        "是什么", "如何", "怎么", "怎样", "多少", "几个", "帮我", "给我", "我想", "我要",
        "请问", "查一下", "找一下", "最近", "今天", "昨天", "明天", "本周", "上周",
        "记录", "日志", "历史", "档案", "信息", "使用", "用法", "命令", "指令",
        "版本", "更新", "升级", "安装", "备份", "恢复", "导出", "导入", "同步",
        "搜索", "查询", "查找", "开启", "关闭", "启用", "禁用",
        "添加", "新增", "创建", "删除", "修改", "编辑", "列表", "清单", "目录",
        "性能", "效率", "速度", "延迟", "吞吐", "找出", "find",
        # 英文
        "config", "setting", "status", "state", "how", "what", "which", "list", "show",
        "get", "set", "add", "remove", "delete", "create", "update", "search", "query",
    ])
    
    _HYBRID_KEYWORDS = frozenset([
        "怎么", "如何", "why", "why", "because", "reason", "原因", "为什么",
        "解释", "说明", "explain", "describe", "分析", "分析", "compare", "比较",
    ])
    
    def route_query(self, query):
        """智能路由 - 判断使用什么搜索策略（优化：frozenset查找）"""
        query_lower = query.lower()
        words = set(query_lower.split())
        
        # 1. FTS关键词命中 → 直接FTS
        if words & self._FTS_KEYWORDS:
            return "fts"
        
        # 2. 短查询+无复杂语义 → FTS
        if len(words) <= 2 and not (words & self._HYBRID_KEYWORDS):
            return "fts"
        
        # 3. 复杂语义 → 混合搜索
        if words & self._HYBRID_KEYWORDS:
            return "hybrid"
        
        # 4. 默认：短词用向量，长词用混合
        return "vector" if len(words) <= 3 else "hybrid"
    def smart_search(self, query, limit=3):
        """智能搜索 - 自动路由 + 模糊后备"""
        route = self.route_query(query)
        if route == "fts":
            results = self._fts_search(query, limit)
        elif route == "vector":
            results = self._vector_search(query, limit)
        else:
            v_results, f_results = self._parallel_search(query, limit)
            results = v_results + f_results
        # 模糊后备:搜索无结果时尝试模糊匹配
        if not results and _is_enabled("search.fuzzy", True):
            results = self._fuzzy_search(query, limit)
        results = self.rerank_results(results, query)
        return self.summarize_results(results[:limit])
    def _fuzzy_search(self, query, limit=3):
        """模糊搜索 - 当精确匹配无结果时后备"""
        q_lower = query.lower()
        results = []
        for item in self._meta.get("index", []):
            title_lower = item.get("title", "").lower()
            # 检查查询的每个字符是否都在标题中出现
            matched = 0
            title_chars = list(title_lower)
            for c in q_lower:
                if c in title_chars:
                    matched += 1
                    title_chars.remove(c)  # 每个字符只用一次
            if matched >= len(q_lower) * 0.5:  # 50%字符匹配即通过
                results.append({
                    "s": item.get("title", ""),
                    "score": matched / len(q_lower) * 0.8,  # 模糊匹配降低分数
                    "type": item.get("type", "info")
                })
        return sorted(results, key=lambda x: -x["score"])[:limit]
    # ========== 学习优化 ==========
    def learn_from_history(self, query, selected_result):
        """从历史中学习 - 记录用户偏好"""
        history_key = "query_history"
        history = self._meta.get("cache", {}).get(history_key, [])
        history.append({
            "query": query,
            "selected": selected_result,
            "timestamp": datetime.now().isoformat()
        })
        # 只保留最近20条
        history = history[-20:]
        self._meta["cache"][history_key] = history
        self._save_meta()
    def deduplicate(self, data):
        """去重 - 基于内容hash"""
        data_hash = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
        existing_hashes = self._meta.get("cache", {}).get("data_hashes", [])
        if data_hash in existing_hashes:
            return False
        existing_hashes.append(data_hash)
        self._meta["cache"]["data_hashes"] = existing_hashes[-100:]
        self._save_meta()
        return True
    # ========== 核心接口 ==========
    def sync_start(self):
        """超轻量会话开始"""
        return {
            "b": "main",
            "t": self._get_type_stats(),
            "n": len(self._meta.get("index", [])),
            "h": self._get_high_count()
        }
    
    def sync_to_chroma(self):
        """同步记忆到ChromaDB向量存储"""
        if _vs is None:
            return {"error": "ChromaDB not available"}
        
        index = self._meta.get("index", [])
        count = _vs.sync_from_memory(index)
        return {"synced": count, "total": len(index)}
    def _get_type_stats(self):
        stats = {}
        for item in self._meta.get("index", []):
            t = item.get("type", "info")
            stats[t] = stats.get(t, 0) + 1
        return stats
    def _get_high_count(self):
        return sum(1 for item in self._meta.get("index", []) if item.get("importance") in ["Critical", "High"])
    def get(self, topic, limit=3):
        """获取记忆"""
        topic_lower = topic.lower()
        results = []
        for item in self._meta.get("index", []):
            if topic_lower in item.get("title", "").lower():
                results.append({
                    "id": item.get("id", ""),
                    "t": item.get("title", ""),
                    "tp": item.get("type", "info")[0].upper(),
                    "i": item.get("importance", "Normal")[0].upper()
                })
                if len(results) >= limit:
                    break
        return {"topic": topic, "mem": results, "total": len(results)}
    def search(self, query, limit=3, method="auto"):
        """搜索 - 支持多种方法(受feature flag控制) + 快速路径"""
        # 快速路径：白名单命令极速响应
        try:
            from optimizer import FastPath, get_perf_monitor
            if FastPath.is_whitelist(query.strip()):
                get_perf_monitor().record_search(0.1, True)  # 记录为缓存命中
                return {
                    "query": query,
                    "results": [],
                    "method": "fast",
                    "total": 0,
                    "fast_response": FastPath.get_fast_response(query.strip())
                }
        except:
            pass
        
        use_vector = _is_enabled("memory.vector_search", True)
        use_hybrid = _is_enabled("search.hybrid", True)
        if method == "auto":
            if not use_vector:
                results = self._fts_search(query, limit)
            elif not use_hybrid:
                results = self.smart_search(query, limit)
            else:
                results = self.smart_search(query, limit)
        elif method == "hybrid":
            results = self.hybrid_search(query, limit) if use_hybrid else self._fts_search(query, limit)
        elif method == "vector":
            results = self._vector_search(query, limit) if use_vector else self._fts_search(query, limit)
        elif method == "parallel":
            v, f = self._parallel_search(query, limit)
            results = v + f if use_vector else f
        else:
            results = self._fts_search(query, limit)
        return {"query": query, "results": results, "method": method, "total": len(results)}
    def stats(self):
        index = self._meta.get("index", [])
        by_type = {}
        by_imp = {"Critical": 0, "High": 0, "Normal": 0, "Low": 0}
        for item in index:
            by_type[item.get("type", "info")] = by_type.get(item.get("type", "info"), 0) + 1
            by_imp[item.get("importance", "Normal")] = by_imp.get(item.get("importance", "Normal"), 0) + 1
        return {"total": len(index), "by_type": by_type, "by_importance": by_imp}
def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("sync-start")
    g = sub.add_parser("get")
    g.add_argument("topic")
    g.add_argument("-l", "--limit", type=int, default=3)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("-l", "--limit", type=int, default=3)
    s.add_argument("-m", "--method", default="auto", choices=["auto", "hybrid", "parallel", "fts"])
    sub.add_parser("stats")
    sub.add_parser("clear-cache")
    args = parser.parse_args()
    if not args.cmd:
        return
    m = Memory()
    if args.cmd == "sync-start":
        print(json.dumps(m.sync_start(), indent=2, ensure_ascii=False))
    elif args.cmd == "get":
        print(json.dumps(m.get(args.topic, args.limit), indent=2, ensure_ascii=False))
    elif args.cmd == "search":
        print(json.dumps(m.search(args.query, args.limit, args.method), indent=2, ensure_ascii=False))
    elif args.cmd == "stats":
        print(json.dumps(m.stats(), indent=2, ensure_ascii=False))
    elif args.cmd == "clear-cache":
        m.clear_cache()
        print(json.dumps({"status": "cache_cleared"}, ensure_ascii=False))
if __name__ == "__main__":
    main()
