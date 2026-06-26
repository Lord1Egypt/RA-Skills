# -*- coding: utf-8 -*-
"""
视频URL转文字脚本 - 独立完整版本
唐潮Toncall工作室开发
功能：
1. 根据URL下载视频到临时目录
2. 使用ffmpeg提取音频
3. 上传音频到火山引擎TOS
4. 调用火山引擎语音转文字API识别
5. 保存结果文本到texts目录
清理规则：无论成功失败，都会清理：
   - 本地下载的视频文件
   - 本地提取的音频文件
   - TOS对象存储上已上传的音频文件
不保存完整API返回的.full.json文件，只保存最终识别文本
"""

import os
import sys
import configparser
import datetime
import subprocess
import requests
import hashlib
import hmac
import uuid
import time
import json
from urllib.parse import quote, urlencode, urlparse

# 解决Windows控制台中文乱码问题
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# 检查依赖
def check_dependencies():
    """检查requests和ffmpeg是否已安装"""
    # 检查requests
    try:
        import requests
    except ImportError:
        print("[错误] requests 库未安装，请执行: pip install requests")
        sys.exit(1)
    
    # 检查ffmpeg
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
        if result.returncode != 0:
            raise FileNotFoundError()
    except FileNotFoundError:
        print("[错误] ffmpeg 未安装或未添加到系统 PATH，请安装 ffmpeg 后再试")
        print("下载地址: https://ffmpeg.org/download.html")
        sys.exit(1)

check_dependencies()

# -------------------------- 读取配置文件 --------------------------
# 配置从skill根目录的 config.ini 读取
def load_config():
    """从config.ini读取配置"""
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'config.ini')
    
    if not os.path.exists(config_path):
        print(f"[错误] 配置文件不存在: {config_path}")
        print("请复制 config.example.ini 为 config.ini 并填写你的配置")
        sys.exit(1)
    
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    
    # 读取配置
    TOS = config['tos']
    TOS_AK = TOS.get('ak', '').strip()
    TOS_SK = TOS.get('sk', '').strip()
    TOS_REGION = TOS.get('region', 'cn-beijing').strip()
    TOS_BUCKET = TOS.get('bucket', '').strip()
    TOS_BUCKET_DOMAIN = TOS.get('bucket_domain', '').strip()
    
    ASR = config['asr']
    VOLCENGINE_APP_KEY = ASR.get('app_key', '').strip()
    VOLCENGINE_ACCESS_KEY = ASR.get('access_key', '').strip()
    
    # 检查配置是否完整
    missing = []
    if not TOS_AK:
        missing.append("tos.ak")
    if not TOS_SK:
        missing.append("tos.sk")
    if not TOS_BUCKET:
        missing.append("tos.bucket")
    if not TOS_BUCKET_DOMAIN:
        missing.append("tos.bucket_domain")
    if not VOLCENGINE_APP_KEY:
        missing.append("asr.app_key")
    if not VOLCENGINE_ACCESS_KEY:
        missing.append("asr.access_key")
    
    if missing:
        print(f"[错误] 配置不完整，请在 config.ini 中填写:")
        for item in missing:
            print(f"   - {item}")
        print()
        print(f"配置文件位置: {config_path}")
        sys.exit(1)
    
    return (TOS_AK, TOS_SK, TOS_REGION, TOS_BUCKET, TOS_BUCKET_DOMAIN,
            VOLCENGINE_APP_KEY, VOLCENGINE_ACCESS_KEY)

# 加载配置
(TOS_AK, TOS_SK, TOS_REGION, TOS_BUCKET, TOS_BUCKET_DOMAIN,
 VOLCENGINE_APP_KEY, VOLCENGINE_ACCESS_KEY) = load_config()

ASR_SUBMIT_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit"
ASR_QUERY_URL = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query"
ASR_RESOURCE_ID = "volc.bigasr.auc"
# ---------------------------------------------------------------

# ========== TOS 操作 ==========
def sha256_hash(data):
    return hashlib.sha256(data).hexdigest()

def tos_put_object(local_file_path, object_key):
    """上传文件到TOS"""
    with open(local_file_path, "rb") as f:
        body = f.read()
    
    now = datetime.datetime.now(datetime.UTC)
    xdate = now.strftime('%Y%m%dT%H%M%SZ')
    datestamp = now.strftime('%Y%m%d')
    expiration = int(datetime.datetime.now(datetime.UTC).timestamp() + 300)
    
    host = TOS_BUCKET_DOMAIN
    uri = f"/{object_key}"
    
    params = {
        'X-Amz-Algorithm': 'AWS4-HMAC-SHA256',
        'X-Amz-Credential': f"{TOS_AK}/{datestamp}/{TOS_REGION}/tos/request",
        'X-Amz-Date': xdate,
        'X-Amz-Expires': '300',
        'X-Amz-SignedHeaders': 'host',
    }
    
    sorted_params = sorted(params.items())
    canonical_querystring = "&".join([f"{k}={quote(v, safe='')}" for k, v in sorted_params])
    payload_hash = sha256_hash(body)
    canonical_headers = f"host:{host}\n"
    signed_headers = "host"
    
    canonical_request = (
        f"PUT\n"
        f"{uri}\n"
        f"{canonical_querystring}\n"
        f"{canonical_headers}\n"
        f"{signed_headers}\n"
        f"{payload_hash}"
    )
    
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{datestamp}/{TOS_REGION}/tos/request"
    string_to_sign = (
        f"{algorithm}\n"
        f"{xdate}\n"
        f"{credential_scope}\n"
        f"{sha256_hash(canonical_request.encode('utf-8'))}"
    )
    
    k_secret = f"AWS4{TOS_SK}".encode('utf-8')
    k_date = hmac.new(k_secret, datestamp.encode('utf-8'), hashlib.sha256).digest()
    k_region = hmac.new(k_date, TOS_REGION.encode('utf-8'), hashlib.sha256).digest()
    k_service = hmac.new(k_region, b"tos", hashlib.sha256).digest()
    k_signing = hmac.new(k_service, b"request", hashlib.sha256).digest()
    signature = hmac.new(k_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    
    params['X-Amz-Signature'] = signature
    url = f"https://{host}{uri}?{urlencode(params)}"
    
    headers = {
        "Host": host,
        "Content-Type": "application/octet-stream"
    }
    
    response = requests.put(url, headers=headers, data=body)
    
    if response.status_code in [200, 201]:
        full_url = f"https://{TOS_BUCKET_DOMAIN}/{quote(object_key)}"
        return True, full_url, object_key
    else:
        print(f"TOS上传失败: Status {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return False, None, None

def tos_delete_object(object_key):
    """删除TOS中的对象"""
    now = datetime.datetime.now(datetime.UTC)
    xdate = now.strftime('%Y%m%dT%H%M%SZ')
    datestamp = now.strftime('%Y%m%d')
    expiration = int(datetime.datetime.now(datetime.UTC).timestamp() + 120)
    
    host = TOS_BUCKET_DOMAIN
    uri = f"/{object_key}"
    
    params = {
        'X-Amz-Algorithm': 'AWS4-HMAC-SHA256',
        'X-Amz-Credential': f"{TOS_AK}/{datestamp}/{TOS_REGION}/tos/request",
        'X-Amz-Date': xdate,
        'X-Amz-Expires': str(expiration),
        'X-Amz-SignedHeaders': 'host',
    }
    
    sorted_params = sorted(params.items())
    canonical_querystring = "&".join([f"{k}={quote(v, safe='')}" for k, v in sorted_params])
    payload_hash = sha256_hash(b"")
    canonical_headers = f"host:{host}\n"
    signed_headers = "host"
    
    canonical_request = (
        f"DELETE\n"
        f"{uri}\n"
        f"{canonical_querystring}\n"
        f"{canonical_headers}\n"
        f"{signed_headers}\n"
        f"{payload_hash}"
    )
    
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{datestamp}/{TOS_REGION}/tos/request"
    string_to_sign = (
        f"{algorithm}\n"
        f"{xdate}\n"
        f"{credential_scope}\n"
        f"{sha256_hash(canonical_request.encode('utf-8'))}"
    )
    
    k_secret = f"AWS4{TOS_SK}".encode('utf-8')
    k_date = hmac.new(k_secret, datestamp.encode('utf-8'), hashlib.sha256).digest()
    k_region = hmac.new(k_date, TOS_REGION.encode('utf-8'), hashlib.sha256).digest()
    k_service = hmac.new(k_region, b"tos", hashlib.sha256).digest()
    k_signing = hmac.new(k_service, b"request", hashlib.sha256).digest()
    signature = hmac.new(k_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    
    params['X-Amz-Signature'] = signature
    url = f"https://{host}{uri}?{urlencode(params)}"
    
    headers = {
        "Host": host
    }
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code in [200, 204]:
        return True
    else:
        print(f"TOS删除失败: Status {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return False

# ========== 语音识别 ==========
def asr_submit_task(audio_url):
    """提交语音识别任务"""
    task_id = str(uuid.uuid4())
    
    headers = {
        "X-Api-App-Key": VOLCENGINE_APP_KEY,
        "X-Api-Access-Key": VOLCENGINE_ACCESS_KEY,
        "X-Api-Resource-Id": ASR_RESOURCE_ID,
        "X-Api-Request-Id": task_id,
        "X-Api-Sequence": "-1"
    }
    
    request_body = {
        "user": {
            "uid": "openclaw_user"
        },
        "audio": {
            "url": audio_url
        },
        "request": {
            "model_name": "bigmodel",
            "enable_channel_split": True,
            "enable_ddc": True,
            "enable_speaker_info": True,
            "enable_punc": True,
            "enable_itn": True,
            "corpus": {
                "correct_table_name": "",
                "context": ""
            }
        }
    }
    
    response = requests.post(ASR_SUBMIT_URL, data=json.dumps(request_body), headers=headers)
    
    if 'X-Api-Status-Code' in response.headers and response.headers["X-Api-Status-Code"] == "20000000":
        x_tt_logid = response.headers.get("X-Tt-Logid", "")
        return task_id, x_tt_logid
    else:
        print(f"识别任务提交失败")
        print(f"Status code: {response.status_code}")
        if response.text:
            print(f"Response: {response.text}")
        return None, None

def asr_query_result(task_id, x_tt_logid):
    """查询识别结果"""
    headers = {
        "X-Api-App-Key": VOLCENGINE_APP_KEY,
        "X-Api-Access-Key": VOLCENGINE_ACCESS_KEY,
        "X-Api-Resource-Id": ASR_RESOURCE_ID,
        "X-Api-Request-Id": task_id,
        "X-Tt-Logid": x_tt_logid
    }
    
    response = requests.post(ASR_QUERY_URL, data=json.dumps({}), headers=headers)
    return response

# ========== 业务流程 ==========
def generate_filename():
    """按当前日期时间生成文件名"""
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    return timestamp

def extract_douyin_video_url(page_url):
    """解析抖音分享页面，提取真实视频URL"""
    # 移动UA更容易拿到源码
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    }
    
    print(f"[解析] 正在解析抖音分享页面: {page_url}")
    
    # 提取video id
    import re
    match = re.search(r'modal_id=(\d+)', page_url)
    if match:
        video_id = match.group(1)
        print(f"[解析] 提取到视频ID: {video_id}")
    
    response = requests.get(page_url, headers=headers, allow_redirects=True)
    if response.status_code != 200:
        print(f"[解析] 页面下载失败，状态码: {response.status_code}")
        return None
    
    html = response.text
    
    # 尝试多种方式提取视频URL
    import re
    patterns = [
        r'"playAddr":\s*"([^"]+)"',
        r'"videoUrl":\s*"([^"]+)"',
        r'"url":\s*"([^"]+\.mp4[^"]*)"',
        r'src="([^"]+\.mp4[^"]*)"',
        r'content="([^"]+)"\s+property="og:video"',
    ]
    
    for pattern in patterns:
        matches = re.search(pattern, html)
        if matches:
            video_url = matches.group(1)
            # 解码转义
            video_url = video_url.replace('\\u0026', '&').replace('\\', '').replace('&amp;', '&')
            if video_url.startswith('//'):
                video_url = 'https:' + video_url
            print(f"[解析] 提取到视频URL: {video_url[:80]}...")
            return video_url
    
    print("[解析] 未能提取到视频URL，请使用分享链接中的直接视频地址")
    return None

def download_video(url, output_dir="downloads"):
    """第一步：下载视频"""
    filename = generate_filename()
    parsed = urlparse(url)
    path = parsed.path
    ext = os.path.splitext(path)[1]
    if not ext or len(ext) > 5:
        ext = ".mp4"
    output_filename = f"{filename}{ext}"
    output_path = os.path.join(output_dir, output_filename)
    
    print(f"[1/5] 正在下载视频: {url}")
    print(f"保存到: {output_path}")
    
    response = requests.get(url, stream=True, timeout=300)
    response.raise_for_status()
    
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    file_size = os.path.getsize(output_path)
    print(f"下载完成，文件大小: {file_size / 1024 / 1024:.2f} MB")
    
    return output_path, filename

def extract_audio(video_path, output_dir="downloads"):
    """第二步：使用ffmpeg提取音频"""
    filename = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_dir, f"{filename}.mp3")
    
    print(f"\n[2/5] 正在提取音频...")
    print(f"视频: {video_path}")
    print(f"输出: {output_path}")
    
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "libmp3lame", "-q:a", "2",
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True)
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"音频提取完成，文件大小: {file_size / 1024 / 1024:.2f} MB")
            return output_path, filename
        else:
            print("音频文件生成失败")
            return None, None
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg执行错误: {e}")
        print(f"stderr: {e.stderr.decode('utf-8')}")
        return None, None
    except FileNotFoundError:
        print("错误：找不到ffmpeg，请确保ffmpeg已安装并添加到PATH")
        return None, None

def upload_audio_to_tos(audio_path):
    """第三步：上传音频到TOS"""
    print(f"\n[3/5] 正在上传音频到TOS...")
    filename = os.path.basename(audio_path)
    object_key = f"temp/{filename}"
    
    success, full_url, object_key_return = tos_put_object(audio_path, object_key)
    if success:
        print(f"上传成功，音频URL: {full_url}")
        return full_url, object_key_return
    else:
        print("上传失败")
        return None, None

def audio_url_to_text(audio_url, output_text_path):
    """第四步和第五步：语音转文字并保存"""
    print(f"\n[4/5] 正在提交语音转文字任务...")
    print(f"音频URL: {audio_url}")
    
    task_id, x_tt_logid = asr_submit_task(audio_url)
    if not task_id:
        return False
    
    print("等待任务完成...")
    while True:
        query_response = asr_query_result(task_id, x_tt_logid)
        code = query_response.headers.get('X-Api-Status-Code', "")
        
        if code == '20000000':  # 任务完成成功
            result = query_response.json()
            text = ""
            if "result" in result and "text" in result["result"]:
                text = result["result"]["text"]
            elif "text" in result:
                text = result["text"]
            
            print(f"\n[5/5] 识别完成，保存文本...")
            print(f"识别结果:\n{text}")
            
            os.makedirs(os.path.dirname(output_text_path), exist_ok=True)
            with open(output_text_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            print(f"\n文本已保存到: {output_text_path}")
            return True
        
        elif code == '20000001' or code == '20000002':  # 处理中
            print("处理中，等待1秒...")
            time.sleep(1)
            continue
        
        else:
            print(f"识别失败，状态码: {code}")
            if query_response.text:
                print(f"响应: {query_response.text}")
            return False

def cleanup_temp_files(video_path=None, audio_path=None, tos_object_key=None):
    """
    清理所有临时文件：
    1. 本地下载的视频文件
    2. 本地提取的音频文件
    3. TOS对象存储上的音频文件
    """
    # 清理本地文件
    temp_files = [video_path, audio_path]
    for file_path in temp_files:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"[清理] 已删除本地临时文件: {file_path}")
            except Exception as e:
                print(f"[清理] 本地删除失败 {file_path}: {e}")
    
    # 清理TOS上的对象
    if tos_object_key:
        try:
            print(f"[清理] 正在删除TOS对象: {tos_object_key}")
            success = tos_delete_object(tos_object_key)
            if success:
                print(f"[清理] TOS对象删除成功: {tos_object_key}")
            else:
                print(f"[清理] TOS对象删除失败: {tos_object_key}")
        except Exception as e:
            print(f"[清理] TOS删除异常 {tos_object_key}: {e}")

def main():
    if len(sys.argv) < 2:
        # 从标准输入读取URL
        print("请输入视频URL:")
        video_url = input().strip()
        if not video_url:
            print("用法: python video_url_to_text.py <视频URL>")
            print("或者直接运行然后粘贴URL")
            sys.exit(1)
    else:
        video_url = sys.argv[1]
    
    # OpenClaw接收到URL后立刻提示用户
    print(f"[开始处理] 识别到视频URL，开始自动处理...")
    print(f"URL: {video_url[:80]}...")
    print()
    
    # 创建必要目录
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("texts", exist_ok=True)
    
    video_path = None
    audio_path = None
    tos_object_key = None
    
    try:
        # 第一步：下载视频
        video_path, base_filename = download_video(video_url, "downloads")
        if not video_path:
            sys.exit(1)
        
        # 第二步：提取音频
        audio_path, _ = extract_audio(video_path, "downloads")
        if not audio_path:
            sys.exit(1)
        
        # 第三步：上传到TOS
        audio_url, tos_object_key = upload_audio_to_tos(audio_path)
        if not audio_url:
            sys.exit(1)
        
        # 保存文本到texts目录
        output_text_path = os.path.join("texts", f"{base_filename}.txt")
        
        # 第四步：语音转文字
        success = audio_url_to_text(audio_url, output_text_path)
        
        if success:
            print("\n[完成] 全部流程完成!")
            print(f"最终文本: {output_text_path}")
            sys.exit(0)
        else:
            print("\n[失败] 流程失败!")
            sys.exit(1)
    finally:
        # 无论成功失败，都清理所有临时文件
        # 本地文件 + TOS上的音频文件
        cleanup_temp_files(video_path, audio_path, tos_object_key)

if __name__ == "__main__":
    main()