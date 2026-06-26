#!/usr/bin/env python3
"""Quick credibility heuristics for a URL."""
import sys
from urllib.parse import urlparse

def score(url: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    # Government / academic boost
    if domain.endswith(".gov") or domain.endswith(".edu"):
        tier = "high"
    # Known reference domains
    elif any(d in domain for d in ["wikipedia.org", "arxiv.org", "nature.com", "sciencedirect.com"]):
        tier = "high"
    # Major news / tech publications
    elif any(d in domain for d in ["reuters.com", "apnews.com", "bbc.com", "nytimes.com", "techcrunch.com"]):
        tier = "medium"
    # Blog platforms (lower default)
    elif any(d in domain for d in ["medium.com", "substack.com", "wordpress.com", "blogspot.com"]):
        tier = "low"
    else:
        tier = "medium"
    
    return {"url": url, "domain": domain, "credibility_tier": tier}

if __name__ == "__main__":
    for url in sys.argv[1:]:
        import json
        print(json.dumps(score(url)))
