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


def analyze_video(input_path=None, url=None, user_type=None, detection_mode=None, api_url=None, api_key=None,
                  output_level=None):
    """调用API分析失禁状态监测视频"""
    if not input_path and not url:
        raise ValueError("必须提供本地文件路径(--input)或网络URL(--url)")

    # 设置护理对象类型参数
    if user_type:
        ConstantEnum.DEFAULT__USER_TYPE = user_type

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


def format_result(result, output_level="standard", user_type="other", detection_mode="real-time"):
    """格式化输出结果"""
    user_type_map = {
        "elderly": "失能老人",
        "bedridden": "卧床病人",
        "infant": "婴幼儿",
        "other": "其他"
    };
    detection_mode_map = {
        "real-time": "实时监控",
        "regular-check": "定时巡查"
    };
    user_type_cn = user_type_map.get(user_type, user_type)
    detection_mode_cn = detection_mode_map.get(detection_mode, detection_mode)

    alert_level_map = {
        "normal": "🟢 正常",
        "warning": "🟡 需要关注",
        "alert": "🟠 需要处理",
        "emergency": "🔴 需要立即处理"
    };

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('incontinenceAlertResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 护安卫士失禁提醒分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        alert_level = diagnosis.get('alert_level', 'normal')
        return f"""
📊 护安卫士失禁状态提醒报告
{'=' * 40}
护理对象: {user_type_cn}
检测模式: {detection_mode_cn}
衣物潮湿检测: {diagnosis.get('damp_clothing', '未检测到')}
预警等级: {alert_level_map.get(alert_level, alert_level)}
护理提示: {data.get('care_warnings', ['无特殊警示'])[0] if data.get('care_warnings') else '无特殊警示'}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        person_detection = data.get('person_detection', {})

        clothing_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('clothing_condition', {}).items()])
        area_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('detection_area', {}).items()])
        warnings = "\n".join([f"  ⚠️  {item}" for item in data.get('care_warnings', [])])
        suggestions = "\n".join([f"  💡 {item}" for item in data.get('care_suggestions', [])])

        alert_level = diagnosis.get('alert_level', 'normal')
        alert_level_cn = alert_level_map.get(alert_level, alert_level)

        return f"""
📊 护安卫士智能失禁状态提醒报告
{'=' * 50}
⏰ 分析时间: {data.get('analysis_time', '未知')}
👤 护理对象: {user_type_cn}
📹 检测模式: {detection_mode_cn}
🎯 对象检测: {person_detection.get('status', '未知')} (置信度: {person_detection.get('quality_score', 0)}分)

🔍 监测结果:
  整体状况评分: {diagnosis.get('health_score', '未知')}
  预警等级: {alert_level_cn}

  衣物状态检查:
{clothing_analysis}

  检测区域评估:
{area_analysis}

  检测结果:
  衣物潮湿: {diagnosis.get('damp_clothing', '否')}
  排泄异常: {diagnosis.get('excretion_detected', '否')}
  需要更换护理用品: {diagnosis.get('need_change', '否')}

⚠️ 护理警示:
{warnings}

💡 清洁护理建议:
{suggestions}
{'=' * 50}
> 注：本报告仅供护理参考，不能替代专业医护人员判断和人工检查。请及时进行人工确认。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="智能失禁状态提醒分析工具")
    parser.add_argument("--input", help="本地视频/图片文件路径")
    parser.add_argument("--url", help="网络视频/图片URL地址")
    parser.add_argument("--user-type", choices=["elderly", "bedridden", "infant", "other"],
                        default=ConstantEnum.DEFAULT__USER_TYPE,
                        help="护理对象类型：elderly(失能老人), bedridden(卧床病人), infant(婴幼儿), other(其他)，默认 other")
    parser.add_argument("--detection-mode", choices=["real-time", "regular-check"],
                        default=ConstantEnum.DEFAULT__DETECTION_MODE,
                        help="检测模式：real-time(实时监控), regular-check(定时巡查)，默认 real-time")
    parser.add_argument("--open-id", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--list", action='store_true', help="显示失禁状态提醒分析列表清单")
    parser.add_argument("--api-url", help="服务端API地址")
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

        print("🔍 正在分析失禁状态，请稍候...")
        output_content = analyze_video(
            input_path=args.input,
            url=args.url,
            user_type=args.user_type,
            detection_mode=args.detection_mode,
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
        print(f"❌ 失禁状态检测分析失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
