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


def analyze_media(input_path=None, url=None, media_type=None, threshold=None, enroll=None, person_name=None,
                  person_id=None, api_url=None, api_key=None, output_level=None):
    """调用API进行陌生人识别/底库录入"""
    if not input_path and not url:
        raise ValueError("必须提供本地媒体路径(--input)或网络媒体URL(--url)")

    # 设置参数
    if media_type:
        ConstantEnum.DEFAULT_MEDIA_TYPE = media_type
    if threshold:
        ConstantEnum.DEFAULT_THRESHOLD = threshold
    if enroll:
        ConstantEnum.DEFAULT_ENROLL = enroll

    try:
        input_path = input_path or url
        # 携带额外参数
        params = {}
        if threshold:
            params["threshold"] = threshold
        if enroll:
            params["enroll"] = enroll
        if person_name:
            params["person_name"] = person_name
        if person_id:
            params["person_id"] = person_id
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


def format_result(result, output_level="standard", media_type="video", threshold=0.6, enroll="no"):
    """格式化输出结果"""
    # 底库录入结果特殊处理
    if enroll == "yes":
        if output_level == "json":
            result_id = None
            if result is not None:
                result_json = result
                result_id = result_json.get('id', {})
                result_json = json.dumps(result_json.get('enrollResponse', {}), ensure_ascii=False, indent=2)
            else:
                return "⚠️ 暂无录入结果"
            return f"""
📊 人脸识别底库录入结构化结果
{result_json}
""", result_id
        elif output_level == "basic":
            data = result.get('data', {})
            return f"""
📊 人脸识别底库录入结果
{'=' * 40}
操作类型: 底库录入
录入状态: {data.get('status', '未知')}
提示信息: {data.get('message', '无提示信息')}
        """
        elif output_level == "standard":
            data = result.get('data', {})
            return f"""
📊 人脸识别底库录入结果
{'=' * 50}
⏰ 操作时间: {data.get('operation_time', '未知')}
🎯 操作类型: 底库录入
👤 录入人员: {data.get('person_name', '未知')}
✅ 录入状态: {data.get('status', '未知')}
💬 提示信息: {data.get('message', '无提示信息')}
{'=' * 50}
> 注：录入成功后即可在陌生人识别中使用该底库进行比对。
        """
        else:
            return json.dumps(result, ensure_ascii=False, indent=2)

    # 陌生人识别结果
    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('strangerRecognitionResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 陌生人识别分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        recognition = data.get('recognition', {})
        known_count = recognition.get('known_person_count', 0)
        stranger_count = recognition.get('stranger_count', 0)
        return f"""
📊 陌生人识别报告
{'=' * 40}
比对阈值: {threshold}
已知人员: {known_count} 人
陌生人员: {stranger_count} 人
预警提示: {data.get('alert_message', ['无特殊提示'])[0] if data.get('alert_message') else '无特殊提示'}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        recognition = data.get('recognition', {})

        known_persons = "\n".join(
            [f"  ✅  {idx + 1}. {p.get('person_name')} - 相似度: {p.get('similarity')}" for idx, p in
             enumerate(recognition.get('known_persons', []))])
        strangers = "\n".join([f"  ⚠️  陌生人 {idx + 1} - 最高相似度: {p.get('max_similarity')}" for idx, p in
                               enumerate(recognition.get('strangers', []))])
        warnings = "\n".join([f"  ⚠️  {item}" for item in data.get('alert_messages', [])])

        return f"""
📊 陌生人识别分析报告
{'=' * 50}
⏰ 识别时间: {data.get('recognition_time', '未知')}
📹 素材类型: {media_type}
🎯 比对阈值: {threshold}

🔍 识别结果:
  检测到人脸总数: {recognition.get('total_face_count', 0)}
  已知人员数量: {recognition.get('known_person_count', 0)}
  陌生人员数量: {recognition.get('stranger_count', 0)}
  是否存在陌生人: {'⚠️ 是' if recognition.get('has_stranger') else '✅ 否'}

  已知人员识别结果:
{known_persons if known_persons else '  未识别到已知人员'}

  陌生人识别结果:
{strangers if strangers else '  未检测到陌生人'}

⚠️ 陌生人预警提示:
{warnings if warnings else '  无陌生人预警'}
{'=' * 50}
> 注：本报告仅供安全管理参考，具体处置请按单位相关规定执行。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="陌生人识别工具")
    parser.add_argument("--input", help="本地视频/图片文件路径")
    parser.add_argument("--url", help="网络视频/图片的URL地址")
    parser.add_argument("--media-type", choices=["video", "image"], default=ConstantEnum.DEFAULT__MEDIA_TYPE,
                        help="媒体类型：video(视频流/视频文件), image(图片)，默认 video")
    parser.add_argument("--threshold", type=float, default=ConstantEnum.DEFAULT__THRESHOLD,
                        help="人脸比对相似度阈值，默认 0.6")
    parser.add_argument("--enroll", choices=["yes", "no"], default=ConstantEnum.DEFAULT__ENROLL,
                        help="是否录入新人脸到人脸识别底库，yes/no，默认 no")
    parser.add_argument("--person-name", help="人员姓名，底库录入(--enroll yes)时必须提供")
    parser.add_argument("--person-id", help="人员ID，底库录入时可选")
    parser.add_argument("--open-id", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--list", action='store_true', help="显示陌生人识别分析列表清单")
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

        # 底库录入检查人员姓名
        if args.enroll == "yes" and not args.person_name:
            print("❌ 错误: 底库录入操作(--enroll yes)必须提供 --person-name 参数")
            exit(1)

        # 检查必需参数
        if not args.input and not args.url:
            print("❌ 错误: 必须提供 --input 或 --url 参数")
            exit(1)

        print("🔍 正在进行陌生人识别，请稍候...")
        output_content = analyze_media(
            input_path=args.input,
            url=args.url,
            media_type=args.media_type,
            threshold=args.threshold,
            enroll=args.enroll,
            person_name=args.person_name,
            person_id=args.person_id,
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
        print(f"❌ 陌生人识别失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
