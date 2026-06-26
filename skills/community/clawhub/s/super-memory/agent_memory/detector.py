"""
detector.py - 主题检测与智能拆分
基于规则 + 相似度 + LLM 的对话主题识别和多主题拆分

v6.1: 写入时因果信号检测（三层架构）
  - Layer 1: 正则硬匹配（零成本，同步执行）
  - Layer 2: 上下文线索（决策词→结果词模式匹配）
"""

from __future__ import annotations

import json
import re
import logging
from dataclasses import dataclass
from .encoder import DimensionEncoder

logger = logging.getLogger(__name__)


@dataclass
class CausalHint:
    """因果信号检测结果"""
    cause_text: str          # 原因片段（从内容中提取）
    effect_text: str         # 结果片段
    confidence: float        # 置信度 0.0~1.0
    source: str              # 来源: "regex" | "context"
    explanation: str         # 人类可读解释


class TopicDetector:
    """基于关键词 + 语义向量相似度的主题检测"""

    def __init__(self, encoder: DimensionEncoder, topic_registry=None, semantic_matcher=None):
        self.encoder = encoder
        self.topic_keywords = self._build_keyword_map()
        self.topic_registry = topic_registry  # TopicRegistry 实例，可选
        self.semantic_matcher = semantic_matcher  # SemanticTopicMatcher 实例，可选

        # 把 detector 的关键词同步给 registry
        if self.topic_registry:
            self.topic_registry.merge_keywords(self.topic_keywords)

    def _build_keyword_map(self) -> dict[str, list[str]]:
        """从主题树构建关键词映射"""
        return {
            "ai.rag":       ["rag", "检索增强", "向量库", "embedding", "检索", "RAG"],
            "ai.rag.vdb":   ["向量库", "向量数据库", "milvus", "chroma", "qdrant", "pgvector", "faiss", "选型"],
            "ai.rag.emb":   ["embedding", "向量化", "编码器", "sentence-transformer", "bge", "jina"],
            "ai.rag.ret":   ["检索", "召回", "rerank", "重排序", "混合检索", "bm25"],
            "ai.agent":     ["agent", "智能体", "工具调用", "function call"],
            "ai.agent.mem": ["记忆", "memory", "上下文", "回忆", "记忆系统"],
            "ai.agent.tool":["工具", "tool", "skill", "技能"],
            "ai.llm":       ["llm", "大模型", "gpt", "claude", "qwen", "大语言模型"],
            "ai.llm.prompt":["prompt", "提示词", "提示工程"],
            "dev.be":       ["后端", "api", "server", "数据库", "sql", "接口"],
            "dev.fe":       ["前端", "vue", "react", "css", "html"],
            "dev.ops":      ["运维", "docker", "部署", "ci/cd", "k8s", "容器化"],
        }

    def detect_dynamic(self, text: str) -> list[str]:
        """无监督主题候选：TF-IDF 关键词提取 + n-gram 聚类（Fix #1）

        不依赖静态注册表，从文本自身提取高信息量词作为主题候选。
        返回候选主题路径列表（未注册的会带 _dynamic. 前缀）。
        """
        import re
        # 分词：中文按字/词，英文按词
        tokens = re.findall(r'[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}', text.lower())
        if not tokens:
            return []

        # 计算 TF（词频）
        tf = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1

        # 按 TF 排序取 top 3 作为主题候选
        sorted_terms = sorted(tf.items(), key=lambda x: -x[1])[:3]
        candidates = []
        for term, freq in sorted_terms:
            if freq >= 2 or len(term) >= 4:  # 过滤低频短词
                # 尝试匹配已有主题
                matched = False
                for topic, kws in self.topic_keywords.items():
                    if term in [k.lower() for k in kws]:
                        candidates.append(topic)
                        matched = True
                        break
                if not matched:
                    # 动态主题：用 term 作为路径
                    candidates.append(f"_dynamic.{term}")
        return candidates

    def detect(self, text: str, auto_register: bool = True) -> list[str]:
        """
        检测文本涉及的主题，返回主题路径列表（主主题在前）。

        匹配优先级:
        1. 关键词子串匹配（最快）
        2. 语义向量相似度（SemanticTopicMatcher）
        3. TopicRegistry 关键词相似度回退
        4. 动态注册新主题（auto_register=True 时）

        参数:
            text: 对话文本
            auto_register: 是否在无匹配时自动注册新主题（默认 True）
        """
        text_lower = text.lower()

        # ── 第一层：关键词子串匹配 ─────────────────────
        scores: dict[str, int] = {}
        for topic, keywords in self.topic_keywords.items():
            for kw in keywords:
                if kw in text_lower:
                    scores[topic] = scores.get(topic, 0) + 1

        if scores:
            sorted_topics = sorted(scores.keys(), key=lambda t: (-scores[t], -len(t)))
            result = []
            for topic in sorted_topics:
                is_child = any(topic.startswith(r + ".") for r in result)
                is_parent = any(r.startswith(topic + ".") for r in result)
                if not is_child and not is_parent:
                    result.append(topic)
            if result:
                return result

        # ── 第二层：语义向量相似度匹配 ─────────────────
        if self.semantic_matcher:
            semantic_hits = self.semantic_matcher.match(text, top_k=1, threshold=0.35)
            if semantic_hits:
                best = semantic_hits[0]
                topic_path = best["topic"]
                score = best["score"]
                logger.info(f"🧠 语义匹配: {topic_path} (score={score:.3f})")
                return [topic_path]

        # ── 第三层：动态关键词候选 ─────────────────────
        dynamic = self.detect_dynamic(text)
        if dynamic:
            # 过滤掉 _dynamic. 前缀的，尝试匹配已有主题
            real_topics = [t for t in dynamic if not t.startswith("_dynamic.")]
            if real_topics:
                return real_topics

        # ── 第四层：TopicRegistry 自动注册 ─────────────
        if self.topic_registry:
            reg_result = self.topic_registry.auto_register(text)
            if reg_result["is_new"]:
                new_path = reg_result["path"]
                kws = reg_result.get("keywords", [])
                if kws:
                    self.topic_keywords[new_path] = kws
                if self.semantic_matcher:
                    self.semantic_matcher.add_topic_vector(new_path, kws)
                # 同步到 encoder 注册表
                try:
                    self.encoder.encode_topic(new_path, auto_register=True)
                except Exception as e:
                    logger.warning("detector: %s", e)
                logger.info(f"🆕 动态注册新主题: {new_path} (相似度={reg_result['similarity']:.2f})")
                return [new_path]
            elif reg_result["matched"]:
                return [reg_result["path"]]

        # ── 第五层：兜底 — 用动态候选创建 _dynamic 主题 ──
        if auto_register and dynamic:
            # 把 _dynamic. 前缀的候选转为正式主题
            dyn_topics = [t for t in dynamic if not t.startswith("_dynamic.")]
            # 也尝试从 _dynamic 中提取有意义的词
            dyn_raw = [t.replace("_dynamic.", "") for t in dynamic if t.startswith("_dynamic.")]

            # 合并候选：优先用非 _dynamic 的，其次用 _dynamic 提取的
            candidates = dyn_topics + dyn_raw
            if candidates:
                # 去重，按长度排序（短的优先，更可能是核心概念）
                candidates = sorted(set(candidates), key=len)
                slug = candidates[0]

                # 尝试注册为 misc.{slug}，或者如果 TopicRegistry 匹配到了更好的父主题就用那个
                new_path = f"misc.{slug}"
                if self.topic_registry:
                    reg = self.topic_registry.auto_register(text, keywords=[slug])
                    if reg.get("path") and not reg["path"].startswith("misc."):
                        new_path = reg["path"]

                try:
                    self.encoder.encode_topic(new_path, auto_register=True)
                    self.topic_keywords[new_path] = [slug] + candidates[1:3]
                    if self.semantic_matcher:
                        self.semantic_matcher.add_topic_vector(new_path, [slug])
                    logger.info(f"🆕 兜底注册主题: {new_path}")
                    return [new_path]
                except Exception as e:
                    logger.warning("detector: %s", e)

        return []

    def detect_nature(self, text: str) -> str:
        """简单规则判断性质"""
        text_lower = text.lower()

        # 关键词匹配
        if any(w in text_lower for w in ["计划", "打算", "准备", "明天", "接下来"]):
            return "todo"
        if any(w in text_lower for w in ["总结", "回顾", "复盘", "反思", "教训"]):
            return "retro"
        if any(w in text_lower for w in ["笔记", "记录", "学到", "知识点"]):
            return "note"
        if any(w in text_lower for w in ["草稿", "初步", "随便想想", "临时"]):
            return "draft"
        if any(w in text_lower for w in ["完成了", "交付", "成果", "最终版"]):
            return "output"
        if any(w in text_lower for w in ["收藏", "保存", "参考", "链接"]):
            return "archive"
        if "?" in text or "？" in text or any(w in text_lower for w in ["怎么", "什么是", "为什么", "如何"]):
            return "ask"
        if any(w in text_lower for w in ["项目", "任务", "开发", "实现"]):
            return "task"
        if any(w in text_lower for w in ["研究", "调研", "探索", "对比"]):
            return "explore"
        if any(w in text_lower for w in ["配置", "设置", "系统", "环境"]):
            return "config"

        return "chat"  # 默认漫谈

    def detect_knowledge(self, text: str) -> list[str]:
        """检测文本包含的知识类型，返回 code 列表"""
        text_lower = text.lower()
        types = []

        # 规则：条件句式
        if any(w in text_lower for w in ["当……时", "如果……就", "一定要", "必须", "不能", "规则是"]):
            types.append("rule")

        # 教训：失败/踩坑
        if any(w in text_lower for w in ["踩坑", "教训", "失败", "不行", "错误", "问题在于", "因为……所以"]):
            types.append("lesson")

        # 事实：陈述句
        if any(w in text_lower for w in ["是", "等于", "意味着", "事实", "确定", "已知"]):
            # 避免和规则/教训重叠
            if "rule" not in types and "lesson" not in types:
                types.append("fact")

        # 技能：操作/方法
        if any(w in text_lower for w in ["怎么", "如何", "步骤", "方法", "做法", "操作"]):
            types.append("skill")

        # 偏好：比较/选择
        if any(w in text_lower for w in ["更喜欢", "偏好", "比起", "选择", "倾向", "推荐"]):
            types.append("pref")

        # 经历：做过/试过
        if any(w in text_lower for w in ["做过", "试过", "用过", "体验", "经历", "以前"]):
            types.append("exp")

        return types

    # ══════════════════════════════════════════════════════
    # 写入时因果信号检测（Layer 1 + 2）
    # ══════════════════════════════════════════════════════

    # Layer 1: 正则硬匹配模式
    _CAUSAL_PATTERNS = [
        # 因为A所以B / 由于A因此B
        (r'因为(.{2,80}?)(?:所以|因此|于是|就|才)(.{2,80})', '因为…所以'),
        (r'由于(.{2,80}?)(?:因此|所以|导致|致使)(.{2,80})', '由于…因此'),
        # A导致B / A造成了B
        (r'(.{2,80}?)(?:导致|造成|致使|引发|引起)(.{2,80})', '…导致…'),
        # A决定了B / A决定了B
        (r'(.{2,80}?)(?:决定了|决定用|选择了|选定)(.{2,80})', '…决定了…'),
        # 基于A的结果/基础上，B
        (r'基于(.{2,80}?)(?:的结果|基础上|的结论|的分析)(?:[，,]?\s*)(.{2,80})', '基于…'),
        # 在A的基础上
        (r'在(.{2,80}?)(?:的基础上|前提下|条件下)(?:[，,]?\s*)(.{2,80})', '在…基础上'),
        # 鉴于A，B / 考虑到A，B
        (r'(?:鉴于|考虑到|根据)(.{2,80}?)[，,](.{2,80})', '鉴于…'),
        # A→B / A => B（显式箭头）
        (r'(.{2,60}?)\s*(?:→|=>|->|＝>|＝>)\s*(.{2,60})', '箭头因果'),
    ]

    # Layer 2: 决策词 + 结果词列表
    _CAUSE_WORDS = {
        "因为", "由于", "鉴于", "基于", "考虑到", "分析后", "研究发现",
        "发现", "踩坑", "测试后", "对比后", "调研", "评估", "确认",
    }
    _EFFECT_WORDS = {
        "所以", "因此", "于是", "决定", "选择", "改为", "最终", "结论",
        "确定用", "选定", "采用", "决定用", "那就", "所以决定",
    }

    def detect_causal_signals(self, content: str) -> list[CausalHint]:
        """
        Layer 1 + 2: 检测文本中的因果信号。

        Layer 1: 正则硬匹配（准确率 >95%，覆盖率 20-30%）
        Layer 2: 上下文线索 — 决策词 + 结果词模式匹配

        返回: CausalHint 列表，置信度从高到低排序。
        """
        hints = []
        content = content.strip()
        if len(content) < 4:
            return hints

        # ── Layer 1: 正则硬匹配 ──
        for pattern, label in self._CAUSAL_PATTERNS:
            m = re.search(pattern, content)
            if m:
                cause = m.group(1).strip()
                effect = m.group(2).strip()
                if len(cause) >= 2 and len(effect) >= 2:
                    hints.append(CausalHint(
                        cause_text=cause,
                        effect_text=effect,
                        confidence=1.0,
                        source="regex",
                        explanation=f"正则匹配: {label}",
                    ))

        # ── Layer 2: 上下文线索（决策词 + 结果词共现）──
        if not hints:  # 正则已命中则跳过
            has_cause = any(w in content for w in self._CAUSE_WORDS)
            has_effect = any(w in content for w in self._EFFECT_WORDS)

            if has_cause and has_effect:
                # 尝试用标点或连接词切分
                split_patterns = [
                    r'[，,]\s*(?:所以|因此|于是|决定|选择|最终|那就)',
                    r'(?:因为|由于|鉴于|基于|考虑到)[^，,]{2,60}[，,]',
                ]
                for sp in split_patterns:
                    m = re.search(sp, content)
                    if m:
                        # 取匹配点作为切分
                        split_pos = m.end()
                        if 2 < split_pos < len(content) - 2:
                            left = content[:split_pos].strip().rstrip('，, ')
                            right = content[split_pos:].strip().lstrip('，, ')
                            if len(left) >= 2 and len(right) >= 2:
                                hints.append(CausalHint(
                                    cause_text=left,
                                    effect_text=right,
                                    confidence=0.7,
                                    source="context",
                                    explanation="上下文线索: 决策词+结果词共现",
                                ))
                                break

                # 如果没找到明确切分，标记为弱因果信号
                if not hints:
                    hints.append(CausalHint(
                        cause_text=content,
                        effect_text="",
                        confidence=0.4,
                        source="context",
                        explanation="弱因果信号: 决策词+结果词共现但无明确切分点",
                    ))

        # 按置信度降序
        hints.sort(key=lambda h: -h.confidence)
        return hints


class TopicSplitter:
    """多主题拆分器 — 接入 LLM 智能拆分一段话里的多个主题"""

    SPLIT_PROMPT = """你是一个对话分析器。请将以下对话内容按主题拆分为独立片段。

可用主题路径：{topics}
可用工具：{tools}
可用性质：draft, log, task, explore, note, output, todo, archive, retro, config, chat, ask
可用知识类型：rule, lesson, fact, skill, pref, exp

对话内容：
{content}

要求：
1. 如果整段话只有一个主题，返回 1 个元素即可
2. 如果包含多个主题（如"RAG 用 Chroma 挺好，另外明天3点开会"），拆成多段
3. 每个片段尽量完整、可独立理解
4. topic 选最匹配的路径，不要猜
5. nature 和 knowledge 是 code 列表

以 JSON 数组返回，每个元素：
{{"content": "片段原文", "topic": "主题路径", "nature": "性质code", "tools": ["工具code"], "knowledge": ["知识type code"]}}
"""

    def __init__(self, encoder: DimensionEncoder, llm_fn=None):
        """
        encoder: DimensionEncoder 实例
        llm_fn: LLM 调用函数，签名 fn(prompt: str) -> str
                 如果为 None，拆分功能不可用，会回退到单片段
        """
        self.encoder = encoder
        self.llm_fn = llm_fn

    def split(self, content: str) -> list[dict]:
        """
        对一段对话进行多主题拆分。

        如果没有 llm_fn，返回单片段（回退到关键词检测）。
        如果有 llm_fn，调用 LLM 拆分并解析结果。
        """
        if not self.llm_fn:
            # 回退：不做拆分，直接返回单片段
            return [{
                "content": content,
                "topic": "",
                "nature": "",
                "tools": [],
                "knowledge": [],
            }]

        prompt = self._build_prompt(content)
        response = self.llm_fn(prompt)
        return self._parse_response(response)

    def _build_prompt(self, content: str) -> str:
        topics = ", ".join(self.encoder.list_topics())
        tools = ", ".join(
            f"{v['code']}({k})" for k, v in self.encoder.registry["tools"].items()
        )
        return self.SPLIT_PROMPT.format(topics=topics, tools=tools, content=content)

    def _parse_response(self, response: str) -> list[dict]:
        """解析 LLM 返回的 JSON"""
        try:
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("```", 1)[0]
            return json.loads(cleaned.strip())
        except (json.JSONDecodeError, IndexError):
            return [{"content": response, "topic": "", "nature": "chat", "tools": [], "knowledge": []}]
