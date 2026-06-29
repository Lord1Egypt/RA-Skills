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


def analyze_video(input_path=None, url=None, alert_threshold=None, api_url=None, api_key=None, output_level=None):
    """调用API进行儿童危险行为识别"""
    if not input_path and not url:
        raise ValueError("必须提供本地视频路径(--input)或网络视频URL(--url)")

    # 设置参数
    if alert_threshold:
        ConstantEnum.DEFAULT_ALERT_THRESHOLD = alert_threshold

    try:
        input_path = input_path or url
        # 携带额外参数
        params = {}
        if alert_threshold:
            params["alert_threshold"] = alert_threshold
        return skill.get_output_analysis(input_path, params)

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


def format_result(result, output_level="standard", alert_threshold=0.6):
    """格式化输出结果"""
    danger_map = {
        "climbing": "攀爬",
        "playing_with_fire": "玩火",
        "touch_power": "触碰电源",
        "window_danger": "窗边危险动作"
    }

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('dangerBehaviorResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 儿童危险行为识别分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        detection = data.get('detection', {})
        return f"""
📊 儿童危险行为识别报告
{'=' * 40}
预警阈值: {alert_threshold}
危险行为次数: {detection.get('total_danger_count', 0)}
是否存在高危行为: {'⚠️ 是' if detection.get('has_high_risk') else '✅ 否'}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        detection = data.get('detection', {})

        danger_stats = "\n".join([
            f"  ⚠️ {danger_map.get(d.get('behavior'), d.get('behavior'))}: {d.get('count', 0)} 次，最高置信度: {d.get('max_confidence', 0)}"
            for d in detection.get('danger_stats', [])])
        warnings = "\n".join([f"  🚨  {item}" for item in data.get('alert_messages', [])])

        return f"""
📊 儿童危险行为识别分析报告
{'=' * 50}
⏰ 识别时间: {data.get('detection_time', '未知')}
🚨 预警阈值: {alert_threshold}

🔍 识别结果:
  危险行为总次数: {detection.get('total_danger_count', 0)}
  是否存在高危行为: {'⚠️ 是' if detection.get('has_high_risk') else '✅ 否'}

  危险行为统计:
{danger_stats if danger_stats else '  ✅ 未检测到危险行为'}

🚨 危险预警提示:
{warnings if warnings else '  无危险预警'}
{'=' * 50}
> 注：本技能仅作儿童安全监护辅助，发现预警请立即确认现场情况。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="儿童危险行为识别工具")
    parser.add_argument("--input", help="本地视频文件路径")
    parser.add_argument("--url", help="网络视频的URL地址")
    parser.add_argument("--alert-threshold", type=float, default=ConstantEnum.DEFAULT__ALERT_THRESHOLD,
                        help="危险行为预警阈值，高于该分值发出预警，默认 0.6")
    parser.add_argument("--open-id", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--list", action='store_true', help="显示儿童危险行为识别列表清单")
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

        print("🔍 正在进行儿童危险行为识别，请稍候...")
        output_content = analyze_video(
            input_path=args.input,
            url=args.url,
            alert_threshold=args.alert_threshold,
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
        print(f"❌ 儿童危险行为识别失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
