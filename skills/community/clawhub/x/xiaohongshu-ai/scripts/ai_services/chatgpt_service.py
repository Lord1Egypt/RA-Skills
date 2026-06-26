import base64
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_TEXT_MODEL = "gpt-5-mini"
IMAGE_MODEL = "gpt-image-2"
DEFAULT_IMAGE_SIZE = "1024x1536"
DEFAULT_IMAGE_QUALITY = "high"


def require_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 OPENAI_API_KEY。请先 export OPENAI_API_KEY='你的 OpenAI API Key'")
    return api_key


def create_client() -> Any:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("缺少 openai SDK。请运行：pip install openai") from exc

    return OpenAI(api_key=require_api_key())


def response_to_dict(response: Any) -> Dict[str, Any]:
    if hasattr(response, "model_dump"):
        return response.model_dump()
    if isinstance(response, dict):
        return response
    raise RuntimeError("openai SDK 返回了无法解析的响应对象")


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
    response = client.responses.create(
        model=text_model or DEFAULT_TEXT_MODEL,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "xhs_note",
                "schema": content_schema,
                "strict": True,
            }
        },
    )
    return json.loads(extract_response_text(response))


def generate_image(
    client: Any,
    prompt: str,
    output_path: Path,
    size: Optional[str] = None,
    quality: Optional[str] = None,
) -> None:
    response = client.images.generate(
        model=IMAGE_MODEL,
        prompt=prompt,
        size=size or DEFAULT_IMAGE_SIZE,
        quality=quality or DEFAULT_IMAGE_QUALITY,
        output_format="png",
        background="opaque",
        n=1,
    )
    response_data = response_to_dict(response)
    data = response_data.get("data") or []
    if not data or not data[0].get("b64_json"):
        raise RuntimeError("图片模型没有返回 b64_json")
    output_path.write_bytes(base64.b64decode(data[0]["b64_json"]))
