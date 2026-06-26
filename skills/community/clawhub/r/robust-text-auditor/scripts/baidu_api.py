# 文件名：baidu_api.py
# 描述：封装了百度智能云文本和图像审核的接口调用（V2 - Secure & Portable）

import argparse
import base64
import json
import os
import sys
from typing import Dict, Optional
from pathlib import Path
import requests
import io

# 强制 stdout 使用 UTF-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- 全局配置 (V2 - Dynamic) ---
TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
TEXT_CENSOR_URL = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
IMAGE_CENSOR_URL = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined"

def get_config_value(key: str, default: Optional[str] = None) -> Optional[str]:
    """从 ~/.openclaw/config.json 安全地读取配置值"""
    config_path = Path.home() / '.openclaw' / 'config.json'
    if not config_path.exists():
        return default
    try:
        config = json.loads(config_path.read_text(encoding='utf-8'))
        return config.get(key, default)
    except (json.JSONDecodeError, IOError):
        return default

class BaiduApi:
    def __init__(self):
        self.api_key, self.secret_key = self._load_credentials()
        self.access_token = self._get_access_token()

    def _load_credentials(self) -> tuple:
        """从主配置文件加载 API Key 和 Secret Key"""
        api_key = get_config_value("baidu_api_key")
        secret_key = get_config_value("baidu_secret_key")
        if not api_key or not secret_key:
            raise ValueError("错误：主配置 ~/.openclaw/config.json 中未设置 'baidu_api_key' 或 'baidu_secret_key'。")
        return api_key, secret_key

    def _get_access_token(self) -> str:
        """获取百度云 access_token"""
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        try:
            response = requests.post(TOKEN_URL, params=params, timeout=10)
            response.raise_for_status()
            token_data = response.json()
            if "access_token" not in token_data:
                error_desc = token_data.get('error_description', '未知错误')
                raise ValueError(f"获取 access_token 失败：{error_desc}")
            return token_data["access_token"]
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"获取 access_token 网络错误：{e}")

    def text_censor(self, text: str) -> Dict:
        """文本审核"""
        url = f"{TEXT_CENSOR_URL}?access_token={self.access_token}"
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        data = {"text": text}
        try:
            response = requests.post(url, data=data, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"文本审核请求网络错误：{e}")

    def image_censor(self, image_path: str) -> Dict:
        """图像审核（本地图片文件）"""
        url = f"{IMAGE_CENSOR_URL}?access_token={self.access_token}"
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        try:
            with open(image_path, 'rb') as f:
                img_base64 = base64.b64encode(f.read()).decode('utf-8')
            data = {"image": img_base64}
            response = requests.post(url, data=data, headers=headers, timeout=20)
            response.raise_for_status()
            return response.json()
        except FileNotFoundError:
            raise FileNotFoundError(f"图片文件不存在：{image_path}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"图像审核请求网络错误：{e}")


def main():
    parser = argparse.ArgumentParser(description="使用百度智能云 API 审核内容 (V2)。")
    subparsers = parser.add_subparsers(dest='command', required=True, help='子命令')

    # 文本审核子命令
    text_parser = subparsers.add_parser('text', help='审核文本内容')
    text_group = text_parser.add_mutually_exclusive_group(required=True)
    text_group.add_argument('--text', type=str, help='需要审核的文本字符串')
    text_group.add_argument('--file', type=str, help='需要审核的文本文件路径')

    # 图像审核子命令
    image_parser = subparsers.add_parser('image', help='审核图像文件')
    image_parser.add_argument('path', type=str, help='需要审核的本地图片路径')

    args = parser.parse_args()

    try:
        api_client = BaiduApi()

        if args.command == 'text':
            text_to_check = ""
            if args.file:
                with open(args.file, 'r', encoding='utf-8') as f:
                    text_to_check = f.read()
            elif args.text:
                text_to_check = args.text
            
            result = api_client.text_censor(text_to_check)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif args.command == 'image':
            result = api_client.image_censor(args.path)
            print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        error_output = {"error": str(e)}
        print(json.dumps(error_output, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
