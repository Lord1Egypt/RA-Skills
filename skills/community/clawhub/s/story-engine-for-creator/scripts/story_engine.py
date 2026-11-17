import uuid
import json
import re
import hashlib
from dataclasses import asdict, dataclass, field
from typing import Dict, Any, List, Callable, Optional, Protocol, Tuple
from collections import defaultdict

# ==================== 语言适配层（协议化：语言相关判定点全部外置）====================
# 引擎只保留语言无关逻辑（哈希链 / 报告结构 / 五步骨架 / 台账状态机 / 插件框架）；
# 语言相关常量（词表 / 正则 / 阈值 / 风格族预设）由 adapters/<lang>.py 提供。
# 部署约束：引擎文件必须与 adapters/ 目录同级，否则启动即报错（不静默回退）。
import importlib.util as _ilu
import os as _os

_ADAPTER_LANG = "zh"


def _load_language_adapter(lang: str = _ADAPTER_LANG):
    """加载语言适配器；缺失或加载失败立即抛错，不做静默降级。"""
    _here = _os.path.dirname(_os.path.abspath(__file__))
    _path = _os.path.join(_here, "adapters", lang + ".py")
    if not _os.path.exists(_path):
        raise ImportError("语言适配器缺失：%s —— 引擎需与 adapters/ 同目录部署" % _path)
    _spec = _ilu.spec_from_file_location("story_engine_adapter_" + lang, _path)
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    return _mod


_LZ = _load_language_adapter()
# ==================== 语言适配层结束 ====================


# ==================== 引擎隔离防护 ====================
# 本文件是 Creator 引擎。同目录「engine for business.py」是 Business 引擎。
# 两个引擎含多个同名异构数据类（CausalNode / ResponsibilityAccount / ImplicitAssumption /
# CognitiveAuditEngine / NarrativeStripper …），字段与接口不兼容：混用会导致类互相覆盖、
# 数据错乱甚至崩溃。唯一例外：SecondPerspectiveCausalEngine（第二视角五步因果内核）
# 在两个引擎中实现完全一致，可安全共享。
_ENGINE_FINGERPRINT = "creator"

# —— 全局引擎注册表 ——
# module_from_spec 方式加载（见 README load() 示例）不会自动注册进 sys.modules，
# 这里把指纹登记到 sys.modules 的保留键，使 check_engine_isolation 对任何加载方式都有效。
import sys as _sys
_SYS_REG_KEY = "__story_engine_fingerprints__"
_loaded = _sys.modules.get(_SYS_REG_KEY)
if not isinstance(_loaded, dict):
    _loaded = {}
    _sys.modules[_SYS_REG_KEY] = _loaded
_loaded.setdefault(__name__, _ENGINE_FINGERPRINT)


def check_engine_isolation() -> List[str]:
    """检测当前进程是否同时加载了 Creator 与 Business 两个引擎，返回冲突描述列表（空 = 安全）。"""
    import sys

    conflicts: List[str] = []
    other_engines: List[str] = []
    # 1) 全局注册表（覆盖 module_from_spec 手动加载的场景）
    reg = sys.modules.get(_SYS_REG_KEY)
    if isinstance(reg, dict):
        for mod_name, fp in reg.items():
            if mod_name != __name__ and fp != _ENGINE_FINGERPRINT and mod_name not in other_engines:
                other_engines.append(mod_name)
    # 2) sys.modules 中已注册的引擎模块（覆盖正常 import 的场景）
    for mod_name, mod in list(sys.modules.items()):
        if mod is None or mod_name == __name__ or mod_name == _SYS_REG_KEY:
            continue
        fp = getattr(mod, "_ENGINE_FINGERPRINT", None)
        if fp is not None and fp != _ENGINE_FINGERPRINT and mod_name not in other_engines:
            other_engines.append(mod_name)
    if other_engines:
        conflicts.append(
            f"检测到 Business 引擎（模块 {other_engines!r}）与 Creator 引擎同时加载："
            "两者同名数据类（CausalNode 等）字段不兼容，混用会导致数据错乱、程序崩溃。"
            "请勿在同一进程混用两个引擎；唯一可安全共享的是 SecondPerspectiveCausalEngine。"
        )
    return conflicts


# ==================== 协议定义 ====================
class LLMProvider(Protocol):
    def generate(self, prompt: str, **kwargs) -> str: ...


class OpenAIProvider:
    """使用 urllib 调用 OpenAI 兼容接口的 LLM 实现（零外部依赖）。

    支持任何 OpenAI 兼容 API（OpenAI、vLLM、Ollama、本地代理等）。

    Args:
        api_key:   API 密钥。
        model:     模型名称，如 "gpt-4o"、"deepseek-chat"。
        base_url:  API 基础地址，默认 "https://api.openai.com/v1"。
        timeout:   请求超时（秒）。
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        base_url: str = "https://api.openai.com/v1",
        timeout: int = 120,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, prompt: str, **kwargs) -> str:
        import json
        import urllib.request
        import urllib.error

        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 4096)

        body = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            return f"[LLM Error] HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:200]}"
        except Exception as e:
            return f"[LLM Error] {e}"


# ==================== 基础数据结构（与原有保持一致）====================
@dataclass
class ResponsibilityAccount:
    organization: str
    role: str
    stage: str
    nonce: Optional[str] = None

    def __post_init__(self):
        if not self.nonce:
            self.nonce = uuid.uuid4().hex[:8]


class AuditConfigLoader:
    @staticmethod
    def load_from_dict(config: Dict[str, Any]) -> Dict[str, Any]:
        return config

    @staticmethod
    def load_from_json(path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


class AuditPlugin:
    def __init__(
        self, name: str, analyze_func: Callable[[Dict[str, Any]], Dict[str, Any]]
    ):
        self.name = name
        self.analyze = analyze_func


class CognitiveAuditEngine:
    def __init__(self, account: ResponsibilityAccount, config: Dict[str, Any]):
        self.account = account
        self.config = config
        self.plugins: List[AuditPlugin] = []
        allowed_stages = self.config.get("allowed_stages", [])
        if account.stage not in allowed_stages:
            raise ValueError(f"Unsupported stage: {account.stage}")

    def register_plugin(self, plugin: AuditPlugin) -> None:
        self.plugins.append(plugin)

    def audit(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        report = {
            "disclaimer": self.config.get(
                "disclaimer", "本报告基于情节逻辑分析，不构成创作建议"
            ),
            "responsibility_account": self.account.__dict__,
            "audit_timestamp": uuid.uuid1().hex[:8],
            "overall_passed": True,
            "overall_score": 100.0,
            "analysis": {},
            "custom_fields": self.config.get("custom_fields", {}),
        }
        total_score = 0.0
        for plugin in self.plugins:
            result = plugin.analyze(decision_context)
            report["analysis"][plugin.name] = result
            if not result["passed"]:
                report["overall_passed"] = False
            total_score += result["score"]
        if self.plugins:
            report["overall_score"] = round(total_score / len(self.plugins), 2)
        return report


@dataclass
class EmotionalConstraint:
    name: str
    weight: float
    target: Optional[str] = None
    source: str = "initialization"
    version: int = 1


@dataclass
class ImplicitAssumption:
    content: str
    confidence: float
    risk_level: str


@dataclass
class CausalNode:
    """【Creator 引擎专用】因果节点。与 Business 引擎的同名类字段不兼容，切勿混用。"""

    premise: str
    conclusion: str
    context: Dict[str, Any] = field(default_factory=dict)
    node_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    implicit_assumptions: List[ImplicitAssumption] = field(default_factory=list)
    vulnerability_score: float = 100.0
    audit_report: Optional[Dict[str, Any]] = None
    parent_nodes: List[str] = field(default_factory=list)
    child_nodes: List[str] = field(default_factory=list)
    causal_weights: Dict[str, float] = field(default_factory=dict)
    character: str = ""  # 新增：节点所属角色，便于自动注册
    time: str = ""  # 时空坐标：节点发生的显式时间标记（留空=未声明）
    place: str = ""  # 时空坐标：节点发生的显式地点标记（留空=未声明）
    foreshadow: str = ""  # 伏笔语义标记，取值 SET(埋伏笔)/PAY(回收)/空串(非伏笔节点)
    foreshadow_topic: str = ""  # 伏笔主题（如"玉佩来历"），空串=未标记


@dataclass
class CausalLine:
    line_id: str
    character: str
    nodes: List[CausalNode] = field(default_factory=list)


@dataclass
class Chapter:
    chapter_id: int
    title: str
    causal_lines: List[CausalLine]
    global_state_before: Dict[str, Any]
    global_state_after: Dict[str, Any] = field(default_factory=dict)
    content: str = ""
    audit_report: Optional[Dict[str, Any]] = None


@dataclass
class GlobalState:
    characters: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    world_rules: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)
    emotional_constraints: Dict[str, List[EmotionalConstraint]] = field(
        default_factory=dict
    )
    version: int = 0
    last_updated: str = field(default_factory=lambda: uuid.uuid1().hex[:8])


# ==================== 核心组件（已优化）====================
class NarrativeStripper:
    """叙事剥离（上游）：把散文文本转成可供因果引擎消费的最小事件序列。

    修正两处历史缺陷（旧版长期为死代码，零调用）：
      1) 旧版用字符类 [的地得] 全局删除，会破坏「目的/得到/地道/值得」等实义词；
         现改为不删实义字，仅剥离标点与空白。
      2) 旧版动作词用字符类 [打跑走看…] 逐字匹配，「拉黑/离开/难过」被拆成单字；
         现改为按显式词表做最长匹配（覆盖现代叙事 + 古白话）。
    """

    # 标点/空白（全角 + 半角 + 常见引号、书名号）
    _PUNCT_RE = _LZ._PUNCT_RE

    # 动作词表：长词在前，保证最长匹配
    _ACTION_WORDS = _LZ._ACTION_WORDS
    _ACTION_RE = _LZ._ACTION_RE

    @classmethod
    def strip(cls, text: str) -> Dict[str, Any]:
        """剥离标点/空白并抽出 (施动片段, 动作词) 候选；保留 raw_text 便于回溯。"""
        stripped = cls._PUNCT_RE.sub("", text or "")
        stripped = re.sub(r"\s+", " ", stripped).strip()
        actions = cls._ACTION_RE.findall(stripped)
        return {"raw_text": text, "stripped_text": stripped, "actions": actions}

    @staticmethod
    def _name_in(sent: str, names: Optional[Any]) -> str:
        """在句中找第一个命中的已知角色名（供外部词表/姓名集注入）。找不到返回空串。"""
        if not names:
            return ""
        for n in names:
            if n and n in sent:
                return n
        return ""

    @classmethod
    def to_events(
        cls, text: str, start_id: int = 0, names: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """把一段散文按句切分，生成最小事件链：上一句=前提，本句=结论。

        这是「上游空」的最小补齐点——让引擎无需外部抽取器即可直接消费原文。
        角色名判定优先级：外部词表 names（如 prose_bridge.build_name_set 产出的姓名集）
        → 内置 _extract_plausible_name（宁缺毋滥，认不出留空）。
        """
        if not text:
            return []
        sentences = [
            s.strip() for s in re.split(r"(?<=[。！？!?；;…])", text) if s.strip()
        ]
        # 角色名判定优先级：外部词表 names（如红楼梦人物词表/姓名集）→ 内置正则兜底。
        # 严格词表模式：一旦提供 names，句中无命中即留空——宁可判「未知」，也不让
        # _extract_plausible_name 兜底产出「第三」「本係此」式伪角色名。实测红楼梦
        # 第 003 回 305 句中 238 句悬空，主因即该兜底把句首短语误认为人名。
        strict = bool(names)
        events: List[Dict[str, Any]] = []
        for i, sent in enumerate(sentences):
            char = cls._name_in(sent, names)
            if not char and not strict:
                char = _extract_plausible_name(sent)
            events.append(
                {
                    "id": f"E{start_id + i:03d}",
                    "premise": sentences[i - 1] if i > 0 else "",
                    "conclusion": sent,
                    "character": char,
                }
            )
        return events


class ImplicitAssumptionDetector:
    @staticmethod
    def detect(node: CausalNode, global_state: GlobalState) -> List[ImplicitAssumption]:
        assumptions = []
        if "追上去" in node.conclusion or "留在原地" in node.conclusion:
            assumptions.append(
                ImplicitAssumption("角色具备物理位移行为能力且共处同一时空", 0.8, "low")
            )
        if "拉黑" in node.conclusion:
            assumptions.append(
                ImplicitAssumption("角色之间拥有生效的通讯网络连接手段", 0.9, "low")
            )
        if "打电话" in node.premise or "发消息" in node.premise:
            assumptions.append(
                ImplicitAssumption("角色持有可正常使用的通讯设备", 0.95, "low")
            )
        for char_name, emotions in global_state.emotional_constraints.items():
            if char_name in node.premise or char_name in node.conclusion:
                for emotion in emotions:
                    if emotion.weight >= 0.7:
                        target_desc = f"对{emotion.target}" if emotion.target else ""
                        assumptions.append(
                            ImplicitAssumption(
                                content=f"{char_name}{target_desc}存在强烈的{emotion.name}情感",
                                confidence=emotion.weight,
                                risk_level="medium",
                            )
                        )
        return assumptions


class VulnerabilityAssessor:
    @staticmethod
    def assess(node: CausalNode) -> float:
        score = 100.0
        physical = [a for a in node.implicit_assumptions if "情感" not in a.content]
        score -= len(physical) * 3
        forbidden = ["突然", "莫名", "毫无理由", "不知怎么", "鬼使神差", "突然之间"]
        for word in forbidden:
            if word in node.premise or word in node.conclusion:
                score -= 15
        if len(node.causal_weights) >= 2:
            score += min(10, len(node.causal_weights) * 2)
        return max(0.0, score)


class AutomaticStateExtractor:
    @staticmethod
    def extract(text: str, current_state: GlobalState) -> Dict[str, Any]:
        changes: Dict[str, Any] = {}
        if "拉黑了" in text or "拉黑" in text:
            changes.setdefault("events", [])
            changes["events"] = current_state.events + [
                {"event": "关系阻断", "desc": "检测到拉黑/单向切断联系的行为"}
            ]
        if "克制住" in text or "留在原地" in text:
            changes.setdefault("events", [])
            changes["events"] = current_state.events + [
                {"event": "核心成长点", "desc": "行为走向独立"}
            ]
        # 情感关键词自动提取
        emotion_keyword_map = {
            "害怕失去": ("fear_of_loss", 0.8),
            "习惯了": ("habit", 0.7),
            "心动": ("attraction", 0.6),
            "难过": ("sadness", 0.6),
            "愤怒": ("anger", 0.7),
            "愧疚": ("guilt", 0.75),
            "依赖": ("dependence", 0.8),
            "占有欲": ("possessiveness", 0.85),
            "不舍": ("reluctance", 0.65),
        }
        emotional_updates: Dict[str, List[EmotionalConstraint]] = defaultdict(list)
        for keyword, (emotion_name, base_weight) in emotion_keyword_map.items():
            if keyword in text:
                for char_name in current_state.characters.keys():
                    parts = text.split(keyword)
                    context_window = (
                        parts[0][-20:] + parts[1][:20] if len(parts) >= 2 else text
                    )
                    if char_name in context_window:
                        target = None
                        for other in current_state.characters.keys():
                            if other != char_name and other in context_window:
                                target = other
                                break
                        emotional_updates[char_name].append(
                            EmotionalConstraint(
                                name=emotion_name,
                                weight=base_weight,
                                target=target,
                                source="text_extraction",
                                version=current_state.version + 1,
                            )
                        )
        if emotional_updates:
            changes["emotional_constraints"] = dict(emotional_updates)
        return changes


class AutomaticRepairEngine:
    # 生硬转折词表（长词在前，保证正则优先匹配最长形态）
    _JUMP_WORDS = _LZ._JUMP_WORDS_ARE
    _JUMP_PATTERN = _LZ._JUMP_PATTERN
    _TRANSITION = _LZ._TRANSITION
    # 连续重复的过渡短语（如「…顺理成章地顺理成章地…」）合并为一个
    _DUP_TRANSITION = _LZ._DUP_TRANSITION

    @staticmethod
    def repair(
        text: str,
        audit_report: Dict[str, Any],
        llm_provider: Optional[LLMProvider] = None,
    ) -> str:
        # 如果提供了 LLM，尝试让 LLM 重写问题片段（仅对逻辑跳跃词进行修复）
        has_jump = False
        for result in audit_report.get("analysis", {}).values():
            for issue in result.get("issues", []):
                if "逻辑跳跃词" in issue:
                    has_jump = True
                    break
        if has_jump and llm_provider is not None:
            prompt = f"以下文本包含了‘突然’、‘莫名’等不自然的转折词。请重写这段文本，使其逻辑流畅、转折自然，不要改变原意和剧情。\n原文：{text}"
            try:
                repaired = llm_provider.generate(
                    prompt, temperature=0.5, max_tokens=800
                )
                return repaired.strip()
            except Exception:
                pass  # 降级到词替换
        # 降级方案：一次性全量替换所有跳跃词（不再只修第一个）
        repaired = AutomaticRepairEngine._JUMP_PATTERN.sub(
            AutomaticRepairEngine._TRANSITION, text
        )
        # 审计报告中出现的、不在内置表内的自定义跳跃词，同样全量替换
        extra_words: List[str] = []
        for result in audit_report.get("analysis", {}).values():
            for issue in result.get("issues", []):
                if "逻辑跳跃词" in issue:
                    m = re.search(r"'([^']+)'", issue)
                    if m and m.group(1) not in AutomaticRepairEngine._JUMP_WORDS:
                        extra_words.append(m.group(1))
        for w in dict.fromkeys(extra_words):
            repaired = re.sub(re.escape(w), AutomaticRepairEngine._TRANSITION, repaired)
        # 合并相邻重复的过渡短语，避免「顺理成章地顺理成章地」
        repaired = AutomaticRepairEngine._DUP_TRANSITION.sub(
            AutomaticRepairEngine._TRANSITION, repaired
        )
        return repaired


class VisualReportGenerator:
    @staticmethod
    def generate(novel_title: str, chapters: List[Chapter]) -> str:
        html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{novel_title} - 情节逻辑校验报告</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 30px; background: #fdfdfd; color: #333; }}
.chapter {{ margin-bottom: 35px; background: white; border: 1px solid #eee; padding: 25px; border-radius: 12px; }}
.node {{ margin-left: 20px; margin-top: 15px; padding: 18px; background: #f9f9f9; border-radius: 8px; border-left: 4px solid #3498db; }}
.emotion-tag {{ display: inline-block; background: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-right: 5px; }}
.passed {{ color: #27ae60; font-weight: bold; }}
.failed {{ color: #e67e22; font-weight: bold; }}
.score {{ float: right; background: #e0f2fe; color: #0369a1; padding: 5px 12px; border-radius: 20px; font-weight: bold; }}
h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
</style>
</head>
<body>
<h1>📊 《{novel_title}》情节逻辑校验报告</h1>
<p style="color:#777;">系统自动梳理多因果链条、检测情感动机并完成逻辑桥接。</p>
"""
        for ch in chapters:
            if not ch.audit_report:
                continue
            status = (
                "passed" if ch.audit_report.get("overall_passed", True) else "failed"
            )
            html += f"""
<div class="chapter">
    <h2>演进段落：{ch.title} <span class="score">稳态评分：{ch.audit_report.get("overall_score", 100)}</span></h2>
    <p>连贯性验证：<span class="{status}">{"✅ 剧情顺畅" if status == "passed" else "⚠️ 部分断层已修复"}</span></p>
"""
            for line in ch.causal_lines:
                html += f"<h3>👤 角色故事线：{line.character}</h3>"
                for node in line.nodes:
                    emotion_tags = ""
                    for a in node.implicit_assumptions:
                        if "情感" in a.content:
                            emotion_tags += (
                                f'<span class="emotion-tag">{a.content}</span>'
                            )
                    physical = (
                        ", ".join(
                            [
                                a.content
                                for a in node.implicit_assumptions
                                if "情感" not in a.content
                            ]
                        )
                        or "无明显物理断层"
                    )
                    html += f"""
<div class="node">
    <strong>🧬 节点 {node.node_id}</strong>
    <p><b>情节起点：</b>{node.premise}</p>
    <p><b>剧情走向：</b>{node.conclusion}</p>
    {f"<p>💡 情感动机：{emotion_tags}</p>" if emotion_tags else ""}
    <p style="color:#666; font-size:13px;">🔍 潜在线索：{physical}</p>
</div>"""
            html += "</div>"
        html += "</body></html>"
        return html


# ==================== 新增：自然语言解析与自动角色注册 ====================
# —— 角色名候选噪声过滤（防「坚持己见→坚持己」「他说→他说」式乱认）——
_NAME_PRONOUN_HEADS = _LZ._NAME_PRONOUN_HEADS
# 古白话人称/指代扩展（防「某便道」「此人道」被当作角色名）
_NAME_PRONOUN_HEADS = _LZ._NAME_PRONOUN_HEADS
_NAME_VERB_HEADS = _LZ._NAME_VERB_HEADS
# 古白话功能词/场景词开头（防「且请坐」「日天色」被当作角色名）
_NAME_VERB_HEADS = _LZ._NAME_VERB_HEADS
_NAME_TAIL_NOISE = _LZ._NAME_TAIL_NOISE
# 古白话动作/副词残片（防「武松便」「李逵喝」落到候选名尾部）
_NAME_TAIL_NOISE = _LZ._NAME_TAIL_NOISE
# 「状态/副词 + 动词」整块残留（如「李逵大喝」「宋江大怒」「武松便道」）；整块剥除而非逐字
_NAME_STATE_TAIL = (
    "大喝道",
    "大喜道",
    "大怒道",
    "大惊道",
    "大喝",
    "大怒",
    "大喜",
    "大惊",
    "大笑",
    "大哭",
    "大骇",
    "便道",
    "即道",
    "遂道",
    "乃道",
    "却道",
    "又道",
    "也道",
    "都道",
    "只道",
    "方道",
    "才道",
    "正道",
    "先道",
    "忙道",
    "急道",
    "再道",
    "亦道",
    "皆道",
    "俱道",
    "应道",
    "回道",
    "喝道",
    "骂道",
    "笑道",
    "哭道",
    "怒道",
    "叹道",
    "问道",
    "答道",
)
_NAME_FULL_NOISE = (
    "下雨",
    "下雪",
    "刮风",
    "起风",
    "打雷",
    "闪电",
    "天亮",
    "天黑",
    "夜幕",
    "黄昏",
    "清晨",
    "午夜",
    "正午",
    "夜晚",
    "白天",
    "晚上",
    "早晨",
    "下午",
    "中午",
    "街道",
    "房间",
    "车站",
    "站台",
    "城市",
    "村庄",
    "森林",
    "大海",
    "天空",
    "大地",
    "世界",
    "战场",
    "广场",
    "众人",
    "两人",
    "双方",
    "一人",
    "三人",
    "大家",
    "所有人",
    "主角",
    "旁白",
    "镜头",
    "画面",
    "场景",
    "天气",
    "故事",
    "剧情",
    "情节",
    "然后",
    "于是",
    "但是",
    "不过",
    "因为",
    "所以",
    "如果",
    "虽然",
    "突然",
    "终于",
    "毕竟",
    "居然",
    "竟然",
    "我们",
    "你们",
    "他们",
    "她们",
    "它们",
    "自己",
    "彼此",
)
# 古白话/明清小说常见非人名主体（防「二人便道」「太尉道」被当作角色名）
_NAME_FULL_NOISE = _NAME_FULL_NOISE + (
    "二人",
    "数人",
    "诸人",
    "众将",
    "诸将",
    "群臣",
    "百官",
    "好汉",
    "军官",
    "军士",
    "喽啰",
    "小喽啰",
    "庄客",
    "客商",
    "百姓",
    "左右",
    "手下",
    "小厮",
    "丫鬟",
    "婆子",
    "妇人",
    "女子",
    "男子",
    "老儿",
    "后生",
    "闲汉",
    "泼皮",
    "长老",
    "道人",
    "和尚",
    "行者",
    "太尉",
    "提辖",
    "押司",
    "都头",
    "教头",
    "知寨",
    "知县",
    "知府",
    "巡检",
    "虞候",
    "都监",
    "统制",
    "节级",
    "差拨",
    "头领",
    "寨主",
    "庄主",
    "员外",
    "相公",
    "陛下",
    "殿下",
    "大人",
    "师父",
    "师兄",
    "师弟",
    "军师",
    "先锋",
    "天色",
    "天气",
    "日色",
    "月色",
    "夜色",
)
# 常见器物（防「桌子掀」「哨棒打」被当作角色名）
_NAME_FULL_NOISE = _NAME_FULL_NOISE + (
    "桌子",
    "椅子",
    "凳子",
    "哨棒",
    "禅杖",
    "朴刀",
    "腰刀",
    "宝剑",
    "弓箭",
    "刀枪",
    "银子",
    "铜钱",
    "酒杯",
    "酒碗",
    "茶碗",
    "马匹",
    "船只",
)
# 名字候选后允许紧跟的内容（动作/虚词/标点），防止把「林夏意识到」吞成「林夏意」
_NAME_FOLLOW_RE = re.compile(
    r"([\u4e00-\u9fa5]{2,3}?)(?=(?:意识到|觉得|认为|坚持|决定|同意|梳理|评估|分析|理解|"
    r"发现|感到|知道|说道|离开|来到|回到|前往|看着|听见|想起|点头|摇头|沉默|开口|"
    r"转身|回头|抬头|低头|坐下|起身|推开|关上|拿起|放下|掏出|停下|愣住|怔住|惊醒|"
    r"醒来|出门|进屋|盘坐|走入|走进|站在|望着|听着|打量|伸手|握住|松开|深吸|叹息|"
    r"皱眉|轻笑|沉声|低声|高声|忽然|终于|缓缓|慢慢|渐渐|随即|径直|直接|继续|说|道|"
    r"问|喊|答|在|了|着|过|的|地|得|和|与|跟|闭关|修炼|炼化|突破|渡劫|入定|出关|"
    r"运功|施法|掐诀|御剑|下山|云游|历练|顿悟|参悟|凝练|淬炼|召见|议事|禀报|"
    # —— 古白话（明清小说）动作/状态词（多字优先，避免「宋江大喜」吞成「宋江大」）——
    r"大喝道|大喜道|大怒道|大惊道|喝道|骂道|笑道|哭道|怒道|叹道|回道|应道|禀道|报道|"
    r"问道|答道|说罢|说完|大喜|大怒|大惊|大笑|大哭|拱手|作揖|下拜|拜见|相见|"
    r"落座|拍案|拍手|按剑|拔刀|上马|下马|"
    # —— 古白话连接/副词（「武松便走」「宋江又劝」）——
    r"便|即|遂|乃|却|又|也|都|只|方|才|就|正|先|忙|急|再|亦|皆|俱|"
    # —— 古白话单字动作词（保证「鲁智深提」切出 3 字名，而非「智深提」）——
    r"提|拿|取|放|掷|砍|杀|斗|战|进|退|追|寻|送|迎|辞|别|归|回|坐|立|站|跪|走|跑|跳|"
    r"喝|骂|笑|哭|怒|喊|叫|报|禀|应|唤|答|见|听|望|闻|吃|饮|斟|扯|推|扶|奔|逃|藏|躲|"
    r"斩|射|劈|抽|拔|抬|扛|挑|背|抱|捧|递|接|抛|敲|拍|踢|踏|跨|迈|翻|滚|爬|攀|守|攻|"
    r"拜|揖|拉|拽|揪|拴|缚|捆|撒|泼|扔|插|夺|抢|遣|差|领|率|引|随|护|押|"
    # —— 称谓（「宋江哥哥」）与官职（「王进教头」）——
    r"哥哥|兄弟|娘子|夫人|嫂嫂|婆婆|太尉|提辖|押司|都头|教头|知寨|知县|知府|"
    r"巡检|虞候|都监|统制|节级|差拨|头领|寨主|庄主|员外|相公|陛下|殿下|大人|"
    r"先生|师父|师兄|师弟|长老|道人|和尚|行者|军师|先锋|掌柜|"
    r"，|。|；|！|？|：|,|;|!|\?|:))"
)


def _clean_name_candidate(cand: str) -> str:
    """剥去候选名尾部的动词/虚词残片。

    例：「林夏在」→「林夏」「李逵大喝」→「李逵」「武松便道」→「武松」。
    先整块剥除「状态/副词+动词」短语，再逐字剥除尾部虚词。
    """
    base = cand
    for phrase in _NAME_STATE_TAIL:
        if len(base) > len(phrase) and base.endswith(phrase):
            base = base[: -len(phrase)]
            break
    while len(base) > 1 and base.endswith(_NAME_TAIL_NOISE):
        base = base[:-1]
    return base


def _is_plausible_name(name: str) -> bool:
    """判断候选名是否像真实角色名（排除代词、动词短语、天气/场景词等非人名）。"""
    if len(name) < 2:
        return False
    if name.startswith(_NAME_PRONOUN_HEADS):
        return False
    if name in _NAME_FULL_NOISE:
        return False
    if any(name.startswith(h) for h in _NAME_VERB_HEADS):
        return False
    return True


def _extract_plausible_name(text: str) -> str:
    """从文本中提取第一个可信角色名；找不到返回空串（宁缺毋滥，绝不乱认）。"""
    if not text:
        return ""
    # 1) 说话者模式：「XX说/道/问/喊…」
    m = re.search(r"([\u4e00-\u9fa5]{2,4})(?:说道|答道|回答|说|道|问|喊|叫)", text)
    if m:
        name = _clean_name_candidate(m.group(1))
        if _is_plausible_name(name):
            return name
    # 2) 通用候选：2~3 字窗口 + 后随动作/虚词/标点
    for m in _NAME_FOLLOW_RE.finditer(text):
        name = _clean_name_candidate(m.group(1))
        if _is_plausible_name(name):
            return name
    return ""


def extract_character_from_text(text: str) -> str:
    """从文本中提取可能的主角名字；无法确认时返回「主角」占位（调用方会跳过）。"""
    return _extract_plausible_name(text) or "主角"


def auto_register_characters(state: GlobalState, nodes: List[CausalNode]):
    """自动注册节点中出现的不在 state.characters 中的角色。
    加固：残片净化——若候选名以动词/虚词结尾（如「林夏在」「周舟梳」），剥去残片后
    以真实名字注册（「林夏」「周舟」）；若净化结果与已注册角色重叠，跳过避免污染。"""
    # 常见动词/虚词残片，防止「林夏在」「周舟梳」被当作角色名
    _TAIL_NOISE = (
        "在",
        "去",
        "来",
        "说",
        "道",
        "了",
        "着",
        "过",
        "和",
        "与",
        "跟",
        "一起",
        "前往",
        "来到",
        "回到",
        "离开",
        "看着",
        "听",
        "见",
        "问",
        "答",
        "坚持",
        "梳理",
        "理",
        "梳",
        "意识",
        "同意",
        "评估",
        "决定",
        "认为",
        "觉得",
        "想",
    )
    for node in nodes:
        # 尝试从 premise 和 conclusion 中提取角色名
        for text in [node.premise, node.conclusion]:
            char = extract_character_from_text(text)
            if not char or char == "主角":
                continue
            # 群像词开头 → 跳过
            if char.startswith(("两人", "双方", "一人", "三人", "众人")):
                continue
            # 残片净化：剥去尾部动词/虚词，得到真实名字
            base = char
            while base.endswith(_TAIL_NOISE):
                base = base[:-1]
            if len(base) < 2:
                continue  # 剥完只剩 1 字或无，放弃
            # 若净化结果与已注册角色重叠（如已有「林夏」，又出现「林夏在」）→ 跳过
            if base != char and any(base in c or c in base for c in state.characters):
                continue
            char = base
            if char not in state.characters:
                state.characters[char] = {"性格": "中性", "简介": "自动注册的角色"}
                # 自动添加默认情感约束（轻度）
                if char not in state.emotional_constraints:
                    state.emotional_constraints[char] = []
                print(f"自动注册角色：{char}")


def parse_outline_to_nodes(outline: str) -> List[CausalNode]:
    """
    将自然语言大纲解析为 CausalNode 列表。
    支持格式：
      "A -> B -> C"            → 生成 A→B、B→C 两个节点
      "A → B; B → C"          → 生成两个节点
      "前提1 → 结论1; 前提2 → 结论2"
    无箭头片段整段作为前提（结论为占位）。
    """
    # 统一箭头符号
    outline = outline.replace("→", "->").replace("→", "->")
    nodes: List[CausalNode] = []
    for part in re.split(r"[;；\n]", outline):
        part = part.strip()
        if not part:
            continue
        pieces = [p.strip() for p in re.split(r"\s*->\s*", part) if p.strip()]
        if len(pieces) >= 2:
            # 因果链：A -> B -> C 生成 (A→B)、(B→C)，避免结论里残留箭头
            for i in range(len(pieces) - 1):
                node = CausalNode(premise=pieces[i], conclusion=pieces[i + 1])
                node.character = _extract_plausible_name(pieces[i] + pieces[i + 1])
                nodes.append(node)
        else:
            node = CausalNode(premise=pieces[0], conclusion="（待续）")
            node.character = _extract_plausible_name(pieces[0])
            nodes.append(node)
    return nodes


# =============================================================================
# 伏笔台账（Foreshadow Ledger）
# P0 唯一真缺口：记录"埋(埋下/铺垫/留下)－收(回收/呼应/揭开/兑现)"全生命周期。
# 决定论：仅凭显式关键词与主题字符串对账，不臆造"哪些算伏笔"。
# =============================================================================
_FORESHADOW_SET_HINTS = _LZ._FORESHADOW_SET_HINTS
_FORESHADOW_PAY_HINTS = _LZ._FORESHADOW_PAY_HINTS
# 主题断开符：用于从剧情句里切出"伏笔对象/主题"（取主题词后再校验，非概率）
_FORESHADOW_TOPIC_SPLIT = _LZ._FORESHADOW_TOPIC_SPLIT


class ForeshadowLedger:
    """伏笔台账：扫描因果节点/文本，登记 SET/PAY 并对账，输出未回收清单。"""

    def __init__(self):
        self.records: List[Dict[str, Any]] = []  # 每项 {node_id, chapter, topic, action}
        self.topics_seen: List[str] = []

    def _detect(self, text: str) -> Tuple[str, str]:
        """从一句剧情文本中检测【伏笔动作 + 主题】。返回 (action, topic)；无命中返回 ("", "")。"""
        if not text:
            return "", ""
        action = ""
        for w in _FORESHADOW_SET_HINTS:
            if w in text:
                action = "SET"
                break
        if not action:
            for w in _FORESHADOW_PAY_HINTS:
                if w in text:
                    action = "PAY"
                    break
        if not action:
            return "", ""
        # 主题提取：定位命中的动作短语，去掉动作词后取第一个非空语义段
        action_word = ""
        if action == "SET":
            hits = [w for w in _FORESHADOW_SET_HINTS if w in text]
            action_word = max(hits, key=len)
        else:
            hits = [w for w in _FORESHADOW_PAY_HINTS if w in text]
            action_word = max(hits, key=len)
        tail = text[text.rfind(action_word) + len(action_word):]
        topic = ""  # 修复：主题切分结果全空时 topic 未赋值即返回，抛 UnboundLocalError
        for seg in _FORESHADOW_TOPIC_SPLIT.split(tail):
            seg = seg.strip(" 的了")
            if seg:
                topic = seg
                break
        return action, topic

    def scan_nodes(self, nodes: List[CausalNode], chapter_id: Any = "") -> None:
        """扫描因果节点链，登记其 premise+conclusion 两端的伏笔语义。"""
        for n in nodes:
            for field_txt in (n.premise, n.conclusion):
                action, topic = self._detect(field_txt)
                if action:
                    n.foreshadow = action
                    if topic:
                        n.foreshadow_topic = topic
                        self.topics_seen.append(topic)
                    self.records.append(
                        {
                            "node_id": n.node_id,
                            "chapter": chapter_id,
                            "character": n.character,
                            "topic": topic,
                            "action": action,
                        }
                    )

    def reconcile(self) -> Dict[str, Any]:
        """对账：找出已 SET 未 PAY 的伏笔主题。输出未回收清单（决定论结论）。"""
        set_topics = {r["topic"] for r in self.records if r["action"] == "SET" and r["topic"]}
        pay_topics = {r["topic"] for r in self.records if r["action"] == "PAY" and r["topic"]}
        unrecovered = sorted(set_topics - pay_topics)
        ledger = {
            "records": self.records,
            "set_count": sum(1 for r in self.records if r["action"] == "SET"),
            "pay_count": sum(1 for r in self.records if r["action"] == "PAY"),
            "unrecovered_topics": unrecovered,
            "all_closed": len(unrecovered) == 0,
            "note": "伏笔台账：SET=埋下 PAY=回收；主题由显式关键词切出，未回收=已埋未收。",
        }
        return ledger

    def to_markdown(self) -> str:
        """把伏笔台账导出为作者可读的回收表（Markdown）。决定论：仅复述已登记记录。"""
        ledger = self.reconcile()
        md = ["# 伏笔回收表（Foreshadow Ledger）", ""]
        md.append(
            f"- 已埋(SET)：{ledger['set_count']} ｜ 已收(PAY)：{ledger['pay_count']} ｜ "
            f"未回收：{len(ledger['unrecovered_topics'])}"
        )
        if ledger["unrecovered_topics"]:
            md.append("")
            md.append("## ⚠️ 未回收伏笔")
            for t in ledger["unrecovered_topics"]:
                md.append(f"- {t}")
        md.append("")
        md.append("## 全部记录")
        for r in self.records:
            md.append(
                f"- [{r['action']}] {r.get('topic') or '（未标记主题）'} "
                f"（节点 {r['node_id']}｜角色 {r.get('character') or '?'}｜"
                f"章节 {r.get('chapter') or '?'}）"
            )
        return "\n".join(md)


# =============================================================================
# 时空坐标一致性校验（角色 × 时间 × 地点 三维交叉）
# P1：复用 timeline/geography 骨架；仅当节点显式声明 time 与 place 时参与校验，缺省跳过。
# =============================================================================
def audit_spacetime_consistency(nodes: List[CausalNode]) -> Dict[str, Any]:
    """检测"同一角色同一时间出现在两个地点"类冲突。宁缺毋滥：无坐标者不参与。"""
    conflicts: List[str] = []
    by_key: Dict[Tuple[str, str], CausalNode] = {}
    for n in nodes:
        if not n.character or not n.time or not n.place:
            continue  # 缺任一坐标，跳过（不臆造）
        key = (n.character, n.time)
        if key in by_key:
            prev = by_key[key]
            if prev.place != n.place:
                conflicts.append(
                    f"时空冲突：{n.character} 于 {n.time} 同时出现在 [{prev.place}] 与 [{n.place}]"
                )
        else:
            by_key[key] = n
    return {
        "passed": len(conflicts) == 0,
        "conflicts": conflicts,
        "checked_nodes": len(by_key),
        "note": "时空校验：仅对同时声明了角色/时间/地点的节点交叉比对。",
    }


# =============================================================================
# 哈希链审计报告（NOHN 差异化：可信审计存证）
# P2：复用 second-perspective 的 hash-chained 思路，为逐章节审计报告串上防篡改哈希链。
# =============================================================================
def _hash_block(prev_hash: str, payload: Any) -> str:
    """计算单块哈希：prev_hash(32位hex) + payload 的字符串化摘要（对任意结构稳健）。"""
    digester = hashlib.sha256()
    digester.update(str(prev_hash).encode("utf-8"))
    try:
        body = json.dumps(payload, ensure_ascii=False, default=asdict)
    except TypeError:
        body = str(payload)
    digester.update(body.encode("utf-8"))
    return digester.hexdigest()


# 哈希载荷中的随机字段（uuid4/uuid1 派生）：不参与内容哈希
_NONDET_HASH_KEYS = ("node_id", "nonce", "audit_timestamp", "last_updated")
# uuid 派生 id 的形态（8 位小写 hex）；确定性序号如 "E001"、中文内容字段均不匹配
_UUID_ID_RE = re.compile(r"^[0-9a-f]{8}$")


def _looks_uuid(v: Any) -> bool:
    """值形态是否 uuid 派生（8 位小写 hex）。"""
    return isinstance(v, str) and bool(_UUID_ID_RE.match(v))


def _strip_nondeterminism(obj: Any) -> Any:
    """递归剥离载荷中的随机字段，替换为固定占位，使「同内容 → 同哈希」。

    根因：报告内含 uuid4/uuid1 派生的 node_id / nonce / audit_timestamp /
    last_updated，以及 parse_outline_to_nodes 用 uuid 生成的 chain[*].id、
    anchors[*].event_id、causal.weakest_variable——同一文本重复审计会得到不同
    audit_hash，哈希链只能证明「本次运行内部链不断」，不能证明「内容未被改动」，
    与可信存证目标矛盾。
    本函数在入哈希前统一剥离这些字段；内容字段（premise/conclusion/character/
    dangling/assumptions 及 E001 式序号）全部保留参与哈希。
    """
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in _NONDET_HASH_KEYS or _looks_uuid(v):
                out[k] = "<NONDET>"
            else:
                out[k] = _strip_nondeterminism(v)
        return out
    if isinstance(obj, (list, tuple)):
        return [_strip_nondeterminism(x) for x in obj]
    return obj


# =============================================================================
# CharacterProfiler：角色档案自动提取（候选，不臆造）
# 从文本自动推断每角色的【语域画像 register_hints】与【已知知识 knowledge】候选。
# 诚实原则：自动产物一律标记为 candidate，需作者确认后才生效；
#            forbidden_knowledge（角色不该知道的事）本质是创作意图，默认由作者填写。
# =============================================================================

# 语域推断时排除的通用词（出现频率高但不构成角色腔调）
_REGISTRY_STOPWORDS = {
    "一个", "这个", "那个", "什么", "怎么", "自己", "我们", "你们", "他们",
    "没有", "不是", "就是", "知道", "觉得", "说道", "时候", "现在", "已经",
    "如果", "然后", "但是", "因为", "所以", "可以", "这样", "那样", "还有",
    "真的", "可能", "应该", "非常", "一直", "终于", "突然", "最后", "开始",
    "有点", "有些", "一下", "起来", "出来", "过来", "进去", "回来", "只是",
}

# knowledge 候选提取：句中明确“说出”的信息实体（名词性短语）
_KNOWLEDGE_ENTITY_RE = re.compile(
    r"(?:封印|禁地|宝藏|秘笈|秘籍|阵法|丹药|功法|宗门|家族|计划|阴谋|真相|秘密|"
    r"身份|身世|往事|线索|卷宗|地图|钥匙|信物|令牌|消息|情报|地点|名单|证据)"
)


def _split_dialogue_blocks(text: str) -> List[Dict[str, str]]:
    """粗粒度切分台词块：提取 [说话人, 台词] 对（说话人取台词前最近的角色名）。"""
    blocks: List[Dict[str, str]] = []
    for re_pat in _DIALOGUE_RES:
        for m in re_pat.finditer(text):
            d = m.group(1).strip()
            if not d:
                continue
            window = text[max(0, m.start() - 60) : m.start()]
            # 说话者模式「XX说/道/问/喊」：取 window 内【最后一个】匹配（最靠近台词）；
            # 名字限 2-3 字，兼容「又说/也道/低声问」等副词/状语
            sp = None
            for sm in re.finditer(
                r"([\u4e00-\u9fa5]{2,3})(?:又|也|再|便|就|却|连忙|低声|大声|冷笑)?[说说道问喊答]",
                window,
            ):
                sp = sm
            speaker = sp.group(1) if sp else ""
            if not speaker:
                # 兜底：窗口内最近的角色名（排除动作词）
                cands = re.findall(r"[\u4e00-\u9fa5]{2,4}", window)
                if cands:
                    speaker = cands[-1]
            blocks.append({"speaker": speaker, "dialogue": d})
    return blocks


def extract_character_profiles(text: str) -> Dict[str, Dict[str, Any]]:
    """从正文文本提取角色档案候选。

    返回 {角色名: {"register_hints_candidates": [...], "knowledge_candidates": [...]}}
    不写入全局状态，由调用方决定是否确认。
    """
    blocks = _split_dialogue_blocks(text)
    if not blocks:
        return {}
    # 说话人统计 + 台词收集
    speaker_dialogues: Dict[str, List[str]] = {}
    for b in blocks:
        if b["speaker"]:
            speaker_dialogues.setdefault(b["speaker"], []).append(b["dialogue"])
    # 全部台词词频（用于识别“他人专属词”候选时过滤通用词）
    from collections import Counter

    all_word_counter: Counter = Counter()
    for dl in speaker_dialogues.values():
        for d in dl:
            pure = re.sub(r"[^\u4e00-\u9fa5]", "", d)
            for i in range(len(pure) - 1):
                all_word_counter[pure[i : i + 2]] += 1
    profiles: Dict[str, Dict[str, Any]] = {}
    for speaker, dls in speaker_dialogues.items():
        per = Counter()
        for d in dls:
            pure = re.sub(r"[^\u4e00-\u9fa5]", "", d)
            for i in range(len(pure) - 1):
                per[pure[i : i + 2]] += 1
        # 语域候选：台词内的 2 字滑动窗口（重叠式，不丢边界：老朽/禁地/碰不得 都能命中）；
        # 过滤停用词与全局高频词；高频专属词（该角色独有的 3-4 字短语）单独补充
        hints = []
        seen_hint = set()
        for d in dls:
            pure = re.sub(r"[^\u4e00-\u9fa5]", "", d)
            for i in range(len(pure) - 1):
                w = pure[i : i + 2]
                if w in _REGISTRY_STOPWORDS or w in seen_hint:
                    continue
                if all_word_counter[w] > 1:
                    continue
                seen_hint.add(w)
                hints.append(w)
        # 补充：高频但非全局高频的词（出现>=2次且只此角色说）
        for w, cnt in per.most_common(60):
            if w in seen_hint or w in _REGISTRY_STOPWORDS:
                continue
            if cnt >= 2 and all_word_counter[w] == cnt:
                seen_hint.add(w)
                hints.append(w)
        # knowledge 候选：台词中出现的实体词
        knowledge = []
        for d in dls:
            for m in _KNOWLEDGE_ENTITY_RE.finditer(d):
                # 取实体词前后最多4字上下文作为“已知信息”候选
                ctx = d[max(0, m.start() - 4) : m.end() + 4]
                if ctx not in knowledge:
                    knowledge.append(ctx)
        profiles[speaker] = {
            "register_hints_candidates": hints[:12],
            "knowledge_candidates": knowledge[:12],
        }
    return profiles


# ==================== 主引擎（已优化）====================
class UltimateCausalNovelEngine:
    def __init__(
        self,
        novel_title: str,
        initial_global_state: GlobalState,
        output_language: str = "zh",
        target_style: Optional[str] = None,
    ):
        self.novel_title = novel_title
        self.global_state = initial_global_state
        self.output_language = output_language
        self.target_style = target_style
        self.chapters: List[Chapter] = []
        self.causal_graph: Dict[str, CausalNode] = {}
        self.llm_provider: Optional[LLMProvider] = None
        # 新增：伏笔台账 + 可信审计哈希链（P0/P2）
        self.foreshadow_ledger = ForeshadowLedger()
        self.audit_chain_prefix: str = "GENESIS"  # 首块前驱，链头占位

        self._init_audit_engines()
        self._register_all_audit_plugins()
        self.stripper = NarrativeStripper()
        self.assumption_detector = ImplicitAssumptionDetector()
        self.vulnerability_assessor = VulnerabilityAssessor()
        self.state_extractor = AutomaticStateExtractor()
        self.repair_engine = AutomaticRepairEngine()
        self.report_generator = VisualReportGenerator()
        self.sp_engine = SecondPerspectiveCausalEngine()
        self.world_builder = WorldBuilder()
        self.style_recognizer = StyleRecognizer()
        self.presentation_auditor = NarrativePresentationAuditor(
            self.global_state.world_rules
        )

    def set_llm_provider(self, provider: LLMProvider) -> None:
        self.llm_provider = provider
        # 同步下游引擎：深度诊断与世界观深校验可由 LLM 驱动
        if getattr(self, "sp_engine", None) is not None:
            self.sp_engine.llm_provider = provider
        if getattr(self, "world_builder", None) is not None:
            self.world_builder.llm_provider = provider
        # 同步文风审计器：可选 LLM 辅助（默认关闭，开启后用于病句/修辞一致性）
        if getattr(self, "presentation_auditor", None) is not None:
            self.presentation_auditor.prose_auditor.llm_provider = provider

    def set_target_style(self, style: Optional[str]) -> None:
        """设定目标文风（A+B）：生成时注入预设约束，审查时按对应族阈值校验；None 退回自动识别。"""
        self.target_style = style

    def _style_family(self) -> Optional[str]:
        """返回当前目标文风映射到的审查族；未设定则回退 world_rules.style_profile.style，再否则 None（自动识别）。"""
        style = self.target_style
        if not style:
            profile = (self.global_state.world_rules or {}).get("style_profile") or {}
            style = profile.get("style")
        if not style:
            return None
        return STYLE_PRESETS.get(style, {}).get("family")

    def _init_audit_engines(self):
        self.planning_auditor = CognitiveAuditEngine(
            ResponsibilityAccount("StoryStudio", "ChapterPlanner", "planning"),
            {"allowed_stages": ["planning"]},
        )
        self.node_auditor = CognitiveAuditEngine(
            ResponsibilityAccount("StoryStudio", "NodeGenerator", "generation"),
            {"allowed_stages": ["generation"]},
        )
        self.consistency_auditor = CognitiveAuditEngine(
            ResponsibilityAccount("StoryStudio", "ConsistencyChecker", "consistency"),
            {"allowed_stages": ["consistency"]},
        )
        self.vulnerability_auditor = CognitiveAuditEngine(
            ResponsibilityAccount(
                "StoryStudio", "VulnerabilityAssessor", "vulnerability"
            ),
            {"allowed_stages": ["vulnerability"]},
        )

    def _register_all_audit_plugins(self):
        self.planning_auditor.register_plugin(
            AuditPlugin("story_chain_integrity", self._audit_story_chain_integrity)
        )
        self.planning_auditor.register_plugin(
            AuditPlugin(
                "implicit_assumption_detection", self._audit_implicit_assumptions
            )
        )
        self.node_auditor.register_plugin(
            AuditPlugin("logical_jump_detection", self._audit_logical_jump)
        )
        self.node_auditor.register_plugin(
            AuditPlugin(
                "premise_conclusion_match", self._audit_premise_conclusion_match
            )
        )
        self.consistency_auditor.register_plugin(
            AuditPlugin("character_consistency", self._audit_character_consistency)
        )
        self.consistency_auditor.register_plugin(
            AuditPlugin(
                "world_rule_consistency",
                lambda ctx: self.world_builder.check_deep_consistency(
                    ctx, self.global_state
                ),
            )
        )
        self.vulnerability_auditor.register_plugin(
            AuditPlugin("vulnerability_assessment", self._audit_vulnerability)
        )

    def _audit_implicit_assumptions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        events = self._context_to_events(context)
        chain = self.sp_engine.narrative_stripping(events)
        self.sp_engine.implicit_assumption_probe(chain)
        critical = 0
        for line in context.get("causal_lines", []):
            for node in line.nodes:
                node.implicit_assumptions = self.assumption_detector.detect(
                    node, self.global_state
                )
        for ev in chain:
            for a in ev.get("assumptions", []):
                if a["collapse"] == "INEVITABLE":
                    critical += 1
        return {
            "passed": critical == 0,
            "score": max(0.0, 100.0 - critical * 20),
            "critical_assumptions": critical,
        }

    def _audit_logical_jump(self, context: Dict[str, Any]) -> Dict[str, Any]:
        text = context.get("text", "")
        forbidden = ["突然", "莫名", "毫无理由", "不知怎么", "鬼使神差", "突然之间"]
        issues = [f"发现逻辑跳跃词：'{w}'" for w in forbidden if w in text]
        score = max(0.0, 100.0 - len(issues) * 15)
        return {"passed": len(issues) == 0, "issues": issues, "score": score}

    def _audit_vulnerability(self, context: Dict[str, Any]) -> Dict[str, Any]:
        node = context["node"]
        score = self.vulnerability_assessor.assess(node)
        node.vulnerability_score = score
        return {"passed": score >= 50, "score": score}

    def _context_to_events(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []
        lines = context.get("causal_lines") or []
        for line in lines:
            nodes = getattr(
                line, "nodes", line.get("nodes", []) if isinstance(line, dict) else []
            )
            for n in nodes:
                events.append(
                    {
                        "id": getattr(n, "node_id", ""),
                        "premise": getattr(n, "premise", ""),
                        "conclusion": getattr(n, "conclusion", ""),
                        "character": getattr(n, "character", ""),
                    }
                )
        if not events and context.get("node"):
            n = context["node"]
            events.append(
                {
                    "id": getattr(n, "node_id", ""),
                    "premise": getattr(n, "premise", ""),
                    "conclusion": getattr(n, "conclusion", ""),
                    "character": getattr(n, "character", ""),
                }
            )
        return events

    def _audit_story_chain_integrity(self, context: Dict[str, Any]) -> Dict[str, Any]:
        chain = self.sp_engine.narrative_stripping(self._context_to_events(context))
        dangling = [e["id"] for e in chain if e.get("dangling")]
        return {
            "passed": not dangling,
            "score": max(0.0, 100.0 - len(dangling) * 15),
            "dangling_events": dangling,
        }

    def _audit_premise_conclusion_match(
        self, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        mismatches = []
        for ev in self._context_to_events(context):
            char = ev.get("character") or ""
            if char and char not in (ev.get("premise", "") + ev.get("conclusion", "")):
                mismatches.append(ev["id"])
        return {
            "passed": not mismatches,
            "score": max(0.0, 100.0 - len(mismatches) * 15),
            "mismatch_events": mismatches,
        }

    def _audit_character_consistency(self, context: Dict[str, Any]) -> Dict[str, Any]:
        violations = []
        for ev in self._context_to_events(context):
            char = ev.get("character")
            profile = self.global_state.characters.get(char, {})
            if profile:
                restraint = profile.get("restraint", profile.get("克制", 0.5))
                if isinstance(restraint, (int, float)) and restraint > 0.7:
                    if any(
                        w in ev.get("conclusion", "")
                        for w in ["大喊", "追赶", "崩溃", "痛哭"]
                    ):
                        violations.append(ev["id"])
        return {
            "passed": not violations,
            "score": max(0.0, 100.0 - len(violations) * 20),
            "violations": violations,
        }

    def plan_chapter(
        self, chapter_id: int, title: str, causal_lines: List[CausalLine]
    ) -> Optional[Chapter]:
        # 自动注册角色
        all_nodes = []
        for line in causal_lines:
            all_nodes.extend(line.nodes)
        auto_register_characters(self.global_state, all_nodes)

        report = self.planning_auditor.audit(
            {"chapter_id": chapter_id, "title": title, "causal_lines": causal_lines}
        )
        for line in causal_lines:
            for node in line.nodes:
                self.causal_graph[node.node_id] = node
        chapter = Chapter(
            chapter_id=chapter_id,
            title=title,
            causal_lines=causal_lines,
            global_state_before=json.loads(json.dumps(asdict(self.global_state))),
            audit_report=report,
        )
        self.chapters.append(chapter)
        return chapter

    def render_chapter(self, chapter: Chapter, max_retries: int = 3) -> Optional[str]:
        full_content = ""
        for line in chapter.causal_lines:
            for i, node in enumerate(line.nodes):
                # 首轮生成（无 provider 时内部降级为规则生成）
                if i > 0:
                    text = self._call_llm_to_bridge_gap(
                        line.nodes[i - 1], node, chapter
                    )
                else:
                    text = self._call_llm_for_node(node, chapter)
                node_audit = None
                vuln_audit = None
                prose_audit = None
                for attempt in range(max_retries):
                    node_audit = self.node_auditor.audit(
                        {
                            "node": node,
                            "text": text,
                            "global_state": asdict(self.global_state),
                        }
                    )
                    vuln_audit = self.vulnerability_auditor.audit(
                        {"node": node, "text": text}
                    )
                    # 段级文风审计（规则版零依赖）；仅在有 LLM 时才阻塞重写（规则层不臆造文字）
                    prose_audit = self.presentation_auditor.prose_auditor.audit(
                        text, style_family=self._style_family()
                    )
                    prose_ok = prose_audit["passed"] or self.llm_provider is None
                    if node_audit["overall_passed"] and vuln_audit["overall_passed"] and prose_ok:
                        node.audit_report = {
                            **node_audit,
                            "vulnerability": vuln_audit,
                            "prose_style": prose_audit,
                        }
                        full_content += text + "\n\n"
                        break
                    # 审计失败：优先带因果/文风约束的 LLM 重写，否则降级规则修复
                    if self.llm_provider is not None:
                        rewritten = self._call_llm_rewrite_with_constraints(
                            node, node_audit, vuln_audit, prose_audit
                        )
                        if rewritten:
                            text = rewritten
                            continue
                    text = self.repair_engine.repair(
                        text, node_audit, self.llm_provider
                    )
            else:
                # 用尽重试仍失败：兜底 repair
                text = self.repair_engine.repair(
                    text,
                    {
                        "analysis": {
                            "logical_jump_detection": {"issues": ["发现逻辑跳跃词"]}
                        }
                    },
                    self.llm_provider,
                )
                node.audit_report = (
                    {**node_audit, "vulnerability": vuln_audit, "prose_style": prose_audit}
                    if node_audit
                    else {}
                )
                full_content += text + "\n\n"
        # —— 整章文风审计（渲染章节后守门）：跨段上下文检查节奏/复用/视角一致性 ——
        chapter_prose = self.presentation_auditor.prose_auditor.audit(
            full_content, style_family=self._style_family()
        )
        for _ in range(max_retries):
            if chapter_prose["passed"] or self.llm_provider is None:
                break
            rewritten = self._call_llm_rewrite_chapter_prose(full_content, chapter_prose)
            if not rewritten:
                break
            full_content = rewritten
            chapter_prose = self.presentation_auditor.prose_auditor.audit(full_content)

        consistency_audit = self.consistency_auditor.audit(
            {
                "chapter": asdict(chapter),
                "text": full_content,
                "global_state": asdict(self.global_state),
            }
        )
        chapter.content = full_content.strip()
        # 第二视角五步内核诊断（嵌入一致性审计结果）
        sp_chain = self.sp_engine.narrative_stripping(
            [
                {
                    "id": n.node_id,
                    "premise": n.premise,
                    "conclusion": n.conclusion,
                    "character": n.character,
                }
                for line in chapter.causal_lines
                for n in line.nodes
            ]
        )
        self.sp_engine.implicit_assumption_probe(sp_chain)
        sp_hedge = self.sp_engine.vulnerability_hedge(sp_chain)
        sp_anchor = self.sp_engine.responsibility_anchor(sp_chain)
        sp_recon = self.sp_engine.causal_reconstruction(
            sp_chain, fix_vars=[], target_state="叙事逻辑自洽"
        )
        # 若注入了 LLM，用 deep_diagnose 做语义级深度诊断并合并（保持字段兼容）
        sp_deep = self.sp_engine.deep_diagnose(sp_chain, self.world_builder.world_rules)
        second_perspective = {
            "collapse_verdict": sp_hedge["collapse_verdict"],
            "anchors": sp_anchor,
            "reconstruction": sp_recon,
        }
        if sp_deep:
            second_perspective["deep"] = sp_deep
        chapter.audit_report = {
            **consistency_audit,
            "second_perspective": second_perspective,
            "prose_style": chapter_prose,
        }
        changes = self.state_extractor.extract(full_content, self.global_state)
        for key, val in changes.items():
            self._apply_state_change(key, val)
        self.global_state.version += 1
        chapter.global_state_after = json.loads(json.dumps(asdict(self.global_state)))
        return full_content

    def _call_llm_rewrite_with_constraints(
        self,
        node: CausalNode,
        node_audit: Dict[str, Any],
        vuln_audit: Dict[str, Any],
        prose_audit: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """审计失败后将审计问题作为约束回传 LLM 重写；无 provider 或异常时返回 None（由调用方降级 repair）。"""
        if self.llm_provider is None:
            return None
        issues = []
        for name, res in node_audit.get("analysis", {}).items():
            for issue in res.get("issues", []):
                issues.append(f"[{name}] {issue}")
        for issue in vuln_audit.get("issues", []):
            issues.append(f"[vulnerability] {issue}")
        # 段级文风问题并入约束（视角头跳/语域漂移/冗余等）
        if prose_audit:
            for key, val in prose_audit.items():
                if isinstance(val, dict) and not val.get("passed", True) and "hits" in val:
                    for hit in val["hits"]:
                        issues.append(f"[prose:{key}] {hit}")
        if not issues:
            return None
        lang = (self.output_language or "zh").lower().strip()
        issue_text = "\n".join(issues)
        style_hint = self._style_instruction()
        style_block = (
            f"\n文体风格约束（必须严格遵守）：\n{style_hint}\n" if style_hint else ""
        )
        if lang in ("en", "english"):
            prompt = f"""You are a top-tier plot-logic architect.
Characters: {self.global_state.characters}
Evolve the plot from premise [{node.premise}] to conclusion [{node.conclusion}].
The previous draft FAILED logic audit with these issues:
{issue_text}
Rewrite to eliminate them. Motivations must be clear. Avoid abrupt words.
Output 120-200 English words."""
        else:
            prompt = f"""你是一名顶级情节逻辑架构师。
角色设定：{self.global_state.characters}
请将情节起点【{node.premise}】自然演进至故事走向【{node.conclusion}】。
上一次生成未通过逻辑审计，具体问题如下：
{issue_text}
请重写以消除上述问题，保持人物性格与情节连贯，严禁生硬转折词。
{style_block}
输出150-250字的小说文本。"""
        try:
            return self.llm_provider.generate(prompt, temperature=0.6, max_tokens=8000)
        except Exception:
            return None

    def _call_llm_rewrite_chapter_prose(
        self, full_content: str, prose_audit: Dict[str, Any]
    ) -> Optional[str]:
        """整章渲染后文风审计不通过：把文风问题作为约束回传 LLM 重写整章；无 provider 返回 None。"""
        if self.llm_provider is None:
            return None
        issues = []
        for key, val in prose_audit.items():
            if isinstance(val, dict) and not val.get("passed", True) and "hits" in val:
                for hit in val["hits"]:
                    issues.append(f"[{key}] {hit}")
        if not issues:
            return None
        lang = (self.output_language or "zh").lower().strip()
        issue_text = "\n".join(issues)
        style_hint = self._style_instruction()
        style_block = (
            f"\n文体风格约束（必须严格遵守）：\n{style_hint}\n" if style_hint else ""
        )
        if lang in ("en", "english"):
            prompt = f"""You are a top-tier prose editor. The chapter below FAILED the prose-style audit:
{issue_text}
Rewrite the ENTIRE chapter to fix these style issues (unify POV, remove register drift, fix rhythm/redundancy) while keeping the plot and events unchanged.
{style_block}
Output the revised full chapter text."""
        else:
            prompt = f"""你是一名顶级文字编辑。以下章节未通过文风一致性审计，问题如下：
{issue_text}
请在保持情节与事件不变的前提下重写整章，消除上述文风问题（统一叙事视角、清除语域漂移、修正节奏单调与冗余赘词等）。
{style_block}
输出重写后的完整章节文本。"""
        try:
            return self.llm_provider.generate(prompt, temperature=0.6, max_tokens=8000)
        except Exception:
            return None

    def _call_llm_for_node(self, node: CausalNode, chapter: Chapter) -> str:
        lang = (self.output_language or "zh").lower().strip()
        if self.llm_provider is not None:
            emotions = []
            for char, cons in self.global_state.emotional_constraints.items():
                if char in node.premise or char in node.conclusion:
                    for e in cons:
                        emotions.append(f"{e.name}(权重{e.weight})")
            emotion_hint = (
                f"当前角色情感状态：{', '.join(emotions)}。请据此合理推导行为动机。"
                if emotions
                else ""
            )
            style_hint = self._style_instruction()
            style_block = (
                f"\n文体风格约束（必须严格遵守）：\n{style_hint}\n"
                if style_hint
                else ""
            )
            if lang in ("en", "english"):
                prompt = f"""You are a top-tier web fiction writer.
Characters: {self.global_state.characters}
{emotion_hint}
Evolve the plot naturally from the premise [{node.premise}] to the conclusion [{node.conclusion}].
Constraints: vivid prose, character-consistent; motivations clear; avoid abrupt words like "suddenly", "out of nowhere".
Output: 120-200 English words."""
            elif lang in ("bilingual", "zh-en", "zh_en", "cn-en", "cn_en", "mix"):
                prompt = f"""你是一名优秀的网络小说作家，同时也是专业英译者。
角色设定：{self.global_state.characters}
{emotion_hint}{style_block}
请将情节起点【{node.premise}】自然演进至故事走向【{node.conclusion}】。
要求：文字细腻流畅，符合人物性格，行为必须有合理动机，严禁使用“突然”“莫名其妙”等生硬转折词。
输出格式必须严格如下：
【中文】
（150-250字中文小说文本）

【English】
(120-200 English words, faithful translation, natural English)"""
            else:
                prompt = f"""你是一名优秀的网络小说作家。
角色设定：{self.global_state.characters}
{emotion_hint}{style_block}
请将情节起点【{node.premise}】自然演进至故事走向【{node.conclusion}】。
要求：文字细腻流畅，符合人物性格，行为必须有合理动机，严禁使用“突然”“莫名其妙”等生硬转折词。
输出150-250字的小说文本。"""
            return self.llm_provider.generate(prompt, temperature=0.7, max_tokens=8000)
        # 演示模式
        if lang in ("en", "english"):
            return f"[Demo] From “{node.premise}” to “{node.conclusion}”, the character’s inner world shifts, plot moves forward."
        if lang in ("bilingual", "zh-en", "zh_en", "cn-en", "cn_en", "mix"):
            return f"【中文】\n【演示】从「{node.premise}」到「{node.conclusion}」，角色的内心经历了转变，情节自然推进。\n\n【English】\n[Demo] From “{node.premise}” to “{node.conclusion}”, the character’s inner world shifts, plot moves forward."
        return f"【演示】从「{node.premise}」到「{node.conclusion}」，角色的内心经历了转变，情节自然推进。"

    def _call_llm_to_bridge_gap(
        self, prev_node: CausalNode, curr_node: CausalNode, chapter: Chapter
    ) -> str:
        lang = (self.output_language or "zh").lower().strip()
        if self.llm_provider is not None:
            emotions = []
            for char, cons in self.global_state.emotional_constraints.items():
                if char in prev_node.conclusion or char in curr_node.premise:
                    for e in cons:
                        if e.weight >= 0.6:
                            emotions.append(f"{char}的{e.name}")
            emotion_hint = (
                f"重点体现{', '.join(emotions)}的变化过程。" if emotions else ""
            )
            style_hint = self._style_instruction()
            style_block = (
                f"\n文体风格约束（必须严格遵守）：\n{style_hint}\n"
                if style_hint
                else ""
            )
            if lang in ("en", "english"):
                prompt = f"""You are a master of narrative continuity.
There is a natural gap: previous ending [{prev_node.conclusion}], next opening [{curr_node.premise}].
Write a seamless transition (~160-240 English words) using inner thoughts, emotional shifts, or environmental details.
{emotion_hint}
Avoid abrupt words like "suddenly", "out of nowhere". Do NOT repeat previous content."""
            elif lang in ("bilingual", "zh-en", "zh_en", "cn-en", "cn_en", "mix"):
                prompt = f"""你是顶级小说情节逻辑架构师，同时也是专业英译者。
作者大纲存在自然断层：上一段结尾【{prev_node.conclusion}】，下一段开头【{curr_node.premise}】。
请写一段过渡剧情，通过心理活动、情绪变化或环境细节将两个场景无缝连接。
{emotion_hint}{style_block}
严禁使用生硬转折词，不要重复前文内容，让过渡自然流畅。
输出格式必须严格如下：
【中文】
（180-260字中文过渡剧情）

【English】
(160-240 English words, faithful translation, natural English)"""
            else:
                prompt = f"""你是顶级小说情节逻辑架构师。
作者大纲存在自然断层：上一段结尾【{prev_node.conclusion}】，下一段开头【{curr_node.premise}】。
请写一段200字左右的过渡剧情，通过心理活动、情绪变化或环境细节将两个场景无缝连接。
{emotion_hint}{style_block}
严禁使用生硬转折词，不要重复前文内容，让过渡自然流畅。"""
            return self.llm_provider.generate(prompt, temperature=0.7, max_tokens=8000)
        return self._call_llm_for_node(curr_node, chapter)

    def _apply_state_change(self, key: str, value: Any) -> None:
        parts = key.split(".")
        obj: Any = self.global_state
        for part in parts[:-1]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            elif isinstance(obj, dict):
                obj = obj.setdefault(part, {})
            elif isinstance(obj, list) and part.lstrip("-").isdigit():
                idx = int(part)
                if idx >= len(obj):
                    obj.extend([{}] * (idx - len(obj) + 1))
                obj = obj[idx]
            else:
                raise KeyError(f"无法解析路径: {key}")
        last = parts[-1]
        if isinstance(obj, dict):
            obj[last] = value
        elif hasattr(obj, last):
            setattr(obj, last, value)
        else:
            raise KeyError(f"无法设置属性 {last} 在 {type(obj)}")

    def generate_novel(
        self, chapter_plans: List[Chapter], output_path: str = "audit_report.html"
    ) -> str:
        full = f"# {self.novel_title}\n\n"
        for ch in chapter_plans:
            content = self.render_chapter(ch)
            if content:
                full += f"## 第{ch.chapter_id}章 {ch.title}\n\n{content}\n\n"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(self.report_generator.generate(self.novel_title, self.chapters))
        return full

    # ==================== 修复通道（Review→Repair 闭环） ====================
    def repair_presentation_issues(
        self,
        text: str,
        issues: List[str],
        outline: str = "",
        characters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """对四审计发现的呈现层问题做修复：

        - 有 LLM：整段重写（注入全部叙事约束，消除问题）；
        - 无 LLM（规则降级）：按问题类型做文本替换（删解说腔词 / 删现代词台词 / 删动机归因句）。
        返回 {"rewritten": bool, "new_text": str, "diff": [...], "actions": [...]}；
        actions 为逐条修复动作（供作者逐条接受/拒绝）。
        """
        actions: List[Dict[str, Any]] = []
        new_text = text
        lang = (self.output_language or "zh").lower().strip()

        # 文风审计：把 prose 层问题也并入修复约束（有 LLM 时进入重写；无 LLM 仅暴露）
        prose_audit = self.presentation_auditor.prose_auditor.audit(text)
        prose_issues = []
        for key, val in prose_audit.items():
            if isinstance(val, dict) and not val.get("passed", True) and "hits" in val:
                for hit in val["hits"]:
                    prose_issues.append(f"[文风:{key}] {hit}")
        fix_issues = list(issues) + prose_issues

        if self.llm_provider is not None:
            issue_text = "\n".join(fix_issues) if fix_issues else "未发现具体问题，请整体提升叙事质量"
            style_hint = self._style_instruction()
            style_block = (
                f"\n文体风格约束（必须严格遵守）：\n{style_hint}\n"
                if style_hint
                else ""
            )
            if lang in ("en", "english"):
                prompt = f"""You are a master editor for web fiction.
Rewrite the passage below to fix these narration issues:
{issue_text}
Rules: chronicler perspective (no omniscient narration, no motive explanation, record only visible actions and heard words); dialogues must fit era, knowledge, and register.
{style_block}
Passage:
{text}
Output the revised passage only."""
            else:
                prompt = f"""你是一名资深网文编辑。
请重写下面的段落，修复以下叙事呈现问题：
{issue_text}
要求：
1. 史官旁观视角——只记可见行动、可闻话语，不替角色解释内心动机；
2. 禁止全知解说腔（殊不知/原来/事实上等向读者讲设定的句子）；
3. 台词符合时代、符合角色认知边界、符合角色语域；
4. 保持人物性格、情节与原有信息量不变。
{style_block}
原文：
{text}
只输出重写后的正文。"""
            try:
                resp = self.llm_provider.generate(
                    prompt, temperature=0.6, max_tokens=8000
                )
                if resp and resp.strip():
                    actions.append(
                        {
                            "type": "llm_rewrite",
                            "target": "整段",
                            "accepted": None,  # 待作者确认
                        }
                    )
                    return {
                        "rewritten": True,
                        "new_text": resp.strip(),
                        "diff": [("REWRITE", text[:40] + "…", resp.strip()[:40] + "…")],
                        "actions": actions,
                        "prose_style": prose_audit,
                    }
            except Exception:
                pass  # 降级到规则修复

        # —— 规则降级修复（无 LLM 或 LLM 失败）——
        # 1) 删全知解说腔词
        for w in _OMNISCIENT_PATTERNS:
            if w in new_text:
                new_text = new_text.replace(w, "")
                actions.append({"type": "remove_omniscient", "target": w, "accepted": None})
        # 2) 删动机归因句（他之所以…是因为… / 她内心真正…是…）
        for pat in _EXPLAIN_MOTIVE_PATTERNS:
            m = pat.search(new_text)
            if m:
                seg = m.group(0)
                new_text = new_text.replace(seg, "")
                actions.append({"type": "remove_motive_explanation", "target": seg[:20], "accepted": None})
        # 3) 台词时代穿越：整句台词替换为省略号（保留对话结构，抹掉现代词；现代题材豁免）
        wr = self.global_state.world_rules or {}
        sp = wr.get("style_profile") or {}
        genre = sp.get("genre") if isinstance(sp, dict) else ""
        modern_setting = bool(wr.get("modern_setting")) or genre in {"都市", "科幻", "现代", "悬疑", "末世", "游戏", "星际", "赛博"}
        forbidden = [] if modern_setting else list(_ERA_FORBIDDEN_DEFAULT)
        if isinstance(wr.get("era_forbidden_words"), list):
            forbidden.extend(wr["era_forbidden_words"])
        for d in _extract_dialogues(new_text):
            if any(w in d for w in forbidden):
                new_text = new_text.replace(d, "……")
                actions.append({"type": "mask_dialogue", "target": d[:24], "accepted": None})
        # 4) 语域漂移：命中他人专属词的台词，抹掉该词（保留句子）
        if characters:
            registry_map = {}
            for name, prof in characters.items():
                prof = prof or {}
                hints = prof.get("register_hints")
                if isinstance(hints, list) and hints:
                    registry_map[name] = hints
            word_owner = {}
            for owner, hints in registry_map.items():
                for w in hints:
                    if w and w not in word_owner:
                        word_owner[w] = owner
            for d in _extract_dialogues(new_text):
                pos = new_text.find(d)
                if pos < 0:
                    continue
                window = new_text[max(0, pos - 60) : pos]
                speaker = None
                last_pos = -1
                for name in characters:
                    p = window.rfind(name)
                    if p > last_pos:
                        speaker, last_pos = name, p
                if not speaker:
                    continue
                for w, owner in word_owner.items():
                    if w in d and owner != speaker:
                        new_text = new_text.replace(w, "")
                        actions.append({"type": "remove_registry_leak", "target": w, "accepted": None})
        changed = new_text != text
        return {
            "rewritten": changed,
            "new_text": new_text,
            "diff": [("EDIT", text[:40] + "…", new_text[:40] + "…")] if changed else [],
            "actions": actions,
            "prose_style": prose_audit,
        }

    # ==================== 推演模式（Simulate） ====================
    def simulate_chapter(
        self,
        outline: str,
        chapter_title: str = "",
        characters: Optional[Dict[str, Any]] = None,
        max_rewrites: int = 2,
    ) -> Dict[str, Any]:
        """推演模式：大纲 → 成文（带全套叙事约束）→ 自动过审 → 不达标重写（≤max_rewrites 次）。

        返回 {"chapter": Chapter|None, "text": str, "audit": dict, "rewrite_count": int, "passed": bool}
        """
        if characters is not None:
            # 推演前注入作者确认的角色档案（含 register_hints / knowledge / forbidden_knowledge）
            self.global_state.characters.update(characters)
        if not chapter_title:
            chapter_title = "推演章节"
        # 用现有生成管线成文：先 plan（大纲→节点+规划审计），再 render（节点扩写+审计）
        ch = self.create_chapter_from_outline(1, chapter_title, outline)
        if ch is None:
            return {"chapter": None, "text": "", "audit": None, "rewrite_count": 0, "passed": False}
        rendered = self.render_chapter(ch)
        text = rendered if isinstance(rendered, str) else (ch.content or "")
        # 自动过审
        audit = self.audit_text(
            text, outline=outline, characters=self.global_state.characters
        )
        rewrite_count = 0
        # 不达标且有 LLM → 修复重写，最多 max_rewrites 次
        while not audit["all_passed"] and self.llm_provider is not None and rewrite_count < max_rewrites:
            issues = []
            pres = audit["presentation"]
            for k in ("narration_perspective", "dialogue_era", "dialogue_cognition", "dialogue_registry"):
                issues += pres.get(k, {}).get("issues", [])
            repair = self.repair_presentation_issues(
                text, issues, outline=outline, characters=self.global_state.characters
            )
            if not repair["rewritten"]:
                break
            text = repair["new_text"]
            rewrite_count += 1
            audit = self.audit_text(
                text, outline=outline, characters=self.global_state.characters
            )
        return {
            "chapter": ch,
            "text": text,
            "audit": audit,
            "rewrite_count": rewrite_count,
            "passed": bool(audit["all_passed"]),
        }

    # 新增辅助方法：从自然语言大纲直接创建章节
    def create_chapter_from_outline(
        self, chapter_id: int, title: str, outline: str
    ) -> Optional[Chapter]:
        nodes = parse_outline_to_nodes(outline)
        if not nodes:
            return None
        # 自动设置角色（如果节点中没有character，尝试提取）
        for node in nodes:
            if not node.character:
                node.character = extract_character_from_text(
                    node.premise + node.conclusion
                )
        # 将所有节点放入一个 CausalLine（角色可以混合，但建议按角色分组，这里简化）
        line = CausalLine(
            line_id=f"ch{chapter_id}",
            character=nodes[0].character if nodes else "主角",
            nodes=nodes,
        )
        return self.plan_chapter(chapter_id, title, [line])

    def audit_prose(
        self, text: str, use_llm: bool = True, names: Optional[Any] = None
    ) -> Dict[str, Any]:
        """上游审计入口：直接消费「原文散文」，走 叙事剥离 → 五步算子（+可选 LLM 深诊）。

        与 audit_story(outline=...) 的分工：后者要求「A -> B」箭头式大纲；
        本方法消费自然散文（小说原文），是对齐「上游空」缺口的最小可用路径。
        names：可选已知角色姓名集（如 prose_bridge.build_name_set 的输出），
               注入后角色归属走词表，准确率显著高于内置正则。
        返回链 + 脆弱性判决 + 责任锚 + 重建建议（字段与 audit_story 的 causal 层一致）。
        """
        chain = self.sp_engine.narrative_stripping(text, names=names)
        self.sp_engine.implicit_assumption_probe(chain)
        hedge = self.sp_engine.vulnerability_hedge(chain)
        anchor = self.sp_engine.responsibility_anchor(chain)
        recon = self.sp_engine.causal_reconstruction(
            chain, fix_vars=[], target_state="叙事逻辑自洽"
        )
        deep = (
            self.sp_engine.deep_diagnose(chain, self.world_builder.world_rules)
            if use_llm
            else None
        )
        return {
            "event_count": len(chain),
            "chain": chain,
            "collapse_verdict": hedge["collapse_verdict"],
            "weakest_variable": hedge["weakest_variable"],
            "anchors": anchor,
            "reconstruction": recon,
            "deep": deep,
        }

    def conceive_world(self, outline: str) -> Dict[str, Any]:
        """构思世界观：从自然语言提纲生成势力/地理/法则/时间线骨架，并写入全局 world_rules。"""
        self.world_builder.generate_skeleton(outline)
        self.global_state.world_rules.update(self.world_builder.world_rules)
        return self.world_builder.world_rules

    def recognize_style(
        self, text: str = "", chapters: List[Chapter] = None, outline: str = ""
    ) -> Dict[str, Any]:
        """文体风格自动识别（接入 StyleRecognizer）。

        两种用法：
          1. recognize_style(text=导入的一段文本)         → 识别单段/单文档文体
          2. recognize_style(chapters=已渲染章节, outline=大纲) → 识别整部作品基调
        识别结果写入 world_rules["style_profile"]，供后续生成提示词按文体微调。
        """
        # 章节非空 → 整部作品基调；否则走单段/大纲识别
        if chapters:
            full = "\n".join(
                [(c.content or "") for c in chapters if getattr(c, "content", None)]
            )
            profile = StyleRecognizer.analyze_work(full, outline)
            profile["scope"] = "whole_work"
        else:
            profile = StyleRecognizer.analyze(text or outline)
            profile["scope"] = "segment"
        self.global_state.world_rules["style_profile"] = profile
        return profile

    def _style_instruction(self) -> str:
        """生成期文体约束（A+B）：优先读取 STYLE_PRESETS[target_style] 生成结构化约束；
        未指定文风时回退到 world_rules.style_profile（向后兼容 StyleRecognizer）。"""
        style = self.target_style
        if not style:
            profile = (self.global_state.world_rules or {}).get("style_profile") or {}
            style = profile.get("style")
        if style:
            preset = STYLE_PRESETS.get(style)
            if preset:
                lines = [
                    f"目标文风：{preset.get('label_zh', '')}（{preset.get('label_en', '')}）",
                    f"句式：{preset.get('sentence', '')}",
                    f"修辞：{preset.get('rhetoric', '')}",
                    f"视角：{preset.get('pov', '')}",
                ]
                if preset.get("encourage"):
                    lines.append("鼓励使用的词汇/意象：" + "、".join(preset["encourage"]))
                if preset.get("forbidden"):
                    lines.append("严禁出现的词汇（语域漂移）：" + "、".join(preset["forbidden"]))
                if preset.get("sample"):
                    lines.append("风格示例：" + preset["sample"])
                return "\n".join(lines)
        # 回退：既有世界规则风格档案
        profile = (self.global_state.world_rules or {}).get("style_profile") or {}
        return StyleRecognizer.style_guidelines(profile)

    # ==================== 角色档案自动提取 ====================
    def extract_character_profiles(
        self, text: str
    ) -> Dict[str, Dict[str, Any]]:
        """从正文提取角色档案候选（register_hints / knowledge），不写入全局状态。"""
        return extract_character_profiles(text)

    # ==================== 审稿模式（Review）公共入口 ====================
    def audit_text(
        self,
        text: str,
        outline: str = "",
        characters: Optional[Dict[str, Any]] = None,
        narration_mode: Optional[str] = None,
        include_causal: bool = True,
        diff_only: bool = False,
        known_names: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """对已有文本/大纲做三层审计，输出完整报告。

        层1 因果层（五步算子）：对大纲事件链做脆弱性/责任/收敛判定
        层2 叙事呈现层（四审计）：史官旁观 / 台词时代 / 台词认知 / 台词语域
        层3 逻辑一致性（已有插件）：逻辑跳跃 / 前提-结论匹配（对文本拆句触发）
        新增层4 伏笔台账 + 时空校验（P0/P1，决定论）
        新增层5 哈希链存证（P2，可信审计）

        参数：
          text: 待审文本（正文或大纲）
          outline: 可选，因果链来源（优先于从 text 拆解）
          characters: 角色档案（knowledge/forbidden_knowledge/register_hints/aliases）
          narration_mode: 叙事立场覆盖；None 时按 outline 关键词推断
          include_causal: 是否跑五步算子因果层
          diff_only: 增量审计模式（P1）——仅对本次传入的 text 做检查，跳过已累积的
                     全局状态重算，适合编辑单章/碎片的"实时守门"短路径。
          known_names: 已知角色名/别称表；用于 prose_style 的人名豁免与说话人归属。
                      红楼梦等别称密集文本传入后可消除言语标记公式类误报。
        返回：结构化报告（含 all_passed 汇总 + 伏笔/时空/哈希字段）。
        """
        char_map = characters or self.global_state.characters
        # —— 层2 叙事呈现层（对正文文本）——
        presentation = self.presentation_auditor.audit(
            text=text,
            characters=char_map or None,
            narration_mode=narration_mode,
            outline=outline,
            style_family=self._style_family(),
            known_names=known_names,
        )
        # —— 层1 因果层（五步算子，对大纲/事件链）——
        causal = None
        if include_causal:
            src = outline or text
            events = parse_outline_to_nodes(src)
            chain = self.sp_engine.narrative_stripping(
                [
                    {
                        "id": n.node_id,
                        "premise": n.premise,
                        "conclusion": n.conclusion,
                        "character": n.character,
                    }
                    for n in events
                ]
            )
            self.sp_engine.implicit_assumption_probe(chain)
            sp_hedge = self.sp_engine.vulnerability_hedge(chain)
            sp_anchor = self.sp_engine.responsibility_anchor(chain)
            sp_recon = self.sp_engine.causal_reconstruction(
                chain, fix_vars=[], target_state="叙事逻辑自洽"
            )
            sp_deep = self.sp_engine.deep_diagnose(chain, self.world_builder.world_rules)
            causal = {
                "chain": chain,
                "collapse_verdict": sp_hedge["collapse_verdict"],
                "weakest_variable": sp_hedge["weakest_variable"],
                "anchors": sp_anchor,
                "reconstruction": sp_recon,
                "deep": sp_deep,
            }
        # —— 层3 逻辑一致性（文本拆句触发节点审计）——
        logical = None
        if text:
            logical = self.node_auditor.audit(
                {"text": text, "global_state": asdict(self.global_state)}
            )
        # —— 增量审计（P1）：diff_only 时跳过全局重审，直接产出聚合报告 ——
        if diff_only:
            return self._build_audit_report(
                presentation=presentation,
                causal=causal,
                logical=logical,
                nodes=None,
                run_ledger_scan=False,
            )
        # —— 层4 伏笔台账 + 时空校验（P0/P1）——
        events_nodes = parse_outline_to_nodes(outline or text)
        ledger_all_passed = True
        spacetime = None
        if events_nodes:
            self.foreshadow_ledger.scan_nodes(events_nodes)
            ledger = self.foreshadow_ledger.reconcile()
            ledger_all_passed = ledger["all_closed"]
            spacetime = audit_spacetime_consistency(events_nodes)
        # —— 汇总 ——
        pres_passed = self.presentation_auditor.all_passed(
            {"presentation": presentation}
        )
        causal_passed = (
            causal is None
            or (causal["collapse_verdict"] == "STABLE" and causal["reconstruction"]["converged"])
        )
        logical_passed = logical is None or bool(logical.get("overall_passed"))
        spacetime_passed = spacetime is None or bool(spacetime["passed"])
        all_passed = (
            pres_passed
            and causal_passed
            and logical_passed
            and ledger_all_passed
            and spacetime_passed
        )
        report = {
            "presentation": presentation,
            "causal": causal,
            "logical": logical,
            "foreshadow": {
                "ledger": self.foreshadow_ledger.reconcile()
            },
            "spacetime": spacetime,
            "all_passed": all_passed,
        }
        return self._stamp_audit_hash(report)

    def _build_audit_report(
        self,
        presentation: Dict[str, Any],
        causal: Optional[Dict[str, Any]],
        logical: Optional[Dict[str, Any]],
        nodes: Optional[List[CausalNode]],
        run_ledger_scan: bool,
    ) -> Dict[str, Any]:
        """增量（diff-only）聚合，跳过全局重审。"""
        pres_passed = self.presentation_auditor.all_passed(
            {"presentation": presentation}
        )
        causal_passed = (
            causal is None
            or (causal["collapse_verdict"] == "STABLE" and causal["reconstruction"]["converged"])
        )
        logical_passed = logical is None or bool(logical.get("overall_passed"))
        spacetime = None
        if nodes:
            spacetime = audit_spacetime_consistency(nodes)
        spacetime_passed = spacetime is None or bool(spacetime["passed"])
        ledger_passed = True
        if run_ledger_scan and nodes:
            self.foreshadow_ledger.scan_nodes(nodes)
            ledger_passed = self.foreshadow_ledger.reconcile()["all_closed"]
        report = {
            "presentation": presentation,
            "causal": causal,
            "logical": logical,
            "foreshadow": {"ledger": self.foreshadow_ledger.reconcile()},
            "spacetime": spacetime,
            "diff_only": True,
            "all_passed": pres_passed and causal_passed and logical_passed
            and spacetime_passed and ledger_passed,
        }
        return self._stamp_audit_hash(report)

    def _stamp_audit_hash(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """P2 哈希链存证：把本块报告串进引擎级哈希链，输出该块哈希与前驱哈希。

        哈希前先剥离随机字段（见 _strip_nondeterminism）——否则载荷中的
        uuid4/uuid1 派生值会让同一文本重复审计得到不同哈希，哈希链失去取证价值。
        """
        report["audit_hash"] = _hash_block(
            self.audit_chain_prefix, _strip_nondeterminism(report)
        )
        report["audit_prev_hash"] = self.audit_chain_prefix
        self.audit_chain_prefix = report["audit_hash"]
        return report


# =============================================================================
# 第二视角因果推理引擎 V2.1（决定论内核，无概率化推测）
# 五步算子：叙事剥离 → 内隐假设透视 → 脆弱性对冲 → 责任闭环锚定 → 因果重构
# 与 business 引擎内联同一份内核，确保两引擎逻辑口径一致。
# =============================================================================
class SecondPerspectiveCausalEngine:
    """决定论因果推理：仅做因果链的结构性判定，不输出概率估计。"""

    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.llm_provider = llm_provider

    _COLOCATION_HINTS = _LZ._COLOCATION_HINTS
    _MOTION_HINTS = _LZ._MOTION_HINTS
    _COMMS_HINTS = _LZ._COMMS_HINTS
    _JUMP_HINTS = _LZ._JUMP_HINTS

    @staticmethod
    def _coerce_events(events, names: Optional[Any] = None) -> List[Dict[str, Any]]:
        """把多种上游输入统一成事件字典列表（类型兼容层）。

        修复「中游断」：旧版只吃 List[dict]，若直接喂原文（str）会按「字符」迭代成垃圾。
        现兼容：None / str（整段散文）/ List[str] / dict / List[dict] /
        CausalNode / List[CausalNode]；names 为可选的已知角色姓名集（用于角色归属）。
        """
        if events is None:
            return []
        if isinstance(events, str):
            return NarrativeStripper.to_events(events, names=names)
        if isinstance(events, CausalNode):
            events = [events]
        elif isinstance(events, dict):
            events = [events]
        out: List[Dict[str, Any]] = []
        for ev in events:
            if isinstance(ev, dict):
                out.append(dict(ev))
            elif isinstance(ev, CausalNode):
                out.append(
                    {
                        "id": getattr(ev, "node_id", "") or f"E{len(out):03d}",
                        "premise": getattr(ev, "premise", ""),
                        "conclusion": getattr(ev, "conclusion", ""),
                        "character": getattr(ev, "character", ""),
                    }
                )
            elif isinstance(ev, str):
                out.extend(
                    NarrativeStripper.to_events(ev, start_id=len(out), names=names)
                )
            else:
                # 未知类型：尽力取通用字段，避免静默丢链
                out.append(
                    {
                        "id": getattr(ev, "id", f"E{len(out):03d}"),
                        "premise": getattr(ev, "premise", ""),
                        "conclusion": getattr(ev, "conclusion", ""),
                        "character": getattr(ev, "character", ""),
                    }
                )
        return out

    def narrative_stripping(self, events, names: Optional[Any] = None):
        coerced = self._coerce_events(events, names)
        # 人物出场频次预统计（修正「悬空」定义）：角色在链内首次出现是正常引入，
        # 旧版把首现也判为悬空，导致红楼梦这类群像登场章节（第 003 回引入
        # 贾母/王夫人/邢夫人/李纨/熙凤等数十人）整章被判 INEVITABLE_COLLAPSE。
        # 新定义：仅当人物在全链中只出现一次、且不在前提句中时，才判悬空。
        char_freq: Dict[str, int] = {}
        for ev in coerced:
            c = ev.get("character") or ""
            if c:
                char_freq[c] = char_freq.get(c, 0) + 1
        chain = []
        for i, ev in enumerate(coerced):
            ev = dict(ev)
            ev.setdefault("id", f"E{i:03d}")
            premise, conclusion = ev.get("premise", ""), ev.get("conclusion", "")
            char = ev.get("character") or ""
            # 严格词表模式（提供了 names）下不做正则兜底，未知角色留空由上游判定
            if not char and not names:
                char = self._infer_character(premise + conclusion)
            ev["character"] = char
            ev["dangling"] = (
                bool(char)
                and (i > 0)
                and (char not in premise)
                and char_freq.get(char, 0) <= 1
            )
            chain.append(ev)
        return chain

    def implicit_assumption_probe(self, chain):
        for ev in chain:
            text = ev.get("premise", "") + ev.get("conclusion", "")
            assumptions = []
            if any(h in text for h in self._COLOCATION_HINTS):
                assumptions.append(
                    {
                        "content": "角色共处同一物理时空，场景自洽",
                        "reverse_check": "撤除：角色不在同一时空 → 位移类行为失去前提",
                        "collapse": "INEVITABLE"
                        if any(
                            m in ev.get("conclusion", "") for m in self._MOTION_HINTS
                        )
                        else "STABLE",
                    }
                )
            if any(h in text for h in self._COMMS_HINTS):
                assumptions.append(
                    {
                        "content": "角色间存在生效的通讯连接手段",
                        "reverse_check": "撤除：无通讯手段 → 通讯类行为不成立",
                        "collapse": "INEVITABLE"
                        if any(h in ev.get("conclusion", "") for h in self._COMMS_HINTS)
                        else "STABLE",
                    }
                )
            ev["assumptions"] = assumptions
        return chain

    def vulnerability_hedge(self, chain):
        weakest, weakest_score = None, -1.0
        for ev in chain:
            frag = sum(
                1 for a in ev.get("assumptions", []) if a["collapse"] == "INEVITABLE"
            )
            if ev.get("dangling"):
                frag += 2
            ev["fragility"] = frag
            if frag > weakest_score:
                weakest_score, weakest = frag, ev
        if weakest is None:
            verdict = "STABLE"
        elif weakest_score >= 2:
            verdict = "INEVITABLE_COLLAPSE"
        elif weakest_score == 1:
            verdict = "CONDITIONAL_COLLAPSE"
        else:
            verdict = "STABLE"
        return {
            "weakest_variable": weakest["id"] if weakest else None,
            "weakest_event": weakest,
            "collapse_verdict": verdict,
            "chain_fragility": [
                {"id": e["id"], "fragility": e.get("fragility", 0)} for e in chain
            ],
        }

    def responsibility_anchor(self, chain):
        anchors = []
        for idx, ev in enumerate(chain):
            char = ev.get("character", "")
            action = self._extract_action(ev.get("conclusion", ""))
            anchors.append(
                {
                    "event_id": ev["id"],
                    "position": idx,
                    "accountable": char,
                    "decision_unit": f"{char}→{action}" if char else action,
                    "premise": ev.get("premise", ""),
                    "conclusion": ev.get("conclusion", ""),
                }
            )
        return anchors

    def causal_reconstruction(self, chain, fix_vars, target_state):
        fixed_ids = set()
        for ev in chain:
            for fix in fix_vars or []:
                if ev["id"] == fix.get("target_id") or fix.get("apply_to") == "all":
                    ev["premise"] = (
                        ev["premise"] + "；" + fix.get("adds_premise", "")
                    ).strip("；")
                    ev["dangling"] = False
                    fixed_ids.add(ev["id"])
        residual = []
        for ev in chain:
            if ev.get("dangling") and ev["id"] not in fixed_ids:
                residual.append(f"事件{ev['id']}结论缺前提支撑")
            for a in ev.get("assumptions", []):
                if a["collapse"] == "INEVITABLE" and not fix_vars:
                    residual.append(f"事件{ev['id']}关键预设不可逆撤除")
        if residual:
            return {
                "converged": False,
                "diagnosis": "[中断：因果链未收敛] " + "；".join(residual),
                "fixed_ids": list(fixed_ids),
            }
        return {
            "converged": True,
            "target_state": target_state,
            "diagnosis": f"因果链收敛至目标稳态：{target_state}",
            "fixed_ids": list(fixed_ids),
        }

    def _infer_character(self, text):
        """兜底角色推断：仅接受可信人名候选；场景/天气/动词短语（如「下雨了」）不再被误认为角色名。"""
        return _extract_plausible_name(text)

    def deep_diagnose(
        self, chain: List[Dict[str, Any]], world_rules: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """注入 LLM 时，把整段因果链 + 世界观规则交给 LLM 做语义级深度诊断；否则返回 None（由调用方降级到五步规则）。"""
        if self.llm_provider is None:
            return None
        chain_json = json.dumps(chain, ensure_ascii=False)
        rules_json = json.dumps(world_rules, ensure_ascii=False)
        prompt = f"""你是决定论因果审计引擎。给定因果链与世界规则，请做语义级深度诊断。
因果链：{chain_json}
世界规则：{rules_json}
请严格输出 JSON：
{{"weakest_variable": <事件id或null>, "inevitable_assumptions": [<str>], "responsibility_anchors": [<str>], "reconstruction_advice": <str>, "collapse_verdict": "INEVITABLE_COLLAPSE|CONDITIONAL_COLLAPSE|STABLE"}}"""
        try:
            resp = self.llm_provider.generate(prompt, temperature=0.2, max_tokens=2000)
            data = json.loads(resp)
            data["deep"] = True
            return data
        except Exception:
            return None

    def _extract_action(self, conclusion):
        for w in self._MOTION_HINTS + self._COMMS_HINTS:
            if w in conclusion:
                return w
        return conclusion[:12]


# =============================================================================
# 叙事呈现层审计（移植自 story-engine-chrome-v2.0.0 engine.js）
# 总纲：旁观历史视角——叙述者如史官，只记看见的行动、听见的话，不替角色解释内心；
#      禁全知——不跳出叙事向读者讲设定（防解说腔）；台词审计——时代/认知/语域三层。
# 提供：四审计 + 叙事立场推断（chronicler/limited/omniscient）
# =============================================================================

# 叙事立场关键词推断
_NARRATION_CHRONICLER_KW = _LZ._NARRATION_CHRONICLER_KW
_NARRATION_LIMITED_KW = _LZ._NARRATION_LIMITED_KW
_NARRATION_OMNISCIENT_KW = _LZ._NARRATION_OMNISCIENT_KW

# 全知解说腔 / 动机归因模式
_OMNISCIENT_PATTERNS = _LZ._OMNISCIENT_PATTERNS
_EXPLAIN_MOTIVE_PATTERNS = _LZ._EXPLAIN_MOTIVE_PATTERNS
# 允许的有限心理描写词（史官视角下可保留，不算动机归因）
_ALLOWED_PSYCH = _LZ._ALLOWED_PSYCH
# 台词时代默认禁用词（现代词，可经 world_rules.era_forbidden_words 扩展）
# 仅保留“时代错位感极强”的词：古风/仙侠/西幻文里出现会瞬间出戏；
# 商业/都市/科幻题材经 modern_setting 豁免，作者可显式补充 era_forbidden_words 强制生效。
_ERA_FORBIDDEN_DEFAULT = _LZ._ERA_FORBIDDEN_DEFAULT

# 台词提取（支持三种引号）
_DIALOGUE_RES = _LZ._DIALOGUE_RES


def infer_narration_mode(outline: str) -> Optional[str]:
    """从大纲关键词推断叙事立场；平手或零命中返回 None。"""
    if not outline:
        return None
    scores = {
        "chronicler": sum(1 for w in _NARRATION_CHRONICLER_KW if w in outline),
        "limited": sum(1 for w in _NARRATION_LIMITED_KW if w in outline),
        "omniscient": sum(1 for w in _NARRATION_OMNISCIENT_KW if w in outline),
    }
    best = max(scores, key=scores.get)
    winners = [k for k in scores if scores[k] == scores[best]]
    return best if (len(winners) == 1 and scores[best] > 0) else None


def _extract_dialogues(text: str) -> List[str]:
    if not text:
        return []
    out: List[str] = []
    for re_pat in _DIALOGUE_RES:
        for m in re_pat.finditer(text):
            d = (m.group(1) or "").strip()
            if d:
                out.append(d)
    return out


def audit_narration_perspective(
    text: str, narration_mode: Optional[str]
) -> Dict[str, Any]:
    """史官旁观 / 禁全知（narration_mode 三档）。"""
    mode = narration_mode or "chronicler"
    if mode == "omniscient":
        return {
            "passed": True,
            "score": 100,
            "issues": [],
            "allowed_psych_hits": [],
            "note": "全知叙事模式：跳过史官视角检查",
        }
    issues: List[str] = []
    if mode == "chronicler":
        for w in _OMNISCIENT_PATTERNS:
            if w in text:
                issues.append(f"全知解说腔：出现'{w}'（叙述者跳出视角向读者讲设定）")
    for pat in _EXPLAIN_MOTIVE_PATTERNS:
        m = pat.search(text)
        if m:
            issues.append(f"动机归因：'{m.group(0)[:20]}…'（史官视角禁替角色解释内心）")
    psych_hits = [w for w in _ALLOWED_PSYCH if w in text]
    score = max(0, 100 - len(issues) * 25)
    return {
        "passed": len(issues) == 0,
        "score": score,
        "issues": issues,
        "allowed_psych_hits": psych_hits,
        "note": "叙事立场=" + mode + "：禁止动机归因"
        + ("；禁止全知解说" if mode == "chronicler" else "；放宽全知解说"),
    }


def audit_dialogue_era(
    text: str, world_rules: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """台词时代（现代词黑名单 + world_rules.era_forbidden_words 扩展）。

    题材感知：若 world_rules 声明了现代/都市/科幻题材（style_profile.genre 或
    world_rules.modern_setting=True），默认黑名单整体豁免（现代词在此类题材中合法）；
    作者显式配置的 era_forbidden_words 仍强制生效。
    """
    dialogues = _extract_dialogues(text)
    if not dialogues:
        return {"passed": True, "score": 100, "issues": [], "note": "无台词，跳过时代审计"}
    wr = world_rules or {}
    # 题材豁免判断
    modern_genres = {"都市", "科幻", "现代", "悬疑", "末世", "游戏", "星际", "赛博"}
    genre = ""
    sp = wr.get("style_profile") or {}
    if isinstance(sp, dict):
        genre = sp.get("genre") or ""
    modern_setting = bool(wr.get("modern_setting")) or genre in modern_genres
    forbidden = [] if modern_setting else list(_ERA_FORBIDDEN_DEFAULT)
    if isinstance(wr.get("era_forbidden_words"), list):
        forbidden.extend(wr["era_forbidden_words"])
    if not forbidden:
        return {
            "passed": True,
            "score": 100,
            "issues": [],
            "note": "现代题材：默认黑名单豁免",
            "modern_setting": modern_setting,
        }
    issues: List[str] = []
    for d in dialogues:
        for w in forbidden:
            if w in d:
                issues.append(f"台词时代穿越：台词「{d[:24]}…」出现现代词'{w}'")
                break
    score = max(0, 100 - len(issues) * 15)
    return {
        "passed": len(issues) == 0,
        "score": score,
        "issues": issues,
        "dialogues_checked": len(dialogues),
        "modern_setting": modern_setting,
    }


def _build_alias_index(characters: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """token → 规范角色名；包含角色本名与 profiles 中的 aliases 别称。

    红楼梦类文本别称密集（宝钗/薛宝钗/宝姐姐/蘅芜君），仅按本名匹配会把
    别称处的台词判为「说话人不明」而整体跳过认知/语域审计。
    """
    idx: Dict[str, str] = {}
    for name in (characters or {}):
        idx[name] = name
        prof = (characters or {}).get(name) or {}
        aliases = prof.get("aliases")
        if isinstance(aliases, list):
            for a in aliases:
                if a and a not in idx:
                    idx[a] = name
    return idx


def _find_speaker_in_window(window: str, alias_index: Dict[str, str]) -> Optional[str]:
    """在台词前文窗口内找最近的说话人 token（支持别称），返回规范角色名。"""
    speaker, last_pos = None, -1
    for token, canonical in alias_index.items():
        p = window.rfind(token)
        if p > last_pos:
            speaker, last_pos = canonical, p
    return speaker


def audit_dialogue_cognition(
    text: str,
    characters: Optional[Dict[str, Any]],
    events: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """台词认知（角色只说己知之事；forbidden_knowledge / knowledge）。"""
    dialogues = _extract_dialogues(text)
    if not dialogues:
        return {"passed": True, "score": 100, "issues": [], "note": "无台词，跳过认知审计"}
    issues: List[str] = []
    # 说话人候选 = 角色档案 keys + 事件链推断角色；档案缺省时用空 profile 兜底，
    # 保证仅靠事件链也能完成说话人归属（认知校验需要档案才有内容）。
    char_profiles: Dict[str, Any] = dict(characters or {})
    if events:
        for ev in events:
            if ev.get("character") and ev["character"] not in char_profiles:
                char_profiles[ev["character"]] = {}
    # 说话人候选含别称：仅当 token 确实出现在文本中才纳入
    alias_index = {t: c for t, c in _build_alias_index(char_profiles).items() if t in text}
    for d in dialogues:
        d_pos = text.find(d)
        if d_pos < 0:
            continue
        window = text[max(0, d_pos - 60) : d_pos]
        speaker = _find_speaker_in_window(window, alias_index)
        if not speaker:
            continue
        profile = char_profiles.get(speaker, {}) or {}
        fk = profile.get("forbidden_knowledge")
        if isinstance(fk, list):
            for item in fk:
                if item and item in d:
                    issues.append(
                        f"认知越界：{speaker} 说出不可知信息'{item}'（台词：{d[:24]}…）"
                    )
        knowledge = profile.get("knowledge")
        if isinstance(knowledge, list) and re.search(
            r"[一二三四五六七八九十0-9]+[阶境级位]|秘密|真实身份|隐藏身份", d
        ):
            known_facts = " ".join(knowledge)
            for m in re.finditer(r"[\u4e00-\u9fa5]{2,4}[阶境级位]", d):
                if m.group(0) not in known_facts:
                    issues.append(
                        f"认知越界：{speaker} 说出'{m.group(0)}'（不在其已知知识清单）"
                    )
                    break
    score = max(0, 100 - len(issues) * 20)
    return {
        "passed": len(issues) == 0,
        "score": score,
        "issues": issues,
        "speakers_matched": len(alias_index),
    }


def audit_dialogue_registry(
    text: str, characters: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """台词语域分层（register_hints 专属词；命中他人专属词 → 语域漂移）。"""
    dialogues = _extract_dialogues(text)
    if not dialogues:
        return {"passed": True, "score": 100, "issues": [], "note": "无台词，跳过语域审计"}
    registry_map = {}
    for name, prof in (characters or {}).items():
        prof = prof or {}
        hints = prof.get("register_hints")
        if isinstance(hints, list) and hints:
            registry_map[name] = hints
    if not registry_map:
        return {
            "passed": True,
            "score": 100,
            "issues": [],
            "note": "未配置角色语域画像，跳过语域审计",
        }
    word_owner = {}
    for owner, hints in registry_map.items():
        for w in hints:
            if w and w not in word_owner:
                word_owner[w] = owner
    issues: List[str] = []
    # 说话人候选含别称（红楼梦宝姐姐/蘅芜君等），仅纳入文本中出现的 token
    alias_index = {t: c for t, c in _build_alias_index(characters).items() if t in text}
    for d in dialogues:
        pos = text.find(d)
        if pos < 0:
            continue
        window = text[max(0, pos - 60) : pos]
        speaker = _find_speaker_in_window(window, alias_index)
        if not speaker:
            continue
        for w, owner in word_owner.items():
            if w in d and owner != speaker:
                issues.append(
                    f"语域漂移：{speaker} 使用了 {owner} 的专属用语'{w}'（台词：{d[:24]}…）"
                )
    score = max(0, 100 - len(issues) * 20)
    return {
        "passed": len(issues) == 0,
        "score": score,
        "issues": issues,
        "registry_profiles": list(registry_map.keys()),
    }


class ProseStyleAuditor:
    """散文文风审计（prose-level style audit）。

    在叙事呈现层之上做逐句文风一致性审查，与 NarrativePresentationAuditor 的
    "叙事纪律"互补：前者管"以何种视角/语域叙述"，本类管"文风本身是否统一"。

    支持两套风格族基线：
      - eastern_ancient 东方古代叙事：文言/古风/章回/半文半白，容许长句、四字格、文言虚字
      - western_plain   西方朴素文风：短句、弱修辞、低成语密度，贴近白描
      - unknown / mixed 未判定或混杂（双向宽松，仅做通用检测）

    纯规则检测器（零依赖、决定论、无黑箱）：
      pov_head_hop      视角头跳：同一叙事流内感知主语逐句切换
      tense_drift       时态漂移：中文弱时态下的过去/将来标记同句共现
      redundancy        冗余赘词：虚字密度过高 / 叠字赘余
      rhythm_monotone   节奏单调：句长变异系数过低
      lexical_repeat    近距词汇复用：滑窗内实义片段重复
      register_drift    语域漂移：东方基线混现代口语；西方基线堆砌文言/成语
      show_dont_tell    抽象叙述占比过高（tell 多于 show）
    可选 LLM 辅助（仅当 llm_provider 提供，默认关闭、不计入硬失败）：
      llm.issues        病句 / 修辞一致性（概率性，标注 source="llm"）

    阈值集中在 _THRESHOLDS，按文库调参。
    """

    _CLASSICAL_CHARS = _LZ._CLASSICAL_CHARS_PSA
    _EASTERN_WORDS = _LZ._EASTERN_WORDS
    _MODERN_NETSLANG = _LZ._MODERN_NETSLANG
    _MODERN_OBJECTS = _LZ._MODERN_OBJECTS
    _PERCEPTION_VB = _LZ._PERCEPTION_VB
    _ABSTRACT_TELL = _LZ._ABSTRACT_TELL
    # 赘余对仅在现代语体族下计罚。
    # 根因：「的了」「是在」「着呢」「着的」在古白话中是合法组合（红楼梦实例：
    # 「放心的了」「或是在你舅舅处」）；「的的」在韵文中是合法形容词叠用
    # （第 005 回警幻赋「耀珠翠之的的兮」，的的=鲜明貌，120 回仅 3 次）。
    # 古典族下按子串匹配会把正常文本判为赘余（实测 5/5 章假失败），故改为族条件计罚。
    _REDUNDANT_PAIRS_MODERN = _LZ._REDUNDANT_PAIRS_MODERN
    _VIRTUAL_CHARS = _LZ._VIRTUAL_CHARS

    _THRESHOLDS = _LZ._THRESHOLDS

    def __init__(self, llm_provider=None):
        self.llm_provider = llm_provider

    # —— 风格族判定 ——
    def detect_style_family(self, text: str, target_style: Optional[str] = None) -> str:
        if target_style:
            return STYLE_PRESETS.get(target_style, {}).get("family", "unknown")
        if not text or not text.strip():
            return "unknown"
        total_han = self._han_chars(text)
        if total_han == 0:
            return "unknown"
        classical = sum(1 for c in text if c in self._CLASSICAL_CHARS)
        ancient_hit = sum(1 for w in self._EASTERN_WORDS if w in text)
        fourchar = len(re.findall(r"[\u4e00-\u9fa5]{4}", text))
        sents = self._split_sentences(text)
        fourchar_density = fourchar / max(1, len(sents))
        avg_len = total_han / max(1, len(sents))
        has_modern = any(
            w in text for w in self._MODERN_NETSLANG + self._MODERN_OBJECTS
        )
        # —— 自动识别：基于文风预设鼓励词命中，映射到具体审查族 ——
        best_fam, best_n = "unknown", 0
        for key, p in STYLE_PRESETS.items():
            n = sum(1 for w in p.get("encourage", []) if w in text)
            if n > best_n:
                best_fam, best_n = p["family"], n
        if best_n >= 2 and avg_len <= 11:
            # 诗歌族必须过「短句」闸门：韵文（诗词/赋）句长短而密集，古典叙事
            # 散文（章回小说）句长显著更长。实测四大名著均句长：三国 12.0–17.3
            # （中位 14.5）、西游记 14.9–21.9、红楼梦 16.4–24.9、水浒 17.1–29.0；
            # 而诗词/赋样本约 5–10。闸门取 11：低于它是韵文，高于它按叙事散文走
            # eastern_ancient。无此闸门时章回文本会命中 classical_poetry 的鼓励词
            # （之/乎/者/也/风/月/梦）被误路由到诗歌族，连带触发「文言堆砌」误报
            # （register_drift 假失败）。
            return best_fam
        if classical >= 8 or ancient_hit >= 2:
            return "eastern_ancient"
        if avg_len <= 22 and classical <= 2 and ancient_hit == 0 and not has_modern:
            return "western_plain"
        if has_modern and (classical >= 4 or ancient_hit >= 1):
            return "mixed"
        return "unknown"

    # —— 工具 ——
    @staticmethod
    def _split_sentences(text: str):
        return [s.strip() for s in re.split(r"[。！？!?；;]", text) if s.strip()]

    @staticmethod
    def _han_chars(text: str) -> int:
        return sum(1 for c in text if "\u4e00" <= c <= "\u9fa5")

    @staticmethod
    def _th(fam: str) -> Dict[str, Any]:
        return ProseStyleAuditor._THRESHOLDS.get(fam, ProseStyleAuditor._THRESHOLDS["unknown"])

    # 引语跨度：视角头跳只审叙述层；台词内的感知主语属角色内心，不构成 POV 跳转
    _QUOTE_SPAN_RE = _LZ._QUOTE_SPAN_RE

    @classmethod
    def _strip_quotes(cls, text: str) -> str:
        """剥掉台词跨度，仅留叙述层（用于视角头跳等叙述纪律检测）。"""
        return cls._QUOTE_SPAN_RE.sub("", text or "")

    # —— 检测器 ——
    def _detect_head_hop(self, text, fam):
        # 只审叙述层：红楼梦等对话密集文本中，「宝玉道：『我想……』」的感知
        # 主语是角色内心活动，旧版不剥引语导致第 027/097 回假失败。
        sents = self._split_sentences(self._strip_quotes(text))
        povs = []
        for i, s in enumerate(sents):
            m = re.search(r"(我|我们|他|她|他们|她们).{0,15}?(" + "|".join(self._PERCEPTION_VB) + ")", s)
            if m:
                povs.append((i, m.group(1)))
        hits = []
        for a, b in zip(povs, povs[1:]):
            if a[1] != b[1]:
                hits.append({"from": a[1], "to": b[1], "near_sentence": b[0]})
        # 容差：长篇章回中偶发的人物感知切换属正常叙事调度，仅当跳转密度
        # 过高（每 100 句 >2 次）才判失败；同时输出计数与密度供分体对照取用。
        density = len(hits) / max(1.0, len(sents) / 100.0)
        return {"passed": density <= 2.0, "hop_count": len(hits),
                "hop_density_per100": round(density, 2), "hits": hits[:10]}

    def _detect_tense(self, text, fam):
        sents = self._split_sentences(text)
        hits = []
        for i, s in enumerate(sents):
            past = ("了" in s) or ("过" in s) or ("着" in s)
            # 将来时强标记：将/即将，或「会」后接动词（避开「会议/会场」等名词）
            future = ("将" in s) or ("即将" in s) or bool(
                re.search(r"会(来|去|做|成|变|发|死|走|跑|想|说|写|看|吃|打|赢|败|裂|塌|倒|升|降|回|出|进|开|关|到|有|被|把|当|为|给|让|使|学|懂|醒|忘|记|知|明|落|散|聚|合)", s)
            )
            if past and future and not re.search(r"(次日|三年后|其后|第二天|彼时|那时|将来|此后|未几|翌日)", s):
                hits.append({"sentence_index": i, "excerpt": s[:30]})
        return {"passed": len(hits) == 0, "hits": hits[:10]}

    def _detect_redundancy(self, text, fam):
        th = self._th(fam)
        total = max(1, self._han_chars(text))
        virtual = sum(1 for c in text if c in self._VIRTUAL_CHARS)
        density = virtual / total
        pair_pool = []
        if fam in ("western_plain", "urban", "webnovel", "hardboiled", "scifi"):
            pair_pool = list(self._REDUNDANT_PAIRS_MODERN)
        pairs = [p for p in pair_pool if p in text]
        return {"passed": density <= th["virtual_density"] and not pairs,
                "metric": round(density, 3), "threshold": th["virtual_density"],
                "redundant_pairs": pairs}

    def _detect_rhythm(self, text, fam):
        th = self._th(fam)
        lens = [self._han_chars(s) for s in self._split_sentences(text)]
        if len(lens) < 5:
            return {"passed": True, "metric": None, "note": "样本不足"}
        mean = sum(lens) / len(lens)
        if mean < 15:  # 短句白描（西方朴素/海明威式）天然匀整，豁免单调判定
            return {"passed": True, "metric": None, "note": "短句白描豁免"}
        var = sum((x - mean) ** 2 for x in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        return {"passed": cv >= th["rhythm_cv"], "metric": round(cv, 3),
                "threshold": th["rhythm_cv"], "mean_len": round(mean, 1)}

    _REPEAT_MIN_FRAG = _LZ._REPEAT_MIN_FRAG
    _REPEAT_CHUNK_SENTS = _LZ._REPEAT_CHUNK_SENTS
    # 言语标记尾字/尾语：以这些结尾的片段（「又聽說道」「眾人聽了」）是章回体
    # 言语/动作标记公式，不属于文风赘余。
    _SPEECH_TAIL_CHARS = _LZ._SPEECH_TAIL_CHARS
    _SPEECH_TAIL_PHRASES = _LZ._SPEECH_TAIL_PHRASES

    def _detect_lexical_repeat(self, text, fam, known_names=None):
        th = self._th(fam)
        sents = self._split_sentences(text)
        win = th["repeat_window"]
        names = [n for n in (known_names or []) if n]
        uniq = {}
        chunks = 0
        # 修复两处历史缺陷：
        # 1) 旧版对 >4000 汉字符的文本整体跳过（"skipped_long_text"），红楼梦
        #    均章约 2100 汉字但长篇网文章节常超限，检测形同虚设；改为分块扫描。
        # 2) 旧版把窗口内多句无分隔拼接后做整串匹配，每窗只剩一个巨型片段、
        #    计数恒为 1，检测器实际不可能触发；改为逐句抽取片段后跨句计数。
        # 人名豁免：含已知角色名的片段（「寶玉笑道」「小紅聽了」）是章回体的
        # 言语/动作标记公式，不是文风赘余——传入 known_names 后跳过。
        for base in range(0, max(1, len(sents)), self._REPEAT_CHUNK_SENTS):
            chunks += 1
            block = sents[base:base + self._REPEAT_CHUNK_SENTS]
            for start in range(max(0, len(block) - win)):
                seen = {}
                for s in block[start:start + win]:
                    for frag in re.findall(r"[\u4e00-\u9fa5]{%d,}" % self._REPEAT_MIN_FRAG, s):
                        if all(c in self._VIRTUAL_CHARS for c in frag):
                            continue
                        if any(n in frag for n in names):
                            continue
                        if frag[-1] in self._SPEECH_TAIL_CHARS:
                            continue
                        if frag.endswith(self._SPEECH_TAIL_PHRASES):
                            continue
                        seen[frag] = seen.get(frag, 0) + 1
                for frag, cnt in seen.items():
                    if cnt >= 2:
                        uniq.setdefault(frag, {"fragment": frag, "count": cnt,
                                               "near_window": base + start})
        return {"passed": len(uniq) == 0, "hits": list(uniq.values())[:10],
                "chunks_scanned": chunks}

    def _detect_register_drift(self, text, fam):
        hits = []
        if fam != "western_plain":  # 非西方朴素基线：查网语漂移（古今叙事均不适）
            for w in self._MODERN_NETSLANG:
                if w in text:
                    hits.append({"type": "modern_intrusion", "token": w})
        if fam != "eastern_ancient":  # 非东方古代基线：查文言堆砌
            classical = sum(1 for c in text if c in self._CLASSICAL_CHARS)
            if classical >= 6:
                hits.append({"type": "classical_pileup", "classical_chars": classical})
        if fam in ("eastern_ancient", "mixed"):  # 古风/混杂：额外查现代物象穿越
            for w in self._MODERN_OBJECTS:
                if w in text:
                    hits.append({"type": "modern_object_intrusion", "token": w})
        return {"passed": len(hits) == 0, "hits": hits[:10]}

    def _detect_tell(self, text, fam):
        th = self._th(fam)
        sents = self._split_sentences(text)
        if not sents:
            return {"passed": True, "metric": 0}
        tell = sum(1 for s in sents if any(w in s for w in self._ABSTRACT_TELL))
        density = tell / len(sents)
        return {"passed": density <= th["tell_density"], "metric": round(density, 3),
                "threshold": th["tell_density"]}

    def _llm_check(self, text, fam):
        if not self.llm_provider:
            return {"enabled": False}
        prompt = (
            f"你是文风审查助手。给定文本（风格族：{fam}），仅列出：\n"
            "1) 病句/不通顺；2) 修辞前后不一致。\n"
            "无明显问题返回空列表。用 JSON 返回 {\"issues\":[...]}。\n\n"
            f"文本：\n{text[:2000]}"
        )
        try:
            return {"enabled": True, "source": "llm", "issues": self.llm_provider.generate(prompt)}
        except Exception:
            return {"enabled": True, "source": "llm", "error": "llm_call_failed"}

    def audit(self, text: str, style_family: Optional[str] = None,
             known_names: Optional[Any] = None) -> Dict[str, Any]:
        fam = style_family or self.detect_style_family(text)
        results = {
            "style_family": fam,
            "pov_head_hop": self._detect_head_hop(text, fam),
            "tense_drift": self._detect_tense(text, fam),
            "redundancy": self._detect_redundancy(text, fam),
            "rhythm_monotone": self._detect_rhythm(text, fam),
            "lexical_repeat": self._detect_lexical_repeat(text, fam, known_names=known_names),
            "register_drift": self._detect_register_drift(text, fam),
            "show_dont_tell": self._detect_tell(text, fam),
        }
        results["passed"] = all(
            v.get("passed", True) for k, v in results.items() if isinstance(v, dict)
        )
        failed = [k for k, v in results.items()
                  if isinstance(v, dict) and v.get("passed") is False]
        results["failed_detectors"] = failed
        # 统一 issues 出口：报告层只读 passed 会丢失可读性，这里把未通过子项
        # 聚合成 issues（指标仍在各子项里，便于回查）。
        results["issues"] = ["%s 未通过（见对应子项指标）" % k for k in failed]
        results["llm"] = self._llm_check(text, fam)  # 可选辅助，不计入硬失败
        return results


# ===================== 文风预设注册表（A+B：生成约束 + 审查族映射） =====================
# 每个预设描述一种可指定的目标文风；family 映射到 ProseStyleAuditor 的审查阈值族，
# 生成端由 _style_instruction 读取生成约束，审查端按 family 阈值校验（决定论、零依赖）。
STYLE_PRESETS = _LZ.STYLE_PRESETS


class NarrativePresentationAuditor:
    """叙事呈现层审计门面：四审计 + 立场推断 + 散文文风审计，供审稿/推演复用。"""

    def __init__(self, world_rules: Optional[Dict[str, Any]] = None, llm_provider=None):
        self.world_rules = world_rules or {}
        self.prose_auditor = ProseStyleAuditor(llm_provider)

    def infer_mode(self, outline: str) -> Optional[str]:
        return infer_narration_mode(outline)

    def audit(
        self,
        text: str,
        characters: Optional[Dict[str, Any]] = None,
        narration_mode: Optional[str] = None,
        events: Optional[List[Dict[str, Any]]] = None,
        outline: str = "",
        style_family: Optional[str] = None,
        known_names: Optional[Any] = None,
    ) -> Dict[str, Any]:
        mode = narration_mode or self.infer_mode(outline) or "chronicler"
        return {
            "narration_mode": mode,
            "narration_perspective": audit_narration_perspective(text, mode),
            "dialogue_era": audit_dialogue_era(text, self.world_rules),
            "dialogue_cognition": audit_dialogue_cognition(text, characters, events),
            "dialogue_registry": audit_dialogue_registry(text, characters),
            "prose_style": self.prose_auditor.audit(
                text, style_family=style_family, known_names=known_names
            ),
        }

    def all_passed(self, result: Dict[str, Any]) -> bool:
        pres = result.get("presentation", result)
        return all(
            pres.get(k, {}).get("passed", True)
            for k in (
                "narration_perspective",
                "dialogue_era",
                "dialogue_cognition",
                "dialogue_registry",
                "prose_style",
            )
        )


# =============================================================================
# WorldBuilder：世界观构思（势力 / 地理 / 法则 / 时间线骨架 + 一致性校验）
# =============================================================================
# —— 世界观词缀（长词在前，匹配时优先长后缀，避免「势力」被拆进地理词）——
_FACTION_SUFFIXES = ("组织", "帝国", "联邦", "公会", "势力", "族", "国", "门", "宗")
_GEO_SUFFIXES = ("大陆", "星球", "界", "域", "城", "山", "海", "渊", "境", "洲")
_LAW_SUFFIXES = ("之道", "法则", "铁则", "律令", "天条")
# 纯连接词/标点切分点：先把长句切成候选片段，避免「与魔道势力」「道势力在苍云大陆」式跨词吞字
_SEGMENT_SPLIT_RE = re.compile(r"[，。；、,.;:：！？!?\s与和及跟同向]")


def _collect_world_terms(segments: List[str], suffixes: Tuple[str, ...]) -> List[str]:
    """在每个候选片段内匹配「名字+后缀」整词；名字块内若有「的/之/在/于」等介词，
    只取最后一个介词之后的部分（「苍云大陆的青云宗」→「青云宗」）。"""
    terms: List[str] = []
    for seg in segments:
        if not seg:
            continue
        for suf in sorted(suffixes, key=len, reverse=True):
            idx = seg.rfind(suf)
            if idx < 0:
                continue
            name_part = seg[:idx]
            m = re.search(r"[\u4e00-\u9fa5]+$", name_part)
            if not m:
                if seg == suf:  # 独立词：如「天条」「法则」
                    terms.append(seg)
                continue
            name = m.group(1)
            for noise in ("的", "之", "在", "于"):
                pos = name.rfind(noise)
                if pos >= 0:
                    name = name[pos + 1 :]
                    break
            if 2 <= len(name) <= 6:
                terms.append(name + suf)
    return list(dict.fromkeys(terms))


class WorldBuilder:
    """从自然语言提纲构思世界观骨架，并维护 world_rules，供 world_rule_consistency 真实校验。"""

    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.llm_provider = llm_provider
        self.factions: List[str] = []
        self.geography: List[str] = []
        self.laws: List[str] = []
        self.timeline: List[str] = []
        self.world_rules: Dict[str, Any] = {}

    def generate_skeleton(self, outline: str) -> Dict[str, Any]:
        text = outline or ""
        segments = [s for s in _SEGMENT_SPLIT_RE.split(text) if s.strip()]
        self.factions = _collect_world_terms(segments, _FACTION_SUFFIXES)
        self.geography = _collect_world_terms(segments, _GEO_SUFFIXES)
        self.laws = _collect_world_terms(segments, _LAW_SUFFIXES)
        self.world_rules = {
            "factions": self.factions,
            "geography": self.geography,
            "laws": self.laws,
            "timeline": self.timeline,
        }
        return self.world_rules

    def add_timeline_event(self, event: str) -> None:
        self.timeline.append(event)

    def check_consistency(
        self, context: Dict[str, Any], global_state=None
    ) -> Dict[str, Any]:
        text = ""
        if isinstance(context, dict):
            text = context.get("text", "") or ""
            ch = context.get("chapter")
            if isinstance(ch, dict):
                text = text or str(ch.get("content", ""))
        if not self.factions and not self.geography and not self.laws:
            return {
                "passed": True,
                "score": 100,
                "note": "世界观骨架未构建，跳过硬性校验",
            }
        violations = []
        for fac in self.factions:
            if (
                fac in text
                and ("灭亡" in text or "覆灭" in text)
                and (fac + "仍" in text)
            ):
                violations.append(f"势力一致性冲突：{fac} 既被宣称覆灭又仍存续")
        score = max(0.0, 100.0 - len(violations) * 20)
        return {
            "passed": len(violations) == 0,
            "score": score,
            "violations": violations,
            "world_rules": self.world_rules,
        }

    def check_deep_consistency(
        self, context: Dict[str, Any], global_state=None
    ) -> Dict[str, Any]:
        """注入 LLM 时，将世界观规则 + 章节文本交给 LLM 检测设定级冲突（如凡人施法）；否则降级到 check_consistency。"""
        if self.llm_provider is None:
            return self.check_consistency(context, global_state)
        text = ""
        if isinstance(context, dict):
            text = context.get("text", "") or ""
            ch = context.get("chapter")
            if isinstance(ch, dict):
                text = text or str(ch.get("content", ""))
        if not text:
            return {
                "passed": True,
                "score": 100,
                "violations": [],
                "deep": True,
                "note": "无可检文本，跳过硬性校验",
            }
        rules_json = json.dumps(self.world_rules, ensure_ascii=False)
        prompt = f"""你是世界观一致性审计专家。
世界观规则：{rules_json}
待检文本：{text}
请检测文本是否违反世界观设定（如凡人施展需灵根者方能为之的法术、禁用之物出现、法则冲突等）。
仅输出 JSON：{{"violations": [<str>], "passed": <bool>}}"""
        try:
            resp = self.llm_provider.generate(prompt, temperature=0.2, max_tokens=800)
            data = json.loads(resp)
            violations = data.get("violations", [])
            return {
                "passed": data.get("passed", len(violations) == 0),
                "score": max(0.0, 100.0 - len(violations) * 20),
                "violations": violations,
                "world_rules": self.world_rules,
                "deep": True,
            }
        except Exception:
            return self.check_consistency(context, global_state)


# =============================================================================
# StyleRecognizer：文体风格识别（题材 / 人称 / 视角 / 语言风格 / 节奏 五维）
# 纯规则、零依赖、可解释。既可识别单段导入文本，也可识别整部作品基调。
# 识别结果写入 world_rules["style_profile"]，供后续生成提示词按文体微调。
# =============================================================================
class StyleRecognizer:
    """从自然语言文本识别文体风格。

    五维输出：
      - genre       题材类型（修仙/玄幻/科幻/悬疑/历史/都市/奇幻/武侠/军事/末世…）
      - person      叙事人称（第一人称 / 第三人称）
      - perspective 叙事视角（全知 / 限知 / 中性的旁观）
      - language    语言风格（古风 / 现代 / 文言）
      - pace        叙事节奏（快 / 中 / 慢）
    """

    # —— 题材特征词表（命中即计分）——
    GENRE_KEYWORDS = {
        "修仙": [
            "修仙",
            "修炼",
            "金丹",
            "元婴",
            "筑基",
            "渡劫",
            "灵根",
            "灵脉",
            "洞府",
            "飞升",
            "道心",
            "丹田",
            "功法",
            "宗门",
        ],
        "玄幻": [
            "斗气",
            "斗者",
            "魂力",
            "斗罗",
            "武魂",
            "血脉觉醒",
            "异火",
            "战尊",
            "圣域",
            "位面",
            "大陆",
            "魔导",
            "斗技",
        ],
        "科幻": [
            "星际",
            "飞船",
            "宇宙",
            "机械",
            "量子",
            "AI",
            "人工智能",
            "机器人",
            "基因",
            "外星球",
            "太空",
            "纳米",
            "冬眠",
        ],
        "悬疑": [
            "线索",
            "真相",
            "谜团",
            "调查",
            "侦探",
            "案件",
            "凶手",
            "证据",
            "密室",
            "推理",
            "嫌疑人",
            "失踪",
            "悬案",
        ],
        "历史": [
            "王朝",
            "皇帝",
            "将军",
            "征战",
            "朝堂",
            "谋略",
            "粮草",
            "边关",
            "府兵",
            "天下",
            "诸侯",
            "科举",
            "宦官",
        ],
        "都市": [
            "都市",
            "公司",
            "职场",
            "总裁",
            "CEO",
            "办公室",
            "合同",
            "会议",
            "咖啡",
            "地铁",
            "合租",
            "加班",
            "白领",
        ],
        "奇幻": [
            "魔法",
            "精灵",
            "巨龙",
            "法师",
            "炼金",
            "王国",
            "骑士",
            "咒语",
            "魔杖",
            "城堡",
            "矮人",
            "兽人",
            "森林精灵",
        ],
        "武侠": [
            "江湖",
            "内力",
            "剑法",
            "掌门",
            "侠客",
            "轻功",
            "点穴",
            "武林",
            "门派",
            "武学",
            "招式",
            "秘籍",
            "暗器",
        ],
        "军事": [
            "战场",
            "部队",
            "指挥官",
            "装甲",
            "战术",
            "包围",
            "前线",
            "突击",
            "军团",
            "火力",
            "侦察",
            "阵地",
            "硝烟",
        ],
        "末世": [
            "末世",
            "丧尸",
            "变异",
            "幸存者",
            "庇护所",
            "病毒",
            "废土",
            "末日",
            "灾变",
            "辐射",
            "救援队",
            "沦陷",
        ],
    }
    # 若同时命中多个题材，取命中数最多者；平手返回 None（不误判）
    _MAX_GENRE_HIT = 3

    # —— 人称特征 ——
    _FIRST_PERSON = ["我", "我们", "我的", "咱们"]
    _THIRD_PERSON = ["他", "她", "他们", "她们", "它的"]

    # —— 视角特征：全知解说词 vs 限知心理词 ——
    _OMNISCIENT_WORDS = [
        "殊不知",
        "原来",
        "事实上",
        "实际上",
        "要知道",
        "众所周知",
        "话说",
        "且说",
        "却说",
        "正是",
        "但见",
    ]
    _LIMITED_WORDS = [
        "心想",
        "暗自",
        "觉得",
        "感到",
        "意识到",
        "恍然",
        "似乎",
        "好像",
        "隐约",
        "猜测",
    ]

    # —— 语言风格 ——
    _ANCIENT_WORDS = [
        "之乎者也",
        "矣",
        "焉",
        "哉",
        "欲",
        "遂",
        "乃",
        "吾",
        "汝",
        "妾",
        "卿",
        "如何",
        "倘若",
        "莫非",
        "何以",
    ]
    # 文言高频虚字：单字计分，出现即加权
    _CLASSICAL_CHARS = _LZ._CLASSICAL_CHARS_SR
    _MODERN_WORDS = [
        "其实",
        "对了",
        "好吧",
        "然后",
        "但是",
        "不过",
        "应该",
        "觉得",
        "真的",
        "特别",
        "非常",
        "居然",
    ]

    @classmethod
    def _score_by_keyword(cls, text: str, word_list) -> int:
        if not text:
            return 0
        return sum(1 for w in word_list if w in text)

    @classmethod
    def analyze(cls, text: str) -> Dict[str, Any]:
        """识别单段/单文档文本的文体风格。返回五维字典。"""
        if not text:
            return {
                "genre": None,
                "person": "未知",
                "perspective": "未知",
                "language": "未知",
                "pace": "未知",
                "confidence": 0.0,
            }
        # 1) 题材：命中即判定（短文本/大纲同样有效）；无中文或零命中则 None
        genre_scores = {
            g: cls._score_by_keyword(text, words)
            for g, words in cls.GENRE_KEYWORDS.items()
        }
        top_genre = max(genre_scores, key=genre_scores.get)
        genre = top_genre if genre_scores[top_genre] >= 1 else None
        # 2) 人称：统计「我/我们」类与「他/她/他们」类，排除短文本噪声
        first = cls._score_by_keyword(text, cls._FIRST_PERSON)
        third = cls._score_by_keyword(text, cls._THIRD_PERSON)
        # 单字"我/他/她"仅在句中独立出现时计入（避免"我们"被"我"重复计、名词误判）
        first += len(re.findall(r"(?<!我们)我(?!们)", text))
        third += len(re.findall(r"他|她", text))
        if first >= 3 and first > third:
            person = "第一人称"
        elif third >= 3 and third > first:
            person = "第三人称"
        elif first > third:
            person = "第一人称"
        elif third > first:
            person = "第三人称"
        else:
            person = "未知"
        # 3) 视角
        omni = cls._score_by_keyword(text, cls._OMNISCIENT_WORDS)
        limited = cls._score_by_keyword(text, cls._LIMITED_WORDS)
        perspective = (
            "全知" if omni > limited else ("限知" if limited > omni else "中性旁观")
        )
        # 4) 语言风格
        ancient = cls._score_by_keyword(text, cls._ANCIENT_WORDS)
        classical = sum(1 for ch in text if ch in cls._CLASSICAL_CHARS)
        modern = cls._score_by_keyword(text, cls._MODERN_WORDS)
        if classical >= 6 or ancient >= 4:
            language = "文言"
        elif ancient >= 2 or classical >= 3:
            language = "古风"
        elif modern >= 3:
            language = "现代"
        else:
            language = "中性"
        # 5) 节奏：句均长（字符/句号+逗号片段数），短句占比
        sentences = [s for s in re.split(r"[。！？!?]", text) if s.strip()]
        total_len = len(text.replace(" ", ""))
        avg = (total_len / max(1, len(sentences))) if sentences else 0
        short_ratio = sum(1 for s in sentences if len(s) <= 12) / max(1, len(sentences))
        if avg <= 18 or short_ratio >= 0.5:
            pace = "快"
        elif avg >= 40 and short_ratio <= 0.25:
            pace = "慢"
        else:
            pace = "中"
        confidence = min(1.0, (len(sentences) / 20.0) + (0.1 if genre else 0))
        return {
            "genre": genre,
            "person": person,
            "perspective": perspective,
            "language": language,
            "pace": pace,
            "confidence": round(confidence, 2),
        }

    @classmethod
    def analyze_work(cls, chapters_text: str, outline: str = "") -> Dict[str, Any]:
        """识别整部作品的文体基调：综合全文 + 大纲，题材取两者中命中更强的一侧。"""
        main = cls.analyze(chapters_text)
        if outline:
            outline_prof = cls.analyze(outline)
            # 题材：全文与大纲合并取命中更强者
            combined = cls.analyze(chapters_text + "\n" + outline)
            main["genre"] = combined["genre"] if combined["genre"] else main["genre"]
            main["genre_source"] = "combined"
        return main

    # —— 风格翻译层：把五维识别结果变成 LLM 可执行的生成约束（多文体适配）——
    _GENRE_GUIDE = {
        "修仙": "营造仙侠意境：修炼、灵根、渡劫、宗门体系等设定自然出现；对话可带古朴气，但以流畅为主；写景多用山泽灵雾、洞府丹炉意象。",
        "玄幻": "突出热血与成长：斗气/武魂/血脉等体系设定铺陈有层次；战斗场面节奏明快、气势足；避免日常琐碎过度展开。",
        "科幻": "保持科学逻辑与未来感：技术细节克制、可信；不出现超自然解释；环境描写强调机械/星际/数据质感；硬科幻世界观下技术设定优先。",
        "悬疑": "营造悬念与压迫感：信息逐步释放，不可一次性全知；细节埋线，呼应前文线索；句式偏短促，留白多；禁止旁白剧透。",
        "历史": "贴合时代语感：朝堂/征战/市井风俗描写有考据感；称谓、器物、制度符合时代背景；行文沉稳，少用现代词汇。",
        "都市": "贴近现代生活质感：场景真实（职场/街道/住所）；心理描写细腻；语言自然口语化，节奏贴近日常；允许现代器物与用语。",
        "奇幻": "营造异世界氛围：魔法、种族、王国设定细节丰富；地名/称谓有异域感；写景多城堡森林与神秘传说气息。",
        "武侠": "突出侠气与招式美感：江湖恩怨、门派情义；打斗写意有招名；语言简练有力，可带文言腔但不拗口。",
        "军事": "保持纪律与真实感：战术、编队、装备描写专业可信；叙事克制硬朗；节奏紧、短句多；禁儿女情长拖戏。",
        "末世": "营造废土生存压迫感：物资、危机、幸存者心态写实；气氛阴郁但留希望；节奏快、冲突密；禁轻浮调侃。",
    }

    _PERSON_GUIDE = {
        "第一人称": "全程使用“我”视角叙述，只写主角所见、所闻、所感；不得切换到其他角色内心。",
        "第三人称": "使用“他/她/他们”叙述；视角可在角色间切换，但切换要自然，不突兀。",
    }

    _PERSPECTIVE_GUIDE = {
        "全知": "允许作者视角俯瞰全局，可适当交代背景与人物内心，但不得破坏悬念。",
        "限知": "严格跟随当前视角角色，只呈现其能看到、听到、猜到、感受到的信息；不得泄露角色未知之事。",
        "中性旁观": "以旁观者视角记录可见行动与可闻对话，不进入任何角色内心，不做主观评价。",
    }

    _LANGUAGE_GUIDE = {
        "文言": "通篇采用文言句式，用词典雅，虚字自然；篇幅可适度精简。",
        "古风": "采用古朴文雅的白话，适当融入文言词汇与四字句，读来有古韵但易懂。",
        "现代": "使用现代口语化表达，自然流畅，贴近当代读者阅读习惯。",
        "中性": "语言平实自然，不刻意文白，以清晰叙事为先。",
    }

    _PACE_GUIDE = {
        "快": "节奏紧凑，短句为主，信息密度高，减少环境铺陈与心理独白。",
        "中": "节奏平稳，长短句结合，叙事、描写、对话均衡。",
        "慢": "节奏舒缓，细节与心理描写丰富，环境氛围充分渲染，不急推进。",
    }

    @classmethod
    def style_guidelines(cls, profile: Dict[str, Any]) -> str:
        """把五维风格档案翻译为生成期约束文本。无档案/未知维度时优雅降级，不输出空壳约束。"""
        if not profile:
            return ""
        parts = []
        genre = profile.get("genre")
        if genre and genre in cls._GENRE_GUIDE:
            parts.append(f"【题材·{genre}】{cls._GENRE_GUIDE[genre]}")
        person = profile.get("person")
        if person in cls._PERSON_GUIDE:
            parts.append(f"【人称】{cls._PERSON_GUIDE[person]}")
        perspective = profile.get("perspective")
        if perspective in cls._PERSPECTIVE_GUIDE:
            parts.append(f"【视角】{cls._PERSPECTIVE_GUIDE[perspective]}")
        language = profile.get("language")
        if language in cls._LANGUAGE_GUIDE:
            parts.append(f"【语言】{cls._LANGUAGE_GUIDE[language]}")
        pace = profile.get("pace")
        if pace in cls._PACE_GUIDE:
            parts.append(f"【节奏】{cls._PACE_GUIDE[pace]}")
        return "\n".join(parts)


# ==================== 演示示例（题材中性） ====================
if __name__ == "__main__":
    for conflict in check_engine_isolation():
        print(f"⚠️ {conflict}")

    # 极简演示：使用 MockLLM（无API）
    class MockLLM(LLMProvider):
        def generate(self, prompt: str, **kwargs) -> str:
            return "（演示模式：未接入 LLM）角色的内心随事件推进自然转变，情节在此节点平滑演进。接入真实 LLM 后可生成匹配情感状态的文学文本。"

    state = GlobalState()
    engine = UltimateCausalNovelEngine("示例：叙事一致性审计", state)
    engine.set_llm_provider(MockLLM())
    # 使用自然语言大纲
    outline = "林夏在评审会上坚持自研方案 → 周舟梳理两套方案利弊 → 林夏意识到忽略成本，同意第三方评审"
    chapter = engine.create_chapter_from_outline(1, "分歧与选择", outline)
    if chapter:
        content = engine.render_chapter(chapter)
        print(content)

    # —— 文体风格自动识别演示（导入文本 / 大纲均可）——
    print("\n===== 文体风格自动识别 =====")
    import textwrap

    demo_para = (
        "李青云盘坐洞府之中，丹田内灵力翻涌，金丹微微颤动。"
        "他运转功法，渡劫在即，道心却有一丝动摇。"
    )
    seg = engine.recognize_style(text=demo_para)
    print(
        f"[导入文本] 题材={seg['genre']} 人称={seg['person']} 视角={seg['perspective']} "
        f"语言={seg['language']} 节奏={seg['pace']}"
    )
    work = engine.recognize_style(chapters=engine.chapters, outline=outline)
    print(
        f"[作品基调] 题材={work['genre']} 人称={work['person']} 视角={work['perspective']} "
        f"语言={work['language']} 节奏={work['pace']}"
    )


# =============================================================================
# 创作者工具箱（Creator Toolkit）—— 把审计内核交付到作者手里的外围模块
#   A. 创作流闭环（增量审计 + 大纲↔正文同步）
#   B. 作者能看懂、能改的产物（设定集 / 因果图谱 / 伏笔&一致性清单）
#   C. 交付与采纳（建议采纳闭环 / 多格式导出）
# 设计原则：纯规则、决定论、零或轻量依赖（docx 导出需 python-docx，已获授权）。
# =============================================================================


# ==================== 模块A：创作流闭环 ====================
class IncrementalAuditor:
    """增量审计器：只对「新增/改动段落」做轻量审计，避免每次全量重跑。

    决定论：复用现有规则（逻辑跳跃词 / 人物一致性 / 伏笔关键词），
    若持有 engine 引用，则把段落解析成单节点跑一次节点级审计（node_auditor）。
    """

    _JUMP_WORDS = _LZ._JUMP_WORDS_IA
    _SET_HINTS = ("埋下伏笔", "埋下", "埋伏笔", "留下线索", "铺下伏笔", "埋线")
    _PAY_HINTS = ("回收伏笔", "呼应", "揭开", "真相大白", "兑现", "收回伏笔", "揭开谜底")

    def __init__(self, engine: Optional["UltimateCausalNovelEngine"] = None):
        self.engine = engine

    def audit_segment(self, text: str, global_state: Optional["GlobalState"] = None) -> Dict[str, Any]:
        """审计单个新增/改动段落，返回 {passed, issues[], segment_len}。"""
        issues: List[Dict[str, str]] = []
        # 1) 逻辑跳跃词
        hits = [w for w in self._JUMP_WORDS if w in text]
        if hits:
            issues.append({"type": "logical_jump", "detail": "发现生硬转折词：" + "、".join(hits)})
        # 2) 伏笔信号
        for w in self._SET_HINTS:
            if w in text:
                issues.append({"type": "foreshadow_set", "detail": f"检测到伏笔埋设信号：{w}"})
                break
        for w in self._PAY_HINTS:
            if w in text:
                issues.append({"type": "foreshadow_pay", "detail": f"检测到伏笔回收信号：{w}"})
                break
        # 3) 若有 engine，跑一次节点级审计（人物/前提结论匹配/脆弱性）
        if self.engine is not None and global_state is not None:
            node = CausalNode(premise="", conclusion=text)
            node.character = _extract_plausible_name(text)
            try:
                rep = self.engine.node_auditor.audit({"node": node, "text": text})
                for name, res in rep.get("analysis", {}).items():
                    for issue in res.get("issues", []):
                        issues.append({"type": f"node:{name}", "detail": issue})
            except Exception:
                pass  # 降级：仅规则层
        return {"passed": len(issues) == 0, "issues": issues, "segment_len": len(text)}


def sync_outline_from_text(engine: "UltimateCausalNovelEngine", text: str) -> List[CausalNode]:
    """正文 → 大纲：把正文用 NarrativeStripper 抽成因果节点，写回 engine.causal_graph。

    返回新增节点列表。相邻节点自动建立父子关系，便于后续图谱可视化。
    """
    events = NarrativeStripper.to_events(text)
    nodes: List[CausalNode] = []
    prev: Optional[CausalNode] = None
    for ev in events:
        node = CausalNode(
            premise=ev.get("premise", ""),
            conclusion=ev["conclusion"],
            character=ev.get("character", ""),
        )
        if prev is not None:
            node.parent_nodes.append(prev.node_id)
            prev.child_nodes.append(node.node_id)
        engine.causal_graph[node.node_id] = node
        nodes.append(node)
        prev = node
    # 同步进伏笔台账（顺手登记正文里的伏笔语义）
    engine.foreshadow_ledger.scan_nodes(nodes, chapter_id="")
    return nodes


def sync_text_from_outline(engine: "UltimateCausalNovelEngine", outline: str) -> str:
    """大纲 → 正文草稿（无副作用版）：把 A→B→C 大纲展开为叙事节拍文本。

    仅做确定性展开，不调用 LLM、不改全局状态；如需丰满正文请用 engine.render_chapter。
    """
    nodes = parse_outline_to_nodes(outline)
    beats: List[str] = []
    for n in nodes:
        if n.premise and n.premise != "（待续）":
            beats.append(f"{n.premise} → {n.conclusion}")
        else:
            beats.append(n.conclusion)
    return "\n".join(beats)


# ==================== 模块B：作者能看懂、能改的产物 ====================
@dataclass
class CharacterProfile:
    """单个角色的权威档案（角色圣经条目）。作者确认后写入，作为一致性审计的基准。"""
    name: str
    traits: Dict[str, Any] = field(default_factory=dict)          # 性格 / 简介等
    arc: List[str] = field(default_factory=list)                  # 角色弧光节点
    relationships: Dict[str, str] = field(default_factory=dict)   # 他角 -> 关系描述
    timeline: List[Dict[str, Any]] = field(default_factory=list)  # 该角色事件时间线
    known_knowledge: List[str] = field(default_factory=list)      # 已知信息
    forbidden_knowledge: List[str] = field(default_factory=list)  # 不该知道的事
    register_hints: List[str] = field(default_factory=list)      # 语域画像候选
    version: int = 1


class CharacterBible:
    """可编辑设定集：把自动抽取的候选档案接进「作者确认」闭环，沉淀为权威角色圣经。

    诚实原则：自动产物一律标记 candidate，需作者 confirm() 后才成为权威字段。
    """

    def __init__(self, global_state: "GlobalState"):
        self.global_state = global_state
        self.profiles: Dict[str, CharacterProfile] = {}
        self._bootstrap_from_state()

    def _bootstrap_from_state(self):
        for name, info in self.global_state.characters.items():
            self.profiles[name] = CharacterProfile(name=name, traits=info or {})

    def ingest_candidates(self, candidates: Dict[str, Dict[str, Any]]) -> List[str]:
        """并入 extract_character_profiles 的候选（仅补充，不覆盖作者已确认字段）。返回受影响角色。"""
        touched: List[str] = []
        for name, cand in candidates.items():
            p = self.profiles.setdefault(name, CharacterProfile(name=name))
            for h in cand.get("register_hints_candidates", []):
                if h not in p.register_hints:
                    p.register_hints.append(h)
            for k in cand.get("knowledge_candidates", []):
                if k not in p.known_knowledge:
                    p.known_knowledge.append(k)
            touched.append(name)
        return touched

    def confirm(self, name: str, **fields) -> CharacterProfile:
        """作者确认：显式写入权威字段（traits/arc/relationships/forbidden_knowledge...）。"""
        p = self.profiles.setdefault(name, CharacterProfile(name=name))
        for k, v in fields.items():
            if hasattr(p, k):
                setattr(p, k, v)
        # 回写 global_state.characters，保持与引擎一致
        self.global_state.characters.setdefault(name, {})
        self.global_state.characters[name].update({
            "性格": p.traits.get("性格", "中性"),
            "简介": p.traits.get("简介", ""),
        })
        p.version += 1
        return p

    def add_forbidden_knowledge(self, name: str, items) -> None:
        """登记角色不该知道的事（创作意图，默认由作者填写）。"""
        p = self.profiles.setdefault(name, CharacterProfile(name=name))
        if isinstance(items, str):
            items = [items]
        for it in items:
            if it not in p.forbidden_knowledge:
                p.forbidden_knowledge.append(it)

    def to_markdown(self) -> str:
        md = ["# 角色圣经（Character Bible）", ""]
        if not self.profiles:
            md.append("_（暂无角色，请先运行抽取或写作以自动注册）_")
            return "\n".join(md)
        for name, p in self.profiles.items():
            md.append(f"## {name}")
            if p.traits:
                md.append(f"- 设定：{p.traits}")
            if p.arc:
                md.append("- 弧光：" + " → ".join(p.arc))
            if p.relationships:
                md.append("- 关系：" + "；".join(f"{k}（{v}）" for k, v in p.relationships.items()))
            if p.known_knowledge:
                md.append("- 已知：" + "、".join(p.known_knowledge))
            if p.forbidden_knowledge:
                md.append("- 禁用知识：" + "、".join(p.forbidden_knowledge))
            if p.register_hints:
                md.append("- 语域候选：" + "、".join(p.register_hints))
            md.append("")
        return "\n".join(md)


def export_causal_graph(engine: "UltimateCausalNovelEngine", fmt: str = "mermaid") -> str:
    """剧情因果图谱可视化：把 engine.causal_graph 的节点与父子关系导出。

    fmt=mermaid → Mermaid flowchart 代码（可贴入支持 Mermaid 的编辑器/README）；
    fmt=dot     → Graphviz DOT（可用 dot 渲染为图片）。
    """
    nodes = list(engine.causal_graph.values())
    if fmt == "mermaid":
        lines = ["graph TD"]
        for n in nodes:
            label = (n.conclusion or n.premise or "")[:18].replace('"', "'")
            lines.append(f'  {n.node_id}["{n.character or "?"}: {label}"]')
            for c in n.child_nodes:
                lines.append(f"  {n.node_id} --> {c}")
        return "\n".join(lines)
    elif fmt == "dot":
        lines = ["digraph G {", "  rankdir=TD;"]
        for n in nodes:
            label = (n.conclusion or n.premise or "")[:18].replace('"', "'")
            lines.append(f'  "{n.node_id}" [label="{n.character or "?"}: {label}"];')
            for c in n.child_nodes:
                lines.append(f'  "{n.node_id}" -> "{c}";')
        lines.append("}")
        return "\n".join(lines)
    else:
        raise ValueError(f"未知格式: {fmt}")


def build_consistency_report(engine: "UltimateCausalNovelEngine") -> Dict[str, Any]:
    """汇总全书的设定冲突清单：伏笔未回收 + 时空冲突。决定论结论，无概率。"""
    report = {
        "foreshadow": engine.foreshadow_ledger.reconcile(),
        "spacetime": audit_spacetime_consistency(list(engine.causal_graph.values())),
        "open_issues": [],
    }
    for t in report["foreshadow"]["unrecovered_topics"]:
        report["open_issues"].append(f"伏笔未回收：{t}")
    for c in report["spacetime"]["conflicts"]:
        report["open_issues"].append(c)
    report["all_clean"] = len(report["open_issues"]) == 0
    return report


# ==================== 模块C：交付与采纳 ====================
def apply_review(
    text: str,
    issues: List[str],
    accept_mask: Optional[List[bool]] = None,
    characters: Optional[Dict[str, Any]] = None,
    global_state: Optional["GlobalState"] = None,
) -> str:
    """逐条采纳/拒绝叙事呈现问题的修复并回写正文（采纳闭环）。

    issues: 问题文本列表（与 accept_mask 一一对应，顺序同识别顺序）。
    accept_mask: 同长度布尔；None=全部采纳。
    规则修复与 repair_presentation_issues 的降级逻辑一致（删解说腔/删动机归因/遮台词）。
    """
    if accept_mask is None:
        accept_mask = [True] * len(issues)
    new_text = text
    wr = (getattr(global_state, "world_rules", None) if global_state else None) or {}
    sp = wr.get("style_profile") or {}
    genre = sp.get("genre") if isinstance(sp, dict) else ""
    modern = bool(wr.get("modern_setting")) or genre in {"都市", "科幻", "现代", "悬疑", "末世", "游戏", "星际", "赛博"}
    forbidden = [] if modern else list(_ERA_FORBIDDEN_DEFAULT)
    if isinstance(wr.get("era_forbidden_words"), list):
        forbidden.extend(wr["era_forbidden_words"])
    for issue, accept in zip(issues, accept_mask):
        if not accept:
            continue
        # 1) 全知解说腔
        applied = False
        for w in _OMNISCIENT_PATTERNS:
            if w in issue and w in new_text:
                new_text = new_text.replace(w, "")
                applied = True
        # 2) 动机归因句
        if not applied:
            for pat in _EXPLAIN_MOTIVE_PATTERNS:
                m = pat.search(new_text)
                if m and any(k in issue for k in ("动机", "归因", "解释", "内心")):
                    new_text = new_text.replace(m.group(0), "")
                    break
        # 3) 台词时代穿越（现代题材豁免）
        if characters:
            for d in _extract_dialogues(new_text):
                if any(w in d for w in forbidden):
                    new_text = new_text.replace(d, "……")
    return new_text


def export_novel(engine: "UltimateCausalNovelEngine", path: str, fmt: str = "md") -> str:
    """多格式导出成书：md / html / epub / docx。

    依赖：epub 用标准库 zipfile 手搓（零依赖）；docx 需要 python-docx（轻量依赖，已获授权）。
    """
    if fmt == "md":
        full = f"# {engine.novel_title}\n\n"
        for ch in engine.chapters:
            if ch.content:
                full += f"## 第{ch.chapter_id}章 {ch.title}\n\n{ch.content}\n\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(full)
    elif fmt == "html":
        html = engine.report_generator.generate(engine.novel_title, engine.chapters)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    elif fmt == "epub":
        _write_epub(path, engine.novel_title, engine.chapters)
    elif fmt == "docx":
        _write_docx(path, engine.novel_title, engine.chapters)
    else:
        raise ValueError(f"未知格式: {fmt}")
    return path


def _write_epub(path: str, title: str, chapters: List["Chapter"]) -> None:
    """用标准库 zipfile 手搓最小可用 EPUB 2.0（零依赖）。"""
    import zipfile
    from xml.sax.saxutils import escape

    items = [(i, ch) for i, ch in enumerate(chapters) if ch.content]
    manifest = [f"chap_{i+1}.xhtml" for i, _ in enumerate(items)]

    def chap_xhtml(name, ch):
        body = "".join(
            f"<p>{escape(p)}</p>" for p in (ch.content or "").split("\n\n") if p.strip()
        )
        return (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml">'
            f"<head><title>{escape(ch.title)}</title></head>"
            f"<body><h1>第{ch.chapter_id}章 {escape(ch.title)}</h1>{body}</body></html>"
        )

    opf = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="bookid">\n'
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        f"<dc:title>{escape(title)}</dc:title>"
        f"<dc:identifier id=\"bookid\">urn:uuid:{uuid.uuid4()}</dc:identifier>\n"
        "<dc:language>zh</dc:language></metadata>\n<manifest>\n"
        '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>\n'
        + "".join(
            f'<item id="item{i}" href="{n}" media-type="application/xhtml+xml"/>\n'
            for i, n in enumerate(manifest)
        )
        + "</manifest>\n<spine>"
        + "".join(f'<itemref idref="item{i}"/>' for i in range(len(manifest)))
        + "</spine>\n</package>"
    )
    ncx = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n'
        f"<docTitle><text>{escape(title)}</text></docTitle>\n<navMap>"
        + "".join(
            f'<navPoint id="np{i}" playOrder="{i+1}"><navLabel><text>{escape(items[i][1].title)}</text></navLabel>'
            f'<content src="{manifest[i]}"/></navPoint>'
            for i in range(len(items))
        )
        + "</navMap>\n</ncx>"
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr(
            "META-INF/container.xml",
            '<?xml version="1.0"?><container version="1.0" '
            'xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>'
            '<rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>'
            "</rootfiles></container>",
        )
        z.writestr("content.opf", opf)
        z.writestr("toc.ncx", ncx)
        for (i, ch), n in zip(items, manifest):
            z.writestr(n, chap_xhtml(n, ch))


def _write_docx(path: str, title: str, chapters: List["Chapter"]) -> None:
    """用 python-docx 导出 Word（轻量依赖，已获授权）。"""
    from docx import Document

    doc = Document()
    doc.add_heading(title, level=0)
    for ch in chapters:
        if not ch.content:
            continue
        doc.add_heading(f"第{ch.chapter_id}章 {ch.title}", level=1)
        for para in ch.content.split("\n\n"):
            if para.strip():
                doc.add_paragraph(para)
    doc.save(path)
