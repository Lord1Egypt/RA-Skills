#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
找茬大师 - 招投标重复项目核实脚本
手动分析 + Python 写入结果的工作流配套

用法：
  python3 zhuocha_finder.py              # 交互式
  python3 zhuocha_finder.py --limit 20  # 指定数量
  python3 zhuocha_finder.py --all        # 处理所有未分析的 reid
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

# ============== 配置 ==============
API_6100 = "http://192.168.88.51:6100/query"
API_5100 = "http://192.168.88.51:5100/query"
API_INSERT = "http://192.168.88.51:6100/insert"
TABLE_RE = "public.dify_ns_re_readsource"
TABLE_RESULT = "result.dify_ns_re_result"
STATE_FILE = os.path.expanduser("~/.openclaw/workspace/.zhuocha_cursor.json")


# ============== 工具函数 ==============
def rp(url, payload, timeout=30):
    for attempt in range(3):
        try:
            resp = requests.post(url, json=payload, timeout=timeout)
            return resp.json()
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
    return None


def get_done_reids():
    """获取已分析的 reid"""
    result = rp(API_6100, {"sql": f"SELECT reid FROM {TABLE_RESULT}"})
    if result and result.get("success"):
        return set(row["reid"] for row in result["data"])
    return set()


def get_reids_to_analyze(limit=20, min_count=2, max_count=None):
    """获取待分析的 reid"""
    done = get_done_reids()
    if max_count:
        sql = f"""
            SELECT reid, COUNT(*) as cnt
            FROM {TABLE_RE}
            WHERE reid NOT IN ({','.join(f"'{r}'" for r in done)})
            GROUP BY reid
            HAVING COUNT(*) >= {min_count} AND COUNT(*) <= {max_count}
            ORDER BY cnt DESC
            LIMIT {limit}
        """
    else:
        sql = f"""
            SELECT reid, COUNT(*) as cnt
            FROM {TABLE_RE}
            WHERE reid NOT IN ({','.join(f"'{r}'" for r in done)})
            GROUP BY reid
            HAVING COUNT(*) = {min_count}
            ORDER BY RANDOM()
            LIMIT {limit}
        """
    result = rp(API_6100, {"sql": sql})
    if result and result.get("success"):
        return [(row["reid"], row["cnt"]) for row in result["data"]]
    return []


def get_jy_fields(reid):
    """获取分组内所有 jy_id 的字段"""
    sql = f"""
        SELECT jy_id, customer_standard_new, title, proj_name, type
        FROM {TABLE_RE}
        WHERE reid = '{reid}'
        ORDER BY jy_id
    """
    result = rp(API_6100, {"sql": sql})
    if result and result.get("success"):
        return result["data"]
    return []


def get_detail(jy_id, limit=200):
    """获取原始正文前 N 字"""
    sql = f"SELECT LEFT(detail, {limit}) as detail, att_ext FROM public.ods_bid_content WHERE jy_id = '{jy_id}'"
    result = rp(API_5100, {"sql": sql})
    if result and result.get("success") and result["data"]:
        return result["data"][0]
    return {"detail": "", "att_ext": None}


# ============== 分析（此处只打印，结果需手动确认后写入）==============
def quick_check(fields):
    """
    快速字段预判。
    返回 (pre_judge, reason)
      pre_judge: 'dup' / 'non_dup' / 'manual'
    """
    if len(fields) < 2:
        return "skip", "记录不足2条"

    proj_names = list(set(f.get("proj_name", "") or "" for f in fields))
    customers = list(set(f.get("customer_standard_new", "") or "" for f in fields))
    titles = [f.get("title", "") or "" for f in fields]

    # proj_name 完全不同 → 非重复
    if len(proj_names) > 1:
        return "non_dup", f"proj_name 有 {len(proj_names)} 种，差异明显"

    # proj_name 完全一致 → 大概率重复
    if len(proj_names) == 1 and proj_names[0]:
        # 有标注差异的字眼
        marker_titles = [t for t in titles if any(m in t for m in ["二次", "重发", "第二次", "第X批", "第2批", "第3批", "第4批", "第5批", "合同公示", "单一来源"])]
        if marker_titles:
            return "dup", f"proj_name 一致，标题有标注差异（{marker_titles[0][:30]}），待查正文确认"
        return "dup", "proj_name 完全一致，判断为重复（待人工确认）"

    # proj_name 为空或无效 → 需要查正文
    return "manual", "proj_name 解析失败，需查正文"


def print_summary(reid, fields, detail_map):
    """打印分析摘要"""
    print(f"\n{'='*60}")
    print(f"reid: {reid}  ({len(fields)} 条)")
    print(f"{'='*60}")
    for f in fields:
        jid = f["jy_id"]
        d = detail_map.get(jid, {})
        detail_preview = (d.get("detail", "") or "")[:80].replace("\n", " ")
        att = d.get("att_ext")
        print(f"  [{jid[:15]}...]")
        print(f"    title: {(f.get('title') or '')[:50]}")
        print(f"    proj:  {(f.get('proj_name') or '')[:40]}")
        print(f"    cust:  {(f.get('customer_standard_new') or '')[:30]}")
        print(f"    type:  {f.get('type', '')}")
        print(f"    detail: {detail_preview}")


# ============== 结果写入 ==============
def write_result(reid, reason, rr, rd, re_result):
    """
    写入一条结果到 result.dify_ns_re_result
    rd: str，多个 jy_id 用英文逗号分隔
    """
    payload = {
        "sql": f"INSERT INTO {TABLE_RESULT} (reid, reason, rr, rd, re_result) VALUES (:reid, :reason, :rr, :rd, :re_result)",
        "params": {"reid": reid, "reason": reason, "rr": rr, "rd": rd, "re_result": re_result}
    }
    result = rp(API_INSERT, payload)
    if result and result.get("success"):
        return True
    return False


def batch_write(records):
    """批量写入，records: [(reid, reason, rr, rd, re_result), ...]"""
    ok = 0
    for reid, reason, rr, rd, re_result in records:
        if write_result(reid, reason, rr, rd, re_result):
            ok += 1
            print(f"  ✅ {reid}: {re_result}")
        else:
            print(f"  ❌ {reid}: 写入失败")
    return ok


# ============== 主流程 ==============
def run(limit=20, manual=False):
    print(f"\n📊 获取待分析 reid（已排除结果表中已有记录）...")
    groups = get_reids_to_analyze(limit=limit, min_count=2)
    print(f"找到 {len(groups)} 个待分析 reid")

    if not groups:
        print("✅ 全部处理完毕")
        return

    results = []
    for reid, cnt in groups:
        fields = get_jy_fields(reid)
        if len(fields) < 2:
            continue

        # 查正文（只取前2条用于预判）
        detail_map = {}
        for f in fields[:2]:
            detail_map[f["jy_id"]] = get_detail(f["jy_id"])

        print_summary(reid, fields, detail_map)
        pre, reason = quick_check(fields)
        print(f"\n  预判: {pre} | {reason}")
        print(f"\n  请确认判断结果：")
        print(f"    1. 重复（是）→ 保留第一条，删除其余")
        print(f"    2. 非重复（否）→ 全部保留")
        print(f"    3. 跳过")
        results.append({"reid": reid, "cnt": cnt, "fields": fields, "pre": pre, "reason": reason})

    print(f"\n{'='*60}")
    print(f"📊 本批汇总：共 {len(results)} 个 reid")
    print(f"   预判重复: {sum(1 for r in results if r['pre'] == 'dup')}")
    print(f"   预判非重复: {sum(1 for r in results if r['pre'] == 'non_dup')}")
    print(f"   需人工判断: {sum(1 for r in results if r['pre'] == 'manual')}")


if __name__ == "__main__":
    args = sys.argv[1:]
    limit = 20
    if "--all" in args:
        limit = 500
        args.remove("--all")
    if args and args[0].isdigit():
        limit = int(args[0])

    print(f"找茬大师 - 招投标重复项目核实")
    print(f"分析数量: {limit}")
    run(limit=limit)
