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


def analyze_video(input_path=None, url=None, analysis_type=None, api_url=None, api_key=None, output_level=None):
    """调用API分析安全驾驶行为"""
    if not input_path and not url:
        raise ValueError("必须提供本地视频路径(--input)或网络视频URL(--url)")

    # 设置分析类型参数
    if analysis_type:
        ConstantEnum.DEFAULT__ANALYSIS_TYPE = analysis_type

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


def format_result(result, output_level="standard", analysis_type="comprehensive"):
    """格式化输出结果"""
    analysis_type_map = {
        "comprehensive": "综合分析",
        "fatigue": "疲劳驾驶评估",
        "distraction": "分心驾驶评估",
        "seatbelt": "安全带专项检查",
        "risk": "危险行为筛查",
        "other": "其他分析"
    }
    analysis_type_cn = analysis_type_map.get(analysis_type, analysis_type)

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('driveResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 安全驾驶行为分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        return f"""
📊 安全驾驶行为分析报告
{'=' * 40}
分析类型: {analysis_type_cn}
整体安全驾驶评分: {diagnosis.get('overall_score', '未知')}
主要问题: {', '.join([f'{k}: {v}' for k, v in diagnosis.get('key_issues', {}).items() if v != '正常'])}
安全提示: {data.get('safety_warnings', ['无特殊警示'])[0] if data.get('safety_warnings') else '无特殊警示'}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        diagnosis = data.get('diagnosis', {})
        person_detection = data.get('person_detection', {})

        fatigue_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('fatigue_driving', {}).items()])
        distraction_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('distraction_driving', {}).items()])
        seatbelt_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('seatbelt_usage', {}).items()])
        posture_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('driving_posture', {}).items()])
        risk_analysis = "\n".join([f"  {k}: {v}" for k, v in diagnosis.get('risk_behavior', {}).items()])
        warnings = "\n".join([f"  ⚠️  {item}" for item in data.get('safety_warnings', [])])
        suggestions = "\n".join([f"  💡 {item}" for item in data.get('safety_suggestions', [])])

        return f"""
📊 安全驾驶行为分析报告
{'=' * 50}
⏰ 分析时间: {data.get('analysis_time', '未知')}
🚗 分析类型: {analysis_type_cn}
🎯 驾驶员检测: {person_detection.get('status', '未知')} (置信度: {person_detection.get('quality_score', 0)}分)

🔍 评估结果:
  整体安全驾驶评分: {diagnosis.get('total_score', '未知')}/100
  整体评价: {diagnosis.get('overall_safety', '未知')}

  疲劳驾驶维度:
{fatigue_analysis}

  分心驾驶维度:
{distraction_analysis}

  安全带使用维度:
{seatbelt_analysis}

  驾驶姿势维度:
{posture_analysis}

  危险行为维度:
{risk_analysis}

⚠️ 风险警示:
{warnings}

💡 安全驾驶改进建议:
{suggestions}
{'=' * 50}
> 重要声明：道路千万条，安全第一条！本分析仅供交通安全教育参考，不能替代专业驾驶培训。请务必严格遵守交通法规，安全文明驾驶。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="安全驾驶行为分析工具")
    parser.add_argument("--input", help="本地视频文件路径")
    parser.add_argument("--url", help="网络视频MP4的URL地址")
    parser.add_argument("--analysis-type",
                        choices=["comprehensive", "fatigue", "distraction", "seatbelt", "risk", "other"],
                        default=ConstantEnum.DEFAULT__ANALYSIS_TYPE,
                        help="分析类型：comprehensive(综合分析), fatigue(疲劳驾驶评估), distraction(分心驾驶评估), seatbelt(安全带专项检查), risk(危险行为筛查), other(其他分析)，默认 comprehensive")
    parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    parser.add_argument("--list", action='store_true', help="显示安全驾驶分析列表清单")
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

        print("🔍 正在进行安全驾驶行为分析，请稍候...")
        output_content = analyze_video(
            input_path=args.input,
            url=args.url,
            analysis_type=args.analysis_type,
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
        print(f"❌ 安全驾驶行为分析失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
