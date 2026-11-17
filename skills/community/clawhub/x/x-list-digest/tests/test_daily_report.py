import json,sys,tempfile,unittest,hashlib,sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from daily_report import merge,ranked,render_daily,render_weekly
from daily_publish_record import finalize
from daily_bundle import bundle
from unittest.mock import patch


class DailyReportTest(unittest.TestCase):
    def test_sunday_bundle_adds_weekly_without_flag(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);run=root/'runs'/'1'/'a';run.mkdir(parents=True)
            meta={'window_end':'2026-10-10T18:00:00Z','timezone':'Asia/Bangkok','coverage':'partial','data_dir':str(root),'run_id':'a','list_url':'https://x.com/i/lists/1'}
            report=run/'report.md';report.write_text('source')
            (run/'metadata.json').write_text(json.dumps(meta));(run/'receipt.json').write_text(json.dumps({'report_path':str(report)}));(run/'enriched.json').write_text('[]')
            state=bundle([run],[],root/'daily.md')
            self.assertTrue(state['weekly_required']);self.assertTrue(state['weekly_included'])
            self.assertIn('Weekly off-topic statistics',(root/'daily.md').read_text());self.assertIn('Insufficient samples',(root/'daily.md').read_text())
    def test_sunday_missing_weekly_rejected_before_write(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);body=root/'daily.md';body.write_text('daily')
            manifest=root/'daily.json';manifest.write_text(json.dumps({'date':'2026-10-11','document_id':'abc','doc_url':'https://my.feishu.cn/docx/abc','report_path':str(body)}))
            before=manifest.read_bytes()
            with self.assertRaisesRegex(ValueError,'Sunday archive'):finalize(manifest,body)
            self.assertEqual(before,manifest.read_bytes())
    def source(self,root,name,rows,end='2026-10-10T10:00:00Z'):
        p=Path(root)/name;p.mkdir()
        meta={'window_start':'2026-10-09T10:00:00Z','window_end':end,'timezone':'Asia/Bangkok','coverage':'partial','list_name':'test','list_url':'https://x.com/i/lists/1'}
        (p/'metadata.json').write_text(json.dumps(meta));(p/'receipt.json').write_text('{}');(p/'enriched.json').write_text(json.dumps(rows));return p
    def row(self,ident='1',author='alice',likes=10):
        return {'tweet_id':ident,'author_handle':author,'timestamp_iso':'2026-10-10T09:00:00Z','text':'observed','expandable':False,'engagement':{'likes':likes,'replies':2,'reposts':1},'category':'crypto','subcategory':'market','tickers':['BTC'],'sentiment':'bullish','key_thesis':'Thesis','url':f'https://x.com/{author}/status/{ident}'}
    def test_merge_deduplicates_and_preserves_known_counts_and_longer_text(self):
        with tempfile.TemporaryDirectory() as d:
            old=self.row();old['text']='longer observed text'
            new=self.row(likes=None);new['key_thesis']='new analysis'
            rows,sources=merge([self.source(d,'old',[old]),self.source(d,'new',[new],end='2026-10-10T11:00:00Z')])
            self.assertEqual(len(rows),1);self.assertEqual(rows[0]['engagement']['likes'],10)
            self.assertEqual(rows[0]['text'],old['text']);self.assertEqual(rows[0]['key_thesis'],'new analysis')
    def test_daily_tables_no_daily_offtopic_or_raw_metadata(self):
        rows=[self.row(str(i),likes=i) for i in range(7)]
        unknown=self.row('8',likes=None);rows.append(unknown)
        sources=[{'metadata':{'coverage':'partial','list_url':'https://x.com/i/lists/1','timezone':'Asia/Bangkok','window_end':'2026-10-10T10:00:00Z'}}]
        top=ranked(rows);self.assertEqual([r['tweet_id'] for r in top],['6','5','4','3','2'])
        body=render_daily(rows,sources,'2026-10-10',{r['tweet_id']:{'topic':'Topic','writing_direction':'Writing angle'} for r in top})
        for forbidden in ['## Individual post details','## Metadata','## Off-topic statistics']:self.assertNotIn(forbidden,body)
        self.assertIn('| BTC | 8 | 1 |',body);self.assertIn('Writing angle',body)
        self.assertIn('Insufficient samples',render_weekly(rows,sources))
    def test_publish_prechecks_all_sources_before_any_write(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);dbpath=root/'digest.db'
            with sqlite3.connect(dbpath) as db:
                db.execute('CREATE TABLE digests(id INTEGER,metadata TEXT,feishu_doc_url TEXT)')
                for i in (1,2):db.execute('INSERT INTO digests VALUES(?,?,NULL)',(i,json.dumps({'run_id':str(i)})))
            body=root/'daily.md';body.write_text('daily /status/1\n');sources=[]
            for i in (1,2):
                p=root/str(i);p.mkdir();report=p/'report.md';report.write_text('source')
                (p/'metadata.json').write_text(json.dumps({'run_id':str(i),'data_dir':str(root)}))
                (p/'receipt.json').write_text(json.dumps({'report_path':str(report),'digest_id':i}))
                sources.append({'run_dir':str(p),'run_id':str(i),'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest() if i==1 else 'invalid'})
            manifest=root/'daily.json';manifest.write_text(json.dumps({'date':'2026-10-10','report_path':str(body),'content_sha256':hashlib.sha256(body.read_bytes()).hexdigest(),'tweet_ids':['1'],'document_id':'abc','doc_url':'https://my.feishu.cn/docx/abc','sources':sources}))
            before=(root/'1/receipt.json').read_bytes()
            with self.assertRaisesRegex(ValueError,'source report changed'):finalize(manifest,body)
            self.assertEqual(before,(root/'1/receipt.json').read_bytes())
            with sqlite3.connect(dbpath) as db:self.assertEqual(db.execute('SELECT feishu_doc_url FROM digests WHERE id=1').fetchone(),(None,))
