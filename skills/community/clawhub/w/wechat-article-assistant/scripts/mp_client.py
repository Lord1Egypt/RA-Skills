#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTTP client for WeChat MP requests with retry, rate-limit and proxy support."""

from __future__ import annotations

import warnings
warnings.filterwarnings("ignore", message="urllib3 .* doesn't match a supported version!")
warnings.filterwarnings("ignore", message=".*doesn't match a supported version!.*")

import json
import random
import re
import time
from typing import Any
from urllib.parse import parse_qsl, quote, urlencode, urlparse, urlunparse

import requests
from requests import Session
from requests.exceptions import ProxyError, RequestException

from config import DEFAULT_USER_AGENT
from database import Database
from log_utils import get_logger
from session_store import get_login_session
from utils import cookiejar_to_entities, normalize_mp_article_short_url

try:  # pragma: no cover - environment-specific
    from requests.exceptions import RequestsDependencyWarning

    warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
except Exception:  # pragma: no cover - optional
    pass


class WechatRequestError(RuntimeError):
    pass


class WechatLoginExpiredError(WechatRequestError):
    pass


class WechatArticleAccessError(WechatRequestError):
    pass


LOGGER = get_logger(__name__)


class ProxyPool:
    def __init__(self, proxies: list[str], cooldown_seconds: float = 60.0, max_failures: int = 2):
        self.proxies = [item.strip() for item in proxies if item and item.strip()]
        self.cooldown_seconds = max(1.0, float(cooldown_seconds))
        self.max_failures = max(1, int(max_failures))
        self.status: dict[str, dict[str, Any]] = {
            proxy: {
                "failures": 0,
                "last_used": 0.0,
                "cooldown": False,
                "total_failures": 0,
                "total_success": 0,
                "total_use": 0,
            }
            for proxy in self.proxies
        }

    def get_best_proxy(self) -> str:
        if not self.proxies:
            raise WechatRequestError("鏈厤缃彲鐢ㄤ唬鐞嗗湴鍧€")

        now = time.time()
        available = [
            proxy
            for proxy in self.proxies
            if not self.status[proxy]["cooldown"] or now - float(self.status[proxy]["last_used"]) >= self.cooldown_seconds
        ]
        if not available:
            return self._reset_and_get_oldest()

        available.sort(key=lambda proxy: (int(self.status[proxy]["failures"]), float(self.status[proxy]["last_used"])))
        selected = available[0]
        self.status[selected]["last_used"] = now
        self.status[selected]["total_use"] += 1
        return selected

    def record_success(self, proxy: str) -> None:
        if proxy not in self.status:
            return
        self.status[proxy]["failures"] = 0
        self.status[proxy]["cooldown"] = False
        self.status[proxy]["total_success"] += 1

    def record_failure(self, proxy: str) -> None:
        if proxy not in self.status:
            return
        self.status[proxy]["failures"] += 1
        self.status[proxy]["total_failures"] += 1
        self.status[proxy]["cooldown"] = int(self.status[proxy]["failures"]) >= self.max_failures

    def snapshot(self) -> list[dict[str, Any]]:
        return [
            {
                "proxy_url": proxy,
                **self.status[proxy],
            }
            for proxy in self.proxies
        ]

    def _reset_and_get_oldest(self) -> str:
        oldest = sorted(self.proxies, key=lambda proxy: float(self.status[proxy]["last_used"]))[0]
        self.status[oldest]["failures"] = 0
        self.status[oldest]["cooldown"] = False
        self.status[oldest]["last_used"] = time.time()
        self.status[oldest]["total_use"] += 1
        return oldest


class WechatMPClient:
    def __init__(self, db: Database):
        self.db = db
        self._last_request_at = 0.0
        self.rate_limit_seconds = 1.0
        self._proxy_pool: ProxyPool | None = None
        self._last_request_debug: dict[str, Any] = {}

    def new_session(self, cookies: list[dict[str, Any]] | None = None) -> Session:
        session = requests.Session()
        session.headers.update(
            {
                "Referer": "https://mp.weixin.qq.com/",
                "Origin": "https://mp.weixin.qq.com",
                "User-Agent": DEFAULT_USER_AGENT,
                "Accept-Encoding": "identity",
            }
        )
        for item in cookies or []:
            name = item.get("name")
            value = item.get("value")
            if not name or not value or value == "EXPIRED":
                continue
            session.cookies.set(
                name,
                value,
                domain=item.get("domain") or ".mp.weixin.qq.com",
                path=item.get("path") or "/",
            )
        return session

    def authenticated_session(self) -> tuple[Session, dict[str, Any]]:
        session_record = get_login_session(self.db)
        if not session_record or not session_record.get("token"):
            raise WechatLoginExpiredError("未找到有效登录态，请先扫码登录或导入登录信息")
        return self.new_session(session_record.get("cookies") or []), session_record

    def request(
        self,
        session: Session,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        operation: str = "api",
        timeout: int = 30,
        allow_redirects: bool = True,
        retries: int = 3,
    ) -> requests.Response:
        proxies = self._resolve_proxies(operation)
        selected_proxy = str((proxies or {}).get("https") or (proxies or {}).get("http") or "")
        last_error: Exception | None = None
        parsed_url = urlparse(url)
        safe_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        for attempt in range(1, retries + 1):
            self._respect_rate_limit()
            try:
                if operation == "sync":
                    prepared = session.prepare_request(
                        requests.Request(method=method, url=url, params=params, data=data)
                    )
                    self._set_last_request_debug(
                        mode="direct",
                        endpoint=safe_url,
                        request_url=prepared.url or safe_url,
                        headers=self._session_forward_headers(session),
                        proxy_url=selected_proxy,
                        note="requests direct transport",
                    )
                LOGGER.debug(
                    "request start method=%s url=%s operation=%s attempt=%s proxies=%s",
                    method,
                    safe_url,
                    operation,
                    attempt,
                    bool(proxies),
                )
                response = session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    timeout=timeout,
                    allow_redirects=allow_redirects,
                    proxies=proxies,
                )
                if response.status_code >= 500:
                    raise WechatRequestError(f"微信接口返回 HTTP {response.status_code}")
                LOGGER.debug(
                    "request ok method=%s url=%s operation=%s status=%s",
                    method,
                    safe_url,
                    operation,
                    response.status_code,
                )
                if selected_proxy and self._proxy_pool is not None:
                    self._proxy_pool.record_success(selected_proxy)
                return response
            except ProxyError as exc:
                last_error = WechatRequestError(
                    f"代理连接失败，请检查 proxy-set 配置或先禁用代理后重试。原始错误: {exc}"
                )
                if selected_proxy and self._proxy_pool is not None:
                    self._proxy_pool.record_failure(selected_proxy)
                LOGGER.warning("request proxy error method=%s url=%s attempt=%s error=%s", method, safe_url, attempt, exc)
                if attempt == retries:
                    break
                time.sleep(1.2 * attempt + random.random())
            except (RequestException, WechatRequestError) as exc:
                last_error = exc
                if selected_proxy and self._proxy_pool is not None:
                    self._proxy_pool.record_failure(selected_proxy)
                LOGGER.warning("request failed method=%s url=%s attempt=%s error=%s", method, safe_url, attempt, exc)
                if attempt == retries:
                    break
                time.sleep(1.2 * attempt + random.random())
        raise WechatRequestError(str(last_error or "微信请求失败"))

    def request_json(
        self,
        session: Session,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        operation: str = "api",
        timeout: int = 30,
        allow_redirects: bool = True,
        retries: int = 3,
    ) -> dict[str, Any]:
        response = self.request(
            session,
            method,
            url,
            params=params,
            data=data,
            operation=operation,
            timeout=timeout,
            allow_redirects=allow_redirects,
            retries=retries,
        )
        try:
            payload = response.json()
        except json.JSONDecodeError as exc:
            raise WechatRequestError(f"微信接口返回非 JSON 数据: {exc}") from exc

        base_resp = payload.get("base_resp")
        if isinstance(base_resp, dict) and base_resp.get("ret") not in (None, 0):
            message = str(base_resp.get("err_msg") or "微信接口返回错误")
            if "登录" in message or "过期" in message or "未登录" in message:
                raise WechatLoginExpiredError(message)
            raise WechatRequestError(message)
        return payload

    def validate_login(self) -> dict[str, Any]:
        LOGGER.debug("validate_login start")
        session, login = self.authenticated_session()
        response = self.request(
            session,
            "GET",
            "https://mp.weixin.qq.com/cgi-bin/home",
            params={"t": "home/index", "token": login["token"], "lang": "zh_CN"},
            operation="api",
        )
        final_url = str(getattr(response, "url", "") or "")
        html = response.text
        login_error_markers = (
            "请重新登录",
            ">请重新登录<",
            "登录微信公众平台",
            "扫描二维码登录",
            "请使用微信扫描二维码登录",
            "weui-desktop-login",
            "bizlogin",
            "layout/error",
            "error.218",
            "icon_msg icon_wrp",
            "frm_msg fail",
        )
        if "/cgi-bin/login" in final_url or "login.weixin.qq.com" in final_url:
            raise WechatLoginExpiredError("登录状态已过期，请重新扫码登录")
        if any(marker in html for marker in login_error_markers):
            raise WechatLoginExpiredError("登录状态已过期，请重新扫码登录")
        if "/cgi-bin/home" not in final_url and "token=" not in final_url:
            if any(marker in html for marker in login_error_markers):
                raise WechatLoginExpiredError("登录状态已过期，请重新扫码登录")

        nickname_match = re.search(r'wx\.cgiData\.nick_name\s*=\s*"(?P<value>[^"]+)"', html)
        head_img_match = re.search(r'wx\.cgiData\.head_img\s*=\s*"(?P<value>[^"]+)"', html)
        if not nickname_match and not head_img_match:
            if (
                "weui-desktop-account" not in html
                and "wx.cgiData" not in html
                and "masssendpage" not in html
                and "home/index" not in html
            ):
                raise WechatLoginExpiredError("未能确认微信后台登录状态，请重新登录")
        nickname = nickname_match.group("value") if nickname_match else login.get("nickname") or ""
        head_img = head_img_match.group("value") if head_img_match else login.get("head_img") or ""
        return {
            "logged_in": True,
            "nickname": nickname,
            "head_img": head_img,
            "token": login["token"],
            "cookies": cookiejar_to_entities(session.cookies),
            "final_url": final_url,
        }

    def check_proxy_health(self, operation: str = "sync", timeout: int = 5) -> dict[str, Any]:
        LOGGER.debug("check_proxy_health operation=%s timeout=%s", operation, timeout)
        row = self.db.row("SELECT * FROM proxy_config WHERE name = 'default'") or {}
        result: dict[str, Any] = {
            "operation": operation,
            "enabled": bool(row.get("enabled")),
            "proxy_url": str(row.get("proxy_url") or ""),
            "proxy_urls": self._proxy_urls(),
            "apply_article_fetch": bool(row.get("apply_article_fetch")),
            "apply_sync": bool(row.get("apply_sync")),
            "applied": False,
            "healthy": None,
            "message": "",
        }
        if not result["enabled"]:
            result["message"] = "代理未启用"
            return result
        if not result["proxy_url"]:
            result["healthy"] = False
            result["message"] = "代理已启用但未配置 URL"
            return result

        proxies = self._resolve_proxies(operation)
        result["applied"] = proxies is not None
        if not proxies:
            result["message"] = "当前操作未启用代理"
            return result

        try:
            if operation == "article":
                health_url = self._build_article_gateway_url("https://mp.weixin.qq.com/")
                response = requests.get(health_url, timeout=timeout, allow_redirects=True)
            else:
                response = self._check_sync_transport_health(timeout=timeout, proxies=proxies)
            result["healthy"] = True
            result["status_code"] = response.status_code
            result["message"] = f"代理连通性正常，HTTP {response.status_code}"
            return result
        except RequestException as exc:
            result["healthy"] = False
            result["message"] = f"代理连通性检查失败: {exc}"
            return result

    def search_accounts(self, keyword: str, count: int = 10) -> list[dict[str, Any]]:
        LOGGER.debug("search_accounts keyword=%s count=%s", keyword, count)
        session, login = self.authenticated_session()
        payload = self.request_json(
            session,
            "GET",
            "https://mp.weixin.qq.com/cgi-bin/searchbiz",
            params={
                "action": "search_biz",
                "begin": 0,
                "count": count,
                "query": keyword,
                "token": login["token"],
                "lang": "zh_CN",
                "f": "json",
                "ajax": 1,
            },
            operation="api",
        )
        return payload.get("list") or []

    def fetch_article_page(
        self,
        fakeid: str,
        begin: int = 0,
        count: int = 5,
        keyword: str = "",
    ) -> dict[str, Any]:
        LOGGER.debug(
            "fetch_article_page fakeid=%s begin=%s count=%s keyword=%s",
            fakeid,
            begin,
            count,
            keyword,
        )
        session, login = self.authenticated_session()
        is_searching = bool(keyword)
        payload = self._request_sync_article_page(
            session,
            {
                "sub": "search" if is_searching else "list",
                "search_field": "7" if is_searching else "null",
                "begin": begin,
                "count": count,
                "query": keyword,
                "fakeid": fakeid,
                "type": "101_1",
                "free_publish_type": 1,
                "sub_action": "list_ex",
                "token": login["token"],
                "lang": "zh_CN",
                "f": "json",
                "ajax": 1,
            },
        )
        publish_page = payload.get("publish_page")
        if not publish_page:
            return {"total_count": 0, "articles": []}
        page = json.loads(publish_page)
        articles: list[dict[str, Any]] = []
        for item in page.get("publish_list") or []:
            publish_info_raw = item.get("publish_info")
            if not publish_info_raw:
                continue
            publish_info = json.loads(publish_info_raw)
            for article in publish_info.get("appmsgex") or []:
                articles.append(article)
        LOGGER.debug(
            "fetch_article_page result fakeid=%s begin=%s total_count=%s articles=%s",
            fakeid,
            begin,
            int(page.get("total_count") or 0),
            len(articles),
        )
        return {
            "total_count": int(page.get("total_count") or 0),
            "articles": articles,
        }

    def fetch_public_article(self, link: str) -> str:
        LOGGER.debug("fetch_public_article link=%s", link)
        candidates: list[Session] = [self.new_session()]
        login_record = get_login_session(self.db)
        if login_record and login_record.get("cookies"):
            candidates.append(self.new_session(login_record["cookies"]))

        last_html = ""
        for session in candidates:
            headers = {
                "User-Agent": session.headers.get("User-Agent", DEFAULT_USER_AGENT),
                "Referer": session.headers.get("Referer", "https://mp.weixin.qq.com/"),
                "Origin": session.headers.get("Origin", "https://mp.weixin.qq.com"),
            }
            cookie_header = requests.utils.dict_from_cookiejar(session.cookies)
            if cookie_header:
                headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookie_header.items())

            if self._is_article_gateway_enabled():
                html = self._fetch_via_article_gateway(link, headers)
            else:
                response = self.request(
                    session,
                    "GET",
                    link,
                    operation="article",
                    allow_redirects=True,
                )
                html = response.text
            if "id=\"js_content\"" in html or "id='js_content'" in html:
                LOGGER.debug("fetch_public_article success link=%s", link)
                return html
            last_html = html

        if "环境异常" in last_html or "verify" in last_html:
            LOGGER.warning("fetch_public_article blocked link=%s", link)
            raise WechatArticleAccessError("微信返回环境异常校验页，请配置代理后重试文章详情抓取")
        raise WechatArticleAccessError("未能抓取到有效文章正文")

    def download_binary(self, url: str, referer: str | None = None, operation: str = "article") -> bytes:
        session = self.new_session()
        if referer:
            session.headers["Referer"] = referer
        if url.startswith("//"):
            url = f"https:{url}"

        if operation == "article" and self._is_article_gateway_enabled():
            headers = {
                "User-Agent": session.headers.get("User-Agent", DEFAULT_USER_AGENT),
                "Referer": session.headers.get("Referer", referer or "https://mp.weixin.qq.com/"),
            }
            return self._download_via_article_gateway(url, headers)

        response = self.request(session, "GET", url, operation=operation, allow_redirects=True)
        return response.content

    def _respect_rate_limit(self) -> None:
        elapsed = time.time() - self._last_request_at
        if elapsed < self.rate_limit_seconds:
            time.sleep(self.rate_limit_seconds - elapsed)
        self._last_request_at = time.time()

    def _proxy_row(self) -> dict[str, Any]:
        return self.db.row("SELECT * FROM proxy_config WHERE name = 'default'") or {}

    def _proxy_urls(self) -> list[str]:
        row = self._proxy_row()
        raw = str(row.get("proxy_url") or "").strip()
        if not raw:
            return []
        if raw.startswith("["):
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed if str(item).strip()]
            except Exception:
                pass
        normalized = raw.replace("\r", "\n").replace(",", "\n").replace(";", "\n")
        return [item.strip() for item in normalized.split("\n") if item.strip()]

    def _proxy_pool_instance(self) -> ProxyPool:
        urls = self._proxy_urls()
        if not urls:
            raise WechatRequestError("鏈厤缃彲鐢ㄤ唬鐞嗗湴鍧€")
        if self._proxy_pool is None or self._proxy_pool.proxies != urls:
            self._proxy_pool = ProxyPool(urls)
        return self._proxy_pool

    def get_last_request_debug(self) -> dict[str, Any]:
        return dict(self._last_request_debug)

    def _is_article_gateway_enabled(self) -> bool:
        row = self._proxy_row()
        return bool(row.get("enabled") and row.get("proxy_url") and row.get("apply_article_fetch"))

    def _is_sync_gateway_enabled(self) -> bool:
        row = self._proxy_row()
        return bool(row.get("enabled") and row.get("proxy_url") and row.get("apply_sync"))

    def _gateway_base_url(self) -> str:
        proxy_url = self._proxy_pool_instance().get_best_proxy()
        if not urlparse(proxy_url).scheme:
            proxy_url = f"https://{proxy_url}"
        return proxy_url

    def _session_forward_headers(self, session: Session, referer: str = "https://mp.weixin.qq.com/") -> dict[str, str]:
        headers = {
            "User-Agent": session.headers.get("User-Agent", DEFAULT_USER_AGENT),
            "Referer": session.headers.get("Referer", referer),
            "Origin": session.headers.get("Origin", "https://mp.weixin.qq.com"),
            "Accept-Encoding": session.headers.get("Accept-Encoding", "identity"),
        }
        cookie_header = requests.utils.dict_from_cookiejar(session.cookies)
        if cookie_header:
            headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookie_header.items())
        return headers

    def _build_gateway_url(
        self,
        target_url: str,
        *,
        proxy_base: str | None = None,
        headers: dict[str, str] | None = None,
        include_headers: bool = False,
        normalize_article: bool = False,
        preset: str = "",
    ) -> str:
        gateway_base = proxy_base or self._gateway_base_url()
        normalized_target = normalize_mp_article_short_url(target_url) if normalize_article else target_url
        separator = '&' if '?' in gateway_base else '?'
        gateway_url = f"{gateway_base}{separator}url={quote(normalized_target, safe=':/')}"
        if preset:
            gateway_url += f"&preset={quote(preset, safe='')}"
        if include_headers and headers:
            header_json = json.dumps(headers or {}, ensure_ascii=False)
            gateway_url += f"&headers={quote(header_json, safe='')}"
        return gateway_url

    def _build_gateway_request(
        self,
        target_url: str,
        *,
        headers: dict[str, str] | None = None,
        include_headers: bool = False,
        normalize_article: bool = False,
        preset: str = "",
    ) -> tuple[str, str]:
        proxy_base = self._gateway_base_url()
        gateway_url = self._build_gateway_url(
            target_url,
            proxy_base=proxy_base,
            headers=headers,
            include_headers=include_headers,
            normalize_article=normalize_article,
            preset=preset,
        )
        return proxy_base, gateway_url

    def _fetch_via_article_gateway(self, url: str, headers: dict[str, str] | None = None) -> str:
        last_error: Exception | None = None
        for include_headers in (False, True):
            proxy_base, gateway_url = self._build_gateway_request(
                url,
                headers=headers,
                include_headers=include_headers,
                normalize_article=True,
                preset="mp",
            )
            try:
                response = requests.get(gateway_url, timeout=30, allow_redirects=True)
                response.raise_for_status()
                self._proxy_pool_instance().record_success(proxy_base)
                return response.text
            except RequestException as exc:
                last_error = exc
                self._proxy_pool_instance().record_failure(proxy_base)
                LOGGER.warning("article gateway fetch failed include_headers=%s url=%s error=%s", include_headers, url, exc)
        raise WechatArticleAccessError(f"文章代理抓取失败: {last_error}")

    def _download_via_article_gateway(self, url: str, headers: dict[str, str] | None = None) -> bytes:
        last_error: Exception | None = None
        for include_headers in (False, True):
            proxy_base, gateway_url = self._build_gateway_request(
                url,
                headers=headers,
                include_headers=include_headers,
                normalize_article=True,
                preset="mp",
            )
            try:
                response = requests.get(gateway_url, timeout=30, allow_redirects=True)
                response.raise_for_status()
                self._proxy_pool_instance().record_success(proxy_base)
                return response.content
            except RequestException as exc:
                last_error = exc
                self._proxy_pool_instance().record_failure(proxy_base)
                LOGGER.warning("article gateway download failed include_headers=%s url=%s error=%s", include_headers, url, exc)
        raise WechatArticleAccessError(f"文章资源代理下载失败: {last_error}")

    def _build_article_gateway_url(self, url: str, headers: dict[str, str] | None = None, include_headers: bool = False) -> str:
        return self._build_gateway_url(
            url,
            headers=headers,
            include_headers=include_headers,
            normalize_article=True,
            preset="mp",
        )

    def _redact_sensitive_value(self, value: Any) -> str:
        text = str(value or "")
        if not text:
            return ""
        if len(text) <= 8:
            return "***"
        return f"{text[:4]}...{text[-4:]}"

    def _redact_cookie_header(self, cookie_header: str) -> str:
        parts: list[str] = []
        for item in str(cookie_header or "").split(";"):
            chunk = item.strip()
            if not chunk:
                continue
            if "=" not in chunk:
                parts.append(chunk)
                continue
            name, value = chunk.split("=", 1)
            parts.append(f"{name.strip()}={self._redact_sensitive_value(value.strip())}")
        return "; ".join(parts)

    def _redact_headers_for_debug(self, headers: dict[str, str] | None) -> dict[str, str]:
        redacted: dict[str, str] = {}
        for key, value in (headers or {}).items():
            lowered = key.lower()
            if lowered == "cookie":
                redacted[key] = self._redact_cookie_header(str(value))
            elif "token" in lowered or lowered in {"authorization", "proxy-authorization"}:
                redacted[key] = self._redact_sensitive_value(value)
            else:
                redacted[key] = str(value)
        return redacted

    def _redact_url_for_debug(self, url: str) -> str:
        parsed = urlparse(url)
        query_items: list[tuple[str, str]] = []
        for key, value in parse_qsl(parsed.query, keep_blank_values=True):
            lowered = key.lower()
            if lowered == "headers":
                try:
                    header_map = json.loads(value)
                    value = json.dumps(self._redact_headers_for_debug(header_map), ensure_ascii=False)
                except Exception:
                    value = "***"
            elif "token" in lowered or lowered in {"cookie", "authorization"}:
                value = self._redact_sensitive_value(value)
            query_items.append((key, value))
        return urlunparse(parsed._replace(query=urlencode(query_items, doseq=True)))

    def _quote_shell_arg(self, value: str) -> str:
        return "'" + str(value).replace("'", "'\"'\"'") + "'"

    def _build_curl_preview(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        proxy_url: str = "",
    ) -> str:
        parts = ["curl", self._quote_shell_arg(self._redact_url_for_debug(url))]
        for key, value in self._redact_headers_for_debug(headers).items():
            parts.extend(["-H", self._quote_shell_arg(f"{key}: {value}")])
        if proxy_url:
            parts.extend(["--proxy", self._quote_shell_arg(proxy_url)])
        return " ".join(parts)

    def _set_last_request_debug(
        self,
        *,
        mode: str,
        endpoint: str,
        request_url: str,
        headers: dict[str, str] | None = None,
        proxy_url: str = "",
        include_headers: bool | None = None,
        note: str = "",
    ) -> None:
        payload: dict[str, Any] = {
            "operation": "sync",
            "mode": mode,
            "endpoint": self._redact_url_for_debug(endpoint),
            "request_url": self._redact_url_for_debug(request_url),
            "headers": self._redact_headers_for_debug(headers),
            "curl": self._build_curl_preview(request_url, headers=headers, proxy_url=proxy_url),
        }
        if proxy_url:
            payload["proxy_url"] = proxy_url
        if include_headers is not None:
            payload["include_headers"] = include_headers
        if note:
            payload["note"] = note
        self._last_request_debug = payload

    def _request_sync_article_page(self, session: Session, params: dict[str, Any]) -> dict[str, Any]:
        endpoint = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish"
        query = urlencode({key: value for key, value in params.items() if value is not None})
        target_url = f"{endpoint}?{query}" if query else endpoint
        if not self._is_sync_gateway_enabled():
            self._set_last_request_debug(
                mode="direct",
                endpoint=endpoint,
                request_url=target_url,
                headers=self._session_forward_headers(session),
                note="sync direct mode without gateway",
            )
            return self.request_json(
                session,
                "GET",
                endpoint,
                params=params,
                operation="sync",
            )

        return self._request_json_via_gateway(
            target_url,
            session=session,
            preset="mp",
        )

    def _request_json_via_gateway(
        self,
        target_url: str,
        *,
        session: Session,
        timeout: int = 30,
        preset: str = "",
    ) -> dict[str, Any]:
        headers = self._session_forward_headers(session)
        last_error: Exception | None = None
        for include_headers in (False, True):
            proxy_base, gateway_url = self._build_gateway_request(
                target_url,
                headers=headers,
                include_headers=include_headers,
                normalize_article=False,
                preset=preset,
            )
            self._set_last_request_debug(
                mode="gateway",
                endpoint=target_url,
                request_url=gateway_url,
                proxy_url=proxy_base,
                include_headers=include_headers,
                note="article_proxy_gateway style GET relay",
            )
            try:
                response = requests.get(gateway_url, timeout=timeout, allow_redirects=True)
                response.raise_for_status()
                payload = response.json()
                base_resp = payload.get("base_resp")
                if isinstance(base_resp, dict) and base_resp.get("ret") not in (None, 0):
                    message = str(base_resp.get("err_msg") or "寰俊鎺ュ彛杩斿洖閿欒")
                    if "鐧诲綍" in message or "杩囨湡" in message or "鏈櫥褰?" in message or "invalid session" in message:
                        raise WechatLoginExpiredError(message)
                    raise WechatRequestError(message)
                self._proxy_pool_instance().record_success(proxy_base)
                return payload
            except json.JSONDecodeError as exc:
                last_error = WechatRequestError(f"缃戝叧杩斿洖闈?JSON 鏁版嵁: {exc}")
                self._proxy_pool_instance().record_failure(proxy_base)
                LOGGER.warning("gateway json decode failed include_headers=%s url=%s error=%s", include_headers, target_url, exc)
            except RequestException as exc:
                last_error = exc
                self._proxy_pool_instance().record_failure(proxy_base)
                LOGGER.warning("gateway request failed include_headers=%s url=%s error=%s", include_headers, target_url, exc)
            except WechatRequestError as exc:
                last_error = exc
                self._proxy_pool_instance().record_failure(proxy_base)
                LOGGER.warning("gateway response failed include_headers=%s url=%s error=%s", include_headers, target_url, exc)
        raise WechatRequestError(f"缃戝叧璇锋眰澶辫触: {last_error}")

    def _check_sync_transport_health(self, timeout: int, proxies: dict[str, str] | None) -> requests.Response:
        health_url = "https://mp.weixin.qq.com/"
        if self._is_sync_gateway_enabled():
            last_error: Exception | None = None
            for include_headers in (False, True):
                proxy_base, gateway_url = self._build_gateway_request(
                    health_url,
                    headers={"User-Agent": DEFAULT_USER_AGENT, "Referer": "https://mp.weixin.qq.com/"},
                    include_headers=include_headers,
                    preset="mp",
                )
                try:
                    response = requests.get(gateway_url, timeout=timeout, allow_redirects=True)
                    response.raise_for_status()
                    self._proxy_pool_instance().record_success(proxy_base)
                    return response
                except RequestException as exc:
                    last_error = exc
                    self._proxy_pool_instance().record_failure(proxy_base)
                    LOGGER.warning("sync gateway health failed include_headers=%s error=%s", include_headers, exc)
            raise last_error or WechatRequestError("sync gateway health check failed")

        session = self.new_session()
        return session.get(
            health_url,
            timeout=timeout,
            allow_redirects=True,
        )

    def _resolve_proxies(self, operation: str) -> dict[str, str] | None:
        return None
