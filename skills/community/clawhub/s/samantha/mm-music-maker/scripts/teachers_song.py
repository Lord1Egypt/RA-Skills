"""
MiniMax Music Generation for Teachers - Li Jian Style
Warm, poetic, folk-pop, grateful
"""
import http.client
import json
import ssl
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.json"
OUTPUT_PATH = Path(__file__).parent / "output" / "teachers_warm_song.mp3"

def load_config():
    with open(CONFIG_PATH, encoding='utf-8') as f:
        return json.load(f)

# 李健风格温暖感恩歌词
LYRICS = """[Verse 1]
春风不急不缓
恰好落在今天
你们走进这个直播间
像一束安静的光

[Verse 2]
窗外有云在走
杯中有茶正暖
你们说的每一句话
都在心里生了根

[Pre-Chorus]
我听过很多道理
却忘了怎么去感受
直到今天 你们在
像一面干净的镜子

[Chorus]
谢谢你们来过
谢谢你们在
这短暂的三小时
种下了一整年的春天
谢谢你们温柔
谢谢你们耐心地等
等一颗种子
慢慢发芽

[Verse 3]
时间会往前走
但有些画面会留下来
你们笑着的样子
是我想成为的人

[Bridge]
也许某天我也会
在另一个春天
把这份温暖
递给下一个人

[Chorus]
谢谢你们来过
谢谢你们在
这短暂的三小时
种下了一整年的春天
谢谢你们温柔
谢谢你们耐心地等
等一颗种子
慢慢发芽

[Outro]
风吹过的时候
我想起今天
想起你们的声音
像水一样清澈
愿你们也被温柔以待
在这个春天
以及以后的每一个春天"""

# 李健风格提示词 - 温暖民谣 + 诗意流行
PROMPT = "Li Jian style, Chinese folk pop, warm acoustic guitar, gentle piano, nostalgic, poetic, spring breeze, gratitude, heartfelt ballad, female vocal, tender melody, Wang Feng style, Chinese singer-songwriter, clean arrangement, intimate, emotional warmth"

def generate_music():
    config = load_config()
    api_key = config.get('api_key')

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    conn = http.client.HTTPSConnection('api.minimaxi.com', 443, timeout=600, context=ctx)

    data = json.dumps({
        'model': 'music-2.5+',
        'lyrics': LYRICS,
        'prompt': PROMPT
    })

    print("Generating warm song for teachers...")
    print("Style: Li Jian + Chinese folk pop + gratitude")
    print("-" * 50)

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

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

        with open(OUTPUT_path := OUTPUT_PATH, 'wb') as f:
            f.write(audio_bytes)

        print(f"[OK] Generated: {OUTPUT_PATH}")
        print(f"File size: {len(audio_bytes) / 1024 / 1024:.2f} MB")
        return OUTPUT_PATH
    else:
        print(f"[Error] Generation failed: {result}")
        return None

    conn.close()

if __name__ == "__main__":
    result = generate_music()
    if result:
        print(f"\nSong saved: {result}")
