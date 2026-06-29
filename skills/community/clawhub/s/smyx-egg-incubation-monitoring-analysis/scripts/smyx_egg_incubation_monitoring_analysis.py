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


def analyze_video(input_path=None, url=None, pet_type=None, api_url=None, api_key=None, output_level=None):
    if pet_type:
        ConstantEnum.DEFAULT__PET_TYPE = pet_type

    input_path = input_path or url
    return skill.get_output_analysis(input_path)


def show_analyze_list(open_id, start_time=None, end_time=None):
    output_content = skill.get_output_analysis_list(open_id=open_id)
    return output_content


def main():
    parser = argparse.ArgumentParser(description="孵化箱内龟蛋/蛇蛋发育监测工具")
    parser.add_argument("--input",
                        help="本地孵化箱内龟蛋/蛇蛋微距高清图像或视频文件路径（建议侧向透光照蛋/微距俯拍，分辨率≥1080p）")
    parser.add_argument("--url", help="网络龟蛋/蛇蛋微距高清图像/视频URL")
    parser.add_argument("--pet-type", choices=["cat", "dog", "other"], default=ConstantEnum.DEFAULT__PET_TYPE,
                        help="类别标识：龟蛋/蛇蛋孵化场景默认 other")
    parser.add_argument("--open-id", required=True,
                        help="当前用户的OpenID/UserId/用户名/手机号（繁殖者/繁殖场/家庭爱好者授权）")
    parser.add_argument("--list", action='store_true', help="显示孵化进度历史记录清单")
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
            ConstantEnumBase.CURRENT__OPEN_ID = args.open_id

        if args.list:
            open_id = ConstantEnum.CURRENT__OPEN_ID
            result = show_analyze_list(open_id)
            print(result)
            exit(0)

        if not args.input and not args.url:
            print("❌ 错误: 必须提供 --input 或 --url 参数")
            exit(1)

        print("🔍 正在分析孵化箱内龟蛋/蛇蛋：蛋壳颜色/血管网络/血丝/胚胎黑影/受精状态/发育阶段，请稍候...")
        output_content = analyze_video(
            input_path=args.input,
            url=args.url,
            pet_type=args.pet_type,
            api_url=args.api_url,
            api_key=args.api_key,
            output_level=args.detail
        )

        print(output_content)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                if args.detail == "full":
                    json.dump(result, f, ensure_ascii=False, indent=2)
                else:
                    f.write(output_content)
            print(f"✅ 结果已保存到: {args.output}")

    except Exception as e:
        traceback.print_stack()
        print(f"❌ 孵化箱内龟蛋/蛇蛋发育监测失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
