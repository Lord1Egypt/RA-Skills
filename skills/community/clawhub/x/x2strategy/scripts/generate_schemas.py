#!/usr/bin/env python3
"""Generate JSON Schema files from paper2spec dataclasses.

Usage:
    python scripts/generate_schemas.py

Outputs:
    schemas/paper_content.schema.json
    schemas/strategy_spec.schema.json
"""

import json
import os
import sys
from dataclasses import fields
from typing import get_type_hints, get_origin, get_args, Optional, Union

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from paper2spec.models import (
    PaperContent,
    StrategySpec,
    Indicator,
    LogicStep,
    ExecutionTrigger,
    PositionSizing,
    ExecutionAction,
    ExecutionPlan,
)


def _python_type_to_json_schema(tp) -> dict:
    """Convert a Python type annotation to JSON Schema."""
    origin = get_origin(tp)
    args = get_args(tp)

    # Handle Optional[X] = Union[X, None]
    if origin is Union:
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            schema = _python_type_to_json_schema(non_none[0])
            return {**schema, "nullable": True}
        return {}

    if origin is list or origin is list:
        if args:
            return {"type": "array", "items": _python_type_to_json_schema(args[0])}
        return {"type": "array"}

    if origin is dict or origin is dict:
        return {"type": "object"}

    if tp is str:
        return {"type": "string"}
    if tp is int:
        return {"type": "integer"}
    if tp is float:
        return {"type": "number"}
    if tp is bool:
        return {"type": "boolean"}

    # Nested dataclass
    if hasattr(tp, "__dataclass_fields__"):
        return {"$ref": f"#/$defs/{tp.__name__}"}

    return {}


def dataclass_to_schema(cls, *, title: str = "", defs: dict = None) -> dict:
    """Convert a dataclass to JSON Schema dict."""
    if defs is None:
        defs = {}

    hints = get_type_hints(cls)
    properties = {}
    for f in fields(cls):
        prop = _python_type_to_json_schema(hints[f.name])
        properties[f.name] = prop

        # If it references a nested dataclass, add to $defs
        tp = hints[f.name]
        origin = get_origin(tp)
        args = get_args(tp)
        if origin is list and args and hasattr(args[0], "__dataclass_fields__"):
            nested = args[0]
            if nested.__name__ not in defs:
                defs[nested.__name__] = _build_object_schema(nested, defs)
        elif hasattr(tp, "__dataclass_fields__") and tp.__name__ not in defs:
            defs[tp.__name__] = _build_object_schema(tp, defs)

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title or cls.__name__,
        "type": "object",
        "properties": properties,
    }
    if defs:
        schema["$defs"] = defs
    return schema


def _build_object_schema(cls, defs: dict) -> dict:
    hints = get_type_hints(cls)
    properties = {}
    for f in fields(cls):
        prop = _python_type_to_json_schema(hints[f.name])
        properties[f.name] = prop

        tp = hints[f.name]
        origin = get_origin(tp)
        args = get_args(tp)
        if origin is list and args and hasattr(args[0], "__dataclass_fields__"):
            nested = args[0]
            if nested.__name__ not in defs:
                defs[nested.__name__] = _build_object_schema(nested, defs)
        elif hasattr(tp, "__dataclass_fields__") and tp.__name__ not in defs:
            defs[tp.__name__] = _build_object_schema(tp, defs)

    return {"type": "object", "properties": properties}


def main():
    schemas_dir = os.path.join(os.path.dirname(__file__), "..", "schemas")
    os.makedirs(schemas_dir, exist_ok=True)

    # PaperContent schema
    pc_schema = dataclass_to_schema(PaperContent, title="PaperContent")
    pc_path = os.path.join(schemas_dir, "paper_content.schema.json")
    with open(pc_path, "w") as f:
        json.dump(pc_schema, f, indent=2)
    print(f"✅ {pc_path}")

    # StrategySpec schema
    defs: dict = {}
    ss_schema = dataclass_to_schema(StrategySpec, title="StrategySpec", defs=defs)
    ss_path = os.path.join(schemas_dir, "strategy_spec.schema.json")
    with open(ss_path, "w") as f:
        json.dump(ss_schema, f, indent=2)
    print(f"✅ {ss_path}")


if __name__ == "__main__":
    main()
