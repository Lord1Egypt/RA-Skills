# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "searoute>=1.5.0",
#     "folium>=0.18.0",
# ]
# ///
"""Generate the shortest sea route between two ports and output an interactive HTML map."""

import argparse
import json
import sys

import folium
import searoute as sr


def main():
    parser = argparse.ArgumentParser(description="Sea route generator")
    parser.add_argument("--origin-lon", type=float, required=True)
    parser.add_argument("--origin-lat", type=float, required=True)
    parser.add_argument("--dest-lon", type=float, required=True)
    parser.add_argument("--dest-lat", type=float, required=True)
    parser.add_argument("--origin-name", default="Origin")
    parser.add_argument("--dest-name", default="Destination")
    parser.add_argument("--output", default="./sea_route_map.html")
    args = parser.parse_args()

    origin = [args.origin_lon, args.origin_lat]
    destination = [args.dest_lon, args.dest_lat]

    route = sr.searoute(origin, destination)
    coords = route["geometry"]["coordinates"]
    distance_km = route["properties"]["length"]
    duration_h = route["properties"]["duration_hours"]

    waypoints = [
        {"seq": i, "lon": round(lon, 4), "lat": round(lat, 4)}
        for i, (lon, lat) in enumerate(coords, 1)
    ]

    # --- Build HTML map ---
    mid_lat = (args.origin_lat + args.dest_lat) / 2
    mid_lon = (args.origin_lon + args.dest_lon) / 2
    m = folium.Map(location=[mid_lat, mid_lon], zoom_start=5, tiles="CartoDB positron")

    latlon = [[lat, lon] for lon, lat in coords]
    folium.PolyLine(
        latlon,
        weight=4,
        color="#1a73e8",
        opacity=0.85,
        tooltip=f"{args.origin_name} → {args.dest_name}  |  {distance_km:.0f} km  |  ~{duration_h:.1f} h",
    ).add_to(m)

    for i, (lon, lat) in enumerate(coords, 1):
        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color="#1a73e8",
            fill=True,
            fill_color="white",
            fill_opacity=1,
            weight=2,
            tooltip=f"#{i}  ({lon:.4f}, {lat:.4f})",
        ).add_to(m)

    folium.Marker(
        [args.origin_lat, args.origin_lon],
        popup=folium.Popup(
            f"<b>{args.origin_name}</b><br>lon {args.origin_lon}°<br>lat {args.origin_lat}°",
            max_width=200,
        ),
        icon=folium.Icon(color="green", icon="anchor", prefix="fa"),
        tooltip=f"起点：{args.origin_name}",
    ).add_to(m)

    folium.Marker(
        [args.dest_lat, args.dest_lon],
        popup=folium.Popup(
            f"<b>{args.dest_name}</b><br>lon {args.dest_lon}°<br>lat {args.dest_lat}°",
            max_width=200,
        ),
        icon=folium.Icon(color="red", icon="anchor", prefix="fa"),
        tooltip=f"终点：{args.dest_name}",
    ).add_to(m)

    info_html = f"""
    <div style="
        position: fixed; top: 12px; left: 60px; z-index: 9999;
        background: white; padding: 14px 20px; border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,.15); font-family: system-ui, sans-serif;
        font-size: 14px; line-height: 1.6;">
        <div style="font-size:16px; font-weight:700; margin-bottom:6px;">
            ⚓ {args.origin_name} → {args.dest_name}
        </div>
        <div>航线距离：<b>{distance_km:.0f} km</b></div>
        <div>预估时间：<b>{duration_h:.1f} 小时</b></div>
        <div>航路点数：<b>{len(coords)}</b></div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(info_html))

    m.save(args.output)

    result = {
        "origin": {"name": args.origin_name, "lon": args.origin_lon, "lat": args.origin_lat},
        "destination": {"name": args.dest_name, "lon": args.dest_lon, "lat": args.dest_lat},
        "distance_km": round(distance_km, 1),
        "duration_hours": round(duration_h, 1),
        "waypoints": waypoints,
        "html_map": args.output,
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
