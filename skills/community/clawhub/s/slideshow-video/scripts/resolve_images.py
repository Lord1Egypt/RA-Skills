#!/usr/bin/env python3
import argparse
import json
import os
import random
import re
import urllib.parse
import urllib.request

from typing import Dict, List, Optional

UNSPLASH_RANDOM = "https://source.unsplash.com/featured/1200x1800/?{query}"
LOREM_PICSUM = "https://picsum.photos/1200/1800"
PINTEREST_SEARCH = "https://www.pinterest.com/search/pins/?q={query}"
PINTEREST_RESOURCE = "https://www.pinterest.com/resource/BaseSearchResource/get/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"

GPT_IMAGE_MODELS = {
    "openai": "openai/gpt-image-2",
    "kie": "kie/gpt-image-2-text-to-image",
}


class PinterestClient:
    def __init__(self):
        self._cache: Dict[str, object] = {}

    @staticmethod
    def _extract_cookie_value(cookies: List[str], name: str) -> Optional[str]:
        for cookie in cookies:
            if cookie.startswith(f"{name}="):
                return cookie.split("=", 1)[1].split(";", 1)[0]
        return None

    def _get_pinterest_context(self, query: str):
        if self._cache:
            return self._cache

        search_url = PINTEREST_SEARCH.format(query=urllib.parse.quote(query))
        req = urllib.request.Request(
            search_url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        with urllib.request.urlopen(req, timeout=25) as response:
            html = response.read().decode("utf-8", errors="ignore")
            cookies = response.headers.get_all("Set-Cookie") or []

        m = re.search(r'"appVersion":"([^"]+)"', html)
        app_version = m.group(1) if m else ""
        cookie = " ; ".join([c.split(";", 1)[0] for c in cookies])
        csrf = self._extract_cookie_value(cookies, "csrftoken") or ""

        if not app_version or not cookie:
            raise RuntimeError("Could not initialize Pinterest session")

        self._cache = {
            "app_version": app_version,
            "cookie": cookie,
            "csrf": csrf,
            "search_query": query,
        }
        return self._cache

    def fetch_query_images(self, query: str, limit: int = 6, seed: str | None = None) -> List[str]:
        context = self._get_pinterest_context(query)
        data = {
            "options": {
                "query": query,
                "scope": "pins",
                "page_size": max(10, limit * 2),
                "bookmarks": [],
            },
            "context": {},
        }
        payload = urllib.parse.urlencode(
            {
                "source_url": f"/search/pins/?q={urllib.parse.quote(query)}",
                "data": json.dumps(data),
                "_": "0",
            }
        )
        url = f"{PINTEREST_RESOURCE}?{payload}"

        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": PINTEREST_SEARCH.format(query=urllib.parse.quote(query)),
            "Cookie": context["cookie"],
            "X-Requested-With": "XMLHttpRequest",
            "X-Pinterest-App-Version": context["app_version"],
            "X-Pinterest-PWS-Handler": "www/search",
            "X-CSRFToken": context["csrf"],
            "X-APP-VERSION": context["app_version"],
        }

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8", errors="ignore"))

        data_obj = payload.get("resource_response", {})
        results = data_obj.get("data", {}).get("results", [])

        urls: List[str] = []
        for item in results:
            if not isinstance(item, dict):
                continue
            images = item.get("images", {})
            if not isinstance(images, dict):
                continue

            for size_key in ("736x", "474x", "orig", "236x", "170x"):
                image_data = images.get(size_key)
                if isinstance(image_data, dict) and isinstance(image_data.get("url"), str):
                    urls.append(image_data["url"])
                    break

        if not urls:
            return []

        random.seed(seed or query)
        random.shuffle(urls)
        uniq = []
        seen = set()
        for u in urls:
            if u not in seen:
                seen.add(u)
                uniq.append(u)

        return uniq[:limit]


def looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def build_image_url(query: str, seed: str | None = None) -> str:
    q = urllib.parse.quote(query.strip())
    if not q:
        return f"{LOREM_PICSUM}?random={urllib.parse.quote(seed or 'default')}"
    if seed:
        return f"{UNSPLASH_RANDOM.format(query=q)}&sig={urllib.parse.quote(seed)}"
    return UNSPLASH_RANDOM.format(query=q)


def get_openclaw_api_base() -> str:
    return os.environ.get("OPENCLAW_BASE_URL", "http://127.0.0.1:3333").rstrip("/")


def get_openclaw_session_key() -> Optional[str]:
    return os.environ.get("OPENCLAW_SESSION_KEY") or os.environ.get("OPENCLAW_SESSION")


def call_openclaw_image_generate(prompt: str, model: str, size: Optional[str] = None, filename: Optional[str] = None) -> Optional[str]:
    session_key = get_openclaw_session_key()
    if not session_key:
        return None

    payload = {
        "tool": "image_generate",
        "arguments": {
            "action": "generate",
            "model": model,
            "prompt": prompt,
        },
    }
    if size:
        payload["arguments"]["size"] = size
    if filename:
        payload["arguments"]["filename"] = filename

    req = urllib.request.Request(
        f"{get_openclaw_api_base()}/api/sessions/{urllib.parse.quote(session_key)}/tool-call",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=180) as response:
        body = json.loads(response.read().decode("utf-8", errors="ignore"))

    candidates = []
    if isinstance(body, dict):
        for key in ("media", "MEDIA", "path", "output", "result"):
            value = body.get(key)
            if isinstance(value, str):
                candidates.append(value)
        tool_result = body.get("toolResult") or body.get("result")
        if isinstance(tool_result, dict):
            for key in ("media", "MEDIA", "path"):
                value = tool_result.get(key)
                if isinstance(value, str):
                    candidates.append(value)
            if isinstance(tool_result.get("media"), list):
                candidates.extend([item for item in tool_result["media"] if isinstance(item, str)])

    for candidate in candidates:
        if candidate.startswith("MEDIA:"):
            return candidate[len("MEDIA:"):]
        if candidate:
            return candidate
    return None


def resolve_query_image_gpt(query: str, model_key: str, size: Optional[str] = None) -> Optional[str]:
    model = GPT_IMAGE_MODELS.get(model_key)
    if not model:
        raise ValueError(f"Unsupported GPT image provider: {model_key}")
    filename = f"resolved-{model_key}-gpt-image-2.png"
    return call_openclaw_image_generate(query, model=model, size=size or "1024x1536", filename=filename)


def resolve_query_image(query: str, pinterest_client: PinterestClient, source_mode: str = "pinterest") -> str:
    if source_mode in GPT_IMAGE_MODELS:
        generated = resolve_query_image_gpt(query, source_mode)
        if generated:
            return generated
        raise RuntimeError(f"GPT image generation failed for provider: {source_mode}")

    if source_mode == "unsplash":
        return build_image_url(query)

    urls = pinterest_client.fetch_query_images(query, limit=6, seed=query)
    if urls:
        return urls[0]
    return build_image_url(query)


def resolve_project(project: dict, source_mode: str = "pinterest", image_size: Optional[str] = None) -> dict:
    slides = project.get('slides', [])
    if not isinstance(slides, list):
        raise ValueError("project.slides must be a list")

    default_query = project.get('defaultImageQuery')
    pinterest_client = PinterestClient()

    for idx, slide in enumerate(slides, start=1):
        if slide.get('imagePath') or slide.get('imageUrl'):
            continue

        query = slide.get('imageQuery') or default_query
        if not query:
            raise ValueError(f"Slide {idx} is missing imagePath, imageUrl, and imageQuery")

        if source_mode in GPT_IMAGE_MODELS:
            resolved_path = resolve_query_image_gpt(query, source_mode, size=image_size)
            if not resolved_path:
                raise RuntimeError(f"Slide {idx} GPT image generation failed")
            slide['imagePath'] = resolved_path
            slide['resolvedFromQuery'] = query
            slide['resolvedBy'] = GPT_IMAGE_MODELS[source_mode]
        else:
            resolved_url = resolve_query_image(query, pinterest_client, source_mode=source_mode)
            slide['imageUrl'] = resolved_url
            slide['resolvedFromQuery'] = query
            slide['resolvedBy'] = source_mode

    return project


def parse_local_file(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description='Resolve imageQuery fields into imageUrl or imagePath values.')
    parser.add_argument('project', help='Project JSON file')
    parser.add_argument('--output', help='Write resolved project JSON to this path')
    parser.add_argument('--source', default='pinterest', choices=['pinterest', 'unsplash', 'openai', 'kie'], help='How to resolve imageQuery values')
    parser.add_argument('--image-size', default=None, help='Image size hint for GPT image generation, for example 1024x1536 or 1536x1024')
    args = parser.parse_args()

    project = parse_local_file(args.project)
    resolved = resolve_project(project, source_mode=args.source, image_size=args.image_size)
    rendered = json.dumps(resolved, ensure_ascii=False, indent=2)

    if args.output:
        out = args.output
        with open(out, 'w', encoding='utf-8') as f:
            f.write(rendered)
        print(out)
    else:
        print(rendered)


if __name__ == '__main__':
    main()
