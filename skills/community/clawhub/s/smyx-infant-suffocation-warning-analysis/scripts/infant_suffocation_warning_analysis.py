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


def analyze_video(input_path=None, url=None, sensitivity=None, api_url=None, api_key=None, output_level=None):
    """调用API进行婴儿趴睡窒息预警分析"""
    if not input_path and not url:
        raise ValueError("必须提供本地视频路径(--input)或网络视频URL(--url)")

    # 设置参数
    if sensitivity and 1 <= sensitivity <= 5:
        ConstantEnum.DEFAULT_SENSITIVITY = sensitivity

    try:
        input_path = input_path or url
        params = {}
        if sensitivity:
            params["sensitivity"] = sensitivity
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


def format_result(result, output_level="standard", sensitivity=3):
    """格式化输出结果"""
    risk_level_map = {
        "low": "低风险",
        "medium": "中风险",
        "high": "⚠️ 高风险"
    }
    position_map = {
        "prone": "俯卧（趴睡）",
        "supine": "仰卧（仰睡）",
        "side": "侧卧"
    }

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('suffocationWarningResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 婴儿趴睡窒息预警分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        risk = data.get('risk_assessment', {})
        return f"""
📊 婴儿趴睡窒息预警报告
{'=' * 40}
睡眠姿势: {position_map.get(data.get('sleep_position', 'supine'), data.get('sleep_position', '未知'))}
口鼻遮挡: {'是' if data.get('mouth_nose_covered', False) else '否'}
头部蒙被: {'是' if data.get('head_covered', False) else '否'}
风险等级: {risk_level_map.get(risk.get('risk_level', 'low'), risk.get('risk_level', '低风险'))}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        risk = data.get('risk_assessment', {})

        risk_factors = []
        if data.get('sleep_position', '') == 'prone':
            risk_factors.append("⚠️ 俯卧趴睡姿势")
        if data.get('mouth_nose_covered', False):
            risk_factors.append("⚠️ 口鼻被被褥/衣物遮挡")
        if data.get('head_covered', False):
            risk_factors.append("⚠️ 头部完全被蒙盖")

        if not risk_factors:
            risk_factors = ["✅ 未识别到高危因素"]
        risk_str = "\n".join([f"  {item}" for item in risk_factors])
        suggestions = "\n".join([f"  💡 {item}" for item in data.get('suggestions', ['建议保持仰睡姿势，避免口鼻遮挡'])])

        return f"""
📊 婴儿趴睡窒息预警分析报告
{'=' * 50}
⏰ 分析时间: {data.get('analysis_time', '未知')}
⚙️ 报警灵敏度: {sensitivity}/5

🔍 识别结果:
  睡眠姿势: {position_map.get(data.get('sleep_position', 'supine'), data.get('sleep_position', '未知'))}
  口鼻遮挡: {'是' if data.get('mouth_nose_covered', False) else '否'}
  头部蒙被: {'是' if data.get('head_covered', False) else '否'}

🚨 风险评估:
  风险等级: {risk_level_map.get(risk.get('risk_level', 'low'), risk.get('risk_level', '低风险'))}
  风险评分: {risk.get('risk_score', '未知')}/100

  高危因素:
{risk_str}

💡 安全提示:
{suggestions}
{'=' * 50}
> ⚠️ 本技能为辅助监测工具，不能替代成人实时看护，发现高风险请立即检查宝宝状况！
> 注：本报告仅供安全参考，不能替代专业医护建议。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="婴儿趴睡窒息预警工具")
    parser.add_argument("--input", help="本地视频文件路径")
    parser.add_argument("--url", help="网络视频的URL地址")
    parser.add_argument("--sensitivity", type=int, choices=[1, 2, 3, 4, 5], default=ConstantEnum.DEFAULT__SENSITIVITY,
                        help="报警灵敏度 1-5，数值越高越敏感，默认 3")
    parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    parser.add_argument("--list", action='store_true', help="显示婴儿趴睡窒息预警列表清单")
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

        print("🚨 正在进行婴儿趴睡窒息预警分析，请稍候...")
        output_content = analyze_video(
            input_path=args.input,
            url=args.url,
            sensitivity=args.sensitivity,
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
        print(f"❌ 婴儿趴睡窒息预警分析失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
