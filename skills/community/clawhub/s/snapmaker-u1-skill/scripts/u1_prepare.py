#!/usr/bin/env python3
"""Deterministically orient, scale, place and screen an existing triangle mesh.

This performs mesh preparation, not reconstruction, background segmentation,
automatic repair, color mixing or slicing. Requires numpy and trimesh.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import shutil
import sys

import numpy as np
import trimesh


NOMINAL_ENVELOPE_MM = np.array([270.0, 270.0, 270.0])
BED_CENTER_MM = np.array([135.5, 136.0])
SUPPORTED_INPUTS = {".stl", ".obj", ".glb"}
INTENT_INFILL = {"draft": 8.0, "normal": 15.0, "strong": 25.0, "flexible": None}


class PreparationError(ValueError):
    """Input cannot safely be prepared without a user-directed geometry edit."""


def _validate_mesh(mesh: trimesh.Trimesh, label: str) -> None:
    if not isinstance(mesh, trimesh.Trimesh):
        raise PreparationError(f"{label}: expected triangle mesh geometry")
    vertices, faces = np.asarray(mesh.vertices), np.asarray(mesh.faces)
    if vertices.ndim != 2 or vertices.shape[1] != 3 or not len(vertices):
        raise PreparationError(f"{label}: contains no usable 3D vertices")
    if faces.ndim != 2 or faces.shape[1] != 3 or not len(faces):
        raise PreparationError(f"{label}: contains no triangle faces")
    if not np.isfinite(vertices).all():
        raise PreparationError(f"{label}: contains NaN or infinite coordinates")
    if not np.issubdtype(faces.dtype, np.integer) or faces.min() < 0 or faces.max() >= len(vertices):
        raise PreparationError(f"{label}: contains invalid vertex indices")


def _load_scene(path: Path) -> trimesh.Scene:
    if path.suffix.lower() not in SUPPORTED_INPUTS:
        raise PreparationError("input must be STL, OBJ or GLB")
    if not path.is_file():
        raise PreparationError(f"input does not exist: {path}")
    try:
        # Processing is deliberately disabled: no hole filling, decimation,
        # normal repair, vertex removal or implicit component filtering.
        original = trimesh.load_scene(path, process=False, allow_remote=False)
    except Exception as exc:
        raise PreparationError(f"cannot load mesh: {exc}") from exc
    return _bake_scene(original)


def _bake_scene(original: trimesh.Scene) -> trimesh.Scene:
    """Flatten instance transforms without processing or repairing geometry."""
    if not original.graph.nodes_geometry:
        raise PreparationError("input contains no mesh instances")
    result = trimesh.Scene()
    for index, node in enumerate(original.graph.nodes_geometry):
        transform, geometry_name = original.graph[node]
        geometry = original.geometry[geometry_name]
        _validate_mesh(geometry, f"geometry {geometry_name!r}")
        transform = np.asarray(transform, dtype=float)
        if transform.shape != (4, 4) or not np.isfinite(transform).all():
            raise PreparationError(f"geometry {geometry_name!r}: invalid scene transform")
        placed = geometry.copy()
        placed.apply_transform(transform)
        _validate_mesh(placed, f"geometry {geometry_name!r}")
        # Bake instance transforms while retaining UVs and material images.
        name = f"part_{index:04d}"
        result.add_geometry(placed, node_name=name, geom_name=name)
    return result


def _combined_mesh(scene: trimesh.Scene) -> trimesh.Trimesh:
    # The scene is flattened and has only identity instance transforms here.
    # Diagnostics and STL need only geometry; avoid building texture atlases.
    vertices, faces, offset = [], [], 0
    for part in scene.geometry.values():
        vertices.append(np.asarray(part.vertices))
        faces.append(np.asarray(part.faces) + offset)
        offset += len(part.vertices)
    return trimesh.Trimesh(vertices=np.vstack(vertices), faces=np.vstack(faces), process=False)


def _topology_mesh(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """Use exact coincident vertices for diagnostics, without changing exports.

    STL stores separate vertices per triangle. Exact welding in a diagnostic
    copy makes edge topology meaningful; no tolerance-based repair is applied.
    Unreferenced source vertices do not affect placement or diagnostics.
    """
    faces = np.asarray(mesh.faces)
    used = np.unique(faces.reshape(-1))
    vertices, inverse = np.unique(np.asarray(mesh.vertices)[used], axis=0, return_inverse=True)
    lookup = np.empty(len(mesh.vertices), dtype=np.int64)
    lookup[used] = inverse
    return trimesh.Trimesh(vertices=vertices, faces=lookup[faces], process=False)


def _face_components(mesh: trimesh.Trimesh) -> list[np.ndarray]:
    components = trimesh.graph.connected_components(
        mesh.face_adjacency, nodes=np.arange(len(mesh.faces)), min_len=1
    )
    # Stable ordering across graph backends; components are edge-connected.
    return sorted((np.sort(item) for item in components), key=lambda item: int(item[0]))


def _referenced_bounds(scene: trimesh.Scene) -> np.ndarray:
    mesh = _combined_mesh(scene)
    return np.array([mesh.triangles.reshape(-1, 3).min(axis=0), mesh.triangles.reshape(-1, 3).max(axis=0)])


def _keep_largest_component(scene: trimesh.Scene) -> tuple[trimesh.Scene, dict]:
    combined = _combined_mesh(scene)
    diagnostic = _topology_mesh(combined)
    components = _face_components(diagnostic)
    # Surface area is independent of triangulation density. Tie: first face.
    winner = max(components, key=lambda part: (float(combined.area_faces[part].sum()), -int(part[0])))
    keep = np.zeros(len(combined.faces), dtype=bool)
    keep[winner] = True
    result, offset = trimesh.Scene(), 0
    for name, geometry in scene.geometry.items():
        indices = np.flatnonzero(keep[offset : offset + len(geometry.faces)])
        offset += len(geometry.faces)
        if not len(indices):
            continue
        if len(indices) == len(geometry.faces):
            retained = geometry.copy()
        else:
            retained = geometry.submesh([indices], append=True, repair=False)
        result.add_geometry(retained, geom_name=name, node_name=name)
    return result, {
        "requested": True,
        "selection_metric": "surface_area",
        "input_components": len(components),
        "removed_components": len(components) - 1,
        "removed_faces": len(combined.faces) - len(winner),
        "warning": "Explicit component removal can discard eyewear or other intended detached details.",
    }


def _up_transform(axis: str) -> np.ndarray:
    # Proper rotations (determinant +1), never a reflection.
    transform = np.eye(4)
    if axis == "x":
        transform[:3, :3] = [[0, 0, -1], [0, 1, 0], [1, 0, 0]]
    elif axis == "y":
        transform[:3, :3] = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]
    return transform


def inspect_mesh(mesh: trimesh.Trimesh) -> dict:
    """Screen geometry in millimeters. This does not establish printability."""
    _validate_mesh(mesh, "prepared mesh")
    diagnostic = _topology_mesh(mesh)
    triangles = diagnostic.triangles
    bounds = np.array([triangles.reshape(-1, 3).min(axis=0), triangles.reshape(-1, 3).max(axis=0)])
    size = bounds[1] - bounds[0]
    double_area = np.linalg.norm(np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0]), axis=1)
    area_tolerance = max(float(size.max()) ** 2 * 1e-24, 1e-24)
    _, edge_counts = np.unique(diagnostic.edges_sorted, axis=0, return_counts=True)
    normalized_faces = np.sort(diagnostic.faces, axis=1)
    duplicate_faces = len(normalized_faces) - len(np.unique(normalized_faces, axis=0))
    lower = np.array([*(BED_CENTER_MM - NOMINAL_ENVELOPE_MM[:2] / 2), 0.0])
    upper = lower + NOMINAL_ENVELOPE_MM
    tolerance = 1e-6
    fit = bool(np.all(bounds[0] >= lower - tolerance) and np.all(bounds[1] <= upper + tolerance))
    watertight = bool(diagnostic.is_watertight)
    winding = bool(diagnostic.is_winding_consistent)
    components = _face_components(diagnostic)
    return {
        "triangles": len(diagnostic.faces),
        "vertices_in_export": len(mesh.vertices),
        "vertices_after_exact_weld_for_diagnostics": len(diagnostic.vertices),
        "bounds_min_mm": bounds[0].tolist(),
        "bounds_max_mm": bounds[1].tolist(),
        "size_mm": size.tolist(),
        "watertight": watertight,
        "winding_consistent": winding,
        "degenerate_triangles": int(np.count_nonzero(double_area <= area_tolerance)),
        "degenerate_double_area_threshold_mm2": area_tolerance,
        "duplicate_triangles": duplicate_faces,
        "open_boundary_edges": int(np.count_nonzero(edge_counts == 1)),
        "nonmanifold_edges": int(np.count_nonzero(edge_counts > 2)),
        "edge_connected_components": len(components),
        "component_signed_volumes_mm3": [float(diagnostic.submesh([part], append=True, repair=False).volume) for part in components] if watertight and winding else None,
        "fits_nominal_u1_envelope": fit,
        "nominal_envelope_mm": NOMINAL_ENVELOPE_MM.tolist(),
        "nominal_placement_bounds_mm": [lower.tolist(), upper.tolist()],
        "fit_scope": "Bounding box in a nominal 270 mm envelope centered at the requested bed coordinates. Actual profile polygon, supports, brim and prime-tower clearance are untested.",
        "topology_method": "Exact coincident-vertex welding in a diagnostic copy; exported geometry is not repaired.",
        "untested": ["self_intersections", "minimum_feature_thickness", "stability_and_adhesion", "likeness", "background_geometry", "actual_printable_polygon", "supports_and_toolhead_clearance"],
    }


def _geometry_review_reasons(screen: dict) -> list[str]:
    reasons = []
    for key, message in [
        ("watertight", "mesh is not watertight"),
        ("winding_consistent", "mesh winding is inconsistent"),
        ("fits_nominal_u1_envelope", "mesh exceeds the nominal U1 envelope"),
    ]:
        if not screen[key]:
            reasons.append(message)
    if screen["degenerate_triangles"]:
        reasons.append("mesh contains degenerate triangles")
    if screen["duplicate_triangles"]:
        reasons.append("mesh contains duplicate triangles")
    volumes = screen["component_signed_volumes_mm3"]
    if volumes is not None and any(volume <= 0 for volume in volumes):
        reasons.append("one or more closed components have nonpositive signed volume")
    return reasons


def _screen_encoded_export(payload: bytes, file_type: str) -> dict:
    """Screen the exact serialized bytes, including float32 coordinate effects."""
    scope = f"Decoded {file_type.upper()} export bytes with processing and repair disabled; instance transforms baked for diagnostics only."
    details = {"scope": scope, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}
    try:
        decoded = trimesh.load_scene(io.BytesIO(payload), file_type=file_type, process=False, allow_remote=False)
        geometry = inspect_mesh(_combined_mesh(_bake_scene(decoded)))
        reasons = _geometry_review_reasons(geometry)
        return {**details, "status": "needs_geometry_review" if reasons else "geometry_screen_passed", "geometry": geometry, "review_reasons": reasons}
    except Exception as exc:
        return {**details, "status": "readback_failed", "review_reasons": [f"encoded mesh could not be screened: {type(exc).__name__}: {exc}"]}


def _print_plan(intent: str, material: str, infill_percent: float | None) -> dict:
    effective_infill = INTENT_INFILL[intent] if infill_percent is None else infill_percent
    return {
        "status": "recommendations_only_unsliced",
        "intent": intent,
        "material": {"requested_family": material, "verified_loaded_spool": False, "recommendation": "Use a matching installed material preset and confirm spool family/brand; no temperature or flow settings have been applied."},
        "infill": {"recommended_percent": effective_infill, "recommended_pattern": "matching TPU profile" if intent == "flexible" else "gyroid or cubic if supported", "applied_to_mesh": False},
        "walls": {"recommended_perimeters": 4 if intent == "strong" else 3, "status": "starting_point_only"},
        "supports": {"status": "unverified", "recommendation": "Inspect overhangs and support access in Snapmaker Orca; compare tree/organic and normal supports where appropriate. Protect delicate features and visible surfaces."},
        "color": {"mode": "preserve_source_textures", "full_spectrum": "not_converted", "recommendation": "Retain source colors. Verify actual filament identities, calibrated Full Spectrum mixing and slicer color assignments before creating a print project; no automatic palette substitution or mixing was performed."},
        "slicing_verified": False,
        "planned_plate_count": None,
        "verified_plate_count": None,
        "sliced_material_grams": None,
        "sliced_duration_seconds": None,
    }


def prepare_mesh(
    input_path: str | Path,
    output_dir: str | Path,
    *,
    height_mm: float = 150.0,
    up_axis: str = "z",
    largest_component: bool = False,
    material: str = "PLA",
    infill_percent: float | None = None,
    intent: str = "normal",
) -> dict:
    """Prepare existing geometry and return the same report written to disk.

    Input axis is an explicit positive up direction, not inferred anatomy.
    A non-passing screen still exports a candidate for review. Malformed,
    nonfinite, empty or heightless input raises PreparationError.
    """
    if not math.isfinite(height_mm) or height_mm <= 0:
        raise PreparationError("height_mm must be finite and positive")
    if up_axis not in {"x", "y", "z"}:
        raise PreparationError("up_axis must be x, y or z")
    if intent not in INTENT_INFILL:
        raise PreparationError("intent must be draft, normal, strong or flexible")
    if infill_percent is not None and (not math.isfinite(infill_percent) or not 0 <= infill_percent <= 100):
        raise PreparationError("infill_percent must be finite and between 0 and 100")
    if not material.strip():
        raise PreparationError("material must not be empty")
    source, destination = Path(input_path).resolve(), Path(output_dir).resolve()
    if source in {destination / name for name in ("prepared.stl", "prepared.glb", "preparation.json")}:
        raise PreparationError("output artifact would overwrite the input master; choose another output directory")
    scene = _load_scene(source)
    source_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    source_faces = sum(len(part.faces) for part in scene.geometry.values())
    source_bounds = _referenced_bounds(scene)
    component_selection = {"requested": False, "removed_components": 0, "removed_faces": 0}
    if largest_component:
        scene, component_selection = _keep_largest_component(scene)

    orientation = _up_transform(up_axis)
    # Work on baked vertices to avoid glTF scene unit/transform ambiguity.
    for geometry in scene.geometry.values():
        geometry.apply_transform(orientation)
    oriented_bounds = _referenced_bounds(scene)
    source_height = float(oriented_bounds[1, 2] - oriented_bounds[0, 2])
    if not math.isfinite(source_height) or source_height <= 0:
        raise PreparationError("input has zero height along the selected up axis")
    scale = height_mm / source_height
    if not math.isfinite(scale):
        raise PreparationError("requested height produces a nonfinite scale")
    scaled_bounds = oriented_bounds * scale
    translation = np.array([*(BED_CENTER_MM - (scaled_bounds[0, :2] + scaled_bounds[1, :2]) / 2), -scaled_bounds[0, 2]])
    placement = np.eye(4)
    placement[:3, :3] *= scale
    placement[:3, 3] = translation
    for geometry in scene.geometry.values():
        geometry.apply_transform(placement)
        _validate_mesh(geometry, "prepared mesh")
    combined = _combined_mesh(scene)
    screen = inspect_mesh(combined)
    screen["scope"] = "Prepared coordinates before export serialization; this does not screen the encoded STL or GLB files."
    if screen["degenerate_triangles"] == screen["triangles"]:
        raise PreparationError("input has no nondegenerate triangles")
    review_reasons = _geometry_review_reasons(screen)

    # Export in memory first so validation failures cannot overwrite outputs.
    stl = combined.export(file_type="stl")
    warnings = []
    try:
        glb = scene.export(file_type="glb")
    except Exception as exc:
        glb = None
        warnings.append(f"GLB export failed; keep original master and sidecars: {type(exc).__name__}: {exc}")
    export_geometry = {"stl": _screen_encoded_export(stl, "stl"), "glb": _screen_encoded_export(glb, "glb") if glb is not None else {"status": "not_exported"}}
    for file_type, diagnostic in export_geometry.items():
        for reason in diagnostic.get("review_reasons", []):
            review_reasons.append(f"exported {file_type.upper()}: {reason}")
    destination.mkdir(parents=True, exist_ok=True)
    source_dir = destination / "source"
    source_dir.mkdir(exist_ok=True)
    source_copy = source_dir / source.name
    if source != source_copy:
        shutil.copy2(source, source_copy)
    (destination / "prepared.stl").write_bytes(stl)
    glb_path = destination / "prepared.glb"
    if glb is not None:
        glb_path.write_bytes(glb)
    elif glb_path.exists():
        # Do not let an earlier run's GLB appear to belong to this run.
        glb_path.unlink()
    visual_kinds = sorted({str(part.visual.kind) for part in scene.geometry.values()})
    report = {
        "schema_version": 1,
        "status": "needs_geometry_review" if review_reasons else "geometry_screen_passed",
        "ready_to_print": False,
        "source": {
            "path": str(source),
            "sha256": source_sha256,
            "copied_input": str(source_copy),
            "copied_input_includes_external_sidecars": False,
            "external_sidecar_note": "OBJ materials/images remain at their original paths. The exported GLB embeds materials/images that the loader successfully resolved; retain the original asset directory.",
            "bounds_input_units": source_bounds.tolist(),
            "triangles": source_faces,
            "visual_kinds": visual_kinds,
        },
        "transform": {
            "up_axis": up_axis,
            "up_axis_inferred": False,
            "height_mm": height_mm,
            "uniform_scale": scale,
            "preserves_aspect_ratio": True,
            "bed_center_xy_mm": BED_CENTER_MM.tolist(),
            "base_z_mm": 0.0,
            "source_world_to_prepared_mm": (placement @ orientation).tolist(),
        },
        "component_selection": component_selection,
        "geometry": screen,
        "export_geometry": export_geometry,
        "review_reasons": review_reasons,
        "operations_not_performed": ["background_removal", "hole_filling", "normal_repair", "self_intersection_repair", "decimation", "pedestal_addition", "full_spectrum_conversion", "slicing"],
        "artifacts": {"stl": str(destination / "prepared.stl"), "glb": str(glb_path) if glb is not None else None, "report": str(destination / "preparation.json")},
        "print_plan": _print_plan(intent, material, infill_percent),
        "warnings": warnings,
        "software": {"trimesh": trimesh.__version__, "numpy": np.__version__},
    }
    (destination / "preparation.json").write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="existing STL, OBJ or GLB mesh")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--height-mm", type=float, default=150.0)
    parser.add_argument("--up-axis", choices=["x", "y", "z"], default="z", help="explicit positive source up direction; default: z")
    parser.add_argument("--largest-component", action="store_true", help="explicitly discard all but the edge-connected component with greatest surface area; can remove intended details")
    parser.add_argument("--intent", choices=list(INTENT_INFILL), default="normal")
    parser.add_argument("--material", default="PLA", help="requested material family for the unsliced recommendation")
    parser.add_argument("--infill-percent", type=float, default=None, help="recommendation only; default follows intent")
    args = parser.parse_args(argv)
    try:
        report = prepare_mesh(args.input, args.output_dir, height_mm=args.height_mm, up_axis=args.up_axis, largest_component=args.largest_component, intent=args.intent, material=args.material, infill_percent=args.infill_percent)
    except (PreparationError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
    return 1 if report["review_reasons"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
