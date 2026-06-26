"""
MiniMax Music Generation Script
用于生成 AI 歌曲
"""
import http.client
import json
import ssl
import os
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.json"

def load_config():
    with open(CONFIG_PATH, encoding='utf-8') as f:
        return json.load(f)

def generate_music(lyrics, prompt, output_path):
    config = load_config()
    api_key = config.get('api_key')
    
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    conn = http.client.HTTPSConnection('api.minimaxi.com', 443, timeout=600, context=ctx)
    
    data = json.dumps({
        'model': 'music-2.5+',
        'lyrics': lyrics,
        'prompt': prompt
    })
    
    print(f"正在生成音乐...")
    print(f"歌词: {lyrics[:50]}...")
    print(f"风格: {prompt}")
    
    conn.request('POST', '/v1/music_generation', body=data, headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    })
    
    resp = conn.getresponse()
    body = resp.read()
    result = json.loads(body)
    
    if 'data' in result and 'audio' in result.get('data', {}):
        audio_hex = result['data']['audio']
        audio_bytes = bytes.fromhex(audio_hex)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(audio_bytes)
        
        print(f"[OK] 已生成: {output_path}")
        print(f"文件大小: {len(audio_bytes) / 1024 / 1024:.2f} MB")
        return output_path
    else:
        print(f"[错误] 生成失败: {result}")
        return None
    
    conn.close()

if __name__ == "__main__":
    # 默认参数
    lyrics = """[Verse 1]
星光洒落在窗前
夜深人静的时刻
我想起你的声音

[Chorus]
You are the one I never needed
穿越时间和空间
你在我身边"""

    prompt = "soft pop, emotional, melodic, piano, female vocals, heartfelt, ballad"
    output = str(Path(__file__).parent / "output" / "samantha_song.mp3")
    
    if len(sys.argv) > 1:
        output = sys.argv[1]
    
    generate_music(lyrics, prompt, output)
