#!/usr/bin/env python3
"""
Raon OS — YC RFS & a16z 기반 창업 아이디어 추천 모듈
"""

import os
import re
import json
import sys
from typing import List, Dict, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
REF_DIR = os.path.join(BASE_DIR, "references")
YC_RFS_FILE = os.path.join(REF_DIR, "yc-rfs.md")


def load_rfs_categories():
    # type: () -> List[Dict]
    """yc-rfs.md 파일에서 카테고리를 파싱하여 반환."""
    try:
        with open(YC_RFS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return []

    categories = []  # type: List[Dict]
    # Split by ## N. pattern
    sections = re.split(r'\n## (\d+)\. ', content)
    # sections[0] is header, then pairs of (number, content)
    for i in range(1, len(sections), 2):
        num = sections[i]
        body = sections[i + 1] if i + 1 < len(sections) else ""
        # Extract title from first line
        lines = body.strip().split("\n")
        title_line = lines[0] if lines else ""
        # title_line: "Cursor for Product Managers — AI 네이티브 PM 도구"
        parts = title_line.split("—")
        name = parts[0].strip() if parts else title_line.strip()
        subtitle = parts[1].strip() if len(parts) > 1 else ""

        # Extract metadata fields
        source = _extract_metadata(body, "소스")
        keywords_str = _extract_metadata(body, "키워드")
        korea_brief = _extract_metadata(body, "한국 적용")

        # Parse source into source_org and season
        source_org, season = _parse_source(source)

        # Parse keywords
        keywords = [k.strip() for k in keywords_str.split(",") if k.strip()] if keywords_str else []

        # Extract sections
        description = _extract_section(body, "설명")
        why_now = _extract_section(body, "왜 지금인지")
        founder = _extract_section(body, "적합한 창업자")
        korea = _extract_section(body, "한국 시장 적용")

        categories.append({
            "id": int(num),
            "name": name,
            "subtitle": subtitle,
            "source": source,
            "source_org": source_org,
            "season": season,
            "keywords": keywords,
            "korea_brief": korea_brief,
            "description": description,
            "why_now": why_now,
            "founder_profile": founder,
            "korea_market": korea,
            "full_text": body,
        })

    return categories


def _extract_metadata(text, field):
    # type: (str, str) -> str
    """Extract value from - **field:** value pattern."""
    pattern = r'-\s*\*\*' + re.escape(field) + r'[:\s]*\*\*\s*(.*?)(?:\n|$)'
    m = re.search(pattern, text)
    if m:
        return m.group(1).strip()
    return ""


def _parse_source(source):
    # type: (str) -> tuple
    """Parse source string like 'YC Spring 2026' into (org, season)."""
    if not source:
        return ("", "")
    s = source.strip()
    if s.startswith("YC"):
        org = "yc"
        season = s[2:].strip()
    elif "a16z" in s.lower():
        org = "a16z"
        season = s.replace("a16z", "").strip()
    else:
        org = s.lower()
        season = ""
    return (org, season)


def _extract_section(text, header):
    # type: (str, str) -> str
    """Extract content after **header:** pattern."""
    pattern = r'\*\*' + re.escape(header) + r'[:\s]*\*\*\s*(.*?)(?=\n\*\*|\n---|\n##|$)'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # Fallback: look for header: pattern
    pattern2 = re.escape(header) + r'[:\s]*\n(.*?)(?=\n\*\*|\n---|\n##|$)'
    m2 = re.search(pattern2, text, re.DOTALL)
    if m2:
        return m2.group(1).strip()
    return ""


def list_categories(source=None, season=None):
    # type: (Optional[str], Optional[str]) -> List[Dict]
    """전체 카테고리 목록 반환. source/season 필터 가능."""
    cats = load_rfs_categories()
    if source:
        src = source.lower()
        cats = [c for c in cats if c.get("source_org", "").lower() == src]
    if season:
        s = season.lower()
        cats = [c for c in cats if s in c.get("season", "").lower()]
    return cats


def get_category_detail(category_id):
    # type: (int) -> Optional[Dict]
    """특정 카테고리의 상세 정보 반환."""
    cats = load_rfs_categories()
    for cat in cats:
        if cat["id"] == category_id:
            return cat
    return None


def suggest_ideas(background, interests):
    # type: (str, str) -> Dict
    """사용자 배경/관심사 기반으로 카테고리 매칭 추천.
    
    키워드 매칭으로 필터링 후 결과 반환.
    """
    cats = load_rfs_categories()
    if not cats:
        return {"error": "아이디어 데이터를 찾을 수 없습니다.", "matches": []}

    raw_text = (background + " " + interests).lower()

    # 자연어 전처리: 불용어 제거 + 핵심 키워드 추출
    stopwords = {
        "관련", "관련해서", "하나", "추천", "추천해줘", "해줘", "해주세요", "알려줘",
        "알려주세요", "뭐가", "있어", "있을까", "좋을까", "좋겠어", "같은", "거",
        "이런", "저런", "그런", "에서", "으로", "하고", "싶어", "분야", "쪽",
        "the", "a", "an", "for", "and", "or", "is", "are", "to", "in", "of",
        "좀", "한번", "뭐", "어떤", "괜찮은", "해볼만한", "재밌는",
    }
    # 키워드 동의어 매핑
    synonyms = {
        "인공지능": "ai", "에이아이": "ai", "머신러닝": "ml", "딥러닝": "ai",
        "정부": "government", "공공": "government", "govtech": "government",
        "금융": "fintech", "핀테크": "fintech", "finance": "fintech",
        "헬스케어": "healthcare", "의료": "healthcare", "병원": "healthcare",
        "제조": "manufacturing", "공장": "manufacturing",
        "로봇": "robotics", "로보틱스": "robotics",
        "블록체인": "crypto", "크립토": "crypto", "웹3": "crypto", "web3": "crypto",
        "스테이블코인": "stablecoin", "defi": "stablecoin",
        "국방": "defense", "방위": "defense", "군사": "defense",
        "우주": "space", "항공": "space",
        "기후": "climate", "환경": "climate", "에너지": "climate",
        "교육": "education", "에듀테크": "education",
        "부동산": "proptech", "프롭테크": "proptech",
        "에이전시": "agency", "마케팅": "agency",
    }

    user_words = []  # type: List[str]
    for w in raw_text.split():
        w = w.strip(".,!?~()[]{}\"'")
        if w and w not in stopwords and len(w) > 0:
            # 동의어 변환
            mapped = synonyms.get(w, w)
            user_words.append(mapped)
    user_text = " ".join(user_words)

    scores = []  # type: List[Dict]
    for cat in cats:
        score = 0.0
        # Keyword matching from parsed keywords
        for kw in cat.get("keywords", []):
            kw_lower = kw.lower()
            if kw_lower in user_text:
                score += 1.0
            # 동의어로 매핑된 키워드도 체크
            mapped_kw = synonyms.get(kw_lower, kw_lower)
            if mapped_kw != kw_lower and mapped_kw in user_text:
                score += 1.0
        # Bonus for matching in category text
        cat_text = (cat.get("description", "") + " " + cat.get("founder_profile", "") + " " + cat.get("subtitle", "") + " " + cat.get("name", "")).lower()
        for word in user_words:
            if len(word) > 1 and word in cat_text:
                score += 0.5
        scores.append({
            "category": cat,
            "score": score,
        })

    scores.sort(key=lambda x: x["score"], reverse=True)

    # Return top 3
    matches = []  # type: List[Dict]
    for item in scores[:3]:
        cat = item["category"]
        matches.append({
            "id": cat["id"],
            "name": cat["name"],
            "subtitle": cat["subtitle"],
            "source": cat.get("source", ""),
            "match_score": round(item["score"], 1),
            "why_now": cat.get("why_now", ""),
            "founder_profile": cat.get("founder_profile", ""),
            "korea_market": cat.get("korea_market", ""),
        })

    return {
        "background": background,
        "interests": interests,
        "matches": matches,
    }


def format_list(categories):
    # type: (List[Dict]) -> str
    """카테고리 목록을 보기 좋게 포맷."""
    lines = [
        "🌅 창업 아이디어 데이터베이스 (YC RFS + a16z Big Ideas)",
        "=" * 55,
        "  총 %d개 아이디어" % len(categories),
        "",
    ]
    current_source = None
    for cat in categories:
        src = cat.get("source", "")
        if src != current_source:
            current_source = src
            lines.append("  [%s]" % src)
        lines.append("  %d. %s" % (cat['id'], cat['name']))
        lines.append("     %s" % cat['subtitle'])
        lines.append("")
    lines.append("상세 보기: raon.sh idea detail <번호>")
    lines.append("필터: raon.sh idea list --source yc | --source a16z")
    lines.append("       raon.sh idea list --season \"Spring 2026\"")
    return "\n".join(lines)


def format_detail(cat):
    # type: (Dict) -> str
    """카테고리 상세 정보를 보기 좋게 포맷."""
    lines = [
        "🌅 [%d] %s" % (cat['id'], cat['name']),
        "   %s" % cat['subtitle'],
        "   📎 %s" % cat.get("source", "N/A"),
        "",
        "📋 설명: %s" % cat.get('description', 'N/A'),
        "",
        "⏰ 왜 지금인지:",
        cat.get("why_now", "N/A"),
        "",
        "👤 적합한 창업자: %s" % cat.get('founder_profile', 'N/A'),
        "",
        "🇰🇷 한국 시장 적용:",
        cat.get("korea_market", "N/A"),
    ]
    if cat.get("keywords"):
        lines.append("")
        lines.append("🏷️ 키워드: %s" % ", ".join(cat["keywords"]))
    return "\n".join(lines)


def format_suggest(result):
    # type: (Dict) -> str
    """추천 결과를 보기 좋게 포맷."""
    if "error" in result:
        return "❌ %s" % result['error']
    
    lines = [
        "🌅 라온의 YC RFS & a16z 기반 창업 아이디어 추천",
        "=" * 55,
        "배경: %s" % result['background'],
        "관심사: %s" % result['interests'],
        "",
    ]
    medals = ["🥇", "🥈", "🥉"]
    for i, match in enumerate(result.get("matches", [])):
        lines.append("%s %s (매칭: %s) [%s]" % (medals[i], match['name'], match['match_score'], match.get('source', '')))
        lines.append("   %s" % match['subtitle'])
        if match.get("founder_profile"):
            lines.append("   👤 %s" % match['founder_profile'])
        if match.get("korea_market"):
            lines.append("   🇰🇷 %s..." % match['korea_market'][:100])
        lines.append("")
    
    return "\n".join(lines)


def cli_main(args=None):
    # type: (Optional[List[str]]) -> None
    """CLI 엔트리포인트."""
    import argparse
    parser = argparse.ArgumentParser(description="YC RFS & a16z 기반 창업 아이디어")
    sub = parser.add_subparsers(dest="command")

    list_p = sub.add_parser("list", help="전체 목록")
    list_p.add_argument("--source", "-s", default=None, help="소스 필터 (yc / a16z)")
    list_p.add_argument("--season", default=None, help="시즌 필터 (예: 'Spring 2026')")

    detail_p = sub.add_parser("detail", help="카테고리 상세")
    detail_p.add_argument("number", type=int, help="카테고리 번호")

    suggest_p = sub.add_parser("suggest", help="아이디어 추천")
    suggest_p.add_argument("--background", "-b", default="", help="사용자 배경")
    suggest_p.add_argument("--interests", "-i", default="", help="관심 분야")
    suggest_p.add_argument("--json", action="store_true", help="JSON 출력")

    parsed = parser.parse_args(args)

    if parsed.command == "list":
        cats = list_categories(source=parsed.source, season=parsed.season)
        if not cats:
            print("❌ 조건에 맞는 아이디어가 없습니다.", file=sys.stderr)
            sys.exit(1)
        print(format_list(cats))

    elif parsed.command == "detail":
        cat = get_category_detail(parsed.number)
        if not cat:
            print("❌ 카테고리 %d을 찾을 수 없습니다." % parsed.number, file=sys.stderr)
            sys.exit(1)
        print(format_detail(cat))

    elif parsed.command == "suggest":
        bg = parsed.background
        interests = parsed.interests
        if not bg and not interests:
            # Interactive
            bg = input("🗣️ 배경 (경력/전공): ").strip()
            interests = input("🗣️ 관심 분야: ").strip()
        result = suggest_ideas(bg, interests)
        if getattr(parsed, "json", False):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_suggest(result))
    else:
        parser.print_help()


if __name__ == "__main__":
    cli_main()
