from __future__ import annotations

import csv
import json
import re
import urllib.parse
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
import argparse

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_PROJECT_ROOT = Path.cwd()
DEFAULT_ANALYSIS_DIR = DEFAULT_PROJECT_ROOT / "analysis"
DEFAULT_LAYOUT_EXTRACT_DIR = DEFAULT_ANALYSIS_DIR / "layout_extract"
DEFAULT_LAYOUT_DIR = DEFAULT_PROJECT_ROOT / "metadata_subset" / "layouts"
DEFAULT_FLEXIPAGE_DIR = DEFAULT_PROJECT_ROOT / "metadata_subset" / "flexipages"
DEFAULT_SOQL_DIR = DEFAULT_ANALYSIS_DIR / "soql"

ANALYSIS_DIR = DEFAULT_ANALYSIS_DIR
LAYOUT_EXTRACT_DIR = DEFAULT_LAYOUT_EXTRACT_DIR
LAYOUT_DIR = DEFAULT_LAYOUT_DIR
FLEXIPAGE_DIR = DEFAULT_FLEXIPAGE_DIR
SOQL_DIR = DEFAULT_SOQL_DIR

NS = {"m": "http://soap.sforce.com/2006/04/metadata"}
FIELD_TOKEN_RE = re.compile(r"(?:\{\!Record\.)([A-Za-z0-9_]+(?:__c|Id))(?:\})")

OBJECTS = [
    "Lead",
    "Account",
    "Contact",
    "Opportunity",
    "Quote",
    "CRM_Contract__c",
    "CRM_Bidding_Project_Establishment__c",
    "CRM_Bidding_Review__c",
    "CRM_Order_Details__c",
    "CRM_Business_Trip_Application__c",
    "CRM_OrderList__c",
    "CRM_Technical_Review__c",
    "CRM_PaybackList__c",
    "CRM_InvoiceList__c",
]

USER_OWNER_OBJECTS = {
    "Account",
    "Contact",
    "Opportunity",
}

POLYMORPHIC_OWNER_OBJECTS = {
    "Lead",
    "Quote",
    "CRM_Contract__c",
    "CRM_Business_Trip_Application__c",
    "CRM_OrderList__c",
    "CRM_PaybackList__c",
    "CRM_InvoiceList__c",
}

OUT_OF_SCOPE_OWNER = "\n".join(
    [
        "(Owner.CRM_Sales_Team__c = 'Europe')",
        "(Owner.CRM_Sales_Team__c = 'LATAM' AND Owner.CRM_Sales_Group__c IN ('Latin America and the Caribbean', 'Iberia'))",
        "(Owner.CRM_Sales_Team__c = 'Japan' AND Owner.CRM_Sales_Group__c = 'Japan')",
        "(Owner.CRM_Sales_Team__c = 'SEAMEA' AND Owner.CRM_Sales_Group__c IN ('Middle East', 'India', 'Africa'))",
        "Owner.CRM_Sales_Team__c = NULL",
        "Owner.CRM_Sales_Group__c = NULL",
        "Owner.CRM_Sales_Team__c = 'Solution-Oversea'",
    ]
)

OUT_OF_SCOPE_USER = "\n".join(
    [
        "CRM_Sales_Team__c = 'Europe'",
        "(CRM_Sales_Team__c = 'LATAM' AND CRM_Sales_Group__c IN ('Latin America and the Caribbean', 'Iberia'))",
        "(CRM_Sales_Team__c = 'Japan' AND CRM_Sales_Group__c = 'Japan')",
        "(CRM_Sales_Team__c = 'SEAMEA' AND CRM_Sales_Group__c IN ('Middle East', 'India', 'Africa'))",
        "CRM_Sales_Team__c = NULL",
        "CRM_Sales_Group__c = NULL",
        "CRM_Sales_Team__c = 'Solution-Oversea'",
    ]
)

QUERY_TEMPLATES = {
    "Lead": """SELECT\n  OwnerId,\n  TYPEOF Owner\n    WHEN User THEN Name, CRM_Sales_Team__c, CRM_Sales_Group__c\n    WHEN Group THEN Name\n  END,\n{fields}\nFROM Lead\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND OwnerId IN (\n  SELECT Id\n  FROM User\n  WHERE\n    {user_filter}\n)""",
    "Account": """SELECT\n{fields}\nFROM Account\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND (\n  {owner_filter}\n)""",
    "Contact": """SELECT\n{fields}\nFROM Contact\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND (\n  {owner_filter}\n)""",
    "Opportunity": """SELECT\n{fields}\nFROM Opportunity\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND (\n  {owner_filter}\n)""",
    "Quote": """SELECT\n  OwnerId,\n  TYPEOF Owner\n    WHEN User THEN Name, CRM_Sales_Team__c, CRM_Sales_Group__c\n    WHEN Group THEN Name\n  END,\n{fields}\nFROM Quote\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND OwnerId IN (\n  SELECT Id\n  FROM User\n  WHERE\n    {user_filter}\n)""",
    "CRM_Contract__c": """SELECT\n  OwnerId,\n  TYPEOF Owner\n    WHEN User THEN Name, CRM_Sales_Team__c, CRM_Sales_Group__c\n    WHEN Group THEN Name\n  END,\n{fields}\nFROM CRM_Contract__c\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND OwnerId IN (\n  SELECT Id\n  FROM User\n  WHERE\n    {user_filter}\n)""",
    "CRM_Business_Trip_Application__c": """SELECT\n  OwnerId,\n  TYPEOF Owner\n    WHEN User THEN Name, CRM_Sales_Team__c, CRM_Sales_Group__c\n    WHEN Group THEN Name\n  END,\n{fields}\nFROM CRM_Business_Trip_Application__c\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND OwnerId IN (\n  SELECT Id\n  FROM User\n  WHERE\n    {user_filter}\n)""",
    "CRM_OrderList__c": """SELECT\n  OwnerId,\n  TYPEOF Owner\n    WHEN User THEN Name, CRM_Sales_Team__c, CRM_Sales_Group__c\n    WHEN Group THEN Name\n  END,\n{fields}\nFROM CRM_OrderList__c\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND OwnerId IN (\n  SELECT Id\n  FROM User\n  WHERE\n    {user_filter}\n)""",
    "CRM_PaybackList__c": """SELECT\n  OwnerId,\n  TYPEOF Owner\n    WHEN User THEN Name, CRM_Sales_Team__c, CRM_Sales_Group__c\n    WHEN Group THEN Name\n  END,\n{fields}\nFROM CRM_PaybackList__c\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND OwnerId IN (\n  SELECT Id\n  FROM User\n  WHERE\n    {user_filter}\n)""",
    "CRM_InvoiceList__c": """SELECT\n  OwnerId,\n  TYPEOF Owner\n    WHEN User THEN Name, CRM_Sales_Team__c, CRM_Sales_Group__c\n    WHEN Group THEN Name\n  END,\n{fields}\nFROM CRM_InvoiceList__c\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND OwnerId IN (\n  SELECT Id\n  FROM User\n  WHERE\n    {user_filter}\n)""",
    "CRM_Bidding_Project_Establishment__c": """SELECT\n{fields}\nFROM CRM_Bidding_Project_Establishment__c\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND CRM_Opportunity__c IN (\n  SELECT Id\n  FROM Opportunity\n  WHERE\n    {owner_filter}\n)""",
    "CRM_Bidding_Review__c": """SELECT\n{fields}\nFROM CRM_Bidding_Review__c\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND CRM_Opportunity__c IN (\n  SELECT Id\n  FROM Opportunity\n  WHERE\n    {owner_filter}\n)""",
    "CRM_Technical_Review__c": """SELECT\n{fields}\nFROM CRM_Technical_Review__c\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND CRM_Opportunity__c IN (\n  SELECT Id\n  FROM Opportunity\n  WHERE\n    {owner_filter}\n)""",
    "CRM_Order_Details__c": """-- Step 1: run CRM_OrderList__c.soql first and replace the placeholder IDs below.\nSELECT\n{fields}\nFROM CRM_Order_Details__c\nWHERE LastModifiedDate < 2026-03-22T16:00:00Z\nAND CRM_Order__c IN (\n  'a14xxxxxxxxxxxx',\n  'a14yyyyyyyyyyyy'\n)""",
}


def decode_name(name: str) -> str:
    return urllib.parse.unquote(name)


def object_from_layout_filename(path: Path) -> str | None:
    raw = decode_name(path.stem.replace(".layout-meta", ""))
    for obj in OBJECTS:
        if raw.startswith(f"{obj}-"):
            return obj
    return None


def load_describe(object_name: str) -> tuple[dict[str, str], set[str]]:
    describe_path = LAYOUT_EXTRACT_DIR / f"{object_name}.describe.json"
    payload = json.loads(describe_path.read_text())
    fields = payload["result"]["fields"]
    labels = {}
    queryable = set()
    for field in fields:
        labels[field["name"]] = field.get("label") or field["name"]
        if field.get("filterable", False):
            queryable.add(field["name"])
    return labels, queryable


def extract_layout_fields() -> tuple[dict[str, set[str]], dict[str, dict[str, set[str]]]]:
    object_fields: dict[str, set[str]] = defaultdict(set)
    field_sources: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for path in LAYOUT_DIR.glob("*.layout-meta.xml"):
        object_name = object_from_layout_filename(path)
        if not object_name:
            continue
        tree = ET.parse(path)
        for field_node in tree.findall(".//m:field", NS):
            field_name = (field_node.text or "").strip()
            if not field_name:
                continue
            object_fields[object_name].add(field_name)
            field_sources[object_name][field_name].add(path.name)
    return object_fields, field_sources


def extract_flexipage_fields() -> tuple[dict[str, set[str]], dict[str, dict[str, set[str]]]]:
    object_fields: dict[str, set[str]] = defaultdict(set)
    field_sources: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for path in FLEXIPAGE_DIR.glob("*.flexipage-meta.xml"):
        tree = ET.parse(path)
        root = tree.getroot()
        sobject_type = root.findtext("m:sobjectType", default="", namespaces=NS).strip()
        if sobject_type not in OBJECTS:
            continue
        text_blob = ET.tostring(root, encoding="unicode")
        for match in FIELD_TOKEN_RE.findall(text_blob):
            object_fields[sobject_type].add(match)
            field_sources[sobject_type][match].add(path.name)
    return object_fields, field_sources


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def merge_sources(
    layout_sources: dict[str, dict[str, set[str]]],
    flexi_sources: dict[str, dict[str, set[str]]],
) -> dict[str, dict[str, set[str]]]:
    merged: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for source_map in (layout_sources, flexi_sources):
        for object_name, field_map in source_map.items():
            for field_name, sources in field_map.items():
                merged[object_name][field_name].update(sources)
    return merged


def add_context_fields(
    object_name: str,
    fields: set[str],
    described_fields: set[str],
    queryable_fields: set[str],
) -> list[str]:
    selected = {field_name for field_name in fields if field_name in described_fields}
    if object_name in POLYMORPHIC_OWNER_OBJECTS:
        selected.discard("OwnerId")
    for base_field in ("Id", "Name", "LastModifiedDate"):
        if base_field in queryable_fields:
            selected.add(base_field)
    context = {
        "Account": ["OwnerId", "Owner.Name", "Owner.CRM_Sales_Team__c", "Owner.CRM_Sales_Group__c"],
        "Contact": ["OwnerId", "Owner.Name", "Owner.CRM_Sales_Team__c", "Owner.CRM_Sales_Group__c"],
        "Opportunity": ["OwnerId", "Owner.Name", "Owner.CRM_Sales_Team__c", "Owner.CRM_Sales_Group__c"],
        "CRM_Bidding_Project_Establishment__c": [
            "CRM_Opportunity__c",
            "CRM_Opportunity__r.Name",
            "CRM_Opportunity__r.Owner.Name",
            "CRM_Opportunity__r.Owner.CRM_Sales_Team__c",
            "CRM_Opportunity__r.Owner.CRM_Sales_Group__c",
        ],
        "CRM_Bidding_Review__c": [
            "CRM_Opportunity__c",
            "CRM_Opportunity__r.Name",
            "CRM_Opportunity__r.Owner.Name",
            "CRM_Opportunity__r.Owner.CRM_Sales_Team__c",
            "CRM_Opportunity__r.Owner.CRM_Sales_Group__c",
        ],
        "CRM_Technical_Review__c": [
            "CRM_Opportunity__c",
            "CRM_Opportunity__r.Name",
            "CRM_Opportunity__r.Owner.Name",
            "CRM_Opportunity__r.Owner.CRM_Sales_Team__c",
            "CRM_Opportunity__r.Owner.CRM_Sales_Group__c",
        ],
        "CRM_Order_Details__c": [
            "CRM_Order__c",
        ],
    }
    ordered = []
    seen = set()
    for field_name in context.get(object_name, []) + sorted(selected):
        if field_name not in seen:
            ordered.append(field_name)
            seen.add(field_name)
    return ordered


def format_owner_filter() -> str:
    return OUT_OF_SCOPE_OWNER.replace("\n", "\n    OR ")


def format_user_filter() -> str:
    return OUT_OF_SCOPE_USER.replace("\n", "\n    OR ")


def write_field_catalog(
    merged_sources: dict[str, dict[str, set[str]]],
    labels_by_object: dict[str, dict[str, str]],
) -> None:
    output_path = ANALYSIS_DIR / "layout_field_catalog.csv"
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["object", "field_api_name", "field_label", "sources"])
        for object_name in OBJECTS:
            for field_name in sorted(merged_sources.get(object_name, {})):
                writer.writerow(
                    [
                        object_name,
                        field_name,
                        labels_by_object.get(object_name, {}).get(field_name, field_name),
                        "; ".join(sorted(merged_sources[object_name][field_name])),
                    ]
                )


def write_object_field_files(
    merged_sources: dict[str, dict[str, set[str]]],
    labels_by_object: dict[str, dict[str, str]],
) -> None:
    for object_name in OBJECTS:
        output_path = ANALYSIS_DIR / f"{object_name}.fields.csv"
        with output_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["field_api_name", "field_label", "sources"])
            for field_name in sorted(merged_sources.get(object_name, {})):
                writer.writerow(
                    [
                        field_name,
                        labels_by_object.get(object_name, {}).get(field_name, field_name),
                        "; ".join(sorted(merged_sources[object_name][field_name])),
                    ]
                )


def write_soql_files(
    object_fields: dict[str, set[str]],
    described_fields_by_object: dict[str, set[str]],
    queryable_by_object: dict[str, set[str]],
) -> None:
    ensure_dir(SOQL_DIR)
    owner_filter = format_owner_filter()
    user_filter = format_user_filter()
    for object_name in OBJECTS:
        selected_fields = add_context_fields(
            object_name,
            object_fields.get(object_name, set()),
            described_fields_by_object[object_name],
            queryable_by_object[object_name],
        )
        rendered_fields = ",\n".join(f"  {field_name}" for field_name in selected_fields)
        soql = QUERY_TEMPLATES[object_name].format(fields=rendered_fields, owner_filter=owner_filter, user_filter=user_filter)
        (SOQL_DIR / f"{object_name}.soql").write_text(soql + "\n", encoding="utf-8")


def write_summary(
    layout_fields: dict[str, set[str]],
    flexi_fields: dict[str, set[str]],
) -> None:
    lines = [
        "# 页面字段提取说明",
        "",
        "- Layout 字段来自 `metadata_subset/layouts/*.layout-meta.xml`。",
        "- FlexiPage 仅补充页面中显式引用到的字段，例如 `{{!Record.Field__c}}` 这种可直接解析的字段。",
        "- 对本次 14 个对象而言，FlexiPage 几乎都使用 `force:detailPanel`，显式字段非常少，因此字段清单以 Layout 为主。",
        "",
        "## 统计",
        "",
        "| Object | Layout Fields | Explicit FlexiPage Fields |",
        "| --- | ---: | ---: |",
    ]
    for object_name in OBJECTS:
        lines.append(
            f"| {object_name} | {len(layout_fields.get(object_name, set()))} | {len(flexi_fields.get(object_name, set()))} |"
        )
    (ANALYSIS_DIR / "layout_field_extraction_notes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis-dir", type=Path, default=DEFAULT_ANALYSIS_DIR)
    parser.add_argument("--layout-dir", type=Path, default=DEFAULT_LAYOUT_DIR)
    parser.add_argument("--flexipage-dir", type=Path, default=DEFAULT_FLEXIPAGE_DIR)
    parser.add_argument("--soql-dir", type=Path, default=DEFAULT_SOQL_DIR)
    args = parser.parse_args()

    global ANALYSIS_DIR, LAYOUT_EXTRACT_DIR, LAYOUT_DIR, FLEXIPAGE_DIR, SOQL_DIR
    ANALYSIS_DIR = args.analysis_dir.resolve()
    LAYOUT_EXTRACT_DIR = ANALYSIS_DIR / "layout_extract"
    LAYOUT_DIR = args.layout_dir.resolve()
    FLEXIPAGE_DIR = args.flexipage_dir.resolve()
    SOQL_DIR = args.soql_dir.resolve()

    layout_fields, layout_sources = extract_layout_fields()
    flexi_fields, flexi_sources = extract_flexipage_fields()
    merged_sources = merge_sources(layout_sources, flexi_sources)
    merged_fields: dict[str, set[str]] = defaultdict(set)
    for object_name in OBJECTS:
        merged_fields[object_name].update(layout_fields.get(object_name, set()))
        merged_fields[object_name].update(flexi_fields.get(object_name, set()))

    labels_by_object = {}
    described_fields_by_object = {}
    queryable_by_object = {}
    for object_name in OBJECTS:
        labels, queryable = load_describe(object_name)
        labels_by_object[object_name] = labels
        described_fields_by_object[object_name] = set(labels)
        queryable_by_object[object_name] = queryable

    write_field_catalog(merged_sources, labels_by_object)
    write_object_field_files(merged_sources, labels_by_object)
    write_soql_files(merged_fields, described_fields_by_object, queryable_by_object)
    write_summary(layout_fields, flexi_fields)


if __name__ == "__main__":
    main()
