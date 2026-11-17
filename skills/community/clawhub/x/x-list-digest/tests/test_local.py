import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from run import parse_init
from render import render
from analyze import enrich
import test_pipeline


class LocalDefaultsTest(unittest.TestCase):
    def test_unknown_engagement_does_not_break_report(self):
        fixture = test_pipeline.PipelineTest()
        fixture.setUp()
        rows = enrich(fixture.raw, fixture.analysis)
        rows[0]['engagement'] = {'likes': None, 'replies': 2}
        self.assertIn('None', render(rows, fixture.meta))

    def test_config_defaults_and_explicit_override(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / 'config.yaml'
            config.write_text('default_window_hours: 48\ndefault_max_tweets: 7\ndefault_output: file\nlists: {}\n')
            args, _ = parse_init(['init', '--config', str(config), '--list', 'https://x.com/i/lists/1'])
            self.assertEqual((args.window, args.max_tweets, args.output), ('48h', 7, 'file'))
            args, _ = parse_init(['init', '--config', str(config), '--list', 'https://x.com/i/lists/1', '--window', '12h', '--max-tweets', '3', '--output', 'both'])
            self.assertEqual((args.window, args.max_tweets, args.output), ('12h', 3, 'both'))

    def test_invalid_config_defaults_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / 'config.yaml'
            config.write_text('default_window_hours: -1\nlists: {}\n')
            with self.assertRaises(ValueError):
                parse_init(['init', '--config', str(config), '--list', 'https://x.com/i/lists/1'])


if __name__ == '__main__':
    unittest.main()
