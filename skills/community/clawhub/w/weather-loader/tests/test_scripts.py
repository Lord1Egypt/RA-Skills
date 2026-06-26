#!/usr/bin/env python3
"""
Weather-fetcher test suite.

Tests:
  1. Utils functions  — get_lat_lon, calculate_evaporation, process_data
  2. Script execution (location) — fetch_historical.py, fetch_forecast.py with location
  3. Script execution (--lat/--lon) — same scripts with --lat and --lon (live API)

Usage:
    python tests/test_scripts.py
"""

import sys
import subprocess
import tempfile
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
_SCRIPTS_DIR = _SKILL_DIR / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR))

PASS = "✅"
FAIL = "❌"


def section(title: str) -> None:
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")


# ---------------------------------------------------------------------------
# 1. Utils functions
# ---------------------------------------------------------------------------

def test_utils() -> bool:
    section("Utils functions")
    try:
        import utils
    except ImportError as e:
        print(f"{FAIL} Could not import utils: {e}")
        return False

    ok = True

    # get_lat_lon (requires network; skip with clear message if unreachable)
    try:
        lat, lon, name = utils.get_lat_lon("Oslo, Norway")
        if lat is None or lon is None:
            print(f"  ⚠ get_lat_lon  →  skipped (location lookup failed, check network/proxy)")
        else:
            print(f"{PASS} get_lat_lon  →  {name} ({lat:.2f}, {lon:.2f})")
    except Exception as e:
        err = str(e).split("\n")[0]
        if "proxy" in err.lower() or "connection" in err.lower() or "403" in err or "Max retries" in err:
            print(f"  ⚠ get_lat_lon  →  skipped (network unreachable: {err[:60]}...)")
        else:
            print(f"{FAIL} get_lat_lon: {e}")
            ok = False

    # calculate_evaporation
    try:
        evap = utils.calculate_evaporation(
            temp=20.0, humidity=60.0, wind_speed=5.0,
            cloud_fraction=50.0, hour_resolution=1.0
        )
        assert evap is not None and evap >= 0, f"invalid value: {evap}"
        print(f"{PASS} calculate_evaporation  →  {evap:.4f} mm")
    except Exception as e:
        print(f"{FAIL} calculate_evaporation: {e}")
        ok = False

    # process_data
    try:
        import pandas as pd
        sample = pd.DataFrame({
            'date': pd.date_range('2026-01-01', periods=3),
            'temp': [10, 12, 11],
            'precip': [2.5, 0.0, 1.0],
            'et0_fao': [1.5, 1.8, 1.6],
            'evaporation': [1.4, 1.7, 1.5],
        })
        result = utils.process_data("historical", sample, kc=1.0)
        assert result is not None and not result.empty
        agg_cols = [c for c in result.columns if c.startswith('agg_')]
        print(f"{PASS} process_data  →  added columns: {', '.join(agg_cols)}")
    except Exception as e:
        print(f"{FAIL} process_data: {e}")
        ok = False

    return ok


# ---------------------------------------------------------------------------
# 2. Script execution (live API)
# ---------------------------------------------------------------------------

def _run_script(script_name: str, args: list) -> bool:
    script_path = _SCRIPTS_DIR / script_name
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        cmd = [sys.executable, str(script_path)] + args
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print(f"{FAIL} {script_name} failed:\n{result.stderr.strip()}")
            return False
        if not result.stdout.strip():
            print(f"{FAIL} {script_name} produced no output")
            return False
        tmp_path.write_text(result.stdout)
        import pandas as pd
        data = pd.read_csv(tmp_path)
        print(f"{PASS} {script_name}  →  {len(data)} rows, columns: {', '.join(data.columns)}")
        return True
    except subprocess.TimeoutExpired:
        print(f"{FAIL} {script_name} timed out (>30 s)")
        return False
    except Exception as e:
        print(f"{FAIL} {script_name}: {e}")
        return False
    finally:
        tmp_path.unlink(missing_ok=True)


def test_scripts() -> bool:
    section("Script execution (live API — location)")
    results = [
        _run_script(s, ["Oslo, Norway", "--format", "csv"])
        for s in ("fetch_historical.py", "fetch_forecast.py")
    ]
    return all(results)


def test_scripts_lat_lon() -> bool:
    section("Script execution (live API — --lat / --lon)")
    # Oslo coordinates
    lat, lon = "59.91", "10.75"
    results = [
        _run_script(s, ["--lat", lat, "--lon", lon, "--format", "csv"])
        for s in ("fetch_historical.py", "fetch_forecast.py")
    ]
    return all(results)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("\n  WEATHER-FETCHER TEST SUITE")

    results = {
        "utils":        test_utils(),
        "scripts":      test_scripts(),
        "scripts_latlon": test_scripts_lat_lon(),
    }

    section("Summary")
    all_ok = True
    for name, ok in results.items():
        icon = PASS if ok else FAIL
        print(f"  {icon}  {name:<10} {'PASS' if ok else 'FAIL'}")
        if not ok:
            all_ok = False
    print()
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
