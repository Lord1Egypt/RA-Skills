#!/usr/bin/env python3
"""
GSData adapter skeleton:
- Wrap 292 endpoints into 11 high-level tools
- Route (tool, action, platform) -> concrete router path
- Sign/auth requests with GSData open platform protocol
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests


DEFAULT_BASE_URL = "http://databus.gsdata.cn:8888/api/service"
DEFAULT_MAPPING_PATH = Path(__file__).with_name("gsdata_tool_mapping_v1.json")
DEFAULT_CREDS_PATH = Path.home() / ".config" / "gsdata" / "credentials.json"


ACCOUNT_PLATFORMS = {
    "weixin",
    "weibo",
    "toutiao",
    "douyin",
    "kuaishou",
    "bili",
    "wxvideo",
    "xigua",
    "xiaohongshu",
}


CONTENT_SEARCH_SORTS = {
    "weixin": {"time": "search1", "read": "search2", "watching": "search3"},
    "weibo": {
        "time": "search1",
        "comment": "search2",
        "repost": "search3",
        "like": "search4",
    },
    "toutiao": {"time": "search1", "comment": "search2", "read": "search3"},
    "xiaohongshu": {"time": "search1", "like": "search2", "comment": "search3"},
    "douyin": {"time": "search1", "like": "search2", "comment": "search3"},
    "kuaishou": {"time": "search1", "like": "search2", "comment": "search3"},
    "bili": {"time": "search1", "like": "search2", "comment": "search3"},
    "wxvideo": {"time": "search1", "like": "search2", "comment": "search3"},
    "xigua": {"time": "search1", "like": "search2", "comment": "search3"},
}


ACCOUNT_LATEST_SUFFIX = {
    "weixin": "news-latest",
    "weibo": "news-latest",
    "toutiao": "news-latest",
    "douyin": "video-latest",
    "kuaishou": "video-latest",
    "bili": "video-latest",
    "wxvideo": "video-latest",
    "xigua": "video-latest",
    "xiaohongshu": "article-latest",
}


ACCOUNT_INFLUENCE_PREFIX = {
    "weixin": "wci",
    "weibo": "bci",
    "toutiao": "tgi",
    "douyin": "dci",
    "kuaishou": "kci",
    "bili": "bvci",
    "wxvideo": "wvci",
    "xigua": "xci",
    "xiaohongshu": "hci",
}


PUBSENT_SEARCH_ACTIONS = {
    "search": "index",
    "num_found": "num-found",
    "emotion_dist": "emotion-dist",
    "yuqing_trend": "yuqing-trend",
    "hot_word": "hot-word",
    "media_dist": "media-dist",
    "hot_refer_area": "hot-refer-area",
    "hot_pub_area": "hot-pub-area",
    "news_trend": "news-trend",
}


PUBSENT_HOT_ACTIONS = {
    "event_list": "index",
    "event_keywords": "hot-keywords",
    "pub_area": "hot-pub-area",
    "refer_area": "hot-refer-area",
    "media_active": "media-active",
    "emotion_dist": "emotion-dist",
    "media_dist": "media-dist",
    "news_list": "news-list",
    "entity_person": "news-entity-person",
    "entity_org": "news-entity-organization",
}


PUBSENT_WARNING_ACTIONS = {
    "list_rules": "index",
    "create_rule": "create",
    "update_rule": "update",
    "open_rule": "open",
    "close_rule": "close",
    "news_push": "news",
    "stats": "stats",
    "add_rec_email": "add-rec-email",
    "del_rec_email": "del-rec-email",
}


NLP_ACTION_TO_PATH = {
    "emotion_long": "/nlp/emotion/emotion-long",
    "emotion_short": "/nlp/emotion/emotion-short",
    "oversea_emotion_long": "/nlp/emotion/oversea-emotion-long",
    "oversea_emotion_short": "/nlp/emotion/oversea-emotion-short",
    "emotion_weibo": "/nlp/emotion/emotion-weibo",
    "sentiment_long": "/nlp/sentiment/sentiment-long",
    "sentiment_short": "/nlp/sentiment/sentiment-short",
    "oversea_sentiment_long": "/nlp/sentiment/oversea-sentiment-long",
    "oversea_sentiment_short": "/nlp/sentiment/oversea-sentiment-short",
    "category_long": "/nlp/category/category-long",
    "category_short": "/nlp/category/category-short",
    "oversea_category_long": "/nlp/category/oversea-category-long",
    "oversea_category_short": "/nlp/category/oversea-category-short",
    "demoner": "/nlp/demoner/index",
    "summary": "/nlp/summary/index",
    "generate_title": "/nlp/summary/generate-title",
    "association": "/nlp/demo-association/index",
    "graph_vertex": "/nlp/graph/get-graph-vertex",
    "graph_edge": "/nlp/graph/get-graph-edge",
    "graph_disambiguation": "/nlp/graph/get-graph-disambiguation",
    "car_tag": "/nlp/car/tag",
    "car_auto_sentiment": "/nlp/car/auto-sentiment",
    "seg_word": "/nlp/other/seg-word",
    "keywords": "/nlp/other/demo-keywords",
    "pos": "/nlp/other/demo-pos",
    "ocr_image": "/nlp/other/ocr-image",
    "region": "/nlp/region/common-region",
    "corrector": "/nlp/corrector/index",
    "point_extract": "/nlp/point/extract",
}


WRITE_SUFFIX_HINTS = (
    "create",
    "update",
    "add",
    "del",
    "open",
    "close",
    "group-add",
    "group-del",
    "acct-add",
    "acct-del",
)


@dataclass
class Endpoint:
    tool: str
    cate_id: int
    cate_name: str
    method: str
    path: str
    desc: str


def load_mapping(mapping_path: Path) -> Tuple[List[Endpoint], Dict[str, str]]:
    payload = json.loads(mapping_path.read_text(encoding="utf-8"))
    endpoints: List[Endpoint] = []
    method_by_path: Dict[str, str] = {}
    for tool_item in payload.get("tools", []):
        tool = tool_item["tool"]
        for ep in tool_item.get("endpoints", []):
            endpoint = Endpoint(
                tool=tool,
                cate_id=int(ep["cateId"]),
                cate_name=ep["cateName"],
                method=ep["method"].upper(),
                path=ep["path"],
                desc=ep["desc"],
            )
            endpoints.append(endpoint)
            method_by_path[endpoint.path] = endpoint.method
    return endpoints, method_by_path


def make_sign(params: Dict[str, Any], app_secret: str) -> str:
    # GSData signature: md5(app_secret + "_" + sorted(kv concat) + "_" + app_secret)
    sorted_items = sorted(params.items(), key=lambda x: x[0])
    concat = "".join(f"{k}{v}" for k, v in sorted_items)
    raw = f"{app_secret}_{concat}_{app_secret}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def make_access_token(app_key: str, sign: str, router: str) -> str:
    return base64.b64encode(f"{app_key}:{sign}:{router}".encode("utf-8")).decode(
        "utf-8"
    )


class GsDataAdapter:
    def __init__(
        self,
        app_key: str,
        app_secret: str,
        base_url: str = DEFAULT_BASE_URL,
        mapping_path: Path = DEFAULT_MAPPING_PATH,
    ) -> None:
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = base_url
        self.mapping_path = mapping_path
        self.endpoints, self.method_by_path = load_mapping(mapping_path)

    def list_tools(self) -> List[str]:
        tools = {ep.tool for ep in self.endpoints}
        tools.add("gsdata_raw")
        return sorted(tools)

    def list_endpoints(self, tool: Optional[str] = None) -> List[Endpoint]:
        if not tool:
            return self.endpoints
        return [ep for ep in self.endpoints if ep.tool == tool]

    def resolve_route(
        self,
        tool: str,
        action: str,
        platform: Optional[str] = None,
        sort: Optional[str] = None,
        path: Optional[str] = None,
    ) -> str:
        if tool == "gsdata_raw":
            if not path:
                raise ValueError("gsdata_raw requires explicit path")
            return path

        if tool == "gsdata_link_resolve":
            if action != "resolve_wechat_url":
                raise ValueError("gsdata_link_resolve only supports resolve_wechat_url")
            return "/spread/gsdata/wx-detail"

        if tool == "gsdata_account":
            self._require_platform(platform)
            if action == "search":
                return f"/account/{platform}/search"
            if action == "attribute":
                return f"/account/{platform}/attribute"
            if action == "latest_content":
                return f"/account/{platform}/{ACCOUNT_LATEST_SUFFIX[platform]}"
            if action == "influence_latest":
                return (
                    f"/account/{platform}/{ACCOUNT_INFLUENCE_PREFIX[platform]}-latest"
                )
            if action == "influence_weekly":
                return (
                    f"/account/{platform}/{ACCOUNT_INFLUENCE_PREFIX[platform]}-weekly"
                )
            if action == "index_latest":
                return f"/account/{platform}/index-latest"
            if action == "index_weekly":
                return f"/account/{platform}/index-weekly"
            if action == "get_ygfs":
                if platform != "weixin":
                    raise ValueError("get_ygfs only supports platform=weixin")
                return "/account/weixin/get-ygfs"
            raise ValueError(f"Unsupported action for gsdata_account: {action}")

        if tool == "gsdata_content":
            self._require_platform(platform)
            if action == "search":
                if not sort:
                    sort = "time"
                return self._resolve_content_search_route(platform, sort)
            if action == "get_content":
                if platform != "weixin":
                    raise ValueError("get_content only supports platform=weixin")
                return "/weixin/article/content"
            if action == "get_clean_content":
                if platform != "weixin":
                    raise ValueError("get_clean_content only supports platform=weixin")
                return "/weixin/article/clean-content"
            raise ValueError(f"Unsupported action for gsdata_content: {action}")

        if tool == "gsdata_rank_public":
            self._require_platform(platform)
            suffix = self._enum(action, {"day", "week", "month", "latest"}, "action")
            return f"/rank/{platform}/{suffix}"

        if tool == "gsdata_myrank_group":
            self._require_platform(platform)
            suffix_map = {
                "group_add": "group-add",
                "group_list": "group-list",
                "group_del": "group-del",
            }
            suffix = self._map_action(action, suffix_map, tool)
            return f"/myrank/{platform}/{suffix}"

        if tool == "gsdata_myrank_account":
            self._require_platform(platform)
            if action == "acct_add":
                return f"/myrank/{platform}/acct-add"
            if action == "acct_del":
                return f"/myrank/{platform}/acct-del"
            if action == "acct_list":
                return f"/myrank/{platform}/acct-list"
            if action == "acct_add_by_url":
                # Some platforms use acct-url-add, while weixin uses acct-add-by-url.
                candidates = [
                    f"/myrank/{platform}/acct-url-add",
                    f"/myrank/{platform}/acct-add-by-url",
                ]
                for cand in candidates:
                    if cand in self.method_by_path:
                        return cand
                raise ValueError(f"Platform={platform} does not support acct_add_by_url")
            if action == "search_account":
                candidate = f"/myrank/{platform}/search-account"
                if candidate not in self.method_by_path:
                    raise ValueError(
                        f"Platform={platform} does not support search_account"
                    )
                return candidate
            raise ValueError(f"Unsupported action for gsdata_myrank_account: {action}")

        if tool == "gsdata_myrank_query":
            self._require_platform(platform)
            suffix_map = {
                "day": "day",
                "week": "week",
                "month": "month",
                "latest": "latest",
                "group_article": "group-article",
            }
            suffix = self._map_action(action, suffix_map, tool)
            return f"/myrank/{platform}/{suffix}"

        if tool == "gsdata_pubsent_search":
            suffix = self._map_action(action, PUBSENT_SEARCH_ACTIONS, tool)
            return f"/pubsent/full-search/{suffix}"

        if tool == "gsdata_pubsent_hot":
            suffix = self._map_action(action, PUBSENT_HOT_ACTIONS, tool)
            return f"/pubsent/hot-news/{suffix}"

        if tool == "gsdata_pubsent_warning":
            suffix = self._map_action(action, PUBSENT_WARNING_ACTIONS, tool)
            return f"/pubsent/warning/{suffix}"

        if tool == "gsdata_nlp":
            route = NLP_ACTION_TO_PATH.get(action)
            if not route:
                raise ValueError(f"Unsupported action for gsdata_nlp: {action}")
            return route

        raise ValueError(f"Unsupported tool: {tool}")

    def invoke(
        self,
        tool: str,
        action: str,
        params: Optional[Dict[str, Any]] = None,
        platform: Optional[str] = None,
        sort: Optional[str] = None,
        dry_run: bool = False,
        allow_write: bool = False,
        explicit_path: Optional[str] = None,
        explicit_method: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = params or {}
        route = self.resolve_route(
            tool=tool, action=action, platform=platform, sort=sort, path=explicit_path
        )
        params = self._normalize_params(tool=tool, action=action, route=route, params=params)
        method = (
            (explicit_method or "").upper().strip() or self.method_by_path.get(route, "GET")
        )

        if self._is_write_route(route) and not allow_write:
            return {
                "ok": False,
                "error": "WRITE_BLOCKED",
                "message": (
                    "This route is considered write/high-risk. "
                    "Pass allow_write=true after explicit confirmation."
                ),
                "route": route,
                "method": method,
            }

        sign = make_sign(params, self.app_secret)
        token = make_access_token(self.app_key, sign, route)
        headers = {"access-token": token}

        if dry_run:
            return {
                "ok": True,
                "dryRun": True,
                "tool": tool,
                "action": action,
                "platform": platform,
                "route": route,
                "method": method,
                "params": params,
            }

        try:
            response = self._request(method=method, params=params, headers=headers)
            body: Any
            try:
                body = response.json()
            except Exception:
                body = {"raw": response.text}
            return {
                "ok": response.ok,
                "statusCode": response.status_code,
                "tool": tool,
                "action": action,
                "platform": platform,
                "route": route,
                "method": method,
                "response": body,
            }
        except Exception as exc:
            return {
                "ok": False,
                "tool": tool,
                "action": action,
                "platform": platform,
                "route": route,
                "method": method,
                "error": str(exc),
            }

    def _request(
        self, method: str, params: Dict[str, Any], headers: Dict[str, str]
    ) -> requests.Response:
        # GSData gateway commonly accepts params in query/body against one base URL.
        if method == "POST":
            return requests.post(
                self.base_url, data=params, headers=headers, timeout=30
            )
        return requests.get(self.base_url, params=params, headers=headers, timeout=30)

    @staticmethod
    def _is_write_route(route: str) -> bool:
        if "/warning/" in route:
            # warning module has both read and write; keep reads open
            if route.endswith(("/index", "/news", "/stats")):
                return False
            return True
        return any(s in route for s in WRITE_SUFFIX_HINTS)

    @staticmethod
    def _map_action(action: str, action_map: Dict[str, str], tool: str) -> str:
        if action not in action_map:
            supported = ", ".join(sorted(action_map.keys()))
            raise ValueError(f"{tool} unsupported action={action}. supported: {supported}")
        return action_map[action]

    @staticmethod
    def _enum(value: str, enums: set, name: str) -> str:
        if value not in enums:
            supported = ", ".join(sorted(enums))
            raise ValueError(f"Unsupported {name}={value}. supported: {supported}")
        return value

    @staticmethod
    def _require_platform(platform: Optional[str]) -> str:
        if not platform:
            raise ValueError("platform is required")
        if platform not in ACCOUNT_PLATFORMS:
            supported = ", ".join(sorted(ACCOUNT_PLATFORMS))
            raise ValueError(f"Unsupported platform={platform}. supported: {supported}")
        return platform

    @staticmethod
    def _resolve_content_search_route(platform: str, sort: str) -> str:
        mapping = CONTENT_SEARCH_SORTS.get(platform)
        if not mapping:
            raise ValueError(f"Unsupported content search platform={platform}")
        if sort not in mapping:
            supported = ", ".join(sorted(mapping.keys()))
            raise ValueError(
                f"Unsupported sort={sort} for platform={platform}. supported: {supported}"
            )
        suffix = mapping[sort]

        if platform in {"weixin", "weibo", "toutiao"}:
            return f"/{platform}/article/{suffix}"
        if platform == "xiaohongshu":
            return f"/article/xiaohongshu/{suffix}"
        return f"/shortvideo/{platform}/{suffix}"

    @staticmethod
    def _normalize_params(
        tool: str, action: str, route: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        out = dict(params)

        # common pagination aliases
        for src in ("size", "limit", "page_size", "pagesize"):
            if src in out and "pageSize" not in out:
                out["pageSize"] = out.pop(src)

        if tool != "gsdata_pubsent_search":
            return out

        # common date aliases -> GSData expected keys
        start_aliases = ("date_start", "start_date", "from_date", "from", "posttimeStart")
        end_aliases = ("date_end", "end_date", "to_date", "to", "posttimeEnd")
        for key in start_aliases:
            if key in out and "posttime_start" not in out:
                out["posttime_start"] = out.pop(key)
                break
        for key in end_aliases:
            if key in out and "posttime_end" not in out:
                out["posttime_end"] = out.pop(key)
                break

        # keyword aliases differ by endpoint.
        # yuqing_trend expects keywords; most others expect keywords_include.
        keyword_candidates = ("keywords", "keyword", "kw")
        if action == "yuqing_trend":
            if "keywords" not in out:
                if "keywords_include" in out:
                    out["keywords"] = out["keywords_include"]
                else:
                    for key in keyword_candidates:
                        if key in out:
                            out["keywords"] = out[key]
                            break
        else:
            if "keywords_include" not in out:
                for key in ("keywords_include",) + keyword_candidates:
                    if key in out:
                        out["keywords_include"] = out[key]
                        break

        # normalize date format to YYYY-MM-DD for pubsent.
        for key in ("posttime_start", "posttime_end"):
            if key not in out:
                continue
            val = str(out[key]).strip()
            if len(val) == 8 and val.isdigit():
                val = f"{val[0:4]}-{val[4:6]}-{val[6:8]}"
            if len(val) >= 10 and val[4] == "-" and val[7] == "-":
                val = val[:10]
            out[key] = val

        # make date-granularity end-date inclusive: [start, end+1day)
        if "posttime_end" in out:
            try:
                end_dt = datetime.strptime(str(out["posttime_end"]), "%Y-%m-%d")
                out["posttime_end"] = (end_dt + timedelta(days=1)).strftime("%Y-%m-%d")
            except Exception:
                pass

        return out


def _load_params(params_str: Optional[str]) -> Dict[str, Any]:
    if not params_str:
        return {}
    params_str = (
        params_str.replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
    )
    try:
        payload = json.loads(params_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON for --params: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("--params must be a JSON object")
    return payload


def _load_params_file(path_str: Optional[str]) -> Dict[str, Any]:
    if not path_str:
        return {}
    path = Path(path_str).expanduser()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("--params-file must contain a JSON object")
    return payload


def _load_kv_params(kv_items: Optional[List[str]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if not kv_items:
        return out
    for raw in kv_items:
        if "=" not in raw:
            raise ValueError(f"Invalid --param '{raw}', expected key=value")
        key, value = raw.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Invalid --param '{raw}', empty key")
        out[key] = value
    return out


def _merge_params(
    params_json: Optional[str],
    params_file: Optional[str],
    params_kv: Optional[List[str]],
) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    merged.update(_load_params_file(params_file))
    merged.update(_load_params(params_json))
    merged.update(_load_kv_params(params_kv))
    return merged


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GSData high-level adapter skeleton")
    parser.add_argument(
        "--mapping",
        default=str(DEFAULT_MAPPING_PATH),
        help=f"Mapping JSON path (default: {DEFAULT_MAPPING_PATH})",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("GSDATA_BASE_URL", DEFAULT_BASE_URL),
        help="GSData gateway base URL",
    )
    parser.add_argument("--app-key", default=None)
    parser.add_argument("--app-secret", default=None)
    parser.add_argument(
        "--creds-file",
        default=str(DEFAULT_CREDS_PATH),
        help=f"Credentials file path (default: {DEFAULT_CREDS_PATH})",
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-tools", help="List high-level tools")

    p_ls = sub.add_parser("list-endpoints", help="List endpoints")
    p_ls.add_argument("--tool", help="Filter by tool")

    p_invoke = sub.add_parser("invoke", help="Invoke a high-level tool")
    p_invoke.add_argument("--tool", required=True)
    p_invoke.add_argument("--action", required=True)
    p_invoke.add_argument("--platform")
    p_invoke.add_argument("--sort")
    p_invoke.add_argument("--params", help='JSON object, e.g. \'{"keyword":"AI"}\'')
    p_invoke.add_argument("--params-file", help="Path to JSON object file")
    p_invoke.add_argument(
        "--param",
        action="append",
        default=[],
        help="Repeatable key=value param. Example: --param keywords_include=AI",
    )
    p_invoke.add_argument("--dry-run", action="store_true")
    p_invoke.add_argument("--allow-write", action="store_true")

    p_raw = sub.add_parser("raw", help="Invoke arbitrary route via gsdata_raw")
    p_raw.add_argument("--path", required=True)
    p_raw.add_argument("--method", default="GET")
    p_raw.add_argument("--params", help='JSON object, e.g. \'{"id":"123"}\'')
    p_raw.add_argument("--params-file", help="Path to JSON object file")
    p_raw.add_argument(
        "--param",
        action="append",
        default=[],
        help="Repeatable key=value param. Example: --param id=123",
    )
    p_raw.add_argument("--dry-run", action="store_true")
    p_raw.add_argument("--allow-write", action="store_true")

    return parser


def _require_creds(args: argparse.Namespace) -> None:
    if not args.app_key or not args.app_secret:
        raise SystemExit(
            "Missing credentials. Pass --app-key/--app-secret, "
            "or set GSDATA_APP_KEY/GSDATA_APP_SECRET, "
            "or provide credentials file (~/.config/gsdata/credentials.json)."
        )


def _load_creds_file(path_str: str) -> Dict[str, str]:
    path = Path(path_str).expanduser()
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}
    app_key = payload.get("app_key") or payload.get("GSDATA_APP_KEY") or ""
    app_secret = payload.get("app_secret") or payload.get("GSDATA_APP_SECRET") or ""
    return {
        "app_key": str(app_key).strip(),
        "app_secret": str(app_secret).strip(),
    }


def _resolve_creds(args: argparse.Namespace) -> Tuple[str, str]:
    # priority: CLI > ENV > creds file
    cli_key = (args.app_key or "").strip()
    cli_secret = (args.app_secret or "").strip()
    if cli_key and cli_secret:
        return cli_key, cli_secret

    env_key = (os.getenv("GSDATA_APP_KEY") or "").strip()
    env_secret = (os.getenv("GSDATA_APP_SECRET") or "").strip()
    if env_key and env_secret:
        return env_key, env_secret

    file_creds = _load_creds_file(args.creds_file)
    file_key = file_creds.get("app_key", "")
    file_secret = file_creds.get("app_secret", "")
    if file_key and file_secret:
        return file_key, file_secret
    return "", ""


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    resolved_key, resolved_secret = _resolve_creds(args)
    args.app_key = resolved_key
    args.app_secret = resolved_secret

    if args.cmd in {"invoke", "raw"} and not args.dry_run:
        _require_creds(args)

    # For dry-run and listing, allow empty creds.
    adapter = GsDataAdapter(
        app_key=args.app_key or "DUMMY_APP_KEY",
        app_secret=args.app_secret or "DUMMY_APP_SECRET",
        base_url=args.base_url,
        mapping_path=Path(args.mapping),
    )

    if args.cmd == "list-tools":
        print(json.dumps(adapter.list_tools(), ensure_ascii=False, indent=2))
        return

    if args.cmd == "list-endpoints":
        items = adapter.list_endpoints(tool=args.tool)
        out = [
            {
                "tool": i.tool,
                "cateId": i.cate_id,
                "cateName": i.cate_name,
                "method": i.method,
                "path": i.path,
                "desc": i.desc,
            }
            for i in items
        ]
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if args.cmd == "invoke":
        result = adapter.invoke(
            tool=args.tool,
            action=args.action,
            params=_merge_params(args.params, args.params_file, args.param),
            platform=args.platform,
            sort=args.sort,
            dry_run=args.dry_run,
            allow_write=args.allow_write,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.cmd == "raw":
        result = adapter.invoke(
            tool="gsdata_raw",
            action="call_any_endpoint",
            params=_merge_params(args.params, args.params_file, args.param),
            dry_run=args.dry_run,
            allow_write=args.allow_write,
            explicit_path=args.path,
            explicit_method=args.method,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    raise SystemExit(f"Unknown cmd: {args.cmd}")


if __name__ == "__main__":
    main()
