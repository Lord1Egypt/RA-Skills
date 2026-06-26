import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse, parse_qs
import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


APP_ID: Optional[str] = None
APP_SECRET: Optional[str] = None
BITABLE_URL: Optional[str] = None
BASE_URL: Optional[str] = None
PATH = "/api/mc/xiaoAiList"
TOKEN: Optional[str] = None
DEFAULT_FOLDER_ID: Optional[int] = None
DEFAULT_CUSTOMER_ID: Optional[str] = None

# ============ 性能优化配置 ============
# 增大批量大小，减少 API 调用次数
BATCH_SIZE = 500  # 飞书上限 500
# 分页大小优化
PAGE_SIZE = 500  # 增大分页大小，减少请求次数
# 缓存配置
CACHE_DIR = os.path.join(os.path.dirname(__file__), '.cache')
TOKEN_CACHE_FILE = os.path.join(CACHE_DIR, 'tenant_token.json')
KEYS_CACHE_FILE = os.path.join(CACHE_DIR, 'existing_keys.json')
CACHE_TTL = 300  # 缓存有效期 5 分钟
# 连接池配置
SESSION = None

FIELD_MAP: Dict[str, str] = {
    "section": "品牌",
    "pub_time": "发布时间",
    "headline": "标题",
    "content": "正文",
    "doc_url": "原文 URL",
    "author": "作者",
    "media_name": "来源渠道",
    "keywords_highlight": "命中关键词",
    "cluster_id": "内容聚合 ID",
    "ocr": "抽帧识别内容",
    "doc_label_name": "版面信息",
    "link_status_id": "链接状态",
    "media_type_name": "文章类型",
    "fans_cnt": "粉丝量",
    "like_cnt": "点赞量",
    "forward_cnt": "转发量",
    "view_cnt": "阅读量",
    "sentiment_type_id": "情感 (慧科)",
    "md5_doc_id": "md5_doc_id",
}

FIELD_TYPES: Dict[str, int] = {
    "case ID": 1,
    "品牌": 3,
    "发布时间": 5,
    "入库时间": 5,
    "标题": 1,
    "正文": 1,
    "抽帧识别内容": 1,
    "原文 URL": 1,
    "作者": 1,
    "来源渠道": 3,
    "命中关键词": 1,
    "标题提及": 1,
    "正文提及": 1,
    "ocr 提及": 1,
    "文章提及": 1,
    "内容聚合 ID": 1,
    "情感 (慧科)": 1,
    "版面信息": 1,
    "链接状态": 1,
    "文章类型": 1,
    "粉丝量": 1,
    "点赞量": 1,
    "转发量": 1,
    "阅读量": 1,
    "文章提及": 1,
    "md5_doc_id": 1,
    "类型（机器）": 1,
    "评价情感（机器）": 1,
    "是否提及竞品(机器)": 1,
    "端(机器)": 1,
    "品牌安全(AI)": 1,
    "内容安全(AI)": 1,
}

KEY_FIELD_NAME = "md5_doc_id"
# 单个 sheet（表）内允许的最大记录数，超过该值则在同一个多维表应用下新建一个表继续写入
PER_TABLE_LIMIT = 10000
# 兜底上限（极端情况下防止意外写爆），一般不会触达
MAX_RECORDS = 200000

SOURCE_CHANNEL_OPTIONS = [
    "小米社区", "小红书 APP", "新浪微博", "网易", "雪球", "今日头条",
    "178 游戏网", "快手 APP", "哔哩哔哩 APP", "微信", "UC 头条 APP", "网易新闻 APP",
]


def get_session() -> requests.Session:
    """获取带连接池的 session，复用 TCP 连接"""
    global SESSION
    if SESSION is None:
        SESSION = requests.Session()
        # 兼容新旧版本 urllib3：allowed_methods (新) vs method_whitelist (旧)
        try:
            retry = Retry(
                total=3,
                backoff_factor=0.3,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
            )
        except TypeError:
            retry = Retry(
                total=3,
                backoff_factor=0.3,
                status_forcelist=[429, 500, 502, 503, 504],
                method_whitelist=["HEAD", "GET", "OPTIONS", "POST"]
            )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=20)
        SESSION.mount("https://", adapter)
        SESSION.mount("http://", adapter)
    return SESSION


def _parse_bitable_url(url: str) -> Tuple[str, str]:
    parsed = urlparse(url)
    app_token = ""
    parts = [p for p in parsed.path.split("/") if p]
    for i, p in enumerate(parts):
        if p == "base" and i + 1 < len(parts):
            app_token = parts[i + 1]
            break
    qs = parse_qs(parsed.query)
    table_id = qs.get("table", [None])[0]
    return app_token, table_id


def _ensure_cache_dir():
    """确保缓存目录存在"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)


def _load_cached_keys() -> Optional[Dict]:
    """加载缓存的唯一键"""
    try:
        if os.path.exists(KEYS_CACHE_FILE):
            with open(KEYS_CACHE_FILE, 'r') as f:
                data = json.load(f)
                # 检查缓存是否过期
                if time.time() - data.get('timestamp', 0) < CACHE_TTL:
                    return data
    except Exception:
        pass
    return None


def _save_cached_keys(keys: set, total_records: int, max_case_id: int):
    """保存唯一键到缓存"""
    try:
        _ensure_cache_dir()
        with open(KEYS_CACHE_FILE, 'w') as f:
            json.dump({
                'timestamp': time.time(),
                'keys': list(keys),
                'total_records': total_records,
                'max_case_id': max_case_id
            }, f)
    except Exception:
        pass  # 缓存失败不影响主流程


def build_headers() -> Dict[str, str]:
    if not TOKEN:
        raise RuntimeError("TOKEN 未初始化")
    return {"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}


def build_body(
    offset: int, limit: int, folder_id: int,
    start_time: datetime, end_time: datetime,
    customer_id: Optional[str] = None,
    clustering: str = "no-clustering", sort: str = "date",
) -> Dict[str, Any]:
    def fmt(dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S.") + "000"
    
    body: Dict[str, Any] = {
        "offset": offset, "limit": limit,
        "date": [fmt(start_time), fmt(end_time)],
        "tracking_time": fmt(end_time),
        "clustering": clustering, "sort": sort,
        "folder_id": [folder_id],
    }
    if customer_id:
        body["customer_id"] = customer_id
    return body


def fetch_page(
    offset: int, limit: int, folder_id: int,
    start_time: datetime, end_time: datetime,
    customer_id: Optional[str] = None,
) -> Dict[str, Any]:
    url = BASE_URL + PATH
    headers = build_headers()
    body = build_body(offset, limit, folder_id, start_time, end_time, customer_id)
    session = get_session()
    resp = session.post(url, headers=headers, json=body, timeout=60)
    resp.raise_for_status()
    return resp.json()


def fetch_all_items(
    folder_id: int, start_time: datetime, end_time: datetime,
    customer_id: Optional[str] = None,
    page_size: int = PAGE_SIZE, max_pages: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """优化：增大批量大小，减少请求次数"""
    items: List[Dict[str, Any]] = []
    offset = 0
    page_count = 0

    while True:
        page_count += 1
        if max_pages is not None and page_count > max_pages:
            break

        data = fetch_page(offset, page_size, folder_id, start_time, end_time, customer_id)
        data_obj = data.get("data") or {}
        page_items = data_obj.get("items") or []
        total = data_obj.get("total")

        if not page_items:
            break

        items.extend(page_items)
        if total is not None and offset + page_size >= int(total):
            break
        offset += page_size

    return items


def get_tenant_access_token() -> str:
    """优化：缓存 token，避免重复请求"""
    _ensure_cache_dir()
    
    # 尝试从缓存加载
    try:
        if os.path.exists(TOKEN_CACHE_FILE):
            with open(TOKEN_CACHE_FILE, 'r') as f:
                data = json.load(f)
                # token 有效期通常 2 小时，提前 10 分钟刷新
                if time.time() - data.get('timestamp', 0) < 7200 - 600:
                    return data['token']
    except Exception:
        pass
    
    if not APP_ID or not APP_SECRET:
        raise RuntimeError("APP_ID / APP_SECRET 未初始化")
    
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    session = get_session()
    resp = session.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"获取 tenant_access_token 失败：{data}")
    
    # 缓存 token
    try:
        with open(TOKEN_CACHE_FILE, 'w') as f:
            json.dump({'token': data["tenant_access_token"], 'timestamp': time.time()}, f)
    except Exception:
        pass
    
    return data["tenant_access_token"]


def get_feishu_field_names(tenant_access_token: str) -> List[str]:
    """优化：只调用一次，结果复用"""
    if not BITABLE_URL:
        raise RuntimeError("BITABLE_URL 未初始化")
    app_token, table_id = _parse_bitable_url(BITABLE_URL)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    params: Dict[str, Any] = {}
    field_names: List[str] = []
    session = get_session()

    while True:
        resp = session.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"获取字段列表失败：{data}")

        items = (data.get("data") or {}).get("items") or []
        for item in items:
            name = item.get("field_name")
            if isinstance(name, str):
                field_names.append(name)

        page_token = (data.get("data") or {}).get("page_token")
        has_more = (data.get("data") or {}).get("has_more")
        if not has_more or not page_token:
            break
        params["page_token"] = page_token

    return field_names


def ensure_feishu_fields(tenant_access_token: str, existing_names: List[str]) -> None:
    """优化：批量检查，减少不必要的字段创建"""
    if not BITABLE_URL:
        raise RuntimeError("BITABLE_URL 未初始化")
    app_token, table_id = _parse_bitable_url(BITABLE_URL)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {"Authorization": f"Bearer {tenant_access_token}", "Content-Type": "application/json"}
    existing_set = set(existing_names)
    session = get_session()

    creation_order = ["case ID"] + [name for name in FIELD_TYPES.keys() if name != "case ID"]

    for name in creation_order:
        ftype = FIELD_TYPES[name]
        if name in existing_set:
            continue

        if name == "来源渠道" and ftype == 3:
            payload = {
                "field_name": name, "type": 3,
                "property": {"options": [{"name": opt} for opt in SOURCE_CHANNEL_OPTIONS]},
            }
        else:
            payload = {"field_name": name, "type": ftype}

        resp = session.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            print(f"创建字段失败：{name}, 响应：{data}")


def get_existing_keys(
    tenant_access_token: str, key_field_name: str, force_refresh: bool = False,
) -> Tuple[set, int, int]:
    """
    优化：
    1. 添加缓存机制，避免每次都读取全表
    2. 增大批量大小到 500
    3. 只在必要时强制刷新
    """
    # 尝试从缓存加载（除非强制刷新）
    if not force_refresh:
        cached = _load_cached_keys()
        if cached:
            print(f"[缓存命中] 从缓存加载 {len(cached['keys'])} 个唯一键")
            return set(cached['keys']), cached['total_records'], cached['max_case_id']
    
    if not BITABLE_URL:
        raise RuntimeError("BITABLE_URL 未初始化")
    
    app_token, table_id = _parse_bitable_url(BITABLE_URL)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    params: Dict[str, Any] = {"page_size": PAGE_SIZE}  # 增大批量
    keys: set = set()
    total_records = 0
    max_case_id = 0
    session = get_session()
    page_count = 0

    print("正在读取多维表已有记录...")
    while True:
        page_count += 1
        if page_count % 10 == 0:
            print(f"  已读取 {page_count} 页，{len(keys)} 个唯一键...")
        
        resp = session.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"获取记录列表失败：{data}")

        data_obj = data.get("data") or {}
        if not total_records:
            total_records = int(data_obj.get("total") or 0)
            print(f"  多维表总记录数：{total_records}")

        items = data_obj.get("items") or []
        for rec in items:
            fields = rec.get("fields") or {}
            v = fields.get(key_field_name)
            if v is not None:
                if isinstance(v, list):
                    v = v[0] if v else None
                if v is not None:
                    keys.add(str(v))
            cid = fields.get("case ID")
            if cid is not None:
                try:
                    max_case_id = max(max_case_id, int(cid))
                except (TypeError, ValueError):
                    pass

        page_token = (data.get("data") or {}).get("page_token")
        has_more = data_obj.get("has_more")
        if not has_more or not page_token:
            break
        params["page_token"] = page_token

    # 保存到缓存
    _save_cached_keys(keys, total_records, max_case_id)
    print(f"  读取完成，共 {len(keys)} 个唯一键")
    return keys, total_records, max_case_id


def _create_new_table_if_needed(tenant_access_token: str, total_records: int) -> Optional[str]:
    """
    当当前表内记录数达到单表上限（PER_TABLE_LIMIT）时，在同一个多维表应用下新建一个表，并返回新的 BITABLE_URL。
    若未达到上限，则返回 None。
    """
    if total_records < PER_TABLE_LIMIT:
        return None

    if not BITABLE_URL:
        raise RuntimeError("BITABLE_URL 未初始化")

    app_token, _ = _parse_bitable_url(BITABLE_URL)

    # 创建新表
    create_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
        "Content-Type": "application/json",
    }
    session = get_session()

    table_name = f"auto_sheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    payload = {"table": {"name": table_name}}

    print(f"当前表记录数 {total_records} 已达到单表上限 {PER_TABLE_LIMIT}，准备新建表：{table_name}")
    resp = session.post(create_url, headers=headers, json=payload, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"创建新表失败：{data}")

    data_obj = data.get("data") or {}
    table_obj = data_obj.get("table") or {}
    new_table_id = table_obj.get("table_id") or data_obj.get("table_id")
    if not new_table_id:
        raise RuntimeError(f"创建新表成功但未返回 table_id：{data}")

    # 复用原始链接中的域名，构造新的多维表链接（保持 ?table=tbl*** 结构）
    parsed = urlparse(BITABLE_URL)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    new_bitable_url = f"{base_url}/base/{app_token}?table={new_table_id}"

    print(f"已新建表 {table_name}，table_id={new_table_id}，后续写入将切换到该表。")
    return new_bitable_url


def build_records_from_items(
    items: List[Dict[str, Any]], feishu_field_names: List[str],
) -> List[Dict[str, Any]]:
    """优化：使用局部变量，减少重复查找"""
    records: List[Dict[str, Any]] = []
    feishu_field_set = set(feishu_field_names)
    field_types = FIELD_TYPES
    field_map = FIELD_MAP
    default_folder_id = DEFAULT_FOLDER_ID

    def to_timestamp_ms(value: Any) -> Any:
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, datetime):
            return int(value.timestamp() * 1000)
        if isinstance(value, str):
            txt = value.strip()
            for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
                try:
                    dt = datetime.strptime(txt, fmt)
                    return int(dt.timestamp() * 1000)
                except ValueError:
                    continue
        return value

    def bool_to_str(flag: bool) -> str:
        return "是" if flag else "否"

    sentiment_mapping = {1: "正面", 0: "中性", -1: "负面"}

    for item in items:
        fields: Dict[str, Any] = {}
        for col_name, value in item.items():
            if value is None:
                continue

            target_name: Optional[str] = field_map.get(col_name)
            if not target_name or target_name not in feishu_field_set:
                if col_name in feishu_field_set:
                    target_name = col_name
                else:
                    continue

            if target_name:
                if field_types.get(target_name) == 5:
                    fields[target_name] = to_timestamp_ms(value)
                elif target_name == "情感 (慧科)":
                    try:
                        fields[target_name] = sentiment_mapping.get(int(value), str(value))
                    except (TypeError, ValueError):
                        fields[target_name] = str(value)
                elif isinstance(value, (list, dict)):
                    fields[target_name] = json.dumps(value, ensure_ascii=False)
                else:
                    fields[target_name] = str(value)

        folders = item.get("folder") or []
        if isinstance(folders, dict):
            folders = [folders]

        headline_hit = any(bool(f.get("headline_keyword_mention")) for f in folders if isinstance(f, dict))
        content_hit = any(bool(f.get("content_keyword_mention")) for f in folders if isinstance(f, dict))
        ocr_hit = any(bool(f.get("ocr_keyword_mention")) for f in folders if isinstance(f, dict))
        subject_hit = any(bool(f.get("subject_mention")) for f in folders if isinstance(f, dict))

        if "标题提及" in feishu_field_set:
            fields.setdefault("标题提及", bool_to_str(headline_hit))
        if "正文提及" in feishu_field_set:
            fields.setdefault("正文提及", bool_to_str(content_hit))
        if "ocr 提及" in feishu_field_set:
            fields.setdefault("ocr 提及", bool_to_str(ocr_hit))
        if "文章提及" in feishu_field_set:
            fields.setdefault("文章提及", bool_to_str(subject_hit or headline_hit or content_hit or ocr_hit))

        if "入库时间" in feishu_field_set:
            fields["入库时间"] = int(datetime.now().timestamp() * 1000)

        if "品牌" in feishu_field_set and default_folder_id == 763579:
            fields["品牌"] = "小爱手机"

        if fields:
            records.append({"fields": fields})

    return records


def batch_create_records(
    tenant_access_token: str, records: List[Dict[str, Any]], batch_size: int = BATCH_SIZE,
) -> int:
    """优化：增大批量大小到 500，使用 session 复用连接"""
    if not BITABLE_URL:
        raise RuntimeError("BITABLE_URL 未初始化")
    app_token, table_id = _parse_bitable_url(BITABLE_URL)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
    headers = {"Authorization": f"Bearer {tenant_access_token}", "Content-Type": "application/json"}
    session = get_session()

    total = len(records)
    print(f"准备写入 {total} 条记录到多维表（批量大小：{batch_size}）...")

    for i in range(0, total, batch_size):
        chunk = records[i : i + batch_size]
        payload = {"records": chunk}
        resp = session.post(
            url, headers=headers,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"批量写入失败：{data}")
        print(f"已写入 {min(i + batch_size, total)}/{total} 条")

    return total


def run_once(interval_minutes: int = 10) -> int:
    """
    优化版本：
    1. 缓存 tenant_access_token
    2. 缓存唯一键（5 分钟有效期）
    3. 增大批量大小
    4. 使用连接池
    5. 只获取一次字段列表
    """
    folder_id = DEFAULT_FOLDER_ID
    customer_id = DEFAULT_CUSTOMER_ID
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=interval_minutes)

    start_ts = time.time()
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始同步，时间窗口：{start_time} ~ {end_time}")

    # 1. 获取数据
    items = fetch_all_items(
        folder_id=folder_id, start_time=start_time, end_time=end_time,
        customer_id=customer_id, page_size=PAGE_SIZE,
    )
    print(f"从小爱接口拉取到 {len(items)} 条记录（耗时：{time.time() - start_ts:.2f}s）")
    
    if not items:
        print("没有可写入的数据。")
        return 0

    # 2. 获取 token（带缓存）
    token_start = time.time()
    token = get_tenant_access_token()
    print(f"获取飞书 token 完成（耗时：{time.time() - token_start:.2f}s）")

    # 3. 获取字段列表（只调用一次）
    field_start = time.time()
    feishu_field_names = get_feishu_field_names(token)
    ensure_feishu_fields(token, feishu_field_names)
    feishu_field_names = get_feishu_field_names(token)  # 刷新字段列表
    print(f"字段准备完成（耗时：{time.time() - field_start:.2f}s）")

    # 4. 获取已有唯一键（带缓存）
    keys_start = time.time()
    # 这里强制从线上读取一次，确保 total_records 准确，以便判断是否需要新建表
    existing_keys, total_records, max_case_id = get_existing_keys(token, KEY_FIELD_NAME, force_refresh=True)
    print(f"唯一键检查完成（耗时：{time.time() - keys_start:.2f}s）")
    print(f"表中当前共有 {total_records} 条记录，其中 {len(existing_keys)} 条包含唯一键，最大 case ID: {max_case_id}")

    # 4.1 若当前表记录数达到单表上限，则在同一个应用下新建一个表，并切换 BITABLE_URL
    global BITABLE_URL
    new_bitable_url = _create_new_table_if_needed(token, total_records)
    if new_bitable_url:
        BITABLE_URL = new_bitable_url
        # 切换到新表后需要重新准备字段与唯一键信息（新表为空，记录数从 0 开始）
        field_start = time.time()
        feishu_field_names = get_feishu_field_names(token)
        ensure_feishu_fields(token, feishu_field_names)
        feishu_field_names = get_feishu_field_names(token)
        print(f"新表字段准备完成（耗时：{time.time() - field_start:.2f}s）")

        keys_start = time.time()
        existing_keys, total_records, max_case_id = get_existing_keys(token, KEY_FIELD_NAME, force_refresh=True)
        print(f"新表唯一键检查完成（耗时：{time.time() - keys_start:.2f}s）")
        print(f"新表当前共有 {total_records} 条记录，其中 {len(existing_keys)} 条包含唯一键，最大 case ID: {max_case_id}")

    # 5. 过滤增量数据
    new_items = []
    for it in items:
        key_val = it.get("md5_doc_id")
        if key_val is None or str(key_val) not in existing_keys:
            new_items.append(it)

    if not new_items:
        print("没有新增记录。")
        return 0

    # 6. 检查容量限制（单表上限 + 兜底上限）
    if total_records >= MAX_RECORDS:
        print("多维表记录数已达兜底上限，停止写入。")
        return 0

    max_can_insert = min(PER_TABLE_LIMIT - total_records, MAX_RECORDS - total_records)
    if len(new_items) > max_can_insert:
        print(f"增量记录 {len(new_items)} 条，将仅写入前 {max_can_insert} 条")
        new_items = new_items[:max_can_insert]

    # 7. 构造 records
    records = build_records_from_items(new_items, feishu_field_names)
    if "case ID" in feishu_field_names:
        next_id = max_case_id + 1
        for rec in records:
            rec_fields = rec.setdefault("fields", {})
            if "case ID" not in rec_fields or rec_fields["case ID"] in (None, ""):
                rec_fields["case ID"] = str(next_id)
                next_id += 1

    if not records:
        print("没有匹配到任何字段。")
        return 0

    # 8. 批量写入
    write_start = time.time()
    inserted = batch_create_records(token, records)
    print(f"写入完成（耗时：{time.time() - write_start:.2f}s）")
    
    total_time = time.time() - start_ts
    print(f"\n✅ 同步完成！总耗时：{total_time:.2f}s，写入 {inserted} 条记录")
    return inserted


def main() -> None:
    interval_minutes = 10
    interval_seconds = interval_minutes * 60
    while True:
        run_once(interval_minutes=interval_minutes)
        print(f"休眠 {interval_minutes} 分钟后进行下一次同步……")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    main()
