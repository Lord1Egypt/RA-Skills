#!/usr/bin/env python3
import argparse
import os
import sqlite3
from datetime import datetime, timedelta

import matplotlib.pyplot as plt


def ensure_out(path: str):
    os.makedirs(path, exist_ok=True)


def stock_status_pie(cur, out_dir):
    cur.execute("SELECT status, COUNT(*) FROM products GROUP BY status")
    rows = cur.fetchall()
    if not rows:
        return
    labels = [r[0] for r in rows]
    values = [r[1] for r in rows]
    plt.figure(figsize=(7, 5))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=130)
    plt.title("Product Stock Status")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "stock_status_pie.png"), dpi=160)
    plt.close()


def revenue_by_category(cur, out_dir):
    cur.execute(
        """
        SELECT p.category, ROUND(SUM(s.qty * s.unit_price * (1 - s.discount_pct/100.0)),2) AS revenue
        FROM sales s
        JOIN products p ON s.product_id = p.id
        GROUP BY p.category
        ORDER BY revenue DESC
        """
    )
    rows = cur.fetchall()
    if not rows:
        return
    x = [r[0] for r in rows]
    y = [r[1] for r in rows]
    plt.figure(figsize=(9, 5))
    plt.bar(x, y)
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Revenue")
    plt.title("Revenue by Category")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "revenue_by_category.png"), dpi=160)
    plt.close()


def daily_profit_30d(cur, out_dir):
    today = datetime.now().date()
    start = today - timedelta(days=29)

    cur.execute(
        """
        SELECT date(s.sold_at) d,
               ROUND(SUM(s.qty * (s.unit_price - p.cost_price)), 2) AS profit
        FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE date(s.sold_at) BETWEEN ? AND ?
        GROUP BY d
        ORDER BY d
        """,
        (str(start), str(today)),
    )
    rows = cur.fetchall()

    values = {d: p for d, p in rows}
    dates = [start + timedelta(days=i) for i in range(30)]
    x = [str(d) for d in dates]
    y = [values.get(str(d), 0) for d in dates]

    plt.figure(figsize=(11, 4.5))
    plt.plot(x, y, marker="o", linewidth=1.8)
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.ylabel("Profit")
    plt.title("Daily Profit (Last 30 Days)")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "daily_profit_30d.png"), dpi=160)
    plt.close()


def missing_products_csv(cur, out_dir):
    cur.execute(
        """
        SELECT sku, name, warehouse, reorder_level
        FROM products
        WHERE stock_qty = 0
        ORDER BY warehouse, sku
        """
    )
    rows = cur.fetchall()
    out = os.path.join(out_dir, "missing_products.csv")
    with open(out, "w", encoding="utf-8") as f:
        f.write("sku,name,warehouse,reorder_level\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")


def product_table_top40(cur, out_dir):
    cur.execute(
        """
        SELECT sku, name, category, warehouse, stock_qty, ROUND(sell_price,2)
        FROM products
        ORDER BY id
        LIMIT 40
        """
    )
    rows = cur.fetchall()
    cols = ["SKU", "Name", "Category", "Warehouse", "Stock", "Price"]

    fig, ax = plt.subplots(figsize=(18, 12))
    ax.axis("off")
    ax.set_title("Warehouse Products (Top 40)", fontsize=18, pad=20)

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
    plt.savefig(os.path.join(out_dir, "product_table_top40.png"), dpi=180, bbox_inches="tight")
    plt.close()


def kpi_summary(cur, out_dir):
    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE stock_qty = 0")
    missing_count = cur.fetchone()[0]

    cur.execute("SELECT ROUND(SUM(qty*unit_price*(1-discount_pct/100.0)),2) FROM sales")
    gross_revenue = cur.fetchone()[0] or 0

    cur.execute(
        """
        SELECT ROUND(SUM(s.qty*(s.unit_price - p.cost_price)),2)
        FROM sales s JOIN products p ON s.product_id = p.id
        """
    )
    gross_profit = cur.fetchone()[0] or 0

    today = datetime.now().strftime("%Y-%m-%d")
    cur.execute(
        """
        SELECT COALESCE(ROUND(SUM(s.qty*(s.unit_price - p.cost_price)),2),0)
        FROM sales s JOIN products p ON s.product_id=p.id
        WHERE date(s.sold_at)=?
        """,
        (today,),
    )
    today_profit = cur.fetchone()[0] or 0

    out = os.path.join(out_dir, "kpi_summary.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Products: {total_products}\n")
        f.write(f"Missing Products: {missing_count}\n")
        f.write(f"Gross Revenue: {gross_revenue}\n")
        f.write(f"Gross Profit: {gross_profit}\n")
        f.write(f"Today's Profit: {today_profit}\n")


def main():
    ap = argparse.ArgumentParser(description="Generate warehouse report images and summary files")
    ap.add_argument("--db", required=True, help="Path to SQLite DB")
    ap.add_argument("--out", required=True, help="Output directory")
    args = ap.parse_args()

    ensure_out(args.out)
    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    stock_status_pie(cur, args.out)
    revenue_by_category(cur, args.out)
    daily_profit_30d(cur, args.out)
    product_table_top40(cur, args.out)
    missing_products_csv(cur, args.out)
    kpi_summary(cur, args.out)

    conn.close()
    print(f"Done. Outputs written to: {args.out}")


if __name__ == "__main__":
    main()
