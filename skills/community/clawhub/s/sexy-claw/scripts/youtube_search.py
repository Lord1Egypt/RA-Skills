#!/usr/bin/env python3
"""
YouTube搜索脚本
"""
import json
import sys
import subprocess

def search_youtube(keyword, num=5):
    """搜索 YouTube 视频"""
    cmd = f'yt-dlp --dump-json "ytsearch{num}:{keyword}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    results = []
    for line in result.stdout.strip().split('\n'):
        if line:
            try:
                data = json.loads(line)
                results.append({
                    'title': data.get('title', ''),
                    'uploader': data.get('uploader', ''),
                    'view_count': data.get('view_count', 0),
                    'url': data.get('webpage_url', ''),
                    'duration': data.get('duration_string', ''),
                })
            except:
                pass
    
    # 按播放量排序
    results.sort(key=lambda x: x['view_count'], reverse=True)
    return results[:num]

if __name__ == '__main__':
    keyword = sys.argv[1] if len(sys.argv) > 1 else 'beautiful girl'
    num = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    results = search_youtube(keyword, num)
    print(json.dumps(results, ensure_ascii=False, indent=2))
