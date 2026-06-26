
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD Task Detail Query Script
Query the execution status and detailed results of a task by task ID (supports tasks submitted within the last 3 days).

Supported task types (full list):
  Procedure            Video processing task
  EditMedia            Video editing task
  SplitMedia           Video splitting task
  ComposeMedia         Media composition task
  WechatPublish        WeChat publish task
  WechatMiniProgramPublish  WeChat Mini Program publish task
  PullUpload           Pull upload task
  FastClipMedia        Fast clip task
  RemoveWatermarkTask  Intelligent watermark removal task
  DescribeFileAttributesTask  Get file attributes task
  RebuildMedia         Audio/video quality restoration task (legacy)
  ReviewAudioVideo     Audio/video review task
  ExtractTraceWatermark  Extract trace watermark task
  ExtractCopyRightWatermark  Extract copyright watermark task
  QualityInspect       Audio/video quality inspection task
  QualityEnhance       Audio/video quality enhancement task
  ComplexAdaptiveDynamicStreaming  Complex adaptive bitrate streaming task
  ProcessMediaByMPS    MPS video processing task
  AigcImageTask        AIGC image generation task
  SceneAigcImageTask   Scene-based AIGC image generation task
  AigcVideoTask        AIGC video generation task
  SceneAigcVideoTask   Scene-based AIGC video generation task
  ImportMediaKnowledge Import media knowledge task
  ExtractBlindWatermark  Extract digital watermark task
  CreateAigcAdvancedCustomElement  Create custom subject task
  CreateAigcCustomVoiceTask  Create custom voice task
  CreateAigcSubjectTask  Create subject task

API documentation: https://cloud.tencent.com/document/api/266/33431
"""

import os
import sys
import json
import argparse
import time


# ── Subject element persistence ───────────────────────────────────────────────

def _save_elements(task_id, info_list):
    """
    Merge the output results of CreateAigcAdvancedCustomElementTask into
    the record matching task_id in mem/elements.json (request + result combined).
    If no matching record is found, create a new one.
    """
    if not info_list:
        return None

    mem_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "mem", "elements.json",
    )
    os.makedirs(os.path.dirname(mem_path), exist_ok=True)

    # Read existing list
    elements = []
    if os.path.exists(mem_path):
        try:
            with open(mem_path, "r", encoding="utf-8") as f:
                elements = json.load(f)
            if not isinstance(elements, list):
                elements = []
        except Exception:
            elements = []

    # Find the record matching task_id and merge results
    matched = False
    for rec in elements:
        if rec.get("task_id") == task_id:
            rec["result"] = {
                "element_count": len(info_list),
                "info_list": info_list,
            }
            matched = True
            break

    # If not found, append a new record (result only)
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


try:
    from vod_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False

try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.vod.v20180717 import vod_client, models
except ImportError:
    print("Error: Please install the Tencent Cloud SDK first: pip install tencentcloud-sdk-python")
    sys.exit(1)


def get_credential():
    """Retrieve Tencent Cloud credentials"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        # Fallback: try to load credentials from ~/.env etc.
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] Environment variables not set, attempting to load from dotenv files...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from vod_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print("Error: Please set environment variables TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
            sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def get_client(region="ap-guangzhou"):
    """Get the VOD client"""
    cred = get_credential()
    http_profile = HttpProfile()
    http_profile.endpoint = "vod.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return vod_client.VodClient(cred, region, client_profile)


# ── Constant mappings ─────────────────────────────────────────────────────────

STATUS_MAP = {
    "WAITING": "Waiting",
    "PROCESSING": "Processing",
    "FINISH": "Completed",
    "ABORTED": "Aborted",
    "FAIL": "Failed",
    "SUCCESS": "Succeeded",
}

TASK_TYPE_MAP = {
    "Procedure": "Video Processing",
    "EditMedia": "Video Editing",
    "SplitMedia": "Video Splitting",
    "ComposeMedia": "Media Composition",
    "WechatPublish": "WeChat Publish",
    "WechatMiniProgramPublish": "WeChat Mini Program Publish",
    "PullUpload": "Pull Upload",
    "FastClipMedia": "Fast Clip",
    "RemoveWatermarkTask": "Intelligent Watermark Removal",
    "DescribeFileAttributesTask": "Get File Attributes",
    "RebuildMedia": "Audio/Video Quality Restoration (Legacy)",
    "ReviewAudioVideo": "Audio/Video Review",
    "ExtractTraceWatermark": "Extract Trace Watermark",
    "ExtractCopyRightWatermark": "Extract Copyright Watermark",
    "QualityInspect": "Audio/Video Quality Inspection",
    "QualityEnhance": "Audio/Video Quality Enhancement",
    "ComplexAdaptiveDynamicStreaming": "Complex Adaptive Bitrate Streaming",
    "ProcessMediaByMPS": "MPS Video Processing",
    "AigcImageTask": "AIGC Image Generation",
    "SceneAigcImageTask": "Scene-based AIGC Image Generation",
    "AigcVideoTask": "AIGC Video Generation",
    "SceneAigcVideoTask": "Scene-based AIGC Video Generation",
    "ImportMediaKnowledge": "Import Media Knowledge",
    "ExtractBlindWatermark": "Extract Digital Watermark",
    "CreateAigcAdvancedCustomElement": "Create Custom Subject",
    "CreateAigcCustomVoiceTask": "Create Custom Voice",
    "CreateAigcSubjectTask": "Create Subject",
}

REVIEW_SUGGESTION_MAP = {"pass": "Passed", "review": "Recommended for Manual Review", "block": "Recommended for Blocking"}
WECHAT_STATUS_MAP = {
    "FAIL": "Publish Failed",
    "SUCCESS": "Publish Successful",
    "AUDITNOTPASS": "Audit Not Passed",
    "NOTTRIGGERED": "Publish Not Yet Initiated",
}


# ── Utility functions ─────────────────────────────────────────────────────────

def fmt_status(status):
    return STATUS_MAP.get(status, status) if status else ""


def fmt_task_type(task_type):
    return TASK_TYPE_MAP.get(task_type, task_type)


def _err(t, prefix=""):
    """Print error code/message if present"""
    err = t.get("ErrCodeExt") or ""
    if not err and t.get("ErrCode"):
        err = str(t["ErrCode"])
    if err:
        print(f"{prefix}Error: {err} - {t.get('Message', '')}")


def _file_output(label, file_id=None, file_url=None, file_type=None, prefix=""):
    """Print file output information in a unified format"""
    if file_id:
        print(f"{prefix}{label} FileId: {file_id}")
    if file_url:
        print(f"{prefix}{label} URL: {file_url}")
    if file_type:
        print(f"{prefix}{label} Type: {file_type}")


def _print_file_infos(file_infos, label="Output files", max_show=3, prefix="  "):
    """Print FileInfos list (common for AIGC tasks)"""
    if not file_infos:
        return
    print(f"{prefix}{label}: {len(file_infos)} item(s)")
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
        print(f"{prefix}  ... {len(file_infos)} item(s) total, use --json to view all")


# ── Per-Task Type print functions ──────────────────────────────────────────────

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def _print_procedure(t, verbose):
    """Procedure: Video processing task"""
    if t.get("FileId"):
        print(f"  File ID: {t['FileId']}")
    if t.get("FileName"):
        print(f"  File name: {t['FileName']}")
    if t.get("FileUrl"):
        print(f"  File URL: {t['FileUrl']}")
    _err(t, "  ")

    # Media processing sub-tasks
    media_results = t.get("MediaProcessResultSet") or []
    if media_results:
        print(f"  Media processing sub-tasks: {len(media_results)} item(s)")
        SUB_TASK_KEY = {  # NOCA:invalid-name(SUB_TASK_KEY is a local dict constant, renaming would reduce readability)
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
                    print(f"      Output URL: {out['Url']}")
                    if out.get("Definition"):
                        print(f"      Template: {out['Definition']}  {out.get('Width', '?')}x{out.get('Height', '?')}  {out.get('Bitrate', '?')}bps")  # NOCA:line-too-long(long output string or URL, cannot be shortened)
                elif sub_type == "AnimatedGraphics" and out.get("Url"):
                    print(f"      Animated image URL: {out['Url']}  ({out.get('Container', '')}, {out.get('Width', '?')}x{out.get('Height', '?')})")  # NOCA:line-too-long(long output string or URL, cannot be shortened)
                elif sub_type == "SnapshotByTimeOffset":
                    pics = out.get("PicInfoSet") or []
                    print(f"      Snapshots: {len(pics)} image(s)")
                    for p in pics[:3]:
                        print(f"        [{p.get('TimeOffset', 0)/1000:.1f}s] {p.get('Url', '')}")
                elif sub_type == "SampleSnapshot":
                    urls = out.get("ImageUrlSet") or []
                    print(f"      Sample snapshots: {len(urls)} image(s)")
                    for u in urls[:3]:
                        print(f"        {u}")
                elif sub_type == "ImageSprites":
                    urls = out.get("ImageUrlSet") or []
                    print(f"      Image sprites: {len(urls)} large image(s), {out.get('TotalCount', '?')} thumbnails total")  # NOCA:line-too-long(long output string or URL, cannot be shortened)
                    if out.get("WebVttUrl"):
                        print(f"      WebVtt: {out['WebVttUrl']}")
                elif sub_type == "CoverBySnapshot" and out.get("CoverUrl"):
                    print(f"      Cover URL: {out['CoverUrl']}")
                elif sub_type == "AdaptiveDynamicStreaming" and out.get("Url"):
                    print(f"      Playback URL: {out['Url']}  ({out.get('Package', '')})")

    # AI analysis / recognition / review sub-tasks
    for field, label in [
        ("AiAnalysisResultSet", "AI analysis"),
        ("AiRecognitionResultSet", "AI recognition"),
    ]:
        results = t.get(field) or []
        if results:
            print(f"  {label} sub-tasks: {len(results)} item(s)")
            for item in results:
                itype = item.get("Type", "")
                sub = item.get(itype + "Task") or {}
                print(f"    - {itype}: {fmt_status(sub.get('Status', ''))}")
                _err(sub, "      ")

    if t.get("ProcedureTaskId"):
        print(f"  Associated Procedure task: {t['ProcedureTaskId']}")
    if t.get("ReviewAudioVideoTaskId"):
        print(f"  Associated review task: {t['ReviewAudioVideoTaskId']}")



def _print_edit_media(t, verbose):
    """EditMedia: Video editing task"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  Progress: {progress}%")
    out = t.get("Output") or {}
    if out.get("FileId"):
        print(f"  Output FileId: {out['FileId']}")
    if out.get("FileUrl"):
        print(f"  Output URL: {out['FileUrl']}")
    if out.get("FileType"):
        print(f"  Output type: {out['FileType']}")
    if out.get("MediaName"):
        print(f"  Output filename: {out['MediaName']}")
    if t.get("ProcedureTaskId"):
        print(f"  Associated Procedure task: {t['ProcedureTaskId']}")
    if t.get("ReviewAudioVideoTaskId"):
        print(f"  Associated review task: {t['ReviewAudioVideoTaskId']}")
    if verbose:
        inp = t.get("Input") or {}
        if inp.get("InputType"):
            print(f"  Input type: {inp['InputType']}")
        files = inp.get("FileInfoSet") or []
        if files:
            print(f"  Input files: {len(files)}")
            for f in files:
                print(f"    FileId={f.get('FileId', '')}  [{f.get('StartTimeOffset', 0)}s ~ {f.get('EndTimeOffset', 'end')}s]")  # NOCA:line-too-long(long output string or URL, cannot be shortened)


def _print_split_media(t, verbose):
    """SplitMedia: Video splitting task"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  Progress: {progress}%")
    if t.get("FileId"):
        print(f"  Source file ID: {t['FileId']}")
    outputs = t.get("OutputSet") or []
    if outputs:
        print(f"  Output segments: {len(outputs)}")
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
            print(f"    ... {len(outputs)} total")


def _print_compose_media(t, verbose):
    """ComposeMedia: Media composition task"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  Progress: {progress}%")
    out = t.get("Output") or {}
    if out.get("FileId"):
        print(f"  Output FileId: {out['FileId']}")
    if out.get("FileUrl"):
        print(f"  Output URL: {out['FileUrl']}")
    if out.get("FileType"):
        print(f"  Output type: {out['FileType']}")


def _print_wechat_publish(t, verbose):
    """WechatPublish: WeChat publish task"""
    wechat_status = t.get("WechatStatus", "")
    print(f"  WeChat publish status: {WECHAT_STATUS_MAP.get(wechat_status, wechat_status)}")
    if t.get("FileId"):
        print(f"  File ID: {t['FileId']}")
    if t.get("WechatVid"):
        print(f"  WeChat Vid: {t['WechatVid']}")
    if t.get("WechatUrl"):
        print(f"  WeChat URL: {t['WechatUrl']}")
    if t.get("ErrCode") and t["ErrCode"] != 0:
        print(f"  Error: {t['ErrCode']} - {t.get('Message', '')}")


def _print_wechat_mini_program(t, verbose):
    """WechatMiniProgramPublish: WeChat Mini Program video publish task"""
    _err(t, "  ")
    if t.get("FileId"):
        print(f"  File ID: {t['FileId']}")
    pub_result = t.get("PublishResult") or {}
    if pub_result:
        print(f"  Publish status: {pub_result.get('Status', '')}")
        if pub_result.get("ErrCode") and pub_result["ErrCode"] != 0:
            print(f"  Publish error: {pub_result['ErrCode']} - {pub_result.get('Message', '')}")
        if pub_result.get("Vid"):
            print(f"  WeChat Vid: {pub_result['Vid']}")


def _print_pull_upload(t, verbose):
    """PullUpload: Pull upload task"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  Progress: {progress}%")
    if t.get("FileId"):
        print(f"  File ID: {t['FileId']}")
    if t.get("FileUrl"):
        print(f"  Playback URL: {t['FileUrl']}")
    basic = t.get("MediaBasicInfo") or {}
    if basic.get("Name"):
        print(f"  Media name: {basic['Name']}")
    if basic.get("MediaUrl"):
        print(f"  Media URL: {basic['MediaUrl']}")
    if basic.get("CoverUrl") and verbose:
        print(f"  Cover URL: {basic['CoverUrl']}")
    if t.get("ProcedureTaskId"):
        print(f"  Associated Procedure task: {t['ProcedureTaskId']}")
    if t.get("ReviewAudioVideoTaskId"):
        print(f"  Associated review task: {t['ReviewAudioVideoTaskId']}")
    if verbose:
        meta = t.get("MetaData") or {}
        if meta.get("Duration"):
            print(f"  Duration: {meta['Duration']:.1f}s  {meta.get('Width', '?')}x{meta.get('Height', '?')}  {meta.get('Bitrate', '?')}bps")  # NOCA:line-too-long(long output string or URL, cannot be shortened)


def _print_remove_watermark(t, verbose):
    """RemoveWatermarkTask: Smart watermark removal task"""
    _err(t, "  ")
    out = t.get("Output") or {}
    _file_output("Output", out.get("FileId"), out.get("FileUrl"), out.get("FileType"), "  ")
    if out.get("MediaName"):
        print(f"  Output filename: {out['MediaName']}")


def _print_rebuild_media(t, verbose):
    """RebuildMedia: Audio/video quality restoration task (legacy)"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  Progress: {progress}%")
    inp = t.get("Input") or {}
    if inp.get("FileId"):
        print(f"  Source file ID: {inp['FileId']}")
    out = t.get("Output") or {}
    _file_output("Output", out.get("FileId"), out.get("FileUrl"), out.get("FileType"), "  ")
    if out.get("MediaName"):
        print(f"  Output filename: {out['MediaName']}")


def _print_extract_trace_watermark(t, verbose):
    """ExtractTraceWatermark: Extract trace watermark task"""
    _err(t, "  ")
    inp = t.get("Input") or {}
    if inp.get("FileId"):
        print(f"  Source file ID: {inp['FileId']}")
    out = t.get("Output") or {}
    if out.get("Uv"):
        print(f"  Trace watermark UV (player ID): {out['Uv']}")
    else:
        print("  No trace watermark extracted")


def _print_extract_copyright_watermark(t, verbose):
    """ExtractCopyRightWatermark: Extract copyright watermark task"""
    _err(t, "  ")
    inp = t.get("Input") or {}
    if inp.get("Url"):
        print(f"  Source URL: {inp['Url']}")
    out = t.get("Output") or {}
    if out.get("Text"):
        print(f"  Copyright watermark text: {out['Text']}")
    else:
        print("  No copyright watermark extracted")


def _print_review_audio_video(t, verbose):
    """ReviewAudioVideo: Audio/video review task"""
    _err(t, "  ")
    inp = t.get("Input") or {}
    if inp.get("FileId"):
        print(f"  File ID: {inp['FileId']}")
    out = t.get("Output") or {}
    suggestion = out.get("Suggestion", "")
    if suggestion:
        print(f"  Review suggestion: {REVIEW_SUGGESTION_MAP.get(suggestion, suggestion)}")
        if suggestion != "pass":
            label = out.get("Label", "")
            form = out.get("Form", "")
            if label:
                print(f"  Violation label: {label}  Form: {form}")
    # Cover review
    cover = out.get("CoverReviewResult") or {}
    if cover.get("Suggestion"):
        csugg = cover["Suggestion"]
        print(f"  Cover review suggestion: {REVIEW_SUGGESTION_MAP.get(csugg, csugg)}")
        if csugg != "pass" and cover.get("Label"):
            print(f"  Cover violation label: {cover['Label']}")
    if verbose:
        segs = out.get("SegmentSet") or []
        if segs:
            print(f"  Suspicious segments: {len(segs)} (showing up to 10)")
            for seg in segs[:5]:
                print(f"    [{seg.get('StartTimeOffset', 0):.1f}s~{seg.get('EndTimeOffset', 0):.1f}s] "
                      f"{seg.get('Label', '')} {seg.get('Form', '')} "
                      f"Confidence:{seg.get('Confidence', 0):.0f}")
        if out.get("SegmentSetFileUrl"):
            print(f"  Full segment file: {out['SegmentSetFileUrl']}")


def _print_describe_file_attributes(t, verbose):
    """DescribeFileAttributesTask: Get file attributes task"""
    _err(t, "  ")
    if t.get("FileId"):
        print(f"  File ID: {t['FileId']}")
    out = t.get("Output") or {}
    if out.get("Md5"):
        print(f"  MD5: {out['Md5']}")


def _print_quality_inspect(t, verbose):
    """QualityInspect: Audio/video quality inspection task"""
    _err(t, "  ")
    inp = t.get("Input") or {}
    if inp.get("FileId"):
        print(f"  File ID: {inp['FileId']}")
    out = t.get("Output") or {}
    score = out.get("QualityEvaluationScore")
    if score is not None:
        print(f"  Video quality score: {score}/100")
    no_audio = out.get("NoAudio")
    no_video = out.get("NoVideo")
    if no_audio is not None:
        print(f"  No audio track: {'Yes' if no_audio else 'No'}  No video track: {'Yes' if no_video else 'No'}")
    issues = out.get("QualityInspectResultSet") or []
    if issues:
        print(f"  Anomalies detected: {len(issues)} type(s)")
        for issue in issues:
            itype = issue.get("Type", "")
            segs = issue.get("SegmentSet") or []
            print(f"    - {itype}: {len(segs)} occurrence(s)")
            if verbose:
                for seg in segs[:3]:
                    print(f"        [{seg.get('StartTimeOffset', 0):.1f}s~{seg.get('EndTimeOffset', 0):.1f}s]")
    else:
        if out:
            print("  No anomalies detected")


def _print_quality_enhance(t, verbose):
    """QualityEnhance: Audio/video quality enhancement task"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  Progress: {progress}%")
    inp = t.get("Input") or {}
    if inp.get("FileId"):
        print(f"  Source file ID: {inp['FileId']}")
    if inp.get("Definition"):
        print(f"  Template ID: {inp['Definition']}")
    out = t.get("Output") or {}
    _file_output("Output", out.get("FileId"), out.get("FileUrl"), out.get("FileType"), "  ")
    if out.get("MediaName"):
        print(f"  Output filename: {out['MediaName']}")



def _print_complex_adaptive_dynamic_streaming(t, verbose):
    """ComplexAdaptiveDynamicStreaming: Complex adaptive bitrate streaming task"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None:
        print(f"  Progress: {progress}%")
    if t.get("FileId"):
        print(f"  File ID: {t['FileId']}")
    stream_results = t.get("ComplexAdaptiveDynamicStreamingTaskResultSet") or []
    if stream_results:
        print(f"  Adaptive bitrate streaming subtasks: {len(stream_results)}")
        for item in stream_results:
            sub = item.get("ComplexAdaptiveDynamicStreamingTask") or {}
            status = fmt_status(sub.get("Status", ""))
            _err(sub, "    ")
            out = sub.get("Output") or {}
            pkg = out.get("Package", "")
            url = out.get("Url", "")
            print(f"    - {status}  {pkg}  {url[:80] if url else ''}")


def _print_process_media_by_mps(t, verbose):
    """ProcessMediaByMPS: MPS video processing task"""
    _err(t, "  ")
    if t.get("FileId"):
        print(f"  File ID: {t['FileId']}")
    if t.get("MpsTaskId"):
        print(f"  MPS Task ID: {t['MpsTaskId']}")
    if t.get("Status"):
        print(f"  MPS task status: {fmt_status(t['Status'])}")


def _print_aigc_image(t, verbose, task_type="AigcImageTask"):
    """AigcImageTask / SceneAigcImageTask: AIGC image generation task"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None and progress < 100:
        print(f"  Progress: {progress}%")
    inp = t.get("Input") or {}
    model = inp.get("ModelName", "")
    version = inp.get("ModelVersion", "")
    if model:
        print(f"  Model: {model} {version}".strip())
    if inp.get("Prompt"):
        prompt = inp["Prompt"]
        print(f"  Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    # Scene information for scene-based image generation
    if task_type == "SceneAigcImageTask":
        scene = inp.get("SceneInfo") or {}
        if scene.get("Type"):
            print(f"  Scene type: {scene['Type']}")
    out = t.get("Output") or {}
    file_infos = out.get("FileInfos") or []
    if file_infos:
        _print_file_infos(file_infos, "Generated images")
    elif out.get("ResultSet"):
        # Compatible with legacy format
        rs = out["ResultSet"]
        print(f"  Generation results: {len(rs)} image(s)")
        for i, img in enumerate(rs[:3]):
            if img.get("Url"):
                print(f"    [{i+1}] {img['Url']}")


def _print_aigc_video(t, verbose, task_type="AigcVideoTask"):
    """AigcVideoTask / SceneAigcVideoTask: AIGC video generation task"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None and progress < 100:
        print(f"  Progress: {progress}%")
    inp = t.get("Input") or {}
    model = inp.get("ModelName", "")
    version = inp.get("ModelVersion", "")
    if model:
        print(f"  Model: {model} {version}".strip())
    if inp.get("Prompt"):
        prompt = inp["Prompt"]
        print(f"  Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    # Scene information for scene-based video generation
    if task_type == "SceneAigcVideoTask":
        scene = inp.get("SceneInfo") or {}
        if scene.get("Type"):
            print(f"  Scene type: {scene['Type']}")
    out_cfg = (inp.get("OutputConfig") or {})
    if out_cfg.get("Duration"):
        print(f"  Duration: {out_cfg['Duration']}s  Resolution: {out_cfg.get('Resolution', '?')}  Aspect ratio: {out_cfg.get('AspectRatio', '?')}")  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    out = t.get("Output") or {}
    file_infos = out.get("FileInfos") or []
    if file_infos:
        _print_file_infos(file_infos, "Generated videos")
    elif out.get("FileId") or out.get("FileUrl"):
        # Compatible with legacy format
        _file_output("Output video", out.get("FileId"), out.get("FileUrl"), prefix="  ")


def _print_import_media_knowledge(t, verbose):
    """ImportMediaKnowledge: Import media knowledge task"""
    if t.get("ErrCode") and t["ErrCode"] != 0:
        print(f"  Error: {t['ErrCode']} - {t.get('Message', '')}")


def _print_extract_blind_watermark(t, verbose):
    """ExtractBlindWatermark: Extract digital watermark task"""
    if t.get("ErrCode") and t["ErrCode"] != 0:
        print(f"  Error: {t['ErrCode']} - {t.get('Message', '')}")
    wtype = t.get("Type", "")
    if wtype:
        print(f"  Watermark type: {wtype}")
    detected = t.get("IsDetected")
    if detected is not None:
        print(f"  Watermark detected: {'Yes' if detected else 'No'}")
    if t.get("Result"):
        print(f"  Watermark content: {t['Result']}")
    if t.get("ResultUV"):
        print(f"  Tracing UV: {t['ResultUV']}")
    inp = t.get("InputInfo") or {}
    if inp.get("FileId"):
        print(f"  Source file ID: {inp['FileId']}")
    elif inp.get("Url"):
        print(f"  Source URL: {inp['Url']}")


def _print_create_aigc_advanced_custom_element(t, verbose, task_id=None):
    """CreateAigcAdvancedCustomElementTask: Create custom element task"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None and progress < 100:
        print(f"  Progress: {progress}%")
    inp = t.get("Input") or {}
    if inp.get("ElementName"):
        print(f"  Element name: {inp['ElementName']}")
    if inp.get("ReferenceType"):
        print(f"  Reference type: {inp['ReferenceType']}")
    out = t.get("Output") or {}
    info_list = out.get("InfoList") or []
    if info_list:
        print(f"  Created elements: {len(info_list)}")
        for item in info_list:
            print(f"    ElementId: {item.get('ElementId', '')}")
            if verbose and item.get("ElementInfo"):
                print(f"    ElementInfo: {item['ElementInfo'][:200]}")
        # Auto-persist to mem/<task_id>/elements.json
        if task_id:
            saved_path = _save_elements(task_id, info_list)
            if saved_path:
                print(f"  ✅ Elements saved: {saved_path}")


def _print_create_aigc_custom_voice(t, verbose):
    """CreateAigcCustomVoiceTask: Create custom voice task"""
    _err(t, "  ")
    progress = t.get("Progress")
    if progress is not None and progress < 100:
        print(f"  Progress: {progress}%")
    inp = t.get("Input") or {}
    if inp.get("VoiceName"):
        print(f"  Voice name: {inp['VoiceName']}")
    out = t.get("Output") or {}
    info_list = out.get("InfoList") or []
    if info_list:
        print(f"  Created voices: {len(info_list)}")
        for item in info_list:
            print(f"    VoiceId: {item.get('VoiceId', '')}")
            if verbose and item.get("VoiceInfo"):
                print(f"    VoiceInfo: {item['VoiceInfo'][:200]}")


def _print_create_aigc_subject(t, verbose):
    """CreateAigcSubjectTask: Create subject task"""
    _err(t, "  ")
    inp = t.get("Input") or {}
    if inp.get("SubjectName"):
        print(f"  Subject name: {inp['SubjectName']}")
    if inp.get("VoiceId"):
        print(f"  Voice ID: {inp['VoiceId']}")
    out = t.get("Output") or {}
    if out.get("SubjectId"):
        print(f"  Subject ID: {out['SubjectId']}")
    if verbose and out.get("SubjectInfo"):
        print(f"  Subject info: {out['SubjectInfo'][:300]}")


# ── Main print entry point ────────────────────────────────────────────────────────────────

# Task Type -> (response_field, handler_func)
_TASK_HANDLERS = {
    "Procedure":                         ("ProcedureTask",                          _print_procedure),
    "EditMedia":                         ("EditMediaTask",                           _print_edit_media),
    "SplitMedia":                        ("SplitMediaTask",                          _print_split_media),
    "ComposeMedia":                      ("ComposeMediaTask",                        _print_compose_media),
    "WechatPublish":                     ("WechatPublishTask",                       _print_wechat_publish),
    "WechatMiniProgramPublish":          ("WechatMiniProgramPublishTask",            _print_wechat_mini_program),
    "PullUpload":                        ("PullUploadTask",                          _print_pull_upload),
    "Fast Clip Media":                     ("Fast Clip Media Task",                       None),  # No dedicated handler yet, use --json to view full response  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    "RemoveWatermarkTask":               ("RemoveWatermarkTask",                     _print_remove_watermark),
    "RebuildMedia":                      ("RebuildMediaTask",                        _print_rebuild_media),
    "ExtractTraceWatermark":             ("ExtractTraceWatermarkTask",               _print_extract_trace_watermark),
    "ExtractCopyRightWatermark":         ("ExtractCopyRightWatermarkTask",           _print_extract_copyright_watermark),  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    "ReviewAudioVideo":                  ("ReviewAudioVideoTask",                    _print_review_audio_video),
    "DescribeFileAttributesTask":        ("DescribeFileAttributesTask",              _print_describe_file_attributes),
    "QualityInspect":                    ("QualityInspectTask",                      _print_quality_inspect),
    "QualityEnhance":                    ("QualityEnhanceTask",                      _print_quality_enhance),
    "ComplexAdaptiveDynamicStreaming":   ("ComplexAdaptiveDynamicStreamingTask",     _print_complex_adaptive_dynamic_streaming),  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    "ProcessMediaByMPS":                 ("ProcessMediaByMPSTask",                   _print_process_media_by_mps),
    "AigcImageTask":                     ("AigcImageTask",                           lambda t, v: _print_aigc_image(t, v, "AigcImageTask")),  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    "SceneAigcImageTask":                ("SceneAigcImageTask",                      lambda t, v: _print_aigc_image(t, v, "SceneAigcImageTask")),  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    "AigcVideoTask":                     ("AigcVideoTask",                           lambda t, v: _print_aigc_video(t, v, "AigcVideoTask")),  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    "SceneAigcVideoTask":                ("SceneAigcVideoTask",                      lambda t, v: _print_aigc_video(t, v, "SceneAigcVideoTask")),  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    "ImportMediaKnowledge":              ("ImportMediaKnowledge",                    _print_import_media_knowledge),
    "ExtractBlindWatermark":             ("ExtractBlindWatermarkTask",               _print_extract_blind_watermark),
    "Create Aigc Advanced Custom Element": ("Create Aigc Advanced Custom Element Task",   None),  # Special handling required, needs task_id  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    "CreateAigcCustomVoiceTask":         ("CreateAigcCustomVoiceTask",               _print_create_aigc_custom_voice),
    "CreateAigcSubjectTask":             ("CreateAigcSubjectTask",                   _print_create_aigc_subject),
}


def print_summary(result, verbose=False, task_id=None):
    """Print task summary information (supports all TaskTypes)"""
    task_type = result.get("TaskType", "Unknown")
    status = result.get("Status", "Unknown")
    create_time = result.get("CreateTime", "")
    begin_time = result.get("BeginProcessTime", "")
    finish_time = result.get("FinishTime", "")
    # Use the provided task_id first, otherwise extract from result
    _task_id = task_id or result.get("TaskId", "")

    print(f"Task type: {fmt_task_type(task_type)} ({task_type})")
    print(f"Task status: {fmt_status(status)}")
    if create_time:
        print(f"Created at: {create_time}")
    if begin_time:
        print(f"Started at: {begin_time}")
    if finish_time:
        print(f"Finished at: {finish_time}")

    # Dispatch to the corresponding handler function
    handler_info = _TASK_HANDLERS.get(task_type)
    if handler_info:
        field, handler = handler_info
        task_data = result.get(field)
        if task_data:
            # Create Aigc Advanced Custom Element requires special handling (pass task_id)
            if task_type == "CreateAigcAdvancedCustomElement":
                _print_create_aigc_advanced_custom_element(task_data, verbose, task_id=_task_id)
            elif handler is not None:
                handler(task_data, verbose)
            else:
                print(f"  (No detailed parser for {task_type}, use --json to view full response)")
        else:
            print(f"  ({field} field is empty)")
    else:
        # Unknown task type, attempt to print all non-empty top-level fields
        print(f"  (Unknown task type, use --json to view full response)")



# ── Query/Wait Logic ──────────────────────────────────────────────────────────

def describe_task(args):
    """Query task details (single call)"""
    client = get_client(args.region)

    req_body = {"TaskId": args.task_id}
    if args.sub_app_id:
        req_body["SubAppId"] = args.sub_app_id

    try:
        # Use call_json instead of SDK model methods to avoid unknown fields being dropped by old SDK to_json_string()
        resp = client.call_json("DescribeTaskDetail", req_body)
        result = resp.get("Response", resp)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result

        print(f"=== Task Details ===")
        print(f"TaskId: {args.task_id}")
        print_summary(result, verbose=args.verbose, task_id=args.task_id)

        if args.verbose:
            print("\n=== Full Response ===")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
        print(f"Query failed: {e}")
        sys.exit(1)


def wait_for_task(args):
    """Poll and wait for task completion"""
    client = get_client(args.region)

    print(f"Waiting for task to complete (TaskId: {args.task_id})...")
    print(f"Max wait time: {args.max_wait}s, polling interval: {args.interval}s")
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed >= args.max_wait:
            print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
            sys.exit(1)

        req_body = {"TaskId": args.task_id}
        if args.sub_app_id:
            req_body["SubAppId"] = args.sub_app_id

        try:
            # Use call_json to avoid unknown fields being dropped by old SDK to_json_string()
            resp = client.call_json("DescribeTaskDetail", req_body)
            result = resp.get("Response", resp)

            status = result.get("Status", "PROCESSING")
            elapsed_str = f"{elapsed:.0f}s"
            print(f"  [{elapsed_str}] Status: {fmt_status(status)}")

            if status == "FINISH":
                print("\n✅ Task completed!")
                print_summary(result, verbose=args.verbose, task_id=args.task_id)
                if args.json:
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                return result

            elif status in ("ABORTED", "FAIL"):
                print(f"\n❌ Task {fmt_status(status)}!")
                print_summary(result, verbose=True, task_id=args.task_id)
                if args.json:
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                sys.exit(1)

            time.sleep(args.interval)

        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
            print(f"  Query failed: {e}, retrying in {args.interval}s...")
            time.sleep(args.interval)


# ── CLI Entry Point ───────────────────────────────────────────────────────────

def main():
    check_sdk_version()
    parser = argparse.ArgumentParser(
        description="VOD Task Detail Query Tool - Query task execution status and results (supports tasks within the last 3 days)",  # NOCA:line-too-long(long output string or URL, cannot be shortened)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query task status
  python vod_describe_task.py --task-id 1490013579-procedurev2-acd135

  # Wait for task completion (up to 10 minutes)
  # Default behavior: wait for task completion
  python vod_describe_task.py --task-id 1490013579-procedurev2-acd135
  
  # Query current status only, do not wait
  python vod_describe_task.py --task-id 1490013579-procedurev2-acd135 --no-wait

  # Output full response in JSON format
  python vod_describe_task.py --task-id 1490013579-procedurev2-acd135 --json

  # Verbose output (including output URLs, etc.)
  python vod_describe_task.py --task-id 1490013579-procedurev2-acd135 --verbose

  # Specify sub-application ID
  python vod_describe_task.py --task-id 1490013579-procedurev2-acd135 --sub-app-id 1500046806

Task status descriptions:
  WAITING    - Waiting
  PROCESSING - Processing
  FINISH     - Finished
  ABORTED    - Aborted
  FAIL       - Failed (sub-task level status)
  SUCCESS    - Succeeded (sub-task level status)
        """
    )

    parser.add_argument("--task-id", required=True, help="Task ID, e.g.: 1490013579-procedurev2-acd135")
    parser.add_argument(
        "--sub-app-id",
        type=int,
        default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
        help="Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)",
    )
    parser.add_argument("--region", default="ap-guangzhou", help="Region (default: ap-guangzhou)")
    parser.add_argument("--no-wait", action="store_true", help="Query current status only, do not wait for completion")
    parser.add_argument("--max-wait", type=int, default=600, help="Maximum wait time in seconds (default: 600)")
    parser.add_argument("--interval", type=int, default=5, help="Polling interval in seconds (default: 5)")
    parser.add_argument("--json", action="store_true", help="Output full response in JSON format")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output (including output URLs, etc.)")

    args = parser.parse_args()

    if not args.no_wait:
        wait_for_task(args)
    else:
        describe_task(args)


if __name__ == "__main__":
    main()
