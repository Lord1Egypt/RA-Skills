"""Guard and real-backend checks using a synthetic painted Bambu cube.

The fixture is constructed here; it is not a user project or a claim of general
MakerWorld compatibility. No printer or slicer is launched by these tests.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("u1_bambu", ROOT / "scripts/u1_bambu.py")
bambu = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bambu)
RUNTIME = ROOT / ".runtime/bambu-to-u1"
REFERENCE = RUNTIME / "profiles/0.20 Standard - Cube.3mf"
CORE = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
MESH_STAT = '<mesh_stat edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>'
RELS = '''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'''
TYPES = '''<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/><Default Extension="config" ContentType="application/octet-stream"/></Types>'''


def synthetic_model(paint="4"):
    vertices = [(0, 0, 0), (20, 0, 0), (20, 20, 0), (0, 20, 0),
                (0, 0, 20), (20, 0, 20), (20, 20, 20), (0, 20, 20)]
    faces = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7),
             (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5),
             (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    xyz = "".join(f'<vertex x="{x}" y="{y}" z="{z}"/>' for x, y, z in vertices)
    triangles = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}" paint_color="{paint if i % 2 == 0 else "8"}"/>' for i, (a, b, c) in enumerate(faces))
    return (f'<model xmlns="{CORE}" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" unit="millimeter" xml:lang="en-US">'
            '<metadata name="Application">BambuStudio-2.3.1</metadata>'
            '<metadata name="BambuStudio:3mfVersion">1</metadata><resources><object id="1" type="model"><mesh><vertices>'
            + xyz + '</vertices><triangles>' + triangles
            + '</triangles></mesh></object></resources><build><item objectid="1" transform="1 0 0 0 1 0 0 0 1 128 128 0"/></build></model>')


def synthetic_project(path, *, paint="4", layer_xml=None, extras=None):
    config = {
        "printer_model": "Bambu Lab X1 Carbon", "printer_settings_id": "Bambu Lab X1 Carbon 0.4 nozzle",
        "gcode_flavor": "marlin", "nozzle_diameter": ["0.4"],
        "printable_area": ["0x0", "256x0", "256x256", "0x256"], "printable_height": "256",
        "print_settings_id": "SYNTHETIC 0.20 Standard", "layer_height": "0.2",
        "filament_settings_id": ["SYNTHETIC PLA RED", "SYNTHETIC PLA WHITE"],
        "filament_type": ["PLA", "PLA"], "filament_vendor": ["Generic", "Generic"],
        "filament_colour": ["#FF0000", "#FFFFFF"], "nozzle_temperature": ["210", "215"],
        "machine_start_gcode": "M620 S1 ; SOURCE_MACHINE_ONLY", "machine_end_gcode": "M621 S1 ; SOURCE_MACHINE_ONLY",
        "filament_start_gcode": ["M620 S1", "M620 S2"], "filament_end_gcode": ["M621 S1", "M621 S2"],
        "change_extrusion_role_gcode": "M620 SOURCE_ROLE_ONLY", "post_process": "SOURCE_SCRIPT_SHOULD_NOT_RUN",
    }
    metadata = ('<config><object id="1"><metadata key="name" value="SYNTHETIC painted cube"/>'
                '<metadata key="extruder" value="1"/><metadata key="wall_filament" value="2"/>'
                '<part id="1" subtype="normal_part"><metadata key="extruder" value="2"/>' + MESH_STAT + '</part></object>'
                '<plate><metadata key="plater_id" value="1"/><metadata key="filament_maps" value="1 2"/>'
                '<model_instance><metadata key="object_id" value="1"/><metadata key="instance_id" value="0"/>'
                '<metadata key="identify_id" value="0"/></model_instance></plate></config>')
    entries = {"[Content_Types].xml": TYPES, "_rels/.rels": RELS,
               "3D/3dmodel.model": synthetic_model(paint), bambu.SETTINGS: json.dumps(config),
               "Metadata/model_settings.config": metadata,
               "Metadata/slice_info.config": '<config><plate><metadata key="index" value="1"/><metadata key="printer_model_id" value="Bambu Lab X1 Carbon"/></plate></config>',
               "Metadata/plate_1.gcode": "M620 SOURCE_CACHE_ONLY\nG1 X0 Y0 E1\n",
               "Metadata/plate_1.gcode.md5": "SYNTHETIC_NOT_A_CHECKSUM",
               "Metadata/Plate_2.GCODE": "SOURCE_NONCANONICAL_CACHE_ONLY",
               "Metadata/plate_1.json": json.dumps({"bed_type": "Textured PEI Plate", "is_seq_print": False})}
    if layer_xml is not None:
        entries[bambu.LAYER_COMMANDS] = layer_xml
    entries.update(extras or {})
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, value in entries.items():
            archive.writestr(name, value)
    return path


def replace_members(path, replacements):
    """Alter only our generated fixture archive for focused regression cases."""
    with zipfile.ZipFile(path) as archive:
        entries = {name: archive.read(name) for name in archive.namelist()}
    entries.update(replacements)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in entries.items():
            archive.writestr(name, data)


class BambuAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_slot_map_requires_complete_distinct_physical_tools(self):
        self.assertEqual(bambu.parse_slot_map(None, 2), {0: 0, 1: 1})
        self.assertEqual(bambu.parse_slot_map("1:4,2:2", 2), {0: 3, 1: 1})
        for mapping, count in [(None, 0), (None, 5), ("1:1", 2), ("1:1,2:1", 2),
                               ("1:1,1:2", 2), ("1:0", 1), ("1:5", 1),
                               ("2:1", 1), ("bad", 1), ("1:1,", 1)]:
            with self.subTest(mapping=mapping, count=count), self.assertRaises(bambu.ConversionError):
                bambu.parse_slot_map(mapping, count)

    def test_paint_tree_decoder_handles_splits_and_rejects_incomplete_data(self):
        self.assertEqual(bambu.paint_states("4"), [1])
        self.assertEqual(bambu.paint_states("8"), [2])
        self.assertEqual(bambu.paint_states("0C"), [3])
        self.assertEqual(bambu.paint_states("1C"), [4])
        self.assertEqual(bambu.paint_states("481"), [2, 1])
        for paint in ["C", "1", "44", "G", "1C4"]:
            with self.subTest(paint=paint), self.assertRaises(bambu.ConversionError):
                bambu.paint_states(paint)

    def test_archive_counts_editable_geometry_and_detects_virtual_paint(self):
        source = synthetic_project(self.root / "synthetic.3mf")
        info = bambu.archive_info(source, 2)["models"]["3D/3dmodel.model"]
        self.assertEqual((info["vertices"], info["triangles"], info["painted_triangles"]), (8, 12, 12))
        self.assertEqual(info["unit"], "millimeter")
        self.assertEqual(len(info["geometry_sha256"]), 64)
        synthetic_project(source, paint="2C")
        with self.assertRaisesRegex(bambu.ConversionError, "virtual/out-of-range"):
            bambu.archive_info(source, 4)

    def test_build_instance_audit_allows_xy_translation_without_changing_shape(self):
        before = [{"objectid": "1", "printable": "1", "transform": "1 0 0 0 1 0 0 0 1 128 128 0"}]
        shifted = [{"objectid": "1", "printable": "1", "transform": "1 0 0 0 1 0 0 0 1 135 135 0"}]
        bambu.audit_build_items(before, shifted)
        bambu.audit_build_items([{"objectid": "1"}], [{"objectid": "1", "transform": "1 0 0 0 1 0 0 0 1 0 0 0"}])
        bad = [[], [{"objectid": "2", "printable": "1", "transform": before[0]["transform"]}],
               [{"objectid": "1", "printable": "0", "transform": before[0]["transform"]}]]
        for replacement in bad:
            with self.subTest(replacement=replacement), self.assertRaises(bambu.ConversionError):
                bambu.audit_build_items(before, replacement)
        for transform in ["2 0 0 0 1 0 0 0 1 128 128 0", "0 1 0 -1 0 0 0 0 1 128 128 0",
                          "1 0 0 0 1 0 0 0 1 128 128 1", "1 0 0 0 1 0 0 0 1 nan 128 0", "1 0 0"]:
            with self.subTest(transform=transform), self.assertRaises(bambu.ConversionError):
                bambu.audit_build_items(before, [{"objectid": "1", "printable": "1", "transform": transform}])

    def test_archive_rejects_unsafe_ambiguous_and_gcode_only_inputs(self):
        for name in ["../escape.txt", "/absolute.txt", "Metadata\\bad.txt"]:
            with self.subTest(name=name):
                path = synthetic_project(self.root / "unsafe.3mf", extras={name: "x"})
                with self.assertRaises(bambu.ConversionError):
                    bambu.archive_info(path)
        duplicate = synthetic_project(self.root / "ambiguous.3mf", extras={"3d/3DMODEL.MODEL": synthetic_model()})
        with self.assertRaisesRegex(bambu.ConversionError, "Duplicate"):
            bambu.archive_info(duplicate)
        sliced = self.root / "sliced.gcode.3mf"
        with zipfile.ZipFile(sliced, "w") as archive:
            archive.writestr("Metadata/plate_1.gcode", "G1 X1 Y1 E1")
        with self.assertRaisesRegex(bambu.ConversionError, "original project"):
            bambu.archive_info(sliced)

    def test_xml_entities_and_malformed_xml_are_rejected(self):
        for xml in [b'<root>', b'<!DOCTYPE root [<!ENTITY x "test">]><root>&x;</root>']:
            with self.subTest(xml=xml), self.assertRaises(bambu.ConversionError):
                bambu.xml_root(xml, "fixture.xml")

    def test_part_without_mesh_statistics_rejected_before_native_import(self):
        source = synthetic_project(self.root / "synthetic-missing-mesh-stat.3mf")
        # A supported part includes native importer mesh-stat fields. Omitting
        # them caused std::bad_alloc in the actual Snapmaker Orca import smoke.
        bambu.slot_references(source, 2)
        with zipfile.ZipFile(source) as archive:
            metadata = archive.read("Metadata/model_settings.config").replace(MESH_STAT.encode(), b"")
        replace_members(source, {"Metadata/model_settings.config": metadata})
        with self.assertRaisesRegex(bambu.ConversionError, "mesh_stat"):
            bambu.slot_references(source, 2)

    def test_layer_pauses_replaced_and_toolchange_script_cleared(self):
        xml = b'<custom_gcodes_per_layer><mode value="MultiExtruder"/><layer top_z="1.2" type="1" extruder="0" gcode="M620"/><layer top_z="2" type="2" extruder="2" gcode="M620"/></custom_gcodes_per_layer>'
        output = bambu.sanitize_layers(xml, {"machine_pause_gcode": "M600"}, {0: 1, 1: 0}, already_mapped=False)
        layers = ET.fromstring(output).findall("layer")
        self.assertEqual([layer.get("gcode") for layer in layers], ["M600", ""])
        self.assertEqual(layers[1].get("extruder"), "2")
        with self.assertRaisesRegex(bambu.ConversionError, "unmapped"):
            bambu.sanitize_layers(xml.replace(b'extruder="2"', b'extruder="4"'), {"machine_pause_gcode": "M600"}, {0: 0, 1: 1}, already_mapped=False)

    def test_layer_custom_scripts_unknown_tags_and_invalid_heights_rejected(self):
        bad = [b'<custom_gcodes_per_layer><layer top_z="1" type="4" gcode="M620"/></custom_gcodes_per_layer>',
               b'<custom_gcodes_per_layer><script>M620</script></custom_gcodes_per_layer>',
               b'<custom_gcodes_per_layer><layer top_z="nan" type="1"/></custom_gcodes_per_layer>',
               b'<custom_gcodes_per_layer><layer top_z="-1" type="1"/></custom_gcodes_per_layer>',
               b'<custom_gcodes_per_layer><layer top_z="1" type="2" extruder="bad"/></custom_gcodes_per_layer>',
               b'<custom_gcodes_per_layer>']
        for xml in bad:
            with self.subTest(xml=xml), self.assertRaises(bambu.ConversionError):
                bambu.sanitize_layers(xml, {"machine_pause_gcode": "M600"}, {0: 0}, already_mapped=False)

    def test_sanitize_clears_source_hooks_presets_postprocessors_and_caches(self):
        source = synthetic_project(self.root / "raw.3mf", extras={"Metadata/machine_settings_8.config": '{"machine_start_gcode":"M620"}', "Metadata/foreign.bgcode": "BINARY_CACHE"})
        output = self.root / "sanitized.3mf"
        reference = {"gcode_flavor": "klipper", "machine_start_gcode": "PRINT_START", "machine_end_gcode": "PRINT_END",
                     "filament_start_gcode": ["REFERENCE_DEMO_SPOOL"], "filament_end_gcode": ["REFERENCE_DEMO_SPOOL"],
                     "change_extrusion_role_gcode": ""}
        changes = bambu.sanitize_project(source, output, reference, {0: 0, 1: 1}, {"sha256": "a" * 64})
        with zipfile.ZipFile(output) as archive:
            cfg = json.loads(archive.read(bambu.SETTINGS))
            marker = json.loads(archive.read(bambu.MARKER))
            self.assertEqual(cfg["gcode_flavor"], "klipper")
            self.assertEqual(cfg["machine_start_gcode"], "PRINT_START")
            self.assertEqual(cfg["filament_start_gcode"], [""] * 4)
            self.assertEqual(cfg["filament_end_gcode"], [""] * 4)
            self.assertEqual(cfg["change_extrusion_role_gcode"], "")
            self.assertNotIn("post_process", cfg)
            self.assertTrue(marker["requires_manual_review"])
            self.assertTrue(marker["requires_reslice"])
            self.assertFalse(marker["ready_to_print"])
            self.assertFalse(any(".gcode" in name.lower() or ".bgcode" in name.lower() for name in archive.namelist()))
            self.assertNotIn("Metadata/machine_settings_8.config", archive.namelist())
        self.assertIn("post_process", changes["removed_post_process"])
        self.assertEqual(bambu.archive_info(source, 2)["models"], bambu.archive_info(output, 2)["models"])

    def test_model_metadata_cleanup_preserves_undeclared_extension_markup(self):
        # Orca accepts literal extension names that lack namespace declarations.
        extension = b'<slic3rpe:text text="x"/>'
        source = (b'<config>\n<object id="1">' + extension
                  + b'<metadata key="machine_start_gcode" value="M620"/>'
                  + b'<metadata key="filament_end_gcode" value="M621">source</metadata>'
                  + b'<metadata key="name" value="keep &amp; preserve"/>'
                  + b'</object><plate><metadata key="filament_maps" value="2 1"/></plate></config>')
        cleaned, removed = bambu.sanitize_model_settings(source)
        expected = (b'<config>\n<object id="1">' + extension
                    + b'<metadata key="name" value="keep &amp; preserve"/>'
                    + b'</object><plate><metadata key="filament_maps" value="1 2 3 4"/></plate></config>')
        self.assertEqual(cleaned, expected)
        self.assertEqual(set(removed), {"machine_start_gcode", "filament_end_gcode"})

    def test_machine_limits_and_identity_come_from_target_reference(self):
        source = synthetic_project(self.root / "raw.3mf")
        with zipfile.ZipFile(source) as archive:
            cfg = json.loads(archive.read(bambu.SETTINGS))
        cfg.update(machine_max_speed_x=["9999"], machine_max_acceleration_x=["999999"],
                   machine_foreign_option="do not retain", printer_foreign_option="do not retain")
        replace_members(source, {bambu.SETTINGS: json.dumps(cfg)})
        reference = {"gcode_flavor": "klipper", "printer_model": "Snapmaker U1",
                     "machine_max_speed_x": ["500"], "machine_max_acceleration_x": ["10000"]}
        output = self.root / "hardware.3mf"
        changes = bambu.sanitize_project(source, output, reference, {0: 0, 1: 1}, {"sha256": "a" * 64})
        with zipfile.ZipFile(output) as archive:
            final = json.loads(archive.read(bambu.SETTINGS))
        self.assertEqual(final["machine_max_speed_x"], ["500"])
        self.assertEqual(final["machine_max_acceleration_x"], ["10000"])
        self.assertEqual(final["printer_model"], "Snapmaker U1")
        self.assertNotIn("machine_foreign_option", final)
        self.assertNotIn("printer_foreign_option", final)
        self.assertIn("machine_max_speed_x", changes["target_hardware"])

    def test_existing_output_and_source_are_never_overwritten(self):
        source = synthetic_project(self.root / "original.3mf")
        reference = synthetic_project(self.root / "reference.3mf")
        destination = self.root / "already-exists"
        destination.mkdir()
        (destination / "keep.txt").write_text("preserve")
        old = source.read_bytes()
        with mock.patch.object(bambu, "verify_runtime"), mock.patch.object(bambu, "call_worker") as worker:
            with self.assertRaises(FileExistsError):
                bambu.convert_project(source, destination, RUNTIME, reference=reference)
            worker.assert_not_called()
        self.assertEqual(source.read_bytes(), old)
        self.assertEqual((destination / "keep.txt").read_text(), "preserve")

    def test_failed_worker_leaves_report_without_deliverable(self):
        source = synthetic_project(self.root / "source.3mf")
        reference = synthetic_project(self.root / "reference.3mf")
        destination = self.root / "failed-job"
        def fail(*args):
            (destination / "converted.3mf").write_text("should be removed")
            (destination / "backend-output.3mf").write_text("should be removed")
            raise bambu.ConversionError("synthetic audit failure")
        with mock.patch.object(bambu, "verify_runtime"), mock.patch.object(bambu, "call_worker", side_effect=fail):
            with self.assertRaisesRegex(bambu.ConversionError, "synthetic audit failure"):
                bambu.convert_project(source, destination, RUNTIME, reference=reference)
        report = json.loads((destination / "report.json").read_text())
        self.assertEqual(report["status"], "conversion_failed")
        self.assertFalse(report["ready_to_print"])
        self.assertFalse((destination / "converted.3mf").exists())
        self.assertFalse((destination / "backend-output.3mf").exists())
        self.assertEqual((destination / "input/source.3mf").read_bytes(), source.read_bytes())

    @unittest.skipUnless((RUNTIME / ".venv/bin/python").is_file() and REFERENCE.is_file(), "optional pinned local backend not installed")
    def test_actual_backend_preserves_synthetic_geometry_and_remaps_paint(self):
        source = synthetic_project(self.root / "synthetic-bambu.3mf")
        old_bytes = source.read_bytes()
        old_hash = bambu.digest(source)
        report = bambu.convert_project(source, self.root / "real-backend-job", RUNTIME, reference=REFERENCE, slot_map="1:2,2:1")
        self.assertEqual(source.read_bytes(), old_bytes)
        self.assertEqual(report["input"]["sha256"], old_hash)
        self.assertEqual(Path(report["input"]["preserved_path"]).read_bytes(), old_bytes)
        self.assertTrue(report["geometry_and_paint_invariants_passed"])
        self.assertEqual(report["slot_map_one_based"], {"1": 2, "2": 1})
        self.assertEqual(report["status"], "converted_review_required")
        self.assertFalse(report["ready_to_print"])
        self.assertFalse(report["slice_completed"])
        self.assertFalse(report["full_spectrum_assigned"])
        output = Path(report["artifacts"]["project"])
        info = bambu.archive_info(output, 4)["models"]["3D/3dmodel.model"]
        self.assertEqual((info["vertices"], info["triangles"]), (8, 12))
        self.assertEqual(info["paint_values"], ["8", "4"] * 6)
        with zipfile.ZipFile(output) as archive:
            cfg = json.loads(archive.read(bambu.SETTINGS))
            model_metadata = ET.fromstring(archive.read("Metadata/model_settings.config"))
            marker = json.loads(archive.read(bambu.MARKER))
            self.assertEqual(cfg["printer_model"], "Snapmaker U1")
            self.assertEqual(cfg["gcode_flavor"], "klipper")
            self.assertEqual(len(cfg["filament_settings_id"]), 4)
            self.assertEqual(cfg["filament_colour"][:2], ["#FFFFFF", "#FF0000"])
            self.assertEqual(cfg["filament_start_gcode"], [""] * 4)
            self.assertEqual(cfg["filament_end_gcode"], [""] * 4)
            self.assertNotIn("SOURCE_MACHINE_ONLY", cfg["machine_start_gcode"])
            self.assertNotIn("post_process", cfg)
            self.assertTrue(marker["requires_manual_review"])
            self.assertFalse(any(".gcode" in name.lower() for name in archive.namelist()))
            self.assertEqual(model_metadata.find('./object/metadata[@key="extruder"]').get("value"), "2")
            self.assertEqual(model_metadata.find('./object/metadata[@key="wall_filament"]').get("value"), "1")
            self.assertEqual(model_metadata.find('./plate/metadata[@key="filament_maps"]').get("value"), "1 2 3 4")

    @unittest.skipUnless((RUNTIME / ".venv/bin/python").is_file() and REFERENCE.is_file(), "optional pinned local backend not installed")
    def test_actual_backend_sparse_assignment_routes_single_color_to_tool_four(self):
        source = synthetic_project(self.root / "synthetic-one-color.3mf")
        with zipfile.ZipFile(source) as archive:
            cfg = json.loads(archive.read(bambu.SETTINGS))
            model = archive.read("3D/3dmodel.model").replace(b'paint_color="8"', b'paint_color="4"')
            metadata = archive.read("Metadata/model_settings.config").replace(b'value="2"', b'value="1"')
        for key, value in cfg.items():
            if isinstance(value, list) and len(value) == 2:
                cfg[key] = value[:1]
        replace_members(source, {bambu.SETTINGS: json.dumps(cfg), "3D/3dmodel.model": model, "Metadata/model_settings.config": metadata})
        report = bambu.convert_project(source, self.root / "sparse-job", RUNTIME, reference=REFERENCE, slot_map="1:4")
        self.assertEqual(report["slot_map_one_based"], {"1": 4})
        output = Path(report["artifacts"]["project"])
        info = bambu.archive_info(output, 4)["models"]["3D/3dmodel.model"]
        self.assertEqual(info["paint_values"], ["1C"] * 12)
        self.assertTrue(all(number == 4 for _, number in report["output_slot_references"]["objects"]))
        self.assertFalse(report["ready_to_print"])

    @unittest.skipUnless((RUNTIME / ".venv/bin/python").is_file() and REFERENCE.is_file(), "optional pinned local backend not installed")
    def test_actual_backend_plate_wrapped_pause_and_toolchange_preserved(self):
        layers = ('<custom_gcodes_per_layer><plate id="1"><mode value="MultiExtruder"/>'
                  '<layer top_z="1" type="1" extruder="0" gcode="M620 SOURCE_PAUSE"/>'
                  '<layer top_z="2" type="2" extruder="2" gcode="M620 SOURCE_TOOLCHANGE"/>'
                  '</plate></custom_gcodes_per_layer>')
        source = synthetic_project(self.root / "synthetic-layer-events.3mf", layer_xml=layers)
        report = bambu.convert_project(source, self.root / "layer-events-job", RUNTIME, reference=REFERENCE, slot_map="1:2,2:1")
        with zipfile.ZipFile(report["artifacts"]["project"]) as archive:
            events = ET.fromstring(archive.read(bambu.LAYER_COMMANDS)).findall("./plate/layer")
        self.assertEqual(events[0].get("gcode"), "M600")
        self.assertEqual(events[1].get("gcode"), "")
        self.assertEqual(events[1].get("extruder"), "1")
        self.assertFalse(report["ready_to_print"])

    @unittest.skipUnless((RUNTIME / ".venv/bin/python").is_file() and REFERENCE.is_file(), "optional pinned local backend not installed")
    def test_out_of_range_object_extruder_rejected_without_changing_source(self):
        source = synthetic_project(self.root / "synthetic-invalid-extruder.3mf")
        with zipfile.ZipFile(source) as archive:
            metadata = archive.read("Metadata/model_settings.config").replace(b'key="extruder" value="1"', b'key="extruder" value="5"')
        replace_members(source, {"Metadata/model_settings.config": metadata})
        original = source.read_bytes()
        output = self.root / "invalid-extruder-job"
        with self.assertRaisesRegex(bambu.ConversionError, "out-of-range filament assignment"):
            bambu.convert_project(source, output, RUNTIME, reference=REFERENCE)
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual((output / "input/source.3mf").read_bytes(), original)
        self.assertFalse((output / "converted.3mf").exists())
        self.assertEqual(json.loads((output / "report.json").read_text())["status"], "conversion_failed")

    @unittest.skipUnless((RUNTIME / ".venv/bin/python").is_file() and REFERENCE.is_file(), "optional pinned local backend not installed")
    def test_variable_layer_range_configs_rejected_for_manual_review(self):
        for member in ["Metadata/layer_config_ranges.xml", "Metadata/layer_heights_profile.txt"]:
            with self.subTest(member=member):
                index = member.rsplit("/", 1)[-1]
                source = synthetic_project(self.root / (index + ".3mf"), extras={member: "<synthetic/>"})
                original = source.read_bytes()
                output = self.root / (index + "-job")
                with self.assertRaisesRegex(bambu.ConversionError, "Variable-layer/range overrides"):
                    bambu.convert_project(source, output, RUNTIME, reference=REFERENCE)
                self.assertEqual(source.read_bytes(), original)
                self.assertFalse((output / "converted.3mf").exists())


if __name__ == "__main__":
    unittest.main()
