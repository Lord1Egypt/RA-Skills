"""Read-only transport and conservative physical-spool comparisons; no live printer."""
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import u1_printer_check as check


class Response:
    def __init__(self, payload, status=200):
        self.status = status
        self.body = json.dumps(payload).encode() if not isinstance(payload, bytes) else payload

    def read(self, size):
        return self.body[:size]


def live_data():
    data = {'print_stats': {'state': 'standby', 'print_duration': 0}, 'virtual_sdcard': {'progress': 0},
            'heater_bed': {'temperature': 23.5, 'target': 0},
            'filament_detect': {'info': [{'VENDOR': 'Snapmaker', 'MAIN_TYPE': 'PLA', 'RGB_1': 0xFF0000, 'WEIGHT': 1000},
                                         {'VENDOR': 'Snapmaker', 'MAIN_TYPE': 'PLA', 'RGB_1': 0xFFFFFF}]}}
    for i in range(4):
        data[f'filament_motion_sensor e{i}_filament'] = {'filament_detected': True, 'enabled': True}
        data['extruder' if i == 0 else f'extruder{i}'] = {'temperature': 24, 'target': 0}
    return data


class PrinterCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.calls = []

    def transport(self, responses):
        owner = self
        class Connection:
            def __init__(self, host, port, timeout):
                self.closed = False
            def request(self, method, path, body=None, headers=None):
                owner.calls.append((method, path, body, headers))
            def getresponse(self):
                return responses.pop(0)
            def close(self):
                self.closed = True
        return mock.patch.object(check.http.client, 'HTTPConnection', Connection)

    def snapshot(self, data=None, state='ready'):
        data = live_data() if data is None else data
        with self.transport([Response({'result': {'state': state}}),
                             Response({'result': {'objects': list(data)}}),
                             Response({'result': {'status': data}})]):
            return check.collect_snapshot('192.168.1.123', api_key='SYNTHETIC_KEY')

    def project(self, **changes):
        settings = {'filament_settings_id': ['PLA red', 'PLA white'], 'filament_type': ['PLA', 'PLA'],
                    'filament_colour': ['#FF0000', '#FFFFFFFF'], 'mixed_filament_definitions': ''}
        settings.update(changes)
        path = self.root / 'project.3mf'
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr('Metadata/project_settings.config', json.dumps(settings))
        return path

    def cli(self, argv):
        output = io.StringIO()
        with redirect_stdout(output):
            code = check.main(argv)
        return code, json.loads(output.getvalue())

    def test_transport_is_get_only_fixed_routes_and_no_payload(self):
        snapshot = self.snapshot()
        self.assertEqual(len(self.calls), 3)
        self.assertTrue(all(method == 'GET' and body is None for method, _, body, _ in self.calls))
        self.assertEqual(self.calls[0][1], '/printer/info')
        self.assertEqual(self.calls[1][1], '/printer/objects/list')
        self.assertIn('filament_motion_sensor%20e0_filament', self.calls[2][1])
        self.assertEqual(self.calls[0][3]['X-Api-Key'], 'SYNTHETIC_KEY')
        self.assertNotIn('SYNTHETIC_KEY', json.dumps(snapshot))
        self.assertEqual(snapshot['temperatures_c']['heater_bed']['temperature'], 23.5)

    def test_no_arbitrary_endpoint_or_object_can_be_requested(self):
        for endpoint, objects in [('gcode', ()), ('/printer/print/cancel', ()), ('query', ('gcode_macro UNLOAD',)), ('info', ('print_stats',)), ('query', ())]:
            with self.subTest(endpoint=endpoint), mock.patch.object(check.http.client, 'HTTPConnection') as connection:
                with self.assertRaises(check.CheckError):
                    check.get_json('192.168.1.123', 80, endpoint, objects=objects)
                connection.assert_not_called()

    def test_public_hosts_hostnames_invalid_ports_timeouts_rejected_before_connect(self):
        for host in ['8.8.8.8', 'https://192.168.1.1', 'printer.local', '0.0.0.0', '224.0.0.1', '2001:4860:4860::8888', '192.0.2.1']:
            with self.subTest(host=host), mock.patch.object(check.http.client, 'HTTPConnection') as connection:
                with self.assertRaises(check.CheckError):
                    check.get_json(host, 80, 'info')
                connection.assert_not_called()
        for host in ['192.168.1.123', '10.1.2.3', '172.16.0.2', '127.0.0.1', '::1', 'fd00::1']:
            check.validate_connection(host, 80, 5)
        for port, timeout in [(0, 5), (65536, 5), (True, 5), (80, float('nan')), (80, 11), (80, 0)]:
            with self.assertRaises(check.CheckError):
                check.validate_connection('192.168.1.123', port, timeout)

    def test_http_api_and_json_errors_never_report_success_or_leak_bodies(self):
        for response in [Response({'result': {}}, 401), Response({'result': {}}, 302),
                         Response({'error': {'message': 'SYNTHETIC_KEY'}}), Response({'result': []}),
                         Response(b'not json'), Response(b'\xff'), Response(b'x' * (check.MAX_BYTES + 1))]:
            with self.subTest(status=response.status), self.transport([response]):
                with self.assertRaises(check.CheckError) as caught:
                    check.get_json('192.168.1.123', 80, 'info')
                self.assertNotIn('SYNTHETIC_KEY', str(caught.exception))
        with mock.patch.object(check.http.client.HTTPConnection, 'request', side_effect=TimeoutError('SYNTHETIC_KEY')):
            with self.assertRaisesRegex(check.CheckError, 'request failed') as caught:
                check.get_json('192.168.1.123', 80, 'info')
        self.assertNotIn('SYNTHETIC_KEY', str(caught.exception))

    def test_missing_rfid_never_infers_white_or_material_from_defaults(self):
        data = live_data()
        data['filament_detect']['info'][0] = {'VENDOR': 'NONE', 'MAIN_TYPE': 'PLA', 'RGB_1': 0xFFFFFF}
        snapshot = self.snapshot(data)
        result = check.compare_slots(snapshot, {1: {'material': 'PLA', 'color': '#FFFFFF'}})
        self.assertFalse(result['passed'])
        self.assertEqual(result['slots'][0]['checks'], {'presence': 'match', 'material': 'unknown', 'color': 'unknown'})
        self.assertIsNone(snapshot['slots'][0]['tag_metadata'])
        self.assertEqual(snapshot['slots'][0]['metadata_source'], 'unknown')

    def test_absent_disabled_and_missing_sensors_are_distinct_from_loaded(self):
        for sensor, expected in [({'enabled': True, 'filament_detected': False}, 'mismatch'),
                                 ({'enabled': False, 'filament_detected': True}, 'unknown'), ({}, 'unknown')]:
            data = live_data()
            data['filament_motion_sensor e0_filament'] = sensor
            result = check.compare_slots(self.snapshot(data), {1: {'material': 'PLA', 'color': '#FF0000'}})
            self.assertEqual(result['slots'][0]['checks']['presence'], expected)
            self.assertFalse(result['passed'])

    def test_material_and_color_mismatches_and_busy_printer_fail_comparison(self):
        snapshot = self.snapshot()
        for expected, field in [({'material': 'PETG', 'color': '#FF0000'}, 'material'),
                                ({'material': 'PLA', 'color': '#FFFF00'}, 'color')]:
            result = check.compare_slots(snapshot, {1: expected})
            self.assertFalse(result['passed'])
            self.assertEqual(result['slots'][0]['checks'][field], 'mismatch')
        self.assertTrue(check.compare_slots(snapshot, {1: {'material': 'PLA', 'color': '#FF0000'}})['passed'])
        for state in ['printing', 'paused', 'error', None]:
            data = live_data(); data['print_stats']['state'] = state
            self.assertFalse(check.compare_slots(self.snapshot(data), {1: {'material': 'PLA', 'color': '#FF0000'}})['passed'])
        self.assertFalse(check.compare_slots(self.snapshot(state='shutdown'), {1: {'material': 'PLA', 'color': '#FF0000'}})['passed'])

    def test_missing_objects_and_nonfinite_values_stay_unknown(self):
        data = {'print_stats': {'state': 'standby'}, 'virtual_sdcard': {'progress': 1.1}, 'heater_bed': {'temperature': float('nan')}}
        snapshot = self.snapshot(data)
        self.assertIsNone(snapshot['progress_percent'])
        self.assertIsNone(snapshot['temperatures_c']['heater_bed']['temperature'])
        self.assertIn('filament_detect', snapshot['unavailable_objects'])
        self.assertEqual(snapshot['slots'][0]['material'], None)
        query = self.calls[-1][1]
        self.assertNotIn('filament_detect', query)
        json.dumps(snapshot, allow_nan=False)

    def test_decoded_tag_fields_are_separate_and_unused_defaults_stay_unknown(self):
        data = live_data()
        data['filament_detect']['info'][0].update({'MANUFACTURER': 'Synthetic Maker', 'SUB_TYPE': 'Basic',
            'DIAMETER': 175, 'WEIGHT': 1000, 'LENGTH': 330, 'DRYING_TEMP': 50, 'DRYING_TIME': 6,
            'HOTEND_MIN_TEMP': 190, 'HOTEND_MAX_TEMP': 230, 'BED_TEMP': 60, 'FIRST_LAYER_TEMP': 0,
            'OTHER_LAYER_TEMP': float('nan'), 'COLOR_NUMS': 1, 'RGB_2': 0xFFFFFF,
            'ALPHA': 0, 'OFFICIAL': True, 'CARD_UID': [1, 2, 3, 4]})
        slot = self.snapshot(data)['slots'][0]
        self.assertEqual(slot['metadata_source'], 'filament_detect')
        tag = slot['tag_metadata']
        self.assertEqual(tag['DIAMETER'], 175)  # Raw firmware encoding, no guessed unit conversion.
        self.assertEqual(tag['WEIGHT'], 1000)
        self.assertEqual(tag['DRYING_TIME'], 6)
        self.assertEqual(tag['CARD_UID'], [1, 2, 3, 4])
        self.assertTrue(tag['OFFICIAL'])
        self.assertEqual(tag['ALPHA'], 0)
        self.assertIsNone(tag['RGB_2'])
        self.assertIsNone(tag['FIRST_LAYER_TEMP'])
        self.assertIsNone(tag['OTHER_LAYER_TEMP'])
        json.dumps(slot, allow_nan=False)

    def test_invalid_tag_fields_are_not_coerced_to_real_values(self):
        for uid in [0, [0, 0, 0, 0], [True, 2, 3, 4], [-1], [256], [1] * 33, 'unrecognized']:
            tag = check.tag_metadata({'VENDOR': 'Synthetic', 'CARD_UID': uid, 'ALPHA': 256,
                                      'RGB_1': True, 'WEIGHT': -1, 'OFFICIAL': 'true'})
            self.assertIsNone(tag['CARD_UID'])
            self.assertIsNone(tag['ALPHA'])
            self.assertIsNone(tag['RGB_1'])
            self.assertIsNone(tag['WEIGHT'])
            self.assertIsNone(tag['OFFICIAL'])
        tag = check.tag_metadata({'VENDOR': 'Synthetic', 'COLOR_NUMS': 2, 'RGB_1': 0, 'RGB_2': 0x123456})
        self.assertEqual(tag['RGB_1'], '#000000')
        self.assertEqual(tag['RGB_2'], '#123456')

    def test_configured_third_party_identity_does_not_become_an_rfid_match(self):
        data = live_data()
        data['filament_detect']['info'][0] = {'VENDOR': 'NONE', 'RGB_1': 0xFFFFFF}
        data['print_task_config'] = {'filament_type': ['PLA'], 'filament_vendor': ['Generic'],
            'filament_sub_type': ['Basic'], 'filament_color_rgba': ['ff000080'],
            'filament_official': [False], 'filament_exist': [True]}
        snapshot = self.snapshot(data)
        slot = snapshot['slots'][0]
        self.assertIsNone(slot['material'])
        self.assertIsNone(slot['color'])
        self.assertIsNone(slot['tag_metadata'])
        self.assertEqual(slot['configured_filament'], {'source': 'printer_configuration', 'material': 'PLA',
            'vendor': 'Generic', 'sub_type': 'Basic', 'color': '#FF0000', 'alpha': 128, 'official': False})
        self.assertFalse(check.compare_slots(snapshot, {1: {'material': 'PLA', 'color': '#FF0000'}})['passed'])
        del data['filament_motion_sensor e0_filament']
        result = check.compare_slots(self.snapshot(data), {1: {'material': 'PLA', 'color': '#FF0000'}})
        self.assertEqual(result['slots'][0]['checks']['presence'], 'unknown')

    def test_configured_rfid_conflicts_prevent_comparison_success(self):
        data = live_data()
        data['print_task_config'] = {'filament_type': ['PETG'], 'filament_color_rgba': ['000000FF']}
        snapshot = self.snapshot(data)
        self.assertEqual(snapshot['slots'][0]['metadata_conflicts'], ['material', 'color'])
        result = check.compare_slots(snapshot, {1: {'material': 'PLA', 'color': '#FF0000'}})
        self.assertFalse(result['passed'])
        self.assertEqual(result['slots'][0]['checks']['metadata_consistency'], 'mismatch')
        data['print_task_config'] = {'filament_type': ['PLA'], 'filament_color_rgba': ['FF0000FF']}
        self.assertTrue(check.compare_slots(self.snapshot(data), {1: {'material': 'PLA', 'color': '#FF0000'}})['passed'])

    def test_partial_configuration_and_current_task_mapping_are_conservative(self):
        data = live_data()
        data['print_task_config'] = {'filament_type': ['NONE', 'PLA'], 'filament_color_rgba': ['FFFFFFFF', '###FF0000FF'],
            'extruder_map_table': [3, 2, 1, 0, 4, True, '1', -1]}
        snapshot = self.snapshot(data)
        self.assertIsNone(snapshot['slots'][0]['configured_filament'])
        self.assertIsNone(snapshot['slots'][1]['configured_filament']['color'])
        self.assertIsNone(snapshot['slots'][2]['configured_filament'])
        self.assertEqual(snapshot['logical_to_physical_tools'], [4, 3, 2, 1, None, None, None, None])
        self.assertIn('not a mapping for a new project', snapshot['tool_map_scope'])
        data['print_task_config'] = {'filament_type': 'PLA', 'extruder_map_table': [0] * 33}
        self.assertIsNone(self.snapshot(data)['logical_to_physical_tools'])

    def test_project_mapping_is_explicit_complete_and_preserves_source(self):
        path = self.project()
        before = path.read_bytes()
        expected = check.project_expected(path, '1:2,2:1')
        self.assertEqual(expected[2], {'material': 'PLA', 'color': '#FF0000'})
        self.assertEqual(expected[1]['color'], '#FFFFFF')
        for mapping in [None, '', '1:1', '1:1,2:1', '1:1,1:2', '1:0,2:2', '1:1,2:5', '1:1:2,2:2']:
            with self.subTest(mapping=mapping), self.assertRaises(check.CheckError):
                check.project_expected(path, mapping)
        self.assertEqual(path.read_bytes(), before)

    def test_mixed_unknown_and_target_projects_require_physical_expectations(self):
        for changes in [{'mixed_filament_definitions': 'opaque calibration recipe'}, {'mixed_filament_definitions': []},
                        {'filament_colour': ['#FF0000']}, {'filament_type': ['PLA', '']},
                        {'filament_colour': ['#FF000000', '#FFFFFF']}]:
            with self.subTest(changes=changes), self.assertRaises(check.CheckError):
                check.project_expected(self.project(**changes), '1:1,2:2')
        path = self.project()
        with zipfile.ZipFile(path, 'a') as archive:
            archive.writestr('Metadata/u1_target_colors.json', '{}')
        with self.assertRaisesRegex(check.CheckError, 'target palette'):
            check.project_expected(path, '1:1,2:2')

    def test_explicit_physical_spools_support_full_spectrum_without_reading_recipes(self):
        path = self.root / 'physical.json'
        path.write_text(json.dumps({'1': {'material': ' pla ', 'color': '#ff0000'}, '4': {'material': 'PLA', 'color': '#FFFFFF'}}))
        expected = check.load_expected(path)
        self.assertEqual(expected[1], {'material': 'PLA', 'color': '#FF0000'})
        self.assertEqual(set(expected), {1, 4})
        for bad in [{}, [], {'0': {}}, {'1': {'material': 'PLA'}}, {'1': {'material': '', 'color': '#FF0000'}}]:
            path.write_text(json.dumps(bad))
            with self.subTest(bad=bad), self.assertRaises(check.CheckError):
                check.load_expected(path)
        path.write_bytes(b'x' * (check.MAX_BYTES + 1))
        with self.assertRaisesRegex(check.CheckError, '1 MiB'):
            check.load_expected(path)

    def test_cli_snapshot_vs_pass_mismatch_unknown_and_connection_failure(self):
        snapshot = self.snapshot()
        project = self.project()
        base = ['--host', '192.168.1.123']
        with mock.patch.object(check, 'collect_snapshot', return_value=snapshot):
            code, report = self.cli(base)
            self.assertEqual(code, 0)
            self.assertEqual(report['target'], {'host': '192.168.1.123', 'port': 80})
            self.assertIsNone(report['preflight_passed'])
            code, report = self.cli(base + ['--project', str(project), '--slot-map', '1:1,2:2'])
            self.assertEqual(code, 0)
            self.assertTrue(report['preflight_passed'])
            self.assertFalse(report['ready_to_print'])
            self.assertEqual(report['expectations_source']['sha256'], hashlib.sha256(project.read_bytes()).hexdigest())
            code, report = self.cli(base + ['--project', str(project), '--slot-map', '1:2,2:1'])
            self.assertEqual(code, 1)
            self.assertFalse(report['preflight_passed'])
        with mock.patch.object(check, 'collect_snapshot', side_effect=check.CheckError('printer unavailable')):
            code, report = self.cli(base)
            self.assertEqual(code, 2)
            self.assertFalse(report['snapshot_completed'])

    def test_invalid_expectations_and_existing_outputs_never_connect_or_overwrite(self):
        path = self.project(mixed_filament_definitions='preserve')
        existing = self.root / 'report.json'; existing.write_text('preserve')
        original = path.read_bytes()
        for flags in [['--project', str(path), '--slot-map', '1:1,2:2'], ['--project', str(path)],
                      ['--slot-map', '1:1'], ['--output', str(existing)], ['--output', str(path)],
                      ['--output', str(self.root / 'missing' / 'report.json')]]:
            with self.subTest(flags=flags), mock.patch.object(check, 'collect_snapshot') as collect:
                code, _ = self.cli(['--host', '192.168.1.123', *flags])
                self.assertEqual(code, 2)
                collect.assert_not_called()
        self.assertEqual(existing.read_text(), 'preserve')
        self.assertEqual(path.read_bytes(), original)

    def test_fresh_report_written_and_api_key_not_serialized(self):
        output = self.root / 'report.json'
        snapshot = self.snapshot()
        with mock.patch.object(check, 'collect_snapshot', return_value=snapshot) as collect, mock.patch.dict(check.os.environ, {'SNAPMAKER_API_KEY': 'SYNTHETIC_KEY'}):
            code, report = self.cli(['--host', '192.168.1.123', '--output', str(output)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.read_text()), report)
        self.assertNotIn('SYNTHETIC_KEY', output.read_text())
        self.assertEqual(collect.call_args.kwargs['api_key'], 'SYNTHETIC_KEY')


if __name__ == '__main__':
    unittest.main()
