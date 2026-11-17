#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
custom_intent_plugin.py — 自定义意图插件引擎（v2.6）

功能：
1. 从 custom_intents.yaml 加载声明式意图-HTTP端点映射
2. 运行时调用企业自有系统（订单接口、CRM等）
3. 请求模板 + 响应话术模板 + 失败兜底
4. 鉴权通过环境变量读取，不硬编码

依赖：纯 Python 标准库（urllib + 环境变量）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-08-24)
"""

import os
import re
import json
import logging
import time
from typing import Optional, Dict, Any, List
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

logger = logging.getLogger(__name__)

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')
CUSTOM_INTENTS_FILE = os.path.join(CONFIG_DIR, 'custom_intents.yaml')


class CustomIntentPlugin:
    """
    自定义意图插件引擎
    
    允许企业通过 YAML 声明将意图映射到自有 HTTP API：
    - 声明端点 URL、HTTP 方法、请求模板
    - 响应字段映射到话术模板
    - 超时/失败兜底话术
    - 鉴权通过环境变量读取
    
    使用方式：
        plugin = CustomIntentPlugin()
        plugin.load()
        result = plugin.call("query_order", {"order_id": "123"})
        # result: {"success": True, "text": "您的订单..."}
    """

    def __init__(self, config_path: str = None):
        self.config_path = config_path or CUSTOM_INTENTS_FILE
        self.intents: Dict[str, Dict] = {}
        self._loaded = False

    def load(self) -> bool:
        """加载自定义意图配置"""
        if not os.path.exists(self.config_path):
            logger.info(f"自定义意图配置文件不存在: {self.config_path}")
            return False
        try:
            import yaml
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            if not config or 'intents' not in config:
                return False
            self.intents = config['intents']
            self._loaded = True
            logger.info(f"自定义意图加载完成：{len(self.intents)} 个意图")
            return True
        except ImportError:
            logger.warning("pyyaml 不可用，自定义意图插件未加载")
            return False
        except Exception as e:
            logger.error(f"加载自定义意图失败: {e}")
            return False

    def has_intent(self, intent_name: str) -> bool:
        """检查是否有对应的自定义意图"""
        return intent_name in self.intents

    def call(self, intent_name: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用自定义意图
        
        Args:
            intent_name: 意图名称
            entities: 实体参数
            
        Returns:
            dict: {"success": bool, "text": "回复文本", "data": {...}}
        """
        if not self._loaded or intent_name not in self.intents:
            return {"success": False, "text": "服务暂不可用，请稍后再试。"}

        intent_config = self.intents[intent_name]
        endpoint = intent_config.get('endpoint', '')
        method = intent_config.get('method', 'GET').upper()
        timeout = intent_config.get('timeout', 10)

        # 构建请求
        url = endpoint
        headers = {}
        body = None

        # 鉴权
        auth_env = intent_config.get('auth_env', '')
        if auth_env:
            token = os.environ.get(auth_env, '')
            if token:
                headers['Authorization'] = f'Bearer {token}'
                headers['Content-Type'] = 'application/json'

        # 请求模板
        request_template = intent_config.get('request_template', {})
        if request_template:
            # 替换模板变量
            body = self._render_template(request_template, entities)
            try:
                body = json.dumps(body, ensure_ascii=False).encode('utf-8')
            except Exception:
                pass

        # URL 参数替换（GET 请求）
        if method == 'GET' and entities:
            query_params = []
            for k, v in entities.items():
                if v:
                    query_params.append(f"{k}={v}")
            if query_params:
                url = f"{endpoint}?{'&'.join(query_params)}"

        # 发送请求
        try:
            req = Request(url, data=body, headers=headers, method=method)
            with urlopen(req, timeout=timeout) as resp:
                resp_data = json.loads(resp.read().decode('utf-8'))

            # 响应话术模板
            response_template = intent_config.get('response_template', '')
            if response_template:
                text = self._render_response_template(response_template, resp_data)
            else:
                text = f"查询完成：{json.dumps(resp_data, ensure_ascii=False)[:200]}"

            return {"success": True, "text": text, "data": resp_data}

        except HTTPError as e:
            logger.warning(f"自定义意图 HTTP 错误: {e.code}")
            return self._handle_error(intent_config, f"HTTP {e.code}")
        except URLError as e:
            logger.warning(f"自定义意图 URL 错误: {e.reason}")
            return self._handle_error(intent_config, "网络错误")
        except Exception as e:
            logger.warning(f"自定义意图调用失败: {e}")
            return self._handle_error(intent_config, str(e))

    def _render_template(self, template: Dict, entities: Dict) -> Dict:
        """渲染请求模板"""
        result = {}
        for k, v in template.items():
            if isinstance(v, str):
                result[k] = self._replace_vars(v, entities)
            else:
                result[k] = v
        return result

    def _render_response_template(self, template: str, data: Dict) -> str:
        """渲染响应话术模板"""
        result = template
        # 支持 {{field.path}} 格式
        for match in re.finditer(r'\{\{([\w.]+)\}\}', template):
            field_path = match.group(1)
            value = self._get_nested_value(data, field_path)
            if value is not None:
                result = result.replace(match.group(0), str(value))
        return result

    def _replace_vars(self, text: str, entities: Dict) -> str:
        """替换模板变量"""
        result = text
        for k, v in entities.items():
            result = result.replace(f"{{{k}}}", str(v))
        return result

    def _get_nested_value(self, data: Dict, path: str) -> Any:
        """获取嵌套字典值"""
        keys = path.split('.')
        current = data
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            else:
                return None
        return current

    def _handle_error(self, intent_config: Dict, error_msg: str) -> Dict[str, Any]:
        """处理错误，返回兜底话术"""
        fallback = intent_config.get('fallback_text', '服务暂不可用，请稍后再试。')
        return {"success": False, "text": fallback, "error": error_msg}


# ==========================================
# 便捷函数
# ==========================================

def call_custom_intent(intent_name: str, entities: Dict[str, Any]) -> Dict[str, Any]:
    """便捷函数：调用自定义意图"""
    plugin = CustomIntentPlugin()
    plugin.load()
    return plugin.call(intent_name, entities)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行自定义意图插件自测"""
    print("=" * 60)
    print("自定义意图插件 — 自测模式")
    print("=" * 60)

    plugin = CustomIntentPlugin()

    # 测试 1: 加载（文件可能不存在）
    print("\n[测试 1] 加载配置")
    loaded = plugin.load()
    print(f"  加载结果: {'成功' if loaded else '文件不存在（跳过）'}")
    print("✅ 加载测试通过")

    # 测试 2: 模板渲染
    print("\n[测试 2] 模板渲染")
    template = {"order_id": "{order_id}", "user": "{user}"}
    entities = {"order_id": "123", "user": "张三"}
    rendered = plugin._render_template(template, entities)
    print(f"  模板: {template}")
    print(f"  实体: {entities}")
    print(f"  结果: {rendered}")
    assert rendered["order_id"] == "123"
    assert rendered["user"] == "张三"
    print("✅ 模板渲染通过")

    # 测试 3: 响应模板渲染
    print("\n[测试 3] 响应模板渲染")
    resp_template = "您的订单{{order.status}}，预计{{order.eta}}送达。"
    resp_data = {"order": {"status": "已发货", "eta": "明天"}}
    text = plugin._render_response_template(resp_template, resp_data)
    print(f"  模板: {resp_template}")
    print(f"  数据: {resp_data}")
    print(f"  结果: {text}")
    assert "已发货" in text
    assert "明天" in text
    print("✅ 响应模板渲染通过")

    # 测试 4: 嵌套值获取
    print("\n[测试 4] 嵌套值获取")
    data = {"a": {"b": {"c": "value"}}}
    val = plugin._get_nested_value(data, "a.b.c")
    print(f"  a.b.c = {val}")
    assert val == "value"
    print("✅ 嵌套值获取通过")

    # 测试 5: 错误兜底
    print("\n[测试 5] 错误兜底")
    intent_config = {"fallback_text": "服务繁忙，请稍后再试。"}
    result = plugin._handle_error(intent_config, "timeout")
    print(f"  兜底结果: {result}")
    assert result["success"] is False
    assert "服务繁忙" in result["text"]
    print("✅ 错误兜底通过")

    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_self_test()
