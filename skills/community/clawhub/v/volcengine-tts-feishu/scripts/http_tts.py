#!/usr/bin/env python3
"""
火山引擎豆包语音合成 - HTTP Chunked 单向流式V3
支持直接发送飞书语音气泡
文档: https://www.volcengine.com/docs/6561/1598757
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
import requests

FEISHU_API = "https://open.feishu.cn/open-apis"

def get_feishu_token(app_id, app_secret):
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(
        f"{FEISHU_API}/auth/v3/tenant_access_token/internal",
        data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["tenant_access_token"]

def upload_opus_file(token, opus_path):
    result = subprocess.run([
        "curl", "-s", "-X", "POST",
        f"{FEISHU_API}/im/v1/files",
        "-H", f"Authorization: Bearer {token}",
        "-F", "file_type=opus",
        "-F", "file_name=voice.opus",
        "-F", f"file=@{opus_path}"
    ], capture_output=True, text=True)
    data = json.loads(result.stdout)
    if data.get("code") != 0:
        print(f"❌ 上传飞书失败: {data}", file=sys.stderr)
        return None
    return data["data"]["file_key"]

def send_audio_message(token, open_id, file_key):
    content = json.dumps({"file_key": file_key})
    body = json.dumps({
        "receive_id": open_id,
        "msg_type": "audio",
        "content": content
    }).encode()
    req = urllib.request.Request(
        f"{FEISHU_API}/im/v1/messages?receive_id_type=open_id",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def main():
    parser = argparse.ArgumentParser(description='Volcengine TTS HTTP Client')
    parser.add_argument('--appid', help='App ID')
    parser.add_argument('--access_token', help='Access Token')
    parser.add_argument('--voice_type', help='Voice/speaker ID')
    parser.add_argument('--text', required=True, help='Text to synthesize')
    parser.add_argument('--output', default='output.mp3', help='Output audio file')
    parser.add_argument('--sample_rate', type=int, default=24000, help='Sample rate')
    parser.add_argument('--format', default='mp3', choices=['mp3', 'pcm', 'ogg_opus'], help='Audio format')
    parser.add_argument('--resource_id', help='Resource ID')
    parser.add_argument('--emotion', default=None, help='Emotion parameter: happy/sad/angry/surprised/fear/hate/excited/coldness/neutral/depressed/lovey-dovey/shy/comfort/tension/tender/vocal-fry/asmr')
    parser.add_argument('--send-to', default=None, help='发送飞书语音到指定open_id，自动转格式发送，不需要output文件')
    parser.add_argument('--config', default=os.path.expanduser("~/.openclaw/workspace/skills/volcengine-tts-feishu/config.json"), help='配置文件路径')
    parser.add_argument('--openclaw-config', default=os.path.expanduser("~/.openclaw/openclaw.json"), help='openclaw.json路径')
    
    args = parser.parse_args()
    
    # 从配置文件读取默认值，命令行参数会覆盖
    if os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.load(f)
        if args.appid is None:
            args.appid = config.get('appid')
        if args.access_token is None:
            args.access_token = config.get('access_token')
        if args.resource_id is None:
            args.resource_id = config.get('default_resource_id', 'seed-tts-2.0')
        if args.voice_type is None:
            args.voice_type = config.get('default_voice')
        if args.emotion is None:
            args.emotion = config.get('default_emotion')
    
    # 检查必填项最终是否有值
    required_missing = []
    if args.appid is None:
        required_missing.append('--appid')
    if args.access_token is None:
        required_missing.append('--access_token')
    if args.voice_type is None:
        required_missing.append('--voice_type')
    if required_missing:
        print(f"❌ 缺少必填参数: {', '.join(required_missing)}。可在配置文件{args.config}中设置默认值，或命令行传入。", file=sys.stderr)
        exit(1)
    
    url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
    
    headers = {
        "X-Api-App-Key": args.appid,
        "X-Api-Access-Key": args.access_token,
        "X-Api-Resource-Id": args.resource_id,
        "Content-Type": "application/json"
    }
    
    payload = {
        "user": {
            "uid": "volcengine_user"
        },
        "req_params": {
            "text": args.text,
            "speaker": args.voice_type,
            "audio_params": {
                "format": args.format,
                "sample_rate": args.sample_rate
            }
        }
    }
    
    # Add emotion parameter if provided
    if args.emotion:
        payload["req_params"]["emotion"] = args.emotion
    
    print(f"Synthesizing: {args.text}")
    response = requests.post(url, headers=headers, json=payload, stream=True)
    
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        exit(1)
    
    total_size = 0
    audio_data = bytearray()
    
    # 每个chunk都是JSON格式，包含音频数据(BASE64)
    import base64
    for line in response.iter_lines(decode_unicode=False):
        if not line:
            continue
        try:
            # Line is JSON response
            chunk_json = json.loads(line.decode('utf-8'))
            if 'data' in chunk_json and chunk_json['data']:
                # audio is base64 encoded in data field
                decoded = base64.b64decode(chunk_json['data'])
                audio_data.extend(decoded)
                total_size += len(decoded)
            elif 'code' in chunk_json and chunk_json['code'] != 0 and chunk_json['code'] != 20000000:
                print(f"Error in response: {chunk_json}")
        except Exception as e:
            print(f"Warning: failed to parse chunk: {e}, skipping")
            continue
    
    # 如果要发送飞书，临时文件放tmp，否则放指定输出路径
    import tempfile
    output_is_temp = False
    output_path = args.output
    if args.send_to:
        # 发送飞书时把临时MP3放tmp目录，避免污染工作目录
        output_path = os.path.join(tempfile.gettempdir(), f"volcengine_tts_{os.getpid()}.mp3")
        output_is_temp = True
    
    with open(output_path, 'wb') as f:
        f.write(audio_data)
    
    if not output_is_temp:
        print(f"Done! Audio saved to {output_path}, size: {total_size} bytes")

    # 如果指定了--send-to，自动转Opus发送飞书语音
    if args.send_to:
        print(f"\n正在发送到飞书 {args.send_to}...")
        
        # 读取飞书配置
        with open(args.openclaw_config) as f:
            cfg = json.load(f)
        feishu = cfg["channels"]["feishu"]
        feishu_app_id = feishu["appId"]
        feishu_app_secret = feishu["appSecret"]

        with tempfile.TemporaryDirectory() as tmpdir:
            opus_path = os.path.join(tmpdir, "voice.opus")
            # ffmpeg转Opus
            result = subprocess.run(
                ["ffmpeg", "-i", output_path, "-c:a", "libopus", opus_path, "-y"],
                capture_output=True
            )
            if result.returncode != 0:
                print(f"❌ ffmpeg转换失败", file=sys.stderr)
                sys.exit(1)
            
            # 获取token上传发送
            token = get_feishu_token(feishu_app_id, feishu_app_secret)
            file_key = upload_opus_file(token, opus_path)
            if not file_key:
                # 清理临时文件
                if output_is_temp and os.path.exists(output_path):
                    os.unlink(output_path)
                sys.exit(1)
            
            result = send_audio_message(token, args.send_to, file_key)
            # 清理临时MP3
            if output_is_temp and os.path.exists(output_path):
                os.unlink(output_path)
            
            if result.get("code") == 0:
                print(f"✅ 飞书语音发送成功！message_id: {result['data']['message_id']}")
            else:
                print(f"❌ 发送失败: {result}", file=sys.stderr)
                sys.exit(1)

if __name__ == "__main__":
    main()
