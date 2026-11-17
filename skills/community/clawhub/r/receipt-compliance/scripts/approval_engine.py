#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
审批系统对接引擎（v4.4.0 重构）

v4.4.0 变化：
- 钉钉 / 企业微信 / 飞书三套独立代码统一到 ApprovalConnector 接口
  （send 发送 / query_status 查状态 / verify_callback 回调验签）
- 本模块保留为兼容层：现有调用方（DingTalkApproval / WeComApproval /
  FeishuApproval / ApprovalManager）无需改动即可继续使用
- 新增审批平台只需在 approval_connector.py 中实现接口，不必改这里

安全约定：
- 密钥通过 secure_config 从环境变量读取（INVOICE_ 前缀），不在配置文件明文存储
- 所有网络请求使用 urllib，不启用 shell
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from approval_connector import (
        ApprovalConnector,
        DingTalkConnector,
        WeComConnector,
        FeishuConnector,
        get_connector,
        supported_platforms,
    )
except ImportError:  # 允许从其他目录调用
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from approval_connector import (
        ApprovalConnector,
        DingTalkConnector,
        WeComConnector,
        FeishuConnector,
        get_connector,
        supported_platforms,
    )


# === 兼容旧类名的外壳：逻辑全部由连接器提供 ===

class DingTalkApproval(DingTalkConnector):
    """钉钉审批（兼容旧名，实现见 DingTalkConnector）"""

    def __init__(self, app_key, app_secret, process_code):
        super().__init__(app_key=app_key, app_secret=app_secret,
                         process_code=process_code)


class WeComApproval(WeComConnector):
    """企业微信审批（兼容旧名，实现见 WeComConnector）"""

    def __init__(self, corp_id, secret, template_id):
        super().__init__(corp_id=corp_id, secret=secret, template_id=template_id)


class FeishuApproval(FeishuConnector):
    """飞书审批（兼容旧名，实现见 FeishuConnector）"""

    def __init__(self, app_id, app_secret, approval_code):
        super().__init__(app_id=app_id, app_secret=app_secret,
                         approval_code=approval_code)


# === 平台与凭证字段的映射 ===
PLATFORM_CREDENTIAL_KEYS = {
    "dingtalk": ("app_key", "app_secret", "process_code"),
    "wecom": ("corp_id", "secret", "template_id"),
    "feishu": ("app_id", "app_secret", "approval_code"),
}


class ApprovalManager:
    """审批管理器 - 统一入口（基于 ApprovalConnector）"""

    def __init__(self, config_path: Optional[str] = None,
                 connector: Optional[ApprovalConnector] = None):
        self.config: Dict[str, Any] = {}
        self.config_path = config_path
        self.connector = connector
        self.engine = None  # 兼容旧属性：等价于 connector

        if connector:
            return

        if config_path and Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as f:
                text = f.read()
            try:
                self.config = json.loads(text)
            except json.JSONDecodeError:
                self.config = {}
            self._init_engine()

    def _init_engine(self):
        approval = self.config.get("approval", {})
        platform = (approval.get("platform") or "none").lower()
        credentials = approval.get(platform, {}) or {}

        self.connector = get_connector(platform, credentials)
        self.engine = self.connector

    # ---------- 对外方法 ----------

    def submit_approval(self, expense_file, **kwargs) -> Dict[str, Any]:
        """发起审批"""
        platform = (self.config.get("approval", {}) or {}).get("platform", "none")
        if not self.connector:
            return self._not_configured(platform, expense_file)
        return self.connector.send(expense_file, **kwargs)

    def query_status(self, approval_id: str) -> Dict[str, Any]:
        """查询审批状态（v4.4.0 新增）"""
        if not self.connector:
            return {"status": "not_configured", "message": "审批系统未配置"}
        return self.connector.query_status(approval_id)

    def verify_callback(self, payload: Dict[str, Any], **kwargs) -> bool:
        """回调验签（v4.4.0 新增）"""
        if not self.connector:
            return False
        return self.connector.verify_callback(payload, **kwargs)

    @staticmethod
    def _not_configured(platform: str, expense_file) -> Dict[str, Any]:
        if platform in ("none", "", None):
            return {
                "status": "not_configured",
                "message": '审批系统未配置，当前platform设置为"none"',
                "hint": "如需启用审批功能，请将 approval.platform 设置为 "
                        f"{'/'.join(supported_platforms())}",
                "file_path": str(expense_file),
            }
        if platform == "custom":
            return {
                "status": "custom_required",
                "message": "企业需自行实现审批系统接口",
                "hint": "在 approval_connector.py 中继承 ApprovalConnector 并实现 "
                        "send / query_status / verify_callback 三个方法即可",
                "file_path": str(expense_file),
            }
        return {
            "status": "config_error",
            "message": f'审批平台"{platform}"初始化失败，支持的平台：'
                       f"{'/'.join(supported_platforms())}",
            "file_path": str(expense_file),
        }


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="审批系统对接引擎")
    parser.add_argument("--config", required=True, help="配置文件路径")
    parser.add_argument("--expense", required=True, help="报销单文件路径")
    parser.add_argument("--output", help="输出文件路径（可选）")
    parser.add_argument("--user-id", help="申请人用户ID")
    parser.add_argument("--amount", help="报销金额")
    parser.add_argument("--expense-type", help="费用类型")
    parser.add_argument("--query", help="查询审批状态：传入审批实例ID")
    args = parser.parse_args()

    try:
        manager = ApprovalManager(args.config)
        if args.query:
            result = manager.query_status(args.query)
        else:
            result = manager.submit_approval(
                args.expense,
                applicant_user_id=args.user_id,
                amount=args.amount,
                expense_type=args.expense_type,
            )
    except Exception as e:
        result = {
            "status": "error",
            "message": str(e),
            "submit_time": datetime.now().isoformat(),
        }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
