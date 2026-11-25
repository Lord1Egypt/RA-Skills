#!/usr/bin/env python3
"""Slice existing geometry locally with installed official Snapmaker U1 presets.

Creates an isolated data directory and preserves every run's resolved settings,
command, transcript and artifacts. Never sends a job to a printer. Successful
CLI execution still requires layer, color, support and clearance review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import zipfile

try:
    from . import u1_gcode
except ImportError:
    import u1_gcode


DEFAULT_APP = Path("/Applications/Snapmaker Orca.app")
MACHINE_NAME = "Snapmaker U1 (0.4 nozzle)"
PROCESS_FLOW_KEYS = {"inner_wall_speed", "outer_wall_speed", "internal_solid_infill_speed", "sparse_infill_speed"}
FILAMENT_FLOW_KEYS = {"filament_flow_ratio", "filament_max_volumetric_speed"}
INTENT_PRESETS = {
    "draft": "0.28mm Standard @Snapmaker U1 (0.4 nozzle)",
    "normal": "0.20mm Standard @Snapmaker U1 (0.4 nozzle)",
    "strong": "0.20mm Standard @Snapmaker U1 (0.4 nozzle)",
    "flexible": "0.20mm Standard @Snapmaker U1 (0.4 nozzle)",
}
MIXING_PRESET = "0.10mm Color Mixing @Snapmaker U1 (0.4 nozzle)"


class SliceError(ValueError):
    pass


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise SliceError(f"cannot read preset {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SliceError(f"preset must be a JSON object: {path}")
    for key, item in value.items():
        if not isinstance(item, str) and not (isinstance(item, list) and all(isinstance(entry, str) for entry in item)):
            raise SliceError(f"preset {path.name}: {key} must be a string or string array")
    return value


def resolve_preset(profiles_dir: str | Path, kind: str, name: str, *, _chain: tuple[str, ...] = ()) -> tuple[dict, list[dict]]:
    """Resolve one vendor's inheritance without asking the CLI to find parents."""
    if kind not in {"machine", "process", "filament"}:
        raise SliceError(f"unsupported preset type: {kind}")
    if not name or name in {".", ".."} or any(char in name for char in "/\\"):
        raise SliceError("preset names must be local vendor preset names")
    if name in _chain:
        raise SliceError("cyclic preset inheritance: " + " -> ".join((*_chain, name)))
    path = Path(profiles_dir) / kind / f"{name}.json"
    current = _read_json(path)
    if current.get("type") != kind:
        raise SliceError(f"preset {path.name}: expected type {kind!r}")
    parent = current.get("inherits", "")
    if not isinstance(parent, str):
        raise SliceError(f"preset {path.name}: inherits must be a string")
    if parent:
        result, sources = resolve_preset(profiles_dir, kind, parent, _chain=(*_chain, name))
    else:
        result, sources = {}, []
    result.update(current)
    result.pop("inherits", None)
    sources.append({"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return result, sources


def _standard_flow(preset: dict, metadata_key: str, flow_keys: set[str], *, scalar: bool) -> list[str]:
    variants = preset.pop(metadata_key, None)
    if variants is None:
        return []
    if not isinstance(variants, list) or "standard" not in variants:
        raise SliceError(f"{metadata_key} does not provide the requested standard flow variant")
    index = variants.index("standard")
    changed = []
    for key in sorted(flow_keys):
        value = preset.get(key)
        if isinstance(value, list):
            if len(value) != len(variants):
                raise SliceError(f"{key} has {len(value)} values for {len(variants)} flow variants")
            preset[key] = value[index] if scalar else [value[index]]
            changed.append(key)
    return changed


def prepare_profiles(profiles_dir: str | Path, *, intent: str = "normal", material: str = "Generic PLA", mixing: bool = False, infill_percent: float | None = None, supports: str = "auto") -> tuple[dict, dict]:
    if intent not in INTENT_PRESETS:
        raise SliceError("intent must be draft, normal, strong or flexible")
    if infill_percent is not None and (not math.isfinite(infill_percent) or not 0 <= infill_percent <= 100):
        raise SliceError("infill_percent must be finite and between 0 and 100")
    if supports not in {"auto", "off"}:
        raise SliceError("supports must be auto or off")
    process_name = MIXING_PRESET if mixing else INTENT_PRESETS[intent]
    presets, provenance = {}, {}
    for kind, name in [("machine", MACHINE_NAME), ("process", process_name), ("filament", material)]:
        presets[kind], provenance[kind] = resolve_preset(profiles_dir, kind, name)
        if presets[kind].get("instantiation") != "true":
            raise SliceError(f"{name!r} is an abstract preset, not an instantiated selection")
    machine, process, filament = (presets[kind] for kind in ("machine", "process", "filament"))
    try:
        u1_gcode.machine_region(machine)
    except ValueError as exc:
        raise SliceError(f"invalid machine build region: {exc}") from exc
    for kind, preset in [("process", process), ("filament", filament)]:
        compatible = preset.get("compatible_printers", [])
        if not isinstance(compatible, list) or compatible and MACHINE_NAME not in compatible:
            raise SliceError(f"{kind} preset is not compatible with {MACHINE_NAME}")
    collapsed = {
        "process": _standard_flow(process, "process_flow_support", PROCESS_FLOW_KEYS, scalar=True),
        "filament": _standard_flow(filament, "filament_flow_support", FILAMENT_FLOW_KEYS, scalar=False),
    }
    nozzles = machine.get("nozzle_diameter")
    if not isinstance(nozzles, list) or not nozzles:
        raise SliceError("machine preset must contain nozzle_diameter as a nonempty string array")
    try:
        if any(not math.isfinite(float(value)) or float(value) <= 0 for value in nozzles):
            raise ValueError
    except ValueError as exc:
        raise SliceError("machine preset contains an invalid nozzle diameter") from exc
    # Precise compatibility workaround for Snapmaker Orca's process-only CLI
    # normalization crash. The CLI normalizes EACH file before merging it:
    # src/Snapmaker_Orca.cpp load_config_file -> config.normalize_fdm(). Old
    # normalize_fdm dereferences nozzle_diameter whenever wipe_tower_filament
    # exists. A process preset lacks the machine option, yielding nullptr.
    # Official upstream fix: https://github.com/Snapmaker/OrcaSlicer/pull/561/files
    # Supplying the selected machine's identical array retains prime-tower
    # semantics and avoids that null dereference without disabling priming.
    process["nozzle_diameter"] = list(nozzles)
    process["enable_support"] = "1" if supports == "auto" else "0"
    process["support_type"] = "tree(auto)"
    applied = {"enable_support": process["enable_support"], "support_type": process["support_type"]}
    default_infill = {"draft": 8.0, "normal": 15.0, "strong": 25.0, "flexible": None}[intent]
    chosen_infill = default_infill if infill_percent is None else infill_percent
    if chosen_infill is not None:
        process["sparse_infill_density"] = f"{chosen_infill:g}%"
        applied["sparse_infill_density"] = process["sparse_infill_density"]
    if intent == "strong":
        process["wall_loops"] = "4"
        applied["wall_loops"] = "4"
    process["print_settings_id"] = process_name
    filament["filament_settings_id"] = [material]
    machine["printer_settings_id"] = MACHINE_NAME
    return presets, {
        "sources": provenance,
        "machine": MACHINE_NAME,
        "process": process_name,
        "filament": material,
        "standard_flow_collapsed_keys": collapsed,
        "intent_overrides": applied,
        "supports": {"mode": supports, "type": "tree(auto)", "preview_reviewed": False},
        "crash_workaround": "Process-only normalization receives nozzle_diameter copied unchanged from the selected machine; wipe_tower_filament and priming remain enabled as specified by the official preset.",
        "crash_reference": "https://github.com/Snapmaker/OrcaSlicer/pull/561/files",
        "mixing": {"requested": mixing, "dedicated_preset_selected": mixing, "ratios_assigned": False, "color_mapping_verified": False},
    }


def build_command(binary: str | Path, input_path: str | Path, run_dir: str | Path) -> list[str]:
    directory = Path(run_dir).resolve()
    # Explicit argument vector; no shell, upload, printer-host or print command.
    # Snapmaker Orca prefixes --outputdir to the export name even when the
    # supplied name is absolute. Use a basename or export fails with a doubled
    # path after slicing (observed with the installed 2.4.1 macOS build).
    return [str(Path(binary).resolve()), "--datadir", str(directory / "datadir"), "--load-settings", str(directory / "machine.json") + ";" + str(directory / "process.json"), "--load-filaments", str(directory / "filament.json"), "--slice", "1", "--export-3mf", "project.3mf", "--outputdir", str(directory), str(Path(input_path).resolve())]


def _duration_seconds(text: str) -> int | None:
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*([dhms])", text.lower())
    if not matches:
        return None
    return round(sum(float(value) * {"d": 86400, "h": 3600, "m": 60, "s": 1}[unit] for value, unit in matches))


def parse_gcode_metadata(text: str) -> dict:
    """Return slicer-written estimates, never geometric consumption guesses."""
    estimates = {"filament_grams_by_tool": None, "filament_mm_by_tool": None, "estimated_duration_seconds": None, "print_settings_id": None}
    for line in text.splitlines():
        match = re.match(r"\s*;\s*([^=]+?)\s*=\s*(.*?)\s*$", line)
        if not match:
            continue
        key, value = match.groups()
        if key in {"filament used [g]", "filament used [mm]"}:
            try:
                values = [float(item.strip()) for item in value.split(",")]
                if all(math.isfinite(item) and item >= 0 for item in values):
                    estimates["filament_grams_by_tool" if "[g]" in key else "filament_mm_by_tool"] = values
            except ValueError:
                pass
        elif key == "estimated printing time (normal mode)":
            estimates["estimated_duration_seconds"] = _duration_seconds(value)
        elif key == "print_settings_id":
            estimates["print_settings_id"] = value
    return estimates


def _gcode_artifacts(run_dir: Path, machine: dict) -> list[dict]:
    artifacts = []
    reviews = {}

    def artifact(path, member, data):
        text = data.decode("utf-8", errors="replace")
        digest = hashlib.sha256(data).hexdigest()
        if digest not in reviews:
            directory = run_dir / f"toolpaths_{len(reviews) + 1:04d}"
            try:
                reviews[digest] = u1_gcode.review_gcode(text, machine, directory)
            except (ValueError, OSError) as exc:
                reviews[digest] = {"passed": False, "review_completed": False, "error": str(exc), "ready_to_print": False}
        review = reviews[digest]
        return {"path": str(path), "archive_member": member, "bytes": len(data), "sha256": digest,
                "has_extrusion_moves": bool(review.get("segments_checked")),
                "estimates": parse_gcode_metadata(text), "toolpath_review": review}

    for path in sorted(run_dir.rglob("*.gcode")):
        artifacts.append(artifact(path, None, path.read_bytes()))
    project = run_dir / "project.3mf"
    if project.is_file() and zipfile.is_zipfile(project):
        with zipfile.ZipFile(project) as archive:
            for name in sorted(archive.namelist()):
                if name.lower().endswith(".gcode"):
                    artifacts.append(artifact(project, name, archive.read(name)))
    return artifacts


def slice_model(input_path: str | Path, output_dir: str | Path, *, app_path: str | Path = DEFAULT_APP, profiles_dir: str | Path | None = None, intent: str = "normal", material: str = "Generic PLA", mixing: bool = False, timeout: float = 600, dry_run: bool = False, infill_percent: float | None = None, supports: str = "auto") -> dict:
    source, destination, app = Path(input_path).resolve(), Path(output_dir).resolve(), Path(app_path).resolve()
    if not source.is_file() or source.suffix.lower() not in {".stl", ".obj", ".3mf"}:
        raise SliceError("input must be an existing STL, OBJ or 3MF file; prepare GLB geometry as STL first")
    if source.suffix.lower() == ".3mf":
        if not zipfile.is_zipfile(source):
            raise SliceError("3MF input must be a valid project archive.")
        with zipfile.ZipFile(source) as archive:
            if "Metadata/u1_conversion.json" in archive.namelist():
                raise SliceError("This converted project requires review and fresh slicing as a project in Snapmaker Orca. This adapter's single-filament overrides would replace its material and color assignments; use the project workflow in BAMBU_CONVERSION.md.")
            marker = "Metadata/u1_target_colors.json"
            if marker in archive.namelist() and json.loads(archive.read(marker)).get("requires_manual_match"):
                raise SliceError("This file contains unmatched logical target colors. Complete Full Spectrum Manual Match and save a calibrated project in Orca before slicing; a provisional single-filament override would lose the target mapping.")
            settings_member = "Metadata/project_settings.config"
            unknown_project = "Generic or unrecognized 3MF cannot use this single-filament adapter: its color assignments could be replaced. Use the color workflow in FULL_SPECTRUM.md and review the file as a native Snapmaker Orca project."
            if settings_member not in archive.namelist():
                raise SliceError(unknown_project)
            try:
                project_settings = json.loads(archive.read(settings_member))
            except (ValueError, UnicodeError) as exc:
                raise SliceError("Cannot read this project's embedded settings.") from exc
            if not isinstance(project_settings, dict):
                raise SliceError("Embedded project settings must be a JSON object.")
            filaments = project_settings.get("filament_settings_id", [])
            palette = project_settings.get("filament_colour", [])
            if ((isinstance(filaments, list) and len(filaments) > 1)
                    or (isinstance(palette, list) and len(palette) > 1)
                    or project_settings.get("mixed_filament_definitions")):
                raise SliceError("This project contains multiple filament or Full Spectrum assignments. Slice it through the native Orca project workflow; this adapter's single-filament overrides would replace its color and material mapping.")
            if (not isinstance(filaments, list) or len(filaments) != 1
                    or not isinstance(filaments[0], str) or not filaments[0].strip()):
                raise SliceError(unknown_project)
    if not math.isfinite(timeout) or timeout <= 0 or timeout > 600:
        raise SliceError("timeout must be finite, positive and at most 600 seconds")
    binary = app / "Contents" / "MacOS" / "Snapmaker_Orca"
    if not binary.is_file():
        raise SliceError(f"Snapmaker Orca executable not found: {binary}")
    vendor = Path(profiles_dir).resolve() if profiles_dir else app / "Contents" / "Resources" / "profiles" / "Snapmaker"
    presets, selection = prepare_profiles(vendor, intent=intent, material=material, mixing=mixing, infill_percent=infill_percent, supports=supports)
    destination.mkdir(parents=True, exist_ok=True)
    # A new directory makes stale G-code impossible to mistake for this run.
    index = 1
    while True:
        run_dir = destination / f"run_{index:04d}"
        try:
            run_dir.mkdir()
            break
        except FileExistsError:
            index += 1
    (run_dir / "datadir").mkdir()
    for kind, preset in presets.items():
        (run_dir / f"{kind}.json").write_text(json.dumps(preset, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    argv = build_command(binary, source, run_dir)
    (run_dir / "command.json").write_text(json.dumps(argv, indent=2) + "\n", encoding="utf-8")
    transcript = run_dir / "slice.log"
    return_code, timed_out, execution_error = None, False, None
    if dry_run:
        transcript.write_text("Dry run: slicer was not executed.\n", encoding="utf-8")
    else:
        with transcript.open("w", encoding="utf-8") as stream:
            try:
                completed = subprocess.run(argv, cwd=run_dir, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout, check=False)
                return_code = completed.returncode
            except subprocess.TimeoutExpired:
                timed_out = True
                stream.write(f"\nAdapter timeout after {timeout:g} seconds.\n")
            except OSError as exc:
                execution_error = str(exc)
                stream.write(f"\nAdapter could not execute slicer: {exc}\n")
    text = transcript.read_text(encoding="utf-8", errors="replace")
    gcodes = _gcode_artifacts(run_dir, presets["machine"]) if not dry_run else []
    project = run_dir / "project.3mf"
    exported = return_code == 0 and project.is_file() and zipfile.is_zipfile(project) and bool(gcodes)
    paths_passed = bool(gcodes) and all(item["toolpath_review"].get("passed") for item in gcodes)
    previews_generated = bool(gcodes) and all("previews" in item["toolpath_review"] for item in gcodes)
    completed = exported and paths_passed and previews_generated
    status = "prepared_not_executed" if dry_run else "slice_completed_review_required" if completed else "toolpath_review_failed" if exported else "slice_timed_out" if timed_out else "slice_failed"
    errors = [line for line in text.splitlines() if re.search(r"\berror\b|segmentation fault|not compatible|failed", line, re.IGNORECASE)][-30:]
    report = {
        "schema_version": 1,
        "status": status,
        "input": {"path": str(source), "sha256": hashlib.sha256(source.read_bytes()).hexdigest()},
        "selection": selection,
        "execution": {"command": argv, "return_code": return_code, "timeout_seconds": timeout, "timed_out": timed_out, "execution_error": execution_error, "dry_run": dry_run, "run_dir": str(run_dir), "error_lines": errors},
        "slice_completed": completed,
        "slicer_output_completed": exported,
        "toolpath_validation_passed": paths_passed,
        "toolpath_previews_generated": previews_generated,
        "slicing_verified": False,
        "ready_to_print": False,
        "printing_or_upload_performed": False,
        "review_required": ["actual_layer_preview", "supports_and_support_access", "seams", "bed_and_toolhead_clearance", "prime_tower", "material_spool_match", "color_or_full_spectrum_tool_mapping"],
        "color_notice": "Selecting a color-mixing process does not convert textures, assign ratios, calibrate filaments or establish printable colors. STL contains geometry only.",
        "artifacts": {"project": str(project) if project.is_file() else None, "gcode": gcodes, "transcript": str(transcript), "command": str(run_dir / "command.json"), "report": str(run_dir / "slicing.json")},
    }
    (run_dir / "slicing.json").write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    (destination / "slicing.json").write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--app-path", type=Path, default=DEFAULT_APP)
    parser.add_argument("--profiles-dir", type=Path, default=None, help="explicit vendor profile directory for another local installation")
    parser.add_argument("--intent", choices=list(INTENT_PRESETS), default="normal")
    parser.add_argument("--material", default="Generic PLA", help="exact installed Snapmaker filament preset name")
    parser.add_argument("--mixing", action="store_true", help="select the official 0.10 mm Color Mixing process; does not assign colors or ratios")
    parser.add_argument("--infill-percent", type=float, default=None)
    parser.add_argument("--supports", choices=["auto", "off"], default="auto", help="auto enables the official tree(auto) support mode; layer/support preview still requires review")
    parser.add_argument("--timeout", type=float, default=600)
    parser.add_argument("--dry-run", action="store_true", help="write resolved settings and command without executing the slicer")
    args = parser.parse_args(argv)
    try:
        report = slice_model(args.input, args.output_dir, app_path=args.app_path, profiles_dir=args.profiles_dir, intent=args.intent, material=args.material, mixing=args.mixing, timeout=args.timeout, dry_run=args.dry_run, infill_percent=args.infill_percent, supports=args.supports)
    except (SliceError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
    return 0 if report["slice_completed"] or args.dry_run else 1


if __name__ == "__main__":
    raise SystemExit(main())
