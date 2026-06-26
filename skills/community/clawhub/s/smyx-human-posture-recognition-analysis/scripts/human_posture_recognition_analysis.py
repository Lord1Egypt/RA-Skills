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


def analyze_video(input_path=None, url=None, alert_fall=None, api_url=None, api_key=None, output_level=None):
    """调用API进行人体姿态识别"""
    if not input_path and not url:
        raise ValueError("必须提供本地视频路径(--input)或网络视频URL(--url)")

    # 设置参数
    if alert_fall:
        ConstantEnum.DEFAULT_ALERT_FALL = alert_fall

    try:
        input_path = input_path or url
        # 携带额外参数
        params = {}
        if alert_fall:
            params["alert_fall"] = alert_fall
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


def format_result(result, output_level="standard", alert_fall="yes"):
    """格式化输出结果"""
    posture_map = {
        "standing": "站立",
        "sitting": "坐姿",
        "lying": "躺卧",
        "bending": "弯腰",
        "raising_hand": "举手",
        "running": "奔跑",
        "falling": "摔倒",
        "abnormal": "异常姿态"
    }

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('postureRecognitionResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 人体姿态识别分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        recognition = data.get('recognition', {})
        fall_detected = recognition.get('fall_detected', False)
        return f"""
📊 人体姿态识别报告
{'=' * 40}
摔倒预警开启: {alert_fall}
检测到姿态种类: {len(recognition.get('postures', []))}
摔倒检测结果: {'⚠️ 检测到摔倒' if fall_detected else '✅ 未检测到摔倒'}
异常姿态次数: {recognition.get('abnormal_count', 0)}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        recognition = data.get('recognition', {})

        posture_stats = "\n".join(
            [f"  {posture_map.get(p.get('posture'), p.get('posture'))}: {p.get('count', 0)} 次" for p in
             recognition.get('posture_stats', [])])
        warnings = "\n".join([f"  ⚠️  {item}" for item in data.get('alert_messages', [])])

        fall_detected = recognition.get('fall_detected', False)
        fall_warning = "⚠️ 检测到摔倒，请及时确认!" if fall_detected and alert_fall == "yes" else "✅ 未检测到摔倒"

        return f"""
📊 人体姿态识别分析报告
{'=' * 50}
⏰ 识别时间: {data.get('recognition_time', '未知')}
🚨 摔倒预警: {alert_fall}

🔍 识别结果:
{fall_warning}
  异常姿态总次数: {recognition.get('total_abnormal_count', 0)}

  各类姿态统计:
{posture_stats if posture_stats else '  未识别到有效姿态'}

⚠️ 预警提示:
{warnings if warnings else '  无预警提示'}
{'=' * 50}
> 注：本报告仅供安全监测参考，紧急情况请及时处置。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="人体姿态识别工具")
    parser.add_argument("--input", help="本地视频文件路径")
    parser.add_argument("--url", help="网络视频的URL地址")
    parser.add_argument("--alert-fall", choices=["yes", "no"], default=ConstantEnum.DEFAULT__ALERT_FALL,
                        help="是否开启摔倒预警，yes/no，默认 yes")
    parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    parser.add_argument("--list", action='store_true', help="显示人体姿态识别列表清单")
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

        print("🔍 正在进行人体姿态识别，请稍候...")
        output_content = analyze_video(
            input_path=args.input,
            url=args.url,
            alert_fall=args.alert_fall,
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
        print(f"❌ 人体姿态识别失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
