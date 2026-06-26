#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一体化脚本共享模块
提供 API 调用和数据处理的共享工具函数

认证方式：access_key 聚合接口认证
环境变量：QIBOOK_ACCESS_KEY, QIBOOK_BASE_URL（必须设置）
"""

import os
import requests
from typing import Any, List


# API 配置
BASE_URL = os.environ.get('QIBOOK_BASE_URL')
ACCESS_KEY = os.environ.get('QIBOOK_ACCESS_KEY')

# 调试开关
DEBUG = False


def debug_print(*args, **kwargs):
    """调试打印函数"""
    if DEBUG:
        print(*args, **kwargs)


# ============ API 调用函数 ============

def fetch_enterprise_data(entname: str, timeout: int = 120) -> dict:
    """
    通过聚合接口获取企业全部数据

    Args:
        entname: 企业名称
        timeout: 超时时间（秒），默认120秒

    Returns:
        包含全部维度数据的字典，结构如下：
        {
            'code': 200,
            'msg': 'ok',
            'data': {
                'get_enterprise_basic_info': '...',
                'get_group_info': '...',
                'get_actual_controller': '...',
                ... (共20个维度)
                'prompt': '一般企业'  # 推荐使用的模板类型
            }
        }

    Raises:
        ValueError: 如果未设置 QIBOOK_ACCESS_KEY 环境变量
    """
    if not ACCESS_KEY:
        raise ValueError("缺少 ACCESS_KEY 配置。请设置环境变量 QIBOOK_ACCESS_KEY")

    url = f"{BASE_URL}/skill/entData/support"
    headers = {
        'access_key': ACCESS_KEY,
        'Accept': 'application/json'
    }
    params = {'entname': entname}

    try:
        debug_print(f"调用聚合接口: {url}, 企业: {entname}")
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        result = response.json()

        if result.get('code') == 200:
            debug_print(f"聚合接口调用成功，获取到 {len(result.get('data', {}))} 个维度数据")
        else:
            debug_print(f"聚合接口返回错误: {result.get('msg')}")

        return result
    except requests.exceptions.Timeout:
        debug_print(f"聚合接口请求超时: {entname}")
        return {'code': -1, 'msg': '请求超时', 'data': {}}
    except requests.exceptions.RequestException as e:
        debug_print(f"聚合接口请求异常: {str(e)}")
        return {'code': -1, 'msg': f'请求异常: {str(e)}', 'data': {}}
    except Exception as e:
        debug_print(f"聚合接口调用失败: {str(e)}")
        return {'code': -1, 'msg': f'调用失败: {str(e)}', 'data': {}}


def get_template_type(data: dict) -> str:
    """
    从聚合接口返回数据中获取推荐的模板类型

    Args:
        data: 聚合接口返回的数据

    Returns:
        模板类型字符串，如 '一般企业'、'分支机构'、'个体工商户' 等
    """
    return data.get('data', {}).get('prompt', '一般企业')


# 数据字段与模板的映射关系
TEMPLATE_MAPPING = {
    '一般企业': 'templates/company.md',
    '分支机构': 'templates/branch.md',
    '个体工商户': 'templates/personal.md',
    '政府机构': 'templates/organization/government.md',
    '医院': 'templates/organization/hospital.md',
    '律师事务所': 'templates/organization/law_firm.md',
    '学校': 'templates/organization/school.md',
    '社会组织': 'templates/organization/social.md',
    '其他组织': 'templates/organization/other.md',
}


def get_template_path(template_type: str) -> str:
    """
    根据模板类型获取模板文件路径

    Args:
        template_type: 模板类型

    Returns:
        模板文件相对路径
    """
    return TEMPLATE_MAPPING.get(template_type, 'templates/company.md')


# ============ 数据处理相关函数 ============

def format_number(value: str) -> str:
    """
    格式化数字，去除无意义的小数位

    Args:
        value: 数字字符串，可能包含 % 符号

    Returns:
        格式化后的数字字符串

    Example:
        >>> format_number("100.00")
        '100'
        >>> format_number("3.50%")
        '3.5%'
    """
    if not value:
        return value

    try:
        clean_value = value.strip().rstrip('%')
        num = float(clean_value)

        if num == int(num):
            result = str(int(num))
        else:
            result = str(num).rstrip('0').rstrip('.')

        if value.strip().endswith('%'):
            return result + '%'
        return result
    except (ValueError, TypeError):
        return value


def safe_get(data: dict, path: str, default: Any = '') -> Any:
    """
    安全获取嵌套字典中的值

    Args:
        data: 目标字典
        path: 用点分隔的路径，如 "level1.level2.key"
        default: 默认值

    Returns:
        获取到的值或默认值
    """
    if not data or not isinstance(data, dict):
        return default

    keys = path.split('.')
    current = data

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current if current is not None else default


def filter_empty_values(data: dict) -> dict:
    """
    过滤字典中的空值

    Args:
        data: 目标字典

    Returns:
        过滤后的字典
    """
    if not isinstance(data, dict):
        return data

    return {
        k: v for k, v in data.items()
        if v is not None and v != '' and v != [] and v != {}
    }


def to_markdown_section(title: str, content: str) -> str:
    """
    将内容格式化为 Markdown 章节

    Args:
        title: 章节标题
        content: 章节内容

    Returns:
        格式化的 Markdown 字符串
    """
    if not content or content.strip() == '':
        return f"### {title}\n暂无数据"
    return f"### {title}\n{content}"


def truncate_text(text: str, max_length: int = 200, suffix: str = '...') -> str:
    """
    截断过长的文本

    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 截断后的后缀

    Returns:
        截断后的文本
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length] + suffix


def format_list_to_string(items: List[str], separator: str = '、', max_items: int = 10) -> str:
    """
    将列表格式化为字符串

    Args:
        items: 字符串列表
        separator: 分隔符
        max_items: 最多显示的项目数

    Returns:
        格式化后的字符串
    """
    if not items:
        return ''

    filtered = [str(item) for item in items if item]

    if len(filtered) > max_items:
        filtered = filtered[:max_items]

    return separator.join(filtered)


def extract_money_amount(value: str, unit: str = '万元') -> str:
    """
    提取并格式化金额

    Args:
        value: 金额字符串
        unit: 金额单位

    Returns:
        格式化后的金额字符串
    """
    formatted = format_number(value)
    if formatted and formatted != '0':
        return f"{formatted}{unit}"
    return ''


__all__ = [
    # API 配置
    'ACCESS_KEY', 'BASE_URL',
    # API 调用
    'fetch_enterprise_data', 'get_template_type', 'get_template_path',
    'TEMPLATE_MAPPING',
    # 数据处理
    'format_number', 'safe_get', 'filter_empty_values',
    'to_markdown_section', 'truncate_text',
    'format_list_to_string', 'extract_money_amount',
    # 调试
    'debug_print', 'DEBUG',
]
