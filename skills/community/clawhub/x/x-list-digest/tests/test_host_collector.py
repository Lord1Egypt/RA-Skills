import json
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run import initialize
from host_collector import collect,run_native,authorize_resume


class HostCollectorTest(unittest.TestCase):
    def test_cleanup_save_error_does_not_mask_browser_exception(self):
        from test_browser_tabs import Browser
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
            browser=Browser();browser.wait_for_load=lambda:None;browser.switch_tab=lambda key,activate=False:None
            browser.js=lambda _:None;browser.scroll=lambda *a,**k:None
            def fail(*args,**kwargs):raise TimeoutError('original')
            with patch.dict(sys.modules,{'browser_harness':SimpleNamespace(helpers=browser)}),patch('host_collector.collect',fail),patch('host_collector.OwnedTabs.finish',side_effect=OSError('cleanup')):
                with self.assertRaisesRegex(TimeoutError,'original'):run_native(run)
            meta=json.loads((run/'metadata.json').read_text())
            self.assertEqual(meta['stop_reason'],'browser_exception')
            self.assertEqual(meta['coverage'],'partial')
            self.assertTrue((run/'browser-error.json').exists())

    def test_native_budget_pause_keeps_owned_list_for_resume(self):
        from test_browser_tabs import Browser
        for reason in ('invocation_budget','max_steps','max_tweets','timeout'):
            with tempfile.TemporaryDirectory() as d:
                run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
                browser=Browser()
                browser.wait_for_load=lambda:None
                browser.switch_tab=lambda key,activate=False:setattr(browser,'current',key)
                browser.current_tab=lambda:{'targetId':browser.current,'url':browser.tabs[browser.current]}
                browser.js=lambda _:None;browser.scroll=lambda *a,**k:None
                def stop(*args,**kwargs):
                    meta=json.loads((run/'metadata.json').read_text())
                    meta.update(collector_stopped=True,stop_reason=reason,steps=1)
                    (run/'metadata.json').write_text(json.dumps(meta))
                    return {'stop':reason}
                with patch.dict(sys.modules,{'browser_harness':SimpleNamespace(helpers=browser)}),patch('host_collector.collect',stop):
                    run_native(run)
                    target=browser.current
                    self.assertEqual(json.loads((run/'browser-tabs.json').read_text())['state'],'paused')
                    run_native(run,resume=True)
                    self.assertEqual(browser.current,target)
                    self.assertEqual(browser.n,1)

    def test_detail_budget_stop_returns_to_list_and_segment_is_audited(self):
        for segment in (False,True):
            with tempfile.TemporaryDirectory() as d:
                run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
                meta=json.loads((run/'metadata.json').read_text())
                if not segment:meta['collector_limits']['max_steps']=2
                (run/'metadata.json').write_text(json.dumps(meta))
                state={'time':0,'calls':0,'navigation':[]}
                row={'tweet_id':'1','timestamp_iso':meta['window_end'],'text':'short','expandable':True,'url':'https://x.com/a/status/1'}
                def js(expr):
                    state['calls']+=1
                    if segment:state['time']=1498 if state['calls']==1 else 1501
                    return {'status':'ok','logged_in':True,'viewport':{'x':400,'y':300},'tweets':[row]}
                def sleep(n):state['time']+=n
                result=collect(run,js,lambda *a,**k:None,state['navigation'].append,clock=lambda:state['time'],sleep=sleep)
                self.assertEqual(state['navigation'],[row['url'],None])
                self.assertEqual(result['stop'],'invocation_budget' if segment else 'max_steps')
                if segment:self.assertTrue((run/'invocation-pause-0002.json').exists())

    def test_resume_keeps_window_events_and_elapsed(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
            meta=json.loads((run/'metadata.json').read_text());window=meta['window_end']
            meta.update(steps=50,collector_stopped=True,stop_reason='max_steps',elapsed_seconds=106)
            (run/'metadata.json').write_text(json.dumps(meta))
            (run/'raw.jsonl').write_text(json.dumps({'tweet_id':'1','timestamp_iso':window,'text':'keep'})+'\n')
            (run/'collector-events.jsonl').write_text(json.dumps({'elapsed_seconds':106,'empty_batches':0,'old_batches':0,'status':'ok','stop':'max_steps'})+'\n')
            resumed=authorize_resume(run)
            self.assertEqual(resumed['window_end'],window)
            self.assertEqual(resumed['steps'],50)
            state={'time':0}
            def sleep(n):state['time']+=n
            collect(run,lambda _: {'status':'ok','logged_in':True,'viewport':{'x':400,'y':300},'tweets':[]},lambda *a,**k:None,lambda _:None,resume=True,clock=lambda:state['time'],sleep=sleep,choose=lambda a,b:a)
            saved=json.loads((run/'metadata.json').read_text())
            self.assertEqual(saved['steps'],55)
            self.assertEqual(saved['elapsed_seconds'],110)
            self.assertIn('keep',(run/'raw.jsonl').read_text())
            self.assertTrue((run/'resume-0001.json').exists())

    def test_resume_rejects_security_stop(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
            meta=json.loads((run/'metadata.json').read_text());meta.update(collector_stopped=True,stop_reason='captcha')
            (run/'metadata.json').write_text(json.dumps(meta))
            with self.assertRaises(ValueError):authorize_resume(run)

    def test_native_detail_uses_another_tab_without_navigating_list(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
            state={'tab':None,'urls':{},'positions':{},'n':0}
            def new_tab(url='about:blank'):
                state['n']+=1;tab=str(state['n']);state['tab']=tab
                state['urls'][tab]=url;state['positions'][tab]=0;return tab
            def goto(url):state['urls'][state['tab']]=url;state['positions'][state['tab']]=0
            def switch(tab,activate=False):
                self.assertTrue(activate)
                state['tab']=tab
            helpers=SimpleNamespace(new_tab=new_tab,wait_for_load=lambda:None,goto_url=goto,switch_tab=switch,js=lambda _:None,scroll=lambda *a,**k:None,
                                    list_tabs=lambda:[{'targetId':key,'url':url} for key,url in state['urls'].items()],close_tab=lambda key:state['urls'].pop(key))
            def fake_collect(directory,js,scroll,navigate,**kwargs):
                list_tab=state['tab'];state['positions'][list_tab]=4200
                navigate('https://x.com/a/status/1')
                self.assertNotEqual(state['tab'],list_tab)
                navigate(None)
                self.assertEqual(state['tab'],list_tab)
                self.assertEqual(state['positions'][list_tab],4200)
                self.assertEqual(state['urls'][list_tab],'https://x.com/i/lists/1')
                return {'stop':'test'}
            with patch.dict(sys.modules,{'browser_harness':SimpleNamespace(helpers=helpers)}),patch('host_collector.collect',fake_collect):
                self.assertEqual(run_native(run),{'stop':'test'})

    def test_detail_rate_limit_wait_is_not_lost(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d)[0]['run_dir'])
            meta=json.loads((run/'metadata.json').read_text());state={'time':0,'calls':0,'wheel':0}
            def js(expr):
                state['calls']+=1
                if state['calls']>1:return {'status':'rate_limited','tweets':[]}
                return {'status':'ok','logged_in':True,'viewport':{'x':400,'y':300},'tweets':[{'tweet_id':'1','timestamp_iso':meta['window_end'],'text':'short','expandable':True,'url':'https://x.com/a/status/1'}]}
            def sleep(n):state['time']+=n
            def wheel(*a,**k):state['wheel']+=1
            result=collect(run,js,wheel,lambda _:None,clock=lambda:state['time'],sleep=sleep)
            self.assertEqual(result['stop'],'rate_limited')
            self.assertEqual(state['time'],121)
            self.assertEqual(state['wheel'],0)

    def test_native_wheel_and_real_pause_are_recorded_until_stop(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d,maximum=3,expand_threads=False)[0]['run_dir'])
            meta=json.loads((run/'metadata.json').read_text())
            state={'time':0,'page':1,'wheel':[]}
            def js(expr):
                return {'status':'ok','logged_in':True,'sorting':'unknown','viewport':{'x':500,'y':400},'tweets':[{'tweet_id':str(state['page']),'timestamp_iso':meta['window_end'],'text':'real','author_handle':'a','url':'https://x.com/a/status/'+str(state['page']),'expandable':False}]}
            def wheel(x,y,dy):
                state['wheel'].append(dy);state['page']+=1
            def sleep(seconds):state['time']+=seconds
            result=collect(run,js,wheel,lambda _:None,clock=lambda:state['time'],sleep=sleep,choose=lambda a,b:a)
            self.assertEqual(result['stop'],'max_tweets')
            self.assertEqual(state['wheel'],[600,600])
            events=[json.loads(x) for x in (run/'collector-events.jsonl').read_text().splitlines()]
            self.assertEqual([x['elapsed_seconds'] for x in events],[0,1,2])
            self.assertEqual([x['pause_seconds'] for x in events],[0,1,1])
            with self.assertRaises(ValueError):collect(run,js,wheel,lambda _:None)

    def test_repeated_pages_stop_without_claiming_boundary(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d,expand_threads=False)[0]['run_dir'])
            state={'time':0}
            def sleep(n):state['time']+=n
            result=collect(run,lambda _: {'status':'ok','logged_in':True,'sorting':'unknown','viewport':{'x':400,'y':300},'tweets':[]},lambda *a,**k:None,lambda _:None,clock=lambda:state['time'],sleep=sleep,choose=lambda a,b:a)
            self.assertEqual(result['stop'],'exhausted_observed')
            self.assertEqual(json.loads((run/'metadata.json').read_text())['coverage'],'partial')

    def test_no_new_posts_above_bottom_is_pagination_stalled(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(initialize({'lists':{}},['https://x.com/i/lists/1'],d,expand_threads=False)[0]['run_dir'])
            state={'time':0}
            def sleep(n):state['time']+=n
            snapshot={'status':'ok','logged_in':True,'viewport':{'x':400,'y':300},'scroll_position':{'y':0,'height':6000,'viewport_height':800},'tweets':[]}
            result=collect(run,lambda _:snapshot.copy(),lambda *a,**k:None,lambda _:None,clock=lambda:state['time'],sleep=sleep,choose=lambda a,b:a)
            self.assertEqual(result['stop'],'pagination_stalled')
            self.assertEqual(json.loads((run/'metadata.json').read_text())['coverage'],'partial')
