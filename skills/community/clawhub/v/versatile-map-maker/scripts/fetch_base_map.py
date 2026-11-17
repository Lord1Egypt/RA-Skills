#!/usr/bin/env python3
"""
Fetch a blank base map (SVG + matching GeoJSON) from the free, public
@highcharts/map-collection npm package.

Usage:
    python fetch_base_map.py --list <search-term>
    python fetch_base_map.py <map-key> <output-dir>

Examples:
    python fetch_base_map.py --list serbia
    python fetch_base_map.py countries/rs/rs-all /home/claude/mapwork
    python fetch_base_map.py --list world
    python fetch_base_map.py custom/world /home/claude/mapwork

The package is ~130MB unpacked but the npm tarball itself is much smaller and
is cached locally after the first fetch, so repeated calls are fast.
"""
import argparse
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

PKG = "@highcharts/map-collection"


def default_cache_dir():
    root = os.environ.get("XDG_CACHE_HOME") or os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()
    return Path(root) / "versatile-map-maker" / "highcharts"


def ensure_tarball(cache_dir):
    cache_dir.mkdir(parents=True, exist_ok=True)
    tarball = cache_dir / "highcharts-map-collection.tgz"
    if tarball.exists():
        return tarball
    if not shutil_which("npm"):
        raise RuntimeError("npm is required for the Highcharts fast path. Use a supplied GeoJSON instead.")
    print(f"Downloading {PKG} (first run only, cached after this)...", file=sys.stderr)
    subprocess.run(
        ["npm", "pack", PKG, "--silent", "--pack-destination", str(cache_dir)],
        check=True, cwd=cache_dir,
    )
    produced = sorted(cache_dir.glob("highcharts-map-collection-*.tgz"))
    if not produced:
        raise RuntimeError("npm pack did not produce a tarball")
    produced[-1].rename(tarball)
    return tarball


def shutil_which(cmd):
    from shutil import which
    return which(cmd) is not None


def list_members(query, cache_dir):
    tb = ensure_tarball(cache_dir)
    query = query.lower()
    with tarfile.open(tb, "r:gz") as tf:
        keys = set()
        for m in tf.getmembers():
            if not m.isfile():
                continue
            name = m.name
            if not (name.endswith(".svg") or name.endswith(".geo.json")):
                continue
            key = name[len("package/"):] if name.startswith("package/") else name
            key = key.replace(".geo.json", "").replace(".svg", "")
            if query in key.lower():
                keys.add(key)
    keys = sorted(keys)
    if not keys:
        print(f"No map keys matched '{query}'. Try a broader term, e.g. the country's "
              f"ISO2 code, 'custom/world', or 'custom/europe'.")
        return
    print(f"{len(keys)} match(es):")
    for k in keys[:40]:
        print(" ", k)
    if len(keys) > 40:
        print(f"  ... and {len(keys) - 40} more")


def fetch(key, out_dir, cache_dir):
    tb = ensure_tarball(cache_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    wanted = {f"package/{key}.svg", f"package/{key}.geo.json"}
    found = []
    with tarfile.open(tb, "r:gz") as tf:
        for m in tf.getmembers():
            if m.name in wanted:
                data = tf.extractfile(m).read()
                out_name = Path(m.name).name
                out_path = out_dir / out_name
                out_path.write_bytes(data)
                found.append(out_path)
    if not found:
        print(f"Nothing found for key '{key}'. Run --list <search-term> to find the "
              f"right key first.", file=sys.stderr)
        sys.exit(1)
    for p in found:
        print(f"Wrote {p}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Fetch Highcharts SVG + GeoJSON map assets.")
    ap.add_argument("key", nargs="?", help="Highcharts map key, e.g. countries/us/us-all")
    ap.add_argument("output_dir", nargs="?", help="Directory for extracted map files")
    ap.add_argument("--list", dest="query", help="Search available map keys")
    ap.add_argument("--cache-dir", default=str(default_cache_dir()))
    args = ap.parse_args()
    cache_dir = Path(args.cache_dir)
    try:
        if args.query:
            list_members(args.query, cache_dir)
        elif args.key and args.output_dir:
            fetch(args.key, args.output_dir, cache_dir)
        else:
            ap.print_help()
            sys.exit(1)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
