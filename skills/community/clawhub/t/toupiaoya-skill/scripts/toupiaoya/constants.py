from __future__ import annotations

import os
from pathlib import Path

# 全局凭证：交互式 login 写入，create 默认读取
CONFIG_DIR = Path.home() / ".toupiaoya"
CONFIG_PATH = CONFIG_DIR / "config.json"
CONFIG_TOKEN_KEY = "X-Openclaw-Token"

PASSPORT_PROFILE_URL = "https://passport.toupiaoya.com/user/profile"
TOUPIAOYA_STORE_SEARCH_URL = "https://msearch-api.toupiaoya.com/m/search/searchProducts"
BASE_PREVIEW_URL = "https://www.toupiaoya.com/mall/detail-h5e/"
BASE_IMAGE_URL = "https://asset.eqh5.com/"

_DEFAULT_BASE = (
    os.environ.get("TOUPIAOYA_API_BASE") or os.environ.get("EQXIU_AIGC_API_BASE") or "https://ai-api.toupiaoya.com"
)
DEFAULT_BASE_URL = str(_DEFAULT_BASE).rstrip("/")

DEFAULT_TIMEOUT = 30

# COS 临时凭证（投票鸭素材上传）
COS_TOKEN_API_BASE = str(
    os.environ.get("TOUPIAOYA_COS_TOKEN_API_BASE") or "https://emw-api.toupiaoya.com"
).rstrip("/")
DEFAULT_COS_BUCKET = "eqxiu"
DEFAULT_COS_PREFIX = "/material/"
# 与模板搜索封面域名一致，便于拼接访问地址（实际是否 CDN 命中以业务为准）
ASSET_PUBLIC_BASE = "https://asset.eqh5.com/"

# 素材库登记（COS 上传成功后写入业务素材）
MATERIAL_API_BASE = str(
    os.environ.get("TOUPIAOYA_MATERIAL_API_BASE") or "https://material-api.toupiaoya.com"
).rstrip("/")
DEFAULT_MATERIAL_SOURCE = "P010238"

# 工作台场景列表（作品列表 project list）
LWORK_API_BASE = str(
    os.environ.get("TOUPIAOYA_LWORK_API_BASE") or "https://lwork-api.toupiaoya.com"
).rstrip("/")

# 与 token / 素材接口一致的浏览器 UA（可按需统一）
BROWSER_CHROME_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
)

# 商城模板搜索（JSON POST）
STORE_SEARCH_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Referer": "https://www.toupiaoya.com/",
    "Accept-Encoding": "gzip, deflate",
}
