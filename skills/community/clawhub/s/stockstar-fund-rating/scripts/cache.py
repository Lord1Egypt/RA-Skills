#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缓存管理模块。

缓存策略：
1. 首次查询：并行下载全部机构的评级页面，构建全量缓存（JSON 文件）
2. 后续查询：快速读取本地缓存（进程内内存缓存，避免重复读盘）
3. 过期检测：并行检测各机构评级日期是否变化
4. 增量更新：检测到某个机构评级日期变化时，只重新下载该机构数据
5. 单基金补查：当某基金不在全量缓存中时（首次评级或新基金），
   并行搜索各页面并提取该基金的评级

所有 HTTP 请求使用 ThreadPoolExecutor 并行化，
并发数等于机构数，单机构失败不影响其他机构。

 缓存 JSON 结构（紧凑格式，无冗余字段）：
{
  "build_date": "2026-07-21",          ← 缓存构建日期
  "institutions": {                     ← 各机构信息
    "shzq": {"name": "上海证券", "rating_date": "2026-06-30"}
  },
  "funds": {                            ← 所有基金评级
    "001075": {
      "name": "宝盈转型动力混合A",
      "ratings": {
        "shzq": 5,                      ← 直接存 int，不套 {"rating": ...} 层级
        ...
      }
    }
  }
}

rating_text（一星~五星）和 rating_stars（★★★☆☆）为 rating 的派生字段，
在输出阶段由 parser._rating_to_text/stars 实时计算，缓存中不存储。
change 字段不缓存（0/74351 条目含 change），如需变动方向可实时从页面解析。
"""

import concurrent.futures
import json
import os
import sys
import time

from config import INSTITUTIONS, CACHE_DIR, CACHE_FILE, BASE_URL
from utils import http_get, http_get_partial
from parser import parse_rating_date, parse_rating_page, extract_fund

# 进程内内存缓存，同进程多次 load() 避免重复读盘
_CACHE = None


def _cache_path():
    """获取缓存文件的完整路径。"""
    if CACHE_DIR:
        return os.path.join(CACHE_DIR, CACHE_FILE)
    return CACHE_FILE


def load():
    """
    从本地 JSON 文件加载缓存。
    文件不存在或损坏时返回 None，触发全量构建。
    首次读取后缓存到模块级变量 _CACHE，同进程内后续调用秒回。
    """
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    path = _cache_path()
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            _CACHE = json.load(f)
            return _CACHE
    except (json.JSONDecodeError, IOError):
        return None


def save(cache):
    """
    将缓存写入本地 JSON 文件。
    紧凑格式（无缩进），减少磁盘占用。
    使用原子写入（先写 .tmp 再 rename），避免写入中断导致文件损坏。
    同时更新进程内内存缓存。
    """
    global _CACHE
    _CACHE = cache
    path = _cache_path()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, path)


# ── 并行下载辅助函数 ──────────────────────────────────────────

def _download_one(key):
    """单个机构的完整页面下载 + 解析。失败时返回 (key, None)。"""
    inst = INSTITUTIONS[key]
    url = BASE_URL + inst["page"]
    try:
        html = http_get(url)
    except Exception:
        return key, None
    date = parse_rating_date(html)
    funds = parse_rating_page(html, key)
    return key, {
        "institution": {"name": inst["name"], "rating_date": date},
        "funds": funds,
    }


def _check_one(key, cache):
    """单个机构的过期检测。返回过期 key 或 None。"""
    url = BASE_URL + INSTITUTIONS[key]["page"]
    try:
        partial = http_get_partial(url, max_bytes=10240)
    except Exception:
        return None
    if not partial:
        return None
    page_date = parse_rating_date(partial)
    cached_date = cache.get("institutions", {}).get(key, {}).get("rating_date", "")
    if page_date and page_date != cached_date:
        return key
    return None


def _search_one_fund(key, code):
    """在单个机构页面中搜索某只基金。返回 (key, 结果字典) 或 (key, None)。"""
    inst = INSTITUTIONS[key]
    url = BASE_URL + inst["page"]
    try:
        html = http_get(url)
    except Exception:
        return key, None
    result = extract_fund(html, code, key)
    return key, result


def _merge_fund_rating(cache, code, data, key):
    """
    将某机构的一只基金评级合并到缓存中。
    评级直接存 int 值（如 5），不套 {"rating": ...} 层级，
    减少 JSON 文件体积（省 ~0.93 MB）。
    cache：缓存字典（会被就地修改）
    data：该基金的数据（来自 parse_rating_page 或 extract_fund）
    key：机构 key
    """
    if code not in cache["funds"]:
        cache["funds"][code] = {"name": data["name"], "ratings": {}}
    cache["funds"][code]["ratings"][key] = int(data["rating"])


def _merge_institution(cache, key, result):
    """将 _download_one 的返回结果合并到缓存中。"""
    cache["institutions"][key] = result["institution"]
    for code, data in result["funds"].items():
        _merge_fund_rating(cache, code, data, key)


# ── 对外接口 ──────────────────────────────────────────────────

def build_cache():
    """
    全量构建缓存：并行下载所有机构的全部评级页面。
    每下载一个页面，解析出该机构的所有基金评级，合并到一个 funds 字典中。
    单机构下载失败（网络/超时）不影响其他机构。
    首轮并行失败后，对失败机构逐一个体重试 ×3。
    仅存储 rating 值（1-5），rating_text/stars 由输出阶段实时推导。
    """
    print("⏳ 正在获取各机构评级数据...", file=sys.stderr)
    cache = {"institutions": {}, "funds": {}}

    # ── 第一轮：并行下载全部 7 家 ──
    def _do_batch(keys):
        failed = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(keys)) as ex:
            futs = {ex.submit(_download_one, k): k for k in keys}
            for fut in concurrent.futures.as_completed(futs):
                k = futs[fut]
                try:
                    _, result = fut.result()
                except Exception:
                    failed.append(k)
                    continue
                if result is None:
                    failed.append(k)
                    continue
                _merge_institution(cache, k, result)
        return failed

    failed = _do_batch(list(INSTITUTIONS.keys()))

    # ── 第二轮：失败机构逐一个体重试 ×3 ──
    still_failed = []
    if failed:
        print(f"⚠️ 部分机构获取失败，正在逐一个体重试...", file=sys.stderr)
        for k in failed:
            ok = False
            for attempt in range(1, 4):
                try:
                    _, result = _download_one(k)
                    if result is not None:
                        _merge_institution(cache, k, result)
                        ok = True
                        break
                except Exception:
                    pass
                if not ok and attempt < 3:
                    print(f"   {INSTITUTIONS[k]['name']} 第{attempt}次失败，正在重试...", file=sys.stderr)
            if not ok:
                still_failed.append(k)

    # ── 报告最终失败 ──
    if still_failed:
        names = [INSTITUTIONS[k]["name"] for k in still_failed]
        print(f"⚠️ 以下机构最终获取失败：{'、'.join(names)}", file=sys.stderr)
        print(f"   下次查询自动重试", file=sys.stderr)

    cache["build_date"] = time.strftime("%Y-%m-%d")
    save(cache)
    print("✅ 数据初始化完成", file=sys.stderr)
    return cache


def check_expiry(cache):
    """
    检查缓存是否过期：并行下载各机构页面前 10KB，提取评级日期比对。
    单机构下载失败则跳过，保留已有缓存。
    返回需要更新的机构 key 列表。
    """
    expired = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(INSTITUTIONS)) as executor:
        futures = {executor.submit(_check_one, key, cache): key for key in INSTITUTIONS}
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
            except Exception:
                continue
            if result:
                expired.append(result)
    return expired


def update_institution(cache, key):
    """
    增量更新某个机构的评级数据。
    在 check_expiry 检测到某个机构的评级日期变化后调用。
    只重新下载该机构的页面，更新 funds 中对应机构的所有基金评级。
    """
    inst = INSTITUTIONS[key]
    url = BASE_URL + inst["page"]
    html = http_get(url)
    date = parse_rating_date(html)
    if "institutions" not in cache:
        cache["institutions"] = {}
    cache["institutions"][key] = {
        "name": inst["name"],
        "rating_date": date,
    }
    funds = parse_rating_page(html, key)
    for code, data in funds.items():
        _merge_fund_rating(cache, code, data, key)
    save(cache)
    return cache


def search_by_name(cache, name):
    """
    按基金名称查找代码。
    精确匹配优先，子串匹配兜底。

    返回：
      - 精确匹配 → 直接返回 {"code": "001075"}
      - 子串匹配 1 个 → 返回 {"code": "001075"}
      - 子串匹配 N 个 → 返回 {"multiple": [{"name": ..., "code": ...}, ...]}
      - 无匹配 → 返回 None
    """
    funds = cache.get("funds", {})
    exact = None
    for code, fund in funds.items():
        if fund["name"] == name:
            exact = code
            break
    if exact:
        return {"code": exact}

    matches = []
    for code, fund in funds.items():
        if name in fund["name"]:
            matches.append({"name": fund["name"], "code": code})

    if len(matches) == 1:
        return {"code": matches[0]["code"]}
    if len(matches) > 1:
        return {"multiple": matches}
    return None


def find_fund(cache, code):
    """
    在缓存中查找某只基金的评级。
    直接字典查询 O(1)，用于缓存命中时的秒回。
    返回 None 表示该基金不在缓存中（新基金或未评级）。
    """
    return cache.get("funds", {}).get(code)


def append_fund(cache, code):
    """
    单基金补查：当基金不在全量缓存中时，并行下载各机构页面，
    从每个页面中提取该基金的评级。
    用于缓存未命中场景——全量缓存只包含评级页面上的所有基金，
    但用户查询的基金可能不在某些机构的列表中。
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(INSTITUTIONS)) as executor:
        futures = {executor.submit(_search_one_fund, key, code): key for key in INSTITUTIONS}
        for future in concurrent.futures.as_completed(futures):
            try:
                key, result = future.result()
            except Exception:
                continue
            if result:
                _merge_fund_rating(cache, code, result, key)
    save(cache)
    return cache.get("funds", {}).get(code)
