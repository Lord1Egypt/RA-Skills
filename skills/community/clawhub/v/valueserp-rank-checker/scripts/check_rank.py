#!/usr/bin/env python3
"""
Checks the Google ranking position of a keyword for a given domain using ValueSERP API.
Usage: python check_rank.py "<keyword>" <domain> [--pages 10]
Requires: VALUESERP_API_KEY environment variable
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode())


def check_rank(keyword: str, domain: str, api_key: str, gl: str = "co", hl: str = "es", max_pages: int = 10):
    base_url = "https://api.valueserp.com/search"
    results_per_page = 10

    for page in range(1, max_pages + 1):
        params = {
            "api_key": api_key,
            "q": keyword,
            "gl": gl,
            "hl": hl,
            "num": str(results_per_page),
            "page": str(page),
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"

        try:
            data = fetch_json(url)
        except Exception as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
            sys.exit(1)

        if not data.get("request_info", {}).get("success", True):
            msg = data.get("request_info", {}).get("message", "Unknown error")
            print(json.dumps({"error": msg}, ensure_ascii=False))
            sys.exit(1)

        organic_results = data.get("organic_results", [])
        if not organic_results:
            break

        for result in organic_results:
            result_domain = result.get("domain", "")
            result_url = result.get("link", "")
            position_in_page = result.get("position", 0)

            clean_target = domain.lower().replace("www.", "")
            clean_result = result_domain.lower().replace("www.", "")

            if clean_target in clean_result or clean_result in clean_target:
                global_position = (page - 1) * results_per_page + position_in_page
                print(json.dumps({
                    "found": True,
                    "keyword": keyword,
                    "domain": domain,
                    "position": global_position,
                    "page": page,
                    "position_in_page": position_in_page,
                    "url": result_url,
                    "title": result.get("title", ""),
                    "gl": gl,
                    "hl": hl,
                }, ensure_ascii=False, indent=2))
                return

    print(json.dumps({
        "found": False,
        "keyword": keyword,
        "domain": domain,
        "pages_checked": max_pages,
        "message": f"No se encontró '{domain}' en las primeras {max_pages * results_per_page} posiciones.",
    }, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", help="Palabra clave a buscar")
    parser.add_argument("domain", help="Dominio objetivo (ej: vajillascorona.com.co)")
    parser.add_argument("--gl", default="co", help="País Google (default: co)")
    parser.add_argument("--hl", default="es", help="Idioma (default: es)")
    parser.add_argument("--pages", type=int, default=10, help="Páginas a revisar, 10 resultados c/u (default: 10 = top 100)")
    args = parser.parse_args()

    api_key = os.environ.get("VALUESERP_API_KEY")
    if not api_key:
        print(json.dumps({"error": "VALUESERP_API_KEY no está definida en el entorno."}))
        sys.exit(1)

    check_rank(args.keyword, args.domain, api_key, args.gl, args.hl, args.pages)


if __name__ == "__main__":
    main()
