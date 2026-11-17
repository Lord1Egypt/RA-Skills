#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全密钥配置模块
功能：从环境变量读取 API 密钥，消除明文泄露风险

设计原则：
1. 密钥优先从环境变量读取，拒绝在配置文件中明文存储
2. 环境变量名统一前缀 INVOICE_，避免命名冲突
3. 未配置时给出明确的中文错误提示，引导用户设置
4. 提供降级方案：环境变量 → 配置文件占位符 → 报错提示
"""

import os
import json
import sys
from typing import Optional, Dict, Any


# === 环境变量名常量 ===
ENV_PREFIX = "INVOICE_"

ENV_KEYS = {
    # 钉钉审批
    "DINGTALK_APPKEY": f"{ENV_PREFIX}DINGTALK_APPKEY",
    "DINGTALK_SECRET": f"{ENV_PREFIX}DINGTALK_SECRET",
    "DINGTALK_PROCESS_CODE": f"{ENV_PREFIX}DINGTALK_PROCESS_CODE",
    # 企业微信审批
    "WECOM_CORP_ID": f"{ENV_PREFIX}WECOM_CORP_ID",
    "WECOM_SECRET": f"{ENV_PREFIX}WECOM_SECRET",
    "WECOM_TEMPLATE_ID": f"{ENV_PREFIX}WECOM_TEMPLATE_ID",
    # 飞书审批
    "FEISHU_APP_ID": f"{ENV_PREFIX}FEISHU_APP_ID",
    "FEISHU_APP_SECRET": f"{ENV_PREFIX}FEISHU_APP_SECRET",
    "FEISHU_APPROVAL_CODE": f"{ENV_PREFIX}FEISHU_APPROVAL_CODE",
    # 查验引擎
    "BAIRONG_API_KEY": f"{ENV_PREFIX}BAIRONG_API_KEY",
    "BAIRONG_API_SECRET": f"{ENV_PREFIX}BAIRONG_API_SECRET",
    "NUONUO_API_KEY": f"{ENV_PREFIX}NUONUO_API_KEY",
    "NUONUO_API_SECRET": f"{ENV_PREFIX}NUONUO_API_SECRET",
}

# === 占位符（表示未配置） ===
PLACEHOLDERS = {"", "your_key_here", "your_secret_here", "your_token_here", "待填写", "your-app-key", "null", "none"}


class SecureConfig:
    """
    安全配置读取器

    读取优先级：
    1. 环境变量（最高优先级）
    2. 系统密钥环（预留扩展接口）
    3. 配置文件（仅作为占位符提示，不含真实值）
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self._cache: Dict[str, Optional[str]] = {}
        self._missing_keys: list = []

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        获取密钥值

        优先从环境变量读取，找不到则返回默认值
        """
        if key in self._cache:
            return self._cache[key]

        # 从环境变量读取
        env_key = ENV_KEYS.get(key, key)
        value = os.environ.get(env_key)

        if value and value.strip().lower() not in PLACEHOLDERS:
            self._cache[key] = value.strip()
            return value.strip()

        # 返回默认值
        if default and default.strip().lower() not in PLACEHOLDERS:
            self._cache[key] = default.strip()
            return default.strip()

        # 记录缺失的密钥
        self._missing_keys.append((key, env_key))
        self._cache[key] = None
        return None

    def get_dingtalk_config(self) -> Dict[str, Optional[str]]:
        """获取钉钉审批配置"""
        return {
            "app_key": self.get("DINGTALK_APPKEY"),
            "app_secret": self.get("DINGTALK_SECRET"),
            "process_code": self.get("DINGTALK_PROCESS_CODE"),
        }

    def get_wecom_config(self) -> Dict[str, Optional[str]]:
        """获取企业微信审批配置"""
        return {
            "corp_id": self.get("WECOM_CORP_ID"),
            "secret": self.get("WECOM_SECRET"),
            "template_id": self.get("WECOM_TEMPLATE_ID"),
        }

    def get_feishu_config(self) -> Dict[str, Optional[str]]:
        """获取飞书审批配置"""
        return {
            "app_id": self.get("FEISHU_APP_ID"),
            "app_secret": self.get("FEISHU_APP_SECRET"),
            "approval_code": self.get("FEISHU_APPROVAL_CODE"),
        }

    def get_bairong_config(self) -> Dict[str, Optional[str]]:
        """获取百望云查验配置"""
        return {
            "api_key": self.get("BAIRONG_API_KEY"),
            "api_secret": self.get("BAIRONG_API_SECRET"),
        }

    def get_nuonuo_config(self) -> Dict[str, Optional[str]]:
        """获取诺诺发票查验配置"""
        return {
            "api_key": self.get("NUONUO_API_KEY"),
            "api_secret": self.get("NUONUO_API_SECRET"),
        }

    def require(self, *keys: str) -> bool:
        """
        检查必需的密钥是否全部配置
        返回 True 表示全部已配置，False 表示有缺失
        """
        all_present = True
        for key in keys:
            if not self.get(key):
                all_present = False
        return all_present

    def get_missing_keys_report(self) -> str:
        """生成缺失密钥的中文报告"""
        if not self._missing_keys:
            return "✅ 所有密钥均已配置"

        lines = ["⚠️ 以下密钥尚未配置：\n"]
        for key, env_key in self._missing_keys:
            lines.append(f"  • {key}")
            lines.append(f"    请设置环境变量: {env_key}")
            lines.append(f"    Windows PowerShell: $env:{env_key} = \"你的密钥\"")
            lines.append(f"    Linux/macOS: export {env_key}=\"你的密钥\"")
            lines.append("")

        return "\n".join(lines)

    def validate_before_call(self, platform: str) -> Dict[str, Any]:
        """
        调用外部 API 前的配置校验
        返回校验结果，仅包含字段名和布尔状态，绝不输出密钥值
        """
        platform = platform.lower()
        result = {"ready": False, "platform": platform, "missing": []}

        if platform == "dingtalk":
            cfg = self.get_dingtalk_config()
        elif platform == "wecom":
            cfg = self.get_wecom_config()
        elif platform == "feishu":
            cfg = self.get_feishu_config()
        elif platform == "bairong":
            cfg = self.get_bairong_config()
        elif platform == "nuonuo":
            cfg = self.get_nuonuo_config()
        else:
            result["error"] = f"未知平台: {platform}"
            return result

        missing = [k for k, v in cfg.items() if not v]
        if missing:
            result["missing"] = missing
            result["error"] = f"缺失配置字段: {', '.join(missing)}"
        else:
            result["ready"] = True
            # 只返回字段名列表，绝不返回任何形态的密钥值
            result["fields_configured"] = list(cfg.keys())

        return result

    @staticmethod
    def _mask_value(value: Optional[str]) -> str:
        """对单个密钥值进行脱敏显示"""
        if not value:
            return "<未配置>"
        if len(value) <= 6:
            return "***"
        return value[:3] + "***" + value[-3:]

    def mask_key(self, key: str) -> str:
        """对密钥进行脱敏显示（用于日志）"""
        value = self._cache.get(key, "")
        if not value:
            return "<未配置>"
        if len(value) <= 6:
            return "***"
        return value[:3] + "***" + value[-3:]


# ======================================================================
# 全局单例
# ======================================================================

_instance: Optional[SecureConfig] = None


def get_config(config_path: Optional[str] = None) -> SecureConfig:
    """获取全局 SecureConfig 单例"""
    global _instance
    if _instance is None:
        _instance = SecureConfig(config_path)
    return _instance


def reset_config():
    """重置全局单例（用于测试）"""
    global _instance
    _instance = None


# ======================================================================
# CLI 入口
# ======================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="安全密钥配置检查")
    parser.add_argument("--platform", choices=["dingtalk", "wecom", "feishu", "bairong", "nuonuo", "all"],
                        default="all", help="检查指定平台的密钥配置")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    args = parser.parse_args()

    cfg = get_config()

    if args.platform == "all":
        platforms = ["dingtalk", "wecom", "feishu", "bairong", "nuonuo"]
    else:
        platforms = [args.platform]

    result = {}
    for platform in platforms:
        validation = cfg.validate_before_call(platform)
        result[platform] = validation

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for platform, info in result.items():
            status = "✅ 已配置" if info["ready"] else f"❌ 未配置: {info.get('error', '')}"
            print(f"{platform}: {status}")

    # 如果有未配置的，退出码为 1
    if not all(info["ready"] for info in result.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
