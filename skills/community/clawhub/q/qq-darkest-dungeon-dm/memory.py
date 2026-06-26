# memory.py
import json
import sys
import os
from datetime import datetime

STATE_FILE = os.path.join(os.path.dirname(__file__), 'campaign.json')

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"story_summary": "跑团尚未开始，玩家正在酒馆集合。", "players": {}, "recent_logs":[]}
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def handle_command(args):
    cmd = args[0]
    state = load_state()
    
    if cmd == 'read':
        print(json.dumps(state, ensure_ascii=False, indent=2))
        
    elif cmd == 'reset':
        new_state = {"story_summary": "新战役开始。玩家在无冬城酒馆。", "players": {}, "recent_logs":[]}
        save_state(new_state)
        print("✅ 存档已重置，准备开始新团。")
        
    elif cmd == 'update_log':
        if len(args) < 2: return "缺少剧情摘要"
        log_entry = f"[{datetime.now().strftime('%m-%d %H:%M')}] {args[1]}"
        state['recent_logs'].append(log_entry)
        # 只保留最近 10 条日志防止文件过大
        if len(state['recent_logs']) > 10:
            state['recent_logs'].pop(0)
        # 更新剧情总纲
        if len(args) > 2:
            state['story_summary'] = args[2]
        save_state(state)
        print("✅ 剧情进度已存档。")
        
    elif cmd == 'update_player':
            # 用法: update_player <角色名> <属性: hp/stress/gold/status> <操作值>
            if len(args) < 4: return "参数不足"
            name, attr, val = args[1], args[2], args[3]
            
            if name not in state['players']:
                # 新手进村，初始 20血，0压力，活着
                state['players'][name] = {"hp": 20, "stress": 0, "status": "alive", "inventory":[]}
                
            if attr in ['hp', 'stress']:
                state['players'][name][attr] = int(val)
                # 如果血量降到 0
                if attr == 'hp' and int(val) <= 0:
                    state['players'][name]['status'] = "DEAD"
                    print(f"💀 警告：玩家 {name} 已经死亡！")
            elif attr == 'status':
                state['players'][name]['status'] = val
                
            save_state(state)
            print(f"✅ 玩家 {name} 的 {attr} 已更新为 {val}。")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python memory.py <read|reset|update_log|update_player> [参数]")
        sys.exit(1)
    handle_command(sys.argv[1:])