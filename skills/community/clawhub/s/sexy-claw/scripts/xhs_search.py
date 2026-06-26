#!/usr/bin/env python3
"""
小红书搜索脚本
"""
import json
import sys
import subprocess

def search_xhs(keyword, num=10):
    """使用 xhs-cli 搜索"""
    cmd = f'source ~/.agent-reach-venv/bin/activate && xhs search "{keyword}" --sort popular --json'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        items = [i for i in data.get('data', {}).get('items', []) if i.get('model_type') == 'note']
        
        results = []
        for item in items[:num]:
            note = item.get('note_card', {})
            interact = note.get('interact_info', {})
            user = note.get('user', {})
            
            results.append({
                'title': note.get('display_title', ''),
                'nickname': user.get('nickname', ''),
                'likes': interact.get('liked_count', '0'),
                'comments': interact.get('comment_count', '0'),
                'note_id': item.get('id', ''),
                'link': f"https://www.xiaohongshu.com/explore/{item.get('id', '')}",
            })
        return results
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    keyword = sys.argv[1] if len(sys.argv) > 1 else '美女'
    num = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    results = search_xhs(keyword, num)
    print(json.dumps(results, ensure_ascii=False, indent=2))
