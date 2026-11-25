"""Synthetic bounds, modal-state and actual-toolpath preview regressions."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import u1_gcode as gcode

MACHINE = {'printable_area': ['0x0', '10x0', '10x10', '0x10'], 'printable_height': '10', 'bed_exclude_area': ['0x0']}
START = 'G90\nM83\nG0 X2 Y2 Z1\n'


def review(text, machine=MACHINE):
    paths = gcode.parse_gcode(text, gcode.machine_region(machine)[4])
    return paths, gcode.validate_paths(paths, machine)


class GcodeTests(unittest.TestCase):
    def test_relative_and_absolute_extrusion_and_resets(self):
        paths, report = review(START + 'G1 X3 E1\nG1 E-1\nG1 E1\nM82\nG92 E100\nG1 X4 E101\nG1 X5 E100\nG92 E0\nG1 X6 E1\n')
        self.assertTrue(report['passed'], report)
        np.testing.assert_allclose(paths['segments'][:, 1, 0], [3, 4, 6])

    def test_klipper_g91_makes_e_relative_even_after_m82(self):
        paths, report = review(START + 'M82\nG92 E100\nG91\nG1 X1 E1\nG1 X1 E1\nG90\nG1 X5 E103\n')
        self.assertTrue(report['passed'], report)
        np.testing.assert_allclose(paths['segments'][:, 1, 0], [3, 4, 5])

    def test_g92_xyz_keeps_physical_offset(self):
        _, report = review(START + 'G92 X0\nG1 X9 E1\n')
        self.assertFalse(report['passed'])
        self.assertEqual(report['bounds_mm'][1][0], 11)

    def test_unknown_start_and_absolute_e_after_tool_change_fail_closed(self):
        for code in ['M83\nG1 X1 Y1 Z1 E1', START + 'M82\nT1\nG1 X3 E100', START + 'G28 X Y\nG1 X3 E1']:
            with self.subTest(code=code):
                self.assertFalse(review(code)[1]['passed'])
        self.assertTrue(review(START + 'T1\nG1 X3 E1')[1]['passed'])
        self.assertTrue(review(START + 'M82\nT1\nG92 E0\nG1 X3 E1')[1]['passed'])

    def test_all_features_and_layers_checked_custom_explicitly_excluded(self):
        text = START + ';TYPE:Custom\nG1 X20 E1\nG0 X2\n;TYPE:Brim\nG1 X3 E1\n;LAYER_CHANGE\n;TYPE:Support interface\nG1 X11 E1\n'
        paths, report = review(text)
        self.assertFalse(report['passed'])
        self.assertEqual(report['skipped_custom_extrusions'], 1)
        self.assertEqual(report['segments_checked'], 2)
        self.assertEqual(report['violation_lines'], [len(text.splitlines())])
        self.assertEqual(paths['features'], ['Brim', 'Support interface'])

    def test_actual_offset_profile_and_z_bounds(self):
        machine = {**MACHINE, 'printable_area': ['1x1', '11x1', '11x11', '1x11']}
        self.assertTrue(review(START + 'G1 X11 E1', machine)[1]['passed'])
        for endpoint in ['X0.5', 'Z10.01', 'Z-0.01']:
            self.assertFalse(review(START + f'G1 {endpoint} E1', machine)[1]['passed'])

    def test_concave_notch_and_exclusion_crossings(self):
        concave = {**MACHINE, 'printable_area': ['0x0', '10x0', '10x10', '6x10', '6x4', '4x4', '4x10', '0x10']}
        self.assertFalse(review('M83\nG0 X2 Y8 Z1\nG1 X8 E1', concave)[1]['passed'])
        hole = {**MACHINE, 'bed_exclude_area': ['4x4', '6x4', '6x6', '4x6']}
        self.assertFalse(review('M83\nG0 X2 Y5 Z1\nG1 X8 E1', hole)[1]['passed'])
        self.assertTrue(review(START + 'G1 X8 E1', hole)[1]['passed'])

    def test_arcs_full_circle_helical_cw_and_ccw(self):
        for command in ['G2', 'G3']:
            paths, report = review('M83\nG0 X8 Y5 Z1\n' + command + ' I-3 J0 Z2 E1 P1')
            self.assertTrue(report['passed'], report)
            self.assertEqual(report['arc_moves'], 1)
            self.assertAlmostEqual(report['bounds_mm'][0][0], 2)
            self.assertAlmostEqual(report['bounds_mm'][1][1], 8)
            self.assertEqual(paths['segments'][-1, 1, 2], 2)

    def test_arc_extrema_caught_even_with_inside_endpoints(self):
        _, report = review('M83\nG0 X1 Y1 Z1\nG2 X9 Y1 I4 J0 E1')
        self.assertTrue(report['passed'])  # Upper semicircle.
        _, report = review('M83\nG0 X1 Y1 Z1\nG3 X9 Y1 I4 J0 E1')
        self.assertFalse(report['passed'])
        self.assertAlmostEqual(report['bounds_mm'][0][1], -3)
        diamond = {**MACHINE, 'printable_area': ['5x0', '10x5', '5x10', '0x5']}
        # Cardinal extrema fit, but the circle crosses the diagonal bed edges.
        self.assertFalse(review('M83\nG0 X9 Y5 Z1\nG3 I-4 E1', diamond)[1]['passed'])

    def test_unsupported_modes_and_malformed_input_cannot_pass(self):
        for tail in ['G20\nG1 X3 E1', 'G18\nG2 X3 I1 E1', 'G2 X3 R1 E1', 'G2 I1 P2 E1', 'G90.1\nG1 X3 E1', 'G1 Xnan E1', 'G1 X3 A2 E1', 'G1 X3 E1 Q2', 'G1??', 'T0.1', 'RESTORE_GCODE_STATE NAME=x\nG1 X3 E1']:
            with self.subTest(tail=tail):
                self.assertFalse(review(START + tail)[1]['passed'])
        hole = {**MACHINE, 'bed_exclude_area': ['4x4', '6x4', '6x6', '4x6']}
        self.assertFalse(review('M83\nG0 X3 Y3 Z1\nG2 I1 E1', hole)[1]['passed'])

    def test_invalid_machine_profiles_are_rejected(self):
        for bad in [[], {}, {**MACHINE, 'printable_height': 'nan'}, {**MACHINE, 'printable_area': ['0x0', '1x1', '0x1', '1x0']}, {**MACHINE, 'printable_area': ['0x0', 'nanx0', '1x1']}]:
            with self.subTest(machine=bad), self.assertRaises(ValueError):
                gcode.machine_region(bad)

    def test_review_writes_actual_path_previews_and_failed_status(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as temp:
            report = gcode.review_gcode(START + ';TYPE:Brim\nG1 X3 E1\n;TYPE:Support\nG1 X11 E1', MACHINE, temp)
            self.assertFalse(report['review_completed'])
            self.assertFalse(report['ready_to_print'])
            self.assertEqual(report['previews']['segments_total'], 2)
            self.assertIn('Support', report['features'])
            for path in report['previews']['files'].values():
                with Image.open(path) as image:
                    self.assertGreater(image.width, 500)
                    image.verify()
            self.assertEqual(json.loads((Path(temp) / 'toolpath-review.json').read_text()), report)

    def test_preview_sampling_cannot_hide_a_validation_failure(self):
        paths = gcode.parse_gcode(START + 'G1 X3 E1')
        count = 100100
        paths['segments'] = np.repeat(paths['segments'], count, axis=0)
        paths['segments'][50000, 1, 0] = 11
        paths['features'] = ['Support'] * (count - 1) + ['Brim']
        paths['lines'] = list(range(1, count + 1))
        paths['tools'] = [0] * count
        report = gcode.validate_paths(paths, MACHINE)
        self.assertFalse(report['passed'])
        self.assertEqual(report['segments_checked'], count)
        self.assertEqual(report['violation_lines'], [50001])
        with tempfile.TemporaryDirectory() as temp:
            previews = gcode.render_paths(paths, report, temp)
        self.assertTrue(previews['sampled'])
        self.assertLessEqual(previews['segments_displayed'], 100000)
        self.assertEqual(previews['segments_total'], count)

    def test_standalone_cli_exit_codes_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, machine = root / 'test.gcode', root / 'machine.json'
            source.write_text(START + 'G1 X11 E1')
            machine.write_text(json.dumps(MACHINE))
            args = [sys.executable, gcode.__file__, str(source), '--machine-json', str(machine), '--output-dir', str(root / 'out')]
            result = subprocess.run(args, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertFalse(json.loads(result.stdout)['passed'])
            self.assertEqual(subprocess.run(args, capture_output=True).returncode, 2)


if __name__ == '__main__':
    unittest.main()
