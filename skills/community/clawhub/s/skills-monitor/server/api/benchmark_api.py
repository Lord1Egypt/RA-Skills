"""
TOP1000 基准评测 API — LLM 跨模型评测数据服务
=============================================
- GET  /benchmark                         基准评测 Dashboard 页面
- GET  /api/benchmark/summary             评测概览摘要
- GET  /api/benchmark/models              模型排行榜
- GET  /api/benchmark/categories          分类最佳模型
- GET  /api/benchmark/matrix              完整评测矩阵 (支持分页/筛选)
- GET  /api/benchmark/skill/<slug>        单个 Skill 跨模型评测
- GET  /api/benchmark/model/<key>         单个模型全 Skills 评测
- GET  /api/benchmark/compare             模型间对比
"""

import json
import os
import logging
from pathlib import Path
from flask import Blueprint, request, render_template, jsonify

logger = logging.getLogger(__name__)

benchmark_bp = Blueprint("benchmark_api", __name__)

# ── 数据缓存 ──
_benchmark_cache = {"data": None, "lite": None}


def _get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).resolve().parent.parent.parent


def _load_benchmark_data() -> dict:
    """加载完整的 benchmark 矩阵数据"""
    if _benchmark_cache["data"]:
        return _benchmark_cache["data"]

    # 按时间倒序找到最新的 benchmark 文件
    report_dir = _get_project_root() / "reports" / "benchmark"
    if not report_dir.exists():
        return {}

    # 查找 benchmark_matrix_*.json（完整数据）
    matrix_files = sorted(report_dir.glob("benchmark_matrix_*.json"), reverse=True)
    if not matrix_files:
        return {}

    try:
        with open(matrix_files[0], "r", encoding="utf-8") as f:
            data = json.load(f)
        _benchmark_cache["data"] = data
        logger.info(f"加载评测矩阵: {matrix_files[0].name} ({len(data.get('cells', []))} cells)")
        return data
    except Exception as e:
        logger.error(f"加载评测矩阵失败: {e}")
        return {}


def _load_benchmark_lite() -> dict:
    """加载精简版 benchmark 数据"""
    if _benchmark_cache["lite"]:
        return _benchmark_cache["lite"]

    report_dir = _get_project_root() / "reports" / "benchmark"
    if not report_dir.exists():
        return {}

    lite_files = sorted(report_dir.glob("benchmark_lite_*.json"), reverse=True)
    if not lite_files:
        return {}

    try:
        with open(lite_files[0], "r", encoding="utf-8") as f:
            data = json.load(f)
        _benchmark_cache["lite"] = data
        logger.info(f"加载精简评测: {lite_files[0].name}")
        return data
    except Exception as e:
        logger.error(f"加载精简评测失败: {e}")
        return {}


def _load_dataset() -> list:
    """加载 TOP1000 Skills 数据集"""
    ds_path = _get_project_root() / "skills_monitor" / "data" / "top1000_skills_dataset.json"
    if not ds_path.exists():
        return []
    try:
        with open(ds_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


# ──────── 页面路由 ────────

@benchmark_bp.route("/benchmark")
def benchmark_page():
    """基准评测 Dashboard 页面"""
    lite = _load_benchmark_lite()
    data = _load_benchmark_data()
    dataset = _load_dataset()

    # 构建页面数据
    page_data = {
        "version": lite.get("version", "0.6.0"),
        "mode": lite.get("mode", "mock"),
        "generated_at": lite.get("generated_at", "未知"),
        "skills_count": lite.get("skills_count", 0),
        "models": lite.get("models", []),
        "model_ranking": lite.get("model_ranking", []),
        "category_leaders": lite.get("category_leaders", {}),
        "matrix": lite.get("matrix", {}),
        "model_summaries": data.get("model_summaries", {}),
        "category_summaries": data.get("category_summaries", {}),
        "dataset_sample": dataset[:20],  # 页面只需部分数据
    }
    return render_template("benchmark.html", data=page_data)


# ──────── 数据 API ────────

@benchmark_bp.route("/api/benchmark/summary")
def benchmark_summary():
    """评测概览摘要"""
    lite = _load_benchmark_lite()
    data = _load_benchmark_data()

    if not lite:
        return jsonify({"ok": False, "error": "暂无评测数据"}), 404

    # 计算统计
    cells = data.get("cells", [])
    total_cells = len(cells)
    avg_quality = sum(c.get("quality_score", 0) for c in cells) / max(total_cells, 1)
    avg_success = sum(c.get("success_rate", 0) for c in cells) / max(total_cells, 1)
    total_cost = sum(c.get("total_cost_usd", 0) for c in cells)

    return jsonify({
        "ok": True,
        "data": {
            "version": lite.get("version"),
            "mode": lite.get("mode"),
            "generated_at": lite.get("generated_at"),
            "skills_count": lite.get("skills_count", 0),
            "models_count": len(lite.get("models", [])),
            "total_cells": total_cells,
            "avg_quality_score": round(avg_quality, 1),
            "avg_success_rate": round(avg_success, 1),
            "total_cost_usd": round(total_cost, 4),
            "model_ranking": lite.get("model_ranking", []),
        }
    })


@benchmark_bp.route("/api/benchmark/models")
def benchmark_models():
    """模型排行榜"""
    lite = _load_benchmark_lite()
    if not lite:
        return jsonify({"ok": False, "error": "暂无评测数据"}), 404

    return jsonify({
        "ok": True,
        "data": {
            "models": lite.get("models", []),
            "ranking": lite.get("model_ranking", []),
        }
    })


@benchmark_bp.route("/api/benchmark/categories")
def benchmark_categories():
    """分类最佳模型"""
    lite = _load_benchmark_lite()
    data = _load_benchmark_data()
    if not lite:
        return jsonify({"ok": False, "error": "暂无评测数据"}), 404

    return jsonify({
        "ok": True,
        "data": {
            "category_leaders": lite.get("category_leaders", {}),
            "category_summaries": data.get("category_summaries", {}),
        }
    })


@benchmark_bp.route("/api/benchmark/matrix")
def benchmark_matrix():
    """完整评测矩阵 (支持分页/筛选)"""
    data = _load_benchmark_data()
    if not data:
        return jsonify({"ok": False, "error": "暂无评测数据"}), 404

    # 参数
    page = max(1, int(request.args.get("page", 1)))
    per_page = min(100, max(10, int(request.args.get("per_page", 50))))
    category = request.args.get("category", "")
    model = request.args.get("model", "")
    search = request.args.get("q", "").lower()
    sort_by = request.args.get("sort", "quality_score")
    order = request.args.get("order", "desc")

    cells = data.get("cells", [])

    # 筛选
    if category:
        cells = [c for c in cells if c.get("category") == category]
    if model:
        cells = [c for c in cells if c.get("model_key") == model]
    if search:
        cells = [c for c in cells if search in c.get("skill_slug", "").lower()
                 or search in c.get("skill_name", "").lower()
                 or search in c.get("category", "").lower()]

    # 排序
    reverse = order == "desc"
    if sort_by in ("quality_score", "success_rate", "avg_latency_ms", "avg_cost_usd"):
        cells = sorted(cells, key=lambda c: c.get(sort_by, 0), reverse=reverse)
    elif sort_by == "skill_name":
        cells = sorted(cells, key=lambda c: c.get("skill_name", ""), reverse=reverse)

    # 分页
    total = len(cells)
    total_pages = max(1, (total + per_page - 1) // per_page)
    start = (page - 1) * per_page
    page_cells = cells[start:start + per_page]

    return jsonify({
        "ok": True,
        "data": {
            "cells": page_cells,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": total_pages,
            },
            "filters": {
                "category": category,
                "model": model,
                "search": search,
            }
        }
    })


@benchmark_bp.route("/api/benchmark/skill/<slug>")
def benchmark_skill(slug):
    """单个 Skill 跨模型评测"""
    data = _load_benchmark_data()
    if not data:
        return jsonify({"ok": False, "error": "暂无评测数据"}), 404

    cells = [c for c in data.get("cells", []) if c.get("skill_slug") == slug]
    if not cells:
        return jsonify({"ok": False, "error": f"未找到 Skill: {slug}"}), 404

    # 找到最佳模型
    best = max(cells, key=lambda c: c.get("quality_score", 0))

    # 从数据集获取 Skill 详情
    dataset = _load_dataset()
    skill_info = next((s for s in dataset if s["slug"] == slug), {})

    return jsonify({
        "ok": True,
        "data": {
            "skill_slug": slug,
            "skill_name": cells[0].get("skill_name", slug),
            "skill_info": skill_info,
            "best_model": best.get("model_name"),
            "best_quality": best.get("quality_score"),
            "models": cells,
        }
    })


@benchmark_bp.route("/api/benchmark/model/<key>")
def benchmark_model(key):
    """单个模型全 Skills 评测"""
    data = _load_benchmark_data()
    if not data:
        return jsonify({"ok": False, "error": "暂无评测数据"}), 404

    cells = [c for c in data.get("cells", []) if c.get("model_key") == key]
    if not cells:
        return jsonify({"ok": False, "error": f"未找到模型: {key}"}), 404

    summary = data.get("model_summaries", {}).get(key, {})

    # 按分类分组
    from collections import defaultdict
    cat_groups = defaultdict(list)
    for c in cells:
        cat_groups[c.get("category", "other")].append(c)

    return jsonify({
        "ok": True,
        "data": {
            "model_key": key,
            "model_name": cells[0].get("model_name", key),
            "summary": summary,
            "total_skills": len(cells),
            "categories": {
                cat: {
                    "count": len(skills),
                    "avg_quality": round(sum(s.get("quality_score", 0) for s in skills) / len(skills), 1),
                    "avg_success_rate": round(sum(s.get("success_rate", 0) for s in skills) / len(skills), 1),
                }
                for cat, skills in cat_groups.items()
            },
            "skills": sorted(cells, key=lambda c: c.get("quality_score", 0), reverse=True),
        }
    })


@benchmark_bp.route("/api/benchmark/compare")
def benchmark_compare():
    """模型间对比"""
    data = _load_benchmark_data()
    if not data:
        return jsonify({"ok": False, "error": "暂无评测数据"}), 404

    models = request.args.get("models", "").split(",")
    models = [m.strip() for m in models if m.strip()]

    if len(models) < 2:
        return jsonify({"ok": False, "error": "请指定至少 2 个模型"}), 400

    summaries = data.get("model_summaries", {})
    result = {}
    for mk in models:
        if mk in summaries:
            result[mk] = summaries[mk]

    return jsonify({
        "ok": True,
        "data": {
            "models": result,
            "categories": data.get("category_summaries", {}),
        }
    })


# ──────── 基线数据服务（供 Agent 对比使用） ────────

@benchmark_bp.route("/api/benchmark/baseline/<slug>")
def get_baseline(slug):
    """获取指定 Skill 的基准线数据（供 Agent Skill 评估使用）"""
    lite = _load_benchmark_lite()
    if not lite:
        return jsonify({"ok": False, "error": "暂无基线数据"}), 404

    matrix = lite.get("matrix", {})
    skill_data = matrix.get(slug)

    if skill_data:
        # 精确匹配
        avg_quality = sum(m["q"] for m in skill_data.values()) / len(skill_data)
        avg_success = sum(m["sr"] for m in skill_data.values()) / len(skill_data)
        avg_latency = sum(m["ms"] for m in skill_data.values()) / len(skill_data)
        best_model = max(skill_data.items(), key=lambda x: x[1]["q"])

        return jsonify({
            "ok": True,
            "data": {
                "slug": slug,
                "source": "exact",
                "avg_quality": round(avg_quality, 1),
                "avg_success_rate": round(avg_success, 1),
                "avg_latency_ms": round(avg_latency, 0),
                "best_model": best_model[0],
                "best_quality": best_model[1]["q"],
                "models": skill_data,
            }
        })

    # 全局平均作为回退
    ranking = lite.get("model_ranking", [])
    if ranking:
        avg_q = sum(m.get("avg_quality_score", 0) for m in ranking) / len(ranking)
        avg_s = sum(m.get("avg_success_rate", 0) for m in ranking) / len(ranking)
        avg_l = sum(m.get("avg_latency_ms", 0) for m in ranking) / len(ranking)
        return jsonify({
            "ok": True,
            "data": {
                "slug": slug,
                "source": "global_avg",
                "avg_quality": round(avg_q, 1),
                "avg_success_rate": round(avg_s, 1),
                "avg_latency_ms": round(avg_l, 0),
                "n_models": len(ranking),
            }
        })

    return jsonify({"ok": False, "error": "暂无基线数据"}), 404
