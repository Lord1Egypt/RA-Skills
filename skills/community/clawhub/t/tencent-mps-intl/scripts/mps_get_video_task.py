#!/usr/bin/env python3
"""
Tencent Cloud MPS Media Processing Task Query Script

Features:
  Query the execution status and result details of media processing tasks
  submitted via ProcessMedia using a task ID.
  Tasks submitted within the last 7 days can be queried.

  Supports querying the overall task status (WAITING / PROCESSING / FINISH),
  as well as the execution results and output file information of each subtask
  (transcoding, screenshot, subtitles, quality enhancement, etc.).

Usage:
  # Query a specific task
  python mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a

  # Query and output the full JSON response
  python mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a --verbose

  # Output raw JSON only (convenient for pipeline processing)
  python mps_get_video_task.py --task-id 1234567890-WorkflowTask-80108cc3380155d98b2e3573a48a --json

Environment Variables:
  TENCENTCLOUD_SECRET_ID   - Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  - Tencent Cloud SecretKey
"""

import argparse
import json
import os
import sys
from mps_auto_upgrade import check_sdk_version

check_sdk_version()
try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.mps.v20190612 import mps_client, models
except ImportError:
    print("Error: Please install the Tencent Cloud SDK first: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


try:
    from qcloud_cos import CosConfig, CosS3Client
    _COS_SDK_AVAILABLE = True
except ImportError:
    _COS_SDK_AVAILABLE = False

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False

# Task status mapping
STATUS_MAP = {
    "WAITING": "Waiting",
    "PROCESSING": "Processing",
    "FINISH": "Completed",
    "SUCCESS": "Success",
    "FAIL": "Failed",
}

# Subtask type mapping
TASK_TYPE_MAP = {
    "Transcode": "Transcode",
    "AnimatedGraphics": "Animated Graphics",
    "SnapshotByTimeOffset": "Time Offset Screenshot",
    "SampleSnapshot": "Sample Screenshot",
    "ImageSprites": "Image Sprites",
    "AdaptiveDynamicStreaming": "Adaptive Bitrate Streaming",
    "AudioExtract": "Audio Separation",
    "CoverBySnapshot": "Cover by Screenshot",
    "AiAnalysis": "AI Content Analysis",
    "AiRecognition": "AI Content Recognition",
    "AiContentReview": "AI Content Review",
    "AiQualityControl": "Media Quality Inspection",
    "SmartSubtitles": "Smart Subtitles",
    "SmartErase": "Smart Erasure",
    "Classification": "Classification",
    "Cover": "Cover",
    "Cutout": "Cutout",
    "DeLogo": "Logo Removal",
    "Description": "Description",
    "Dubbing": "Dubbing",
    "FrameTag": "Frame Tag",
    "HeadTail": "Intro & Outro",
    "Highlight": "Highlight Reel",
    "HorizontalToVertical": "Horizontal to Vertical",
    "Reel": "Smart Remix",
    "Segment": "Scene Segmentation",
    "Tag": "Tag",
    "VideoComprehension": "Video Comprehension",
    "VideoRemake": "Video Remake / Deduplication",
    "Face": "Face Recognition",
    "Asr": "Speech Recognition",
    "AsrFullText": "Full-text Speech Recognition",
    "AsrWords": "Speech Word Recognition",
    "Ocr": "Text Recognition",
    "OcrFullText": "Full-text OCR",
    "OcrWords": "OCR Word Recognition",
    "Object": "Object Recognition",
    "TransText": "Speech Translation",
    "Porn": "Pornography Review",
    "Terrorism": "Terrorism Review",
    "Political": "Political Review",
    "Prohibited": "Prohibited Content Review",
    "PoliticalAsr": "Political Speech Review",
    "PoliticalOcr": "Political Text Review",
    "PornAsr": "Pornography Speech Review",
    "PornOcr": "Pornography Text Review",
    "ProhibitedAsr": "Prohibited Speech Review",
    "ProhibitedOcr": "Prohibited Text Review",
    "TerrorismOcr": "Terrorism Text Review",
}


def get_credentials():
    """Get Tencent Cloud credentials from environment variables. If missing, attempt to auto-load from system files and retry."""  # NOCA:line-too-long(content cannot be shortened)
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        # Attempt to auto-load from system environment variable files
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] Environment variables not set, attempting to auto-load from system files...", file=sys.stderr)  # NOCA:line-too-long(line cannot be shortened)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from mps_load_env import _print_setup_hint, _TARGET_VARS
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print(
                    "\nError: TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY are not set.\n"
                    "Please add these variables in /etc/environment, ~/.profile, or similar files.\n",
                    file=sys.stderr,
                )
            sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def create_mps_client(cred, region):
    """Create an MPS client."""
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    http_profile.reqMethod = "POST"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return mps_client.MpsClient(cred, region, client_profile)


def format_status(status):
    """Format status display."""
    return STATUS_MAP.get(status, status)


def _try_print_cos_presigned_url(bucket, region, out_path, indent="       "):
    """Attempt to generate and print a pre-signed download URL for a COS output file. Silently skip on failure."""
    if not bucket or not out_path or not _COS_SDK_AVAILABLE:
        return
    try:
        cred = get_credentials()
        cos_config = CosConfig(Region=region, SecretId=cred.secret_id, SecretKey=cred.secret_key)
        cos_client = CosS3Client(cos_config)
        signed_url = cos_client.get_presigned_url(
            Bucket=bucket,
            Key=out_path.lstrip("/"),
            Method="GET",
            Expired=3600
        )
        print(f"{indent}🔗 Download link (pre-signed, valid for 1 hour): {signed_url}")
    except Exception as e:  # NOCA:broad-except(CLI script needs to handle all exceptions)
        print(f"{indent}⚠️  Failed to generate pre-signed URL: {e}")


def print_input_info(input_info):
    """Print input file information."""
    if not input_info:
        return
    input_type = input_info.get("Type", "")
    if input_type == "COS":
        cos = input_info.get("CosInputInfo", {}) or {}
        print(f"   Input: COS - {cos.get('Bucket', '')}:{cos.get('Object', '')} (region: {cos.get('Region', '')})")
    elif input_type == "URL":
        url_info = input_info.get("UrlInputInfo", {}) or {}
        print(f"   Input: URL - {url_info.get('Url', '')}")
    else:
        print(f"   Input type: {input_type}")


def print_meta_data(meta):
    """Print media metadata."""
    if not meta:
        return
    duration = meta.get("Duration", 0)
    width = meta.get("Width", 0)
    height = meta.get("Height", 0)
    bitrate = meta.get("Bitrate", 0)
    container = meta.get("Container", "")
    size = meta.get("Size", 0)
    print(f"   Original info: {container.upper() if container else 'N/A'} | "
          f"{width}x{height} | "
          f"{bitrate // 1000 if bitrate else 0} kbps | "
          f"{duration:.1f}s | "
          f"{size / 1024 / 1024:.2f} MB")


def print_media_process_results(result_set):
    """Print media processing subtask results."""
    if not result_set:
        print("   Subtasks: None")
        return

    for i, item in enumerate(result_set, 1):
        task_type = item.get("Type", "")
        type_name = TASK_TYPE_MAP.get(task_type, task_type)

        # Get the corresponding task detail field based on type
        task_key_map = {
            "Transcode": "TranscodeTask",
            "AnimatedGraphics": "AnimatedGraphicsTask",
            "SnapshotByTimeOffset": "SnapshotByTimeOffsetTask",
            "SampleSnapshot": "SampleSnapshotTask",
            "ImageSprites": "ImageSpritesTask",
            "AdaptiveDynamicStreaming": "AdaptiveDynamicStreamingTask",
            "AudioExtract": "AudioExtractTask",
            "CoverBySnapshot": "CoverBySnapshotTask",
        }
        task_key = task_key_map.get(task_type, "")
        task_detail = item.get(task_key, {}) if task_key else None

        if task_detail:
            status = task_detail.get("Status", "")
            err_code = task_detail.get("ErrCode") or 0
            message = task_detail.get("Message", "")
            progress = task_detail.get("Progress", None)

            status_str = format_status(status)
            progress_str = f" ({progress}%)" if progress is not None else ""
            err_str = f" | Error code: {err_code} - {message}" if err_code != 0 else ""

            print(f"   [{i}] {type_name}: {status_str}{progress_str}{err_str}")

            # Print output file information
            output = task_detail.get("Output", {})
            if output:
                out_storage = output.get("OutputStorage", {}) or {}
                out_path = output.get("Path", "")
                out_type = out_storage.get("Type", "")
                if out_type == "COS":
                    cos_out = out_storage.get("CosOutputStorage", {}) or {}
                    bucket = cos_out.get("Bucket", "")
                    region = cos_out.get("Region", "")
                    print(f"       Output: COS - {bucket}:{out_path} (region: {region})")
                    _try_print_cos_presigned_url(bucket, region, out_path)
                elif out_path:
                    print(f"       Output: {out_path}")

                # Print output video information
                out_width = output.get("Width", 0)
                out_height = output.get("Height", 0)
                out_bitrate = output.get("Bitrate", 0)
                out_duration = output.get("Duration", 0)
                out_size = output.get("Size", 0)
                out_container = output.get("Container", "")
                if out_width or out_height:
                    print(f"       Specs: {out_container.upper() if out_container else 'N/A'} | "
                          f"{out_width}x{out_height} | "
                          f"{out_bitrate // 1000 if out_bitrate else 0} kbps | "
                          f"{out_duration:.1f}s | "
                          f"{out_size / 1024 / 1024:.2f} MB")
        else:
            print(f"   [{i}] {type_name}: No details")


def print_ai_analysis_results(result_set):
    """Print AI content analysis task results, including error detection."""
    if not result_set:
        return

    for i, item in enumerate(result_set, 1):
        task_type = item.get("Type", "")
        # Get corresponding task details based on type
        task_key_map = {
            "Classification": "ClassificationTask",
            "Cover": "CoverTask",
            "Tag": "TagTask",
            "FrameTag": "FrameTagTask",
            "Highlight": "HighlightTask",
            "DeLogo": "DeLogoTask",
            "Description": "DescriptionTask",
            "Dubbing": "DubbingTask",
            "VideoRemake": "VideoRemakeTask",
            "VRemake": "Video Remake Task",   # Actual abbreviation returned by API
            "VideoComprehension": "VideoComprehensionTask",
            "Cutout": "CutoutTask",
            "Reel": "ReelTask",
            "HeadTail": "HeadTailTask",
            "HorizontalToVertical": "HorizontalToVerticalTask",
            "Segment": "SegmentTask",
        }
        task_key = task_key_map.get(task_type, "")
        # For VRemake type, uniformly handle as Video Remake
        normalized_type = "VideoRemake" if task_type == "VRemake" else task_type
        task_detail = item.get(task_key, {}) if task_key else None

        if task_detail:
            status = task_detail.get("Status", "")
            err_code = task_detail.get("ErrCode") or 0
            err_code_ext = task_detail.get("ErrCodeExt", "")
            message = task_detail.get("Message", "")

            status_str = format_status(status)
            err_str = ""
            if err_code != 0:
                err_str = f" | Error code: {err_code}"
            if err_code_ext:
                err_str += f" ({err_code_ext})"
            if message and message != "SUCCESS":
                err_str += f" - {message}"

            print(f"   [{i}] AI analysis-{task_type}: {status_str}{err_str}")

            # Print analysis output information
            output = task_detail.get("Output", {})
            if output:
                # Classification results
                classifications = output.get("Classifications", [])
                if classifications:
                    print(f"       Classification results:")
                    for cls in classifications[:5]:  # Display up to 5
                        name = cls.get("Name", "")
                        conf = cls.get("Confidence", 0)
                        print(f"         - {name} ({conf * 100:.1f}%)")

                # Tags
                tags = output.get("Tags", [])
                if tags:
                    print(f"       Tags: {', '.join(tags[:10])}")  # Display up to 10 tags

                # Cover
                cover_path = output.get("CoverPath", "")
                if cover_path:
                    print(f"       Cover: {cover_path}")

                # Description
                description = output.get("Description", "")
                if description:
                    print(f"       Description: {description[:100]}{'...' if len(description) > 100 else ''}")

                # Highlights
                highlights = output.get("Highlights", [])
                if highlights:
                    print(f"       Highlights:")
                    for hl in highlights[:3]:  # Display up to 3
                        start = hl.get("StartTime", 0)
                        end = hl.get("EndTime", 0)
                        conf = hl.get("Confidence", 0)
                        print(f"         - {start}s - {end}s (Confidence: {conf * 100:.1f}%)")

                # Video Remake output video path (video deduplication / video remix)
                if normalized_type == "VideoRemake":
                    out_path = output.get("Path", "")
                    if out_path:
                        confidence = output.get("Confidence", None)
                        conf_str = f" (Confidence: {confidence})" if confidence is not None else ""
                        print(f"       Output path: {out_path}{conf_str}")
                        out_storage = output.get("OutputStorage", {}) or {}
                        out_type = out_storage.get("Type", "")
                        if out_type == "COS":
                            cos_out = out_storage.get("CosOutputStorage", {}) or {}
                            bucket = cos_out.get("Bucket", "")
                            region = cos_out.get("Region", "")
                            if bucket and region:
                                _try_print_cos_presigned_url(bucket, region, out_path)
        else:
            print(f"   [{i}] AI analysis-{task_type}: No details")


def print_ai_recognition_results(result_set):
    """Print AI content recognition task results, including error detection."""
    if not result_set:
        return

    for i, item in enumerate(result_set, 1):
        task_type = item.get("Type", "")
        # Get corresponding task details based on type
        task_key_map = {
            "Face": "FaceTask",
            "Asr": "AsrTask",
            "Ocr": "OcrTask",
            "Object": "ObjectTask",
            "AsrWords": "AsrWordsTask",
            "OcrWords": "OcrWordsTask",
            "TransText": "TransTextTask",
        }
        task_key = task_key_map.get(task_type, "")
        task_detail = item.get(task_key, {}) if task_key else None

        if task_detail:
            status = task_detail.get("Status", "")
            err_code = task_detail.get("ErrCode") or 0
            err_code_ext = task_detail.get("ErrCodeExt", "")
            message = task_detail.get("Message", "")

            status_str = format_status(status)
            err_str = ""
            if err_code != 0:
                err_str = f" | Error code: {err_code}"
            if err_code_ext:
                err_str += f" ({err_code_ext})"
            if message and message != "SUCCESS":
                err_str += f" - {message}"

            print(f"   [{i}] AI recognition-{task_type}: {status_str}{err_str}")

            # Print recognition output information
            output = task_detail.get("Output", {})
            if output:
                # Face recognition
                if task_type == "Face":
                    face_set = output.get("FaceSet", [])
                    if face_set:
                        print(f"       Recognized {len(face_set)} faces:")
                        for face in face_set[:5]:  # Display up to 5
                            name = face.get("Name", "Unknown")
                            conf = face.get("Confidence", 0)
                            print(f"         - {name} ({conf * 100:.1f}%)")

                # Speech recognition
                elif task_type == "Asr":
                    subtitle_path = output.get("SubtitlePath", "")
                    if subtitle_path:
                        print(f"       Subtitle file: {subtitle_path}")

                # Text recognition
                elif task_type == "Ocr":
                    text_set = output.get("TextSet", [])
                    if text_set:
                        print(f"       Recognized {len(text_set)} text boxes")

                # Object recognition
                elif task_type == "Object":
                    object_set = output.get("ObjectSet", [])
                    if object_set:
                        print(f"       Recognized {len(object_set)} objects:")
                        for obj in object_set[:5]:  # Display up to 5
                            name = obj.get("Name", "")
                            conf = obj.get("Confidence", 0)
                            print(f"         - {name} ({conf * 100:.1f}%)")

                # Speech translation
                elif task_type == "TransText":
                    subtitle_path = output.get("SubtitlePath", "")
                    if subtitle_path:
                        print(f"       Translated subtitle file: {subtitle_path}")
        else:
            print(f"   [{i}] AI recognition-{task_type}: No details")


def print_ai_content_review_results(result_set):
    """Print AI content review task results, including error detection."""
    if not result_set:
        return

    for i, item in enumerate(result_set, 1):
        task_type = item.get("Type", "")
        # Get corresponding task details based on type
        task_key_map = {
            "Porn": "PornTask",
            "Terrorism": "TerrorismTask",
            "Political": "PoliticalTask",
            "Prohibited": "ProhibitedTask",
            "PoliticalAsr": "PoliticalAsrTask",
            "PoliticalOcr": "PoliticalOcrTask",
            "PornAsr": "PornAsrTask",
            "PornOcr": "PornOcrTask",
            "ProhibitedAsr": "ProhibitedAsrTask",
            "ProhibitedOcr": "ProhibitedOcrTask",
            "TerrorismOcr": "TerrorismOcrTask",
        }
        task_key = task_key_map.get(task_type, "")
        task_detail = item.get(task_key, {}) if task_key else None

        if task_detail:
            status = task_detail.get("Status", "")
            err_code = task_detail.get("ErrCode") or 0
            err_code_ext = task_detail.get("ErrCodeExt", "")
            message = task_detail.get("Message", "")

            status_str = format_status(status)
            err_str = ""
            if err_code != 0:
                err_str = f" | Error code: {err_code}"
            if err_code_ext:
                err_str += f" ({err_code_ext})"
            if message and message != "SUCCESS":
                err_str += f" - {message}"

            print(f"   [{i}] AI review-{task_type}: {status_str}{err_str}")

            # Print review output information
            output = task_detail.get("Output", {})
            if output:
                suggestion = output.get("Suggestion", "")
                label = output.get("Label", "")
                confidence = output.get("Confidence", 0)

                if suggestion:
                    suggestion_map = {
                        "pass": "Pass",
                        "review": "Review",
                        "block": "Block"
                    }
                    sug_text = suggestion_map.get(suggestion, suggestion)
                    print(f"       Suggestion: {sug_text}")
                if label:
                    print(f"       Label: {label}")
                if confidence:
                    print(f"       Confidence: {confidence * 100:.1f}%")
        else:
            print(f"   [{i}] AI review-{task_type}: No details")


def print_ai_quality_control_result(result):
    """Print AI media quality control task results, including error detection."""
    if not result:
        return

    status = result.get("Status", "")
    err_code = result.get("ErrCode") or 0
    err_code_ext = result.get("ErrCodeExt", "")
    message = result.get("Message", "")

    status_str = format_status(status)
    err_str = ""
    if err_code != 0:
        err_str = f" | Error code: {err_code}"
    if err_code_ext:
        err_str += f" ({err_code_ext})"
    if message and message != "SUCCESS":
        err_str += f" - {message}"

    print(f"   AI quality control: {status_str}{err_str}")

    # Get output information
    output = result.get("Output", {})

    # Check for missing audio/video
    no_audio = output.get("NoAudio", False)
    no_video = output.get("NoVideo", False)
    if no_audio or no_video:
        issues = []
        if no_audio:
            issues.append("Missing audio")
        if no_video:
            issues.append("Missing video")
        print(f"   ⚠️  {', '.join(issues)}")

    # Quality score
    score = output.get("QualityEvaluationScore")
    if score is not None:
        print(f"   Quality score: {score}")

    # Check container diagnosis results
    diagnose_results = output.get("ContainerDiagnoseResultSet", [])
    if diagnose_results:
        has_fatal = False
        _ = False

        print(f"   Quality control diagnosis results:")
        for diagnose in diagnose_results:
            category = diagnose.get("Category", "")
            type_name = diagnose.get("Type", "")
            severity = diagnose.get("SeverityLevel", "")

            # Output based on severity level
            if severity == "Fatal":
                has_fatal = True
                print(f"       ❌ [Fatal]{category}/{type_name}")
            elif severity == "Warning":
                _has_warning = True
                print(f"       ⚠️  [Warning]{category}/{type_name}")
            else:
                print(f"       ℹ️  [{severity}]{category}/{type_name}")

            # Output timestamps (if any)
            timestamps = diagnose.get("TimestampSet", [])
            if timestamps:
                print(f"          Time points: {', '.join(map(str, timestamps))} seconds")

        # If there are fatal errors, mark task as failed at the beginning
        if has_fatal and status_str == "Completed":
            print(f"   ⚠️  Quality control detected fatal errors, task status should be failed")

    # Check quality control statistics
    qc_stats = output.get("QualityControlStatSet", [])
    if qc_stats:
        print(f"   Quality control statistics:")
        for stat in qc_stats:
            stat_type = stat.get("Type", "")
            avg_val = stat.get("AvgValue", 0)
            max_val = stat.get("MaxValue", 0)
            min_val = stat.get("MinValue", 0)

            # Only output meaningful statistics (non-zero values)
            if max_val > 0 or avg_val > 0:
                print(f"       {stat_type}: Average={avg_val}, Maximum={max_val}, Minimum={min_val}")


def print_smart_subtitles_results(result_set):
    """Print smart subtitle task results, including error detection."""
    if not result_set:
        return

    for i, item in enumerate(result_set, 1):
        task_type = item.get("Type", "")
        task_key_map = {
            "AsrFullText": "AsrFullTextTask",
            "TransText": "TransTextTask",
            "PureSubtitleTrans": "PureSubtitleTransTask",
            "OcrFullText": "OcrFullTextTask",
        }
        task_key = task_key_map.get(task_type, "")
        task_detail = item.get(task_key, {}) if task_key else None

        if task_detail:
            status = task_detail.get("Status", "")
            err_code = task_detail.get("ErrCode") or 0
            err_code_ext = task_detail.get("ErrCodeExt", "")
            message = task_detail.get("Message", "")

            status_str = format_status(status)
            err_str = ""
            if err_code != 0:
                err_str = f" | Error code: {err_code}"
            if err_code_ext:
                err_str += f" ({err_code_ext})"
            if message and message != "SUCCESS":
                err_str += f" - {message}"

            print(f"   [{i}] Smart subtitle-{task_type}: {status_str}{err_str}")

            # Check for errors in subtitle results
            output = task_detail.get("Output", {})
            if output:
                # Subtitle results for Trans Text Task
                subtitle_results = output.get("SubtitleResults", [])
                for j, sub in enumerate(subtitle_results, 1):
                    sub_status = sub.get("Status", "")
                    sub_err = sub.get("ErrCode") or 0
                    sub_err_ext = sub.get("ErrCodeExt", "")
                    sub_msg = sub.get("Message", "")
                    if sub_err != 0 or sub_status == "FAIL":
                        err_info = f"Error code: {sub_err}"
                        if sub_err_ext:
                            err_info += f" ({sub_err_ext})"
                        if sub_msg:
                            err_info += f" - {sub_msg}"
                        print(f"       Subtitle result[{j}]: {format_status(sub_status)} | {err_info}")

                # Recognition results for Ocr Full Text Task
                recognize_results = output.get("RecognizeSubtitleResult", [])
                for j, rec in enumerate(recognize_results, 1):
                    rec_status = rec.get("Status", "")
                    rec_err = rec.get("ErrCode") or 0
                    rec_err_ext = rec.get("ErrCodeExt", "")
                    rec_msg = rec.get("Message", "")
                    if rec_err != 0 or rec_status == "FAIL":
                        err_info = f"Error code: {rec_err}"
                        if rec_err_ext:
                            err_info += f" ({rec_err_ext})"
                        if rec_msg:
                            err_info += f" - {rec_msg}"
                        print(f"       OCR recognition result[{j}]: {format_status(rec_status)} | {err_info}")

                # Translation results for Ocr Full Text Task
                trans_results = output.get("TransSubtitleResult", [])
                for j, trans in enumerate(trans_results, 1):
                    trans_status = trans.get("Status", "")
                    trans_err = trans.get("ErrCode") or 0
                    trans_err_ext = trans.get("ErrCodeExt", "")
                    trans_msg = trans.get("Message", "")
                    if trans_err != 0 or trans_status == "FAIL":
                        err_info = f"Error code: {trans_err}"
                        if trans_err_ext:
                            err_info += f" ({trans_err_ext})"
                        if trans_msg:
                            err_info += f" - {trans_msg}"
                        print(f"       Subtitle translation result[{j}]: {format_status(trans_status)} | {err_info}")
        else:
            print(f"   [{i}] Smart subtitle-{task_type}: No details")


def print_smart_erase_result(result):
    """Print smart erasure task results, including error detection."""
    if not result:
        return

    status = result.get("Status", "")
    err_code = result.get("ErrCode") or 0
    message = result.get("Message", "")

    status_str = format_status(status)
    err_str = ""
    if err_code != 0:
        err_str = f" | Error code: {err_code}"
    if message and message != "SUCCESS":
        err_str += f" - {message}"

    print(f"   Smart erasure: {status_str}{err_str}")


def print_edit_media_task(task):
    """Print video editing task results, including error detection."""
    if not task:
        return

    status = task.get("Status", "")
    err_code = task.get("ErrCode") or 0
    message = task.get("Message", "")

    status_str = format_status(status)
    err_str = ""
    if err_code != 0:
        err_str = f" | Error code: {err_code}"
    if message and message != "SUCCESS":
        err_str += f" - {message}"

    print(f"   Video editing: {status_str}{err_str}")

    # Input information
    print_input_info(task.get("InputInfo"))

    # Output information
    output = task.get("Output", {})
    if output:
        out_storage = output.get("OutputStorage", {}) or {}
        out_path = output.get("Path", "")
        out_type = out_storage.get("Type", "")
        if out_type == "COS":
            cos_out = out_storage.get("CosOutputStorage", {}) or {}
            bucket = cos_out.get("Bucket", "")
            region = cos_out.get("Region", "")
            print(f"       Output: COS - {bucket}:{out_path} (region: {region})")
            _try_print_cos_presigned_url(bucket, region, out_path)


def print_live_stream_task(task):
    """Print live stream processing task results, including error detection."""
    if not task:
        return

    status = task.get("Status", "")
    err_code = task.get("ErrCode") or 0
    message = task.get("Message", "")

    status_str = format_status(status)
    err_str = ""
    if err_code != 0:
        err_str = f" | Error code: {err_code}"
    if message and message != "SUCCESS":
        err_str += f" - {message}"

    print(f"   Live stream processing: {status_str}{err_str}")


def print_extract_blind_watermark_task(task):
    """Print extract blind watermark task results, including error detection."""
    if not task:
        return

    status = task.get("Status", "")
    err_code = task.get("ErrCode") or 0
    message = task.get("Message", "")

    status_str = format_status(status)
    err_str = ""
    if err_code != 0:
        err_str = f" | Error code: {err_code}"
    if message and message != "SUCCESS":
        err_str += f" - {message}"

    print(f"   Extract blind watermark: {status_str}{err_str}")

    # Extracted text
    output_text = task.get("OutputText", "")
    if output_text:
        print(f"       Extracted content: {output_text}")


def print_schedule_activity_results(result_set):
    """
    Print orchestration task activity results, including error detection.

    Dynamically retrieves corresponding task details based on ActivityType,
    recursively processes each subtask's ErrCode, ErrCodeExt, and Message.
    """
    if not result_set:
        return

    # Activity Type to task detail field mapping
    ACTIVITY_TYPE_MAP = {  # NOCA:invalid-name(legacy naming convention)
        "Transcode": "TranscodeTask",
        "AnimatedGraphics": "AnimatedGraphicsTask",
        "SnapshotByTimeOffset": "SnapshotByTimeOffsetTask",
        "SampleSnapshot": "SampleSnapshotTask",
        "ImageSprites": "ImageSpritesTask",
        "AdaptiveDynamicStreaming": "AdaptiveDynamicStreamingTask",
        "Recognition": "RecognitionTask",
        "Review": "ReviewTask",
        "Analysis": "AnalysisTask",
        "QualityControl": "QualityControlTask",
        "SmartSubtitles": "SmartSubtitlesTask",
        "SmartErase": "SmartEraseTask",
        "ExecRule": "ExecRuleTask",
        "AudioExtract": "AudioExtractTask",
        "CoverBySnapshot": "CoverBySnapshotTask",
        "Classification": "ClassificationTask",
        "Cover": "CoverTask",
        "Cutout": "CutoutTask",
        "DeLogo": "DeLogoTask",
        "Description": "DescriptionTask",
        "Dubbing": "DubbingTask",
        "FrameTag": "FrameTagTask",
        "HeadTail": "HeadTailTask",
        "Highlight": "HighlightTask",
        "HorizontalToVertical": "HorizontalToVerticalTask",
        "Reel": "ReelTask",
        "Segment": "SegmentTask",
        "Tag": "TagTask",
        "VideoComprehension": "VideoComprehensionTask",
        "VideoRemake": "VideoRemakeTask",
        "Face": "FaceTask",
        "Asr": "AsrTask",
        "AsrFullText": "AsrFullTextTask",
        "AsrWords": "AsrWordsTask",
        "Ocr": "OcrTask",
        "OcrFullText": "OcrFullTextTask",
        "OcrWords": "OcrWordsTask",
        "Object": "ObjectTask",
        "TransText": "TransTextTask",
        "Porn": "PornTask",
        "Terrorism": "TerrorismTask",
        "Political": "PoliticalTask",
        "Prohibited": "ProhibitedTask",
        "PoliticalAsr": "PoliticalAsrTask",
        "PoliticalOcr": "PoliticalOcrTask",
        "PornAsr": "PornAsrTask",
        "PornOcr": "PornOcrTask",
        "ProhibitedAsr": "ProhibitedAsrTask",
        "ProhibitedOcr": "ProhibitedOcrTask",
        "TerrorismOcr": "TerrorismOcrTask",
    }

    for i, item in enumerate(result_set, 1):
        activity_res = item.get("ActivityResItem", {})
        activity_type = item.get("ActivityType", "")

        # Get corresponding task detail field name based on Activity Type
        task_key = ACTIVITY_TYPE_MAP.get(activity_type)

        if task_key and task_key in activity_res:
            task = activity_res[task_key]
            # Uniformly process error information for all subtask types
            _print_schedule_subtask_error(task, activity_type, i)
        else:
            # Unknown type, try to traverse all possible task fields
            _print_unknown_activity_type(activity_res, activity_type, i)


def _print_schedule_subtask_error(task, activity_type, index):
    """
    Unified function to print orchestration subtask error information.
    Recursively handles ErrCode, ErrCodeExt, and Message.
    """
    if not task:
        return

    status = task.get("Status", "")
    err_code = task.get("ErrCode") or 0
    err_code_ext = task.get("ErrCodeExt", "")
    message = task.get("Message", "")
    progress = task.get("Progress")

    # Type name mapping
    type_name_map = {
        "Transcode": "Transcoding",
        "AnimatedGraphics": "Animated Graphics",
        "SnapshotByTimeOffset": "Time Offset Snapshot",
        "SampleSnapshot": "Sample Snapshot",
        "ImageSprites": "Image Sprites",
        "AdaptiveDynamicStreaming": "Adaptive Bitrate Streaming",
        "AudioExtract": "Audio Extraction",
        "CoverBySnapshot": "Snapshot as Cover",
        "Recognition": "AI Recognition",
        "Review": "AI Review",
        "Analysis": "AI Analysis",
        "QualityControl": "Quality Control",
        "SmartSubtitles": "Smart Subtitles",
        "SmartErase": "Smart Erasure",
        "ExecRule": "Rule Execution",
        "Classification": "Classification",
        "Cover": "Cover",
        "Cutout": "Cutout",
        "DeLogo": "Logo Removal",
        "Description": "Description",
        "Dubbing": "Dubbing",
        "FrameTag": "Frame Tagging",
        "HeadTail": "Head and Tail",
        "Highlight": "Highlight Reel",
        "HorizontalToVertical": "Horizontal to Vertical",
        "Reel": "Smart Remix",
        "Segment": "Scene Segmentation",
        "Tag": "Tagging",
        "VideoComprehension": "Video Understanding",
        "VideoRemake": "Video Remix/Deduplication",
        "Face": "Face Recognition",
        "Asr": "Speech Recognition",
        "AsrFullText": "Full-Text Speech Recognition",
        "AsrWords": "Word-level Speech Recognition",
        "Ocr": "Text Recognition",
        "OcrFullText": "Full-Text Text Recognition",
        "OcrWords": "Word-level Text Recognition",
        "Object": "Object Recognition",
        "TransText": "Translation",
        "Porn": "Pornography Review",
        "Terrorism": "Terrorism Review",
        "Political": "Political Review",
        "Prohibited": "Prohibited Content Review",
        "PoliticalAsr": "Political Speech Review",
        "PoliticalOcr": "Political Text Review",
        "PornAsr": "Pornographic Speech Review",
        "PornOcr": "Pornographic Text Review",
        "ProhibitedAsr": "Prohibited Content Speech Review",
        "ProhibitedOcr": "Prohibited Content Text Review",
        "TerrorismOcr": "Terrorism Text Review",
    }
    type_name = type_name_map.get(activity_type, activity_type)

    status_str = format_status(status)
    progress_str = f" ({progress}%)" if progress is not None else ""

    # Build error information string
    err_str = ""
    if err_code != 0:
        err_str = f" | Error code: {err_code}"
    if err_code_ext:
        err_str += f" ({err_code_ext})"
    if message and message != "SUCCESS":
        err_str += f" - {message}"

    print(f"   Orchestration-{type_name}[{index}]: {status_str}{progress_str}{err_str}")

    # Recursively handle nested output results errors (e.g., subtitle task sub-results)
    _print_nested_task_errors(task, f"Orchestration-{type_name}[{index}]")


def _print_nested_task_errors(task, parent_label):
    """Recursively print nested task error information."""
    if not task:
        return

    output = task.get("Output", {})
    if not output:
        return

    # Handle nested subtitle results errors
    subtitle_results = output.get("SubtitleResults", [])
    for j, sub in enumerate(subtitle_results, 1):
        sub_status = sub.get("Status", "")
        sub_err = sub.get("ErrCode") or 0
        sub_err_ext = sub.get("ErrCodeExt", "")
        sub_msg = sub.get("Message", "")
        if sub_err != 0 or sub_status == "FAIL":
            err_info = f"Error code: {sub_err}"
            if sub_err_ext:
                err_info += f" ({sub_err_ext})"
            if sub_msg:
                err_info += f" - {sub_msg}"
            print(f"       └─ Subtitle result[{j}]: {format_status(sub_status)} | {err_info}")

    # Handle OCR recognition results nested errors
    recognize_results = output.get("RecognizeSubtitleResult", [])
    for j, rec in enumerate(recognize_results, 1):
        rec_status = rec.get("Status", "")
        rec_err = rec.get("ErrCode") or 0
        rec_err_ext = rec.get("ErrCodeExt", "")
        rec_msg = rec.get("Message", "")
        if rec_err != 0 or rec_status == "FAIL":
            err_info = f"Error code: {rec_err}"
            if rec_err_ext:
                err_info += f" ({rec_err_ext})"
            if rec_msg:
                err_info += f" - {rec_msg}"
            print(f"       └─ OCR recognition result[{j}]: {format_status(rec_status)} | {err_info}")

    # Handle subtitle translation results nested errors
    trans_results = output.get("TransSubtitleResult", [])
    for j, trans in enumerate(trans_results, 1):
        trans_status = trans.get("Status", "")
        trans_err = trans.get("ErrCode") or 0
        trans_err_ext = trans.get("ErrCodeExt", "")
        trans_msg = trans.get("Message", "")
        if trans_err != 0 or trans_status == "FAIL":
            err_info = f"Error code: {trans_err}"
            if trans_err_ext:
                err_info += f" ({trans_err_ext})"
            if trans_msg:
                err_info += f" - {trans_msg}"
            print(f"       └─ Subtitle translation result[{j}]: {format_status(trans_status)} | {err_info}")

    # Handle quality control task diagnostic results
    diagnose_results = output.get("ContainerDiagnoseResultSet", [])
    if diagnose_results:
        print(f"       └─ Quality control diagnostic results:")
        has_fatal = False
        _has_warning = False

        for diagnose in diagnose_results:
            category = diagnose.get("Category", "")
            type_name = diagnose.get("Type", "")
            severity = diagnose.get("SeverityLevel", "")

            if severity == "Fatal":
                has_fatal = True
                print(f"          ❌ [Fatal]{category}/{type_name}")
            elif severity == "Warning":
                _has_warning = True
                print(f"          ⚠️  [Warning]{category}/{type_name}")
            else:
                print(f"          ℹ️  [{severity}]{category}/{type_name}")

            timestamps = diagnose.get("TimestampSet", [])
            if timestamps:
                print(f"             Timestamps: {', '.join(map(str, timestamps))} seconds")

        if has_fatal:
            print(f"       ⚠️  Quality control detected fatal errors")


def _print_unknown_activity_type(activity_res, activity_type, index):
    """Handle unknown ActivityType by attempting to iterate through all possible task fields."""
    # Try all known task fields
    known_tasks = [
        ("TranscodeTask", "Transcoding"),
        ("AnimatedGraphicsTask", "Animated Graphics"),
        ("SnapshotByTimeOffsetTask", "Time Offset Snapshot"),
        ("SampleSnapshotTask", "Sample Snapshot"),
        ("ImageSpritesTask", "Image Sprites"),
        ("AdaptiveDynamicStreamingTask", "Adaptive Bitrate Streaming"),
        ("AudioExtractTask", "Audio Extraction"),
        ("CoverBySnapshotTask", "Snapshot as Cover"),
        ("RecognitionTask", "AI Recognition"),
        ("ReviewTask", "AI Review"),
        ("AnalysisTask", "AI Analysis"),
        ("QualityControlTask", "Quality Control"),
        ("SmartSubtitlesTask", "Smart Subtitles"),
        ("SmartEraseTask", "Smart Erasure"),
        ("ExecRuleTask", "Rule Execution"),
        ("ClassificationTask", "Classification"),
        ("CoverTask", "Cover"),
        ("CutoutTask", "Cutout"),
        ("DeLogoTask", "Logo Removal"),
        ("DescriptionTask", "Description"),
        ("DubbingTask", "Dubbing"),
        ("FrameTagTask", "Frame Tagging"),
        ("HeadTailTask", "Head and Tail"),
        ("HighlightTask", "Highlight Reel"),
        ("HorizontalToVerticalTask", "Horizontal to Vertical"),
        ("ReelTask", "Smart Remix"),
        ("SegmentTask", "Scene Segmentation"),
        ("TagTask", "Tagging"),
        ("VideoComprehensionTask", "Video Understanding"),
        ("VideoRemakeTask", "Video Remix/Deduplication"),
        ("FaceTask", "Face Recognition"),
        ("AsrTask", "Speech Recognition"),
        ("AsrFullTextTask", "Full-Text Speech Recognition"),
        ("AsrWordsTask", "Word-level Speech Recognition"),
        ("OcrTask", "Text Recognition"),
        ("OcrFullTextTask", "Full-Text Text Recognition"),
        ("OcrWordsTask", "Word-level Text Recognition"),
        ("ObjectTask", "Object Recognition"),
        ("TransTextTask", "Translation"),
        ("PornTask", "Pornography Review"),
        ("TerrorismTask", "Terrorism Review"),
        ("PoliticalTask", "Political Review"),
        ("ProhibitedTask", "Prohibited Content Review"),
        ("PoliticalAsrTask", "Political Speech Review"),
        ("PoliticalOcrTask", "Political Text Review"),
        ("PornAsrTask", "Pornographic Speech Review"),
        ("PornOcrTask", "Pornographic Text Review"),
        ("ProhibitedAsrTask", "Prohibited Content Speech Review"),
        ("ProhibitedOcrTask", "Prohibited Content Text Review"),
        ("TerrorismOcrTask", "Terrorism Text Review"),
    ]

    found = False
    for task_key, type_name in known_tasks:
        if task_key in activity_res:
            task = activity_res[task_key]
            _print_schedule_subtask_error(task, type_name, index)
            found = True
            break

    if not found:
        # Completely unknown type, print warning
        print(f"   Orchestration-Unknown type[{index}] (ActivityType: {activity_type}): Unrecognized task type")


def print_media_task_error(task, label):
    """Print media processing task error information."""
    if not task:
        return
    status = task.get("Status", "")
    err_code = task.get("ErrCode") or 0
    err_code_ext = task.get("ErrCodeExt", "")
    message = task.get("Message", "")
    progress = task.get("Progress", None)

    status_str = format_status(status)
    progress_str = f" ({progress}%)" if progress is not None else ""
    err_str = ""
    if err_code != 0:
        err_str = f" | Error code: {err_code}"
    if err_code_ext:
        err_str += f" ({err_code_ext})"
    if message and message != "SUCCESS":
        err_str += f" - {message}"

    print(f"   {label}: {status_str}{progress_str}{err_str}")


def print_ai_task_error(task, label):
    """Print AI task error information."""
    if not task:
        return
    status = task.get("Status", "")
    err_code = task.get("ErrCode") or 0
    err_code_ext = task.get("ErrCodeExt", "")
    message = task.get("Message", "")

    status_str = format_status(status)
    err_str = ""
    if err_code != 0:
        err_str = f" | Error code: {err_code}"
    if err_code_ext:
        err_str += f" ({err_code_ext})"
    if message and message != "SUCCESS":
        err_str += f" - {message}"

    print(f"   {label}: {status_str}{err_str}")


def print_schedule_task(task):
    """Print scheduling task result, including error detection."""
    if not task:
        return

    status = task.get("Status", "")
    err_code = task.get("ErrCode") or 0
    message = task.get("Message", "")

    status_str = format_status(status)
    err_str = ""
    if err_code != 0:
        err_str = f" | Error code: {err_code}"
    if message and message != "SUCCESS":
        err_str += f" - {message}"

    print(f"   Scheduling task: {status_str}{err_str}")

    # Input information
    print_input_info(task.get("InputInfo"))

    # Activity results
    print("-" * 60)
    print("   Scheduling activity results:")
    print_schedule_activity_results(task.get("ActivityResultSet", []))


def print_live_schedule_task(task):
    """Print live streaming scheduling task result, including error detection."""
    if not task:
        return

    status = task.get("Status", "")
    err_code = task.get("ErrCode") or 0
    message = task.get("Message", "")

    status_str = format_status(status)
    err_str = ""
    if err_code != 0:
        err_str = f" | Error code: {err_code}"
    if message and message != "SUCCESS":
        err_str += f" - {message}"

    print(f"   Live streaming scheduling: {status_str}{err_str}")

    # Live activity results
    live_results = task.get("LiveActivityResultSet", [])
    if live_results:
        print("-" * 60)
        print("   Live activity results:")
        for i, item in enumerate(live_results, 1):
            live_res = item.get("LiveActivityResItem", {})

            if "LiveRecordTask" in live_res:
                record_task = live_res["LiveRecordTask"]
                rec_status = record_task.get("Status", "")
                rec_err = record_task.get("ErrCode") or 0
                rec_msg = record_task.get("Message", "")
                rec_status_str = format_status(rec_status)
                rec_err_str = ""
                if rec_err != 0:
                    rec_err_str = f" | Error code: {rec_err}"
                if rec_msg and rec_msg != "SUCCESS":
                    rec_err_str += f" - {rec_msg}"
                print(f"   [{i}] Live recording: {rec_status_str}{rec_err_str}")

            if "LiveQualityControlTask" in live_res:
                qc_task = live_res["LiveQualityControlTask"]
                qc_status = qc_task.get("Status", "")
                qc_err = qc_task.get("ErrCode") or 0
                qc_msg = qc_task.get("Message", "")
                qc_status_str = format_status(qc_status)
                qc_err_str = ""
                if qc_err != 0:
                    qc_err_str = f" | Error code: {qc_err}"
                if qc_msg and qc_msg != "SUCCESS":
                    qc_err_str += f" - {qc_msg}"
                print(f"   [{i}] Live quality control: {qc_status_str}{qc_err_str}")


def query_task(args):
    """Query media processing task details."""
    region = args.region or os.environ.get("TENCENTCLOUD_API_REGION", "ap-guangzhou")

    # 1. Get credentials and client
    cred = get_credentials()
    client = create_mps_client(cred, region)

    # 2. Build request
    params = {"TaskId": args.task_id}

    # 3. Make API call
    try:
        req = models.DescribeTaskDetailRequest()
        req.from_json_string(json.dumps(params))

        resp = client.DescribeTaskDetail(req)
        result = json.loads(resp.to_json_string())

        # JSON-only output mode
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return result

        # Parse response
        task_type = result.get("TaskType", "")
        status = result.get("Status", "")
        create_time = result.get("CreateTime", "")
        begin_time = result.get("BeginProcessTime", "")
        finish_time = result.get("FinishTime", "")

        print("=" * 60)
        print("Tencent Cloud MPS Media Processing Task Details")
        print("=" * 60)
        print(f"   TaskId:    {args.task_id}")
        print(f"   Task type:  {task_type}")
        print(f"   Status:      {format_status(status)}")
        print(f"   Creation time:  {create_time}")
        if begin_time:
            print(f"   Start time:  {begin_time}")
        if finish_time:
            print(f"   Completion time:  {finish_time}")
        print("-" * 60)

        # WorkflowTask (tasks submitted via ProcessMedia)
        workflow_task = result.get("WorkflowTask")
        if workflow_task:
            wf_status = workflow_task.get("Status", "")
            wf_err = workflow_task.get("ErrCode") or 0
            wf_msg = workflow_task.get("Message", "")

            print(f"   Workflow status: {format_status(wf_status)}", end="")
            if wf_err != 0:
                print(f" | Error code: {wf_err} - {wf_msg}", end="")
            print()

            # Input information
            print_input_info(workflow_task.get("InputInfo"))

            # Metadata
            print_meta_data(workflow_task.get("MetaData"))

            # Sub-task results
            print("-" * 60)
            print("   Sub-task results:")
            print_media_process_results(workflow_task.get("MediaProcessResultSet", []))

            # AI task results
            print("-" * 60)
            print("   AI task results:")
            print_ai_analysis_results(workflow_task.get("AiAnalysisResultSet", []))
            print_ai_recognition_results(workflow_task.get("AiRecognitionResultSet", []))
            print_ai_content_review_results(workflow_task.get("AiContentReviewResultSet", []))
            print_ai_quality_control_result(workflow_task.get("AiQualityControlTaskResult", {}))

            # Smart subtitles task
            smart_subtitles = workflow_task.get("SmartSubtitlesTaskResultSet", [])
            if smart_subtitles:
                print("-" * 60)
                print("   Smart subtitles task:")
                print_smart_subtitles_results(smart_subtitles)

            # Smart erase task
            smart_erase = workflow_task.get("SmartEraseTaskResult", {})
            if smart_erase:
                print("-" * 60)
                print("   Smart erase task:")
                print_smart_erase_result(smart_erase)

        # Edit Media Task (video editing task)
        elif result.get("EditMediaTask"):
            edit_task = result.get("EditMediaTask")
            print_edit_media_task(edit_task)

        # Live Stream Process Task (live stream processing task)
        elif result.get("LiveStreamProcessTask"):
            live_task = result.get("LiveStreamProcessTask")
            print_live_stream_task(live_task)

        # Extract Blind Watermark Task (blind watermark extraction task)
        elif result.get("ExtractBlindWatermarkTask"):
            watermark_task = result.get("ExtractBlindWatermarkTask")
            print_extract_blind_watermark_task(watermark_task)

        # Schedule Task (scheduling task)
        elif result.get("ScheduleTask"):
            schedule_task = result.get("ScheduleTask")
            print_schedule_task(schedule_task)

        # Live Schedule Task (live streaming scheduling task)
        elif result.get("LiveScheduleTask"):
            live_schedule_task = result.get("LiveScheduleTask")
            print_live_schedule_task(live_schedule_task)

        else:
            # Other task types, notify user
            print(f"   Note: This task type is {task_type}, the current script may not fully support detailed display for this type.")  # NOCA:line-too-long(content cannot be shortened)
            print(f"         To view complete information, use the --verbose or --json parameter.")

        print("-" * 60)
        print(f"   RequestId: {result.get('RequestId', 'N/A')}")

        # Verbose mode: output complete JSON
        if args.verbose:
            print("\nComplete response:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        return result

    except TencentCloudSDKException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Media Processing Task Query —— Query ProcessMedia submitted task status and results",  # NOCA:line-too-long(line cannot be shortened)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query specified task
  python mps_get_video_task.py --task-id 235303-WorkflowTask-80108cc3380155d98b2e3573a48a

  # Query and output complete JSON response
  python mps_get_video_task.py --task-id 235303-WorkflowTask-80108cc3380155d98b2e3573a48a --verbose

  # Only output raw JSON (convenient for pipeline processing)
  python mps_get_video_task.py --task-id 235303-WorkflowTask-80108cc3380155d98b2e3573a48a --json

Environment variables:
  TENCENTCLOUD_SECRET_ID   Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  Tencent Cloud SecretKey
        """
    )

    parser.add_argument("--task-id", type=str, required=True,
                        help="Media processing task ID, returned by ProcessMedia interface")
    parser.add_argument("--region", type=str,
                        help="MPS service region (default ap-guangzhou)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Output complete JSON response")
    parser.add_argument("--json", action="store_true",
                        help="Only output raw JSON, do not print formatted summary")

    args = parser.parse_args()

    print("=" * 60)
    print("Tencent Cloud MPS Media Processing Task Query")
    print("=" * 60)
    print(f"TaskId: {args.task_id}")
    print("-" * 60)

    query_task(args)
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
