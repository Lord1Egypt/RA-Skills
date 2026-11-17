"""SDK configuration for Vmake AI."""

import os

# V2 config and consume requests use the same gateway.
WAPI_ENDPOINT = "wapi-skill.vmake.ai"

# GID cache (persistent on disk, no TTL in this skill)
GID_CACHE_FILE = "~/.cache/vmake/gid_cache.json"

VERSION = "v2.0.0"
# USER_AGENT_NAME identifies this branded Skill distribution in HTTP requests.
# Domestic distributions only need to replace this value.
USER_AGENT_NAME = "vmake-skill"
USER_AGENT = f"{USER_AGENT_NAME}-{VERSION}"

# Config schemas this Skill can parse, in preference order.
SUPPORTED_SCHEMAS = ("v2", "v1")

# HTTP(S) input download (run-task --input URL and resolve-input --url); overridable via env.
URL_DOWNLOAD_MAX_BYTES_DEFAULT = 100 * 1024 * 1024
URL_DOWNLOAD_CONNECT_TIMEOUT_DEFAULT = 15
URL_DOWNLOAD_READ_TIMEOUT_DEFAULT = 120


def url_download_max_bytes() -> int:
    raw = os.environ.get("MT_AI_URL_MAX_BYTES", "").strip()
    if raw:
        try:
            return max(1, int(raw))
        except ValueError:
            pass
    return URL_DOWNLOAD_MAX_BYTES_DEFAULT


def url_download_connect_timeout() -> int:
    raw = os.environ.get("MT_AI_URL_CONNECT_TIMEOUT", "").strip()
    if raw:
        try:
            return max(1, min(int(raw), 300))
        except ValueError:
            pass
    return URL_DOWNLOAD_CONNECT_TIMEOUT_DEFAULT


def url_download_read_timeout() -> int:
    raw = os.environ.get("MT_AI_URL_READ_TIMEOUT", "").strip()
    if raw:
        try:
            return max(1, min(int(raw), 3600))
        except ValueError:
            pass
    return URL_DOWNLOAD_READ_TIMEOUT_DEFAULT


def url_download_timeout_tuple() -> tuple[int, int]:
    return (url_download_connect_timeout(), url_download_read_timeout())


# Region map (overwritten by server config when fetched)
REGIONS = {}

# Invoke presets (overwritten by server config when fetched)
INVOKE = {}

# Default parameters for tasks
DEFAULT_PARAMS = {"parameter": {"rsp_media_type": "url"}}
