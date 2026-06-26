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


def analyze_video(input_path=None, url=None, analyze_duration=None, focus_threshold=None, scene=None, api_url=None,
                  api_key=None, output_level=None):
    """调用API进行专注度分析"""
    if not input_path and not url:
        raise ValueError("必须提供本地视频路径(--input)或网络视频URL(--url)")

    # 设置参数
    if analyze_duration:
        ConstantEnum.DEFAULT_ANALYZE_DURATION = analyze_duration
    if focus_threshold:
        ConstantEnum.DEFAULT_FOCUS_THRESHOLD = focus_threshold
    if scene:
        ConstantEnum.DEFAULT_SCENE = scene

    try:
        input_path = input_path or url
        # 携带额外参数
        params = {}
        if analyze_duration:
            params["analyze_duration"] = analyze_duration
        if focus_threshold:
            params["focus_threshold"] = focus_threshold
        if scene:
            params["scene"] = scene
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


def format_result(result, output_level="standard", analyze_duration=30, focus_threshold=0.6, scene="classroom"):
    """格式化输出结果"""
    scene_map = {
        "classroom": "课堂学习",
        "office": "办公会议",
        "driving": "驾驶出行"
    }
    scene_cn = scene_map.get(scene, scene)

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('focusAnalysisResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 专注度分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        analysis = data.get('analysis', {})
        return f"""
📊 专注度分析报告
{'=' * 40}
应用场景: {scene_cn}
分析时长: {analyze_duration} 分钟
整体专注度评分: {analysis.get('overall_focus_score', '未知')}
专注时长占比: {analysis.get('focus_ratio', '未知')}%
分心走神次数: {analysis.get('distraction_count', 0)}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        analysis = data.get('analysis', {})

        time_stats = f"""  总分析时长: {analyze_duration} 分钟
  专注时长: {analysis.get('focus_duration', 0)} 分钟
  分心时长: {analysis.get('distraction_duration', 0)} 分钟
  专注占比: {analysis.get('focus_ratio', 0)}%"""

        distraction_stats = "\n".join([f"  ⏰ {item.get('time_period')}: 专注度 {item.get('avg_score')}" for item in
                                       analysis.get('time_period_stats', [])])
        suggestions = "\n".join([f"  💡 {item}" for item in data.get('improve_suggestions', [])])

        return f"""
📊 专注度分析报告
{'=' * 50}
⏰ 分析时间: {data.get('analysis_time', '未知')}
📌 应用场景: {scene_cn}
🎯 专注度阈值: {focus_threshold}

🔍 分析结果:
{time_stats}

  整体专注度评分: {analysis.get('overall_focus_score', '未知')}
  分心走神总次数: {analysis.get('distraction_count', 0)}
  是否整体达标: {'✅ 达标' if analysis.get('is_qualified') else '⚠️ 未达标'}

  分段专注度统计:
{distraction_stats if distraction_stats else '  无分段统计'}

💡 专注度改善建议:
{suggestions if suggestions else '  当前专注度表现不错，请继续保持！'}
{'=' * 50}
> 注：本报告仅供参考，不能替代人工评估，具体改善方案请结合实际情况调整。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="专注度分析工具")
    parser.add_argument("--input", help="本地视频文件路径")
    parser.add_argument("--url", help="网络视频的URL地址")
    parser.add_argument("--analyze-duration", type=int, default=ConstantEnum.DEFAULT__ANALYZE_DURATION,
                        help="分析视频时长，单位：分钟，默认 30")
    parser.add_argument("--focus-threshold", type=float, default=ConstantEnum.DEFAULT__FOCUS_THRESHOLD,
                        help="专注度阈值，低于该分值判定为分心，默认 0.6")
    parser.add_argument("--scene", choices=["classroom", "office", "driving"], default=ConstantEnum.DEFAULT__SCENE,
                        help="应用场景：classroom(课堂学习), office(办公会议), driving(驾驶)，默认 classroom")
    parser.add_argument("--open-id", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--list", action='store_true', help="显示专注度分析列表清单")
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

        print("🔍 正在进行专注度分析，请稍候...")
        output_content = analyze_video(
            input_path=args.input,
            url=args.url,
            analyze_duration=args.analyze_duration,
            focus_threshold=args.focus_threshold,
            scene=args.scene,
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
        print(f"❌ 专注度分析失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
