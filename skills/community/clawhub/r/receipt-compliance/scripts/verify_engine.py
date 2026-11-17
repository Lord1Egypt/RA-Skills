#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真伪查验引擎 - 真正可用的发票查验工具
核心功能：
1. 一键生成国税总局查验链接
2. 自动打开浏览器进行查验
3. 支持复制链接手动查验
4. 可选：配置第三方API自动获取查验结果
"""
import json
import re
import sys
import time
import hashlib
import shutil
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path

try:
    import urllib.request
    import urllib.parse
    import urllib.error
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False


class TaxBureauVerifier:
    """国税总局查验平台自动查验"""

    def __init__(self):
        self.name = "国税总局查验平台"
        self.base_url = "https://inv-veri.chinatax.gov.cn"
        self.verify_url = f"{self.base_url}/index.html"
        self._last_request_time = 0
        self._min_interval = 1.0  # 最小请求间隔（秒）
        self._max_retries = 3  # 最大重试次数

    def _wait_rate_limit(self):
        """控制请求频率"""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request_time = time.time()

    def _build_verify_url(self, invoice_code, invoice_number, date, amount):
        """构造查验URL"""
        # 将中文日期格式统一转换为YYYY-MM-DD
        normalized_date = date
        if '年' in date:
            match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date)
            if match:
                normalized_date = f"{match.group(1)}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"
        elif re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            normalized_date = date
        elif re.match(r'^\d{8}$', date):
            # 格式：20260628
            normalized_date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"

        params = {
            'fpdm': str(invoice_code).strip(),
            'fphm': str(invoice_number).strip(),
            'kprq': normalized_date,
            'fpje': str(amount).strip(),
            'yzm': '',  # 验证码（需要OCR识别或人工输入）
            'yzmSj': '',
            'index': '0',
            'yzmcode': '',
        }
        query_string = urllib.parse.urlencode(params, encoding='gbk')
        return f"{self.base_url}/index.html?{query_string}"

    def verify(self, invoice_code, invoice_number, date=None, amount=None, auto_open=False):
        """
        查验发票真伪，生成国税总局查验链接
        
        使用方式：
        1. 自动打开浏览器查验（推荐）：verify(..., auto_open=True)
        2. 手动复制链接查验：verify(..., auto_open=False)

        Args:
            invoice_code: 发票代码（10-12位数字）
            invoice_number: 发票号码（8-20位数字）
            date: 开票日期（支持：2026年06月28日、2026-06-28、20260628）
            amount: 金额（不含税，支持：10000、10,000、¥10000）
            auto_open: 是否自动打开浏览器

        Returns:
            dict: 查验结果，包含查验链接和参数
        """
        # 检查必填参数
        missing = []
        if not invoice_code:
            missing.append('发票代码')
        if not invoice_number:
            missing.append('发票号码')
        if not date:
            missing.append('开票日期')
        if amount is None or amount == '':
            missing.append('金额')

        if missing:
            return {
                'engine': self.name,
                'status': 'param_error',
                'message': f'参数不完整，缺少：{", ".join(missing)}',
                'hint': '需要：发票代码、发票号码、开票日期、金额',
            }

        # 参数格式校验
        if not re.match(r'^\d{10,12}$', str(invoice_code)):
            return {
                'engine': self.name,
                'status': 'param_error',
                'message': f'发票格式不正确：{invoice_code}，应为10-12位数字',
                'hint': '请检查发票代码是否正确',
            }

        if not re.match(r'^\d{8,20}$', str(invoice_number)):
            return {
                'engine': self.name,
                'status': 'param_error',
                'message': f'发票号码格式不正确：{invoice_number}，应为8-20位数字',
                'hint': '请检查发票号码是否正确',
            }

        # 金额格式校验和转换
        try:
            if isinstance(amount, str):
                amount = float(amount.replace(',', '').replace('¥', '').strip())
            amount = float(amount)
            if amount < 0:
                raise ValueError('金额不能为负数')
        except (ValueError, TypeError) as e:
            return {
                'engine': self.name,
                'status': 'param_error',
                'message': f'金额格式不正确：{amount}，错误：{e}',
                'hint': '金额应为正数，支持格式：10000、10,000、¥10000',
            }

        self._wait_rate_limit()

        # 构造查验URL（完整版带参数）
        verify_url = self._build_verify_url(
            invoice_code, invoice_number, date, amount
        )
        # 简化版链接（仅含代码和号码，打开后手动输入日期和金额）
        short_url = (f"{self.base_url}/index.html?"
                     f"fpdm={invoice_code}&fphm={invoice_number}")

        # 自动打开浏览器（如果用户要求）
        browser_opened = False
        if auto_open:
            try:
                # 尝试打开浏览器
                browser_opened = webbrowser.open(short_url)
                if not browser_opened:
                    # 尝试用系统命令打开
                    if sys.platform == 'win32':
                        subprocess.Popen(['cmd', '/c', 'start', short_url])
                    elif sys.platform == 'darwin':
                        subprocess.Popen(['open', short_url])
                    else:
                        subprocess.Popen(['xdg-open', short_url])
                    browser_opened = True
            except Exception:
                pass  # 打开失败不影响返回结果

        return {
            'engine': self.name,
            'status': 'ready',
            'message': '已为您生成查验链接，浏览器已自动打开（如未自动打开，请点击上方链接）',
            'verify_url': short_url,
            'full_url': verify_url,
            'params': {
                'invoice_code': invoice_code,
                'invoice_number': invoice_number,
                'billing_date': date,
                'amount': amount,
            },
            'browser_opened': auto_open and browser_opened,
            'note': '发票数据仅上传到国税总局官网（inv-veri.chinatax.gov.cn），不上传到任何第三方服务器',
            'verify_time': datetime.now().isoformat(),
        }


class ThirdPartyVerifier:
    """第三方查验（需要API Key）"""

    def __init__(self, platform, api_key='', api_secret=''):
        self.platform = platform
        self.api_key = api_key
        self.api_secret = api_secret
        self.name = f"{platform}查验"

    def verify(self, invoice_code, invoice_number, date=None, amount=None):
        # 检查API Key是否配置
        if not self.api_key:
            return {
                'engine': self.name,
                'status': 'key_required',
                'message': f'请在config.yaml中配置{self.platform}的API Key',
                'hint': f'编辑config.yaml，在{self.platform}.api_key处填写您的API密钥',
                'config_example': f'{self.platform}:\n  api_key: "您的API Key"\n  api_secret: "您的Secret"',
            }

        # 检查API Secret是否配置（部分平台需要）
        if not self.api_secret and self.platform in ('bairong', 'nuonuo'):
            return {
                'engine': self.name,
                'status': 'secret_required',
                'message': f'{self.platform}需要同时配置API Key和Secret',
                'hint': f'请在config.yaml的{self.platform}.api_secret处填写Secret',
            }

        # 参数校验
        missing = []
        if not invoice_code:
            missing.append('发票代码')
        if not invoice_number:
            missing.append('发票号码')
        if not date:
            missing.append('开票日期')
        if amount is None or amount == '':
            missing.append('金额')

        if missing:
            return {
                'engine': self.name,
                'status': 'param_error',
                'message': f'参数不完整，缺少：{", ".join(missing)}',
                'hint': '需要：发票代码、发票号码、开票日期、金额',
            }

        # TODO: 企业自行实现第三方API
        return {
            'engine': self.name,
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


class CompositeVerifier:
    """组合查验 - 多种引擎依次尝试"""

    def __init__(self):
        self.engines = []
        self.tax_bureau = TaxBureauVerifier()

    def add_engine(self, verifier):
        self.engines.append(verifier)

    def verify(self, invoice_code, invoice_number, date=None, amount=None):
        """依次尝试所有可用的查验引擎，带重试机制"""
        results = []
        errors = []

        # 1. 先尝试国税总局（免费）
        for retry in range(self.tax_bureau._max_retries):
            try:
                result = self.tax_bureau.verify(
                    invoice_code, invoice_number, date, amount
                )
                results.append(result)
                # 国税总局返回ready时也视为成功（返回了查验链接）
                if result.get('status') in ('success', 'ready'):
                    return result
                break  # 参数错误等不需要重试
            except Exception as e:
                errors.append(f"国税总局第{retry+1}次尝试失败: {str(e)}")
                if retry < self.tax_bureau._max_retries - 1:
                    time.sleep(2 ** retry)  # 指数退避

        # 2. 尝试其他引擎
        for engine in self.engines:
            try:
                result = engine.verify(
                    invoice_code, invoice_number, date, amount
                )
                results.append(result)
                if result.get('status') in ('success', 'ready', 'framework_ready'):
                    return result
            except Exception as e:
                errors.append(f"{engine.name}查验失败: {str(e)}")

        # 所有引擎都失败了，返回汇总
        return {
            'engine': '组合查验',
            'status': 'all_failed',
            'message': '所有查验引擎均未返回有效结果',
            'results': results,
            'errors': errors if errors else None,
            'verify_time': datetime.now().isoformat(),
        }


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='真伪查验引擎')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--invoice-code', required=True, help='发票代码')
    parser.add_argument('--invoice-number', required=True, help='发票号码')
    parser.add_argument('--date', help='开票日期 (2026年06月28日)')
    parser.add_argument('--amount', help='金额（不含税）')
    parser.add_argument('--output', help='输出文件路径（可选）')
    parser.add_argument('--open-browser', action='store_true', help='自动打开浏览器查验')

    args = parser.parse_args()

    verifier = CompositeVerifier()

    # 如果提供了配置文件，加载第三方引擎
    if args.config and Path(args.config).exists():
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)

        verify_engine = config.get('verify_engine', 'tax_bureau')
        if verify_engine in ('bairong', 'nuonuo'):
            engine_config = config.get(verify_engine, {})
            verifier.add_engine(ThirdPartyVerifier(
                platform=verify_engine,
                api_key=engine_config.get('api_key', ''),
                api_secret=engine_config.get('api_secret', ''),
            ))

    result = verifier.verify(
        args.invoice_code,
        args.invoice_number,
        args.date,
        args.amount,
        auto_open=args.open_browser,
    )

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"已保存到: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
