#!/usr/bin/env python3
"""
IPLoop Support AI — HTTP endpoint for customer/bot queries
POST /chat  {"question": "..."}  →  {"answer": "..."}

Uses knowledge base + pattern matching + fallback to helpful links.
"""

import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

KNOWLEDGE_BASE = {
    "about": {
        "keywords": ["what is iploop", "about iploop", "what do you do", "tell me about"],
        "answer": "IPLoop is a residential proxy platform with 1M+ real IPs across 195+ countries. Built for AI agents, bots, and data pipelines. City-level targeting, HTTP/HTTPS/SOCKS5. Install with `pip install iploop[stealth]` or `npm install iploop`."
    },
    "pricing": {
        "keywords": ["cost", "price", "pricing", "how much", "free plan", "free tier", "plans", "payment", "pay"],
        "answer": "5 plans:\n• Free: $0 — 0.5 GB, 30 req/min, all 195+ countries\n• Starter: $4.50/GB\n• Growth: $3.50/GB\n• Business: $2.50/GB\n• Enterprise: Custom\n\nPromo code OPENCLAW = 20% off. Sign up free: https://iploop.io/signup.html"
    },
    "countries": {
        "keywords": ["countr", "geo", "location", "target", "region", "city"],
        "answer": "195+ countries with city-level, ZIP code, ISP, and ASN targeting.\n\nUsage: `iploop:APIKEY-country-US-city-miami@proxy.iploop.io:8880`"
    },
    "python_sdk": {
        "keywords": ["python", "pip install", "pip"],
        "answer": "```\npip install iploop[stealth]\n```\n\n```python\nfrom iploop import IPLoop\nclient = IPLoop(api_key='YOUR_KEY', stealth=True)\nresult = client.fetch('https://example.com', country='US')\n```\n\nStealth mode adds anti-bot bypass via Scrapling."
    },
    "node_sdk": {
        "keywords": ["node", "npm", "javascript", "js sdk"],
        "answer": "```\nnpm install iploop\n```\n\n```javascript\nconst { IPLoop } = require('iploop');\nconst client = new IPLoop('YOUR_API_KEY');\nconst result = await client.fetch('https://example.com', { country: 'US' });\n```\n\nFor anti-bot sites, use Python SDK with stealth mode."
    },
    "endpoint": {
        "keywords": ["endpoint", "proxy url", "proxy address", "curl", "connect"],
        "answer": "Proxy: `proxy.iploop.io:8880`\n\n```bash\ncurl -x http://iploop:APIKEY-country-us@proxy.iploop.io:8880 https://example.com\n```\n\nSupports HTTP, HTTPS, SOCKS5."
    },
    "sessions": {
        "keywords": ["sticky", "session", "same ip", "rotate", "rotation"],
        "answer": "• Rotating (default): New IP per request\n• Sticky: Same IP — add `session-ID-sesstype-sticky` to auth string\n\nExample: `iploop:APIKEY-session-abc123-sesstype-sticky@proxy.iploop.io:8880`"
    },
    "antibot": {
        "keywords": ["cloudflare", "anti-bot", "antibot", "bypass", "block", "stealth", "captcha", "protect"],
        "answer": "Python SDK stealth mode uses Scrapling browser fingerprinting:\n• Bypasses Cloudflare, Akamai, most anti-bot\n• 66 sites tested at 100% success\n• `client = IPLoop(api_key='KEY', stealth=True)`\n\nSites: BestBuy, Nike, Zillow, Walmart, Booking, Airbnb, etc."
    },
    "serp": {
        "keywords": ["serp", "google search", "search results", "startpage", "verification", "unusual traffic", "raw google"],
        "answer": "For public SERP research, do not scrape raw google.com/search directly. Use the SERP-safe Python SDK preset:\n\n```python\nfrom iploop import IPLoop\nip = IPLoop('YOUR_API_KEY', country='US')\nresults = ip.serp.search('public search query', country='US')\nprint(results['results'])\n```\n\n`ip.google.search(...)` uses the safe SERP path by default. Raw Google is QA-only with `direct=True` and may return verification pages. Docs: https://github.com/Iploop/proxyclaw/blob/master/docs/SERP.md"
    },
    "sites": {
        "keywords": ["site", "preset", "supported site", "which site", "what site", "scrape"],
        "answer": "67 site presets, 100% success rate:\nYouTube, Reddit, Amazon, LinkedIn, eBay, Twitter, TikTok, Instagram, Booking, Walmart, Target, Airbnb, BestBuy, Pinterest, Zillow, Nike, IKEA, Apple, Samsung, BBC, CNN, NYTimes + 44 more.\n\nFull list: https://github.com/Iploop/proxyclaw"
    },
    "ethical": {
        "keywords": ["gdpr", "ccpa", "ethical", "legal", "comply", "compliance", "sourced", "source", "legit"],
        "answer": "100% ethical. All IPs from voluntary opt-in users who consent to bandwidth sharing in exchange for free proxy credits (EarnClaw). Fully GDPR and CCPA compliant."
    },
    "protocols": {
        "keywords": ["protocol", "socks", "http", "https"],
        "answer": "HTTP, HTTPS, and SOCKS5. The SDK handles protocol selection automatically, or configure manually via the proxy gateway."
    },
    "signup": {
        "keywords": ["api key", "sign up", "register", "account", "get started", "start"],
        "answer": "Sign up free at https://iploop.io/signup.html — no credit card required.\nYou get an API key immediately. Free plan: 0.5 GB included.\n\nSet your key: `export IPLOOP_API_KEY='your-key'`"
    },
    "proxyclaw": {
        "keywords": ["proxyclaw", "difference", "api.proxyclaw"],
        "answer": "**IPLoop** = proxy network (residential IPs, SDK, direct access)\n**ProxyClaw** = AI scraping agent (JS rendering, CAPTCHA solving, structured data)\n\nProxyClaw uses IPLoop proxies under the hood. API: `GET https://api.proxyclaw.ai/browser?url=<url>`"
    },
    "fleet": {
        "keywords": ["how many", "fleet", "nodes", "ips", "pool size"],
        "answer": "1,000,000+ residential IPs in our pool across 195+ countries. 9,600+ nodes connected right now, 77,000+ daily unique IPs rotating through 4 gateway servers."
    },
    "success": {
        "keywords": ["success rate", "reliable", "uptime", "stable"],
        "answer": "100% success rate across 66 major sites (verified with 5 consecutive runs). Includes Amazon, Zillow, Walmart, BestBuy, Nike, Booking.com, Airbnb. Proxy uptime: 99.9%+."
    },
    "speed": {
        "keywords": ["fast", "speed", "latency", "slow", "performance"],
        "answer": "Typical latency: 200-500ms for residential proxies. The SDK supports concurrent requests for higher throughput. Use `format=raw` in the ProxyClaw API to skip JS rendering (faster)."
    },
    "datacenter": {
        "keywords": ["datacenter", "data center", "dc proxy"],
        "answer": "IPLoop provides residential proxies only — real IPs from real devices. No datacenter IPs. This means higher success rates on anti-bot sites since the IPs are genuine residential."
    },
    "troubleshoot": {
        "keywords": ["not working", "error", "fail", "timeout", "403", "blocked", "issue", "problem", "help"],
        "answer": "Common fixes:\n• 403/blocked → Enable stealth mode: `stealth=True`\n• Timeout → Try a different country/region\n• Auth error → Check API key format: `iploop:APIKEY@proxy.iploop.io:8880`\n\nStill stuck? Email partners@iploop.io or visit https://iploop.io/contact.html"
    },
    "china": {
        "keywords": ["china", "russia", "iran", "restricted"],
        "answer": "We have residential IPs in 195+ countries. Availability varies by region. Contact partners@iploop.io for specific country requirements."
    },
    "api": {
        "keywords": ["api", "rest api", "http api"],
        "answer": "ProxyClaw API:\n`GET https://api.proxyclaw.ai/browser?url=<url>`\n\nParams: format (rendered/raw), delay (0.1-10s), device (desktop/mobile), country (ISO code)\nAuth: `Authorization: Bearer YOUR_TOKEN`\n\nDocs: https://proxyclaw.ai/docs.html"
    },
    "earnclaw": {
        "keywords": ["earn", "earnclaw", "bandwidth", "share", "money", "credit"],
        "answer": "EarnClaw lets you share idle bandwidth and earn free proxy credits. Install the agent, contribute to the network, use proxies at zero cost. Fully opt-in, GDPR compliant."
    },
}

# Greeting patterns
GREETINGS = ["hi", "hello", "hey", "sup", "yo", "greetings", "good morning", "good afternoon"]

def find_answer(question: str) -> dict:
    q = question.lower().strip()
    
    # Greetings
    if q in GREETINGS or any(q.startswith(g + " ") or q == g for g in GREETINGS):
        return {
            "answer": "Hey! 👋 I'm IPLoop Support AI. I can help with:\n• Pricing & plans\n• SDK setup (Python/Node.js)\n• Proxy configuration\n• Anti-bot bypass\n• Troubleshooting\n\nWhat do you need?",
            "category": "greeting",
            "confidence": 1.0
        }
    
    # Score each category
    best_score = 0
    best_key = None
    
    for key, data in KNOWLEDGE_BASE.items():
        score = 0
        for kw in data["keywords"]:
            if kw in q:
                # Longer keyword matches = higher confidence
                score += len(kw.split())
        if score > best_score:
            best_score = score
            best_key = key
    
    if best_key and best_score > 0:
        return {
            "answer": KNOWLEDGE_BASE[best_key]["answer"],
            "category": best_key,
            "confidence": min(best_score / 3, 1.0)
        }
    
    # Fallback
    return {
        "answer": "I can help with IPLoop pricing, setup, features, and troubleshooting.\n\n• Docs: https://proxyclaw.ai/docs.html\n• Sign up: https://iploop.io/signup.html\n• Contact: partners@iploop.io\n\nCould you rephrase your question?",
        "category": "fallback",
        "confidence": 0.0
    }


class SupportHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/chat":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            question = body.get("question", body.get("q", ""))
            
            result = find_answer(question)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "categories": len(KNOWLEDGE_BASE)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Quiet


if __name__ == "__main__":
    # Test mode
    print("=" * 60)
    print("  IPLoop Support AI — Full Test Suite")
    print("=" * 60)
    
    all_questions = [
        # Core questions (should all match)
        "What is IPLoop?",
        "How much does it cost?",
        "Is there a free plan?",
        "What countries do you support?",
        "How do I install the Python SDK?",
        "How do I use the proxy with curl?",
        "What's the proxy endpoint?",
        "How do I target a specific country?",
        "How do sticky sessions work?",
        "Can I scrape Amazon?",
        "Does it bypass Cloudflare?",
        "What sites are supported?",
        "How does stealth mode work?",
        "Can I scrape Zillow?",
        "What about anti-bot protection?",
        "How are the IPs sourced?",
        "Is it GDPR compliant?",
        "What protocols are supported?",
        "How do I get an API key?",
        "Can I use this for web scraping?",
        "Do you have a Node.js SDK?",
        "What's the difference between IPLoop and ProxyClaw?",
        "How many IPs do you have?",
        "What's the success rate?",
        # Edge cases
        "hi",
        "hello",
        "help me",
        "I need to scrape 1 million pages",
        "do you have datacenter proxies?",
        "what payment methods do you accept?",
        "my proxy is not working",
        "can I use this in China?",
        "what is your uptime?",
        "do you have an API?",
        "how fast is it?",
        "what about EarnClaw?",
        "how do I earn credits?",
    ]
    
    categories = {}
    for q in all_questions:
        result = find_answer(q)
        cat = result["category"]
        conf = result["confidence"]
        icon = "✅" if cat != "fallback" else "⚠️"
        categories[cat] = categories.get(cat, 0) + 1
        print(f"{icon} [{cat:12s}] {conf:.1f} | {q}")
        if cat == "fallback":
            print(f"   → FALLBACK")
    
    matched = sum(1 for q in all_questions if find_answer(q)["category"] != "fallback")
    print(f"\n{'=' * 60}")
    print(f"  {matched}/{len(all_questions)} matched ({matched/len(all_questions)*100:.0f}%)")
    print(f"  Categories hit: {dict(sorted(categories.items()))}")
    print(f"{'=' * 60}")
