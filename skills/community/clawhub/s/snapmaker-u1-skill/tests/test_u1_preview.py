"""Geometry preview integration checks; no neural weights or network required."""

import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest

import numpy as np
from PIL import Image
import trimesh

from scripts import u1_preview


class MeshPreviewTests(unittest.TestCase):
    def test_cube_renders_png_and_embedded_offline_viewer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "cube.glb"
            cube = trimesh.creation.box(extents=[2, 3, 4])
            cube.visual.vertex_colors = np.tile([220, 40, 20, 255], (len(cube.vertices), 1))
            cube.export(source)
            before = hashlib.sha256(source.read_bytes()).digest()
            result = u1_preview.generate_preview(source, root / "preview")
            self.assertEqual(result["source_triangles"], 12)
            self.assertFalse(result["sampled"])
            self.assertEqual(result["up_axis"], "z")
            with Image.open(result["views"]) as image:
                self.assertEqual(image.format, "PNG")
                self.assertGreater(image.width, 1000)
                self.assertGreater(np.asarray(image).std(), 5)
            document = Path(result["viewer"]).read_text()
            match = re.search(r'<script id="mesh-data" type="application/json">(.*?)</script>', document, re.S)
            data = json.loads(match.group(1))
            self.assertEqual(len(data["triangles"]), 12)
            self.assertTrue(np.isfinite(data["triangles"]).all())
            self.assertGreater(data["colors"][0][0], data["colors"][0][1])
            self.assertIn("pointermove", document)
            self.assertIn("Clay geometry", document)
            self.assertNotRegex(document, r'<(?:script|link)[^>]+(?:src|href)=')
            self.assertEqual(before, hashlib.sha256(source.read_bytes()).digest())

    def test_sampling_is_display_only_and_scene_transforms_are_retained(self):
        scene = trimesh.Scene()
        cube = trimesh.creation.box()
        transform = np.eye(4)
        transform[:3, 3] = [4, 5, 6]
        scene.add_geometry(cube, transform=transform)
        vertices = cube.vertices.copy()
        preview = u1_preview.prepare_scene(scene, max_triangles=5)
        self.assertEqual(preview["source_triangles"], 12)
        self.assertEqual(len(preview["triangles"]), 5)
        self.assertTrue(preview["sampled"])
        np.testing.assert_allclose(preview["bounds"], [[3.5, 4.5, 5.5], [4.5, 5.5, 6.5]])
        np.testing.assert_array_equal(cube.vertices, vertices)

    def test_texture_is_sampled_from_source(self):
        cube = trimesh.creation.box()
        cube.visual = trimesh.visual.texture.TextureVisuals(
            uv=np.full((len(cube.vertices), 2), 0.5),
            image=Image.new("RGB", (4, 4), (15, 210, 30)),
        )
        preview = u1_preview.prepare_scene(cube)
        self.assertIn("texture sampled", preview["appearance"][0])
        self.assertTrue((preview["colors"][:, 1] > 0.75).all())

    def test_obj_and_stl_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            for suffix in ("obj", "stl"):
                path = Path(tmp) / f"cube.{suffix}"
                trimesh.creation.box().export(path)
                scene = trimesh.load(path, force="scene", process=False)
                self.assertEqual(u1_preview.prepare_scene(scene)["source_triangles"], 12)

    def test_nonfinite_geometry_is_rejected(self):
        for value in (float("nan"), float("inf")):
            mesh = trimesh.Trimesh(vertices=[[value, 0, 0], [1, 0, 0], [0, 1, 0]], faces=[[0, 1, 2]], process=False)
            with self.assertRaisesRegex(ValueError, "coordinates"):
                u1_preview.prepare_scene(mesh)

    def test_empty_and_invalid_limits_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "no triangle mesh"):
            u1_preview.prepare_scene(trimesh.Scene())
        with self.assertRaisesRegex(ValueError, "positive"):
            u1_preview.prepare_scene(trimesh.creation.box(), max_triangles=0)

    def test_camera_directions_are_explicit(self):
        specs = u1_preview.view_specs("z")
        self.assertEqual([label for label, _ in specs[:4]], ["From +Y", "From +X", "From -X", "From -Y"])
        for _, eye in specs:
            basis = np.asarray(u1_preview.camera_basis(eye, "z"))
            np.testing.assert_allclose(basis @ basis.T, np.eye(3), atol=1e-12)


if __name__ == "__main__":
    unittest.main()
