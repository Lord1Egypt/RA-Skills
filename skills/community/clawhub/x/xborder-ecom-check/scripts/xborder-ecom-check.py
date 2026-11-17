#!/usr/bin/env python3
"""
Cross-Border E-Commerce Compliance Check — Cross-border e-commerce rules: customs, product safety, consumer protection, tax (VAT/GST), advertising, and data privacy of destination markets

Free skill + CQDev cloud compliance engine (compliancehub.cn).
Scoring and quota are computed in the cloud; before first use, get a free
API Key (100 free calls): open the account page, copy the Key, then set the
COMPLIANCEHUB_API_KEY environment variable or save it to
~/.config/compliancehub/<skill>.key (mode 0600).

Flow:
  1. Load API Key (env COMPLIANCEHUB_API_KEY, or ~/.config/compliancehub/<slug>.key)
  2. Fetch check items from the cloud rule-library API (public read)
  3. Collect per-item compliance status (y=pass / n=fail / na=n/a)
  4. Submit to the cloud evaluate endpoint (auth) OR score locally on 404
  5. Render a professional report locally

No API Key yet? The skill runs in anonymous trial mode automatically: a local
random anon_id is issued, and you get up to 5 real cloud-scored evaluations per
skill (7-day window). When the trial runs out the skill points you to the
one-click registration page, carrying your anon_id so nothing is lost.

Uses only Python built-in urllib — zero third-party dependencies. HTTPS + Bearer
transport for the key; no hardcoding, no covert exfiltration.

Network usage is limited to SCORING runs (when a valid API Key is present):
(a) fetching the public check-item rule library from the pinned endpoint (read-only, NO answers sent);
and (b) your scored answers + the API Key (as a Bearer token) to the pinned evaluate endpoint.
The free PREVIEW modes (--non-interactive / --non-interactive-json) run FULLY OFFLINE using the
bundled CHECK_ITEMS and NEVER contact the network. No credentials are collected in the terminal.
No other data leaves the machine.

Language: bilingual (中文/English). Item names, categories and recommendations are
presented in Chinese by default for Chinese-speaking compliance teams; legal/regulatory
references keep English originals. Users may request English output at any time.
"""
import sys, os, json, argparse, datetime, ssl, uuid
import urllib.request
import urllib.error
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))

# ─── Cloud endpoints ──────────────────────────────────────────────
# API_BASE is PINNED to the operator's official compliance cloud and is
# intentionally NOT overridable via an environment variable. Allowing a
# COMPLIANCEHUB_API_BASE override would let a malicious environment redirect
# users' compliance answers AND their API Key (sent as a Bearer token) to an
# attacker-controlled server — flagged by security scanners as a "redirectable
# cloud endpoint" / credential-exfiltration chain. The destination is fixed.
API_BASE = "https://compliancehub.cn"
SKILL_SLUG = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RULES_URL = f"{API_BASE}/api/v1/rules/{SKILL_SLUG}/rules"        # public read: check items
EVALUATE_URL = f"{API_BASE}/api/v1/rules/{SKILL_SLUG}/evaluate"  # auth: scoring
ACCOUNT_PAGE = f"{API_BASE}/account.html?skill={SKILL_SLUG}&utm_source=skill&utm_medium=agent"      # unified account center (utm for attribution)


def _skill_version():
    pkg = os.path.join(os.path.dirname(__file__), "..", "package.json")
    try:
        if os.path.isfile(pkg):
            with open(pkg, encoding="utf-8") as f:
                return json.load(f).get("version", "1.0.0")
    except Exception:
        pass
    return "1.0.0"


def _ua():
    return f"{SKILL_SLUG}/{_skill_version()}"


def _key_path():
    """Private, per-user key store OUTSIDE the skill directory.
    The API Key is written here (mode 0600) rather than inside the skill
    folder, so it is never bundled with or leaked by the skill package.
    """
    d = os.path.join(os.path.expanduser("~"), ".config", "compliancehub")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{SKILL_SLUG}.key")


def load_api_key():
    env_key = os.environ.get("COMPLIANCEHUB_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()
    p = _key_path()
    if os.path.isfile(p):
        try:
            with open(p, encoding="utf-8") as f:
                s = f.read().strip()
                if s:
                    return s
        except Exception:
            pass
    return None


def _anon_id_path():
    """Per-user anonymous trial id store (mode 0600), outside the skill dir."""
    d = os.path.join(os.path.expanduser("~"), ".config", "compliancehub")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{SKILL_SLUG}.anon_id")


def load_or_create_anon_id():
    """Return the persistent anonymous trial id, creating a fresh uuid on first run.

    The anon_id lets the cloud engine keep a 7-day, up-to-5-use anonymous quota
    per skill WITHOUT requiring registration first. It is a plain random uuid and
    carries no personal data; it is only used to continue the anonymous trial
    and to pre-fill the registration page when the trial runs out.
    """
    p = _anon_id_path()
    if os.path.isfile(p):
        try:
            with open(p, encoding="utf-8") as f:
                s = f.read().strip()
                if s and len(s) <= 64:
                    return s
        except Exception:
            pass
    aid = str(uuid.uuid4())
    try:
        with open(p, "w", encoding="utf-8") as f:
            f.write(aid)
        os.chmod(p, 0o600)
    except Exception:
        pass
    return aid


def _register_page(anon_id=None):
    """Registration funnel URL. The anon_id is passed through so the account page
    can keep the visitor's trial context and make registering a one-click jump."""
    url = ACCOUNT_PAGE
    if anon_id:
        url += "&anon_id=" + urllib.parse.quote(anon_id)
    return url


def fetch_rules():
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(RULES_URL, headers={"User-Agent": _ua()})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            if resp.status != 200:
                return None
            payload = json.loads(resp.read().decode("utf-8"))
        if not payload.get("success"):
            return None
        raw_items = payload.get("items") or []
        if not raw_items:
            return None
        items = []
        for it in raw_items:
            items.append({
                "id": it.get("item_key"),
                "name": it.get("name"),
                "desc": it.get("question") or it.get("description") or "",
                "ref": it.get("legal_ref") or "",
                "category": it.get("category_name") or "",
                "recommendation": it.get("recommendation") or "",
            })
        return items
    except Exception:
        return None


CHECK_ITEMS = [
    {"id": "business_registration", "name": "\u4e3b\u4f53\u4e0e\u5e73\u53f0\u6ce8\u518c", "ref": "\u76ee\u7684\u5730\u5e02\u573a\u51c6\u5165", "category": "A. \u5e02\u573a\u51c6\u5165",
     "desc": "\u662f\u5426\u5728\u76ee\u6807\u5e02\u573a\u5b8c\u6210\u8de8\u5883\u7535\u5546\u4e3b\u4f53/\u5e73\u53f0\u5408\u89c4\u6ce8\u518c\uff08\u5982 EU OSS\u3001UK VT\u3001\u5e73\u53f0\u5356\u5bb6\u8d44\u8d28\uff09\uff1f", "recommendation": "\u5b8c\u6210\u5f53\u5730\u7a0e\u52a1/\u5546\u4e8b\u767b\u8bb0\u518d\u5f00\u552e\u3002"},
    {"id": "country_of_origin", "name": "\u539f\u4ea7\u56fd\u6807\u6ce8", "ref": "\u6d77\u5173\u4e0e\u539f\u4ea7\u5730\u89c4\u5219", "category": "B. \u5546\u54c1\u5408\u89c4",
     "desc": "\u662f\u5426\u51c6\u786e\u6807\u6ce8\u5546\u54c1\u539f\u4ea7\u56fd\uff08\u5730\u533a\uff09\u4e14\u4e0d\u865a\u5047\uff1f", "recommendation": "\u8be6\u60c5\u9875\u4e0e\u7269\u6d41\u5355\u636e\u4e00\u81f4\u6807\u6ce8\u3002"},
    {"id": "customs_declaration", "name": "\u6d77\u5173\u7533\u62a5\u5408\u89c4", "ref": "\u6d77\u5173\u6cd5", "category": "B. \u5546\u54c1\u5408\u89c4",
     "desc": "\u662f\u5426\u5982\u5b9e\u7533\u62a5\u5546\u54c1\u5f52\u7c7b\u3001\u4ef7\u503c\u3001\u6570\u91cf\uff0c\u65e0\u4f4e\u62a5/\u7792\u62a5\uff1f", "recommendation": "\u7533\u62a5\u4ef7\u683c\u4e0e\u4ea4\u6613\u4e00\u81f4\uff0c\u7559\u5b58\u51ed\u8bc1\u3002"},
    {"id": "tariff_compliance", "name": "\u5173\u7a0e\u4e0e\u8fdb\u53e3\u7a0e", "ref": "\u5173\u7a0e\u6cd5", "category": "C. \u7a0e\u52a1",
     "desc": "\u662f\u5426\u4f9d\u6cd5\u7f34\u7eb3\u5173\u7a0e\u4e0e\u8fdb\u53e3\u73af\u8282\u7a0e\uff0c\u6216\u5408\u89c4\u9002\u7528\u514d\u7a0e\u989d\u5ea6\uff1f", "recommendation": "\u6838\u7b97\u5230\u5cb8\u6210\u672c\u5e76\u7533\u62a5\u3002"},
    {"id": "ce_marking", "name": "CE \u6807\u5fd7\uff08\u6b27\u76df\uff09", "ref": "EU \u6cd5\u89c4 (\u5982 MDR/LVD)", "category": "B. \u5546\u54c1\u5408\u89c4",
     "desc": "\u6d89\u8bc1\u4ea7\u54c1\u662f\u5426\u52a0\u8d34 CE \u6807\u5fd7\u5e76\u9644\u5408\u89c4\u58f0\u660e (DoC)\uff1f", "recommendation": "\u5f3a\u5236\u76ee\u5f55\u4ea7\u54c1\u5b8c\u6210 CE \u5408\u683c\u8bc4\u5b9a\u3002"},
    {"id": "product_safety", "name": "\u5546\u54c1\u5b89\u5168\u73af\u4fdd", "ref": "REACH / CPSC / \u76ee\u7684\u5730\u6cd5\u89c4", "category": "B. \u5546\u54c1\u5408\u89c4",
     "desc": "\u5546\u54c1\u662f\u5426\u7b26\u5408\u76ee\u7684\u5730\u5b89\u5168/\u73af\u4fdd\u6cd5\u89c4\uff08\u5316\u5b66\u3001\u963b\u71c3\u3001\u673a\u68b0\u7b49\uff09\uff1f", "recommendation": "\u4e0a\u67b6\u524d\u505a\u5408\u89c4\u6d4b\u8bd5\u4e0e\u6750\u6599\u58f0\u660e\u3002"},
    {"id": "label_language", "name": "\u6807\u7b7e\u4e0e\u8bf4\u660e\u4e66\u8bed\u8a00", "ref": "\u76ee\u7684\u5730\u6807\u7b7e\u6cd5\u89c4", "category": "B. \u5546\u54c1\u5408\u89c4",
     "desc": "\u6807\u7b7e/\u8bf4\u660e\u4e66\u662f\u5426\u6ee1\u8db3\u76ee\u7684\u5730\u8bed\u8a00\u4e0e\u5185\u5bb9\u5f3a\u5236\u8981\u6c42\uff1f", "recommendation": "\u6309\u5f53\u5730\u8bed\u8a00\u63d0\u4f9b\u8b66\u793a\u4e0e\u8bf4\u660e\u3002"},
    {"id": "consumer_protection", "name": "\u6d88\u8d39\u8005\u6743\u76ca", "ref": "\u76ee\u7684\u5730\u6d88\u4fdd\u6cd5", "category": "D. \u6d88\u8d39\u8005",
     "desc": "\u662f\u5426\u6ee1\u8db3\u9000\u6362\u8d27\u3001\u65e0\u7406\u7531\u9000\u8d27\u3001\u552e\u540e\u54cd\u5e94\u7b49\u5f53\u5730\u6d88\u8d39\u8005\u4fdd\u62a4\u8981\u6c42\uff1f", "recommendation": "\u5e97\u94fa\u653f\u7b56\u4e0d\u4f4e\u4e8e\u5f53\u5730\u6cd5\u5b9a\u4e0b\u9650\u3002"},
    {"id": "ad_compliance", "name": "\u5e7f\u544a\u4e0e\u76f4\u64ad\u8bdd\u672f", "ref": "\u5e7f\u544a\u6cd5/\u8de8\u5883", "category": "E. \u8425\u9500",
     "desc": "\u8de8\u5883\u5e7f\u544a/\u76f4\u64ad\u662f\u5426\u5408\u89c4\uff08\u7981\u7528\u7edd\u5bf9\u5316\u7528\u8bed\u3001\u7597\u6548\u65ad\u8a00\u3001\u865a\u5047\u8bc4\u8bba\uff09\uff1f", "recommendation": "\u8bdd\u672f\u8d70\u5408\u89c4\u62a4\u680f\uff08\u53c2\u8003 shop-ad-guard\uff09\u3002"},
    {"id": "data_privacy", "name": "\u4e70\u5bb6\u6570\u636e\u9690\u79c1", "ref": "GDPR / CCPA \u7b49", "category": "F. \u6570\u636e",
     "desc": "\u662f\u5426\u9075\u5b88\u76ee\u7684\u5730\u6570\u636e\u9690\u79c1\u6cd5\u5904\u7406\u4e70\u5bb6\u59d3\u540d/\u5730\u5740/\u652f\u4ed8\u4fe1\u606f\uff1f", "recommendation": "\u9690\u79c1\u653f\u7b56\u4e0e\u6570\u636e\u7559\u5b58\u7b26\u5408\u5f53\u5730\u6cd5\u3002"},
    {"id": "ip_compliance", "name": "\u77e5\u8bc6\u4ea7\u6743", "ref": "\u5546\u6807/\u4e13\u5229/\u7248\u6743\u6cd5", "category": "G. \u77e5\u8bc6\u4ea7\u6743",
     "desc": "\u5546\u54c1\u662f\u5426\u4fb5\u6743\uff08\u5546\u6807/\u4e13\u5229/\u7248\u6743/\u5916\u89c2\u8bbe\u8ba1\uff09\uff1f", "recommendation": "\u4e0a\u67b6\u524d\u505a\u5546\u6807\u4e0e\u4e13\u5229\u6392\u67e5\u3002"},
    {"id": "tax_vat", "name": "\u589e\u503c\u7a0e/VAT \u7533\u62a5", "ref": "EU OSS/IOSS\u3001UK VAT \u7b49", "category": "C. \u7a0e\u52a1",
     "desc": "\u662f\u5426\u4f9d\u6cd5\u6ce8\u518c\u767b\u8bb0\u5e76\u7533\u62a5\u589e\u503c\u7a0e/VAT\uff08\u5982\u6b27\u76df OSS/IOSS\uff09\uff1f", "recommendation": "\u8425\u4e1a\u989d\u8fbe\u9608\u503c\u5373\u6ce8\u518c\u5e76\u6309\u671f\u7533\u62a5\u3002"},
]


def collect_responses(items):
    responses = []
    total = len(items)
    print(f"\n📋 Cross-Border E-Commerce Compliance Check — {total} items")
    print("   Answer each item's actual status (y=pass / n=fail / na=not applicable)\n")
    for i, item in enumerate(items):
        idx = i + 1
        while True:
            ans = input(f"  [{idx}/{total}] {item['name']} [{item['ref']}]\n"
                        f"        {item['desc']}\n"
                        f"        (y/n/na) > ").strip().lower()
            if ans in ('y', 'n', 'na'):
                if ans == 'na':
                    responses.append({**item, "status": "na"})
                else:
                    responses.append({**item, "status": "pass" if ans == 'y' else "fail"})
                break
            print("        please enter y, n or na")
    return responses


def build_submission(responses):
    items = []
    for r in responses:
        if r["status"] == "na":
            continue
        items.append({"item_key": r["id"], "passed": r["status"] == "pass", "evidence": None})
    return items


def compute_local_score(submission, items):
    """Fallback scoring when cloud rule library is not yet open (404)."""
    meta = {it["id"]: it for it in items}
    total = len(submission)
    passed = sum(1 for s in submission if s["passed"])
    score = round(passed / total * 100) if total else 0
    out_items = []
    for s in submission:
        it = meta.get(s["item_key"], {}) or {}
        out_items.append({
            "item_key": s["item_key"], "name": it.get("name", s["item_key"]),
            "passed": s["passed"], "legal_ref": it.get("ref", ""),
            "recommendation": it.get("recommendation", ""), "category_name": it.get("category", ""),
        })
    return {
        "version": _skill_version(), "score": score,
        "passed_count": passed, "failed_count": total - passed, "total_items": total,
        "quota_remaining": None, "scored_locally": True, "items": out_items,
    }


def call_evaluate(key, submission, anon_id=None):
    payload = {"items": submission, "context": None}
    if anon_id:
        payload["anon_id"] = anon_id
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json", "User-Agent": _ua()}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(EVALUATE_URL, data=body, headers=headers, method="POST")
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            if resp.status != 200:
                return None, f"cloud returned HTTP {resp.status}"
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = json.loads(e.read().decode("utf-8", "ignore")).get("detail", "")
        except Exception:
            pass
        if e.code == 401:
            return None, "API Key invalid; get a free Key at: " + ACCOUNT_PAGE
        if e.code == 403:
            if anon_id:
                # Anonymous trial exhausted -> the caller routes to registration.
                return None, "ANON_QUOTA_EXHAUSTED"
            return None, f"free quota exhausted: {detail}"
        if e.code == 404:
            return None, "RULE_LIB_NOT_OPEN"
        return None, f"cloud error HTTP {e.code}: {detail}"
    except Exception as e:
        return None, f"cloud call failed: {e}"


def _score_block(data):
    return (f"  Compliance score: {data.get('score')}/100\n"
            f"  ✅ Pass {data.get('passed_count')} | ❌ Fail {data.get('failed_count')} | Items {data.get('total_items')}")


def render_text(data, items):
    s = data
    lines = ["=" * 60, f"  Cross-Border E-Commerce Compliance Check Report (cloud-scored)" if not s.get("scored_locally") else f"  Cross-Border E-Commerce Compliance Check Report (local fallback score)",
             f"  Law: Cross-border e-commerce rules: customs, product safety, consumer protection, tax (VAT/GST), advertising, and data privacy of destination markets", f"  Engine version: {s.get('version', '?')}",
             _score_block(s), "=" * 60]
    current_cat = ""
    for r in items:
        if r.get("category_name") != current_cat:
            current_cat = r.get("category_name", "")
            lines.append(f"\n  ── {current_cat} ──")
        icon = "✅" if r.get("passed") else "❌"
        lines.append(f"\n  {icon} [{r.get('item_key')}] {r.get('name')}")
        if r.get("legal_ref"):
            lines.append(f"    Authority: {r.get('legal_ref')}")
        if r.get("recommendation"):
            lines.append(f"    Recommendation: {r.get('recommendation')}")
    lines.append("=" * 60)
    lines.append("\n💡 Disclaimer: reference only, not legal advice.")
    return "\n".join(lines)


def render_html(data, items):
    s = data
    score = s.get("score", 0)
    color = "#4caf50" if score >= 80 else "#ff9800" if score >= 60 else "#f44336"
    rows = ""
    current_cat = ""
    for r in items:
        if r.get("category_name") != current_cat:
            current_cat = r.get("category_name", "")
            rows += f'<tr class="category-row"><td colspan="5">{current_cat}</td></tr>\n'
        icon = "✅" if r.get("passed") else "❌"
        cls = "pass" if r.get("passed") else "fail"
        rec = r.get("recommendation") or "Keep it up"
        rows += f"""<tr class="{cls}"><td>{icon}</td><td>{r.get('name')}</td><td>{r.get('legal_ref') or ''}</td><td>{cls.upper()}</td><td>{rec}</td></tr>\n"""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Cross-Border E-Commerce Compliance Check Report</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#333}}
h1{{border-bottom:2px solid #2563eb;padding-bottom:.5rem}}
.score-card{{background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff;padding:2rem;border-radius:12px;text-align:center;margin:1.5rem 0}}
.score{{font-size:4rem;font-weight:700}}
.summary{{display:flex;gap:2rem;justify-content:center;margin-top:1rem}}
.summary div{{text-align:center;font-size:1.2rem}}
table{{width:100%;border-collapse:collapse;margin-top:1.5rem}}
th{{background:#f1f5f9;text-align:left;padding:.75rem;border-bottom:2px solid #e2e8f0}}
td{{padding:.75rem;border-bottom:1px solid #e2e8f0}}
tr.pass td:first-child{{color:#4caf50}}
tr.fail td:first-child{{color:#f44336}}
tr.category-row td{{background:#dbeafe;font-weight:600;color:#1d4ed8}}
.note{{color:#94a3b8;margin-top:2rem;font-size:.85rem}}
</style></head><body>
<h1>Cross-Border E-Commerce Compliance Check Report</h1>
<p>Law: Cross-border e-commerce rules: customs, product safety, consumer protection, tax (VAT/GST), advertising, and data privacy of destination markets</p>
<p>Engine version: {s.get('version','?')}{' ｜ Local fallback score (cloud rule library not open yet)' if s.get('scored_locally') else ''}</p>
<div class="score-card"><div class="score">{score}</div><div>Compliance score / 100</div>
<div class="summary"><div>✅ Pass<br><b>{s.get('passed_count')}</b></div><div>❌ Fail<br><b>{s.get('failed_count')}</b></div><div>Items<br><b>{s.get('total_items')}</b></div></div></div>
<table><thead><tr><th></th><th>Check</th><th>Authority</th><th>Status</th><th>Recommendation</th></tr></thead><tbody>{rows}</tbody></table>
<p class="note">This report is generated by the CQDev cloud compliance engine for reference only and does not constitute legal advice.</p>
</body></html>"""


def generate_report(payload, format="text"):
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    items = data.get("items", [])
    if format == "json":
        return json.dumps(payload, ensure_ascii=False, indent=2)
    elif format == "html":
        return render_html(data, items)
    return render_text(data, items)


def main():
    parser = argparse.ArgumentParser(description="Cross-Border E-Commerce Compliance Check (free skill + cloud engine)")
    parser.add_argument("--non-interactive", action="store_true", help="free preview mode (list items, no scoring)")
    parser.add_argument("--non-interactive-json", action="store_true", help="free preview JSON mode")
    parser.add_argument("--format", "-f", choices=["text", "json", "html"], default="text")
    parser.add_argument("--output", "-o", help="report output file path")
    args = parser.parse_args()

    # ── free preview (OFFLINE: bundled items, no network) ──
    if args.non_interactive or args.non_interactive_json:
        items = CHECK_ITEMS

    if args.non_interactive_json:
        preview_data = [{"id": it["id"], "name": it["name"], "desc": it["desc"], "ref": it["ref"], "category": it["category"]} for it in items]
        print(json.dumps({"preview": True, "offline": True, "total_items": len(items), "free": True, "needs_api_key": True,
                          "register_page": ACCOUNT_PAGE, "message": "Free skill; scoring runs on the CQDev cloud engine (free API Key).",
                          "preview_items": preview_data}, ensure_ascii=False, indent=2))
        return

    if args.non_interactive:
        print(f"\n🔍 Free preview mode (fully offline) — {len(items)} items; scoring needs a free API Key\n")
        current_cat = ""
        for it in items:
            if it.get("category") != current_cat:
                current_cat = it.get("category", "")
                print(f"\n  ── {current_cat} ──")
            print(f"  • [{it['id']}] {it['name']}  [{it['ref']}]")
            print(f"      {it['desc']}")
        print(f"\n💡 Scoring runs on the cloud engine. Get a free API Key: {ACCOUNT_PAGE}")
        return

    # ── full check: registered Key, or anonymous trial when no Key ──
    items = fetch_rules() or CHECK_ITEMS
    key = load_api_key()
    anon_id = None
    if not key:
        anon_id = load_or_create_anon_id()
        print("🔒 匿名试用模式：本检查将通过 compliancehub.cn 云端引擎真实评分，无需注册可免费试 5 次。")
        print("   你的作答将发送到 compliancehub.cn 云端引擎进行评分，用于生成本次合规报告；详细数据处理见隐私政策 https://compliancehub.cn/privacy.html")
    responses = collect_responses(items)
    submission = build_submission(responses)
    if not submission:
        print("❌ No countable items (all marked not applicable).")
        sys.exit(1)

    print("\n⏳ Submitting to cloud compliance engine for scoring…")
    payload, err = call_evaluate(key, submission, anon_id)
    if err == "ANON_QUOTA_EXHAUSTED":
        reg = _register_page(anon_id)
        if args.format == "json":
            print(json.dumps({"error": "anon_quota_exhausted",
                              "message": "匿名试用额度已用尽（每 skill 5 次），请注册后继续使用",
                              "get_key_page": reg}, ensure_ascii=False, indent=2))
        else:
            print("❌ 匿名试用的 5 次额度已用尽。")
            print("💡 注册即可继续使用（免费 API Key 含 100 次额度）。")
            print(f"👉 打开注册页（已带入你的试用进度）：{reg}")
        sys.exit(2)
    elif err == "RULE_LIB_NOT_OPEN":
        print("⚠️ Cloud rule library not open yet — using local fallback score (same questions, local computation).")
        data = compute_local_score(submission, items)
        payload = {"data": data}
    elif err:
        print(f"❌ {err}")
        sys.exit(1)

    report = generate_report(payload, format=args.format)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ Report saved to: {args.output}")
    else:
        print(report)
    data_out = payload.get("data") or {}
    if anon_id:
        tl = data_out.get("trials_left")
        if tl is not None:
            print(f"\n💡 匿名试用剩余次数：{tl}/5（注册后每把 Key 含 100 次免费额度）。")
    else:
        rem = data_out.get("quota_remaining")
        if rem is not None:
            print(f"\n💡 This Key's remaining free quota: {rem} calls.")


if __name__ == "__main__":
    main()
