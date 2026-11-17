"""Persist ownership of tabs explicitly created by the native browser helper."""
import json
from pathlib import Path
from common import write


class OwnedTabs:
    def __init__(self,directory,helpers):
        self.directory=Path(directory);self.helpers=helpers
        self.path=self.directory/'browser-tabs.json'
        self.state=json.loads(self.path.read_text()) if self.path.exists() else {
            'state':'active','tabs':{},'cleanup_errors':[]}

    def save(self):write(self.path,self.state)

    def create(self,role,url):
        # Passing about:blank forces native new_tab to create a new target;
        # passing a destination URL could reuse somebody else's blank tab.
        target=self.helpers.new_tab('about:blank')
        self.state['tabs'][target]={'role':role,'url':'about:blank'};self.save()
        self.helpers.goto_url(url)
        self.state['tabs'][target]['url']=url;self.save()
        return target

    def destination(self,target,url):
        self.helpers.goto_url(url)
        self.state['tabs'][target]['url']=url;self.save()

    def cleanup(self,keep=None):
        try:
            live={tab['targetId']:tab.get('url') for tab in self.helpers.list_tabs()}
            for target,entry in list(self.state['tabs'].items()):
                if target==keep:continue
                if target not in live:
                    del self.state['tabs'][target];continue
                # A changed destination may reflect user intervention. Leave it.
                if live[target]!=entry['url']:continue
                try:
                    self.helpers.close_tab(target);del self.state['tabs'][target]
                except Exception as error:
                    self.state['cleanup_errors'].append({'targetId':target,'error_type':type(error).__name__})
        except Exception as error:
            self.state['cleanup_errors'].append({'error_type':type(error).__name__})
        self.save()

    def finish(self,state,keep=None):
        self.state['state']=state;self.cleanup(keep)

    def sweep(self):
        # Only sibling runs of this list, with a terminal ownership record.
        # Old runs without ownership records, active runs and pauses are excluded.
        for path in self.directory.parent.glob('*/browser-tabs.json'):
            if path==self.path:continue
            try:
                prior=OwnedTabs(path.parent,self.helpers)
                if prior.state['state']=='paused' and (path.parent/'receipt.json').exists():
                    prior.finish('finished')
                elif prior.state['state'] in ('finished','failed'):prior.cleanup()
            except (ValueError,KeyError,OSError):continue
