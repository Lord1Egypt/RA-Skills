"""Behavioral requirements for local geographic scope resolution."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import qianlima_skill as runtime


class AreaResolutionTests(unittest.TestCase):
    def resolve(self, name, limit=20, parent=None):
        return runtime.cmd_area(SimpleNamespace(name=name, limit=limit, parent=parent))

    def test_city_is_not_province(self):
        p = self.resolve('吉林市')
        self.assertEqual(p['effective_query'].get('areaIds'), [1252])
        self.assertEqual(p.get('resolution_status'), 'resolved')

    def test_city_names_keep_lexical_characters(self):
        for phrase, ids in [('广州市', [305]), ('呼和浩特', [1566]), ('内蒙古自治区', [18])]:
            with self.subTest(phrase=phrase):
                p = self.resolve(phrase)
                self.assertEqual(p['effective_query'].get('areaIds'), ids)

    def test_union_does_not_split_conjunction_inside_place_name(self):
        for text, parent, expected in [('天津、和平区', None, 'ambiguous'),
                                       ('和平和河西', '天津', 'resolved'),
                                       ('呼和浩特和北京', None, 'resolved')]:
            with self.subTest(text=text):
                result = self.resolve(text, parent=parent)
                self.assertEqual(result['resolution_status'], expected)
                if expected == 'resolved':
                    parts = ['和平', '河西'] if parent else ['呼和浩特', '北京']
                    ids = [i for p in parts for i in self.resolve(p, parent=parent)['effective_query']['areaIds']]
                    self.assertEqual(result['effective_query']['areaIds'], ids)

    def test_prefecture_and_its_same_named_city_are_distinct(self):
        for city, city_id, prefecture, prefecture_id in [
            ('阿克苏市',2364,'阿克苏地区',2348),
            ('和田市',2398,'和田地区',2354),
            ('喀什市',2406,'喀什地区',2355),
        ]:
            with self.subTest(city=city):
                self.assertEqual(self.resolve(city)['effective_query'].get('areaIds'),[city_id])
                self.assertEqual(self.resolve(prefecture)['effective_query'].get('areaIds'),[prefecture_id])

    def test_union_ambiguity_limit_keeps_real_total(self):
        for text, total in [('北京、朝阳区',2),('朝阳区、南山区',4)]:
            with self.subTest(text=text):
                p = self.resolve(text,limit=1)
                self.assertEqual(p['total_count'],total)
                self.assertTrue(p['truncated'])
                self.assertEqual(len(p['candidates']),1)

    def test_explicit_scope_can_search_without_narrowing(self):
        for phrase, ids in [('北京市', [2]), ('广东省', [5]), ('深圳市', [316])]:
            with self.subTest(phrase=phrase):
                p = self.resolve(phrase)
                self.assertEqual(p.get('resolution_status'), 'resolved')
                self.assertEqual(p['effective_query']['areaIds'], ids)
                self.assertNotIn('warnings', p)
                self.assertNotIn('user_message', p)

    def test_qualified_and_short_forms(self):
        for phrase, ids in [('海淀', [3320]), ('北京海淀', [3320]), ('北京市海淀区', [3320]),
                            ('上海浦东', [3411]), ('广东省深圳市南山区', [2807]), ('深圳南山', [2807])]:
            with self.subTest(phrase=phrase):
                self.assertEqual(runtime.area_resolver.catalog().match(phrase), [tuple(ids)])
                p = self.resolve(phrase)
                self.assertEqual(p['effective_query'].get('areaIds'), ids)

    def test_ambiguity_has_no_executable_query(self):
        p = self.resolve('朝阳区')
        self.assertEqual(p.get('resolution_status'), 'ambiguous')
        self.assertNotIn('effective_query', p)
        self.assertEqual({a['name'].split('/')[-2] for a in p['candidates']}, {'北京市（市级）', '长春市'})

    def test_bare_same_name_must_not_choose_exact_text_only(self):
        p = self.resolve('朝阳')
        self.assertEqual(p.get('resolution_status'), 'ambiguous')
        self.assertNotIn('effective_query', p)
        self.assertGreaterEqual(len(p['candidates']), 3)

    def test_functional_zone_does_not_match_counties(self):
        p = self.resolve('高新区')
        self.assertEqual(p.get('resolution_status'), 'unmapped')
        self.assertNotIn('areas', p)
        self.assertNotIn('effective_query', p)

    def test_parent_constraint_disambiguates(self):
        p = self.resolve('朝阳区', parent='北京')
        self.assertEqual(p['effective_query']['areaIds'], [3316])

    def test_conflicting_parent_never_relocates(self):
        p = self.resolve('深圳南山区', parent='北京')
        self.assertNotIn('effective_query', p)
        self.assertNotEqual(p.get('resolution_status'), 'resolved')

    def test_union_is_not_choice(self):
        p = self.resolve('北京、上海')
        self.assertEqual(p['effective_query'].get('areaIds'), [2, 24])
        self.assertEqual(p.get('resolution_status'), 'resolved')

    def test_union_partial_match_does_not_execute(self):
        p = self.resolve('北京、火星市')
        self.assertNotIn('effective_query', p)
        self.assertNotEqual(p.get('resolution_status'), 'resolved')

    def test_shared_explicit_parent(self):
        p = self.resolve('海淀和朝阳', parent='北京')
        self.assertEqual(p['effective_query']['areaIds'], [3320, 3316])

    def test_explicit_conjunction_does_not_invent_parent(self):
        p = self.resolve('北京和朝阳区')
        self.assertEqual(p.get('resolution_status'), 'ambiguous')
        self.assertNotIn('effective_query', p)

    def test_region_limit_does_not_truncate_query(self):
        p = self.resolve('华东', limit=1)
        self.assertEqual(p['effective_query'].get('areaIds'), [24, 15, 30, 1, 3, 16, 21])
        self.assertEqual(len(p['areas']), 7)

    def test_candidate_limit_preserves_total_and_ambiguity(self):
        p = self.resolve('朝阳区', limit=1)
        self.assertEqual(p['total_count'], 2)
        self.assertEqual(len(p['candidates']), 1)
        self.assertTrue(p.get('truncated'))
        self.assertEqual(p.get('resolution_status'), 'ambiguous')
        self.assertNotIn('effective_query', p)

    def test_national_is_explicit_clear_operation(self):
        p = self.resolve('全国')
        self.assertEqual(p['effective_query'].get('areaIds'), [])
        self.assertEqual(p.get('resolution_status'), 'resolved')

    def test_exclusion_is_unsupported(self):
        p = self.resolve('全国但排除北京')
        self.assertEqual(p.get('resolution_status'), 'unsupported')
        self.assertNotIn('effective_query', p)

    def test_greater_bay_is_not_silently_mainland_only(self):
        p = self.resolve('粤港澳大湾区')
        self.assertNotEqual(p.get('resolution_status'), 'resolved')
        self.assertNotIn('effective_query', p)
        self.assertIn('内地九市', p['user_message'])
        mainland = self.resolve('大湾区内地九市')
        self.assertEqual(mainland.get('resolution_status'), 'resolved')
        self.assertEqual(len(mainland['effective_query'].get('areaIds', [])), 9)

    def test_full_path_is_visible_without_maintenance_fields(self):
        p = self.resolve('深圳南山')
        self.assertEqual(p['areas'][0]['name'], '广东省/深圳市/南山区')
        self.assertEqual(set(p['areas'][0]), {'name'})

    def test_invalid_limits_rejected(self):
        for limit in [0, -1]:
            with self.subTest(limit=limit), self.assertRaises(runtime.SkillError):
                self.resolve('华东', limit=limit)


if __name__ == '__main__':
    unittest.main()
