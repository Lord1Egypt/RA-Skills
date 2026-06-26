#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
组合查询一体化脚本
支持三种场景：主体识别、查企业、查人
统一接口：fetch(entmark, name, province) -> str (Markdown)
"""

import sys
import os

if __package__:
    from .base import call_api, convert_to_chinese, dict_to_markdown
else:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from base import call_api, convert_to_chinese, dict_to_markdown


def _fetch_raw(entmark: str = "", name: str = "", province: str = "") -> dict:
    """调接口拿原始数据"""
    params = {}
    if entmark:
        params["entmark"] = entmark
    if name:
        params["name"] = name
    if province:
        params["province"] = province

    if not params:
        return {}

    resp = call_api(params)
    if resp.get("code") != 200:
        return {}
    return resp.get("data", {})


# ============ 功能一：主体识别 ============

def fetch_entity_id(entmark: str) -> str:
    """
    主体识别：输入企业标识，返回企业名称 + 统一社会信用代码

    Args:
        entmark: 企业名称/简称/信用代码/注册号等

    Returns:
        Markdown 格式的主体识别结果
    """
    raw = _fetch_raw(entmark=entmark)
    if not raw:
        return "未查询到相关企业信息"

    basic = raw.get("ENT_INFO", {}).get("BASIC", {})
    if not basic:
        return "未查询到相关企业信息"

    ent_name = basic.get("ENTNAME", "")
    credit_code = basic.get("CREDITCODE", "")

    lines = [
        "## 主体识别结果",
        "",
        f"- **企业名称**：{ent_name}",
        f"- **统一社会信用代码**：{credit_code}",
    ]
    return "\n".join(lines)


# ============ 功能二：查企业 ============

def fetch_enterprise(entmark: str) -> str:
    """
    查企业：输入企业标识，返回照面、股东、高管、对外投资

    Args:
        entmark: 企业名称/简称/信用代码/注册号等

    Returns:
        Markdown 格式的企业信息
    """
    raw = _fetch_raw(entmark=entmark)
    if not raw:
        return "未查询到相关企业信息"

    ent_info = raw.get("ENT_INFO", {})
    if not ent_info:
        return "未查询到相关企业信息"

    cn_data = convert_to_chinese(ent_info)
    return dict_to_markdown(cn_data, title="企业信息查询结果")


# ============ 功能三：查人 ============

def fetch_person_summary(name: str, province: str = "") -> str:
    """
    查人（仅人名 / 人名+省份）：返回人员统计汇总

    Args:
        name: 人员姓名
        province: 省份（可选，预留）

    Returns:
        Markdown 格式的人员统计
    """
    raw = _fetch_raw(name=name, province=province)
    if not raw:
        return "未查询到相关人员信息"

    person_info = raw.get("MANAGER_INFO", raw.get("PERSON_INFO", {}))
    if not person_info:
        return "未查询到相关人员信息"

    # MANAGER_INFO 返回的是 list，需要特殊处理
    if isinstance(person_info, list):
        cn_data = [convert_to_chinese(item) if isinstance(item, dict) else item for item in person_info]
        lines = [f"## 人员查询结果：{name}", ""]
        for item in cn_data:
            if isinstance(item, dict):
                person_name = item.get("高管名称", item.get("姓名", item.get("NAME", name)))
                ent_count = item.get("关联企业个数", item.get("ENT_COUNT", ""))
                legal_count = item.get("担任法人企业数量", item.get("LEGAL_COUNT", ""))
                manager_count = item.get("担任高管企业数量", item.get("MANAGER_COUNT", ""))
                inv_count = item.get("投资企业数量", item.get("INV_COUNT", ""))
                lines.append(f"**{person_name}**")
                lines.append(f"- 关联企业：{ent_count} 家")
                lines.append(f"- 担任法人：{legal_count} 家")
                lines.append(f"- 担任高管：{manager_count} 家")
                lines.append(f"- 投资企业：{inv_count} 家")
                # 企业分布
                ent_list = item.get("关联企业", item.get("ENTLIST", []))
                if ent_list:
                    lines.append("")
                    lines.append("| 省份 | 企业名称 | 该省企业数 |")
                    lines.append("| --- | --- | --- |")
                    for ent in ent_list:
                        if isinstance(ent, dict):
                            prov = ent.get("省份", ent.get("PROVINCENAME", ""))
                            ename = ent.get("企业名称", ent.get("ENTNAME", ""))
                            area_count = ent.get("地区企业数量", ent.get("AREAENT_COUNT", ""))
                            lines.append(f"| {prov} | {ename} | {area_count} |")
                lines.append("")
        return "\n".join(lines)
    else:
        cn_data = convert_to_chinese(person_info)
        return dict_to_markdown(cn_data, title=f"人员查询结果：{name}")


def fetch_person_detail(name: str, entmark: str) -> str:
    """
    查人（人名+企业）：返回企业信息 + 投资任职情况

    Args:
        name: 人员姓名
        entmark: 企业标识

    Returns:
        Markdown 格式的企业信息 + 人员投资任职详情
    """
    raw = _fetch_raw(entmark=entmark, name=name)
    if not raw:
        return "未查询到相关信息"

    parts = []

    # 企业信息（ENT_INFO）
    ent_info = raw.get("ENT_INFO", {})
    if ent_info:
        cn_ent = convert_to_chinese(ent_info)
        parts.append(dict_to_markdown(cn_ent, title="企业信息"))

    # 投资任职情况（PERSON_INFO）
    person_info = raw.get("PERSON_INFO", raw.get("MANAGER_INFO", {}))
    if person_info:
        if isinstance(person_info, list):
            cn_list = [convert_to_chinese(item) if isinstance(item, dict) else item for item in person_info]
            lines = [f"## {name} 在 {entmark} 的投资任职情况", ""]
            for item in cn_list:
                if isinstance(item, dict):
                    lines.append(dict_to_markdown(item, level=3))
            parts.append("\n".join(lines))
        elif isinstance(person_info, dict):
            cn_person = convert_to_chinese(person_info)
            parts.append(dict_to_markdown(cn_person, title=f"{name} 在 {entmark} 的投资任职情况"))

    if not parts:
        return "未查询到相关信息"

    return "\n\n".join(parts)


# ============ 统一入口 ============

def fetch(entmark: str = "", name: str = "", province: str = "") -> str:
    """
    统一入口，根据参数组合自动判断场景

    Args:
        entmark: 企业标识（可选）
        name: 人员姓名（可选）
        province: 省份（可选，预留）

    Returns:
        Markdown 格式的查询结果
    """
    if entmark and name:
        return fetch_person_detail(name, entmark)
    elif entmark:
        return fetch_enterprise(entmark)
    elif name:
        return fetch_person_summary(name, province)
    else:
        return "请提供企业标识(entmark)或人员姓名(name)"


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="企业/人员组合查询")
    parser.add_argument("--entmark", type=str, default="", help="企业标识")
    parser.add_argument("--name", type=str, default="", help="人员姓名")
    parser.add_argument("--province", type=str, default="", help="省份（预留）")
    args = parser.parse_args()

    print(fetch(entmark=args.entmark, name=args.name, province=args.province))
