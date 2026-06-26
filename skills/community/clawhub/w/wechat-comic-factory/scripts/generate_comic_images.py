from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common import (  # noqa: E402
    SkillError,
    build_api_url,
    ensure_directory,
    load_config,
    normalize_comic_type,
    parse_json_response,
    read_json_file,
    request_with_retry,
    resolve_project_path,
    setup_logger,
    write_json_file,
)


def resolve_dashscope_family(model_name: str) -> str:
    normalized = str(model_name).strip().lower()
    if normalized.startswith(("wan2.6", "qwen-image")):
        return "message"
    return "legacy"


def build_dashscope_headers(image_config: dict[str, Any]) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {image_config['api_key']}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }
    workspace_id = str(image_config.get("workspace_id", "")).strip()
    if workspace_id:
        headers["X-DashScope-WorkSpace"] = workspace_id
    return headers


def build_dashscope_submit_request(
    image_config: dict[str, Any],
    prompt: str,
    width: int,
    height: int,
) -> tuple[str, dict[str, Any], str]:
    model_name = str(image_config["model"]).strip()
    family = resolve_dashscope_family(model_name)
    size = f"{width}*{height}"
    if family == "message":
        payload = {
            "model": model_name,
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}],
                    }
                ]
            },
            "parameters": {
                "size": size,
                "n": 1,
            },
        }
        endpoint = "/services/aigc/image-generation/generation"
    else:
        payload = {
            "model": model_name,
            "input": {
                "prompt": prompt,
            },
            "parameters": {
                "size": size,
                "n": 1,
            },
        }
        endpoint = "/services/aigc/text2image/image-synthesis"
    return endpoint, payload, family


def submit_dashscope_task(
    image_config: dict[str, Any],
    prompt: str,
    width: int,
    height: int,
    logger,
) -> dict[str, Any]:
    endpoint, payload, family = build_dashscope_submit_request(image_config, prompt, width, height)
    headers = build_dashscope_headers(image_config)
    url = build_api_url(image_config["base_url"], endpoint)
    logger.info("提交 DashScope 生图任务，model=%s family=%s endpoint=%s", image_config["model"], family, endpoint)
    response = request_with_retry(
        "POST",
        url,
        stage="image_llm",
        headers=headers,
        json_body=payload,
        timeout=120,
        logger=logger,
    )
    data = parse_json_response(response, "image_llm")
    task_id = data.get("output", {}).get("task_id")
    if not task_id:
        raise SkillError(
            "image_llm",
            "DashScope 提交成功但未返回 task_id",
            details=data,
        )
    return data


def poll_dashscope_task(
    image_config: dict[str, Any],
    task_id: str,
    poll_interval: int,
    timeout_seconds: int,
    logger,
) -> dict[str, Any]:
    headers = build_dashscope_headers(image_config)
    headers.pop("X-DashScope-Async", None)
    url = build_api_url(image_config["base_url"], f"/tasks/{task_id}")
    deadline = time.time() + timeout_seconds
    last_payload: dict[str, Any] | None = None

    while time.time() < deadline:
        response = request_with_retry(
            "GET",
            url,
            stage="image_llm",
            headers=headers,
            timeout=90,
            logger=logger,
        )
        payload = parse_json_response(response, "image_llm")
        last_payload = payload
        task_status = str(payload.get("output", {}).get("task_status", "")).upper()
        logger.info("DashScope 任务轮询 task_id=%s status=%s", task_id, task_status or "UNKNOWN")
        if task_status == "SUCCEEDED":
            return payload
        if task_status in {"FAILED", "CANCELED", "UNKNOWN"}:
            raise SkillError(
                "image_llm",
                f"DashScope 生图任务失败: {task_status}",
                details=payload,
            )
        time.sleep(poll_interval)

    raise SkillError(
        "image_llm",
        "DashScope 生图任务轮询超时",
        details={"task_id": task_id, "last_payload": last_payload},
    )


def collect_candidate_urls(payload: Any) -> list[str]:
    candidates: list[str] = []
    url_keys = {"url", "image_url", "result_url", "orig", "origin_url"}

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                lower_key = str(key).lower()
                if (
                    lower_key in url_keys or lower_key.endswith("_url")
                ) and isinstance(value, str) and value.startswith("http"):
                    candidates.append(value)
                walk(value)
            return
        if isinstance(node, list):
            for item in node:
                walk(item)

    walk(payload)
    unique_urls: list[str] = []
    for url in candidates:
        if url not in unique_urls:
            unique_urls.append(url)
    return unique_urls


def extract_legacy_result_url(output_payload: dict[str, Any]) -> str | None:
    for result in output_payload.get("results", []) or []:
        if isinstance(result, dict) and isinstance(result.get("url"), str):
            return str(result["url"])
    return None


def extract_message_result_url(output_payload: dict[str, Any]) -> str | None:
    for choice in output_payload.get("choices", []) or []:
        message = choice.get("message", {}) if isinstance(choice, dict) else {}
        for content in message.get("content", []) or []:
            if not isinstance(content, dict):
                continue
            image_url = content.get("image")
            if isinstance(image_url, str) and image_url.startswith("http"):
                return image_url
    return None


def extract_dashscope_image_url(task_payload: dict[str, Any], model_name: str) -> str:
    # DashScope 任务成功后返回结构会随模型族变化。
    # 若官方结构有变动，优先在这里校准即可。
    output_payload = task_payload.get("output", {})
    family = resolve_dashscope_family(model_name)
    image_url = None
    if family == "message":
        image_url = extract_message_result_url(output_payload)
    else:
        image_url = extract_legacy_result_url(output_payload)
    if image_url:
        return image_url

    urls = collect_candidate_urls(output_payload)
    if not urls:
        raise SkillError(
            "image_llm",
            "DashScope 任务成功，但未在返回结果中找到图片 URL",
            hint="请根据实际 DashScope 返回结构校准 extract_dashscope_image_url。",
            details=task_payload,
        )
    return urls[0]


def download_image(url: str, target_path: Path, logger) -> Path:
    response = request_with_retry(
        "GET",
        url,
        stage="image_download",
        timeout=120,
        logger=logger,
    )
    ensure_directory(target_path.parent)
    target_path.write_bytes(response.content)
    return target_path


def build_font_candidates(config: dict[str, Any]) -> list[Path]:
    defaults = config.get("defaults", {})
    configured = defaults.get("font_path", "./fonts/MiSans-Regular.ttf")
    candidates = [resolve_project_path(configured)]
    windows_fonts = [
        Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
    ]
    for item in windows_fonts:
        if item not in candidates:
            candidates.append(item)
    return candidates


def load_font(config: dict[str, Any], size: int) -> tuple[ImageFont.FreeTypeFont | ImageFont.ImageFont, str]:
    for candidate in build_font_candidates(config):
        if not candidate.exists():
            continue
        try:
            return ImageFont.truetype(str(candidate), size=size), str(candidate)
        except OSError:
            continue
    return ImageFont.load_default(), "Pillow default"


def text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    current = ""
    lines: list[str] = []
    for char in text:
        candidate = f"{current}{char}"
        width, _ = text_size(draw, candidate, font)
        if current and width > max_width:
            lines.append(current)
            current = char
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines or [text]


def overlay_caption(
    source_path: Path,
    target_path: Path,
    caption: str,
    config: dict[str, Any],
    logger,
) -> tuple[Path, str]:
    defaults = config.get("defaults", {})
    font_size = int(defaults.get("caption_font_size", 34))
    line_spacing = int(defaults.get("caption_line_spacing", 12))
    padding_x = int(defaults.get("caption_padding_x", 42))
    padding_y = int(defaults.get("caption_padding_y", 30))

    image = Image.open(source_path).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(overlay)
    font, font_used = load_font(config, font_size)
    lines = wrap_text(temp_draw, caption, font, image.width - padding_x * 2)
    line_heights = [max(text_size(temp_draw, line, font)[1], font_size) for line in lines]
    panel_height = sum(line_heights) + max(0, len(lines) - 1) * line_spacing + padding_y * 2
    panel_top = max(0, image.height - panel_height)

    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle(
        [(0, panel_top), (image.width, image.height)],
        radius=24,
        fill=(0, 0, 0, 160),
    )

    cursor_y = panel_top + padding_y
    for line, line_height in zip(lines, line_heights):
        draw.text(
            (padding_x, cursor_y),
            line,
            font=font,
            fill=(255, 255, 255, 235),
        )
        cursor_y += line_height + line_spacing

    composed = Image.alpha_composite(image, overlay).convert("RGB")
    ensure_directory(target_path.parent)
    composed.save(target_path)
    logger.info("叠字完成，font=%s image=%s", font_used, target_path)
    return target_path, font_used


def generate_comic_images(plan_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    output_dir = ensure_directory(output_dir)
    logger = setup_logger("wechat_comic_factory", output_dir)
    plan = read_json_file(plan_path)
    comic_type = plan.get("comic_type", "")
    profile = normalize_comic_type(comic_type)
    config = load_config(
        required_paths=[
            "image_llm.provider",
            "image_llm.model",
            "image_llm.api_key",
            "image_llm.base_url",
        ]
    )
    defaults = config.get("defaults", {})
    image_width = int(defaults.get("image_width", 1024))
    image_height = int(defaults.get("image_height", 1024))
    poll_interval = int(defaults.get("dashscope_poll_interval", 10))
    timeout_seconds = int(defaults.get("dashscope_timeout_seconds", 300))

    raw_dir = ensure_directory(Path(output_dir) / "raw_images")
    final_dir = ensure_directory(Path(output_dir) / "images")
    images: list[dict[str, Any]] = []

    for item in plan.get("items", []):
        index = int(item["index"])
        prompt = str(item["image_prompt"]).strip()
        caption = str(item["caption"]).strip()
        logger.info("开始生成图片 index=%s prompt=%s", index, prompt)
        submit_result = submit_dashscope_task(
            config["image_llm"],
            prompt=prompt,
            width=image_width,
            height=image_height,
            logger=logger,
        )
        task_id = submit_result["output"]["task_id"]
        task_result = poll_dashscope_task(
            config["image_llm"],
            task_id=task_id,
            poll_interval=poll_interval,
            timeout_seconds=timeout_seconds,
            logger=logger,
        )
        image_url = extract_dashscope_image_url(task_result, str(config["image_llm"]["model"]))
        raw_path = download_image(image_url, raw_dir / f"{index:02d}.png", logger)
        composed_path, font_used = overlay_caption(
            raw_path,
            final_dir / f"{index:02d}.png",
            caption,
            config,
            logger,
        )
        images.append(
            {
                "index": index,
                "image_prompt": prompt,
                "caption": caption,
                "image_path": composed_path.relative_to(output_dir).as_posix(),
                "raw_image_path": raw_path.relative_to(output_dir).as_posix(),
                "task_id": task_id,
                "image_url": image_url,
                "font_used": font_used,
            }
        )

    manifest = {
        "comic_type": profile.canonical_name,
        "topic": plan.get("topic"),
        "title": plan.get("title"),
        "intro": plan.get("intro"),
        "ending": plan.get("ending"),
        "images": images,
    }
    manifest_path = write_json_file(Path(output_dir) / "manifest.json", manifest)
    logger.info("漫画图片生成完成，manifest_path=%s", manifest_path)
    return {
        "success": True,
        "stage": "generate_comic_images",
        "comic_type": profile.canonical_name,
        "title": str(plan.get("title", "")).strip(),
        "manifest_path": str(manifest_path),
        "image_count": len(images),
        "output_dir": str(output_dir),
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="根据 plan.json 生成漫画图片并叠加文案")
    parser.add_argument("--plan_path", required=True, help="plan.json 路径")
    parser.add_argument("--output_dir", required=True, help="输出目录")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        result = generate_comic_images(args.plan_path, args.output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except SkillError as exc:
        print(json.dumps({"success": False, **exc.to_dict()}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
