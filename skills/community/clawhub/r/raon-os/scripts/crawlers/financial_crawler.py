#!/usr/bin/env python3
"""
KODIT/KIBO 금융 상품 정보 업데이트 크롤러

FINANCIAL_PRODUCTS 정적 데이터를 기반으로
실시간 URL 유효성 체크 및 금리 업데이트.

⚠️ urllib.request 사용 (requests 없음)
⚠️ Python 3.9+ compatible
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = SCRIPT_DIR.parent
EVAL_DATA_DIR = BASE_DIR / "eval_data"

sys.path.insert(0, str(SCRIPT_DIR))

from financial_map import FINANCIAL_PRODUCTS

USER_AGENT = "RaonOS-Crawler/0.7.6 (+https://k-startup.ai; url-health-check)"
CHECK_TIMEOUT = 10
CRAWL_DELAY = 1.0

OUTPUT_FILE = EVAL_DATA_DIR / "financial_products_updated.json"


def check_url_alive(url: str) -> tuple:
    """
    URL 유효성 체크.

    Returns:
        (is_alive: bool, status_code: int, response_time_ms: float)
    """
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": USER_AGENT},
    )
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=CHECK_TIMEOUT) as resp:  # nosec B310
            elapsed = (time.time() - start) * 1000
            return True, resp.getcode(), round(elapsed, 1)
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - start) * 1000
        # 4xx는 URL 자체는 살아있음
        if e.code < 500:
            return True, e.code, round(elapsed, 1)
        return False, e.code, round(elapsed, 1)
    except Exception as e:
        elapsed = (time.time() - start) * 1000
        print(f"[financial_crawler] 연결 실패 {url}: {e}", file=sys.stderr)
        return False, 0, round(elapsed, 1)


def extract_rate_from_html(html: str, product_name: str) -> Optional[str]:
    """HTML에서 금리 정보 추출 시도."""
    import re

    if not html:
        return None

    patterns = [
        r"금리[:\s]*(\d+\.?\d*)\s*%",
        r"이자율[:\s]*(\d+\.?\d*)\s*%",
        r"연\s*(\d+\.?\d*)\s*%",
    ]
    for pat in patterns:
        m = re.search(pat, html)
        if m:
            rate_val = float(m.group(1))
            if 0.1 <= rate_val <= 20:  # 현실적 금리 범위
                return f"{rate_val}%"
    return None


def fetch_page(url: str) -> Optional[str]:
    """페이지 HTML 가져오기."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=CHECK_TIMEOUT) as resp:  # nosec B310
            charset = "utf-8"
            ct = resp.headers.get("Content-Type", "")
            if "euc-kr" in ct.lower():
                charset = "euc-kr"
            return resp.read().decode(charset, errors="replace")
    except Exception:
        return None


def update_products(dry_run: bool = False) -> list:
    """
    FINANCIAL_PRODUCTS 전체 URL 유효성 체크 및 금리 업데이트.

    Returns:
        업데이트된 상품 목록
    """
    print("[financial_crawler] 금융 상품 URL 체크 시작", file=sys.stderr)
    updated_products = []
    check_time = datetime.now(timezone.utc).isoformat()

    for product in FINANCIAL_PRODUCTS:
        url = product.get("url", "")
        if not url:
            updated_products.append({**product, "url_status": "no_url"})
            continue

        print(f"[financial_crawler] 체크 중: {product['name'][:40]}...", file=sys.stderr)
        is_alive, status_code, resp_time = check_url_alive(url)

        updated = dict(product)
        updated["url_check"] = {
            "alive": is_alive,
            "status_code": status_code,
            "response_time_ms": resp_time,
            "checked_at": check_time,
        }

        # URL 살아있으면 금리 업데이트 시도
        if is_alive and product.get("type") in ("융자", "보증"):
            html = fetch_page(url)
            new_rate = extract_rate_from_html(html, product["name"])
            if new_rate:
                old_rate = product.get("rate", "N/A")
                if new_rate != old_rate:
                    print(
                        f"[financial_crawler] 금리 업데이트: {product['name']}: "
                        f"{old_rate} → {new_rate}",
                        file=sys.stderr,
                    )
                    updated["rate"] = new_rate
                    updated["rate_updated_at"] = check_time

        status_emoji = "✅" if is_alive else "❌"
        print(
            f"  {status_emoji} {product['name'][:35]}: "
            f"HTTP {status_code} ({resp_time}ms)",
            file=sys.stderr,
        )

        updated_products.append(updated)
        time.sleep(CRAWL_DELAY)

    # 결과 저장
    if not dry_run:
        EVAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(str(OUTPUT_FILE), "w", encoding="utf-8") as f:
            json.dump(
                {
                    "updated_at": check_time,
                    "total": len(updated_products),
                    "alive_count": sum(1 for p in updated_products if p.get("url_check", {}).get("alive")),
                    "products": updated_products,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        print(f"[financial_crawler] 저장 완료: {OUTPUT_FILE}", file=sys.stderr)

    alive = sum(1 for p in updated_products if p.get("url_check", {}).get("alive"))
    print(f"[financial_crawler] 완료: {alive}/{len(updated_products)}개 URL 정상", file=sys.stderr)
    return updated_products


def get_updated_products() -> list:
    """
    저장된 업데이트 결과 로드. 없으면 원본 반환.
    """
    if OUTPUT_FILE.exists():
        try:
            with open(str(OUTPUT_FILE), "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("products", FINANCIAL_PRODUCTS)
        except Exception:
            pass
    return FINANCIAL_PRODUCTS


# ─── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="금융 상품 URL 유효성 체크")
    parser.add_argument("--dry-run", action="store_true", help="파일 저장 없이 결과 확인")
    args = parser.parse_args()

    results = update_products(dry_run=args.dry_run)
    print(f"\n체크 완료: {len(results)}개 상품")
    alive = sum(1 for r in results if r.get("url_check", {}).get("alive"))
    print(f"URL 정상: {alive}/{len(results)}")
