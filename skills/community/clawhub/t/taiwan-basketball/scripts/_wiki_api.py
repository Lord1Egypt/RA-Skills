"""
台灣籃球維基館 (wikibasketball) API 模組
使用 Scrapling StealthyFetcher 繞過 Anubis 防護機制

主要用途：
1. 球員經歷（跨聯盟球隊歷史）
2. 球員獎項紀錄
3. T1 聯盟歷史數據（已消失聯盟）
4. 本土球員詳細資料

洋將可能不在維基館，以本土球員為主。
"""

import json
import re
import urllib.parse
from typing import Any

WIKI_BASE = 'https://wikibasketball.dils.tku.edu.tw/wiki/index.php'

# Scrapling venv 路徑（共用 CPBL skill 的 venv）
SCRAPLING_VENV = '/home/ichen/.openclaw/workspace/skills/cpbl/.venv'


def _get_stealthy_fetcher():
    """取得 Scrapling StealthyFetcher（需要 CPBL skill 的 venv）"""
    import sys
    import os
    venv_lib = f'{SCRAPLING_VENV}/lib'
    for d in os.listdir(venv_lib):
        if d.startswith('python3.'):
            site_packages = f'{venv_lib}/{d}/site-packages'
            if os.path.isdir(site_packages) and site_packages not in sys.path:
                sys.path.insert(0, site_packages)
            break
    from scrapling.fetchers import StealthyFetcher
    return StealthyFetcher


def _wiki_url(title: str) -> str:
    """建構維基館 URL"""
    encoded = urllib.parse.quote(title)
    return f'{WIKI_BASE}?title={encoded}'


def _parse_experience(dl_element) -> list[dict]:
    """解析經歷區塊的 <dl><dd><ul><li> 結構

    格式：聯盟球隊（年份～年份）或 聯盟球隊A→球隊B（年份～）
    """
    results = []
    if not dl_element:
        return results

    for li in dl_element.find_all('li'):
        text = li.get_text(strip=True)
        if not text:
            continue

        org_team = ''
        start_year = 0
        end_year = 0

        # 格式1：聯盟+球隊（YYYY年～YYYY年）
        m = re.match(r'(.+?)（(\d{4})年～(\d{4})年）', text)
        if m:
            org_team = m.group(1).strip()
            start_year = int(m.group(2))
            end_year = int(m.group(3))
        else:
            # 格式2：聯盟+球隊（YYYY年）只有一年
            m = re.match(r'(.+?)（(\d{4})年）', text)
            if m:
                org_team = m.group(1).strip()
                start_year = int(m.group(2))
                end_year = start_year
            else:
                # 格式3：聯盟+球隊（YYYY年～）無結束年份，代表仍在效力
                m = re.match(r'(.+?)（(\d{4})年～）', text)
                if m:
                    org_team = m.group(1).strip()
                    start_year = int(m.group(2))
                    end_year = start_year  # 仍在效力
                else:
                    continue

        # 分離聯盟和球隊
        league_prefixes = [
            'P. LEAGUE+', '台灣職業籃球大聯盟', 'T1聯盟',
            '超級籃球聯賽', 'NBA', 'NCAA', 'CBA',
            '東亞超級聯賽', '丹麥籃球聯賽', '義大利籃球乙級聯賽',
            '加拿大精英籃球聯賽', '美國職籃發展聯盟', '美國職籃',
            '亞洲俱樂部冠軍聯賽',
        ]

        league = ''
        team = org_team
        for prefix in sorted(league_prefixes, key=len, reverse=True):
            if org_team.startswith(prefix):
                league = prefix
                team = org_team[len(prefix):].strip()
                break

        # 處理球隊更名：A→B
        teams = [t.strip() for t in team.split('→')] if '→' in team else [team]

        results.append({
            'league': league,
            'team': team,
            'teams': teams,
            'start_year': start_year,
            'end_year': end_year,
            'raw': text,
        })

    return results


def _parse_awards(content_div) -> list[str]:
    """解析特殊事蹟/獎項"""
    awards = []

    # 找「特殊事蹟」h2
    for heading in content_div.find_all('h2'):
        span = heading.find('span', class_='mw-headline')
        if span and ('特殊事蹟' in span.get_text() or '獎項' in span.get_text()):
            dl = heading.find_next_sibling('dl')
            if dl:
                for dd in dl.find_all('dd'):
                    text = dd.get_text(strip=True)
                    if text and ('年度' in text or '王' in text or '獎' in text or '最佳' in text or '入選' in text):
                        awards.append(text)
            break

    return awards


def get_player_wiki(name: str) -> dict[str, Any]:
    """從台灣籃球維基館抓取球員資料

    Returns:
        dict with keys: name, found, experience, awards, wiki_url
    """
    StealthyFetcher = _get_stealthy_fetcher()
    result: dict[str, Any] = {
        'name': name,
        'found': False,
        'experience': [],
        'awards': [],
        'wiki_url': _wiki_url(name),
        'league': 'wiki',
    }

    # 嘗試直接訪問球員頁面
    try:
        page = StealthyFetcher.fetch(_wiki_url(name), headless=True, wait=10000)
    except Exception as e:
        result['error'] = f'Failed to load page: {e}'
        return result

    content_div = page.css('#mw-content-text')
    if not content_div:
        return result

    text = content_div[0].get_all_text() if content_div else ''

    # 如果頁面不存在，嘗試搜尋
    if '沒有內容' in text or '此頁目前沒有內容' in text:
        try:
            search_page = StealthyFetcher.fetch(
                f'{WIKI_BASE}?title=特殊:搜尋&search={urllib.parse.quote(name)}',
                headless=True,
                wait=10000,
            )
        except Exception:
            return result

        search_text = ''
        search_content = search_page.css('#mw-content-text')
        if search_content:
            search_text = search_content[0].get_all_text()

        # 嘗試找到匹配的結果
        from bs4 import BeautifulSoup
        try:
            soup = BeautifulSoup(page.get_all_text(), 'lxml')
        except Exception:
            return result

        for link in soup.find_all('a', href=True):
            href = link['href']
            title_text = link.get_text(strip=True)
            if name in title_text and '/wiki/' in href:
                full_url = f'https://wikibasketball.dils.tku.edu.tw{href}' if href.startswith('/') else href
                try:
                    page = StealthyFetcher.fetch(full_url, headless=True, wait=10000)
                except Exception:
                    continue
                result['wiki_url'] = full_url
                result['name'] = title_text
                break
        else:
            return result

    result['found'] = True

    # 用 BeautifulSoup 解析 HTML
    from bs4 import BeautifulSoup
    # page.get() returns the HTML of the first matched element
    html_content = page.css('#mw-content-text').get() or ''
    soup = BeautifulSoup(html_content, 'lxml')
    content = soup.find('div', id='mw-content-text') if soup.find('div', id='mw-content-text') else soup

    # 1. 解析經歷
    for heading in content.find_all('h2'):
        span = heading.find('span', class_='mw-headline')
        if span and '經歷' in span.get_text() and '籃球' not in span.get_text():
            dl = heading.find_next_sibling('dl')
            if dl:
                result['experience'] = _parse_experience(dl)
            break

    # 2. 解析獎項
    result['awards'] = _parse_awards(content)

    return result


def search_player_wiki(name: str, limit: int = 10) -> list[dict]:
    """搜尋台灣籃球維基館的球員頁面

    Returns:
        list of [{title, url, snippet}]
    """
    StealthyFetcher = _get_stealthy_fetcher()
    results = []

    page = StealthyFetcher.fetch(
        f'{WIKI_BASE}?title=特殊:搜尋&search={urllib.parse.quote(name)}',
        headless=True,
        wait=10000,
    )

    from bs4 import BeautifulSoup
    # Use the full page HTML for parsing
    full_html = page.get() if hasattr(page, 'get') else ''
    soup = BeautifulSoup(full_html, 'lxml')
    content = soup.find('div', class_='searchresults')

    if not content:
        # 嘗試另一種結構
        content = soup.find('div', id='mw-content-text')

    if content:
        for link in content.find_all('a', href=True):
            href = link['href']
            title = link.get_text(strip=True)
            if '/wiki/' in href and title and name in title:
                full_url = f'https://wikibasketball.dils.tku.edu.tw{href}' if href.startswith('/') else href
                snippet = ''
                # 找摘要
                parent = link.find_parent('div')
                if parent:
                    snippet = parent.get_text(strip=True)[:200]
                results.append({
                    'title': title,
                    'url': full_url,
                    'snippet': snippet,
                })
                if len(results) >= limit:
                    break

    return results


if __name__ == '__main__':
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else '高柏鎧'
    data = get_player_wiki(name)
    print(json.dumps(data, ensure_ascii=False, indent=2))