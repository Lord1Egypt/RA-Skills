#!/usr/bin/env python3
"""微排版 API 源站校验。上传、取素材、发布三个脚本共用。

只允许 https://weipaiban.cn（含子域）以及本机
localhost / 127.0.0.1 / ::1 的 http 或 https。
不提供跳过证书校验的开关。
"""

from __future__ import annotations

import ssl
import urllib.parse

API_KEY_PAGE = "https://weipaiban.cn/settings/api-keys"


def missing_api_key_message() -> str:
    return (
        "错误：缺少环境变量 WEIPAIBAN_API_KEY。"
        f"请登录微排版，打开 {API_KEY_PAGE} 创建或复制以 sk- 开头的密钥，"
        "再设为该环境变量。不要把密钥贴进对话或写进任务文件。"
    )


def invalid_api_key_message() -> str:
    return (
        "提示：密钥缺失、无效或已过期。"
        f"请到 {API_KEY_PAGE} 创建或复制新的 sk- 密钥，并更新 WEIPAIBAN_API_KEY。"
    )


def validate_api_base(api_base: str) -> str:
    raw = api_base.strip().rstrip("/")
    parsed = urllib.parse.urlparse(raw)
    host = (parsed.hostname or "").lower().rstrip(".")
    if (
        parsed.username
        or parsed.password
        or parsed.params
        or parsed.query
        or parsed.fragment
        or parsed.path not in ("", "/")
        or not host
    ):
        raise ValueError("API 地址只能是源站，不能带路径、账号或查询")

    loopback = host in {"localhost", "127.0.0.1", "::1"}
    official = host == "weipaiban.cn" or host.endswith(".weipaiban.cn")
    if loopback and parsed.scheme in {"http", "https"}:
        return raw
    if official and parsed.scheme == "https":
        return raw
    raise ValueError(
        "API 地址只允许 https://weipaiban.cn（含子域）或本机 "
        "http(s)://localhost、127.0.0.1、::1"
    )


def build_ssl_context() -> ssl.SSLContext:
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def self_test() -> None:
    assert validate_api_base("https://weipaiban.cn") == "https://weipaiban.cn"
    assert validate_api_base("https://api.weipaiban.cn/") == "https://api.weipaiban.cn"
    assert validate_api_base("http://127.0.0.1:3000") == "http://127.0.0.1:3000"
    assert validate_api_base("http://localhost") == "http://localhost"
    assert validate_api_base("https://[::1]:8787") == "https://[::1]:8787"
    for bad in (
        "http://weipaiban.cn",
        "https://evil.com",
        "https://weipaiban.cn.evil.com",
        "https://weipaiban.cn/api",
        "https://user:pass@weipaiban.cn",
        "https://weipaiban.cn?x=1",
        "",
    ):
        try:
            validate_api_base(bad)
        except ValueError:
            continue
        raise AssertionError(bad)
    build_ssl_context()
    assert API_KEY_PAGE in missing_api_key_message()
    assert API_KEY_PAGE in invalid_api_key_message()
    print("ok")


if __name__ == "__main__":
    self_test()
