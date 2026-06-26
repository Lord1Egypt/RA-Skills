#!/usr/bin/env python3
"""
06_robots.py - 抓取并解析 robots.txt
用法: python3 06_robots.py <domain_or_url> [--json]
自动尝试 https/http，解析 User-agent / Allow / Disallow / Sitemap / Crawl-delay
"""
import sys, json, re, requests
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
}

def fetch_robots(domain):
    """尝试 https 和 http 两种协议"""
    # 清理输入
    if not domain.startswith("http"):
        urls_to_try = [f"https://{domain}/robots.txt", f"http://{domain}/robots.txt"]
    else:
        parsed = urlparse(domain)
        base = f"{parsed.scheme}://{parsed.netloc}"
        urls_to_try = [f"{base}/robots.txt"]

    for url in urls_to_try:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
            return {
                "url": url,
                "final_url": r.url,
                "status_code": r.status_code,
                "content_type": r.headers.get("Content-Type", ""),
                "content_length": len(r.content),
                "text": r.text if r.status_code == 200 else None,
                "redirect_chain": [resp.url for resp in r.history] if r.history else [],
            }
        except requests.exceptions.SSLError:
            continue
        except Exception as e:
            last_error = str(e)

    return {"url": urls_to_try[0], "error": last_error if 'last_error' in dir() else "unknown"}

def parse_robots_txt(text):
    """解析 robots.txt，返回规则结构"""
    if not text:
        return {}

    rules = {}
    sitemaps = []
    current_agents = []
    crawl_delay = {}

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if ':' not in line:
            continue

        key, _, value = line.partition(':')
        key = key.strip().lower()
        value = value.strip()

        if key == 'user-agent':
            current_agents = [value] if value not in ('', ) else []
            for agent in current_agents:
                if agent not in rules:
                    rules[agent] = {"allow": [], "disallow": []}

        elif key == 'allow':
            for agent in current_agents:
                if agent in rules:
                    rules[agent]["allow"].append(value)

        elif key == 'disallow':
            for agent in current_agents:
                if agent in rules:
                    rules[agent]["disallow"].append(value)

        elif key == 'sitemap':
            sitemaps.append(value)

        elif key == 'crawl-delay':
            for agent in current_agents:
                try:
                    crawl_delay[agent] = float(value)
                except:
                    pass

    # 判断对主要爬虫的态度
    def assess_agent(agent_rules):
        disallows = agent_rules.get("disallow", [])
        allows = agent_rules.get("allow", [])
        if "/" in disallows and not allows:
            return "blocked"
        elif disallows:
            return "partial"
        else:
            return "allowed"

    assessments = {}
    for agent, agent_rules in rules.items():
        assessments[agent] = assess_agent(agent_rules)

    return {
        "rules": rules,
        "sitemaps": sitemaps,
        "crawl_delay": crawl_delay,
        "assessments": assessments,
        "total_agents": len(rules),
    }

def summarize(parsed):
    """生成人类可读摘要"""
    assessments = parsed.get("assessments", {})
    rules = parsed.get("rules", {})
    sitemaps = parsed.get("sitemaps", [])
    crawl_delay = parsed.get("crawl_delay", {})

    lines = []
    # 重点关注 * 和常见爬虫
    key_agents = ["*", "googlebot", "bingbot", "baiduspider", "yandexbot"]
    for agent in key_agents:
        if agent in assessments:
            status = assessments[agent]
            emoji = "✅" if status == "allowed" else "🚫" if status == "blocked" else "⚠️"
            r = rules[agent]
            disallow_summary = ', '.join(r['disallow'][:5]) if r['disallow'] else "(none)"
            allow_summary = ', '.join(r['allow'][:3]) if r['allow'] else "(none)"
            delay = crawl_delay.get(agent, "")
            delay_str = f"  crawl-delay={delay}" if delay else ""
            lines.append(f"  {emoji} {agent}: {status}{delay_str}")
            if r['disallow']:
                lines.append(f"     Disallow({len(r['disallow'])}): {disallow_summary}{'...' if len(r['disallow']) > 5 else ''}")

    if sitemaps:
        lines.append(f"\n  Sitemaps ({len(sitemaps)}): {', '.join(sitemaps[:3])}")

    return "\n".join(lines)

def run(domain, as_json=False):
    fetch_result = fetch_robots(domain)

    result = {
        "domain": domain,
        "fetch": fetch_result,
    }

    if fetch_result.get("text"):
        parsed = parse_robots_txt(fetch_result["text"])
        result["parsed"] = parsed
        result["summary"] = summarize(parsed)
    elif fetch_result.get("status_code"):
        result["note"] = f"HTTP {fetch_result['status_code']} - no robots.txt content"
    else:
        result["note"] = f"Fetch failed: {fetch_result.get('error', 'unknown')}"

    if as_json:
        out = {k: v for k, v in result.items() if k != "fetch" or True}
        # 不输出原始 text 以节省空间
        if "fetch" in out and "text" in out["fetch"]:
            out["fetch"] = {k: v for k, v in out["fetch"].items() if k != "text"}
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        status = fetch_result.get("status_code", "ERR")
        final_url = fetch_result.get("final_url", fetch_result.get("url", "?"))
        print(f"\n=== robots.txt: {domain} ===")
        print(f"  URL: {final_url}  [HTTP {status}]")
        if fetch_result.get("redirect_chain"):
            print(f"  重定向: {' -> '.join(fetch_result['redirect_chain'])}")
        if result.get("summary"):
            print(f"\n爬虫规则摘要:")
            print(result["summary"])
        elif result.get("note"):
            print(f"  {result['note']}")
        print()

    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("domain")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    run(args.domain, as_json=args.json)
