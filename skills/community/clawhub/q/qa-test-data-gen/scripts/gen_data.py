#!/usr/bin/env python3
"""Test data generator script.
Usage:
    python3 gen_data.py --type users --count 100 --format json --output users.json
    python3 gen_data.py --type orders --count 500 --format csv --output orders.csv
    python3 gen_data.py --type users --count 50 --format sql --table users --output seed.sql
"""
import argparse
import csv
import json
import random
import sys
from datetime import datetime, timedelta

try:
    from faker import Faker
    fake = Faker('zh_CN')
except ImportError:
    print("Error: faker not installed. Run: pip install faker", file=sys.stderr)
    sys.exit(1)


def gen_user(uid):
    return {
        "id": uid,
        "name": fake.name(),
        "email": fake.ascii_free_email(),
        "phone": fake.phone_number(),
        "gender": random.choice(["male", "female"]),
        "birth_date": str(fake.date_of_birth(minimum_age=18, maximum_age=60)),
        "address": fake.address().replace("\n", " "),
        "status": random.choices(["active", "inactive", "banned"], weights=[85, 10, 5])[0],
        "created_at": str(fake.date_time_between(start_date='-2y')),
    }


def gen_order(oid):
    qty = random.randint(1, 10)
    price = round(random.uniform(9.9, 999.9), 2)
    return {
        "id": oid,
        "user_id": random.randint(1, 1000),
        "product_id": random.randint(1, 200),
        "quantity": qty,
        "unit_price": price,
        "total": round(qty * price, 2),
        "status": random.choices(
            ["pending", "paid", "shipped", "delivered", "cancelled"],
            weights=[10, 20, 25, 40, 5])[0],
        "created_at": str(fake.date_time_between(start_date='-6m')),
    }


def gen_product(pid):
    categories = ["电子产品", "服装", "食品", "图书", "家居", "运动", "美妆"]
    return {
        "id": pid,
        "name": fake.catch_phrase(),
        "category": random.choice(categories),
        "price": round(random.uniform(1.0, 9999.0), 2),
        "stock": random.randint(0, 10000),
        "status": random.choices(["on_sale", "off_shelf", "sold_out"], weights=[70, 15, 15])[0],
        "created_at": str(fake.date_time_between(start_date='-1y')),
    }


GENERATORS = {
    "users": gen_user,
    "orders": gen_order,
    "products": gen_product,
}


def to_sql(data, table):
    if not data:
        return ""
    cols = list(data[0].keys())
    lines = [f"INSERT INTO `{table}` ({', '.join(f'`{c}`' for c in cols)}) VALUES"]
    for i, row in enumerate(data):
        vals = []
        for v in row.values():
            if v is None:
                vals.append("NULL")
            elif isinstance(v, (int, float)):
                vals.append(str(v))
            else:
                vals.append("'" + str(v).replace("'", "''") + "'")
        sep = "," if i < len(data) - 1 else ";"
        lines.append(f"  ({', '.join(vals)}){sep}")
    return "\n".join(lines)


def write_output(data, fmt, output, table):
    if fmt == "json":
        content = json.dumps(data, ensure_ascii=False, indent=2, default=str)
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print(content)

    elif fmt == "csv":
        if output:
            with open(output, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        else:
            writer = csv.DictWriter(sys.stdout, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    elif fmt == "sql":
        content = to_sql(data, table)
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(content + "\n")
        else:
            print(content)

    if output:
        print(f"✅ Generated {len(data)} records → {output}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Generate test data")
    parser.add_argument("--type", required=True, choices=GENERATORS.keys(), help="Data type")
    parser.add_argument("--count", type=int, default=100, help="Number of records (default: 100)")
    parser.add_argument("--format", default="json", choices=["json", "csv", "sql"], help="Output format")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    parser.add_argument("--table", help="SQL table name (for sql format)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    args = parser.parse_args()

    if args.seed is not None:
        Faker.seed(args.seed)
        random.seed(args.seed)

    if args.format == "sql" and not args.table:
        args.table = args.type

    gen_fn = GENERATORS[args.type]
    data = [gen_fn(i) for i in range(1, args.count + 1)]
    write_output(data, args.format, args.output, args.table)


if __name__ == "__main__":
    main()
