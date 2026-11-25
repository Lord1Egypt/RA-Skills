#!/usr/bin/env python3
"""Convert editable Bambu/Orca projects locally using a reviewed third-party backend.

No service account, web server, uploads or printer commands. Conversion produces
an unsliced project for manual review in Snapmaker Orca, never print-ready G-code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from xml.parsers import expat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "639b822e2db3b59b0dc7379771f7cdf872b06910"
REPOSITORY = "https://github.com/thadius83/bambu-to-snapmaker-u1"
DEFAULT_PROFILE = "0.20 Standard - Cube"
SETTINGS = "Metadata/project_settings.config"
LAYER_COMMANDS = "Metadata/custom_gcode_per_layer.xml"
MARKER = "Metadata/u1_conversion.json"
FILAMENT_HOOKS = {"filament_start_gcode", "filament_end_gcode"}
POST_PROCESS = {"post_process", "post_process_script", "post_process_scripts"}
SLOT_KEYS = {"extruder", "wall_filament", "sparse_infill_filament", "solid_infill_filament", "support_filament", "support_interface_filament", "wipe_tower_filament"}
HARDWARE_KEYS = {"extruder_offset", "single_extruder_multi_material", "single_extruder_multi_material_priming", "manual_filament_change", "use_relative_e_distances", "use_firmware_retraction"}


class ConversionError(ValueError):
    pass


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def runtime_path(config_path):
    config = json.loads(config_path.read_text()) if config_path.is_file() else {}
    return Path(config.get("bambu_runtime", Path(config.get("runtime_dir", ROOT / ".runtime")) / "bambu-to-u1")).expanduser().absolute()


def verify_runtime(runtime):
    """Use only the reviewed revision with unchanged code, references and rules."""
    try:
        revision = subprocess.check_output(["git", "-C", str(runtime), "rev-parse", "HEAD"], text=True, stderr=subprocess.STDOUT).strip()
        changes = subprocess.check_output(["git", "-C", str(runtime), "status", "--porcelain", "--untracked-files=all", "--", "backend", "profiles", "rules", "LICENSE"], text=True, stderr=subprocess.STDOUT).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ConversionError("Local Bambu converter is missing; see references/BAMBU_CONVERSION.md for setup.") from exc
    if revision != COMMIT or changes:
        raise ConversionError("Bambu converter revision/files changed; review the installation before conversion.")
    python = runtime / ".venv/bin/python"
    if not python.is_file() or not os.access(python, os.X_OK):
        raise ConversionError("Bambu converter's isolated Python environment is missing.")
    return python


def parse_slot_map(text, count):
    if not 1 <= count <= 4:
        raise ConversionError("This adapter supports 1–4 project filaments. More colors/spool swaps require a separate reviewed plan; Full Spectrum is not assigned automatically.")
    if not text:
        return {i: i for i in range(count)}
    mapping = {}
    try:
        for pair in text.split(","):
            source, target = map(int, pair.split(":"))
            if source in mapping:
                raise ValueError
            mapping[source] = target
    except ValueError as exc:
        raise ConversionError("Use a complete slot map such as 1:2,2:1 (one-based source:U1 tool).") from exc
    if set(mapping) != set(range(1, count + 1)) or not all(1 <= target <= 4 for target in mapping.values()):
        raise ConversionError("Map every source filament exactly once to U1 tools 1–4.")
    if len(set(mapping.values())) != count:
        raise ConversionError("Many-to-one mappings need spool-swap/material planning and are not supported by this adapter.")
    return {source - 1: target - 1 for source, target in mapping.items()}


def xml_root(data, name):
    if re.search(br"<!\s*(DOCTYPE|ENTITY)\b", data, re.I):
        raise ConversionError(f"XML declarations/entities are unsupported: {name}")
    try:
        return ET.fromstring(data)
    except ET.ParseError as exc:
        raise ConversionError(f"Malformed XML: {name}") from exc


def local_tag(element):
    return element.tag.rsplit("}", 1)[-1]


def paint_states(text):
    """Read Orca triangle-selector hex trees; reject incomplete/virtual paint."""
    if not text:
        return []
    try:
        digits = [int(char, 16) for char in text]
        pending, index, states = 1, len(digits), []
        while pending:
            index -= 1
            if index < 0:
                raise ValueError
            code = digits[index]
            pending -= 1
            if code % 4:
                pending += code % 4 + 1
            else:
                state = code // 4
                if state == 3:
                    while True:
                        index -= 1
                        if index < 0:
                            raise ValueError
                        state += digits[index]
                        if digits[index] != 15:
                            break
                states.append(state)
        if index:
            raise ValueError
        return states
    except ValueError as exc:
        raise ConversionError("Malformed or unsupported triangle paint; re-export the source project.") from exc


def audit_build_items(before, after):
    if len(before) != len(after):
        raise ConversionError("Build instance count changed unexpectedly.")
    identity = "1 0 0 0 1 0 0 0 1 0 0 0"
    for old, new in zip(before, after):
        if {k: v for k, v in old.items() if k != "transform"} != {k: v for k, v in new.items() if k != "transform"}:
            raise ConversionError("Build instance identity/attributes changed unexpectedly.")
        try:
            first = [float(value) for value in old.get("transform", identity).split()]
            second = [float(value) for value in new.get("transform", identity).split()]
            if len(first) != 12 or len(second) != 12 or not all(math.isfinite(value) for value in first + second):
                raise ValueError
        except ValueError as exc:
            raise ConversionError("Invalid build instance transform.") from exc
        if any(not math.isclose(first[index], second[index], rel_tol=1e-9, abs_tol=1e-9) for index in [*range(9), 11]):
            raise ConversionError("Build instance scale/rotation/Z changed; only bed XY translation is allowed.")


def archive_info(path, filament_count=None):
    """Screen archive structure and local mesh invariants, without claiming topology."""
    with zipfile.ZipFile(path) as archive:
        members = archive.infolist()
        names = [item.filename for item in members]
        if len(set(name.casefold() for name in names)) != len(names):
            raise ConversionError("Duplicate/case-ambiguous 3MF members are unsupported.")
        for item in members:
            name = item.filename
            if "\\" in name or name.startswith("/") or ".." in PurePosixPath(name).parts or item.flag_bits & 1:
                raise ConversionError("Unsafe or encrypted 3MF archive member.")
            if item.file_size > 512 * 1024**2:
                raise ConversionError("A 3MF member exceeds this adapter's 512 MiB limit.")
        if sum(item.file_size for item in members) > 2 * 1024**3:
            raise ConversionError("Uncompressed project exceeds this adapter's 2 GiB limit.")
        models = {}
        for name in names:
            if not name.lower().endswith(".model"):
                continue
            root = xml_root(archive.read(name), name)
            geometry, paints, builds = [], [], []
            vertices = triangles = 0
            for element in root.iter():
                tag = local_tag(element)
                if tag in {"object", "vertex", "triangle", "component"}:
                    attrs = {key: value for key, value in element.attrib.items() if key != "paint_color"}
                    geometry.append([tag, sorted(attrs.items())])
                    vertices += tag == "vertex"
                    triangles += tag == "triangle"
                if tag == "item":
                    builds.append(dict(element.attrib))
                if "paint_color" in element.attrib:
                    paint = element.attrib["paint_color"]
                    states = paint_states(paint)
                    if filament_count is not None and any(state > filament_count for state in states):
                        raise ConversionError("Project contains virtual/out-of-range paint colors. Use the separate Full Spectrum workflow and inspect it in Snapmaker Orca.")
                    paints.append(paint)
            models[name] = {"geometry_sha256": hashlib.sha256(json.dumps(geometry, sort_keys=True).encode()).hexdigest(), "unit": root.get("unit", "millimeter"), "vertices": vertices, "triangles": triangles, "painted_triangles": len(paints), "paint_values": paints, "build_items": builds}
        if not sum(item["triangles"] for item in models.values()):
            raise ConversionError("No editable triangle geometry found. A sliced .gcode.3mf is insufficient; use the original project 3MF.")
        return {"models": models, "members": names}


def sanitize_layers(data, reference, mapping, *, already_mapped):
    root = xml_root(data, LAYER_COMMANDS)
    pause = reference.get("machine_pause_gcode", "")
    if not isinstance(pause, str) or not pause.strip():
        raise ConversionError("Reference must define U1 pause G-code for layer pauses.")
    for layer in root.iter():
        if local_tag(layer) != "layer":
            if local_tag(layer) not in {"custom_gcodes_per_layer", "custom_gcodes", "plate", "mode"}:
                raise ConversionError("Unknown per-layer command XML; review it in the source slicer.")
            continue
        kind = layer.get("type")
        if kind not in {"1", "2"}:
            raise ConversionError("Custom per-layer commands/color-change scripts are unsupported. Remove them in the source slicer; ordinary pause/tool-change events are supported.")
        try:
            height = float(layer.get("top_z", layer.get("print_z", "nan")))
            tool = int(layer.get("extruder", "0"))
        except ValueError as exc:
            raise ConversionError("Invalid per-layer height/tool number.") from exc
        if not math.isfinite(height) or height < 0:
            raise ConversionError("Invalid per-layer height.")
        if kind == "2":
            valid = set(mapping.values()) if already_mapped else set(mapping)
            if tool - 1 not in valid:
                raise ConversionError("Per-layer tool change refers to an unmapped source/tool slot.")
            layer.set("gcode", "")
        else:
            layer.set("gcode", pause)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def is_hook(key):
    return key.lower().endswith("_gcode")


def slot_references(path, count):
    def slot(key, value):
        try:
            number = int(value)
        except (ValueError, TypeError) as exc:
            raise ConversionError(f"Invalid filament assignment: {key}") from exc
        if str(number) != str(value) or not 0 <= number <= count:
            raise ConversionError(f"Virtual/out-of-range filament assignment {key}={value}; use the manual color workflow.")
        return number

    with zipfile.ZipFile(path) as archive:
        config = json.loads(archive.read(SETTINGS))
        project = {key: slot(key, value) for key, value in config.items() if key in SLOT_KEYS}
        objects = []
        if "Metadata/model_settings.config" in archive.namelist():
            data = archive.read("Metadata/model_settings.config")
            if re.search(br"<!\s*(DOCTYPE|ENTITY)\b", data, re.I):
                raise ConversionError("Unsupported model-settings XML declarations/entities.")
            parser = expat.ParserCreate()
            parts = []

            def start(name, attrs):
                if name == "part":
                    parts.append(False)
                elif name == "mesh_stat" and parts:
                    parts[-1] = True
                key = attrs.get("key")
                if name == "metadata" and key in SLOT_KEYS:
                    objects.append([key, slot(key, attrs.get("value"))])

            def finish(name):
                if name == "part" and not parts.pop():
                    raise ConversionError("Part metadata lacks mesh_stat, which can crash this Orca importer. Re-export the editable project from its source slicer.")

            parser.StartElementHandler = start
            parser.EndElementHandler = finish
            try:
                parser.Parse(data, True)
            except expat.ExpatError as exc:
                raise ConversionError("Malformed model-settings XML.") from exc
        return {"project": project, "objects": objects}


def sanitize_model_settings(data):
    """Patch metadata spans without rewriting Orca's extension prefixes/markup."""
    if re.search(br"<!\s*(DOCTYPE|ENTITY)\b", data, re.I):
        raise ConversionError("Unsupported model-settings XML declarations/entities.")
    parser = expat.ParserCreate()  # Keep literal names, including Orca extension prefixes.
    patches, stack, removed = [], [], []

    def tag_end(start):
        quote = None
        for index in range(start, len(data)):
            value = data[index]
            if quote is not None:
                if value == quote:
                    quote = None
            elif value in (34, 39):
                quote = value
            elif value == 62:
                return index + 1
        raise ConversionError("Unterminated model-settings XML tag.")

    def start(name, attrs):
        if name == "metadata" and any(entry[0] == "metadata" for entry in stack):
            raise ConversionError("Nested model-settings metadata is unsupported.")
        offset = parser.CurrentByteIndex
        end = tag_end(offset)
        stack.append((name, attrs.get("key", ""), offset, end, data[offset:end].rstrip().endswith(b"/>")))

    def finish(name):
        _, key, begin, end, self_closing = stack.pop()
        if name != "metadata":
            return
        if is_hook(key) or key in POST_PROCESS or key in {"gcode_flavor", "custom_gcode_per_layer"}:
            patches.append((begin, end if self_closing else tag_end(parser.CurrentByteIndex), b""))
            removed.append(key)
        elif key == "filament_maps":
            tag = data[begin:end]
            fixed, count = re.subn(br"(\bvalue\s*=\s*)([\"'])(.*?)\2", lambda match: match[1] + match[2] + b"1 2 3 4" + match[2], tag, count=1, flags=re.S)
            if count != 1:
                raise ConversionError("Malformed filament routing metadata.")
            patches.append((begin, end, fixed))

    parser.StartElementHandler = start
    parser.EndElementHandler = finish
    try:
        parser.Parse(data, True)
    except expat.ExpatError as exc:
        raise ConversionError("Malformed model-settings XML.") from exc
    for begin, end, replacement in sorted(patches, reverse=True):
        data = data[:begin] + replacement + data[end:]
    return data, removed


def sanitize_project(path, output, reference, mapping, source_info):
    changes = {"target_hooks": [], "target_hardware": [], "cleared_filament_hooks": sorted(FILAMENT_HOOKS), "removed_post_process": [], "stripped_members": [], "removed_object_hooks": []}
    with zipfile.ZipFile(path) as archive, zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as target:
        config = json.loads(archive.read(SETTINGS))
        for key in set(config) | set(reference):
            if key in POST_PROCESS or key == "custom_gcode_per_layer":
                if key in config:
                    config.pop(key)
                    changes["removed_post_process"].append(key)
            elif key in FILAMENT_HOOKS:
                config[key] = [""] * 4
            elif is_hook(key) or key == "gcode_flavor":
                if key in reference:
                    config[key] = reference[key]
                else:
                    config.pop(key, None)
                changes["target_hooks"].append(key)
            elif key.startswith(("machine_", "printer_")) or key in HARDWARE_KEYS:
                if key in reference:
                    config[key] = reference[key]
                else:
                    config.pop(key, None)
                changes["target_hardware"].append(key)
        if config.get("gcode_flavor") != "klipper":
            raise ConversionError("Selected reference must use the U1 Klipper flavor.")
        for item in archive.infolist():
            name = item.filename
            if name == MARKER:
                continue
            if re.search(r"\.(?:gcode|bgcode)(?:\.|$)", name, re.I) or re.match(r"Metadata/(?:machine|printer|process|filament)_settings.*\.config$", name, re.I):
                changes["stripped_members"].append(name)
                continue
            data = archive.read(name)
            if name == SETTINGS:
                data = json.dumps(config, indent=2).encode()
            elif name == LAYER_COMMANDS:
                data = sanitize_layers(data, reference, mapping, already_mapped=True)
            elif name == "Metadata/model_settings.config":
                data, removed = sanitize_model_settings(data)
                changes["removed_object_hooks"].extend(removed)
            target.writestr(name, data)
        target.writestr(MARKER, json.dumps({"schema_version": 1, "requires_manual_review": True, "requires_reslice": True, "ready_to_print": False, "source_sha256": source_info["sha256"], "backend_commit": COMMIT, "full_spectrum_assigned": False}))
    return changes


def run_conversion(request, runtime):
    sys.path.insert(0, str(runtime / "backend"))
    from converter import convert
    from models import ConversionSettings
    from paint_remap import remap_paint_color
    from profile_loader import read_project_settings, read_source_settings
    from rules_engine import load_rules

    source, reference, directory = (Path(request[key]) for key in ("source", "reference", "output_dir"))
    # Structure/size checks precede backend parsing of either archive.
    archive_info(reference)
    archive_info(source)
    source_cfg, source_slicer = read_source_settings(source)
    ref = read_project_settings(reference)
    if str(ref.get("printer_model", "")).strip().lower() != "snapmaker u1" or ref.get("gcode_flavor") != "klipper":
        raise ConversionError("Reference must be a Snapmaker U1 Klipper project exported from Snapmaker Orca.")
    nozzles = ref.get("nozzle_diameter")
    try:
        if not isinstance(nozzles, list) or len(nozzles) != 4 or any(not math.isfinite(float(n)) or float(n) <= 0 for n in nozzles):
            raise ValueError
    except (ValueError, TypeError) as exc:
        raise ConversionError("U1 reference must define four valid nozzle diameters.") from exc
    ids = source_cfg.get("filament_settings_id")
    if not isinstance(ids, list) or not ids:
        raise ConversionError("Use an editable Bambu/Orca project with filament settings. Geometry-only 3MF follows the normal mesh-preparation workflow.")
    count = len(ids)
    mapping = parse_slot_map(request.get("slot_map"), count)
    before = archive_info(source, count)
    source_slots = slot_references(source, count)
    with zipfile.ZipFile(source) as archive:
        if any(name.startswith("Metadata/layer_config_ranges") or name.startswith("Metadata/layer_heights_profile") for name in archive.namelist()):
            raise ConversionError("Variable-layer/range overrides need manual conversion and prime-tower review. Export a project without these overrides for this adapter.")
        if LAYER_COMMANDS in archive.namelist():
            sanitize_layers(archive.read(LAYER_COMMANDS), ref, mapping, already_mapped=False)
    raw = directory / "backend-output.3mf"
    result = convert(source_path=source, reference_path=reference, output_path=raw,
                     settings=ConversionSettings(reference_profile=reference.stem, apply_rules=request["apply_rules"], clamp_speeds=True, slot_map=mapping),
                     rules=load_rules(runtime / "rules") if request["apply_rules"] else [], preserve_bambu_metadata=False)
    write_json(directory / "diff.json", result.diff.model_dump(mode="json"))
    final = directory / "converted.3mf"
    changes = sanitize_project(raw, final, ref, mapping, request["input"])
    after = archive_info(final, 4)
    with zipfile.ZipFile(final) as archive:
        final_config = json.loads(archive.read(SETTINGS))
    if len(final_config.get("filament_settings_id", [])) != 4:
        raise ConversionError("Converted project does not define four physical tool slots.")
    for source_index, target_index in mapping.items():
        for key in ("filament_colour", "filament_settings_id"):
            if key in source_cfg and final_config.get(key, [])[target_index] != source_cfg[key][source_index]:
                raise ConversionError(f"Source palette/material identity was not retained: {key}")
    output_slots = slot_references(final, 4)
    expected_objects = [[key, mapping[value - 1] + 1 if value else 0] for key, value in source_slots["objects"]]
    if expected_objects != output_slots["objects"]:
        raise ConversionError("Object/part filament assignments changed unexpectedly.")
    for key, value in source_slots["project"].items():
        if key == "extruder" and key not in output_slots["project"]:
            continue  # Not a supported global setting in the reference schema.
        if value == 0 and key in {"wall_filament", "sparse_infill_filament", "solid_infill_filament"}:
            value = 1  # Upstream resolves the Bambu auto sentinel before routing.
        expected = mapping[value - 1] + 1 if value else 0
        if output_slots["project"].get(key) != expected:
            raise ConversionError(f"Global feature assignment was not preserved: {key}")
    if set(before["models"]) != set(after["models"]):
        raise ConversionError("Model member set changed unexpectedly; output is not validated.")
    audit = {}
    with zipfile.ZipFile(source) as original:
        for name, old in before["models"].items():
            new = after["models"][name]
            audit_build_items(old["build_items"], new["build_items"])
            for key in ("geometry_sha256", "unit", "vertices", "triangles", "painted_triangles"):
                if old[key] != new[key]:
                    raise ConversionError(f"Geometry/paint count changed unexpectedly: {name}, {key}")
            expected = xml_root(remap_paint_color(original.read(name).decode("utf-8-sig"), mapping, count).encode(), name)
            expected_paint = [e.attrib["paint_color"] for e in expected.iter() if "paint_color" in e.attrib]
            if expected_paint != new["paint_values"]:
                raise ConversionError("Paint remap was not retained in output.")
            audit[name] = {key: value for key, value in new.items() if key not in {"paint_values", "build_items"}}
            audit[name]["source_build_items"] = old["build_items"]
            audit[name]["output_build_items"] = new["build_items"]
    raw.unlink()  # Only expose the sanitized converted project as a deliverable.
    report = {"schema_version": 1, "status": "converted_review_required", "input": request["input"], "reference": request["reference_record"],
              "backend": {"repository": REPOSITORY, "commit": COMMIT, "license": "PolyForm Noncommercial 1.0.0", "required_notice": "Copyright thadius83 (https://github.com/thadius83)"},
              "source_slicer": source_slicer, "slot_map_one_based": {str(k + 1): v + 1 for k, v in mapping.items()},
              "source_filaments": ids, "target_nozzle_diameters": nozzles, "apply_rules": request["apply_rules"], "clamp_speeds": True,
              "source_nozzle_diameters": source_cfg.get("nozzle_diameter"), "nozzle_change_requires_review": set(source_cfg.get("nozzle_diameter") or []) != set(nozzles),
              "source_slot_references": source_slots, "output_slot_references": output_slots,
              "geometry_audit": audit, "geometry_and_paint_invariants_passed": True, "adapter_changes": changes,
              "geometry_checks_not_performed": ["manifoldness", "self_intersections", "minimum_feature_thickness", "actual_plate_fit_and_clearance"],
              "full_spectrum_assigned": False, "native_import_verified": False, "slice_completed": False, "slicing_verified": False, "ready_to_print": False, "printing_or_upload_performed": False,
              "review_required": ["actual_loaded_spool_presets_and_temperatures", "all_object_and_paint_tool_assignments", "nozzle_and_layer_height", "build_plates_orientation_prime_tower_and_clearance", "supports_walls_infill_and_material_use", "fresh_slice_and_layer_preview"],
              "artifacts": {"project": str(final), "diff": str(directory / "diff.json"), "report": str(directory / "report.json")}}
    write_json(directory / "report.json", report)
    return report


def worker(operation, runtime, request_path=None):
    sys.path.insert(0, str(runtime / "backend"))
    if operation == "convert":
        return run_conversion(json.loads(request_path.read_text()), runtime)
    from profile_loader import list_profiles
    profiles = [item.model_dump(mode="json") for item in list_profiles(runtime / "profiles")]
    if operation == "profiles":
        return profiles
    import importlib.metadata
    return {"available": True, "runtime": str(runtime), "commit": COMMIT, "profile_count": len(profiles), "local_only": True,
            "dependencies": {name: importlib.metadata.version(name) for name in ("pydantic", "PyYAML", "ijson")}, "ready_to_print": False}


def call_worker(operation, runtime, request_path=None):
    python = verify_runtime(runtime)
    command = [str(python), "-I", str(ROOT / "scripts/u1_offline_exec.py"), "--", str(Path(__file__).absolute()), "_worker", operation, str(runtime)]
    if request_path:
        command.append(str(request_path))
    completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600, check=False)
    if completed.returncode:
        raise ConversionError(completed.stderr.strip()[-4000:] or "Local conversion worker failed.")
    return json.loads(completed.stdout)


def convert_project(source, output_dir, runtime, *, profile=DEFAULT_PROFILE, reference=None, slot_map=None, apply_rules=False):
    source = Path(source).expanduser().absolute()
    destination = Path(output_dir).expanduser().absolute()
    if not source.is_file() or source.suffix.lower() != ".3mf" or not zipfile.is_zipfile(source):
        raise ConversionError("Input must be an existing editable project .3mf.")
    verify_runtime(runtime)
    if reference is None:
        profiles = call_worker("profiles", runtime)
        matches = [item for item in profiles if profile in {item["id"], item["display_name"], Path(item["path"]).stem}]
        if len(matches) != 1:
            raise ConversionError("Unknown reference profile; run profiles or supply --reference U1.3mf.")
        reference = Path(matches[0]["path"])
    reference = Path(reference).expanduser().absolute()
    if not reference.is_file() or not zipfile.is_zipfile(reference):
        raise ConversionError("Reference must be an existing U1 project 3MF.")
    # Refuse existing output directories, including symlinks, before making files.
    destination.mkdir(parents=True, exist_ok=False)
    preserved = destination / "input"
    preserved.mkdir()
    saved_source, saved_reference = preserved / "source.3mf", preserved / "reference.3mf"
    input_record = {"path": str(source), "sha256": digest(source), "preserved_path": str(saved_source)}
    reference_record = {"path": str(reference), "sha256": digest(reference), "preserved_path": str(saved_reference), "bundled": reference.parent == runtime / "profiles"}
    shutil.copy2(source, saved_source)
    shutil.copy2(reference, saved_reference)
    if digest(saved_source) != input_record["sha256"] or digest(saved_reference) != reference_record["sha256"]:
        raise ConversionError("Input/reference changed while being preserved; no conversion performed.")
    request = {"source": str(saved_source), "reference": str(saved_reference), "output_dir": str(destination), "input": input_record, "reference_record": reference_record, "slot_map": slot_map, "apply_rules": apply_rules}
    write_json(destination / "request.json", request)
    try:
        return call_worker("convert", runtime, destination / "request.json")
    except Exception as exc:
        # A failed audit must never leave a seemingly validated deliverable.
        for name in ("converted.3mf", "backend-output.3mf"):
            (destination / name).unlink(missing_ok=True)
        write_json(destination / "report.json", {"status": "conversion_failed", "error": str(exc), "input": input_record, "reference": reference_record, "ready_to_print": False})
        raise


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args and args[0] == "_worker":
        try:
            print(json.dumps(worker(args[1], Path(args[2]), Path(args[3]) if len(args) > 3 else None), allow_nan=False))
            return 0
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "local-runtime.json")
    parser.add_argument("--runtime-dir", type=Path, help="path to the pinned bambu-to-u1 checkout")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("profiles")
    convert = sub.add_parser("convert")
    convert.add_argument("input", type=Path)
    convert.add_argument("--output-dir", type=Path, required=True)
    target = convert.add_mutually_exclusive_group()
    target.add_argument("--profile", default=DEFAULT_PROFILE)
    target.add_argument("--reference", type=Path)
    convert.add_argument("--slot-map", help="complete one-based mapping, e.g. 1:2,2:1; no merged slots")
    convert.add_argument("--apply-rules", action="store_true", help="apply upstream global filament-tuning rules; inspect diff")
    options = parser.parse_args(args)
    try:
        runtime = options.runtime_dir.expanduser().absolute() if options.runtime_dir else runtime_path(options.config)
        if options.command == "convert":
            result = convert_project(options.input, options.output_dir, runtime, profile=options.profile, reference=options.reference, slot_map=options.slot_map, apply_rules=options.apply_rules)
        else:
            result = call_worker(options.command, runtime)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0
    except (ConversionError, OSError, ValueError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
