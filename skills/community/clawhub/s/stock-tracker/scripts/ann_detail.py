#!/usr/bin/env python3
"""公告正文抓取模块 - 通过东方财富 API 获取公告全文

获取策略:
  1. 优先调用 np-cnotice-stock API（需东方财富网络环境）
  2. API 失败时回退到下载 PDF 并提取文本（适合服务器环境）

清洗策略:
  - 获取全文后自动调用 text_cleaner 移除模板套话
  - full_text 存原始文本，clean_text 存清洗后文本

跳过采集:
  - 公司章程（纯法律模板，无公司特有信息）
"""

import io
import json
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Callable

import pdfplumber
import requests

from text_cleaner import clean_announcement_text
from llm_judge import LLMJudge

logger = logging.getLogger(__name__)

CNOTICE_API = "https://np-cnotice-stock.eastmoney.com/api/content/ann"

# 跳过全文采集的标题模式
SKIP_CONTENT_PATTERNS = [
    re.compile(r"公司章程", re.IGNORECASE),
    re.compile(r"信用评级|跟踪评级", re.IGNORECASE),
    re.compile(r"募集说明书", re.IGNORECASE),
    # 债券程序性公告（付息、上市、摘牌、发行结果等），保留发行公告
    re.compile(r"付息公告|付息\s*公告", re.IGNORECASE),
    re.compile(r"上市公告|上市的公告|摘牌", re.IGNORECASE),
    re.compile(r"发行结果公告|票面利率|簿记建档|更名公告|发行完毕", re.IGNORECASE),
    # 董事会报告、法律意见书（纯程序性文件）
    re.compile(r"董事会报告", re.IGNORECASE),
    re.compile(r"法律意见书|法律意见\s*$", re.IGNORECASE),
    # 股东会决议公告、投票表决结果
    re.compile(r"股东会决议公告|股东会表决结果|投票表决结果", re.IGNORECASE),
    # 薪酬制度、股东周年会通告、担保额度、业绩说明会召开情况
    re.compile(r"薪酬", re.IGNORECASE),
    re.compile(r"周年会通告", re.IGNORECASE),
    re.compile(r"担保额度|提供担保|为.*担保|担保公告|合计.*担保", re.IGNORECASE),
    re.compile(r"召开情况", re.IGNORECASE),
    # 公司内部制度文件（离职管理制度、议事规则、工作细则等）
    re.compile(r"管理制度|议事规则|工作细则|管理规则|内控手册|合规手册", re.IGNORECASE),
    # 回购注销股权激励的限制性股票（量小无影响，保留普通回购注销）
    re.compile(r"回购注销.*(?:股权激励|限制性股票|激励对象)", re.IGNORECASE),
    # 业绩说明会（纯形式，无实质内容）
    re.compile(r"业绩说明会|业绩发布会|召开情况", re.IGNORECASE),
    # 限制性股票/股票期权授予登记（常规程序性公告）
    re.compile(r"限制性股票.*(?:预留授予|完成登记)|股票期权.*(?:预留授予|完成登记)", re.IGNORECASE),
    # 限制性股票作废（量小无市场影响）
    re.compile(r"作废.*限制性股票|限制性股票.*作废", re.IGNORECASE),
]
PDF_BASE = "https://pdf.dfcfw.com/pdf/H2_{art_code}_1.pdf"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://data.eastmoney.com/",
    "Connection": "close",
}


def _get_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def _extract_text_from_pdf(pdf_url: str, timeout: int = 30) -> Optional[str]:
    """下载 PDF 并提取文本"""
    try:
        resp = requests.get(pdf_url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        with pdfplumber.open(io.BytesIO(resp.content)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        text = "\n".join(pages).strip()
        return text if text else None
    except (OSError, ValueError) as e:
        logger.debug("PDF 提取失败 %s: %s", pdf_url, e)
        return None


# 超长文档只提取目录/概要（保留 attach_url 指向原始 PDF）
TOC_ONLY_PATTERNS = [
    re.compile(r"通函", re.IGNORECASE),
    re.compile(r"海外市场公告|海外监管公告", re.IGNORECASE),
    re.compile(r"股东会会议资料|股东大会会议资料|会议文件", re.IGNORECASE),
    re.compile(r"发行公告", re.IGNORECASE),
]


def _extract_toc_only(text: str, title: str = "") -> str:
    """从超长文档中提取目录/概要部分，省略冗长正文

    策略:
      1. 查找 "目 录" 或 "目录" 标记，截取到其后的条目列表末尾
      2. 没有目录标记时，保留开头 1500 字（通常包含提案摘要）
      3. 最终不超过 2000 字
    """
    max_toc = 2000

    # 尝试找目录标记
    for marker in ["目 录", "目  录", "目录"]:
        idx = text.find(marker)
        if idx >= 0:
            # 从目录标记开始，截取目录条目部分
            tail = text[idx:]
            # 目录条目通常简短，找到第一个段落结束或连续页码结束
            end = min(len(tail), 800)
            for stop in range(100, len(tail)):
                if tail[stop:stop+2] in ("\n\n", "页次"):
                    end = stop + 100
                    break
            return tail[:end].strip()[:max_toc]

    # 没有目录标记，取开头
    return text[:max_toc].strip()


def should_skip_content(ann: dict) -> bool:
    """判断是否应跳过全文采集（如公司章程等纯模板文档）"""
    title = ann.get("title", "")
    for pattern in SKIP_CONTENT_PATTERNS:
        if pattern.search(title):
            logger.info("跳过全文采集: %s", title[:60])
            return True
    return False


def fetch_announcement_content(
    art_code: str,
    stock_code: str = "",
    timeout: int = 15,
    retries: int = 1,
    pdf_url_override: str = "",
) -> Optional[dict]:
    """获取公告全文内容

    优先调用内容 API，失败时回退到 PDF 提取。
    pdf_url_override 不为空时优先使用该 URL 下载 PDF。

    Args:
        art_code: 公告文章编码
        stock_code: 股票代码（可选，仅用于日志）
        timeout: 请求超时时间
        retries: API 重试次数
        pdf_url_override: 直接指定 PDF 链接（巨潮来源）

    Returns:
        dict 包含 notice_content 等字段，失败返回 None
    """
    params = {
        "art_code": art_code,
        "client_source": "web",
    }
    session = _get_session()
    try:
        for attempt in range(retries + 1):
            try:
                resp = session.get(
                    CNOTICE_API,
                    params=params,
                    timeout=timeout,
                )
                resp.raise_for_status()
                if not resp.text:
                    if attempt < retries:
                        continue
                    break
                data = resp.json()
                if data.get("success") != 1:
                    if attempt < retries:
                        continue
                    break
                return data.get("data")
            except (requests.RequestException, json.JSONDecodeError) as e:
                logger.debug("东方财富 API 请求失败 (尝试 %d/%d): %s", attempt + 1, retries, e)
                if attempt < retries:
                    time.sleep((attempt + 1) * 2)
                continue
    finally:
        session.close()

    pdf_url = pdf_url_override or PDF_BASE.format(art_code=art_code)
    text = _extract_text_from_pdf(pdf_url)
    if text:
        return {
            "notice_content": text,
            "attach_url": pdf_url,
            "notice_title": "",
            "art_code": art_code,
        }

    return None


def fetch_all_contents(
    announcements: list[dict],
    save_batch: Optional[Callable[[list[dict]], None]] = None,
    batch_size: int = 10,
    llm_judge: Optional[LLMJudge] = None,
    max_workers: int = 5,
    judge_workers: int = 20,
) -> list[dict]:
    """批量获取公告全文（并发判断 + 并发下载 + 顺序保存）

    Phase 1: 跳过检查（顺序） + LLM 标题判断（并发）
    Phase 2: 并发下载 PDF / 调用 API 获取正文
    Phase 3: 顺序清洗文本 + 分批保存到数据库
    """

    # ── Phase 1a: 正则跳过检查（顺序，极快） ──
    need_judge = []   # 需要 LLM 判断的 (index, ann)
    skipped = 0
    for i, ann in enumerate(announcements):
        art_code = ann.get("art_code", "")
        if not art_code:
            skipped += 1
            continue
        if should_skip_content(ann):
            ann["full_text"] = ""
            ann["clean_text"] = ""
            ann["attach_url"] = ""
            skipped += 1
            continue
        need_judge.append((i, ann))

    # ── Phase 1b: LLM 标题判断（并发） ──
    to_fetch = []
    if llm_judge is not None and llm_judge.enabled and need_judge:
        logger.info("LLM 并发判断 %d 条标题 (workers=%d)...", len(need_judge), judge_workers)

        def _judge_one(item):
            idx, ann = item
            title = ann.get("title", "")
            stock_name = ann.get("stock_name", "")
            market = ann.get("market", "A股")
            result = llm_judge.judge(title, stock_name, market)
            return idx, result

        with ThreadPoolExecutor(max_workers=judge_workers) as executor:
            futures = {executor.submit(_judge_one, item): item for item in need_judge}
            done_count = 0
            for future in as_completed(futures):
                idx, judge_result = future.result()
                ann = announcements[idx]
                ann["ann_type_tag"] = judge_result.get("type", "个股其他公告")
                ann["ann_type_category"] = judge_result.get("category", "")
                if judge_result.get("valuable", True):
                    to_fetch.append((idx, ann))
                else:
                    ann["full_text"] = ""
                    ann["clean_text"] = ""
                    ann["attach_url"] = ""
                    skipped += 1
                done_count += 1
                if done_count % 20 == 0 or done_count == len(need_judge):
                    logger.info("  LLM 判断进度: %d/%d", done_count, len(need_judge))
    else:
        # 无 LLM judge，所有通过正则的都直接下载
        to_fetch = need_judge

    if save_batch:
        save_batch(announcements)

    if not to_fetch:
        logger.info("Phase 1 完成：跳过 %d 条，待下载 0 条", skipped)
        return announcements

    logger.info("Phase 1 完成：跳过 %d 条，待下载 %d 条", skipped, len(to_fetch))

    # ── Phase 2: 并发下载正文 ──
    def _fetch_one(ann):
        pdf_url = ann.get("url", "")
        if pdf_url and not pdf_url.upper().endswith(".PDF"):
            pdf_url = ""
        return fetch_announcement_content(
            ann.get("art_code", ""),
            ann.get("stock_code", ""),
            pdf_url_override=pdf_url,
        )

    fetched = {}   # {index: result_dict}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_fetch_one, ann): idx for idx, ann in to_fetch}
        done_count = 0
        for future in as_completed(futures):
            idx = futures[future]
            try:
                result = future.result()
                fetched[idx] = result
            except Exception as e:
                logger.warning("下载失败公告 %d: %s", idx, e)
                fetched[idx] = None
            done_count += 1
            if done_count % 10 == 0 or done_count == len(to_fetch):
                logger.info("  下载进度: %d/%d", done_count, len(to_fetch))

    # 统计下载成功/失败，并收集失败列表
    fetch_success = sum(1 for r in fetched.values() if r)
    fetch_fail = len(fetched) - fetch_success
    logger.info("下载完成: %d/%d 成功, %d 失败", fetch_success, len(to_fetch), fetch_fail)

    # 打印失败详情
    if fetch_fail > 0:
        logger.warning("--- 以下 %d 条公告正文获取失败 ---", fetch_fail)
        for i, ann in enumerate(announcements):
            if i in fetched and not fetched[i]:
                stock_code = ann.get("stock_code", "")
                stock_name = ann.get("stock_name", "")
                title = ann.get("title", "")
                url = ann.get("url", "")
                art_code = ann.get("art_code", "")
                pdf_url = url or PDF_BASE.format(art_code=art_code)
                logger.warning("  [%s %s] %s | 链接: %s", stock_code, stock_name, title, pdf_url)
        logger.warning("--- 失败列表结束 ---")

    # ── Phase 3: 顺序清洗 + 分批保存 ──
    process_idx = 0
    for i, ann in enumerate(announcements):
        if i not in fetched:
            continue
        process_idx += 1
        result = fetched[i]
        logger.info(
            "处理正文 [%d/%d] %s - %s...",
            process_idx, len(fetched),
            ann.get("stock_name", ann.get("stock_code", "")),
            ann.get("title", "")[:30],
        )
        if result:
            raw_text = result.get("notice_content", "")
            ann["full_text"] = raw_text
            title = ann.get("title", "")
            if any(p.search(title) for p in TOC_ONLY_PATTERNS) and len(raw_text) > 5000:
                ann["clean_text"] = clean_announcement_text(_extract_toc_only(raw_text, title))
                ann["attach_url"] = result.get("attach_url", "")
                logger.info("  提取目录 (%d 字，全文 %d 字)", len(ann["clean_text"]), len(raw_text))
            else:
                ann["clean_text"] = clean_announcement_text(raw_text)
                ann["attach_url"] = result.get("attach_url", "")
        else:
            ann["full_text"] = ""
            ann["clean_text"] = ""
            ann["attach_url"] = ""
            logger.info("  正文获取失败，已清空")

        if save_batch and process_idx % batch_size == 0:
            save_batch(announcements)

    if save_batch:
        save_batch(announcements)

    return announcements
