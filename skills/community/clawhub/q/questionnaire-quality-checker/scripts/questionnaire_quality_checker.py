#!/usr/bin/env python3
"""Questionnaire data quality screening for CSV files.

Checks:
- invalid / out-of-range values
- respondent-level missingness
- within-scale straightlining
- within-scale extreme-response concentration

The script FLAGS cases for review. It does not delete observations.
"""

import argparse
import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path

DEFAULT_MISSING_TOKENS = ["", "NA", "N/A", "null", "."]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Screen questionnaire CSV data for basic response-quality issues."
    )
    parser.add_argument("data", help="Input CSV file")
    parser.add_argument("--config", required=True, help="JSON configuration file")
    parser.add_argument("--output", help="Optional path for JSON report")
    return parser.parse_args()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row.")
        return reader.fieldnames, list(reader)


def normalize_missing_tokens(tokens):
    return {str(x).strip().lower() for x in tokens}


def parse_cell(raw, missing_tokens):
    if raw is None:
        return "missing", None

    text = str(raw).strip()
    if text.lower() in missing_tokens:
        return "missing", None

    try:
        value = float(text)
        if not math.isfinite(value):
            return "invalid", text
        return "numeric", value
    except ValueError:
        return "invalid", text


def validate_config(config, fieldnames):
    scales = config.get("scales")
    if not isinstance(scales, list) or not scales:
        raise ValueError("Config must contain a non-empty 'scales' list.")

    id_column = config.get("id_column")
    if id_column and id_column not in fieldnames:
        raise ValueError(f"ID column not found in CSV: {id_column}")

    configured_items = []
    scale_names = set()

    for scale in scales:
        for key in ("name", "items", "min", "max"):
            if key not in scale:
                raise ValueError(f"Each scale must contain '{key}'.")

        name = str(scale["name"])
        if name in scale_names:
            raise ValueError(f"Duplicate scale name: {name}")
        scale_names.add(name)

        items = scale["items"]
        if not isinstance(items, list) or not items:
            raise ValueError(f"Scale '{name}' has no items.")

        try:
            min_value = float(scale["min"])
            max_value = float(scale["max"])
        except (TypeError, ValueError):
            raise ValueError(f"Scale '{name}' min/max must be numeric.")

        if min_value >= max_value:
            raise ValueError(f"Scale '{name}' requires min < max.")

        missing_columns = [item for item in items if item not in fieldnames]
        if missing_columns:
            raise ValueError(
                f"Scale '{name}' contains columns missing from CSV: "
                + ", ".join(missing_columns)
            )

        configured_items.extend(items)

    duplicates = [item for item, n in Counter(configured_items).items() if n > 1]
    if duplicates:
        raise ValueError(
            "An item is assigned to more than one scale: " + ", ".join(duplicates)
        )

    return configured_items


def screen(rows, config, configured_items):
    criteria = config.get("criteria", {})
    max_missing_prop = float(criteria.get("max_missing_prop", 0.20))
    straightline_min_answered = int(criteria.get("straightline_min_answered", 4))
    extreme_prop_threshold = float(criteria.get("extreme_prop_threshold", 0.90))

    if not 0 <= max_missing_prop <= 1:
        raise ValueError("max_missing_prop must be between 0 and 1.")
    if straightline_min_answered < 2:
        raise ValueError("straightline_min_answered must be >= 2.")
    if not 0 <= extreme_prop_threshold <= 1:
        raise ValueError("extreme_prop_threshold must be between 0 and 1.")

    missing_tokens = normalize_missing_tokens(
        config.get("missing_tokens", DEFAULT_MISSING_TOKENS)
    )
    id_column = config.get("id_column")

    respondent_reports = []
    criterion_counts = Counter()

    for row_number, row in enumerate(rows, start=1):
        respondent_id = row.get(id_column) if id_column else str(row_number)
        if respondent_id is None or str(respondent_id).strip() == "":
            respondent_id = f"row_{row_number}"

        flags = []
        details = []
        missing_count = 0
        parsed_by_scale = {}

        for scale in config["scales"]:
            name = str(scale["name"])
            min_value = float(scale["min"])
            max_value = float(scale["max"])
            parsed_by_scale[name] = []

            for item in scale["items"]:
                status, value = parse_cell(row.get(item), missing_tokens)
                parsed_by_scale[name].append((item, status, value))

                if status == "missing":
                    missing_count += 1
                elif status == "invalid":
                    if "invalid_value" not in flags:
                        flags.append("invalid_value")
                    details.append(f"{item}='{value}' is non-numeric")
                elif value < min_value or value > max_value:
                    if "out_of_range" not in flags:
                        flags.append("out_of_range")
                    details.append(
                        f"{item}={value:g}, legal range {min_value:g}-{max_value:g}"
                    )

        missing_prop = missing_count / len(configured_items)
        if missing_prop > max_missing_prop:
            flags.append("high_missingness")
            details.append(
                f"missing proportion={missing_prop:.3f} "
                f"(threshold > {max_missing_prop:.3f})"
            )

        for scale in config["scales"]:
            name = str(scale["name"])
            min_value = float(scale["min"])
            max_value = float(scale["max"])

            valid_values = [
                value
                for _, status, value in parsed_by_scale[name]
                if status == "numeric" and min_value <= value <= max_value
            ]

            if len(valid_values) >= straightline_min_answered:
                if len(set(valid_values)) == 1:
                    flag = f"straightlining:{name}"
                    flags.append(flag)
                    details.append(
                        f"{name}: all {len(valid_values)} valid answers "
                        f"equal {valid_values[0]:g}"
                    )

                extreme_count = sum(
                    value == min_value or value == max_value
                    for value in valid_values
                )
                extreme_prop = extreme_count / len(valid_values)

                if extreme_prop >= extreme_prop_threshold:
                    flag = f"extreme_response:{name}"
                    flags.append(flag)
                    details.append(
                        f"{name}: extreme-response proportion={extreme_prop:.3f} "
                        f"(threshold >= {extreme_prop_threshold:.3f})"
                    )

        flags = list(dict.fromkeys(flags))
        for flag in flags:
            criterion_counts[flag] += 1

        respondent_reports.append(
            {
                "id": str(respondent_id),
                "flagged": bool(flags),
                "missing_prop": round(missing_prop, 4),
                "flags": flags,
                "details": details,
            }
        )

    flagged_n = sum(report["flagged"] for report in respondent_reports)

    return {
        "summary": {
            "total_respondents": len(respondent_reports),
            "configured_items": len(configured_items),
            "flagged_respondents": flagged_n,
            "flagged_rate": round(flagged_n / len(respondent_reports), 4)
            if respondent_reports else 0,
            "criterion_counts": dict(sorted(criterion_counts.items())),
        },
        "thresholds": {
            "max_missing_prop": max_missing_prop,
            "straightline_min_answered": straightline_min_answered,
            "extreme_prop_threshold": extreme_prop_threshold,
        },
        "respondents": respondent_reports,
    }


def main():
    args = parse_args()

    try:
        config = load_json(args.config)
        fieldnames, rows = load_csv(args.data)
        configured_items = validate_config(config, fieldnames)
        report = screen(rows, config, configured_items)

        output_text = json.dumps(report, ensure_ascii=False, indent=2)
        print(output_text)

        if args.output:
            Path(args.output).write_text(output_text, encoding="utf-8")

    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
