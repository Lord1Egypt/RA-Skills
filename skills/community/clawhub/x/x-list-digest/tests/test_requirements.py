import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from analyze import aggregate, enrich
from render import render
from run import parse_init
import test_pipeline


class RequirementsTest(unittest.TestCase):
    def setUp(self):
        fixture = test_pipeline.PipelineTest()
        fixture.setUp()
        self.rows = enrich(fixture.raw, fixture.analysis)
        self.meta = fixture.meta

    def test_unknown_engagement_never_claims_popularity(self):
        self.rows[0]['engagement'] = {'likes': None, 'replies': 9, 'reposts': 1}
        self.rows[1]['category'] = 'off_topic'
        self.rows[1]['engagement'] = {'likes': 100, 'replies': 100, 'reposts': 100}
        summary = render(self.rows, self.meta).split('## Category distribution')[0]
        self.assertNotIn('- Popular：', summary)
        self.assertIn('Insufficient engagement data', summary)

    def test_author_categories_and_summary_dedup(self):
        self.assertEqual(aggregate(self.rows)['authors']['alice']['categories'], {'crypto': 2})
        summary = render(self.rows, self.meta).split('## Category distribution')[0]
        self.assertIn('Off-topic TOP 3', summary)
        self.assertEqual(summary.count('- Core thesis：'), 1)

    def test_collector_contract_parameters(self):
        args, _ = parse_init(['init', '--list', 'primary', '--rhythm', 'aggressive', '--no-expand-threads'])
        self.assertEqual(args.rhythm, 'aggressive')
        self.assertFalse(args.expand_threads)

    def test_thread_parent_must_be_observed(self):
        self.rows[1].update(is_thread_continuation=True, thread_root_id='missing')
        with self.assertRaises(ValueError):
            enrich(self.rows, self.rows)

    def test_thread_with_window_external_root_keeps_reply(self):
        self.rows[1].update(is_thread_continuation=True, thread_root_id='999')
        result=enrich(self.rows,self.rows)
        self.assertFalse(result[1]['thread_root_observed'])
        self.assertIn('root not observed in this window',render(result,self.meta))


if __name__ == '__main__':
    unittest.main()
