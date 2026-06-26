#!/usr/bin/env python3
"""
youtube_upload.py — YouTube 视频自动上传工具

基于 YouTube Data API v3 + OAuth 2.0，支持：
- 视频上传（支持大文件断点续传）
- 设置标题、描述、标签、分类、隐私状态
- 设置缩略图
- 查看上传进度

用法:
  python3 youtube_upload.py upload <video_file> --title "标题" [选项]
  python3 youtube_upload.py auth          # 首次授权
  python3 youtube_upload.py channels      # 查看频道信息
  python3 youtube_upload.py list          # 列出已上传视频

前提:
  1. pip3 install google-api-python-client google-auth-oauthlib
  2. 从 Google Cloud Console 下载 OAuth 凭证文件 (client_secret.json)
  3. 放置到 ~/.openclaw/workspace/skills/youtube-publisher/client_secret.json
"""

import os
import sys
import json
import argparse
import http.client
import httplib2
import random
import time

# === 配置 ===
SKILL_DIR = os.path.expanduser("~/.openclaw/workspace/skills/youtube-publisher")
CLIENT_SECRET_FILE = os.path.join(SKILL_DIR, "client_secret.json")
TOKEN_FILE = os.path.join(SKILL_DIR, "token.json")
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

# YouTube 视频分类 ID
CATEGORIES = {
    "电影": "1", "动画": "1",
    "汽车": "2", "交通": "2",
    "音乐": "10",
    "宠物": "15", "动物": "15",
    "体育": "17",
    "短片": "18",
    "旅游": "19", "活动": "19",
    "游戏": "20",
    "博客": "22", "人物": "22", "vlog": "22",
    "喜剧": "23", "搞笑": "23",
    "娱乐": "24",
    "新闻": "25",
    "时尚": "26",
    "教育": "27",
    "科技": "28", "技术": "28",
    "公益": "29",
}

# 最大重试次数
MAX_RETRIES = 10
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


def get_authenticated_service():
    """获取已认证的 YouTube API 服务"""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        print("❌ 缺少依赖库，请运行：")
        print("   pip3 install google-api-python-client google-auth-oauthlib")
        sys.exit(1)

    credentials = None

    # 加载已有 token
    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # 如果无效，重新授权
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("🔄 刷新访问令牌...")
            credentials.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET_FILE):
                print(f"❌ 找不到 OAuth 凭证文件: {CLIENT_SECRET_FILE}")
                print()
                print("📋 请按以下步骤获取：")
                print("   1. 打开 https://console.cloud.google.com")
                print("   2. 创建项目 → 启用 YouTube Data API v3")
                print("   3. 凭据 → 创建 OAuth 2.0 客户端 ID（桌面应用）")
                print(f"   4. 下载 JSON 并保存为: {CLIENT_SECRET_FILE}")
                sys.exit(1)

            print("🔐 首次授权，将打开浏览器...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=8090, prompt="consent")
            print("✅ 授权成功！")

        # 保存 token
        with open(TOKEN_FILE, "w") as f:
            f.write(credentials.to_json())
        print(f"💾 Token 已保存: {TOKEN_FILE}")

    return build("youtube", "v3", credentials=credentials)


def upload_video(youtube, file_path, title, description="", tags=None,
                 category="28", privacy="private", thumbnail=None,
                 language="zh-Hans", playlist_id=None):
    """上传视频到 YouTube"""
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError

    if not os.path.exists(file_path):
        print(f"❌ 视频文件不存在: {file_path}")
        return None

    file_size = os.path.getsize(file_path)
    print(f"📁 视频文件: {file_path} ({file_size / 1024 / 1024:.1f} MB)")

    # 构建视频元数据
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category,
            "defaultLanguage": language,
            "defaultAudioLanguage": language,
        },
        "status": {
            "privacyStatus": privacy,  # private, public, unlisted
            "selfDeclaredMadeForKids": False,
        },
    }

    print(f"📤 开始上传...")
    print(f"   标题: {title}")
    print(f"   隐私: {privacy}")
    print(f"   分类: {category}")
    print(f"   标签: {', '.join(tags or [])}")

    # 创建媒体上传对象（支持断点续传）
    media = MediaFileUpload(
        file_path,
        mimetype="video/*",
        chunksize=10 * 1024 * 1024,  # 10MB 分块
        resumable=True,
    )

    # 发起上传请求
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    retry = 0

    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"   ⏳ 上传进度: {progress}%")
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                retry += 1
                if retry > MAX_RETRIES:
                    print(f"❌ 超过最大重试次数 ({MAX_RETRIES})")
                    return None
                sleep_seconds = random.random() * (2 ** retry)
                print(f"   ⚠️ 重试 {retry}/{MAX_RETRIES} (等待 {sleep_seconds:.1f}s)...")
                time.sleep(sleep_seconds)
            else:
                print(f"❌ 上传失败: {e}")
                return None
        except Exception as e:
            retry += 1
            if retry > MAX_RETRIES:
                print(f"❌ 超过最大重试次数: {e}")
                return None
            sleep_seconds = random.random() * (2 ** retry)
            print(f"   ⚠️ 网络错误，重试 {retry}/{MAX_RETRIES}...")
            time.sleep(sleep_seconds)

    video_id = response["id"]
    print(f"\n✅ 上传成功！")
    print(f"   视频 ID: {video_id}")
    print(f"   链接: https://www.youtube.com/watch?v={video_id}")
    print(f"   Studio: https://studio.youtube.com/video/{video_id}/edit")

    # 设置缩略图
    if thumbnail and os.path.exists(thumbnail):
        try:
            print(f"🖼️ 设置缩略图: {thumbnail}")
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail, mimetype="image/png"),
            ).execute()
            print("   ✅ 缩略图已设置")
        except HttpError as e:
            print(f"   ⚠️ 缩略图设置失败（需要验证频道）: {e}")

    # 添加到播放列表
    if playlist_id:
        try:
            print(f"📂 添加到播放列表: {playlist_id}")
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id,
                        },
                    }
                },
            ).execute()
            print("   ✅ 已添加到播放列表")
        except HttpError as e:
            print(f"   ⚠️ 添加播放列表失败: {e}")

    return video_id


def list_channels(youtube):
    """列出频道信息"""
    response = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        mine=True,
    ).execute()

    if not response.get("items"):
        print("❌ 未找到关联的 YouTube 频道")
        return

    for ch in response["items"]:
        snippet = ch["snippet"]
        stats = ch["statistics"]
        print(f"📺 频道: {snippet['title']}")
        print(f"   ID: {ch['id']}")
        print(f"   描述: {snippet.get('description', '无')[:80]}")
        print(f"   订阅者: {stats.get('subscriberCount', '?')}")
        print(f"   视频数: {stats.get('videoCount', '?')}")
        print(f"   总播放: {stats.get('viewCount', '?')}")
        uploads_playlist = ch["contentDetails"]["relatedPlaylists"]["uploads"]
        print(f"   上传列表: {uploads_playlist}")


def list_videos(youtube, max_results=10):
    """列出已上传的视频"""
    # 先获取上传播放列表 ID
    channels = youtube.channels().list(part="contentDetails", mine=True).execute()
    if not channels.get("items"):
        print("❌ 未找到频道")
        return

    uploads_id = channels["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    response = youtube.playlistItems().list(
        part="snippet,status",
        playlistId=uploads_id,
        maxResults=max_results,
    ).execute()

    if not response.get("items"):
        print("📭 暂无上传视频")
        return

    print(f"📹 最近上传的视频 ({len(response['items'])} 个):\n")
    for item in response["items"]:
        snippet = item["snippet"]
        status = item.get("status", {})
        video_id = snippet["resourceId"]["videoId"]
        print(f"  🎬 {snippet['title']}")
        print(f"     ID: {video_id}")
        print(f"     发布: {snippet['publishedAt'][:10]}")
        print(f"     隐私: {status.get('privacyStatus', '?')}")
        print(f"     链接: https://youtu.be/{video_id}")
        print()


def list_playlists(youtube):
    """列出播放列表"""
    response = youtube.playlists().list(
        part="snippet,contentDetails",
        mine=True,
        maxResults=50,
    ).execute()

    if not response.get("items"):
        print("📭 暂无播放列表")
        return

    print(f"📂 播放列表 ({len(response['items'])} 个):\n")
    for pl in response["items"]:
        print(f"  📋 {pl['snippet']['title']}")
        print(f"     ID: {pl['id']}")
        print(f"     视频数: {pl['contentDetails']['itemCount']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="YouTube 视频自动上传工具（基于 YouTube Data API v3）"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # auth 子命令
    subparsers.add_parser("auth", help="执行 OAuth 2.0 授权")

    # channels 子命令
    subparsers.add_parser("channels", help="查看频道信息")

    # list 子命令
    list_parser = subparsers.add_parser("list", help="列出已上传视频")
    list_parser.add_argument("-n", "--max-results", type=int, default=10)

    # playlists 子命令
    subparsers.add_parser("playlists", help="列出播放列表")

    # upload 子命令
    upload_parser = subparsers.add_parser("upload", help="上传视频")
    upload_parser.add_argument("file", help="视频文件路径")
    upload_parser.add_argument("-t", "--title", required=True, help="视频标题")
    upload_parser.add_argument("-d", "--description", default="", help="视频描述")
    upload_parser.add_argument("--tags", nargs="+", default=[], help="标签列表")
    upload_parser.add_argument(
        "-c", "--category", default="28",
        help="分类 ID (28=科技, 22=博客, 27=教育, 10=音乐)"
    )
    upload_parser.add_argument(
        "-p", "--privacy", default="private",
        choices=["private", "public", "unlisted"],
        help="隐私状态 (默认: private)"
    )
    upload_parser.add_argument("--thumbnail", help="缩略图文件路径")
    upload_parser.add_argument("--playlist", help="添加到播放列表 ID")
    upload_parser.add_argument("--language", default="zh-Hans", help="语言代码")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 获取认证服务
    youtube = get_authenticated_service()

    if args.command == "auth":
        print("✅ OAuth 2.0 授权已完成！")
        list_channels(youtube)

    elif args.command == "channels":
        list_channels(youtube)

    elif args.command == "list":
        list_videos(youtube, args.max_results)

    elif args.command == "playlists":
        list_playlists(youtube)

    elif args.command == "upload":
        # 解析分类（支持中文名称）
        category = args.category
        if category in CATEGORIES:
            category = CATEGORIES[category]

        video_id = upload_video(
            youtube,
            file_path=args.file,
            title=args.title,
            description=args.description,
            tags=args.tags,
            category=category,
            privacy=args.privacy,
            thumbnail=args.thumbnail,
            playlist_id=args.playlist,
            language=args.language,
        )

        if video_id:
            print(f"\n🎉 完成！视频已上传到 YouTube")
        else:
            print(f"\n❌ 上传失败")
            sys.exit(1)


if __name__ == "__main__":
    main()
