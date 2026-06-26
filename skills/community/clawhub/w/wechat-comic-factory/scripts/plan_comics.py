from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common import (  # noqa: E402
    ComicProfile,
    SkillError,
    build_api_url,
    ensure_directory,
    extract_json_object,
    load_config,
    normalize_display_text,
    normalize_comic_type,
    request_with_retry,
    parse_json_response,
    read_text_file,
    setup_logger,
    write_json_file,
)


def render_prompt(profile: ComicProfile, topic: str, count: int) -> str:
    template = read_text_file(profile.prompt_path)
    return (
        template.replace("__COMIC_TYPE__", profile.canonical_name)
        .replace("__TOPIC__", topic)
        .replace("__COUNT__", str(count))
    )


def call_text_llm(
    llm_config: dict[str, Any],
    prompt: str,
    logger,
) -> str:
    provider = str(llm_config.get("provider", "")).strip().lower()
    if provider != "deepseek":
        raise SkillError(
            "text_llm",
            f"暂不支持的文本模型 provider: {provider}",
            hint="当前仅实现 deepseek，可在后续扩展通义文本模型。",
        )

    url = build_api_url(str(llm_config["base_url"]), "/chat/completions")
    payload = {
        "model": llm_config["model"],
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是微信公众号漫画策划助手。你必须严格输出合法 JSON 对象，"
                    "不得输出解释、代码块、前后缀。"
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.8,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {llm_config['api_key']}",
        "Content-Type": "application/json",
    }
    response = request_with_retry(
        "POST",
        url,
        stage="text_llm",
        headers=headers,
        json_body=payload,
        timeout=120,
        logger=logger,
    )
    data = parse_json_response(response, "text_llm")
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise SkillError(
            "text_llm",
            "文本模型返回结构异常",
            details=data,
        ) from exc


def validate_plan_payload(
    payload: dict[str, Any],
    profile: ComicProfile,
    topic: str,
    count: int,
) -> dict[str, Any]:
    title = normalize_display_text(payload.get("title", ""))
    intro = normalize_display_text(payload.get("intro", ""))
    ending = normalize_display_text(payload.get("ending", ""))
    items = payload.get("items")
    if not title:
        raise SkillError("model_output", "模型输出缺少 title")
    if not intro:
        raise SkillError("model_output", "模型输出缺少 intro")
    if not ending:
        raise SkillError("model_output", "模型输出缺少 ending")
    if not isinstance(items, list):
        raise SkillError("model_output", "模型输出缺少 items 数组")
    if len(items) != count:
        raise SkillError(
            "model_output",
            "模型输出的 items 数量与 count 不一致",
            details={"expected": count, "actual": len(items)},
        )

    normalized_items: list[dict[str, Any]] = []
    for expected_index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise SkillError(
                "model_output",
                "items 中存在非对象元素",
                details={"index": expected_index, "item": item},
            )
        image_prompt = normalize_display_text(item.get("image_prompt", ""))
        caption = normalize_display_text(item.get("caption", ""))
        if not image_prompt or not caption:
            raise SkillError(
                "model_output",
                "image_prompt 或 caption 为空",
                details={"index": expected_index, "item": item},
            )
        normalized_items.append(
            {
                "index": expected_index,
                "image_prompt": image_prompt,
                "caption": caption,
            }
        )

    return {
        "comic_type": profile.canonical_name,
        "topic": normalize_display_text(topic),
        "title": title,
        "intro": intro,
        "items": normalized_items,
        "ending": ending,
    }


def plan_comics(comic_type: str, topic: str, count: int, output_dir: str | Path) -> dict[str, Any]:
    if count <= 0:
        raise SkillError("input", "count 必须大于 0")
    output_dir = ensure_directory(output_dir)
    logger = setup_logger("wechat_comic_factory", output_dir)
    profile = normalize_comic_type(comic_type)
    config = load_config(
        required_paths=[
            "text_llm.provider",
            "text_llm.model",
            "text_llm.api_key",
            "text_llm.base_url",
        ]
    )
    logger.info("开始规划漫画：type=%s topic=%s count=%s", profile.canonical_name, topic, count)
    prompt = render_prompt(profile, topic, count)
    raw_content = call_text_llm(config["text_llm"], prompt, logger)
    logger.info("文本模型返回成功，开始清洗 JSON")
    raw_payload = extract_json_object(raw_content, stage="model_output")
    plan_payload = validate_plan_payload(raw_payload, profile, topic, count)
    plan_path = write_json_file(Path(output_dir) / "plan.json", plan_payload)
    logger.info("漫画规划完成，plan_path=%s", plan_path)
    return {
        "success": True,
        "stage": "plan_comics",
        "comic_type": profile.canonical_name,
        "topic": topic,
        "count": count,
        "title": plan_payload["title"],
        "plan_path": str(plan_path),
        "output_dir": str(output_dir),
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="调用文本模型生成漫画分镜规划")
    parser.add_argument("--comic_type", required=True, help="漫画类型，例如：小林漫画")
    parser.add_argument("--topic", required=True, help="漫画主题")
    parser.add_argument("--count", required=True, type=int, help="图片数量")
    parser.add_argument("--output_dir", required=True, help="输出目录")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        result = plan_comics(
            comic_type=args.comic_type,
            topic=args.topic,
            count=args.count,
            output_dir=args.output_dir,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except SkillError as exc:
        print(json.dumps({"success": False, **exc.to_dict()}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
