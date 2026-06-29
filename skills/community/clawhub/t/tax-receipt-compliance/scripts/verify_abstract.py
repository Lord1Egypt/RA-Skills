#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真伪查验抽象接口 - 企业自主配置引擎
Skill仅提供技术框架，所有决策权交给企业
"""

import json
import argparse
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime

# 尝试导入yaml
try:
    import yaml
except ImportError:
    print("WARNING: pyyaml未安装，将使用JSON配置")
    yaml = None


class VerifyEngine(ABC):
    """查验引擎抽象基类"""

    @abstractmethod
    def verify(self, invoice_code, invoice_number, date=None, amount=None):
        """
        查验发票真伪

        Args:
            invoice_code: 发票代码
            invoice_number: 发票号码
            date: 开票日期（可选）
            amount: 金额（可选）

        Returns:
            dict: 查验结果
        """
        pass

    @abstractmethod
    def get_engine_name(self):
        """返回引擎名称"""
        pass


class TaxBureauEngine(VerifyEngine):
    """
    国税总局查验平台引擎（免费）
    企业无需申请API Key，直接调用
    """

    def __init__(self):
        self.name = "国税总局查验平台"

    def get_engine_name(self):
        return self.name

    def verify(self, invoice_code, invoice_number, date=None, amount=None):
        """
        通过国税总局平台查验

        说明：此方法为示例实现，实际使用时需要：
        1. 模拟访问 https://inv-veri.chinatax.gov.cn/
        2. 解析返回结果
        3. 处理验证码等问题

        由于国税总局平台的防爬机制，建议企业自行：
        - 使用浏览器插件辅助识别
        - 或接入其官方API（如有开放）
        """
        return {
            'engine': self.get_engine_name(),
            'status': 'manual_required',
            'message': '请手动访问国税总局查验平台进行验证',
            'url': 'https://inv-veri.chinatax.gov.cn/',
            'params': {
                'invoice_code': invoice_code,
                'invoice_number': invoice_number,
                'date': date,
                'amount': amount,
            },
            'verify_time': datetime.now().isoformat(),
        }


class CustomEngine(VerifyEngine):
    """
    自定义查验引擎（企业自建接口）
    企业需要提供接口地址和鉴权方式
    """

    def __init__(self, endpoint, method='POST', headers=None, timeout=30):
        self.name = "企业自建接口"
        self.endpoint = endpoint
        self.method = method
        self.headers = headers or {}
        self.timeout = timeout

    def get_engine_name(self):
        return self.name

    def verify(self, invoice_code, invoice_number, date=None, amount=None):
        """
        调用企业自建接口查验

        说明：此方法为接口框架，实际使用时需要：
        1. 企业自建查验接口
        2. 实现接口鉴权
        3. 解析返回结果
        """
        import urllib.request
        import urllib.error

        payload = json.dumps({
            'invoice_code': invoice_code,
            'invoice_number': invoice_number,
            'date': date,
            'amount': amount,
        }).encode('utf-8')

        req = urllib.request.Request(
            self.endpoint,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                **self.headers
            },
            method=self.method
        )

        try:
            # 注意：实际生产环境建议使用requests库而非urllib
            # 此处使用urllib是为了减少外部依赖
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode('utf-8'))
                return {
                    'engine': self.get_engine_name(),
                    'status': result.get('status', 'unknown'),
                    'message': result.get('message', ''),
                    'data': result.get('data', {}),
                    'verify_time': datetime.now().isoformat(),
                }
        except urllib.error.URLError as e:
            return {
                'engine': self.get_engine_name(),
                'status': 'error',
                'message': f'接口调用失败: {str(e)}',
                'verify_time': datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                'engine': self.get_engine_name(),
                'status': 'error',
                'message': f'未知错误: {str(e)}',
                'verify_time': datetime.now().isoformat(),
            }


class VerifyManager:
    """查验管理器"""

    def __init__(self, config_path=None):
        """
        初始化管理器

        Args:
            config_path: 配置文件路径（YAML或JSON）
        """
        self.config = {}
        self.engine = None

        if config_path and Path(config_path).exists():
            self._load_config(config_path)
            self._init_engine()

    def _load_config(self, path):
        """加载配置文件"""
        with open(path, 'r', encoding='utf-8') as f:
            if yaml and path.endswith(('.yaml', '.yml')):
                self.config = yaml.safe_load(f)
            else:
                self.config = json.load(f)

    def _init_engine(self):
        """初始化查验引擎"""
        engine_type = self.config.get('verify_engine', 'tax_bureau')

        if engine_type == 'tax_bureau':
            self.engine = TaxBureauEngine()
        elif engine_type == 'custom':
            custom = self.config.get('custom', {})
            self.engine = CustomEngine(
                endpoint=custom.get('endpoint', ''),
                method=custom.get('method', 'POST'),
                headers=custom.get('headers', {}),
                timeout=custom.get('timeout', 30),
            )
        elif engine_type in ('bairong', 'nuonuo'):
            # 第三方平台需要企业自行申请API Key
            self.engine = ThirdPartyEngine(engine_type, self.config)
        elif engine_type == 'none':
            self.engine = None
        else:
            raise ValueError(f"未知的查验引擎类型: {engine_type}")

    def verify(self, receipt_data):
        """
        执行查验

        Args:
            receipt_data: 发票数据dict

        Returns:
            dict: 查验结果
        """
        if not self.engine:
            return {
                'status': 'not_configured',
                'message': '查验引擎未配置，请编辑config.yaml',
                'suggestion': '如需使用免费平台，请将verify_engine设为"tax_bureau"',
            }

        return self.engine.verify(
            invoice_code=receipt_data.get('invoice_code', ''),
            invoice_number=receipt_data.get('invoice_number', ''),
            date=receipt_data.get('invoice_date', ''),
            amount=receipt_data.get('amount', 0),
        )

    def get_engine_info(self):
        """获取当前引擎信息"""
        if not self.engine:
            return {'status': 'not_configured'}
        return {
            'status': 'ready',
            'engine': self.engine.get_engine_name(),
        }


class ThirdPartyEngine(VerifyEngine):
    """第三方平台引擎（示例框架）"""

    def __init__(self, platform, config):
        self.platform = platform
        self.config = config
        self.api_key = config.get(platform, {}).get('api_key', '')
        self.api_secret = config.get(platform, {}).get('api_secret', '')

    def get_engine_name(self):
        return f"{self.platform}查验"

    def verify(self, invoice_code, invoice_number, date=None, amount=None):
        """第三方平台调用框架"""
        if not self.api_key:
            return {
                'engine': self.get_engine_name(),
                'status': 'key_required',
                'message': f'请在config.yaml中配置{self.platform}的API Key',
                'apply_url': self._get_apply_url(),
            }

        # TODO: 企业自行实现第三方平台API调用
        return {
            'engine': self.get_engine_name(),
            'status': 'not_implemented',
            'message': f'企业需自行实现{self.platform}平台的API调用逻辑',
            'params': {
                'invoice_code': invoice_code,
                'invoice_number': invoice_number,
                'date': date,
                'amount': amount,
            },
            'verify_time': datetime.now().isoformat(),
        }

    def _get_apply_url(self):
        """获取申请链接"""
        urls = {
            'bairong': 'https://www.bairong.com',
            'nuonuo': 'https://www.nuonuo.com',
        }
        return urls.get(self.platform, '')


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='真伪查验引擎')
    parser.add_argument('--config', required=True, help='配置文件路径')
    parser.add_argument('--receipt', required=True, help='发票数据JSON文件路径')
    parser.add_argument('--output', help='输出文件路径（可选）')

    args = parser.parse_args()

    # 读取发票数据
    with open(args.receipt, 'r', encoding='utf-8') as f:
        receipt_data = json.load(f)

    # 初始化管理器
    try:
        manager = VerifyManager(args.config)
    except Exception as e:
        print(f"ERROR: 配置加载失败: {e}")
        sys.exit(1)

    # 执行查验
    result = manager.verify(receipt_data)

    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
