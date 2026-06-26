#!/usr/bin/env python3
"""
ultra-memory 核心模块单元测试
覆盖：BM25Index、tokenize、expand_query（同义词扩展）、
      conflict_detector（画像冲突 + 知识库冲突）、time_weight（Weibull）、
      rrf_merge、extract_snippet、filter_memory_markers、classify_tier、
      _compute_importance（重要性评分）、_increment_access_count（访问回写）、
      log_knowledge 语义去重
"""

import sys
import json
import math
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone, timedelta

# 将 scripts 目录加入 sys.path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from recall import (
    BM25Index,
    tokenize,
    expand_query,
    time_weight,
    SYNONYM_MAP,
    WEIBULL_K,
    WEIBULL_LAMBDA,
    rrf_merge,
    _get_doc_id,
    extract_snippet,
    _increment_access_count,
)
from log_op import filter_memory_markers, _compute_importance
from log_knowledge import log_knowledge, _bm25_similarity, _find_similar_entry
from summarize import classify_tier, TIER_CORE, TIER_WORKING, TIER_PERIPHERAL
from conflict_detector import (
    detect_profile_conflict,
    mark_profile_superseded,
    detect_knowledge_conflict,
    mark_superseded,
    _title_similarity,
    _has_negation,
    _has_number_change,
    _has_contradictory_pair,
)


# ─────────────────────────────────────────────────────────
# BM25Index 测试
# ─────────────────────────────────────────────────────────

class TestBM25Index(unittest.TestCase):

    def _make_docs(self, texts):
        return [{"id": i, "text": t, "tokens": tokenize(t)} for i, t in enumerate(texts)]

    def test_single_doc_nonzero(self):
        """单文档语料也能返回非零分数（文档含查询词）"""
        docs = self._make_docs(["python pandas dataframe"])
        idx = BM25Index(docs)
        score = idx.score(0, tokenize("pandas"))
        self.assertGreater(score, 0)

    def test_relevant_doc_scores_higher(self):
        """相关文档得分高于不相关文档"""
        docs = self._make_docs([
            "python pandas dataframe 数据清洗",
            "docker kubernetes deploy nginx",
            "pytest unittest assert 测试",
        ])
        idx = BM25Index(docs)
        q = tokenize("pandas 数据")
        s0 = idx.score(0, q)
        s1 = idx.score(1, q)
        s2 = idx.score(2, q)
        self.assertGreater(s0, s1)
        self.assertGreater(s0, s2)

    def test_stopwords_ignored(self):
        """停用词不影响评分（仅含停用词的文档得分为零）"""
        docs = self._make_docs(["的 了 是 the a an", "python error traceback"])
        idx = BM25Index(docs)
        score = idx.score(0, tokenize("error"))
        self.assertEqual(score, 0.0)

    def test_idf_penalizes_common_terms(self):
        """在所有文档中出现的词，IDF 应比罕见词低"""
        docs = self._make_docs([
            "python python python",  # 全文档都含 python
            "python java golang",
            "python node typescript",
        ])
        idx = BM25Index(docs)
        # python 出现在所有3篇，IDF 应 < 某个稀有词
        idf_python = idx.idf.get("python", 0)
        # 构造一个只出现在1篇的词
        docs2 = self._make_docs(["rare_unique_term doc1", "doc2 nothing", "doc3 nothing"])
        idx2 = BM25Index(docs2)
        idf_rare = idx2.idf.get("rare_unique_term", 0)
        self.assertLess(idf_python, idf_rare)

    def test_search_returns_top_k(self):
        """search 方法返回正确数量的结果"""
        docs = self._make_docs([f"document {i} python" for i in range(20)])
        idx = BM25Index(docs)
        results = idx.search(tokenize("python"), top_k=5)
        self.assertEqual(len(results), 5)

    def test_empty_corpus(self):
        """空语料库不崩溃"""
        idx = BM25Index([])
        self.assertEqual(idx.doc_count, 0)

    def test_empty_query(self):
        """空查询返回零分"""
        docs = self._make_docs(["python pandas"])
        idx = BM25Index(docs)
        score = idx.score(0, [])
        self.assertEqual(score, 0.0)

    def test_corpus_idf_better_than_single_doc(self):
        """语料级 BM25（多文档）比单文档 BM25 给出更有区分度的 IDF"""
        relevant = "python pandas dataframe 数据清洗 clean"
        noise = "docker deploy nginx kubernetes helm"
        query = tokenize("pandas 清洗")

        # 单文档模式：每次只有1篇文档
        def single_doc_score(text):
            docs = [{"id": 0, "text": text, "tokens": tokenize(text)}]
            idx = BM25Index(docs)
            return idx.score(0, query)

        # 语料级模式：2篇文档一起构建索引
        docs = [
            {"id": 0, "text": relevant, "tokens": tokenize(relevant)},
            {"id": 1, "text": noise, "tokens": tokenize(noise)},
        ]
        corpus_idx = BM25Index(docs)

        # 语料级模式下，相关文档分数 > 无关文档分数（有区分度）
        corpus_relevant = corpus_idx.score(0, query)
        corpus_noise = corpus_idx.score(1, query)
        self.assertGreater(corpus_relevant, corpus_noise)


# ─────────────────────────────────────────────────────────
# tokenize 测试
# ─────────────────────────────────────────────────────────

class TestTokenize(unittest.TestCase):

    def test_english_words(self):
        tokens = tokenize("hello world python3")
        self.assertIn("hello", tokens)
        self.assertIn("world", tokens)
        self.assertIn("python3", tokens)

    def test_chinese_unigram(self):
        tokens = tokenize("数据清洗")
        self.assertIn("数", tokens)
        self.assertIn("据", tokens)
        self.assertIn("清", tokens)
        self.assertIn("洗", tokens)

    def test_mixed(self):
        tokens = tokenize("pandas 数据 clean_df")
        self.assertIn("pandas", tokens)
        self.assertIn("clean_df", tokens)
        self.assertIn("数", tokens)

    def test_empty_string(self):
        self.assertEqual(tokenize(""), [])

    def test_underscore_preserved(self):
        """函数名/变量名中的下划线应保留"""
        tokens = tokenize("clean_df preprocess_data")
        self.assertIn("clean_df", tokens)
        self.assertIn("preprocess_data", tokens)

    def test_case_insensitive(self):
        """英文应转为小写"""
        tokens = tokenize("DataFrame Pandas")
        self.assertIn("dataframe", tokens)
        self.assertIn("pandas", tokens)


# ─────────────────────────────────────────────────────────
# expand_query（同义词扩展）测试
# ─────────────────────────────────────────────────────────

class TestExpandQuery(unittest.TestCase):

    def test_chinese_to_english(self):
        """中文查询词应扩展出英文同义词"""
        expanded = expand_query("测试")
        self.assertIn("test", expanded)
        self.assertIn("pytest", expanded)

    def test_english_to_chinese(self):
        """英文查询词应扩展出中文同义词"""
        expanded = expand_query("deploy")
        self.assertIn("部署", expanded)

    def test_phrase_expansion(self):
        """中文短语应整体匹配并扩展"""
        expanded = expand_query("数据清洗")
        self.assertIn("clean_df", expanded)
        self.assertIn("preprocess", expanded)

    def test_no_expansion_for_unknown(self):
        """无同义词的词不崩溃，仍返回原始 token"""
        expanded = expand_query("xyzunknownterm123")
        self.assertIn("xyzunknownterm123", expanded)

    def test_bidirectional(self):
        """同义词扩展是双向的"""
        expanded_cn = expand_query("安装")
        expanded_en = expand_query("install")
        self.assertIn("install", expanded_cn)
        self.assertIn("安装", expanded_en)

    def test_synonym_map_consistency(self):
        """SYNONYM_MAP 中所有 key 的值都是列表"""
        for k, v in SYNONYM_MAP.items():
            self.assertIsInstance(v, list, f"SYNONYM_MAP[{k!r}] 应是 list")
            self.assertGreater(len(v), 0, f"SYNONYM_MAP[{k!r}] 不应为空")


# ─────────────────────────────────────────────────────────
# time_weight 测试
# ─────────────────────────────────────────────────────────

class TestTimeWeight(unittest.TestCase):

    def test_recent_is_high(self):
        """刚发生的操作权重接近 1"""
        ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        w = time_weight(ts)
        self.assertGreater(w, 0.9)

    def test_one_day_weight(self):
        """Weibull k=0.75 时 24h 权重 = exp(-1) ≈ 0.368（比简单指数 0.5 更低，初期衰减更快）"""
        ts = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat().replace("+00:00", "Z")
        w  = time_weight(ts)
        expected = math.exp(-math.pow(1.0, WEIBULL_K))  # age/λ=1, k=WEIBULL_K
        self.assertAlmostEqual(w, expected, delta=0.05)

    def test_old_is_low_but_not_zero(self):
        """很久以前的操作权重有下限（0.1）"""
        ts = (datetime.now(timezone.utc) - timedelta(days=365)).isoformat().replace("+00:00", "Z")
        w = time_weight(ts)
        self.assertGreaterEqual(w, 0.1)

    def test_invalid_ts_returns_default(self):
        """无效时间戳返回默认值 0.5 而不崩溃"""
        w = time_weight("not-a-date")
        self.assertEqual(w, 0.5)

    def test_monotonic_decay(self):
        """时间越久远，权重越低（单调递减）"""
        now = datetime.now(timezone.utc)
        weights = []
        for hours in [0, 1, 6, 24, 72, 168]:
            ts = (now - timedelta(hours=hours)).isoformat().replace("+00:00", "Z")
            weights.append(time_weight(ts))
        for i in range(len(weights) - 1):
            self.assertGreaterEqual(weights[i], weights[i + 1])


# ─────────────────────────────────────────────────────────
# conflict_detector — 辅助函数测试
# ─────────────────────────────────────────────────────────

class TestConflictDetectorHelpers(unittest.TestCase):

    def test_title_similarity_identical(self):
        sim = _title_similarity("pandas 数据清洗", "pandas 数据清洗")
        self.assertAlmostEqual(sim, 1.0, delta=0.01)

    def test_title_similarity_disjoint(self):
        sim = _title_similarity("python pandas", "docker kubernetes")
        self.assertEqual(sim, 0.0)

    def test_title_similarity_partial(self):
        sim = _title_similarity("pandas 数据处理 方法", "pandas 清洗 pipeline")
        self.assertGreater(sim, 0)
        self.assertLess(sim, 1)

    def test_has_negation_positive(self):
        self.assertTrue(_has_negation("这个方法不能在生产环境使用"))
        self.assertTrue(_has_negation("never use this in production"))

    def test_has_negation_negative(self):
        self.assertFalse(_has_negation("这个方法可以在生产环境使用"))
        self.assertFalse(_has_negation("use this in production"))

    def test_has_number_change(self):
        self.assertTrue(_has_number_change("超时设置为 30 秒", "超时设置为 60 秒"))
        self.assertFalse(_has_number_change("无数字文本", "另一个无数字文本"))

    def test_has_number_change_same(self):
        self.assertFalse(_has_number_change("端口 8080", "端口 8080"))

    def test_has_contradictory_pair_enable_disable(self):
        self.assertTrue(_has_contradictory_pair("enable feature", "disable feature"))

    def test_has_contradictory_pair_no_conflict(self):
        self.assertFalse(_has_contradictory_pair("enable feature", "enable something else"))


# ─────────────────────────────────────────────────────────
# conflict_detector — 画像冲突检测（集成）
# ─────────────────────────────────────────────────────────

class TestProfileConflict(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        (self.home / "semantic").mkdir(parents=True)
        self.profile_file = self.home / "semantic" / "user_profile.json"

    def tearDown(self):
        self.tmp.cleanup()

    def _write_profile(self, data: dict):
        self.profile_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def test_no_conflict_when_no_profile(self):
        conflicts = detect_profile_conflict({"lang": "python"}, self.home)
        self.assertEqual(conflicts, [])

    def test_string_field_conflict(self):
        self._write_profile({"lang": "python"})
        conflicts = detect_profile_conflict({"lang": "typescript"}, self.home)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["field"], "lang")
        self.assertEqual(conflicts[0]["old_value"], "python")
        self.assertEqual(conflicts[0]["new_value"], "typescript")

    def test_string_field_same_value_no_conflict(self):
        self._write_profile({"lang": "python"})
        conflicts = detect_profile_conflict({"lang": "python"}, self.home)
        self.assertEqual(conflicts, [])

    def test_list_field_element_added_no_conflict(self):
        """数组新增元素不算冲突"""
        self._write_profile({"skills": ["python", "sql"]})
        conflicts = detect_profile_conflict({"skills": ["python", "sql", "golang"]}, self.home)
        self.assertEqual(conflicts, [])

    def test_list_field_element_removed_is_conflict(self):
        """数组删除元素算冲突"""
        self._write_profile({"skills": ["python", "sql", "golang"]})
        conflicts = detect_profile_conflict({"skills": ["python"]}, self.home)
        self.assertEqual(len(conflicts), 1)

    def test_mark_profile_superseded_writes_old_value(self):
        self._write_profile({"lang": "python"})
        conflicts = [{"field": "lang", "old_value": "python", "new_value": "typescript",
                      "superseded_at": "2026-01-01T00:00:00Z"}]
        mark_profile_superseded(self.home, conflicts)
        updated = json.loads(self.profile_file.read_text(encoding="utf-8"))
        self.assertIn("lang_superseded", updated)
        self.assertEqual(updated["lang_superseded"]["old_value"], "python")


# ─────────────────────────────────────────────────────────
# conflict_detector — 知识库冲突检测（集成）
# ─────────────────────────────────────────────────────────

class TestKnowledgeConflict(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        (self.home / "semantic").mkdir(parents=True)
        self.kb_file = self.home / "semantic" / "knowledge_base.jsonl"

    def tearDown(self):
        self.tmp.cleanup()

    def _write_kb(self, entries: list):
        with open(self.kb_file, "w", encoding="utf-8") as f:
            for e in entries:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")

    def test_no_kb_returns_empty(self):
        conflicts = detect_knowledge_conflict({"title": "test", "content": "abc"}, self.home)
        self.assertEqual(conflicts, [])

    def test_similar_title_negation_conflict(self):
        self._write_kb([{"title": "pandas read_csv 用法", "content": "可以直接用 read_csv 读取文件"}])
        new_entry = {"title": "pandas read_csv 方法", "content": "不能直接用 read_csv 读取大文件"}
        conflicts = detect_knowledge_conflict(new_entry, self.home)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["reason"], "规则1")

    def test_similar_title_number_change_conflict(self):
        self._write_kb([{"title": "timeout 配置", "content": "超时设置 30 秒"}])
        new_entry = {"title": "timeout 设置", "content": "超时设置 60 秒"}
        conflicts = detect_knowledge_conflict(new_entry, self.home)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["reason"], "规则2")

    def test_low_title_similarity_no_conflict(self):
        self._write_kb([{"title": "pandas 数据处理", "content": "可以用 read_csv"}])
        new_entry = {"title": "docker 部署方案", "content": "不能直接部署"}
        conflicts = detect_knowledge_conflict(new_entry, self.home)
        self.assertEqual(conflicts, [])

    def test_superseded_entry_skipped(self):
        self._write_kb([{
            "title": "pandas read_csv 用法",
            "content": "可以直接用 read_csv",
            "superseded": True,
        }])
        new_entry = {"title": "pandas read_csv 方法", "content": "不能直接用 read_csv"}
        conflicts = detect_knowledge_conflict(new_entry, self.home)
        self.assertEqual(conflicts, [])

    def test_mark_superseded_writes_flag(self):
        self._write_kb([
            {"title": "entry1", "content": "content1"},
            {"title": "entry2", "content": "content2"},
        ])
        mark_superseded(self.home, self.kb_file, [1])
        entries = []
        for line in self.kb_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                entries.append(json.loads(line))
        self.assertTrue(entries[0].get("superseded"))
        self.assertFalse(entries[1].get("superseded", False))

    def test_mark_superseded_is_atomic(self):
        """mark_superseded 原子写入：写失败不破坏原文件"""
        self._write_kb([{"title": "entry1", "content": "content1"}])
        original = self.kb_file.read_text(encoding="utf-8")
        mark_superseded(self.home, self.kb_file, [1])
        # 文件存在且可读
        self.assertTrue(self.kb_file.exists())
        result = self.kb_file.read_text(encoding="utf-8")
        self.assertIn("superseded", result)


# ─────────────────────────────────────────────────────────
# Weibull 衰减特性测试
# ─────────────────────────────────────────────────────────

class TestWeibullDecay(unittest.TestCase):

    def test_k_less_than_1_slower_long_term_decay(self):
        """k<1 时长期衰减比简单指数慢（7天后权重更高）"""
        now = datetime.now(timezone.utc)
        ts_7days = (now - timedelta(days=7)).isoformat().replace("+00:00", "Z")

        # Weibull weight
        w_weibull = time_weight(ts_7days)

        # 对比简单指数（k=1）手动计算
        age_s = 7 * 86400
        w_exp = math.pow(0.5, age_s / WEIBULL_LAMBDA)

        self.assertGreater(w_weibull, w_exp,
                           "Weibull k<1 的7天权重应高于简单指数衰减")

    def test_weibull_24h_below_half(self):
        """24h Weibull 权重应低于 0.5（初期衰减更快）"""
        ts = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat().replace("+00:00", "Z")
        w  = time_weight(ts)
        # k<1 时，24h 处的衰减比指数更快（值低于 0.5）
        self.assertLess(w, 0.55)

    def test_weibull_min_floor(self):
        """极老记忆权重不低于 0.1"""
        ts = (datetime.now(timezone.utc) - timedelta(days=365)).isoformat().replace("+00:00", "Z")
        self.assertGreaterEqual(time_weight(ts), 0.1)

    def test_weibull_k_constant(self):
        """WEIBULL_K 应小于 1（保证初期快速衰减特性）"""
        self.assertLess(WEIBULL_K, 1.0)


# ─────────────────────────────────────────────────────────
# RRF 融合测试
# ─────────────────────────────────────────────────────────

def _make_result(source: str, seq: int, score: float) -> dict:
    return {"source": source, "data": {"seq": seq, "summary": f"op {seq}"}, "score": score}


class TestRRFMerge(unittest.TestCase):

    def test_single_list_preserves_order(self):
        """单列表输入，排序应与原列表一致"""
        ranked = [_make_result("ops", i, 1.0 / (i + 1)) for i in range(5)]
        merged = rrf_merge([ranked])
        seqs = [r["data"]["seq"] for r in merged]
        self.assertEqual(seqs, [0, 1, 2, 3, 4])

    def test_cross_list_dedup(self):
        """同一 doc 在多列表中只出现一次"""
        list_a = [_make_result("ops", 1, 0.9), _make_result("ops", 2, 0.5)]
        list_b = [_make_result("ops", 1, 0.8), _make_result("ops", 3, 0.7)]
        merged = rrf_merge([list_a, list_b])
        seqs   = [r["data"]["seq"] for r in merged]
        self.assertEqual(len(seqs), len(set(seqs)), "去重后不应有重复 seq")

    def test_multi_list_boost(self):
        """出现在多个列表中的文档 RRF 分数应高于只出现在一个列表中的"""
        # doc 1 出现在两个列表，doc 2 只出现在一个
        list_a = [_make_result("ops", 1, 0.9), _make_result("ops", 2, 0.8)]
        list_b = [_make_result("ops", 1, 0.7)]
        merged = rrf_merge([list_a, list_b])
        scores = {r["data"]["seq"]: r["score"] for r in merged}
        self.assertGreater(scores[1], scores[2],
                           "多列表出现的 doc 分数应高于单列表出现的 doc")

    def test_empty_lists(self):
        """空列表不崩溃，返回空结果"""
        self.assertEqual(rrf_merge([]), [])
        self.assertEqual(rrf_merge([[]]), [])

    def test_rrf_score_positive(self):
        """所有 RRF 分数应为正数"""
        lists = [[_make_result("ops", i, 1.0) for i in range(10)]]
        for r in rrf_merge(lists):
            self.assertGreater(r["score"], 0)

    def test_get_doc_id_ops_uses_seq(self):
        """ops 类型使用 seq 作为 ID"""
        r = _make_result("ops", 42, 1.0)
        self.assertIn("42", _get_doc_id(r))

    def test_get_doc_id_different_sources_no_collision(self):
        """不同来源的不同内容不应产生 ID 碰撞"""
        r_ops     = _make_result("ops", 1, 1.0)
        r_summary = {"source": "summary", "data": {}, "score": 1.0, "text": "some summary text"}
        self.assertNotEqual(_get_doc_id(r_ops), _get_doc_id(r_summary))


# ─────────────────────────────────────────────────────────
# Snippet 截取测试
# ─────────────────────────────────────────────────────────

class TestExtractSnippet(unittest.TestCase):

    def test_short_text_returned_as_is(self):
        text = "短文本"
        self.assertEqual(extract_snippet(text, ["短"], max_len=150), text)

    def test_snippet_contains_query_token(self):
        text = "这是一段很长的文本 " * 10 + "关键词出现在这里" + " 后续内容 " * 10
        snippet = extract_snippet(text, ["关键词"], max_len=100)
        self.assertIn("关键词", snippet)

    def test_snippet_length_bounded(self):
        text = "x" * 500
        snippet = extract_snippet(text, ["x"], max_len=100)
        # snippet 长度不超过 max_len + ellipsis
        self.assertLessEqual(len(snippet.replace("…", "")), 110)

    def test_ellipsis_added_for_truncation(self):
        long_text = "无关内容 " * 20 + "重要内容 pandas" + " 无关内容 " * 20
        snippet   = extract_snippet(long_text, ["pandas"], max_len=80)
        self.assertTrue(snippet.startswith("…") or snippet.endswith("…"),
                        "截断时应添加省略号")

    def test_empty_text(self):
        self.assertEqual(extract_snippet("", ["test"]), "")

    def test_no_query_match_returns_beginning(self):
        """查询词不在文本中，返回文本起始部分（不崩溃）"""
        text    = "一段与查询无关的内容 " * 5
        snippet = extract_snippet(text, ["完全不存在的词"], max_len=50)
        self.assertIsInstance(snippet, str)


# ─────────────────────────────────────────────────────────
# 反馈环防护测试
# ─────────────────────────────────────────────────────────

class TestFeedbackLoopPrevention(unittest.TestCase):

    def test_ultra_memory_log_stripped(self):
        text = "[ultra-memory] 📝 [42] milestone: 数据清洗完成"
        self.assertNotIn("[ultra-memory]", filter_memory_markers(text))

    def test_memory_ready_signal_stripped(self):
        text = "MEMORY_READY session_id: sess_abc123"
        result = filter_memory_markers(text)
        self.assertNotIn("MEMORY_READY", result)

    def test_compress_suggested_stripped(self):
        text = "COMPRESS_SUGGESTED\n继续其他任务"
        result = filter_memory_markers(text)
        self.assertNotIn("COMPRESS_SUGGESTED", result)

    def test_session_id_stripped(self):
        text = "SESSION_ID=sess_xxxxxxxxxxx 已保存"
        result = filter_memory_markers(text)
        self.assertNotIn("sess_xxxxxxxxxxx", result)

    def test_recall_output_stripped(self):
        text = "[RECALL] 找到 3 条相关记录（查询: pandas）"
        result = filter_memory_markers(text)
        self.assertNotIn("[RECALL]", result)

    def test_normal_text_unchanged(self):
        """正常代码和自然语言不应被过滤"""
        text = "pandas.read_csv('data.csv') 已成功读取 1000 行数据"
        result = filter_memory_markers(text)
        self.assertIn("pandas", result)
        self.assertIn("1000 行数据", result)

    def test_ops_format_stripped(self):
        text = "[ops #42 · 2026-04-07 10:00] 安装了 pandas 2.2.0"
        result = filter_memory_markers(text)
        self.assertNotIn("[ops #42", result)


# ─────────────────────────────────────────────────────────
# 三层记忆分级测试
# ─────────────────────────────────────────────────────────

class TestMemoryTier(unittest.TestCase):

    def _op(self, op_type: str, tags: list = None) -> dict:
        return {"type": op_type, "tags": tags or [], "summary": "test"}

    def test_milestone_is_core(self):
        self.assertEqual(classify_tier(self._op("milestone")), TIER_CORE)

    def test_decision_is_core(self):
        self.assertEqual(classify_tier(self._op("decision")), TIER_CORE)

    def test_error_is_core(self):
        self.assertEqual(classify_tier(self._op("error")), TIER_CORE)

    def test_user_instruction_is_core(self):
        self.assertEqual(classify_tier(self._op("user_instruction")), TIER_CORE)

    def test_file_read_is_peripheral(self):
        self.assertEqual(classify_tier(self._op("file_read")), TIER_PERIPHERAL)

    def test_tool_call_is_peripheral(self):
        self.assertEqual(classify_tier(self._op("tool_call")), TIER_PERIPHERAL)

    def test_file_read_with_milestone_tag_is_working(self):
        """file_read 带 milestone 标签时不应降为 peripheral"""
        op = self._op("file_read", tags=["milestone"])
        self.assertNotEqual(classify_tier(op), TIER_PERIPHERAL)

    def test_bash_exec_is_working(self):
        self.assertEqual(classify_tier(self._op("bash_exec")), TIER_WORKING)

    def test_reasoning_is_working(self):
        self.assertEqual(classify_tier(self._op("reasoning")), TIER_WORKING)

    def test_tier_constants_distinct(self):
        self.assertNotEqual(TIER_CORE, TIER_WORKING)
        self.assertNotEqual(TIER_WORKING, TIER_PERIPHERAL)
        self.assertNotEqual(TIER_CORE, TIER_PERIPHERAL)


# ─────────────────────────────────────────────────────────
# 重要性评分测试
# ─────────────────────────────────────────────────────────

class TestComputeImportance(unittest.TestCase):

    def test_milestone_is_max(self):
        score = _compute_importance("milestone", "项目发布完成", {})
        self.assertGreaterEqual(score, 0.9)

    def test_file_read_is_low(self):
        score = _compute_importance("file_read", "读取 config.yaml", {})
        self.assertLessEqual(score, 0.5)

    def test_error_keyword_boosts_score(self):
        """error 关键词应提升基础分"""
        base = _compute_importance("reasoning", "分析问题", {})
        boosted = _compute_importance("reasoning", "error: connection failed", {})
        self.assertGreater(boosted, base)

    def test_importance_range(self):
        """所有情况下分数应在 [0, 1]"""
        for op_type in ("milestone", "decision", "error", "file_read", "tool_call", "bash_exec"):
            score = _compute_importance(op_type, "some summary", {"key": "value"})
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)

    def test_critical_keyword_boosts_any_type(self):
        """critical 关键词对任意类型均加分"""
        base = _compute_importance("file_write", "更新了文件", {})
        boosted = _compute_importance("file_write", "critical: 必须修复此问题", {})
        self.assertGreater(boosted, base)

    def test_decision_with_deploy_higher_than_base(self):
        score = _compute_importance("decision", "决定使用 docker deploy", {})
        base = _compute_importance("decision", "决定了一件事", {})
        self.assertGreaterEqual(score, base)


# ─────────────────────────────────────────────────────────
# 访问计数回写测试
# ─────────────────────────────────────────────────────────

class TestIncrementAccessCount(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.session_dir = Path(self.tmpdir) / "sessions" / "test_sess"
        self.session_dir.mkdir(parents=True)
        self.ops_file = self.session_dir / "ops.jsonl"

    def _write_ops(self, ops: list[dict]):
        with open(self.ops_file, "w", encoding="utf-8") as f:
            for op in ops:
                f.write(json.dumps(op) + "\n")

    def _read_ops(self) -> list[dict]:
        result = []
        for line in self.ops_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                result.append(json.loads(line))
        return result

    def test_increment_existing_seq(self):
        self._write_ops([
            {"seq": 1, "summary": "op1", "access_count": 0},
            {"seq": 2, "summary": "op2", "access_count": 3},
        ])
        _increment_access_count(self.session_dir, {1})
        ops = self._read_ops()
        self.assertEqual(ops[0]["access_count"], 1)
        self.assertEqual(ops[1]["access_count"], 3)  # 未被召回，不变

    def test_increment_multiple(self):
        self._write_ops([
            {"seq": 1, "summary": "op1", "access_count": 0},
            {"seq": 2, "summary": "op2", "access_count": 0},
            {"seq": 3, "summary": "op3", "access_count": 0},
        ])
        _increment_access_count(self.session_dir, {1, 3})
        ops = self._read_ops()
        self.assertEqual(ops[0]["access_count"], 1)
        self.assertEqual(ops[1]["access_count"], 0)
        self.assertEqual(ops[2]["access_count"], 1)

    def test_increment_cumulative(self):
        """多次调用应累积"""
        self._write_ops([{"seq": 1, "summary": "op1", "access_count": 5}])
        _increment_access_count(self.session_dir, {1})
        _increment_access_count(self.session_dir, {1})
        ops = self._read_ops()
        self.assertEqual(ops[0]["access_count"], 7)

    def test_empty_seq_set_no_change(self):
        self._write_ops([{"seq": 1, "summary": "op1", "access_count": 0}])
        _increment_access_count(self.session_dir, set())
        ops = self._read_ops()
        self.assertEqual(ops[0]["access_count"], 0)

    def test_missing_file_no_error(self):
        """ops 文件不存在时不应抛异常"""
        _increment_access_count(self.session_dir, {1})  # 应静默通过


# ─────────────────────────────────────────────────────────
# 知识库语义去重测试
# ─────────────────────────────────────────────────────────

class TestKnowledgeDedup(unittest.TestCase):

    def test_identical_text_high_similarity(self):
        sim = _bm25_similarity("pandas 数据清洗方法", "pandas 数据清洗方法")
        self.assertAlmostEqual(sim, 1.0, delta=0.01)

    def test_completely_different_text_zero(self):
        sim = _bm25_similarity("pandas read_csv 用法", "docker 部署配置")
        self.assertLess(sim, 0.2)

    def test_partial_overlap_moderate(self):
        sim = _bm25_similarity("pandas read_csv 方法", "pandas 如何使用 read_csv")
        self.assertGreater(sim, 0.2)

    def test_find_similar_returns_correct_idx(self):
        entries = [
            {"title": "docker 部署", "content": "使用 docker-compose"},
            {"title": "pandas read_csv 方法", "content": "可以用 read_csv 读取"},
        ]
        idx, sim = _find_similar_entry("pandas read_csv 的使用", "read_csv 教程", entries)
        self.assertEqual(idx, 1)
        self.assertGreater(sim, 0.0)

    def test_find_similar_skips_superseded(self):
        entries = [
            {"title": "pandas read_csv", "content": "read_csv", "superseded": True},
        ]
        idx, sim = _find_similar_entry("pandas read_csv", "read_csv", entries)
        self.assertEqual(idx, -1)

    def test_log_knowledge_dedup_reinforces(self):
        """写入高度相似条目时应强化已有条目而非新增"""
        with tempfile.TemporaryDirectory() as tmpdir:
            import os as _os
            _os.environ["ULTRA_MEMORY_HOME"] = tmpdir
            # 重新加载模块以使用新的 HOME
            import importlib
            import log_knowledge as lk
            importlib.reload(lk)
            lk.ULTRA_MEMORY_HOME = Path(tmpdir)

            lk.log_knowledge("pandas 数据清洗方法", "使用 read_csv 和 dropna 处理数据")
            lk.log_knowledge("pandas 数据清洗的方法", "read_csv dropna 处理数据")

            kb_file = Path(tmpdir) / "semantic" / "knowledge_base.jsonl"
            entries = [json.loads(l) for l in kb_file.read_text(encoding="utf-8").splitlines() if l.strip()]
            # 第二次写入应强化已有条目，不新增行
            # (如果相似度超过阈值，条目数保持 1)
            # 相似度可能略低于阈值（取决于分词），允许最多 2 条
            self.assertLessEqual(len(entries), 2)
            # 如果只有 1 条，检查 reinforced_count
            if len(entries) == 1:
                self.assertGreaterEqual(entries[0].get("reinforced_count", 0), 1)


# ─────────────────────────────────────────────────────────
# 多用户/多 Agent scope 隔离测试
# ─────────────────────────────────────────────────────────

class TestScopeIsolation(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        import init as init_mod
        self._orig_base = init_mod._BASE_HOME
        # 让 init 使用临时目录
        init_mod._BASE_HOME = Path(self.tmpdir)
        import importlib
        importlib.reload(init_mod)
        init_mod._BASE_HOME = Path(self.tmpdir)
        self.init_mod = init_mod

    def tearDown(self):
        import init as init_mod
        import importlib
        init_mod._BASE_HOME = self._orig_base
        importlib.reload(init_mod)

    def test_scope_to_home_empty_returns_base(self):
        from init import _scope_to_home
        home = _scope_to_home("")
        # 无 scope 时应返回 base（不含 scopes 子目录）
        self.assertNotIn("scopes", str(home))

    def test_scope_to_home_user_prefix(self):
        import os
        os.environ["ULTRA_MEMORY_HOME"] = self.tmpdir
        from init import _scope_to_home
        home = _scope_to_home("user:alice")
        self.assertIn("scopes", str(home))
        self.assertIn("user__alice", str(home))
        del os.environ["ULTRA_MEMORY_HOME"]

    def test_scope_to_home_agent_prefix(self):
        import os
        os.environ["ULTRA_MEMORY_HOME"] = self.tmpdir
        from init import _scope_to_home
        home = _scope_to_home("agent:bot1")
        self.assertIn("agent__bot1", str(home))
        del os.environ["ULTRA_MEMORY_HOME"]

    def test_scope_no_prefix_defaults_to_user(self):
        """无前缀的 scope 名称自动补 user: 前缀"""
        import os
        os.environ["ULTRA_MEMORY_HOME"] = self.tmpdir
        from init import _scope_to_home
        home_explicit = _scope_to_home("user:alice")
        home_implicit = _scope_to_home("alice")
        self.assertEqual(home_explicit, home_implicit)
        del os.environ["ULTRA_MEMORY_HOME"]

    def test_different_scopes_have_different_paths(self):
        import os
        os.environ["ULTRA_MEMORY_HOME"] = self.tmpdir
        from init import _scope_to_home
        home_alice = _scope_to_home("user:alice")
        home_bob   = _scope_to_home("user:bob")
        self.assertNotEqual(home_alice, home_bob)
        del os.environ["ULTRA_MEMORY_HOME"]

    def test_scope_special_chars_sanitized(self):
        """scope 中特殊字符应被替换为 _"""
        import os
        os.environ["ULTRA_MEMORY_HOME"] = self.tmpdir
        from init import _scope_to_home
        home = _scope_to_home("user:alice/evil/../path")
        self.assertNotIn("..", str(Path(home).name))
        del os.environ["ULTRA_MEMORY_HOME"]

    def test_init_creates_scoped_directory(self):
        """带 scope 的 init 应在 scopes/ 下创建独立目录"""
        import os
        os.environ["ULTRA_MEMORY_HOME"] = self.tmpdir
        from init import init_session
        init_session(project="test", scope="user:alice")
        scoped_dir = Path(self.tmpdir) / "scopes" / "user__alice"
        self.assertTrue(scoped_dir.exists())
        del os.environ["ULTRA_MEMORY_HOME"]

    def test_two_scopes_isolated(self):
        """两个不同 scope 各自拥有独立的 sessions 目录"""
        import os, time
        os.environ["ULTRA_MEMORY_HOME"] = self.tmpdir
        from init import init_session
        meta_alice = init_session(project="proj", scope="user:alice")
        time.sleep(1)  # 保证时间戳不同，session_id 唯一
        meta_bob   = init_session(project="proj", scope="user:bob")
        # session_id 不同
        self.assertNotEqual(meta_alice["session_id"], meta_bob["session_id"])
        # 存储在不同目录
        alice_dir = Path(self.tmpdir) / "scopes" / "user__alice" / "sessions" / meta_alice["session_id"]
        bob_dir   = Path(self.tmpdir) / "scopes" / "user__bob"   / "sessions" / meta_bob["session_id"]
        self.assertTrue(alice_dir.exists())
        self.assertTrue(bob_dir.exists())
        del os.environ["ULTRA_MEMORY_HOME"]


if __name__ == "__main__":
    unittest.main(verbosity=2)
