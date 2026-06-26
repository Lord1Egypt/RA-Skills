#!/usr/bin/env python3
"""
WHOOP Health Data Sync — Direct API, no third-party SDK.

Usage:
    python3 sync.py                     # Sync today
    python3 sync.py --date 2026-03-07   # Sync specific date
    python3 sync.py --days 7            # Sync last 7 days
    python3 sync.py --weekly            # Generate weekly report
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.error import HTTPError

BASE_DIR = Path(__file__).resolve().parent.parent
HEALTH_DIR = BASE_DIR.parent.parent / "health"  # ~/.openclaw/workspace/health/
DATA_DIR = BASE_DIR / "data"
TOKEN_FILE = DATA_DIR / "tokens.json"

API_BASE = "https://api.prod.whoop.com/developer/v2"
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"


# ── Token Management ──────────────────────────────────────────────

def load_tokens() -> dict:
    if not TOKEN_FILE.exists():
        print("Error: No tokens found. Run auth.py first.", file=sys.stderr)
        sys.exit(1)
    return json.loads(TOKEN_FILE.read_text())


def save_tokens(tokens: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
    os.chmod(TOKEN_FILE, 0o600)


def get_credentials():
    """Get client_id and client_secret from 1Password."""
    try:
        op_token_path = Path.home() / ".openclaw" / ".op-token"
        if op_token_path.exists():
            os.environ["OP_SERVICE_ACCOUNT_TOKEN"] = op_token_path.read_text().strip()
        import subprocess
        result = subprocess.run(
            ["op", "item", "get", "whoop", "--vault", "Agent", "--format", "json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            item = json.loads(result.stdout)
            cid, csec = "", ""
            for f in item.get("fields", []):
                if f.get("purpose") == "USERNAME":
                    cid = f.get("value", "")
                elif f.get("purpose") == "PASSWORD":
                    csec = f.get("value", "")
            if cid and csec:
                return cid, csec
    except Exception:
        pass
    return os.environ.get("WHOOP_CLIENT_ID", ""), os.environ.get("WHOOP_CLIENT_SECRET", "")


def refresh_access_token(tokens: dict) -> dict:
    """Refresh the access token using the refresh token."""
    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        print("Error: No refresh token. Re-run auth.py.", file=sys.stderr)
        sys.exit(1)

    client_id, client_secret = get_credentials()
    if not client_id:
        print("Error: Cannot refresh — no client credentials.", file=sys.stderr)
        sys.exit(1)

    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()

    # Use curl for token exchange to avoid Cloudflare 1010 blocking urllib
    import subprocess as _sp
    curl_r = _sp.run([
        "curl", "-s", "-w", "\n%{http_code}",
        "-X", "POST", TOKEN_URL,
        "-H", "Content-Type: application/x-www-form-urlencoded",
        "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "-d", data.decode(),
    ], capture_output=True, text=True, timeout=15)
    lines = curl_r.stdout.strip().rsplit("\n", 1)
    body = lines[0] if len(lines) > 1 else curl_r.stdout
    status = lines[-1] if len(lines) > 1 else "?"

    if status != "200":
        print(f"Token refresh failed: {status} {body[:300]}", file=sys.stderr)
        sys.exit(1)

    new_tokens = json.loads(body)
    # Preserve refresh token if not returned
    if "refresh_token" not in new_tokens and refresh_token:
        new_tokens["refresh_token"] = refresh_token
    save_tokens(new_tokens)
    return new_tokens


def get_access_token() -> str:
    """Get a valid access token, refreshing if needed."""
    tokens = load_tokens()

    # Try using current token first
    # If it fails with 401, refresh
    return tokens.get("access_token", ""), tokens


# ── API Calls ─────────────────────────────────────────────────────

def api_get(endpoint: str, token: str, params: dict | None = None) -> dict | list:
    """GET from WHOOP API. Returns parsed JSON."""
    if params:
        query = urllib.parse.urlencode(params)
        url = f"{API_BASE}/{endpoint}?{query}"
    else:
        url = f"{API_BASE}/{endpoint}"

    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "User-Agent": "WHOOP-Sync/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        if e.code == 401:
            return {"_auth_error": True}
        print(f"  API error {endpoint}: {e.code}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"  API error {endpoint}: {e}", file=sys.stderr)
        return {}


def api_get_with_refresh(endpoint: str, tokens: dict, params: dict | None = None):
    """API GET with auto token refresh on 401."""
    token = tokens.get("access_token", "")
    result = api_get(endpoint, token, params)

    if isinstance(result, dict) and result.get("_auth_error"):
        print("  Token expired, refreshing...", file=sys.stderr)
        tokens = refresh_access_token(tokens)
        token = tokens.get("access_token", "")
        result = api_get(endpoint, token, params)

    return result, tokens


def get_collection(endpoint: str, tokens: dict, start: str, end: str) -> tuple[list, dict]:
    """Get paginated collection data."""
    params = {"start": start, "end": end, "limit": "25"}
    all_records = []

    while True:
        data, tokens = api_get_with_refresh(endpoint, tokens, params)
        if not isinstance(data, dict):
            break
        records = data.get("records", [])
        all_records.extend(records)
        next_token = data.get("next_token")
        if not next_token or not records:
            break
        params["nextToken"] = next_token

    return all_records, tokens


# ── Formatting Helpers ────────────────────────────────────────────

def fmt_dur(ms: int | float | None) -> str:
    if not ms:
        return "N/A"
    total_sec = int(ms / 1000)
    h, rem = divmod(total_sec, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h}h{m:02d}m"
    return f"{m}m{s:02d}s"


def fmt_pct(val: float | None) -> str:
    if val is None:
        return "N/A"
    return f"{val:.0f}%"


def score_emoji(score: float | None, thresholds=(33, 66)) -> str:
    if score is None:
        return "❓"
    if score >= thresholds[1]:
        return "🟢"
    if score >= thresholds[0]:
        return "🟡"
    return "🔴"


# ── Sync Logic ────────────────────────────────────────────────────

def sync_day(tokens: dict, target_date: date) -> tuple[str | None, dict]:
    """Sync one day of WHOOP data. Returns (markdown_content, updated_tokens)."""
    ds = target_date.isoformat()
    # WHOOP uses ISO datetime for start/end
    start = f"{ds}T00:00:00.000Z"
    end = f"{(target_date + timedelta(days=1)).isoformat()}T00:00:00.000Z"

    print(f"  Syncing {ds}...")
    lines = [f"# WHOOP — {ds}\n"]

    # ── Recovery ──
    recoveries, tokens = get_collection("recovery", tokens, start, end)
    if recoveries:
        r = recoveries[-1]  # Latest
        score = r.get("score", {})
        rec_score = score.get("recovery_score")
        hrv = score.get("hrv_rmssd_milli")
        rhr = score.get("resting_heart_rate")
        spo2 = score.get("spo2_percentage")
        skin_temp = score.get("skin_temp_celsius")

        lines.append(f"## Recovery {score_emoji(rec_score)}")
        lines.append(f"- **Recovery Score**: {fmt_pct(rec_score)}")
        lines.append(f"- **HRV (RMSSD)**: {hrv:.1f} ms" if hrv else "- **HRV**: N/A")
        lines.append(f"- **Resting HR**: {rhr} bpm" if rhr else "- **Resting HR**: N/A")
        if spo2:
            lines.append(f"- **SpO2**: {spo2:.1f}%")
        if skin_temp:
            lines.append(f"- **Skin Temp**: {skin_temp:.1f}°C")
        lines.append("")
    else:
        lines.append("## Recovery\nNo data.\n")

    # ── Sleep ──
    sleeps, tokens = get_collection("activity/sleep", tokens, start, end)
    if sleeps:
        s = sleeps[-1]
        score = s.get("score", {})
        stage = score.get("stage_summary", {})

        lines.append("## Sleep")
        perf = score.get("sleep_performance_percentage")
        if perf is not None:
            lines.append(f"- **Performance**: {score_emoji(perf)} {fmt_pct(perf)}")
        eff = score.get("sleep_efficiency_percentage")
        if eff is not None:
            lines.append(f"- **Efficiency**: {fmt_pct(eff)}")
        consistency = score.get("sleep_consistency_percentage")
        if consistency is not None:
            lines.append(f"- **Consistency**: {fmt_pct(consistency)}")

        total = stage.get("total_in_bed_time_milli")
        if total:
            lines.append(f"- **Total in Bed**: {fmt_dur(total)}")

        # Sleep stages
        light = stage.get("total_light_sleep_time_milli")
        slow = stage.get("total_slow_wave_sleep_time_milli")
        rem = stage.get("total_rem_sleep_time_milli")
        awake = stage.get("total_awake_time_milli")

        if any(x is not None for x in [light, slow, rem, awake]):
            lines.append("- **Stages**:")
            if light:
                lines.append(f"  - Light: {fmt_dur(light)}")
            if slow:
                lines.append(f"  - Deep (SWS): {fmt_dur(slow)}")
            if rem:
                lines.append(f"  - REM: {fmt_dur(rem)}")
            if awake:
                lines.append(f"  - Awake: {fmt_dur(awake)}")

        resp_rate = score.get("respiratory_rate")
        if resp_rate:
            lines.append(f"- **Respiratory Rate**: {resp_rate:.1f} breaths/min")

        # Sleep need / debt
        need = score.get("sleep_needed", {})
        if need:
            baseline = need.get("baseline_milli")
            debt = need.get("need_from_sleep_debt_milli")
            strain_need = need.get("need_from_recent_strain_milli")
            nap_credit = need.get("need_from_recent_nap_milli")
            if baseline:
                total_need = baseline + (debt or 0) + (strain_need or 0) - (nap_credit or 0)
                lines.append(f"- **Sleep Need**: {fmt_dur(total_need)}")
                lines.append(f"  - Baseline: {fmt_dur(baseline)}")
                if debt:
                    lines.append(f"  - Sleep Debt: +{fmt_dur(debt)}")
                if strain_need:
                    lines.append(f"  - Strain Need: +{fmt_dur(strain_need)}")
                if nap_credit:
                    lines.append(f"  - Nap Credit: -{fmt_dur(nap_credit)}")
                # Actual sleep vs need
                actual_sleep = (stage.get("total_in_bed_time_milli", 0)
                                - stage.get("total_awake_time_milli", 0))
                if actual_sleep and total_need:
                    diff_ms = actual_sleep - total_need
                    sign = "+" if diff_ms >= 0 else ""
                    lines.append(f"  - **Balance**: {sign}{fmt_dur(abs(diff_ms))} {'surplus' if diff_ms >= 0 else 'deficit'}")

        lines.append("")
    else:
        lines.append("## Sleep\nNo data.\n")

    # ── Cycles (Strain) ──
    cycles, tokens = get_collection("cycle", tokens, start, end)
    if cycles:
        c = cycles[-1]
        score = c.get("score", {})
        strain = score.get("strain")
        kj = score.get("kilojoule")
        avg_hr = score.get("average_heart_rate")
        max_hr = score.get("max_heart_rate")

        lines.append("## Day Strain")
        if strain is not None:
            lines.append(f"- **Strain**: {strain:.1f} / 21.0")
        if kj is not None:
            lines.append(f"- **Calories**: {kj:.0f} kJ ({kj * 0.239:.0f} kcal)")
        if avg_hr:
            lines.append(f"- **Avg HR**: {avg_hr} bpm")
        if max_hr:
            lines.append(f"- **Max HR**: {max_hr} bpm")
        lines.append("")
    else:
        lines.append("## Day Strain\nNo data.\n")

    # ── Workouts ──
    workouts, tokens = get_collection("activity/workout", tokens, start, end)
    if workouts:
        lines.append("## Workouts")
        for i, w in enumerate(workouts, 1):
            score = w.get("score", {})
            sport_id = w.get("sport_id", "?")
            strain = score.get("strain")
            avg_hr = score.get("average_heart_rate")
            max_hr = score.get("max_heart_rate")
            kj = score.get("kilojoule")
            dur = score.get("duration_milli") or w.get("end") and w.get("start")

            sport_name = w.get("sport_name", "").replace("-", " ").title() or f"Sport {sport_id}"
            # Duration from start/end
            duration_str = ""
            start_t = w.get("start")
            end_t = w.get("end")
            if start_t and end_t:
                try:
                    from datetime import datetime as _dt
                    s_t = _dt.fromisoformat(start_t.replace("Z", "+00:00"))
                    e_t = _dt.fromisoformat(end_t.replace("Z", "+00:00"))
                    dur_ms = (e_t - s_t).total_seconds() * 1000
                    duration_str = f" · {fmt_dur(dur_ms)}"
                except Exception:
                    pass

            lines.append(f"### {sport_name}{duration_str}")
            if strain is not None:
                lines.append(f"- **Strain**: {strain:.1f}")
            if kj is not None:
                lines.append(f"- **Calories**: {kj:.0f} kJ ({kj * 0.239:.0f} kcal)")
            if avg_hr:
                lines.append(f"- **Avg HR**: {avg_hr} bpm")
            if max_hr:
                lines.append(f"- **Max HR**: {max_hr} bpm")
            dist = score.get("distance_meter")
            if dist:
                if dist >= 1000:
                    lines.append(f"- **Distance**: {dist/1000:.2f} km")
                else:
                    lines.append(f"- **Distance**: {dist:.0f} m")
            alt_gain = score.get("altitude_gain_meter")
            alt_change = score.get("altitude_change_meter")
            if alt_gain:
                alt_str = f"- **Elevation**: ↑{alt_gain:.0f}m"
                if alt_change is not None:
                    alt_str += f" (net {alt_change:+.0f}m)"
                lines.append(alt_str)

            # HR zones
            zones = score.get("zone_durations", {}) or score.get("zone_duration", {})
            if zones:
                lines.append("- **HR Zones**:")
                for z_name in ["zone_zero_milli", "zone_one_milli", "zone_two_milli",
                               "zone_three_milli", "zone_four_milli", "zone_five_milli"]:
                    z_val = zones.get(z_name)
                    if z_val:
                        z_label = z_name.replace("_milli", "").replace("zone_", "Zone ").title()
                        lines.append(f"  - {z_label}: {fmt_dur(z_val)}")
            lines.append("")
    else:
        lines.append("## Workouts\nNo workouts.\n")

    content = "\n".join(lines)

    # Only return if we got any actual data
    has_data = any(x for x in [recoveries, sleeps, cycles, workouts])
    return (content if has_data else None), tokens


def generate_weekly(tokens: dict, end_date: date) -> tuple[str, dict]:
    """Generate a weekly summary report."""
    start_date = end_date - timedelta(days=6)
    start = f"{start_date.isoformat()}T00:00:00.000Z"
    end = f"{(end_date + timedelta(days=1)).isoformat()}T00:00:00.000Z"

    lines = [f"# WHOOP Weekly Report — {start_date} → {end_date}\n"]

    # Get all data for the week
    recoveries, tokens = get_collection("recovery", tokens, start, end)
    sleeps, tokens = get_collection("activity/sleep", tokens, start, end)
    cycles, tokens = get_collection("cycle", tokens, start, end)
    workouts, tokens = get_collection("activity/workout", tokens, start, end)

    # Recovery summary
    lines.append("## Recovery")
    if recoveries:
        scores = [r["score"]["recovery_score"] for r in recoveries if r.get("score", {}).get("recovery_score") is not None]
        hrvs = [r["score"]["hrv_rmssd_milli"] for r in recoveries if r.get("score", {}).get("hrv_rmssd_milli") is not None]
        rhrs = [r["score"]["resting_heart_rate"] for r in recoveries if r.get("score", {}).get("resting_heart_rate") is not None]

        if scores:
            lines.append(f"- **Avg Recovery**: {sum(scores)/len(scores):.0f}% (range: {min(scores):.0f}%–{max(scores):.0f}%)")
        if hrvs:
            lines.append(f"- **Avg HRV**: {sum(hrvs)/len(hrvs):.1f} ms (range: {min(hrvs):.1f}–{max(hrvs):.1f})")
        if rhrs:
            lines.append(f"- **Avg RHR**: {sum(rhrs)/len(rhrs):.0f} bpm")
        lines.append(f"- **Days with data**: {len(recoveries)}/7")
    else:
        lines.append("No recovery data.")
    lines.append("")

    # Sleep summary
    lines.append("## Sleep")
    if sleeps:
        perfs = [s["score"]["sleep_performance_percentage"] for s in sleeps
                 if s.get("score", {}).get("sleep_performance_percentage") is not None]
        total_beds = [s["score"]["stage_summary"]["total_in_bed_time_milli"] for s in sleeps
                      if s.get("score", {}).get("stage_summary", {}).get("total_in_bed_time_milli")]

        if perfs:
            lines.append(f"- **Avg Sleep Performance**: {sum(perfs)/len(perfs):.0f}%")
        if total_beds:
            avg_bed_h = (sum(total_beds) / len(total_beds)) / 3600000
            lines.append(f"- **Avg Time in Bed**: {avg_bed_h:.1f}h")
        lines.append(f"- **Nights with data**: {len(sleeps)}/7")
    else:
        lines.append("No sleep data.")
    lines.append("")

    # Strain summary
    lines.append("## Strain")
    if cycles:
        strains = [c["score"]["strain"] for c in cycles if c.get("score", {}).get("strain") is not None]
        cals = [c["score"]["kilojoule"] for c in cycles if c.get("score", {}).get("kilojoule") is not None]

        if strains:
            lines.append(f"- **Avg Day Strain**: {sum(strains)/len(strains):.1f}")
            lines.append(f"- **Max Strain**: {max(strains):.1f}")
        if cals:
            lines.append(f"- **Avg Daily Calories**: {sum(cals)/len(cals)*0.239:.0f} kcal")
    else:
        lines.append("No cycle data.")
    lines.append("")

    # Workouts
    lines.append("## Workouts")
    if workouts:
        lines.append(f"- **Total workouts**: {len(workouts)}")
        total_strain = sum(w["score"]["strain"] for w in workouts if w.get("score", {}).get("strain") is not None)
        lines.append(f"- **Total workout strain**: {total_strain:.1f}")
    else:
        lines.append("No workouts.")
    lines.append("")

    return "\n".join(lines), tokens


# ── Main ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Sync WHOOP health data")
    parser.add_argument("--date", help="Specific date (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, help="Sync last N days")
    parser.add_argument("--weekly", action="store_true", help="Generate weekly report")
    parser.add_argument("--output-dir", help="Output directory (default: health/)")
    args = parser.parse_args()

    tokens = load_tokens()
    out_dir = Path(args.output_dir) if args.output_dir else HEALTH_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.weekly:
        end = date.fromisoformat(args.date) if args.date else date.today()
        content, tokens = generate_weekly(tokens, end)
        out_file = out_dir / f"whoop-weekly-{end.isoformat()}.md"
        out_file.write_text(content)
        save_tokens(tokens)
        print(f"Weekly report: {out_file}")
        print(content)
        return

    if args.days:
        days = [date.today() - timedelta(days=i) for i in range(args.days)]
    elif args.date:
        days = [date.fromisoformat(args.date)]
    else:
        days = [date.today()]

    print(f"Syncing {len(days)} day(s)...")
    for day in sorted(days):
        content, tokens = sync_day(tokens, day)
        if content:
            out_file = out_dir / f"whoop-{day.isoformat()}.md"
            out_file.write_text(content)
            print(f"  ✅ {out_file}")
        else:
            print(f"  ⚠️ No data for {day}")

    save_tokens(tokens)
    print("Done.")


if __name__ == "__main__":
    main()
