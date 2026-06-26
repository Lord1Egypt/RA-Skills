#!/usr/bin/env python3
"""
千问 TTS 语音生成并发送到飞书
- 默认音色: Nofish
- 末尾自动加1.5秒空白，防止语音被截断
用法: python3 speak_and_send.py "要说话的文本" [音色]
"""
import sys
import os
import json
import requests
import subprocess
import tempfile

# 飞书配置（从环境变量读取，用户必须自行配置）
FEISHU_APP_ID = os.environ.get('FEISHU_APP_ID', '')
FEISHU_APP_SECRET = os.environ.get('FEISHU_APP_SECRET', '')
FEISHU_USER_ID = os.environ.get('FEISHU_USER_ID', '')

if not FEISHU_APP_ID or not FEISHU_APP_SECRET or not FEISHU_USER_ID:
    raise ValueError("需要配置环境变量: FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_USER_ID")


def get_feishu_token():
    resp = requests.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        json={'app_id': FEISHU_APP_ID, 'app_secret': FEISHU_APP_SECRET}
    )
    return resp.json().get('tenant_access_token')


def generate_qwen_audio(text, voice="Nofish"):
    api_key = os.environ.get('DASHSCOPE_API_KEY', '')
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY not set")

    resp = requests.post(
        'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'qwen3-tts-flash',
            'input': {
                'text': text,
                'voice': voice,
                'language_type': 'Chinese'
            }
        }
    )
    data = resp.json()
    audio_url = (
        data.get('data', {}).get('audio', {}).get('url') or
        data.get('audio', {}).get('url') or
        data.get('output', {}).get('audio', {}).get('url')
    )
    if not audio_url:
        raise ValueError(f"Failed to get audio URL: {data}")
    return audio_url


def download_wav(url):
    resp = requests.get(url)
    fd, wav_path = tempfile.mkstemp(suffix='.wav')
    os.write(fd, resp.content)
    os.close(fd)
    return wav_path


def add_silence_and_convert(wav_path):
    """给音频末尾加1秒空白，转换为ogg"""
    silence_path = tempfile.mktemp(suffix='.wav')
    # 生成1秒静音
    subprocess.run([
        'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono', '-t', '1.5',
        silence_path, '-y'
    ], capture_output=True)

    # 拼接原音频 + 静音
    concat_list = tempfile.mktemp(suffix='.txt')
    with open(concat_list, 'w') as f:
        f.write(f"file '{wav_path}'\n")
        f.write(f"file '{silence_path}'\n")

    ogg_path = tempfile.mktemp(suffix='.ogg')
    subprocess.run([
        'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_list,
        '-c:a', 'libopus', '-b:a', '64k', '-ar', '48000',
        ogg_path, '-y'
    ], capture_output=True)

    # 清理临时文件
    for f in [wav_path, silence_path, concat_list]:
        try:
            os.unlink(f)
        except:
            pass

    return ogg_path


def send_audio(token, ogg_path):
    with open(ogg_path, 'rb') as f:
        upload_resp = requests.post(
            'https://open.feishu.cn/open-apis/im/v1/files',
            headers={'Authorization': f'Bearer {token}'},
            files={'file': ('audio.ogg', f, 'audio/ogg')},
            data={'file_type': 'opus', 'file_name': 'audio.ogg'}
        )

    upload_data = upload_resp.json()
    if upload_data.get('code') != 0:
        raise ValueError(f"Upload failed: {upload_data}")

    file_key = upload_data['data']['file_key']

    send_resp = requests.post(
        'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'receive_id': FEISHU_USER_ID,
            'msg_type': 'audio',
            'content': json.dumps({'file_key': file_key})
        }
    )
    return send_resp.json()


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else "测试语音"
    voice = sys.argv[2] if len(sys.argv) > 2 else "Nofish"

    print(f"生成语音: {text[:20]}... 音色: {voice}")

    audio_url = generate_qwen_audio(text, voice)
    print(f"音频URL: {audio_url[:50]}...")

    wav_path = download_wav(audio_url)
    ogg_path = add_silence_and_convert(wav_path)
    print(f"转换完成(已加1.5秒空白): {ogg_path}")

    token = get_feishu_token()
    result = send_audio(token, ogg_path)
    print(f"发送结果: {result.get('code')} - {result.get('msg')}")

    os.unlink(ogg_path)


if __name__ == '__main__':
    main()
