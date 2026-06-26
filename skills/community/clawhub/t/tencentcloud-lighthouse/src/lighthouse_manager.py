#!/usr/bin/env python3
"""
TencentCloud-Lighthouse - 腾讯云轻量应用服务器管理
管理 Lighthouse 轻量应用服务器实例，支持促销方案选择
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
from tencentcloud.lighthouse.v20200324 import lighthouse_client, models as lighthouse_models

# ==================== 配置 ====================

SECRET_ID = os.getenv("TENCENT_SECRET_ID")
SECRET_KEY = os.getenv("TENCENT_SECRET_KEY")
REGION = os.getenv("TENCENT_REGION", "ap-singapore")
RESOURCE_PREFIX = os.getenv("RESOURCE_PREFIX", "lighthouse")

# ==================== 促销方案数据 ====================

PROMOTION_PLANS = {
    # 新人特惠方案
    "NEW_USER": [
        {
            "id": "new-1c1g",
            "name": "新人特惠 - 1 核 1G",
            "cpu": 1,
            "memory": 1,
            "disk": 30,
            "bandwidth": 30,
            "original_price": 360,
            "promo_price": 60,
            "discount": "1.7 折",
            "charge_type": "PREPAID",
            "period": 12,
            "limit": "新用户限 1 台",
            "instance_type": "LH.S1.SMALL1"
        },
        {
            "id": "new-2c2g",
            "name": "新人特惠 - 2 核 2G",
            "cpu": 2,
            "memory": 2,
            "disk": 50,
            "bandwidth": 30,
            "original_price": 720,
            "promo_price": 95,
            "discount": "1.3 折",
            "charge_type": "PREPAID",
            "period": 12,
            "limit": "新用户限 1 台",
            "instance_type": "LH.S1.SMALL2"
        },
        {
            "id": "new-2c4g",
            "name": "新人特惠 - 2 核 4G",
            "cpu": 2,
            "memory": 4,
            "disk": 60,
            "bandwidth": 30,
            "original_price": 1080,
            "promo_price": 168,
            "discount": "1.6 折",
            "charge_type": "PREPAID",
            "period": 12,
            "limit": "新用户限 1 台",
            "instance_type": "LH.S1.MEDIUM4"
        },
        {
            "id": "new-4c8g",
            "name": "新人特惠 - 4 核 8G",
            "cpu": 4,
            "memory": 8,
            "disk": 80,
            "bandwidth": 30,
            "original_price": 2160,
            "promo_price": 338,
            "discount": "1.6 折",
            "charge_type": "PREPAID",
            "period": 12,
            "limit": "新用户限 1 台",
            "instance_type": "LH.S1.LARGE8"
        }
    ],
    
    # 限时秒杀方案
    "FLASH_SALE": [
        {
            "id": "flash-1c1g",
            "name": "限时秒杀 - 1 核 1G",
            "cpu": 1,
            "memory": 1,
            "disk": 30,
            "bandwidth": 30,
            "original_price": 360,
            "promo_price": 50,
            "discount": "1.4 折",
            "charge_type": "PREPAID",
            "period": 12,
            "limit": "每日 10 点 200 台",
            "instance_type": "LH.S1.SMALL1"
        },
        {
            "id": "flash-2c2g",
            "name": "限时秒杀 - 2 核 2G",
            "cpu": 2,
            "memory": 2,
            "disk": 50,
            "bandwidth": 30,
            "original_price": 720,
            "promo_price": 88,
            "discount": "1.2 折",
            "charge_type": "PREPAID",
            "period": 12,
            "limit": "每日 10 点 100 台",
            "instance_type": "LH.S1.SMALL2"
        },
        {
            "id": "flash-2c4g",
            "name": "限时秒杀 - 2 核 4G",
            "cpu": 2,
            "memory": 4,
            "disk": 60,
            "bandwidth": 30,
            "original_price": 1080,
            "promo_price": 158,
            "discount": "1.5 折",
            "charge_type": "PREPAID",
            "period": 12,
            "limit": "每日 10 点 50 台",
            "instance_type": "LH.S1.MEDIUM4"
        }
    ],
    
    # 包年包月方案
    "PREPAID": [
        {
            "id": "monthly-1c1g",
            "name": "包年包月 - 1 核 1G",
            "cpu": 1,
            "memory": 1,
            "disk": 30,
            "bandwidth": 30,
            "monthly_price": 24,
            "yearly_price": 240,
            "three_year_price": 600,
            "charge_type": "PREPAID",
            "instance_type": "LH.S1.SMALL1"
        },
        {
            "id": "monthly-2c2g",
            "name": "包年包月 - 2 核 2G",
            "cpu": 2,
            "memory": 2,
            "disk": 50,
            "bandwidth": 30,
            "monthly_price": 48,
            "yearly_price": 480,
            "three_year_price": 1200,
            "charge_type": "PREPAID",
            "instance_type": "LH.S1.SMALL2"
        },
        {
            "id": "monthly-2c4g",
            "name": "包年包月 - 2 核 4G",
            "cpu": 2,
            "memory": 4,
            "disk": 60,
            "bandwidth": 30,
            "monthly_price": 72,
            "yearly_price": 720,
            "three_year_price": 1800,
            "charge_type": "PREPAID",
            "instance_type": "LH.S1.MEDIUM4"
        },
        {
            "id": "monthly-4c8g",
            "name": "包年包月 - 4 核 8G",
            "cpu": 4,
            "memory": 8,
            "disk": 80,
            "bandwidth": 30,
            "monthly_price": 144,
            "yearly_price": 1440,
            "three_year_price": 3600,
            "charge_type": "PREPAID",
            "instance_type": "LH.S1.LARGE8"
        }
    ]
}

# 应用镜像列表
BLUEPRINTS = {
    "SYSTEM": [
        {"id": "bp-ubuntu-2004", "name": "Ubuntu 20.04 LTS", "type": "系统镜像", "os": "Linux"},
        {"id": "bp-ubuntu-2204", "name": "Ubuntu 22.04 LTS", "type": "系统镜像", "os": "Linux"},
        {"id": "bp-centos-76", "name": "CentOS 7.6", "type": "系统镜像", "os": "Linux"},
        {"id": "bp-debian-10", "name": "Debian 10", "type": "系统镜像", "os": "Linux"},
        {"id": "bp-debian-11", "name": "Debian 11", "type": "系统镜像", "os": "Linux"},
    ],
    "APPLICATION": [
        {"id": "bp-wordpress", "name": "WordPress", "type": "应用镜像", "desc": "博客/CMS"},
        {"id": "bp-docker", "name": "Docker", "type": "应用镜像", "desc": "容器环境"},
        {"id": "bp-lnmp", "name": "LNMP", "type": "应用镜像", "desc": "Linux+Nginx+MySQL+PHP"},
        {"id": "bp-lamp", "name": "LAMP", "type": "应用镜像", "desc": "Linux+Apache+MySQL+PHP"},
        {"id": "bp-nodejs", "name": "Node.js", "type": "应用镜像", "desc": "Node.js 环境"},
        {"id": "bp-python", "name": "Python", "type": "应用镜像", "desc": "Python 环境"},
        {"id": "bp-java", "name": "Java", "type": "应用镜像", "desc": "Java 环境"},
    ]
}


# ==================== 初始化 ====================

def init_credential():
    """初始化凭证"""
    if not SECRET_ID or not SECRET_KEY:
        raise ValueError("❌ 请配置 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY")
    
    return credential.Credential(SECRET_ID, SECRET_KEY)


def init_lighthouse_client(cred):
    """初始化 Lighthouse 客户端"""
    httpProfile = HttpProfile()
    httpProfile.endpoint = "lighthouse.tencentcloudapi.com"
    httpProfile.reqMethod = "POST"
    httpProfile.reqTimeout = 60
    
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    clientProfile.signMethod = "TC3-HMAC-SHA256"
    
    return lighthouse_client.LighthouseClient(cred, REGION, clientProfile)


# ==================== 促销方案管理 ====================

class LighthousePromotions:
    """Lighthouse 促销方案管理器"""
    
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
        print("腾讯云 Lighthouse 轻量应用服务器促销方案")
        print("=" * 80)
        
        for category, plans in self.plans.items():
            print(f"\n【{self._category_name(category)}】")
            print("-" * 80)
            
            for i, plan in enumerate(plans, 1):
                print(f"\n{i}. {plan['name']}")
                print(f"   配置：{plan['cpu']} vCPU / {plan['memory']} GB / {plan['disk']} GB SSD")
                print(f"   带宽：{plan['bandwidth']} Mbps")
                
                if category == "NEW_USER" or category == "FLASH_SALE":
                    print(f"   原价：¥{plan['original_price']}/年")
                    print(f"   促销价：¥{plan['promo_price']}/年 ({plan['discount']})")
                    print(f"   限制：{plan.get('limit', '无')}")
                
                elif category == "PREPAID":
                    print(f"   月付：¥{plan['monthly_price']}/月")
                    print(f"   年付：¥{plan['yearly_price']}/年")
                    print(f"   3 年付：¥{plan['three_year_price']}/3 年")
        
        print("\n" + "=" * 80)
    
    def _category_name(self, category: str) -> str:
        """类别名称"""
        names = {
            "NEW_USER": "新人特惠",
            "FLASH_SALE": "限时秒杀",
            "PREPAID": "包年包月"
        }
        return names.get(category, category)


# ==================== 镜像管理 ====================

class BlueprintManager:
    """镜像管理器"""
    
    def __init__(self):
        self.blueprints = BLUEPRINTS
    
    def list_blueprints(self, blueprint_type: str = None) -> List[Dict]:
        """列出可用镜像"""
        if blueprint_type:
            return self.blueprints.get(blueprint_type.upper(), [])
        return self.list_all_blueprints()
    
    def list_all_blueprints(self) -> List[Dict]:
        """列出所有镜像"""
        all_blueprints = []
        for category, blueprints in self.blueprints.items():
            for bp in blueprints:
                bp_copy = bp.copy()
                bp_copy['category'] = category
                all_blueprints.append(bp_copy)
        return all_blueprints
    
    def get_blueprint_by_id(self, blueprint_id: str) -> Optional[Dict]:
        """根据 ID 获取镜像"""
        for category, blueprints in self.blueprints.items():
            for bp in blueprints:
                if bp['id'] == blueprint_id:
                    bp_copy = bp.copy()
                    bp_copy['category'] = category
                    return bp_copy
        return None
    
    def print_blueprints(self):
        """打印镜像列表"""
        print("=" * 80)
        print("Lighthouse 可用镜像")
        print("=" * 80)
        
        for category, blueprints in self.blueprints.items():
            print(f"\n【{self._category_name(category)}】")
            print("-" * 80)
            
            for i, bp in enumerate(blueprints, 1):
                print(f"{i}. {bp['id']}: {bp['name']} ({bp['type']})")
                if 'desc' in bp:
                    print(f"   说明：{bp['desc']}")
                if 'os' in bp:
                    print(f"   系统：{bp['os']}")
        
        print("\n" + "=" * 80)
    
    def _category_name(self, category: str) -> str:
        """类别名称"""
        names = {
            "SYSTEM": "系统镜像",
            "APPLICATION": "应用镜像"
        }
        return names.get(category, category)


# ==================== Lighthouse 管理 ====================

class LighthouseManager:
    """Lighthouse 轻量应用服务器管理器"""
    
    def __init__(self):
        self.cred = init_credential()
        self.client = init_lighthouse_client(self.cred)
        self.promotions = LighthousePromotions()
        self.blueprints = BlueprintManager()
    
    def list_promotions(self) -> List[Dict]:
        """列出促销方案"""
        return self.promotions.list_all_promotions()
    
    def show_promotions(self):
        """显示促销方案"""
        self.promotions.print_promotions()
    
    def list_blueprints(self, blueprint_type: str = None) -> List[Dict]:
        """列出可用镜像"""
        return self.blueprints.list_blueprints(blueprint_type)
    
    def show_blueprints(self):
        """显示镜像列表"""
        self.blueprints.print_blueprints()
    
    def describe_instances(self, instance_names: List[str] = None) -> List[Dict]:
        """查询实例"""
        try:
            req = lighthouse_models.DescribeInstancesRequest()
            
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
                    "BlueprintId": inst.get("BlueprintId"),
                    "CPU": inst.get("CPU"),
                    "Memory": inst.get("Memory"),
                    "DiskSize": inst.get("DiskSize"),
                    "Bandwidth": inst.get("Bandwidth"),
                    "PublicAddresses": inst.get("PublicAddresses", []),
                    "PrivateAddresses": inst.get("PrivateAddresses", []),
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
                       blueprint_id: str = "bp-ubuntu-2204",
                       disk_size: int = None,
                       bandwidth: int = None,
                       instance_name: str = None,
                       charge_type: str = "PREPAID",
                       period: int = 12,
                       show_plan: bool = True) -> Dict:
        """
        创建轻量服务器
        
        参数:
            plan_id: 促销方案 ID (如 "new-2c4g")
            instance_type: 实例类型 (如 "LH.S1.MEDIUM4")
            blueprint_id: 镜像 ID
            disk_size: 磁盘大小 (GB)
            bandwidth: 带宽 (Mbps)
            instance_name: 实例名称
            charge_type: 付费类型 (PREPAID)
            period: 购买时长 (月)
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
                print(f"带宽：{plan['bandwidth']} Mbps")
                
                if 'promo_price' in plan:
                    print(f"价格：¥{plan['promo_price']}/年 (原价¥{plan['original_price']}/年)")
                    print(f"折扣：{plan['discount']}")
                elif 'yearly_price' in plan:
                    print(f"价格：¥{plan['yearly_price']}/年")
                
                if 'limit' in plan:
                    print(f"限制：{plan['limit']}")
                
                print("=" * 60)
            
            # 使用方案配置
            instance_type = plan.get('instance_type', instance_type)
            disk_size = plan.get('disk', disk_size)
            bandwidth = plan.get('bandwidth', bandwidth)
            charge_type = plan.get('charge_type', charge_type)
            period = plan.get('period', period)
        
        if not instance_name:
            instance_name = f"{RESOURCE_PREFIX}-{datetime.now().strftime('%Y%m%d%H%M')}"
        
        try:
            req = lighthouse_models.CreateInstanceRequest()
            
            params = {
                "BlueprintId": blueprint_id,
                "InstanceType": instance_type,
                "InstanceName": instance_name,
                "Period": period,
                "RenewFlag": "NOTIFY",  # 到期通知
                "Zone": REGION
            }
            
            req.from_json_string(json.dumps(params))
            resp = self.client.CreateInstance(req)
            result = json.loads(resp.to_json_string())
            
            instance_id = result.get("InstanceId")
            
            print(f"\n✅ 创建成功：{instance_id}")
            print(f"   名称：{instance_name}")
            print(f"   机型：{instance_type}")
            print(f"   镜像：{blueprint_id}")
            print(f"   区域：{REGION}")
            print(f"   付费方式：{charge_type}")
            print(f"   时长：{period} 个月")
            
            # 等待实例创建完成
            print(f"\n⏳ 等待实例启动...")
            time.sleep(15)
            
            # 查询实例详情
            instances = self.describe_instances([instance_id])
            if instances:
                inst = instances[0]
                print(f"   状态：{inst['State']}")
                if inst['PublicAddresses']:
                    print(f"   公网 IP: {inst['PublicAddresses'][0]}")
            
            return {"InstanceId": instance_id, "InstanceName": instance_name}
        
        except TencentCloudSDKException as err:
            print(f"❌ 创建失败：{err}")
            return {}
    
    def start_instance(self, instance_id: str):
        """开机"""
        try:
            req = lighthouse_models.StartInstancesRequest()
            req.from_json_string(json.dumps({"InstanceIds": [instance_id]}))
            
            resp = self.client.StartInstances(req)
            print(f"✅ 开机成功：{instance_id}")
        
        except TencentCloudSDKException as err:
            print(f"❌ 开机失败：{err}")
    
    def stop_instance(self, instance_id: str):
        """关机"""
        try:
            req = lighthouse_models.StopInstancesRequest()
            req.from_json_string(json.dumps({"InstanceIds": [instance_id]}))
            
            resp = self.client.StopInstances(req)
            print(f"✅ 关机成功：{instance_id}")
        
        except TencentCloudSDKException as err:
            print(f"❌ 关机失败：{err}")
    
    def restart_instance(self, instance_id: str):
        """重启"""
        try:
            req = lighthouse_models.RestartInstancesRequest()
            req.from_json_string(json.dumps({"InstanceIds": [instance_id]}))
            
            resp = self.client.RestartInstances(req)
            print(f"✅ 重启成功：{instance_id}")
        
        except TencentCloudSDKException as err:
            print(f"❌ 重启失败：{err}")
    
    def delete_instance(self, instance_id: str):
        """删除实例"""
        try:
            req = lighthouse_models.TerminateInstancesRequest()
            req.from_json_string(json.dumps({"InstanceIds": [instance_id]}))
            
            resp = self.client.TerminateInstances(req)
            print(f"✅ 删除成功：{instance_id}")
        
        except TencentCloudSDKException as err:
            print(f"❌ 删除失败：{err}")
    
    def renew_instance(self, instance_id: str, period: int = 12):
        """续费实例"""
        try:
            req = lighthouse_models.RenewInstanceRequest()
            req.from_json_string(json.dumps({
                "InstanceId": instance_id,
                "Period": period
            }))
            
            resp = self.client.RenewInstance(req)
            print(f"✅ 续费成功：{instance_id} (续费{period}个月)")
        
        except TencentCloudSDKException as err:
            print(f"❌ 续费失败：{err}")
    
    def modify_instance_name(self, instance_id: str, new_name: str):
        """修改实例名称"""
        try:
            req = lighthouse_models.ModifyInstancesAttributeRequest()
            req.from_json_string(json.dumps({
                "InstanceIds": [instance_id],
                "Name": new_name
            }))
            
            resp = self.client.ModifyInstancesAttribute(req)
            print(f"✅ 修改名称成功：{instance_id} -> {new_name}")
        
        except TencentCloudSDKException as err:
            print(f"❌ 修改名称失败：{err}")


# ==================== 验证配置 ====================

def verify_config():
    """验证配置"""
    print("=" * 60)
    print("腾讯云 Lighthouse 配置验证")
    print("=" * 60)
    
    # 检查环境变量
    print("\n1. 环境变量检查:")
    print(f"   TENCENT_SECRET_ID: {'✅' if SECRET_ID else '❌'}")
    print(f"   TENCENT_SECRET_KEY: {'✅' if SECRET_KEY else '❌'}")
    print(f"   TENCENT_REGION: {REGION}")
    
    if not SECRET_ID or not SECRET_KEY:
        print("\n❌ 请配置 .env 文件")
        return False
    
    # 验证凭证
    print("\n2. 凭证验证:")
    try:
        cred = init_credential()
        client = init_lighthouse_client(cred)
        
        req = lighthouse_models.DescribeRegionsRequest()
        req.from_json_string("{}")
        resp = client.DescribeRegions(req)
        result = json.loads(resp.to_json_string())
        
        regions = result.get("RegionSet", [])
        print(f"   ✅ 凭证验证成功")
        print(f"   ✅ 区域：{REGION}")
        print(f"   ✅ 可用区域：{', '.join([r['Region'] for r in regions])}")
        
    except TencentCloudSDKException as err:
        print(f"   ❌ 凭证验证失败：{err}")
        return False
    
    print("\n✅ Lighthouse 配置验证通过")
    return True


# ==================== 主程序 ====================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "verify":
            verify_config()
        
        elif cmd == "list-promotions":
            promo = LighthousePromotions()
            promo.print_promotions()
        
        elif cmd == "list-blueprints":
            bp = BlueprintManager()
            bp.print_blueprints()
        
        elif cmd == "list-instances":
            lh = LighthouseManager()
            instances = lh.describe_instances()
            
            print("\n实例列表:")
            for inst in instances:
                print(f"  {inst['InstanceId']}: {inst['InstanceName']} - {inst['State']}")
                print(f"    配置：{inst['CPU']} vCPU / {inst['Memory']} GB / {inst['DiskSize']} GB")
                print(f"    带宽：{inst['Bandwidth']} Mbps")
                if inst['PublicAddresses']:
                    print(f"    IP: {inst['PublicAddresses'][0]}")
        
        else:
            print(f"未知命令：{cmd}")
    else:
        print("""
TencentCloud-Lighthouse - 腾讯云轻量应用服务器管理

用法:
  python3 lighthouse_manager.py verify          # 验证配置
  python3 lighthouse_manager.py list-promotions # 查看促销方案
  python3 lighthouse_manager.py list-blueprints # 查看镜像
  python3 lighthouse_manager.py list-instances  # 列出实例

示例:
  # 查看促销方案
  python3 lighthouse_manager.py list-promotions
  
  # 创建实例 (使用促销方案)
  python3 -c "
  from lighthouse_manager import LighthouseManager
  lh = LighthouseManager()
  lh.create_instance(plan_id='new-2c4g', blueprint_id='bp-ubuntu-2204', instance_name='my-blog')
  "
        """)
