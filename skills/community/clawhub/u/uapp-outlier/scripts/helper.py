#!/usr/bin/env python3
"""
UApp Outlier Detection Helper

Utility script for querying 友盟+ (UApp) application anomaly data.
Provides convenient functions for all three API endpoints.

Usage:
    # Set credentials first (one of these methods):
    # 1. Create umeng-config.json in current directory or home directory
    # 2. Set environment variables: UMENG_API_KEY and UMENG_API_SECURITY
    # 3. Pass credentials directly in function calls

    # Get outlier report for specific app
    python helper.py report --appkey YOUR_APPKEY --date 20260401

    # Get yesterday's outliers
    python helper.py yesterday

    # Get intelligent inspection summary
    python helper.py inspection

    # With direct credentials
    python helper.py report --appkey YOUR_APPKEY --date 20260401 --ak YOUR_AK --sk YOUR_SK
"""

import requests
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from stats_client import StatsClient


class UAppOutlierClient:
    """Client for UApp Outlier Detection APIs."""

    BASE_URL = "https://mobile.umeng.com/ht/api/v3"

    ERROR_CODES = {
        "100001": "事件标识符（event ID）为null",
        "100002": "事件标识符（event ID）为空串或全空格",
        "100003": "事件标识符（event ID）与系统预留事件冲突",
        "100004": "事件标识符（event ID）超过128字节",
        "100005": "事件标识符（event ID）含不合法字符",
        "100006": "事件属性数量超限",
        "100007": "属性标识符（key）与系统预留属性冲突",
        "100008": "IOS的key类型不合法",
        "100009": "属性标识符（key）超过128字节",
        "100010": "属性值（value）为空@\"\"",
        "100011": "属性值（value）为null",
        "100012": "属性值（value）超过256字节",
        "100013": "IOS下属性值（value）类型不合法",
        "100014": "参数参数类型不合法",
        "100015": "属性数量为0",
        "100016": "属性标识符（key）为空@\"\"",
        "100020": "事件时长（duration）超长",
        "100022": "label参数值超过256字节",
        "100023": "参数事件接口调用时传入属性值为null",
        "100024": "属性标识符（key）为null",
        "100025": "属性标识符（key）含不合法字符",
        "100026": "Android下属性值（value）类型不合法",
        "200002": "事件标识符/事件名重复",
        "200001": "事件数量超限",
        "200003": "属性标识符/属性名重复",
    }

    def __init__(self, ak=None, sk=None):
        """Initialize client with credentials."""
        self.ak = ak
        self.sk = sk
        self._load_credentials()
        self._app_map = self._load_app_mapping()

        self.headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Accept': '*/*',
            'Host': 'mobile.umeng.com',
            'Connection': 'keep-alive'
        }

        self.stats = StatsClient()

    def _load_app_mapping(self):
        """Load app name to appkey mapping from config file."""
        config = self._find_config_file()
        if config:
            apps = config.get("apps", {})
            # Build bidirectional map: both name->key and key->key
            mapping = {}
            for key, name in apps.items():
                mapping[key] = key
                mapping[name.lower()] = key
                mapping[name] = key
            return mapping
        return {}

    def resolve_appkey(self, app_input):
        """
        Resolve app input to appkey.

        Args:
            app_input: Either an appkey (string of hex chars) or app name

        Returns:
            str: The resolved appkey

        Raises:
            ValueError: If appkey cannot be resolved
        """
        if not app_input:
            raise ValueError("App input is required (appkey or app name)")

        # Check if input looks like an appkey (hex string, typically 24+ chars)
        if all(c in '0123456789abcdef' for c in app_input.lower()) and len(app_input) >= 20:
            return app_input

        # Try to find in app mapping
        if app_input in self._app_map:
            return self._app_map[app_input]

        # Try case-insensitive match
        for key, value in self._app_map.items():
            if key.lower() == app_input.lower():
                return value

        raise ValueError(
            f"Cannot find appkey for '{app_input}'. "
            f"Please provide a valid appkey or add the app mapping to umeng-config.json.\n"
            f"Config format: {{\"apps\": {{\"appkey\": \"app_name\"}}}}"
        )

    def _load_credentials(self):
        """Load credentials from various sources with priority order."""
        # Priority 1: Direct parameters (already set in __init__)
        if self.ak and self.sk:
            return

        # Priority 2: Config file
        config = self._find_config_file()
        if config:
            self.ak = self.ak or config.get("apiKey")
            self.sk = self.sk or config.get("apiSecurity")
            if self.ak and self.sk:
                return

        # Priority 3: Environment variables
        self.ak = self.ak or os.environ.get("UMENG_API_KEY")
        self.sk = self.sk or os.environ.get("UMENG_API_SECURITY")

        if not self.ak or not self.sk:
            raise ValueError(
                "Credentials not found. Please provide apiKey and apiSecurity via:\n"
                "1. Direct parameters\n"
                "2. umeng-config.json file\n"
                "3. Environment variables: UMENG_API_KEY and UMENG_API_SECURITY"
            )

    def _find_config_file(self):
        """Search for umeng-config.json in common locations."""
        search_paths = [
            Path.cwd() / "umeng-config.json",
            Path.home() / "umeng-config.json",
        ]

        for path in search_paths:
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception:
                    continue

        return None

    def get_outlier_report(self, app_input, date):
        """
        Get outlier report for a specific app on a given date.

        Args:
            app_input: Application key or app name
            date: Date in yyyyMMdd format (e.g., '20260401')

        Returns:
            dict: API response data
        """
        appkey = self.resolve_appkey(app_input)
        url = f"{self.BASE_URL}/ai/getOutlierPoints"
        params = {
            'ak': self.ak,
            'sk': self.sk,
            'appkey': appkey,
            'ds': date
        }

        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        result = response.json()
        self.stats.report('outlier_report', appkey=appkey, extra={'date': date})
        return result

    def get_yesterday_outliers(self):
        """
        Get yesterday's outlier information for all applications.

        Returns:
            dict: API response data
        """
        url = f"{self.BASE_URL}/ai/getYesterdayOutliers"
        params = {
            'ak': self.ak,
            'sk': self.sk
        }

        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        result = response.json()
        self.stats.report('yesterday_outliers')
        return result

    def get_inspection_summary(self):
        """
        Get intelligent inspection summary.

        Returns:
            dict: API response data
        """
        url = f"{self.BASE_URL}/claw/meta/aiEventSummary"
        headers = {
            **self.headers,
            'Authorization': f'Bearer {self.sk}'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        self.stats.report('inspection_summary')
        return result

    def translate_error_code(self, code):
        """Translate error code to human-readable description."""
        return self.ERROR_CODES.get(str(code), f"Unknown error code: {code}")


def format_outlier_report(response):
    """Format outlier report response for display."""
    if response.get('code') != 200:
        print(f"Error: {response.get('msg', 'Unknown error')}")
        return

    data = response.get('data', {})
    for appkey, info in data.items():
        status_text = "异常" if info.get('status') == 1 else "正常"
        type_text = "绿点" if info.get('type') == 'green' else "红点"

        print(f"应用: {appkey}")
        print(f"日期: {info.get('ds')}")
        print(f"状态: {status_text}")
        print(f"类型: {type_text}")
        print(f"摘要: {info.get('category', 'N/A')}")
        print(f"报告链接: {info.get('shareUrl')}")
        print("-" * 50)


def format_yesterday_outliers(response):
    """Format yesterday's outliers response for display."""
    if response.get('code') != 200:
        print(f"Error: {response.get('msg', 'Unknown error')}")
        return

    data = response.get('data', [])
    if not data:
        print("昨天没有应用数据。")
        return

    anomalies = []
    normals = []

    for app in data:
        outlier = app.get('outlierTip', {})
        if outlier.get('status') == 1:
            anomalies.append(app)
        else:
            normals.append(app)

    if anomalies:
        print(f"发现 {len(anomalies)} 个应用存在异常：\n")
        for app in anomalies:
            outlier = app.get('outlierTip', {})
            type_text = "绿点" if outlier.get('type') == 'green' else "红点"
            print(f"应用名称: {app.get('name')}")
            print(f"应用Key: {app.get('appkey')}")
            print(f"平台: {app.get('platform')}")
            print(f"异常类型: {type_text}")
            print(f"异常日期: {outlier.get('ds')}")
            print(f"今日活跃: {app.get('todayActiveUser', 'N/A')}")
            print(f"今日新增: {app.get('todayNewUser', 'N/A')}")
            print("-" * 50)
    else:
        print("✓ 昨天所有应用均正常，未发现异常。")


def format_inspection_summary(response):
    """Format inspection summary response for display."""
    if response.get('code') != 200:
        print(f"Error: {response.get('msg', 'Unknown error')}")
        return

    data = response.get('data', {})
    summary = data.get('eventSummary', {})
    metas = data.get('metas', [])

    print("智能巡检摘要：")
    print(f"  正常事件数: {summary.get('normal', 0)}")
    print(f"  暂停计算事件数: {summary.get('stopped', 0)}")
    print(f"  未注册时间数: {summary.get('unReg', 0)}")
    print()

    if metas:
        print("埋点异常上报（最近30天）：")
        client = UAppOutlierClient()
        for meta in metas:
            err_code = meta.get('err_code')
            error_count = meta.get('error_count')
            description = client.translate_error_code(err_code)
            print(f"  错误码 {err_code}: {description}")
            print(f"  错误次数: {error_count}")
            print()

    no_quota = data.get('noEventQuotaAppNames', [])
    if no_quota:
        print("没有事件额度的应用：")
        for name in no_quota:
            print(f"  - {name}")
        print()


def main():
    """Main entry point for CLI."""
    import argparse

    parser = argparse.ArgumentParser(description='UApp Outlier Detection Helper')
    parser.add_argument('--ak', help='API Key')
    parser.add_argument('--sk', help='API Security Token')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Report command
    report_parser = subparsers.add_parser('report', help='Get outlier report for specific app')
    report_parser.add_argument('--app', required=True, help='Application key or app name')
    report_parser.add_argument('--date', required=True, help='Date in yyyyMMdd format')

    # Yesterday command
    subparsers.add_parser('yesterday', help='Get yesterday\'s outliers')

    # Inspection command
    subparsers.add_parser('inspection', help='Get intelligent inspection summary')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        client = UAppOutlierClient(ak=args.ak, sk=args.sk)

        if args.command == 'report':
            response = client.get_outlier_report(args.app, args.date)
            format_outlier_report(response)

        elif args.command == 'yesterday':
            response = client.get_yesterday_outliers()
            format_yesterday_outliers(response)

        elif args.command == 'inspection':
            response = client.get_inspection_summary()
            format_inspection_summary(response)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
