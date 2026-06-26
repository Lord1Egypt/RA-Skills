#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Web Fetcher - 웹 콘텐츠 수집 및 처리 엔진
OpenClaw Web Fetcher - Core web content collection and processing engine

이 스크립트는 다양한 방식으로 웹 콘텐츠를 수집하고 구조화합니다:
- 단일 URL 페칭
- Google 검색 결과 크롤링
- 배치 모드에서 여러 URL 처리
- 사전설정된 프리셋 실행
- 자동 태깅 및 메타데이터 추가
"""

import argparse
import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup, NavigableString, Tag


# ============================================================================
# 상수 및 설정 (Constants and Configuration)
# ============================================================================

# 기본 사용자 에이전트
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

# 도메인별 마지막 요청 시간 (Rate limiting)
DOMAIN_LAST_REQUEST = {}
REQUEST_DELAY = 1.0  # 초 (Seconds between requests to same domain)

# 타임아웃 설정
REQUEST_TIMEOUT = 10  # 초 (Seconds)

# robots.txt 캐시
ROBOTS_CACHE = {}


# ============================================================================
# 유틸리티 함수 (Utility Functions)
# ============================================================================


def get_domain(url: str) -> str:
    """URL에서 도메인 추출 (Extract domain from URL)"""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def check_robots_txt(url: str) -> bool:
    """robots.txt 확인 (Check if URL is allowed by robots.txt)"""
    try:
        domain = get_domain(url)

        if domain not in ROBOTS_CACHE:
            rp = RobotFileParser()
            robots_url = urljoin(domain, '/robots.txt')
            rp.set_url(robots_url)
            try:
                rp.read()
                ROBOTS_CACHE[domain] = rp
            except Exception:
                # robots.txt를 읽을 수 없으면 허용으로 처리
                ROBOTS_CACHE[domain] = None
                return True

        robot_parser = ROBOTS_CACHE[domain]
        if robot_parser is None:
            return True

        return robot_parser.can_fetch(USER_AGENT, url)
    except Exception as e:
        print(f"[경고] robots.txt 확인 중 오류: {e}")
        return True  # 오류 발생 시 허용


def rate_limit(url: str) -> None:
    """도메인별 레이트 제한 적용 (Apply rate limiting per domain)"""
    domain = get_domain(url)

    if domain in DOMAIN_LAST_REQUEST:
        elapsed = time.time() - DOMAIN_LAST_REQUEST[domain]
        if elapsed < REQUEST_DELAY:
            time.sleep(REQUEST_DELAY - elapsed)

    DOMAIN_LAST_REQUEST[domain] = time.time()


def extract_structured_data(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """페이지에서 구조화된 데이터 추출 (Extract structured data from page)"""
    extracted = {
        "tables": [],
        "lists": [],
        "links": []
    }

    # 테이블 추출
    for table in soup.find_all('table', limit=5):
        try:
            rows = []
            for tr in table.find_all('tr', limit=10):
                cells = []
                for td in tr.find_all(['td', 'th']):
                    cells.append(td.get_text(strip=True))
                if cells:
                    rows.append(cells)
            if rows:
                extracted["tables"].append(rows)
        except Exception:
            continue

    # 목록 추출
    for ul_ol in soup.find_all(['ul', 'ol'], limit=3):
        try:
            items = []
            for li in ul_ol.find_all('li', limit=20):
                text = li.get_text(strip=True)
                if text:
                    items.append(text)
            if items:
                extracted["lists"].append(items)
        except Exception:
            continue

    # 링크 추출 (상위 10개)
    for a in soup.find_all('a', limit=10):
        try:
            href = a.get('href', '')
            if href:
                # 상대 URL을 절대 URL로 변환
                absolute_url = urljoin(url, href)
                link_text = a.get_text(strip=True)
                extracted["links"].append({
                    "text": link_text[:100],
                    "url": absolute_url
                })
        except Exception:
            continue

    return extracted


def extract_content(
    soup: BeautifulSoup,
    css_selector: Optional[str] = None
) -> str:
    """
    HTML에서 텍스트 콘텐츠 추출
    Extract text content from HTML (optionally using CSS selector)
    """
    try:
        if css_selector:
            # CSS 선택자 사용
            element = soup.select_one(css_selector)
            if element:
                return element.get_text(separator=" ", strip=True)[:5000]

        # 기본: 스크립트와 스타일 제거 후 텍스트 추출
        for script in soup(['script', 'style']):
            script.decompose()

        # main, article, body 등의 주요 콘텐츠 영역 찾기
        for selector in ['main', 'article', '[role="main"]', '.content', '#content']:
            element = soup.select_one(selector)
            if element:
                return element.get_text(separator=" ", strip=True)[:5000]

        # 폴백: 전체 body 텍스트
        body = soup.find('body')
        if body:
            return body.get_text(separator=" ", strip=True)[:5000]

        return soup.get_text(separator=" ", strip=True)[:5000]

    except Exception as e:
        return f"콘텐츠 추출 실패: {str(e)}"


def auto_tag(content: str, title: str, url: str) -> List[str]:
    """
    페이지 콘텐츠를 분석하여 자동 태깅
    Analyze page content and auto-tag
    """
    tags = set()

    # URL 기반 태그
    if 'github.com' in url:
        tags.add('github')
    if 'arxiv.org' in url:
        tags.add('academic')
    if 'wikipedia.org' in url:
        tags.add('reference')
    if 'stackoverflow.com' in url:
        tags.add('q-and-a')

    # 콘텐츠 기반 태그 (간단한 키워드 분석)
    content_lower = (content + " " + title).lower()

    keyword_tags = {
        'python': ['python', 'django', 'flask', 'fastapi'],
        'javascript': ['javascript', 'react', 'vue', 'node.js', 'typescript'],
        'machine-learning': ['machine learning', 'neural', 'tensorflow', 'pytorch', 'ai', 'deep learning'],
        'web-development': ['html', 'css', 'web development', 'frontend', 'backend'],
        'database': ['database', 'sql', 'mongodb', 'postgresql', 'redis'],
        'devops': ['docker', 'kubernetes', 'devops', 'ci/cd', 'deployment'],
        'security': ['security', 'encryption', 'password', 'auth', 'vulnerability'],
        'tutorial': ['tutorial', 'guide', 'how to', 'step by step'],
        'documentation': ['documentation', 'docs', 'api reference'],
        'news': ['news', 'announcement', 'update', 'release'],
    }

    for tag, keywords in keyword_tags.items():
        if any(keyword in content_lower for keyword in keywords):
            tags.add(tag)

    return sorted(list(tags))


# ============================================================================
# 페칭 함수 (Fetching Functions)
# ============================================================================


def fetch_url(
    url: str,
    css_selector: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    단일 URL 페칭
    Fetch a single URL
    """
    try:
        # robots.txt 확인
        if not check_robots_txt(url):
            return {
                "url": url,
                "error": "robots.txt에 의해 차단됨 (Blocked by robots.txt)",
                "fetched_at": datetime.now(timezone.utc).isoformat()
            }

        # 레이트 제한 적용
        rate_limit(url)

        # 요청 수행
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True
        )
        response.raise_for_status()

        # HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')

        # 제목 추출
        title = ""
        if soup.title:
            title = soup.title.string or ""
        elif soup.find('h1'):
            title = soup.find('h1').get_text(strip=True)

        # 콘텐츠 추출
        content = extract_content(soup, css_selector)

        # 구조화된 데이터 추출
        extracted_data = extract_structured_data(soup, url)

        # 자동 태깅
        tags = auto_tag(content, title, url)

        return {
            "url": url,
            "title": title,
            "content": content,
            "extracted_data": extracted_data,
            "tags": tags,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "status_code": response.status_code
        }

    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "error": f"요청 실패: {str(e)}",
            "fetched_at": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "url": url,
            "error": f"처리 중 오류: {str(e)}",
            "fetched_at": datetime.now(timezone.utc).isoformat()
        }


def search_google(query: str) -> Optional[Dict[str, Any]]:
    """
    Google 검색 결과 페칭
    Fetch Google search results
    """
    try:
        # Google 검색 URL 구성
        search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"

        # robots.txt 확인
        if not check_robots_txt(search_url):
            return {
                "query": query,
                "error": "robots.txt에 의해 차단됨",
                "fetched_at": datetime.now(timezone.utc).isoformat()
            }

        # 레이트 제한 적용
        rate_limit(search_url)

        # 요청 수행
        response = requests.get(
            search_url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

        # HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')

        results = []

        # 검색 결과 추출 (Google의 구조에 따라 조정 필요)
        for result in soup.find_all('div', class_='g', limit=10):
            try:
                # 링크와 제목 추출
                link_elem = result.find('a', href=True)
                if not link_elem:
                    continue

                url = link_elem.get('href', '')
                title = link_elem.get_text(strip=True)

                # 스니펫 추출
                snippet = ""
                snippet_elem = result.find('span', class_='st')
                if snippet_elem:
                    snippet = snippet_elem.get_text(strip=True)

                results.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet
                })
            except Exception:
                continue

        return {
            "query": query,
            "search_url": search_url,
            "results": results,
            "result_count": len(results),
            "fetched_at": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        return {
            "query": query,
            "error": f"검색 실패: {str(e)}",
            "fetched_at": datetime.now(timezone.utc).isoformat()
        }


def batch_fetch(file_path: str, delay: float = 1.0) -> Dict[str, Any]:
    """
    파일에서 URL 읽어서 배치 페칭
    Read URLs from file and fetch in batch
    """
    pages = []
    success_count = 0
    failed_count = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except Exception as e:
        return {
            "error": f"파일 읽기 실패: {str(e)}",
            "pages": [],
            "summary": {"total_pages": 0, "success": 0, "failed": 0}
        }

    for idx, url in enumerate(urls):
        print(f"[{idx+1}/{len(urls)}] 페칭 중: {url}")

        result = fetch_url(url)
        if result:
            pages.append(result)
            if "error" not in result:
                success_count += 1
            else:
                failed_count += 1
        else:
            failed_count += 1

        # 다음 URL 전에 지연
        if idx < len(urls) - 1:
            time.sleep(delay)

    return {
        "metadata": {
            "collection_id": str(uuid.uuid4()),
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "source_file": file_path,
            "method": "python_fetcher",
            "collector": "web_browser_toolkit",
            "version": "1.0"
        },
        "pages": pages,
        "summary": {
            "total_pages": len(urls),
            "success": success_count,
            "failed": failed_count
        }
    }


def load_preset(preset_name: str) -> Optional[Dict[str, Any]]:
    """
    사전설정 파일에서 프리셋 로드
    Load preset from references/aviation_presets.json
    """
    try:
        preset_path = Path(__file__).parent.parent / "references" / "aviation_presets.json"

        if not preset_path.exists():
            return {
                "error": f"프리셋 파일을 찾을 수 없음: {preset_path}"
            }

        with open(preset_path, 'r', encoding='utf-8') as f:
            presets = json.load(f)

        if preset_name not in presets:
            available = list(presets.keys())
            return {
                "error": f"프리셋 '{preset_name}'을 찾을 수 없음",
                "available_presets": available
            }

        preset = presets[preset_name]
        return preset

    except Exception as e:
        return {
            "error": f"프리셋 로드 실패: {str(e)}"
        }


def execute_preset(preset_name: str) -> Dict[str, Any]:
    """
    사전설정 실행
    Execute a preset
    """
    preset = load_preset(preset_name)

    if "error" in preset:
        return preset

    # 프리셋의 URLs 또는 queries 처리
    pages = []
    success_count = 0
    failed_count = 0

    urls = preset.get("urls", [])
    queries = preset.get("queries", [])

    for url in urls:
        result = fetch_url(url)
        if result:
            pages.append(result)
            if "error" not in result:
                success_count += 1
            else:
                failed_count += 1
        time.sleep(REQUEST_DELAY)

    for query in queries:
        result = search_google(query)
        if result:
            pages.append(result)
            if "error" not in result:
                success_count += 1
            else:
                failed_count += 1
        time.sleep(REQUEST_DELAY)

    return {
        "metadata": {
            "collection_id": str(uuid.uuid4()),
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "preset_name": preset_name,
            "method": "python_fetcher",
            "collector": "web_browser_toolkit",
            "version": "1.0"
        },
        "pages": pages,
        "summary": {
            "total_pages": len(urls) + len(queries),
            "success": success_count,
            "failed": failed_count,
            "preset_description": preset.get("description", "")
        }
    }


def structurize_json(input_file: str, output_file: Optional[str] = None) -> Dict[str, Any]:
    """
    수집된 JSON에 태그/메타데이터 추가
    Add tags and metadata to raw collected JSON
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 메타데이터 확인/업데이트
        if "metadata" not in data:
            data["metadata"] = {
                "collection_id": str(uuid.uuid4()),
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "method": "python_fetcher",
                "collector": "web_browser_toolkit",
                "version": "1.0"
            }

        # 각 페이지에 태그 추가
        if "pages" in data:
            for page in data["pages"]:
                if "tags" not in page:
                    content = page.get("content", "")
                    title = page.get("title", "")
                    url = page.get("url", "")
                    page["tags"] = auto_tag(content, title, url)

                # fetched_at 확인
                if "fetched_at" not in page:
                    page["fetched_at"] = datetime.now(timezone.utc).isoformat()

        # 요약 통계 계산
        if "pages" in data and "summary" not in data:
            total = len(data["pages"])
            success = sum(1 for p in data["pages"] if "error" not in p)
            data["summary"] = {
                "total_pages": total,
                "success": success,
                "failed": total - success
            }

        # 출력 파일에 저장
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"구조화된 데이터 저장됨: {output_file}")

        return data

    except Exception as e:
        return {
            "error": f"구조화 실패: {str(e)}"
        }


# ============================================================================
# 메인 함수 (Main Function)
# ============================================================================


def main():
    """메인 엔트리 포인트 (Main entry point)"""
    parser = argparse.ArgumentParser(
        description="OpenClaw Web Fetcher - 웹 콘텐츠 수집 엔진",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python fetcher.py fetch "https://example.com" -s "article"
  python fetcher.py search "python programming"
  python fetcher.py batch urls.txt
  python fetcher.py preset aviation
  python fetcher.py structurize data.json -o structured.json
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='실행할 명령 (Command to execute)')

    # fetch 서브커맨드
    fetch_parser = subparsers.add_parser('fetch', help='단일 URL 페칭 (Fetch single URL)')
    fetch_parser.add_argument('url', help='페칭할 URL (URL to fetch)')
    fetch_parser.add_argument('-s', '--selector', help='CSS 선택자 (CSS selector for extraction)')
    fetch_parser.add_argument('-o', '--output', help='출력 파일 (Output JSON file)')

    # search 서브커맨드
    search_parser = subparsers.add_parser('search', help='Google 검색 (Search Google)')
    search_parser.add_argument('query', help='검색 쿼리 (Search query)')
    search_parser.add_argument('-o', '--output', help='출력 파일 (Output JSON file)')

    # batch 서브커맨드
    batch_parser = subparsers.add_parser('batch', help='배치 페칭 (Batch fetch from file)')
    batch_parser.add_argument('file', help='URL 목록 파일 (Text file with URLs)')
    batch_parser.add_argument('-d', '--delay', type=float, default=1.0, help='요청 간 지연 (Delay between requests)')
    batch_parser.add_argument('-o', '--output', help='출력 파일 (Output JSON file)')

    # preset 서브커맨드
    preset_parser = subparsers.add_parser('preset', help='프리셋 실행 (Execute preset)')
    preset_parser.add_argument('name', help='프리셋 이름 (Preset name)')
    preset_parser.add_argument('-o', '--output', help='출력 파일 (Output JSON file)')

    # structurize 서브커맨드
    struct_parser = subparsers.add_parser('structurize', help='JSON 구조화 (Structurize JSON)')
    struct_parser.add_argument('file', help='입력 JSON 파일 (Input JSON file)')
    struct_parser.add_argument('-o', '--output', help='출력 파일 (Output JSON file)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    result = None

    # 커맨드별 실행
    if args.command == 'fetch':
        result = fetch_url(args.url, args.selector)
        if result:
            result = {
                "metadata": {
                    "collection_id": str(uuid.uuid4()),
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "source_url": args.url,
                    "method": "python_fetcher",
                    "collector": "web_browser_toolkit",
                    "version": "1.0"
                },
                "pages": [result] if result else [],
                "summary": {
                    "total_pages": 1,
                    "success": 0 if "error" in result else 1,
                    "failed": 1 if "error" in result else 0
                }
            }

    elif args.command == 'search':
        result = search_google(args.query)
        if result:
            result = {
                "metadata": {
                    "collection_id": str(uuid.uuid4()),
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "query": args.query,
                    "method": "python_fetcher",
                    "collector": "web_browser_toolkit",
                    "version": "1.0"
                },
                "pages": [result] if result else [],
                "summary": {
                    "total_pages": 1,
                    "success": 0 if "error" in result else 1,
                    "failed": 1 if "error" in result else 0
                }
            }

    elif args.command == 'batch':
        result = batch_fetch(args.file, args.delay)

    elif args.command == 'preset':
        result = execute_preset(args.name)

    elif args.command == 'structurize':
        output = args.output or args.file.replace('.json', '_structured.json')
        result = structurize_json(args.file, output)

    # 결과 출력
    if result:
        # 파일로 저장
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"결과 저장됨: {args.output}")

        # 콘솔에 출력
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
