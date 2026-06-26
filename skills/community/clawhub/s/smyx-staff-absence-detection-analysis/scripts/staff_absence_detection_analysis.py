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


def analyze_media(input_path=None, url=None, media_type=None, confidence_threshold=None, absence_threshold=None,
                  api_url=None, api_key=None,
                  output_level=None):
    """调用API进行人员离岗检测"""
    if not input_path and not url:
        raise ValueError("必须提供本地媒体路径(--input)或网络媒体URL(--url)")

    # 设置参数
    if media_type:
        ConstantEnum.DEFAULT__MEDIA_TYPE = media_type
    if confidence_threshold:
        ConstantEnum.DEFAULT__CONFIDENCE_THRESHOLD = confidence_threshold
    if absence_threshold:
        ConstantEnum.DEFAULT__ABSENCE_THRESHOLD = absence_threshold

    try:
        input_path = input_path or url
        # 携带额外参数
        params = {}
        if confidence_threshold:
            params["confidence_threshold"] = confidence_threshold
        if absence_threshold:
            params["absence_threshold"] = absence_threshold
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


def format_result(result, output_level="standard", media_type="video", confidence_threshold=0.5, absence_threshold=300):
    """格式化输出结果"""
    category_map = {
        "on_duty": "在岗",
        "leave_post": "异常离岗",
        "temporary_leave": "短暂离开"
    }

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('postDetectionResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 人员离岗监测分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        detection = data.get('detection', {})
        return f"""
📊 人员离岗监测报告
{'=' * 40}
监测区域在岗状态: {category_map.get(detection.get('post_status', 'on_duty'), detection.get('post_status'))}
异常离岗次数: {detection.get('abnormal_absence_count', 0)} 次
累计离岗时长: {detection.get('total_absence_duration', 0)} 秒
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        detection = data.get('detection', {})

        objects = "\n".join([
            f"  📍 {category_map.get(obj.get('status'), obj.get('status'))}: {obj.get('count', 0)} 段，累计时长: {obj.get('total_duration', 0)} 秒"
            for obj in detection.get('status_stats', [])])

        return f"""
📊 人员离岗实时监测分析报告
{'=' * 50}
⏰ 检测时间: {data.get('detection_time', '未知')}
📹 素材类型: {media_type}
🎯 置信度阈值: {confidence_threshold}
⏱️  离岗判定阈值: {absence_threshold} 秒

🔍 监测结果:
  当前在岗状态: {category_map.get(detection.get('post_status', 'on_duty'), detection.get('post_status'))}
  异常离岗总次数: {detection.get('abnormal_absence_count', 0)} 次
  累计异常离岗时长: {detection.get('total_absence_duration', 0)} 秒

  各状态统计:
{objects if objects else '  ✅ 未检测到异常离岗记录'}
{'=' * 50}
> 注：本报告仅供岗位管理参考，具体处置请结合实际管理制度。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="人员离岗实时监测工具")
    parser.add_argument("--input", help="本地视频/图片文件路径")
    parser.add_argument("--url", help="网络视频/图片的URL地址")
    parser.add_argument("--media-type", choices=["video", "image"], default=ConstantEnum.DEFAULT__MEDIA_TYPE,
                        help="媒体类型：video(视频流/视频文件), image(图片)，默认 video")
    parser.add_argument("--confidence-threshold", type=float, default=ConstantEnum.DEFAULT__CONFIDENCE_THRESHOLD,
                        help="置信度阈值，低于该分值不输出，默认 0.5")
    parser.add_argument("--absence-threshold", type=int, default=ConstantEnum.DEFAULT__ABSENCE_THRESHOLD,
                        help="离岗判定阈值，超过该时长(秒)判定为异常离岗，默认 300")
    parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    parser.add_argument("--list", action='store_true', help="显示离岗监测列表清单")
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

        print("🔍 正在进行人员离岗监测，请稍候...")
        output_content = analyze_media(
            input_path=args.input,
            url=args.url,
            media_type=args.media_type,
            confidence_threshold=args.confidence_threshold,
            absence_threshold=args.absence_threshold,
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
        print(f"❌ 人员离岗监测失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
