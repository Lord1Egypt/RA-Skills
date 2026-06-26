#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD 场景化 AIGC 图片生成脚本
基于 CreateSceneAigcImageTask API
"""

import os
import sys
import json
import argparse
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vod_auto_upgrade import check_sdk_version


# 软依赖：vod_load_env 用于在凭证缺失时从 ~/.env 等 dotenv 文件兜底加载
try:
    from vod_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False

check_sdk_version()

try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.vod.v20180717 import vod_client, models
except ImportError:
    print("错误：请先安装腾讯云 SDK: pip install tencentcloud-sdk-python")
    sys.exit(1)


def get_credential():
    """获取腾讯云认证信息。若环境变量缺失则尝试从 dotenv 文件自动加载。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        # 兜底：尝试从 ~/.env 等 dotenv 文件加载
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] 环境变量未设置，尝试从 dotenv 文件自动加载...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from vod_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print("错误：请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
            sys.exit(1)

    return credential.Credential(secret_id, secret_key)


def get_client(region="ap-guangzhou"):
    """获取 VOD 客户端"""
    cred = get_credential()
    http_profile = HttpProfile()
    http_profile.endpoint = "vod.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return vod_client.VodClient(cred, region, client_profile)


def build_scene_info(args):
    """构建场景化生图参数 SceneInfo"""
    scene_info = {
        "Type": args.scene_type
    }

    # AI换衣场景配置
    if args.scene_type == "change_clothes":
        change_clothes_config = {}

        # 衣物图片列表
        if args.clothes_files:
            clothes_file_infos = []
            for file_info in args.clothes_files:
                # 格式: type:file_id 或 type:url
                parts = file_info.split(":", 1)
                if len(parts) == 2:
                    file_type, file_value = parts
                    info = {"Type": file_type}
                    if file_type == "File":
                        info["FileId"] = file_value
                    elif file_type == "Url":
                        info["Url"] = file_value
                    clothes_file_infos.append(info)
            if clothes_file_infos:
                change_clothes_config["ClothesFileInfos"] = clothes_file_infos

        # 换衣提示词
        if args.change_prompt:
            change_clothes_config["Prompt"] = args.change_prompt

        if change_clothes_config:
            scene_info["ChangeClothesConfig"] = change_clothes_config

    # AI生商品图场景配置
    elif args.scene_type == "product_image":
        product_image_config = {}

        if args.product_prompt:
            product_image_config["Prompt"] = args.product_prompt
        if args.negative_prompt:
            product_image_config["NegativePrompt"] = args.negative_prompt
        if args.product_desc:
            product_image_config["ProductDesc"] = args.product_desc
        if args.more_requirement:
            product_image_config["MoreRequirement"] = args.more_requirement
        if args.output_image_count:
            product_image_config["OutputImageCount"] = args.output_image_count

        if product_image_config:
            scene_info["ProductImageConfig"] = product_image_config

    return scene_info


def build_file_infos(args):
    """构建输入图片列表 FileInfos"""
    file_infos = []

    if args.input_files:
        for file_info in args.input_files:
            # 格式: type:file_id 或 type:url
            parts = file_info.split(":", 1)
            if len(parts) == 2:
                file_type, file_value = parts
                info = {"Type": file_type}
                if file_type == "File":
                    info["FileId"] = file_value
                elif file_type == "Url":
                    info["Url"] = file_value
                file_infos.append(info)

    return file_infos if file_infos else None


def build_output_config(args):
    """构建输出配置 OutputConfig"""
    output_config = {}

    if args.output_storage_mode:
        output_config["StorageMode"] = args.output_storage_mode
    if args.media_name:
        output_config["MediaName"] = args.media_name
    if args.class_id is not None:
        output_config["ClassId"] = args.class_id
    if args.expire_time:
        output_config["ExpireTime"] = args.expire_time
    if args.aspect_ratio:
        output_config["AspectRatio"] = args.aspect_ratio
    if args.image_width:
        output_config["ImageWidth"] = args.image_width
    if args.image_height:
        output_config["ImageHeight"] = args.image_height
    if args.resolution:
        output_config["Resolution"] = args.resolution

    # 编码配置（仅AI换衣场景有效）
    if args.encode_format or args.encode_quality:
        encode_config = {}
        if args.encode_format:
            encode_config["Format"] = args.encode_format
        if args.encode_quality:
            encode_config["Quality"] = args.encode_quality
        output_config["EncodeConfig"] = encode_config

    return output_config if output_config else None


def create_scene_aigc_image_task(args):
    """创建场景化 AIGC 图片生成任务"""
    client = get_client(args.region)

    req = models.CreateSceneAigcImageTaskRequest()

    # 必需参数
    if not args.sub_app_id:
        print("错误：必须指定 --sub-app-id 或设置环境变量 TENCENTCLOUD_VOD_SUB_APP_ID")
        sys.exit(1)
    req.SubAppId = args.sub_app_id
    req.SceneInfo = build_scene_info(args)

    # 输入图片列表
    file_infos = build_file_infos(args)
    if file_infos:
        req.FileInfos = file_infos

    # 输出配置
    output_config = build_output_config(args)
    if output_config:
        req.OutputConfig = output_config

    # 可选参数
    if args.session_id:
        req.SessionId = args.session_id
    if args.session_context:
        req.SessionContext = args.session_context
    if args.tasks_priority is not None:
        req.TasksPriority = args.tasks_priority
    if args.ext_info:
        req.ExtInfo = args.ext_info

    if args.dry_run:
        print("[DRY RUN] 请求参数:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return

    try:
        resp = client.CreateSceneAigcImageTask(req)
        result = json.loads(resp.to_json_string())

        print(f"场景化 AIGC 图片生成任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")
        print(f"RequestId: {result.get('RequestId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except TencentCloudSDKException as e:
        print(f"创建任务失败: {e}")
        sys.exit(1)
    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        print(f"发生错误: {e}")
        sys.exit(1)


def query_task(args):
    """查询任务详情"""
    if hasattr(args, 'dry_run') and args.dry_run:
        print(f"[DRY RUN] DescribeTaskDetail 请求预览:")
        print(f"  TaskId: {args.task_id}")
        if getattr(args, 'sub_app_id', None):
            print(f"  SubAppId: {args.sub_app_id}")
        return

    client = get_client(args.region)

    req = models.DescribeTaskDetailRequest()
    req.TaskId = args.task_id

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id

    try:
        resp = client.DescribeTaskDetail(req)
        result = json.loads(resp.to_json_string())

        task_type = result.get('TaskType', 'N/A')
        status = result.get('Status', 'N/A')

        print(f"任务类型: {task_type}")
        print(f"任务状态: {status}")

        if result.get('TaskId'):
            print(f"TaskId: {result['TaskId']}")
        if result.get('CreateTime'):
            print(f"创建时间: {result['CreateTime']}")

        # 输出任务详情
        if result.get('ProcedureTask'):
            print(f"\n媒体处理任务详情:")
            print(json.dumps(result['ProcedureTask'], indent=2, ensure_ascii=False))
        if result.get('EditMediaTask'):
            print(f"\n视频编辑任务详情:")
            print(json.dumps(result['EditMediaTask'], indent=2, ensure_ascii=False))
        if result.get('WechatPublishTask'):
            print(f"\n微信发布任务详情:")
            print(json.dumps(result['WechatPublishTask'], indent=2, ensure_ascii=False))
        if result.get('ComposeMediaTask'):
            print(f"\n制作媒体文件任务详情:")
            print(json.dumps(result['ComposeMediaTask'], indent=2, ensure_ascii=False))
        if result.get('SplitMediaTask'):
            print(f"\n视频拆条任务详情:")
            print(json.dumps(result['SplitMediaTask'], indent=2, ensure_ascii=False))
        if result.get('WechatMiniProgramPublishTask'):
            print(f"\n微信小程序发布任务详情:")
            print(json.dumps(result['WechatMiniProgramPublishTask'], indent=2, ensure_ascii=False))

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except TencentCloudSDKException as e:
        print(f"查询失败: {e}")
        sys.exit(1)
    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        print(f"发生错误: {e}")
        sys.exit(1)


def wait_for_task(client, task_id, sub_app_id=None, max_wait=600):
    """等待任务完成"""
    print(f"\n等待任务完成 (TaskId: {task_id})...")
    start_time = time.time()

    while time.time() - start_time < max_wait:
        req = models.DescribeTaskDetailRequest()
        req.TaskId = task_id
        if sub_app_id:
            req.SubAppId = sub_app_id

        try:
            resp = client.DescribeTaskDetail(req)
            result = json.loads(resp.to_json_string())

            status = result.get('Status', 'PROCESSING')
            print(f"  当前状态: {status}")

            if status == 'SUCCESS':
                print("任务完成!")
                return result
            elif status == 'FAIL':
                print("任务失败!")
                return result

            time.sleep(5)
        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
            print(f"查询任务状态失败: {e}")
            time.sleep(5)

    print(f"⏱️ 等待超时（{max_wait}秒），任务仍在执行中")
    return None


def main():
    parser = argparse.ArgumentParser(
        description='VOD 场景化 AIGC 图片生成工具\n基于 CreateSceneAigcImageTask API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # AI换衣场景
  python vod_scene_aigc_image.py generate \\
    --sub-app-id 251007502 \\
    --scene-type change_clothes \\
    --input-files "File:3704211xxx" \\
    --clothes-files "File:3704211yyy" \\
    --change-prompt "衬衫打开一点"

  # AI生商品图场景
  python vod_scene_aigc_image.py generate \\
    --sub-app-id 251007502 \\
    --scene-type product_image \\
    --input-files "File:3704211xxx" "File:3704211yyy" \\
    --product-prompt "红色春节背景" \\
    --product-desc "这是一瓶可乐" \\
    --output-image-count 6

  # 查询任务
  python vod_scene_aigc_image.py query --task-id "251007502-SceneAigcImageTask-xxx"

场景类型:
  - change_clothes: AI换衣
  - product_image: AI生商品图
  - outpainting: AI扩图

输入文件格式:
  - File:FileId  (使用点播媒体文件)
  - Url:URL      (使用可访问的URL)
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # 生成图片任务
    gen_parser = subparsers.add_parser('generate', help='创建场景化 AIGC 图片生成任务')

    # 必需参数
    gen_parser.add_argument('--sub-app-id', type=int,
                           default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                           help='点播应用 ID（必填，也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    gen_parser.add_argument('--scene-type', required=True,
                           choices=['change_clothes', 'product_image', 'outpainting'],
                           help='AI生图场景类型 (必需)')

    # 输入图片列表
    gen_parser.add_argument('--input-files', nargs='+',
                           help='输入图片列表，格式: File:FileId 或 Url:URL')

    # AI换衣场景参数
    gen_parser.add_argument('--clothes-files', nargs='+',
                           help='[换衣场景] 衣物图片列表，格式: File:FileId 或 Url:URL')
    gen_parser.add_argument('--change-prompt',
                           help='[换衣场景] AI换衣的提示词')

    # AI生商品图场景参数
    gen_parser.add_argument('--product-prompt',
                           help='[商品图场景] 生成图片背景的提示词')
    gen_parser.add_argument('--negative-prompt',
                           help='[商品图场景] 要阻止模型生成图片的提示词')
    gen_parser.add_argument('--product-desc',
                           help='[商品图场景] 关于产品的详细描述')
    gen_parser.add_argument('--more-requirement',
                           help='[商品图场景] 特殊要求')
    gen_parser.add_argument('--output-image-count', type=int,
                           help='[商品图场景] 期望生成的图片张数 (1-10, 默认1)')

    # 输出配置
    gen_parser.add_argument('--output-storage-mode',
                           choices=['Permanent', 'Temporary'],
                           help='存储模式: Permanent(永久存储)/Temporary(临时存储,默认)')
    gen_parser.add_argument('--media-name',
                           help='输出文件名 (最长64字符)')
    gen_parser.add_argument('--class-id', type=int,
                           help='分类ID (默认0)')
    gen_parser.add_argument('--expire-time',
                           help='过期时间 (ISO 8601格式)')
    gen_parser.add_argument('--aspect-ratio',
                           choices=['1:1', '3:2', '2:3', '3:4', '4:3', '4:5', '5:4', '16:9', '9:16', '21:9'],
                           help='生成图片的宽高比')
    gen_parser.add_argument('--image-width', type=int,
                           help='[扩图场景] 输出图像宽度')
    gen_parser.add_argument('--image-height', type=int,
                           help='[扩图场景] 输出图像高度')
    gen_parser.add_argument('--resolution',
                           choices=['1K', '2K', '4K'],
                           help='[换衣场景] 输出分辨率')

    # 编码配置（仅AI换衣场景有效）
    gen_parser.add_argument('--encode-format',
                           choices=['JPEG', 'PNG'],
                           help='[换衣场景] 图片格式')
    gen_parser.add_argument('--encode-quality', type=int,
                           help='[换衣场景] 图片相对质量 (1-100)')

    # 其他可选参数
    gen_parser.add_argument('--session-id',
                           help='用于去重的识别码 (最长50字符)')
    gen_parser.add_argument('--session-context',
                           help='来源上下文 (最长1000字符)')
    gen_parser.add_argument('--tasks-priority', type=int,
                           help='任务优先级 (-10到10, 默认0)')
    gen_parser.add_argument('--ext-info',
                           help='保留字段，特殊用途时使用')

    # 通用参数
    gen_parser.add_argument('--region', default='ap-guangzhou',
                           help='地域 (默认: ap-guangzhou)')
    gen_parser.add_argument('--no-wait', action='store_true',
                           help='仅提交任务，不等待结果')
    gen_parser.add_argument('--max-wait', type=int, default=600,
                           help='最大等待时间(秒) (默认: 600)')
    gen_parser.add_argument('--json', action='store_true',
                           help='JSON 格式输出')
    gen_parser.add_argument('--dry-run', action='store_true',
                           help='预览请求参数，不实际执行')

    # 查询任务
    query_parser = subparsers.add_parser('query', help='查询任务详情')
    query_parser.add_argument('--task-id', required=True,
                             help='任务 ID')
    query_parser.add_argument('--sub-app-id', type=int,
                             default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                             help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    query_parser.add_argument('--region', default='ap-guangzhou',
                             help='地域')
    query_parser.add_argument('--json', action='store_true',
                             help='JSON 格式输出')
    query_parser.add_argument('--dry-run', action='store_true',
                             help='预览请求参数，不实际执行')

    args = parser.parse_args()

    if args.command == 'generate':
        create_scene_aigc_image_task(args)
    elif args.command == 'query':
        query_task(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
