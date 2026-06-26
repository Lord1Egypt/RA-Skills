#!/usr/bin/env python3
"""
Arabic Threat Intelligence Tool
Monitor Arabic-language threat actor channels, generate bilingual reports,
search dark web via Tor, enumerate subdomains via CT logs.
Usage: python3 run.py <command> [args]
"""
import sys, subprocess, json, re

def scrape_telegram(channel):
    try:
        p = subprocess.run(["curl","-sL","--max-time","10",f"https://t.me/s/{channel}"],
            capture_output=True,text=True,timeout=12)
        msgs = re.findall(r'class="tgme_widget_message_text[^>]*>(.*?)</div>',p.stdout,re.DOTALL)
        times = re.findall(r'<time[^>]*datetime="([^"]+)"',p.stdout)
        out = []
        for i,m in enumerate(msgs[-8:]):
            clean = re.sub(r'<[^>]+>',' ',m).strip()[:300]
            t = times[-(8-i)] if i < len(times) else ''
            out.append({"text":clean,"time":t})
        return out
    except:
        return []

def dark_web_search(query):
    engines = [
        "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={}",
        "http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/search?q={}",
    ]
    results = []
    for engine in engines:
        try:
            p = subprocess.run(["torsocks","curl","-sL","--max-time","15",engine.format(query)],
                capture_output=True,text=True,timeout=20)
            links = re.findall(r'href="(http://[a-z0-9]+\.onion[^"]*)"',p.stdout)
            titles = re.findall(r'<a[^>]*href="http://[^"]+"[^>]*>([^<]+)',p.stdout)
            for i,link in enumerate(links[:5]):
                title = titles[i] if i < len(titles) else link
                results.append({"title":title.strip()[:80],"link":link})
        except:
            pass
    return results[:10]

def ct_scan(domain):
    try:
        p = subprocess.run(["curl","-s","--max-time","15",f"https://crt.sh/?q=%25.{domain}&output=json"],
            capture_output=True,text=True,timeout=18)
        d = json.loads(p.stdout)
        names = set()
        for c in d:
            for n in c.get('name_value','').split('\n'):
                n = n.strip()
                if n and '*' not in n: names.add(n)
        # Flag interesting ones
        interesting_keywords = ['admin','api','dev','test','vpn','mail','staging','internal','beta','old']
        flagged = [n for n in names if any(k in n.lower() for k in interesting_keywords)]
        return {"all":sorted(names),"flagged":flagged}
    except:
        return {"all":[],"flagged":[]}

DEFAULT_CHANNELS = ['hak994','xX313XxTeam','fattah_irili','elamharbi']

args = sys.argv[1:]
cmd = args[0] if args else 'help'
lang = next((args[i+1] for i,a in enumerate(args) if a=='--lang' and i+1<len(args)),'both')

if cmd == 'channel':
    ch = args[1] if len(args)>1 and not args[1].startswith('-') else 'hak994'
    posts = scrape_telegram(ch)
    print(f"\n📡 @{ch} — {len(posts)} recent posts\n{'─'*50}")
    for p in posts:
        print(f"[{p['time'][:16]}]\n{p['text'][:200]}\n")

elif cmd == 'report':
    topic = ' '.join([a for a in args[1:] if not a.startswith('-')]) or 'threat intelligence'
    print(f"\n{'═'*50}\n🔍 THREAT INTELLIGENCE REPORT\nTopic: {topic}\n{'═'*50}")
    for ch in DEFAULT_CHANNELS:
        posts = scrape_telegram(ch)
        if posts:
            print(f"\n📡 @{ch} ({len(posts)} posts):")
            for p in posts[:3]:
                print(f"  • {p['text'][:100]}")
    print(f"\n{'─'*50}\nReport generated. Review and verify before sharing.")

elif cmd == 'darkweb':
    query = ' '.join([a for a in args[1:] if not a.startswith('-')]) or 'data leak'
    print(f"\n🕵️ Dark Web Search: {query}")
    print("(Searching via Tor — may take 30-60 seconds...)")
    results = dark_web_search(query)
    if results:
        print(f"\nFound {len(results)} results:")
        for r in results:
            print(f"  • {r['title']}\n    {r['link']}")
    else:
        print("No results found or Tor unavailable.")

elif cmd == 'scan':
    domain = args[1] if len(args)>1 else 'example.com'
    print(f"\n🔬 CT Log Scan: {domain}")
    result = ct_scan(domain)
    all_subs = result['all']
    flagged = result['flagged']
    print(f"Total subdomains: {len(all_subs)}")
    if flagged:
        print(f"\n⚠️ Interesting ({len(flagged)}):")
        for s in flagged[:20]: print(f"  🎯 {s}")
    print(f"\nAll subdomains ({min(len(all_subs),30)} shown):")
    for s in sorted(all_subs)[:30]: print(f"  {s}")

else:
    print("""
Arabic Threat Intelligence Tool — OSINT for Arabic threat actors

Commands:
  channel <name>              Monitor a Telegram channel
  report <topic>              Generate threat report from all channels
  darkweb <query>             Search dark web via Tor
  scan <domain>               CT log subdomain discovery

Options:
  --lang ar|en|both           Output language (default: both)
  --region me|africa|asia|all Target region (default: all)

Examples:
  python3 run.py channel hak994
  python3 run.py report "ransomware campaign"
  python3 run.py darkweb "company data leak"
  python3 run.py scan target-company.com
""")
