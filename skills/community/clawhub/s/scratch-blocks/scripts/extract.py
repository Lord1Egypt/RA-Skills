#!/usr/bin/env python3
"""
Extract Scratch blocks from .sb3/.sprite3 files and output scratch-json.

Usage:
    python3 extract.py [--output PATH] <file.sb3|file.sprite3|project.json>

No external dependencies for Scratch parsing/output - uses only Python standard
library.
"""

import argparse
import hashlib
import json
import os
import sys
import zipfile


def parse_args():
    parser = argparse.ArgumentParser(prog="extract.py")
    parser.add_argument("filepath", help="Scratch archive or JSON file to extract")
    parser.add_argument("--output", help="Write the extracted JSON to this exact path")
    return parser.parse_args()


def get_project_json(filepath):
    """Return (parsed_data, workdir) from a .sb3/.sprite3 zip or a .json file.

    workdir is None for plain .json inputs (output written alongside input).
    """
    def fail(message):
        print(f"Error: {message}", file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".json":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        filename = os.path.basename(filepath).lower()
        if filename == "project.json":
            if not isinstance(data, dict) or not isinstance(data.get("targets"), list):
                fail("invalid Scratch project.json; expected a top-level object with a 'targets' list")
            return data, None

        if filename == "sprite.json":
            if not isinstance(data, dict):
                fail("invalid Scratch sprite.json; expected a top-level object")
            return {"targets": [data]}, None

        if isinstance(data, list):
            fail("expected Scratch project.json or sprite.json; extracted scratch-json (*.blocks.json) is not valid input")

        fail("loose JSON input must be named project.json or sprite.json")

    if ext not in (".sb3", ".sprite3"):
        fail(f"unsupported extension '{ext}'. Expected .sb3, .sprite3, or .json")

    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    md5hex = md5.hexdigest()

    workdir = os.path.join("/tmp/scratchcode", md5hex)
    os.makedirs(workdir, exist_ok=True)

    with zipfile.ZipFile(filepath, "r") as zf:
        names = zf.namelist()
        if "project.json" in names:
            json_name = "project.json"
        elif "sprite.json" in names:
            json_name = "sprite.json"
        else:
            fail("neither project.json nor sprite.json found in archive")
        zf.extract(json_name, workdir)

    json_path = os.path.join(workdir, json_name)
    print(f"Working directory: {workdir}", file=sys.stderr)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if json_name == "sprite.json":
        data = {"targets": [data]}

    return data, workdir


def extract_code(project_data):
    objects = []

    for target in project_data.get("targets", []):
        target_name = target["name"]
        emitted = False

        raw_vars = target.get("variables", {})
        for var in raw_vars.values():
            if isinstance(var, list) and len(var) >= 2:
                objects.append(
                    {
                        "type": "variable",
                        "target": target_name,
                        "name": var[0],
                        "value": var[1],
                    }
                )
                emitted = True

        raw_lists = target.get("lists", {})
        for item in raw_lists.values():
            if isinstance(item, list) and len(item) >= 2:
                objects.append(
                    {
                        "type": "list",
                        "target": target_name,
                        "name": item[0],
                        "items": item[1],
                    }
                )
                emitted = True

        blocks = target.get("blocks", {})

        def resolve_primitive(prim):
            ptype, value = prim[0], prim[1]
            if ptype == 12:
                return {"type": "variable", "name": value}
            if ptype == 13:
                return {"type": "list", "name": value}
            if ptype == 11:
                return {"type": "broadcast", "name": value}
            if 4 <= ptype <= 8:
                try:
                    number = float(value)
                    return int(number) if number == int(number) else number
                except (ValueError, TypeError):
                    return value
            return value

        def resolve_shadow_block(block):
            entries = list((block.get("fields") or {}).items())
            if len(entries) == 1:
                return entries[0][1][0]
            if len(entries) > 1:
                return {key: value[0] for key, value in entries}
            return None

        def resolve_input_value(inp):
            primary = inp[1]
            if isinstance(primary, list):
                return resolve_primitive(primary)
            if isinstance(primary, str):
                block = blocks.get(primary)
                if block is None:
                    return None
                if block.get("shadow"):
                    return resolve_shadow_block(block)
                return build_block(primary)
            return None

        def build_block(block_id):
            block = blocks.get(block_id)
            if not block or block.get("shadow"):
                return None

            params = []
            branches = []

            if block["opcode"] == "procedures_definition":
                custom_block_input = (block.get("inputs") or {}).get("custom_block")
                proto_id = custom_block_input[1] if custom_block_input else None
                proto = blocks.get(proto_id) if proto_id else None
                if proto and proto.get("mutation"):
                    mutation = proto["mutation"]
                    params.append(mutation.get("proccode", ""))
                    try:
                        argnames = json.loads(mutation.get("argumentnames", "[]"))
                        params.extend(argnames)
                    except (json.JSONDecodeError, TypeError):
                        pass
                node = {"opcode": block["opcode"]}
                if params:
                    node["params"] = params
                if branches:
                    node["blocks"] = branches
                return node

            if block["opcode"] == "procedures_call":
                mutation = block.get("mutation")
                if mutation and mutation.get("proccode"):
                    params.append(mutation["proccode"])

            for field_val in (block.get("fields") or {}).values():
                params.append(field_val[0])

            for key, inp in (block.get("inputs") or {}).items():
                if key in ("SUBSTACK", "SUBSTACK2"):
                    sub_id = inp[1]
                    if (
                        sub_id
                        and isinstance(sub_id, str)
                        and blocks.get(sub_id)
                        and not blocks[sub_id].get("shadow")
                    ):
                        branches.append(build_sequence(sub_id))
                    else:
                        branches.append([])
                else:
                    val = resolve_input_value(inp)
                    if val is not None:
                        params.append(val)

            node = {"opcode": block["opcode"]}
            if params:
                node["params"] = params
            if branches:
                node["blocks"] = branches
            return node

        def build_sequence(start_id):
            seq = []
            current_id = start_id
            while current_id:
                node = build_block(current_id)
                if node:
                    seq.append(node)
                blk = blocks.get(current_id)
                current_id = blk.get("next") if blk else None
            return seq

        for block_id, block in blocks.items():
            if block.get("topLevel") and not block.get("shadow"):
                objects.append(
                    {
                        "type": "script",
                        "target": target_name,
                        "blocks": build_sequence(block_id),
                    }
                )
                emitted = True

        if not emitted:
            objects.append({"type": "script", "target": target_name, "blocks": []})

    return objects


def to_scratch_json(objects):
    """Convert extracted Scratch objects to scratch-json string."""
    return json.dumps(objects, indent=2, ensure_ascii=False) + "\n"


def main():
    args = parse_args()
    filepath = args.filepath
    if not os.path.isfile(filepath):
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    project_data, workdir = get_project_json(filepath)
    extracted = extract_code(project_data)

    if args.output:
        out_path = args.output
    elif workdir:
        out_path = os.path.join(workdir, "blocks.json")
    else:
        base = os.path.splitext(filepath)[0]
        out_path = base + ".blocks.json"

    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(to_scratch_json(extracted))
    print(out_path)


if __name__ == "__main__":
    main()
