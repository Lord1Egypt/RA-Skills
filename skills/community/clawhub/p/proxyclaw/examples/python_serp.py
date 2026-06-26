"""ProxyClaw/IPLoop SERP preset example.

Set IPLOOP_API_KEY first:
  export IPLOOP_API_KEY="your_key_here"

Run:
  python examples/python_serp.py "public search query"
"""
import os
import sys

from iploop import IPLoop


query = " ".join(sys.argv[1:]) or "iploop proxy"
api_key = os.environ.get("IPLOOP_API_KEY")
if not api_key:
    raise SystemExit("Set IPLOOP_API_KEY first")

ip = IPLoop(api_key, country="US")
result = ip.serp.search(query, country="US")

print({
    "success": result.get("success"),
    "source": result.get("source"),
    "country": result.get("country"),
    "count": result.get("count"),
})

for item in result.get("results", [])[:5]:
    print(f"- {item.get('title')} — {item.get('url')}")
