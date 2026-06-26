#!/usr/bin/env python3
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, parent_dir)

import argparse
import json
import mimetypes
import traceback
from datetime import datetime

import requests
import sys
import os

from .config import *

from .skill import skill

from skills.smyx_common.scripts.util import RequestUtil


def search_video(input_path=None, url=None, text=None, api_url=None, api_key=None, output_level=None):
    input_path = input_path or url or text
    return skill.get_output_analysis(input_path)


def show_analyze_list(open_id, start_time=None, end_time=None):
    output_content = skill.get_output_analysis_list()
    return output_content


def main():
    parser = argparse.ArgumentParser(description="视频搜索/视频检索智能分析工具")
    parser.add_argument("--input", help="本地视频文件路径")
    parser.add_argument("--url", help="网络视频URL地址")
    parser.add_argument("--text", help="搜索目标/自然语言描述（说明要找什么内容）")
    parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    parser.add_argument("--list", action='store_true', help="显示视频搜索分析列表清单")
    parser.add_argument("--api-url", help="服务端API地址")
    parser.add_argument("--api-key", help="API访问密钥（必需）")
    parser.add_argument("--output", help="结果输出文件路径")
    parser.add_argument("--detail", choices=["basic", "standard", "json"],
                        default=ConstantEnum.DEFAULT__OUTPUT_LEVEL,
                        help="输出详细程度")
    parser.add_argument("--export-env-only", action='store_true',
                        help="仅输出 export 命令设置环境变量，不执行分析")

    args = parser.parse_args()

    try:
        if args.open_id:
            # 设置 Python 进程内的环境变量
            ConstantEnumBase.CURRENT__OPEN_ID = args.open_id

        # 检查必需参数
        if args.list:
            open_id = ConstantEnum.CURRENT__OPEN_ID
            result = show_analyze_list(open_id)
            print(result)
            exit(0)

        # 检查必需参数
        if not args.input and not args.url:
            print("❌ 错误: 必须提供 --input 或 --url 参数")
            exit(1)

        if not args.text:
            print("⚠️  提示：未提供搜索目标/描述，建议使用 --text 参数说明要找什么内容")

        print("🔍 正在智能搜索视频，请稍候...")
        output_content = search_video(
            input_path=args.input,
            url=args.url,
            text=args.text,
            api_url=args.api_url,
            api_key=args.api_key,
            output_level=args.detail
        )

        print(output_content)

        # 保存到文件
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                if args.detail == "full":
                    json.dump(result, f, ensure_ascii=False, indent=2)
                else:
                    f.write(output_content)
            print(f"✅ 结果已保存到: {args.output}")

    except Exception as e:
        traceback.print_stack()
        print(f"❌ 视频搜索分析失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
