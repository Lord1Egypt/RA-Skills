"""Test profile resolution and adapter contracts without launching Orca."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "u1_slice.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("u1_slice", SCRIPT)
slicer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(slicer)


class SliceAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load font discovery before mocking the slicer's shared subprocess module.
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib import pyplot

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.vendor = self.root / "profiles"
        for kind in ["machine", "process", "filament"]:
            (self.vendor / kind).mkdir(parents=True)
        self.app = self.root / "Snapmaker Orca.app"
        binary = self.app / "Contents" / "MacOS" / "Snapmaker_Orca"
        binary.parent.mkdir(parents=True)
        binary.touch()
        self.source = self.root / "mesh.stl"
        self.source.write_text("fixture; subprocess is mocked")
        self.write("machine", "parent-machine", nozzle_diameter=["0.4"] * 4, printable_height="270.05", printable_area=["0x0", "270x0", "270x270", "0x270"])
        self.write("machine", slicer.MACHINE_NAME, inherits="parent-machine", instantiation="true", name=slicer.MACHINE_NAME)
        self.write("process", "parent-process", sparse_infill_density="15%", wall_loops="2", wipe_tower_filament="0", enable_prime_tower="1")
        for name in {*slicer.INTENT_PRESETS.values(), slicer.MIXING_PRESET}:
            self.write("process", name, inherits="parent-process", instantiation="true", name=name, compatible_printers=[slicer.MACHINE_NAME], process_flow_support=["standard", "high_flow"], outer_wall_speed=["200", "500"])
        self.write("filament", "Generic PLA", instantiation="true", name="Generic PLA", filament_type=["PLA"], compatible_printers=[slicer.MACHINE_NAME], filament_flow_support=["standard"], filament_max_volumetric_speed=["12"])

    def write(self, kind, preset_name, **values):
        data = {"type": kind, "from": "system", **values}
        (self.vendor / kind / f"{preset_name}.json").write_text(json.dumps(data), encoding="utf-8-sig")

    def test_unmatched_target_colors_cannot_be_sliced_as_one_filament(self):
        source = self.root / "unmatched.3mf"
        with zipfile.ZipFile(source, "w") as archive:
            archive.writestr("Metadata/u1_target_colors.json", json.dumps({"requires_manual_match": True}))
        with mock.patch.object(slicer.subprocess, "run") as run:
            with self.assertRaisesRegex(slicer.SliceError, "Manual Match"):
                slicer.slice_model(source, self.root / "out", app_path=self.app, profiles_dir=self.vendor)
            run.assert_not_called()
        self.assertFalse((self.root / "out").exists())

    def test_converted_project_cannot_have_assignments_overridden(self):
        source = self.root / "converted.3mf"
        with zipfile.ZipFile(source, "w") as archive:
            archive.writestr("Metadata/u1_conversion.json", json.dumps({"requires_manual_review": True}))
        with mock.patch.object(slicer.subprocess, "run") as run:
            with self.assertRaisesRegex(slicer.SliceError, "as a project"):
                slicer.slice_model(source, self.root / "out", app_path=self.app, profiles_dir=self.vendor)
            run.assert_not_called()
        self.assertFalse((self.root / "out").exists())

    def test_native_multi_or_mixed_project_is_protected_without_marker(self):
        for settings in [{"filament_settings_id": ["white", "red"]}, {"filament_settings_id": ["white"], "filament_colour": ["#FFFFFF", "#FF0000"]}, {"filament_settings_id": ["white"], "mixed_filament_definitions": "existing-native-recipe"}]:
            source = self.root / "native-calibrated.3mf"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("Metadata/project_settings.config", json.dumps(settings))
            with mock.patch.object(slicer.subprocess, "run") as run:
                with self.assertRaisesRegex(slicer.SliceError, "native Orca project"):
                    slicer.slice_model(source, self.root / "out", app_path=self.app, profiles_dir=self.vendor)
                run.assert_not_called()
            self.assertFalse((self.root / "out").exists())

    def test_generic_two_color_3mf_is_rejected_before_output_or_execution(self):
        # The generic color exporter uses this Materials-extension structure,
        # without Orca project settings or the native unmatched-target marker.
        source = self.root / "generic-color-regions.3mf"
        model = '''<model xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
            xmlns:m="http://schemas.microsoft.com/3dmanufacturing/material/2015/02" requiredextensions="m">
            <resources><m:colorgroup id="1"><m:color color="#FF0000FF"/><m:color color="#FFFFFFFF"/></m:colorgroup>
            <object id="2"><mesh><vertices><vertex x="0" y="0" z="0"/><vertex x="1" y="0" z="0"/>
            <vertex x="0" y="1" z="1"/></vertices><triangles>
            <triangle v1="0" v2="1" v3="2" pid="1" p1="0" p2="1" p3="0"/>
            </triangles></mesh></object></resources><build><item objectid="2"/></build></model>'''
        with zipfile.ZipFile(source, "w") as archive:
            archive.writestr("3D/3dmodel.model", model)
        original = source.read_bytes()
        with mock.patch.object(slicer.subprocess, "run") as run:
            with self.assertRaisesRegex(slicer.SliceError, "color workflow"):
                slicer.slice_model(source, self.root / "out", app_path=self.app, profiles_dir=self.vendor)
            run.assert_not_called()
        self.assertFalse((self.root / "out").exists())
        self.assertEqual(source.read_bytes(), original)

    def test_unknown_embedded_filament_settings_are_not_assumed_monochrome(self):
        for settings in [{}, {"filament_settings_id": []}, {"filament_settings_id": "PLA"}, {"filament_settings_id": [""]}]:
            with self.subTest(settings=settings):
                source = self.root / "unknown-project.3mf"
                with zipfile.ZipFile(source, "w") as archive:
                    archive.writestr("Metadata/project_settings.config", json.dumps(settings))
                with mock.patch.object(slicer.subprocess, "run") as run:
                    with self.assertRaisesRegex(slicer.SliceError, "unrecognized 3MF"):
                        slicer.slice_model(source, self.root / "out", app_path=self.app, profiles_dir=self.vendor)
                    run.assert_not_called()
                self.assertFalse((self.root / "out").exists())

    def test_identified_single_filament_native_project_can_still_be_prepared(self):
        source = self.root / "single-filament-native.3mf"
        with zipfile.ZipFile(source, "w") as archive:
            archive.writestr("Metadata/project_settings.config", json.dumps({"filament_settings_id": ["PLA"], "filament_colour": ["#FFFFFF"], "mixed_filament_definitions": ""}))
        with mock.patch.object(slicer.subprocess, "run") as run:
            report = slicer.slice_model(source, self.root / "out", app_path=self.app, profiles_dir=self.vendor, dry_run=True)
            run.assert_not_called()
        self.assertEqual(report["status"], "prepared_not_executed")
        self.assertFalse(report["slice_completed"])

    def test_invalid_3mf_archive_fails_before_output_or_execution(self):
        source = self.root / "invalid.3mf"
        source.write_bytes(b"not a 3MF archive")
        with mock.patch.object(slicer.subprocess, "run") as run:
            with self.assertRaisesRegex(slicer.SliceError, "valid project archive"):
                slicer.slice_model(source, self.root / "out", app_path=self.app, profiles_dir=self.vendor)
            run.assert_not_called()
        self.assertFalse((self.root / "out").exists())

    def test_inheritance_is_flattened_with_provenance(self):
        preset, sources = slicer.resolve_preset(self.vendor, "machine", slicer.MACHINE_NAME)
        self.assertEqual(preset["printable_height"], "270.05")
        self.assertNotIn("inherits", preset)
        self.assertEqual(len(sources), 2)
        self.assertTrue(all(len(item["sha256"]) == 64 for item in sources))

    def test_cycles_missing_parents_and_bad_types_are_rejected(self):
        self.write("process", "a", inherits="b")
        self.write("process", "b", inherits="a")
        with self.assertRaisesRegex(slicer.SliceError, "cyclic"):
            slicer.resolve_preset(self.vendor, "process", "a")
        self.write("process", "b", inherits="missing")
        with self.assertRaisesRegex(slicer.SliceError, "cannot read"):
            slicer.resolve_preset(self.vendor, "process", "a")
        self.write("process", "bad", wall_loops=3)
        with self.assertRaisesRegex(slicer.SliceError, "string"):
            slicer.resolve_preset(self.vendor, "process", "bad")
        self.write("process", "wrong", type="filament")
        with self.assertRaisesRegex(slicer.SliceError, "expected type"):
            slicer.resolve_preset(self.vendor, "process", "wrong")

    def test_standard_flow_and_precise_crash_workaround(self):
        presets, selection = slicer.prepare_profiles(self.vendor, intent="strong")
        process = presets["process"]
        self.assertEqual(process["outer_wall_speed"], "200")
        self.assertEqual(process["nozzle_diameter"], presets["machine"]["nozzle_diameter"])
        self.assertEqual(process["wipe_tower_filament"], "0")
        self.assertEqual(process["enable_prime_tower"], "1")
        self.assertEqual(process["wall_loops"], "4")
        self.assertEqual(process["sparse_infill_density"], "25%")
        self.assertEqual(process["enable_support"], "1")
        self.assertEqual(process["support_type"], "tree(auto)")
        off, _ = slicer.prepare_profiles(self.vendor, supports="off")
        self.assertEqual(off["process"]["enable_support"], "0")
        self.assertNotIn("process_flow_support", process)
        self.assertIn("561", selection["crash_reference"])

    def test_mixing_selects_dedicated_profile_without_assigning_ratios(self):
        presets, selection = slicer.prepare_profiles(self.vendor, mixing=True)
        self.assertEqual(presets["process"]["name"], slicer.MIXING_PRESET)
        self.assertTrue(selection["mixing"]["dedicated_preset_selected"])
        self.assertFalse(selection["mixing"]["ratios_assigned"])

    def test_command_is_local_argument_vector_and_isolated(self):
        run_dir = self.root / "out with spaces"
        command = slicer.build_command(self.app / "Contents/MacOS/Snapmaker_Orca", self.source, run_dir)
        self.assertEqual(command[command.index("--datadir") + 1], str(run_dir.resolve() / "datadir"))
        self.assertEqual(command[command.index("--slice") + 1], "1")
        self.assertIn("--export-3mf", command)
        # Actual Snapmaker Orca CLI concatenates outputdir + '/' + export name.
        # An absolute export name produced run_0001//absolute/path/project.3mf.tmp.
        export_name = command[command.index("--export-3mf") + 1]
        output_dir = command[command.index("--outputdir") + 1]
        self.assertEqual(export_name, "project.3mf")
        self.assertFalse(Path(export_name).is_absolute())
        self.assertEqual(str(output_dir) + "/" + export_name, str(run_dir.resolve() / "project.3mf"))
        self.assertIn("--load-filaments", command)
        self.assertFalse(any("upload" in item or "send" in item or "print-host" in item for item in command))
        self.assertEqual(command[-1], str(self.source.resolve()))

    def test_dry_run_does_not_launch_and_does_not_claim_success(self):
        with mock.patch.object(slicer.subprocess, "run") as run:
            report = slicer.slice_model(self.source, self.root / "out", app_path=self.app, profiles_dir=self.vendor, dry_run=True)
        run.assert_not_called()
        self.assertFalse(report["slice_completed"])
        self.assertFalse(report["slicing_verified"])
        self.assertEqual(report["status"], "prepared_not_executed")
        self.assertEqual(json.loads(Path(report["artifacts"]["report"]).read_text()), report)

    def test_success_requires_real_gcode_and_still_requires_review(self):
        def execute(argv, **kwargs):
            directory = Path(kwargs["cwd"])
            code = "; filament used [g] = 2.5, 0\n; filament used [mm] = 822.4, 0\n; estimated printing time (normal mode) = 1h 2m 3s\nG90\nM83\nG0 X1 Y1 Z0.2\nG1 X2 Y1 E0.5\n"
            with zipfile.ZipFile(directory / "project.3mf", "w") as archive:
                archive.writestr("Metadata/plate_1.gcode", code)
            return subprocess.CompletedProcess(argv, 0)
        with mock.patch.object(slicer.subprocess, "run", side_effect=execute) as run:
            report = slicer.slice_model(self.source, self.root / "out", app_path=self.app, profiles_dir=self.vendor)
        self.assertTrue(report["slice_completed"])
        self.assertTrue(report["toolpath_validation_passed"])
        self.assertTrue(report["toolpath_previews_generated"])
        self.assertFalse(report["slicing_verified"])
        self.assertFalse(report["ready_to_print"])
        estimates = report["artifacts"]["gcode"][0]["estimates"]
        self.assertEqual(estimates["filament_grams_by_tool"], [2.5, 0])
        self.assertEqual(estimates["estimated_duration_seconds"], 3723)
        self.assertNotIn("shell", run.call_args.kwargs)
        self.assertEqual(run.call_args.kwargs["timeout"], 600)

    def test_failed_exit_preserves_transcript_and_new_run_ignores_stale_output(self):
        def failure(argv, **kwargs):
            kwargs["stdout"].write("[error] process preset not compatible\n")
            return subprocess.CompletedProcess(argv, -11)
        with mock.patch.object(slicer.subprocess, "run", side_effect=failure):
            first = slicer.slice_model(self.source, self.root / "out", app_path=self.app, profiles_dir=self.vendor)
            second = slicer.slice_model(self.source, self.root / "out", app_path=self.app, profiles_dir=self.vendor)
        self.assertEqual(first["status"], "slice_failed")
        self.assertEqual(first["execution"]["return_code"], -11)
        self.assertIn("not compatible", Path(first["artifacts"]["transcript"]).read_text())
        self.assertNotEqual(first["execution"]["run_dir"], second["execution"]["run_dir"])
        self.assertTrue(Path(first["artifacts"]["report"]).is_file())

    def test_zero_exit_with_out_of_bounds_or_unsupported_paths_fails_review(self):
        for tail in ['G1 X271 E1', 'G20\nG1 X3 E1']:
            def execute(argv, **kwargs):
                directory = Path(kwargs['cwd'])
                code = 'M83\nG0 X1 Y1 Z1\n' + tail
                (directory / 'plate_1.gcode').write_text(code)
                with zipfile.ZipFile(directory / 'project.3mf', 'w') as archive:
                    archive.writestr('Metadata/plate_1.gcode', code)
                return subprocess.CompletedProcess(argv, 0)
            with self.subTest(tail=tail), mock.patch.object(slicer.subprocess, 'run', side_effect=execute):
                report = slicer.slice_model(self.source, self.root / 'out', app_path=self.app, profiles_dir=self.vendor)
            self.assertTrue(report['slicer_output_completed'])
            self.assertFalse(report['slice_completed'])
            self.assertFalse(report['toolpath_validation_passed'])
            self.assertEqual(report['status'], 'toolpath_review_failed')
            artifacts = report['artifacts']['gcode']
            self.assertEqual(len(artifacts), 2)
            self.assertEqual(artifacts[0]['toolpath_review'], artifacts[1]['toolpath_review'])
            self.assertEqual(len(list(Path(report['execution']['run_dir']).glob('toolpaths_*'))), 1)

    def test_missing_printable_region_fails_before_execution_or_output(self):
        self.write('machine', 'parent-machine', nozzle_diameter=['0.4'] * 4)
        with mock.patch.object(slicer.subprocess, 'run') as run:
            with self.assertRaisesRegex(slicer.SliceError, 'printable_area'):
                slicer.slice_model(self.source, self.root / 'out', app_path=self.app, profiles_dir=self.vendor)
        run.assert_not_called()
        self.assertFalse((self.root / 'out').exists())

    def test_zero_exit_without_gcode_does_not_claim_slice_and_timeout_is_saved(self):
        with mock.patch.object(slicer.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)):
            report = slicer.slice_model(self.source, self.root / "out", app_path=self.app, profiles_dir=self.vendor)
        self.assertFalse(report["slice_completed"])
        with mock.patch.object(slicer.subprocess, "run", side_effect=subprocess.TimeoutExpired([], 1)):
            report = slicer.slice_model(self.source, self.root / "out", app_path=self.app, profiles_dir=self.vendor, timeout=1)
        self.assertEqual(report["status"], "slice_timed_out")
        self.assertTrue(report["execution"]["timed_out"])

    def test_invalid_names_flow_and_timeouts_fail_before_execution(self):
        for name in ["../Generic PLA", "/tmp/preset"]:
            with self.assertRaises(slicer.SliceError):
                slicer.resolve_preset(self.vendor, "filament", name)
        for timeout in [0, 601, float("nan")]:
            with self.assertRaises(slicer.SliceError):
                slicer.slice_model(self.source, self.root / "out", app_path=self.app, profiles_dir=self.vendor, timeout=timeout)
        self.write("process", slicer.INTENT_PRESETS["normal"], instantiation="true", process_flow_support=["high_flow"], outer_wall_speed=["500"])
        with self.assertRaisesRegex(slicer.SliceError, "standard"):
            slicer.prepare_profiles(self.vendor)


if __name__ == "__main__":
    unittest.main()
