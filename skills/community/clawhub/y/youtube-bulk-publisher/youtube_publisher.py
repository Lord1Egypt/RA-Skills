#!/usr/bin/env python3
"""
YouTube 视频发布器
实现 AutoPost SaaS 的 YouTube 自动上传发布功能
"""
import os
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

# Google API 库
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# 配置
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CREDENTIALS_DIR = Path(__file__).parent / 'credentials'
TOKEN_FILE = CREDENTIALS_DIR / 'token.pickle'


class YouTubePublisher:
    """YouTube 视频发布器"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        初始化 YouTube 发布器
        
        Args:
            credentials_path: OAuth 凭证 JSON 文件路径，默认使用内置路径
        """
        if credentials_path is None:
            credentials_path = CREDENTIALS_DIR / 'youtube_credentials.json'
        
        self.credentials_path = Path(credentials_path)
        self.youtube = None
        self._authenticate()
    
    def _authenticate(self):
        """OAuth 2.0 认证"""
        creds = None
        
        # 尝试加载已保存的 token
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # 如果没有有效凭证，获取新的
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                # 使用 run_local_server 进行本地授权（使用随机端口）
                creds = flow.run_local_server(port=0)
            
            # 保存 token
            CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        
        # 构建 YouTube API 客户端
        self.youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        print("✅ YouTube 认证成功")
    
    def upload_video(self,
                     video_path: str,
                     title: str,
                     description: str = "",
                     tags: Optional[list] = None,
                     category_id: str = "22",
                     privacy_status: str = "unlisted",
                     thumbnail_path: Optional[str] = None) -> Dict[str, Any]:
        """
        上传视频到 YouTube
        
        Args:
            video_path: 视频文件路径
            title: 视频标题
            description: 视频描述
            tags: 标签列表
            category_id: 分类 ID（默认 22=人物博客）
            privacy_status: 隐私状态
                - public: 公开
                - unlisted: 不公开（仅链接可访问）
                - private: 私密
            thumbnail_path: 缩略图路径（可选）
        
        Returns:
            {
                'success': bool,
                'video_id': str,
                'video_url': str,
                'title': str,
                'error': str (if failed)
            }
        """
        try:
            # 验证视频文件
            if not os.path.exists(video_path):
                return {
                    'success': False,
                    'error': f'视频文件不存在：{video_path}'
                }
            
            # 构建视频元数据
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags or [],
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False  # 声明不是儿童内容
                }
            }
            
            # 创建媒体上传对象（分片上传，1MB chunks）
            media = MediaFileUpload(
                video_path,
                chunksize=1024 * 1024,  # 1MB chunks
                resumable=True,
                mimetype='video/mp4'
            )
            
            # 调用 API 上传视频
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            # 执行上传（带进度显示）
            response = self._resumable_upload(request)
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            result = {
                'success': True,
                'video_id': video_id,
                'video_url': video_url,
                'title': title
            }
            
            # 如果提供了缩略图，上传缩略图
            if thumbnail_path and os.path.exists(thumbnail_path):
                thumbnail_result = self._upload_thumbnail(video_id, thumbnail_path)
                if thumbnail_result:
                    result['thumbnail'] = 'uploaded'
            
            return result
            
        except HttpError as e:
            error_message = f"YouTube API 错误：{e.resp.status} - {e.content.decode('utf-8')}"
            print(f"❌ {error_message}")
            return {
                'success': False,
                'error': error_message
            }
        except Exception as e:
            error_message = f"上传失败：{str(e)}"
            print(f"❌ {error_message}")
            return {
                'success': False,
                'error': error_message
            }
    
    def _resumable_upload(self, request) -> Dict:
        """执行分片上传，显示进度"""
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"📤 上传进度：{progress}%")
        return response
    
    def _upload_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """上传视频缩略图"""
        try:
            media = MediaFileUpload(thumbnail_path, mimetype='image/jpeg')
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=media
            ).execute()
            print(f"✅ 缩略图已上传")
            return True
        except Exception as e:
            print(f"⚠️ 缩略图上传失败：{e}")
            return False
    
    def get_video_status(self, video_id: str) -> Optional[Dict[str, Any]]:
        """查询视频状态"""
        try:
            response = self.youtube.videos().list(
                part='status,snippet',
                id=video_id
            ).execute()
            
            if response['items']:
                item = response['items'][0]
                return {
                    'title': item['snippet']['title'],
                    'privacy_status': item['status']['privacyStatus'],
                    'upload_status': item['status']['uploadStatus'],
                    'embeddable': item['status']['embeddable']
                }
            return None
        except Exception as e:
            print(f"❌ 查询视频状态失败：{e}")
            return None


def main():
    """命令行测试工具"""
    parser = argparse.ArgumentParser(description='YouTube 视频上传工具')
    parser.add_argument('--video', required=True, help='视频文件路径')
    parser.add_argument('--title', required=True, help='视频标题')
    parser.add_argument('--description', default='', help='视频描述')
    parser.add_argument('--tags', default='', help='标签（逗号分隔）')
    parser.add_argument('--privacy', choices=['public', 'unlisted', 'private'],
                       default='unlisted', help='隐私状态')
    parser.add_argument('--category', default='22', help='分类 ID')
    parser.add_argument('--thumbnail', help='缩略图路径')
    parser.add_argument('--credentials', help='OAuth 凭证 JSON 文件路径')
    
    args = parser.parse_args()
    
    # 初始化发布器
    publisher = YouTubePublisher(credentials_path=args.credentials)
    
    # 解析标签
    tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
    
    # 上传视频
    print(f"\n📤 开始上传视频...")
    print(f"   文件：{args.video}")
    print(f"   标题：{args.title}")
    print(f"   隐私：{args.privacy}")
    print()
    
    result = publisher.upload_video(
        video_path=args.video,
        title=args.title,
        description=args.description,
        tags=tags,
        category_id=args.category,
        privacy_status=args.privacy,
        thumbnail_path=args.thumbnail
    )
    
    # 输出结果
    print("\n" + "="*60)
    if result['success']:
        print("✅ 上传成功！")
        print(f"   视频 ID: {result['video_id']}")
        print(f"   视频 URL: {result['video_url']}")
    else:
        print("❌ 上传失败")
        print(f"   错误：{result['error']}")
    print("="*60)


if __name__ == '__main__':
    main()
