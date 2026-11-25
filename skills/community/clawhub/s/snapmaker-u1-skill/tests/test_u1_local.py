import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
import numpy as np

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
from u1_mcubes import marching_cubes
from u1_local import prepare_image, verify_runtime

class LocalEngineTests(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec("torch") and importlib.util.find_spec("skimage"), "optional Torch/scikit-image inference dependencies not installed")
    def test_cpu_isosurface_adapter_preserves_axis_order(self):
        import torch
        # Offset ellipsoid distinguishes XYZ from a mirrored/transposed output.
        xyz=np.stack(np.meshgrid(*[np.arange(33)]*3,indexing='ij'),axis=-1)
        field=1-(((xyz-np.array([10,16,20]))/np.array([5,7,9]))**2).sum(axis=-1)
        v,f=marching_cubes(torch.tensor(field,dtype=torch.float32),0.)
        restored=v.numpy()[:,::-1]  # pinned upstream helper's reversal
        np.testing.assert_allclose((restored.min(0)+restored.max(0))/2,[10,16,20],atol=.1)
        self.assertEqual(f.shape[1],3)
        self.assertTrue(np.isfinite(restored).all())
    @unittest.skipUnless(importlib.util.find_spec("torch") and importlib.util.find_spec("skimage"), "optional Torch/scikit-image inference dependencies not installed")
    def test_no_isosurface_is_an_error(self):
        import torch
        with self.assertRaises(ValueError):marching_cubes(torch.ones((5,5,5)),0)
    def test_supplied_alpha_is_preserved_and_centered(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            out=Path(d);image=Image.new('RGBA',(120,80),(0,0,0,0))
            for i in range(40,80):
                for j in range(10,70):image.putpixel((i,j),(200,100,50,255))
            image.save(out/'source.png')
            prepared,report=prepare_image(out/'source.png',out,.85,'alpha')
            self.assertEqual(prepared.size,(512,512))
            self.assertAlmostEqual(report['foreground_fraction'],.25)
            self.assertTrue(report['mask_review_required'])
            self.assertTrue((out/'subject_rgba.png').is_file())
    def test_opaque_input_requires_real_segmentation(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            out=Path(d);Image.new('RGB',(10,10)).save(out/'source.png')
            with self.assertRaises(ValueError):prepare_image(out/'source.png',out,.85,'alpha')
    def test_missing_engine_is_not_simulated(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):verify_runtime(Path(d))


class RuntimeSafetyTests(unittest.TestCase):
    def test_doctor_accepts_a_new_nested_runtime(self):
        import contextlib,io,json
        from u1_local import doctor
        with tempfile.TemporaryDirectory() as d:
            text=io.StringIO()
            with contextlib.redirect_stdout(text):doctor(Path(d)/'new'/'nested'/'runtime')
            self.assertGreater(json.loads(text.getvalue())['free_disk_gib'],0)
    def test_asset_verification_rejects_changed_segmentation_and_dino(self):
        import json
        from u1_local import SOURCE_COMMIT,sha256
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);weights=root/'weights';weights.mkdir()
            (weights/'model.ckpt').write_bytes(b'fixture-checkpoint')
            (weights/'config.yaml').write_text('fixture-config')
            dino=root/'dino.json';dino.write_text('{}')
            seg=root/'segmentation'/'u2net_human_seg.onnx';seg.parent.mkdir();seg.write_bytes(b'fixture-mask-model')
            m={'source_commit':SOURCE_COMMIT,'setup_complete':True,'source_patches':{},'weights':str(weights),
               'checkpoint_sha256':sha256(weights/'model.ckpt'),'config_sha256':sha256(weights/'config.yaml'),
               'dino_config_path':str(dino),'dino_config_sha256':sha256(dino),'segmentation_sha256':sha256(seg)}
            (root/'engine.json').write_text(json.dumps(m))
            verify_runtime(root)
            seg.write_bytes(b'corrupt')
            with self.assertRaisesRegex(ValueError,'Segmentation'):verify_runtime(root)
            seg.write_bytes(b'fixture-mask-model');dino.unlink()
            with self.assertRaisesRegex(ValueError,'DINO'):verify_runtime(root)



class NativeAppleRoutingTests(unittest.TestCase):
    def test_explicit_vision_never_silently_selects_human_model(self):
        from u1_local import select_segmentation_backend
        self.assertEqual(select_segmentation_backend('vision', Path('/missing/native/helper')), 'vision')
    def test_explicit_vision_reports_missing_helper(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            out=Path(d);Image.new('RGB',(10,10),(200,150,100)).save(out/'source.png')
            with self.assertRaisesRegex(ValueError,'Vision helper'):
                prepare_image(out/'source.png',out,.85,'vision',native_binary=out/'missing')
    def test_existing_alpha_is_labeled_as_supplied_not_apple_inference(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            out=Path(d);a=Image.new('RGBA',(20,20),(120,90,60,0))
            for x in range(5,15):
                for y in range(5,15):a.putpixel((x,y),(120,90,60,255))
            a.save(out/'source.png')
            _,r=prepare_image(out/'source.png',out,.85,'vision',native_binary=out/'missing')
            self.assertEqual(r['background_method'],'provided_alpha')
            self.assertIsNone(r['native_vision_report'])

if __name__=='__main__':unittest.main()
