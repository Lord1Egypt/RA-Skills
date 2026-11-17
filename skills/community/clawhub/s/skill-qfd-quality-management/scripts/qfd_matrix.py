#!/usr/bin/env python3
"""
QFD质量屋矩阵构建工具
支持：模板生成、矩阵构建、权重计算、增量更新
"""

import argparse
import json
import sys
import numpy as np
from typing import Dict, List, Any


def generate_template(num_cr: int, num_tr: int) -> Dict[str, Any]:
    """生成空白质量屋模板"""
    customer_requirements = [
        {"id": f"CR{i+1}", "name": f"客户需求{i+1}", "weight": 3, "category": "功能"}
        for i in range(num_cr)
    ]
    technical_requirements = [
        {"id": f"TR{i+1}", "name": f"技术指标{i+1}", "unit": "-"}
        for i in range(num_tr)
    ]
    
    # 生成空白关系矩阵
    relationship_matrix = [[0 for _ in range(num_tr)] for _ in range(num_cr)]
    
    # 生成屋顶相关性矩阵（对称矩阵）
    correlation_matrix = [[0 for _ in range(num_tr)] for _ in range(num_tr)]
    for i in range(num_tr):
        for j in range(i+1, num_tr):
            correlation_matrix[i][j] = correlation_matrix[j][i] = "?"
    
    template = {
        "version": "1.0",
        "customer_requirements": customer_requirements,
        "technical_requirements": technical_requirements,
        "relationship_matrix": relationship_matrix,
        "correlation_matrix": correlation_matrix,
        "technical_targets": {f"TR{i+1}": "" for i in range(num_tr)}
    }
    return template


def build_matrix_from_input(input_file: str) -> Dict[str, Any]:
    """从输入文件构建质量屋"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cr_list = data.get("customer_requirements", [])
    tr_list = data.get("technical_requirements", [])
    
    num_cr = len(cr_list)
    num_tr = len(tr_list)
    
    if num_cr == 0 or num_tr == 0:
        print("警告：需求或技术指标为空", file=sys.stderr)
        return {"error": "需求和技术指标不能为空"}
    
    # 生成初始关系矩阵（用户需手动填写）
    relationship_matrix = [[0 for _ in range(num_tr)] for _ in range(num_cr)]
    
    # 生成屋顶相关性矩阵
    correlation_matrix = [[0 for _ in range(num_tr)] for _ in range(num_tr)]
    for i in range(num_tr):
        for j in range(i+1, num_tr):
            correlation_matrix[i][j] = correlation_matrix[j][i] = "?"
    
    hoq = {
        "version": "1.0",
        "customer_requirements": cr_list,
        "technical_requirements": tr_list,
        "relationship_matrix": relationship_matrix,
        "correlation_matrix": correlation_matrix,
        "technical_targets": {tr["id"]: "" for tr in tr_list}
    }
    
    return hoq


def calculate_weights(matrix_file: str) -> Dict[str, Any]:
    """计算技术指标权重"""
    with open(matrix_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if "error" in data:
        return data
    
    cr_list = data["customer_requirements"]
    tr_list = data["technical_requirements"]
    rel_matrix = data["relationship_matrix"]
    
    num_cr = len(cr_list)
    num_tr = len(tr_list)
    
    # 提取权重
    weights = np.array([cr["weight"] for cr in cr_list], dtype=float)
    
    # 转换为numpy矩阵计算
    rel_array = np.array(rel_matrix, dtype=float)
    
    # 计算绝对权重：关系强度 × 需求权重
    abs_weights = rel_array * weights.reshape(-1, 1)
    
    # 计算技术指标绝对权重
    abs_tr_weights = abs_weights.sum(axis=0)
    
    # 计算技术指标相对权重
    total = abs_tr_weights.sum()
    if total > 0:
        rel_tr_weights = abs_tr_weights / total
    else:
        rel_tr_weights = np.zeros(num_tr)
    
    # 计算归一化权重（百分比）
    norm_tr_weights = abs_tr_weights / abs_tr_weights.max() * 100 if abs_tr_weights.max() > 0 else np.zeros(num_tr)
    
    # 构建结果
    results = {
        "technical_weights": [],
        "priority_ranking": [],
        "matrix_stats": {
            "total_relationships": int((rel_array > 0).sum()),
            "strong_relationships": int((rel_array >= 9).sum()),
            "medium_relationships": int((rel_array == 3).sum()),
            "weak_relationships": int((rel_array == 1).sum())
        }
    }
    
    tr_weights = []
    for i, tr in enumerate(tr_list):
        tr_info = {
            "id": tr["id"],
            "name": tr["name"],
            "unit": tr.get("unit", "-"),
            "absolute_weight": round(float(abs_tr_weights[i]), 4),
            "relative_weight": round(float(rel_tr_weights[i]), 4),
            "normalized_weight": round(float(norm_tr_weights[i]), 2),
            "raw_contribution": [float(rel_array[j, i]) for j in range(num_cr)]
        }
        tr_weights.append(tr_info)
    
    # 按绝对权重排序
    tr_weights.sort(key=lambda x: x["absolute_weight"], reverse=True)
    
    for rank, tr in enumerate(tr_weights, 1):
        results["priority_ranking"].append({
            "rank": rank,
            "id": tr["id"],
            "name": tr["name"],
            "weight": tr["absolute_weight"],
            "priority_level": "高" if tr["normalized_weight"] >= 70 else ("中" if tr["normalized_weight"] >= 30 else "低")
        })
        tr["rank"] = rank
    
    results["technical_weights"] = tr_weights
    
    return results


def update_matrix(base_file: str, changes_file: str) -> Dict[str, Any]:
    """增量更新质量屋"""
    with open(base_file, 'r', encoding='utf-8') as f:
        base = json.load(f)
    
    with open(changes_file, 'r', encoding='utf-8') as f:
        changes = json.load(f)
    
    # 更新需求权重
    if "updated_weights" in changes:
        cr_map = {cr["id"]: cr for cr in base["customer_requirements"]}
        for update in changes["updated_weights"]:
            if update["id"] in cr_map:
                cr_map[update["id"]]["weight"] = update["weight"]
    
    # 更新关系矩阵
    if "updated_relationships" in changes:
        rel_matrix = base["relationship_matrix"]
        for rel in changes["updated_relationships"]:
            cr_idx = int(rel["cr_idx"])
            tr_idx = int(rel["tr_idx"])
            if 0 <= cr_idx < len(rel_matrix) and 0 <= tr_idx < len(rel_matrix[0]):
                rel_matrix[cr_idx][tr_idx] = rel["strength"]
    
    # 更新技术目标
    if "updated_targets" in changes:
        base["technical_targets"].update(changes["updated_targets"])
    
    return base


def matrix_to_markdown(hoq: Dict[str, Any], weights: Dict[str, Any] = None) -> str:
    """将质量屋转换为Markdown格式便于查看"""
    cr_list = hoq["customer_requirements"]
    tr_list = hoq["technical_requirements"]
    rel_matrix = hoq["relationship_matrix"]
    corr_matrix = hoq.get("correlation_matrix", [])
    
    md = ["# 质量屋 (House of Quality)\n"]
    
    # 客户需求
    md.append("## 客户需求\n")
    md.append("| ID | 名称 | 权重 | 类别 |")
    md.append("|---|---|---|---|")
    for cr in cr_list:
        md.append(f"| {cr['id']} | {cr['name']} | {cr['weight']} | {cr.get('category', '-')} |")
    
    # 技术指标
    md.append("\n## 技术指标\n")
    md.append("| ID | 名称 | 单位 |")
    md.append("|---|---|---|")
    for tr in tr_list:
        md.append(f"| {tr['id']} | {tr['name']} | {tr.get('unit', '-')} |")
    
    # 关系矩阵
    md.append("\n## 关系矩阵\n")
    header = "| 客户需求 | " + " | ".join([tr["id"] for tr in tr_list]) + " |"
    md.append(header)
    md.append("|" + "|".join(["---"] * (len(tr_list) + 1)) + "|")
    
    for i, cr in enumerate(cr_list):
        row = f"| **{cr['id']} {cr['name']}** |"
        for j in range(len(tr_list)):
            val = rel_matrix[i][j] if i < len(rel_matrix) and j < len(rel_matrix[i]) else 0
            if val == 0:
                row += " | "
            elif val >= 9:
                row += " | **●** |"
            elif val >= 3:
                row += " | ○ |"
            else:
                row += " | · |"
        md.append(row)
    
    # 权重排名
    if weights and "priority_ranking" in weights:
        md.append("\n## 技术指标优先级\n")
        md.append("| 排名 | ID | 技术指标 | 绝对权重 | 优先级 |")
        md.append("|---|---|---|---|---|")
        for item in weights["priority_ranking"]:
            md.append(f"| {item['rank']} | {item['id']} | {item['name']} | {item['weight']:.2f} | {item['priority_level']} |")
    
    # 屋顶相关性
    if corr_matrix and len(corr_matrix) > 0:
        md.append("\n## 屋顶相关性矩阵\n")
        header = "| TR | " + " | ".join([tr["id"] for tr in tr_list]) + " |"
        md.append(header)
        md.append("|" + "|".join(["---"] * (len(tr_list) + 1)) + "|")
        for i, tr in enumerate(tr_list):
            row = f"| **{tr['id']}** |"
            for j in range(len(tr_list)):
                val = corr_matrix[i][j] if i < len(corr_matrix) and j < len(corr_matrix[i]) else 0
                if val == "?" or val == 0:
                    row += " | - |"
                elif val > 0:
                    row += f" | +{val} |"
                else:
                    row += f" | {val} |"
            md.append(row)
    
    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="QFD质量屋矩阵构建工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # template子命令
    parser_template = subparsers.add_parser("template", help="生成空白质量屋模板")
    parser_template.add_argument("--cr", type=int, required=True, help="客户需求数量")
    parser_template.add_argument("--tr", type=int, required=True, help="技术指标数量")
    parser_template.add_argument("--output", type=str, required=True, help="输出文件路径")
    
    # build子命令
    parser_build = subparsers.add_parser("build", help="从VOC数据构建质量屋")
    parser_build.add_argument("--input", type=str, required=True, help="VOC输入文件路径")
    parser_build.add_argument("--output", type=str, required=True, help="输出文件路径")
    
    # weight子命令
    parser_weight = subparsers.add_parser("weight", help="计算技术指标权重")
    parser_weight.add_argument("--matrix", type=str, required=True, help="质量屋矩阵文件路径")
    parser_weight.add_argument("--output", type=str, help="输出文件路径（可选，默认stdout）")
    parser_weight.add_argument("--format", choices=["json", "markdown"], default="json", help="输出格式")
    
    # update子命令
    parser_update = subparsers.add_parser("update", help="增量更新质量屋")
    parser_update.add_argument("--base", type=str, required=True, help="基础质量屋文件路径")
    parser_update.add_argument("--changes", type=str, required=True, help="变更文件路径")
    parser_update.add_argument("--output", type=str, required=True, help="输出文件路径")
    
    args = parser.parse_args()
    
    if args.command == "template":
        template = generate_template(args.cr, args.tr)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        print(f"模板已生成: {args.output}")
        print(f"客户需求: {args.cr}, 技术指标: {args.tr}")
    
    elif args.command == "build":
        hoq = build_matrix_from_input(args.input)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(hoq, f, ensure_ascii=False, indent=2)
        print(f"质量屋已构建: {args.output}")
    
    elif args.command == "weight":
        results = calculate_weights(args.matrix)
        if args.format == "markdown":
            with open(args.matrix, 'r', encoding='utf-8') as f:
                hoq = json.load(f)
            output = matrix_to_markdown(hoq, results)
        else:
            output = json.dumps(results, ensure_ascii=False, indent=2)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"权重计算结果已保存: {args.output}")
        else:
            print(output)
    
    elif args.command == "update":
        updated = update_matrix(args.base, args.changes)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(updated, f, ensure_ascii=False, indent=2)
        print(f"质量屋已更新: {args.output}")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
