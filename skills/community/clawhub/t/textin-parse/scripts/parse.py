#!/usr/bin/env python3
"""
Textin 文档解析 Python 客户端
"""

import argparse
import json
import os
import sys
import requests

CONFIG_FILE = os.path.expanduser("~/.openclaw/textin-config.json")
API_URL = "https://api.textin.com/ai/service/v1/pdf_to_markdown"


def load_config():
    """加载配置"""
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(app_id: str, secret_code: str):
    """保存配置"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    config = {"app_id": app_id, "secret_code": secret_code}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print("✅ 凭证已保存")


def parse_document(
    file_path: str,
    app_id: str,
    secret_code: str,
    **kwargs
) -> dict:
    """解析文档"""
    # 判断是 URL 还是本地文件
    is_url = file_path.startswith(("http://", "https://"))
    
    params = {
        "parse_mode": kwargs.get("parse_mode", "scan"),
        "table_flavor": kwargs.get("table_flavor", "html"),
        "get_image": kwargs.get("get_image", "objects"),
        "apply_document_tree": kwargs.get("apply_document_tree", 1),
        "formula_level": kwargs.get("formula_level", 0),
        "remove_watermark": kwargs.get("remove_watermark", 0),
        "apply_chart": kwargs.get("apply_chart", 0),
        "markdown_details": kwargs.get("markdown_details", 1),
        "page_details": kwargs.get("page_details", 1),
        "get_excel": kwargs.get("get_excel", 0),
        "crop_dewarp": kwargs.get("crop_dewarp", 0),
    }
    
    # 添加可选参数
    optional_params = [
        "page_start", "page_count", "pdf_pwd", "dpi", "paratext_mode",
        "underline_level", "apply_merge", "apply_image_analysis",
        "raw_ocr", "char_details", "catalog_details", "image_output_type"
    ]
    for p in optional_params:
        if p in kwargs and kwargs[p] is not None:
            params[p] = kwargs[p]
    
    headers = {
        "x-ti-app-id": app_id,
        "x-ti-secret-code": secret_code,
    }
    
    if is_url:
        headers["Content-Type"] = "text/plain"
        response = requests.post(API_URL, params=params, headers=headers, data=file_path.encode())
    else:
        headers["Content-Type"] = "application/octet-stream"
        with open(file_path, "rb") as f:
            response = requests.post(API_URL, params=params, headers=headers, data=f)
    
    result = response.json()
    
    if result.get("code") == 200:
        return result.get("result", {})
    else:
        raise Exception(f"Error {result.get('code')}: {result.get('message')}")


def main():
    parser = argparse.ArgumentParser(description="Textin 文档解析工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # config 子命令
    config_parser = subparsers.add_parser("config", help="配置管理")
    config_parser.add_argument("--save", nargs=2, metavar=("APP_ID", "SECRET"), help="保存凭证")
    config_parser.add_argument("--show", action="store_true", help="显示当前配置")
    
    # parse 子命令
    parse_parser = subparsers.add_parser("parse", help="解析文档")
    parse_parser.add_argument("file", help="文件路径或 URL")
    parse_parser.add_argument("--parse-mode", choices=["auto", "scan", "lite", "parse", "vlm"], default="scan")
    parse_parser.add_argument("--table-flavor", choices=["html", "md", "none"], default="html")
    parse_parser.add_argument("--get-image", choices=["none", "page", "objects", "both"], default="objects")
    parse_parser.add_argument("--apply-document-tree", type=int, choices=[0, 1], default=1)
    parse_parser.add_argument("--formula-level", type=int, choices=[0, 1, 2], default=0)
    parse_parser.add_argument("--remove-watermark", type=int, choices=[0, 1], default=0)
    parse_parser.add_argument("--apply-chart", type=int, choices=[0, 1], default=0)
    parse_parser.add_argument("--markdown-details", type=int, choices=[0, 1], default=1)
    parse_parser.add_argument("--page-details", type=int, choices=[0, 1], default=1)
    parse_parser.add_argument("--get-excel", type=int, choices=[0, 1], default=0)
    parse_parser.add_argument("--crop-dewarp", type=int, choices=[0, 1], default=0)
    parse_parser.add_argument("--page-start", type=int)
    parse_parser.add_argument("--page-count", type=int)
    parse_parser.add_argument("--pdf-pwd")
    parse_parser.add_argument("--dpi", type=int, choices=[72, 144, 216])
    parse_parser.add_argument("--output", "-o", help="输出文件路径")
    parse_parser.add_argument("--full", action="store_true", help="输出完整结果（不只是 markdown）")
    
    args = parser.parse_args()
    
    if args.command == "config":
        if args.save:
            save_config(args.save[0], args.save[1])
        elif args.show:
            config = load_config()
            if config:
                print(json.dumps(config, indent=2))
            else:
                print("未配置凭证")
        else:
            parser.print_help()
    
    elif args.command == "parse":
        config = load_config()
        if not config:
            print("❌ 请先配置 API 凭证")
            print("用法: textin-parse config --save <APP_ID> <SECRET>")
            sys.exit(1)
        
        try:
            # 提取参数
            params = {k: v for k, v in vars(args).items() 
                     if k not in ["command", "file", "output", "full"] and v is not None}
            
            result = parse_document(args.file, config["app_id"], config["secret_code"], **params)
            
            if args.full:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(result.get("markdown", ""))
            
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"\n✅ 完整结果已保存到 {args.output}")
                
        except Exception as e:
            print(f"❌ {e}")
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()