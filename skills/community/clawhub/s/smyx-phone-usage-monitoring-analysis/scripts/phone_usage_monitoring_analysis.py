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


def analyze_video(input_path=None, url=None, detection_type=None, work_area=None, api_url=None, api_key=None,
                  output_level=None):
    """调用API分析玩手机行为监测视频"""
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


def format_result(result, output_level="standard", detection_type="video", work_area="other"):
    """格式化输出结果"""
    detection_type_map = {
        "video": "视频流检测",
        "image": "图片静态检测"
    }
    work_area_map = {
        "open-office": "开放办公区",
        "cubicle": "独立工位",
        "meeting-room": "会议室",
        "other": "其他区域"
    }
    detection_type_cn = detection_type_map.get(detection_type, detection_type)
    work_area_cn = work_area_map.get(work_area, work_area)

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('phoneUsageResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 职畅卫士办公行为分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        return f"""
📊 职畅卫士玩手机监测报告
{'=' * 40}
检测类型: {detection_type_cn}
监测区域: {work_area_cn}
整体合规状况: {diagnosis.get('overall_compliance', '未知')}
主要问题: {diagnosis.get('total_phone_usage_count', 0)} 次玩手机行为，累计 {diagnosis.get('total_phone_usage_duration', 0)} 秒
效率提示: {data.get('efficiency_warnings', ['无特殊警示'])[0] if data.get('efficiency_warnings') else '无特殊警示'}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        person_detection = data.get('person_detection', {})

        behavior_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('phone_usage_behavior', {}).items()])
        duration_analysis = "\n".join([f"  {k}: {v} 秒" for k, v in diagnosis.get('usage_duration', {}).items()])
        area_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('area_compliance', {}).items()])
        warnings = "\n".join([f"  ⚠️  {item}" for item in data.get('efficiency_warnings', [])])
        suggestions = "\n".join([f"  💡 {item}" for item in data.get('improvement_suggestions', [])])

        return f"""
📊 职畅卫士玩手机行为监测报告
{'=' * 50}
⏰ 分析时间: {data.get('analysis_time', '未知')}
📹 检测类型: {detection_type_cn}
🏢 监测区域: {work_area_cn}
🎯 人员检测: {person_detection.get('status', '未知')} (置信度: {person_detection.get('quality_score', 0)}分)

🔍 监测结果:
  整体合规评分: {diagnosis.get('compliance_score', '未知')}
  整体状况: {diagnosis.get('overall_compliance', '未知')}
  检测到玩手机次数: {diagnosis.get('total_phone_usage_count', 0)} 次
  累计玩手机时长: {diagnosis.get('total_phone_usage_duration', 0)} 秒

  玩手机行为识别:
{behavior_analysis}

  时长分段统计:
{duration_analysis}

  各区域合规评估:
{area_analysis}

⚠️ 效率风险预警:
{warnings}

💡 工作效率提升建议:
{suggestions}
{'=' * 50}
> 注：本报告仅供企业内部管理参考，请遵守相关劳动法律法规，保护员工合法权益。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="职场玩手机行为监测分析工具")
    parser.add_argument("--input", help="本地视频/图片文件路径")
    parser.add_argument("--url", help="网络视频/图片URL地址")
    parser.add_argument("--detection-type", choices=["video", "image"], default=ConstantEnum.DEFAULT__DETECTION_TYPE,
                        help="检测类型：video(视频流检测), image(图片静态检测)，默认 video")
    parser.add_argument("--work-area", choices=["open-office", "cubicle", "meeting-room", "other"],
                        default=ConstantEnum.DEFAULT__WORK_AREA,
                        help="工作区域类型：open-office(开放办公区), cubicle(独立工位), meeting-room(会议室), other(其他)，默认 other")
    parser.add_argument("--open-id", required=True, help="当前用户/企业的OpenID/UserId/用户名/手机号")
    parser.add_argument("--list", action='store_true', help="显示玩手机行为监测分析列表清单")
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

        print("🔍 正在分析办公行为，请稍候...")
        output_content = analyze_video(
            input_path=args.input,
            url=args.url,
            detection_type=args.detection_type,
            work_area=args.work_area,
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
        print(f"❌ 玩手机行为监测分析失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
