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

# 从config导入常量
SUPPORTED_FORMATS = ConstantEnum.SUPPORTED_FORMATS
MAX_FILE_SIZE_MB = ConstantEnum.MAX_FILE_SIZE_MB


def validate_file(file_path):
    """验证输入文件是否合法"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"文件没有读权限: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()[1:]
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"不支持的文件格式，支持的格式: {', '.join(SUPPORTED_FORMATS)}")

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"文件过大，最大支持 {MAX_FILE_SIZE_MB}MB，当前文件大小: {file_size_mb:.1f}MB")

    return True


def analyze_video(input_path=None, url=None, detection_region=None, api_url=None, api_key=None, output_level=None):
    """调用API进行人形检测"""
    if not input_path and not url:
        raise ValueError("必须提供本地视频路径(--input)或网络视频URL(--url)")

    try:
        input_path = input_path or url
        # 携带检测区域参数
        params = {}
        if detection_region:
            params["detection_region"] = detection_region
        return skill.get_output_analysis(input_path, params)

    except requests.exceptions.RequestException as e:
        traceback.print_stack()
        raise Exception(f"API请求失败: {str(e)}")


def show_analyze_list(open_id, start_time=None, end_time=None):
    # if not open_id:
    #     raise ValueError("必须提供本用户的OpenId/UserId")

    try:
        output_content = skill.get_output_analysis_list()
        return output_content

    except requests.exceptions.RequestException as e:
        traceback.print_stack()
        raise Exception(f"API请求失败: {str(e)}")


def get_analysis_export_url(request_id=None):
    """调用API分析视频"""
    if not request_id:
        return ""
    return ApiEnum.DETAIL_EXPORT_URL + request_id


def format_result(result, output_level="standard", detection_region=None):
    """格式化输出结果"""

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('humanDetectionResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 人形检测分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        detection = data.get('detection', {})
        return f"""
📊 人形检测报告
{'=' * 40}
检测到人数: {detection.get('human_count', 0)}
出现频次: {detection.get('appear_count', 0)} 次
是否有入侵: {'⚠️ 是' if detection.get('has_intrusion') else '✅ 否'}
预警提示: {data.get('alert_message', ['无特殊提示'])[0] if data.get('alert_message') else '无特殊提示'}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        detection = data.get('detection', {})

        regions_analysis = "\n".join(
            [f"  📍 区域 {idx + 1}: 检测到 {item.get('human_count', 0)} 人，置信度 {item.get('confidence', 0)}" for
             idx, item in enumerate(detection.get('regions', []))])
        warnings = "\n".join([f"  ⚠️  {item}" for item in data.get('alert_messages', [])])

        detection_region_info = ""
        if detection_region:
            detection_region_info = f"\n🎯 指定检测区域: {detection_region}"

        return f"""
📊 区域人形检测分析报告
{'=' * 50}
⏰ 检测时间: {data.get('detection_time', '未知')}
{detection_region_info}

🔍 检测结果:
  检测到总人数: {detection.get('total_human_count', 0)}
  人员出现总频次: {detection.get('total_appear_count', 0)}
  是否检测到人员: {'✅ 是' if detection.get('has_human') else '❌ 否'}
  是否存在入侵: {'⚠️ 是' if detection.get('has_intrusion') else '✅ 否'}

  各区域检测详情:
{regions_analysis if regions_analysis else '  无区域信息'}

⚠️ 入侵预警提示:
{warnings if warnings else '  无入侵预警'}
{'=' * 50}
> 注：本报告仅供安全管理参考，具体处置请按单位相关规定执行。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="区域人形检测工具")
    parser.add_argument("--input", help="本地视频文件路径")
    parser.add_argument("--url", help="网络视频的URL地址")
    parser.add_argument("--detection-region", help="限定检测区域，格式：x1,y1,x2,y2")
    parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    parser.add_argument("--list", action='store_true', help="显示人形检测分析列表清单")
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

        print("🔍 正在进行人形检测，请稍候...")
        output_content = analyze_video(
            input_path=args.input,
            url=args.url,
            detection_region=args.detection_region,
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
        print(f"❌ 人形检测分析失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
