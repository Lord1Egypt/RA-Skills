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


def analyze_media(input_path=None, url=None, media_type=None, blood_pressure=None, blood_sugar=None, blood_lipid=None,
                  api_url=None, api_key=None, output_level=None):
    """调用API进行脑卒中风险筛查"""
    if not input_path and not url:
        raise ValueError("必须提供本地媒体路径(--input)或网络媒体URL(--url)")

    # 设置参数
    if media_type:
        ConstantEnum.DEFAULT_MEDIA_TYPE = media_type

    try:
        input_path = input_path or url
        # 携带生理指标参数
        params = {}
        if blood_pressure:
            params["blood_pressure"] = blood_pressure
        if blood_sugar:
            params["blood_sugar"] = blood_sugar
        if blood_lipid:
            params["blood_lipid"] = blood_lipid
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


def format_result(result, output_level="standard", media_type="video", blood_pressure=None, blood_sugar=None,
                  blood_lipid=None):
    """格式化输出结果"""
    risk_level_map = {
        "low": "低风险",
        "medium": "中风险",
        "high": "高风险",
        "very_high": "极高风险"
    }

    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('strokeRiskResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 脑卒中风险筛查分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        screening = data.get('screening', {})
        risk_level = screening.get('risk_level', '未知')
        risk_level_cn = risk_level_map.get(risk_level, risk_level)
        return f"""
📊 脑卒中风险筛查报告
{'=' * 40}
风险等级: {risk_level_cn}
风险评分: {screening.get('risk_score', '未知')}
主要高危因素: {', '.join(screening.get('high_risk_factors', ['未发现明确高危因素']))}
预警提示: {data.get('warning_message', ['无特殊警示'])[0] if data.get('warning_message') else '无特殊警示'}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        screening = data.get('screening', {})

        # 面部特征
        face_features = "\n".join([f"  {k}: {v}" for k, v in screening.get('face_features', {}).items()])
        # 高危因素
        high_risk_factors = "\n".join([f"  ⚠️  {item}" for item in screening.get('high_risk_factors', [])])
        warnings = "\n".join([f"  ⚠️  {item}" for item in data.get('health_warnings', [])])
        suggestions = "\n".join([f"  💡 {item}" for item in data.get('lifestyle_suggestions', [])])
        medical_advices = "\n".join([f"  🏥 {item}" for item in data.get('medical_advices', [])])

        risk_level = screening.get('risk_level', '未知')
        risk_level_cn = risk_level_map.get(risk_level, risk_level)

        # 生理指标信息
        physiological_info = ""
        if blood_pressure or blood_sugar or blood_lipid:
            physiological_info = "\n📊 提供的生理指标:"
            if blood_pressure:
                physiological_info += f"\n  血压: {blood_pressure} mmHg"
            if blood_sugar:
                physiological_info += f"\n  空腹血糖: {blood_sugar} mmol/L"
            if blood_lipid:
                physiological_info += f"\n  总胆固醇: {blood_lipid} mmol/L"

        return f"""
📊 脑卒中风险筛查分析报告
{'=' * 50}
⏰ 筛查时间: {data.get('screening_time', '未知')}
📹 素材类型: {media_type}
{physiological_info}

🎯 筛查结果:
  风险评分: {screening.get('risk_score', '未知')}
  风险等级: {risk_level_cn}

🔍 面部特征辨识:
{face_features if face_features else '  未提取到明显特征'}

🚨 高危因素识别:
{high_risk_factors if high_risk_factors else '  ✅ 未发现明确高危因素'}

⚠️ 健康预警提示:
{warnings if warnings else '  无特殊预警'}

💡 生活方式干预建议:
{suggestions if suggestions else '  保持健康生活方式即可'}

🏥 就医指引:
{medical_advices if medical_advices else '  定期体检，关注血压血糖变化即可'}
{'=' * 50}
> 注：本报告仅供健康风险筛查参考，不能替代专业医学检查和医生诊断，发现高危请及时就医。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="脑卒中风险筛查分析工具")
    parser.add_argument("--input", help="本地视频/图片文件路径")
    parser.add_argument("--url", help="网络视频/图片的URL地址")
    parser.add_argument("--media-type", choices=["video", "image"], default=ConstantEnum.DEFAULT__MEDIA_TYPE,
                        help="媒体类型：video(视频), image(图片)，默认 video")
    parser.add_argument("--blood-pressure", help="血压值，格式：收缩压/舒张压，如 140/90")
    parser.add_argument("--blood-sugar", type=float, help="空腹血糖值 mmol/L")
    parser.add_argument("--blood-lipid", type=float, help="总胆固醇值 mmol/L")
    parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    parser.add_argument("--list", action='store_true', help="显示脑卒中风险筛查列表清单")
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

        print("🔍 正在进行脑卒中风险筛查，请稍候...")
        output_content = analyze_media(
            input_path=args.input,
            url=args.url,
            media_type=args.media_type,
            blood_pressure=args.blood_pressure,
            blood_sugar=args.blood_sugar,
            blood_lipid=args.blood_lipid,
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
        print(f"❌ 脑卒中风险筛查失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
