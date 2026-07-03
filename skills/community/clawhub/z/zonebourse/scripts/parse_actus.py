#!/usr/bin/env python3
"""Récupère les liens d'actualités depuis la page cours ZoneBourse.

Trois sections (IDs sur la page cours) :
  - allNews       → Actualités (toutes)
  - news_headlines → Analyses / Opinions
  - newsrecobroker → Recommandations des analystes

Les liens article ont un hash hex de 10-12 caractères à la fin :
  /actualite-bourse/titre-ce7f5adfde81f32c
"""

import subprocess, json, re, sys


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

# Mapping section_key -> page element ID
SECTION_IDS = {
    "actualites": "allNews",
    "analyses": "news_headlines",
    "recommandations": "newsrecobroker",
}


def is_article_link(url: str) -> bool:
    """Les liens article ont un hash hex de 16 caractères à la fin du slug."""
    return bool(re.search(r'/[a-z0-9_-]+-[a-f0-9]{16}(?:/|$)', url))


def fetch_actus(slug: str, limit: int = 10) -> dict:
    """Récupère les liens d'actualité depuis les 3 sections de la page cours."""
    url = f"https://www.zonebourse.com/cours/action/{slug}/"
    
    result = subprocess.run(CURL_ARGS + [url], capture_output=True, text=True, timeout=20)
    html = result.stdout

    results = {k: [] for k in SECTION_IDS}
    seen = set()

    for section_key, section_id in SECTION_IDS.items():
        idx = html.find(f'id="{section_id}"')
        if idx < 0:
            continue

        # allNews est un <span> data-collapse — la card est le parent
        # On prend 8000 chars à partir de l'ID pour couvrir la card entière
        section_html = html[idx:idx + 8000]

        # Extraire tous les liens actualite-bourse
        raw_links = re.findall(r'href="(/actualite-bourse/[^"]+)"', section_html)

        for link in raw_links:
            clean = link.split('?')[0]
            # Filtrer uniquement les liens article (avec hash hex)
            if not is_article_link(clean):
                continue
            if clean not in seen:
                seen.add(clean)
                results[section_key].append(f"https://www.zonebourse.com{clean}")
            if len(results[section_key]) >= limit:
                break

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parse_actus.py <slug> [limit]")
        sys.exit(1)
    
    slug = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    result = fetch_actus(slug, limit)
    print(json.dumps(result, indent=2, ensure_ascii=False))