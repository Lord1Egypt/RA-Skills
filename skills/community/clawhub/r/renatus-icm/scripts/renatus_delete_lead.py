#!/usr/bin/env python3
"""
renatus_delete_lead.py

Attach to a live authenticated browser session over CDP and delete a lead 
from Renatus by email. This is the unsubscribe companion to renatus_register_guest.py.

Requires: A running Chrome/Brave instance with --remote-debugging-port=9222
          AND an active logged-in session to backoffice.myrenatus.com

Examples:
  # Dry run - find the lead but don't delete
  python3 scripts/renatus_delete_lead.py --email user@example.com

  # Actually delete
  python3 scripts/renatus_delete_lead.py --email user@example.com --execute

  # Delete multiple from a file
  python3 scripts/renatus_delete_lead.py --file unsubscribes.txt --execute
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

DEFAULT_CDP_URL = "http://127.0.0.1:9222"
RENATUS_HOST = "https://backoffice.myrenatus.com"
RENATUS_HOME_URL = f"{RENATUS_HOST}/Home/index#/index"

JS_DELETE_FLOW = r"""
async (args) => {
  const { email, execute } = args;

  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  function cookies() {
    const out = {};
    const raw = document.cookie || '';
    for (const part of raw.split(/;\s*/)) {
      if (!part) continue;
      const idx = part.indexOf('=');
      const k = decodeURIComponent(idx >= 0 ? part.slice(0, idx) : part);
      const v = decodeURIComponent(idx >= 0 ? part.slice(idx + 1) : '');
      out[k] = v;
    }
    return out;
  }

  function storageAuth() {
    try {
      return JSON.parse(localStorage.getItem('auth') || '{}') || {};
    } catch (_) {
      return {};
    }
  }

  let currentAuth = storageAuth();

  function xsrfToken() {
    const ls = localStorage.getItem('__RequestVerificationToken');
    if (ls) return ls;
    const c = cookies();
    for (const [k, v] of Object.entries(c)) {
      if (k.toLowerCase().includes('requestverificationtoken') || k.toLowerCase().includes('xsrf')) return v;
    }
    return null;
  }

  function accessToken() {
    return currentAuth?.access_token || '';
  }

  async function api(method, url, body = null, contentType = 'application/json; charset=UTF-8') {
    const headers = {
      'x-requested-with': 'XMLHttpRequest',
    };
    const xsrf = xsrfToken();
    const bearer = accessToken();
    if (xsrf) headers['x-xsrf-token'] = xsrf;
    if (bearer && !url.endsWith('/Token')) headers['Authorization'] = `Bearer ${bearer}`;
    if (contentType) headers['content-type'] = contentType;

    const res = await fetch(url, {
      method,
      credentials: 'include',
      headers,
      body: body == null ? undefined : (typeof body === 'string' ? body : JSON.stringify(body)),
    });

    const text = await res.text();
    let parsed = null;
    try { parsed = JSON.parse(text); } catch (_) {}

    return {
      ok: res.ok,
      status: res.status,
      url: res.url,
      text,
      json: parsed,
    };
  }

  // Step 1: Search for lead by email
  const searchResp = await api('GET', 
    `${location.origin}/api/queryproxy/execute?url=/api/lead/search?` +
    `&Email=${encodeURIComponent(email)}&CurrentPage=0&PageSize=10`, 
    null, null
  );

  if (!searchResp.ok || !searchResp.json) {
    return {
      ok: false,
      stage: 'search',
      message: 'Failed to search for lead',
      status: searchResp.status,
    };
  }

  const results = searchResp.json.Results || searchResp.json.results || searchResp.json.Data || [];
  
  if (!results.length) {
    return {
      ok: true,
      stage: 'not_found',
      message: 'Lead not found in Renatus (may already be deleted or email mismatch)',
      email,
    };
  }

  const lead = results[0];
  const leadId = lead.Id || lead.id || lead.LeadId || lead.leadId;
  const leadName = lead.Name || lead.FullName || `${lead.FirstName || ''} ${lead.LastName || ''}`.trim();

  if (!leadId) {
    return {
      ok: false,
      stage: 'parse',
      message: 'Could not extract lead ID from search results',
      lead,
    };
  }

  if (!execute) {
    return {
      ok: true,
      stage: 'dry_run',
      message: 'Found lead - would delete if --execute was passed',
      email,
      leadId,
      leadName,
      totalResults: results.length,
    };
  }

  // Step 2: Delete the lead
  // Try multiple endpoints that might work
  const deleteEndpoints = [
    `/api/commandproxy/execute?url=/api/lead/delete?`,
    `/api/commandproxy/execute?url=/api/marketingLead/delete?`,
    `/api/lead/delete?`,
  ];

  let deleteResp = null;
  let lastError = null;

  for (const endpoint of deleteEndpoints) {
    try {
      deleteResp = await api('POST', `${location.origin}${endpoint}`, {
        Value: leadId,
        Key: leadId,
        Id: leadId,
        LeadId: leadId,
      });
      
      if (deleteResp.ok || deleteResp.status === 200) {
        break;
      }
    } catch (e) {
      lastError = e;
    }
  }

  if (!deleteResp || (!deleteResp.ok && deleteResp.status !== 200)) {
    return {
      ok: false,
      stage: 'delete',
      message: 'Failed to delete lead after trying multiple endpoints',
      leadId,
      lastStatus: deleteResp?.status,
      lastError: lastError?.message,
    };
  }

  return {
    ok: true,
    stage: 'deleted',
    email,
    leadId,
    leadName,
    deleteResponse: deleteResp.json || deleteResp.text,
  };
}
"""


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Delete a Renatus lead via a live authenticated browser session.")
    ap.add_argument("--email", help="Email of lead to delete")
    ap.add_argument("--file", help="File containing emails to delete (one per line)")
    ap.add_argument("--cdp-url", default=DEFAULT_CDP_URL, help="Chrome/Brave CDP URL")
    ap.add_argument("--execute", action="store_true", help="Actually delete (default: dry-run)")
    ap.add_argument("--json", action="store_true", help="Print raw JSON result")
    ap.add_argument("--timeout-seconds", type=int, default=45)
    return ap.parse_args()


def delete_single(page, email: str, execute: bool) -> dict:
    return page.evaluate(JS_DELETE_FLOW, {"email": email, "execute": execute})


def find_authenticated_page(browser, args: argparse.Namespace):
    diagnostics = []
    if not browser.contexts:
        raise RuntimeError("No browser contexts found on attached CDP browser.")

    for context_index, context in enumerate(browser.contexts):
        page = context.new_page()
        try:
            page.goto(RENATUS_HOME_URL, wait_until="domcontentloaded", timeout=args.timeout_seconds * 1000)
            page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        time.sleep(2)

        # Quick auth check
        result = page.evaluate("""
          () => {
            const auth = localStorage.getItem('auth');
            const xsrf = localStorage.getItem('__RequestVerificationToken');
            return { hasAuth: !!auth, hasXsrf: !!xsrf, currentUrl: location.href };
          }
        """)

        diagnostics.append({
            "contextIndex": context_index,
            "hasAuth": result.get("hasAuth"),
            "hasXsrf": result.get("hasXsrf"),
            "url": result.get("currentUrl"),
        })

        if result.get("hasAuth") and result.get("hasXsrf"):
            return page, diagnostics

        try:
            page.close()
        except Exception:
            pass

    return None, diagnostics


def main() -> int:
    args = parse_args()

    if not args.email and not args.file:
        print("Either --email or --file is required", file=sys.stderr)
        return 2

    emails = []
    if args.email:
        emails.append(args.email)
    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"File not found: {args.file}", file=sys.stderr)
            return 2
        emails.extend([line.strip() for line in path.read_text().splitlines() if line.strip()])

    print(f"Processing {len(emails)} email(s)...")
    print(f"Mode: {'DELETE' if args.execute else 'DRY RUN'}")
    print()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(args.cdp_url, timeout=args.timeout_seconds * 1000)
        page, diagnostics = find_authenticated_page(browser, args)

        if page is None:
            print("FAILED: No authenticated Renatus session found", file=sys.stderr)
            print("Diagnostics:", json.dumps(diagnostics, indent=2), file=sys.stderr)
            print("\nMake sure you have:", file=sys.stderr)
            print("1. Chrome/Brave running with: --remote-debugging-port=9222", file=sys.stderr)
            print("2. Logged into backoffice.myrenatus.com in that browser", file=sys.stderr)
            return 1

        results = []
        for email in emails:
            print(f"Processing: {email}")
            result = delete_single(page, email, args.execute)
            results.append(result)
            
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                if result.get("ok"):
                    if result.get("stage") == "deleted":
                        print(f"  ✓ Deleted: {result.get('leadName')} (ID: {result.get('leadId')})")
                    elif result.get("stage") == "not_found":
                        print(f"  ℹ Not found (already deleted or different email)")
                    elif result.get("stage") == "dry_run":
                        print(f"  → Would delete: {result.get('leadName')} (ID: {result.get('leadId')})")
                else:
                    print(f"  ✗ Failed: {result.get('stage')} - {result.get('message')}")
            print()

        try:
            page.close()
        except Exception:
            pass

    # Summary
    successful = sum(1 for r in results if r.get("ok"))
    print(f"\nSummary: {successful}/{len(results)} successful")
    
    return 0 if successful == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
