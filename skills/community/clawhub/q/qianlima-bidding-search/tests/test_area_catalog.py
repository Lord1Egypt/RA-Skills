import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from area_resolver import AreaCatalog, AreaError, REFERENCES, catalog


class AreaCatalogTests(unittest.TestCase):
    def test_every_original_id_parent_and_order_is_preserved(self):
        rows = json.loads((REFERENCES/'area.json').read_text())
        digest = hashlib.sha256(json.dumps([(r['areaid'],r['parentid']) for r in rows],separators=(',',':')).encode()).hexdigest()
        self.assertEqual(digest, '6a82ca6fa2e8eab3f960dba45ebe018ec7a1688b4e65528f72c63c8f4a640793')
        self.assertEqual(len(rows),3536)

    def test_directly_administered_county_keeps_upper_business_node(self):
        for name,area_id in [('临高县',618),('济源市',806),('石河子市',2358)]:
            self.assertEqual(catalog().resolve(name)['effective_query']['areaIds'],[area_id])
            self.assertIsNone(catalog().city_parent(area_id))

    def test_technical_nodes_are_retained_and_valid(self):
        for area_id,parent in [(126,2),(127,126),(1274,1252),(636,618)]:
            self.assertEqual(catalog().by_id[area_id]['parentid'],parent)
            self.assertEqual(catalog().validate_ids([area_id]),[area_id])
        self.assertEqual(catalog().query_ids(1274),(1252,))

    def test_invalid_catalog_structure_rejected(self):
        for records in [
            [{'areaid':1,'name':'A','parentid':2}],
            [{'areaid':1,'name':'A','parentid':1}],
            [{'areaid':1,'name':'A','parentid':0},{'areaid':1,'name':'B','parentid':0}],
            [{'areaid':1,'name':'A','parentid':0},{'areaid':2,'name':'B','parentid':1}],
        ]:
            with self.subTest(records=records), self.assertRaises(AreaError):AreaCatalog(records)

    def test_historical_names_remain_in_original_parent(self):
        result = catalog().resolve('公主岭市',parent='四平市')
        self.assertEqual(result['effective_query']['areaIds'],[1283])
        self.assertIn('四平市',result['areas'][0]['name'])

    def test_old_city_is_not_renamed_to_modern_district(self):
        self.assertEqual(catalog().resolve('莱芜市')['effective_query']['areaIds'],[1740])
        self.assertNotIn('effective_query',catalog().resolve('莱芜区'))
        self.assertIn(2976,catalog().by_id)

    def test_jianyang_mapping_always_keeps_both_records(self):
        result=catalog().resolve('简阳市')
        self.assertEqual(result['effective_query']['areaIds'],[2251,3500])
        self.assertEqual(len(result['areas']),1)
        self.assertEqual(catalog().by_id[2251]['parentid'],2087)
        self.assertEqual(catalog().by_id[3500]['parentid'],2087)

    def test_parent_constraint_does_not_confuse_two_ids_with_two_places(self):
        result=catalog().resolve('城区',parent='简阳市')
        self.assertEqual(result['resolution_status'],'unmapped')
        self.assertNotIn('candidates',result)


if __name__=='__main__':unittest.main()
