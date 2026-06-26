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


def analyze_video(input_path=None, url=None, infant_age_group=None, api_url=None, api_key=None, output_level=None):
    """调用API分析婴儿安全看护视频"""
    if not input_path and not url:
        raise ValueError("必须提供本地视频路径(--input)或网络视频URL(--url)")

    # 设置婴儿年龄段参数
    if infant_age_group:
        ConstantEnum.DEFAULT__INFANT_AGE_GROUP = infant_age_group

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


def format_result(result, output_level="standard", infant_age_group="other"):
    """格式化输出结果"""
    infant_age_group_map = {
        "newborn": "0-3个月(新生儿)",
        "infant": "3-12个月(婴儿)",
        "toddler": "1-3岁(学步期)",
        "other": "其他年龄段"
    }
    infant_age_group_cn = infant_age_group_map.get(infant_age_group, infant_age_group)

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('infantSafetyResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 婴安卫士智能看护结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        return f"""
📊 婴安卫士安全看护报告
{'=' * 40}
婴儿年龄段: {infant_age_group_cn}
整体安全状况: {diagnosis.get('overall_safety', '未知')}
主要风险: {', '.join([f'{k}: {v}' for k, v in diagnosis.get('risk_issues', {}).items() if v != '正常'])}
安全提示: {data.get('safety_warnings', ['无特殊警示'])[0] if data.get('safety_warnings') else '无特殊警示'}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        infant_detection = data.get('infant_detection', {})

        risk_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('risk_behavior', {}).items()])
        position_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('body_position', {}).items()])
        environment_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('environment', {}).items()])
        warnings = "\n".join([f"  ⚠️  {item}" for item in data.get('safety_warnings', [])])
        suggestions = "\n".join([f"  💡 {item}" for item in data.get('care_suggestions', [])])

        return f"""
📊 婴安卫士智能安全看护报告
{'=' * 50}
⏰ 分析时间: {data.get('analysis_time', '未知')}
👶 婴儿年龄段: {infant_age_group_cn}
🎯 婴儿检测: {infant_detection.get('status', '未知')} (置信度: {infant_detection.get('quality_score', 0)}分)

🔍 监测结果:
  整体安全评分: {diagnosis.get('safety_score', '未知')}
  整体状况: {diagnosis.get('overall_safety', '未知')}

  风险行为识别:
{risk_analysis}

  身体姿势监测:
{position_analysis}

  环境安全评估:
{environment_analysis}

⚠️ 高风险预警:
{warnings}

💡 安全看护建议:
{suggestions}
{'=' * 50}
> 注：本报告仅供安全参考，不能替代家长实时看护与专业护理。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="婴儿智能安全看护分析工具")
    parser.add_argument("--input", help="本地视频文件路径")
    parser.add_argument("--url", help="网络视频MP4的URL地址")
    parser.add_argument("--infant-age-group", choices=["newborn", "infant", "toddler", "other"],
                        default=ConstantEnum.DEFAULT__INFANT_AGE_GROUP,
                        help="婴儿年龄段：newborn(0-3个月), infant(3-12个月), toddler(1-3岁), other(其他)，默认 other")
    parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    parser.add_argument("--list", action='store_true', help="显示婴儿安全看护分析列表清单")
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

        print("🔍 正在分析婴儿安全看护，请稍候...")
        output_content = analyze_video(
            input_path=args.input,
            url=args.url,
            infant_age_group=args.infant_age_group,
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
        print(f"❌ 婴儿安全看护分析失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
