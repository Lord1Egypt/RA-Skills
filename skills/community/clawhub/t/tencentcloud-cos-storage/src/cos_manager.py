#!/usr/bin/env python3
"""
TencentCloud-COS - 腾讯云对象存储管理
管理 COS 存储桶，支持文件上传/下载、生命周期配置
"""

import os
import json
import hashlib
import mimetypes
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# COS SDK
from qcloud_cos import CosConfig, CosS3Client
from qcloud_cos.cos_exception import CosServiceError, CosClientError
from qcloud_cos.cos_threadpool import SimpleThreadPool

# ==================== 配置 ====================

SECRET_ID = os.getenv("TENCENT_SECRET_ID")
SECRET_KEY = os.getenv("TENCENT_SECRET_KEY")
REGION = os.getenv("TENCENT_REGION", "ap-singapore")
RESOURCE_PREFIX = os.getenv("RESOURCE_PREFIX", "cos")
DEFAULT_STORAGE_CLASS = os.getenv("DEFAULT_STORAGE_CLASS", "STANDARD")

# 存储类型
STORAGE_CLASSES = {
    "STANDARD": "标准存储",
    "STANDARD_IA": "低频存储",
    "ARCHIVE": "归档存储",
    "DEEP_ARCHIVE": "深度归档"
}


# ==================== 初始化 ====================

def init_cos_client():
    """初始化 COS 客户端"""
    if not SECRET_ID or not SECRET_KEY:
        raise ValueError("❌ 请配置 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY")
    
    config = CosConfig(
        Region=REGION,
        SecretId=SECRET_ID,
        SecretKey=SECRET_KEY,
        Timeout=60,
        Scheme="https"
    )
    
    return CosS3Client(config)


# ==================== 价格数据 ====================

PRICING = {
    "STANDARD": {
        "storage": 0.13,      # ¥/GB/月
        "download": 0.50,     # ¥/GB
        "upload": 0,          # 免费
        "request": 0.01       # ¥/万次
    },
    "STANDARD_IA": {
        "storage": 0.08,      # ¥/GB/月
        "download": 0.50,     # ¥/GB
        "upload": 0,          # 免费
        "request": 0.02,      # ¥/万次
        "min_days": 30        # 最小存储天数
    },
    "ARCHIVE": {
        "storage": 0.03,      # ¥/GB/月
        "download": 0.50,     # ¥/GB
        "upload": 0,          # 免费
        "request": 0.03,      # ¥/万次
        "min_days": 180,      # 最小存储天数
        "restore_time": "1-2 小时"  # 解冻时间
    },
    "DEEP_ARCHIVE": {
        "storage": 0.02,      # ¥/GB/月
        "download": 0.50,     # ¥/GB
        "upload": 0,          # 免费
        "request": 0.03,      # ¥/万次
        "min_days": 365,      # 最小存储天数
        "restore_time": "5-12 小时"  # 解冻时间
    }
}


# ==================== 成本管理 ====================

class COSCostManager:
    """COS 成本管理器"""
    
    def __init__(self):
        self.pricing = PRICING
    
    def estimate_cost(self, 
                     storage_gb: float,
                     storage_class: str = "STANDARD",
                     download_gb: float = 0,
                     requests_count: int = 0,
                     days: int = 30) -> Dict:
        """
        估算成本
        
        参数:
            storage_gb: 存储量 (GB)
            storage_class: 存储类型
            download_gb: 下载流量 (GB)
            requests_count: 请求次数
            days: 天数
        """
        pricing = self.pricing.get(storage_class, self.pricing["STANDARD"])
        months = days / 30
        
        storage_cost = storage_gb * pricing["storage"] * months
        download_cost = download_gb * pricing["download"]
        request_cost = (requests_count / 10000) * pricing["request"]
        
        total = storage_cost + download_cost + request_cost
        
        return {
            "storage_cost": round(storage_cost, 2),
            "download_cost": round(download_cost, 2),
            "request_cost": round(request_cost, 2),
            "total": round(total, 2),
            "currency": "CNY"
        }
    
    def compare_storage_classes(self, storage_gb: float, months: int = 12) -> List[Dict]:
        """比较不同存储类型的成本"""
        results = []
        
        for storage_class, pricing in self.pricing.items():
            cost = storage_gb * pricing["storage"] * months
            results.append({
                "storage_class": storage_class,
                "name": STORAGE_CLASSES.get(storage_class, storage_class),
                "monthly_cost": round(storage_gb * pricing["storage"], 2),
                "total_cost": round(cost, 2),
                "min_days": pricing.get("min_days", 0),
                "savings": round((1 - pricing["storage"] / 0.13) * 100, 1) if storage_class != "STANDARD" else 0
            })
        
        return sorted(results, key=lambda x: x["total_cost"])
    
    def print_cost_comparison(self, storage_gb: float, months: int = 12):
        """打印成本对比"""
        print("=" * 80)
        print(f"COS 存储类型成本对比 (存储量：{storage_gb} GB, 时长：{months} 个月)")
        print("=" * 80)
        
        results = self.compare_storage_classes(storage_gb, months)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['name']} ({result['storage_class']})")
            print(f"   月成本：¥{result['monthly_cost']}")
            print(f"   总成本：¥{result['total_cost']}")
            if result['savings'] > 0:
                print(f"   节省：{result['savings']}% (相比标准存储)")
            if result['min_days'] > 0:
                print(f"   最小存储期：{result['min_days']} 天")
        
        print("\n" + "=" * 80)


# ==================== COS 管理 ====================

class COSManager:
    """COS 对象存储管理器"""
    
    def __init__(self):
        self.client = init_cos_client()
        self.cost_manager = COSCostManager()
    
    def create_bucket(self, 
                     bucket_name: str = None,
                     region: str = None,
                     storage_class: str = "STANDARD",
                     acl: str = "private") -> Dict:
        """
        创建存储桶
        
        参数:
            bucket_name: 存储桶名称
            region: 区域
            storage_class: 存储类型
            acl: 访问权限 (private/public-read/public-read-write)
        """
        if not bucket_name:
            bucket_name = f"{RESOURCE_PREFIX}-{datetime.now().strftime('%Y%m%d%H%M')}"
        
        if not region:
            region = REGION
        
        # 确保 bucket 名称包含 appid (简化处理，使用默认格式)
        if "-" not in bucket_name or len(bucket_name.split("-")) < 2:
            bucket_name = f"{bucket_name}-{REGION}"
        
        bucket = f"{bucket_name}.cos.{region}.myqcloud.com"
        
        try:
            self.client.create_bucket(
                Bucket=bucket,
                ACL=acl
            )
            
            # 设置存储类型
            if storage_class != "STANDARD":
                self.client.put_bucket_versioning(
                    Bucket=bucket,
                    Status='Enabled'
                )
            
            print(f"✅ 创建存储桶成功：{bucket}")
            print(f"   区域：{region}")
            print(f"   存储类型：{storage_class}")
            print(f"   权限：{acl}")
            
            return {
                "bucket": bucket,
                "region": region,
                "storage_class": storage_class,
                "acl": acl
            }
        
        except CosServiceError as e:
            print(f"❌ 创建失败：{e}")
            return {}
    
    def delete_bucket(self, bucket: str, force: bool = False):
        """
        删除存储桶
        
        参数:
            bucket: 存储桶名称
            force: 是否强制删除 (先清空内容)
        """
        try:
            if force:
                # 先删除所有对象
                self._clear_bucket(bucket)
            
            self.client.delete_bucket(Bucket=bucket)
            print(f"✅ 删除存储桶成功：{bucket}")
        
        except CosServiceError as e:
            print(f"❌ 删除失败：{e}")
    
    def _clear_bucket(self, bucket: str):
        """清空存储桶"""
        try:
            # 删除所有对象
            while True:
                response = self.client.list_objects(Bucket=bucket, MaxKeys=1000)
                if 'Contents' not in response or len(response['Contents']) == 0:
                    break
                
                for obj in response['Contents']:
                    self.client.delete_object(Bucket=bucket, Key=obj['Key'])
            
            # 删除所有分片
            while True:
                response = self.client.list_multipart_uploads(Bucket=bucket, MaxUploads=1000)
                if 'Upload' not in response or len(response['Upload']) == 0:
                    break
                
                for upload in response['Upload']:
                    self.client.abort_multipart_upload(
                        Bucket=bucket,
                        Key=upload['Key'],
                        UploadId=upload['UploadId']
                    )
            
            print(f"✅ 清空存储桶：{bucket}")
        
        except Exception as e:
            print(f"⚠️  清空失败：{e}")
    
    def list_buckets(self) -> List[Dict]:
        """列出所有存储桶"""
        try:
            response = self.client.list_buckets()
            
            buckets = []
            for bucket in response.get('Buckets', []):
                buckets.append({
                    "name": bucket.get("Name"),
                    "region": bucket.get("Region", REGION),
                    "create_date": bucket.get("CreationDate"),
                    "storage_class": bucket.get("StorageClass", "STANDARD")
                })
            
            return buckets
        
        except CosServiceError as e:
            print(f"❌ 查询失败：{e}")
            return []
    
    def upload_file(self,
                   bucket: str,
                   local_path: str,
                   key: str = None,
                   storage_class: str = None,
                   progress_callback=None) -> Dict:
        """
        上传文件
        
        参数:
            bucket: 存储桶名称
            local_path: 本地文件路径
            key: COS 中的对象键 (默认使用文件名)
            storage_class: 存储类型
            progress_callback: 进度回调函数
        """
        if not os.path.exists(local_path):
            print(f"❌ 文件不存在：{local_path}")
            return {}
        
        if not key:
            key = os.path.basename(local_path)
        
        file_size = os.path.getsize(local_path)
        
        try:
            # 自动检测 MIME 类型
            content_type, _ = mimetypes.guess_type(local_path)
            if not content_type:
                content_type = "application/octet-stream"
            
            # 上传参数
            kwargs = {
                'Bucket': bucket,
                'LocalPath': local_path,
                'Key': key,
                'ContentType': content_type
            }
            
            if storage_class:
                kwargs['StorageClass'] = storage_class
            
            if progress_callback:
                kwargs['EnableMD5'] = True
            
            self.client.upload_file(**kwargs)
            
            print(f"✅ 上传成功：{key}")
            print(f"   存储桶：{bucket}")
            print(f"   大小：{self._format_size(file_size)}")
            if storage_class:
                print(f"   存储类型：{storage_class}")
            
            return {
                "bucket": bucket,
                "key": key,
                "size": file_size,
                "storage_class": storage_class or DEFAULT_STORAGE_CLASS
            }
        
        except CosClientError as e:
            print(f"❌ 上传失败：{e}")
            return {}
    
    def download_file(self,
                     bucket: str,
                     key: str,
                     local_path: str = None,
                     progress_callback=None) -> str:
        """
        下载文件
        
        参数:
            bucket: 存储桶名称
            key: 对象键
            local_path: 本地保存路径 (默认当前目录)
            progress_callback: 进度回调函数
        """
        if not local_path:
            local_path = os.path.basename(key)
        
        try:
            kwargs = {
                'Bucket': bucket,
                'Key': key,
                'DestFilePath': local_path
            }
            
            if progress_callback:
                kwargs['EnableMD5'] = True
            
            self.client.download_file(**kwargs)
            
            file_size = os.path.getsize(local_path)
            print(f"✅ 下载成功：{local_path}")
            print(f"   大小：{self._format_size(file_size)}")
            
            return local_path
        
        except CosClientError as e:
            print(f"❌ 下载失败：{e}")
            return ""
    
    def batch_upload(self,
                    bucket: str,
                    files: List[str],
                    prefix: str = "",
                    storage_class: str = None,
                    max_workers: int = 5) -> Dict:
        """
        批量上传
        
        参数:
            bucket: 存储桶名称
            files: 文件路径列表
            prefix: COS 中的前缀路径
            storage_class: 存储类型
            max_workers: 最大并发数
        """
        pool = SimpleThreadPool(max_workers=max_workers)
        
        success_count = 0
        failed_count = 0
        
        for file_path in files:
            if not os.path.exists(file_path):
                print(f"⚠️  文件不存在：{file_path}")
                failed_count += 1
                continue
            
            key = prefix + os.path.basename(file_path)
            
            def upload_task(fp=file_path, k=key):
                nonlocal success_count, failed_count
                result = self.upload_file(bucket, fp, k, storage_class)
                if result:
                    success_count += 1
                else:
                    failed_count += 1
            
            pool.add_task(upload_task)
        
        pool.wait_completion()
        
        print(f"\n✅ 批量上传完成")
        print(f"   成功：{success_count}")
        print(f"   失败：{failed_count}")
        
        return {
            "success": success_count,
            "failed": failed_count,
            "total": len(files)
        }
    
    def list_objects(self,
                    bucket: str,
                    prefix: str = "",
                    max_keys: int = 100) -> List[Dict]:
        """列出对象"""
        try:
            response = self.client.list_objects(
                Bucket=bucket,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            objects = []
            for obj in response.get('Contents', []):
                objects.append({
                    "key": obj.get("Key"),
                    "size": obj.get("Size", 0),
                    "last_modified": obj.get("LastModified"),
                    "storage_class": obj.get("StorageClass", "STANDARD"),
                    "etag": obj.get("ETag", "")
                })
            
            return objects
        
        except CosServiceError as e:
            print(f"❌ 查询失败：{e}")
            return []
    
    def delete_object(self, bucket: str, key: str):
        """删除对象"""
        try:
            self.client.delete_object(Bucket=bucket, Key=key)
            print(f"✅ 删除成功：{key}")
        
        except CosServiceError as e:
            print(f"❌ 删除失败：{e}")
    
    def put_lifecycle(self,
                     bucket: str,
                     rules: List[Dict]):
        """
        设置生命周期规则
        
        参数:
            bucket: 存储桶名称
            rules: 生命周期规则列表
                   [{
                       "id": "rule1",
                       "prefix": "tick/",
                       "status": "Enabled",
                       "transitions": [
                           {"days": 7, "storage_class": "STANDARD_IA"},
                           {"days": 30, "storage_class": "ARCHIVE"}
                       ]
                   }]
        """
        try:
            lifecycle_config = {
                'Rule': []
            }
            
            for rule in rules:
                rule_config = {
                    'ID': rule.get('id', f"rule-{len(lifecycle_config['Rule'])}"),
                    'Status': rule.get('status', 'Enabled'),
                    'Filter': {
                        'Prefix': rule.get('prefix', '')
                    }
                }
                
                # 添加转换规则
                if 'transitions' in rule:
                    rule_config['Transition'] = []
                    for transition in rule['transitions']:
                        rule_config['Transition'].append({
                            'Days': transition['days'],
                            'StorageClass': transition['storage_class']
                        })
                
                # 添加过期规则
                if 'expiration_days' in rule:
                    rule_config['Expiration'] = {
                        'Days': rule['expiration_days']
                    }
                
                lifecycle_config['Rule'].append(rule_config)
            
            self.client.put_bucket_lifecycle(
                Bucket=bucket,
                Configuration=lifecycle_config
            )
            
            print(f"✅ 设置生命周期规则成功：{bucket}")
            for rule in rules:
                print(f"   规则：{rule.get('id', 'N/A')}")
                if 'transitions' in rule:
                    for t in rule['transitions']:
                        print(f"     - {t['days']} 天后转为 {t['storage_class']}")
                if 'expiration_days' in rule:
                    print(f"     - {rule['expiration_days']} 天后删除")
        
        except CosServiceError as e:
            print(f"❌ 设置失败：{e}")
    
    def get_lifecycle(self, bucket: str) -> List[Dict]:
        """获取生命周期规则"""
        try:
            response = self.client.get_bucket_lifecycle(Bucket=bucket)
            
            rules = []
            for rule in response.get('Rule', []):
                rule_dict = {
                    'id': rule.get('ID'),
                    'prefix': rule.get('Filter', {}).get('Prefix', ''),
                    'status': rule.get('Status')
                }
                
                if 'Transition' in rule:
                    rule_dict['transitions'] = [
                        {
                            'days': t.get('Days'),
                            'storage_class': t.get('StorageClass')
                        }
                        for t in rule['Transition']
                    ]
                
                if 'Expiration' in rule:
                    rule_dict['expiration_days'] = rule['Expiration'].get('Days')
                
                rules.append(rule_dict)
            
            return rules
        
        except CosServiceError as e:
            print(f"❌ 获取失败：{e}")
            return []
    
    def get_bucket_info(self, bucket: str) -> Dict:
        """获取存储桶信息"""
        try:
            # 获取 ACL
            acl_response = self.client.get_bucket_acl(Bucket=bucket)
            
            # 获取位置
            location_response = self.client.get_bucket_location(Bucket=bucket)
            
            # 列出对象统计
            objects_response = self.client.list_objects(Bucket=bucket, MaxKeys=1)
            
            return {
                "bucket": bucket,
                "acl": acl_response.get('AccessControlList', []),
                "region": location_response.get('LocationConstraint', REGION),
                "has_objects": 'Contents' in objects_response and len(objects_response['Contents']) > 0
            }
        
        except CosServiceError as e:
            print(f"❌ 获取失败：{e}")
            return {}
    
    def _format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"


# ==================== 验证配置 ====================

def verify_config():
    """验证配置"""
    print("=" * 60)
    print("腾讯云 COS 配置验证")
    print("=" * 60)
    
    # 检查环境变量
    print("\n1. 环境变量检查:")
    print(f"   TENCENT_SECRET_ID: {'✅' if SECRET_ID else '❌'}")
    print(f"   TENCENT_SECRET_KEY: {'✅' if SECRET_KEY else '❌'}")
    print(f"   TENCENT_REGION: {REGION}")
    print(f"   DEFAULT_STORAGE_CLASS: {DEFAULT_STORAGE_CLASS}")
    
    if not SECRET_ID or not SECRET_KEY:
        print("\n❌ 请配置 .env 文件")
        return False
    
    # 验证凭证
    print("\n2. 凭证验证:")
    try:
        client = init_cos_client()
        
        # 列出存储桶来验证凭证
        response = client.list_buckets()
        buckets = response.get('Buckets', [])
        
        print(f"   ✅ 凭证验证成功")
        print(f"   ✅ 区域：{REGION}")
        print(f"   ✅ 存储桶数量：{len(buckets)}")
        
    except CosServiceError as e:
        print(f"   ❌ 凭证验证失败：{e}")
        return False
    
    print("\n✅ COS 配置验证通过")
    return True


# ==================== 主程序 ====================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "verify":
            verify_config()
        
        elif cmd == "list-buckets":
            cos = COSManager()
            buckets = cos.list_buckets()
            
            print("\n存储桶列表:")
            for bucket in buckets:
                print(f"  {bucket['name']} - {bucket['region']}")
        
        elif cmd == "list-objects":
            if len(sys.argv) < 3:
                print("用法：python3 cos_manager.py list-objects <bucket> [prefix]")
            else:
                bucket = sys.argv[2]
                prefix = sys.argv[3] if len(sys.argv) > 3 else ""
                
                cos = COSManager()
                objects = cos.list_objects(bucket, prefix)
                
                print(f"\n对象列表 ({bucket}, prefix='{prefix}'):")
                for obj in objects:
                    size = cos._format_size(obj['size'])
                    print(f"  {obj['key']} - {size} - {obj['storage_class']}")
        
        elif cmd == "cost-compare":
            storage_gb = float(sys.argv[2]) if len(sys.argv) > 2 else 100
            months = int(sys.argv[3]) if len(sys.argv) > 3 else 12
            
            cost_mgr = COSCostManager()
            cost_mgr.print_cost_comparison(storage_gb, months)
        
        else:
            print(f"未知命令：{cmd}")
    else:
        print("""
TencentCloud-COS - 腾讯云对象存储管理

用法:
  python3 cos_manager.py verify          # 验证配置
  python3 cos_manager.py list-buckets    # 列出存储桶
  python3 cos_manager.py list-objects <bucket> [prefix]  # 列出对象
  python3 cos_manager.py cost-compare [storage_gb] [months]  # 成本对比

示例:
  # 验证配置
  python3 cos_manager.py verify
  
  # 创建存储桶并上传文件
  python3 -c "
  from cos_manager import COSManager
  cos = COSManager()
  cos.create_bucket(bucket_name='my-data-bucket', storage_class='STANDARD')
  cos.upload_file('my-data-bucket.cos.ap-singapore.myqcloud.com', '/tmp/data.parquet', 'data/data.parquet')
  "
  
  # 设置生命周期规则
  python3 -c "
  from cos_manager import COSManager
  cos = COSManager()
  cos.put_lifecycle('my-data-bucket.cos.ap-singapore.myqcloud.com', [
      {
          'id': 'rule1',
          'prefix': 'data/',
          'transitions': [
              {'days': 7, 'storage_class': 'STANDARD_IA'},
              {'days': 30, 'storage_class': 'ARCHIVE'}
          ]
      }
  ])
  "
        """)
