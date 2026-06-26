"""
飞书平台集成实现
"""

from ..base_platform import BasePlatform, PlatformConfig, PlatformType, UploadResult, MessageResult
from typing import Optional, List, Any
import requests
from urllib.parse import urljoin
import os
import time
import json


class FeishuPlatform(BasePlatform):
    """飞书平台集成"""
    
    def __init__(self, config: PlatformConfig):
        super().__init__(config)
        self.base_url = "https://open.feishu.cn/open-apis"
        self.access_token = None
        self.token_expiry = 0
        
        if config.platform_type != PlatformType.FEISHU:
            raise ValueError("平台类型必须为 FEISHU")
    
    def _get_required_config_fields(self) -> List[str]:
        """
        获取必需的配置字段
        
        Returns:
            必需字段列表
        """
        return ['api_key', 'api_secret']
    
    def _perform_connection_test(self) -> bool:
        """
        执行具体的连接测试
        
        Returns:
            连接是否成功
        """
        try:
            token = self._get_access_token()
            return token is not None
        except Exception as e:
            print(f"飞书连接测试失败: {e}")
            return False
    
    def _get_access_token(self) -> Optional[str]:
        """
        获取飞书访问令牌
        
        Returns:
            访问令牌，如果获取失败则返回None
        """
        # 检查token是否有效
        if self.access_token and time.time() < self.token_expiry:
            return self.access_token
        
        url = urljoin(self.base_url, "/auth/v3/tenant_access_token/internal")
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {"app_id": self.config.api_key, "app_secret": self.config.api_secret}
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=self.config.timeout)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    self.access_token = result.get('tenant_access_token')
                    # 设置token过期时间（提前5分钟更新）
                    self.token_expiry = time.time() + 7200 - 300  # 2小时 - 5分钟
                    return self.access_token
                else:
                    print(f"飞书Token API错误: {result.get('msg')}")
            else:
                print(f"飞书Token HTTP错误: {response.status_code}")
        
        except requests.exceptions.Timeout:
            print("获取飞书token超时")
        except requests.exceptions.RequestException as e:
            print(f"获取飞书token网络错误: {e}")
        
        return None
    
    def upload_file(self, file_path: str, file_name: Optional[str] = None,
                   folder_id: Optional[str] = None) -> UploadResult:
        """
        上传文件到飞书云盘
        
        Args:
            file_path: 本地文件路径
            file_name: 上传后的文件名
            folder_id: 目标文件夹ID
            
        Returns:
            上传结果
        """
        # 验证文件存在
        if not os.path.exists(file_path):
            return UploadResult(
                success=False,
                error_message=f"文件不存在: {file_path}"
            )
        
        # 获取访问令牌
        token = self._get_access_token()
        if not token:
            return UploadResult(
                success=False,
                error_message="无法获取飞书访问令牌"
            )
        
        # 准备文件名
        if file_name is None:
            file_name = os.path.basename(file_path)
        
        file_size = os.path.getsize(file_path)
        
        # 确定MIME类型
        mime_type = self._detect_mime_type(file_path)
        
        print(f"📤 上传文件到飞书云盘: {file_name}")
        print(f"   文件大小: {file_size} 字节")
        print(f"   MIME类型: {mime_type}")
        
        # 上传URL
        upload_url = urljoin(self.base_url, "/drive/v1/files/upload_all")
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            with open(file_path, 'rb') as f:
                # 构建multipart/form-data
                files = {
                    'file': (file_name, f, mime_type)
                }
                
                data = {
                    'file_name': file_name,
                    'parent_type': 'explorer',
                    'parent_node': folder_id or '',
                    'size': str(file_size)
                }
                
                response = requests.post(upload_url, headers=headers, files=files, data=data, timeout=self.config.timeout)
                
                print(f"📊 上传响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('code') == 0:
                        file_token = result.get('data', {}).get('file_token')
                        
                        if file_token:
                            file_url = f"https://feishu.cn/file/{file_token}"
                            
                            print(f"✅ 文件上传成功!")
                            print(f"   文件token: {file_token}")
                            print(f"   文件URL: {file_url}")
                            
                            return UploadResult(
                                success=True,
                                file_url=file_url,
                                file_token=file_token,
                                file_id=file_token,
                                platform_specific_data={
                                    "upload_result": result,
                                    "file_info": {
                                        "name": file_name,
                                        "size": file_size,
                                        "mime_type": mime_type
                                    }
                                }
                            )
                        else:
                            error_msg = "API返回成功但未包含file_token"
                            print(f"❌ {error_msg}")
                    else:
                        error_msg = f"上传API错误: {result.get('msg')}"
                        print(f"❌ {error_msg}")
                else:
                    error_msg = f"上传HTTP错误: {response.status_code}"
                    print(f"❌ {error_msg}")
                    print(f"错误响应: {response.text}")
                    
                    # 如果是400错误且可能token过期，清除token缓存
                    if response.status_code == 400:
                        self.access_token = None
            
        except Exception as e:
            error_msg = f"上传异常: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()
        
        return UploadResult(
            success=False,
            error_message=error_msg or "未知错误"
        )
    
    def _detect_mime_type(self, file_path: str) -> str:
        """
        检测文件的MIME类型
        
        Args:
            file_path: 文件路径
            
        Returns:
            MIME类型字符串
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        mime_types = {
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            '.ppt': 'application/vnd.ms-powerpoint',
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.doc': 'application/msword',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.xls': 'application/vnd.ms-excel',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.txt': 'text/plain',
            '.zip': 'application/zip'
        }
        
        return mime_types.get(ext, 'application/octet-stream')
    
    def send_message(self, message: str, attachments: Optional[List[str]] = None,
                    target: Optional[str] = None) -> MessageResult:
        """
        发送消息到飞书
        
        Args:
            message: 消息内容

            attachments: 附件文件路径列表
            target: 目标（用户/群组ID）
            
        Returns:
            消息发送结果
        """
        # 获取访问令牌
        token = self._get_access_token()
        if not token:
            return MessageResult(
                success=False,
                error_message="无法获取飞书访问令牌"
            )
        
        # 构建API URL
        send_url = urljoin(self.base_url, "/im/v1/messages")
        
        # 确定接收者类型
        if target and target.startswith('ou_'):
            # 用户ID
            receive_id_type = 'user_id'
            receive_id = target
        elif target and target.startswith('oc_'):
            # 群组ID
            receive_id_type = 'chat_id'
            receive_id = target
        else:
            # 使用配置中的默认接收者
            receive_id_type = self._get_default_receive_id_type()
            receive_id = self._get_default_receive_id()
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        data = {
            "receive_id": receive_id,
            "msg_type": "text",
            "content": json.dumps({"text": message}, ensure_ascii=False)
        }
        
        try:
            response = requests.post(send_url, headers=headers, json=data, timeout=self.config.timeout)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('code') == 0:
                    message_id = result.get('data', {}).get('message_id')
                    
                    print(f"✅ 消息发送成功!")
                    print(f"   接收者: {receive_id}")
                    print(f"   消息ID: {message_id}")
                    
                    return MessageResult(
                        success=True,
                        message_id=message_id,
                        platform_specific_data={
                            "send_result": result,
                            "receive_info": {
                                "id": receive_id,
                                "type": receive_id_type
                            }
                        }
                    )
                else:
                    error_msg = f"消息发送API错误: {result.get('msg')}"
                    print(f"❌ {error_msg}")
            else:
                error_msg = f"消息发送HTTP错误: {response.status_code}"
                print(f"❌ {error_msg}")
                print(f"错误响应: {response.text}")
                
        except Exception as e:
            error_msg = f"消息发送异常: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            traceback.print_exc()
        
        return MessageResult(
            success=False,
            error_message=error_msg or "未知错误"
        )
    
    def _get_default_receive_id_type(self) -> str:
        """
        获取默认接收者类型
        
        Returns:
            接收者类型
        """
        if self.config.user_id:
            return 'user_id'
        elif self.config.channel_id:
            return 'channel_id'
        else:
            return 'chat_id'
    
    def _get_default_receive_id(self) -> str:
        """
        获取默认接收者ID
        
        Returns:
            接收者ID
        """
        if self.config.user_id:
            return self.config.user_id
        elif self.config.channel_id:
            return self.config.channel_id
        elif self.config.group_id:
            return self.config.group_id
        else:
            # 返回当前用户的ID（需要从配置或环境中获取）
            return os.getenv('FEISHU_USER_ID', '')
    
    def get_file_url(self, file_id: str) -> str:
        """
        根据文件ID获取访问URL
        
        Args:
            file_id: 文件ID
            
        Returns:
            文件访问URL
        """
        return f"https://feishu.cn/file/{file_id}"