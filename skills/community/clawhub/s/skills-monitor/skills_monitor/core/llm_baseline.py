"""
大模型基准线测试器 v0.6.0 — LLM Baseline Benchmark (TOP50 × 6 Models)
======================================================================
支持模型: Claude Opus 4.6 / MiniMax 2.5 / GLM-5 / GPT-5.4 / Gemini 3.0 Pro / DeepSeek 3.2
运行模式: mock (高仿真模拟,零成本) / live (真实 API 调用)

使用:
  from skills_monitor.core.llm_baseline import LLMBaselineTester, BatchBenchmark
  batch = BatchBenchmark(mode="mock")
  matrix = batch.run_full_benchmark()
  report = batch.generate_matrix_report(matrix)
"""

import json, hashlib, logging, math, os, random, statistics, time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
#  模型定义
# ═══════════════════════════════════════════════════════════════════

class ModelProvider(str, Enum):
    OPENAI = "openai"; ANTHROPIC = "anthropic"; GOOGLE = "google"
    ZHIPU = "zhipu"; MINIMAX = "minimax"; DEEPSEEK = "deepseek"
    LOCAL = "local"; MOCK = "mock"

@dataclass
class ModelConfig:
    provider: ModelProvider; model_name: str; display_name: str
    api_key_env: str = ""; base_url: str = ""
    max_tokens: int = 2048; temperature: float = 0.0
    cost_per_1k_input: float = 0; cost_per_1k_output: float = 0
    mock_avg_latency_ms: float = 2000; mock_latency_stddev_ms: float = 500
    mock_success_rate: float = 0.90
    mock_avg_input_tokens: int = 500; mock_avg_output_tokens: int = 350
    @property
    def api_key(self) -> str:
        return os.environ.get(self.api_key_env, "") if self.api_key_env else ""

PRESET_MODELS: Dict[str, ModelConfig] = {
    "claude-opus-4.6": ModelConfig(
        ModelProvider.ANTHROPIC, "claude-opus-4-6-20260301", "Claude Opus 4.6",
        "ANTHROPIC_API_KEY", "", 2048, 0.0, 0.015, 0.075,
        3200, 800, 0.96, 550, 420),
    "minimax-2.5": ModelConfig(
        ModelProvider.MINIMAX, "minimax-2.5", "MiniMax 2.5",
        "MINIMAX_API_KEY", "https://api.minimax.chat/v1", 2048, 0.0, 0.004, 0.012,
        1800, 400, 0.91, 500, 380),
    "glm-5": ModelConfig(
        ModelProvider.ZHIPU, "glm-5", "GLM-5",
        "ZHIPU_API_KEY", "https://open.bigmodel.cn/api/paas/v4", 2048, 0.0, 0.005, 0.015,
        2200, 600, 0.92, 520, 390),
    "gpt-5.4": ModelConfig(
        ModelProvider.OPENAI, "gpt-5.4", "GPT-5.4",
        "OPENAI_API_KEY", "", 2048, 0.0, 0.010, 0.030,
        2500, 700, 0.95, 530, 400),
    "gemini-3.0-pro": ModelConfig(
        ModelProvider.GOOGLE, "gemini-3.0-pro", "Gemini 3.0 Pro",
        "GOOGLE_API_KEY", "https://generativelanguage.googleapis.com/v1beta",
        2048, 0.0, 0.007, 0.021, 2800, 650, 0.93, 510, 410),
    "deepseek-3.2": ModelConfig(
        ModelProvider.DEEPSEEK, "deepseek-chat-v3.2", "DeepSeek 3.2",
        "DEEPSEEK_API_KEY", "https://api.deepseek.com/v1", 2048, 0.0, 0.002, 0.008,
        1600, 350, 0.91, 490, 360),
    "mock": ModelConfig(
        ModelProvider.MOCK, "mock-baseline", "模拟模型 (Demo)",
        mock_avg_latency_ms=1500, mock_latency_stddev_ms=300, mock_success_rate=0.85),
}

# ═══════════════════════════════════════════════════════════════════
#  数据类
# ═══════════════════════════════════════════════════════════════════

@dataclass
class SingleRunResult:
    run_index: int; success: bool; duration_ms: float
    output: Any = None; error: Optional[str] = None
    token_usage: Dict[str, int] = field(default_factory=dict)
    cost_usd: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    def to_dict(self) -> dict:
        return {"run_index": self.run_index, "success": self.success,
                "duration_ms": round(self.duration_ms, 2), "error": self.error,
                "token_usage": self.token_usage, "cost_usd": round(self.cost_usd, 6)}

@dataclass
class BaselineStats:
    source: str; display_name: str; total_runs: int; success_count: int
    results: List[SingleRunResult] = field(default_factory=list)
    @property
    def success_rate(self) -> float:
        return (self.success_count / self.total_runs * 100) if self.total_runs > 0 else 0
    @property
    def _ok_d(self) -> List[float]:
        return [r.duration_ms for r in self.results if r.success]
    @property
    def avg_duration_ms(self) -> Optional[float]:
        d = self._ok_d; return round(statistics.mean(d), 2) if d else None
    @property
    def median_duration_ms(self) -> Optional[float]:
        d = self._ok_d; return round(statistics.median(d), 2) if d else None
    @property
    def p95_duration_ms(self) -> Optional[float]:
        d = sorted(self._ok_d); return round(d[int(len(d)*0.95)], 2) if d else None
    @property
    def total_cost_usd(self) -> float:
        return round(sum(r.cost_usd for r in self.results), 6)
    @property
    def avg_cost_usd(self) -> float:
        return round(self.total_cost_usd / max(self.total_runs, 1), 6)
    def to_dict(self) -> dict:
        return {"source": self.source, "display_name": self.display_name,
                "total_runs": self.total_runs, "success_count": self.success_count,
                "success_rate": round(self.success_rate, 1),
                "avg_duration_ms": self.avg_duration_ms,
                "total_cost_usd": self.total_cost_usd, "avg_cost_usd": self.avg_cost_usd}

@dataclass
class SkillModelScore:
    """单个 Skill × 单个 Model 的评分"""
    skill_slug: str; skill_name: str; model_key: str; model_name: str
    category: str; task_type: str
    success_rate: float; avg_latency_ms: float; avg_cost_usd: float
    quality_score: float; total_runs: int; success_count: int; total_cost_usd: float
    def to_dict(self) -> dict:
        return {k: (round(v, 4) if isinstance(v, float) else v)
                for k, v in self.__dict__.items()}

@dataclass
class BenchmarkMatrix:
    """完整评测矩阵 (50 Skills × 6 Models)"""
    version: str = "0.6.0"; mode: str = "mock"
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    models: List[str] = field(default_factory=list)
    skills_count: int = 0; models_count: int = 0; n_runs_per_cell: int = 3
    cells: List[SkillModelScore] = field(default_factory=list)
    model_summaries: Dict[str, Dict] = field(default_factory=dict)
    category_summaries: Dict[str, Dict] = field(default_factory=dict)
    def to_dict(self) -> dict:
        return {"version": self.version, "mode": self.mode,
                "generated_at": self.generated_at, "models": self.models,
                "skills_count": self.skills_count, "models_count": self.models_count,
                "n_runs_per_cell": self.n_runs_per_cell,
                "total_cells": len(self.cells),
                "cells": [c.to_dict() for c in self.cells],
                "model_summaries": self.model_summaries,
                "category_summaries": self.category_summaries}
    def get_model_ranking(self) -> List[Dict]:
        return sorted(self.model_summaries.values(),
                      key=lambda x: x.get("avg_quality_score", 0), reverse=True)

# ═══════════════════════════════════════════════════════════════════
#  LLM 适配器
# ═══════════════════════════════════════════════════════════════════

class LLMAdapter(ABC):
    @abstractmethod
    def call(self, prompt: str, config: ModelConfig) -> Tuple[str, Dict[str, int]]: ...

class OpenAIAdapter(LLMAdapter):
    def call(self, prompt, config):
        import requests as req
        if not config.api_key: raise ValueError(f"未配置 {config.api_key_env}")
        base = config.base_url or "https://api.openai.com/v1"
        r = req.post(f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {config.api_key}"},
            json={"model": config.model_name, "messages": [{"role":"user","content":prompt}],
                  "max_tokens": config.max_tokens, "temperature": config.temperature},
            timeout=120).json()
        u = r.get("usage", {})
        return r["choices"][0]["message"]["content"], \
               {"input_tokens": u.get("prompt_tokens",0), "output_tokens": u.get("completion_tokens",0)}

class AnthropicAdapter(LLMAdapter):
    def call(self, prompt, config):
        import requests as req
        if not config.api_key: raise ValueError(f"未配置 {config.api_key_env}")
        r = req.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key": config.api_key, "anthropic-version": "2023-06-01",
                     "content-type": "application/json"},
            json={"model": config.model_name, "max_tokens": config.max_tokens,
                  "temperature": config.temperature,
                  "messages": [{"role":"user","content":prompt}]},
            timeout=120).json()
        u = r.get("usage", {})
        return r["content"][0]["text"], \
               {"input_tokens": u.get("input_tokens",0), "output_tokens": u.get("output_tokens",0)}

class GoogleGeminiAdapter(LLMAdapter):
    def call(self, prompt, config):
        import requests as req
        if not config.api_key: raise ValueError(f"未配置 {config.api_key_env}")
        base = config.base_url or "https://generativelanguage.googleapis.com/v1beta"
        r = req.post(f"{base}/models/{config.model_name}:generateContent?key={config.api_key}",
            json={"contents": [{"parts": [{"text": prompt}]}],
                  "generationConfig": {"maxOutputTokens": config.max_tokens,
                                        "temperature": config.temperature}},
            timeout=120).json()
        c = r.get("candidates", [{}])
        text = c[0].get("content",{}).get("parts",[{}])[0].get("text","") if c else ""
        u = r.get("usageMetadata", {})
        return text, {"input_tokens": u.get("promptTokenCount",0),
                      "output_tokens": u.get("candidatesTokenCount",0)}

class ZhipuAdapter(LLMAdapter):
    def call(self, prompt, config):
        import requests as req
        if not config.api_key: raise ValueError(f"未配置 {config.api_key_env}")
        base = config.base_url or "https://open.bigmodel.cn/api/paas/v4"
        r = req.post(f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {config.api_key}"},
            json={"model": config.model_name, "messages": [{"role":"user","content":prompt}],
                  "max_tokens": config.max_tokens,
                  "temperature": max(config.temperature, 0.01)},
            timeout=120).json()
        u = r.get("usage", {})
        return r["choices"][0]["message"]["content"], \
               {"input_tokens": u.get("prompt_tokens",0), "output_tokens": u.get("completion_tokens",0)}

class MiniMaxAdapter(LLMAdapter):
    def call(self, prompt, config):
        import requests as req
        if not config.api_key: raise ValueError(f"未配置 {config.api_key_env}")
        base = config.base_url or "https://api.minimax.chat/v1"
        r = req.post(f"{base}/text/chatcompletion_v2",
            headers={"Authorization": f"Bearer {config.api_key}"},
            json={"model": config.model_name, "messages": [{"role":"user","content":prompt}],
                  "max_tokens": config.max_tokens, "temperature": config.temperature},
            timeout=120).json()
        text = r["choices"][0]["message"]["content"] if "choices" in r else r.get("reply","")
        u = r.get("usage", {})
        return text, {"input_tokens": u.get("prompt_tokens",0),
                      "output_tokens": u.get("completion_tokens",0)}

class DeepSeekAdapter(LLMAdapter):
    def call(self, prompt, config):
        import requests as req
        if not config.api_key: raise ValueError(f"未配置 {config.api_key_env}")
        base = config.base_url or "https://api.deepseek.com/v1"
        r = req.post(f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {config.api_key}"},
            json={"model": config.model_name, "messages": [{"role":"user","content":prompt}],
                  "max_tokens": config.max_tokens, "temperature": config.temperature},
            timeout=120).json()
        u = r.get("usage", {})
        return r["choices"][0]["message"]["content"], \
               {"input_tokens": u.get("prompt_tokens",0), "output_tokens": u.get("completion_tokens",0)}

# 任务难度系数 & 模型特长
_TASK_DIFF = {
    "search_and_summarize": (0.8, 0.7), "translation": (0.9, 0.5),
    "file_operation": (0.7, 0.8), "code_analysis": (1.3, 1.2),
    "api_query": (0.6, 0.6), "data_processing": (1.1, 1.0),
    "document_processing": (1.0, 0.9), "text_formatting": (0.7, 0.4),
    "text_generation": (1.0, 0.6), "code_generation": (1.4, 1.3),
    "config_generation": (1.1, 1.0), "sql_generation": (1.0, 0.9),
    "financial_analysis": (1.5, 1.5), "workflow_design": (1.2, 1.1),
    "media_processing": (1.0, 1.0), "nlp_analysis": (1.2, 1.1),
    "security_task": (1.3, 1.2), "api_testing": (0.9, 0.8),
    "calculation": (0.8, 0.7), "troubleshooting": (1.2, 1.0),
}
_MODEL_STR = {
    "claude-opus-4.6":  {"code_analysis":8,"code_generation":7,"security_task":6,"text_generation":5,"nlp_analysis":6},
    "gpt-5.4":          {"code_generation":8,"api_testing":6,"data_processing":7,"workflow_design":5,"config_generation":6},
    "gemini-3.0-pro":   {"search_and_summarize":7,"data_processing":6,"calculation":8,"nlp_analysis":5,"media_processing":5},
    "glm-5":            {"translation":8,"text_generation":7,"financial_analysis":6,"sql_generation":5,"text_formatting":5},
    "minimax-2.5":      {"text_generation":6,"translation":5,"nlp_analysis":5,"search_and_summarize":4,"document_processing":4},
    "deepseek-3.2":     {"code_generation":7,"code_analysis":6,"calculation":7,"sql_generation":6,"config_generation":5},
}

class MockLLMAdapter(LLMAdapter):
    """高仿真模拟 — 基于各模型已知特性"""
    def __init__(self, task_type="text_generation"):
        self.task_type = task_type
        self._last_latency = 0; self._last_quality_bonus = 0
    def call(self, prompt, config):
        lat_m, fail_m = _TASK_DIFF.get(self.task_type, (1.0, 1.0))
        latency = max(200, random.gauss(config.mock_avg_latency_ms * lat_m, config.mock_latency_stddev_ms))
        if random.random() < (1 - config.mock_success_rate) * fail_m:
            raise Exception(f"模拟 {config.display_name} 失败 (task={self.task_type})")
        inp = max(100, int(config.mock_avg_input_tokens * len(prompt)/500 * random.uniform(0.8,1.2)))
        out = max(50, int(config.mock_avg_output_tokens * random.uniform(0.7,1.3)))
        qb = _MODEL_STR.get(config.display_name, _MODEL_STR.get(config.model_name, {})).get(self.task_type, 0)
        # 也用 key 匹配
        for k, v in _MODEL_STR.items():
            if k in (config.model_name or "") or k in (config.display_name or ""):
                qb = max(qb, v.get(self.task_type, 0)); break
        self._last_latency = latency; self._last_quality_bonus = qb
        time.sleep(0.005)  # 极小真实延迟
        return json.dumps({"mock":True,"model":config.display_name}, ensure_ascii=False), \
               {"input_tokens": inp, "output_tokens": out}

def _get_adapter(provider: ModelProvider, task_type: str = "") -> LLMAdapter:
    if provider == ModelProvider.MOCK: return MockLLMAdapter(task_type)
    m = {ModelProvider.OPENAI: OpenAIAdapter, ModelProvider.ANTHROPIC: AnthropicAdapter,
         ModelProvider.GOOGLE: GoogleGeminiAdapter, ModelProvider.ZHIPU: ZhipuAdapter,
         ModelProvider.MINIMAX: MiniMaxAdapter, ModelProvider.DEEPSEEK: DeepSeekAdapter}
    cls = m.get(provider)
    if not cls: raise ValueError(f"不支持: {provider}")
    return cls()

# ═══════════════════════════════════════════════════════════════════
#  单 Skill 测试器
# ═══════════════════════════════════════════════════════════════════

class LLMBaselineTester:
    def __init__(self, models=None, cache_dir="reports/baseline", mode="mock"):
        self.model_names = models or list(PRESET_MODELS.keys())
        self.models = {n: PRESET_MODELS[n] for n in self.model_names if n in PRESET_MODELS}
        self.mode = mode; self.cache_dir = cache_dir
        Path(cache_dir).mkdir(parents=True, exist_ok=True)

    def get_available_models(self) -> List[Dict]:
        return [{"name": n, "display_name": c.display_name, "provider": c.provider.value,
                 "cost_1k_in": c.cost_per_1k_input, "cost_1k_out": c.cost_per_1k_output}
                for n, c in self.models.items()]

    def run_llm_baseline(self, model_name, prompt, n_runs=3, task_type="text_generation") -> BaselineStats:
        config = self.models[model_name]
        adapter = MockLLMAdapter(task_type) if self.mode == "mock" else _get_adapter(config.provider, task_type)
        results, ok = [], 0
        for i in range(n_runs):
            t0 = time.time(); success, output, error, tokens, cost = False, None, None, {}, 0.0
            try:
                text, tokens = adapter.call(prompt, config); success = True; output = text
                cost = tokens.get("input_tokens",0)/1000*config.cost_per_1k_input + \
                       tokens.get("output_tokens",0)/1000*config.cost_per_1k_output
            except Exception as e: error = str(e)
            dur = adapter._last_latency if (self.mode=="mock" and success and hasattr(adapter,'_last_latency')) \
                  else (time.time()-t0)*1000
            results.append(SingleRunResult(i+1, success, dur, output, error, tokens, cost))
            if success: ok += 1
        return BaselineStats(model_name, config.display_name, n_runs, ok, results)

    def run_skill_baseline(self, skill_id, n_runs=3) -> BaselineStats:
        """模拟 Skill 基准 (Skill 直接执行一般更快更稳)"""
        results, ok = [], 0
        for i in range(n_runs):
            success = random.random() < 0.95
            dur = random.uniform(500, 2500)
            if success: ok += 1
            results.append(SingleRunResult(i+1, success, dur, error="模拟失败" if not success else None))
        return BaselineStats("skill", f"Skill [{skill_id}]", n_runs, ok, results)

    def _cache_result(self, data: dict, prefix: str):
        try:
            fn = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(os.path.join(self.cache_dir, fn), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e: logger.warning(f"缓存失败: {e}")


# ═══════════════════════════════════════════════════════════════════
#  批量评测引擎 — TOP50 × 6 Models
# ═══════════════════════════════════════════════════════════════════

class BatchBenchmark:
    """
    批量基准评测引擎

    加载 TOP50 Skills 数据集，对每个 Skill 用 6 个大模型跑标准化 Prompt，
    生成 50×6=300 个评分单元的完整矩阵。

    使用:
        batch = BatchBenchmark(mode="mock", n_runs=3)
        matrix = batch.run_full_benchmark()
        report_md = batch.generate_matrix_report(matrix)
        batch.save_matrix(matrix, "reports/benchmark")
    """

    # 6 个评测模型 (不含 mock)
    DEFAULT_MODELS = [
        "claude-opus-4.6", "minimax-2.5", "glm-5",
        "gpt-5.4", "gemini-3.0-pro", "deepseek-3.2",
    ]

    def __init__(
        self,
        models: List[str] = None,
        mode: str = "mock",
        n_runs: int = 3,
        output_dir: str = "reports/benchmark",
    ):
        self.model_keys = models or self.DEFAULT_MODELS
        self.mode = mode
        self.n_runs = n_runs
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        self.tester = LLMBaselineTester(
            models=self.model_keys, mode=mode, cache_dir=output_dir,
        )
        self._dataset = None

    def _load_dataset(self) -> List[Dict]:
        """加载 Skills 基准数据集 (TOP1000)"""
        if self._dataset:
            return self._dataset
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        # 加载 TOP1000 基准数据集（优先），如无法匹配具体 Skill 则使用均值作为基准线
        for fname in ("top1000_skills_dataset.json",):
            ds_path = os.path.join(data_dir, fname)
            if os.path.exists(ds_path):
                with open(ds_path, "r", encoding="utf-8") as f:
                    self._dataset = json.load(f)
                logger.info(f"加载基准数据集: {fname} ({len(self._dataset)} Skills)")
                return self._dataset
        raise FileNotFoundError("找不到 Skills 基准数据集文件 (top1000_skills_dataset.json)")

    def get_baseline_for_skill(self, slug: str, model_key: str) -> Dict:
        """
        获取指定 Skill + Model 的基准分数。

        优先级:
          1. 精确匹配 slug + model_key → 返回该 Skill 在该模型上的真实评测分数
          2. 精确匹配 slug → 返回该 Skill 跨模型平均基准分
          3. 同分类平均值
          4. 全局平均值 (最终回退)

        Returns:
            {"quality": float, "success_rate": float, "latency_ms": float,
             "source": "exact_model"|"exact"|"category_avg"|"global_avg"}
        """
        dataset = self._load_dataset()

        # 1. 精确匹配 slug
        for skill in dataset:
            if skill["slug"] == slug:
                # 1a. 如果有 model_baselines 且包含指定模型 → 最精确
                model_bl = skill.get("model_baselines", {}).get(model_key)
                if model_bl:
                    return {
                        "quality": model_bl["quality"],
                        "success_rate": model_bl["success_rate"],
                        "latency_ms": model_bl["latency_ms"],
                        "source": "exact_model",
                        "slug": slug,
                        "model": model_key,
                    }
                # 1b. 有跨模型平均基准 (baseline_quality 字段存在)
                if "baseline_quality" in skill:
                    return {
                        "quality": skill["baseline_quality"],
                        "success_rate": skill["baseline_success_rate"],
                        "latency_ms": skill["baseline_latency_ms"],
                        "source": "exact",
                        "slug": slug,
                    }
                # 1c. slug 匹配但无评测数据 → fallback 到默认值
                return {
                    "quality": 80.0,
                    "success_rate": 0.90,
                    "latency_ms": 2500,
                    "source": "exact_no_data",
                    "slug": slug,
                }

        # 2. 按分类匹配 — 找到同分类的所有 Skills 取平均值
        target_skill_category = None
        for skill in dataset:
            if slug.startswith(skill.get("category", "")[:3]):
                target_skill_category = skill["category"]
                break
        if target_skill_category:
            same_cat = [s for s in dataset
                        if s["category"] == target_skill_category and "baseline_quality" in s]
            if same_cat:
                avg_quality = sum(s["baseline_quality"] for s in same_cat) / len(same_cat)
                avg_sr = sum(s["baseline_success_rate"] for s in same_cat) / len(same_cat)
                avg_lat = sum(s["baseline_latency_ms"] for s in same_cat) / len(same_cat)
                return {
                    "quality": round(avg_quality, 1),
                    "success_rate": round(avg_sr, 3),
                    "latency_ms": round(avg_lat),
                    "source": "category_avg",
                    "category": target_skill_category,
                    "n_skills": len(same_cat),
                }

        # 3. 全局平均值作为最终回退基准线
        with_bl = [s for s in dataset if "baseline_quality" in s]
        if with_bl:
            avg_quality = sum(s["baseline_quality"] for s in with_bl) / len(with_bl)
            avg_sr = sum(s["baseline_success_rate"] for s in with_bl) / len(with_bl)
            avg_lat = sum(s["baseline_latency_ms"] for s in with_bl) / len(with_bl)
        else:
            avg_quality, avg_sr, avg_lat = 80.0, 0.90, 2500
        return {
            "quality": round(avg_quality, 1),
            "success_rate": round(avg_sr, 3),
            "latency_ms": round(avg_lat),
            "source": "global_avg",
            "n_skills": len(with_bl) or len(dataset),
        }

    def _get_prompt(self, skill: Dict) -> str:
        """为指定 Skill 生成评测 Prompt"""
        try:
            from skills_monitor.data.benchmark_prompts import get_benchmark_prompt
            return get_benchmark_prompt(skill["task_type"], skill["benchmark_task"])
        except Exception:
            return f"请完成以下任务：\n{skill['benchmark_task']}\n返回结构化 JSON 结果。"

    def run_full_benchmark(
        self,
        limit: int = 50,
        progress_callback: Optional[Callable] = None,
    ) -> BenchmarkMatrix:
        """
        运行完整的 TOP50 × 6 Models 批量评测

        Args:
            limit: 最多评测几个 Skills (调试时可设小)
            progress_callback: fn(current, total, skill_slug, model_key)
        """
        dataset = self._load_dataset()[:limit]
        matrix = BenchmarkMatrix(
            mode=self.mode,
            models=list(self.model_keys),
            skills_count=len(dataset),
            models_count=len(self.model_keys),
            n_runs_per_cell=self.n_runs,
        )

        total_cells = len(dataset) * len(self.model_keys)
        current = 0

        for skill in dataset:
            slug = skill["slug"]
            prompt = self._get_prompt(skill)

            for model_key in self.model_keys:
                current += 1
                if progress_callback:
                    progress_callback(current, total_cells, slug, model_key)

                try:
                    stats = self.tester.run_llm_baseline(
                        model_key, prompt,
                        n_runs=self.n_runs,
                        task_type=skill["task_type"],
                    )

                    # 计算质量评分 (基于成功率 + 速度 + 模型特长)
                    quality = self._calc_quality(stats, model_key, skill["task_type"])

                    cell = SkillModelScore(
                        skill_slug=slug,
                        skill_name=skill["name"],
                        model_key=model_key,
                        model_name=PRESET_MODELS[model_key].display_name,
                        category=skill.get("category", "other"),
                        task_type=skill["task_type"],
                        success_rate=stats.success_rate,
                        avg_latency_ms=stats.avg_duration_ms or 0,
                        avg_cost_usd=stats.avg_cost_usd,
                        quality_score=quality,
                        total_runs=stats.total_runs,
                        success_count=stats.success_count,
                        total_cost_usd=stats.total_cost_usd,
                    )
                    matrix.cells.append(cell)

                except Exception as e:
                    logger.error(f"评测失败 [{slug}] x [{model_key}]: {e}")
                    matrix.cells.append(SkillModelScore(
                        skill_slug=slug, skill_name=skill["name"],
                        model_key=model_key,
                        model_name=PRESET_MODELS.get(model_key, ModelConfig(
                            ModelProvider.MOCK, "", "")).display_name,
                        category=skill.get("category", "other"),
                        task_type=skill["task_type"],
                        success_rate=0, avg_latency_ms=0, avg_cost_usd=0,
                        quality_score=0, total_runs=self.n_runs,
                        success_count=0, total_cost_usd=0,
                    ))

        # 计算汇总
        self._calc_summaries(matrix)
        return matrix

    def _calc_quality(self, stats: BaselineStats, model_key: str, task_type: str) -> float:
        """计算综合质量评分 (0-100)"""
        # 基础分 = 成功率权重 60%
        base = stats.success_rate * 0.6

        # 速度分 = 越快越好, 最高 20 分
        if stats.avg_duration_ms and stats.avg_duration_ms > 0:
            speed_score = max(0, 20 - (stats.avg_duration_ms / 500))
        else:
            speed_score = 0

        # 模型特长加分 (最高 10 分)
        strength = _MODEL_STR.get(model_key, {}).get(task_type, 0)

        # 稳定性 (成功次数/总次数 的额外奖励, 最高 10 分)
        if stats.total_runs > 0:
            stability = (stats.success_count / stats.total_runs) * 10
        else:
            stability = 0

        total = min(100, base + speed_score + strength + stability)
        return round(total, 1)

    def _calc_summaries(self, matrix: BenchmarkMatrix):
        """计算模型维度和分类维度的汇总"""
        from collections import defaultdict

        # 模型维度汇总
        model_cells = defaultdict(list)
        for c in matrix.cells:
            model_cells[c.model_key].append(c)

        for mk, cells in model_cells.items():
            qualities = [c.quality_score for c in cells]
            latencies = [c.avg_latency_ms for c in cells if c.avg_latency_ms > 0]
            costs = [c.avg_cost_usd for c in cells]
            success_rates = [c.success_rate for c in cells]

            matrix.model_summaries[mk] = {
                "model_key": mk,
                "model_name": PRESET_MODELS[mk].display_name,
                "skills_evaluated": len(cells),
                "avg_quality_score": round(statistics.mean(qualities), 1) if qualities else 0,
                "avg_success_rate": round(statistics.mean(success_rates), 1) if success_rates else 0,
                "avg_latency_ms": round(statistics.mean(latencies), 1) if latencies else 0,
                "total_cost_usd": round(sum(costs), 4),
                "avg_cost_per_skill": round(statistics.mean(costs), 6) if costs else 0,
                "best_categories": self._find_best_categories(cells),
            }

        # 分类维度汇总
        cat_cells = defaultdict(lambda: defaultdict(list))
        for c in matrix.cells:
            cat_cells[c.category][c.model_key].append(c)

        for cat, model_map in cat_cells.items():
            model_scores = {}
            for mk, cells in model_map.items():
                q = [c.quality_score for c in cells]
                model_scores[mk] = {
                    "avg_quality": round(statistics.mean(q), 1) if q else 0,
                    "avg_success_rate": round(
                        statistics.mean([c.success_rate for c in cells]), 1
                    ) if cells else 0,
                    "count": len(cells),
                }

            best_model = max(model_scores.items(), key=lambda x: x[1]["avg_quality"])[0] \
                         if model_scores else ""

            matrix.category_summaries[cat] = {
                "category": cat,
                "total_skills": sum(v["count"] for v in model_scores.values()) // max(len(model_scores), 1),
                "best_model": best_model,
                "best_model_name": PRESET_MODELS.get(best_model, ModelConfig(
                    ModelProvider.MOCK, "", "")).display_name,
                "model_scores": model_scores,
            }

    def _find_best_categories(self, cells: List[SkillModelScore]) -> List[str]:
        """找出该模型表现最好的分类"""
        from collections import defaultdict
        cat_q = defaultdict(list)
        for c in cells:
            cat_q[c.category].append(c.quality_score)
        avgs = {cat: statistics.mean(qs) for cat, qs in cat_q.items()}
        sorted_cats = sorted(avgs.items(), key=lambda x: x[1], reverse=True)
        return [c[0] for c in sorted_cats[:3]]

    # ──────── 保存 ────────

    def save_matrix(self, matrix: BenchmarkMatrix, output_dir: str = None) -> Dict[str, str]:
        """
        保存评测矩阵为多种格式

        Returns:
            {"json": path, "md": path, "csv": path}
        """
        out = output_dir or self.output_dir
        Path(out).mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        paths = {}

        # JSON (完整数据,可上传中心服务器)
        json_path = os.path.join(out, f"benchmark_matrix_{ts}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(matrix.to_dict(), f, ensure_ascii=False, indent=2)
        paths["json"] = json_path

        # Markdown 报告
        md_path = os.path.join(out, f"benchmark_report_{ts}.md")
        report = self.generate_matrix_report(matrix)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(report)
        paths["md"] = md_path

        # CSV (便于导入 Excel/数据库)
        csv_path = os.path.join(out, f"benchmark_matrix_{ts}.csv")
        self._save_csv(matrix, csv_path)
        paths["csv"] = csv_path

        # 精简版 JSON (用于 Skills 内置预存)
        lite_path = os.path.join(out, f"benchmark_lite_{ts}.json")
        self._save_lite(matrix, lite_path)
        paths["lite_json"] = lite_path

        logger.info(f"评测矩阵已保存: {paths}")
        return paths

    def _save_csv(self, matrix: BenchmarkMatrix, path: str):
        """保存为 CSV"""
        header = "rank,skill_slug,skill_name,category,task_type,model_key,model_name," \
                 "success_rate,avg_latency_ms,avg_cost_usd,quality_score\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(header)
            for i, c in enumerate(matrix.cells, 1):
                f.write(f"{i},{c.skill_slug},{c.skill_name},{c.category},{c.task_type},"
                        f"{c.model_key},{c.model_name},"
                        f"{c.success_rate:.1f},{c.avg_latency_ms:.1f},"
                        f"{c.avg_cost_usd:.6f},{c.quality_score:.1f}\n")

    def _save_lite(self, matrix: BenchmarkMatrix, path: str):
        """保存精简版 (用于 Skills 内置预存，去掉详细运行数据)"""
        lite = {
            "version": matrix.version,
            "mode": matrix.mode,
            "generated_at": matrix.generated_at,
            "models": matrix.models,
            "skills_count": matrix.skills_count,
            "model_ranking": matrix.get_model_ranking(),
            "category_leaders": {
                cat: info.get("best_model_name", "")
                for cat, info in matrix.category_summaries.items()
            },
            "matrix": {},  # skill_slug -> {model_key -> quality_score}
        }
        for c in matrix.cells:
            lite["matrix"].setdefault(c.skill_slug, {})[c.model_key] = {
                "q": round(c.quality_score, 1),
                "sr": round(c.success_rate, 1),
                "ms": round(c.avg_latency_ms, 0),
                "cost": round(c.avg_cost_usd, 6),
            }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(lite, f, ensure_ascii=False, indent=2)

    # ──────── 矩阵报告生成 ────────

    def generate_matrix_report(self, matrix: BenchmarkMatrix) -> str:
        """生成完整的 Markdown 矩阵评测报告"""
        lines = [
            "# 🧪 Skills × LLM 跨模型基准评测报告",
            "",
            f"> **评测规模**: {matrix.skills_count} Skills × {matrix.models_count} Models = "
            f"{len(matrix.cells)} 评测单元  ",
            f"> **每单元运行**: {matrix.n_runs_per_cell} 次  ",
            f"> **运行模式**: `{matrix.mode}`  ",
            f"> **生成时间**: {matrix.generated_at}  ",
            f"> **版本**: Skills Monitor v{matrix.version}",
            "", "---", "",
        ]

        # 1. 模型综合排行
        lines.extend(self._section_model_ranking(matrix))
        # 2. 分类最佳模型
        lines.extend(self._section_category_leaders(matrix))
        # 3. 完整矩阵 (按分类分组)
        lines.extend(self._section_full_matrix(matrix))
        # 4. 成本对比
        lines.extend(self._section_cost_comparison(matrix))
        # 5. 结论
        lines.extend(self._section_conclusion(matrix))

        lines.extend([
            "", "---", "",
            "*报告由 Skills Monitor v0.6.0 BatchBenchmark 引擎生成*  ",
            f"*数据格式兼容中心服务器存储和 Skills 内置预存*",
        ])

        return "\n".join(lines)

    def _section_model_ranking(self, matrix: BenchmarkMatrix) -> List[str]:
        lines = ["## 🏆 模型综合排行", ""]
        ranking = matrix.get_model_ranking()
        lines.append("| 排名 | 模型 | 综合质量 | 平均成功率 | 平均延迟 | 总费用 | 最强分类 |")
        lines.append("|:----:|------|:-------:|:---------:|:-------:|:-----:|---------|")
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣"]
        for i, m in enumerate(ranking):
            medal = medals[i] if i < len(medals) else f"{i+1}"
            best_cats = ", ".join(m.get("best_categories", [])[:2])
            lines.append(
                f"| {medal} | **{m['model_name']}** | "
                f"{m['avg_quality_score']:.1f} | "
                f"{m['avg_success_rate']:.1f}% | "
                f"{m['avg_latency_ms']:.0f}ms | "
                f"${m['total_cost_usd']:.4f} | "
                f"{best_cats} |"
            )
        lines.extend(["", "---", ""])
        return lines

    def _section_category_leaders(self, matrix: BenchmarkMatrix) -> List[str]:
        lines = ["## 📂 分类最佳模型", ""]
        lines.append("| 分类 | Skills 数 | 最佳模型 | 该模型平均质量 |")
        lines.append("|------|:---------:|---------|:------------:|")
        from skills_monitor.data.category_mapping import CLAWHUB_CATEGORIES
        for cat, info in sorted(matrix.category_summaries.items()):
            cat_meta = CLAWHUB_CATEGORIES.get(cat, {"icon": "📦", "name": cat})
            best = info.get("best_model_name", "N/A")
            best_key = info.get("best_model", "")
            ms = info.get("model_scores", {}).get(best_key, {})
            q = ms.get("avg_quality", 0)
            lines.append(
                f"| {cat_meta['icon']} {cat_meta['name']} | "
                f"{info.get('total_skills', 0)} | "
                f"**{best}** | {q:.1f} |"
            )
        lines.extend(["", "---", ""])
        return lines

    def _section_full_matrix(self, matrix: BenchmarkMatrix) -> List[str]:
        lines = ["## 📊 完整评测矩阵", ""]
        model_names = [PRESET_MODELS[k].display_name for k in self.model_keys]
        # 表头
        header = "| # | Skill | 分类 |"
        separator = "|:-:|-------|------|"
        for mn in model_names:
            short = mn.split()[0] if len(mn) > 10 else mn  # 缩短表头
            header += f" {short} |"
            separator += ":---------:|"
        lines.extend([header, separator])

        # 按分类排序
        dataset = self._load_dataset()
        for i, skill in enumerate(dataset, 1):
            slug = skill["slug"]
            row = f"| {i} | {skill['name']} | {skill.get('category','')} |"
            for mk in self.model_keys:
                cell = None
                for c in matrix.cells:
                    if c.skill_slug == slug and c.model_key == mk:
                        cell = c; break
                if cell:
                    # 用 emoji 表示质量等级
                    q = cell.quality_score
                    if q >= 80: icon = "🟢"
                    elif q >= 60: icon = "🟡"
                    elif q >= 40: icon = "🟠"
                    else: icon = "🔴"
                    row += f" {icon} {q:.0f} |"
                else:
                    row += " ❌ - |"
            lines.append(row)

        lines.extend([
            "",
            "> 🟢 ≥80 | 🟡 ≥60 | 🟠 ≥40 | 🔴 <40 | ❌ 评测失败",
            "", "---", "",
        ])
        return lines

    def _section_cost_comparison(self, matrix: BenchmarkMatrix) -> List[str]:
        lines = ["## 💰 成本对比 (每次调用平均费用)", ""]
        lines.append("| 模型 | 输入价/1K tok | 输出价/1K tok | 评测总费用 | 平均/Skill |")
        lines.append("|------|:-----------:|:-----------:|:---------:|:---------:|")
        for mk in self.model_keys:
            cfg = PRESET_MODELS[mk]
            sm = matrix.model_summaries.get(mk, {})
            lines.append(
                f"| {cfg.display_name} | "
                f"${cfg.cost_per_1k_input:.4f} | "
                f"${cfg.cost_per_1k_output:.4f} | "
                f"${sm.get('total_cost_usd', 0):.4f} | "
                f"${sm.get('avg_cost_per_skill', 0):.6f} |"
            )
        lines.extend(["", "---", ""])
        return lines

    def _section_conclusion(self, matrix: BenchmarkMatrix) -> List[str]:
        lines = ["## 💡 结论与建议", ""]
        ranking = matrix.get_model_ranking()
        if not ranking:
            lines.append("无足够数据生成结论。")
            return lines

        top = ranking[0]
        lines.append(f"### 综合最强：**{top['model_name']}**")
        lines.append(f"- 综合质量评分 **{top['avg_quality_score']:.1f}/100**")
        lines.append(f"- 平均成功率 **{top['avg_success_rate']:.1f}%**")
        lines.append(f"- 平均延迟 **{top['avg_latency_ms']:.0f}ms**")
        lines.append("")

        # 性价比之王
        if len(ranking) > 1:
            # 质量/费用 比值最高的
            best_ratio = max(ranking,
                key=lambda x: x["avg_quality_score"] / max(x.get("total_cost_usd", 0.001), 0.001))
            lines.append(f"### 性价比之王：**{best_ratio['model_name']}**")
            lines.append(f"- 质量 {best_ratio['avg_quality_score']:.1f}，"
                         f"费用仅 ${best_ratio.get('total_cost_usd', 0):.4f}")
            lines.append("")

        # 速度之王
        fastest = min(ranking, key=lambda x: x.get("avg_latency_ms", 99999))
        lines.append(f"### 速度之王：**{fastest['model_name']}**")
        lines.append(f"- 平均延迟 **{fastest['avg_latency_ms']:.0f}ms**")
        lines.append("")

        # 分类推荐
        lines.append("### 分类推荐")
        for cat, info in sorted(matrix.category_summaries.items()):
            best_name = info.get("best_model_name", "N/A")
            lines.append(f"- **{cat}**: 推荐 {best_name}")

        lines.append("")
        return lines
