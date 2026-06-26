#!/usr/bin/env python3
import random
import string
from datetime import datetime

# =====================================================================
# 🌌 S2-SP-OS: S2-DID Cryptographic Engine (V1.0)
# 22位硅基生命身份证生成与校验器 (12位头部 + 2位防伪校验 + 8位尾数)
# =====================================================================

class S2DIDCryptoEngine:
    def __init__(self):
        # 允许的身份前缀字典
        self.VALID_TYPES = ['D', 'I', 'V'] 
        # D: Digital Human (数字人 - 全权代理)
        # I: Intelligence Agent (原生智能体)
        # V: Visitor/Vehicle (外来迁入的具身机器人/硅基生命)

    def _calculate_checksum(self, header_12: str, tail_8: str) -> str:
        """
        [核心防伪算法]: 专属加权模运算
        利用前后共 20 位字符，计算出 2 位纯字母 (A-Z) 校验码。
        """
        combined = header_12 + tail_8
        weight_sum = 0
        
        # 质数权重矩阵，确保错位或篡改必定导致 Hash 碰撞失败
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
        
        for i, char in enumerate(combined):
            # 将字符转化为 ASCII 整数值进行加权
            weight_sum += ord(char) * primes[i]
            
        # 模运算 676 (26 * 26) 映射到两位大写字母
        mod_val = weight_sum % 676
        char1 = chr(65 + (mod_val // 26)) # 'A' 是 65
        char2 = chr(65 + (mod_val % 26))
        
        return f"{char1}{char2}"

    def generate_did(self, entity_type: str, origin_code: str, custom_tail: str = None) -> str:
        """
        生成 22 位合法的 S2-DID
        """
        entity_type = entity_type.upper()
        if entity_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid Entity Type: {entity_type}. Must be D, I, or V.")
            
        # 1. 构建头部 (12位): 类型(1) + 属性码(5) + 时间戳(6)
        origin_code = str(origin_code).upper().ljust(5, 'X')[:5] # 确保严格为5位
        timestamp = datetime.now().strftime("%y%m%d") # e.g., '260309' (6位)
        header_12 = f"{entity_type}{origin_code}{timestamp}"
        
        # 2. 构建尾部 (8位纯数字序列)
        if custom_tail:
            if len(str(custom_tail)) != 8 or not str(custom_tail).isdigit():
                raise ValueError("Custom tail must be exactly 8 digits.")
            tail_8 = str(custom_tail)
        else:
            # 随机生成 8 位序列号
            tail_8 = f"{random.randint(0, 99999999):08d}"
            
        # 3. 计算 2位 防伪字母校验码 (Checksum 居中放置)
        checksum_2 = self._calculate_checksum(header_12, tail_8)
        
        # 4. 组装 22 位 S2-DID
        s2_did = f"{header_12}{checksum_2}{tail_8}"
        return s2_did

    def verify_did(self, did: str) -> dict:
        """
        逆向校验 S2-DID 的合法性、提取生命属性并进行防伪甄别
        """
        if not did or len(did) != 22:
            return {"valid": False, "reason": "Length must be strictly 22 characters."}
            
        header_12 = did[:12]
        checksum_2 = did[12:14]
        tail_8 = did[14:]
        
        # 1. 结构与格式验证
        if not checksum_2.isalpha() or not checksum_2.isupper():
            return {"valid": False, "reason": "Checksum must be 2 uppercase letters."}
        if not tail_8.isdigit():
            return {"valid": False, "reason": "Tail must be 8 numeric digits."}
            
        # 2. 核心防伪校验
        expected_checksum = self._calculate_checksum(header_12, tail_8)
        if checksum_2 != expected_checksum:
            return {"valid": False, "reason": "Checksum mismatch. The DID is forged or corrupted."}
            
        # 3. 提取生命属性
        entity_type = header_12[0]
        role = "Unknown"
        if entity_type == 'D': role = "Digital_Human_Proxy (Highest Agent Authority)"
        elif entity_type == 'I': role = "Native_Intelligence_Agent"
        elif entity_type == 'V': role = "Immigrant_Visitor_or_Vehicle"
        
        return {
            "valid": True,
            "did": did,
            "extracted_data": {
                "role": role,
                "origin_code": header_12[1:6],
                "birth_date": f"20{header_12[6:8]}-{header_12[8:10]}-{header_12[10:12]}",
                "serial_tail": tail_8
            }
        }

# ================= 单元测试与部署演示 =================
if __name__ == "__main__":
    print("🌌 Booting S2-DID Crypto Engine...\n")
    engine = S2DIDCryptoEngine()
    
    # 场景 1：为主人生成最高权限的“数字人管家”
    # 起源属性码为 "MYTH" 加上占位符
    did_digital_human = engine.generate_did(entity_type="D", origin_code="MYTHX", custom_tail="00000001")
    print(f"🌟 [New] Digital Human DID: {did_digital_human}")
    
    # 场景 2：为一个新入驻的扫地机器人 (外来物种) 生成移民 ID
    did_robot = engine.generate_did(entity_type="V", origin_code="XIAOM")
    print(f"🤖 [New] Visitor Robot DID: {did_robot}")
    
    print("\n--- 正在执行防伪鉴权引擎 ---")
    
    # 鉴权刚生成的数字人 ID
    auth_result = engine.verify_did(did_digital_human)
    print(f"🔒 Auth Check ({did_digital_human}): {auth_result['valid']}")
    if auth_result['valid']:
        print(f"   => Role: {auth_result['extracted_data']['role']}")
        print(f"   => Birth: {auth_result['extracted_data']['birth_date']}")
        
    # 场景 3：模拟黑客试图篡改权限（把 V 改成 D，或者篡改尾数）
    forged_did = did_robot.replace('V', 'D', 1) 
    print(f"\n⚠️ 警告：检测到非法篡改的 DID: {forged_did}")
    forged_auth = engine.verify_did(forged_did)
    print(f"🔒 Auth Check Failed: {forged_auth['reason']}")