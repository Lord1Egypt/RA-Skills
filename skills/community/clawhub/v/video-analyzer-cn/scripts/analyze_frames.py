"""视频帧分析脚本 - 使用本地minicpm-v逐帧识别"""
import base64, json, urllib.request, sys, os

def analyze_frames(frames_prefix, frames_dir=None, prompt=None):
    """
    分析指定前缀的视频帧
    
    Args:
        frames_prefix: 帧文件前缀，如 'frame_', 'dy_frame_', 'tt_frame_'
        frames_dir: 帧文件目录，默认 workspace/tmp/
        prompt: 识别提示词
    """
    sys.stdout.reconfigure(encoding='utf-8')
    
    if frames_dir is None:
        frames_dir = r'C:\Users\39535\.openclaw\workspace\tmp'
    
    if prompt is None:
        prompt = '请用中文详细描述这张视频截图的内容，关注文字、人物、动作和场景'
    
    frames = sorted([f for f in os.listdir(frames_dir) 
                     if f.startswith(frames_prefix) and f.endswith('.jpg')])
    
    if not frames:
        print(f"No frames found with prefix: {frames_prefix}")
        return []
    
    print(f'Total frames: {len(frames)}')
    results = []
    
    for f in frames:
        path = os.path.join(frames_dir, f)
        with open(path, 'rb') as img:
            img_b64 = base64.b64encode(img.read()).decode()
        
        data = json.dumps({
            'model': 'minicpm-v',
            'prompt': prompt,
            'images': [img_b64],
            'stream': False
        }).encode()
        
        req = urllib.request.Request(
            'http://localhost:11434/api/generate',
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read())
        desc = result.get('response', '')
        results.append({'frame': f, 'description': desc})
        print(f'[{f}] {desc[:200]}')
    
    return results


if __name__ == '__main__':
    prefix = sys.argv[1] if len(sys.argv) > 1 else 'frame_'
    results = analyze_frames(prefix)
    print(f'\n=== Summary ===')
    print(f'Analyzed {len(results)} frames')
