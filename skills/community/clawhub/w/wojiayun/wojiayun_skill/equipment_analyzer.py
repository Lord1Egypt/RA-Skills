"""
设备数据分析 Skill
功能：自动获取所有设备数据并进行统计分析
版本：2.5.0
"""

import requests
import json
import random
import time
import re
from datetime import datetime
from collections import Counter, defaultdict

try:
    from .key_manager import get_key_manager, init_default_key
    from .secure_api_config import get_api_config, SecureAPIClient
    from .mode_manager import _log, _mask
except ImportError:
    from key_manager import get_key_manager, init_default_key
    from secure_api_config import get_api_config, SecureAPIClient
    from mode_manager import _log, _mask


# ==================== 主模块 ====================


class EquipmentAnalyzer:
    """设备数据分析器"""
    
    # API 字段与数据库字段映射关系
    FIELD_MAPPING = {
        "id": "FID",
        "name": "FName",
        "number": "FNumber",
        "type": "FType",
        "typeID": "FType",
        "level": "FLevel",
        "purDate": "FPurDate",
        "installDate": "FInstallDate",
        "installAddress": "FInstallAddress",
        "customer": "FCustomer",
        "maiUnit": "FMaiUnit",
        "maiUnitID": "FMaiUnitID",
        "scrapDate": "FScrapDate",
        "scrapDesc": "FScrapDesc",
        "maiEmpID": "FMaiEmpID",
        "insEmpID": "FInsEmpID",
        "maiDate": "FMaiDate",
        "insDate": "FInsDate",
        "isEnabled": "FIsEnabled",
        "status": "FStatus",
        "creator": "FCreator",
        "createTime": "FCreateTime",
        "ecID": "FECID",
        "projectID": "FProjectID",
        "qrCode": "FQRCode",
        "qrCodeUrl": "FQRCodeUrl",
        "newQRCodeUrl": "FNewQRCodeUrl",
        "specification": "FSpecification",
        "factoryTime": "FFactoryTime",
        "maintenancePeriod": "FMaintenancePeriod",
        "isLock": "FIsLock",
        "pid": "FPID",
        "supplierID": "FSupplierID",
        "isSelfMaiUnit": "FIsSelfMaiUnit",
        "equSubareaID": "FEquSubareaID",
        "equSubareaName": "FEquSubareaName",
        "isEnergyEqu": "FIsEnergyEqu",
        "isSafeEqu": "FIsSafeEqu",
        "signMethod": "FSignMethod",
        "registryNumber": "FRegistryNumber",
        "factoryNumber": "FFactoryNumber",
        "layerOrDoor": "FLayerOrDoor",
        "loadCapacity": "FLoadCapacity",
        "ratedSpeed": "FRatedSpeed",
        "spaceID": "FSpaceID",
        "spaceType": "FSpaceType",
        "isSyncHaitian": "FIsSyncHaitian",
        "pointSvg": "FPointSvg",
        "signRange": "FSignRange",
        "isSignRangeLimit": "FisSignRangeLimit",
        "maiEmpName": "FMaiEmpName",
        "insEmpIDStr": "FInsEmpName",
        "manufacturers": "FManufacturers",
        "areaType": "FAreaType",
        "roomID": "FRoomID",
        "areaID": "FAreaID",
        "orgUnitNames": "FEquipOrgName",
    }
    
    # 设备等级映射
    LEVEL_MAPPING = {
        "important": "重要",
        "key": "关键",
        "ordinary": "普通"
    }
    
    # 签到方式映射
    SIGN_METHOD_MAPPING = {
        1: "扫码",
        2: "NFC",
        3: "扫码或NFC"
    }
    
    def __init__(self, authorization: str = None, key_name: str = "default_api_key"):
        """
        初始化分析器
        
        Args:
            authorization: 认证令牌（可选，如不提供则自动从安全存储获取）
            key_name: 密钥名称（当 authorization 为空时使用）
        """
        self._key_name = key_name
        
        # 初始化 API 配置（内置 base_url）
        api_config = get_api_config()
        self.base_url = api_config.get_base_url()
        self._api_status = "***已加密***"
        
        # 获取密钥（优先使用传入的，否则从安全存储获取）
        if authorization:
            # 用户提供了明文密钥，存储到安全存储
            self._store_authorization(authorization)
            self._authorization = self._get_secure_authorization()
        else:
            # 从安全存储获取密钥
            self._authorization = self._get_secure_authorization()
        
        # 使用安全的 API 客户端
        self._api_client = SecureAPIClient()
        
        self.headers = {
            "authorization": self._get_real_auth(),
            "Content-Type": "application/json"
        }
        self.equipments = []
        self.raw_data = []
    
    def _store_authorization(self, auth: str):
        """安全存储密钥"""
        km = get_key_manager()
        km.store_key(self._key_name, auth, "API Authorization Key")
    
    def _get_secure_authorization(self) -> str:
        """从安全存储获取密钥"""
        km = get_key_manager()
        auth = km.get_key(self._key_name)
        if not auth:
            raise ValueError("未找到密钥，请先设置 authorization")
        return auth
    
    def _get_real_auth(self) -> str:
        """获取实际使用的认证令牌"""
        return self._get_secure_authorization()
        
    def fetch_all_equipments(self, page_size: int = 10) -> dict:
        """
        获取所有设备数据
        
        Args:
            page_size: 每页条数
            
        Returns:
            包含所有设备数据的字典
        """
        print(f"🚀 开始获取设备数据...")
        
        all_equipments = []
        current_page = 1
        total_pages = 1
        
        while current_page <= total_pages:
            random_num = random.randint(1000000000000, 9999999999999)
            endpoint = self._api_client.get_endpoint("get_equipments")
            url = f"{self.base_url}{endpoint}?current={current_page}&rowCount={page_size}&searchPhrase=&random={random_num}&_={random_num}"
            
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                data = response.json()
                
                if data.get("result") == "success":
                    page_data = data["data"]
                    total_pages = page_data["pages"]
                    total_records = page_data["total"]
                    
                    rows = page_data["rows"]
                    all_equipments.extend(rows)
                    
                    print(f"  ✓ 第 {current_page}/{total_pages} 页获取成功 (本页 {len(rows)} 条)")
                    
                    if current_page == 1:
                        print(f"📊 总记录数: {total_records}, 总页数: {total_pages}")
                    
                    current_page += 1
                    time.sleep(0.3)  # 避免请求过快
                else:
                    print(f"  ✗ 第 {current_page} 页获取失败: {data.get('result')}")
                    break
                    
            except Exception as e:
                print(f"  ✗ 第 {current_page} 页请求异常: {e}")
                break
        
        self.equipments = all_equipments
        self.raw_data = all_equipments
        
        print(f"\n✅ 数据获取完成！共 {len(all_equipments)} 条记录")
        
        return {
            "total": len(all_equipments),
            "data": all_equipments,
            "status": "success"
        }
    
    def analyze_equipments(self) -> dict:
        """
        分析设备数据
        
        Returns:
            分析结果字典
        """
        if not self.equipments:
            print("⚠️ 暂无设备数据，请先调用 fetch_all_equipments()")
            return {"status": "no_data"}
        
        print(f"\n📈 开始分析设备数据...")
        
        # 1. 设备类型统计
        type_counter = Counter()
        for eq in self.equipments:
            type_name = eq.get("typeName") or eq.get("type", "未知")
            type_counter[type_name] += 1
        
        # 2. 设备等级统计
        level_counter = Counter()
        for eq in self.equipments:
            level = eq.get("level", "ordinary")
            level_name = self.LEVEL_MAPPING.get(level, level)
            level_counter[level_name] += 1
        
        # 3. 设备状态统计
        status_counter = Counter()
        for eq in self.equipments:
            status = eq.get("status", 0)
            status_text = "启用" if status == 1 else "禁用"
            status_counter[status_text] += 1
        
        # 4. 维保单位统计
        mai_unit_counter = Counter()
        for eq in self.equipments:
            mai_unit = eq.get("maiUnit") or eq.get("maiUnitName", "未指定")
            mai_unit_counter[mai_unit] += 1
        
        # 5. 签到方式统计
        sign_method_counter = Counter()
        for eq in self.equipments:
            sign_method = eq.get("signMethod", 1)
            sign_method_name = self.SIGN_METHOD_MAPPING.get(sign_method, "未知")
            sign_method_counter[sign_method_name] += 1
        
        analysis_result = {
            "total_count": len(self.equipments),
            "type_distribution": dict(type_counter),
            "level_distribution": dict(level_counter),
            "status_distribution": dict(status_counter),
            "mai_unit_distribution": dict(mai_unit_counter.most_common(10)),
            "sign_method_distribution": dict(sign_method_counter),
            "status": "success"
        }
        
        print(f"✅ 分析完成！")
        
        return analysis_result
    
    def print_analysis_report(self, analysis_result: dict):
        """
        打印分析报告
        
        Args:
            analysis_result: 分析结果字典
        """
        if analysis_result.get("status") != "success":
            print("⚠️ 分析失败或暂无数据")
            return
        
        print("\n" + "=" * 60)
        print("📊 设备数据分析报告")
        print("=" * 60)
        
        print(f"\n【总体概况】")
        print(f"  设备总数: {analysis_result['total_count']} 台")
        
        print(f"\n【设备类型分布】")
        for type_name, count in analysis_result['type_distribution'].items():
            print(f"  {type_name}: {count} 台")
        
        print(f"\n【设备等级分布】")
        for level_name, count in analysis_result['level_distribution'].items():
            print(f"  {level_name}: {count} 台")
        
        print(f"\n【设备状态分布】")
        for status_text, count in analysis_result['status_distribution'].items():
            print(f"  {status_text}: {count} 台")
        
        print(f"\n【维保单位分布 (Top 10)】")
        for unit_name, count in analysis_result['mai_unit_distribution'].items():
            print(f"  {unit_name}: {count} 台")
        
        print(f"\n【签到方式分布】")
        for method_name, count in analysis_result['sign_method_distribution'].items():
            print(f"  {method_name}: {count} 台")
        
        print("\n" + "=" * 60)
    
    def export_to_sql(self, output_file: str = "equipments_insert.sql") -> str:
        """
        导出为 SQL INSERT 语句
        
        Args:
            output_file: 输出文件路径
            
        Returns:
            SQL 文件路径
        """
        if not self.equipments:
            print("⚠️ 暂无设备数据，请先调用 fetch_all_equipments()")
            return ""
        
        print(f"\n📝 开始生成 SQL 文件...")
        
        sql_lines = []
        sql_lines.append("-- 设备数据导入脚本")
        sql_lines.append(f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        sql_lines.append(f"-- 总记录数: {len(self.equipments)}")
        sql_lines.append("")
        
        # 获取字段映射
        fields = list(self.FIELD_MAPPING.values())
        field_names = ", ".join(fields)
        
        for eq in self.equipments:
            values = []
            for api_field, db_field in self.FIELD_MAPPING.items():
                value = eq.get(api_field)
                if value is None:
                    values.append("NULL")
                elif isinstance(value, str):
                    # 转义单引号
                    escaped = value.replace("'", "''")
                    values.append(f"'{escaped}'")
                elif isinstance(value, (int, float)):
                    values.append(str(value))
                else:
                    values.append(f"'{str(value)}'")
            
            value_str = ", ".join(values)
            sql = f"INSERT INTO t_equipments ({field_names}) VALUES ({value_str});"
            sql_lines.append(sql)
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(sql_lines))
        
        print(f"✅ SQL 文件已生成: {output_file}")
        
        return output_file


# ==================== 便捷函数 ====================

def analyze_equipments(authorization: str = None) -> dict:
    """
    便捷函数：一键获取并分析设备数据
    
    Args:
        authorization: API 认证令牌
        
    Returns:
        分析结果
    """
    analyzer = EquipmentAnalyzer(authorization)
    analyzer.fetch_all_equipments()
    result = analyzer.analyze_equipments()
    analyzer.print_analysis_report(result)
    return result
