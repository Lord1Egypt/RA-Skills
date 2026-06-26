#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Skill - 西部数码域名解析管理
Skill ID: west-dns-manager
Version: 1.0.0
Author: OpenClaw
Description: 基于西部数码API实现域名解析的添加、修改、删除操作
"""

import requests
import time
import hashlib
from typing import Dict, Tuple, Optional

# ======================== OpenClaw Skill 元信息 ========================
SKILL_META = {
    "skill_id": "west-dns-manager",
    "name": "西部数码域名解析管理",
    "version": "1.0.0",
    "description": "提供西部数码域名解析的添加、修改、删除功能",
    "author": "OpenClaw",
    "tags": ["域名解析", "西部数码", "DNS"],
    "input_schema": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["add", "modify", "delete"], "description": "操作类型"},
            "config": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "西部数码用户名"},
                    "api_password": {"type": "string", "description": "西部数码API密码"}
                },
                "required": ["username", "api_password"]
            },
            "dns_params": {
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "主域名，如test.com"},
                    "host": {"type": "string", "description": "主机头，如www、@、blog"},
                    "type": {"type": "string", "enum": ["A", "CNAME", "MX", "TXT", "AAAA"], "description": "解析类型"},
                    "value": {"type": "string", "description": "解析值（添加/修改时必填）"},
                    "old_value": {"type": "string", "description": "旧解析值（修改时必填）"},
                    "record_id": {"type": "string", "description": "解析记录ID（修改/删除优先使用）"},
                    "ttl": {"type": "integer", "default": 900, "description": "缓存时间"},
                    "level": {"type": "integer", "default": 10, "description": "优先级"},
                    "line": {"type": "string", "default": "", "description": "解析线路"}
                },
                "required": ["domain", "host", "type"]
            }
        },
        "required": ["action", "config", "dns_params"]
    },
    "output_schema": {
        "type": "object",
        "properties": {
            "success": {"type": "boolean", "description": "操作是否成功"},
            "message": {"type": "string", "description": "操作结果信息"},
            "data": {"type": "object", "description": "返回数据（如record_id）"},
            "error": {"type": "string", "description": "错误信息（失败时返回）"}
        }
    }
}

# ======================== 核心功能类 ========================
class WestDnsManager:
    """西部数码域名解析管理核心类"""
    
    def __init__(self, username: str, api_password: str):
        self.username = username
        self.api_password = api_password
        self.base_url = "https://api.west.cn/api/v2/domain/"
    
    def _generate_token(self) -> str:
        """生成身份验证Token（10分钟有效期）"""
        timestamp = str(int(time.time() * 1000))
        raw_str = f"{self.username}{self.api_password}{timestamp}"
        return hashlib.md5(raw_str.encode('utf-8')).hexdigest()
    
    def _send_request(self, params: Dict) -> Tuple[bool, Dict]:
        """发送API请求通用方法"""
        try:
            # 添加身份验证Token
            params["token"] = self._generate_token()
            
            # 发送POST请求
            response = requests.post(
                url=self.base_url,
                data=params,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30
            )
            response.raise_for_status()  # 抛出HTTP错误
            
            result = response.json()
            if result.get("result") == 200:
                return True, {
                    "success": True,
                    "message": "操作成功",
                    "data": result.get("data", {})
                }
            else:
                return False, {
                    "success": False,
                    "message": "操作失败",
                    "error": f"API返回错误: {result}"
                }
        
        except requests.exceptions.RequestException as e:
            return False, {
                "success": False,
                "message": "请求异常",
                "error": f"网络请求错误: {str(e)}"
            }
        except Exception as e:
            return False, {
                "success": False,
                "message": "系统异常",
                "error": f"未知错误: {str(e)}"
            }
    
    def add_dns(self, dns_params: Dict) -> Dict:
        """添加域名解析记录"""
        params = {
            "act": "adddnsrecord",
            "domain": dns_params["domain"],
            "host": dns_params["host"],
            "type": dns_params["type"],
            "value": dns_params["value"],
            "ttl": dns_params.get("ttl", 900),
            "level": dns_params.get("level", 10),
            "line": dns_params.get("line", "")
        }
        _, result = self._send_request(params)
        return result
    
    def modify_dns(self, dns_params: Dict) -> Dict:
        """修改域名解析记录"""
        params = {
            "act": "moddnsrecord",
            "domain": dns_params["domain"],
            "host": dns_params["host"],
            "type": dns_params["type"],
            "oldvalue": dns_params["old_value"],
            "value": dns_params["value"],
            "ttl": dns_params.get("ttl", 900),
            "level": dns_params.get("level", 10),
            "line": dns_params.get("line", "")
        }
        # 优先使用record_id定位
        if dns_params.get("record_id"):
            params["id"] = dns_params["record_id"]
        
        _, result = self._send_request(params)
        return result
    
    def delete_dns(self, dns_params: Dict) -> Dict:
        """删除域名解析记录"""
        params = {
            "act": "deldnsrecord",
            "domain": dns_params["domain"]
        }
        
        # 优先使用record_id删除
        if dns_params.get("record_id"):
            params["id"] = dns_params["record_id"]
        else:
            params["host"] = dns_params["host"]
            params["type"] = dns_params["type"]
            params["line"] = dns_params.get("line", "")
        
        _, result = self._send_request(params)
        return result

# ======================== OpenClaw Skill 入口函数 ========================
def handler(event: Dict, context: Optional[Dict] = None) -> Dict:
    """
    OpenClaw Skill 统一入口函数
    :param event: 输入参数（包含action、config、dns_params）
    :param context: 上下文参数（OpenClaw平台传入）
    :return: 标准化输出结果
    """
    # 1. 参数校验
    required_fields = ["action", "config", "dns_params"]
    for field in required_fields:
        if field not in event:
            return {
                "success": False,
                "message": "参数缺失",
                "error": f"必须包含参数: {field}"
            }
    
    # 2. 初始化管理器
    config = event["config"]
    try:
        dns_manager = WestDnsManager(
            username=config["username"],
            api_password=config["api_password"]
        )
    except KeyError as e:
        return {
            "success": False,
            "message": "配置参数缺失",
            "error": f"config中缺少参数: {str(e)}"
        }
    
    # 3. 执行对应操作
    action = event["action"]
    dns_params = event["dns_params"]
    
    try:
        if action == "add":
            # 检查添加操作必填参数
            if "value" not in dns_params:
                raise ValueError("添加解析时必须提供value参数")
            result = dns_manager.add_dns(dns_params)
        
        elif action == "modify":
            # 检查修改操作必填参数
            if "old_value" not in dns_params or "value" not in dns_params:
                raise ValueError("修改解析时必须提供old_value和value参数")
            result = dns_manager.modify_dns(dns_params)
        
        elif action == "delete":
            result = dns_manager.delete_dns(dns_params)
        
        else:
            result = {
                "success": False,
                "message": "不支持的操作类型",
                "error": f"action必须是add/modify/delete，当前值: {action}"
            }
    
    except ValueError as e:
        result = {
            "success": False,
            "message": "参数错误",
            "error": str(e)
        }
    except Exception as e:
        result = {
            "success": False,
            "message": "执行失败",
            "error": f"系统异常: {str(e)}"
        }
    
    return result

# ======================== 本地测试入口 ========================
if __name__ == "__main__":
    # 测试用例 - 添加解析
    test_event = {
        "action": "add",
        "config": {
            "username": "你的西部数码用户名",
            "api_password": "你的西部数码API密码"
        },
        "dns_params": {
            "domain": "test.com",
            "host": "www",
            "type": "A",
            "value": "1.2.3.4",
            "ttl": 900,
            "level": 10
        }
    }
    
    # 执行测试
    result = handler(test_event)
    print("操作结果:", result)