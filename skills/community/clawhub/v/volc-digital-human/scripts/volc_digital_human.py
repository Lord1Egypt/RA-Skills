#!/usr/bin/env python3
"""
火山引擎数字人视频生成核心脚本
支持：自动图片上传、自动形象创建、自动TTS配音、自动视频合成、自动性别识别
"""

import sys
import os
import json
import time
import base64
import subprocess
import requests
from pathlib import Path
import cv2
import numpy as np

# ============ 配置 ============
# 从环境变量读取火山引擎 AK/SK（上架应用市场时不能硬编码）
# 用户需要设置环境变量：VOLC_AK 和 VOLC_SK
# 或者在 ~/.openclaw/extensions/volc-digital-human/config.json 中配置
SKILL_DIR = Path(__file__).parent.parent

def load_credentials():
    """加载火山引擎凭证，优先级：环境变量 > 配置文件"""
    # 1. 先尝试环境变量
    ak = os.environ.get('VOLC_AK', '')
    sk = os.environ.get('VOLC_SK', '')
    
    if ak and sk:
        return ak, sk
    
    # 2. 再尝试配置文件
    config_path = SKILL_DIR / 'config.json'
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                ak = config.get('ak', '')
                sk = config.get('sk', '')
                if ak and sk:
                    return ak, sk
        except Exception as e:
            print(f"[警告] 读取配置文件失败: {e}")
    
    # 3. 都没有，报错提示
    raise Exception(
        "❌ 未配置火山引擎凭证！请通过以下方式之一配置：\n"
        "  1. 设置环境变量: export VOLC_AK='your_ak' VOLC_SK='your_sk'\n"
        "  2. 创建配置文件: ~/.openclaw/extensions/volc-digital-human/config.json\n"
        "     内容: {\"ak\": \"your_ak\", \"sk\": \"your_sk\"}\n"
        "  3. 获取 AK/SK: https://console.volcengine.com/iam/keymanage/"
    )

AK, SK = load_credentials()

# 临时文件目录（使用通用路径）
TEMP_DIR = Path('/tmp/volc_digital_human')
TEMP_DIR.mkdir(exist_ok=True)

# ============ 音色配置 ============
VOICE_MAP = {
    'male': 'zh-CN-YunxiNeural',      # 男声，阳光
    'female': 'zh-CN-XiaoxiaoNeural',  # 女声，自然（默认）
    'cartoon_female': 'zh-CN-XiaoyiNeural',  # 活泼女声，适合卡通角色
    'cartoon_male': 'zh-CN-YunxiaNeural',    # 可爱男声，适合卡通角色
}

# ============ 工具函数 ============
def upload_file(file_path, mime_type):
    """上传文件到 catbox.moe，返回公开URL（国内可访问）"""
    url = "https://catbox.moe/user/api.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    with open(file_path, 'rb') as f:
        data = {'reqtype': 'fileupload'}
        files = {'fileToUpload': (Path(file_path).name, f.read(), mime_type)}
        r = requests.post(url, data=data, files=files, headers=headers, timeout=60)
    if r.status_code == 200 and r.text.startswith('https://'):
        return r.text.strip()
    # fallback: 0x0.st
    url2 = "https://0x0.st"
    with open(file_path, 'rb') as f:
        files2 = {'file': (Path(file_path).name, f.read(), mime_type)}
        r2 = requests.post(url2, files=files2, headers=headers, timeout=30)
    if r2.status_code == 200 and r2.text.startswith('https://'):
        return r2.text.strip()
    raise Exception(f"上传失败: catbox={r.status_code} 0x0={r2.status_code}")

# 兼容旧名
upload_to_uguu = upload_file

def get_latest_image():
    """获取最新收到的图片（排除mp3等其他文件）"""
    inbound = Path('/root/.openclaw/media/inbound')
    # 只取图片后缀，排除 mp3 等其他文件
    images = []
    for ext in ('*.jpg', '*.jpeg', '*.png', '*.webp', '*.gif'):
        images.extend(inbound.glob(ext))
    images = sorted(images)
    if not images:
        raise Exception("未找到图片，请先发送图片")
    return str(images[-1])

def detect_gender_simple(image_path):
    """
    用 deepface + retinaface 检测性别
    返回: 'male' | 'female' | 'unknown'
    精度高，首次调用需下载模型（自动缓存）
    """
    try:
        # 抑制 TF 日志
        import os as _os
        _os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        _os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
        
        from deepface import DeepFace
        result = DeepFace.analyze(
            image_path,
            actions=['gender'],
            detector_backend='retinaface',
            enforce_detection=False,
            silent=True
        )
        
        if isinstance(result, list):
            result = result[0]
        
        gender = result.get('gender', '')
        confidence = result.get('detection_confidence', 0)
        
        print(f"  [性别检测] deepface: {gender} ({confidence:.2%})")
        
        if gender.lower() in ('woman', 'female'):
            return 'female'
        elif gender.lower() in ('man', 'male'):
            return 'male'
        return 'female'
    
    except Exception as e:
        print(f"  [性别检测] deepface失败: {e}，降级到 Haar 启发式")
        # 降级方案：OpenCV Haar 眼检
        return _detect_gender_haar_fallback(image_path)

def _detect_gender_haar_fallback(image_path):
    """Haar 眼检降级方案"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return 'unknown'
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(gray, 1.1, 5, minSize=(8, 8))
        if len(eyes) >= 2:
            sorted_eyes = sorted(eyes, key=lambda e: e[0])[:2]
            (_, ey1, _, _), (_, ey2, _, _) = sorted_eyes[0], sorted_eyes[1]
            avg_eye_y = (ey1 + ey2) / 2
            eye_y_ratio = avg_eye_y / h
            if eye_y_ratio < 0.35:
                return 'male'
            return 'female'
        return 'female'
    except Exception:
        return 'female'

def select_voice(gender, is_cartoon=False):
    """根据性别和是否卡通选择音色"""
    if is_cartoon:
        return VOICE_MAP['cartoon_female' if gender == 'female' else 'cartoon_male']
    return VOICE_MAP['female' if gender in ('female', 'unknown') else 'male']

def exec_volc_api(action, body):
    """执行火山引擎API调用（使用原始V4签名，火山引擎API兼容性更好）"""
    import datetime, hashlib, hmac, requests
    
    t = datetime.datetime.utcnow()
    current_date = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d')
    
    body_str = json.dumps(body, ensure_ascii=False)
    payload_hash = hashlib.sha256(body_str.encode('utf-8')).hexdigest()
    content_type = 'application/json'
    
    HOST = 'visual.volcengineapi.com'
    REGION = 'cn-north-1'
    SERVICE = 'cv'
    ENDPOINT = 'https://visual.volcengineapi.com'
    
    def _sign(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
    
    def _getSignatureKey(key, dateStamp, regionName, serviceName):
        kDate = _sign(key.encode('utf-8'), dateStamp)
        kRegion = _sign(kDate, regionName)
        kService = _sign(kRegion, serviceName)
        kSigning = _sign(kService, 'request')
        return kSigning
    
    canonical_uri = '/'
    canonical_querystring = f'Action={action}&Version=2022-08-31'
    signed_headers = 'content-type;host;x-content-sha256;x-date'
    canonical_headers = f'content-type:{content_type}\nhost:{HOST}\nx-content-sha256:{payload_hash}\nx-date:{current_date}\n'
    canonical_request = f'POST\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}'
    algorithm = 'HMAC-SHA256'
    credential_scope = f'{datestamp}/{REGION}/{SERVICE}/request'
    string_to_sign = f'{algorithm}\n{current_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()}'
    signing_key = _getSignatureKey(SK, datestamp, REGION, SERVICE)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    authorization_header = f'{algorithm} Credential={AK}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'
    
    headers = {
        'X-Date': current_date,
        'Authorization': authorization_header,
        'X-Content-Sha256': payload_hash,
        'Content-Type': content_type
    }
    
    request_url = f'{ENDPOINT}?{canonical_querystring}'
    r = requests.post(request_url, headers=headers, data=body_str, timeout=30)
    return r.json()

def wait_task_done(task_id, req_key, timeout=120, interval=5):
    """轮询等待任务完成"""
    for i in range(timeout // interval):
        time.sleep(interval)
        result = exec_volc_api('query', {"req_key": req_key, "task_id": task_id})
        data = result.get('data', {})
        status = data.get('status', '')
        print(f"  [{i}] status={status}", flush=True)
        if status == 'done':
            resp_data_str = data.get('resp_data', '')
            if resp_data_str:
                return json.loads(resp_data_str)
            return {}
    raise Exception("任务超时")

def download_video(url, output_path):
    """下载视频到本地"""
    r = requests.get(url, timeout=60, stream=True)
    r.raise_for_status()
    with open(output_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

def generate_thumb(video_path, output_path, timestamp="00:00:02"):
    """截取视频缩略图"""
    subprocess.run([
        'ffmpeg', '-i', video_path, '-ss', timestamp,
        '-vframes', '1', '-q:v', '2', output_path, '-y'
    ], capture_output=True, timeout=15)

# ============ 步骤1：创建形象 ============
def create_avatar(image_url):
    """用图片URL创建数字人形象"""
    print(f"[Step1] 创建形象，图片URL: {image_url}")
    body = {
        "req_key": "realman_avatar_picture_create_role",
        "image_url": image_url
    }
    resp = exec_volc_api('submit', body)
    if resp.get('code') != 10000:
        raise Exception(f"创建形象失败: {resp.get('message')}")
    
    task_id = resp['data']['task_id']
    print(f"[Step1] task_id={task_id}，等待生成...")
    resp_data = wait_task_done(task_id, "realman_avatar_picture_create_role")
    
    resource_id = resp_data.get('resource_id', '')
    if not resource_id:
        raise Exception(f"未获取到resource_id: {json.dumps(resp_data)}")
    
    print(f"[Step1] ✅ 形象创建完成，resource_id={resource_id}")
    return resource_id

# ============ 步骤2：TTS配音 ============
def generate_tts(text, output_path, voice=None, gender='female', is_cartoon=False):
    """用edge-tts生成TTS音频"""
    if voice is None:
        voice = select_voice(gender, is_cartoon)
    print(f"[Step2] 生成TTS，音色={voice}，文本: {text[:30]}...")
    
    result = subprocess.run([
        'edge-tts',
        '--voice', voice,
        '--text', text,
        '--write-media', str(output_path)
    ], capture_output=True, timeout=30)
    
    if result.returncode != 0:
        raise Exception(f"TTS生成失败: {result.stderr.decode()}")
    
    # 上传到uguu
    audio_url = upload_to_uguu(output_path, 'audio/mpeg')
    print(f"[Step2] ✅ TTS完成，URL: {audio_url}")
    return audio_url

# ============ 步骤3：视频合成 ============
def generate_video(resource_id, audio_url):
    """用形象+音频合成视频"""
    print(f"[Step3] 提交视频合成任务...")
    body = {
        "req_key": "realman_avatar_picture_v2",
        "resource_id": resource_id,
        "audio_url": audio_url
    }
    resp = exec_volc_api('submit', body)
    if resp.get('code') != 10000:
        raise Exception(f"提交视频任务失败: {resp.get('message')}")
    
    task_id = resp['data']['task_id']
    print(f"[Step3] task_id={task_id}，等待生成(约10-30秒)...")
    resp_data = wait_task_done(task_id, "realman_avatar_picture_v2", timeout=180, interval=5)
    
    preview_urls = resp_data.get('preview_url', [])
    video_url = preview_urls[0] if preview_urls else ''
    duration = resp_data.get('video', {}).get('VideoMeta', {}).get('Duration', 0)
    
    print(f"[Step3] ✅ 视频生成完成，URL长度={len(video_url)}，时长={duration:.1f}秒")
    return video_url

# ============ 主流程 ============
def run_full_workflow(image_path=None, dialog_text=None, gender=None, 
                      is_cartoon=False, voice=None, resource_id=None):
    """
    完整流程：图片+对白 -> 数字人视频
    
    参数:
        image_path: 图片路径，None=自动获取最新
        dialog_text: 对白文案
        gender: 'male'|'female'|None（None=自动检测）
        is_cartoon: 是否卡通角色
        voice: 手动指定音色，覆盖自动选择
        resource_id: 可选，已有形象ID则跳过创建
    """
    print("=" * 50)
    print("火山引擎数字人视频生成开始")
    print("=" * 50)
    
    # Step 0: 获取/检测图片
    if image_path is None:
        image_path = get_latest_image()
    print(f"[Step0] 使用图片: {image_path}")
    
    # 自动性别检测
    if gender is None:
        gender = detect_gender_simple(image_path)
        print(f"[Step0] 自动性别检测结果: {gender}")
    
    # Step 0.5: 上传图片
    print("[Step0] 上传图片到uguu...")
    img_url = upload_to_uguu(image_path, 'image/jpeg')
    print(f"[Step0] ✅ 图片URL: {img_url}")
    
    # Step 1: 创建形象（可复用resource_id）
    if resource_id is None:
        resource_id = create_avatar(img_url)
    
    # Step 2: TTS
    if dialog_text is None:
        raise Exception("未提供对白文案，请提供dialog_text参数")
    tts_path = TEMP_DIR / "tts_audio.mp3"
    audio_url = generate_tts(dialog_text, tts_path, voice=voice, gender=gender, is_cartoon=is_cartoon)
    
    # Step 3: 视频合成
    video_url = generate_video(resource_id, audio_url)
    
    # Step 4: 下载视频
    print("[Step4] 下载视频...")
    video_path = TEMP_DIR / "output_video.mp4"
    download_video(video_url, video_path)
    print(f"[Step4] ✅ 视频已下载: {video_path} ({os.path.getsize(video_path)//1024}KB)")
    
    # Step 5: 截图
    thumb_path = TEMP_DIR / "thumb.jpg"
    generate_thumb(video_path, thumb_path)
    print(f"[Step5] ✅ 缩略图已生成: {thumb_path}")
    
    print("=" * 50)
    print("🎉 全部完成！")
    print("=" * 50)
    
    return {
        'video_path': str(video_path),
        'thumb_path': str(thumb_path),
        'video_url': video_url,
        'resource_id': resource_id,
        'audio_url': audio_url,
        'gender': gender,
        'voice': voice or select_voice(gender, is_cartoon)
    }

if __name__ == '__main__':
    # 测试
    image = sys.argv[1] if len(sys.argv) > 1 else None
    text = sys.argv[2] if len(sys.argv) > 2 else "你好，这是测试音频。"
    gender = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = run_full_workflow(image, text, gender=gender)
    print(json.dumps({k: v if k != 'video_path' else os.path.getsize(v) for k, v in result.items()}, indent=2, ensure_ascii=False))
