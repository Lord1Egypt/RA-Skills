#!/usr/bin/env python3
"""
와디즈/텀블벅 DM 파이프라인
달비님 맥에서 직접 실행하는 버전 (Playwright 기반)

사용법:
    python3 pipeline.py [카테고리] [최대개수]
    python3 pipeline.py all 100
    python3 pipeline.py beauty 50
"""

import sys
import os
import csv
import time
import random
import json
import re
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Playwright 미설치. 아래 명령어 실행 후 다시 시도하세요:")
    print("   pip install playwright")
    print("   python -m playwright install chromium")
    sys.exit(1)

try:
    import anthropic
except ImportError:
    print("❌ anthropic 미설치. 아래 명령어 실행 후 다시 시도하세요:")
    print("   pip install anthropic")
    sys.exit(1)

# ── 설정 ─────────────────────────────────────────
CATEGORY_MAP = {
    "food":      "https://www.wadiz.kr/web/wreward/category/100?sort=funding&status=opening",
    "beauty":    "https://www.wadiz.kr/web/wreward/category/106?sort=funding&status=opening",
    "lifestyle": "https://www.wadiz.kr/web/wreward/category/101?sort=funding&status=opening",
    "fashion":   "https://www.wadiz.kr/web/wreward/category/102?sort=funding&status=opening",
    "all":       "https://www.wadiz.kr/web/wreward/main?sort=funding&status=opening",
}

ACHIEVEMENT_MIN = 50
ACHIEVEMENT_MAX = 99
REQUEST_DELAY = (2, 4)  # 초 (랜덤 딜레이)

OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

DM_TEMPLATE = """안녕하세요, {project_name} 보고 연락드렸어요.

{hook}

저는 상세 페이지 읽고 소재 100개 만들어드리는 서비스를 하는데,
첫 의뢰는 10개 먼저 무료로 만들어드리고 마음에 드시면 그때 결제하시는 방식이에요.

관심 있으시면 편하게 말씀해 주세요."""


# ── 크롤링 ─────────────────────────────────────────
def get_project_list(page, category_url: str, max_count: int) -> list[dict]:
    """와디즈 카테고리 페이지에서 프로젝트 목록 수집"""
    print(f"\n📋 프로젝트 목록 수집 중...")
    page.goto(category_url, wait_until="networkidle", timeout=30000)
    time.sleep(2)

    projects = []
    last_count = 0
    scroll_attempts = 0

    while len(projects) < max_count and scroll_attempts < 30:
        # 카드 수집
        cards = page.query_selector_all(".ProjectCard_projectCard__GcBEG, [class*='projectCard'], [class*='ProjectCard']")
        if not cards:
            # 대안 셀렉터
            cards = page.query_selector_all("a[href*='/web/wreward/project/']")

        for card in cards:
            if len(projects) >= max_count:
                break
            try:
                # URL
                href = card.get_attribute("href") or ""
                if not href.startswith("http"):
                    href = "https://www.wadiz.kr" + href
                if href in [p["url"] for p in projects]:
                    continue

                # 달성률 추출
                text = card.inner_text()
                rate_match = re.search(r"(\d+(?:\.\d+)?)\s*%", text)
                if not rate_match:
                    continue
                rate = float(rate_match.group(1))
                if not (ACHIEVEMENT_MIN <= rate <= ACHIEVEMENT_MAX):
                    continue

                # 프로젝트명
                title_el = card.query_selector("h3, h2, [class*='title'], [class*='Title']")
                title = title_el.inner_text().strip() if title_el else "알 수 없음"

                projects.append({
                    "url": href,
                    "title": title,
                    "achievement_rate": rate,
                    "description": "",
                    "dm": "",
                })
                print(f"  [{len(projects)}] {title[:30]} — {rate}%")
            except Exception:
                continue

        # 스크롤
        if len(projects) == last_count:
            scroll_attempts += 1
            page.evaluate("window.scrollBy(0, window.innerHeight)")
            time.sleep(random.uniform(*REQUEST_DELAY))
        else:
            scroll_attempts = 0
            last_count = len(projects)

    return projects


def get_project_detail(page, url: str) -> str:
    """프로젝트 상세 페이지에서 핵심 내용 추출"""
    try:
        page.goto(url, wait_until="networkidle", timeout=20000)
        time.sleep(1)
        # 제목 + 소개 텍스트만
        texts = []
        for sel in ["h1", ".reward-intro", "[class*='intro']", "[class*='summary']", "[class*='description']"]:
            els = page.query_selector_all(sel)
            for el in els[:2]:
                t = el.inner_text().strip()
                if len(t) > 10:
                    texts.append(t[:300])
        return " | ".join(texts[:3])
    except Exception:
        return ""


# ── DM 생성 ─────────────────────────────────────────
def generate_dm(title: str, description: str) -> str:
    """Anthropic API로 개인화 DM 생성"""
    if not ANTHROPIC_API_KEY:
        # API 키 없으면 기본 템플릿
        hook = f"{title}의 제품 방향이 흥미로워서요."
        return DM_TEMPLATE.format(project_name=title, hook=hook)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt = f"""아래 와디즈 펀딩 프로젝트를 보고, 메이커에게 보낼 짧은 DM 메시지를 만들어줘.

프로젝트명: {title}
프로젝트 내용: {description[:500]}

DM 조건:
- 전체 100단어 이내
- 첫 줄: 프로젝트 특징 한 가지를 짚어서 "보고 연락드렸어요" 형태
- AI 언급 절대 금지
- 자기자랑 금지
- 오퍼: "상세 페이지 읽고 소재 100개 만들어드리는 서비스인데, 첫 의뢰는 10개 먼저 무료로 만들어드리고 마음에 드시면 결제하는 방식"
- 마무리: "관심 있으시면 편하게 말씀해 주세요."
- 존댓말, 자연스러운 한국어

DM 텍스트만 출력. 다른 설명 없이."""

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text.strip()
    except Exception as e:
        print(f"  ⚠️  DM 생성 실패 ({e}), 기본 템플릿 사용")
        hook = f"{title}의 방향이 흥미로워서요."
        return DM_TEMPLATE.format(project_name=title, hook=hook)


# ── 메인 ─────────────────────────────────────────
def main():
    category = sys.argv[1] if len(sys.argv) > 1 else "all"
    max_count = int(sys.argv[2]) if len(sys.argv) > 2 else 50

    if category not in CATEGORY_MAP:
        print(f"❌ 지원하지 않는 카테고리: {category}")
        print(f"   사용 가능: {', '.join(CATEGORY_MAP.keys())}")
        sys.exit(1)

    if not ANTHROPIC_API_KEY:
        print("⚠️  ANTHROPIC_API_KEY 환경변수 없음. 기본 템플릿으로 DM 생성합니다.")
        print("   export ANTHROPIC_API_KEY='sk-ant-...' 설정 후 실행하면 개인화 DM 생성됩니다.\n")

    print(f"🚀 와디즈 DM 파이프라인 시작")
    print(f"   카테고리: {category} | 목표: {max_count}개 | 달성률: {ACHIEVEMENT_MIN}~{ACHIEVEMENT_MAX}%")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 디버깅 위해 헤드풀
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
        )
        page = context.new_page()

        # 1. 프로젝트 목록 수집
        projects = get_project_list(page, CATEGORY_MAP[category], max_count)
        print(f"\n✅ {len(projects)}개 프로젝트 수집 완료 (달성률 {ACHIEVEMENT_MIN}~{ACHIEVEMENT_MAX}%)")

        if not projects:
            print("❌ 조건에 맞는 프로젝트가 없습니다.")
            browser.close()
            return

        # 2. 상세 페이지 분석 + DM 생성
        print(f"\n✍️  DM 생성 중...")
        for i, proj in enumerate(projects):
            print(f"  [{i+1}/{len(projects)}] {proj['title'][:30]}")
            desc = get_project_detail(page, proj["url"])
            proj["description"] = desc
            proj["dm"] = generate_dm(proj["title"], desc)
            time.sleep(random.uniform(*REQUEST_DELAY))

        browser.close()

    # 3. CSV 저장
    today = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = OUTPUT_DIR / f"dm_results_{today}.csv"
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url", "achievement_rate", "description", "dm"])
        writer.writeheader()
        writer.writerows(projects)

    print(f"\n🎉 완료! {len(projects)}개 DM 저장됨")
    print(f"   📁 {output_path}")
    print(f"\n--- DM 미리보기 (첫 3개) ---")
    for proj in projects[:3]:
        print(f"\n[{proj['title']} — {proj['achievement_rate']}%]")
        print(proj["dm"])
        print()


if __name__ == "__main__":
    main()
