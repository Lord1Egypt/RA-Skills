#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Single-article detail fetching and persistence."""

from __future__ import annotations

import json
import mimetypes
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown

from article_metadata_service import get_article_row
from config import get_paths
from database import Database
from log_utils import get_logger
from mp_client import WechatArticleAccessError, WechatMPClient
from utils import (
    article_identity_from_link,
    ensure_dir,
    failure,
    format_timestamp,
    normalize_mp_article_short_url,
    now_ts,
    safe_filename,
    stable_hash,
    success,
    write_json,
)


LOGGER = get_logger(__name__)


def parse_article_html(html: str, fallback_article: dict[str, Any] | None = None) -> dict[str, Any]:
    if "閻滎垰顣ㄥ鍌氱埗" in html or "瑜版挸澧犻悳顖氼暔瀵倸鐖?" in html:
        raise WechatArticleAccessError("瀵邦喕淇婃潻鏂挎礀閻滎垰顣ㄥ鍌氱埗閺嶏繝鐛欐い纰夌礉鐠囩兘鍘ょ純顔诲敩閻炲棗鎮楅柌宥堢槸")
    soup = BeautifulSoup(html, "html.parser")
    container = soup.select_one("#js_content") or soup.select_one("#js_article")
    if not container:
        raise WechatArticleAccessError("妞ょ敻娼版稉顓熸弓閹垫儳鍩岄弬鍥╃彿濮濓絾鏋冪€圭懓娅?")
    for selector in ["script", "style", "#js_pc_qr_code", "#js_tags_preview_toast", "#js_top_ad_area", "#content_bottom_area"]:
        for node in container.select(selector):
            node.decompose()
    activity_name = soup.select_one("#activity-name")
    title = activity_name.get_text(strip=True) if activity_name else ""
    if not title:
        meta_title = soup.find("meta", attrs={"property": "og:title"})
        title = meta_title.get("content", "") if meta_title else ""
    if not title and fallback_article:
        title = str(fallback_article.get("title") or "")
    author = ""
    author_node = soup.select_one("#js_author_name")
    if author_node:
        author = author_node.get_text(strip=True)
    if not author:
        meta_author = soup.find("meta", attrs={"name": "author"})
        author = meta_author.get("content", "") if meta_author else ""
    if not author and fallback_article:
        author = str(fallback_article.get("author_name") or "")
    account_name = ""
    account_node = soup.select_one("#js_name")
    if account_node:
        account_name = account_node.get_text(strip=True)
    if not account_name:
        profile_meta = soup.find("meta", attrs={"property": "profile:nickname"})
        account_name = profile_meta.get("content", "") if profile_meta else ""
    ct_match = re.search(r'var ct = "(?P<ts>\d+)";', html)
    publish_time = int(ct_match.group("ts")) if ct_match else 0
    text_content = "\n".join(line.strip() for line in container.stripped_strings if line.strip())
    digest = text_content.replace("\n", " ")[:160]
    return {
        "title": title,
        "author_name": author,
        "account_name": account_name,
        "publish_time": publish_time,
        "text_content": text_content,
        "digest": digest,
        "html_content": str(container),
    }


def guess_extension(url: str) -> str:
    match = re.search(r"\.(jpg|jpeg|png|gif|webp|bmp)(?:\?|$)", url, re.IGNORECASE)
    if match:
        return f".{match.group(1).lower()}"
    guessed = mimetypes.guess_extension(url.split("?")[0])
    return guessed or ".jpg"


def localize_article_images(
    client: WechatMPClient,
    article_id: str,
    article_link: str,
    html_content: str,
    download_images_enabled: bool,
) -> tuple[str, list[dict[str, Any]]]:
    soup = BeautifulSoup(html_content, "html.parser")
    image_records: list[dict[str, Any]] = []
    article_images_dir = ensure_dir(get_paths().images_dir / article_id.replace(":", "_"))
    LOGGER.debug("download_images article_id=%s enabled=%s", article_id, download_images_enabled)
    for index, node in enumerate(soup.find_all("img"), start=1):
        source = str(node.get("data-src") or node.get("src") or "").strip()
        if not source:
            continue
        if source.startswith("//"):
            source = f"https:{source}"
        extension = guess_extension(source)
        filename = f"image_{index:02d}{extension}"
        local_path = article_images_dir / filename
        saved = False
        error = ""
        if download_images_enabled:
            try:
                binary = client.download_binary(source, referer=article_link, operation="article")
                local_path.write_bytes(binary)
                node["src"] = local_path.as_posix()
                saved = True
            except Exception as exc:  # pragma: no cover
                error = str(exc)
                LOGGER.warning("download_image failed article_id=%s source=%s error=%s", article_id, source, exc)
        image_records.append({"url": source, "local_path": str(local_path) if saved else "", "saved": saved, "error": error})
    return str(soup), image_records


def build_article_detail_payload(
    *,
    article_id: str,
    fakeid: str,
    aid_value: str,
    link: str,
    title: str = "",
    author_name: str = "",
    account_name: str = "",
    digest: str = "",
    create_time: int = 0,
    markdown_content: str = "",
    html_content: str = "",
    images: list[dict[str, Any]] | None = None,
    saved_json_path: str = "",
    saved_md_path: str = "",
    saved_html_path: str = "",
    cached: bool = False,
    include_html: bool = False,
) -> dict[str, Any]:
    return {
        "article_id": article_id,
        "fakeid": fakeid,
        "aid": aid_value,
        "title": title,
        "author_name": author_name,
        "account_name": account_name,
        "digest": digest,
        "link": link,
        "create_time": create_time,
        "create_time_formatted": format_timestamp(create_time),
        "markdown_content": markdown_content,
        "html_content": html_content if include_html else "",
        "images": images or [],
        "saved_json_path": saved_json_path,
        "saved_md_path": saved_md_path,
        "saved_html_path": saved_html_path,
        "cached": cached,
    }


def article_detail(
    db: Database,
    aid: str = "",
    link: str = "",
    download_images: bool = True,
    include_html: bool = False,
    force_refresh: bool = False,
    save_files: bool = True,
) -> dict[str, Any]:
    LOGGER.info("article_detail start aid=%s link=%s download_images=%s include_html=%s force_refresh=%s save_files=%s", aid, link, download_images, include_html, force_refresh, save_files)
    article = get_article_row(db, aid=aid, link=link)
    if not link and article:
        link = str(article.get("link", ""))
    if not link:
        return failure("鏈壘鍒版枃绔犻摼鎺ワ紝璇锋彁渚?link 鎴栫‘淇?aid 宸插湪鏈湴鏁版嵁搴撲腑瀛樺湪")
    link = normalize_mp_article_short_url(link)
    identity = article_identity_from_link(link)
    fakeid = str(article.get("fakeid")) if article else identity["fakeid"]
    aid_value = str(article.get("aid")) if article else identity["aid"]
    article_id = f"{fakeid}:{aid_value}"
    cached = db.row("SELECT * FROM article_detail WHERE article_id = ?", (article_id,))
    if cached and not force_refresh:
        payload = build_article_detail_payload(
            article_id=article_id,
            fakeid=fakeid,
            aid_value=aid_value,
            link=link,
            title=str((article or {}).get("title") or ""),
            author_name=str((article or {}).get("author_name") or ""),
            account_name=str(cached.get("account_name") or ""),
            digest=str((article or {}).get("digest") or ""),
            create_time=int((article or {}).get("create_time") or 0),
            markdown_content=str(cached.get("markdown_content") or ""),
            html_content=str(cached.get("html_content") or ""),
            images=json.loads(cached.get("image_json") or "[]"),
            saved_json_path=str(cached.get("saved_json_path") or ""),
            saved_md_path=str(cached.get("saved_md_path") or ""),
            saved_html_path=str(cached.get("saved_html_path") or ""),
            cached=True,
            include_html=include_html,
        )
        return success(payload, f"宸茶繑鍥炵紦瀛樻枃绔犺鎯? {article_id}")
    client = WechatMPClient(db)
    html = client.fetch_public_article(link)
    parsed = parse_article_html(html, fallback_article=article)
    localized_html, image_records = localize_article_images(client, article_id, link, parsed["html_content"], download_images)
    markdown = html_to_markdown(localized_html, heading_style="ATX")
    now = now_ts()
    article_dir = ensure_dir(get_paths().articles_dir / safe_filename(fakeid or "single"))
    base_name = safe_filename(f"article_{aid_value}", fallback=f"article_{stable_hash(link)}")
    json_path = article_dir / f"{base_name}.json"
    md_path = article_dir / f"{base_name}.md"
    html_path = article_dir / f"{base_name}.html"
    create_time = parsed["publish_time"] or int(article.get("create_time") or 0 if article else 0)
    payload = build_article_detail_payload(
        article_id=article_id,
        fakeid=fakeid,
        aid_value=aid_value,
        link=link,
        title=parsed["title"],
        author_name=parsed["author_name"],
        account_name=parsed["account_name"],
        digest=parsed["digest"],
        create_time=create_time,
        markdown_content=markdown,
        html_content=localized_html,
        images=image_records,
        cached=False,
        include_html=include_html,
    )
    saved_json_path = ""
    saved_md_path = ""
    saved_html_path = ""
    if save_files:
        write_json(json_path, payload)
        md_path.write_text(markdown, encoding="utf-8")
        saved_json_path = str(json_path)
        saved_md_path = str(md_path)
        if include_html:
            html_path.write_text(localized_html, encoding="utf-8")
            saved_html_path = str(html_path)
    with db.transaction():
        db.connection.execute(
            """
            INSERT INTO article_detail
            (article_id, fakeid, aid, link, account_name, markdown_content, html_content, text_content, image_json, saved_json_path, saved_md_path, saved_html_path, fetched_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(article_id) DO UPDATE SET
              account_name = excluded.account_name,
              markdown_content = excluded.markdown_content,
              html_content = excluded.html_content,
              text_content = excluded.text_content,
              image_json = excluded.image_json,
              saved_json_path = excluded.saved_json_path,
              saved_md_path = excluded.saved_md_path,
              saved_html_path = excluded.saved_html_path,
              updated_at = excluded.updated_at,
              fetched_at = excluded.fetched_at
            """,
            (
                article_id, fakeid, aid_value, link, parsed["account_name"], markdown, localized_html, parsed["text_content"],
                json.dumps(image_records, ensure_ascii=False), saved_json_path, saved_md_path, saved_html_path, now, now,
            ),
        )
        db.connection.execute(
            """
            INSERT INTO article (id, fakeid, aid, title, link, digest, cover, author_name, create_time, update_time, is_deleted, detail_fetched, payload_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
              title = excluded.title,
              link = excluded.link,
              digest = excluded.digest,
              author_name = excluded.author_name,
              create_time = CASE WHEN excluded.create_time > 0 THEN excluded.create_time ELSE article.create_time END,
              update_time = excluded.update_time,
              detail_fetched = 1,
              payload_json = excluded.payload_json,
              updated_at = excluded.updated_at
            """,
            (
                article_id, fakeid, aid_value, parsed["title"], link, parsed["digest"], str(article.get("cover") or "") if article else "",
                parsed["author_name"], create_time, now, json.dumps(payload, ensure_ascii=False), now, now,
            ),
        )
    payload["saved_json_path"] = saved_json_path
    payload["saved_md_path"] = saved_md_path
    payload["saved_html_path"] = saved_html_path
    payload["cached"] = False
    if not include_html:
        payload["html_content"] = ""
    return success(payload, f"宸叉姄鍙栨枃绔犺鎯? {parsed['title'] or article_id}")
