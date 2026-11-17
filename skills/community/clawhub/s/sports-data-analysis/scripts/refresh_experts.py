#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每期专家刷新注入器（agent 出报时调用，绝不包含任何写死的专家内容）。

设计原则（防止"专家不更新"的 bug）：
  - 本脚本【不】内置任何硬编码专家观点。所有专家观点必须来自 agent 当期的 WebSearch 结果。
  - agent 把每期 WebSearch 核实到的专家观点写入 fresh_experts.json（按 match 名索引），
    本脚本仅做"合并注入 + 打时间戳"，并从 live 场清理任何残留的旧专家，杜绝陈旧内容冒充本期。
  - 若某 live 场在 fresh_experts.json 中找不到新鲜观点，则标记 experts_pending=True（报告如实显示
    "本期未获取到公开专家观点"），【绝不】回退到写死内容。
  - 对 live=false 的示例兜底场，保留原精选静态库（experts_static=True），并在报告中明确标注非本期。

合规：仅注入公开战术分析、赛前情报、伤停；agent 在写 fresh_experts.json 时须剔除任何
与赛果判定、方向性结论相关的内容。
"""
import json
import os
import sys
import datetime

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LIVE = os.path.join(SKILL_DIR, "..", "assets", "live_today.json")
FRESH = os.path.join(SKILL_DIR, "..", "assets", "fresh_experts.json")


def main():
    fresh_path = sys.argv[1] if len(sys.argv) > 1 else FRESH
    d = json.load(open(LIVE, encoding="utf-8"))

    fresh = {}
    if os.path.exists(fresh_path):
        try:
            fresh = json.load(open(fresh_path, encoding="utf-8"))
        except Exception as e:
            print("  ⚠️ 读取新鲜专家文件失败：%s（将把所有 live 场标 pending）" % e)
    else:
        print("  ⚠️ 未找到新鲜专家文件 %s（将把所有 live 场标 pending，需先 WebSearch 产出）" % fresh_path)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    n_ok, n_pending, n_static = 0, 0, 0
    pending_names = []
    for m in d.get("matches", []):
        name = m.get("match")
        if m.get("live"):
            # 清理任何残留旧专家，防止陈旧内容混入本期
            m.pop("experts", None)
            m.pop("experts_refreshed_at", None)
            m.pop("experts_static", None)
            m.pop("experts_pending", None)
            if name in fresh and fresh[name]:
                m["experts"] = fresh[name]
                m["experts_refreshed_at"] = now
                n_ok += 1
            else:
                m["experts_pending"] = True
                n_pending += 1
                pending_names.append(name)
        else:
            # 示例兜底场：保留原精选静态库（不清 experts），仅打标
            m["experts_static"] = True
            n_static += 1

    json.dump(d, open(LIVE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("✅ 专家注入完成（本期联网核实）：实时场已更新 %d 场 / 待补(本期无公开观点) %d 场 / 示例静态库 %d 场"
          % (n_ok, n_pending, n_static))
    if pending_names:
        print("   ⚠️ 以下实时场本期未提供新鲜专家观点（将被标 pending，不冒充更新）：")
        for nm in pending_names:
            print("      · %s" % nm)
    if n_pending:
        print("   → 若要求专家每期必更新，请先对以上对阵 WebSearch 产出 fresh_experts.json 后再注入。")


if __name__ == "__main__":
    main()
