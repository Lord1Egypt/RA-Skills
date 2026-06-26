#!/usr/bin/env python3
import argparse
import getpass
import json
import math
import os
import statistics
import time
from pathlib import Path
from typing import Optional
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

API_URL = "https://api.tibber.com/v1-beta/gql"


def load_local_env_file() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        os.environ.setdefault(key, value.strip())


def load_home_config(config_dirname: str) -> dict:
    """
    Loads ~/.config/<config_dirname>/config.json if present.
    This allows sharing a public skill without committing secrets.
    """
    cfg_path = Path.home() / ".config" / config_dirname / "config.json"
    if not cfg_path.exists():
        return {}
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {cfg_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected object JSON in {cfg_path}.")
    return data


def config_get_str(cfg: dict, *keys: str) -> str | None:
    for k in keys:
        v = cfg.get(k)
        if v is None:
            continue
        if isinstance(v, str):
            v = v.strip()
        else:
            v = str(v).strip()
        if v:
            return v
    return None


def prompt_value(label: str, is_secret: bool) -> str:
    if is_secret:
        return getpass.getpass(f"Enter {label}: ").strip()
    return input(f"Enter {label}: ").strip()


def env_nonempty(name: str) -> str | None:
    value = os.environ.get(name)
    if value is None:
        return None
    value = value.strip()
    return value if value else None


def resolve_credential(
    *,
    env_name: str,
    config: dict,
    config_keys: tuple[str, ...],
    prompt_missing: bool,
    prompt_label: str,
    is_secret: bool,
    default: str | None = None,
) -> str | None:
    env_value = env_nonempty(env_name)
    if env_value:
        return env_value

    cfg_value = config_get_str(config, *config_keys)
    if cfg_value:
        return cfg_value

    if prompt_missing:
        return prompt_value(prompt_label, is_secret=is_secret)

    return default

# Aligns with Tibber developer examples (viewer.homes + subscription + priceInfo).
# today/tomorrow are kept for hourly upcoming prices used by prices/optimize.
QUERY_HOME_PRICES = """
query HomeElectricityPrices {
  viewer {
    homes {
      id
      appNickname
      timeZone
      address {
        address1
        postalCode
        city
      }
      owner {
        firstName
        lastName
        contactInfo {
          email
          mobile
        }
      }
      currentSubscription {
        status
        priceInfo {
          current {
            total
            energy
            tax
            startsAt
            currency
            level
          }
          today {
            total
            energy
            tax
            startsAt
            currency
            level
          }
          tomorrow {
            total
            energy
            tax
            startsAt
            currency
            level
          }
        }
      }
    }
  }
}
"""

QUERY_CONSUMPTION = """
query HomeConsumption($last: Int!) {
  viewer {
    homes {
      id
      appNickname
      consumption(resolution: HOURLY, last: $last) {
        nodes {
          from
          to
          cost
          unitPrice
          unitPriceVAT
          consumption
          consumptionUnit
        }
      }
    }
  }
}
"""


def parse_dt(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def tibber_query(token: str, query: str, variables=None):
    payload = {"query": query, "variables": variables or {}}
    max_attempts = 4
    body = None
    for attempt in range(1, max_attempts + 1):
        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")
            break
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < max_attempts:
                delay = min(2 ** (attempt - 1), 8)
                retry_after = exc.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    delay = max(delay, int(retry_after))
                time.sleep(delay)
                continue
            raise
        except urllib.error.URLError:
            if attempt < max_attempts:
                time.sleep(min(2 ** (attempt - 1), 8))
                continue
            raise
    if body is None:
        raise RuntimeError("No response body returned from Tibber API.")
    data = json.loads(body)
    if data.get("errors"):
        raise RuntimeError(f"Tibber API error: {data['errors']}")
    return data.get("data", {})


def select_home(data, home_id):
    homes = data.get("viewer", {}).get("homes", [])
    if not homes:
        raise RuntimeError("No Tibber homes found for this account.")
    if home_id:
        for h in homes:
            if h.get("id") == home_id:
                return h
        raise RuntimeError(f"Home id not found: {home_id}")
    return homes[0]


def _currency_for_row(row, fallback="EUR"):
    c = row.get("currency") if row else None
    return c if c else fallback


def get_current_and_today_prices(token: str, home_id: str):
    query = """
    query {
        viewer {
            homes {
                id
                current {
                    total
                    energy
                    tax
                    startsAt
                    currency
                }
                today {
                    total
                    energy
                    tax
                    startsAt
                    currency
                }
            }
        }
    }
    """

    try:
        data = tibber_query(token, query)
        home = select_home(data, home_id)
        current_price = home["current"]
        todays_prices = home["today"]
    except Exception:
        fallback_query = """
        query {
            viewer {
                homes {
                    id
                    currentSubscription {
                        priceInfo {
                            current {
                                total
                                energy
                                tax
                                startsAt
                                currency
                            }
                            today {
                                total
                                energy
                                tax
                                startsAt
                                currency
                            }
                        }
                    }
                }
            }
        }
        """
        data = tibber_query(token, fallback_query)
        home = select_home(data, home_id)
        price_info = (home.get("currentSubscription") or {}).get("priceInfo") or {}
        current_price = price_info.get("current")
        todays_prices = price_info.get("today") or []

    return current_price, todays_prices


def fetch_prices(token: str, home_id: Optional[str]):
    if not token:
        raise RuntimeError("TIBBER_ACCESS_TOKEN is missing.")
    data = tibber_query(token, QUERY_HOME_PRICES)
    if not data:
        raise RuntimeError("No data returned from Tibber API.")
    home = select_home(data, home_id)
    sub = home.get("currentSubscription") or {}
    pi = sub.get("priceInfo") or {}
    points = []
    default_currency = "EUR"
    cur_now = pi.get("current") or {}
    if cur_now.get("currency"):
        default_currency = cur_now["currency"]
    for row in (pi.get("today") or []) + (pi.get("tomorrow") or []):
        if row and row.get("startsAt") and row.get("total") is not None:
            points.append(
                {
                    "startsAt": row["startsAt"],
                    "total": float(row["total"]),
                    "energy": float(row["energy"]) if row.get("energy") is not None else None,
                    "tax": float(row["tax"]) if row.get("tax") is not None else None,
                    "currency": _currency_for_row(row, default_currency),
                    "level": row.get("level") or "N/A",
                }
            )
    points.sort(key=lambda x: x["startsAt"])
    return home, pi.get("current"), points


def fetch_consumption(token: str, home_id: Optional[str], lookback_hours: int):
    data = tibber_query(token, QUERY_CONSUMPTION, {"last": int(lookback_hours)})
    home = select_home(data, home_id)
    nodes = (home.get("consumption") or {}).get("nodes") or []
    clean = []
    for n in nodes:
        val = n.get("consumption")
        if val is None:
            continue
        clean.append(
            {
                "from": n.get("from"),
                "to": n.get("to"),
                "consumption": float(val),
                "cost": float(n["cost"]) if n.get("cost") is not None else None,
                "unitPrice": float(n["unitPrice"]) if n.get("unitPrice") is not None else None,
                "unitPriceVAT": float(n["unitPriceVAT"]) if n.get("unitPriceVAT") is not None else None,
                "consumptionUnit": n.get("consumptionUnit"),
            }
        )
    clean.sort(key=lambda x: x.get("from") or "")
    return home, clean


def _home_title(home):
    nick = home.get("appNickname")
    parts = [nick, home.get("id")]
    addr = home.get("address") or {}
    city = addr.get("city")
    if city:
        parts.append(city)
    return " — ".join(p for p in parts if p) or "Home"


def command_prices(args, token, home_id):
    home, current, points = fetch_prices(token, home_id)
    if current is None:
        current, _ = get_current_and_today_prices(token, home_id)
    now = datetime.now(timezone.utc)
    future = [p for p in points if parse_dt(p["startsAt"]).astimezone(timezone.utc) >= now]
    limited = future[: args.hours]
    tz = home.get("timeZone") or ""
    print(f"Home: {_home_title(home)}" + (f" ({tz})" if tz else ""))
    if current:
        cur_curr = current.get("currency") or "EUR"
        print(
            f"Current: {current.get('total')} {cur_curr}/kWh "
            f"at {current.get('startsAt')} (energy={current.get('energy')}, tax={current.get('tax')}, "
            f"level={current.get('level', 'N/A')})"
        )
    print(f"Upcoming prices (next {len(limited)}h):")
    for p in limited:
        print(f"- {p['startsAt']}  {p['total']:.4f} {p['currency']}/kWh  level={p['level']}")


def best_window(points, window_start, window_end, duration_hours):
    scoped = []
    for p in points:
        ts = parse_dt(p["startsAt"])
        if window_start and ts < window_start:
            continue
        if window_end and ts >= window_end:
            continue
        scoped.append({"ts": ts, **p})
    if len(scoped) < duration_hours:
        raise RuntimeError("Not enough hourly points in selected window.")

    best = None
    for i in range(0, len(scoped) - duration_hours + 1):
        chunk = scoped[i : i + duration_hours]
        contiguous = True
        for j in range(1, len(chunk)):
            if int((chunk[j]["ts"] - chunk[j - 1]["ts"]).total_seconds()) != 3600:
                contiguous = False
                break
        if not contiguous:
            continue
        total = sum(x["total"] for x in chunk)
        if best is None or total < best["total"]:
            best = {"total": total, "chunk": chunk}
    if best is None:
        raise RuntimeError("No contiguous price window found.")
    return best


def command_optimize(args, token, home_id):
    home, _, points = fetch_prices(token, home_id)
    if args.duration_hours:
        duration = args.duration_hours
    else:
        if not args.kwh or not args.power_kw:
            raise RuntimeError("Provide either --duration-hours or both --kwh and --power-kw.")
        duration = math.ceil(args.kwh / args.power_kw)
        duration = max(duration, 1)
    ws = parse_dt(args.window_start) if args.window_start else None
    we = parse_dt(args.window_end) if args.window_end else None
    best = best_window(points, ws, we, duration)
    chunk = best["chunk"]
    avg_price = best["total"] / len(chunk)
    est_cost = (args.kwh * avg_price) if args.kwh else None
    print(f"Home: {_home_title(home)}")
    print(f"Optimal {duration}h window:")
    print(f"- Start: {chunk[0]['startsAt']}")
    print(f"- End:   {chunk[-1]['startsAt']} +1h")
    print(f"- Avg price: {avg_price:.4f} {chunk[0]['currency']}/kWh")
    if est_cost is not None:
        print(f"- Estimated energy cost ({args.kwh} kWh): {est_cost:.2f} {chunk[0]['currency']}")
    print("Window details:")
    for p in chunk:
        print(f"  * {p['startsAt']} -> {p['total']:.4f} {p['currency']}/kWh")


def command_anomalies(args, token, home_id):
    home, nodes = fetch_consumption(token, home_id, args.lookback_hours)
    if len(nodes) < 5:
        raise RuntimeError("Not enough consumption points for anomaly detection.")
    latest = nodes[-1]
    hist = [n["consumption"] for n in nodes[:-1]]
    mean = statistics.mean(hist)
    stdev = statistics.pstdev(hist)
    threshold = mean + args.sigma * stdev
    z = ((latest["consumption"] - mean) / stdev) if stdev > 0 else 0.0
    print(f"Home: {_home_title(home)}")
    print(
        f"Latest hour {latest.get('from')} -> {latest.get('to')}: "
        f"{latest['consumption']:.3f} {latest.get('consumptionUnit') or 'kWh'}"
    )
    print(f"Baseline mean={mean:.3f} kWh, stdev={stdev:.3f}, threshold={threshold:.3f}")
    if latest["consumption"] > threshold:
        print(f"ANOMALY: detected spike (z={z:.2f} > {args.sigma:.2f}).")
    else:
        print(f"OK: no anomaly (z={z:.2f}, sigma={args.sigma:.2f}).")


def run_cmd(label: str, cmd: str, execute: bool):
    print(f"{label}: {cmd}")
    if execute:
        subprocess.run(cmd, shell=True, check=True)


def command_control(args, token, home_id):
    home, current, _ = fetch_prices(token, home_id)
    if current is None:
        current, _ = get_current_and_today_prices(token, home_id)
    if not current or current.get("total") is None:
        raise RuntimeError("No current price available.")
    price = float(current["total"])
    cur_curr = current.get("currency") or "EUR"
    print(f"Home: {_home_title(home)}")
    print(f"Current price: {price:.4f} {cur_curr}/kWh at {current.get('startsAt')}")
    execute = args.execute
    if not execute:
        print("Mode: dry-run (add --execute to run commands).")
    action_taken = False
    if args.price_below is not None and price <= args.price_below:
        if args.on_command:
            run_cmd("Price is below threshold -> ON command", args.on_command, execute)
            action_taken = True
    if args.price_above is not None and price >= args.price_above:
        if args.off_command:
            run_cmd("Price is above threshold -> OFF command", args.off_command, execute)
            action_taken = True
    if not action_taken:
        print("No threshold condition matched; no command executed.")


def build_parser():
    p = argparse.ArgumentParser(description="Tibber energy helper for OpenClaw skill.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("prices", help="Show upcoming hourly spot prices.")
    s1.add_argument("--hours", type=int, default=24)
    s1.add_argument(
        "--prompt-missing-secrets",
        action="store_true",
        help="Prompt for missing credentials (interactive mode).",
    )

    s2 = sub.add_parser("optimize", help="Find cheapest contiguous time window.")
    s2.add_argument("--duration-hours", type=int)
    s2.add_argument("--kwh", type=float)
    s2.add_argument("--power-kw", type=float)
    s2.add_argument("--window-start")
    s2.add_argument("--window-end")
    s2.add_argument(
        "--prompt-missing-secrets",
        action="store_true",
        help="Prompt for missing credentials (interactive mode).",
    )

    s3 = sub.add_parser("anomalies", help="Detect hourly consumption anomalies.")
    s3.add_argument("--lookback-hours", type=int, default=168)
    s3.add_argument("--sigma", type=float, default=2.5)
    s3.add_argument(
        "--prompt-missing-secrets",
        action="store_true",
        help="Prompt for missing credentials (interactive mode).",
    )

    s4 = sub.add_parser("control", help="Trigger commands from current price thresholds.")
    s4.add_argument("--price-below", type=float)
    s4.add_argument("--price-above", type=float)
    s4.add_argument("--on-command")
    s4.add_argument("--off-command")
    s4.add_argument("--execute", action="store_true")
    s4.add_argument(
        "--prompt-missing-secrets",
        action="store_true",
        help="Prompt for missing credentials (interactive mode).",
    )

    return p


def main():
    load_local_env_file()
    parser = build_parser()
    args = parser.parse_args()

    prompt_missing = bool(getattr(args, "prompt_missing_secrets", False))
    config = load_home_config("tibber-energy")

    token = resolve_credential(
        env_name="TIBBER_ACCESS_TOKEN",
        config=config,
        config_keys=("access_token", "TIBBER_ACCESS_TOKEN"),
        prompt_missing=prompt_missing,
        prompt_label="TIBBER_ACCESS_TOKEN",
        is_secret=True,
        default=None,
    )
    home_id = resolve_credential(
        env_name="TIBBER_HOME_ID",
        config=config,
        config_keys=("home_id", "TIBBER_HOME_ID"),
        prompt_missing=False,
        prompt_label="TIBBER_HOME_ID",
        is_secret=False,
        default=None,
    )

    if not token:
        cfg_path = Path.home() / ".config" / "tibber-energy" / "config.json"
        raise RuntimeError(
            "Missing Tibber credentials. Set TIBBER_ACCESS_TOKEN as an environment variable, "
            f"or create {cfg_path}. "
            "To be prompted interactively, rerun with --prompt-missing-secrets."
        )

    if args.cmd == "prices":
        command_prices(args, token, home_id)
    elif args.cmd == "optimize":
        command_optimize(args, token, home_id)
    elif args.cmd == "anomalies":
        command_anomalies(args, token, home_id)
    elif args.cmd == "control":
        command_control(args, token, home_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
