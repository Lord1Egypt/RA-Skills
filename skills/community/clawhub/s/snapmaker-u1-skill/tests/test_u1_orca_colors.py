import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile, ZIP_DEFLATED
import xml.etree.ElementTree as ET

from scripts import u1_orca_colors as colors


class OrcaColorsTests(unittest.TestCase):
    def make_source(self, path):
        xml = f'''<model xmlns="{colors.CORE}" xmlns:m="{colors.MATERIAL}" requiredextensions="m"><resources><m:colorgroup id="1"><m:color color="#A08060FF"/></m:colorgroup><object id="2"><mesh><vertices><vertex x="0" y="0" z="0"/><vertex x="1" y="0" z="0"/><vertex x="0" y="1" z="0"/></vertices><triangles><triangle v1="0" v2="1" v3="2" pid="1" p1="0" p2="0" p3="0"/></triangles></mesh></object></resources><build><item objectid="2"/></build></model>'''
        with ZipFile(path, 'w', ZIP_DEFLATED) as archive:
            archive.writestr('3D/3dmodel.model', xml)

    def write_template(self, path, config):
        with ZipFile(path, 'w', ZIP_DEFLATED) as archive:
            archive.writestr('Metadata/project_settings.config', json.dumps(config))

    def test_eight_targets_paint_and_no_stale_slice_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, template, output = (root / name for name in ("source.3mf", "template.3mf", "native.3mf"))
            palette = [f"#{i * 31:02X}2030FF" for i in range(8)]
            xml = f'<model xmlns="{colors.CORE}" xmlns:m="{colors.MATERIAL}" requiredextensions="m"><resources><m:colorgroup id="1">'
            xml += ''.join(f'<m:color color="{c}"/>' for c in palette)
            xml += '</m:colorgroup><object id="2"><mesh><vertices><vertex x="0" y="0" z="0"/><vertex x="1" y="0" z="0"/><vertex x="0" y="1" z="0"/></vertices><triangles>'
            xml += ''.join(f'<triangle v1="0" v2="1" v3="2" pid="1" p1="{i}" p2="{i}" p3="{i}"/>' for i in range(8))
            xml += '</triangles></mesh></object></resources><build><item objectid="2"/></build></model>'
            with ZipFile(source, 'w', ZIP_DEFLATED) as z:
                z.writestr('3D/3dmodel.model', xml)
            with ZipFile(template, 'w', ZIP_DEFLATED) as z:
                z.writestr('Metadata/project_settings.config', json.dumps({'filament_settings_id':['Generic PLA'], 'filament_colour':['#FFFFFF'], 'filament_type':['PLA'], 'nozzle_diameter':['0.4'] * 4}))
                z.writestr('Metadata/plate_1.gcode', 'STALE')
                z.writestr('Metadata/slice_info.config', 'STALE')
            report = colors.convert(source, template, output)
            self.assertEqual(set(report['paint_counts']), set(colors.CODES[:8]))
            self.assertEqual(report['corner_approximated_triangles'], 0)
            self.assertTrue(report['requires_reslice'])
            with ZipFile(output) as z:
                self.assertFalse(any('gcode' in name or 'plate_' in name or 'slice_info' in name for name in z.namelist()))
                model = ET.fromstring(z.read('3D/3dmodel.model'))
                self.assertEqual([t.get('paint_color') for t in model.iter(f'{{{colors.CORE}}}triangle')], list(colors.CODES[:8]))
                settings = json.loads(z.read('Metadata/project_settings.config'))
                self.assertEqual(settings['filament_colour'], [c[:7] for c in palette])
                self.assertEqual(settings['filament_settings_id'], ['Generic PLA'] * 8)
                self.assertEqual(len(settings['nozzle_diameter']), 4)
                parts = ET.fromstring(z.read('Metadata/model_settings.config')).findall('./object/part')
                self.assertEqual(len(parts), 1)
                self.assertEqual(parts[0].find('mesh_stat').attrib, {'edges_fixed': '0', 'degenerate_facets': '0', 'facets_removed': '0', 'facets_reversed': '0', 'backwards_edges': '0'})
                self.assertEqual([vertex.attrib for vertex in model.iter(f'{{{colors.CORE}}}vertex')], [{'x': '0', 'y': '0', 'z': '0'}, {'x': '1', 'y': '0', 'z': '0'}, {'x': '0', 'y': '1', 'z': '0'}])
                self.assertTrue(all([triangle.get('v1'), triangle.get('v2'), triangle.get('v3')] == ['0', '1', '2'] for triangle in model.iter(f'{{{colors.CORE}}}triangle')))
                self.assertTrue(z.read('_rels/.rels').startswith(b'<?xml'))
                self.assertNotIn(b'ns0:', z.read('_rels/.rels'))

    def test_existing_mix_definitions_are_rejected_without_writing_or_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, template, output = (root / name for name in ('source.3mf', 'calibrated.3mf', 'out.3mf'))
            self.make_source(source)
            for definitions in ('2,4,0,1,50,0,g,w,m0', {'recipe': 'existing'}, ['existing']):
                with self.subTest(definitions=definitions):
                    self.write_template(template, {'filament_settings_id': ['PLA'], 'filament_colour': ['#FFFFFF'], 'mixed_filament_definitions': definitions})
                    source_bytes, template_bytes = source.read_bytes(), template.read_bytes()
                    with self.assertRaisesRegex(ValueError, 'existing mixing definitions'):
                        colors.convert(source, template, output)
                    self.assertFalse(output.exists())
                    self.assertEqual(source.read_bytes(), source_bytes)
                    self.assertEqual(template.read_bytes(), template_bytes)

    def test_multiple_or_missing_source_filaments_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, template, output = (root / name for name in ('source.3mf', 'template.3mf', 'out.3mf'))
            self.make_source(source)
            configurations = [
                {'filament_settings_id': ['PLA', 'PETG'], 'filament_colour': ['#FFFFFF', '#000000']},
                {'filament_settings_id': ['PLA'], 'filament_colour': ['#FFFFFF', '#000000']},
                {'filament_settings_id': ['PLA', 'PLA'], 'filament_colour': ['#FFFFFF']},
                {'filament_settings_id': [], 'filament_colour': []},
                {'filament_colour': ['#FFFFFF']},
                {'filament_settings_id': [''], 'filament_colour': ['#FFFFFF']},
                {'filament_settings_id': 'PLA', 'filament_colour': ['#FFFFFF']},
            ]
            for config in configurations:
                with self.subTest(config=config):
                    self.write_template(template, config)
                    template_bytes = template.read_bytes()
                    with self.assertRaisesRegex(ValueError, 'exactly one source filament'):
                        colors.convert(source, template, output)
                    self.assertFalse(output.exists())
                    self.assertEqual(template.read_bytes(), template_bytes)

    def test_template_guard_runs_before_source_parse_and_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, template, output = (root / name for name in ('invalid-source.3mf', 'calibrated.3mf', 'keep.3mf'))
            source.write_bytes(b'not a model; template should fail first')
            output.write_bytes(b'preserve existing output')
            self.write_template(template, {'filament_settings_id': ['PLA'], 'filament_colour': ['#FFFFFF'], 'mixed_filament_definitions': 'existing'})
            with self.assertRaisesRegex(ValueError, 'existing mixing definitions'):
                colors.convert(source, template, output)
            self.assertEqual(output.read_bytes(), b'preserve existing output')

    def test_empty_mixing_field_allows_fresh_unmatched_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, template, output = (root / name for name in ('source.3mf', 'template.3mf', 'out.3mf'))
            self.make_source(source)
            self.write_template(template, {'filament_settings_id': ['PLA'], 'filament_colour': ['#FFFFFF'], 'mixed_filament_definitions': ''})
            report = colors.convert(source, template, output)
            self.assertEqual(report['target_palette'], ['#A08060'])
            self.assertTrue(report['requires_manual_match'])
            self.assertFalse(report['native_roundtrip_verified'])
            with ZipFile(output) as archive:
                self.assertEqual(json.loads(archive.read('Metadata/project_settings.config'))['mixed_filament_definitions'], '')


if __name__ == '__main__':
    unittest.main()
