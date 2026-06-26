#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云 COS 上传模块
"""

from qcloud_cos import CosConfig, CosS3Client
from typing import Optional


class CosUploader:
    """腾讯云 COS 上传器"""
    
    def __init__(
        self,
        secret_id: str,
        secret_key: str,
        region: str,
        bucket: str
    ):
        """
        初始化上传器
        
        Args:
            secret_id: 腾讯云 SecretId
            secret_key: 腾讯云 SecretKey
            region: 地域 (如 ap-guangzhou)
            bucket: 存储桶名称
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.region = region
        self.bucket = bucket
        
        # 初始化客户端
        config = CosConfig(
            Region=region,
            SecretId=secret_id,
            SecretKey=secret_key
        )
        self.client = CosS3Client(config)
    
    def upload(
        self,
        local_path: str,
        key: Optional[str] = None,
        part_size: int = 10,
        max_thread: int = 10
    ) -> str:
        """
        上传文件
        
        Args:
            local_path: 本地文件路径
            key: COS 对象键 (文件名)，默认使用本地文件名
            part_size: 分块大小 (MB)
            max_thread: 最大线程数
        
        Returns:
            文件的 COS URL
        """
        if key is None:
            key = local_path.split('/')[-1].split('\\')[-1]
        
        response = self.client.upload_file(
            Bucket=self.bucket,
            LocalFilePath=local_path,
            Key=key,
            PartSize=part_size,
            MAXThread=max_thread,
            EnableMD5=False
        )
        
        if response.get('ETag'):
            url = f"https://{self.bucket}.cos.{self.region}.myqcloud.com/{key}"
            return url
        else:
            raise Exception(f"上传失败: {response}")
    
    def delete(self, key: str) -> bool:
        """
        删除文件
        
        Args:
            key: COS 对象键
        
        Returns:
            是否成功
        """
        try:
            self.client.delete_object(
                Bucket=self.bucket,
                Key=key
            )
            return True
        except Exception as e:
            print(f"删除失败: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        检查文件是否存在
        
        Args:
            key: COS 对象键
        
        Returns:
            是否存在
        """
        try:
            self.client.head_object(
                Bucket=self.bucket,
                Key=key
            )
            return True
        except:
            return False
    
    def get_url(self, key: str) -> str:
        """
        获取文件 URL
        
        Args:
            key: COS 对象键
        
        Returns:
            文件 URL
        """
        return f"https://{self.bucket}.cos.{self.region}.myqcloud.com/{key}"
