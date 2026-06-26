#!/usr/bin/env python3
"""
TikTok 视频发布器
实现 AutoPost SaaS 的 TikTok 自动上传发布功能

注意：需要 TikTok Content Posting API 权限和 video.publish Scope
"""
import os
import json
import hashlib
import hmac
import time
import requests
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any

# 配置
BASE_URL = "https://open.tiktokapis.com/v2"


class TikTokPublisher:
    """TikTok 视频发布器"""
    
    def __init__(self, client_key: str, client_secret: str, access_token: Optional[str] = None):
        """
        初始化 TikTok 发布器
        
        Args:
            client_key: TikTok Client Key
            client_secret: TikTok Client Secret
            access_token: 用户访问令牌（可选，如不提供需要授权流程）
        """
        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token = access_token
        self.base_url = BASE_URL
    
    def set_access_token(self, token: str):
        """设置访问令牌"""
        self.access_token = token
    
    def upload_video(self,
                     video_path: str,
                     title: str,
                     privacy_level: str = "PUBLIC_TO_EVERYONE",
                     disable_duet: bool = False,
                     disable_comment: bool = False,
                     disable_stitch: bool = False,
                     source: str = "FILE_UPLOAD") -> Dict[str, Any]:
        """
        上传视频到 TikTok
        
        Args:
            video_path: 视频文件路径
            title: 视频标题/描述
            privacy_level: 隐私级别
                - PUBLIC_TO_EVERYONE: 公开
                - MUTUAL_FOLLOW_FRIENDS: 互关好友可见
                - FOLLOWER_OF_CREATOR: 粉丝可见
                - SELF_ONLY: 仅自己可见
            disable_duet: 禁用合拍
            disable_comment: 禁用评论
            disable_stitch: 禁用拼接
            source: 上传方式
                - FILE_UPLOAD: 本地文件上传
                - PULL_FROM_URL: 从 URL 拉取
        
        Returns:
            {
                'success': bool,
                'publish_id': str,
                'video_url': str,
                'error': str (if failed)
            }
        """
        try:
            if not self.access_token:
                return {
                    'success': False,
                    'error': '缺少访问令牌，请先进行 OAuth 授权'
                }
            
            # 步骤 1: 初始化上传
            print(f"📤 初始化上传：{title}")
            init_response = self._init_upload(
                title=title,
                privacy_level=privacy_level,
                disable_duet=disable_duet,
                disable_comment=disable_comment,
                disable_stitch=disable_stitch,
                video_path=video_path if source == "FILE_UPLOAD" else None,
                source=source
            )
            
            if not init_response.get('success'):
                return init_response
            
            publish_id = init_response['publish_id']
            print(f"✅ 初始化成功，publish_id: {publish_id}")
            
            # 步骤 2: 上传视频文件（仅 FILE_UPLOAD 需要）
            if source == "FILE_UPLOAD" and 'upload_url' in init_response:
                upload_url = init_response['upload_url']
                print(f"📤 上传视频文件到：{upload_url[:50]}...")
                upload_response = self._upload_video_chunked(upload_url, video_path)
                
                if not upload_response.get('success'):
                    return upload_response
            
            # 步骤 3: 完成发布
            print(f"📤 完成发布...")
            finalize_response = self._finalize_publish(publish_id)
            
            if finalize_response.get('success'):
                video_url = f"https://www.tiktok.com/@user/video/{publish_id}"
                return {
                    'success': True,
                    'publish_id': publish_id,
                    'video_url': video_url
                }
            else:
                return finalize_response
            
        except Exception as e:
            return {
                'success': False,
                'error': f"上传失败：{str(e)}"
            }
    
    def _init_upload(self,
                     title: str,
                     privacy_level: str,
                     disable_duet: bool,
                     disable_comment: bool,
                     disable_stitch: bool,
                     video_path: Optional[str] = None,
                     source: str = "FILE_UPLOAD") -> Dict[str, Any]:
        """初始化上传会话"""
        url = f"{self.base_url}/post/publish/video/init/"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        
        # 构建请求体
        post_info = {
            "title": title,
            "privacy_level": privacy_level,
            "disable_duet": disable_duet,
            "disable_comment": disable_comment,
            "disable_stitch": disable_stitch,
            "video_cover_timestamp_ms": 1000
        }
        
        if source == "FILE_UPLOAD":
            # 获取文件大小
            video_size = os.path.getsize(video_path)
            chunk_size = 10 * 1024 * 1024  # 10MB chunks
            total_chunks = (video_size + chunk_size - 1) // chunk_size
            
            source_info = {
                "source": "FILE_UPLOAD",
                "video_size": video_size,
                "chunk_size": chunk_size,
                "total_chunk_count": total_chunks
            }
        else:
            source_info = {
                "source": "PULL_FROM_URL",
                "video_url": video_path  # 此时 video_path 是 URL
            }
        
        payload = {
            "post_info": post_info,
            "source_info": source_info
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        result = response.json()
        
        if response.status_code == 200 and result.get('error', {}).get('code') == 'ok':
            data = result.get('data', {})
            return_data = {
                'success': True,
                'publish_id': data.get('publish_id')
            }
            
            if 'upload_url' in data:
                return_data['upload_url'] = data['upload_url']
            
            return return_data
        else:
            error = result.get('error', {})
            return {
                'success': False,
                'error': f"{error.get('code', 'Unknown')}: {error.get('message', 'Unknown error')}"
            }
    
    def _upload_video_chunked(self, upload_url: str, video_path: str) -> Dict[str, Any]:
        """分片上传视频文件"""
        file_size = os.path.getsize(video_path)
        chunk_size = 10 * 1024 * 1024  # 10MB
        
        try:
            with open(video_path, 'rb') as f:
                chunk_number = 0
                bytes_uploaded = 0
                
                while bytes_uploaded < file_size:
                    chunk = f.read(chunk_size)
                    chunk_start = bytes_uploaded
                    chunk_end = min(bytes_uploaded + len(chunk), file_size) - 1
                    
                    headers = {
                        "Content-Range": f"bytes {chunk_start}-{chunk_end}/{file_size}",
                        "Content-Type": "video/mp4"
                    }
                    
                    response = requests.put(
                        upload_url,
                        data=chunk,
                        headers=headers,
                        timeout=300
                    )
                    
                    if response.status_code not in [200, 204, 308]:
                        return {
                            'success': False,
                            'error': f"上传分片 {chunk_number} 失败：{response.status_code}"
                        }
                    
                    bytes_uploaded += len(chunk)
                    progress = (bytes_uploaded / file_size) * 100
                    print(f"   上传进度：{progress:.1f}% ({bytes_uploaded}/{file_size})")
                    chunk_number += 1
                
                return {'success': True}
                
        except Exception as e:
            return {
                'success': False,
                'error': f"上传失败：{str(e)}"
            }
    
    def _finalize_publish(self, publish_id: str) -> Dict[str, Any]:
        """完成发布"""
        url = f"{self.base_url}/post/publish/video/finalize/"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        
        payload = {
            "publish_id": publish_id
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        result = response.json()
        
        if response.status_code == 200 and result.get('error', {}).get('code') == 'ok':
            return {
                'success': True,
                'publish_id': publish_id
            }
        else:
            error = result.get('error', {})
            return {
                'success': False,
                'error': f"{error.get('code', 'Unknown')}: {error.get('message', 'Unknown error')}"
            }
    
    def check_publish_status(self, publish_id: str) -> Dict[str, Any]:
        """查询发布状态"""
        url = f"{self.base_url}/post/publish/status/fetch/"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        
        payload = {
            "publish_id": publish_id
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        result = response.json()
        
        if response.status_code == 200 and result.get('error', {}).get('code') == 'ok':
            data = result.get('data', {})
            return {
                'success': True,
                'status': data.get('status'),  # in_queue, processing, published, failed
                'publish_id': publish_id,
                'video_url': data.get('video_url'),
                'error': data.get('error_message')
            }
        else:
            error = result.get('error', {})
            return {
                'success': False,
                'error': f"{error.get('code', 'Unknown')}: {error.get('message', 'Unknown error')}"
            }


def get_authorization_url(client_key: str, redirect_uri: str = "http://localhost") -> str:
    """
    获取 OAuth 授权 URL
    
    Args:
        client_key: TikTok Client Key
        redirect_uri: 重定向 URI
    
    Returns:
        授权 URL
    """
    base_url = "https://www.tiktok.com/v2/auth/authorize/"
    params = {
        'client_key': client_key,
        'redirect_uri': redirect_uri,
        'state': 'auto_generated_state',
        'response_type': 'code',
        'scope': 'video.publish,user.info.basic'
    }
    
    from urllib.parse import urlencode
    return base_url + '?' + urlencode(params)


def fetch_access_token(client_key: str, client_secret: str, code: str, redirect_uri: str = "http://localhost") -> Dict[str, Any]:
    """
    换取访问令牌
    
    Args:
        client_key: TikTok Client Key
        client_secret: TikTok Client Secret
        code: 授权码
        redirect_uri: 重定向 URI
    
    Returns:
        {
            'success': bool,
            'access_token': str,
            'open_id': str,
            'error': str (if failed)
        }
    """
    url = "https://open.tiktokapis.com/v2/oauth/token/"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        'client_key': client_key,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }
    
    response = requests.post(url, headers=headers, data=data, timeout=30)
    result = response.json()
    
    if response.status_code == 200 and 'access_token' in result:
        return {
            'success': True,
            'access_token': result['access_token'],
            'open_id': result.get('open_id')
        }
    else:
        return {
            'success': False,
            'error': result.get('message', 'Unknown error')
        }


if __name__ == '__main__':
    """命令行测试工具"""
    import argparse
    
    parser = argparse.ArgumentParser(description='TikTok 视频上传工具')
    parser.add_argument('--video', required=True, help='视频文件路径')
    parser.add_argument('--title', required=True, help='视频标题')
    parser.add_argument('--privacy', choices=['PUBLIC_TO_EVERYONE', 'MUTUAL_FOLLOW_FRIENDS', 'SELF_ONLY'],
                       default='PUBLIC_TO_EVERYONE', help='隐私级别')
    parser.add_argument('--client-key', help='TikTok Client Key')
    parser.add_argument('--client-secret', help='TikTok Client Secret')
    parser.add_argument('--access-token', help='Access Token')
    
    args = parser.parse_args()
    
    # 从环境变量读取凭证
    client_key = args.client_key or os.getenv('TIKTOK_CLIENT_KEY')
    client_secret = args.client_secret or os.getenv('TIKTOK_CLIENT_SECRET')
    access_token = args.access_token or os.getenv('TIKTOK_ACCESS_TOKEN')
    
    if not client_key or not client_secret:
        print("❌ 缺少 TikTok 凭证，请设置 --client-key 和 --client-secret，或设置环境变量")
        exit(1)
    
    # 初始化发布器
    publisher = TikTokPublisher(client_key, client_secret, access_token)
    
    # 上传视频
    print(f"\n📤 开始上传视频...")
    print(f"   文件：{args.video}")
    print(f"   标题：{args.title}")
    print(f"   隐私：{args.privacy}")
    print()
    
    result = publisher.upload_video(
        video_path=args.video,
        title=args.title,
        privacy_level=args.privacy
    )
    
    # 输出结果
    print("\n" + "="*60)
    if result['success']:
        print("✅ 上传成功！")
        print(f"   Publish ID: {result['publish_id']}")
        print(f"   视频 URL: {result['video_url']}")
    else:
        print("❌ 上传失败")
        print(f"   错误：{result['error']}")
    print("="*60)
