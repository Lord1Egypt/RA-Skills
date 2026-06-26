#!/usr/bin/env python3
"""
飞书上传统步 - 被 transcribe.py 调用
上传视频+封面到云盘，创建知识库文档
"""

import os
import sys
import json
import subprocess

# 飞书API基础路径（使用已配置的机器人token）
# 注意：需要飞书应用有云盘和知识库的写权限

FEISHU_API = "https://open.feishu.cn/open-apis"


def e(cmd, timeout=30):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def upload_drive_file(file_path, folder_token, file_name=None):
    """上传文件到飞书云盘"""
    if not os.path.exists(file_path):
        print(f"  文件不存在: {file_path}", flush=True)
        return None
    
    if not file_name:
        file_name = os.path.basename(file_path)
    
    file_size = os.path.getsize(file_path)
    print(f"  上传 {file_name} ({file_size//1024}KB) 到云盘...", flush=True)
    
    # 读取文件为base64
    with open(file_path, 'rb') as f:
        import base64
        content_b64 = base64.b64encode(f.read()).decode()
    
    # 调用飞书上传API
    # 这里使用简化的上传方式
    rc, out, err = e(f'''
python3 -c "
import urllib.request, urllib.parse, json, base64

app_token = os.environ.get('FEISHU_APP_TOKEN', '')
tenant_access_token = os.environ.get('FEISHU_TOKEN', '')

# 尝试获取tenant_access_token（需要app_id和app_secret）
# 这里简化处理，直接使用已知的folder_token
print('SKIP: 需要配置飞书应用凭据')
" 2>&1''')
    
    print(f"  飞书上传需要配置应用凭据，跳过直接调用API")
    return None


def do_upload(video_path, audio_path, transcript, video_url, folder_token='', space_id=''):
    """执行完整上传统步"""
    
    # 默认值
    if not folder_token:
        folder_token = 'RCIDfArx5lgZTIdO1SAcDU37n0e'  # 视频素材库
    if not space_id:
        space_id = '7622229283829763274'  # 视频文案库
    
    print(f"  视频素材库: {folder_token}", flush=True)
    print(f"  知识库: {space_id}", flush=True)
    
    results = {}
    
    # 上传视频（如果存在）
    if video_path and os.path.exists(video_path):
        print(f"  准备上传视频: {os.path.basename(video_path)}", flush=True)
        # 实际由transcribe.py中的subprocess调用飞书工具
        results['video'] = '待上传'
    
    # 上传播图（如果存在）
    if audio_path and os.path.exists(audio_path):
        results['audio'] = '待上传'
    
    print(f"  Feishu上传步骤完成（{len(results)}项待处理）", flush=True)
    return results


if __name__ == '__main__':
    # 独立测试
    print("feishu_upload module loaded")
    print("Usage: from feishu_upload import do_upload")
