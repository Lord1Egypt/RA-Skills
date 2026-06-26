#!/usr/bin/env python3
"""
WeChat GZH API Client
微信公众号 API 封装

功能：
- 获取 Stable Access Token
- 获取永久素材
- 发布能力：草稿管理、发布文章、查询状态、删除文章
"""

import json
import time
import requests
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass


@dataclass
class WeChatConfig:
    """微信公众号配置"""
    appid: str
    secret: str
    force_refresh: bool = False
    
    @classmethod
    def load(cls, config_path: str = None) -> 'WeChatConfig':
        """从文件加载配置"""
        if config_path is None:
            config_path = Path.home() / ".wechat_gzh_config.json"
        else:
            config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(
                f"配置文件不存在: {config_path}\n"
                f"请创建配置文件:\n"
                f'  echo \'{{"appid": "your_appid", "secret": "your_secret"}}\' > {config_path}\n'
                f"  chmod 600 {config_path}"
            )
        
        with open(config_path) as f:
            data = json.load(f)
        
        if 'appid' not in data or 'secret' not in data:
            raise ValueError("配置文件必须包含 appid 和 secret")
        
        return cls(appid=data['appid'], secret=data['secret'])


class WeChatError(Exception):
    """微信公众号 API 错误"""
    def __init__(self, errcode: int, errmsg: str):
        self.errcode = errcode
        self.errmsg = errmsg
        super().__init__(f"[{errcode}] {errmsg}")


class WeChatGZH:
    """微信公众号 API 客户端"""
    
    BASE_URL = "https://api.weixin.qq.com/cgi-bin"
    
    def __init__(self, config: WeChatConfig = None, config_path: str = None):
        """初始化客户端"""
        if config is None:
            config = WeChatConfig.load(config_path)
        self.config = config
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0
        self._session = requests.Session()
        self._session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'OpenClaw-WeChatGZH/1.0'
        })
    
    # ==================== 凭证管理 ====================
    
    def get_stable_access_token(self, force_refresh: bool = None) -> str:
        """
        获取稳定版 Access Token
        
        Args:
            force_refresh: 是否强制刷新（每天限20次，需间隔30秒）
        
        Returns:
            access_token 字符串
        """
        # 检查缓存的 token 是否有效（提前 5 分钟刷新）
        if self._access_token and time.time() < self._token_expires_at - 300:
            return self._access_token
        
        if force_refresh is None:
            force_refresh = self.config.force_refresh
        
        url = f"{self.BASE_URL}/stable_token"
        payload = {
            "grant_type": "client_credential",
            "appid": self.config.appid,
            "secret": self.config.secret,
            "force_refresh": force_refresh
        }
        
        response = self._session.post(url, json=payload, timeout=10)
        result = response.json()
        
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatError(result['errcode'], result.get('errmsg', 'Unknown error'))
        
        self._access_token = result['access_token']
        self._token_expires_at = time.time() + result['expires_in']
        
        return self._access_token
    
    # ==================== 素材管理 ====================

    def add_material(
        self,
        file_path: str,
        material_type: str,
        video_info: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        上传永久素材

        Args:
            file_path: 本地文件路径
            material_type: 素材类型 (image, voice, video, thumb)
            video_info: 视频素材信息（仅 type=video 时需要）
                - title: 视频标题
                - introduction: 视频描述

        Returns:
            {
                "media_id": "xxx",
                "url": "xxx" (仅图片素材返回)
            }
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        url = f"{self.BASE_URL}/material/add_material"
        params = {
            "access_token": self.get_stable_access_token(),
            "type": material_type
        }

        # 根据文件扩展名推断 MIME 类型
        import mimetypes
        mime_type, _ = mimetypes.guess_type(str(path))
        if not mime_type:
            mime_type = "application/octet-stream"

        with open(path, 'rb') as f:
            files = {
                'media': (path.name, f, mime_type)
            }

            # 视频素材需要额外传 description
            data = None
            if material_type == 'video':
                if not video_info:
                    video_info = {
                        'title': path.stem,
                        'introduction': ''
                    }
                data = {
                    'description': json.dumps(video_info, ensure_ascii=False)
                }

            # 临时移除 Content-Type header（requests 会自动设置 multipart）
            headers = self._session.headers.copy()
            if 'Content-Type' in headers:
                del headers['Content-Type']

            response = self._session.post(
                url,
                params=params,
                files=files,
                data=data,
                headers=headers,
                timeout=60
            )

        result = response.json()

        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatError(result['errcode'], result.get('errmsg', 'Unknown error'))

        return result

    def get_material(self, media_id: str) -> Dict[str, Any]:
        """
        获取永久素材
        
        Args:
            media_id: 素材的 media_id
        
        Returns:
            素材信息（图文/视频返回 JSON，其他返回二进制）
        """
        url = f"{self.BASE_URL}/material/get_material"
        params = {"access_token": self.get_stable_access_token()}
        payload = {"media_id": media_id}
        
        response = self._session.post(
            url,
            params=params,
            json=payload,
            timeout=30
        )
        
        # 尝试解析 JSON
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            result = response.json()
            if 'errcode' in result and result['errcode'] != 0:
                raise WeChatError(result['errcode'], result.get('errmsg', 'Unknown error'))
            return result
        else:
            # 返回二进制内容（图片/音频等）
            return {
                'type': 'binary',
                'content_type': content_type,
                'data': response.content
            }
    
    # ==================== 草稿管理 ====================
    
    def add_draft(self, articles: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        新建草稿
        
        Args:
            articles: 图文消息列表，每项包含:
                - title: 标题
                - content: 正文（支持 HTML）
                - thumb_media_id: 封面图 media_id
                - author: 作者（可选）
                - digest: 摘要（可选）
                - content_source_url: 原文链接（可选）
                - copyright_stat: 版权声明（11=原创声明，可选）
                - mp_album_id: 合集ID（可选，需先在后台创建合集）
        
        Returns:
            {"media_id": "xxx"}
        """
        url = f"{self.BASE_URL}/draft/add"
        params = {"access_token": self.get_stable_access_token()}
        payload = {"articles": articles}
        
        # 使用 ensure_ascii=False 保持中文字符不被转义
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = self._session.post(
            url,
            params=params,
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
            headers=headers,
            timeout=30
        )
        result = response.json()
        
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatError(result['errcode'], result.get('errmsg', 'Unknown error'))
        
        return result
    
    def get_draft_list(
        self,
        offset: int = 0,
        count: int = 10,
        no_content: bool = False
    ) -> Dict[str, Any]:
        """
        获取草稿列表
        
        Args:
            offset: 偏移位置
            count: 数量（1-20）
            no_content: 是否不返回 content 字段
        
        Returns:
            {
                "total_count": 总数,
                "item_count": 本次数量,
                "item": [...]
            }
        """
        url = f"{self.BASE_URL}/draft/batchget"
        params = {"access_token": self.get_stable_access_token()}
        payload = {
            "offset": offset,
            "count": min(count, 20),
            "no_content": 1 if no_content else 0
        }
        
        response = self._session.post(
            url,
            params=params,
            json=payload,
            timeout=30
        )
        result = response.json()
        
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatError(result['errcode'], result.get('errmsg', 'Unknown error'))
        
        return result
    
    def delete_draft(self, media_id: str) -> bool:
        """
        删除草稿
        
        Args:
            media_id: 草稿的 media_id
        
        Returns:
            成功返回 True
        """
        url = f"{self.BASE_URL}/draft/delete"
        params = {"access_token": self.get_stable_access_token()}
        payload = {"media_id": media_id}
        
        response = self._session.post(
            url,
            params=params,
            json=payload,
            timeout=30
        )
        result = response.json()
        
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatError(result['errcode'], result.get('errmsg', 'Unknown error'))
        
        return True
    
    # ==================== 发布能力 ====================
    
    def submit_publish(self, media_id: str) -> Dict[str, str]:
        """
        发布草稿
        
        Args:
            media_id: 草稿的 media_id
        
        Returns:
            {"publish_id": "xxx"} - 发布任务 ID
        """
        url = f"{self.BASE_URL}/freepublish/submit"
        params = {"access_token": self.get_stable_access_token()}
        payload = {"media_id": media_id}
        
        response = self._session.post(
            url,
            params=params,
            json=payload,
            timeout=30
        )
        result = response.json()
        
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatError(result['errcode'], result.get('errmsg', 'Unknown error'))
        
        return result
    
    def get_publish_status(self, publish_id: str) -> Dict[str, Any]:
        """
        发布状态查询
        
        Args:
            publish_id: 发布任务 ID
        
        Returns:
            {
                "publish_status": 状态（0=成功, 1=发布中, 2+失败）,
                "article_id": 成功后的图文 ID,
                "article_detail": {...}
            }
        """
        url = f"{self.BASE_URL}/freepublish/get"
        params = {"access_token": self.get_stable_access_token()}
        payload = {"publish_id": publish_id}
        
        response = self._session.post(
            url,
            params=params,
            json=payload,
            timeout=30
        )
        result = response.json()
        
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatError(result['errcode'], result.get('errmsg', 'Unknown error'))
        
        return result
    
    def get_published_article(self, article_id: str) -> Dict[str, Any]:
        """
        获取已发布图文信息
        
        Args:
            article_id: 图文消息的 article_id
        
        Returns:
            图文消息详情
        """
        url = f"{self.BASE_URL}/freepublish/getarticle"
        params = {"access_token": self.get_stable_access_token()}
        payload = {"article_id": article_id}
        
        response = self._session.post(
            url,
            params=params,
            json=payload,
            timeout=30
        )
        result = response.json()
        
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatError(result['errcode'], result.get('errmsg', 'Unknown error'))
        
        return result
    
    def get_published_list(
        self,
        offset: int = 0,
        count: int = 10,
        no_content: bool = False
    ) -> Dict[str, Any]:
        """
        获取已发布的消息列表
        
        Args:
            offset: 偏移位置
            count: 数量（1-20）
            no_content: 是否不返回 content 字段
        
        Returns:
            {
                "total_count": 总数,
                "item_count": 本次数量,
                "item": [
                    {
                        "article_id": "xxx",
                        "content": {...},
                        "update_time": 时间戳
                    },
                    ...
                ]
            }
        """
        url = f"{self.BASE_URL}/freepublish/batchget"
        params = {"access_token": self.get_stable_access_token()}
        payload = {
            "offset": offset,
            "count": min(count, 20),
            "no_content": 1 if no_content else 0
        }
        
        response = self._session.post(
            url,
            params=params,
            json=payload,
            timeout=30
        )
        result = response.json()
        
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatError(result['errcode'], result.get('errmsg', 'Unknown error'))
        
        return result
    
    def delete_publish(self, article_id: str, index: int = 0) -> bool:
        """
        删除发布文章
        
        Args:
            article_id: 图文消息的 article_id
            index: 要删除的文章在图文消息中的位置（第一篇为 0）
        
        Returns:
            成功返回 True
        """
        url = f"{self.BASE_URL}/freepublish/delete"
        params = {"access_token": self.get_stable_access_token()}
        payload = {
            "article_id": article_id,
            "index": index
        }
        
        response = self._session.post(
            url,
            params=params,
            json=payload,
            timeout=30
        )
        result = response.json()
        
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatError(result['errcode'], result.get('errmsg', 'Unknown error'))
        
        return True


# ==================== CLI 接口 ====================

def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="微信公众号 API 命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s get-token                         # 获取 Access Token
  %(prog)s upload-material -f image.jpg -t image   # 上传图片素材
  %(prog)s upload-material -f video.mp4 -t video --title "标题"  # 上传视频
  %(prog)s list-published -o 0 -c 10         # 获取已发布列表
  %(prog)s publish -m MEDIA_ID               # 发布草稿
  %(prog)s status -p PUBLISH_ID              # 查询发布状态
  %(prog)s article -a ARTICLE_ID             # 获取图文详情
  %(prog)s delete -a ARTICLE_ID              # 删除发布文章
        """
    )
    
    parser.add_argument('command', choices=[
        'get-token',
        'list-published',
        'list-draft',
        'publish',
        'status',
        'article',
        'delete',
        'get-material',
        'upload-material'
    ], help='命令')
    
    parser.add_argument('--config', '-C', help='配置文件路径')
    parser.add_argument('--appid', help='AppID（覆盖配置文件）')
    parser.add_argument('--secret', help='AppSecret（覆盖配置文件）')
    
    # 子命令参数
    parser.add_argument('--offset', '-o', type=int, default=0, help='偏移位置')
    parser.add_argument('--count', '-c', type=int, default=10, help='数量（1-20）')
    parser.add_argument('--no-content', action='store_true', help='不返回 content 字段')
    parser.add_argument('--media-id', '-m', help='素材/草稿的 media_id')
    parser.add_argument('--publish-id', '-p', help='发布任务 ID')
    parser.add_argument('--article-id', '-a', help='图文消息 ID')
    parser.add_argument('--index', '-i', type=int, default=0, help='文章索引')
    parser.add_argument('--force-refresh', action='store_true', help='强制刷新 Token')
    parser.add_argument('--file', '-f', help='上传文件路径')
    parser.add_argument('--type', '-t', choices=['image', 'voice', 'video', 'thumb'],
                        help='素材类型 (image/voice/video/thumb)')
    parser.add_argument('--title', help='视频标题（仅 video 类型）')
    parser.add_argument('--intro', help='视频描述（仅 video 类型）')
    
    args = parser.parse_args()
    
    try:
        # 加载配置
        config = WeChatConfig.load(args.config)
        if args.appid:
            config.appid = args.appid
        if args.secret:
            config.secret = args.secret
        if args.force_refresh:
            config.force_refresh = True
        
        # 初始化客户端
        wechat = WeChatGZH(config)
        
        # 执行命令
        if args.command == 'get-token':
            token = wechat.get_stable_access_token()
            print(f"Access Token: {token}")
        
        elif args.command == 'list-published':
            result = wechat.get_published_list(
                offset=args.offset,
                count=args.count,
                no_content=args.no_content
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == 'list-draft':
            result = wechat.get_draft_list(
                offset=args.offset,
                count=args.count,
                no_content=args.no_content
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == 'publish':
            if not args.media_id:
                parser.error("--media-id is required for publish")
            result = wechat.submit_publish(args.media_id)
            print(f"✅ 发布任务已提交")
            print(f"Publish ID: {result['publish_id']}")
        
        elif args.command == 'status':
            if not args.publish_id:
                parser.error("--publish-id is required for status")
            result = wechat.get_publish_status(args.publish_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == 'article':
            if not args.article_id:
                parser.error("--article-id is required for article")
            result = wechat.get_published_article(args.article_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.command == 'delete':
            if not args.article_id:
                parser.error("--article-id is required for delete")
            wechat.delete_publish(args.article_id, args.index)
            print(f"✅ 已删除文章")
        
        elif args.command == 'get-material':
            if not args.media_id:
                parser.error("--media-id is required for get-material")
            result = wechat.get_material(args.media_id)
            if isinstance(result, dict) and result.get('type') == 'binary':
                # 保存二进制文件
                import mimetypes
                ext = mimetypes.guess_extension(result['content_type']) or '.bin'
                filename = f"material_{args.media_id}{ext}"
                with open(filename, 'wb') as f:
                    f.write(result['data'])
                print(f"✅ 素材已保存: {filename}")
            else:
                print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == 'upload-material':
            if not args.file:
                parser.error("--file is required for upload-material")
            if not args.type:
                parser.error("--type is required for upload-material")
            video_info = None
            if args.type == 'video':
                video_info = {
                    'title': args.title or Path(args.file).stem,
                    'introduction': args.intro or ''
                }
            result = wechat.add_material(args.file, args.type, video_info)
            print(f"✅ 上传成功")
            print(f"Media ID: {result.get('media_id')}")
            if 'url' in result:
                print(f"URL: {result['url']}")
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return 1
    except WeChatError as e:
        print(f"❌ 微信 API 错误: {e}")
        return 1
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
