import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import area_resolver as a
import qianlima_skill as runtime


class FlatAreaTests(unittest.TestCase):
    def test_parenthesized_limits_are_never_discarded(self):
        self.assertEqual(a.catalog().match('北京（海淀区）'), [(3320,)])
        self.assertEqual(a.resolve('北京（海淀区）')['effective_query']['areaIds'], [3320])
        for name, parent in [('香港（九龙）', None), ('朝阳区', '北京（海淀区）')]:
            self.assertNotIn('effective_query', a.resolve(name, parent=parent))

    def test_whole_city_expression_preserves_city_level(self):
        for name, ids in [('北京全市', [2]), ('吉林市全市', [1252])]:
            self.assertEqual(a.resolve(name)['effective_query']['areaIds'], ids)

    def test_result_rendering_shows_jianyang_once(self):
        self.assertEqual(runtime.area_display_names([2251, 3500]), ['四川省-成都市-简阳市'])

    def test_confirmed_non_city_same_names_select_upper_without_invented_fallback(self):
        directory = a.catalog()
        for lower in [2706, 628, 629, 630, 631, 632, 635, 636, 637, 639, 641, 1092]:
            parent = directory.by_id[lower]['parentid']
            name = directory.by_id[parent]['name']
            self.assertEqual(a.resolve(name)['effective_query']['areaIds'], [parent])
            self.assertIn('同名下级', directory.labels[lower])
            self.assertNotIn('未明确', directory.labels[lower])
        self.assertEqual(directory.fallbacks, {127, 2084, 2267, 2698})

    def test_all_records_stay_in_one_flat_catalog(self):
        rows = json.loads((ROOT / 'references/area.json').read_text())
        self.assertEqual(len(rows), 3536)
        self.assertTrue(all(set(r) == {'areaid', 'name', 'parentid'} for r in rows))
        self.assertEqual(len({r['areaid'] for r in rows}), 3536)
        names = {r['areaid']: r['name'] for r in rows}
        self.assertIn('省级', names[2])
        self.assertIn('市级', names[126])
        self.assertIn('其他', names[127])
        self.assertIn('北京市', names[3316])
        self.assertIn('长春市', names[3181])

    def test_confirmed_query_rules(self):
        for phrase, ids in [('北京', [2]), ('上海', [24]), ('天津', [26]), ('重庆', [31]),
                            ('吉林市', [1252]), ('香港特别行政区', [3557]),
                            ('澳门', [3558]), ('台湾省', [3559]),
                            ('简阳', [2251, 3500]), ('成都简阳市', [2251, 3500]),
                            ('广州市', [305]), ('临高县', [618]), ('巢湖市', [34])]:
            with self.subTest(phrase=phrase):
                p = a.resolve(phrase)
                self.assertEqual(p['resolution_status'], 'resolved', p)
                self.assertEqual(p['effective_query'], {'areaIds': ids})

    def test_jianyang_ids_survive_unions(self):
        p = a.resolve('北京、简阳市')
        self.assertEqual(p['effective_query'], {'areaIds': [2, 2251, 3500]})
        self.assertEqual(len(p['areas']), 2)

    def test_historical_source_regions_are_not_removed(self):
        for phrase, parent, expected in [('公主岭市', '四平市', 1283), ('莱芜', '山东省', 1740)]:
            with self.subTest(phrase=phrase):
                p = a.resolve(phrase, parent=parent)
                self.assertEqual(p['effective_query'], {'areaIds': [expected]})

    def test_only_confirmed_results_expose_query_parameters(self):
        for phrase in ['朝阳区', '高新区', '北京、火星市', '全国排除北京']:
            with self.subTest(phrase=phrase):
                p = a.resolve(phrase)
                self.assertNotIn('effective_query', p)
                for c in p.get('candidates', []):
                    self.assertNotIn('area_id', c)
                    self.assertNotIn('areaIds', c)

    def test_results_are_concise_and_members_are_not_repeated(self):
        for phrase, limit in [('北京海淀', 500), ('朝阳区', 600), ('华东', 1200)]:
            with self.subTest(phrase=phrase):
                p = a.resolve(phrase)
                self.assertLessEqual(len(json.dumps(p, ensure_ascii=False, indent=2)), limit)
                self.assertNotIn('members', p)
                self.assertNotIn('catalog_version', p)
                self.assertNotIn('expansion_suggestion', p)

    def test_complete_group_ignores_candidate_display_limit(self):
        p = a.resolve('华东', limit=1)
        self.assertEqual(p['effective_query']['areaIds'], [24, 15, 30, 1, 3, 16, 21])
        self.assertEqual(len(p['areas']), 7)

    def test_city_and_county_with_different_formal_names_are_not_conflated(self):
        self.assertEqual(a.resolve('承德县')['effective_query']['areaIds'], [696])
        self.assertEqual(a.resolve('阿克苏市')['effective_query']['areaIds'], [2364])
        self.assertNotIn('effective_query', a.resolve('吉林'))


if __name__ == '__main__':
    unittest.main()
