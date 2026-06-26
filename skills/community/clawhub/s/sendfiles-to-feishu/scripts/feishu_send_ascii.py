#!/usr/bin/env python3
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import json
import uuid
import subprocess
import tempfile
import re
import math
import zipfile
import shutil

PYTHON_DEPS = ['requests']
SYSTEM_DEPS = ['ffmpeg', 'ffprobe']

def check_python_package(package):
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def install_python_package(package):
    print(f'正在安装 Python 依赖: {package}...')
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f'{package} 安装成功')
        return True
    except subprocess.CalledProcessError:
        print(f'{package} 安装失败，请手动执行: pip install {package}')
        return False

def check_system_command(cmd):
    try:
        result = subprocess.run([cmd, '-version'], capture_output=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def get_install_hint(cmd):
    hints = {
        'ffmpeg': {
            'win32': 'choco install ffmpeg 或 winget install ffmpeg',
            'darwin': 'brew install ffmpeg',
            'linux': 'sudo apt install ffmpeg 或 sudo yum install ffmpeg'
        },
        'ffprobe': {
            'win32': 'choco install ffmpeg 或 winget install ffmpeg',
            'darwin': 'brew install ffmpeg',
            'linux': 'sudo apt install ffmpeg 或 sudo yum install ffmpeg'
        }
    }
    return hints.get(cmd, {}).get(sys.platform, f'请安装 {cmd}')

def check_environment(auto_install=True):
    missing_python = []
    for pkg in PYTHON_DEPS:
        if not check_python_package(pkg):
            missing_python.append(pkg)
    
    if missing_python:
        print(f'检测到缺失的 Python 依赖: {", ".join(missing_python)}')
        if auto_install:
            for pkg in missing_python:
                install_python_package(pkg)
        else:
            print(f'请手动安装: pip install {" ".join(missing_python)}')
            return False
    
    missing_system = []
    for cmd in SYSTEM_DEPS:
        if not check_system_command(cmd):
            missing_system.append(cmd)
    
    if missing_system:
        print(f'检测到缺失的系统依赖: {", ".join(missing_system)}')
        for cmd in missing_system:
            hint = get_install_hint(cmd)
            print(f'  {cmd}: {hint}')
        return False
    
    return True

def load_env_from_skill_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    env_path = os.path.join(skill_dir, '.env')
    if os.path.isfile(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    if key and key not in os.environ:
                        os.environ[key] = value

load_env_from_skill_dir()

if not check_environment():
    print('环境检测未通过，请先安装缺失的依赖')
    sys.exit(1)

import requests

APP_ID = os.getenv('FEISHU_APP_ID')
APP_SECRET = os.getenv('FEISHU_APP_SECRET')
MAX_FILE_SIZE_MB = 20

def get_tenant_token():
    if not APP_ID or not APP_SECRET:
        raise Exception('未配置 FEISHU_APP_ID 或 FEISHU_APP_SECRET 环境变量。请设置后重试。')
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    resp = requests.post(url, json={'app_id': APP_ID, 'app_secret': APP_SECRET}, timeout=10)
    data = resp.json()
    if data.get('code') != 0:
        raise Exception(f'获取 token 失败: {data}')
    return data['tenant_access_token']

def get_duration(filepath):
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filepath], capture_output=True, text=True, timeout=10)
        return int(float(result.stdout.strip()) * 1000)
    except (subprocess.TimeoutExpired, ValueError, OSError):
        return 0

def has_audio_stream(filepath):
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', filepath], capture_output=True, text=True, timeout=10)
        return result.stdout.strip() != ''
    except (subprocess.TimeoutExpired, OSError):
        return False

def has_video_stream(filepath):
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', filepath], capture_output=True, text=True, timeout=10)
        return result.stdout.strip() != ''
    except (subprocess.TimeoutExpired, OSError):
        return False

def merge_audio_video_if_needed(video_path, output_dir):
    if has_video_stream(video_path) and has_audio_stream(video_path):
        return video_path
    print('检测到音视频分离，尝试合并...')
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    dir_path = os.path.dirname(video_path)
    candidates = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.startswith(base_name) and f != os.path.basename(video_path)]
    if len(candidates) == 1:
        other_file = candidates[0]
        v_has = has_video_stream(video_path)
        a_has = has_audio_stream(video_path)
        o_has_a = has_audio_stream(other_file)
        o_has_v = has_video_stream(other_file)
        if (v_has and o_has_a) or (a_has and o_has_v):
            merged_path = os.path.join(output_dir, f'{base_name}_merged.mp4')
            cmd = ['ffmpeg', '-i', video_path, '-i', other_file, '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0', merged_path]
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=120)
                if os.path.exists(merged_path):
                    print(f'合并完成: {merged_path}')
                    return merged_path
            except subprocess.CalledProcessError as e:
                print(f'合并失败: {e}')
    return video_path

def get_audio_codec(filepath):
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', filepath], capture_output=True, text=True, timeout=10)
        codecs = result.stdout.strip().split('\n')
        return codecs[0] if codecs else None
    except (subprocess.TimeoutExpired, OSError):
        return None

def convert_to_aac_if_needed(filepath, output_dir):
    codec = get_audio_codec(filepath)
    if codec and codec.lower() in ['opus', 'vorbis', 'flac']:
        print(f'检测到 {codec} 音频，转换为 AAC 以提高兼容性...')
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        output_path = os.path.join(output_dir, f'{base_name}_aac.mp4')
        cmd = [
            'ffmpeg', '-i', filepath,
            '-c:v', 'copy',
            '-c:a', 'aac', '-b:a', '192k',
            '-movflags', '+faststart',
            output_path
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=300)
            if os.path.exists(output_path):
                print(f'转换完成: {output_path}')
                return output_path
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            err = e.stderr.decode(errors='ignore') if hasattr(e, 'stderr') and e.stderr else str(e)
            print(f'转换失败: {err}')
    return filepath

def sanitize_filename(name, max_len=50):
    name = os.path.basename(name)
    name = re.sub(r'[^\w\u4e00-\u9fff\-\.]', '_', name)
    if len(name) > max_len:
        base, ext = os.path.splitext(name)
        base = base[:max_len - len(ext)]
        name = base + ext
    return name

def split_video_by_size(filepath, max_size_mb=MAX_FILE_SIZE_MB):
    size_mb = os.path.getsize(filepath) / (1024*1024)
    if size_mb <= max_size_mb:
        return [filepath]
    print(f'视频 {size_mb:.1f}MB 超过 {max_size_mb}MB，开始分割...')
    duration = get_duration(filepath) / 1000.0
    num_parts = math.ceil(size_mb / max_size_mb)
    segment_duration = int(duration / num_parts) + 1
    output_dir = os.path.dirname(filepath)
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_template = os.path.join(output_dir, f'{base_name}_part%03d.mp4')
    cmd = [
        'ffmpeg', '-i', filepath,
        '-c', 'copy',
        '-map', '0',
        '-segment_time', str(segment_duration),
        '-f', 'segment',
        '-reset_timestamps', '1',
        output_template
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=600)
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        print(f'分割失败: {err}')
        return [filepath]
    part_files = []
    for i in range(num_parts):
        candidate = os.path.join(output_dir, f'{base_name}_part{i:03d}.mp4')
        if os.path.exists(candidate) and os.path.getsize(candidate) > 0:
            part_files.append(candidate)
        else:
            break
    print(f'分割完成: {len(part_files)} 段')
    return part_files if part_files else [filepath]

def compress_to_zip(filepath, output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(filepath)
    zip_path = os.path.join(output_dir, f"{sanitize_filename(os.path.basename(filepath))}.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        zf.write(filepath, arcname=os.path.basename(filepath))
    return zip_path

def split_zip_by_size(zip_path, max_size_mb=MAX_FILE_SIZE_MB):
    size_mb = os.path.getsize(zip_path) / (1024*1024)
    if size_mb <= max_size_mb:
        return [zip_path]
    print(f'ZIP {size_mb:.1f}MB 超过 {max_size_mb}MB，需要分割...')
    base_name = os.path.splitext(zip_path)[0]
    original_size = os.path.getsize(zip_path)
    num_parts = math.ceil(original_size / (max_size_mb * 1024 * 1024))
    part_files = []
    for i in range(num_parts):
        part_path = f"{base_name}_part{i:03d}.zip"
        with zipfile.ZipFile(part_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
            zf.write(zip_path, arcname=os.path.basename(zip_path))
        part_files.append(part_path)
    print(f'ZIP 分割完成: {len(part_files)} 段')
    return part_files

def upload_file(token, filepath, filename=None, file_type='stream'):
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f'文件不存在: {filepath}')
    if filename is None:
        filename = os.path.basename(filepath)
    filename = sanitize_filename(filename)
    dur = get_duration(filepath)
    url = 'https://open.feishu.cn/open-apis/im/v1/files'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'file_type': file_type, 'file_name': filename, 'duration': str(dur)}
    with open(filepath, 'rb') as f:
        files = {'file': (filename, f, 'application/octet-stream')}
        resp = requests.post(url, headers=headers, files=files, data=data, timeout=120)
    result = resp.json()
    if result.get('code') != 0:
        raise Exception(f'上传失败: {result}')
    return result['data']['file_key']

def send_file_message(token, file_key, receive_id, receive_id_type='open_id'):
    url = f'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}'
    body = {'receive_id': receive_id, 'msg_type': 'file', 'content': json.dumps({'file_key': file_key}), 'uuid': str(uuid.uuid4())}
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json; charset=utf-8'}
    resp = requests.post(url, headers=headers, json=body, timeout=60)
    return resp.json()

def process_and_send_file(token, filepath, receive_id, receive_id_type):
    ext = os.path.splitext(filepath)[1].lower()
    is_video = has_video_stream(filepath)
    is_audio = has_audio_stream(filepath) and not is_video
    files_to_send = []
    temp_dir = None
    if is_video or is_audio:
        print(f'检测到{"视频" if is_video else "音频"}文件')
        temp_dir = tempfile.mkdtemp(prefix='feishu_proc_')
        processed = merge_audio_video_if_needed(filepath, temp_dir)
        processed = convert_to_aac_if_needed(processed, temp_dir)
        parts = split_video_by_size(processed, MAX_FILE_SIZE_MB)
        files_to_send.extend(parts)
    else:
        print('压缩文件为 ZIP...')
        zip_path = compress_to_zip(filepath)
        zip_size = os.path.getsize(zip_path) / (1024*1024)
        if zip_size > MAX_FILE_SIZE_MB:
            print(f'压缩后 {zip_size:.1f}MB 仍超出限制，分割 ZIP...')
            parts = split_zip_by_size(zip_path, MAX_FILE_SIZE_MB)
            files_to_send.extend(parts)
        else:
            files_to_send.append(zip_path)
    results = []
    for fp in files_to_send:
        print(f'处理: {os.path.basename(fp)}')
        try:
            file_key = upload_file(token, fp)
            print(f'  上传成功，file_key: {file_key}')
            result = send_file_message(token, file_key, receive_id, receive_id_type)
            if result.get('code') == 0:
                print(f'  发送成功')
                results.append({'file': fp, 'file_key': file_key, 'msg_id': result['data']['message_id'], 'error': None})
            else:
                print(f'  发送失败: {result}')
                results.append({'file': fp, 'error': result})
        except Exception as e:
            print(f'  出错: {e}')
            results.append({'file': fp, 'error': str(e)})
    if temp_dir and os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass
    return results

def main():
    if len(sys.argv) < 3:
        print('用法: python feishu_send.py <文件路径> <接收者ID> [ID类型]')
        print('示例: python feishu_send.py "video.mp4" "ou_xxx"')
        sys.exit(1)
    filepath = sys.argv[1]
    receive_id = sys.argv[2]
    receive_id_type = sys.argv[3] if len(sys.argv) > 3 else ('union_id' if receive_id.startswith('on_') else 'open_id')
    try:
        token = get_tenant_token()
        print('已获取 token')
        results = process_and_send_file(token, filepath, receive_id, receive_id_type)
        print('\n===== 结果 =====')
        success = sum(1 for r in results if not r['error'])
        total = len(results)
        print(f'成功: {success}/{total}')
        for r in results:
            if r['error']:
                print(f"FAIL {os.path.basename(r['file'])}: {r['error']}")
            else:
                print(f"OK {os.path.basename(r['file'])} -> msg_id: {r['msg_id']}")
    except Exception as e:
        print(f'出错: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()