#!/usr/bin/env python3
"""
parse_products.py — Parse product catalog files into structured JSON
Supports: Excel (.xlsx/.xls), CSV (.csv)

Usage:
    python3 parse_products.py <input_file> [--output <output.json>] [--vertical <apparel|beauty|electronics|general>]

Output: JSON array of normalized product entries
"""

import sys
import json
import argparse
import re
from pathlib import Path

# Try to import optional deps; gracefully degrade
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

RETAIL_CATEGORIES = {
    "apparel": ["上衣", "下装", "裙装", "外套", "内衣", "配件", "鞋帽"],
    "beauty": ["护肤", "彩妆", "香水", "洗护", "男士护理", "母婴护肤"],
    "electronics": ["手机", "电脑", "音频", "影像", "家电", "配件"],
    "general": ["其他"],
}

# Column name aliases — normalized to standard field names
COLUMN_MAP = {
    # SKU
    "sku": "sku", "商品编码": "sku", "商品编号": "sku", "编码": "sku",
    "货号": "sku", "product_id": "sku", "item_no": "sku",
    # Name
    "商品名称": "name", "name": "name", "品名": "name", "产品名称": "name",
    "商品": "name", "product_name": "name", "title": "name",
    # Category
    "分类": "category", "category": "category", "类目": "category",
    "品类": "category", "大类": "category",
    # Price
    "售价": "price", "price": "price", "价格": "price", "零售价": "price",
    "单价": "price", "retail_price": "price",
    # Sale price
    "优惠价": "sale_price", "sale_price": "sale_price", "促销价": "sale_price",
    "折扣价": "sale_price", "活动价": "sale_price",
    # Description
    "描述": "description", "description": "description", "商品描述": "description",
    "详情": "description", "卖点": "description", "产品介绍": "description",
    # Stock
    "库存": "stock", "stock": "stock", "库存数量": "stock", "数量": "stock",
    "qty": "stock", "quantity": "stock",
    # Variants
    "尺码": "sizes", "size": "sizes", "型号": "sizes",
    "颜色": "colors", "color": "colors", "颜色/款式": "colors",
    # Tags
    "标签": "tags", "tags": "tags", "关键词": "tags", "keywords": "tags",
    # Suitable for
    "适合人群": "suitable_for", "适用人群": "suitable_for", "适合": "suitable_for",
}


def normalize_column(col_name: str) -> str:
    """Map raw column name to standard field name."""
    normalized = col_name.strip().lower()
    return COLUMN_MAP.get(col_name.strip(), COLUMN_MAP.get(normalized, col_name.strip().lower()))


def parse_variants(value: str, attribute: str) -> dict:
    """Parse a comma/slash-separated variant string."""
    if not value or str(value).strip() in ("", "nan", "无", "N/A"):
        return {}
    parts = [v.strip() for v in re.split(r"[,，/、;；]", str(value)) if v.strip()]
    return {"attribute": attribute, "values": parts} if parts else {}


def infer_category(name: str, vertical: str) -> str:
    """Infer category from product name when not provided."""
    for cat in RETAIL_CATEGORIES.get(vertical, RETAIL_CATEGORIES["general"]):
        if cat in name:
            return cat
    return "其他"


def clean_price(value) -> float | None:
    """Parse price from string or number."""
    if value is None or str(value).strip() in ("", "nan", "N/A", "无"):
        return None
    cleaned = re.sub(r"[^\d.]", "", str(value))
    try:
        return round(float(cleaned), 2)
    except ValueError:
        return None


def normalize_product(row: dict, vertical: str) -> dict:
    """Normalize a raw row dict into a standard product entry."""
    entry = {
        "sku": str(row.get("sku", "")).strip() or None,
        "name": str(row.get("name", "")).strip() or None,
        "category": str(row.get("category", "")).strip() or None,
        "subcategory": None,
        "description": str(row.get("description", "")).strip() or None,
        "price": clean_price(row.get("price")),
        "sale_price": clean_price(row.get("sale_price")),
        "variants": [],
        "tags": [],
        "suitable_for": [],
        "stock_status": "unknown",
        "stock_qty": None,
        "images": [],
        "_flags": [],
    }

    # Infer missing category
    if not entry["category"] and entry["name"]:
        entry["category"] = infer_category(entry["name"], vertical)
        entry["_flags"].append("category_inferred")

    # Parse variants
    sizes = parse_variants(row.get("sizes", ""), "size")
    if sizes:
        entry["variants"].append(sizes)
    colors = parse_variants(row.get("colors", ""), "color")
    if colors:
        entry["variants"].append(colors)

    # Parse tags
    raw_tags = str(row.get("tags", "")).strip()
    if raw_tags and raw_tags not in ("", "nan"):
        entry["tags"] = [t.strip() for t in re.split(r"[,，;；]", raw_tags) if t.strip()]

    # Parse suitable_for
    raw_suitable = str(row.get("suitable_for", "")).strip()
    if raw_suitable and raw_suitable not in ("", "nan"):
        entry["suitable_for"] = [s.strip() for s in re.split(r"[,，;；]", raw_suitable) if s.strip()]

    # Stock
    raw_stock = row.get("stock")
    if raw_stock is not None and str(raw_stock).strip() not in ("", "nan"):
        try:
            entry["stock_qty"] = int(float(str(raw_stock)))
            entry["stock_status"] = "static_count"
        except ValueError:
            pass

    # Flag low-quality entries
    required = ["sku", "name", "price"]
    missing = [f for f in required if not entry.get(f)]
    if missing:
        entry["_flags"].append(f"missing_required:{','.join(missing)}")

    if not entry.get("description"):
        entry["_flags"].append("missing_description")

    return entry


def parse_csv(filepath: str, vertical: str) -> list[dict]:
    if not HAS_PANDAS:
        raise ImportError("pandas is required: pip install pandas openpyxl")
    df = pd.read_csv(filepath, dtype=str)
    return _parse_dataframe(df, vertical)


def parse_excel(filepath: str, vertical: str) -> list[dict]:
    if not HAS_PANDAS:
        raise ImportError("pandas is required: pip install pandas openpyxl")
    df = pd.read_excel(filepath, dtype=str)
    return _parse_dataframe(df, vertical)


def _parse_dataframe(df, vertical: str) -> list[dict]:
    # Normalize column names
    df.columns = [normalize_column(c) for c in df.columns]
    records = df.to_dict(orient="records")
    return [normalize_product(r, vertical) for r in records]


def score_products(products: list[dict]) -> dict:
    """Compute completeness score for the product list."""
    if not products:
        return {"total": 0, "score": 0, "field_coverage": {}}

    fields = ["sku", "name", "category", "description", "price", "variants", "tags"]
    field_scores = {}
    for field in fields:
        filled = sum(1 for p in products if p.get(field) and p[field] != [] and p[field] != "")
        field_scores[field] = round(filled / len(products) * 100)

    weights = {"sku": 1, "name": 2, "category": 1, "description": 2, "price": 2, "variants": 1, "tags": 1}
    weighted_sum = sum(field_scores.get(f, 0) * w for f, w in weights.items())
    total_weight = sum(weights.values())
    overall = round(weighted_sum / total_weight)

    flagged = [p for p in products if p.get("_flags")]

    return {
        "total_products": len(products),
        "overall_score": overall,
        "field_coverage": field_scores,
        "flagged_count": len(flagged),
        "flagged_samples": [{"name": p.get("name"), "flags": p["_flags"]} for p in flagged[:5]],
    }


def main():
    parser = argparse.ArgumentParser(description="Parse product catalog into structured JSON")
    parser.add_argument("input_file", help="Path to Excel or CSV file")
    parser.add_argument("--output", default=None, help="Output JSON path (default: stdout)")
    parser.add_argument("--vertical", default="general",
                        choices=["apparel", "beauty", "electronics", "general"],
                        help="Retail vertical for category inference")
    parser.add_argument("--score-only", action="store_true", help="Print score summary only")
    args = parser.parse_args()

    filepath = Path(args.input_file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    ext = filepath.suffix.lower()
    if ext in (".xlsx", ".xls"):
        products = parse_excel(str(filepath), args.vertical)
    elif ext == ".csv":
        products = parse_csv(str(filepath), args.vertical)
    else:
        print(f"Error: Unsupported format '{ext}'. Supported: .xlsx, .xls, .csv", file=sys.stderr)
        sys.exit(1)

    score = score_products(products)

    if args.score_only:
        print(json.dumps(score, ensure_ascii=False, indent=2))
        return

    result = {
        "products": products,
        "meta": {
            "source_file": str(filepath),
            "vertical": args.vertical,
            "score": score,
        }
    }

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output_json, encoding="utf-8")
        print(f"✅ Parsed {len(products)} products → {args.output}", file=sys.stderr)
        print(f"   Overall score: {score['overall_score']}/100", file=sys.stderr)
        if score["flagged_count"]:
            print(f"   ⚠️  {score['flagged_count']} products flagged for review", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
