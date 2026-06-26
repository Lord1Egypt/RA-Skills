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


def analyze_video(input_path=None, url=None, fish_type=None, api_url=None, api_key=None, output_level=None, **kwargs):
    """调用API分析鱼类宠物视频"""
    if not input_path and not url:
        raise ValueError("必须提供本地视频路径(--input)或网络视频URL(--url)")

    # 设置鱼类宠物类型参数
    if fish_type:
        ConstantEnum.DEFAULT__FISH_TYPE = fish_type

    try:
        input_path = input_path or url
        return skill.get_output_analysis(input_path, **kwargs)

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


def format_result(result, output_level="standard", fish_type="other"):
    """格式化输出结果"""
    fish_type_map = {
        "goldfish": "金鱼",
        "koi": "锦鲤",
        "betta": "斗鱼",
        "shrimp": "虾",
        "crab": "蟹",
        "turtle": "龟",
        "clownfish": "小丑鱼",
        "guppy": "孔雀鱼",
        "arowana": "龙鱼",
        "angel": "神仙鱼",
        "other": "其他"
    }
    fish_type_cn = fish_type_map.get(fish_type, fish_type)

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('fishHealthResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 宠安卫士健康分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        return f"""
📊 宠安卫士健康报告
{'=' * 40}
鱼宠类型: {fish_type_cn}
整体健康状况: {diagnosis.get('overall_health', '未知')}
主要问题: {', '.join([f'{k}: {v}' for k, v in diagnosis.get('key_issues', {}).items() if v != '正常'])}
健康提示: {data.get('health_warnings', ['无特殊警示'])[0] if data.get('health_warnings') else '无特殊警示'}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        fish_detection = data.get('fish_detection', {})

        scale_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('scale_condition', {}).items()])
        fin_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('fin_condition', {}).items()])
        color_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('color_condition', {}).items()])
        activity_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('activity_condition', {}).items()])
        warnings = "\n".join([f"  ⚠️  {item}" for item in data.get('health_warnings', [])])
        suggestions = "\n".join([f"  💡 {item}" for item in data.get('care_suggestions', [])])

        return f"""
📊 宠安卫士健康报告
{'=' * 50}
⏰ 分析时间: {data.get('analysis_time', '未知')}
🐟 鱼宠类型: {fish_type_cn}
🎯 鱼宠检测: {fish_detection.get('status', '未知')} (置信度: {fish_detection.get('quality_score', 0)}分)

🔍 诊断结果:
  整体健康评分: {diagnosis.get('health_score', '未知')}
  整体状况: {diagnosis.get('overall_health', '未知')}

  鳞片状况:
{scale_analysis}

  鱼鳍状况:
{fin_analysis}

  体色状况:
{color_analysis}

  活跃度:
{activity_analysis}

⚠️ 潜在疾病预警:
{warnings}

💡 健康养护建议:
{suggestions}
{'=' * 50}
> 注：本报告仅供健康参考，不能替代专业兽医诊断。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="鱼类宠物健康诊断分析工具")
    parser.add_argument("--input", help="本地视频文件路径")
    parser.add_argument("--url", help="网络视频MP4的URL地址")
    parser.add_argument("--fish-type",
                        choices=["goldfish", "koi", "betta", "shrimp", "crab", "turtle", "clownfish", "guppy",
                                 "arowana", "angel", "other"], default=ConstantEnum.DEFAULT__FISH_TYPE,
                        help="鱼类宠物类型：goldfish(金鱼), koi(锦鲤), betta(斗鱼), shrimp(虾), crab(蟹), turtle(龟), clownfish(小丑鱼), guppy(孔雀鱼), arowana(龙鱼), angel(神仙鱼), other(其他)，默认 other")
    parser.add_argument("--open-id", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--list", action='store_true', help="显示鱼类宠物健康分析列表清单")
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

        print("🔍 正在分析鱼类宠物健康，请稍候...")
        output_content = analyze_video(
            open_id=args.open_id,
            input_path=args.input,
            url=args.url,
            fish_type=args.fish_type,
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
        print(f"❌ 鱼类宠物健康分析失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
