#!/usr/bin/env python3
import argparse
import sqlite3
import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser(description="Generate product table image from warehouse DB")
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=40)
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT sku, name, category, warehouse, stock_qty, ROUND(sell_price,2)
        FROM products
        ORDER BY id
        LIMIT ?
        """,
        (args.limit,),
    )
    rows = cur.fetchall()
    conn.close()

    cols = ["SKU", "Name", "Category", "Warehouse", "Stock", "Price"]

    fig, ax = plt.subplots(figsize=(18, 12))
    ax.axis("off")
    ax.set_title(f"Warehouse Products (Top {args.limit})", fontsize=18, pad=20)

    tbl = ax.table(cellText=rows, colLabels=cols, loc="center", cellLoc="left")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1.5)

    for (r, _), cell in tbl.get_celld().items():
        if r == 0:
            cell.set_text_props(weight="bold", color="white")
            cell.set_facecolor("#2E3B4E")
        else:
            cell.set_facecolor("#F7F9FC" if r % 2 == 0 else "white")

    plt.tight_layout()
    plt.savefig(args.out, dpi=180, bbox_inches="tight")
    print(args.out)


if __name__ == "__main__":
    main()
