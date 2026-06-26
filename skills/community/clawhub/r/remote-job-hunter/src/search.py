#!/usr/bin/env python3
"""
search.py — Multi-platform job fetcher.
Loads platform config from config/platforms.json.
"""
import json, urllib.request, html
from pathlib import Path
try:
    import xml.etree.ElementTree as ET
except:
    pass

CONFIG_DIR = Path(__file__).parent.parent / "config"

def load_platforms():
    with open(CONFIG_DIR / "platforms.json") as f:
        return json.load(f)

def safe_str(val, default=""):
    if val is None:
        return default
    if isinstance(val, list):
        return ", ".join(str(v) for v in val)
    return str(val)


HARD_EXCLUDE_PHRASES = [
    "must be located in", "must reside in", "us only", "usa only",
    "united states only", "requires us work authorization",
    "must be authorized to work in the us", "us citizen",
    "us permanent resident", "requires security clearance",
    "us security clearance", "must be in", "onsite", "on-site", "on site",
    "new york only", "san francisco only", "seattle only",
    "california only", "texas only"
]

def is_location_ok(location):
    if not location:
        return True
    loc = location.lower().strip()
    if any(phrase in loc for phrase in HARD_EXCLUDE_PHRASES):
        return False
    return True

def fetch_remotive(config, domain):
    category = config["category_map"].get(domain, domain)
    url = f"{config['base_url']}?category={category}&limit=100"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            jobs = data.get("jobs", [])
            print(f"  Remotive [{category}]: {len(jobs)} jobs")
            return [{
                "title": html.unescape(safe_str(job.get("title", ""))),
                "company": html.unescape(safe_str(job.get("company_name", ""))),
                "salary": safe_str(job.get("salary", "")) or "Not listed",
                "url": safe_str(job.get("url", "")),
                "location": safe_str(job.get("candidate_required_location", "Worldwide")),
                "posted": safe_str(job.get("publication_date", ""))[:10],
                "tags": ", ".join(job.get("tags", [])[:5]),
                "description": safe_str(job.get("description", "")),
                "source": "Remotive"
            } for job in jobs]
    except Exception as e:
        print(f"  Remotive error: {e}")
        return []

def fetch_jobicy(config, domain):
    tags = config["tag_map"].get(domain, [])
    results = []
    seen_ids = set()
    for tag in tags:
        url = f"{config['base_url']}?count=20&tag={tag}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
                jobs = data.get("jobs", [])
                print(f"  Jobicy [{tag}]: {len(jobs)} jobs")
                for job in jobs:
                    jid = str(job.get("id", ""))
                    if jid in seen_ids:
                        continue
                    seen_ids.add(jid)
                    job_loc = html.unescape(safe_str(job.get("jobGeo", "")))
                    if not is_location_ok(job_loc):
                        continue
                    results.append({
                        "title": html.unescape(safe_str(job.get("jobTitle", ""))),
                        "company": html.unescape(safe_str(job.get("companyName", ""))),
                        "salary": "Not listed",
                        "url": safe_str(job.get("url", "")),
                        "location": safe_str(job.get("jobGeo", "Worldwide")),
                        "posted": safe_str(job.get("pubDate", ""))[:10],
                        "tags": safe_str(job.get("jobIndustry", "")),
                        "description": html.unescape(safe_str(job.get("jobDescription", ""))),
                        "source": "Jobicy"
                    })
        except Exception as e:
            print(f"  Jobicy [{tag}] error: {e}")
    return results

def fetch_remoteok(config, phrases):
    url = config["base_url"]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            jobs = [j for j in data if isinstance(j, dict) and j.get("position")]
            print(f"  RemoteOK: {len(jobs)} total jobs")
            results = []
            for job in jobs:
                position = html.unescape(safe_str(job.get("position", "")))
                tags = " ".join(job.get("tags", []))
                if not any(p in (position + " " + tags).lower() for p in phrases):
                    continue
                sal_min = job.get("salary_min") or 0
                sal_max = job.get("salary_max") or 0
                try:
                    sal_min = int(sal_min) if sal_min else 0
                    sal_max = int(sal_max) if sal_max else 0
                except:
                    sal_min = sal_max = 0
                salary_str = f"${sal_min//1000}K-${sal_max//1000}K USD" if sal_min and sal_max else \
                             f"${sal_min//1000}K+ USD" if sal_min else "Not listed"
                job_loc = safe_str(job.get("location", ""))
                if not is_location_ok(job_loc):
                    continue
                results.append({
                    "title": position,
                    "company": html.unescape(safe_str(job.get("company", ""))),
                    "salary": salary_str,
                    "url": safe_str(job.get("apply_url") or job.get("url", "")),
                    "location": safe_str(job.get("location", "Worldwide")),
                    "posted": "",
                    "tags": ", ".join(job.get("tags", [])[:5]),
                    "description": safe_str(job.get("description", "")),
                    "source": "RemoteOK"
                })
            print(f"  RemoteOK: {len(results)} relevant matches")
            return results
    except Exception as e:
        print(f"  RemoteOK error: {e}")
        return []

def fetch_wwr(config, domain, phrases):
    feeds = config["feeds"].get(domain, [])
    results = []
    for feed_url in feeds:
        try:
            req = urllib.request.Request(feed_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                content = r.read().decode("utf-8")
            root = ET.fromstring(content)
            items = root.findall(".//item")
            matched = 0
            for item in items:
                title_el = item.find("title")
                link_el = item.find("link")
                region_el = item.find("region")
                pubdate_el = item.find("pubDate")
                desc_el = item.find("description")
                if title_el is None:
                    continue
                raw_title = html.unescape(safe_str(title_el.text, ""))
                if ": " in raw_title:
                    company, job_title = raw_title.split(": ", 1)
                else:
                    company, job_title = "", raw_title
                if not any(p in (job_title + " " + company).lower() for p in phrases):
                    continue
                import re
                desc = re.sub(r'<[^>]+>', ' ', safe_str(desc_el.text if desc_el is not None else ""))
                results.append({
                    "title": job_title.strip(),
                    "company": company.strip(),
                    "salary": "Not listed",
                    "url": safe_str(link_el.text if link_el is not None else ""),
                    "location": safe_str(region_el.text if region_el is not None else "Worldwide"),
                    "posted": safe_str(pubdate_el.text if pubdate_el is not None else "")[:16],
                    "tags": "",
                    "description": desc,
                    "source": "WeWorkRemotely"
                })
                matched += 1
            feed_name = feed_url.split('/')[-1].replace('.rss', '')
            print(f"  WWR [{feed_name}]: {matched} matches from {len(items)} items")
        except Exception as e:
            print(f"  WWR error [{feed_url}]: {e}")
    return results

def fetch_himalayas(config, phrases):
    url = f"{config['base_url']}?limit=20"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0", "Accept": "application/json"
        })
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            jobs = data.get("jobs", [])
            results = []
            for job in jobs:
                title = html.unescape(safe_str(job.get("title", "")))
                if not any(p in title.lower() for p in phrases):
                    continue
                sal_min = job.get("minSalary") or 0
                sal_max = job.get("maxSalary") or 0
                try:
                    sal_min = int(sal_min) if sal_min else 0
                    sal_max = int(sal_max) if sal_max else 0
                except:
                    sal_min = sal_max = 0
                salary_str = f"${sal_min//1000}K-${sal_max//1000}K" if sal_min and sal_max else \
                             f"${sal_min//1000}K+" if sal_min else "Not listed"
                results.append({
                    "title": title,
                    "company": html.unescape(safe_str(job.get("companyName", ""))),
                    "salary": salary_str,
                    "url": safe_str(job.get("applicationLink") or job.get("guid", "")),
                    "location": safe_str(job.get("locationRestrictions", ["Worldwide"])),
                    "posted": safe_str(job.get("pubDate", ""))[:10],
                    "tags": "",
                    "description": safe_str(job.get("description", "")),
                    "source": "Himalayas"
                })
            print(f"  Himalayas: {len(results)} matches from {len(jobs)} latest jobs")
            return results
    except Exception as e:
        print(f"  Himalayas error: {e}")
        return []

def fetch_all(domain, phrases, profile_config):
    platforms = load_platforms()
    all_jobs = []
    if platforms.get("remotive", {}).get("enabled"):
        all_jobs += fetch_remotive(platforms["remotive"], domain)
    if platforms.get("jobicy", {}).get("enabled"):
        all_jobs += fetch_jobicy(platforms["jobicy"], domain)
    if platforms.get("remoteok", {}).get("enabled"):
        all_jobs += fetch_remoteok(platforms["remoteok"], phrases)
    if platforms.get("weworkremotely", {}).get("enabled"):
        all_jobs += fetch_wwr(platforms["weworkremotely"], domain, phrases)
    if platforms.get("himalayas", {}).get("enabled"):
        all_jobs += fetch_himalayas(platforms["himalayas"], phrases)

    # Deduplicate by URL
    seen = set()
    unique = []
    for j in all_jobs:
        if j["url"] not in seen and j["title"]:
            seen.add(j["url"])
            unique.append(j)
    print(f"\n  Total unique jobs: {len(unique)}")
    return unique
