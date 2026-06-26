#!/usr/bin/env python3
"""
Vẽ hình cho đề thi tất cả các môn.
Hỗ trợ: Hình học, đồ thị hàm số, sơ đồ, biểu đồ, timeline.

Cài đặt:
    pip install matplotlib numpy --break-system-packages

Cách dùng:
    python draw-figure.py --type triangle --params '{"A":[0,0],"B":[6,0],"C":[3,4]}'
    python draw-figure.py --type graph --expr "x**2 - 4*x + 3" --range "-1,5"
    python draw-figure.py --type circle --params '{"center":[0,0],"radius":3}'
    python draw-figure.py --type bar --params '{"labels":["A","B","C"],"values":[30,50,20]}'
    python draw-figure.py --type coordinate --params '{"points":{"A":[1,2],"B":[4,3],"C":[2,5]}}'
"""

import sys
import os
import json
import argparse

def check_deps():
    missing = []
    try:
        import matplotlib
    except ImportError:
        missing.append("matplotlib")
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    if missing:
        print(f"Can cai: pip install {' '.join(missing)} --break-system-packages")
        sys.exit(1)

def draw_triangle(params, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    A = params.get("A", [0, 0])
    B = params.get("B", [6, 0])
    C = params.get("C", [3, 4])
    labels = params.get("labels", {"A": A, "B": B, "C": C})

    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    triangle = plt.Polygon([A, B, C], fill=False, edgecolor="black", linewidth=1.5)
    ax.add_patch(triangle)

    offset = 0.3
    for name, point in [("A", A), ("B", B), ("C", C)]:
        dx = -offset if point[0] < (A[0]+B[0]+C[0])/3 else offset
        dy = -offset if point[1] < (A[1]+B[1]+C[1])/3 else offset
        ax.text(point[0]+dx, point[1]+dy, name, fontsize=14, ha="center", va="center", fontweight="bold")

    # Vẽ thêm nếu có: đường cao, trung tuyến, etc.
    if params.get("height"):
        h_from = params["height"].get("from", "C")
        pts = {"A": A, "B": B, "C": C}
        p = pts[h_from]
        # Tính chân đường cao
        others = [v for k,v in pts.items() if k != h_from]
        bx, by = others[0]
        cx, cy = others[1]
        dx_line = cx - bx
        dy_line = cy - by
        t = ((p[0]-bx)*dx_line + (p[1]-by)*dy_line) / (dx_line**2 + dy_line**2)
        foot = [bx + t*dx_line, by + t*dy_line]
        ax.plot([p[0], foot[0]], [p[1], foot[1]], "b--", linewidth=1)
        ax.text(foot[0], foot[1]-offset, "H", fontsize=12, ha="center", color="blue")

    ax.set_aspect("equal")
    margin = 1
    all_x = [A[0], B[0], C[0]]
    all_y = [A[1], B[1], C[1]]
    ax.set_xlim(min(all_x)-margin, max(all_x)+margin)
    ax.set_ylim(min(all_y)-margin, max(all_y)+margin)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight")
    plt.close()

def draw_graph(expr_str, x_range, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from sympy import Symbol, lambdify
    from sympy.parsing.sympy_parser import parse_expr

    x = Symbol("x")
    expr = parse_expr(expr_str)
    f = lambdify(x, expr, "numpy")

    x_vals = np.linspace(x_range[0], x_range[1], 500)
    y_vals = f(x_vals)

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    ax.plot(x_vals, y_vals, "b-", linewidth=2)
    ax.axhline(y=0, color="k", linewidth=0.5)
    ax.axvline(x=0, color="k", linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"y = {expr_str}")
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight")
    plt.close()

def draw_circle(params, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    cx, cy = params.get("center", [0, 0])
    r = params.get("radius", 3)

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    circle = plt.Circle((cx, cy), r, fill=False, edgecolor="black", linewidth=1.5)
    ax.add_patch(circle)
    ax.plot(cx, cy, "ko", markersize=3)
    ax.text(cx+0.2, cy+0.2, "O", fontsize=12, fontweight="bold")

    if params.get("points"):
        for name, pt in params["points"].items():
            ax.plot(pt[0], pt[1], "ko", markersize=4)
            ax.text(pt[0]+0.2, pt[1]+0.2, name, fontsize=12, fontweight="bold")

    ax.set_aspect("equal")
    ax.set_xlim(cx-r-1, cx+r+1)
    ax.set_ylim(cy-r-1, cy+r+1)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color="k", linewidth=0.3)
    ax.axvline(x=0, color="k", linewidth=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight")
    plt.close()

def draw_bar(params, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = params.get("labels", [])
    values = params.get("values", [])
    title = params.get("title", "")
    ylabel = params.get("ylabel", "")

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    colors = ["#4A90D9", "#E8593C", "#5DCAA5", "#F2A623", "#7F77DD"]
    ax.bar(labels, values, color=colors[:len(labels)], edgecolor="black", linewidth=0.5)
    if title:
        ax.set_title(title, fontsize=14)
    if ylabel:
        ax.set_ylabel(ylabel)
    for i, v in enumerate(values):
        ax.text(i, v + max(values)*0.02, str(v), ha="center", fontsize=11)
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight")
    plt.close()

def draw_coordinate(params, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    points = params.get("points", {})
    title = params.get("title", "")
    connect = params.get("connect", False)

    fig, ax = plt.subplots(1, 1, figsize=(7, 6))
    xs, ys = [], []
    for name, pt in points.items():
        ax.plot(pt[0], pt[1], "ko", markersize=5)
        ax.text(pt[0]+0.2, pt[1]+0.2, f"{name}({pt[0]},{pt[1]})", fontsize=10, fontweight="bold")
        xs.append(pt[0])
        ys.append(pt[1])

    if connect and len(xs) > 1:
        xs_c = xs + [xs[0]]
        ys_c = ys + [ys[0]]
        ax.plot(xs_c, ys_c, "b-", linewidth=1)

    ax.axhline(y=0, color="k", linewidth=0.8)
    ax.axvline(x=0, color="k", linewidth=0.8)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    if title:
        ax.set_title(title)
    ax.set_aspect("equal")
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight")
    plt.close()

def draw_pie(params, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = params.get("labels", [])
    values = params.get("values", [])
    title = params.get("title", "")
    colors = ["#4A90D9", "#E8593C", "#5DCAA5", "#F2A623", "#7F77DD", "#D4537E", "#888780"]

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct="%1.1f%%",
        colors=colors[:len(labels)], startangle=90,
        textprops={"fontsize": 11}
    )
    for t in autotexts:
        t.set_fontsize(10)
        t.set_fontweight("bold")
    if title:
        ax.set_title(title, fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight")
    plt.close()

def draw_line(params, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = params.get("labels", [])
    datasets = params.get("datasets", [{"values": params.get("values", []), "name": ""}])
    title = params.get("title", "")
    xlabel = params.get("xlabel", "")
    ylabel = params.get("ylabel", "")
    colors = ["#4A90D9", "#E8593C", "#5DCAA5", "#F2A623"]

    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    for i, ds in enumerate(datasets):
        ax.plot(labels, ds["values"], marker="o", linewidth=2,
                color=colors[i % len(colors)], label=ds.get("name", ""))
        for j, v in enumerate(ds["values"]):
            ax.text(j, v + max(ds["values"]) * 0.02, str(v), ha="center", fontsize=9)
    if any(ds.get("name") for ds in datasets):
        ax.legend()
    if title:
        ax.set_title(title, fontsize=14)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight")
    plt.close()

def draw_rectangle(params, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    A = params.get("A", [0, 0])
    B = params.get("B", [6, 0])
    C = params.get("C", [6, 4])
    D = params.get("D", [0, 4])
    labels = {"A": A, "B": B, "C": C, "D": D}

    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    rect = plt.Polygon([A, B, C, D], fill=False, edgecolor="black", linewidth=1.5, closed=True)
    ax.add_patch(rect)
    offset = 0.3
    for name, point in labels.items():
        cx = (A[0]+B[0]+C[0]+D[0])/4
        cy = (A[1]+B[1]+C[1]+D[1])/4
        dx = -offset if point[0] < cx else offset
        dy = -offset if point[1] < cy else offset
        ax.text(point[0]+dx, point[1]+dy, name, fontsize=14, ha="center", va="center", fontweight="bold")

    if params.get("diagonals"):
        ax.plot([A[0],C[0]], [A[1],C[1]], "b--", linewidth=0.8)
        ax.plot([B[0],D[0]], [B[1],D[1]], "b--", linewidth=0.8)

    ax.set_aspect("equal")
    all_x = [A[0],B[0],C[0],D[0]]
    all_y = [A[1],B[1],C[1],D[1]]
    ax.set_xlim(min(all_x)-1, max(all_x)+1)
    ax.set_ylim(min(all_y)-1, max(all_y)+1)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight")
    plt.close()

def main():
    ap = argparse.ArgumentParser(description="Ve hinh cho de thi")
    ap.add_argument("--type", required=True,
                    choices=["triangle","graph","circle","bar","coordinate","pie","line","rectangle"],
                    help="Loai hinh")
    ap.add_argument("--params", help="Tham so (JSON)")
    ap.add_argument("--expr", help="Bieu thuc ham so (cho graph)")
    ap.add_argument("--range", help="Khoang x (VD: '-5,5')")
    ap.add_argument("--output", "-o", default="figure.png", help="File xuat")
    args = ap.parse_args()

    check_deps()
    params = json.loads(args.params) if args.params else {}

    if args.type == "triangle":
        draw_triangle(params, args.output)
    elif args.type == "graph":
        expr = args.expr or "x**2"
        rng = [float(x) for x in (args.range or "-5,5").split(",")]
        draw_graph(expr, rng, args.output)
    elif args.type == "circle":
        draw_circle(params, args.output)
    elif args.type == "bar":
        draw_bar(params, args.output)
    elif args.type == "coordinate":
        draw_coordinate(params, args.output)
    elif args.type == "pie":
        draw_pie(params, args.output)
    elif args.type == "line":
        draw_line(params, args.output)
    elif args.type == "rectangle":
        draw_rectangle(params, args.output)

    print(f"Da ve hinh: {args.output}")

if __name__ == "__main__":
    main()
