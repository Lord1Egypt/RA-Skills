#!/usr/bin/env python3
"""Reusable local LLM memory-fit estimator.

The estimator plans single-GPU text-generation inference.  It deliberately
separates model weights, runtime reserve and KV cache instead of treating model
parameter count as the final VRAM figure.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
YAML_SUFFIX = "." + "yaml"
_YAML_POLICY_PATH = ROOT / "data" / f"model_fit{YAML_SUFFIX}"
_TEXT_POLICY_PATH = ROOT / "data" / "model_fit.txt"
DEFAULT_POLICY_PATH = _YAML_POLICY_PATH if _YAML_POLICY_PATH.exists() else _TEXT_POLICY_PATH
PARAMETER_LABEL_TOLERANCE = 1.05


class ModelFitError(ValueError):
    """Structured input/data error for the model-fit CLI."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message

    def as_dict(self) -> dict:
        return {"code": self.code, "message": self.message}


@dataclass(frozen=True)
class ModelSpec:
    id: str
    name: str
    params_b: float
    architecture: str = "unknown"
    active_params_b: float | None = None
    hf_repo: str | None = None
    num_hidden_layers: int | None = None
    num_attention_heads: int | None = None
    num_key_value_heads: int | None = None
    hidden_size: int | None = None
    head_dim: int | None = None
    native_context_tokens: int | None = None
    default_quantization: str = "q4"
    default_context_tokens: int = 4096

    @classmethod
    def from_mapping(cls, value: dict) -> "ModelSpec":
        return cls(**{field: value[field] for field in cls.__dataclass_fields__ if field in value})


@dataclass(frozen=True)
class HardwareSpec:
    vram_gib: float
    ram_gib: float | None = None
    memory_generation: str | None = None
    memory_mt: int | None = None


@dataclass(frozen=True)
class MemoryBreakdown:
    weights_gib: float
    runtime_gib: float
    kv_cache_gib: float | None
    estimated_total_gib: float | None
    config_complete: bool


@dataclass(frozen=True)
class FitPolicy:
    recommended_ratio: float
    conditional_ratio: float
    base_runtime_gib: float
    runtime_ratio: float
    fallback_kv_gib_at_4k: float
    config_required_above_tokens: int
    weight_factors: dict[str, float]
    vram_tiers: tuple[int, ...]
    capacity_tiers: tuple[dict, ...]
    ram_tiers: tuple[int, ...]
    os_reserve_gib: float
    offload_multiplier: float
    slow_memory_threshold_mt: dict[str, int]

    @classmethod
    def from_mapping(cls, value: dict) -> "FitPolicy":
        return cls(
            recommended_ratio=float(value["recommended_vram_utilization"]),
            conditional_ratio=float(value["conditional_vram_utilization"]),
            base_runtime_gib=float(value["base_runtime_gib"]),
            runtime_ratio=float(value["runtime_vram_ratio"]),
            fallback_kv_gib_at_4k=float(value["fallback_kv_gib_at_4k"]),
            config_required_above_tokens=int(value["config_required_above_tokens"]),
            weight_factors={key: float(number) for key, number in value["weight_gib_per_billion_params"].items()},
            vram_tiers=tuple(int(number) for number in value["vram_tiers_gib"]),
            capacity_tiers=tuple(dict(item) for item in value["capacity_tiers"]),
            ram_tiers=tuple(int(number) for number in value["system_ram_tiers_gib"]),
            os_reserve_gib=float(value["os_and_apps_reserve_gib"]),
            offload_multiplier=float(value["offload_multiplier"]),
            slow_memory_threshold_mt={key.upper(): int(number) for key, number in value["slow_memory_threshold_mt"].items()},
        )


@dataclass(frozen=True)
class ModelFitCatalog:
    policy: FitPolicy
    models: tuple[ModelSpec, ...]
    metadata: dict
    sources: dict

    def model(self, model_id: str) -> ModelSpec:
        target = str(model_id or "").strip().casefold()
        for item in self.models:
            aliases = {item.id.casefold(), item.name.casefold(), str(item.hf_repo or "").casefold()}
            if target in aliases:
                return item
        raise ModelFitError("model_not_found", f"离线模型样本未收录：{model_id}")


def load_catalog(path: Path | str = DEFAULT_POLICY_PATH) -> ModelFitCatalog:
    source = Path(path)
    try:
        document = yaml.safe_load(source.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ModelFitError("invalid_model_fit_data", f"无法读取模型适配数据：{exc}") from exc
    if not isinstance(document.get("policy"), dict) or not isinstance(document.get("models"), list):
        raise ModelFitError("invalid_model_fit_data", "模型适配数据缺少 policy 或 models")
    try:
        policy = FitPolicy.from_mapping(document["policy"])
        models = tuple(ModelSpec.from_mapping(item) for item in document["models"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ModelFitError("invalid_model_fit_data", f"模型适配数据字段无效：{exc}") from exc
    if not models or any(not model.id or model.params_b <= 0 for model in models):
        raise ModelFitError("invalid_model_fit_data", "模型适配样本必须有正参数量和唯一 ID")
    if len({model.id for model in models}) != len(models):
        raise ModelFitError("invalid_model_fit_data", "模型适配样本 ID 重复")
    return ModelFitCatalog(policy=policy, models=models, metadata=document.get("metadata", {}), sources=document.get("sources", {}))


def _round_gib(value: float | None) -> float | None:
    return None if value is None else round(value, 2)


def kv_cache_gib(model: ModelSpec, context_tokens: int, batch_size: int = 1, dtype_bytes: int = 2) -> float | None:
    if context_tokens <= 0 or batch_size <= 0:
        raise ModelFitError("invalid_request", "上下文和并发数必须是正整数")
    required = (model.num_hidden_layers, model.num_attention_heads, model.num_key_value_heads)
    if any(value is None or value <= 0 for value in required):
        return None
    head_dim = model.head_dim
    if not head_dim and model.hidden_size:
        head_dim = model.hidden_size / model.num_attention_heads
    if not head_dim:
        return None
    bytes_used = (
        2 * model.num_hidden_layers * model.num_key_value_heads * head_dim
        * dtype_bytes * context_tokens * batch_size
    )
    return bytes_used / (1024 ** 3)


def estimate_memory(model: ModelSpec, hardware: HardwareSpec, policy: FitPolicy,
                    quantization: str, context_tokens: int, batch_size: int = 1) -> MemoryBreakdown:
    quant = quantization.lower()
    if quant not in policy.weight_factors:
        raise ModelFitError("invalid_quantization", f"不支持的量化档：{quantization}")
    if hardware.vram_gib <= 0:
        raise ModelFitError("invalid_request", "显存必须大于 0")
    if model.native_context_tokens and context_tokens > model.native_context_tokens:
        raise ModelFitError(
            "context_exceeds_model_limit",
            f"请求上下文 {context_tokens} 超过离线模型配置记录的 {model.native_context_tokens} tokens；"
            "如使用 YaRN/RoPE 扩展，需先联网核对该模型官方配置后重新估算。",
        )
    weights = model.params_b * policy.weight_factors[quant]
    runtime = max(policy.base_runtime_gib, hardware.vram_gib * policy.runtime_ratio)
    cache = kv_cache_gib(model, context_tokens, batch_size)
    if cache is None and context_tokens <= policy.config_required_above_tokens:
        cache = policy.fallback_kv_gib_at_4k * context_tokens / policy.config_required_above_tokens * batch_size
    total = None if cache is None else weights + runtime + cache
    return MemoryBreakdown(
        weights_gib=_round_gib(weights),
        runtime_gib=_round_gib(runtime),
        kv_cache_gib=_round_gib(cache),
        estimated_total_gib=_round_gib(total),
        config_complete=kv_cache_gib(model, context_tokens, batch_size) is not None,
    )


def next_tier(required_gib: float, tiers: tuple[int, ...]) -> int | None:
    return next((tier for tier in tiers if tier >= required_gib), None)


def _preferred_ram_for_vram(vram_gib: float, policy: FitPolicy) -> int:
    for row in policy.capacity_tiers:
        if vram_gib <= float(row["vram_gib"]):
            return int(row["preferred_ram_gib"])
    return int(policy.capacity_tiers[-1]["preferred_ram_gib"])


def _capacity_for_vram(vram_gib: float, policy: FitPolicy) -> dict:
    return next(
        (row for row in policy.capacity_tiers if vram_gib <= float(row["vram_gib"])),
        policy.capacity_tiers[-1],
    )


def _required_ram(offload_gib: float, policy: FitPolicy) -> int:
    raw = policy.os_reserve_gib + policy.offload_multiplier * max(0.0, offload_gib)
    return next_tier(raw, policy.ram_tiers) or math.ceil(raw)


def slow_memory_warning(hardware: HardwareSpec, offload_gib: float, policy: FitPolicy) -> str | None:
    if offload_gib <= 0:
        return None
    generation = str(hardware.memory_generation or "").upper()
    threshold = policy.slow_memory_threshold_mt.get(generation)
    if not threshold or not hardware.memory_mt:
        return "当前方案需要 CPU/KV offload；内存代际或频率未知，响应速度需实测。"
    if hardware.memory_mt < threshold:
        return (
            f"当前方案需要 CPU/KV offload，{generation} {hardware.memory_mt} MT/s 低于保守警戒值 "
            f"{threshold} MT/s，响应会明显变慢；内存频率不会把该方案升级为推荐。"
        )
    return None


def evaluate_model(model: ModelSpec, hardware: HardwareSpec, policy: FitPolicy,
                   quantization: str, context_tokens: int, batch_size: int = 1) -> dict:
    memory = estimate_memory(model, hardware, policy, quantization, context_tokens, batch_size)
    if memory.estimated_total_gib is None:
        return {
            "status": "needs_model_config",
            "reason": "缺少 KV cache 结构字段；超过 4K 上下文不得给推荐结论。",
            "memory": memory.__dict__,
            "required_ram_gib": _preferred_ram_for_vram(hardware.vram_gib, policy),
            "slow_memory_warning": None,
        }
    utilization = memory.estimated_total_gib / hardware.vram_gib
    offload = max(0.0, memory.estimated_total_gib - hardware.vram_gib)
    preferred_ram = _preferred_ram_for_vram(hardware.vram_gib, policy)
    required_ram = max(min(32, preferred_ram), _required_ram(offload, policy))
    if utilization <= policy.recommended_ratio:
        status = "recommended"
        offload = 0.0
    elif utilization <= policy.conditional_ratio:
        status = "conditional"
    elif utilization <= 1.0:
        status = "conditional"
    elif (
        quantization == "q4"
        and 29 <= model.params_b <= 35
        and hardware.vram_gib >= 24
    ):
        status = "needs_offload" if hardware.ram_gib and hardware.ram_gib >= required_ram else "not_recommended"
    else:
        status = "needs_offload" if hardware.ram_gib and hardware.ram_gib >= required_ram else "not_recommended"
    capacity = _capacity_for_vram(hardware.vram_gib, policy)
    if quantization == "q4" and model.params_b > float(capacity["conditional_max_params_b"]) * PARAMETER_LABEL_TOLERANCE:
        if status in {"recommended", "conditional", "needs_offload"}:
            status = "not_recommended"
    elif (
        quantization == "q4"
        and model.params_b > float(capacity["recommended_max_params_b"]) * PARAMETER_LABEL_TOLERANCE
        and status == "recommended"
    ):
        status = "conditional"
    if hardware.ram_gib and hardware.ram_gib < required_ram:
        status = "ram_insufficient"
    return {
        "status": status,
        "vram_utilization": round(utilization, 3),
        "offload_gib": _round_gib(offload),
        "required_ram_gib": required_ram,
        "slow_memory_warning": slow_memory_warning(hardware, offload, policy),
        "memory": memory.__dict__,
    }


def model_for_params(params_b: float, catalog: ModelFitCatalog) -> ModelSpec:
    if params_b <= 0:
        raise ModelFitError("invalid_request", "模型参数量必须大于 0B")
    return ModelSpec(
        id=f"generic-{params_b:g}b",
        name=f"通用 {params_b:g}B 模型",
        params_b=params_b,
        default_quantization="q4",
        default_context_tokens=4096,
    )


def reverse_recommendation(model: ModelSpec, catalog: ModelFitCatalog, quantization: str,
                           context_tokens: int, batch_size: int = 1) -> dict:
    policy = catalog.policy
    minimum_tier = None
    recommended_tier = None
    tier_results = []
    for tier in policy.vram_tiers:
        result = evaluate_model(model, HardwareSpec(vram_gib=tier), policy, quantization, context_tokens, batch_size)
        tier_results.append({"vram_gib": tier, "status": result["status"], "estimated_total_gib": result["memory"]["estimated_total_gib"]})
        if minimum_tier is None and result["status"] in {"recommended", "conditional"}:
            minimum_tier = tier
        if recommended_tier is None and result["status"] == "recommended":
            recommended_tier = tier
    if tier_results and all(row["status"] == "needs_model_config" for row in tier_results):
        return {
            "minimum_vram_gib": None,
            "recommended_vram_gib": None,
            "preferred_ram_gib": None,
            "needs_model_config": True,
            "tier_results": tier_results,
        }
    if minimum_tier is None:
        memory = estimate_memory(model, HardwareSpec(vram_gib=policy.vram_tiers[-1]), policy, quantization, context_tokens, batch_size)
        required = memory.estimated_total_gib or model.params_b * policy.weight_factors[quantization]
        minimum_tier = next_tier(required / policy.conditional_ratio, policy.vram_tiers)
    if recommended_tier is None:
        memory = estimate_memory(model, HardwareSpec(vram_gib=policy.vram_tiers[-1]), policy, quantization, context_tokens, batch_size)
        required = memory.estimated_total_gib or model.params_b * policy.weight_factors[quantization]
        recommended_tier = next_tier(required / policy.recommended_ratio, policy.vram_tiers)

    # A 30/32B Q4 model may fit 24 GiB at short context, but the 32 GiB tier
    # is the first stable consumer tier with useful room for cache and runtime.
    if 29 <= model.params_b <= 35 and quantization == "q4" and recommended_tier is not None:
        recommended_tier = max(32, recommended_tier or 32)

    preferred_ram = _preferred_ram_for_vram(recommended_tier, policy) if recommended_tier is not None else None
    # Consumer 30/32B Q4 inference is usually all-GPU on a 32 GiB card; 32 GiB
    # system RAM is the capacity floor, while 64 GiB remains the safer upgrade
    # when long context, offload or several local tools must coexist.
    if 29 <= model.params_b <= 35 and quantization == "q4" and recommended_tier is not None and recommended_tier <= 32:
        preferred_ram = 32
    return {
        "minimum_vram_gib": minimum_tier,
        "recommended_vram_gib": recommended_tier,
        "preferred_ram_gib": preferred_ram,
        "tier_results": tier_results,
    }


def forward_profile(hardware: HardwareSpec, catalog: ModelFitCatalog) -> dict:
    policy = catalog.policy
    capacity = _capacity_for_vram(hardware.vram_gib, policy)
    evaluations = []
    for model in catalog.models:
        result = evaluate_model(
            model,
            hardware,
            policy,
            model.default_quantization,
            model.default_context_tokens,
        )
        evaluations.append({
            "model_id": model.id,
            "model": model.name,
            "params_b": model.params_b,
            "quantization": model.default_quantization,
            "context_tokens": model.default_context_tokens,
            **result,
        })
    return {
        "vram_gib": hardware.vram_gib,
        "ram_gib": hardware.ram_gib,
        "recommended_max_params_b": capacity["recommended_max_params_b"],
        "conditional_max_params_b": capacity["conditional_max_params_b"],
        "preferred_ram_gib": capacity["preferred_ram_gib"],
        "models": evaluations,
    }
