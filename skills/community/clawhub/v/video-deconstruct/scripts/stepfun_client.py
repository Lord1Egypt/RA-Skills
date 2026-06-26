"""StepFun chat completions 封装：原生视频路径（upload → stepfile:// → chat）。"""
from __future__ import annotations

import json
import os
from pathlib import Path

import httpx
from openai import OpenAI

MODEL = "step-1o-turbo-vision"
BASE_URL = "https://api.stepfun.com/v1"
UPLOAD_TIMEOUT_SEC = 600.0
ANALYZE_TIMEOUT_SEC = 420.0


def _api_key() -> str:
    key = os.environ.get("STEP_API_KEY")
    if key:
        return key
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == "STEP_API_KEY":
                return v.strip().strip('"').strip("'")
    raise RuntimeError(
        "STEP_API_KEY 未设置。先 `export STEP_API_KEY=sk-xxx` 或写到 skill 根目录的 .env 文件里，"
        "key 从 https://platform.stepfun.com 拿。"
    )


def _client() -> OpenAI:
    return OpenAI(api_key=_api_key(), base_url=BASE_URL)


def upload_video(video_path: Path) -> str:
    """上传 mp4 到 StepFun 文件 API (purpose=storage)，返回 file_id。"""
    with video_path.open("rb") as f:
        resp = httpx.post(
            f"{BASE_URL}/files",
            headers={"Authorization": f"Bearer {_api_key()}"},
            files={"file": (video_path.name, f, "video/mp4")},
            data={"purpose": "storage"},
            timeout=UPLOAD_TIMEOUT_SEC,
        )
    if resp.status_code != 200:
        raise RuntimeError(f"文件上传失败 (HTTP {resp.status_code}): {resp.text}")
    return resp.json()["id"]


def delete_file(file_id: str) -> None:
    """用完后删除云端文件，避免占用配额。失败不抛。"""
    try:
        httpx.delete(
            f"{BASE_URL}/files/{file_id}",
            headers={"Authorization": f"Bearer {_api_key()}"},
            timeout=30.0,
        )
    except Exception as e:
        print(f"⚠️  清理云端文件 {file_id} 失败（可忽略）: {e}")


def analyze_video(
    file_id: str,
    system_prompt: str,
    rubric_prompt: str,
    asr_transcript: str | None = None,
) -> dict:
    """调用 step-1o-turbo-vision，传 stepfile:// URL，返回解析后的 JSON dict。

    asr_transcript: 若启用 --with-asr，会在用户消息里追加一段 ASR 转录文本，
                    模型可同时利用画面 + 对白做更准确的拆解（落幕文案/心理动机
                    /内容描述都会更精准）。
    """
    client = _client()
    user_content: list[dict] = [
        {"type": "video_url", "video_url": {"url": f"stepfile://{file_id}"}},
    ]
    if asr_transcript:
        user_content.append({
            "type": "text",
            "text": (
                "==================================================\n"
                "【ASR 对白转录（stepaudio-2.5-asr，仅辅助参考，不一定完整）】\n"
                "==================================================\n"
                f"{asr_transcript}\n"
                "==================================================\n"
                "注意：上面是从原视频音轨里 ASR 出来的对白文本，可能有错字/漏字/换行不准。\n"
                "请把它和画面信息**结合**起来分析；尤其是『内容描述』『落幕文案』『受众启示』\n"
                "三个字段要优先采用 ASR 文本而不是凭画面猜测台词。\n"
            ),
        })
    user_content.append({
        "type": "text",
        "text": rubric_prompt + "\n\n严格输出 JSON，禁止任何 markdown 包裹。",
    })
    resp = client.with_options(timeout=ANALYZE_TIMEOUT_SEC).chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_object"},
        max_tokens=8192,
        temperature=0.3,
    )
    raw = resp.choices[0].message.content
    return json.loads(raw)
