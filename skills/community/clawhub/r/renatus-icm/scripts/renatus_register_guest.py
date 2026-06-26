#!/usr/bin/env python3
"""
renatus_register_guest.py

Attach to a live authenticated browser session over CDP and register a guest for a
Renatus event using the Back Office API flow recovered from
Dropbox/registration_backoffice.myrenatus.com.har.

Safety:
- Dry-run by default (no write calls).
- Use --execute for the real registration.

Default session behavior:
- If no --session-guid flags are provided and --all-sessions is not set,
  the script defaults to the FIRST event session only. This matches the captured
  HAR registration submit more closely than blindly registering every session.

Examples:
  python3 scripts/renatus_register_guest.py \
    --first-name Test --last-name Guest \
    --email test@example.com --phone '(518) 555-1212' \
    --event-id 0817966f-b9bb-448e-bbb8-b4160115bcc8

  python3 scripts/renatus_register_guest.py \
    --first-name Test --last-name Guest \
    --email test@example.com --phone '(518) 555-1212' \
    --event-id 0817966f-b9bb-448e-bbb8-b4160115bcc8 \
    --all-sessions --execute
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

DEFAULT_EVENT_ID = "0817966f-b9bb-448e-bbb8-b4160115bcc8"
DEFAULT_CDP_URL = "http://127.0.0.1:9222"
DEFAULT_SOURCE_ID = 8115
RENATUS_HOST = "https://backoffice.myrenatus.com"
RENATUS_HOME_URL = f"{RENATUS_HOST}/Home/index#/index"

JS_FLOW = r"""
async (args) => {
  const {
    eventId,
    firstName,
    lastName,
    email,
    phone,
    sourceId,
    execute,
    allSessions,
    explicitSessionGuids,
  } = args;

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
      headers: Object.fromEntries(res.headers.entries()),
    };
  }

  async function getEvent() {
    return api('GET', `${location.origin}/api/queryproxy/execute?url=/api/event/getsavedevent?&Value=${encodeURIComponent(eventId)}`, null, null);
  }

  async function maybeRefreshAuth() {
    const attempts = [];
    const refreshToken = currentAuth?.refresh_token || storageAuth()?.refresh_token || '';
    if (!refreshToken) {
      return {
        refreshed: false,
        attempts,
        refreshTokensTried: 0,
        eventResp: await getEvent(),
      };
    }
    const body = `refresh_token=${encodeURIComponent(refreshToken)}&grant_type=refresh_token`;
    const resp = await api('POST', `${location.origin}/Token`, body, 'application/x-www-form-urlencoded');
    attempts.push({status: resp.status, ok: resp.ok, hasAccessToken: !!resp?.json?.access_token});
    if (resp?.json?.access_token) {
      currentAuth = { ...currentAuth, ...resp.json };
      try {
        localStorage.setItem('auth', JSON.stringify(currentAuth));
      } catch (_) {}
    }
    await sleep(800);
    return {
      refreshed: !!resp?.json?.access_token,
      attempts,
      refreshTokensTried: 1,
      eventResp: await getEvent(),
    };
  }

  let eventResp = await getEvent();
  let refreshMeta = {
    refreshed: false,
    attempts: [],
    refreshTokensTried: 0,
  };

  if (eventResp.status === 401) {
    await sleep(1500);
    eventResp = await getEvent();
  }

  if (eventResp.status === 401) {
    refreshMeta = await maybeRefreshAuth();
    eventResp = refreshMeta.eventResp;
  }

  if (eventResp.status === 401 || !eventResp.ok || !eventResp.json) {
    return {
      ok: false,
      stage: 'auth',
      message: 'Unable to access Renatus event API from the attached browser session.',
      eventStatus: eventResp.status,
      hasXsrf: !!xsrfToken(),
      hasAccessToken: !!accessToken(),
      hasRefreshToken: !!(currentAuth?.refresh_token),
      cookieNames: Object.keys(cookies()),
      localStorageKeys: Object.keys(localStorage || {}),
      refreshMeta,
      currentUrl: location.href,
      title: document.title,
    };
  }

  const eventData = eventResp.json;
  const allEventSessions = (eventData.Sessions || []).map((s) => ({
    sessionGuid: s.SessionGuid,
    name: s.Name,
    startDate: s.StartDate,
    endDate: s.EndDate,
    fee: s.Fee,
    inPersonFee: s.InPersonAttendingFee,
    mediumId: s.MediumId,
    capacity: s.Capacity,
    requireXtreamEducation: !!s.RequireXtreamEducation,
    requireActiveIMA: !!s.RequireActiveIMA,
    requireNoEducation: !!s.RequireNoEducation,
    locationName: s.LocationName,
  }));

  let selectedSessions = [];
  if (explicitSessionGuids && explicitSessionGuids.length) {
    selectedSessions = allEventSessions.filter((s) => explicitSessionGuids.includes(s.sessionGuid));
  } else if (allSessions) {
    selectedSessions = allEventSessions.slice();
  } else {
    selectedSessions = allEventSessions.slice(0, 1);
  }

  if (!selectedSessions.length) {
    return {
      ok: false,
      stage: 'session_selection',
      message: 'No matching event sessions selected.',
      allEventSessions,
    };
  }

  if (!execute) {
    return {
      ok: true,
      stage: 'dry_run',
      eventId,
      eventName: eventData.Name,
      eventStartDate: eventData.EventStartDate,
      eventEndDate: eventData.EventEndDate,
      selectedSessions,
      allEventSessions,
      guest: { firstName, lastName, email, phone },
      defaults: {
        sourceId,
        defaultMode: explicitSessionGuids?.length ? 'explicit-sessions' : (allSessions ? 'all-sessions' : 'first-session-only'),
      },
      auth: {
        hasXsrf: !!xsrfToken(),
        refreshMeta,
      },
    };
  }

  const addCustomerPayload = {
    LeadId: '',
    OwnerId: '',
    CampaignId: '0',
    CampaignStatus: '',
    Phone: { CountryId: 'US', Number: phone },
    Address: {
      AddressLine1: '',
      AddressLine2: '',
      City: '',
      State: '',
      PostalCode: '',
      Country: 'US',
    },
    Email: email,
    FirstName: firstName,
    LastName: lastName,
    SourceId: sourceId,
    IsGuest: false,
    IsCustomer: true,
    MotivationText: '',
    OptIn: true,
    CanSms: true,
    ConsentDate: '',
    IsInternationalCustomer: false,
  };

  const addResp = await api('POST', `${location.origin}/api/commandproxy/execute?url=/api/guestRegistration/addcustomer?`, addCustomerPayload);
  if (!addResp.ok || !addResp.json || !addResp.json.User) {
    return {
      ok: false,
      stage: 'addcustomer',
      message: 'guestRegistration/addcustomer failed',
      response: {
        status: addResp.status,
        text: addResp.text,
      },
    };
  }

  const addedUser = addResp.json.User;
  const ownerId = addedUser.OwnerId || addedUser.EnteredById || null;
  const leadId = addedUser.LeadId || null;

  if (!ownerId || !leadId) {
    return {
      ok: false,
      stage: 'addcustomer-parse',
      message: 'Could not extract ownerId/leadId from addcustomer response',
      response: addResp.json,
    };
  }

  const customerResp = await api('POST', `${location.origin}/api/commandproxy/execute?url=/api/marketingLead/customerbyleadid?`, {
    Value: leadId,
    Key: ownerId,
  });

  if (!customerResp.ok || !customerResp.json || !customerResp.json.CustomerUserId) {
    return {
      ok: false,
      stage: 'customerbyleadid',
      message: 'marketingLead/customerbyleadid failed',
      response: {
        status: customerResp.status,
        text: customerResp.text,
      },
    };
  }

  const guestUserId = customerResp.json.CustomerUserId;

  const feesResp = await api('POST', `${location.origin}/api/commandproxy/execute?url=/api/registration/fees?`, {
    EventId: eventId,
    Guests: [{
      GuestLeadId: leadId,
      GuestUserId: guestUserId,
      Sessions: selectedSessions.map((s) => ({ SessionId: s.sessionGuid })),
    }],
    IsGuestParentRegistering: false,
  });

  const feeGuest = feesResp?.json?.Guests?.[0];
  if (!feesResp.ok || !feeGuest) {
    return {
      ok: false,
      stage: 'fees',
      message: 'registration/fees failed',
      response: {
        status: feesResp.status,
        text: feesResp.text,
      },
    };
  }

  const registrationSessions = (feeGuest.Sessions || []).map((s) => ({
    SessionId: s.SessionId,
    Cost: Number(s.Fees || 0),
    PromoCodeApplied: '',
    QuestionAndAnswers: [],
  }));

  const totalCost = registrationSessions.reduce((sum, s) => sum + (Number(s.Cost) || 0), 0);

  const registerPayload = {
    EventId: eventId,
    Cost: totalCost,
    UserId: ownerId,
    GuestsList: [{
      GuestId: leadId,
      GuestUserId: guestUserId,
      FirstName: firstName,
      LastName: lastName,
      IsGuest: false,
      SessionsList: registrationSessions,
      AttendInPersonChecked: false,
    }],
    PaymentsOptions: [],
    Added: new Date().toISOString(),
    NoOfTickets: 0,
    Seats: [],
  };

  const registerResp = await api('POST', `${location.origin}/api/commandproxy/execute?url=/api/eventRegistration/registerForEvent?`, registerPayload);
  if (!registerResp.ok || !registerResp.json) {
    return {
      ok: false,
      stage: 'registerForEvent',
      message: 'eventRegistration/registerForEvent failed',
      response: {
        status: registerResp.status,
        text: registerResp.text,
      },
      payloadPreview: registerPayload,
    };
  }

  const reg = registerResp.json;
  return {
    ok: true,
    stage: 'registered',
    eventId,
    eventName: eventData.Name,
    selectedSessions,
    guest: {
      firstName,
      lastName,
      email,
      phone,
      leadId,
      guestUserId,
      ownerId,
    },
    fees: {
      totalCost,
      sessions: registrationSessions,
    },
    registration: {
      eventRegistrationContainerId: reg.EventRegistrationContainerId || null,
      guestRegistrationId: reg.GuestsList?.[0]?.RegistrationId || null,
      returnedGuestId: reg.GuestsList?.[0]?.GuestId || null,
      returnedGuestUserId: reg.GuestsList?.[0]?.GuestUserId || null,
      sessionIds: (reg.GuestsList?.[0]?.SessionsList || []).map((s) => s.SessionId),
    },
  };
}
"""


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Register a Renatus guest via a live authenticated browser session.")
    ap.add_argument("--first-name", required=True)
    ap.add_argument("--last-name", required=True)
    ap.add_argument("--email", required=True)
    ap.add_argument("--phone", required=True)
    ap.add_argument("--event-id", default=DEFAULT_EVENT_ID)
    ap.add_argument("--source-id", type=int, default=DEFAULT_SOURCE_ID)
    ap.add_argument("--cdp-url", default=DEFAULT_CDP_URL, help="Chrome/Brave CDP URL, e.g. http://127.0.0.1:9222")
    ap.add_argument("--session-guid", action="append", dest="session_guids", default=[], help="Repeat to select specific session GUID(s)")
    ap.add_argument("--all-sessions", action="store_true", help="Register all event sessions instead of default first session only")
    ap.add_argument("--execute", action="store_true", help="Actually perform registration writes (default: dry-run)")
    ap.add_argument("--json", action="store_true", help="Print raw JSON result")
    ap.add_argument("--timeout-seconds", type=int, default=45)
    return ap.parse_args()


def build_flow_args(args: argparse.Namespace, execute: bool) -> dict:
    return {
        "eventId": args.event_id,
        "firstName": args.first_name,
        "lastName": args.last_name,
        "email": args.email,
        "phone": args.phone,
        "sourceId": args.source_id,
        "execute": bool(execute),
        "allSessions": bool(args.all_sessions),
        "explicitSessionGuids": args.session_guids,
    }


def run_flow(page, args: argparse.Namespace, execute: bool) -> dict:
    target_url = RENATUS_HOME_URL
    page.goto(target_url, wait_until="domcontentloaded", timeout=args.timeout_seconds * 1000)
    try:
        page.wait_for_load_state("networkidle", timeout=5000)
    except Exception:
        pass
    time.sleep(2)
    return page.evaluate(JS_FLOW, build_flow_args(args, execute=execute))


def find_authenticated_page(browser, args: argparse.Namespace):
    diagnostics = []
    if not browser.contexts:
        raise RuntimeError("No browser contexts found on attached CDP browser.")

    for context_index, context in enumerate(browser.contexts):
        page = context.new_page()
        try:
            result = run_flow(page, args, execute=False)
            diagnostics.append({
                "contextIndex": context_index,
                "ok": bool(result.get("ok")),
                "stage": result.get("stage"),
                "eventStatus": result.get("eventStatus"),
                "currentUrl": result.get("currentUrl") or page.url,
                "title": result.get("title") or page.title(),
            })
            if result.get("ok"):
                result["scanDiagnostics"] = diagnostics
                return page, result
        except Exception as e:
            diagnostics.append({
                "contextIndex": context_index,
                "ok": False,
                "stage": "exception",
                "error": str(e),
                "currentUrl": page.url,
            })
        try:
            page.close()
        except Exception:
            pass

    return None, {
        "ok": False,
        "stage": "auth_scan",
        "message": "No authenticated Renatus session found in any attached browser context.",
        "scanDiagnostics": diagnostics,
    }


def human_print(result: dict) -> None:
    if not result.get("ok"):
        print("FAILED")
        print(f"stage: {result.get('stage')}")
        if result.get("message"):
            print(f"message: {result['message']}")
        if result.get("eventStatus") is not None:
            print(f"eventStatus: {result['eventStatus']}")
        if result.get("response"):
            print("response:")
            print(json.dumps(result["response"], indent=2))
        if result.get("allEventSessions"):
            print("availableSessions:")
            for s in result["allEventSessions"]:
                print(f"- {s['sessionGuid']} | {s['name']}")
        return

    if result.get("stage") == "dry_run":
        print("DRY RUN")
        print(f"event: {result.get('eventName')} ({result.get('eventId')})")
        print(f"guest: {result['guest']['firstName']} {result['guest']['lastName']} <{result['guest']['email']}> {result['guest']['phone']}")
        print("selected sessions:")
        for s in result.get("selectedSessions", []):
            print(f"- {s['sessionGuid']} | {s['name']} | {s['startDate']}")
        if result.get("allEventSessions"):
            print("all event sessions:")
            for s in result["allEventSessions"]:
                reqs = []
                if s.get("requireXtreamEducation"):
                    reqs.append("RequireXtreamEducation")
                if s.get("requireActiveIMA"):
                    reqs.append("RequireActiveIMA")
                req_str = f" | requirements={','.join(reqs)}" if reqs else ""
                print(f"- {s['sessionGuid']} | {s['name']} | {s['startDate']}{req_str}")
        return

    print("REGISTERED")
    print(f"event: {result.get('eventName')} ({result.get('eventId')})")
    print(f"guest lead id: {result['guest'].get('leadId')}")
    print(f"guest user id: {result['guest'].get('guestUserId')}")
    print(f"owner id: {result['guest'].get('ownerId')}")
    print(f"container id: {result['registration'].get('eventRegistrationContainerId')}")
    print(f"registration id: {result['registration'].get('guestRegistrationId')}")
    print("session ids:")
    for sid in result["registration"].get("sessionIds", []):
        print(f"- {sid}")


def main() -> int:
    args = parse_args()

    if args.all_sessions and args.session_guids:
        print("Use either --all-sessions or --session-guid, not both.", file=sys.stderr)
        return 2

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(args.cdp_url, timeout=args.timeout_seconds * 1000)
        page, result = find_authenticated_page(browser, args)

        if page is not None and args.execute:
            result = run_flow(page, args, execute=True)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            human_print(result)

        try:
            if page is not None:
                page.close()
        except Exception:
            pass

        return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
