#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "run.py"
sys.path.insert(0, str(ROOT))

import run


def run_command(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def run_action(action, payload, cwd, allowed_statuses=None):
    allowed_statuses = allowed_statuses or {"success"}
    result = run_command(
        [sys.executable, str(RUN), "-a", action, "-i", json.dumps(payload)],
        cwd=cwd,
    )
    stdout = result.stdout
    start = stdout.find("{")
    if start == -1:
        raise RuntimeError(f"No JSON object in output:\n{stdout}")
    data = json.loads(stdout[start:])
    if data.get("status") not in allowed_statuses:
        raise RuntimeError(f"{action} failed: {data}")
    return data


def wait_for_http_job(client, poll_url, timeout=10):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        response = client.get(poll_url)
        data = response.get_json()
        last = data
        if data.get("status") in {"success", "partial", "skipped", "error"}:
            return data
        time.sleep(0.05)
    raise RuntimeError(f"Job did not finish in time: {last}")


def main():
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required for smoke test")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        video_path = tmp_path / "sample_local.mp4"
        run_command(
            [
                "ffmpeg",
                "-f",
                "lavfi",
                "-i",
                "testsrc=size=160x120:rate=10",
                "-f",
                "lavfi",
                "-i",
                "sine=frequency=1000:sample_rate=44100",
                "-t",
                "1",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-y",
                str(video_path),
            ],
            cwd=tmp_path,
        )

        source = str(video_path)
        checks = [
            ("info", {"source": source}),
            ("thumbnail", {"source": source, "overwrite": True}),
            ("audio", {"source": source, "format": "mp3", "overwrite": True}),
            ("compress", {"source": source, "adaptive": False, "overwrite": True}),
            ("batch", {
                "action": "audio",
                "format": "mp3",
                "overwrite": True,
                "videos": [{"source": source, "name": "batch_local"}],
            }),
        ]

        for action, payload in checks:
            data = run_action(action, payload, tmp_path)
            print(f"{action}: {data['status']}")

        pipeline_checks = [
            {
                "source": source,
                "name": "pipeline_preview",
                "output_dir": "output/pipeline/preview",
                "overwrite": True,
                "steps": [
                    {"id": "metadata", "action": "info", "enabled": True},
                    {"id": "cover", "action": "thumbnail", "enabled": True},
                ],
            },
            {
                "source": source,
                "name": "pipeline_audio",
                "output_dir": "output/pipeline/audio",
                "overwrite": True,
                "steps": [
                    {"id": "audio_mp3", "action": "audio", "enabled": True, "params": {"format": "mp3"}},
                ],
            },
            {
                "source": source,
                "name": "pipeline_skip",
                "output_dir": "output/pipeline/skip",
                "overwrite": True,
                "steps": [
                    {"id": "disabled_audio", "action": "audio", "enabled": False},
                ],
            },
        ]

        for payload in pipeline_checks:
            data = run_action("pipeline", payload, tmp_path, allowed_statuses={"success", "skipped"})
            manifest_path = Path(data["manifest_path"])
            if not manifest_path.exists():
                raise RuntimeError(f"Missing manifest: {manifest_path}")
            manifest = json.loads(manifest_path.read_text())
            if manifest["status"] != data["status"]:
                raise RuntimeError(f"Manifest status mismatch: {manifest}")
            print(f"pipeline:{payload['name']}: {data['status']}")

        chat_checks = [
            ("chat_audio", f'将 "{source}" 提取音频', True),
            ("chat_thumbnail", f'给 "{source}" 提取第 0 秒封面', True),
            ("chat_compress", f'压缩 "{source}"', True),
            ("chat_info", f'查看 "{source}" 信息', False),
        ]
        for name, message, expect_output in chat_checks:
            data = run_action("chat", {"message": message}, tmp_path)
            if not data.get("reply"):
                raise RuntimeError(f"Missing chat reply: {data}")
            if expect_output:
                paths = data.get("output_paths") or []
                if not paths:
                    raise RuntimeError(f"Missing chat output path: {data}")
                output_path = Path(paths[0])
                if not output_path.is_absolute():
                    output_path = tmp_path / output_path
                if not output_path.exists():
                    raise RuntimeError(f"Chat output does not exist: {paths[0]}")
                if paths[0] not in data["reply"]:
                    raise RuntimeError(f"Chat reply does not include output path: {data}")
            print(f"{name}: {data['status']}")

        old_cwd = Path.cwd()
        os.chdir(tmp_path)
        try:
            app = run.create_app()
            client = app.test_client()
            for action, payload, expect_output in [
                ("info", {"source": source, "media_roots": [str(tmp_path)]}, False),
                ("thumbnail", {"source": source, "media_roots": [str(tmp_path)], "overwrite": True}, True),
            ]:
                response = client.post("/skill/jobs", json={"action": action, "params": payload})
                data = response.get_json()
                if response.status_code != 202 or data.get("status") != "queued":
                    raise RuntimeError(f"Async job submit failed: {data}")
                job = wait_for_http_job(client, data["poll_url"])
                if job.get("status") != "success":
                    raise RuntimeError(f"Async job failed: {job}")
                if expect_output:
                    output_paths = job.get("output_paths") or []
                    if not output_paths or not Path(output_paths[0]).exists():
                        raise RuntimeError(f"Async output missing: {job}")
                print(f"job_{action}: {job['status']}")
        finally:
            os.chdir(old_cwd)

        segment_data = run_action(
            "caption_segment",
            {
                "captions": [
                    {
                        "captionTxt": "今天我们聊苹果华为和吉利的新产品",
                        "startTimeUs": 0,
                        "endTimeUs": 3000000,
                    }
                ],
                "max_chars": 12,
                "protected_terms": ["苹果", "华为", "吉利"],
                "overwrite": True,
            },
            tmp_path,
        )
        segment_output = Path(segment_data["outputPath"])
        if not segment_output.exists():
            raise RuntimeError(f"Missing caption segment output: {segment_data}")
        print(f"caption_segment: {segment_data['status']}")

        subtitle_data = run_action(
            "subtitle",
            {"source": source, "mode": "asr", "overwrite": True},
            tmp_path,
            allowed_statuses={"success", "error"},
        )
        if subtitle_data["status"] == "success":
            output_path = Path(subtitle_data["outputPath"])
            if not output_path.is_absolute():
                output_path = tmp_path / output_path
            if not output_path.exists():
                raise RuntimeError(f"Missing subtitle output: {subtitle_data}")
        elif subtitle_data.get("code") != "missing_asr_dependency":
            raise RuntimeError(f"Unexpected subtitle failure: {subtitle_data}")
        print(f"subtitle_asr: {subtitle_data['status']}")


if __name__ == "__main__":
    main()
