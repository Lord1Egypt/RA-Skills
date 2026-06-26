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


def analyze_media(input_path=None, url=None, pet_type=None, media_type=None, action=None, pet_id=None, api_url=None,
                  api_key=None, output_level=None):
    """调用API进行宠物检测识别或底库录入"""
    if not input_path and not url:
        raise ValueError("必须提供本地媒体路径(--input)或网络媒体URL(--url)")

    # 设置参数
    if pet_type:
        ConstantEnum.DEFAULT_PET_TYPE = pet_type
    if media_type:
        ConstantEnum.DEFAULT_MEDIA_TYPE = media_type
    if action:
        ConstantEnum.DEFAULT_ACTION = action

    try:
        input_path = input_path or url
        # 对于底库录入，额外携带宠物ID参数
        params = {}
        if pet_id:
            params["pet_id"] = pet_id
        if action:
            params["action"] = action
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


def format_result(result, output_level="standard", pet_type="cat", action="detect"):
    """格式化输出结果"""
    pet_type_map = {
        "cat": "猫",
        "dog": "狗"
    }
    action_map = {
        "detect": "检测识别",
        "enroll": "底库录入"
    }
    pet_type_cn = pet_type_map.get(pet_type, pet_type)
    action_cn = action_map.get(action, action)

    # 底库录入结果特殊处理
    if action == "enroll":
        if output_level == "json":
            result_id = None
            if result is not None:
                result_json = result
                result_id = result_json.get('id', {})
                result_json = json.dumps(result_json.get('enrollResponse', {}), ensure_ascii=False, indent=2)
            else:
                return "⚠️ 暂无录入结果"
            return f"""
📊 宠物底库录入结构化结果
{result_json}
""", result_id
        elif output_level == "basic":
            data = result.get('data', {})
            status = data.get('status', '未知')
            return f"""
📊 宠物底库录入结果
{'=' * 40}
操作类型: {action_cn}
宠物类型: {pet_type_cn}
录入状态: {status}
提示: {data.get('message', '无提示信息')}
        """
        elif output_level == "standard":
            data = result.get('data', {})
            return f"""
📊 宠物底库录入结果
{'=' * 50}
⏰ 操作时间: {data.get('operation_time', '未知')}
🎯 操作类型: {action_cn}
🐾 宠物类型: {pet_type_cn}
🏷️ 宠物ID: {data.get('pet_id', '未知')}
✅ 录入状态: {data.get('status', '未知')}
💬 提示信息: {data.get('message', '无提示信息')}
{'=' * 50}
> 注：录入成功后即可在检测识别中使用底库进行身份匹配。
        """
        else:
            return json.dumps(result, ensure_ascii=False, indent=2)

    # 检测识别结果
    if output_level == "json":
        result_id = None
        if result is not None:
            result_json = result
            result_id = result_json.get('id', {})
            result_json = json.dumps(result_json.get('detectionResponse', {}), ensure_ascii=False, indent=2)
        else:
            return "⚠️ 暂无分析结果"
        return f"""
📊 喂食器宠物检测分析结构化结果
{result_json}
""", result_id
    elif output_level == "basic":
        # 精简输出
        data = result.get('data', {})
        detection = data.get('detection', {})
        return f"""
📊 宠物检测报告
{'=' * 40}
宠物类型: {pet_type_cn}
检测结果: {detection.get('detection_result', '未知')}
宠物数量: {detection.get('pet_count', 0)}
识别结果: {', '.join([f'{p.get("pet_name")}({p.get("confidence")}分)' for p in detection.get('pets', [])]) if detection.get('pets') else '未识别到宠物'}
        """
    elif output_level == "standard":
        # 标准输出
        data = result.get('data', {})
        detection = data.get('detection', {})

        pets_analysis = "\n".join([
            f"  🐾 {idx + 1}. 宠物ID: {p.get('pet_id', '未知')} 名称: {p.get('pet_name', '未知')} 置信度: {p.get('confidence', 0)}"
            for idx, p in enumerate(detection.get('pets', []))])
        regions_analysis = "\n".join(
            [f"  📍 区域 {idx + 1}: 置信度 {item.get('confidence', 0)} - {item.get('pet_type', '未知')}" for idx, item in
             enumerate(detection.get('regions', []))])
        suggestions = "\n".join([f"  💡 {item}" for item in data.get('feed_suggestions', [])])

        return f"""
📊 智能喂食器宠物检测分析报告
{'=' * 50}
⏰ 检测时间: {data.get('detection_time', '未知')}
📹 操作类型: {action_cn}
🐾 目标宠物类型: {pet_type_cn}
🎯 检测状态: {detection.get('status', '未知')} (整体置信度: {detection.get('overall_confidence', 0)}分)

🔍 检测结果:
  检测到宠物总数: {detection.get('total_pet_count', 0)}
  是否识别到目标区域有宠物: {'✅ 是' if detection.get('has_pet') else '❌ 否'}

  识别到宠物身份列表:
{pets_analysis if pets_analysis else '  未识别到宠物身份'}

  检测区域详情:
{regions_analysis if regions_analysis else '  无区域信息'}

💡 喂食建议:
{suggestions if suggestions else '  暂无特别建议'}
{'=' * 50}
> 注：本报告仅供智能喂养参考，实际请以人工确认结果为准。
        """
    else:
        # 完整输出（JSON格式）
        return json.dumps(result, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="智能喂食器宠物检测识别工具")
    parser.add_argument("--input", help="本地视频/图片文件路径")
    parser.add_argument("--url", help="网络视频/图片的URL地址")
    parser.add_argument("--media-type", choices=["video", "image"], default=ConstantEnum.DEFAULT__MEDIA_TYPE,
                        help="媒体类型：video(视频流/视频文件), image(图片)，默认 video")
    parser.add_argument("--pet-type", choices=["cat", "dog"], default=ConstantEnum.DEFAULT__PET_TYPE,
                        help="宠物类型：cat(猫), dog(狗)，默认 cat")
    parser.add_argument("--pet-id", help="宠物ID/名称，底库录入时必须提供")
    parser.add_argument("--action", choices=["detect", "enroll"], default=ConstantEnum.DEFAULT__ACTION,
                        help="操作类型：detect(检测识别), enroll(底库录入)，默认 detect")
    parser.add_argument("--open-id", required=True, help="当前用户的OpenID/UserId/用户名/手机号")
    parser.add_argument("--list", action='store_true', help="显示宠物检测分析列表清单")
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

        # 底库录入检查宠物ID
        if args.action == "enroll" and not args.pet_id:
            print("❌ 错误: 底库录入操作(--action enroll)必须提供 --pet-id 参数")
            exit(1)

        print("🔍 正在进行宠物检测识别，请稍候...")
        output_content = analyze_media(
            input_path=args.input,
            url=args.url,
            media_type=args.media_type,
            pet_type=args.pet_type,
            action=args.action,
            pet_id=args.pet_id,
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
        print(f"❌ 宠物检测识别失败: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
