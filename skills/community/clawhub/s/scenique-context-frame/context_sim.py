#!/usr/bin/env python3
# Simple simulation of ContextFrame skill (MVP)
from collections import deque

def detect_topic(prev_summary, message):
    # naive keyword overlap heuristic for demo
    prev_words=set(prev_summary.lower().split())
    words=set(message.lower().split())
    overlap=len(prev_words & words)
    if overlap<2:
        return True
    return False

class ContextManager:
    def __init__(self):
        self.frames=[]
        self.current=None
    def new_frame(self,title,seed):
        frame={'id':len(self.frames)+1,'title':title,'summary':seed,'history':[]}
        self.frames.append(frame)
        self.current=frame
        return frame
    def snapshot_current(self):
        if not self.current: return
        self.current['summary']=(' '.join(self.current['history'])[:200])
    def switch_if_needed(self,message):
        if not self.current:
            f=self.new_frame('general',message)
            f['history'].append(message)
            return ('created', f)
        if detect_topic(self.current['summary'] or '',message):
            # create new frame from first few words as title
            title=' '.join(message.split()[:4])
            f=self.new_frame(title,message)
            f['history'].append(message)
            # mark previous frame pending for consolidation
            try:
                import json
                pending_path = '/root/.openclaw/workspace/context_frames_pending.json'
                prev = self.frames[-2] if len(self.frames)>=2 else None
                if prev:
                    entry = {'frame_id': prev['id'], 'title': prev['title'], 'summary': ' '.join(prev['history'])[:400]}
                    try:
                        with open(pending_path,'r') as pf:
                            data=json.load(pf)
                    except Exception:
                        data=[]
                    data.append(entry)
                    with open(pending_path,'w') as pf:
                        json.dump(data,pf)
            except Exception:
                pass
            return ('switched',f)
        else:
            self.current['history'].append(message)
            return ('appended',self.current)

if __name__=='__main__':
    cm=ContextManager()
    # simulated conversation
    convo=[
        'Let us discuss the FET position and whether to trim at 0.16',
        'I think we should consider Kelly sizing and capital buffer',
        'Now a different topic: setup the nyx cbt module integration',
        'How should Nyx prompt the user for mood? 0-10 scale?',
        'Back to FET: what if Nvidia rumors are false? 0.144 support?',
        'Switch: planning the release schedule for scenique-prevision skill',
        'Final: schedule consolidation and memory snapshot now'
    ]
    for i,m in enumerate(convo,1):
        res=cm.switch_if_needed(m)
        if res[0]=='switched':
            print(f"[{i}] MESSAGE: {m}\n    --> TOPIC SWITCHED -> new frame id={res[1]['id']} title='{res[1]['title']}'\n")
        else:
            f=res[1]
            print(f"[{i}] MESSAGE: {m}\n    --> Appended to frame id={f['id']} title='{f['title']}'\n")
    print('\n-- FRAMES SUMMARY --')
    for f in cm.frames:
        cm.current=f
        cm.snapshot_current()
        print(f"Frame {f['id']}: title='{f['title']}' summary='{f['summary'][:80]}...' history_count={len(f['history'])}")
