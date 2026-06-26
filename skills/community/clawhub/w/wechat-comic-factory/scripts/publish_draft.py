from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common import (  # noqa: E402
    SkillError,
    ensure_directory,
    get_wechat_access_token,
    load_config,
    normalize_display_text,
    read_json_file,
    read_text_file,
    setup_logger,
    update_json_file,
    wechat_post_json,
    wechat_upload_file,
    write_json_file,
)

MAX_WECHAT_TITLE_BYTES = 64
MAX_WECHAT_DIGEST_BYTES = 120


def truncate_utf8_bytes(text: str, max_bytes: int) -> str:
    if len(text.encode("utf-8")) <= max_bytes:
        return text
    current = ""
    for char in text:
        candidate = f"{current}{char}"
        if len(candidate.encode("utf-8")) > max_bytes:
            break
        current = candidate
    return current.strip()


def normalize_wechat_text(text: str) -> str:
    return " ".join(str(text).replace("\r", " ").replace("\n", " ").split()).strip()


def build_draft_articles_payload(
    *,
    title: str,
    digest: str,
    content_html: str,
    thumb_media_id: str,
) -> dict[str, Any]:
    return {
        "articles": [
            {
                "title": title,
                "digest": digest,
                "content": content_html,
                "content_source_url": "",
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
            }
        ]
    }


def extract_wechat_content(html_path: str | Path) -> str:
    soup = BeautifulSoup(read_text_file(html_path), "html.parser")
    container = soup.find("section", id="article-root")
    if container is None:
        body = soup.body
        if body is None:
            raise SkillError("publish_draft", "final.html 缺少可发布的文章内容")
        return "".join(str(child) for child in body.contents)
    return "".join(str(child) for child in container.contents)


def publish_draft(
    html_path: str | Path,
    assets_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    output_dir = ensure_directory(output_dir)
    logger = setup_logger("wechat_comic_factory", output_dir)
    config = load_config(required_paths=["wechat.appid", "wechat.appsecret"])
    assets_payload = read_json_file(assets_path)
    access_token = get_wechat_access_token(config, logger)

    cover_path = Path(output_dir) / str(assets_payload.get("cover_path", "")).strip()
    if not cover_path.exists():
        raise SkillError("publish_draft", f"封面图不存在: {cover_path}")

    cover_upload = wechat_upload_file(
        access_token,
        "/material/add_material",
        cover_path,
        params={"type": "image"},
        logger=logger,
    )
    thumb_media_id = cover_upload.get("media_id")
    if not thumb_media_id:
        raise SkillError(
            "publish_draft",
            "封面图上传成功，但未返回 thumb_media_id",
            details=cover_upload,
        )

    content_html = extract_wechat_content(html_path)
    title = normalize_display_text(assets_payload.get("title", ""))
    topic = normalize_display_text(assets_payload.get("topic", ""))
    digest = normalize_display_text(assets_payload.get("intro", ""))
    if not digest:
        digest = topic
    if not digest:
        images = assets_payload.get("images", [])
        if images:
            digest = normalize_display_text(images[0].get("caption", ""))
    normalized_title = truncate_utf8_bytes(normalize_wechat_text(title), MAX_WECHAT_TITLE_BYTES)
    normalized_digest = truncate_utf8_bytes(normalize_wechat_text(digest), MAX_WECHAT_DIGEST_BYTES)
    attempted_title_fallback = False
    attempted_digest_fallback = False
    while True:
        payload = build_draft_articles_payload(
            title=normalized_title,
            digest=normalized_digest,
            content_html=content_html,
            thumb_media_id=thumb_media_id,
        )
        try:
            draft_result = wechat_post_json(
                access_token,
                "/draft/add",
                payload,
                logger=logger,
            )
            break
        except SkillError as exc:
            errcode = None
            if isinstance(exc.details, dict):
                errcode = exc.details.get("errcode")
            normalized_errcode = int(errcode or 0)
            if normalized_errcode == 45003 and not attempted_title_fallback:
                fallback_seed = topic or normalized_title
                fallback_title = truncate_utf8_bytes(normalize_wechat_text(fallback_seed), 24)
                if fallback_title and fallback_title != normalized_title:
                    logger.warning("微信公众号标题疑似超限，使用更短标题重试: %s -> %s", normalized_title, fallback_title)
                    normalized_title = fallback_title
                    attempted_title_fallback = True
                    continue
            if normalized_errcode == 45004 and not attempted_digest_fallback:
                fallback_digest_seed = topic or normalized_title or "漫画内容"
                fallback_digest = truncate_utf8_bytes(normalize_wechat_text(fallback_digest_seed), 54)
                if fallback_digest and fallback_digest != normalized_digest:
                    logger.warning("微信公众号摘要疑似超限，使用更短摘要重试: %s -> %s", normalized_digest, fallback_digest)
                    normalized_digest = fallback_digest
                    attempted_digest_fallback = True
                    continue
            raise
    publish_result_path = write_json_file(
        Path(output_dir) / "publish_result.json",
        {
            "cover_upload": cover_upload,
            "draft_result": draft_result,
            "title": normalized_title,
            "digest": normalized_digest,
        },
    )
    update_json_file(
        assets_path,
        {
            "thumb_media_id": thumb_media_id,
            "draft_media_id": draft_result.get("media_id"),
            "publish_result_path": str(publish_result_path),
        },
    )
    logger.info("草稿已创建，media_id=%s", draft_result.get("media_id"))
    return {
        "success": True,
        "stage": "publish_draft",
        "title": normalized_title,
        "draft_status": "success",
        "draft_id": draft_result.get("media_id"),
        "draft_media_id": draft_result.get("media_id"),
        "raw_response": draft_result,
        "publish_result_path": str(publish_result_path),
        "output_dir": str(output_dir),
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="将文章推送到微信公众号草稿箱")
    parser.add_argument("--html_path", required=True, help="final.html 路径")
    parser.add_argument("--assets_path", required=True, help="publish_assets.json 路径")
    parser.add_argument("--output_dir", required=True, help="输出目录")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        result = publish_draft(args.html_path, args.assets_path, args.output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except SkillError as exc:
        print(json.dumps({"success": False, **exc.to_dict()}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
