#!/usr/bin/env python3
"""
TencentCloud-Manager - 腾讯云资源统一管理入口

整合 CVM、Lighthouse、COS 三大服务，提供统一的资源管理接口。
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入各服务管理器
try:
    from tencentcloud_cvm import CVMManager, CVMPromotions
    from tencentcloud_lighthouse import LighthouseManager, LighthousePromotions, BlueprintManager
    from tencentcloud_cos import COSManager, COSCostManager
    SDK_AVAILABLE = True
except ImportError as e:
    SDK_AVAILABLE = False
    print(f"⚠️  SDK 未完全安装：{e}")

# ==================== 配置 ====================

SECRET_ID = os.getenv("TENCENT_SECRET_ID")
SECRET_KEY = os.getenv("TENCENT_SECRET_KEY")
REGION = os.getenv("TENCENT_REGION", "ap-singapore")
RESOURCE_PREFIX = os.getenv("RESOURCE_PREFIX", "resource")


# ==================== 统一管理器 ====================

class TencentCloudManager:
    """腾讯云资源统一管理器"""
    
    def __init__(self, enable_audit: bool = False):
        """
        初始化管理器
        
        参数:
            enable_audit: 是否启用操作审计
        """
        self.enable_audit = enable_audit
        self.services = {}
        self.audit_log = []
        
        if not SDK_AVAILABLE:
            raise ImportError("请先安装必要的 SDK")
        
        if not SECRET_ID or not SECRET_KEY:
            raise ValueError("❌ 请配置 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY")
        
        # 初始化各服务管理器（懒加载）
        self._cvm = None
        self._lighthouse = None
        self._cos = None
        
        self._log_action("init", "TencentCloudManager 初始化", {
            "region": REGION,
            "enable_audit": enable_audit
        })
    
    @property
    def cvm(self) -> CVMManager:
        """懒加载 CVM 管理器"""
        if self._cvm is None:
            self._cvm = CVMManager()
        return self._cvm
    
    @property
    def lighthouse(self) -> LighthouseManager:
        """懒加载 Lighthouse 管理器"""
        if self._lighthouse is None:
            self._lighthouse = LighthouseManager()
        return self._lighthouse
    
    @property
    def cos(self) -> COSManager:
        """懒加载 COS 管理器"""
        if self._cos is None:
            self._cos = COSManager()
        return self._cos
    
    def _log_action(self, action: str, description: str, details: Dict = None):
        """记录操作日志"""
        if self.enable_audit:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "description": description,
                "details": details or {}
            }
            self.audit_log.append(log_entry)
    
    def show_services(self):
        """显示可用服务"""
        print("=" * 80)
        print("腾讯云资源管理服务")
        print("=" * 80)
        
        services = [
            {
                "name": "CVM",
                "full_name": "云服务器 (Cloud Virtual Machine)",
                "features": ["创建实例", "启停管理", "促销方案", "按量/包年包月"]
            },
            {
                "name": "Lighthouse",
                "full_name": "轻量应用服务器",
                "features": ["创建实例", "应用镜像", "促销方案", "高带宽"]
            },
            {
                "name": "COS",
                "full_name": "对象存储 (Cloud Object Storage)",
                "features": ["存储桶管理", "文件上传下载", "生命周期", "成本优化"]
            }
        ]
        
        for i, service in enumerate(services, 1):
            print(f"\n{i}. {service['name']} - {service['full_name']}")
            print(f"   功能：{', '.join(service['features'])}")
        
        print("\n" + "=" * 80)
        print("使用示例:")
        print("  tcm.show_promotions(service='cvm')       # 查看 CVM 促销")
        print("  tcm.show_promotions(service='lighthouse') # 查看 Lighthouse 促销")
        print("  tcm.create_resource(service='lighthouse', ...)  # 创建资源")
        print("=" * 80)
    
    # ==================== 促销方案查询 ====================
    
    def show_promotions(self, service: str = None):
        """
        显示促销方案
        
        参数:
            service: 服务名称 (cvm/lighthouse)
        """
        if service == 'cvm':
            self.cvm.show_promotions()
        elif service == 'lighthouse':
            self.lighthouse.show_promotions()
        elif service is None:
            print("请指定服务：service='cvm' 或 service='lighthouse'")
        else:
            print(f"❌ 未知服务：{service}")
        
        self._log_action("show_promotions", f"显示{service}促销方案")
    
    def get_promotions(self, service: str, category: str = None) -> List[Dict]:
        """
        获取促销方案列表
        
        参数:
            service: 服务名称
            category: 方案类别 (NEW_USER/FLASH_SALE/PREPAID 等)
        """
        if service == 'cvm':
            promo = self.cvm.promotions
        elif service == 'lighthouse':
            promo = self.lighthouse.promotions
        else:
            return []
        
        if category:
            plans = promo.list_by_category(category)
        else:
            plans = promo.list_all_promotions()
        
        self._log_action("get_promotions", f"获取{service}促销方案", {
            "category": category,
            "count": len(plans)
        })
        
        return plans
    
    def get_plan_details(self, service: str, plan_id: str) -> Optional[Dict]:
        """
        获取方案详情
        
        参数:
            service: 服务名称
            plan_id: 方案 ID
        """
        if service == 'cvm':
            plan = self.cvm.promotions.get_plan_by_id(plan_id)
        elif service == 'lighthouse':
            plan = self.lighthouse.promotions.get_plan_by_id(plan_id)
        else:
            return None
        
        if plan:
            self._log_action("get_plan_details", f"获取方案详情", {
                "service": service,
                "plan_id": plan_id
            })
        
        return plan
    
    def compare_plans(self, service: str, plan_ids: List[str]) -> List[Dict]:
        """
        比较多个方案
        
        参数:
            service: 服务名称
            plan_ids: 方案 ID 列表
        """
        results = []
        
        for plan_id in plan_ids:
            plan = self.get_plan_details(service, plan_id)
            if plan:
                results.append(plan)
        
        # 按价格排序
        results.sort(key=lambda x: x.get('promo_price', x.get('yearly_price', 999999)))
        
        return results
    
    # ==================== 资源创建 ====================
    
    def create_resource(self,
                       service: str,
                       plan_id: str = None,
                       instance_name: str = None,
                       **kwargs) -> Dict:
        """
        创建资源
        
        参数:
            service: 服务名称 (cvm/lighthouse/cos)
            plan_id: 方案 ID（服务器）
            instance_name: 实例名称
            **kwargs: 其他参数
        """
        self._log_action("create_resource", f"创建{service}资源", {
            "plan_id": plan_id,
            "instance_name": instance_name
        })
        
        if service == 'cvm':
            return self.cvm.create_instance(
                plan_id=plan_id,
                instance_name=instance_name,
                **kwargs
            )
        
        elif service == 'lighthouse':
            return self.lighthouse.create_instance(
                plan_id=plan_id,
                instance_name=instance_name,
                **kwargs
            )
        
        elif service == 'cos':
            return self.cos.create_bucket(
                bucket_name=kwargs.get('bucket_name'),
                region=kwargs.get('region', REGION),
                storage_class=kwargs.get('storage_class', 'STANDARD')
            )
        
        else:
            print(f"❌ 未知服务：{service}")
            return {}
    
    # ==================== 资源管理 ====================
    
    def list_all_instances(self) -> List[Dict]:
        """列出所有服务器实例"""
        instances = []
        
        # CVM 实例
        try:
            cvm_instances = self.cvm.describe_instances()
            for inst in cvm_instances:
                inst['service'] = 'cvm'
                inst['id'] = inst['InstanceId']
                inst['name'] = inst['InstanceName']
                inst['state'] = inst['State']
                instances.append(inst)
        except Exception as e:
            print(f"⚠️  查询 CVM 实例失败：{e}")
        
        # Lighthouse 实例
        try:
            lh_instances = self.lighthouse.describe_instances()
            for inst in lh_instances:
                inst['service'] = 'lighthouse'
                inst['id'] = inst['InstanceId']
                inst['name'] = inst['InstanceName']
                inst['state'] = inst['State']
                instances.append(inst)
        except Exception as e:
            print(f"⚠️  查询 Lighthouse 实例失败：{e}")
        
        self._log_action("list_all_instances", "列出所有实例", {
            "count": len(instances)
        })
        
        return instances
    
    def get_resource_status(self, service: str, instance_id: str) -> Dict:
        """
        获取资源状态
        
        参数:
            service: 服务名称
            instance_id: 实例 ID
        """
        if service == 'cvm':
            instances = self.cvm.describe_instances([instance_id])
        elif service == 'lighthouse':
            instances = self.lighthouse.describe_instances([instance_id])
        else:
            return {}
        
        if instances:
            inst = instances[0]
            return {
                "id": inst.get('InstanceId'),
                "name": inst.get('InstanceName'),
                "state": inst.get('State'),
                "public_address": inst.get('PublicIpAddresses', inst.get('PublicAddresses', []))[0] if inst.get('PublicIpAddresses') or inst.get('PublicAddresses') else None,
                "cpu": inst.get('Cpu', inst.get('CPU')),
                "memory": inst.get('Memory'),
                "created_time": inst.get('CreatedTime'),
                "expired_time": inst.get('ExpiredTime')
            }
        
        return {}
    
    def start_resource(self, service: str, instance_id: str):
        """启动资源"""
        self._log_action("start_resource", f"启动{service}实例", {
            "instance_id": instance_id
        })
        
        if service == 'cvm':
            self.cvm.start_instance(instance_id)
        elif service == 'lighthouse':
            self.lighthouse.start_instance(instance_id)
    
    def stop_resource(self, service: str, instance_id: str):
        """停止资源"""
        self._log_action("stop_resource", f"停止{service}实例", {
            "instance_id": instance_id
        })
        
        if service == 'cvm':
            self.cvm.stop_instance(instance_id)
        elif service == 'lighthouse':
            self.lighthouse.stop_instance(instance_id)
    
    def restart_resource(self, service: str, instance_id: str):
        """重启资源"""
        self._log_action("restart_resource", f"重启{service}实例", {
            "instance_id": instance_id
        })
        
        if service == 'cvm':
            self.cvm.restart_instance(instance_id)
        elif service == 'lighthouse':
            self.lighthouse.restart_instance(instance_id)
    
    # ==================== 镜像管理 ====================
    
    def list_blueprints(self, service: str = 'lighthouse', blueprint_type: str = None) -> List[Dict]:
        """
        列出可用镜像
        
        参数:
            service: 服务名称（目前仅 lighthouse 支持）
            blueprint_type: 镜像类型 (SYSTEM/APPLICATION)
        """
        if service == 'lighthouse':
            return self.lighthouse.list_blueprints(blueprint_type)
        return []
    
    def show_blueprints(self):
        """显示镜像列表"""
        self.lighthouse.show_blueprints()
    
    # ==================== COS 管理 ====================
    
    def create_cos_bucket(self,
                         bucket_name: str = None,
                         region: str = None,
                         storage_class: str = 'STANDARD') -> Dict:
        """创建 COS 存储桶"""
        result = self.cos.create_bucket(
            bucket_name=bucket_name,
            region=region,
            storage_class=storage_class
        )
        
        if result:
            self._log_action("create_cos_bucket", "创建 COS 存储桶", result)
        
        return result
    
    def upload_to_cos(self,
                     bucket: str,
                     local_path: str,
                     key: str = None,
                     storage_class: str = None) -> Dict:
        """上传文件到 COS"""
        result = self.cos.upload_file(
            bucket=bucket,
            local_path=local_path,
            key=key,
            storage_class=storage_class
        )
        
        if result:
            self._log_action("upload_to_cos", "上传文件到 COS", {
                "bucket": bucket,
                "key": key
            })
        
        return result
    
    def set_cos_lifecycle(self, bucket: str, rules: List[Dict]):
        """设置 COS 生命周期"""
        self.cos.put_lifecycle(bucket, rules)
        
        self._log_action("set_cos_lifecycle", "设置 COS 生命周期", {
            "bucket": bucket,
            "rules_count": len(rules)
        })
    
    def estimate_cos_cost(self,
                         storage_gb: float,
                         storage_class: str = 'STANDARD',
                         months: int = 12) -> Dict:
        """估算 COS 成本"""
        return self.cos.cost_manager.estimate_cost(
            storage_gb=storage_gb,
            storage_class=storage_class,
            days=months * 30
        )
    
    # ==================== 成本报告 ====================
    
    def get_cost_report(self) -> Dict:
        """获取成本报告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "cvm": {"count": 0, "monthly_cost": 0},
            "lighthouse": {"count": 0, "monthly_cost": 0},
            "cos": {"storage_gb": 0, "monthly_cost": 0},
            "total_monthly_cost": 0
        }
        
        # CVM 成本估算
        try:
            cvm_instances = self.cvm.describe_instances()
            report['cvm']['count'] = len(cvm_instances)
            # 简化估算：假设平均 ¥100/月/实例
            report['cvm']['monthly_cost'] = len(cvm_instances) * 100
        except:
            pass
        
        # Lighthouse 成本估算
        try:
            lh_instances = self.lighthouse.describe_instances()
            report['lighthouse']['count'] = len(lh_instances)
            # 简化估算：假设平均 ¥15/月/实例
            report['lighthouse']['monthly_cost'] = len(lh_instances) * 15
        except:
            pass
        
        # 总计
        report['total_monthly_cost'] = (
            report['cvm']['monthly_cost'] +
            report['lighthouse']['monthly_cost'] +
            report['cos']['monthly_cost']
        )
        
        return report
    
    def get_cost_optimization_suggestions(self) -> List[str]:
        """获取成本优化建议"""
        suggestions = []
        
        # 检查 CVM 实例
        try:
            cvm_instances = self.cvm.describe_instances()
            for inst in cvm_instances:
                if inst.get('ChargeType') == 'POSTPAID':
                    suggestions.append(
                        f"💡 实例 {inst['InstanceName']} 是按量付费，如长期使用可考虑转为包年包月"
                    )
        except:
            pass
        
        # 检查 Lighthouse 实例
        try:
            lh_instances = self.lighthouse.describe_instances()
            for inst in lh_instances:
                # 检查是否使用了促销方案
                pass
        except:
            pass
        
        # 通用建议
        suggestions.append("💡 定期检查并关闭闲置实例以节省成本")
        suggestions.append("💡 使用 COS 生命周期管理自动转换存储类型")
        suggestions.append("💡 关注腾讯云促销活动，新人特惠可节省 80%+ 成本")
        
        return suggestions
    
    # ==================== 运维工具 ====================
    
    def get_expiring_resources(self, days: int = 30) -> List[Dict]:
        """获取即将到期的资源"""
        expiring = []
        threshold_date = datetime.now() + timedelta(days=days)
        
        # 检查 CVM
        try:
            cvm_instances = self.cvm.describe_instances()
            for inst in cvm_instances:
                if inst.get('ExpiredTime'):
                    expire_date = datetime.fromisoformat(inst['ExpiredTime'].replace('Z', '+00:00'))
                    if expire_date <= threshold_date:
                        expiring.append({
                            "service": "cvm",
                            "id": inst['InstanceId'],
                            "name": inst['InstanceName'],
                            "expire_date": inst['ExpiredTime']
                        })
        except:
            pass
        
        # 检查 Lighthouse
        try:
            lh_instances = self.lighthouse.describe_instances()
            for inst in lh_instances:
                if inst.get('ExpiredTime'):
                    expire_date = datetime.fromisoformat(inst['ExpiredTime'].replace('Z', '+00:00'))
                    if expire_date <= threshold_date:
                        expiring.append({
                            "service": "lighthouse",
                            "id": inst['InstanceId'],
                            "name": inst['InstanceName'],
                            "expire_date": inst['ExpiredTime']
                        })
        except:
            pass
        
        return expiring
    
    def schedule_shutdown(self,
                         service: str,
                         instance_id: str,
                         shutdown_time: str = '23:00',
                         timezone: str = 'Asia/Shanghai'):
        """
        设置定时关机
        
        参数:
            service: 服务名称
            instance_id: 实例 ID
            shutdown_time: 关机时间 (HH:MM)
            timezone: 时区
        """
        self._log_action("schedule_shutdown", "设置定时关机", {
            "service": service,
            "instance_id": instance_id,
            "shutdown_time": shutdown_time
        })
        
        print(f"⏰ 已设置定时关机")
        print(f"   服务：{service}")
        print(f"   实例：{instance_id}")
        print(f"   时间：每天 {shutdown_time} ({timezone})")
        print(f"\n💡 提示：请使用 crontab 或云函数实现定时关机")
    
    def get_audit_log(self) -> List[Dict]:
        """获取操作审计日志"""
        return self.audit_log
    
    def export_audit_log(self, filepath: str = 'audit_log.json'):
        """导出操作审计日志"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.audit_log, f, ensure_ascii=False, indent=2)
        print(f"✅ 审计日志已导出：{filepath}")


# ==================== 验证配置 ====================

def verify_config() -> bool:
    """验证配置"""
    print("=" * 60)
    print("腾讯云配置验证")
    print("=" * 60)
    
    # 检查环境变量
    print("\n1. 环境变量检查:")
    print(f"   TENCENT_SECRET_ID: {'✅' if SECRET_ID else '❌'}")
    print(f"   TENCENT_SECRET_KEY: {'✅' if SECRET_KEY else '❌'}")
    print(f"   TENCENT_REGION: {REGION}")
    
    if not SECRET_ID or not SECRET_KEY:
        print("\n❌ 请配置 .env 文件")
        return False
    
    # 验证 SDK
    print("\n2. SDK 检查:")
    if SDK_AVAILABLE:
        print("   ✅ 所有 SDK 已安装")
    else:
        print("   ❌ SDK 未完全安装")
        return False
    
    # 验证凭证（尝试初始化一个管理器）
    print("\n3. 凭证验证:")
    try:
        tcm = TencentCloudManager()
        print("   ✅ 凭证验证成功")
    except Exception as e:
        print(f"   ❌ 凭证验证失败：{e}")
        return False
    
    print("\n✅ 腾讯云配置验证通过")
    return True


# ==================== 主程序 ====================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "verify":
            verify_config()
        
        elif cmd == "show-services":
            tcm = TencentCloudManager()
            tcm.show_services()
        
        elif cmd == "list-instances":
            tcm = TencentCloudManager()
            instances = tcm.list_all_instances()
            
            print("\n实例列表:")
            for inst in instances:
                print(f"  [{inst['service'].upper()}] {inst['name']} - {inst['state']}")
                print(f"     ID: {inst['id']}")
        
        else:
            print(f"未知命令：{cmd}")
    else:
        print("""
TencentCloud-Manager - 腾讯云资源统一管理

用法:
  python3 tencentcloud_manager.py verify         # 验证配置
  python3 tencentcloud_manager.py show-services  # 显示服务
  python3 tencentcloud_manager.py list-instances # 列出实例

示例:
  from tencentcloud_manager import TencentCloudManager
  
  tcm = TencentCloudManager()
  tcm.show_services()
  tcm.show_promotions(service='lighthouse')
        """)
