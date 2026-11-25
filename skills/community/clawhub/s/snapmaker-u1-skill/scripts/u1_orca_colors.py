#!/usr/bin/env python3
"""Convert this skill's generic color 3MF to unsliced Orca whole-face paint.

Target palette entries remain logical appearance targets. They require Manual
Match and a fresh slice before printing; no physical mixing recipes are inferred.
Format references: Snapmaker/OrcaSlicer src/libslic3r/Model.cpp CONST_FILAMENTS
and src/libslic3r/Format/bbs_3mf.cpp MMU_SEGMENTATION_ATTR (paint_color).

The settings template must contain one source filament and no existing mixing
definitions. Calibrated multicolor projects need the separate GUI workflow.
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

import numpy as np
from skimage.color import rgb2lab

CORE = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
MATERIAL = "http://schemas.microsoft.com/3dmanufacturing/material/2015/02"
CODES = ("4", "8", "0C", "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "AC", "BC", "CC", "DC")
RELS = b'''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'''
TYPES = b'''<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/><Default Extension="config" ContentType="application/octet-stream"/></Types>'''


def load_unmatched_template(template):
    """Reject templates whose physical/virtual color indices must be preserved."""
    with ZipFile(template) as archive:
        config = json.loads(archive.read("Metadata/project_settings.config"))
    if not isinstance(config, dict):
        raise ValueError("template project settings must be a JSON object")
    definitions = config.get("mixed_filament_definitions", "")
    if not isinstance(definitions, str) or definitions.strip():
        raise ValueError("template contains existing mixing definitions; preserve the calibrated project and use Full Spectrum Manual Match in Snapmaker Orca. This helper creates fresh unmatched target colors only.")
    for key in ("filament_settings_id", "filament_colour"):
        values = config.get(key)
        if (not isinstance(values, list) or len(values) != 1
                or not isinstance(values[0], str) or not values[0].strip()):
            raise ValueError("template must contain exactly one source filament (filament_settings_id and filament_colour). Multicolor/calibrated templates require the separate Snapmaker Orca project workflow.")
    return config


def convert(source, template, output):
    source, template, output = Path(source), Path(template), Path(output)
    if output.resolve() in {source.resolve(), template.resolve()}:
        raise ValueError("output must differ from source and template")
    # Check before reading/repainting a potentially large source mesh or writing
    # any output: old virtual definitions cannot be rebound to new palette IDs.
    config = load_unmatched_template(template)
    with ZipFile(source) as archive:
        root = ET.fromstring(archive.read("3D/3dmodel.model"))
    resources = root.find(f"{{{CORE}}}resources")
    if resources is None:
        raise ValueError("source has no model resources")
    groups = resources.findall(f"{{{MATERIAL}}}colorgroup")
    if len(groups) != 1:
        raise ValueError("source must contain exactly one material color group")
    group = groups[0]
    palette = [entry.attrib["color"] for entry in group]
    if not 1 <= len(palette) <= len(CODES):
        raise ValueError("native whole-face export supports 1..16 target colors")
    if any(len(c) not in (7, 9) or c[0] != "#" or (len(c) == 9 and c[7:].upper() != "FF") for c in palette):
        raise ValueError("target colors must be opaque #RRGGBB or #RRGGBBFF")
    palette = [c[:7].upper() for c in palette]
    rgb = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in palette])
    lab = rgb2lab(rgb.astype(float) / 255.0)
    gid = group.attrib["id"]
    counts, approximated = Counter(), 0
    objects = resources.findall(f"{{{CORE}}}object")
    for obj in objects:
        for triangle in obj.iter(f"{{{CORE}}}triangle"):
            if triangle.get("pid", obj.get("pid")) != gid:
                raise ValueError("triangle references an unsupported color group")
            first = triangle.get("p1", obj.get("pindex", "0"))
            corners = [int(first), int(triangle.get("p2", first)), int(triangle.get("p3", first))]
            if min(corners) < 0 or max(corners) >= len(palette):
                raise ValueError("triangle references an invalid target color")
            votes = Counter(corners)
            winner = max(votes.values())
            candidates = [index for index, count in votes.items() if count == winner]
            chosen = min(candidates, key=lambda index: (float(np.square(lab[corners] - lab[index]).sum()), index))
            approximated += len(votes) > 1
            counts[CODES[chosen]] += 1
            for name in ("pid", "p1", "p2", "p3"):
                triangle.attrib.pop(name, None)
            triangle.set("paint_color", CODES[chosen])
        obj.attrib.pop("pid", None)
        obj.attrib.pop("pindex", None)
    if not counts:
        raise ValueError("source contains no colored triangles")
    resources.remove(group)
    root.attrib.pop("requiredextensions", None)
    for entry in list(root):
        if entry.tag == f"{{{CORE}}}metadata" and entry.get("name") in {"Application", "Snapmaker_Orca:3mfVersion"}:
            root.remove(entry)
    # Application marks native format; provenance records this external writer.
    for name, value in (("Application", "Snapmaker_Orca-2.4.1"), ("Snapmaker_Orca:3mfVersion", "1"), ("Designer", "u1_orca_colors external converter"), ("Description", "Logical target colors. Manual Match and fresh slicing REQUIRED. Whole-face color approximation; no mixing recipes.")):
        entry = ET.Element(f"{{{CORE}}}metadata", {"name": name})
        entry.text = value
        root.insert(0, entry)
    for key, value in list(config.items()):
        if key.startswith("filament_") and isinstance(value, list) and len(value) == 1:
            config[key] = value * len(palette)
    config["filament_colour"] = palette
    # Keep machine geometry/tool counts from the template; targets are logical.
    settings = ET.Element("config")
    for obj in objects:
        entry = ET.SubElement(settings, "object", {"id": obj.attrib["id"]})
        ET.SubElement(entry, "metadata", {"key": "name", "value": "Target colors — Manual Match required"})
        ET.SubElement(entry, "metadata", {"key": "extruder", "value": "1"})
        part = ET.SubElement(entry, "part", {"id": obj.attrib["id"], "subtype": "normal_part"})
        # Native Orca parts require this block. No mesh repair occurs here.
        ET.SubElement(part, "mesh_stat", {"edges_fixed": "0", "degenerate_facets": "0", "facets_removed": "0", "facets_reversed": "0", "backwards_edges": "0"})
    ET.register_namespace("", CORE)
    entries = {
        "[Content_Types].xml": TYPES, "_rels/.rels": RELS,
        "3D/3dmodel.model": ET.tostring(root, encoding="utf-8", xml_declaration=True),
        "Metadata/model_settings.config": ET.tostring(settings, encoding="utf-8", xml_declaration=True),
        "Metadata/project_settings.config": json.dumps(config, indent=2).encode(),
    }
    report = {"target_palette": palette, "paint_counts": dict(counts), "triangles": sum(counts.values()), "corner_approximated_triangles": approximated, "requires_manual_match": True, "requires_reslice": True, "native_roundtrip_verified": False, "note": "Whole-face majority colors; ties use a Lab medoid. Palette retained as logical targets, not four physical spool assignments. No stale G-code, slice data or plate references copied."}
    entries["Metadata/u1_target_colors.json"] = json.dumps(report, indent=2).encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for name, data in entries.items():
            archive.writestr(name, data)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--template", type=Path, required=True, help="single-filament native Orca project with no existing mixing definitions; calibrated/multicolor projects require the separate GUI workflow")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = convert(args.input, args.template, args.output)
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
