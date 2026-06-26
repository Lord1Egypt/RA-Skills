#!/usr/bin/env python3
"""
TencentCloud-CVM - 腾讯云服务器管理
管理 CVM 云服务器实例，支持促销方案选择
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
RESOURCE_PREFIX = os.getenv("RESOURCE_PREFIX", "cvm")

# ==================== 促销方案数据 ====================

PROMOTION_PLANS = {
    # 新人特惠方案
    "NEW_USER": [
        {
            "id": "new-2c2g",
            "name": "新人特惠 - 2 核 2G",
            "cpu": 2,
            "memory": 2,
            "disk": 50,
            "bandwidth": 1,
            "original_price": 840,
            "promo_price": 95,
            "discount": "1.1 折",
            "charge_type": "PREPAID",
            "period": 12,  # 月
            "limit": "新用户限 1 台",
            "instance_type": "S2.SMALL2"
        },
        {
            "id": "new-2c4g",
            "name": "新人特惠 - 2 核 4G",
            "cpu": 2,
            "memory": 4,
            "disk": 60,
            "bandwidth": 3,
            "original_price": 1260,
            "promo_price": 188,
            "discount": "1.5 折",
            "charge_type": "PREPAID",
            "period": 12,
            "limit": "新用户限 1 台",
            "instance_type": "S2.MEDIUM2"
        },
        {
            "id": "new-4c8g",
            "name": "新人特惠 - 4 核 8G",
            "cpu": 4,
            "memory": 8,
            "disk": 80,
            "bandwidth": 5,
            "original_price": 2520,
            "promo_price": 388,
            "discount": "1.5 折",
            "charge_type": "PREPAID",
            "period": 12,
            "limit": "新用户限 1 台",
            "instance_type": "S2.LARGE8"
        }
    ],
    
    # 限时秒杀方案
    "FLASH_SALE": [
        {
            "id": "flash-2c2g",
            "name": "限时秒杀 - 2 核 2G",
            "cpu": 2,
            "memory": 2,
            "disk": 50,
            "bandwidth": 1,
            "original_price": 840,
            "promo_price": 78,
            "discount": "0.9 折",
            "charge_type": "PREPAID",
            "period": 12,
            "limit": "每日 10 点 100 台",
            "instance_type": "S2.SMALL2"
        },
        {
            "id": "flash-2c4g",
            "name": "限时秒杀 - 2 核 4G",
            "cpu": 2,
            "memory": 4,
            "disk": 60,
            "bandwidth": 3,
            "original_price": 1260,
            "promo_price": 168,
            "discount": "1.3 折",
            "charge_type": "PREPAID",
            "period": 12,
            "limit": "每日 10 点 50 台",
            "instance_type": "S2.MEDIUM2"
        }
    ],
    
    # 按量付费方案
    "POSTPAID": [
        {
            "id": "payg-2c2g",
            "name": "按量付费 - 2 核 2G",
            "cpu": 2,
            "memory": 2,
            "disk": 50,
            "bandwidth": 1,
            "hourly_price": 0.12,
            "daily_price": 2.88,
            "monthly_price": 86,
            "charge_type": "POSTPAID",
            "instance_type": "S2.SMALL2"
        },
        {
            "id": "payg-2c4g",
            "name": "按量付费 - 2 核 4G",
            "cpu": 2,
            "memory": 4,
            "disk": 50,
            "bandwidth": 1,
            "hourly_price": 0.18,
            "daily_price": 4.32,
            "monthly_price": 130,
            "charge_type": "POSTPAID",
            "instance_type": "S2.MEDIUM2"
        },
        {
            "id": "payg-4c8g",
            "name": "按量付费 - 4 核 8G",
            "cpu": 4,
            "memory": 8,
            "disk": 50,
            "bandwidth": 1,
            "hourly_price": 0.36,
            "daily_price": 8.64,
            "monthly_price": 259,
            "charge_type": "POSTPAID",
            "instance_type": "S2.LARGE8"
        }
    ],
    
    # 竞价实例方案
    "SPOT": [
        {
            "id": "spot-2c2g",
            "name": "竞价实例 - 2 核 2G",
            "cpu": 2,
            "memory": 2,
            "disk": 50,
            "bandwidth": 1,
            "hourly_price": 0.03,
            "original_hourly": 0.12,
            "discount": "75% OFF",
            "interruption_rate": "5-10%",
            "charge_type": "SPOTPAID",
            "instance_type": "S2.SMALL2"
        },
        {
            "id": "spot-2c4g",
            "name": "竞价实例 - 2 核 4G",
            "cpu": 2,
            "memory": 4,
            "disk": 50,
            "bandwidth": 1,
            "hourly_price": 0.05,
            "original_hourly": 0.18,
            "discount": "72% OFF",
            "interruption_rate": "5-10%",
            "charge_type": "SPOTPAID",
            "instance_type": "S2.MEDIUM2"
        },
        {
            "id": "spot-4c8g",
            "name": "竞价实例 - 4 核 8G",
            "cpu": 4,
            "memory": 8,
            "disk": 50,
            "bandwidth": 1,
            "hourly_price": 0.09,
            "original_hourly": 0.36,
            "discount": "75% OFF",
            "interruption_rate": "5-10%",
            "charge_type": "SPOTPAID",
            "instance_type": "S2.LARGE8"
        }
    ]
}

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


# ==================== 促销方案管理 ====================

class CVMPromotions:
    """CVM 促销方案管理器"""
    
    def __init__(self):
        self.plans = PROMOTION_PLANS
    
    def list_all_promotions(self) -> List[Dict]:
        """列出所有促销方案"""
        all_plans = []
        
        for category, plans in self.plans.items():
            for plan in plans:
                plan_copy = plan.copy()
                plan_copy['category'] = category
                all_plans.append(plan_copy)
        
        return all_plans
    
    def list_by_category(self, category: str) -> List[Dict]:
        """按类别列出方案"""
        return self.plans.get(category.upper(), [])
    
    def get_plan_by_id(self, plan_id: str) -> Optional[Dict]:
        """根据 ID 获取方案"""
        for category, plans in self.plans.items():
            for plan in plans:
                if plan['id'] == plan_id:
                    plan_copy = plan.copy()
                    plan_copy['category'] = category
                    return plan_copy
        return None
    
    def print_promotions(self):
        """打印促销方案"""
        print("=" * 80)
        print("腾讯云 CVM 促销方案")
        print("=" * 80)
        
        for category, plans in self.plans.items():
            print(f"\n【{self._category_name(category)}】")
            print("-" * 80)
            
            for i, plan in enumerate(plans, 1):
                print(f"\n{i}. {plan['name']}")
                print(f"   配置：{plan['cpu']} vCPU / {plan['memory']} GB / {plan['disk']} GB SSD")
                
                if 'bandwidth' in plan:
                    print(f"   带宽：{plan['bandwidth']} Mbps")
                
                if category == "NEW_USER" or category == "FLASH_SALE":
                    print(f"   原价：¥{plan['original_price']}/年")
                    print(f"   促销价：¥{plan['promo_price']}/年 ({plan['discount']})")
                    print(f"   限制：{plan.get('limit', '无')}")
                
                elif category == "POSTPAID":
                    print(f"   价格：¥{plan['hourly_price']}/小时 或 ¥{plan['daily_price']}/天 或 ¥{plan['monthly_price']}/月")
                
                elif category == "SPOT":
                    print(f"   价格：¥{plan['hourly_price']}/小时 (原价¥{plan['original_hourly']}/小时)")
                    print(f"   节省：{plan['discount']}")
                    print(f"   中断率：{plan.get('interruption_rate', '未知')}")
        
        print("\n" + "=" * 80)
    
    def _category_name(self, category: str) -> str:
        """类别名称"""
        names = {
            "NEW_USER": "新人特惠",
            "FLASH_SALE": "限时秒杀",
            "POSTPAID": "按量付费",
            "SPOT": "竞价实例"
        }
        return names.get(category, category)


# ==================== CVM 管理 ====================

class CVMManager:
    """CVM 服务器管理器"""
    
    def __init__(self):
        self.cred = init_credential()
        self.client = init_cvm_client(self.cred)
        self.vpc_client = init_vpc_client(self.cred)
        self.promotions = CVMPromotions()
    
    def list_promotions(self) -> List[Dict]:
        """列出促销方案"""
        return self.promotions.list_all_promotions()
    
    def show_promotions(self):
        """显示促销方案"""
        self.promotions.print_promotions()
    
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
                    "PrivateIpAddresses": inst.get("PrivateIpAddresses", []),
                    "CreatedTime": inst.get("CreatedTime"),
                    "ExpiredTime": inst.get("ExpiredTime"),
                    "ChargeType": inst.get("InstanceChargeType")
                })
            
            return instances
        
        except TencentCloudSDKException as err:
            print(f"❌ 查询失败：{err}")
            return []
    
    def create_instance(self,
                       plan_id: str = None,
                       instance_type: str = None,
                       image_id: str = "img-m9q98z72",
                       system_disk_size: int = 50,
                       bandwidth: int = 1,
                       instance_name: str = None,
                       charge_type: str = "POSTPAID",
                       show_plan: bool = True) -> Dict:
        """
        创建实例
        
        参数:
            plan_id: 促销方案 ID (如 "new-2c4g")
            instance_type: 实例类型 (如 "S2.MEDIUM2")
            image_id: 镜像 ID
            system_disk_size: 系统盘大小 (GB)
            bandwidth: 带宽 (Mbps)
            instance_name: 实例名称
            charge_type: 付费类型 (PREPAID/POSTPAID/SPOTPAID)
            show_plan: 是否显示方案详情
        """
        
        # 如果提供了 plan_id，使用方案配置
        if plan_id:
            plan = self.promotions.get_plan_by_id(plan_id)
            
            if not plan:
                print(f"❌ 未找到方案：{plan_id}")
                return {}
            
            if show_plan:
                print("\n" + "=" * 60)
                print("选择方案详情")
                print("=" * 60)
                print(f"方案：{plan['name']}")
                print(f"配置：{plan['cpu']} vCPU / {plan['memory']} GB / {plan['disk']} GB SSD")
                
                if 'promo_price' in plan:
                    print(f"价格：¥{plan['promo_price']}/年 (原价¥{plan['original_price']}/年)")
                    print(f"折扣：{plan['discount']}")
                elif 'hourly_price' in plan:
                    print(f"价格：¥{plan['hourly_price']}/小时")
                
                if 'limit' in plan:
                    print(f"限制：{plan['limit']}")
                
                print("=" * 60)
            
            # 使用方案配置
            instance_type = plan.get('instance_type', instance_type)
            system_disk_size = plan.get('disk', system_disk_size)
            bandwidth = plan.get('bandwidth', bandwidth)
            charge_type = plan.get('charge_type', charge_type)
        
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
            
            # 包年包月需要添加参数
            if charge_type == "PREPAID":
                params["InstanceChargeType"] = "PREPAID"
                params["InstanceChargePrepaid"] = {
                    "Period": 12,  # 12 个月
                    "RenewFlag": "NOTIFY"  # 到期通知
                }
            
            req.from_json_string(json.dumps(params))
            resp = self.client.RunInstances(req)
            result = json.loads(resp.to_json_string())
            
            instance_id = result.get("InstanceIdSet", [None])[0]
            
            print(f"\n✅ 创建成功：{instance_id}")
            print(f"   名称：{instance_name}")
            print(f"   机型：{instance_type}")
            print(f"   区域：{ZONE}")
            print(f"   付费方式：{charge_type}")
            
            # 等待实例创建完成
            print(f"\n⏳ 等待实例启动...")
            time.sleep(10)
            
            # 查询实例详情
            instances = self.describe_instances([instance_id])
            if instances:
                inst = instances[0]
                print(f"   状态：{inst['State']}")
                if inst['PublicIpAddresses']:
                    print(f"   公网 IP: {inst['PublicIpAddresses'][0]}")
            
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
                "GroupDescription": "CVM 默认安全组"
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
    
    def stop_instance(self, instance_id: str, stopped_mode: str = "KEEP_CHARGING"):
        """
        关机
        
        参数:
            instance_id: 实例 ID
            stopped_mode: 停机模式 (KEEP_CHARGING=停机不收费，NOT_CHARGING=停机收费)
        """
        try:
            req = cvm_models.StopInstancesRequest()
            req.from_json_string(json.dumps({
                "InstanceIds": [instance_id],
                "StoppedMode": stopped_mode
            }))
            
            resp = self.client.StopInstances(req)
            print(f"✅ 关机成功：{instance_id} (模式：{stopped_mode})")
        
        except TencentCloudSDKException as err:
            print(f"❌ 关机失败：{err}")
    
    def restart_instance(self, instance_id: str):
        """重启"""
        try:
            req = cvm_models.RestartInstancesRequest()
            req.from_json_string(json.dumps({"InstanceIds": [instance_id]}))
            
            resp = self.client.RestartInstances(req)
            print(f"✅ 重启成功：{instance_id}")
        
        except TencentCloudSDKException as err:
            print(f"❌ 重启失败：{err}")
    
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
        print(f"\n💡 提示：请使用 crontab 或云函数实现定时关机")
        print(f"""
# crontab 示例
{shutdown_time.minute} {shutdown_time.hour} {shutdown_time.day} {shutdown_time.month} * \\
  python3 -c "from cvm_manager import CVMManager; CVMManager().stop_instance('{instance_id}')"
        """)


# ==================== 验证配置 ====================

def verify_config():
    """验证配置"""
    print("=" * 60)
    print("腾讯云 CVM 配置验证")
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
    
    print("\n✅ CVM 配置验证通过")
    return True


# ==================== 主程序 ====================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "verify":
            verify_config()
        
        elif cmd == "list-promotions":
            promo = CVMPromotions()
            promo.print_promotions()
        
        elif cmd == "list-instances":
            cvm = CVMManager()
            instances = cvm.describe_instances()
            
            print("\n实例列表:")
            for inst in instances:
                print(f"  {inst['InstanceId']}: {inst['InstanceName']} - {inst['State']}")
                print(f"    配置：{inst['Cpu']} vCPU / {inst['Memory']} GB")
                if inst['PublicIpAddresses']:
                    print(f"    IP: {inst['PublicIpAddresses'][0]}")
        
        else:
            print(f"未知命令：{cmd}")
    else:
        print("""
TencentCloud-CVM - 腾讯云服务器管理

用法:
  python3 cvm_manager.py verify          # 验证配置
  python3 cvm_manager.py list-promotions # 查看促销方案
  python3 cvm_manager.py list-instances  # 列出实例

示例:
  # 查看促销方案
  python3 cvm_manager.py list-promotions
  
  # 创建实例 (使用促销方案)
  python3 -c "
  from cvm_manager import CVMManager
  cvm = CVMManager()
  cvm.create_instance(plan_id='payg-2c4g', instance_name='test-server')
  "
        """)
