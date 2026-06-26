#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一数据服务模块
通过 /skill/entData/support 聚合接口获取所有企业数据

认证方式：使用 access_key 请求头认证
环境变量：QIBOOK_ACCESS_KEY, QIBOOK_BASE_URL（必须设置）
"""

import os
from typing import Dict, Any, Optional

import requests

# API 基础地址 - 从环境变量获取
BASE_URL = os.environ.get('QIBOOK_BASE_URL')


class EntDataService:
    """企业数据服务类"""

    def __init__(self, access_key: str = None):
        """
        初始化数据服务

        Args:
            access_key: API 访问密钥，如不传则从环境变量 QIBOOK_ACCESS_KEY 获取

        Raises:
            ValueError: 如果未设置 QIBOOK_ACCESS_KEY 环境变量
        """
        self.access_key = access_key or os.environ.get('QIBOOK_ACCESS_KEY')
        self.base_url = BASE_URL

        if not self.access_key:
            raise ValueError(
                "缺少 ACCESS_KEY 配置。请设置环境变量 QIBOOK_ACCESS_KEY"
            )

    def _get_headers(self) -> Dict[str, str]:
        """
        生成 API 请求头

        Returns:
            包含认证信息的请求头字典
        """
        return {
            "Accept": "application/json",
            "access_key": self.access_key,
        }

    def fetch_all_data(self, entname: str, timeout: int = 60) -> Dict[str, Any]:
        """
        通过聚合接口获取企业全量数据

        Args:
            entname: 企业名称
            timeout: 请求超时时间（秒）

        Returns:
            包含所有维度数据的字典，结构如下：
            {
                "success": bool,
                "code": int,
                "message": str,
                "data": dict  # 企业全量数据
            }
        """
        url = f"{self.base_url}/skill/entData/support"
        headers = self._get_headers()
        params = {"entname": entname}

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=timeout,
                verify=True
            )

            response_json = response.json()

            # 处理不同的响应码格式（CODE 或 code）
            code = response_json.get("code") or response_json.get("CODE")

            if code == 200:
                # API返回结构为 {code, msg, data}
                # data 中包含各维度的处理后数据和 prompt 字段
                return {
                    "success": True,
                    "code": 200,
                    "message": response_json.get("msg") or response_json.get("MSG") or "查询成功",
                    "data": response_json.get("data") or response_json
                }
            else:
                return {
                    "success": False,
                    "code": code,
                    "message": response_json.get("msg") or response_json.get("MSG") or "查询失败",
                    "data": None
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "code": -1,
                "message": "请求超时",
                "data": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "code": -1,
                "message": f"请求异常: {str(e)}",
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "code": -1,
                "message": f"未知错误: {str(e)}",
                "data": None
            }


# 模块级便捷函数
_service_instance: Optional[EntDataService] = None


def get_service() -> EntDataService:
    """获取数据服务单例"""
    global _service_instance
    if _service_instance is None:
        _service_instance = EntDataService()
    return _service_instance


def fetch_all_data(entname: str, timeout: int = 60) -> Dict[str, Any]:
    """
    便捷函数：获取企业全量数据

    Args:
        entname: 企业名称
        timeout: 请求超时时间（秒）

    Returns:
        包含所有维度数据的字典
    """
    return get_service().fetch_all_data(entname, timeout)


__all__ = [
    'EntDataService',
    'get_service',
    'fetch_all_data',
]
