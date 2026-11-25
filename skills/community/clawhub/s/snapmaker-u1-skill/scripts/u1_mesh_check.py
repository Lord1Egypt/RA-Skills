#!/usr/bin/env python3
"""Basic STL geometry screening for Snapmaker U1 sized parts (stdlib only)."""

from __future__ import annotations

import argparse
import math
import struct
import sys
from collections import Counter
from pathlib import Path

U1_MM = (270.0, 270.0, 270.0)


def read_stl(path: Path):
    data = path.read_bytes()
    if len(data) < 84:
        raise ValueError("file is too short to be an STL")
    count = struct.unpack_from("<I", data, 80)[0]
    if 84 + count * 50 == len(data):
        triangles = []
        offset = 84
        for _ in range(count):
            values = struct.unpack_from("<12fH", data, offset)
            triangles.append((values[3:6], values[6:9], values[9:12]))
            offset += 50
        return triangles

    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("not a valid binary or ASCII STL") from exc
    vertices = []
    for line in text.splitlines():
        words = line.strip().split()
        if len(words) == 4 and words[0].lower() == "vertex":
            try:
                vertices.append(tuple(float(v) for v in words[1:]))
            except ValueError as exc:
                raise ValueError("invalid vertex coordinate") from exc
    if not vertices or len(vertices) % 3:
        raise ValueError("ASCII STL must contain complete triangle vertex triples")
    return [tuple(vertices[i : i + 3]) for i in range(0, len(vertices), 3)]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def edge_key(a, b, precision):
    qa = tuple(round(v / precision) for v in a)
    qb = tuple(round(v / precision) for v in b)
    return (qa, qb) if qa <= qb else (qb, qa)


def inspect(triangles, scale):
    points = [tuple(c * scale for c in p) for tri in triangles for p in tri]
    if not points:
        raise ValueError("STL contains no triangles")
    if any(not math.isfinite(c) for p in points for c in p):
        raise ValueError("STL contains NaN or infinite coordinates")
    mins = tuple(min(p[i] for p in points) for i in range(3))
    maxs = tuple(max(p[i] for p in points) for i in range(3))
    size = tuple(maxs[i] - mins[i] for i in range(3))
    edge_counts = Counter()
    degenerate = 0
    signed_volume = 0.0
    for tri in triangles:
        a, b, c = (tuple(v * scale for v in p) for p in tri)
        ab = tuple(b[i] - a[i] for i in range(3))
        ac = tuple(c[i] - a[i] for i in range(3))
        area2 = math.sqrt(sum(v * v for v in cross(ab, ac)))
        if area2 <= 1e-12:
            degenerate += 1
        signed_volume += (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            + a[1] * (b[2] * c[0] - b[0] * c[2])
            + a[2] * (b[0] * c[1] - b[1] * c[0])
        ) / 6.0
        for p, q in ((a, b), (b, c), (c, a)):
            edge_counts[edge_key(p, q, 1e-5)] += 1
    open_edges = sum(n == 1 for n in edge_counts.values())
    nonmanifold_edges = sum(n > 2 for n in edge_counts.values())
    return {
        "triangles": len(triangles),
        "bounds_min": mins,
        "bounds_max": maxs,
        "size": size,
        "degenerate": degenerate,
        "open_edges": open_edges,
        "nonmanifold_edges": nonmanifold_edges,
        "volume_cm3": abs(signed_volume) / 1000.0 if not open_edges and not nonmanifold_edges else None,
        "fits_nominal_u1": all(size[i] <= U1_MM[i] for i in range(3)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stl", type=Path)
    parser.add_argument("--scale", type=float, default=1.0, help="multiply coordinates by this factor; default assumes mm")
    args = parser.parse_args()
    if args.scale <= 0 or not math.isfinite(args.scale):
        parser.error("--scale must be a finite positive number")
    try:
        report = inspect(read_stl(args.stl), args.scale)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"File: {args.stl}")
    print(f"Triangles: {report['triangles']}")
    print("Bounds (mm): " + ", ".join(f"{v:.3f}" for v in report["bounds_min"]) + " to " + ", ".join(f"{v:.3f}" for v in report["bounds_max"]))
    print("Size (mm): " + " × ".join(f"{v:.3f}" for v in report["size"]))
    print(f"Nominal U1 270 mm envelope: {'PASS' if report['fits_nominal_u1'] else 'FAIL'} (confirm the actual Orca printable polygon)")
    print(f"Degenerate triangles: {report['degenerate']}")
    print(f"Edges used once (open boundary): {report['open_edges']}")
    print(f"Edges used more than twice: {report['nonmanifold_edges']}")
    if report["volume_cm3"] is not None:
        print(f"Enclosed signed-mesh volume: {report['volume_cm3']:.3f} cm³ (geometric solid volume, not sliced filament use)")
    print("Note: this screening does not detect self-intersections, design errors, support needs, or slicer collisions. Review in CAD and Snapmaker Orca.")
    return 1 if report["degenerate"] or report["open_edges"] or report["nonmanifold_edges"] or not report["fits_nominal_u1"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
