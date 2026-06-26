#!/usr/bin/env python3
"""Generate AWS pricing CSVs from a user-supplied service list."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.request import urlopen

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - PyYAML optional
    yaml = None

REGION_TO_LOCATION = {
    "us-east-1": "US East (N. Virginia)",
    "us-east-2": "US East (Ohio)",
    "us-west-1": "US West (N. California)",
    "us-west-2": "US West (Oregon)",
    "ap-northeast-1": "Asia Pacific (Tokyo)",
    "ap-northeast-2": "Asia Pacific (Seoul)",
    "ap-northeast-3": "Asia Pacific (Osaka)",
    "ap-south-1": "Asia Pacific (Mumbai)",
    "ap-south-2": "Asia Pacific (Hyderabad)",
    "ap-southeast-1": "Asia Pacific (Singapore)",
    "ap-southeast-2": "Asia Pacific (Sydney)",
    "ap-southeast-3": "Asia Pacific (Jakarta)",
    "ap-southeast-4": "Asia Pacific (Melbourne)",
    "ap-east-1": "Asia Pacific (Hong Kong)",
    "ap-east-2": "Asia Pacific (Taipei)",
    "ca-central-1": "Canada (Central)",
    "eu-central-1": "EU (Frankfurt)",
    "eu-central-2": "EU (Zurich)",
    "eu-north-1": "EU (Stockholm)",
    "eu-south-1": "EU (Milan)",
    "eu-south-2": "EU (Spain)",
    "eu-west-1": "EU (Ireland)",
    "eu-west-2": "EU (London)",
    "eu-west-3": "EU (Paris)",
    "me-central-1": "Middle East (UAE)",
    "me-south-1": "Middle East (Bahrain)",
    "sa-east-1": "South America (São Paulo)",
}

CACHE_TTL = timedelta(days=30)
BULK_URL_TEMPLATE = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/{service}/current/{region}/index.json"


def normalize_term_type(value: Optional[str]) -> str:
    if not value:
        return "OnDemand"
    value = value.strip()
    if value.lower() in {"reserved", "ri"}:
        return "Reserved"
    return "OnDemand"


@dataclass
class PricingItem:
    name: str
    service_code: str
    filters: Dict[str, str]
    quantity: Decimal
    usage_unit: Optional[str]
    term_type: str
    term_attributes: Dict[str, str]


class PricingError(RuntimeError):
    """Domain-specific error."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate AWS pricing CSV from a service list")
    parser.add_argument("--input", required=True, help="Path to YAML/JSON list with pricing items")
    parser.add_argument("--region", required=True, help="AWS region code (e.g. ap-northeast-1)")
    parser.add_argument("--output", default="aws_pricing.csv", help="Output CSV path")
    parser.add_argument(
        "--source",
        choices=["api", "bulk"],
        default="api",
        help="Use AWS Price List API via aws-cli (api) or local bulk JSON files (bulk)",
    )
    parser.add_argument(
        "--bulk-files",
        nargs="*",
        help="Optional mappings serviceCode=/path/to/bulk.json (overrides cache)",
    )
    parser.add_argument(
        "--cache-dir",
        default="~/.cache/aws-price-csv",
        help="Directory to store cached bulk pricing files",
    )
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Ignore cached bulk files and re-download (aka 即時計算)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load and validate items without fetching pricing",
    )
    return parser.parse_args()


def load_items(path: Path) -> List[PricingItem]:
    text = path.read_text(encoding="utf-8")
    data: Any
    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise PricingError("PyYAML not available; install pyyaml or use JSON input")
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)

    if isinstance(data, dict) and "items" in data:
        items = data["items"]
    else:
        items = data

    parsed: List[PricingItem] = []
    for idx, item in enumerate(items):
        try:
            name = item["name"]
            service_code = item["service_code"]
            filters = item["filters"].copy()
        except KeyError as exc:
            raise PricingError(f"Item #{idx} missing required field: {exc}")

        usage = item.get("usage", {})
        quantity = Decimal(str(usage.get("quantity", 1)))
        usage_unit = usage.get("unit")

        term_info = item.get("term", {})
        term_type = normalize_term_type(term_info.get("type"))
        term_attributes = {k: str(v) for k, v in term_info.get("attributes", {}).items()}

        parsed.append(
            PricingItem(
                name=name,
                service_code=service_code,
                filters={k: str(v) for k, v in filters.items()},
                quantity=quantity,
                usage_unit=usage_unit,
                term_type=term_type,
                term_attributes=term_attributes,
            )
        )
    return parsed


def build_cli_filters(region: str, base_filters: Dict[str, str]) -> List[str]:
    filters = base_filters.copy()
    filters.setdefault("regionCode", region)
    location = REGION_TO_LOCATION.get(region)
    if location:
        filters.setdefault("location", location)
    cli_filters = []
    for field, value in filters.items():
        cli_filters.append(f"Field={field},Type=TERM_MATCH,Value={value}")
    return cli_filters


def term_matches(term: Dict[str, Any], required: Dict[str, str]) -> bool:
    if not required:
        return True
    attrs = term.get("termAttributes", {})
    for key, value in required.items():
        cand = attrs.get(key)
        if cand is None:
            return False
        if str(cand).lower() != str(value).lower():
            return False
    return True


def fetch_price_via_cli(
    service_code: str,
    cli_filters: List[str],
    term_type: str,
    term_attributes: Dict[str, str],
) -> Tuple[Decimal, str, str]:
    cmd = [
        "aws",
        "pricing",
        "get-products",
        "--service-code",
        service_code,
        "--format-version",
        "aws_v1",
        "--max-results",
        "100",
        "--region",
        "us-east-1",
        "--output",
        "json",
    ]
    if cli_filters:
        cmd.extend(["--filters", *cli_filters])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise PricingError(result.stderr.strip() or f"aws-cli failed for {service_code}")

    payload = json.loads(result.stdout)
    for entry in payload.get("PriceList", []):
        product = json.loads(entry)
        terms = product.get("terms", {})
        term_entries = terms.get(term_type)
        if not term_entries:
            continue
        for term in term_entries.values():
            if not term_matches(term, term_attributes):
                continue
            for dim in term.get("priceDimensions", {}).values():
                price = Decimal(dim["pricePerUnit"].get("USD", "0"))
                unit = dim.get("unit", "")
                description = dim.get("description", term.get("sku", ""))
                if price:
                    return price, unit, description
    raise PricingError(f"No {term_type} pricing data returned for {service_code} with given filters")


def parse_bulk_mapping(args_list: Optional[Iterable[str]]) -> Dict[str, Path]:
    mapping: Dict[str, Path] = {}
    if not args_list:
        return mapping
    for entry in args_list:
        if "=" not in entry:
            raise PricingError(f"Invalid bulk mapping '{entry}'. Use ServiceCode=/path/file.json")
        service_code, path = entry.split("=", 1)
        mapping[service_code.strip()] = Path(path).expanduser().resolve()
    return mapping


def ensure_cached_bulk_file(
    service_code: str,
    region: str,
    cache_dir: Path,
    force_refresh: bool,
) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{service_code}_{region}.json"
    if cache_path.exists() and not force_refresh:
        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime, tz=timezone.utc)
        if datetime.now(timezone.utc) - mtime <= CACHE_TTL:
            return cache_path
    url = BULK_URL_TEMPLATE.format(service=service_code, region=region)
    print(f"Downloading bulk pricing: {url}")
    with urlopen(url) as resp, cache_path.open("wb") as fh:
        shutil.copyfileobj(resp, fh)
    return cache_path


def load_bulk_cache(service_code: str, path: Path, cache: Dict[str, Any]) -> Any:
    key = f"{service_code}:{path}"
    if key not in cache:
        cache[key] = json.loads(path.read_text(encoding="utf-8"))
    return cache[key]


def fetch_price_via_bulk(
    service_code: str,
    filters: Dict[str, str],
    term_type: str,
    term_attributes: Dict[str, str],
    dataset: Any,
) -> Tuple[Decimal, str, str]:
    products = dataset.get("products", {})
    terms = dataset.get("terms", {}).get(term_type, {})
    location = filters.get("location")
    for sku, product in products.items():
        attrs = product.get("attributes", {})
        if location and attrs.get("location") != location:
            continue
        if attrs.get("regionCode") and attrs.get("regionCode") != filters.get("regionCode"):
            continue
        matched = True
        for field, value in filters.items():
            if field in {"regionCode", "location"}:
                continue
            if str(attrs.get(field)) != value:
                matched = False
                break
        if not matched:
            continue
        term_entry = terms.get(sku)
        if not term_entry:
            continue
        for term in term_entry.values():
            if not term_matches(term, term_attributes):
                continue
            for dim in term.get("priceDimensions", {}).values():
                price = Decimal(dim["pricePerUnit"].get("USD", "0"))
                unit = dim.get("unit", "")
                description = dim.get("description", sku)
                if price:
                    return price, unit, description
    raise PricingError(f"No matching SKU found in bulk JSON for {service_code}")


def resolve_bulk_path(
    service_code: str,
    region: str,
    user_mapping: Dict[str, Path],
    cache_dir: Path,
    force_refresh: bool,
) -> Path:
    if service_code in user_mapping:
        return user_mapping[service_code]
    return ensure_cached_bulk_file(service_code, region, cache_dir, force_refresh)


def main() -> None:
    args = parse_args()
    items = load_items(Path(args.input))
    bulk_mapping = parse_bulk_mapping(args.bulk_files)
    bulk_cache: Dict[str, Any] = {}
    cache_dir = Path(args.cache_dir).expanduser()

    if args.source == "bulk" and not bulk_mapping and not cache_dir:
        raise PricingError("Bulk mode requires cache-dir or explicit --bulk-files")

    if args.dry_run:
        print(f"Loaded {len(items)} items (dry run). No pricing fetched.")
        return

    rows: List[Dict[str, Any]] = []
    total = Decimal("0")

    for item in items:
        cli_filters = build_cli_filters(args.region, item.filters)
        try:
            if args.source == "bulk":
                bulk_path = resolve_bulk_path(
                    item.service_code,
                    args.region,
                    bulk_mapping,
                    cache_dir,
                    args.force_refresh,
                )
                dataset = load_bulk_cache(item.service_code, bulk_path, bulk_cache)
                merged_filters = dict(regionCode=args.region, location=REGION_TO_LOCATION.get(args.region, ""))
                merged_filters.update(item.filters)
                price, price_unit, description = fetch_price_via_bulk(
                    item.service_code,
                    merged_filters,
                    item.term_type,
                    item.term_attributes,
                    dataset,
                )
            else:
                price, price_unit, description = fetch_price_via_cli(
                    item.service_code,
                    cli_filters,
                    item.term_type,
                    item.term_attributes,
                )
        except PricingError as exc:
            raise PricingError(f"{item.name}: {exc}") from exc

        cost = (item.quantity * price).quantize(Decimal("0.0000001"))
        total += cost
        rows.append(
            {
                "item_name": item.name,
                "service_code": item.service_code,
                "term_type": item.term_type,
                "region": args.region,
                "location": REGION_TO_LOCATION.get(args.region, ""),
                "quantity": f"{item.quantity}",
                "usage_unit": item.usage_unit or price_unit,
                "price_unit": price_unit,
                "price_per_unit_usd": f"{price}",
                "cost_usd": f"{cost}",
                "description": description,
            }
        )

    with Path(args.output).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "item_name",
                "service_code",
                "term_type",
                "region",
                "location",
                "quantity",
                "usage_unit",
                "price_unit",
                "price_per_unit_usd",
                "cost_usd",
                "description",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        writer.writerow(
            {
                "item_name": "TOTAL",
                "service_code": "",
                "term_type": "",
                "region": "",
                "location": "",
                "quantity": "",
                "usage_unit": "",
                "price_unit": "",
                "price_per_unit_usd": "",
                "cost_usd": f"{total}",
                "description": "",
            }
        )

    print(f"Wrote {len(rows)} rows to {args.output}. Total USD {total}")


if __name__ == "__main__":  # pragma: no cover
    try:
        main()
    except PricingError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:  # pragma: no cover
        sys.exit(130)
