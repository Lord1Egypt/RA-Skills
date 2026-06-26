#!/usr/bin/env python3
import argparse
import json
import sqlite3
from pathlib import Path


def get_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    return [row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]


def pick_first(columns: list[str], *candidates: str) -> str | None:
    for name in candidates:
        if name in columns:
            return name
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--db', required=True)
    args = ap.parse_args()

    db_path = Path(args.db)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        columns = get_columns(conn, 'rides')
        if not columns:
            raise RuntimeError('No rides table found')

        provider_col = pick_first(columns, 'provider')
        currency_col = pick_first(columns, 'currency')
        amount_col = pick_first(columns, 'amount', 'total_amount')
        date_col = pick_first(columns, 'email_date_text', 'trip_date_local', 'requested_at_local', 'receipt_date')
        city_expr = None
        if 'pickup_city' in columns and 'dropoff_city' in columns:
            city_expr = 'coalesce(pickup_city, dropoff_city, "unknown")'
        elif 'pickup_city' in columns:
            city_expr = 'coalesce(pickup_city, "unknown")'
        elif 'dropoff_city' in columns:
            city_expr = 'coalesce(dropoff_city, "unknown")'

        summary = {
            'schema': {
                'columns': columns,
                'date_column': date_col,
                'amount_column': amount_col,
            },
            'total_rides': conn.execute('select count(*) from rides').fetchone()[0],
        }

        if provider_col:
            summary['providers'] = [dict(r) for r in conn.execute(
                f'select {provider_col} as provider, count(*) as rides from rides group by {provider_col} order by rides desc, provider asc'
            ).fetchall()]

        if date_col:
            summary['months'] = [dict(r) for r in conn.execute(
                f"select substr({date_col},1,7) as month, count(*) as rides from rides group by month order by month asc"
            ).fetchall()]

        if currency_col:
            if amount_col:
                summary['currencies'] = [dict(r) for r in conn.execute(
                    f'select coalesce({currency_col}, "unknown") as currency, count(*) as rides, round(sum({amount_col}),2) as total_amount from rides group by coalesce({currency_col}, "unknown") order by rides desc, currency asc'
                ).fetchall()]
            else:
                summary['currencies'] = [dict(r) for r in conn.execute(
                    f'select coalesce({currency_col}, "unknown") as currency, count(*) as rides from rides group by coalesce({currency_col}, "unknown") order by rides desc, currency asc'
                ).fetchall()]

        if provider_col and currency_col:
            if amount_col:
                summary['providers_by_currency'] = [dict(r) for r in conn.execute(
                    f'select {provider_col} as provider, coalesce({currency_col}, "unknown") as currency, count(*) as rides, round(sum({amount_col}),2) as total_amount from rides group by {provider_col}, coalesce({currency_col}, "unknown") order by rides desc, provider asc'
                ).fetchall()]
            else:
                summary['providers_by_currency'] = [dict(r) for r in conn.execute(
                    f'select {provider_col} as provider, coalesce({currency_col}, "unknown") as currency, count(*) as rides from rides group by {provider_col}, coalesce({currency_col}, "unknown") order by rides desc, provider asc'
                ).fetchall()]

        if city_expr:
            summary['cities'] = [dict(r) for r in conn.execute(
                f'select {city_expr} as city, count(*) as rides from rides group by {city_expr} order by rides desc, city asc limit 10'
            ).fetchall()]

        print(json.dumps(summary, ensure_ascii=False, indent=2))
    finally:
        conn.close()


if __name__ == '__main__':
    main()
