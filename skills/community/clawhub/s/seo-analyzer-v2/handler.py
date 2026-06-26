"""SEO Analyzer - Analyze webpage SEO"""
import requests, re, json

def analyze_seo(url: str) -> dict:
    try:
        resp = requests.get(url, timeout=10)
        html = resp.text
        title = re.findall(r'<title>([^<]+)', html)
        desc = re.findall(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html)
        h1 = re.findall(r'<h1[^>]*>([^<]+)', html, re.I)
        
        score = 0
        issues = []
        if title: score += 30
        else: issues.append("Missing title tag")
        if desc: score += 30
        else: issues.append("Missing meta description")
        if h1: score += 20
        else: issues.append("Missing H1 tag")
        if len(html) > 500: score += 20
        
        return {"url": url, "score": score, "title": title[0] if title else None,
                "description": desc[0] if desc else None, "h1_count": len(h1),
                "issues": issues, "recommendations": ["Add keywords to title", "Add meta description"]}
    except Exception as e:
        return {"error": str(e)}

def handle(input_text: str, user_id: str = "default") -> dict:
    url = re.search(r'https?://[^\s]+', input_text)
    if not url: return {"error": "Please provide a URL"}
    return analyze_seo(url.group(0))

if __name__ == "__main__":
    import sys
    print(json.dumps(handle(sys.argv[1] if len(sys.argv) > 1 else "", "cli"), indent=2))
