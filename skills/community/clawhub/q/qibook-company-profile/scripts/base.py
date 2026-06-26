#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共享模块：API 认证、调用、字段映射、空值过滤
"""

import requests
import os
from typing import Any

# API 配置 - 从环境变量获取
ACCESS_KEY = os.environ.get('QIBOOK_ACCESS_KEY')
BASE_URL = os.environ.get('QIBOOK_BASE_URL')


# ============ API 调用 ============

ALLOWED_PARAMS = {'entmark', 'name', 'province'}

def call_api(params: dict) -> dict:
    """
    调用组合查询接口

    Args:
        params: 请求参数，仅支持 entmark、name、province 三个字段

    Returns:
        API 返回的 JSON dict
    """
    # 只保留接口支持的三个入参
    if not ACCESS_KEY or not BASE_URL:
        return {'code': -1, 'msg': '缺少 API 配置，请设置环境变量 QIBOOK_ACCESS_KEY 和 QIBOOK_BASE_URL'}
    filtered = {k: v for k, v in params.items() if k in ALLOWED_PARAMS and v}
    if not filtered:
        return {'code': -1, 'msg': '缺少有效参数（支持 entmark/name/province）'}
    url = f"{BASE_URL}/skill/entData/combinedQuery"
    headers = {'access_key': ACCESS_KEY}
    try:
        response = requests.get(url, headers=headers, params=filtered, verify=True, timeout=30)
        return response.json()
    except requests.exceptions.Timeout:
        return {'code': -1, 'msg': '请求超时'}
    except requests.exceptions.RequestException as e:
        return {'code': -1, 'msg': f'请求异常: {e}'}
    except ValueError:
        return {'code': -1, 'msg': f'响应解析失败（HTTP {response.status_code}）'}


# ============ 字段映射 ============

MODULE_NAME_MAP = {
    "ENT_INFO":          "企业信息",
    "PERSON_INFO":       "人员信息",
    "MANAGER_INFO":      "人员统计信息",
    "BASIC":             "企业基本信息",
    "SHAREHOLDER":       "股东及出资信息",
    "PERSON":            "主要管理人员",
    "ENTINV":            "企业对外投资信息",
    "LISTEDSHAREHOLDER": "十大股东名单",
    "RYPOSFR":           "担任法人信息",
    "RYPOSPER":          "担任高管信息",
    "RYPOSSHA":          "投资企业信息",
    "MANAGERLIST":       "高管列表",
    "ENTLIST":           "关联企业",
}

FIELD_NAME_MAP = {
    "ENTNAME":        "企业名称",
    "SHORTNAME":      "企业简称",
    "ORGCODES":       "组织机构代码",
    "CREDITCODE":     "统一社会信用代码",
    "REGNO":          "注册号",
    "FRNAME":         "法定代表人",
    "REGCAP":         "注册资本(万元)",
    "REGCAPCUR":      "注册资本币种",
    "ESDATE":         "成立日期",
    "OPFROM":         "经营期限自",
    "OPTO":           "经营期限至",
    "ENTSTATUS":      "经营状态",
    "REGORG":         "登记机关",
    "ANCHEYEAR":      "最后年检年度",
    "DOM":            "住所",
    "OPSCOPE":        "经营范围",
    "REGORGPROVINCE": "所在省份",
    "REGORGCITY":     "所在城市",
    "REGORGDISTRICT": "所在区县",
    "COMPINTRO":      "公司简介",
    "COMPURL":        "公司网址",
    "SHANAME":        "股东名称",
    "SUBCONAM":       "认缴出资额(万元)",
    "CONDATE":        "出资日期",
    "FUNDEDRATIO":    "出资比例",
    "PERNAME":        "高管姓名",
    "POSITION":       "职务",
    "ENTJGNAME":      "企业(机构)名称",
    "SHHOLDERNAME":   "股东名称",
    "HOLDERRTO":      "持股比例",
    "HOLDERAMT":      "持股数量",
    "RYNAME":         "查询人姓名",
    "NAME":           "高管名称",
    "ENT_COUNT":      "关联企业个数",
    "LEGAL_COUNT":    "担任法人企业数量",
    "MANAGER_COUNT":  "担任高管企业数量",
    "INV_COUNT":      "投资企业数量",
    "PROVINCENAME":   "省份",
    "AREAENT_COUNT":  "地区企业数量",
}

# 同一字段在不同模块下含义不同
MODULE_FIELD_MAP = {
    "ENTINV": {
        "REGCAP":      "注册资本(万元)",
        "REGCAPCUR":   "注册资本币种",
        "ENTSTATUS":   "企业状态",
        "REGORG":      "登记机关",
        "FUNDEDRATIO": "投资比例",
        "CONDATE":     "投资日期",
    },
    "SHAREHOLDER": {
        "REGCAPCUR": "认缴出资币种",
    },
}


def translate_field(field: str, module: str = None) -> str:
    """字段名英文转中文，优先模块级覆盖"""
    if module and module in MODULE_FIELD_MAP:
        cn = MODULE_FIELD_MAP[module].get(field)
        if cn:
            return cn
    return FIELD_NAME_MAP.get(field, field)


def convert_to_chinese(data: Any, parent_module: str = None) -> Any:
    """递归将英文 key 转为中文，同时过滤空值"""
    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            # 跳过空值
            if v is None or v == '' or v == [] or v == {}:
                continue
            if k in MODULE_NAME_MAP:
                cn_key = MODULE_NAME_MAP[k]
                result[cn_key] = convert_to_chinese(v, parent_module=k)
            else:
                cn_key = translate_field(k, parent_module)
                result[cn_key] = convert_to_chinese(v, parent_module)
        return result
    elif isinstance(data, list):
        items = [convert_to_chinese(item, parent_module) for item in data]
        return [item for item in items if item]  # 过滤空 dict/list
    else:
        return data


# ============ Markdown 格式化 ============

def dict_to_markdown(data: dict, title: str = "", level: int = 2) -> str:
    """将 dict 转为 Markdown，对象用 key: value，数组用表格"""
    lines = []
    if title:
        lines.append(f"{'#' * level} {title}")
        lines.append("")

    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(dict_to_markdown(value, title=key, level=level + 1))
        elif isinstance(value, list) and value:
            lines.append(f"{'#' * (level + 1)} {key}")
            lines.append("")
            if isinstance(value[0], dict):
                # 表格
                headers = list(value[0].keys())
                lines.append("| " + " | ".join(headers) + " |")
                lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                for item in value:
                    row = [str(item.get(h, "")) for h in headers]
                    lines.append("| " + " | ".join(row) + " |")
            else:
                for item in value:
                    lines.append(f"- {item}")
            lines.append("")
        else:
            lines.append(f"- **{key}**：{value}")

    return "\n".join(lines)
