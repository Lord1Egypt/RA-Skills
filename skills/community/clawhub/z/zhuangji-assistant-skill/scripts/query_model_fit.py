#!/usr/bin/env python3
"""双向查询本地大模型与显卡/内存容量的保守适配关系。"""

from __future__ import annotations

import argparse
import json
import sys

from catalog_overlay import OverlayError
from model_fit import (
    HardwareSpec,
    ModelFitError,
    evaluate_model,
    forward_profile,
    load_catalog,
    model_for_params,
    reverse_recommendation,
)
from query_components import configure_overlays, query, summarize


try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def _positive(value, label):
    if value is None:
        return None
    number = float(value)
    if number <= 0:
        raise ModelFitError("invalid_request", f"{label}必须大于 0")
    return number


def _exact_component(category, item_id):
    if not item_id:
        return None
    rows = query(
        category=category,
        item_id=item_id,
        include_legacy=True,
        include_workstation_gpu=category == "gpu",
        gpu_cooling="any" if category == "gpu" else None,
        has_price_only=False,
        limit=2,
    )
    if len(rows) != 1:
        raise ModelFitError("component_not_found", f"找不到唯一的{category}硬件 ID：{item_id}")
    return rows[0]


def _hardware_from_args(args):
    gpu = _exact_component("gpu", args.gpu_id)
    memory = _exact_component("memory", args.memory_id)
    vram = args.vram_gib if args.vram_gib is not None else (gpu or {}).get("vram_gb")
    ram = args.ram_gib if args.ram_gib is not None else (memory or {}).get("capacity_gb")
    generation = args.memory_generation or (memory or {}).get("generation")
    memory_mt = args.memory_mt if args.memory_mt is not None else (memory or {}).get("frequency_mt")
    if vram is None:
        return None, gpu, memory
    hardware = HardwareSpec(
        vram_gib=_positive(vram, "显存"),
        ram_gib=_positive(ram, "系统内存") if ram is not None else None,
        memory_generation=str(generation).upper() if generation else None,
        memory_mt=int(_positive(memory_mt, "内存频率")) if memory_mt is not None else None,
    )
    return hardware, gpu, memory


def _candidate_rows(vram_gib, limit):
    if not vram_gib:
        return []
    rows = query(
        category="gpu",
        min_vram=int(vram_gib),
        include_workstation_gpu=vram_gib >= 48,
        gpu_cooling="any",
        has_price_only=True,
        sort="asc",
        limit=max(50, limit * 8),
    )
    rows.sort(key=lambda item: (float(item.get("vram_gb") or 0) != float(vram_gib), item.get("price_cny") or 10**9, item.get("id", "")))
    return [summarize(item, "gpu") for item in rows[:limit]]


def build_result(args):
    catalog = load_catalog()
    configure_overlays(args.overlay, args.currency)
    hardware, gpu, memory = _hardware_from_args(args)

    requested_model = None
    if args.model:
        requested_model = catalog.model(args.model)
    elif args.params_b is not None:
        requested_model = model_for_params(_positive(args.params_b, "模型参数量"), catalog)

    if not requested_model and not hardware:
        raise ModelFitError("invalid_request", "请给出 --model/--params-b，或 --gpu-id/--vram-gib")

    result = {
        "ok": True,
        "scope": catalog.metadata.get("scope"),
        "assumptions": {
            "single_gpu": True,
            "single_concurrency": args.batch_size == 1,
            "inference_only": True,
            "estimate_not_benchmark": True,
        },
    }
    if gpu:
        result["gpu"] = summarize(gpu, "gpu")
    if memory:
        result["memory"] = summarize(memory, "memory")

    if requested_model:
        quantization = args.quantization or requested_model.default_quantization
        context_tokens = args.context_tokens or requested_model.default_context_tokens
        result["model"] = {
            "id": requested_model.id,
            "name": requested_model.name,
            "hf_repo": requested_model.hf_repo,
            "params_b": requested_model.params_b,
            "active_params_b": requested_model.active_params_b,
            "architecture": requested_model.architecture,
            "native_context_tokens": requested_model.native_context_tokens,
        }
        result["request"] = {
            "quantization": quantization,
            "context_tokens": context_tokens,
            "batch_size": args.batch_size,
        }
        reverse = reverse_recommendation(requested_model, catalog, quantization, context_tokens, args.batch_size)
        result["hardware_recommendation"] = reverse
        result["minimum_gpu_candidates"] = _candidate_rows(reverse["minimum_vram_gib"], args.limit)
        result["recommended_gpu_candidates"] = _candidate_rows(reverse["recommended_vram_gib"], args.limit)
        if hardware:
            result["fit_on_given_hardware"] = evaluate_model(
                requested_model,
                hardware,
                catalog.policy,
                quantization,
                context_tokens,
                args.batch_size,
            )

    if hardware and not requested_model:
        result["hardware"] = {
            "vram_gib": hardware.vram_gib,
            "ram_gib": hardware.ram_gib,
            "memory_generation": hardware.memory_generation,
            "memory_mt": hardware.memory_mt,
        }
        result["model_profile"] = forward_profile(hardware, catalog)
    return result


def _human(result):
    if "hardware_recommendation" in result:
        model = result["model"]
        request = result["request"]
        recommendation = result["hardware_recommendation"]
        if recommendation.get("needs_model_config"):
            return (
                f"{model['name']} 缺少计算长上下文 KV cache 所需的模型结构字段；"
                "请先读取该 Hugging Face repo 的官方 config.json，再给显存档结论。"
            )
        if recommendation.get("recommended_vram_gib") is None:
            return (
                f"{model['name']} 在当前量化、上下文和并发条件下超过离线策略覆盖的单卡显存档；"
                "请缩短上下文、降低并发、使用更小模型，或另行核验多卡/工作站方案。"
            )
        lines = [
            f"{model['name']}（按 {model['params_b']}B 总参数、{request['quantization']}、{request['context_tokens']} tokens、单并发估算）：",
            f"最低显存档约 {recommendation['minimum_vram_gib']}GB；更稳妥的推荐档为 {recommendation['recommended_vram_gib']}GB，系统内存至少 {recommendation['preferred_ram_gib']}GB。",
        ]
        if model.get("active_params_b"):
            lines.append(f"这是 MoE 模型；虽然每 token 约激活 {model['active_params_b']}B 参数，加载权重仍按 {model['params_b']}B 总参数规划。")
        if recommendation["recommended_vram_gib"] == 32 and recommendation["preferred_ram_gib"] == 32:
            lines.append("若需要长上下文、CPU/KV offload 或同时常驻多个本地工具，系统内存升级到 64GB 更稳。")
        if result.get("fit_on_given_hardware"):
            lines.append(f"给定硬件评估：{result['fit_on_given_hardware']['status']}。")
        candidates = result.get("recommended_gpu_candidates", [])
        if candidates:
            names = "；".join(f"{item.get('model')}（{item.get('vram_gb')}GB，¥{item.get('price')}）" for item in candidates)
            lines.append(f"当前库内推荐档候选：{names}。")
        lines.append("模型卡最大上下文不等于该显卡可无约束使用的上下文；长上下文、多并发和 offload 需重新估算。")
        return "\n".join(lines)

    profile = result["model_profile"]
    lines = [
        f"{profile['vram_gib']:g}GB 显存：默认推荐约到 {profile['recommended_max_params_b']}B，条件可尝试约到 {profile['conditional_max_params_b']}B；系统内存建议 {profile['preferred_ram_gib']}GB 起。"
    ]
    recommended = [row for row in profile["models"] if row["status"] == "recommended"]
    conditional = [row for row in profile["models"] if row["status"] in {"conditional", "needs_offload"}]
    if recommended:
        lines.append("推荐样本：" + "、".join(f"{row['model']} {row['quantization']}" for row in recommended) + "。")
    if conditional:
        lines.append("条件可跑：" + "、".join(f"{row['model']} {row['quantization']}" for row in conditional) + "；需缩短上下文或接受 offload 降速。")
    lines.append("这是容量规划估算，不是吞吐、首 token 延迟或生成速度实测。")
    return "\n".join(lines)


def _parser():
    parser = argparse.ArgumentParser(description="双向估算本地大模型与显卡/内存容量适配", allow_abbrev=False)
    model_group = parser.add_mutually_exclusive_group()
    model_group.add_argument("--model", help="离线样本 ID、名称或 Hugging Face repo")
    model_group.add_argument("--params-b", type=float, help="模型总参数量（B），例如 30")
    gpu_group = parser.add_mutually_exclusive_group()
    gpu_group.add_argument("--gpu-id", help="库内显卡 ID")
    gpu_group.add_argument("--vram-gib", type=float, help="显存容量（GiB/常见标称 GB 档）")
    ram_group = parser.add_mutually_exclusive_group()
    ram_group.add_argument("--memory-id", help="库内内存 ID")
    ram_group.add_argument("--ram-gib", type=float, help="系统内存容量（GiB/常见标称 GB 档）")
    parser.add_argument("--memory-generation", choices=["DDR4", "DDR5"], help="手动内存代际")
    parser.add_argument("--memory-mt", type=int, help="手动内存速率 MT/s；只在 offload 时触发慢速提示")
    parser.add_argument("--quantization", choices=["q4", "q5", "q8", "bf16"], help="权重量化档；默认采用模型样本建议")
    parser.add_argument("--context-tokens", type=int, help="输入+计划生成的总 token 数")
    parser.add_argument("--batch-size", type=int, default=1, help="并发批大小，默认 1")
    parser.add_argument("--overlay", action="append", default=[], help="显式用户 overlay；可重复")
    parser.add_argument("--currency", choices=["CNY", "USD", "EUR", "GBP", "JPY", "TWD"], default="CNY")
    parser.add_argument("--limit", type=int, default=5, help="每档最多返回多少张显卡")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv=None):
    parser = _parser()
    args = parser.parse_args(argv)
    if args.batch_size <= 0 or args.limit <= 0 or (args.context_tokens is not None and args.context_tokens <= 0):
        parser.error("--batch-size、--limit 和 --context-tokens 必须是正整数")
    try:
        result = build_result(args)
    except (ModelFitError, OverlayError) as exc:
        error = exc.as_dict() if hasattr(exc, "as_dict") else {"code": "invalid_request", "message": str(exc)}
        print(json.dumps({"ok": False, "errors": [error]}, ensure_ascii=False), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_human(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
