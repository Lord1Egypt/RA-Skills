#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮储银行财资管理系统报文验证工具
支持：JSON Schema 校验、字段类型/长度/取值范围验证
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


class ValidationError(Exception):
    """验证异常"""
    def __init__(self, field: str, message: str, value: Any = None):
        self.field = field
        self.message = message
        self.value = value
        super().__init__(f"[{field}] {message}: {value}")


class PSBCValidator:
    """邮储财资报文验证器"""
    
    # 数据类型正则
    PATTERNS = {
        "AN": r"^[A-Za-z0-9]*$",           # 字母数字
        "A": r"^[A-Za-z]*$",                # 字母
        "N": r"^\d*$",                      # 数字
        "ANS": r"^[A-Za-z0-9\u4e00-\u9fa5]*$",  # 字母数字汉字
        "D": r"^\d+(\.\d+)?$",              # 浮点数
    }
    
    def __init__(self, apis_config: str = "apis.json"):
        """
        初始化验证器
        
        Args:
            apis_config: API 配置文件路径
        """
        with open(apis_config, "r", encoding="utf-8") as f:
            self.apis = json.load(f)
        self.api_map = {api["txCode"]: api for api in self.apis["apis"]}
    
    def validate(self, tx_code: str, data: Dict[str, Any], 
                 direction: str = "request") -> List[str]:
        """
        验证报文
        
        Args:
            tx_code: 交易码
            data: 报文数据
            direction: 方向（request/response）
        
        Returns:
            错误列表，空列表表示验证通过
        """
        errors = []
        
        if tx_code not in self.api_map:
            errors.append(f"未知的交易码：{tx_code}")
            return errors
        
        api = self.api_map[tx_code]
        spec = api.get(direction, {})
        fields = spec.get("businessFields", [])
        
        for field_spec in fields:
            field_id = field_spec["fieldId"]
            field_name = field_spec["name"]
            field_type = field_spec["type"]
            required = field_spec.get("required", False)
            
            value = data.get(field_id)
            
            # 必填性检查
            if required and (value is None or value == ""):
                errors.append(f"[{field_id}] 必填字段缺失：{field_name}")
                continue
            
            if value is None:
                continue
            
            # 类型验证
            try:
                self._validate_field(field_id, field_name, field_type, value, field_spec)
            except ValidationError as e:
                errors.append(str(e))
            
            # 枚举值检查
            if "enum" in field_spec:
                enum_values = field_spec["enum"]
                if isinstance(enum_values, dict):
                    if str(value) not in enum_values:
                        errors.append(f"[{field_id}] 值不在允许范围内：{value}，允许值：{list(enum_values.keys())}")
                elif isinstance(enum_values, list):
                    if value not in enum_values:
                        errors.append(f"[{field_id}] 值不在允许范围内：{value}，允许值：{enum_values}")
        
        return errors
    
    def _validate_field(self, field_id: str, field_name: str, 
                        field_type: str, value: Any, spec: Dict) -> None:
        """验证单个字段"""
        
        # 解析类型定义
        type_match = re.match(r"^([A-Z]+)(\.\.)?(\d+)(?:,(\d+))?$", field_type)
        if not type_match:
            # 特殊类型处理
            if field_type in ["JsonArray", "JsonObject", "list", "CLOB", "Int", "INT", "double", "long"]:
                return  # 复杂类型暂不验证
            return
        
        base_type = type_match.group(1)
        is_variable = type_match.group(2) == ".."
        max_length = int(type_match.group(3))
        precision = int(type_match.group(4)) if type_match.group(4) else None
        
        # 长度检查
        str_value = str(value)
        if not is_variable:
            # 定长
            if len(str_value) != max_length:
                raise ValidationError(field_id, f"长度应为{max_length}位", f"实际{len(str_value)}位")
        else:
            # 变长
            if len(str_value) > max_length:
                raise ValidationError(field_id, f"长度不能超过{max_length}位", f"实际{len(str_value)}位")
        
        # 类型检查
        if base_type == "N" and precision is None:
            # 整数
            if not re.match(r"^-?\d+$", str_value):
                raise ValidationError(field_id, "应为整数", value)
        
        elif base_type == "D" and precision:
            # 浮点数 D(m,n)
            if not re.match(r"^-?\d+(\.\d+)?$", str_value):
                raise ValidationError(field_id, "应为浮点数", value)
            if "." in str_value:
                decimal_part = str_value.split(".")[1]
                if len(decimal_part) > precision:
                    raise ValidationError(field_id, f"小数位数不能超过{precision}位", f"实际{len(decimal_part)}位")
        
        elif base_type == "AN":
            if not re.match(r"^[A-Za-z0-9]*$", str_value):
                raise ValidationError(field_id, "应只包含字母和数字", value)
        
        elif base_type == "ANS":
            if not re.match(r"^[A-Za-z0-9\u4e00-\u9fa5]*$", str_value):
                raise ValidationError(field_id, "应只包含字母、数字和汉字", value)
        
        # 日期格式检查
        if "Date" in field_name or "Time" in field_name or field_id in ["sendTime", "txStartDate", "txEndDate"]:
            self._validate_date(field_id, str_value, spec)
        
        # 金额检查
        if "Amt" in field_id or "Bal" in field_id or "Amount" in field_id:
            self._validate_amount(field_id, value)
    
    def _validate_date(self, field_id: str, value: str, spec: Dict) -> None:
        """验证日期格式"""
        formats = [
            ("%Y%m%d%H%M%S", "yyyyMMddHHmmss"),
            ("%Y%m%d%H%M%S%f", "yyyyMMddHHmmssSSS"),
            ("%Y%m%d", "yyyyMMdd"),
            ("%Y-%m-%d", "yyyy-MM-dd"),
            ("%H:%M", "HH:mm"),
        ]
        
        for fmt, desc in formats:
            try:
                datetime.strptime(value, fmt)
                return
            except ValueError:
                continue
        
        raise ValidationError(field_id, f"日期格式错误，应为 {desc}", value)
    
    def _validate_amount(self, field_id: str, value: Any) -> None:
        """验证金额"""
        try:
            amount = float(value)
            if amount < 0:
                raise ValidationError(field_id, "金额不能为负数", value)
            if amount > 999999999999999999.99:
                raise ValidationError(field_id, "金额超出最大范围", value)
        except (ValueError, TypeError):
            raise ValidationError(field_id, "金额应为数字", value)
    
    def validate_tx_comm(self, data: Dict[str, Any], security_level: str = "10") -> List[str]:
        """
        验证公共请求参数 (txComm)
        
        Args:
            data: 请求数据
            security_level: 安全级别
        
        Returns:
            错误列表
        """
        errors = []
        tx_comm = data.get("txComm", {})
        
        # 必填字段
        required_fields = ["sysTrackNo", "reqSysCode", "txCode", "txTime", "securityLevel", "sign", "userCertSN"]
        for field in required_fields:
            if field not in tx_comm:
                errors.append(f"txComm 缺少必填字段：{field}")
        
        # 系统跟踪号长度检查
        sys_track_no = tx_comm.get("sysTrackNo", "")
        if len(sys_track_no) != 32:
            errors.append(f"系统跟踪号应为 32 位，实际{len(sys_track_no)}位")
        
        # 接入系统代码长度检查
        req_sys_code = tx_comm.get("reqSysCode", "")
        if len(req_sys_code) != 12:
            errors.append(f"接入系统代码应为 12 位，实际{len(req_sys_code)}位")
        
        # 交易码长度检查
        tx_code = tx_comm.get("txCode", "")
        if len(tx_code) != 6:
            errors.append(f"交易码应为 6 位，实际{len(tx_code)}位")
        
        # 请求时间格式检查
        tx_time = tx_comm.get("txTime", "")
        if not re.match(r"^\d{17}$", tx_time):
            errors.append(f"请求时间格式错误，应为 yyyyMMddHHmmssSSS")
        
        # 安全级别检查
        sec_level = tx_comm.get("securityLevel", "")
        if sec_level not in ["10", "15"]:
            errors.append(f"安全级别应为 10 或 15，实际{sec_level}")
        
        # 安全级别 10 的特殊字段
        if security_level == "10":
            if "bankCertSN" not in tx_comm:
                errors.append("安全级别 10 时 bankCertSN 为必填")
            if "encData" not in tx_comm:
                errors.append("安全级别 10 时 encData 为必填")
            if "encKey" not in tx_comm:
                errors.append("安全级别 10 时 encKey 为必填")
        
        return errors


def interactive_validate():
    """交互式验证模式"""
    print("=" * 60)
    print("邮储银行财资管理系统 - 报文验证工具")
    print("=" * 60)
    
    validator = PSBCValidator()
    
    # 列出所有接口
    print("\n可用接口列表:")
    for api in validator.apis["apis"]:
        print(f"  {api['txCode']} - {api['name']}")
    
    print("\n请输入交易码（或输入 'q' 退出）: ", end="")
    tx_code = input().strip()
    
    if tx_code.lower() == 'q':
        return
    
    if tx_code not in validator.api_map:
        print(f"错误：未知的交易码 {tx_code}")
        return
    
    print("\n请输入请求报文 JSON（支持多行，输入空行结束）:")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    
    try:
        data = json.loads("\n".join(lines))
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误：{e}")
        return
    
    # 验证
    print("\n验证结果:")
    errors = validator.validate(tx_code, data, "request")
    
    # 验证 txComm
    if "txComm" in data:
        tx_comm_errors = validator.validate_tx_comm(data)
        errors.extend(tx_comm_errors)
    
    if errors:
        print(f"\n❌ 发现 {len(errors)} 个错误:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
    else:
        print("\n✅ 验证通过！报文格式正确。")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_validate()
    else:
        # 示例验证
        validator = PSBCValidator()
        
        # 测试用例：余额查询
        test_data = {
            "txCode": "100016",
            "tenantID": "eam_tenant_a_0001",
            "sendTime": "20250318163811",
            "srcSysId": "140001",
            "bankAccno": "951011013000006323"
        }
        
        errors = validator.validate("601118", test_data, "request")
        
        if errors:
            print("验证失败:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✅ 验证通过！")
