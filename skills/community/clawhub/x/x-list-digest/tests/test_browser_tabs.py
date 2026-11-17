import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from browser_tabs import OwnedTabs


class Browser:
    def __init__(self):
        self.tabs={'user':'https://x.com/i/lists/1'};self.closed=[];self.n=0
    def list_tabs(self):
        return [{'targetId':key,'url':url} for key,url in self.tabs.items()]
    def new_tab(self,url):
        self.n+=1;self.current=str(self.n);self.tabs[self.current]=url;return self.current
    def goto_url(self,url):self.tabs[self.current]=url
    def close_tab(self,key):self.closed.append(key);del self.tabs[key]


class OwnedTabsTest(unittest.TestCase):
    def test_terminal_closes_only_owned_and_pause_preserves_list(self):
        for pause in (False,True):
            with tempfile.TemporaryDirectory() as root:
                run=Path(root)/'run';run.mkdir();browser=Browser();owner=OwnedTabs(run,browser)
                listing=owner.create('list','https://x.com/i/lists/1')
                detail=owner.create('detail','https://x.com/a/status/1')
                owner.finish('paused' if pause else 'finished',keep=listing if pause else None)
                self.assertIn('user',browser.tabs)
                self.assertNotIn(detail,browser.tabs)
                self.assertEqual(listing in browser.tabs,pause)

    def test_sweep_ignores_unknown_active_and_changed_url(self):
        with tempfile.TemporaryDirectory() as root:
            browser=Browser()
            for state in ('finished','active','paused'):
                run=Path(root)/state;run.mkdir();owner=OwnedTabs(run,browser)
                owner.create('list','https://x.com/i/lists/1');owner.state['state']=state;owner.save()
            changed=Path(root)/'changed';changed.mkdir();owner=OwnedTabs(changed,browser)
            target=owner.create('list','https://x.com/i/lists/1');browser.tabs[target]='https://example.com'
            owner.state['state']='failed';owner.save()
            current=Path(root)/'new';current.mkdir();OwnedTabs(current,browser).sweep()
            self.assertEqual(browser.closed,['1'])
            self.assertIn('user',browser.tabs)

    def test_close_failure_is_recorded_without_masking_collection(self):
        with tempfile.TemporaryDirectory() as root:
            browser=Browser();owner=OwnedTabs(root,browser);owner.create('list','https://x.com/i/lists/1')
            def fail(key):raise TimeoutError('test')
            browser.close_tab=fail
            owner.finish('failed')
            data=json.loads((Path(root)/'browser-tabs.json').read_text())
            self.assertEqual(data['cleanup_errors'][0]['error_type'],'TimeoutError')
            self.assertEqual(len(data['tabs']),1)

    def test_archived_budget_pause_is_swept(self):
        with tempfile.TemporaryDirectory() as root:
            browser=Browser();run=Path(root)/'old';run.mkdir();owner=OwnedTabs(run,browser)
            target=owner.create('list','https://x.com/i/lists/1');owner.finish('paused',keep=target)
            (run/'receipt.json').write_text('{}')
            current=Path(root)/'new';current.mkdir();OwnedTabs(current,browser).sweep()
            self.assertNotIn(target,browser.tabs)
