#!/usr/bin/env python3
"""
Invoice Extractor — PDF text extraction, batch file discovery, and CSV ledger management.

Usage:
    python3 extract.py pdf <file>
    python3 extract.py batch <folder>
    python3 extract.py ledger add <json-file-or->
    python3 extract.py ledger edit --id N [--vendor V] [--total T] [--date D] ...
    python3 extract.py ledger delete --id N
    python3 extract.py ledger undo
    python3 extract.py ledger view [--from DATE] [--to DATE] [--category CAT] [--vendor VENDOR] [--format json|csv]
    python3 extract.py ledger summary [--period week|month|year]
    python3 extract.py ledger export --platform <name> [filters]
    python3 extract.py categories
"""

import argparse
import csv
import hashlib
import io
import json
import os
import re
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "categories": {
        "software": ["github", "aws", "google cloud", "vercel", "openai", "anthropic", "azure"],
        "travel": ["ryanair", "airbnb", "hotel", "taxi", "uber", "bus éireann", "irish rail"],
        "office": ["staples", "amazon", "equipment", "monitor", "keyboard"],
        "utilities": ["electric", "gas", "internet", "phone", "vodafone", "virgin", "eir"],
        "food": ["restaurant", "cafe", "tesco", "supervalu", "lidl", "aldi", "insomnia", "starbucks"],
        "professional": ["accountant", "legal", "insurance", "subscription", "membership"],
    },
    "defaults": {
        "currency": "EUR",
        "taxRate": 0.23,
        "dateFormat": "DD/MM/YYYY",
    },
    "ledger": {
        "path": "data/ledger.csv",
        "backupCount": 5,
    },
}

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent


def load_config(config_path: str | None = None) -> dict:
    """Load config from file, falling back through search paths then defaults."""
    candidates = []
    if config_path:
        candidates.append(Path(config_path))
    candidates.extend([
        SCRIPT_DIR / "expense-config.json",
        SKILL_DIR / "expense-config.json",
    ])
    for p in candidates:
        if p.is_file():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                print(f"Warning: failed to load config {p}: {e}", file=sys.stderr)
                break
    return DEFAULT_CONFIG


def resolve_ledger_path(config: dict) -> Path:
    """Resolve the ledger CSV path relative to the skill directory."""
    raw = config.get("ledger", {}).get("path", "data/ledger.csv")
    p = Path(raw)
    if not p.is_absolute():
        p = SKILL_DIR / p
    return p


# ---------------------------------------------------------------------------
# PDF text extraction
# ---------------------------------------------------------------------------

def extract_pdf_text(filepath: str) -> str:
    """Extract text from a PDF file. Returns text string or raises."""
    # Try pdfplumber first
    try:
        import pdfplumber
        texts = []
        with pdfplumber.open(filepath) as pdf:
            for i, page in enumerate(pdf.pages):
                t = page.extract_text()
                if t:
                    texts.append(t)
        if texts:
            return "\n".join(texts)
        print("Warning: pdfplumber extracted no text (possibly a scanned PDF)", file=sys.stderr)
        print("Consider extracting the first page as an image and using the agent's vision tool.", file=sys.stderr)
        return ""
    except ImportError:
        pass
    except Exception as e:
        print(f"Warning: pdfplumber failed: {e}", file=sys.stderr)

    # Fallback: PyPDF2
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(filepath)
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                raise RuntimeError("PDF is encrypted and requires a password.")
        texts = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                texts.append(t)
        if texts:
            return "\n".join(texts)
        return ""
    except ImportError:
        pass
    except Exception as e:
        print(f"Warning: PyPDF2 failed: {e}", file=sys.stderr)

    print("Error: no PDF library available. Install one with:", file=sys.stderr)
    print("  pip install pdfplumber", file=sys.stderr)
    print("  # or: pip install PyPDF2", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Batch file discovery
# ---------------------------------------------------------------------------

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff"}
PDF_EXTENSIONS = {".pdf"}


def batch_scan(folder: str) -> list[dict]:
    """Recursively find all PDF and image files in a folder."""
    root = Path(folder)
    if not root.is_dir():
        print(f"Error: {folder} is not a directory", file=sys.stderr)
        sys.exit(1)

    files = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in PDF_EXTENSIONS:
            ftype = "pdf"
        elif ext in IMAGE_EXTENSIONS:
            ftype = "image"
        else:
            continue
        stat = p.stat()
        files.append({
            "path": str(p.resolve()),
            "name": p.name,
            "size": stat.st_size,
            "type": ftype,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        })

    # Sort newest first
    files.sort(key=lambda x: x["modified"], reverse=True)
    return files


# ---------------------------------------------------------------------------
# Ledger management
# ---------------------------------------------------------------------------

LEDGER_HEADERS = [
    "id", "date", "vendor", "description", "category",
    "subtotal", "tax", "total", "currency", "source_file", "extracted_at",
    "dedup_hash",
]


def auto_categorize(vendor: str, description: str, config: dict) -> str:
    """Match vendor/description against category keywords."""
    search_text = f"{vendor} {description}".lower()
    categories = config.get("categories", {})
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw.lower() in search_text:
                return cat
    return "uncategorized"


def backup_ledger(ledger_path: Path, backup_count: int):
    """Create a rotated backup of the ledger file."""
    if not ledger_path.exists():
        return
    for i in range(backup_count, 0, -1):
        src = ledger_path if i == 1 else ledger_path.with_suffix(f".csv.bak.{i-1}")
        dst = ledger_path.with_suffix(f".csv.bak.{i}")
        if src.exists():
            shutil.copy2(src, dst)


def next_id(ledger_path: Path) -> int:
    """Get the next sequential ID for the ledger."""
    if not ledger_path.exists():
        return 1
    try:
        with open(ledger_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if not rows:
                return 1
            return max((int(r["id"]) for r in rows if r.get("id", "").isdigit()), default=0) + 1
    except Exception:
        return 1


def read_ledger(ledger_path: Path) -> list[dict]:
    """Read the full ledger CSV into a list of dicts."""
    if not ledger_path.exists():
        return []
    try:
        with open(ledger_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f"Error reading ledger: {e}", file=sys.stderr)
        return []


def ensure_ledger_headers(ledger_path: Path):
    """Ensure the ledger CSV has the latest headers. Returns True if file was migrated."""
    if not ledger_path.exists():
        return False
    try:
        with open(ledger_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            current_headers = next(reader, None)
        if current_headers is None:
            return False
        # Check if dedup_hash column is missing
        if "dedup_hash" not in current_headers:
            # Migrate: rewrite file with new header row
            backup_count = 5  # default, config not available here
            backup_ledger(ledger_path, backup_count)
            rows = []
            with open(ledger_path, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row["dedup_hash"] = ""
                    rows.append(row)
            with open(ledger_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=LEDGER_HEADERS, extrasaction="ignore",
                                        quoting=csv.QUOTE_MINIMAL)
                writer.writeheader()
                writer.writerows(rows)
            return True
    except Exception as e:
        print(f"Warning: could not check ledger headers: {e}", file=sys.stderr)
    return False


def write_ledger_entry(ledger_path: Path, entry: dict, config: dict):
    """Append an entry to the ledger CSV."""
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    backup_count = config.get("ledger", {}).get("backupCount", 5)
    backup_ledger(ledger_path, backup_count)

    file_exists = ledger_path.exists()
    with open(ledger_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LEDGER_HEADERS, extrasaction="ignore",
                                quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)


def write_ledger_all(ledger_path: Path, rows: list[dict], config: dict):
    """Rewrite the entire ledger CSV with the given rows."""
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    backup_count = config.get("ledger", {}).get("backupCount", 5)
    backup_ledger(ledger_path, backup_count)

    with open(ledger_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LEDGER_HEADERS, extrasaction="ignore",
                                quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def compute_dedup_hash(vendor: str, date: str, total: float) -> str:
    """Compute a 12-char hex hash for duplicate detection."""
    payload = f"{vendor}|{date}|{total:.2f}"
    return hashlib.sha256(payload.encode()).hexdigest()[:12]


def load_existing_hashes(ledger_path: Path) -> set[str]:
    """Load all dedup hashes from existing ledger entries."""
    hashes = set()
    if not ledger_path.exists():
        return hashes
    try:
        with open(ledger_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                h = row.get("dedup_hash", "").strip()
                if h:
                    hashes.add(h)
    except Exception:
        pass
    return hashes


def normalize_date(date_str: str, config: dict) -> str:
    """Normalize a date string to YYYY-MM-DD format."""
    date_val = str(date_str)
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y", "%Y/%m/%d",
                "%d %b %Y", "%d %B %Y", "%b %d %Y", "%B %d %Y"):
        try:
            return datetime.strptime(date_val, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    # If we can't parse it, return as-is (validation will catch bad dates elsewhere)
    return date_val


def ledger_add(json_input: str | None, config: dict, source_file: str | None = None,
              force: bool = False):
    """Add an entry to the ledger from JSON input."""
    # Read JSON
    try:
        if json_input and json_input != "-":
            with open(json_input, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = json.load(sys.stdin)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate required fields
    for field in ("vendor", "total", "date"):
        if field not in data or not data[field]:
            print(f"Error: missing required field '{field}'", file=sys.stderr)
            sys.exit(1)

    ledger_path = resolve_ledger_path(config)

    # Normalize date
    date_val = normalize_date(data["date"], config)

    # Normalize total
    try:
        total_val = float(data["total"])
    except (ValueError, TypeError):
        print(f"Error: invalid total value '{data['total']}'", file=sys.stderr)
        sys.exit(1)

    vendor_val = str(data["vendor"]).strip()

    # Duplicate detection
    if not force:
        ensure_ledger_headers(ledger_path)
        existing_hashes = load_existing_hashes(ledger_path)
        new_hash = compute_dedup_hash(vendor_val, date_val, total_val)
        if new_hash in existing_hashes:
            print(f"Duplicate detected: {vendor_val} | {date_val} | {total_val:.2f} (hash: {new_hash})", file=sys.stderr)
            print(f"Entry skipped. Use --force to add anyway.", file=sys.stderr)
            sys.exit(2)
    else:
        new_hash = compute_dedup_hash(vendor_val, date_val, total_val)

    # Auto-categorize if not specified
    category = data.get("category") or auto_categorize(
        vendor_val, data.get("description", ""), config
    )

    entry = {
        "id": next_id(ledger_path),
        "date": date_val,
        "vendor": vendor_val,
        "description": str(data.get("description", "")).strip(),
        "category": category,
        "subtotal": str(data.get("subtotal", "")),
        "tax": str(data.get("tax", "")),
        "total": str(total_val),
        "currency": str(data.get("currency", config.get("defaults", {}).get("currency", "EUR"))),
        "source_file": str(source_file or data.get("source_file", "")),
        "extracted_at": datetime.now(tz=None).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dedup_hash": new_hash,
    }

    write_ledger_entry(ledger_path, entry, config)
    print(json.dumps(entry, indent=2))


def ledger_delete(config: dict, entry_id: int):
    """Delete a ledger entry by ID. Renumbers remaining IDs."""
    ledger_path = resolve_ledger_path(config)
    rows = read_ledger(ledger_path)

    if not rows:
        print("No entries in ledger.", file=sys.stderr)
        sys.exit(1)

    # Find the entry
    target_idx = None
    for i, row in enumerate(rows):
        if row.get("id", "").strip() == str(entry_id):
            target_idx = i
            break

    if target_idx is None:
        print(f"Error: no entry with ID {entry_id} found.", file=sys.stderr)
        sys.exit(1)

    deleted = rows.pop(target_idx)

    # Renumber remaining IDs sequentially
    for i, row in enumerate(rows):
        row["id"] = str(i + 1)

    write_ledger_all(ledger_path, rows, config)

    # Print what was removed
    print(f"Deleted entry ID {entry_id}:")
    print(json.dumps(deleted, indent=2))


def ledger_edit(config: dict, entry_id: int, updates: dict):
    """Edit fields of a ledger entry by ID. Recalculates dedup_hash."""
    ledger_path = resolve_ledger_path(config)
    rows = read_ledger(ledger_path)

    if not rows:
        print("No entries in ledger.", file=sys.stderr)
        sys.exit(1)

    # Find the entry
    target_idx = None
    for i, row in enumerate(rows):
        if row.get("id", "").strip() == str(entry_id):
            target_idx = i
            break

    if target_idx is None:
        print(f"Error: no entry with ID {entry_id} found.", file=sys.stderr)
        sys.exit(1)

    entry = rows[target_idx]

    # Apply updates
    editable_fields = {"vendor", "total", "date", "description", "category",
                       "currency", "subtotal", "tax"}
    applied = {}
    for field, value in updates.items():
        if field not in editable_fields:
            print(f"Warning: unknown field '{field}', skipping.", file=sys.stderr)
            continue
        entry[field] = str(value).strip()
        applied[field] = entry[field]

    # Normalize date if it was changed
    if "date" in applied:
        entry["date"] = normalize_date(entry["date"], config)

    # Recalculate dedup_hash (vendor/date/total may have changed)
    vendor = entry.get("vendor", "")
    date = entry.get("date", "")
    try:
        total = float(entry.get("total", 0) or 0)
    except (ValueError, TypeError):
        total = 0.0
    entry["dedup_hash"] = compute_dedup_hash(vendor, date, total)

    write_ledger_all(ledger_path, rows, config)

    print(f"Updated entry ID {entry_id} ({', '.join(applied.keys())}):")
    print(json.dumps(entry, indent=2))


def ledger_undo(config: dict):
    """Remove the most recently added entry (highest ID). One-level undo only."""
    ledger_path = resolve_ledger_path(config)
    rows = read_ledger(ledger_path)

    if not rows:
        print("No entries in ledger.", file=sys.stderr)
        sys.exit(1)

    # Find the last entry (highest ID)
    last_idx = 0
    last_id = -1
    for i, row in enumerate(rows):
        try:
            rid = int(row.get("id", "0"))
        except ValueError:
            rid = 0
        if rid > last_id:
            last_id = rid
            last_idx = i

    removed = rows.pop(last_idx)

    write_ledger_all(ledger_path, rows, config)

    print(f"Undone (removed last entry, was ID {last_id}):")
    print(json.dumps(removed, indent=2))


def parse_date_filter(date_str: str) -> datetime | None:
    """Parse a date filter string into a datetime."""
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def ledger_view(config: dict, from_date: str = None, to_date: str = None,
                category: str = None, vendor: str = None, fmt: str = "json"):
    """View ledger entries with optional filters."""
    ledger_path = resolve_ledger_path(config)
    rows = read_ledger(ledger_path)

    if not rows:
        print("No entries in ledger." if fmt == "json" else "No entries in ledger.")
        return

    from_dt = parse_date_filter(from_date)
    to_dt = parse_date_filter(to_date)

    filtered = []
    for row in rows:
        # Date filter
        if from_dt or to_dt:
            row_date = parse_date_filter(row.get("date", ""))
            if row_date:
                if from_dt and row_date < from_dt:
                    continue
                if to_dt and row_date > to_dt + timedelta(days=1) - timedelta(seconds=1):
                    continue
        # Category filter
        if category and row.get("category", "").lower() != category.lower():
            continue
        # Vendor filter (partial match)
        if vendor and vendor.lower() not in row.get("vendor", "").lower():
            continue
        filtered.append(row)

    if fmt == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=LEDGER_HEADERS, extrasaction="ignore",
                                quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in filtered:
            writer.writerow(row)
    else:
        total = sum(float(r.get("total", 0) or 0) for r in filtered)
        output = {"entries": filtered, "count": len(filtered), "total": round(total, 2)}
        print(json.dumps(output, indent=2))


def ledger_summary(config: dict, period: str = None):
    """Summarize ledger by category."""
    ledger_path = resolve_ledger_path(config)
    rows = read_ledger(ledger_path)

    if not rows:
        print("No entries in ledger.")
        return

    now = datetime.now()
    if period == "week":
        from_dt = now - timedelta(days=7)
    elif period == "month":
        from_dt = now.replace(day=1)
    elif period == "year":
        from_dt = now.replace(month=1, day=1)
    else:
        from_dt = None

    categories: dict[str, float] = {}
    count = 0
    for row in rows:
        if from_dt:
            row_date = parse_date_filter(row.get("date", ""))
            if row_date and row_date < from_dt:
                continue
        cat = row.get("category", "uncategorized")
        total = float(row.get("total", 0) or 0)
        categories[cat] = categories.get(cat, 0) + total
        count += 1

    grand_total = round(sum(categories.values()), 2)
    output = {
        "period": period or "all",
        "entryCount": count,
        "categories": {k: round(v, 2) for k, v in sorted(categories.items(), key=lambda x: -x[1])},
        "grandTotal": grand_total,
    }
    print(json.dumps(output, indent=2))


def list_categories(config: dict):
    """List all configured categories and their keywords."""
    categories = config.get("categories", {})
    print(json.dumps(categories, indent=2))


# ---------------------------------------------------------------------------
# Export presets
# ---------------------------------------------------------------------------

BUILTIN_PRESETS = {
    "xero": {
        "columns": ["ContactName", "InvoiceNumber", "InvoiceDate", "DueDate",
                     "Description", "Quantity", "UnitAmount", "AccountCode", "TaxRate"],
        "headerRow": True,
        "dateFormat": "%d/%m/%Y",
        "amountHandling": "positive",
        "transform": "xero",
    },
    "freeagent": {
        "columns": ["claimant_name", "category", "date", "currency", "value", "description"],
        "headerRow": False,
        "dateFormat": "%d/%m/%Y",
        "amountHandling": "positive",
        "transform": "freeagent",
    },
    "wave": {
        "columns": ["Date", "Description", "Amount"],
        "headerRow": True,
        "dateFormat": "%Y-%m-%d",
        "amountHandling": "negative",
        "transform": "wave",
    },
    "generic": {
        "columns": ["Date", "Vendor", "Description", "Category", "Subtotal", "Tax", "Total", "Currency"],
        "headerRow": True,
        "dateFormat": "%Y-%m-%d",
        "amountHandling": "positive",
        "transform": "generic",
    },
}

# FreeAgent category mapping
FREEAGENT_CATEGORY_MAP = {
    "software": "Software",
    "travel": "Travel",
    "office": "Office Costs",
    "utilities": "Business Costs",
    "food": "Entertaining",
    "professional": "Legal and Professional Fees",
    "marketing": "Marketing",
    "uncategorized": "General Expenses",
}


def load_export_preset(platform: str, config: dict) -> dict:
    """Load a preset: custom from config first, then built-in."""
    # Check custom presets
    custom = config.get("exportPresets", {}).get(platform)
    if custom:
        return custom
    # Check built-in
    builtin = BUILTIN_PRESETS.get(platform)
    if builtin:
        return builtin
    # Not found
    available = list(config.get("exportPresets", {}).keys()) + list(BUILTIN_PRESETS.keys())
    print(f"Error: unknown platform '{platform}'. Available: {', '.join(sorted(available))}", file=sys.stderr)
    sys.exit(1)


def format_date(date_str: str, target_fmt: str) -> str:
    """Convert a YYYY-MM-DD date string to the target format."""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime(target_fmt)
    except ValueError:
        return date_str


def transform_row(row: dict, preset: dict, config: dict) -> list[str]:
    """Transform a ledger row into CSV columns according to the preset."""
    # Detect custom preset (has fieldMapping) vs built-in (has transform key)
    if "fieldMapping" in preset:
        transform = "custom"
    else:
        transform = preset.get("transform", "generic")
    date_fmt = preset.get("dateFormat", "%Y-%m-%d")
    amount_handling = preset.get("amountHandling", "positive")

    if transform == "xero":
        account_code = config.get("xero", {}).get("defaultAccountCode", "200")
        tax_rate = config.get("xero", {}).get("defaultTaxRate", "23% (VAT on Expenses)")
        total = float(row.get("total", 0) or 0)
        return [
            row.get("vendor", ""),
            row.get("id", ""),
            format_date(row.get("date", ""), date_fmt),
            format_date(row.get("dueDate", ""), date_fmt) or format_date(row.get("date", ""), date_fmt),
            row.get("description", ""),
            "1",
            f"{total:.2f}",
            account_code,
            tax_rate,
        ]

    elif transform == "freeagent":
        claimant = config.get("freeagent", {}).get("claimantName", "")
        cat = row.get("category", "uncategorized")
        fa_cat = FREEAGENT_CATEGORY_MAP.get(cat, "General Expenses")
        total = float(row.get("total", 0) or 0)
        return [
            claimant,
            fa_cat,
            format_date(row.get("date", ""), date_fmt),
            row.get("currency", "EUR"),
            f"{total:.2f}",
            row.get("description", ""),
        ]

    elif transform == "wave":
        total = float(row.get("total", 0) or 0)
        amount = f"-{total:.2f}" if amount_handling == "negative" else f"{total:.2f}"
        return [
            format_date(row.get("date", ""), date_fmt),
            row.get("description", ""),
            amount,
        ]

    elif transform == "custom":
        # Custom preset with fieldMapping
        field_mapping = preset.get("fieldMapping", {})
        result = []
        for col in preset.get("columns", []):
            ledger_field = field_mapping.get(col, col)
            val = row.get(ledger_field, "")
            # Format date fields
            if ledger_field == "date" and val:
                val = format_date(val, date_fmt)
            # Handle amount fields
            if ledger_field == "total" and val:
                total = float(val)
                if amount_handling == "negative":
                    val = f"-{total:.2f}"
                else:
                    val = f"{total:.2f}"
            result.append(str(val))
        return result

    else:  # generic
        subtotal = float(row.get("subtotal", 0) or 0)
        tax = float(row.get("tax", 0) or 0)
        total = float(row.get("total", 0) or 0)
        return [
            format_date(row.get("date", ""), date_fmt),
            row.get("vendor", ""),
            row.get("description", ""),
            row.get("category", ""),
            f"{subtotal:.2f}",
            f"{tax:.2f}",
            f"{total:.2f}",
            row.get("currency", "EUR"),
        ]


def filter_rows(rows: list[dict], from_date: str = None, to_date: str = None,
                category: str = None, vendor: str = None) -> list[dict]:
    """Apply filters to ledger rows."""
    from_dt = parse_date_filter(from_date)
    to_dt = parse_date_filter(to_date)

    filtered = []
    for row in rows:
        if from_dt or to_dt:
            row_date = parse_date_filter(row.get("date", ""))
            if row_date:
                if from_dt and row_date < from_dt:
                    continue
                if to_dt and row_date > to_dt + timedelta(days=1) - timedelta(seconds=1):
                    continue
        if category and row.get("category", "").lower() != category.lower():
            continue
        if vendor and vendor.lower() not in row.get("vendor", "").lower():
            continue
        filtered.append(row)
    return filtered


def ledger_export(config: dict, platform: str, from_date: str = None,
                  to_date: str = None, category: str = None, vendor: str = None,
                  output: str = None):
    """Export ledger entries in a platform-specific CSV format."""
    preset = load_export_preset(platform, config)

    ledger_path = resolve_ledger_path(config)
    rows = read_ledger(ledger_path)

    if not rows:
        print("No entries in ledger.", file=sys.stderr)
        sys.exit(1)

    filtered = filter_rows(rows, from_date, to_date, category, vendor)

    if not filtered:
        print("No entries match the specified filters.", file=sys.stderr)
        sys.exit(1)

    buf = io.StringIO()
    writer = csv.writer(buf, quoting=csv.QUOTE_MINIMAL)

    if preset.get("headerRow", True):
        writer.writerow(preset.get("columns", []))

    for row in filtered:
        writer.writerow(transform_row(row, preset, config))

    csv_content = buf.getvalue()

    if output:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            f.write(csv_content)
        print(f"Exported {len(filtered)} entries to {out_path}", file=sys.stderr)
    else:
        sys.stdout.write(csv_content)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Invoice Extractor — extract text from PDFs, manage expense ledger",
    )
    parser.add_argument("--config", "-c", help="Path to config JSON file")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # --pdf
    pdf_parser = subparsers.add_parser("pdf", help="Extract text from a PDF file")
    pdf_parser.add_argument("file", help="Path to PDF file")

    # batch
    batch_parser = subparsers.add_parser("batch", help="List PDFs and images in a folder")
    batch_parser.add_argument("folder", help="Path to folder")

    # ledger
    ledger_parser = subparsers.add_parser("ledger", help="Manage expense ledger")
    ledger_sub = ledger_parser.add_subparsers(dest="ledger_command")

    # ledger add
    add_parser = ledger_sub.add_parser("add", help="Add entry to ledger")
    add_parser.add_argument("json_file", nargs="?", help="JSON file path (or - for stdin)")
    add_parser.add_argument("--source", help="Source filename for the entry")
    add_parser.add_argument("--force", action="store_true", help="Skip duplicate detection")

    # ledger edit
    edit_parser = ledger_sub.add_parser("edit", help="Edit a ledger entry")
    edit_parser.add_argument("--id", type=int, required=True, help="Entry ID to edit")
    edit_parser.add_argument("--vendor", help="New vendor name")
    edit_parser.add_argument("--total", help="New total amount")
    edit_parser.add_argument("--date", help="New date (YYYY-MM-DD)")
    edit_parser.add_argument("--description", help="New description")
    edit_parser.add_argument("--category", help="New category")
    edit_parser.add_argument("--currency", help="New currency code")
    edit_parser.add_argument("--subtotal", help="New subtotal")
    edit_parser.add_argument("--tax", help="New tax amount")

    # ledger delete
    delete_parser = ledger_sub.add_parser("delete", help="Delete a ledger entry")
    delete_parser.add_argument("--id", type=int, required=True, help="Entry ID to delete")

    # ledger undo
    ledger_sub.add_parser("undo", help="Remove the last entry (one-level undo)")

    # ledger export
    export_parser = ledger_sub.add_parser("export", help="Export ledger to platform CSV")
    export_parser.add_argument("--platform", required=True, help="Target platform (xero, freeagent, wave, generic, or custom)")
    export_parser.add_argument("--from", dest="from_date", help="Filter from date (YYYY-MM-DD)")
    export_parser.add_argument("--to", dest="to_date", help="Filter to date (YYYY-MM-DD)")
    export_parser.add_argument("--category", help="Filter by category")
    export_parser.add_argument("--vendor", help="Filter by vendor (partial match)")
    export_parser.add_argument("--output", help="Output file path (default: stdout)")

    # ledger --view
    view_parser = ledger_sub.add_parser("view", help="View ledger entries")
    view_parser.add_argument("--from", dest="from_date", help="Filter from date (YYYY-MM-DD)")
    view_parser.add_argument("--to", dest="to_date", help="Filter to date (YYYY-MM-DD)")
    view_parser.add_argument("--category", help="Filter by category")
    view_parser.add_argument("--vendor", help="Filter by vendor (partial match)")
    view_parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")

    # ledger --summary
    summary_parser = ledger_sub.add_parser("summary", help="Summarize expenses by category")
    summary_parser.add_argument("--period", choices=["week", "month", "year"], help="Time period")

    # categories
    subparsers.add_parser("categories", help="List configured expense categories")

    args = parser.parse_args()
    config = load_config(args.config if hasattr(args, "config") else None)

    if args.command == "pdf":
        text = extract_pdf_text(args.file)
        if text:
            print(text)
    elif args.command == "batch":
        files = batch_scan(args.folder)
        print(json.dumps(files, indent=2))
    elif args.command == "ledger":
        if args.ledger_command == "add":
            ledger_add(args.json_file, config, args.source, force=args.force)
        elif args.ledger_command == "edit":
            updates = {}
            for field in ("vendor", "total", "date", "description", "category",
                          "currency", "subtotal", "tax"):
                val = getattr(args, field, None)
                if val is not None:
                    updates[field] = val
            if not updates:
                print("Error: no fields specified to edit. Use --vendor, --total, --date, etc.", file=sys.stderr)
                sys.exit(1)
            ledger_edit(config, args.id, updates)
        elif args.ledger_command == "delete":
            ledger_delete(config, args.id)
        elif args.ledger_command == "undo":
            ledger_undo(config)
        elif args.ledger_command == "view":
            ledger_view(config, args.from_date, args.to_date, args.category, args.vendor, args.format)
        elif args.ledger_command == "summary":
            ledger_summary(config, args.period)
        elif args.ledger_command == "export":
            ledger_export(config, args.platform, args.from_date, args.to_date,
                          args.category, args.vendor, args.output)
        else:
            ledger_parser.print_help()
    elif args.command == "categories":
        list_categories(config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
