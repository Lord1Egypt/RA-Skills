#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
审批系统对接抽象接口
企业自主配置审批平台，Skill仅提供技术框架
"""

import sys
import json
import argparse
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    yaml = None


class ApprovalEngine(ABC):
    """审批引擎抽象基类"""

    @abstractmethod
    def submit_approval(self, expense_file, approval_config):
        """提交审批"""
        pass

    @abstractmethod
    def get_engine_name(self):
        """返回引擎名称"""
        pass


class DingTalkEngine(ApprovalEngine):
    """钉钉审批引擎（待企业自行实现）"""

    def __init__(self, app_key, app_secret, process_code):
        self.name = "钉钉审批"
        self.app_key = app_key
        self.app_secret = app_secret
        self.process_code = process_code

    def get_engine_name(self):
        return self.name

    def submit_approval(self, expense_file, approval_config):
        """
        提交钉钉审批

        说明：此为接口框架，企业需自行：
        1. 在钉钉开放平台创建审批应用
        2. 获得AppKey和AppSecret
        3. 获取审批流程编码
        4. 实现OAuth2.0鉴权
        5. 调用审批提交API
        """
        if not self.app_key or not self.app_secret:
            return {
                'engine': self.get_engine_name(),
                'status': 'credentials_required',
                'message': '请提供钉钉应用的AppKey和AppSecret',
                'apply_url': 'https://open-dev.dingtalk.com',
            }

        return {
            'engine': self.get_engine_name(),
            'status': 'not_implemented',
            'message': '企业需自行调用钉钉审批API实现提交逻辑',
            'params': {
                'app_key': self.app_key[:4] + '****',  # 脱敏显示
                'process_code': self.process_code,
                'expense_file': expense_file,
            },
            'reference_url': 'https://open-dev.dingtalk.com/document',
            'submit_time': datetime.now().isoformat(),
        }


class WeComEngine(ApprovalEngine):
    """企业微信审批引擎（待企业自行实现）"""

    def __init__(self, corp_id, secret, template_id):
        self.name = "企业微信审批"
        self.corp_id = corp_id
        self.secret = secret
        self.template_id = template_id

    def get_engine_name(self):
        return self.name

    def submit_approval(self, expense_file, approval_config):
        """提交企业微信审批"""
        if not self.corp_id or not self.secret:
            return {
                'engine': self.get_engine_name(),
                'status': 'credentials_required',
                'message': '请提供企业微信的CorpID和Secret',
                'apply_url': 'https://work.weixin.qq.com',
            }

        return {
            'engine': self.get_engine_name(),
            'status': 'not_implemented',
            'message': '企业需自行调用企业微信审批API实现提交逻辑',
            'params': {
                'corp_id': self.corp_id[:4] + '****',
                'template_id': self.template_id,
                'expense_file': expense_file,
            },
            'reference_url': 'https://developer.weixin.qq.com/document/90000',
            'submit_time': datetime.now().isoformat(),
        }


class FeishuEngine(ApprovalEngine):
    """飞书审批引擎（待企业自行实现）"""

    def __init__(self, app_id, app_secret, approval_code):
        self.name = "飞书审批"
        self.app_id = app_id
        self.app_secret = app_secret
        self.approval_code = approval_code

    def get_engine_name(self):
        return self.name

    def submit_approval(self, expense_file, approval_config):
        """提交飞书审批"""
        if not self.app_id or not self.app_secret:
            return {
                'engine': self.get_engine_name(),
                'status': 'credentials_required',
                'message': '请提供飞书应用的AppID和AppSecret',
                'apply_url': 'https://open.feishu.cn',
            }

        return {
            'engine': self.get_engine_name(),
            'status': 'not_implemented',
            'message': '企业需自行调用飞书审批API实现提交逻辑',
            'params': {
                'app_id': self.app_id[:4] + '****',
                'approval_code': self.approval_code,
                'expense_file': expense_file,
            },
            'reference_url': 'https://open.feishu.cn/document/server-docs/approval-v4/message',
            'submit_time': datetime.now().isoformat(),
        }


class CustomApprovalEngine(ApprovalEngine):
    """企业自建审批引擎"""

    def __init__(self, endpoint, method='POST', headers=None):
        self.name = "企业自建审批系统"
        self.endpoint = endpoint
        self.method = method
        self.headers = headers or {}

    def get_engine_name(self):
        return self.name

    def submit_approval(self, expense_file, approval_config):
        """企业自建接口调用框架"""
        if not self.endpoint:
            return {
                'engine': self.get_engine_name(),
                'status': 'endpoint_required',
                'message': '请提供企业自建审批系统的接口地址',
            }

        return {
            'engine': self.get_engine_name(),
            'status': 'framework_ready',
            'message': '企业需自行实现实际接口调用逻辑',
            'params': {
                'endpoint': self.endpoint,
                'method': self.method,
                'expense_file': expense_file,
            },
            'submit_time': datetime.now().isoformat(),
        }


class ManualSubmission(ApprovalEngine):
    """手动提交（默认）"""

    def __init__(self):
        self.name = "手动提交"

    def get_engine_name(self):
        return self.name

    def submit_approval(self, expense_file, approval_config):
        return {
            'engine': self.get_engine_name(),
            'status': 'manual_required',
            'message': '审批系统未配置，请手动提交报销单',
            'file_path': str(expense_file),
            'submit_time': datetime.now().isoformat(),
        }


class ApprovalManager:
    """审批管理器"""

    def __init__(self, config_path=None):
        self.config = {}
        self.engine = None

        if config_path and Path(config_path).exists():
            self._load_config(config_path)
            self._init_engine()

    def _load_config(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            if yaml and path.endswith(('.yaml', '.yml')):
                self.config = yaml.safe_load(f)
            else:
                self.config = json.load(f)

    def _init_engine(self):
        approval = self.config.get('approval', {})
        platform = approval.get('platform', 'none')

        if platform == 'dingtalk':
            dt = approval.get('dingtalk', {})
            self.engine = DingTalkEngine(
                app_key=dt.get('app_key', ''),
                app_secret=dt.get('app_secret', ''),
                process_code=dt.get('process_code', ''),
            )
        elif platform == 'wecom':
            wc = approval.get('wecom', {})
            self.engine = WeComEngine(
                corp_id=wc.get('corp_id', ''),
                secret=wc.get('secret', ''),
                template_id=wc.get('template_id', ''),
            )
        elif platform == 'feishu':
            fs = approval.get('feishu', {})
            self.engine = FeishuEngine(
                app_id=fs.get('app_id', ''),
                app_secret=fs.get('app_secret', ''),
                approval_code=fs.get('approval_code', ''),
            )
        elif platform == 'custom':
            custom = approval.get('custom', {})
            self.engine = CustomApprovalEngine(
                endpoint=custom.get('endpoint', ''),
                method=custom.get('method', 'POST'),
                headers=custom.get('headers', {}),
            )
        else:
            self.engine = ManualSubmission()

    def submit_approval(self, expense_file):
        if not self.engine:
            return {
                'status': 'not_configured',
                'message': '审批系统未配置',
            }

        return self.engine.submit_approval(expense_file, {})


def main():
    parser = argparse.ArgumentParser(description='审批系统对接引擎')
    parser.add_argument('--config', required=True, help='配置文件路径')
    parser.add_argument('--expense', required=True, help='报销单文件路径')
    parser.add_argument('--output', help='输出文件路径（可选）')

    args = parser.parse_args()

    try:
        manager = ApprovalManager(args.config)
        result = manager.submit_approval(args.expense)
    except Exception as e:
        result = {
            'status': 'error',
            'message': str(e),
            'submit_time': datetime.now().isoformat(),
        }

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
