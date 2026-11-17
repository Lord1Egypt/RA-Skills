import json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run import initialize
from collector_record import record
from host_collector import collect


class IncrementalTests(unittest.TestCase):
    def fixture(self,root):
        run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],root)[0]['run_dir'])
        meta=json.loads((run/'metadata.json').read_text())
        previous=Path(root)/'runs/1/prior';previous.mkdir()
        (previous/'receipt.json').write_text('{}')
        (previous/'enriched.json').write_text(json.dumps([{'tweet_id':'1'}]))
        row={'tweet_id':'1','timestamp_iso':meta['window_end'],'text':'already archived','expandable':True,'url':'https://x.com/a/status/1','engagement':{'replies':3}}
        return run,row
    def test_archived_post_not_collected_or_expanded(self):
        with tempfile.TemporaryDirectory() as root:
            run,row=self.fixture(root);state={'time':0};navigation=[]
            def js(_):return {'status':'ok','logged_in':True,'viewport':{'x':1,'y':1},'tweets':[row]}
            def sleep(n):state['time']+=n
            result=collect(run,js,lambda *a,**k:None,navigation.append,clock=lambda:state['time'],sleep=sleep,choose=lambda a,b:a)
            self.assertEqual(navigation,[])
            self.assertEqual((run/'raw.jsonl').read_text(),'')
            self.assertEqual(result['stop'],'exhausted_observed')
            meta=json.loads((run/'metadata.json').read_text());self.assertEqual(meta['historical_skipped'],1)
            self.assertEqual(meta['thread_failures'],0)
    def test_history_only_batches_do_not_prematurely_stall(self):
        with tempfile.TemporaryDirectory() as root:
            run,row=self.fixture(root);previous=Path(root)/'runs/1/prior/enriched.json'
            previous.write_text(json.dumps([{'tweet_id':str(i)} for i in range(1,8)]))
            for i in range(1,7):
                result=record(run,{'status':'ok','tweets':[{**row,'tweet_id':str(i)}]},i,0)
                self.assertIsNone(result['stop'])
                self.assertEqual(result['new_posts'],0)
            result=record(run,{'status':'ok','tweets':[{**row,'tweet_id':'8'}]},7,0)
            self.assertEqual(result['new_posts'],1)
            self.assertEqual(json.loads((run/'raw.jsonl').read_text())['tweet_id'],'8')


if __name__=='__main__':unittest.main()
