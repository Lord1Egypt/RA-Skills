#!/usr/bin/env python3
"""Parse a GPX route and summarize track, waypoint, and segment stats."""

from __future__ import annotations

import argparse
import json
import math
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class TrackPoint:
    lat: float
    lon: float
    ele: float | None
    dist_m: float = 0.0


@dataclass
class Waypoint:
    name: str
    lat: float
    lon: float
    ele: float | None
    track_index: int
    track_km: float
    snap_m: float


@dataclass
class Segment:
    name: str
    from_name: str
    to_name: str
    distance_km: float
    gain_m: float
    loss_m: float
    net_m: float | None
    start_km: float
    end_km: float
    start_ele_m: float | None
    end_ele_m: float | None


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_m = 6_371_000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * radius_m * math.asin(math.sqrt(a))


def child_text(element: ET.Element, child_name: str) -> str | None:
    for child in element:
        if local_name(child.tag) == child_name and child.text:
            return child.text.strip()
    return None


def child_float(element: ET.Element, child_name: str) -> float | None:
    value = child_text(element, child_name)
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_gpx(path: Path) -> tuple[str, list[TrackPoint], list[dict[str, object]]]:
    root = ET.parse(path).getroot()
    route_name = ""
    for child in root:
        if local_name(child.tag) == "name" and child.text:
            route_name = child.text.strip()
            break

    points: list[TrackPoint] = []
    waypoints_raw: list[dict[str, object]] = []

    for element in root.iter():
        name = local_name(element.tag)
        if name == "trkpt":
            points.append(
                TrackPoint(
                    lat=float(element.attrib["lat"]),
                    lon=float(element.attrib["lon"]),
                    ele=child_float(element, "ele"),
                )
            )
        elif name == "wpt":
            waypoints_raw.append(
                {
                    "name": child_text(element, "name") or "",
                    "lat": float(element.attrib["lat"]),
                    "lon": float(element.attrib["lon"]),
                    "ele": child_float(element, "ele"),
                }
            )

    if not points:
        raise ValueError(f"No track points found in {path}")

    for i in range(1, len(points)):
        points[i].dist_m = points[i - 1].dist_m + haversine_m(
            points[i - 1].lat,
            points[i - 1].lon,
            points[i].lat,
            points[i].lon,
        )

    return route_name, points, waypoints_raw


def elevation_at(points: list[TrackPoint], index: int) -> float | None:
    return points[index].ele


def gain_loss(points: list[TrackPoint], start: int, end: int, threshold_m: float) -> tuple[float, float]:
    elevations = [p.ele for p in points[start : end + 1]]
    if any(ele is None for ele in elevations):
        return 0.0, 0.0

    values = [float(ele) for ele in elevations if ele is not None]
    if len(values) < 2:
        return 0.0, 0.0

    gain = 0.0
    loss = 0.0
    ref = values[0]
    high = ref
    low = ref
    trend = 0

    for ele in values[1:]:
        high = max(high, ele)
        low = min(low, ele)

        if trend >= 0 and high - ele >= threshold_m:
            gain += max(0.0, high - ref)
            ref = high
            high = ele
            low = ele
            trend = -1
        elif trend <= 0 and ele - low >= threshold_m:
            loss += max(0.0, ref - low)
            ref = low
            high = ele
            low = ele
            trend = 1

    last = values[-1]
    if trend >= 0:
        gain += max(0.0, last - ref)
    else:
        loss += max(0.0, ref - last)

    return gain, loss


def snap_waypoints(points: list[TrackPoint], raw: Iterable[dict[str, object]]) -> list[Waypoint]:
    snapped: list[Waypoint] = []
    for wp in raw:
        lat = float(wp["lat"])
        lon = float(wp["lon"])
        best_index = min(
            range(len(points)),
            key=lambda i: haversine_m(lat, lon, points[i].lat, points[i].lon),
        )
        snap = haversine_m(lat, lon, points[best_index].lat, points[best_index].lon)
        snapped.append(
            Waypoint(
                name=str(wp.get("name") or f"WP{len(snapped) + 1}"),
                lat=lat,
                lon=lon,
                ele=wp.get("ele") if isinstance(wp.get("ele"), float) else points[best_index].ele,
                track_index=best_index,
                track_km=points[best_index].dist_m / 1000,
                snap_m=snap,
            )
        )
    return sorted(snapped, key=lambda wp: wp.track_index)


def build_segments(
    points: list[TrackPoint],
    waypoints: list[Waypoint],
    threshold_m: float,
) -> list[Segment]:
    segments: list[Segment] = []
    if len(waypoints) < 2:
        return segments

    for start_wp, end_wp in zip(waypoints, waypoints[1:]):
        start = start_wp.track_index
        end = end_wp.track_index
        if end < start:
            start, end = end, start
        gain, loss = gain_loss(points, start, end, threshold_m)
        start_ele = elevation_at(points, start)
        end_ele = elevation_at(points, end)
        net = None if start_ele is None or end_ele is None else end_ele - start_ele
        segments.append(
            Segment(
                name=f"{start_wp.name} -> {end_wp.name}",
                from_name=start_wp.name,
                to_name=end_wp.name,
                distance_km=(points[end].dist_m - points[start].dist_m) / 1000,
                gain_m=gain,
                loss_m=loss,
                net_m=net,
                start_km=points[start].dist_m / 1000,
                end_km=points[end].dist_m / 1000,
                start_ele_m=start_ele,
                end_ele_m=end_ele,
            )
        )
    return segments


def fmt_num(value: float | None, digits: int = 1) -> str:
    if value is None:
        return "-"
    return f"{value:.{digits}f}"


def markdown_report(data: dict[str, object]) -> str:
    summary = data["summary"]
    waypoints = data["waypoints"]
    segments = data["segments"]

    lines = [
        f"# GPX Summary: {summary['name'] or summary['file']}",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Track points | {summary['track_points']} |",
        f"| Distance | {summary['distance_km']:.2f} km |",
        f"| Gain / loss | +{summary['gain_m']:.0f} / -{summary['loss_m']:.0f} m |",
        f"| Min / max elevation | {fmt_num(summary['min_ele_m'], 0)} / {fmt_num(summary['max_ele_m'], 0)} m |",
        "",
    ]

    if waypoints:
        lines += [
            "## Waypoints",
            "",
            "| # | Name | Track km | Elevation | Snap distance |",
            "|---:|---|---:|---:|---:|",
        ]
        for i, wp in enumerate(waypoints, start=1):
            lines.append(
                f"| {i} | {wp['name']} | {wp['track_km']:.2f} | "
                f"{fmt_num(wp['ele'], 0)} m | {wp['snap_m']:.1f} m |"
            )
        lines.append("")

    if segments:
        lines += [
            "## Segments",
            "",
            "| Segment | Distance | Gain / loss | Net | Start-End km |",
            "|---|---:|---:|---:|---:|",
        ]
        for seg in segments:
            net = "-" if seg["net_m"] is None else f"{seg['net_m']:.0f} m"
            lines.append(
                f"| {seg['name']} | {seg['distance_km']:.2f} km | "
                f"+{seg['gain_m']:.0f} / -{seg['loss_m']:.0f} m | {net} | "
                f"{seg['start_km']:.2f}-{seg['end_km']:.2f} |"
            )
        lines.append("")

    return "\n".join(lines)


def build_report(path: Path, threshold_m: float) -> dict[str, object]:
    route_name, points, waypoints_raw = parse_gpx(path)
    total_gain, total_loss = gain_loss(points, 0, len(points) - 1, threshold_m)
    elevations = [p.ele for p in points if p.ele is not None]
    waypoints = snap_waypoints(points, waypoints_raw)
    segments = build_segments(points, waypoints, threshold_m)

    return {
        "summary": {
            "file": str(path),
            "name": route_name,
            "track_points": len(points),
            "distance_km": points[-1].dist_m / 1000,
            "gain_m": total_gain,
            "loss_m": total_loss,
            "min_ele_m": min(elevations) if elevations else None,
            "max_ele_m": max(elevations) if elevations else None,
            "gain_threshold_m": threshold_m,
        },
        "waypoints": [asdict(wp) for wp in waypoints],
        "segments": [asdict(seg) for seg in segments],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gpx", type=Path, help="Path to a GPX file")
    parser.add_argument(
        "--gain-threshold",
        type=float,
        default=3.0,
        help="Elevation reversal threshold in meters for gain/loss smoothing",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format",
    )
    args = parser.parse_args()

    try:
        report = build_report(args.gpx, args.gain_threshold)
    except Exception as exc:
        print(f"read_gpx.py: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(markdown_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
