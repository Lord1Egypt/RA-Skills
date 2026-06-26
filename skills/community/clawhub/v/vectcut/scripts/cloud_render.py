#!/usr/bin/env python3
"""Cloud Render Script - Render a VectCut draft into a playable/downloadable video."""

import os
import sys
import json
import time
import requests

BASE_URL = "https://open.vectcut.com"
POLL_INTERVAL = 5
TIMEOUT = 600


def render_video(draft_id, resolution="720P", framerate="24"):
    jwt_token = os.getenv("VECTCUT_API_KEY")
    if not jwt_token:
        raise RuntimeError(
            "Environment variable VECTCUT_API_KEY is not set. "
            "Please call the vectcut-login skill first, then retry rendering."
        )

    auth_headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }

    # Step 1: Submit render task
    print(f"[1/2] Submitting render task for draft: {draft_id} ({resolution}, {framerate}fps)...")
    payload = {"draft_id": draft_id, "resolution": resolution, "framerate": framerate}
    resp = requests.post(
        f"{BASE_URL}/cut_jianying/generate_video",
        headers=auth_headers,
        json=payload,
        timeout=30,
    )
    body = resp.json()
    if resp.status_code != 200 or not body.get("success"):
        error = body.get("error") or body.get("output", {}).get("error") or str(body)
        raise RuntimeError(f"generate_video failed: {error}")

    task_id = body["output"]["task_id"]
    print(f"    Task submitted: {task_id}")

    # Step 2: Poll for completion
    print("[2/2] Waiting for render to complete...")
    start = time.time()
    last_status = ""

    while True:
        elapsed = time.time() - start
        if elapsed > TIMEOUT:
            raise RuntimeError(f"Render timed out after {TIMEOUT}s. task_id: {task_id}")

        resp = requests.post(
            f"{BASE_URL}/cut_jianying/task_status",
            headers=auth_headers,
            json={"task_id": task_id},
            timeout=30,
        )
        status_body = resp.json()

        if resp.status_code != 200 or not status_body.get("success"):
            raise RuntimeError(f"task_status request failed: {status_body}")

        output = status_body["output"]
        status = output["status"]
        progress = output.get("progress")
        message = output.get("message")

        if status != last_status:
            progress_str = f" ({progress}%)" if progress is not None else ""
            msg_str = f" - {message}" if message else ""
            print(f"    [{status}]{progress_str}{msg_str}")
            last_status = status

        if output.get("success") and status == "SUCCESS":
            video_url = output.get("result")
            result = {
                "draft_id": draft_id,
                "task_id": task_id,
                "status": "SUCCESS",
                "video_url": video_url,
            }
            print("Render completed successfully!")
            return result

        if status == "FAILURE":
            error = output.get("error") or "Unknown render error"
            raise RuntimeError(f"Render failed: {error}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python cloud_render.py <draft_id> [resolution] [framerate]")
        print("  resolution: 480P / 720P (default) / 1080P / 2K / 4K")
        print("  framerate:  24 (default) / 25 / 30 / 50 / 60")
        sys.exit(1)

    try:
        result = render_video(
            draft_id=sys.argv[1],
            resolution=sys.argv[2] if len(sys.argv) > 2 else "720P",
            framerate=sys.argv[3] if len(sys.argv) > 3 else "24",
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
