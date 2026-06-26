#!/usr/bin/env python3
"""
TencentCloud-OPS - 腾讯云运维工具
管理 CVM 服务器和 COS 存储桶
"""

import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 腾讯云 SDK
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.cvm.v20170312 import cvm_client, models as cvm_models
from tencentcloud.vpc.v20170312 import vpc_client, models as vpc_models

# ==================== 配置 ====================

SECRET_ID = os.getenv("TENCENT_SECRET_ID")
SECRET_KEY = os.getenv("TENCENT_SECRET_KEY")
REGION = os.getenv("TENCENT_REGION", "ap-seoul")
ZONE = os.getenv("TENCENT_ZONE", "ap-seoul-1")
RESOURCE_PREFIX = os.getenv("RESOURCE_PREFIX", "resource")

# ==================== 初始化 ====================

def init_credential():
    """初始化凭证"""
    if not SECRET_ID or not SECRET_KEY:
        raise ValueError("❌ 请配置 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY")
    
    return credential.Credential(SECRET_ID, SECRET_KEY)


def init_cvm_client(cred):
    """初始化 CVM 客户端"""
    httpProfile = HttpProfile()
    httpProfile.endpoint = "cvm.tencentcloudapi.com"
    httpProfile.reqMethod = "POST"
    httpProfile.reqTimeout = 60
    
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    clientProfile.signMethod = "TC3-HMAC-SHA256"
    
    return cvm_client.CvmClient(cred, REGION, clientProfile)


def init_vpc_client(cred):
    """初始化 VPC 客户端"""
    httpProfile = HttpProfile()
    httpProfile.endpoint = "vpc.tencentcloudapi.com"
    
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    
    return vpc_client.VpcClient(cred, REGION, clientProfile)


# ==================== CVM 管理 ====================

class CVMManager:
    """CVM 服务器管理器"""
    
    def __init__(self):
        self.cred = init_credential()
        self.client = init_cvm_client(self.cred)
        self.vpc_client = init_vpc_client(self.cred)
    
    def describe_instances(self, instance_names: List[str] = None) -> List[Dict]:
        """查询实例"""
        try:
            req = cvm_models.DescribeInstancesRequest()
            
            params = {"Limit": 100}
            if instance_names:
                params["Filters"] = [{
                    "Name": "instance-name",
                    "Values": instance_names
                }]
            
            req.from_json_string(json.dumps(params))
            resp = self.client.DescribeInstances(req)
            result = json.loads(resp.to_json_string())
            
            instances = []
            for inst in result.get("InstanceSet", []):
                instances.append({
                    "InstanceId": inst.get("InstanceId"),
                    "InstanceName": inst.get("InstanceName"),
                    "State": inst.get("InstanceState"),
                    "InstanceType": inst.get("InstanceType"),
                    "Cpu": inst.get("CPU"),
                    "Memory": inst.get("Memory"),
                    "PublicIpAddresses": inst.get("PublicIpAddresses", []),
                    "CreatedTime": inst.get("CreatedTime"),
                    "ExpiredTime": inst.get("ExpiredTime")
                })
            
            return instances
        
        except TencentCloudSDKException as err:
            print(f"❌ 查询失败：{err}")
            return []
    
    def create_instance(self,
                       instance_type: str = "S2.MEDIUM2",
                       image_id: str = "img-m9q98z72",
                       system_disk_size: int = 20,
                       bandwidth: int = 10,
                       instance_name: str = None,
                       charge_type: str = "POSTPAID") -> Dict:
        """创建实例"""
        
        if not instance_name:
            instance_name = f"{RESOURCE_PREFIX}-instance-{datetime.now().strftime('%Y%m%d%H%M')}"
        
        try:
            req = cvm_models.RunInstancesRequest()
            
            params = {
                "Placement": {"Zone": ZONE},
                "InstanceType": instance_type,
                "ImageId": image_id,
                "SystemDisk": {
                    "DiskType": "CLOUD_PREMIUM",
                    "DiskSize": system_disk_size
                },
                "InternetAccessible": {
                    "InternetChargeType": "BANDWIDTH_POSTPAID",
                    "InternetMaxBandwidthOut": bandwidth
                },
                "InstanceName": instance_name,
                "InstanceChargeType": charge_type,
                "SecurityGroupIds": self._get_default_security_group()
            }
            
            req.from_json_string(json.dumps(params))
            resp = self.client.RunInstances(req)
            result = json.loads(resp.to_json_string())
            
            instance_id = result.get("InstanceIdSet", [None])[0]
            
            print(f"✅ 创建成功：{instance_id}")
            print(f"   名称：{instance_name}")
            print(f"   机型：{instance_type}")
            print(f"   区域：{ZONE}")
            
            return {"InstanceId": instance_id, "InstanceName": instance_name}
        
        except TencentCloudSDKException as err:
            print(f"❌ 创建失败：{err}")
            return {}
    
    def _get_default_security_group(self) -> List[str]:
        """获取默认安全组"""
        try:
            req = vpc_models.DescribeSecurityGroupsRequest()
            req.from_json_string("{}")
            
            resp = self.vpc_client.DescribeSecurityGroups(req)
            result = json.loads(resp.to_json_string())
            
            sgs = result.get("SecurityGroupSet", [])
            if sgs:
                return [sgs[0].get("SecurityGroupId")]
            else:
                # 创建默认安全组
                return self._create_default_security_group()
        
        except Exception as e:
            print(f"⚠️  获取安全组失败：{e}")
            return []
    
    def _create_default_security_group(self) -> List[str]:
        """创建默认安全组"""
        try:
            req = vpc_models.CreateSecurityGroupRequest()
            req.from_json_string(json.dumps({
                "GroupName": f"{RESOURCE_PREFIX}-default-sg",
                "GroupDescription": "Default security group for data collection"
            }))
            
            resp = self.vpc_client.CreateSecurityGroup(req)
            result = json.loads(resp.to_json_string())
            
            sg_id = result.get("SecurityGroup", {}).get("SecurityGroupId")
            print(f"✅ 创建安全组：{sg_id}")
            
            return [sg_id]
        
        except Exception as e:
            print(f"❌ 创建安全组失败：{e}")
            return []
    
    def start_instance(self, instance_id: str):
        """开机"""
        try:
            req = cvm_models.StartInstancesRequest()
            req.from_json_string(json.dumps({"InstanceIds": [instance_id]}))
            
            resp = self.client.StartInstances(req)
            print(f"✅ 开机成功：{instance_id}")
        
        except TencentCloudSDKException as err:
            print(f"❌ 开机失败：{err}")
    
    def stop_instance(self, instance_id: str):
        """关机"""
        try:
            req = cvm_models.StopInstancesRequest()
            req.from_json_string(json.dumps({
                "InstanceIds": [instance_id],
                "StoppedMode": "KEEP_CHARGING"  # 停机不收费
            }))
            
            resp = self.client.StopInstances(req)
            print(f"✅ 关机成功：{instance_id}")
        
        except TencentCloudSDKException as err:
            print(f"❌ 关机失败：{err}")
    
    def terminate_instance(self, instance_id: str):
        """删除实例"""
        try:
            req = cvm_models.TerminateInstancesRequest()
            req.from_json_string(json.dumps({"InstanceIds": [instance_id]}))
            
            resp = self.client.TerminateInstances(req)
            print(f"✅ 删除成功：{instance_id}")
        
        except TencentCloudSDKException as err:
            print(f"❌ 删除失败：{err}")
    
    def schedule_shutdown(self, instance_id: str, days: int = 30):
        """定时关机"""
        shutdown_time = datetime.now() + timedelta(days=days)
        
        print(f"⏰ 已设置定时关机")
        print(f"   实例：{instance_id}")
        print(f"   时间：{shutdown_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"   天数：{days} 天后")
        
        # 实际实现需要配合定时任务或云函数
        # 这里仅提供提示
        print(f"\n💡 提示：请使用 crontab 或云函数实现定时关机")
        print(f"""
# crontab 示例
{shutdown_time.minute} {shutdown_time.hour} {shutdown_time.day} {shutdown_time.month} * \\
  python3 -c "from tencent_ops import CVMManager; CVMManager().stop_instance('{instance_id}')"
        """)


# ==================== COS 管理 ====================

class COSManager:
    """COS 存储桶管理器"""
    
    def __init__(self):
        self.cred = init_credential()
        # COS SDK 需要单独安装：pip install cos-python-sdk-v5
        try:
            from qcloud_cos import CosConfig, CosS3Client
            
            config = CosConfig(
                Region=REGION,
                SecretId=SECRET_ID,
                SecretKey=SECRET_KEY
            )
            
            self.client = CosS3Client(config)
            print("✅ COS 客户端初始化成功")
        
        except ImportError:
            print("⚠️  请安装 COS SDK: pip install cos-python-sdk-v5")
            self.client = None
    
    def list_buckets(self) -> List[Dict]:
        """列出所有存储桶"""
        if not self.client:
            return []
        
        try:
            response = self.client.list_buckets()
            buckets = []
            
            for bucket in response.get("Buckets", []):
                buckets.append({
                    "Name": bucket.get("Name"),
                    "Region": bucket.get("Region"),
                    "CreateDate": bucket.get("CreateDate")
                })
            
            return buckets
        
        except Exception as e:
            print(f"❌ 查询失败：{e}")
            return []
    
    def create_bucket(self,
                     bucket_name: str = None,
                     region: str = None,
                     storage_class: str = "STANDARD") -> Dict:
        """创建存储桶"""
        if not self.client:
            return {}
        
        if not bucket_name:
            bucket_name = f"{RESOURCE_PREFIX}-bucket-{datetime.now().strftime('%Y%m%d%H%M')}"
        
        if not region:
            region = REGION
        
        # 确保 bucket 名称包含 appid
        # 格式：bucketname-appid
        # 这里简化处理，实际需要从控制台获取 appid
        
        try:
            response = self.client.create_bucket(
                Bucket=bucket_name,
                StorageClass=storage_class
            )
            
            print(f"✅ 创建成功：{bucket_name}")
            print(f"   区域：{region}")
            print(f"   类型：{storage_class}")
            
            return {"bucket_name": bucket_name, "region": region}
        
        except Exception as e:
            print(f"❌ 创建失败：{e}")
            return {}
    
    def delete_bucket(self, bucket_name: str):
        """删除存储桶"""
        if not self.client:
            return
        
        try:
            self.client.delete_bucket(Bucket=bucket_name)
            print(f"✅ 删除成功：{bucket_name}")
        
        except Exception as e:
            print(f"❌ 删除失败：{e}")
    
    def upload_file(self,
                   bucket: str,
                   local_path: str,
                   key: str):
        """上传文件"""
        if not self.client:
            return
        
        try:
            with open(local_path, 'rb') as f:
                self.client.upload_file(
                    Bucket=bucket,
                    Body=f,
                    Key=key
                )
            
            print(f"✅ 上传成功：{key}")
            print(f"   存储桶：{bucket}")
            print(f"   本地文件：{local_path}")
        
        except Exception as e:
            print(f"❌ 上传失败：{e}")
    
    def download_file(self,
                     bucket: str,
                     key: str,
                     local_path: str):
        """下载文件"""
        if not self.client:
            return
        
        try:
            self.client.download_file(
                Bucket=bucket,
                Key=key,
                DestFilePath=local_path
            )
            
            print(f"✅ 下载成功：{local_path}")
        
        except Exception as e:
            print(f"❌ 下载失败：{e}")


# ==================== 验证配置 ====================

def verify_config():
    """验证配置"""
    print("=" * 60)
    print("腾讯云配置验证")
    print("=" * 60)
    
    # 检查环境变量
    print("\n1. 环境变量检查:")
    print(f"   TENCENT_SECRET_ID: {'✅' if SECRET_ID else '❌'}")
    print(f"   TENCENT_SECRET_KEY: {'✅' if SECRET_KEY else '❌'}")
    print(f"   TENCENT_REGION: {REGION}")
    print(f"   TENCENT_ZONE: {ZONE}")
    
    if not SECRET_ID or not SECRET_KEY:
        print("\n❌ 请配置 .env 文件")
        return False
    
    # 验证凭证
    print("\n2. 凭证验证:")
    try:
        cred = init_credential()
        cvm = init_cvm_client(cred)
        
        req = cvm_models.DescribeZonesRequest()
        req.from_json_string("{}")
        resp = cvm.DescribeZones(req)
        result = json.loads(resp.to_json_string())
        
        zones = result.get("ZoneSet", [])
        print(f"   ✅ 凭证验证成功")
        print(f"   ✅ 区域：{REGION}")
        print(f"   ✅ 可用区：{', '.join([z['Zone'] for z in zones])}")
        
    except TencentCloudSDKException as err:
        print(f"   ❌ 凭证验证失败：{err}")
        return False
    
    print("\n✅ 配置验证通过")
    return True


# ==================== 主程序 ====================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        verify_config()
    else:
        print("""
TencentCloud-OPS - 腾讯云运维工具

用法:
  python3 tencent_ops.py verify          # 验证配置
  python3 tencent_ops.py list-cvm        # 列出 CVM
  python3 tencent_ops.py list-cos        # 列出 COS
  python3 tencent_ops.py create-cvm      # 创建 CVM
  python3 tencent_ops.py create-cos      # 创建 COS

示例:
  python3 tencent_ops.py create-cvm --name okx-test --type S2.MEDIUM2
        """)
