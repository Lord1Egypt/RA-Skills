#!/usr/bin/env python3
"""Lit le contenu d'un article ZoneBourse.

Le contenu est dans une variable JavaScript `articleBody` (page HTML complète,
pas de rendu JS nécessaire). Les entités HTML sont échappées dans la page
et sont déséchappées ici.
"""

import subprocess, json, re, sys, html as html_lib
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent.resolve()
COOKIES_FILE = SCRIPT_DIR / "cookies.txt"


CURL_ARGS = [
    "curl", "-s",
    "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "-H", "Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "-H", "Accept-Encoding: gzip, deflate, br",
    "-H", "Connection: keep-alive",
    "-H", "Upgrade-Insecure-Requests: 1",
    "-H", "Sec-Fetch-Dest: document",
    "-H", "Sec-Fetch-Mode: navigate",
    "-H", "Sec-Fetch-Site: none",
    "-H", "Sec-Fetch-User: ?1",
    "-H", "Cache-Control: max-age=0",
    "--compressed",
]


def load_cookies(path: Path) -> str:
    """Construit le header Cookie depuis le fichier key=value."""
    if not path.exists():
        return ""
    cookies = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            cookies.append(line)
    return "; ".join(cookies)


def unescape(text: str) -> str:
    """Déséchappe les entités HTML (double-encoded dans le JSON ZoneBourse)."""
    text = text.replace("\\n", "\n")
    text = html_lib.unescape(text)  # 1st pass: &amp;amp; → &amp;
    text = html_lib.unescape(text)  # 2nd pass: &amp; → &
    return text


def fetch_article(url: str) -> dict:
    """Récupère titre + contenu complet d'un article ZoneBourse."""
    cookie_header = load_cookies(COOKIES_FILE)

    cmd = CURL_ARGS + ["-H", f"Cookie: {cookie_header}", url]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    html = result.stdout

    if result.returncode != 0 or len(html) < 200:
        return {"url": url, "titre": None, "contenu": None, "paywall": None, "error": "page inaccessible"}

    if "Access Denied" in html:
        return {"url": url, "titre": None, "contenu": None, "paywall": None, "error": "access_denied"}

    # Titre
    title_match = re.search(r"<title>([^<]+)</title>", html)
    titre = title_match.group(1).replace(" | Zonebourse", "").strip() if title_match else None

    # Date de publication — depuis <meta property="article:published_time">
    date_iso = None
    date_match = re.search(r'<meta property="article:published_time" content="([^"]+)"', html)
    if date_match:
        date_iso = date_match.group(1)[:10]  # "2026-05-18T16:37:52+02:00" → "2026-05-18"

    # Contenu principal — embedded dans articleBody (JS variable dans le HTML)
    article_match = re.search(r'"articleBody":\s*"([^"]+)"', html)
    if article_match:
        raw = article_match.group(1)
        contenu = unescape(raw)
        if len(contenu) > 100:
            return {
                "url": url,
                "titre": titre,
                "date": date_iso,
                "contenu": contenu[:10000],
                "paywall": False,
            }

    # Fallback : og:description (teaser)
    lead = None
    og_desc = re.search(r'<meta[^>]+og:description[^>]+content="([^"]+)"', html)
    if og_desc:
        raw = og_desc.group(1).strip()
        lead = unescape(raw)

    return {
        "url": url,
        "titre": titre,
        "date": date_iso,
        "contenu": lead[:2000] if lead else None,
        "paywall": True,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 read_article.py <url>")
        sys.exit(1)

    result = fetch_article(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))