#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD 任务详情查询脚本
通过任务 ID 查询任务的执行状态和结果的详细信息（最多可以查询3天之内提交的任务）。

支持的任务类型（全量）：
  Procedure            视频处理任务
  EditMedia            视频编辑任务
  SplitMedia           视频拆条任务
  ComposeMedia         制作媒体文件任务
  WechatPublish        微信发布任务
  WechatMiniProgramPublish  微信小程序发布任务
  PullUpload           拉取上传任务
  FastClipMedia        快速剪辑任务
  RemoveWatermarkTask  智能去除水印任务
  DescribeFileAttributesTask  获取文件属性任务
  RebuildMedia         音画质重生任务（旧）
  ReviewAudioVideo     音视频审核任务
  ExtractTraceWatermark  提取溯源水印任务
  ExtractCopyRightWatermark  提取版权水印任务
  QualityInspect       音画质检测任务
  QualityEnhance       音画质重生任务
  ComplexAdaptiveDynamicStreaming  复杂自适应码流任务
  ProcessMediaByMPS    MPS 视频处理任务
  AigcImageTask        AIGC 生图任务
  SceneAigcImageTask   场景化 AIGC 生图任务
  AigcVideoTask        AIGC 生视频任务
  SceneAigcVideoTask   场景化 AIGC 生视频任务
  ImportMediaKnowledge 导入媒体知识任务
  ExtractBlindWatermark  提取数字水印任务
  CreateAigcAdvancedCustomElement  创建自定义主体任务
  CreateAigcCustomVoiceTask  创建自定义音色任务
  CreateAigcSubjectTask  创建主体任务

API 文档：https://cloud.tencent.com/document/api/266/33431
"""

import os
import sys
import json
import argparse
import time


# ── 主体元素持久化 ────────────────────────────────────────────────────────────

def _save_elements(task_id, info_list):
    """
    将 CreateAigcAdvancedCustomElementTask 的输出结果合并到
    mem/elements.json 中对应 task_id 的记录里（请求 + 结果一体）。
    若找不到对应记录则新建一条。
    """
    if not info_list:
        return None

    mem_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "mem", "elements.json",
    )
    os.makedirs(os.path.dirname(mem_path), exist_ok=True)

    # 读取已有列表
    elements = []
    if os.path.exists(mem_path):
        try:
            with open(mem_path, "r", encoding="utf-8") as f:
                elements = json.load(f)
            if not isinstance(elements, list):
                elements = []
        except Exception:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
            elements = []

    # 找到对应 task_id 的记录并合并结果
    matched = False
    for rec in elements:
        if rec.get("task_id") == task_id:
            rec["result"] = {
                "element_count": len(info_list),
                "info_list": info_list,
            }
            matched = True
            break

    # 没有找到则新增一条（仅含结果）
    if not matched:
        elements.append({
            "task_id": task_id,
            "result": {
                "element_count": len(info_list),
                "info_list": info_list,
            },
        })

    with open(mem_path, "w", encoding="utf-8") as f:
        json.dump(elements, f, indent=2, ensure_ascii=False)

    return mem_path

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
    from tencentcloud.vod.v20180717 import vod_client, models  # NOCA:unused-import(may be needed for future use)
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


# ── 常量映射 ──────────────────────────────────────────────────────────────────

STATUS_MAP = {
    "WAITING": "等待中",
    "PROCESSING": "处理中",
    "FINISH": "已完成",
    "ABORTED": "已终止",
    "FAIL": "失败",
    "SUCCESS": "成功",
}

TASK_TYPE_MAP = {
    "Procedure": "视频处理",
    "EditMedia": "视频编辑",
    "SplitMedia": "视频拆条",
    "ComposeMedia": "制作媒体文件",
    "WechatPublish": "微信发布",
    "WechatMiniProgramPublish": "微信小程序发布",
    "PullUpload": "拉取上传",
    "FastClipMedia": "快速剪辑",
    "RemoveWatermarkTask": "智能去除水印",
    "DescribeFileAttributesTask": "获取文件属性",
    "RebuildMedia": "音画质重生（旧）",
    "ReviewAudioVideo": "音视频审核",
    "ExtractTraceWatermark": "提取溯源水印",
    "ExtractCopyRightWatermark": "提取版权水印",
    "QualityInspect": "音画质检测",
    "QualityEnhance": "音画质重生",
    "ComplexAdaptiveDynamicStreaming": "复杂自适应码流",
    "ProcessMediaByMPS": "MPS 视频处理",
    "AigcImageTask": "AIGC 生图",
    "SceneAigcImageTask": "场景化 AIGC 生图",
    "AigcVideoTask": "AIGC 生视频",
    "SceneAigcVideoTask": "场景化 AIGC 生视频",
    "ImportMediaKnowledge": "导入媒体知识",
    "ExtractBlindWatermark": "提取数字水印",
    "CreateAigcAdvancedCustomElement": "创建自定义主体",
    "CreateAigcCustomVoiceTask": "创建自定义音色",
    "CreateAigcSubjectTask": "创建主体",
}

REVIEW_SUGGESTION_MAP = {"pass": "通过", "review": "建议人工复审", "block": "建议封禁"}
WECHAT_STATUS_MAP = {
    "FAIL": "发布失败",
    "SUCCESS": "发布成功",
    "AUDITNOTPASS": "审核未通过",
    "NOTTRIGGERED": "尚未发起发布",
}


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def fmt_status(status):
    return STATUS_MAP.get(status, status) if status else ""


def fmt_task_type(task_type):
    return TASK_TYPE_MAP.get(task_type, task_type)


def _err(t, prefix=""):
    """打印错误码/错误信息（若有）"""
    err = t.get("ErrCodeExt") or ""
    if not err and t.get("ErrCode"):
        err = str(t["ErrCode"])
    if err:
        print(f"{prefix}错误: {err} - {t.get('Message', '')}")


def _file_output(label, file_id=None, file_url=None, file_type=None, prefix=""):
    """统一打印文件输出信息"""
    if file_id:
        print(f"{prefix}{label} FileId: {file_id}")
    if file_url:
        print(f"{prefix}{label} URL: {file_url}")
    if file_type:
        print(f"{prefix}{label} 类型: {file_type}")


def _print_file_infos(file_infos, label="输出文件", max_show=3, prefix="  "):
    """打印 FileInfos 列表（AIGC 任务通用）"""
    if not file_infos:
        return
    print(f"{prefix}{label}: {len(file_infos)} 个")
    for i, fi in enumerate(file_infos[:max_show]):
        storage = fi.get("StorageMode", "")
        ftype = fi.get("FileType", "")
        furl = fi.get("FileUrl", "")
        fid = fi.get("FileId", "")
        name = fi.get("MediaName", "")
        parts = []
        if ftype:
            parts.append(ftype)
        if storage:
            parts.append(f"[{storage}]")
        if name:
            parts.append(name)
        print(f"{prefix}  [{i+1}] {' '.join(parts)}")
        if fid:
            print(f"{prefix}       FileId: {fid}")
        if furl:
            print(f"{prefix}       URL: {furl}")
    if len(file_infos) > max_show:
        print(f"{prefix}  ... 共 {len(file_infos)} 个，使用 --json 查看全部")


# ── 各 TaskType 打印函数 ───────────────────────────────────────────────────────

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def _print_procedure(t, verbose):
    """Procedure: 视频处理任务"""
    if t.get("FileId"):
        print(f"  文件 ID: {t['FileId']}")
    if t.get("FileName"):
        print(f"  文件名: {t['FileName']}")
    if t.get("FileUrl"):
        print(f"  文件 URL: {t['FileUrl']}")
    _err(t, "  ")

    # 媒体处理子任务
    media_results = t.get("MediaProcessResultSet") or []
    if media_results:
        print(f"  媒体处理子任务: {len(media_results)} 个")
        SUB_TASK_KEY = {  # NOCA:invalid-name(naming follows SDK convention)
            "Transcode": "TranscodeTask",
            "AnimatedGraphics": "AnimatedGraphicTask",
            "SnapshotByTimeOffset": "SnapshotByTimeOffsetTask",
            "SampleSnapshot": "SampleSnapshotTask",
            "ImageSprites": "ImageSpriteTask",
            "CoverBySnapshot": "CoverBySnapshotTask",
            "AdaptiveDynamicStreaming": "AdaptiveDynamicStreamingTask",
        }
        for item in media_results:
            sub_type = item.get("Type", "")
            key = SUB_TASK_KEY.get(sub_type, sub_type + "Task")
            sub_task = item.get(key) or {}
            sub_status = sub_task.get("Status", "")
            progress = sub_task.get("Progress")
            prog_str = f" ({progress}%)" if progress is not None and sub_status == "PROCESSING" else ""
            print(f"    - {sub_type}: {fmt_status(sub_status)}{prog_str}")
            _err(sub_task, "      ")
            if verbose and sub_task.get("Output"):
                out = sub_task["Output"]
                if sub_type == "Transcode" and out.get("Url"):
                    print(f"      输出 URL: {out['Url']}")
                    if out.get("Definition"):
                        print(f"      模板: {out['Definition']}  {out.get('Width', '?')}x{out.get('Height', '?')}  {out.get('Bitrate', '?')}bps")  # NOCA:line-too-long(long SDK parameter or URL string)
                elif sub_type == "AnimatedGraphics" and out.get("Url"):
                    print(f"      动图 URL: {out['Url']}  ({out.get('Container', '')}, {out.get('Width', '?')}x{out.get('Height', '?')})")  # NOCA:line-too-long(long SDK parameter or URL string)
                elif sub_type == "SnapshotByTimeOffset":
                    pics = out.get("PicInfoSet") or []
                    print(f"      截图: {len(pics)} 张")
                    for p in pics[:3]:
                        print(f"        [{p.get('TimeOffset', 0)/1000:.1f}s] {p.get('Url', '')}")
                elif sub_type == "SampleSnapshot":
                    urls = out.get("ImageUrlSet") or []
                    print(f"      采样截图: {len(urls)} 张")
                    for u in urls[:3]:
                        print(f"        {u}")
                elif sub_type == "ImageSprites":
                    urls = out.get("ImageUrlSet") or []
                    print(f"      雪碧图: {len(urls)} 张大图，共 {out.get('TotalCount', '?')} 小图")
                    if out.get("WebVttUrl"):
                        print(f"      WebVtt: {out['WebVttUrl']}")
                elif sub_type == "CoverBySnapshot" and out.get("CoverUrl"):
                    print(f"      封面 URL: {out['CoverUrl']}")
                elif sub_type == "AdaptiveDynamicStreaming" and out.get("Url"):
                    print(f"      播放地址: {out['Url']}  ({out.get('Package', '')})")

    # AI 分析/识别/审核子任务
    for field, label in [
        ("AiAnalysisResultSet", "AI 分析"),
        ("AiRecognitionResultSet", "AI 识别"),
    ]:
        results = t.get(field) or []
        if results:
            print(f"  {label}子任务: {len(results)} 个")
            for item in results:
                itype = item.get("Type", "")
                sub = item.get(itype + "Task") or {}
                print(f"    - {itype}: {fmt_status(sub.get('Status', ''))}")
                _err(sub, "      ")

    if t.get("ProcedureTaskId"):
        print(f"  关联 Procedure 任务: {t['ProcedureTaskId']}")
    if t.get("ReviewAudioVideoTaskId"):
        print(f"  关联审核任务: {t['ReviewAudioVideoTaskId']}")


def _print_edit_media(t, verbose):
    """EditMedia: 视频编辑任务"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  进度: {progress}%")
    out = t.get("Output") or {}
    if out.get("FileId"):
        print(f"  输出 FileId: {out['FileId']}")
    if out.get("FileUrl"):
        print(f"  输出 URL: {out['FileUrl']}")
    if out.get("FileType"):
        print(f"  输出类型: {out['FileType']}")
    if out.get("MediaName"):
        print(f"  输出文件名: {out['MediaName']}")
    if t.get("ProcedureTaskId"):
        print(f"  关联 Procedure 任务: {t['ProcedureTaskId']}")
    if t.get("ReviewAudioVideoTaskId"):
        print(f"  关联审核任务: {t['ReviewAudioVideoTaskId']}")
    if verbose:
        inp = t.get("Input") or {}
        if inp.get("InputType"):
            print(f"  输入类型: {inp['InputType']}")
        files = inp.get("FileInfoSet") or []
        if files:
            print(f"  输入文件: {len(files)} 个")
            for f in files:
                print(f"    FileId={f.get('FileId', '')}  [{f.get('StartTimeOffset', 0)}s ~ {f.get('EndTimeOffset', '末尾')}s]")  # NOCA:line-too-long(long SDK parameter or URL string)


def _print_split_media(t, verbose):
    """SplitMedia: 视频拆条任务"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  进度: {progress}%")
    if t.get("FileId"):
        print(f"  源文件 ID: {t['FileId']}")
    outputs = t.get("OutputSet") or []
    if outputs:
        print(f"  输出片段: {len(outputs)} 个")
        for i, o in enumerate(outputs[:5]):
            task = o.get("SplitMediaTask") or {}
            out = task.get("Output") or {}
            status = fmt_status(task.get("Status", ""))
            fid = out.get("FileId", "")
            furl = out.get("FileUrl", "")
            print(f"    [{i+1}] {status}  FileId={fid}")
            if verbose and furl:
                print(f"         URL: {furl}")
        if len(outputs) > 5:
            print(f"    ... 共 {len(outputs)} 个")


def _print_compose_media(t, verbose):
    """ComposeMedia: 制作媒体文件任务"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  进度: {progress}%")
    out = t.get("Output") or {}
    if out.get("FileId"):
        print(f"  输出 FileId: {out['FileId']}")
    if out.get("FileUrl"):
        print(f"  输出 URL: {out['FileUrl']}")
    if out.get("FileType"):
        print(f"  输出类型: {out['FileType']}")


def _print_wechat_publish(t, verbose):
    """WechatPublish: 微信发布任务"""
    wechat_status = t.get("WechatStatus", "")
    print(f"  微信发布状态: {WECHAT_STATUS_MAP.get(wechat_status, wechat_status)}")
    if t.get("FileId"):
        print(f"  文件 ID: {t['FileId']}")
    if t.get("WechatVid"):
        print(f"  微信 Vid: {t['WechatVid']}")
    if t.get("WechatUrl"):
        print(f"  微信地址: {t['WechatUrl']}")
    if t.get("ErrCode") and t["ErrCode"] != 0:
        print(f"  错误: {t['ErrCode']} - {t.get('Message', '')}")


def _print_wechat_mini_program(t, verbose):
    """WechatMiniProgramPublish: 微信小程序视频发布任务"""
    _err(t, "  ")
    if t.get("FileId"):
        print(f"  文件 ID: {t['FileId']}")
    pub_result = t.get("PublishResult") or {}
    if pub_result:
        print(f"  发布状态: {pub_result.get('Status', '')}")
        if pub_result.get("ErrCode") and pub_result["ErrCode"] != 0:
            print(f"  发布错误: {pub_result['ErrCode']} - {pub_result.get('Message', '')}")
        if pub_result.get("Vid"):
            print(f"  微信 Vid: {pub_result['Vid']}")


def _print_pull_upload(t, verbose):
    """PullUpload: 拉取上传任务"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  进度: {progress}%")
    if t.get("FileId"):
        print(f"  文件 ID: {t['FileId']}")
    if t.get("FileUrl"):
        print(f"  播放地址: {t['FileUrl']}")
    basic = t.get("MediaBasicInfo") or {}
    if basic.get("Name"):
        print(f"  媒体名称: {basic['Name']}")
    if basic.get("MediaUrl"):
        print(f"  媒体 URL: {basic['MediaUrl']}")
    if basic.get("CoverUrl") and verbose:
        print(f"  封面 URL: {basic['CoverUrl']}")
    if t.get("ProcedureTaskId"):
        print(f"  关联 Procedure 任务: {t['ProcedureTaskId']}")
    if t.get("ReviewAudioVideoTaskId"):
        print(f"  关联审核任务: {t['ReviewAudioVideoTaskId']}")
    if verbose:
        meta = t.get("MetaData") or {}
        if meta.get("Duration"):
            print(f"  时长: {meta['Duration']:.1f}s  {meta.get('Width', '?')}x{meta.get('Height', '?')}  {meta.get('Bitrate', '?')}bps")  # NOCA:line-too-long(long SDK parameter or URL string)


def _print_remove_watermark(t, verbose):
    """RemoveWatermarkTask: 智能去除水印任务"""
    _err(t, "  ")
    out = t.get("Output") or {}
    _file_output("输出", out.get("FileId"), out.get("FileUrl"), out.get("FileType"), "  ")
    if out.get("MediaName"):
        print(f"  输出文件名: {out['MediaName']}")


def _print_rebuild_media(t, verbose):
    """RebuildMedia: 音画质重生任务（旧）"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  进度: {progress}%")
    inp = t.get("Input") or {}
    if inp.get("FileId"):
        print(f"  源文件 ID: {inp['FileId']}")
    out = t.get("Output") or {}
    _file_output("输出", out.get("FileId"), out.get("FileUrl"), out.get("FileType"), "  ")
    if out.get("MediaName"):
        print(f"  输出文件名: {out['MediaName']}")


def _print_extract_trace_watermark(t, verbose):
    """ExtractTraceWatermark: 提取溯源水印任务"""
    _err(t, "  ")
    inp = t.get("Input") or {}
    if inp.get("FileId"):
        print(f"  源文件 ID: {inp['FileId']}")
    out = t.get("Output") or {}
    if out.get("Uv"):
        print(f"  溯源水印 UV (播放者 ID): {out['Uv']}")
    else:
        print("  未提取到溯源水印")


def _print_extract_copyright_watermark(t, verbose):
    """ExtractCopyRightWatermark: 提取版权水印任务"""
    _err(t, "  ")
    inp = t.get("Input") or {}
    if inp.get("Url"):
        print(f"  源 URL: {inp['Url']}")
    out = t.get("Output") or {}
    if out.get("Text"):
        print(f"  版权水印文本: {out['Text']}")
    else:
        print("  未提取到版权水印")


def _print_review_audio_video(t, verbose):
    """ReviewAudioVideo: 音视频审核任务"""
    _err(t, "  ")
    inp = t.get("Input") or {}
    if inp.get("FileId"):
        print(f"  文件 ID: {inp['FileId']}")
    out = t.get("Output") or {}
    suggestion = out.get("Suggestion", "")
    if suggestion:
        print(f"  审核建议: {REVIEW_SUGGESTION_MAP.get(suggestion, suggestion)}")
        if suggestion != "pass":
            label = out.get("Label", "")
            form = out.get("Form", "")
            if label:
                print(f"  违规标签: {label}  形式: {form}")
    # 封面审核
    cover = out.get("CoverReviewResult") or {}
    if cover.get("Suggestion"):
        csugg = cover["Suggestion"]
        print(f"  封面审核建议: {REVIEW_SUGGESTION_MAP.get(csugg, csugg)}")
        if csugg != "pass" and cover.get("Label"):
            print(f"  封面违规标签: {cover['Label']}")
    if verbose:
        segs = out.get("SegmentSet") or []
        if segs:
            print(f"  嫌疑片段: {len(segs)} 个（最多展示10个）")
            for seg in segs[:5]:
                print(f"    [{seg.get('StartTimeOffset', 0):.1f}s~{seg.get('EndTimeOffset', 0):.1f}s] "
                      f"{seg.get('Label', '')} {seg.get('Form', '')} "
                      f"置信度:{seg.get('Confidence', 0):.0f}")
        if out.get("SegmentSetFileUrl"):
            print(f"  完整片段文件: {out['SegmentSetFileUrl']}")


def _print_describe_file_attributes(t, verbose):
    """DescribeFileAttributesTask: 获取文件属性任务"""
    _err(t, "  ")
    if t.get("FileId"):
        print(f"  文件 ID: {t['FileId']}")
    out = t.get("Output") or {}
    if out.get("Md5"):
        print(f"  MD5: {out['Md5']}")


def _print_quality_inspect(t, verbose):
    """QualityInspect: 音画质检测任务"""
    _err(t, "  ")
    inp = t.get("Input") or {}
    if inp.get("FileId"):
        print(f"  文件 ID: {inp['FileId']}")
    out = t.get("Output") or {}
    score = out.get("QualityEvaluationScore")
    if score is not None:
        print(f"  画面质量评分: {score}/100")
    no_audio = out.get("NoAudio")
    no_video = out.get("NoVideo")
    if no_audio is not None:
        print(f"  无音频轨: {'是' if no_audio else '否'}  无视频轨: {'是' if no_video else '否'}")
    issues = out.get("QualityInspectResultSet") or []
    if issues:
        print(f"  检测到异常: {len(issues)} 类")
        for issue in issues:
            itype = issue.get("Type", "")
            segs = issue.get("SegmentSet") or []
            print(f"    - {itype}: {len(segs)} 处")
            if verbose:
                for seg in segs[:3]:
                    print(f"        [{seg.get('StartTimeOffset', 0):.1f}s~{seg.get('EndTimeOffset', 0):.1f}s]")
    else:
        if out:
            print("  未检测到异常")


def _print_quality_enhance(t, verbose):
    """QualityEnhance: 音画质重生任务"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  进度: {progress}%")
    inp = t.get("Input") or {}
    if inp.get("FileId"):
        print(f"  源文件 ID: {inp['FileId']}")
    if inp.get("Definition"):
        print(f"  模板 ID: {inp['Definition']}")
    out = t.get("Output") or {}
    _file_output("输出", out.get("FileId"), out.get("FileUrl"), out.get("FileType"), "  ")
    if out.get("MediaName"):
        print(f"  输出文件名: {out['MediaName']}")


def _print_complex_adaptive_dynamic_streaming(t, verbose):
    """ComplexAdaptiveDynamicStreaming: 复杂自适应码流任务"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  进度: {progress}%")
    if t.get("FileId"):
        print(f"  文件 ID: {t['FileId']}")
    stream_results = t.get("ComplexAdaptiveDynamicStreamingTaskResultSet") or []
    if stream_results:
        print(f"  自适应码流子任务: {len(stream_results)} 个")
        for item in stream_results:
            sub = item.get("ComplexAdaptiveDynamicStreamingTask") or {}
            status = fmt_status(sub.get("Status", ""))
            _err(sub, "    ")
            out = sub.get("Output") or {}
            pkg = out.get("Package", "")
            url = out.get("Url", "")
            print(f"    - {status}  {pkg}  {url[:80] if url else ''}")


def _print_process_media_by_mps(t, verbose):
    """ProcessMediaByMPS: MPS 视频处理任务"""
    _err(t, "  ")
    if t.get("FileId"):
        print(f"  文件 ID: {t['FileId']}")
    if t.get("MpsTaskId"):
        print(f"  MPS 任务 ID: {t['MpsTaskId']}")
    if t.get("Status"):
        print(f"  MPS 任务状态: {fmt_status(t['Status'])}")


def _print_aigc_image(t, verbose, task_type="AigcImageTask"):
    """AigcImageTask / SceneAigcImageTask: AIGC 生图任务"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None and progress < 100:
        print(f"  进度: {progress}%")
    inp = t.get("Input") or {}
    model = inp.get("ModelName", "")
    version = inp.get("ModelVersion", "")
    if model:
        print(f"  模型: {model} {version}".strip())
    if inp.get("Prompt"):
        prompt = inp["Prompt"]
        print(f"  提示词: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    # 场景化生图的场景信息
    if task_type == "SceneAigcImageTask":
        scene = inp.get("SceneInfo") or {}
        if scene.get("Type"):
            print(f"  场景类型: {scene['Type']}")
    out = t.get("Output") or {}
    file_infos = out.get("FileInfos") or []
    if file_infos:
        _print_file_infos(file_infos, "生成图片")
    elif out.get("ResultSet"):
        # 兼容旧格式
        rs = out["ResultSet"]
        print(f"  生成结果: {len(rs)} 张")
        for i, img in enumerate(rs[:3]):
            if img.get("Url"):
                print(f"    [{i+1}] {img['Url']}")


def _print_aigc_video(t, verbose, task_type="AigcVideoTask"):
    """AigcVideoTask / SceneAigcVideoTask: AIGC 生视频任务"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None and progress < 100:
        print(f"  进度: {progress}%")
    inp = t.get("Input") or {}
    model = inp.get("ModelName", "")
    version = inp.get("ModelVersion", "")
    if model:
        print(f"  模型: {model} {version}".strip())
    if inp.get("Prompt"):
        prompt = inp["Prompt"]
        print(f"  提示词: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    # 场景化生视频的场景信息
    if task_type == "SceneAigcVideoTask":
        scene = inp.get("SceneInfo") or {}
        if scene.get("Type"):
            print(f"  场景类型: {scene['Type']}")
    out_cfg = (inp.get("OutputConfig") or {})
    if out_cfg.get("Duration"):
        print(f"  时长: {out_cfg['Duration']}s  分辨率: {out_cfg.get('Resolution', '?')}  宽高比: {out_cfg.get('AspectRatio', '?')}")  # NOCA:line-too-long(long SDK parameter or URL string)
    out = t.get("Output") or {}
    file_infos = out.get("FileInfos") or []
    if file_infos:
        _print_file_infos(file_infos, "生成视频")
    elif out.get("FileId") or out.get("FileUrl"):
        # 兼容旧格式
        _file_output("输出视频", out.get("FileId"), out.get("FileUrl"), prefix="  ")


def _print_import_media_knowledge(t, verbose):
    """ImportMediaKnowledge: 导入媒体知识任务"""
    if t.get("ErrCode") and t["ErrCode"] != 0:
        print(f"  错误: {t['ErrCode']} - {t.get('Message', '')}")


def _print_extract_blind_watermark(t, verbose):
    """ExtractBlindWatermark: 提取数字水印任务"""
    if t.get("ErrCode") and t["ErrCode"] != 0:
        print(f"  错误: {t['ErrCode']} - {t.get('Message', '')}")
    wtype = t.get("Type", "")
    if wtype:
        print(f"  水印类型: {wtype}")
    detected = t.get("IsDetected")
    if detected is not None:
        print(f"  检测到水印: {'是' if detected else '否'}")
    if t.get("Result"):
        print(f"  水印内容: {t['Result']}")
    if t.get("ResultUV"):
        print(f"  溯源 UV: {t['ResultUV']}")
    inp = t.get("InputInfo") or {}
    if inp.get("FileId"):
        print(f"  源文件 ID: {inp['FileId']}")
    elif inp.get("Url"):
        print(f"  源 URL: {inp['Url']}")


def _print_create_aigc_advanced_custom_element(t, verbose, task_id=None):
    """CreateAigcAdvancedCustomElementTask: 创建自定义主体任务"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None and progress < 100:
        print(f"  进度: {progress}%")
    inp = t.get("Input") or {}
    if inp.get("ElementName"):
        print(f"  主体名称: {inp['ElementName']}")
    if inp.get("ReferenceType"):
        print(f"  参考方式: {inp['ReferenceType']}")
    out = t.get("Output") or {}
    info_list = out.get("InfoList") or []
    if info_list:
        print(f"  创建主体: {len(info_list)} 个")
        for item in info_list:
            print(f"    ElementId: {item.get('ElementId', '')}")
            if verbose and item.get("ElementInfo"):
                print(f"    ElementInfo: {item['ElementInfo'][:200]}")
        # 自动持久化到 mem/<task_id>/elements.json
        if task_id:
            saved_path = _save_elements(task_id, info_list)
            if saved_path:
                print(f"  ✅ 主体已保存: {saved_path}")


def _print_create_aigc_custom_voice(t, verbose):
    """CreateAigcCustomVoiceTask: 创建自定义音色任务"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None and progress < 100:
        print(f"  进度: {progress}%")
    inp = t.get("Input") or {}
    if inp.get("VoiceName"):
        print(f"  音色名称: {inp['VoiceName']}")
    out = t.get("Output") or {}
    info_list = out.get("InfoList") or []
    if info_list:
        print(f"  创建音色: {len(info_list)} 个")
        for item in info_list:
            print(f"    VoiceId: {item.get('VoiceId', '')}")
            if verbose and item.get("VoiceInfo"):
                print(f"    VoiceInfo: {item['VoiceInfo'][:200]}")


def _print_create_aigc_subject(t, verbose):
    """CreateAigcSubjectTask: 创建主体任务"""
    _err(t, "  ")
    inp = t.get("Input") or {}
    if inp.get("SubjectName"):
        print(f"  主体名称: {inp['SubjectName']}")
    if inp.get("VoiceId"):
        print(f"  音色 ID: {inp['VoiceId']}")
    out = t.get("Output") or {}
    if out.get("SubjectId"):
        print(f"  主体 ID: {out['SubjectId']}")
    if verbose and out.get("SubjectInfo"):
        print(f"  主体信息: {out['SubjectInfo'][:300]}")


# ── 主打印入口 ────────────────────────────────────────────────────────────────

# TaskType -> (response_field, handler_func)
_TASK_HANDLERS = {
    "Procedure":                         ("ProcedureTask",                          _print_procedure),
    "EditMedia":                         ("EditMediaTask",                           _print_edit_media),
    "SplitMedia":                        ("SplitMediaTask",                          _print_split_media),
    "ComposeMedia":                      ("ComposeMediaTask",                        _print_compose_media),
    "WechatPublish":                     ("WechatPublishTask",                       _print_wechat_publish),
    "WechatMiniProgramPublish":          ("WechatMiniProgramPublishTask",            _print_wechat_mini_program),
    "PullUpload":                        ("PullUploadTask",                          _print_pull_upload),
    "FastClipMedia":                     ("FastClipMediaTask",                       None),  # 暂无专用 handler，使用 --json 查看完整响应  # NOCA:line-too-long(long SDK parameter or URL string)
    "RemoveWatermarkTask":               ("RemoveWatermarkTask",                     _print_remove_watermark),
    "RebuildMedia":                      ("RebuildMediaTask",                        _print_rebuild_media),
    "ExtractTraceWatermark":             ("ExtractTraceWatermarkTask",               _print_extract_trace_watermark),
    "ExtractCopyRightWatermark":         ("ExtractCopyRightWatermarkTask",           _print_extract_copyright_watermark),  # NOCA:line-too-long(long SDK parameter or URL string)
    "ReviewAudioVideo":                  ("ReviewAudioVideoTask",                    _print_review_audio_video),
    "DescribeFileAttributesTask":        ("DescribeFileAttributesTask",              _print_describe_file_attributes),
    "QualityInspect":                    ("QualityInspectTask",                      _print_quality_inspect),
    "QualityEnhance":                    ("QualityEnhanceTask",                      _print_quality_enhance),
    "ComplexAdaptiveDynamicStreaming":   ("ComplexAdaptiveDynamicStreamingTask",     _print_complex_adaptive_dynamic_streaming),  # NOCA:line-too-long(long SDK parameter or URL string)
    "ProcessMediaByMPS":                 ("ProcessMediaByMPSTask",                   _print_process_media_by_mps),
    "AigcImageTask":                     ("AigcImageTask",                           lambda t, v: _print_aigc_image(t, v, "AigcImageTask")),  # NOCA:line-too-long(long SDK parameter or URL string)
    "SceneAigcImageTask":                ("SceneAigcImageTask",                      lambda t, v: _print_aigc_image(t, v, "SceneAigcImageTask")),  # NOCA:line-too-long(long SDK parameter or URL string)
    "AigcVideoTask":                     ("AigcVideoTask",                           lambda t, v: _print_aigc_video(t, v, "AigcVideoTask")),  # NOCA:line-too-long(long SDK parameter or URL string)
    "SceneAigcVideoTask":                ("SceneAigcVideoTask",                      lambda t, v: _print_aigc_video(t, v, "SceneAigcVideoTask")),  # NOCA:line-too-long(long SDK parameter or URL string)
    "ImportMediaKnowledge":              ("ImportMediaKnowledge",                    _print_import_media_knowledge),
    "ExtractBlindWatermark":             ("ExtractBlindWatermarkTask",               _print_extract_blind_watermark),
    "CreateAigcAdvancedCustomElement": ("CreateAigcAdvancedCustomElementTask",   None),  # 特殊处理，需要 task_id
    "CreateAigcCustomVoiceTask":         ("CreateAigcCustomVoiceTask",               _print_create_aigc_custom_voice),
    "CreateAigcSubjectTask":             ("CreateAigcSubjectTask",                   _print_create_aigc_subject),
}


def print_summary(result, verbose=False, task_id=None):
    """打印任务摘要信息（支持所有 TaskType）"""
    task_type = result.get("TaskType", "未知")
    status = result.get("Status", "未知")
    create_time = result.get("CreateTime", "")
    begin_time = result.get("BeginProcessTime", "")
    finish_time = result.get("FinishTime", "")
    # 优先使用传入的 task_id，否则从结果中提取
    _task_id = task_id or result.get("TaskId", "")

    print(f"任务类型: {fmt_task_type(task_type)} ({task_type})")
    print(f"任务状态: {fmt_status(status)}")
    if create_time:
        print(f"创建时间: {create_time}")
    if begin_time:
        print(f"开始时间: {begin_time}")
    if finish_time:
        print(f"完成时间: {finish_time}")

    # 分派到对应的处理函数
    handler_info = _TASK_HANDLERS.get(task_type)
    if handler_info:
        field, handler = handler_info
        task_data = result.get(field)
        if task_data:
            # CreateAigcAdvancedCustomElement 需要特殊处理（传入 task_id）
            if task_type == "CreateAigcAdvancedCustomElement":
                _print_create_aigc_advanced_custom_element(task_data, verbose, task_id=_task_id)
            elif handler is not None:
                handler(task_data, verbose)
            else:
                print(f"  （{task_type} 暂无详细解析，请使用 --json 查看完整响应）")
        else:
            print(f"  （{field} 字段为空）")
    else:
        # 未知任务类型，尝试打印所有非空的顶层字段
        print(f"  （未知任务类型，请使用 --json 查看完整响应）")


# ── 查询/等待逻辑 ─────────────────────────────────────────────────────────────

def describe_task(args):
    """查询任务详情（单次）"""
    client = get_client(args.region)

    req_body = {"TaskId": args.task_id}
    if args.sub_app_id:
        req_body["SubAppId"] = args.sub_app_id

    try:
        # 使用 call_json 而非 SDK 模型方法，避免旧版 SDK to_json_string() 丢失未知字段
        resp = client.call_json("DescribeTaskDetail", req_body)
        result = resp.get("Response", resp)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result

        print(f"=== 任务详情 ===")
        print(f"TaskId: {args.task_id}")
        print_summary(result, verbose=args.verbose, task_id=args.task_id)

        if args.verbose:
            print("\n=== 完整响应 ===")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        print(f"查询失败: {e}")
        sys.exit(1)


def wait_for_task(args):
    """轮询等待任务完成"""
    client = get_client(args.region)

    print(f"等待任务完成 (TaskId: {args.task_id})...")
    print(f"最大等待时间: {args.max_wait}s，轮询间隔: {args.interval}s")
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed >= args.max_wait:
            print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
            sys.exit(1)

        req_body = {"TaskId": args.task_id}
        if args.sub_app_id:
            req_body["SubAppId"] = args.sub_app_id

        try:
            # 使用 call_json 避免旧版 SDK to_json_string() 丢失未知字段
            resp = client.call_json("DescribeTaskDetail", req_body)
            result = resp.get("Response", resp)

            status = result.get("Status", "PROCESSING")
            elapsed_str = f"{elapsed:.0f}s"
            print(f"  [{elapsed_str}] 状态: {fmt_status(status)}")

            if status == "FINISH":
                print("\n✅ 任务完成!")
                print_summary(result, verbose=args.verbose, task_id=args.task_id)
                if args.json:
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                return result

            elif status in ("ABORTED", "FAIL"):
                print(f"\n❌ 任务{fmt_status(status)}!")
                print_summary(result, verbose=True, task_id=args.task_id)
                if args.json:
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                sys.exit(1)

            time.sleep(args.interval)

        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
            print(f"  查询失败: {e}，{args.interval}s 后重试...")
            time.sleep(args.interval)


# ── CLI 入口 ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="VOD 任务详情查询工具 - 查询任务执行状态和结果（最多查询3天内的任务）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查询任务状态
  python vod_describe_task.py --task-id 1490013579-procedurev2-acd135

  # 等待任务完成（最多等 10 分钟）
  # 默认等待任务完成
  python vod_describe_task.py --task-id 1490013579-procedurev2-acd135
  
  # 仅查询当前状态，不等待
  python vod_describe_task.py --task-id 1490013579-procedurev2-acd135 --no-wait

  # JSON 格式输出完整响应
  python vod_describe_task.py --task-id 1490013579-procedurev2-acd135 --json

  # 详细输出（含输出 URL 等）
  python vod_describe_task.py --task-id 1490013579-procedurev2-acd135 --verbose

  # 指定子应用 ID
  python vod_describe_task.py --task-id 1490013579-procedurev2-acd135 --sub-app-id 1500046806

任务状态说明:
  WAITING    - 等待中
  PROCESSING - 处理中
  FINISH     - 已完成
  ABORTED    - 已终止
  FAIL       - 失败（子任务级别状态）
  SUCCESS    - 成功（子任务级别状态）
        """
    )

    parser.add_argument("--task-id", required=True, help="任务 ID，例如: 1490013579-procedurev2-acd135")
    parser.add_argument(
        "--sub-app-id",
        type=int,
        default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
        help="子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）",
    )
    parser.add_argument("--region", default="ap-guangzhou", help="地域（默认: ap-guangzhou）")
    parser.add_argument("--no-wait", action="store_true", help="仅查询当前状态，不等待完成")
    parser.add_argument("--max-wait", type=int, default=600, help="最大等待时间，单位秒（默认: 600）")
    parser.add_argument("--interval", type=int, default=5, help="轮询间隔，单位秒（默认: 5）")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出完整响应")
    parser.add_argument("-v", "--verbose", action="store_true", help="输出详细信息（含输出 URL 等）")

    args = parser.parse_args()

    if not args.no_wait:
        wait_for_task(args)
    else:
        describe_task(args)


if __name__ == "__main__":
    main()
