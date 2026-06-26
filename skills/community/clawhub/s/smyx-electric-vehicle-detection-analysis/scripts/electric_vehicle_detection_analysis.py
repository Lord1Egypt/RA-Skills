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

from skills.smyx_common.scripts.util import RequestUtil, OpenIdUtil

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


def analyze_video(input_path=None, url=None, detection_type=None, area_type=None, api_url=None, api_key=None,
                  output_level=None):
    """调用API分析电动车检测视频"""
    if not input_path and not url:
        raise ValueError("必须提供本地文件路径(--input)或网络URL(--url)")

    # 设置检测类型参数
    if detection_type:
        ConstantEnum.DEFAULT__DETECTION_TYPE = detection_type

    try:
        input_path = input_path or url
        return skill.get_output_analysis(input_path)

    except requests.exceptions.RequestException as e:
        traceback.print_stack()
        raise Exception(f"API请求失败: {str(e)}")


def show_analyze_list(open_id, start_time=None, end_time=None):
    try:
        output_content = skill.get_output_analysis_list(open_id=open_id)
        return output_content

    except requests.exceptions.RequestException as e:
        traceback.print_stack()
        raise Exception(f"API请求失败: {str(e)}")


def get_analysis_export_url(request_id=None):
    """调用API分析视频"""
    if not request_id:
        return ""
    return ApiEnum.DETAIL_EXPORT_URL + request_id


def format_result(result, output_level="standard", detection_type="video", area_type="other"):
    """格式化输出结果"""
    detection_type_map = {
        "video": "视频流检测",
        "image": "图片静态检测"
    };
    area_type_map = {
        "parking-lot": "停车场",
        "community": "社区园区",
        "campus": "校园单位",
        "road": "禁行道路",
        "other": "其他区域"
    };
    detection_type_cn = detection_type_map.get(detection_type, detection_type)
    area_type_cn = area_type_map.get(area_type, area_type)

    violation_level_map = {
        "normal": "🟢 无违规",
        "mild": "🟡 轻度违规",
        "moderate": "🟠 中度违规",
        "severe": "🔴 严重违规"
    };

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('evDetectionResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 安管卫士电动车检测分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        violation_level = diagnosis.get('violation_level', 'normal')
        return f"""
📊 安管卫士电动车检测报告
{'=' * 40}
检测类型: {detection_type_cn}
禁行区域: {area_type_cn}
检测到电动车数量: {diagnosis.get('total_ev_count', 0)} 辆
违规等级: {violation_level_map.get(violation_level, violation_level)}
管理提示: {data.get('management_warnings', ['无特殊警示'])[0] if data.get('management_warnings') else '无特殊警示'}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        area_detection = data.get('area_detection', {})

        vehicle_analysis = "\n".join([f"  {k}: {v} 辆" for k, v in diagnosis.get('vehicle_counts', {}).items()])
        violation_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('violation_assessment', {}).items()])
        warnings = "\n".join([f"  ⚠️  {item}" for item in data.get('management_warnings', [])])
        suggestions = "\n".join([f"  💡 {item}" for item in data.get('management_suggestions', [])])

        violation_level = diagnosis.get('violation_level', 'normal')
        violation_level_cn = violation_level_map.get(violation_level, violation_level)

        return f"""
📊 安管卫士智能电动车检测报告
{'=' * 50}
⏰ 分析时间: {data.get('analysis_time', '未知')}
📹 检测类型: {detection_type_cn}
🚧 禁行区域类型: {area_type_cn}
🎯 区域检测: {area_detection.get('status', '未知')} (置信度: {area_detection.get('quality_score', 0)}分)

🔍 检测结果:
  整体风险评分: {diagnosis.get('risk_score', '未知')}
  违规等级: {violation_level_cn}

  车辆统计:
{vehicle_analysis}

  违规评估:
{violation_analysis}

  汇总统计:
  检测到电动车总量: {diagnosis.get('total_ev_count', 0)} 辆
  违规停放电动车: {diagnosis.get('illegal_parking_count', 0)} 辆
  违规行驶电动车: {diagnosis.get('illegal_driving_count', 0)} 辆
  平均密度: {diagnosis.get('average_density_per_frame', 0)} 辆/帧

⚠️ 管理警示:
{warnings}

💡 处理建议:
{suggestions}
{'=' * 50}
> 注：本报告仅供安全管理参考，请结合人工复核确认违规事实。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="电动车智能检测分析工具")
    parser.add_argument("--input", help="本地视频/图片文件路径")
    parser.add_argument("--url", help="网络视频/图片URL地址")
    parser.add_argument("--detection-type", choices=["video", "image"], default=ConstantEnum.DEFAULT__DETECTION_TYPE,
                        help="检测类型：video(视频流检测), image(图片静态检测)，默认 video")
    parser.add_argument("--area-type", choices=["parking-lot", "community", "campus", "road", "other"],
                        default=ConstantEnum.DEFAULT__AREA_TYPE,
                        help="禁行区域类型：parking-lot(停车场), community(社区园区), campus(校园单位), road(禁行道路), other(其他)，默认 other")
    # 内部兼容参数：不在 --help 中展示，不要求用户输入。
    parser.add_argument("--open-id", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--list", action='store_true', help="显示电动车检测分析列表清单")
    parser.add_argument("--api-url", help="服务端API地址")
    # 内部兼容参数：不在 --help 中展示，不要求用户输入。
    parser.add_argument("--api-key", help=argparse.SUPPRESS)
    parser.add_argument("--output", help="结果输出文件路径")
    parser.add_argument("--detail", choices=["basic", "standard", "json"],
                        default=ConstantEnum.DEFAULT__OUTPUT_LEVEL,
                        help="输出详细程度")
    parser.add_argument("--export-env-only", action='store_true',
                        help="仅输出 export 命令设置环境变量，不执行分析")

    args = parser.parse_args()

    try:
        # 初始化内部用户身份；不要求用户输入，也不在帮助信息中展示。
        OpenIdUtil.resolve_current_open_id(args.open_id, use_current=bool(args.open_id))

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

        print("🔍 正在分析电动车检测，请稍候...")
        output_content = analyze_video(
            input_path=args.input,
            url=args.url,
            detection_type=args.detection_type,
            area_type=args.area_type,
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
        print(f"❌ 电动车检测分析失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
