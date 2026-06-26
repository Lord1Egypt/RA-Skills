#!/usr/bin/env python3
"""
Tencent Cloud MPS Task Polling Utility Module

Provides poll_video_task() and poll_image_task() functions,
allowing processing scripts to poll and wait inline after submitting tasks,
without requiring the Agent to manually initiate queries.

Usage (imported by other scripts):
    from mps_poll_task import poll_video_task, poll_image_task

    # Poll directly after submitting a task
    result = poll_video_task(task_id, region="ap-guangzhou", interval=10, max_wait=1800)
    result = poll_image_task(task_id, region="ap-guangzhou", interval=5, max_wait=300)
"""

import json
import os
import sys
import time

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


STATUS_MAP = {
    "WAITING": "Waiting",
    "PROCESSING": "Processing",
    "FINISH": "Finished",
    "SUCCESS": "Success",
    "FAIL": "Failed",
}


def _get_credentials():
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        print("Error: Please set environment variables TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
        sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def _create_client(region):
    cred = _get_credentials()
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    http_profile.reqMethod = "POST"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(cred, region, client_profile)


def _fmt(status):
    return STATUS_MAP.get(status, status)


def _print_video_result(result):
    """Print audio/video task result summary (including output file paths)."""
    workflow_task = result.get("WorkflowTask") or {}
    result_set = workflow_task.get("MediaProcessResultSet") or []

    TASK_KEY_MAP = {  # NOCA:invalid-name(module-level constant follows existing naming convention)
        "Transcode": "TranscodeTask",
        "AnimatedGraphics": "AnimatedGraphicsTask",
        "SnapshotByTimeOffset": "SnapshotByTimeOffsetTask",
        "SampleSnapshot": "SampleSnapshotTask",
        "ImageSprites": "ImageSpritesTask",
        "AdaptiveDynamicStreaming": "AdaptiveDynamicStreamingTask",
    }
    TASK_NAME_MAP = {  # NOCA:invalid-name(module-level constant follows existing naming convention)
        "Transcode": "Transcode",
        "AnimatedGraphics": "Animated Graphics",
        "SnapshotByTimeOffset": "Time Offset Snapshot",
        "SampleSnapshot": "Sample Snapshot",
        "ImageSprites": "Image Sprites",
        "AdaptiveDynamicStreaming": "Adaptive Bitrate Streaming",
        "AiAnalysis": "AI Content Analysis",
        "AiRecognition": "AI Content Recognition",
    }

    for i, item in enumerate(result_set, 1):
        task_type = item.get("Type", "")
        type_name = TASK_NAME_MAP.get(task_type, task_type)
        task_key = TASK_KEY_MAP.get(task_type, "")
        task_detail = item.get(task_key, {}) if task_key else None

        if task_detail:
            status = task_detail.get("Status", "")
            err_code = task_detail.get("ErrCode", 0)
            message = task_detail.get("Message", "")
            err_str = f" | Error code: {err_code} - {message}" if err_code != 0 else ""
            print(f"   [{i}] {type_name}: {_fmt(status)}{err_str}")

            output = task_detail.get("Output", {})
            if output:
                out_path = output.get("Path", "")
                out_storage = output.get("OutputStorage", {}) or {}
                out_type = out_storage.get("Type", "")
                if out_type == "COS":
                    cos_out = out_storage.get("CosOutputStorage", {}) or {}
                    bucket = cos_out.get("Bucket", "")
                    region = cos_out.get("Region", "")
                    print(f"       📁 Output: COS - {bucket}:{out_path} (region: {region})")
                    if bucket and out_path and _COS_SDK_AVAILABLE:
                        try:
                            cred = _get_credentials()
                            cos_config = CosConfig(Region=region, SecretId=cred.secret_id, SecretKey=cred.secret_key)
                            cos_client = CosS3Client(cos_config)
                            signed_url = cos_client.get_presigned_url(
                                Bucket=bucket,
                                Key=out_path.lstrip("/"),
                                Method="GET",
                                Expired=3600
                            )
                            print(f"       🔗 Download link (pre-signed, valid for 1 hour): {signed_url}")
                        except Exception as e:  # NOCA:broad-except(SDK exceptions need broad catch for user-friendly error reporting)  # NOCA:line-too-long(line cannot be shortened)
                            print(f"       ⚠️  Failed to generate pre-signed URL: {e}")
                elif out_path:
                    print(f"       📁 Output: {out_path}")


def _print_image_result(result):
    """Print image task result summary (including output file paths and signed URLs)."""
    result_set = result.get("ImageProcessTaskResultSet") or []
    for i, item in enumerate(result_set, 1):
        status = item.get("Status", "")
        err_msg = item.get("ErrMsg", "")
        err_str = f" | Error: {err_msg}" if err_msg else ""
        print(f"   [{i}] Status: {_fmt(status)}{err_str}")

        output = item.get("Output") or {}
        out_path = output.get("Path", "")
        signed_url = output.get("SignedUrl", "")
        out_storage = output.get("OutputStorage", {}) or {}
        out_type = out_storage.get("Type", "")

        if out_type == "COS":
            cos_out = out_storage.get("CosOutputStorage", {}) or {}
            bucket = cos_out.get("Bucket", "")
            region = cos_out.get("Region", "")
            print(f"       📁 Output: COS - {bucket}:{out_path} (region: {region})")
        elif out_path:
            print(f"       📁 Output: {out_path}")

        if signed_url:
            print(f"       🔗 Download link: {signed_url}")
        elif out_type == "COS" and bucket and out_path and _COS_SDK_AVAILABLE:
            try:
                cred = _get_credentials()
                cos_config = CosConfig(Region=region, SecretId=cred.secret_id, SecretKey=cred.secret_key)
                cos_client = CosS3Client(cos_config)
                signed_url = cos_client.get_presigned_url(
                    Bucket=bucket,
                    Key=out_path,
                    Method="GET",
                    Expired=3600
                )
                print(f"       🔗 Download link (pre-signed, valid for 1 hour): {signed_url}")
            except Exception as e:  # NOCA:broad-except(SDK exceptions need broad catch for user-friendly error reporting)  # NOCA:line-too-long(line cannot be shortened)
                print(f"       ⚠️  Failed to generate pre-signed URL: {e}")

        content = output.get("Content", "")
        if content:
            display = content if len(content) <= 100 else content[:100] + "..."
            print(f"       📝 Image-to-text result: {display}")


def poll_video_task(task_id, region="ap-guangzhou", interval=10, max_wait=1800, verbose=False):
    """
    Poll an audio/video processing task (submitted via ProcessMedia) until completion.

    Args:
        task_id:   Task ID
        region:    MPS service region
        interval:  Polling interval (seconds), default 10
        max_wait:  Maximum wait time (seconds), default 1800 (30 minutes)
        verbose:   Whether to output the full JSON

    Returns:
        Final task result dict, or None (on timeout)
    """
    client = _create_client(region)
    elapsed = 0
    attempt = 0

    print(f"\n⏳ Starting task status polling (interval {interval}s, max wait {max_wait}s)...")

    while elapsed < max_wait:
        attempt += 1
        try:
            req = models.DescribeTaskDetailRequest()
            req.from_json_string(json.dumps({"TaskId": task_id}))
            resp = client.DescribeTaskDetail(req)
            result = json.loads(resp.to_json_string())

            status = result.get("Status", "")
            workflow_task = result.get("WorkflowTask") or {}
            wf_status = workflow_task.get("Status", status)

            print(f"   [{attempt}] Status: {_fmt(wf_status)}  (waited {elapsed}s)")

            if wf_status == "FINISH":
                wf_err = workflow_task.get("ErrCode") or 0
                wf_msg = workflow_task.get("Message") or ""
                if wf_err != 0:
                    print(f"\n❌ Task failed! Error code: {wf_err} - {wf_msg}")
                else:
                    print(f"\n✅ Task completed!")
                    _print_video_result(result)

                if verbose:
                    print("\nFull response:")
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                return result

            if wf_status == "FAIL":
                wf_err = workflow_task.get("ErrCode") or 0
                wf_msg = workflow_task.get("Message") or ""
                print(f"\n❌ Task failed! Error code: {wf_err} - {wf_msg}")
                if verbose:
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                return result

        except TencentCloudSDKException as e:
            print(f"   [{attempt}] Query failed: {e}, retrying in {interval}s...")

        time.sleep(interval)
        elapsed += interval

    print(f"\n⚠️  Timed out (waited {max_wait}s), the task may still be processing.")
    print(f"   You can query manually: python scripts/mps_get_video_task.py --task-id {task_id}")
    return None


def poll_image_task(task_id, region="ap-guangzhou", interval=5, max_wait=300, verbose=False):
    """
    Poll an image processing task (submitted via ProcessImage) until completion.

    Args:
        task_id:   Task ID
        region:    MPS service region
        interval:  Polling interval (seconds), default 5
        max_wait:  Maximum wait time (seconds), default 300 (5 minutes)
        verbose:   Whether to output the full JSON

    Returns:
        Final task result dict, or None (on timeout)
    """
    client = _create_client(region)
    elapsed = 0
    attempt = 0

    print(f"\n⏳ Starting task status polling (interval {interval}s, max wait {max_wait}s)...")

    while elapsed < max_wait:
        attempt += 1
        try:
            req = models.DescribeImageTaskDetailRequest()
            req.from_json_string(json.dumps({"TaskId": task_id}))
            resp = client.DescribeImageTaskDetail(req)
            result = json.loads(resp.to_json_string())

            status = result.get("Status", "")
            print(f"   [{attempt}] Status: {_fmt(status)}  (waited {elapsed}s)")

            if status == "FINISH":
                err_code = result.get("ErrCode") or 0
                err_msg = result.get("ErrMsg") or ""
                if err_code != 0:
                    print(f"\n❌ Task failed! Error code: {err_code} - {err_msg}")
                else:
                    print(f"\n✅ Task completed!")
                    _print_image_result(result)

                if verbose:
                    print("\nFull response:")
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                return result

            if status == "FAIL":
                err_code = result.get("ErrCode") or 0
                err_msg = result.get("ErrMsg") or ""
                print(f"\n❌ Task failed! Error code: {err_code} - {err_msg}")
                if verbose:
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                return result

        except TencentCloudSDKException as e:
            print(f"   [{attempt}] Query failed: {e}, retrying in {interval}s...")

        time.sleep(interval)
        elapsed += interval

    print(f"\n⚠️  Timed out (waited {max_wait}s), the task may still be processing.")
    print(f"   You can query manually: python scripts/mps_get_image_task.py --task-id {task_id}")
    return None
# ─── Local file auto-upload ──────────────────────────────────────────────────────────


def auto_upload_local_file(local_path, cos_key=None, verbose=False):
    """
    Automatically upload to COS and return the upload result when a local file path is detected.

    Args:
        local_path: Local file path
        cos_key:    Target COS Key (if not specified, auto-generates /input/<filename>)
        verbose:    Whether to output verbose logs

    Returns:
        dict: { "Bucket", "Region", "Key", "URL", "PresignedURL" }, returns None on failure
    """
    if not os.path.isfile(local_path):
        print(f"❌ Local file does not exist: {local_path}", file=sys.stderr)
        print(f"   Please specify the file source explicitly:", file=sys.stderr)
        print(f"   - Local file: --local-file <local_path>", file=sys.stderr)
        print(f"   - COS file: --cos-input-key <COS_path> (e.g. input/video.mp4)", file=sys.stderr)
        return None

    bucket = os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
    region = os.environ.get("TENCENTCLOUD_COS_REGION", "ap-guangzhou")
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")

    if not bucket:
        print("Error: Local file upload requires the TENCENTCLOUD_COS_BUCKET environment variable to be configured", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
        return None
    if not secret_id or not secret_key:
        print("Error: Please set the environment variables TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
        return None

    if not _COS_SDK_AVAILABLE:
        print("Error: Local file upload requires the COS SDK: pip install cos-python-sdk-v5", file=sys.stderr)
        return None

    # Auto-generate cos_key
    if not cos_key:
        filename = os.path.basename(local_path)
        cos_key = f"/input/{filename}"

    file_size = os.path.getsize(local_path)
    print(f"📤 Local file detected, auto-uploading to COS...")
    print(f"   Local file: {local_path} ({file_size / 1024 / 1024:.2f} MB)")
    print(f"   Target: {bucket}:{cos_key} (region: {region})")

    try:
        cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
        cos_client = CosS3Client(cos_config)

        cos_client.upload_file(
            Bucket=bucket,
            LocalFilePath=local_path,
            Key=cos_key,
            PartSize=10,
            MAXThread=5,
            EnableMD5=False
        )

        url = f"https://{bucket}.cos.{region}.myqcloud.com/{cos_key.lstrip('/')}"
        presigned_url = None
        try:
            presigned_url = cos_client.get_presigned_url(
                Method="GET", Bucket=bucket, Key=cos_key.lstrip("/"), Expired=3600
            )
        except Exception:  # NOCA:broad-except(SDK exceptions need broad catch for user-friendly error reporting)
            pass

        result = {
            "Bucket": bucket,
            "Region": region,
            "Key": cos_key,
            "URL": url,
            "PresignedURL": presigned_url,
        }
        print(f"   ✅ Upload successful! COS Key: {cos_key}")
        return result

    except Exception as e:  # NOCA:broad-except(SDK exceptions need broad catch for user-friendly error reporting)
        print(f"❌ Upload failed: {e}", file=sys.stderr)
        return None


# ─── Task output file extraction and auto-download ───────────────────────────────────

def extract_output_files(task_result):
    """
    Extract all output file information from the task result.

    Returns:
        list of dict: [{ "bucket", "region", "key", "signed_url" }, ...]
    """
    if not task_result:
        return []

    outputs = []

    def _try_presign(bucket, region, key):
        if not bucket or not key or not _COS_SDK_AVAILABLE:
            return None
        try:
            cred = _get_credentials()
            cos_config = CosConfig(Region=region, SecretId=cred.secret_id, SecretKey=cred.secret_key)
            cos_client = CosS3Client(cos_config)
            return cos_client.get_presigned_url(
                Bucket=bucket, Key=key.lstrip("/"), Method="GET", Expired=3600
            )
        except Exception:  # NOCA:broad-except(SDK exceptions need broad catch for user-friendly error reporting)
            return None

    def _add_cos_output(out_storage, out_path, signed_url=None):
        if not out_path:
            return
        out_type = (out_storage or {}).get("Type", "")
        if out_type == "COS":
            cos_out = (out_storage or {}).get("CosOutputStorage", {}) or {}
            bucket = cos_out.get("Bucket", "")
            region = cos_out.get("Region", "")
            if not signed_url:
                signed_url = _try_presign(bucket, region, out_path)
            outputs.append({
                "bucket": bucket, "region": region,
                "key": out_path, "signed_url": signed_url
            })

    # WorkflowTask (video tasks submitted via ProcessMedia)
    workflow_task = task_result.get("WorkflowTask") or {}
    for item in (workflow_task.get("MediaProcessResultSet") or []):
        task_type = item.get("Type", "")
        key_map = {
            "Transcode": "TranscodeTask", "AnimatedGraphics": "AnimatedGraphicsTask",
            "SnapshotByTimeOffset": "SnapshotByTimeOffsetTask",
            "SampleSnapshot": "SampleSnapshotTask", "ImageSprites": "ImageSpritesTask",
            "AdaptiveDynamicStreaming": "AdaptiveDynamicStreamingTask",
            "AudioExtract": "AudioExtractTask",
        }
        task_key = key_map.get(task_type, "")
        task_detail = item.get(task_key, {}) if task_key else None
        if task_detail:
            output = task_detail.get("Output", {}) or {}
            _add_cos_output(output.get("OutputStorage"), output.get("Path", ""))

    # Subtitle task
    for item in (workflow_task.get("SmartSubtitlesTaskResultSet") or []):
        sub_task = item.get("SmartSubtitlesTask") or {}
        output = sub_task.get("Output") or {}
        _add_cos_output(output.get("OutputStorage"), output.get("Path", ""))

    # AiAnalysisResultSet (AI analysis tasks: DubbingTask / SmartEraseTask, etc.)
    for item in (workflow_task.get("AiAnalysisResultSet") or []):
        # DubbingTask (TTS / STS)
        dubbing_task = item.get("DubbingTask") or {}
        if dubbing_task:
            output = dubbing_task.get("Output") or {}
            _add_cos_output(output.get("OutputStorage"), output.get("VideoPath", ""))
            # SpeakerPath (cloned voice audio in STS mode)
            speaker_path = output.get("SpeakerPath", "")
            if speaker_path:
                _add_cos_output(output.get("OutputStorage"), speaker_path)

    # SmartEraseTaskResult (smart erase task)
    smart_erase = workflow_task.get("SmartEraseTaskResult") or {}
    if smart_erase:
        output = smart_erase.get("Output") or {}
        _add_cos_output(output.get("OutputStorage"), output.get("Path", ""))

    # Image Process Task Result Set (image tasks)
    for item in (task_result.get("ImageProcessTaskResultSet") or []):
        output = item.get("Output") or {}
        out_path = output.get("Path", "")
        signed_url = output.get("SignedUrl", "")
        _add_cos_output(output.get("OutputStorage"), out_path, signed_url or None)

    return outputs


def auto_download_outputs(task_result, download_dir=".", verbose=False):
    """
    Automatically download all output files to a local directory after the task completes.

    Args:
        task_result:  Result dict returned by poll_video_task / poll_image_task
        download_dir: Local download directory, defaults to current directory
        verbose:      Whether to output verbose logs

    Returns:
        list of str: List of downloaded local file paths
    """
    outputs = extract_output_files(task_result)
    if not outputs:
        return []

    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")

    if not _COS_SDK_AVAILABLE:
        print("⚠️  COS SDK not installed, skipping auto-download (pip install cos-python-sdk-v5)", file=sys.stderr)
        return []

    os.makedirs(download_dir, exist_ok=True)
    downloaded = []

    print(f"\n📥 Auto-downloading output files to: {os.path.abspath(download_dir)}")
    for i, out in enumerate(outputs, 1):
        bucket = out["bucket"]
        region = out["region"]
        key = out["key"]
        filename = os.path.basename(key.lstrip("/"))
        local_path = os.path.join(download_dir, filename)

        # If filename is duplicated, add a sequence number
        if os.path.exists(local_path):
            base, ext = os.path.splitext(filename)
            local_path = os.path.join(download_dir, f"{base}_{i}{ext}")

        print(f"   [{i}] {bucket}:{key} → {local_path}")
        try:
            cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
            cos_client = CosS3Client(cos_config)
            cos_client.download_file(
                Bucket=bucket,
                Key=key.lstrip("/"),
                DestFilePath=local_path
            )
            file_size = os.path.getsize(local_path)
            print(f"       ✅ Download successful ({file_size / 1024 / 1024:.2f} MB): {local_path}")
            downloaded.append(local_path)
        except Exception as e:  # NOCA:broad-except(SDK exceptions need broad catch for user-friendly error reporting)
            print(f"       ❌ Download failed: {e}", file=sys.stderr)

    if downloaded:
        print(f"\n✅ Downloaded {len(downloaded)} files in total to {os.path.abspath(download_dir)}")

    return downloaded


def auto_gen_compare(task_result, input_url, media_type="video", title=None, output_path=None):
    """
    Automatically generate a comparison HTML page after the task completes.

    Args:
        task_result: Task result dict after polling completion
        input_url:   Original input URL (or COS permanent link)
        media_type:  Media type 'video' or 'image'
        title:       Comparison page title (auto-generated by default)
        output_path: Output HTML path (auto-generated to evals/test_result/ by default)

    Returns:
        str: Path of the generated HTML file, returns None on failure
    """
    if not task_result:
        return None

    try:
        from mps_gen_compare import generate_html, get_display_name
    except ImportError:
        print("⚠️  mps_gen_compare module not found, skipping comparison page generation", file=sys.stderr)
        return None

    # Extract output files
    outputs = extract_output_files(task_result)
    if not outputs:
        print("⚠️  No output files found, skipping comparison page generation", file=sys.stderr)
        return None

    # Get the presigned URL of the first output file
    out = outputs[0]
    enhanced_url = out.get("signed_url", "")
    if not enhanced_url and out.get("bucket") and out.get("key"):
        enhanced_url = f"https://{out['bucket']}.cos.{out['region']}.myqcloud.com/{out['key'].lstrip('/')}"

    if not enhanced_url:
        print("⚠️  Unable to get output file URL, skipping comparison page generation", file=sys.stderr)
        return None

    # Build comparison data
    if not title:
        type_label = "Video" if media_type == "video" else "Image"
        title = f"{type_label} Processing Effect Comparison"

    pairs = [{
        'original': input_url,
        'enhanced': enhanced_url,
        'type': media_type,
        'title': '',
    }]

    # Determine output path
    if not output_path:
        from datetime import datetime as _dt
        script_dir = os.path.dirname(os.path.abspath(__file__))
        result_dir = os.path.join(os.path.dirname(script_dir), "evals", "test_result")
        os.makedirs(result_dir, exist_ok=True)
        timestamp = _dt.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(result_dir, f"compare_{timestamp}.html")

    # Generate HTML
    html = generate_html(pairs, title=title)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    orig_name = get_display_name(input_url)
    enh_name = get_display_name(enhanced_url)
    icon = "🎬" if media_type == "video" else "🖼️"
    print(f"\n{icon} Comparison page generated: {output_path}")
    print(f"   Original: {orig_name}")
    print(f"   Enhanced: {enh_name}")

    return output_path
# Command Line Entry
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Tencent Cloud MPS Task Polling Tool - Supports Audio/Video and Image Tasks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Examples:
  # Poll audio/video task
  python mps_poll_task.py --task-id 1234567890 --type video

  # Poll image task
  python mps_poll_task.py --task-id 1234567890 --type image

  # Specify region and polling parameters
  python mps_poll_task.py --task-id 1234567890 --region ap-beijing --interval 5 --max-wait 600

  # Verbose output mode
  python mps_poll_task.py --task-id 1234567890 --verbose

Environment Variables:
  TENCENTCLOUD_SECRET_ID    - Tencent Cloud SecretId (required)
  TENCENTCLOUD_SECRET_KEY   - Tencent Cloud SecretKey (required)
        """.strip()
    )

    parser.add_argument(
        '--task-id',
        required=True,
        help='Task ID (required)'
    )
    parser.add_argument(
        '--region',
        default='ap-guangzhou',
        help='MPS service region (default: ap-guangzhou)'
    )
    parser.add_argument(
        '--type',
        choices=['video', 'image'],
        default='video',
        help='Task type: video(audio/video) or image (default: video)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=None,
        help='Polling interval in seconds (default: video=10, image=5)'
    )
    parser.add_argument(
        '--max-wait',
        type=int,
        default=None,
        help='Maximum wait time in seconds (default: video=1800, image=300)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Output detailed logs (includes full API responses)'
    )

    args = parser.parse_args()

    # Set default values
    interval = args.interval or (10 if args.type == 'video' else 5)
    max_wait = args.max_wait or (1800 if args.type == 'video' else 300)

    # Execute polling
    if args.type == 'video':
        result = poll_video_task(args.task_id, args.region, interval, max_wait, args.verbose)
    else:
        result = poll_image_task(args.task_id, args.region, interval, max_wait, args.verbose)

    # Set exit code based on result
    if result is None:
        sys.exit(1)  # Timeout
    elif result.get('Status') == 'FAIL' or (result.get('WorkflowTask', {}).get('ErrCode', 0) != 0):
        sys.exit(2)  # Task failed
    else:
        sys.exit(0)  # Success
