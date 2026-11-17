import sys,tempfile,sqlite3,unittest
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from collect import normalize
from analyze import enrich,aggregate
from render import render
from persist import persist
class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.raw=[dict(tweet_id=str(i),author_handle='alice',timestamp_iso='2026-10-09T12:00:00Z',text='BTCThesis',url=f'https://x.com/alice/status/{i}') for i in (1,2)]
        self.analysis=[dict(tweet_id=str(i),category='crypto',subcategory='BTC',tickers=['BTC'],sentiment=s,key_thesis='Thesis',is_actionable=False,confidence='med',is_thread_continuation=False,thread_root_id=None) for i,s in ((1,'bullish'),(2,'bearish'))]
        self.meta=dict(list_name='Test',list_url='https://x.com/i/lists/1',window_hours=24,window_start='2026-10-09T00:00:00Z',window_end='2026-10-10T00:00:00Z',coverage='partial',stop_reason='max_tweets')
    def test_window_dedup(self):
        rows=self.raw+[self.raw[0],{**self.raw[0],'tweet_id':'3','timestamp_iso':'2026-10-08T12:00:00Z'}]
        self.assertEqual(len(normalize(rows,datetime(2026,10,10,tzinfo=timezone.utc),24,100)),2)
    def test_analysis_and_independent_votes(self):
        rows=enrich(self.raw,self.analysis)
        self.assertEqual(aggregate(rows)['tickers']['BTC']['author_votes'],{'alice':'mixed'})
        self.assertIn('partial',render(rows,self.meta))
        with self.assertRaises(ValueError):enrich(self.raw,self.analysis[:1])
    def test_overlapping_digest_membership(self):
        with tempfile.TemporaryDirectory() as d:
            db=str(Path(d)/'digest.db');rows=enrich(self.raw,self.analysis)
            persist(db,rows,self.meta,'raw.json','enriched.json');persist(db,rows,self.meta,'raw.json','enriched.json')
            with sqlite3.connect(db) as c:
                self.assertEqual(c.execute('SELECT COUNT(*) FROM tweets').fetchone()[0],2)
                self.assertEqual(c.execute('SELECT COUNT(*) FROM digest_tweets').fetchone()[0],4)
if __name__=='__main__':unittest.main()
