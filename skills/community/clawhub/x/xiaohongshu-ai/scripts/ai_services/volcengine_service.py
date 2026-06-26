import base64
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


ARK_BASE_URL = os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
DEFAULT_TEXT_MODEL = "doubao-seed-2-0-pro-260215"
IMAGE_MODEL = "doubao-seedream-4-5-251128"
DEFAULT_IMAGE_SIZE = "2K"
DEFAULT_WATERMARK = os.getenv("XHS_VOLCENGINE_WATERMARK", "false").lower() in {"1", "true", "yes", "on"}


def require_api_key() -> str:
    api_key = os.getenv("ARK_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 ARK_API_KEY。请先 export ARK_API_KEY='你的火山引擎 Ark API Key'")
    return api_key


def create_client(base_url: Optional[str] = None) -> Any:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("缺少 openai SDK。请运行：pip install openai") from exc

    return OpenAI(
        base_url=base_url or ARK_BASE_URL,
        api_key=require_api_key(),
    )


def response_to_dict(response: Any) -> Dict[str, Any]:
    if hasattr(response, "model_dump"):
        return response.model_dump()
    if isinstance(response, dict):
        return response
    raise RuntimeError("openai SDK 返回了无法解析的响应对象")


def event_value(event: Any, key: str) -> Any:
    if isinstance(event, dict):
        return event.get(key)
    return getattr(event, key, None)


def extract_response_text(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text

    response_data = response_to_dict(response)
    if response_data.get("output_text"):
        return response_data["output_text"]

    chunks = []
    for item in response_data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                chunks.append(content["text"])
    if not chunks:
        raise RuntimeError("文本模型没有返回可解析内容")
    return "".join(chunks)


def generate_content(
    client: Any,
    system_prompt: str,
    user_prompt: str,
    content_schema: Dict[str, Any],
    text_model: Optional[str] = None,
) -> Dict[str, Any]:
    prompt = (
        f"{system_prompt}\n\n"
        f"{user_prompt}\n\n"
        "只返回一个 JSON 对象，不要输出 Markdown 或解释。JSON 必须符合这个 schema：\n"
        f"{json.dumps(content_schema, ensure_ascii=False)}"
    )
    response = client.responses.create(
        model=text_model or DEFAULT_TEXT_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                ],
            }
        ],
    )
    return json.loads(extract_response_text(response))


def generate_image(
    client: Any,
    prompt: str,
    output_path: Path,
    size: Optional[str] = None,
    watermark: Optional[bool] = None,
) -> None:
    events = client.images.generate(
        model=IMAGE_MODEL,
        prompt=prompt,
        size=size or DEFAULT_IMAGE_SIZE,
        response_format="b64_json",
        stream=True,
        extra_body={
            "watermark": DEFAULT_WATERMARK if watermark is None else watermark,
            "sequential_image_generation": "auto",
            "sequential_image_generation_options": {
                "max_images": 1,
            },
        },
    )

    image_b64 = None
    for event in events:
        if event is None:
            continue
        event_type = event_value(event, "type")
        event_b64 = event_value(event, "b64_json")
        if event_b64 and event_type in {"image_generation.partial_succeeded", "image_generation.completed", None}:
            image_b64 = event_b64

    if not image_b64:
        raise RuntimeError("火山引擎图片模型没有返回 b64_json")
    output_path.write_bytes(base64.b64decode(image_b64))
