#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮储银行财资管理系统接口调用示例
包含：报文加密/解密、签名/验签、HTTP 请求
"""

import json
import base64
import hashlib
import requests
from datetime import datetime
from typing import Dict, Any, Optional

# ==================== 配置区域 ====================
CONFIG = {
    "test": {
        "base_url": "https://olt.api-test.psbc.com:9902/gateway/std/",
        "req_sys_code": "99711940001",
        "user_cert_sn": "0817fbeecc848",
        "bank_cert_sn": "12e15039e89ff93c",
    },
    "staging": {
        "base_url": "https://olt.api-test.psbc.com:19902/gateway/std/",
    },
    "production": {
        "base_url": "https://api.psbc.com:443/gateway/std/",
    }
}

# ==================== 国密工具类（需替换为实际实现）====================
class SMCrypto:
    """
    国密算法工具类
    注意：实际使用时需要集成国密库，如 gmssl 或 pysm2
    """
    
    @staticmethod
    def sm4_encrypt(data: bytes, key: bytes) -> bytes:
        """SM4 加密"""
        # TODO: 使用实际国密库实现
        raise NotImplementedError("请集成国密库实现 SM4 加密")
    
    @staticmethod
    def sm4_decrypt(cipher: bytes, key: bytes) -> bytes:
        """SM4 解密"""
        # TODO: 使用实际国密库实现
        raise NotImplementedError("请集成国密库实现 SM4 解密")
    
    @staticmethod
    def sm2_sign(data: bytes, private_key: bytes) -> bytes:
        """SM2 签名"""
        # TODO: 使用实际国密库实现
        raise NotImplementedError("请集成国密库实现 SM2 签名")
    
    @staticmethod
    def sm2_verify(data: bytes, signature: bytes, public_key: bytes) -> bool:
        """SM2 验签"""
        # TODO: 使用实际国密库实现
        raise NotImplementedError("请集成国密库实现 SM2 验签")
    
    @staticmethod
    def sm3_hash(data: bytes) -> bytes:
        """SM3 哈希"""
        # TODO: 使用实际国密库实现
        raise NotImplementedError("请集成国密库实现 SM3 哈希")


# ==================== 报文处理类 ====================
class PSBCTreasuryClient:
    """邮储财资系统客户端"""
    
    def __init__(self, env: str = "test"):
        self.config = CONFIG.get(env, CONFIG["test"])
        self.base_url = self.config["base_url"]
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json;charset=UTF-8"
        })
    
    def generate_sys_track_no(self) -> str:
        """生成系统跟踪号：时间戳 (14 位) + 接入系统代码 (12 位) + 6 位唯一序列号"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:14]
        req_sys_code = self.config["req_sys_code"]
        unique_seq = f"{id(self) % 1000000:06d}"
        return f"{timestamp}{req_sys_code}{unique_seq}"
    
    def build_request(self, tx_code: str, business_data: Dict[str, Any], 
                      security_level: str = "10") -> Dict[str, Any]:
        """
        构建请求报文
        
        Args:
            tx_code: 交易码（6 位）
            business_data: 业务报文字典
            security_level: 安全级别（10 或 15）
        
        Returns:
            完整请求报文字典
        """
        tx_time = datetime.now().strftime("%Y%m%d%H%M%S%f")[:17]
        sys_track_no = self.generate_sys_track_no()
        
        # 业务报文转 JSON 字符串
        business_json = json.dumps(business_data, ensure_ascii=False, separators=(',', ':'))
        
        if security_level == "10":
            # 生成随机 SM4 密钥
            sm4_key = self._generate_sm4_key()
            
            # SM4 加密业务报文
            enc_data = SMCrypto.sm4_encrypt(business_json.encode('utf-8'), sm4_key)
            enc_data_b64 = base64.b64encode(enc_data).decode('ascii')
            
            # 使用银行证书加密 SM4 密钥
            enc_key = self._encrypt_sm4_key(sm4_key)
            enc_key_b64 = base64.b64encode(enc_key).decode('ascii')
            
            # 构建签名字符串
            sign_str = f"{sys_track_no}{self.config['req_sys_code']}{tx_code}{tx_time}{enc_data_b64}{enc_key_b64}"
            signature = SMCrypto.sm2_sign(sign_str.encode('utf-8'), self._get_private_key())
            sign_b64 = base64.b64encode(signature).decode('ascii')
            
            return {
                "txComm": {
                    "sysTrackNo": sys_track_no,
                    "reqSysCode": self.config["req_sys_code"],
                    "txCode": tx_code,
                    "txTime": tx_time,
                    "securityLevel": security_level,
                    "sign": sign_b64,
                    "bankCertSN": self.config["bank_cert_sn"],
                    "userCertSN": self.config["user_cert_sn"],
                    "encData": enc_data_b64,
                    "encKey": enc_key_b64
                }
            }
        
        elif security_level == "15":
            # 安全级别 15 仅签名，不加密
            sign_str = f"{sys_track_no}{self.config['req_sys_code']}{tx_code}{tx_time}"
            signature = SMCrypto.sm2_sign(sign_str.encode('utf-8'), self._get_private_key())
            sign_b64 = base64.b64encode(signature).decode('ascii')
            
            # 业务报文平铺
            request_data = {
                "txComm": {
                    "sysTrackNo": sys_track_no,
                    "reqSysCode": self.config["req_sys_code"],
                    "txCode": tx_code,
                    "txTime": tx_time,
                    "securityLevel": security_level,
                    "sign": sign_b64,
                    "userCertSN": self.config["user_cert_sn"]
                }
            }
            request_data.update(business_data)
            return request_data
        
        else:
            raise ValueError(f"不支持的安全级别：{security_level}")
    
    def send_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """发送 HTTP 请求"""
        response = self.session.post(self.base_url, json=request_data, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def parse_response(self, response_data: Dict[str, Any], 
                       security_level: str = "10") -> Dict[str, Any]:
        """
        解析响应报文
        
        Args:
            response_data: 原始响应数据
            security_level: 安全级别
        
        Returns:
            解析后的业务报文
        """
        tx_comm = response_data.get("txComm", {})
        resp_code = tx_comm.get("respCode", "")
        
        # 检查前置响应码
        if resp_code != "0000000000000000":
            raise Exception(f"请求失败：{tx_comm.get('respDesc', '未知错误')}")
        
        if security_level == "10":
            # 解密业务报文
            enc_data_b64 = tx_comm.get("encData", "")
            enc_data = base64.b64decode(enc_data_b64)
            sm4_key = self._decrypt_sm4_key(self._get_private_key())
            business_json = SMCrypto.sm4_decrypt(enc_data, sm4_key)
            return json.loads(business_json.decode('utf-8'))
        
        elif security_level == "15":
            # 安全级别 15，业务报文平铺
            business_data = {k: v for k, v in response_data.items() if k != "txComm"}
            return business_data
        
        else:
            raise ValueError(f"不支持的安全级别：{security_level}")
    
    # ==================== 辅助方法 ====================
    def _generate_sm4_key(self) -> bytes:
        """生成随机 SM4 密钥（16 字节）"""
        import os
        return os.urandom(16)
    
    def _encrypt_sm4_key(self, sm4_key: bytes) -> bytes:
        """使用银行证书公钥加密 SM4 密钥"""
        # TODO: 使用银行证书公钥进行 SM2 加密
        raise NotImplementedError("请实现银行证书公钥加密")
    
    def _decrypt_sm4_key(self, private_key: bytes) -> bytes:
        """使用私钥解密 SM4 密钥"""
        # TODO: 使用私钥进行 SM2 解密
        raise NotImplementedError("请实现私钥解密")
    
    def _get_private_key(self) -> bytes:
        """获取用户私钥"""
        # TODO: 从证书文件或密钥管理系统获取
        raise NotImplementedError("请配置用户私钥")


# ==================== 使用示例 ====================
def example_balance_query():
    """示例：账户余额实时查询（601118）"""
    client = PSBCTreasuryClient(env="test")
    
    # 构建业务报文
    business_data = {
        "txCode": "100016",
        "tenantID": "eam_tenant_a_0001",
        "sendTime": datetime.now().strftime("%Y%m%d%H%M%S"),
        "srcSysId": "140001",
        "bankAccno": "951011013000006323"
    }
    
    # 构建完整请求
    request_data = client.build_request(
        tx_code="601118",
        business_data=business_data,
        security_level="10"
    )
    
    print("请求报文:")
    print(json.dumps(request_data, indent=2, ensure_ascii=False))
    
    # 发送请求（需要实现国密算法后才能运行）
    # response_data = client.send_request(request_data)
    # business_response = client.parse_response(response_data)
    # print("响应报文:")
    # print(json.dumps(business_response, indent=2, ensure_ascii=False))


def example_payment_create():
    """示例：生成单笔支付申请单（601116）"""
    client = PSBCTreasuryClient(env="test")
    
    business_data = {
        "txCode": "100014",
        "tenantID": "eam_tenant_a_0001",
        "sendTime": datetime.now().strftime("%Y%m%d%H%M%S"),
        "srcSysId": "140001",
        "txType": "1",  # 对公支付
        "busiTypeCode": "002",  # 手续费
        "batchNo": "PAY202503180001",
        "payerAccno": "921026013000016778",
        "payAmt": "1000.00",
        "payType": "2",  # 预约支付
        "paymDate": "20250320",
        "fundsUsageInfo": "往来款",
        "payMode": "1",  # 账户
        "networkflagCode": "1",  # 直连
        "payeeAccno": "6217994660005823",
        "payeeAccname": "北京金帮伟业商贸中心",
        "recpayBankCnapsNo": "403100001082",
        "txPtscrt": "测试",
        "creatorName": "admin",
        "custFdsrcTpCd": "01"  # 普通支付单
    }
    
    request_data = client.build_request(
        tx_code="601116",
        business_data=business_data,
        security_level="10"
    )
    
    print("支付申请单请求报文:")
    print(json.dumps(request_data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    # 运行示例
    example_balance_query()
    print("\n" + "="*50 + "\n")
    example_payment_create()
