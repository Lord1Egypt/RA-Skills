"""Geometry/color contract tests for the generic 3MF preparation tool."""

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image

from scripts import u1_color


NS = {"c": u1_color.CORE_NS, "m": u1_color.MATERIAL_NS}


def unpack_3mf(path):
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise AssertionError("corrupt ZIP archive")
        model = ET.fromstring(archive.read("3D/3dmodel.model"))
        # The package parts must also be valid XML, with the appropriate namespaces.
        content = ET.fromstring(archive.read("[Content_Types].xml"))
        relationships = ET.fromstring(archive.read("_rels/.rels"))
    return model, content, relationships


class ColorPreparationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def colored_cube(self, name="cube.ply"):
        mesh = trimesh.creation.box(extents=[8, 12, 16])
        face_rgb = np.repeat(np.array([
            [255, 0, 0], [0, 255, 0], [0, 0, 255],
            [255, 255, 255], [0, 0, 0], [220, 130, 90],
        ], dtype=np.uint8), 2, axis=0)
        mesh.visual.face_colors = np.column_stack([face_rgb, np.full(len(face_rgb), 255)])
        path = self.directory / name
        mesh.export(path)
        return path

    def test_opc_documents_use_default_namespace_for_native_reader(self):
        source = self.colored_cube()
        output, _, _ = u1_color.prepare_colors(source, self.directory / "native-reader")
        with zipfile.ZipFile(output) as archive:
            relationships = archive.read("_rels/.rels")
            types = archive.read("[Content_Types].xml")
            self.assertIn(b"<Relationships xmlns=", relationships)
            self.assertIn(b"<Relationship ", relationships)
            self.assertIn(b"<Types xmlns=", types)
            self.assertNotIn(b"ns0:", relationships + types)

    def test_cube_retains_geometry_and_per_face_rgb_and_source_master(self):
        source = self.colored_cube()
        before = source.read_bytes()
        original = trimesh.load(source, process=False)
        output, report_path, report = u1_color.prepare_colors(source, self.directory / "out")
        model, content, relationships = unpack_3mf(output)
        self.assertEqual(source.read_bytes(), before)
        self.assertEqual(report["source_master"]["sha256"], hashlib.sha256(before).hexdigest())
        self.assertTrue(report["source_master"]["preserved"])
        self.assertEqual(json.loads(report_path.read_text()), report)
        self.assertEqual(model.attrib["unit"], "millimeter")
        self.assertEqual(model.attrib["requiredextensions"], "m")
        self.assertEqual(content.tag, f"{{{u1_color.CONTENT_NS}}}Types")
        self.assertEqual(relationships[0].attrib["Target"], "/3D/3dmodel.model")
        self.assertIsNone(model.find("c:resources/c:basematerials", NS))
        palette = np.array([
            [int(item.attrib["color"][i:i + 2], 16) for i in (1, 3, 5)]
            for item in model.findall("c:resources/m:colorgroup/m:color", NS)
        ])
        self.assertEqual(len(palette), 6)  # Eight requested target colors does not force four spool colors.
        vertices = model.findall("c:resources/c:object/c:mesh/c:vertices/c:vertex", NS)
        serialized_vertices = np.array([[float(vertex.attrib[axis]) for axis in "xyz"] for vertex in vertices])
        np.testing.assert_array_equal(serialized_vertices, original.vertices)
        triangles = model.findall("c:resources/c:object/c:mesh/c:triangles/c:triangle", NS)
        serialized_faces = np.array([[int(face.attrib[f"v{i}"]) for i in (1, 2, 3)] for face in triangles])
        np.testing.assert_array_equal(serialized_faces, original.faces)
        for index, face in enumerate(triangles):
            self.assertEqual(face.attrib["pid"], "1")
            for corner in (1, 2, 3):
                np.testing.assert_array_equal(palette[int(face.attrib[f"p{corner}"])], original.visual.face_colors[index, :3])
        np.testing.assert_array_equal(report["geometry"]["bounds_mm"], original.bounds)
        self.assertEqual(sum(region["corner_count"] for region in report["target_color_regions"]), len(original.faces) * 3)
        self.assertFalse(report["fullspectrum"]["recipes_calculated"])
        self.assertEqual(report["orca"]["status"], "manual_import_and_color_matching_required")

    def test_vertex_colors_remain_per_corner_and_extraction_does_not_mutate_mesh(self):
        mesh = trimesh.creation.box()
        rgb = np.array([[i * 25, 255 - i * 20, i * 13] for i in range(len(mesh.vertices))], dtype=np.uint8)
        mesh.visual.vertex_colors = np.column_stack([rgb, np.full(len(rgb), 255)])
        vertices, faces, colors = mesh.vertices.copy(), mesh.faces.copy(), mesh.visual.vertex_colors.copy()
        extracted, kind, nonopaque = u1_color.extract_corner_colors(mesh)
        np.testing.assert_array_equal(extracted, rgb[mesh.faces])
        self.assertEqual(kind, "vertex_colors")
        self.assertEqual(nonopaque, 0)
        # Modifying returned samples cannot alter the source visual.
        extracted[:] = 17
        np.testing.assert_array_equal(mesh.vertices, vertices)
        np.testing.assert_array_equal(mesh.faces, faces)
        np.testing.assert_array_equal(mesh.visual.vertex_colors, colors)

    def test_glb_instances_keep_world_bounds_and_vertex_colors(self):
        mesh = trimesh.creation.box(extents=[2, 4, 6])
        mesh.visual.vertex_colors = np.array([[v * 20, 255 - v * 20, 80, 255] for v in range(8)], dtype=np.uint8)
        scene = trimesh.Scene()
        translated = np.eye(4)
        translated[:3, 3] = [5, -7, 20]
        scene.add_geometry(mesh, node_name="translated", transform=translated)
        reflected = np.diag([-1.0, 1.0, 1.0, 1.0])
        reflected[:3, 3] = [18, 0, 4]
        scene.add_geometry(mesh.copy(), node_name="reflected", transform=reflected)
        source = self.directory / "instances.glb"
        scene.export(source)
        loaded = trimesh.load_scene(source, process=False)
        meshes = u1_color.load_colored_meshes(source)
        before = source.read_bytes()
        output, _, report = u1_color.prepare_colors(source, self.directory / "out")
        model, _, _ = unpack_3mf(output)
        self.assertEqual(len(model.findall("c:resources/c:object", NS)), 2)
        self.assertEqual(report["geometry"]["triangles"], 24)
        np.testing.assert_allclose(report["geometry"]["bounds_mm"], loaded.bounds)
        self.assertEqual(source.read_bytes(), before)
        self.assertEqual(len(report["target_color_regions"]), 8)
        for colored in meshes:
            # Baking reflections must retain outward winding and corner pairing.
            check = trimesh.Trimesh(vertices=colored.vertices, faces=colored.faces, process=False)
            self.assertGreater(check.volume, 0)

    def test_obj_texture_is_sampled_and_original_assets_are_untouched(self):
        mesh = trimesh.Trimesh(vertices=[[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0]], faces=[[0, 1, 2], [0, 2, 3]], process=False)
        pixels = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]], dtype=np.uint8)
        mesh.visual = trimesh.visual.texture.TextureVisuals(uv=[[0, 0], [1, 0], [1, 1], [0, 1]], image=Image.fromarray(pixels))
        source = self.directory / "texture.obj"
        mesh.export(source)
        assets_before = {path.name: path.read_bytes() for path in self.directory.iterdir() if path.is_file()}
        output, _, report = u1_color.prepare_colors(source, self.directory / "out")
        self.assertTrue(output.is_file())
        self.assertIn("texture_uv_corners", report["color_extraction"]["meshes"][0]["source"])
        self.assertEqual(report["quantization"]["target_color_count"], 4)
        for filename, original in assets_before.items():
            self.assertEqual((self.directory / filename).read_bytes(), original)

    def test_meter_conversion_is_explicit_and_default_numeric_mm_is_preserved(self):
        source = self.colored_cube()
        _, _, millimeters = u1_color.prepare_colors(source, self.directory / "mm")
        _, _, meters = u1_color.prepare_colors(source, self.directory / "m", input_units="m")
        np.testing.assert_array_equal(meters["geometry"]["bounds_mm"], np.array(millimeters["geometry"]["bounds_mm"]) * 1000)
        self.assertEqual(millimeters["millimeters_per_input_unit"], 1)
        self.assertEqual(meters["millimeters_per_input_unit"], 1000)

    def test_quantization_is_deterministic_and_retains_exact_palette_when_possible(self):
        rgb = np.array([[40, 100, 160], [255, 0, 0], [40, 100, 160], [1, 2, 3]], dtype=np.uint8)
        palette, assignments = u1_color.quantize_target_colors(rgb, 8)
        np.testing.assert_array_equal(palette[assignments], rgb)
        rng = np.random.default_rng(12)
        many = rng.integers(0, 256, (1200, 3), dtype=np.uint8)
        first, assigned = u1_color.quantize_target_colors(many, 8)
        second, reordered = u1_color.quantize_target_colors(many[::-1], 8)
        np.testing.assert_array_equal(first, second)
        np.testing.assert_array_equal(assigned, reordered[::-1])
        self.assertLessEqual(len(first), 8)
        self.assertGreater(len(first), 4)

    def test_repeated_preparation_is_byte_deterministic(self):
        source = self.colored_cube()
        first, _, _ = u1_color.prepare_colors(source, self.directory / "out")
        first_data = first.read_bytes()
        second, _, _ = u1_color.prepare_colors(source, self.directory / "out")
        self.assertEqual(first_data, second.read_bytes())

    def test_perceptual_palette_preserves_two_percent_warm_patch(self):
        # A jacket and white shirt occupy 98% of samples. Numerous common
        # shades must not consume every entry and turn the small warm patch gray.
        from skimage.color import rgb2lab
        rng = np.random.default_rng(284)
        navy = np.array([25, 35, 60]) + rng.integers(-12, 13, (7500, 3))
        white = np.repeat(rng.integers(170, 251, (2300, 1)), 3, axis=1)
        warm = np.array([140, 105, 96]) + rng.integers(-4, 5, (200, 3))
        samples = np.concatenate([navy, white, warm]).astype(np.uint8)
        palette, labels = u1_color.quantize_target_colors(samples, 8)
        lab_palette = rgb2lab(palette.astype(float) / 255)
        lab_warm = rgb2lab(np.array([[140, 105, 96]], dtype=float) / 255)
        self.assertLess(float(np.linalg.norm(lab_palette - lab_warm, axis=1).min()), 5)
        reconstructed = palette[labels[-len(warm):]].astype(np.int16)
        self.assertGreater(float(np.mean(reconstructed[:, 0] > reconstructed[:, 2] + 12)), 0.95)
        self.assertLessEqual(len(palette), 8)
        np.testing.assert_array_equal(samples[-200:], warm)

    def test_nearest_filament_is_opt_in_and_keeps_virtual_target_report(self):
        source = self.colored_cube()
        spool_file = self.directory / "spools.json"
        spool_file.write_text(json.dumps({"filaments": [{"name": "Actual black", "rgb": [0, 0, 0]}, {"name": "Actual white", "rgb": [255, 255, 255]}]}))
        output, _, report = u1_color.prepare_colors(source, self.directory / "out", mode="nearest-filament", filament_palette=spool_file)
        model, _, _ = unpack_3mf(output)
        self.assertEqual(len(model.findall("c:resources/m:colorgroup/m:color", NS)), 2)
        self.assertEqual(len(report["target_color_regions"]), 6)
        self.assertEqual(report["quantization"]["choice"], "nearest-filament")
        self.assertFalse(report["fullspectrum"]["recipes_calculated"])
        self.assertEqual({region["filament_name"] for region in report["output_color_regions"]}, {"Actual black", "Actual white"})

    def test_invalid_inputs_fail_before_outputs_are_created(self):
        source = self.colored_cube()
        destination = self.directory / "never_created"
        for options in ({"colors": 0}, {"colors": 257}, {"colors": True}, {"input_units": "cm"},
                        {"mode": "nearest-filament"}, {"mode": "target", "filament_palette": "unused"}, {"mode": "bogus"}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                u1_color.prepare_colors(source, destination, **options)
            self.assertFalse(destination.exists())
        with self.assertRaisesRegex(ValueError, "does not exist"):
            u1_color.prepare_colors(self.directory / "missing.glb", destination)
        unsupported = self.directory / "plain.stl"
        trimesh.creation.box().export(unsupported)
        with self.assertRaisesRegex(ValueError, "input must be"):
            u1_color.prepare_colors(unsupported, destination)
        uncolored = self.directory / "uncolored.ply"
        trimesh.creation.box().export(uncolored)
        with self.assertRaisesRegex(ValueError, "no explicit"):
            u1_color.prepare_colors(uncolored, destination)

    def test_nonfinite_geometry_and_invalid_palette_fail(self):
        source = self.directory / "bad.ply"
        source.write_text("ply\nformat ascii 1.0\nelement vertex 3\nproperty float x\nproperty float y\nproperty float z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\nelement face 1\nproperty list uchar int vertex_indices\nend_header\nnan 0 0 255 0 0\n1 0 0 255 0 0\n0 1 0 255 0 0\n3 0 1 2\n")
        with self.assertRaisesRegex(ValueError, "finite"):
            u1_color.prepare_colors(source, self.directory / "out")
        for records in ([], [{"name": "Red", "rgb": [300, 0, 0]}], [{"name": "Red", "rgb": [True, 0, 0]}], [{"rgb": [1, 2, 3]}],
                        [{"name": "A", "rgb": [1, 2, 3]}, {"name": "B", "rgb": [1, 2, 3]}]):
            palette = self.directory / "palette.json"
            palette.write_text(json.dumps(records))
            with self.subTest(records=records), self.assertRaises(ValueError):
                u1_color.load_filament_palette(palette)

    def test_cli_runs_and_reports_errors_without_traceback(self):
        source = self.colored_cube()
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            status = u1_color.main([str(source), "--output-dir", str(self.directory / "out"), "--colors", "8", "--units", "mm"])
        self.assertEqual(status, 0)
        self.assertIn("Source master retained", stdout.getvalue())
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            status = u1_color.main([str(source), "--output-dir", str(self.directory / "out"), "--colors", "0"])
        self.assertEqual(status, 2)
        self.assertIn("ERROR:", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
