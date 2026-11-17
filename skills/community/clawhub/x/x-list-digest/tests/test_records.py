import hashlib
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run import initialize,finish
from collector_record import record
from publish_record import finalize
from common import write
from daily_bundle import bundle
from collect import normalize
from common import iso
from datetime import timedelta


class RecordTest(unittest.TestCase):
    def test_no_silent_batch_truncation(self):
        end=iso('2026-10-10T00:00:00Z')
        rows=[{'tweet_id':str(i),'timestamp_iso':end.isoformat()} for i in range(305)]
        self.assertEqual(len(normalize(rows,end,24,300)),305)

    def test_default_daily_limits(self):
        with tempfile.TemporaryDirectory() as d:
            meta=initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]
            self.assertEqual((meta['max_tweets'],meta['collector_limits']['timeout_seconds'],meta['collector_limits']['max_steps']),(500,2700,300))

    def test_finish_rejects_unproved_complete_and_keeps_overshoot(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d,maximum=1)[0]['run_dir'])
            meta=json.loads((run/'metadata.json').read_text())
            rows=[{'tweet_id':str(i),'author_handle':'alice','text':'observed','timestamp_iso':meta['window_end'],'expandable':True} for i in (1,2)]
            record(run,{'tweets':rows},1,0)
            meta=json.loads((run/'metadata.json').read_text());meta['coverage']='boundary_observed';write(run/'metadata.json',meta)
            write(run/'analysis.json',[{'tweet_id':r['tweet_id'],'category':'other','subcategory':'test','tickers':[],'sentiment':'neutral','key_thesis':'observed','is_actionable':False,'confidence':'low','is_thread_continuation':False,'thread_root_id':None} for r in rows])
            receipt=finish(run)
            self.assertEqual((receipt['tweet_count'],receipt['coverage']),(2,'partial'))
            meta=json.loads((run/'metadata.json').read_text())
            self.assertEqual((meta['window_coverage'],meta['budget_overshoot'],meta['unexpanded_posts']),('partial',1,2))

    def test_boundary_evidence_and_empty_is_partial(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
            start=iso(json.loads((run/'metadata.json').read_text())['window_start'])
            for i in range(3):
                result=record(run,{'sorting':'chronological','tweets':[{'tweet_id':str(i+1),'timestamp_iso':(start-timedelta(hours=i+1)).isoformat()}]},i*4,0)
            self.assertEqual(result['stop'],'boundary_observed')
            self.assertEqual(json.loads((run/'metadata.json').read_text())['coverage'],'boundary_observed')
            other=Path(initialize({'lists':{}},['https://x.com/i/lists/2'],d)[0]['run_dir'])
            for i in range(5):result=record(other,{'tweets':[]},i*4,0)
            self.assertEqual(result['stop'],'exhausted_observed')
            self.assertEqual(json.loads((other/'metadata.json').read_text())['coverage'],'partial')

    def test_finish_boundary_and_content_completeness(self):
        with tempfile.TemporaryDirectory() as d:
            for index,(expandable,failures,expected) in enumerate([(False,0,'boundary_observed'),(True,0,'partial'),(False,1,'partial')]):
                run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
                meta=json.loads((run/'metadata.json').read_text());meta['thread_failures']=failures;write(run/'metadata.json',meta)
                row={'tweet_id':str(10+index),'author_handle':'alice','text':'observed','timestamp_iso':meta['window_end'],'expandable':expandable}
                record(run,{'sorting':'chronological','tweets':[row]},0,0)
                start=iso(meta['window_start'])
                for i in range(3):record(run,{'sorting':'chronological','tweets':[{'tweet_id':str(i+1),'timestamp_iso':(start-timedelta(hours=i+1)).isoformat()}]},4+i*4,0)
                write(run/'analysis.json',[{'tweet_id':row['tweet_id'],'category':'other','subcategory':'test','tickers':[],'sentiment':'neutral','key_thesis':'observed','is_actionable':False,'confidence':'low','is_thread_continuation':False,'thread_root_id':None}])
                self.assertEqual(finish(run)['coverage'],expected)
                self.assertEqual(json.loads((run/'metadata.json').read_text())['window_coverage'],'boundary_observed')

    def test_unknown_sort_and_repeated_old_posts_do_not_complete(self):
        with tempfile.TemporaryDirectory() as d:
            for sorting in ['unknown','chronological']:
                run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
                start=iso(json.loads((run/'metadata.json').read_text())['window_start'])
                for i in range(3 if sorting=='unknown' else 4):
                    result=record(run,{'sorting':sorting,'tweets':[{'tweet_id':'1' if sorting=='chronological' else str(i+1),'timestamp_iso':(start-timedelta(hours=i+1)).isoformat()}]},i*4,0)
                    self.assertEqual(result['stop'],'window_boundary_unverified' if sorting=='unknown' and i==2 else None)
                self.assertEqual(json.loads((run/'metadata.json').read_text())['coverage'],'partial')

    def test_unknown_boundary_counter_resets_on_in_window_and_detail_does_not_advance(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
            meta=json.loads((run/'metadata.json').read_text());start=iso(meta['window_start'])
            def old(i):return {'tweet_id':str(i),'timestamp_iso':(start-timedelta(hours=i)).isoformat()}
            record(run,{'tweets':[old(1)]},1,0)
            record(run,{'kind':'detail','tweets':[old(2)]},2,0)
            self.assertEqual(json.loads((run/'metadata.json').read_text())['observed_old_batches'],1)
            record(run,{'tweets':[{'tweet_id':'3','timestamp_iso':meta['window_end']}]},3,0)
            self.assertEqual(json.loads((run/'metadata.json').read_text())['observed_old_batches'],0)
            for i in (4,5,6):result=record(run,{'tweets':[old(i)]},i,0)
            self.assertEqual(result['stop'],'window_boundary_unverified')

    def test_timeout_and_steps_are_partial(self):
        with tempfile.TemporaryDirectory() as d:
            for elapsed,steps,reason in [(2700,0,'timeout'),(1,299,'max_steps')]:
                run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
                meta=json.loads((run/'metadata.json').read_text());meta['steps']=steps;write(run/'metadata.json',meta)
                self.assertEqual(record(run,{'kind':'detail','tweets':[]},elapsed,0)['stop'],reason)
                self.assertEqual(json.loads((run/'metadata.json').read_text())['coverage'],'partial')

    def test_detail_reads_do_not_exhaust_list(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
            for i in range(6):self.assertIsNone(record(run,{'status':'ok','kind':'detail','tweets':[]},1+i*3,3)['stop'])

    def test_bundle_unique_keywords_and_multiple_lists(self):
        with tempfile.TemporaryDirectory() as d:
            runs=[]
            for i in [1,2]:
                run=Path(initialize({'lists':{}},[f'https://x.com/i/lists/{i}'],d)[0]['run_dir'])
                report=run/'report.md';report.write_text(f'# List {i}\n')
                write(run/'receipt.json',{'report_path':str(report)})
                write(run/'enriched.json',[])
                runs.append(run)
            for words in [[],['Low information'],['one','two'],['a'*20+'x','a'*20+'y']]:
                result=bundle(runs,words,Path(d)/'daily.md')
                self.assertEqual(len(set(result['keywords'])),3)
                self.assertEqual(len(result['sources']),2)
            self.assertEqual(len(bundle([runs[0],runs[0]],[],Path(d)/'daily.md')['sources']),1)

    def test_collector_budget_and_terminal_state(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d,maximum=1)[0]['run_dir'])
            post={'tweet_id':'1','timestamp_iso':json.loads((run/'metadata.json').read_text())['window_end']}
            self.assertEqual(record(run,{'status':'ok','tweets':[post]},1,0)['stop'],'max_tweets')
            with self.assertRaises(ValueError):record(run,{'status':'ok','tweets':[]},2,1)

    def test_repeat_limit_and_empty_batches(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
            self.assertIsNone(record(run,{'status':'rate_limited'},1,0)['stop'])
            self.assertEqual(record(run,{'status':'rate_limited'},121,120)['stop'],'rate_limited')

    def test_expansion_updates_snapshot_and_errors_not_exhaustion(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
            post={'tweet_id':'1','timestamp_iso':json.loads((run/'metadata.json').read_text())['window_end'],'text':'short','engagement':{'likes':None}}
            record(run,{'status':'ok','tweets':[post]},1,0)
            record(run,{'status':'ok','tweets':[{**post,'text':'complete expanded text','engagement':{'likes':3}}]},4,3)
            row=json.loads((run/'raw.jsonl').read_text())
            self.assertEqual((row['text'],row['engagement']['likes']),('complete expanded text',3))
            for i in range(3):record(run,{'status':'ok','tweets':[]},7+i*3,3)
            self.assertIsNone(record(run,{'status':'rate_limited'},20,3)['stop'])

    def test_verified_publish_and_resume(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);report=run/'report.md';report.write_text('# Daily digest\n\nCoverage：partial\n')
            write(run/'receipt.json',{'report_path':str(report),'digest_id':1})
            write(run/'metadata.json',{'data_dir':d,'run_id':'r1'})
            url='https://my.feishu.cn/docx/test'
            write(run/'publish-state.json',{'document_id':'test','doc_url':url,'content_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),'pending':'readback'})
            with sqlite3.connect(run/'digest.db') as db:
                db.execute('CREATE TABLE digests(id INTEGER PRIMARY KEY,metadata TEXT,feishu_doc_url TEXT)')
                db.execute('INSERT INTO digests VALUES(1,?,NULL)',(json.dumps({'run_id':'r1'}),))
            fetched=run/'fetched.md';fetched.write_text('# Daily digest\n')
            with self.assertRaises(ValueError):finalize(run,'test',url,fetched)
            fetched.write_text(report.read_text())
            report.write_text(report.read_text()+'\nFull Feishu report：'+url+'\n')
            self.assertEqual(finalize(run,'test',url,fetched)['feishu_doc_url'],url)
            self.assertEqual(finalize(run,'test',url,fetched)['feishu_doc_url'],url)
            with sqlite3.connect(run/'digest.db') as db:self.assertEqual(db.execute('SELECT feishu_doc_url FROM digests').fetchone()[0],url)
