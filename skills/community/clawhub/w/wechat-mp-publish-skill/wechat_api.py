#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号 API 封装
封装公众号官方 API 调用，包括 token 管理、素材管理、发布等
"""

import requests
import time
import json
import os
import base64
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WeChatAPI:
    """微信公众号 API 客户端"""
    
    def __init__(self, appid: str, appsecret: str, cache_file: str = ".token_cache"):
        """
        初始化 API 客户端
        
        Args:
            appid: 公众号 AppID
            appsecret: 公众号 AppSecret
            cache_file: access_token 缓存文件路径
        """
        self.appid = appid
        self.appsecret = appsecret
        self.cache_file = Path(cache_file)
        self.api_base = "https://api.weixin.qq.com/cgi-bin"
        
        self._access_token = None
        self._token_expires_at = 0
    
    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        获取 access_token（带缓存）
        
        Args:
            force_refresh: 是否强制刷新
            
        Returns:
            access_token 字符串
        """
        # 检查缓存是否有效
        if not force_refresh and self._access_token and time.time() < self._token_expires_at:
            return self._access_token
        
        # 尝试从文件加载缓存
        if not force_refresh and self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    if cache.get('expires_at', 0) > time.time():
                        self._access_token = cache['access_token']
                        self._token_expires_at = cache['expires_at']
                        logger.info("从文件加载 access_token 缓存")
                        return self._access_token
            except Exception as e:
                logger.warning(f"加载 token 缓存失败：{e}")
        
        # 获取新 token
        self._refresh_token()
        return self._access_token
    
    def _refresh_token(self):
        """刷新 access_token"""
        url = f"{self.api_base}/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.appsecret
        }
        
        logger.info("正在获取新的 access_token...")
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        if "access_token" in result:
            self._access_token = result["access_token"]
            # 提前 5 分钟过期
            expires_in = result.get("expires_in", 7200)
            self._token_expires_at = time.time() + expires_in - 300
            
            # 保存到文件
            self._save_token_cache()
            
            # 脱敏记录日志（只显示前 8 位和后 4 位）
            token = self._access_token
            masked_token = f"{token[:8]}...{token[-4:]}" if len(token) > 12 else "***"
            logger.info(f"access_token 获取成功，有效期 {expires_in}秒，Token: {masked_token}")
        else:
            errcode = result.get("errcode", 0)
            errmsg = result.get("errmsg", "未知错误")
            logger.error(f"获取 access_token 失败：{errcode} - {errmsg}")
            raise Exception(f"获取 access_token 失败：{errmsg}")
    
    def _save_token_cache(self):
        """保存 token 到文件"""
        try:
            cache = {
                "access_token": self._access_token,
                "expires_at": self._token_expires_at,
                "updated_at": datetime.now().isoformat()
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
            # 设置文件权限
            os.chmod(self.cache_file, 0o600)
        except Exception as e:
            logger.warning(f"保存 token 缓存失败：{e}")
    
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """GET 请求"""
        url = f"{self.api_base}/{endpoint}"
        if params is None:
            params = {}
        params["access_token"] = self.get_access_token()
        
        response = requests.get(url, params=params, timeout=30)
        return response.json()
    
    def _post(self, endpoint: str, data: Any = None, files: Optional[Dict] = None) -> Dict:
        """POST 请求"""
        url = f"{self.api_base}/{endpoint}"
        params = {"access_token": self.get_access_token()}
        
        if files:
            # 文件上传
            response = requests.post(url, params=params, files=files, timeout=60)
        else:
            # JSON 数据 - 关键：确保 UTF-8 编码，不转义中文
            json_str = json.dumps(data, ensure_ascii=False)
            response = requests.post(
                url, 
                params=params, 
                data=json_str.encode('utf-8'),
                headers={"Content-Type": "application/json; charset=utf-8"},
                timeout=30
            )
        
        # 关键：确保响应使用 UTF-8 解码
        response.encoding = 'utf-8'
        return response.json()
    
    # ========== 素材管理 ==========
    
    def upload_image(self, image_path: str) -> Dict:
        """
        上传图片到微信服务器（使用 uploadimg 接口）
        
        Args:
            image_path: 本地图片路径
            
        Returns:
            {"url": "图片 URL"}
        """
        endpoint = "media/uploadimg"
        
        with open(image_path, 'rb') as f:
            files = {"media": f}
            result = self._post(endpoint, files=files)
        
        if "url" in result:
            logger.info(f"图片上传成功：{result['url']}")
            return {"url": result["url"]}
        else:
            errcode = result.get("errcode", 0)
            errmsg = result.get("errmsg", "未知错误")
            logger.error(f"图片上传失败：{errcode} - {errmsg}")
            raise Exception(f"图片上传失败：{errmsg}")
    
    def upload_cover_media(self, image_path: str) -> Dict:
        """
        上传封面素材（使用 material/add_material 接口）
        用于草稿箱的 thumb_media_id
        
        Args:
            image_path: 本地图片路径
            
        Returns:
            {"media_id": "媒体 ID", "url": "图片 URL"}
        """
        import requests
        
        endpoint = "material/add_material"
        url = f"{self.api_base}/{endpoint}"
        params = {"access_token": self.get_access_token()}
        
        # 构建 multipart/form-data 请求
        with open(image_path, 'rb') as f:
            # 微信要求：type=image, 并且需要 description 字段
            files = {
                'media': ('cover.jpg', f, 'image/jpeg'),
                'type': (None, 'image'),
            }
            
            response = requests.post(url, params=params, files=files, timeout=60)
            result = response.json()
        
        if "media_id" in result:
            logger.info(f"封面素材上传成功：media_id={result['media_id']}, url={result.get('url', '')}")
            return {
                "media_id": result["media_id"],
                "url": result.get("url", "")
            }
        else:
            errcode = result.get("errcode", 0)
            errmsg = result.get("errmsg", "未知错误")
            logger.error(f"封面素材上传失败：{errcode} - {errmsg}")
            # 降级使用 uploadimg
            logger.warning("降级使用 uploadimg 接口")
            img_result = self.upload_image(image_path)
            # uploadimg 只返回 URL，没有 media_id
            return {
                "media_id": None,
                "url": img_result["url"]
            }
    
    def upload_temp_media(self, image_path: str, media_type: str = "image") -> Dict:
        """
        上传临时素材（3 天有效期）
        
        Args:
            image_path: 本地图片路径
            media_type: 媒体类型 (image, voice, video, thumb)
            
        Returns:
            {"media_id": "媒体 ID", "created_at": 创建时间}
        """
        endpoint = f"media/upload?type={media_type}"
        
        with open(image_path, 'rb') as f:
            files = {"media": f}
            result = self._post(endpoint, files=files)
        
        if "media_id" in result:
            logger.info(f"临时素材上传成功：{result['media_id']}")
            return result
        else:
            errcode = result.get("errcode", 0)
            errmsg = result.get("errmsg", "未知错误")
            logger.error(f"临时素材上传失败：{errcode} - {errmsg}")
            raise Exception(f"临时素材上传失败：{errmsg}")
    
    def upload_permanent_material(self, image_path: str) -> Dict:
        """
        上传永久素材（用于封面图）
        
        Args:
            image_path: 本地图片路径
            
        Returns:
            {"media_id": "媒体 ID", "url": "图片 URL"}
        """
        endpoint = "material/add_material"
        
        # 需要特殊的 form 格式
        data = {
            "type": "image",
            "description": json.dumps({"title": "cover", "introduction": "article cover"})
        }
        
        with open(image_path, 'rb') as f:
            files = {
                "media": f
            }
            # 手动构建 multipart 请求
            import requests
            from requests_toolbelt.multipart.encoder import MultipartEncoder
            
            try:
                # 使用 requests_toolbelt 或手动构建
                url = f"{self.api_base}/{endpoint}"
                params = {"access_token": self.get_access_token()}
                
                # 简单方式：直接 POST 文件
                files = {"media": f}
                response = requests.post(url, params=params, files=files, timeout=60)
                result = response.json()
                
                if "media_id" in result:
                    logger.info(f"永久素材上传成功：{result['media_id']}")
                    return result
                else:
                    errcode = result.get("errcode", 0)
                    errmsg = result.get("errmsg", "未知错误")
                    logger.error(f"永久素材上传失败：{errcode} - {errmsg}")
                    raise Exception(f"永久素材上传失败：{errmsg}")
            except ImportError:
                # 回退到 uploadimg
                logger.warning("requests_toolbelt 未安装，使用 uploadimg 接口")
                return self.upload_image(image_path)
    
    # ========== 草稿箱管理 ==========
    
    def create_draft(self, articles: List[Dict]) -> Dict:
        """
        创建草稿（支持多图文）
        """
        endpoint = "draft/add"
        
        # 构建 articles 数组
        articles_data = []
        for article in articles:
            art = {
                "title": article.get("title", ""),
                "author": article.get("author", ""),
                "digest": article.get("digest", ""),
                "content": article.get("content", ""),
                "thumb_media_id": article.get("thumb_media_id", ""),
                "show_cover_pic": 1,  # 强制设置为 1
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }
            # 调试日志
            logger.info(f"文章标题：{art['title']}, thumb_media_id: {art['thumb_media_id'][:20]}..., show_cover_pic: {art['show_cover_pic']}")
            articles_data.append(art)
        
        data = {"articles": articles_data}
        logger.info(f"发送草稿数据：{json.dumps({'articles': [{'title': a['title'], 'thumb_media_id': a['thumb_media_id'][:20], 'show_cover_pic': a['show_cover_pic']} for a in articles_data]}, ensure_ascii=False)}")
        result = self._post(endpoint, data=data)
        
        if "media_id" in result:
            logger.info(f"草稿创建成功：{result['media_id']}")
            return result
        else:
            errcode = result.get("errcode", 0)
            errmsg = result.get("errmsg", "未知错误")
            logger.error(f"草稿创建失败：{errcode} - {errmsg}")
            raise Exception(f"草稿创建失败：{errmsg}")
    
    def update_draft(self, media_id: str, index: int, articles: Dict) -> Dict:
        """
        修改草稿
        
        Args:
            media_id: 草稿 media_id
            index: 要修改的文章位置（从 0 开始）
            articles: 新的文章数据
            
        Returns:
            API 响应
        """
        endpoint = "draft/update"
        
        data = {
            "media_id": media_id,
            "index": index,
            "articles": articles
        }
        
        return self._post(endpoint, data=data)
    
    def delete_draft(self, media_id: str) -> Dict:
        """删除草稿"""
        endpoint = "draft/delete"
        data = {"media_id": media_id}
        return self._post(endpoint, data=data)
    
    def get_draft(self, media_id: str) -> Dict:
        """获取草稿内容"""
        endpoint = "draft/get"
        data = {"media_id": media_id}
        return self._post(endpoint, data=data)
    
    def list_drafts(self, offset: int = 0, count: int = 20, no_content: bool = False) -> Dict:
        """
        获取草稿列表
        
        Args:
            offset: 偏移量
            count: 数量（最多 20）
            no_content: 是否不返回内容
            
        Returns:
            {"item": [...], "total_count": 总数, "item_count": 本次数量}
        """
        endpoint = "draft/batchget"
        data = {
            "offset": offset,
            "count": count,
            "no_content": 1 if no_content else 0
        }
        return self._post(endpoint, data=data)
    
    # ========== 发布管理 ==========
    
    def publish_all(self, media_id: str, preview: bool = False) -> Dict:
        """
        群发所有用户
        
        Args:
            media_id: 草稿 media_id 或 永久素材 media_id
            preview: 是否预览
            
        Returns:
            {"errcode": 0, "errmsg": "send job submission success", ...}
        """
        if preview:
            endpoint = "message/mass/preview"
            # 预览需要额外的 openid 参数
            raise NotImplementedError("预览功能需要指定 openid")
        else:
            endpoint = "message/mass/sendall"
            data = {
                "filter": {"is_to_all": True},
                "mpnews": {"media_id": media_id},
                "msgtype": "mpnews",
                "send_ignore_reprint": 1  # 忽略原创检查
            }
            return self._post(endpoint, data=data)
    
    def publish(self, media_id: str) -> Dict:
        """
        发布（新版发布接口，返回 publish_id）
        
        Args:
            media_id: 草稿 media_id
            
        Returns:
            {"publish_id": 发布 ID}
        """
        endpoint = "freepublish/submit"
        data = {"media_id": media_id}
        return self._post(endpoint, data=data)
    
    def get_publish_status(self, publish_id: int) -> Dict:
        """查询发布状态"""
        endpoint = "freepublish/get"
        data = {"publish_id": publish_id}
        return self._post(endpoint, data=data)
    
    # ========== 其他工具 ==========
    
    def get_menu(self) -> Dict:
        """获取自定义菜单"""
        return self._get("menu/get")
    
    def get_user_count(self) -> Dict:
        """获取用户总数"""
        return self._get("user/get")
    
    def short_url(self, long_url: str, action: str = "long2short") -> Dict:
        """生成短链接"""
        endpoint = "shorturl"
        data = {"action": action, "long_url": long_url}
        return self._post(endpoint, data=data)


def test_api():
    """测试 API 连接"""
    import sys
    
    if len(sys.argv) < 3:
        print("用法：python wechat_api.py <appid> <appsecret>")
        sys.exit(1)
    
    appid = sys.argv[1]
    appsecret = sys.argv[2]
    
    api = WeChatAPI(appid, appsecret)
    
    print("🧪 测试微信公众号 API")
    print("=" * 50)
    
    try:
        # 测试 token
        token = api.get_access_token()
        print(f"✅ access_token: {token[:20]}...")
        
        # 测试获取草稿列表
        drafts = api.list_drafts(count=5, no_content=True)
        print(f"✅ 草稿数量：{drafts.get('total_count', 0)}")
        
        print("\n✅ API 测试通过！")
        
    except Exception as e:
        print(f"❌ API 测试失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    test_api()
