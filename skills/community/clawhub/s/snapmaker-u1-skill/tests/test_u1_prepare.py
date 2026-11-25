"""Small generated fixtures test transformations, topology and CLI contracts."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image
import trimesh


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "u1_prepare.py"
SPEC = importlib.util.spec_from_file_location("u1_prepare", SCRIPT)
prepare = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prepare)


class PrepareMeshTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def fixture(self, mesh, filename="source.stl"):
        path = self.root / filename
        mesh.export(path)
        return path

    def test_cube_stl_scale_placement_and_provenance(self):
        cube = trimesh.creation.box(extents=[2, 4, 6])
        cube.apply_translation([21, -32, 54])
        source = self.fixture(cube)
        report = prepare.prepare_mesh(source, self.root / "out")
        geometry = report["geometry"]
        np.testing.assert_allclose(geometry["size_mm"], [50, 100, 150])
        np.testing.assert_allclose(geometry["bounds_min_mm"], [110.5, 86, 0])
        np.testing.assert_allclose(geometry["bounds_max_mm"], [160.5, 186, 150])
        self.assertTrue(geometry["watertight"])
        self.assertTrue(geometry["winding_consistent"])
        self.assertEqual(geometry["degenerate_triangles"], 0)
        self.assertEqual(report["status"], "geometry_screen_passed")
        self.assertIn("before export", geometry["scope"])
        for extension in ("stl", "glb"):
            exported = report["export_geometry"][extension]
            self.assertEqual(exported["status"], "geometry_screen_passed")
            self.assertTrue(exported["geometry"]["watertight"])
            self.assertEqual(exported["geometry"]["degenerate_triangles"], 0)
            artifact = Path(report["artifacts"][extension])
            self.assertEqual(exported["bytes"], artifact.stat().st_size)
        self.assertFalse(report["ready_to_print"])
        self.assertFalse(report["print_plan"]["slicing_verified"])
        self.assertEqual(Path(report["source"]["copied_input"]).read_bytes(), source.read_bytes())
        self.assertEqual(json.loads(Path(report["artifacts"]["report"]).read_text()), report)
        loaded = trimesh.load_mesh(report["artifacts"]["stl"])
        np.testing.assert_allclose(loaded.bounds, [geometry["bounds_min_mm"], geometry["bounds_max_mm"]])

    def test_axis_rotation_preserves_handedness_and_aspect(self):
        source = self.fixture(trimesh.creation.box(extents=[2, 4, 6]))
        for axis, expected in [("x", [60, 40, 20]), ("y", [10, 30, 20]), ("z", [20 / 3, 40 / 3, 20])]:
            report = prepare.prepare_mesh(source, self.root / axis, height_mm=20, up_axis=axis)
            np.testing.assert_allclose(report["geometry"]["size_mm"], expected)
            self.assertTrue(all(volume > 0 for volume in report["geometry"]["component_signed_volumes_mm3"]))

    def test_multipart_default_retains_details_explicit_largest_removes(self):
        large = trimesh.creation.box(extents=[10, 10, 10])
        small = trimesh.creation.box(extents=[1, 1, 1])
        small.apply_translation([20, 0, 0])
        source = self.fixture(trimesh.util.concatenate([large, small]), "parts.obj")
        retained = prepare.prepare_mesh(source, self.root / "retain", height_mm=50)
        self.assertEqual(retained["geometry"]["triangles"], 24)
        self.assertEqual(retained["geometry"]["edge_connected_components"], 2)
        self.assertEqual(retained["component_selection"]["removed_components"], 0)
        selected = prepare.prepare_mesh(source, self.root / "largest", height_mm=50, largest_component=True)
        self.assertEqual(selected["geometry"]["triangles"], 12)
        self.assertEqual(selected["geometry"]["edge_connected_components"], 1)
        self.assertEqual(selected["component_selection"]["removed_components"], 1)
        np.testing.assert_allclose(selected["geometry"]["size_mm"], [50, 50, 50])

    def test_textured_glb_and_scene_instance_transform_are_preserved(self):
        cube = trimesh.creation.box(extents=[2, 4, 6])
        pixels = np.zeros((2, 2, 3), dtype=np.uint8)
        pixels[:, :] = [13, 47, 129]
        cube.visual = trimesh.visual.texture.TextureVisuals(uv=np.zeros((len(cube.vertices), 2)), image=Image.fromarray(pixels))
        scene = trimesh.Scene()
        transform = np.eye(4)
        transform[:3, 3] = [100, 200, 300]
        scene.add_geometry(cube, transform=transform)
        source = self.fixture(scene, "textured.glb")
        report = prepare.prepare_mesh(source, self.root / "textured", height_mm=60)
        np.testing.assert_allclose(report["geometry"]["size_mm"], [20, 40, 60])
        preserved = trimesh.load_scene(report["artifacts"]["glb"], process=False)
        part = next(iter(preserved.geometry.values()))
        self.assertEqual(part.visual.kind, "texture")
        self.assertTrue(np.array_equal(np.asarray(part.visual.material.baseColorTexture.convert("RGB"))[0, 0], [13, 47, 129]))
        self.assertEqual(report["print_plan"]["color"]["full_spectrum"], "not_converted")

    def test_open_mesh_is_reported_and_not_silently_repaired(self):
        cube = trimesh.creation.box()
        cube.update_faces(np.arange(len(cube.faces) - 1))
        source = self.fixture(cube)
        report = prepare.prepare_mesh(source, self.root / "open")
        self.assertEqual(report["geometry"]["triangles"], 11)
        self.assertFalse(report["geometry"]["watertight"])
        self.assertEqual(report["geometry"]["open_boundary_edges"], 3)
        self.assertEqual(report["status"], "needs_geometry_review")
        self.assertIn("self_intersections", report["geometry"]["untested"])
        self.assertIn("minimum_feature_thickness", report["geometry"]["untested"])
        self.assertIn("likeness", report["geometry"]["untested"])

    def test_degenerate_triangle_and_inverted_component_are_flagged(self):
        cube = trimesh.creation.box()
        cube.invert()
        degenerate = trimesh.Trimesh(vertices=[[5, 0, 0], [5, 0, 0], [5, 1, 0]], faces=[[0, 1, 2]], process=False)
        report = prepare.prepare_mesh(self.fixture(trimesh.util.concatenate([cube, degenerate])), self.root / "degenerate", height_mm=10)
        self.assertEqual(report["geometry"]["degenerate_triangles"], 1)
        self.assertIn("mesh contains degenerate triangles", report["review_reasons"])
        inverted = prepare.prepare_mesh(self.fixture(cube, "inverted.stl"), self.root / "inverted", height_mm=10)
        self.assertIn("one or more closed components have nonpositive signed volume", inverted["review_reasons"])

    def test_float32_export_collapse_is_reported_without_automatic_repair(self):
        # All four source vertices remain distinct near zero in glTF float32.
        # After scale/bed placement, the first two X coordinates round to the
        # same float32 value around135.5mm. The float64 screen alone misses it.
        vertices = np.array([[0, 0, 0], [1e-9, 0, 0], [0, 1, 0], [0, 0, 1]])
        faces = np.array([[0, 2, 1], [0, 1, 3], [0, 3, 2], [1, 2, 3]])
        source = self.fixture(trimesh.Trimesh(vertices=vertices, faces=faces, process=False), "thin-tetra.glb")
        source_bytes = source.read_bytes()
        source_mesh = trimesh.load_mesh(source, process=False)
        self.assertEqual(len(np.unique(source_mesh.vertices, axis=0)), 4)
        report = prepare.prepare_mesh(source, self.root / "collapsed", height_mm=150)
        self.assertEqual(report["geometry"]["degenerate_triangles"], 0)
        self.assertTrue(report["geometry"]["watertight"])
        self.assertEqual(report["status"], "needs_geometry_review")
        self.assertFalse(report["ready_to_print"])
        for extension in ("stl", "glb"):
            exported = report["export_geometry"][extension]
            self.assertEqual(exported["status"], "needs_geometry_review")
            self.assertGreater(exported["geometry"]["degenerate_triangles"], 0)
            self.assertEqual(exported["geometry"]["triangles"], 4)
            # No collapsed faces are deleted and no coordinates get changed
            # to hide the encoding problem; the actual artifact stays flagged.
            loaded = trimesh.load_mesh(report["artifacts"][extension], process=False)
            self.assertEqual(len(loaded.faces), 4)
            self.assertTrue(any(reason.startswith(f"exported {extension.upper()}:") for reason in report["review_reasons"]))
        self.assertEqual(source.read_bytes(), source_bytes)

    def test_encoded_readback_failure_is_not_a_passing_screen(self):
        diagnostic = prepare._screen_encoded_export(b"not valid mesh bytes", "glb")
        self.assertEqual(diagnostic["status"], "readback_failed")
        self.assertTrue(diagnostic["review_reasons"])
        self.assertNotIn("geometry", diagnostic)

    def test_invalid_and_heightless_input_rejected_before_output(self):
        bad = self.root / "bad.obj"
        bad.write_text("v nan 0 0\nv 1 0 0\nv 0 1 1\nf 1 2 3\n")
        output = self.root / "bad-output"
        with self.assertRaises(prepare.PreparationError):
            prepare.prepare_mesh(bad, output)
        self.assertFalse(output.exists())
        flat = trimesh.Trimesh(vertices=[[0, 0, 0], [1, 0, 0], [0, 1, 0]], faces=[[0, 1, 2]], process=False)
        with self.assertRaisesRegex(prepare.PreparationError, "zero height"):
            prepare.prepare_mesh(self.fixture(flat, "flat.obj"), output)
        for height in [0, -1, float("nan"), float("inf")]:
            with self.assertRaises(prepare.PreparationError):
                prepare.prepare_mesh(bad, output, height_mm=height)

    def test_cli_json_fit_failure_and_recommendations(self):
        source = self.fixture(trimesh.creation.box(extents=[4, 1, 1]))
        command = [sys.executable, str(SCRIPT), str(source), "--output-dir", str(self.root / "cli"), "--height-mm", "100", "--intent", "strong", "--material", "PETG", "--infill-percent", "30"]
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report["geometry"]["fits_nominal_u1_envelope"])
        self.assertEqual(report["print_plan"]["infill"]["recommended_percent"], 30)
        self.assertEqual(report["print_plan"]["material"]["requested_family"], "PETG")
        self.assertEqual(report["print_plan"]["status"], "recommendations_only_unsliced")
        self.assertIsNone(report["print_plan"]["sliced_material_grams"])
        failed = subprocess.run([sys.executable, str(SCRIPT), str(self.root / "missing.stl"), "--output-dir", str(self.root / "missing")], text=True, capture_output=True, check=False)
        self.assertEqual(failed.returncode, 2)
        self.assertIn("ERROR:", failed.stderr)

    def test_repeat_runs_are_deterministic(self):
        source = self.fixture(trimesh.creation.box())
        output = self.root / "repeat"
        first = prepare.prepare_mesh(source, output)
        first_stl = Path(first["artifacts"]["stl"]).read_bytes()
        first_glb = Path(first["artifacts"]["glb"]).read_bytes()
        second = prepare.prepare_mesh(source, output)
        self.assertEqual(first, second)
        self.assertEqual(first_stl, Path(second["artifacts"]["stl"]).read_bytes())
        self.assertEqual(first_glb, Path(second["artifacts"]["glb"]).read_bytes())

    def test_output_cannot_overwrite_input_master(self):
        source = self.fixture(trimesh.creation.box(), "prepared.stl")
        original = source.read_bytes()
        with self.assertRaisesRegex(prepare.PreparationError, "overwrite the input master"):
            prepare.prepare_mesh(source, self.root)
        self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
