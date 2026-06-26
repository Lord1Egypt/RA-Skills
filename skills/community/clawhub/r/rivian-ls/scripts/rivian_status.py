#!/usr/bin/env python3
"""
Fetch Rivian vehicle telemetry via rivian-ls CLI and return structured data.

Usage:
    python3 rivian_status.py [--live] [--format text|json]

Options:
    --live      Fetch fresh data from Rivian API (requires cached credentials)
    --format    Output format: 'text' (default) or 'json'

Exits:
    0  Success
    1  rivian-ls not found or not authenticated
    2  No data available
"""

import argparse
import json
import subprocess
import sys
from typing import Optional


def run_rivian_ls(live: bool = False) -> Optional[dict]:
    """Run rivian-ls and return parsed JSON data."""
    cmd = ["rivian-ls", "status", "--format", "json"]
    if not live:
        cmd.append("--offline")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=20,
            shell=False,
        )
        if result.returncode != 0:
            print(f"Error: rivian-ls exited {result.returncode}: {result.stderr.strip()}", file=sys.stderr)
            return None
        return json.loads(result.stdout)
    except FileNotFoundError:
        print("Error: rivian-ls not found. Install with: go install github.com/pfrederiksen/rivian-ls@latest", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: rivian-ls timed out.", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse rivian-ls output: {e}", file=sys.stderr)
        return None


def format_text(data: dict) -> str:
    """Format vehicle data as human-readable text."""
    lines = []
    lines.append(f"🚙 Rivian  |  {'● Online' if data.get('IsOnline') else '○ Offline'}")
    lines.append(f"Battery:  {data.get('BatteryLevel', 0):.1f}%  |  Range: {data.get('RangeEstimate', 0):.0f} mi")
    lines.append(f"Charge:   {data.get('ChargeState', '—')}  (limit: {data.get('ChargeLimit', '—')}%)")
    if data.get('ChargingRate'):
        lines.append(f"          ⚡ {data['ChargingRate']} kW charging")
    lines.append(f"Locked:   {'Yes 🔒' if data.get('IsLocked') else 'No 🔓'}")
    lines.append(f"Cabin:    {data.get('CabinTemp', 'N/A')}°F")
    lines.append(f"Odometer: {data.get('Odometer', 0):,.0f} mi")
    lines.append(f"Ready:    {data.get('ReadyScore', 0):.0f}%")

    doors = data.get('Doors', {})
    if doors:
        door_states = [
            f"FL:{doors.get('FrontLeft','?')}",
            f"FR:{doors.get('FrontRight','?')}",
            f"RL:{doors.get('RearLeft','?')}",
            f"RR:{doors.get('RearRight','?')}",
        ]
        lines.append(f"Doors:    {' | '.join(door_states)}")

    frunk = data.get('Frunk', 'unknown')
    liftgate = data.get('Liftgate', 'unknown')
    lines.append(f"Frunk: {frunk}  |  Liftgate: {liftgate}")

    tires = data.get('TirePressures', {})
    if tires and tires.get('FrontLeft', 0) > 0:
        lines.append(
            f"Tires:    FL:{tires['FrontLeft']} FR:{tires['FrontRight']} "
            f"RL:{tires['RearLeft']} RR:{tires['RearRight']} PSI"
        )

    loc = data.get('Location')
    if loc and loc.get('Latitude'):
        lines.append(f"Location: {loc['Latitude']:.4f}, {loc['Longitude']:.4f}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Rivian vehicle telemetry")
    parser.add_argument("--live", action="store_true", help="Fetch live data (default: offline cache)")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    data = run_rivian_ls(live=args.live)
    if not data:
        sys.exit(2)

    if args.format == "json":
        print(json.dumps(data, indent=2))
    else:
        print(format_text(data))


if __name__ == "__main__":
    main()
