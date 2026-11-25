#!/usr/bin/env python3
"""Prepare a colored mesh as a generic color-capable 3MF; keep the source master.

The default palette contains target appearance colors, not spool assignments or
FullSpectrum recipes. Coordinates are assumed to be millimeters unless the user
explicitly selects another input unit. No centering, repair, or resizing occurs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import trimesh
from trimesh.visual.color import uv_to_color

CORE_NS = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
MATERIAL_NS = "http://schemas.microsoft.com/3dmanufacturing/material/2015/02"
CONTENT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
MIXING_NOTE = (
    "FullSpectrum mixing recipes are pending actual spool optical/transmission "
    "data (including polymer and transmission distance) and Orca Manual Match. "
    "Filament names/RGB values, including red, white, black, and yellow, do not "
    "determine physical mixing ratios."
)


@dataclass
class ColoredMesh:
    name: str
    vertices: np.ndarray
    faces: np.ndarray
    corner_rgb: np.ndarray
    color_source: str
    nonopaque_corners: int = 0


def _rgba(values, count):
    values = np.asarray(values)
    if values.ndim == 1:
        values = np.broadcast_to(values, (count, len(values)))
    if values.shape not in ((count, 3), (count, 4)):
        raise ValueError("color data must have three or four channels per sample")
    if not np.isfinite(values).all() or np.any(values < 0) or np.any(values > 255):
        raise ValueError("color data must contain finite channels in the range 0..255")
    # Trimesh exposes imported vertex, face, and material colors as byte RGBA.
    result = np.empty((count, 4), dtype=np.uint8)
    result[:, :3] = np.rint(values[:, :3]).astype(np.uint8)
    result[:, 3] = np.rint(values[:, 3]).astype(np.uint8) if values.shape[1] == 4 else 255
    return result


def _material_colors(material, uv, count):
    """Sample the base color only; lighting, normals, and emissive maps are omitted."""
    image = getattr(material, "baseColorTexture", None)
    is_pbr = hasattr(material, "baseColorFactor")
    if image is None:
        image = getattr(material, "image", None)
    factor = getattr(material, "baseColorFactor", None) if is_pbr else getattr(material, "diffuse", None)
    if image is not None:
        if uv is None:
            raise ValueError("textured mesh has no UV coordinates")
        sampled = _rgba(uv_to_color(uv, image), count)
        if is_pbr and factor is not None:
            # glTF baseColorFactor multiplies the texture in linear RGB space.
            factor = _rgba(factor, count).astype(np.float64) / 255.0
            srgb = sampled[:, :3].astype(np.float64) / 255.0
            linear = np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)
            linear *= factor[:, :3]
            srgb = np.where(linear <= 0.0031308, 12.92 * linear, 1.055 * linear ** (1 / 2.4) - 0.055)
            sampled[:, :3] = np.rint(np.clip(srgb, 0, 1) * 255).astype(np.uint8)
            sampled[:, 3] = np.rint(sampled[:, 3] * factor[:, 3]).astype(np.uint8)
        return sampled, "texture_uv_corners"
    if factor is not None:
        return _rgba(factor, count), "material_base_color"
    raise ValueError("mesh material has no base color or texture")


def extract_corner_colors(mesh):
    """Return independent RGB samples for each triangle corner, without mutation."""
    visual = mesh.visual
    kind = visual.kind
    if kind == "face":
        rgba = np.repeat(_rgba(visual.face_colors, len(mesh.faces))[:, None, :], 3, axis=1)
        source = "face_colors"
    elif kind == "vertex":
        rgba = _rgba(visual.vertex_colors, len(mesh.vertices))[mesh.faces]
        source = "vertex_colors"
    elif kind == "texture":
        uv = getattr(visual, "uv", None)
        if uv is not None:
            uv = np.asarray(uv, dtype=np.float64)
            if uv.shape != (len(mesh.vertices), 2) or not np.isfinite(uv).all():
                raise ValueError("UV coordinates must be finite and match the mesh vertices")
            uv = uv[mesh.faces].reshape(-1, 2)
        material = visual.material
        materials = getattr(material, "materials", None)
        if materials is None:
            rgba, source = _material_colors(material, uv, len(mesh.faces) * 3)
            rgba = rgba.reshape(-1, 3, 4)
        else:
            face_materials = getattr(visual, "face_materials", None)
            if face_materials is None:
                raise ValueError("multi-material mesh has no face-to-material assignments")
            face_materials = np.asarray(face_materials)
            if (face_materials.shape != (len(mesh.faces),) or not np.issubdtype(face_materials.dtype, np.integer)
                    or np.any(face_materials < 0) or np.any(face_materials >= len(materials))):
                raise ValueError("invalid face-to-material assignments")
            rgba = np.empty((len(mesh.faces), 3, 4), dtype=np.uint8)
            sources = set()
            uv_faces = None if uv is None else uv.reshape(-1, 3, 2)
            for index in np.unique(face_materials):
                selected = face_materials == index
                selected_uv = None if uv_faces is None else uv_faces[selected].reshape(-1, 2)
                colors, source = _material_colors(materials[int(index)], selected_uv, int(selected.sum()) * 3)
                rgba[selected] = colors.reshape(-1, 3, 4)
                sources.add(source)
            source = "+".join(sorted(sources))
    else:
        raise ValueError("mesh has no explicit face, vertex, material, or texture colors")
    return rgba[:, :, :3].copy(), source, int(np.count_nonzero(rgba[:, :, 3] != 255))


def load_colored_meshes(path, input_units="mm"):
    path = Path(path)
    if path.suffix.lower() not in {".glb", ".gltf", ".ply", ".obj"}:
        raise ValueError("input must be a GLB, glTF, PLY, or OBJ colored mesh")
    if input_units not in {"mm", "m", "model"}:
        raise ValueError("input units must be mm, m, or model")
    scene = trimesh.load_scene(path, process=False, maintain_order=True)
    result = []
    for node in sorted(scene.graph.nodes_geometry, key=str):
        transform, geometry_name = scene.graph[node]
        geometry = scene.geometry[geometry_name]
        if not isinstance(geometry, trimesh.Trimesh):
            raise ValueError(f"scene node {node!r} is not a triangle mesh")
        vertices = np.asarray(geometry.vertices, dtype=np.float64)
        faces = np.asarray(geometry.faces)
        if vertices.ndim != 2 or vertices.shape[1] != 3 or len(vertices) == 0:
            raise ValueError(f"scene node {node!r} has no valid vertices")
        if (faces.ndim != 2 or faces.shape[1] != 3 or len(faces) == 0
                or not np.issubdtype(faces.dtype, np.integer)
                or np.any(faces < 0) or np.any(faces >= len(vertices))):
            raise ValueError(f"scene node {node!r} has no valid triangle faces")
        if not np.isfinite(vertices).all() or not np.isfinite(transform).all():
            raise ValueError("mesh coordinates and scene transforms must be finite")
        colors, source, nonopaque = extract_corner_colors(geometry)
        vertices = trimesh.transform_points(vertices, transform).copy()
        if input_units == "m":
            vertices *= 1000.0
        if not np.isfinite(vertices).all():
            raise ValueError("transformed mesh coordinates must be finite")
        faces = faces.copy()
        if np.linalg.det(np.asarray(transform)[:3, :3]) < 0:
            faces = faces[:, [0, 2, 1]]
            colors = colors[:, [0, 2, 1]]
        result.append(ColoredMesh(str(node), vertices, faces, colors, source, nonopaque))
    if not result:
        raise ValueError("input contains no triangle meshes")
    return result


def _lab(rgb):
    from skimage.color import rgb2lab
    return rgb2lab(np.asarray(rgb, dtype=np.float64) / 255.0).astype(np.float32)


def _nearest_vectors(values, palette):
    # Work in chunks so a large mesh or a 256-color palette cannot create a
    # faces-times-palette-times-channels temporary array for the entire model.
    result = np.empty(len(values), dtype=np.int64)
    palette = np.asarray(palette, dtype=np.float32)
    for start in range(0, len(values), 16384):
        difference = np.asarray(values[start:start + 16384], dtype=np.float32)[:, None, :] - palette[None, :, :]
        result[start:start + 16384] = np.argmin(np.sum(difference * difference, axis=2), axis=1)
    return result


def _nearest_indices(rgb, palette):
    return _nearest_vectors(_lab(rgb), _lab(palette))


def quantize_target_colors(rgb, colors=8):
    """Deterministic Lab coverage palette that retains supported minority hues.

    Population-only clustering can spend every entry on a large jacket and erase
    the small, visibly different face. Five-unit Lab cells merge near-identical
    samples, then farthest-point selection covers perceptually distinct colors.
    Population support only suppresses isolated outliers; it saturates at 0.1%
    of samples so a small colored patch can compete with a large neutral region.
    No semantic color substitution or physical filament mixing is performed.
    """
    if not isinstance(colors, int) or isinstance(colors, bool) or not 1 <= colors <= 256:
        raise ValueError("--colors must be an integer between 1 and 256")
    rgb = np.asarray(rgb)
    if rgb.ndim != 2 or rgb.shape[1] != 3 or not len(rgb):
        raise ValueError("at least one RGB sample is required")
    if not np.isfinite(rgb).all() or np.any(rgb < 0) or np.any(rgb > 255):
        raise ValueError("RGB samples must contain finite channels in the range 0..255")
    unique, inverse, weights = np.unique(np.rint(rgb).astype(np.uint8), axis=0, return_inverse=True, return_counts=True)
    if len(unique) <= colors:
        return unique, inverse
    lab = _lab(unique)
    _, cells = np.unique(np.rint(lab / 5).astype(np.int16), axis=0, return_inverse=True)
    population = np.bincount(cells, weights=weights)
    representatives = np.column_stack([
        np.bincount(cells, weights=weights * unique[:, axis]) / population
        for axis in range(3)
    ])
    representatives = np.rint(representatives).astype(np.uint8)
    # RGB rounding can merge adjacent cells; accumulate their support explicitly.
    representatives, merged = np.unique(representatives, axis=0, return_inverse=True)
    population = np.bincount(merged, weights=population)
    candidate_lab = _lab(representatives)
    selected = [int(np.argmax(population))]
    distance = np.full(len(representatives), np.inf, dtype=np.float32)
    support = np.sqrt(np.minimum(population / max(1.0, float(weights.sum()) * 0.001), 1.0))
    while len(selected) < min(colors, len(representatives)):
        delta = candidate_lab - candidate_lab[selected[-1]]
        distance = np.minimum(distance, np.sum(delta * delta, axis=1))
        score = distance * support
        score[selected] = -1
        selected.append(int(np.argmax(score)))
    palette = np.unique(representatives[selected], axis=0)
    return palette, _nearest_vectors(lab, _lab(palette))[inverse]


def load_filament_palette(path):
    """Read explicitly supplied spool RGBs; these are not mixing recipes."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = data.get("filaments") if isinstance(data, dict) else data
    if not isinstance(entries, list) or not 1 <= len(entries) <= 256:
        raise ValueError("filament palette must be a list of 1..256 {name, rgb} records, or a filaments list")
    normalized = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str) or not entry["name"].strip():
            raise ValueError("each filament needs a nonempty name and an RGB triplet")
        rgb = entry.get("rgb")
        if (not isinstance(rgb, list) or len(rgb) != 3
                or any(not isinstance(channel, int) or isinstance(channel, bool) or not 0 <= channel <= 255 for channel in rgb)):
            raise ValueError("filament RGB must be three integers in the range 0..255")
        normalized.append({"name": entry["name"], "rgb": rgb})
    if len({tuple(entry["rgb"]) for entry in normalized}) != len(normalized):
        raise ValueError("filament RGB triplets must be distinct")
    return np.array([entry["rgb"] for entry in normalized], dtype=np.uint8), normalized


def _xml(tag, namespace=CORE_NS):
    return f"{{{namespace}}}{tag}"


def build_3mf(meshes, palette, assignments):
    """Serialize intact geometry with an explicit material-extension color at every corner."""
    ET.register_namespace("", CORE_NS)
    ET.register_namespace("m", MATERIAL_NS)
    model = ET.Element(_xml("model"), {
        "unit": "millimeter", "{http://www.w3.org/XML/1998/namespace}lang": "en-US", "requiredextensions": "m",
    })
    ET.SubElement(model, _xml("metadata"), {"name": "Title"}).text = "Target color regions"
    ET.SubElement(model, _xml("metadata"), {"name": "Description"}).text = "Surface target colors; spool matching and FullSpectrum recipes remain pending."
    resources = ET.SubElement(model, _xml("resources"))
    group = ET.SubElement(resources, _xml("colorgroup", MATERIAL_NS), {"id": "1"})
    for rgb in palette:
        ET.SubElement(group, _xml("color", MATERIAL_NS), {"color": "#" + "".join(f"{int(c):02X}" for c in rgb) + "FF"})
    build = ET.SubElement(model, _xml("build"))
    offset = 0
    for index, mesh in enumerate(meshes, start=2):
        obj = ET.SubElement(resources, _xml("object"), {"id": str(index), "type": "model", "name": mesh.name, "pid": "1", "pindex": "0"})
        element = ET.SubElement(obj, _xml("mesh"))
        vertices = ET.SubElement(element, _xml("vertices"))
        for vertex in mesh.vertices:
            ET.SubElement(vertices, _xml("vertex"), {axis: format(float(value), ".17g") for axis, value in zip("xyz", vertex)})
        triangles = ET.SubElement(element, _xml("triangles"))
        count = len(mesh.faces) * 3
        indices = assignments[offset:offset + count].reshape(-1, 3)
        offset += count
        for face, color in zip(mesh.faces, indices):
            attrs = {f"v{i + 1}": str(int(value)) for i, value in enumerate(face)}
            attrs.update({"pid": "1", **{f"p{i + 1}": str(int(value)) for i, value in enumerate(color)}})
            ET.SubElement(triangles, _xml("triangle"), attrs)
        ET.SubElement(build, _xml("item"), {"objectid": str(index)})
    if offset != len(assignments):
        raise ValueError("color assignment count does not match the mesh")
    content_types = ET.Element(_xml("Types", CONTENT_NS))
    ET.SubElement(content_types, _xml("Default", CONTENT_NS), {"Extension": "rels", "ContentType": "application/vnd.openxmlformats-package.relationships+xml"})
    ET.SubElement(content_types, _xml("Default", CONTENT_NS), {"Extension": "model", "ContentType": "application/vnd.ms-package.3dmanufacturing-3dmodel+xml"})
    relationships = ET.Element(_xml("Relationships", REL_NS))
    ET.SubElement(relationships, _xml("Relationship", REL_NS), {"Target": "/3D/3dmodel.model", "Id": "rel0", "Type": "http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"})
    # Orca's OPC reader compares literal element names, so package relationship
    # and content-type documents need default namespaces rather than ns0 tags.
    # Serialize each document while its own namespace is the default.
    model_bytes = ET.tostring(model, encoding="utf-8", xml_declaration=True)
    ET.register_namespace("", CONTENT_NS)
    content_bytes = ET.tostring(content_types, encoding="utf-8", xml_declaration=True)
    ET.register_namespace("", REL_NS)
    relationship_bytes = ET.tostring(relationships, encoding="utf-8", xml_declaration=True)
    ET.register_namespace("", CORE_NS)
    return {
        "[Content_Types].xml": content_bytes,
        "_rels/.rels": relationship_bytes,
        "3D/3dmodel.model": model_bytes,
    }


def _write_3mf(path, entries):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in entries.items():
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data, compresslevel=9)


def prepare_colors(input_path, output_dir, colors=8, input_units="mm", mode="target", filament_palette=None):
    input_path = Path(input_path).resolve()
    output_dir = Path(output_dir).resolve()
    if not input_path.is_file():
        raise ValueError(f"input file does not exist: {input_path}")
    if mode not in {"target", "nearest-filament"}:
        raise ValueError("mode must be target or nearest-filament")
    if not isinstance(colors, int) or isinstance(colors, bool) or not 1 <= colors <= 256:
        raise ValueError("--colors must be an integer between 1 and 256")
    if mode == "target" and filament_palette is not None:
        raise ValueError("--filament-palette requires --mode nearest-filament")
    if mode == "nearest-filament" and filament_palette is None:
        raise ValueError("--mode nearest-filament requires --filament-palette")
    mesh_path = output_dir / f"{input_path.stem}_color_regions.3mf"
    report_path = output_dir / "target_color_regions.json"
    if input_path in {mesh_path.resolve(), report_path.resolve()}:
        raise ValueError("output must not replace the source master")
    source_hash = hashlib.sha256(input_path.read_bytes()).hexdigest()
    meshes = load_colored_meshes(input_path, input_units)
    samples = np.concatenate([mesh.corner_rgb.reshape(-1, 3) for mesh in meshes])
    target_palette, target_assignments = quantize_target_colors(samples, colors)
    filaments = None
    if mode == "nearest-filament":
        palette, filaments = load_filament_palette(filament_palette)
        assignments = _nearest_indices(samples, palette)
    else:
        palette, assignments = target_palette, target_assignments
    bounds = np.array([np.min(np.vstack([mesh.vertices.min(axis=0) for mesh in meshes]), axis=0),
                       np.max(np.vstack([mesh.vertices.max(axis=0) for mesh in meshes]), axis=0)])
    faces = assignments.reshape(-1, 3)
    regions = []
    for index, rgb in enumerate(target_palette):
        regions.append({
            "index": index, "target_rgb": [int(c) for c in rgb],
            "target_hex": "#" + "".join(f"{int(c):02X}" for c in rgb),
            "corner_count": int(np.count_nonzero(target_assignments == index)),
            "triangle_count": int(np.count_nonzero(np.any(target_assignments.reshape(-1, 3) == index, axis=1))),
        })
    output_regions = [{
        "index": index, "rgb": [int(c) for c in rgb],
        "corner_count": int(np.count_nonzero(assignments == index)),
        "triangle_count": int(np.count_nonzero(np.any(faces == index, axis=1))),
        **({"filament_name": filaments[index]["name"]} if filaments is not None else {}),
    } for index, rgb in enumerate(palette)]
    report = {
        "schema_version": 1,
        "source_master": {"path": str(input_path), "sha256": source_hash, "preserved": True},
        "input_units": input_units,
        "millimeters_per_input_unit": 1000.0 if input_units == "m" else 1.0,
        "unit_note": "Numeric coordinates are assumed millimeters; GLB/glTF nominal meter units are deliberately overridden by this explicit input-units choice." if input_units == "mm" else (
            "Meter coordinates were converted to millimeters." if input_units == "m" else "Uncalibrated model coordinates were assigned one millimeter per unit; physical size must be checked."),
        "output_3mf": str(mesh_path),
        "output_format": "generic_3mf_materials_extension_colorgroup",
        "geometry": {
            "mesh_instances": len(meshes), "vertices": sum(len(mesh.vertices) for mesh in meshes),
            "triangles": sum(len(mesh.faces) for mesh in meshes), "bounds_mm": bounds.tolist(),
            "size_mm": (bounds[1] - bounds[0]).tolist(),
            "changes": "Scene transforms baked; reflected instances have winding corrected. No repair, simplification, centering, or resizing; only explicit input-unit conversion.",
        },
        "color_extraction": {
            "meshes": [{"name": mesh.name, "source": mesh.color_source} for mesh in meshes],
            "sample_count": len(samples), "unique_sampled_rgb": len(np.unique(samples, axis=0)),
            "sample_unit": "triangle_corner", "nonopaque_corner_count": sum(mesh.nonopaque_corners for mesh in meshes),
            "alpha_note": "RGB is retained and output colors are opaque; transparency is not a printable mixing ratio.",
            "texture_note": "Texture base colors are sampled at existing triangle UV corners with nearest-pixel sampling; interior texture detail, custom sampler modes, and lighting are not baked. Dense geometry may be needed for texture fidelity.",
        },
        "quantization": {
            "choice": mode, "requested_target_colors": colors, "target_color_count": len(target_palette),
            "method": "deterministic support-weighted perceptual Lab farthest-point coverage; nearest DeltaE76; no dithering",
            "salience_note": "Perceptually distinct minority hues compete for palette entries after near-identical colors are grouped. This preserves color coverage without identifying anatomy or substituting expected skin colors; finite palettes can still lose detail.",
            "counts_note": "Corner counts measure sampled references, not surface area or filament amounts. A triangle can reference multiple target colors and count in multiple regions.",
            "target_colors_are_virtual": True,
        },
        "target_color_regions": regions,
        "output_color_regions": output_regions,
        "fullspectrum": {"status": "pending_actual_spool_data_and_orca_manual_match", "recipes_calculated": False, "note": MIXING_NOTE},
        "orca": {
            "status": "manual_import_and_color_matching_required",
            "note": "This is a generic surface-color 3MF, not an Orca project or preconfigured FullSpectrum job. Native Orca color import and matching have not been verified by this tool. Review geometry, colors, actual spool assignments, and sliced output in Snapmaker Orca.",
        },
    }
    entries = build_3mf(meshes, palette, assignments)
    output_dir.mkdir(parents=True, exist_ok=True)
    # Stage both complete derivatives before replacing any previous derivative.
    with tempfile.TemporaryDirectory(prefix=".u1-color-", dir=output_dir) as staging:
        staged_mesh = Path(staging) / mesh_path.name
        staged_report = Path(staging) / report_path.name
        _write_3mf(staged_mesh, entries)
        staged_report.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        os.replace(staged_mesh, mesh_path)
        os.replace(staged_report, report_path)
    return mesh_path, report_path, report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="source master GLB/glTF, PLY, or OBJ (left untouched)")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--colors", type=int, default=8, help="maximum virtual target colors, 1..256; default: 8")
    parser.add_argument("--input-units", "--units", choices=("mm", "m", "model"), default="mm", help="explicit coordinate interpretation; default: mm (even for GLB)")
    parser.add_argument("--mode", choices=("target", "nearest-filament"), default="target", help="default preserves target colors; nearest-filament explicitly uses supplied spool RGBs")
    parser.add_argument("--filament-palette", type=Path, help="JSON list of {name, rgb:[r,g,b]} actual spool records, or {filaments:[...]}; nearest-filament mode only")
    args = parser.parse_args(argv)
    try:
        mesh, report_path, report = prepare_colors(args.input, args.output_dir, args.colors, args.input_units, args.mode, args.filament_palette)
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"3MF: {mesh}")
    print(f"Target color report: {report_path}")
    print(f"Target colors: {report['quantization']['target_color_count']} (choice: {args.mode})")
    print(f"Source master retained: {args.input}")
    print(MIXING_NOTE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
