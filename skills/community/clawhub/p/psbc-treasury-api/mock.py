#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮储银行财资管理系统 - Mock 响应生成器
支持：预设成功/失败响应、延迟模拟、异常场景
"""

import json
import random
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class PSBCMockServer:
    """邮储财资 Mock 响应服务器"""
    
    def __init__(self, apis_config: str = "apis.json", 
                 response_codes_config: str = "response-codes.json"):
        """
        初始化 Mock 服务器
        
        Args:
            apis_config: API 配置文件路径
            response_codes_config: 响应码配置文件路径
        """
        with open(apis_config, "r", encoding="utf-8") as f:
            self.apis = json.load(f)
        with open(response_codes_config, "r", encoding="utf-8") as f:
            self.response_codes = json.load(f)
        
        self.api_map = {api["txCode"]: api for api in self.apis["apis"]}
        
        # Mock 数据池
        self.mock_data = {
            "accounts": [
                {"bankAccno": "951011013000006323", "accName": "晨云儿有限公司", "accBal": 1000000.00, "avalBal": 1000000.00},
                {"bankAccno": "6217994660005821", "accName": "测试企业 A", "accBal": 500000.50, "avalBal": 450000.50},
                {"bankAccno": "921026013000016778", "accName": "示例公司 B", "accBal": 2000000.00, "avalBal": 1800000.00},
            ],
            "transactions": [
                {"txDate": "20250318", "txTime": "143022", "txAmt": 1000.00, "opsAccName": "供应商 A", "txSumm": "货款支付"},
                {"txDate": "20250317", "txTime": "091530", "txAmt": 5000.00, "opsAccName": "客户 B", "txSumm": "收款"},
                {"txDate": "20250316", "txTime": "162045", "txAmt": 200.00, "opsAccName": "水电费", "txSumm": "公用事业费"},
            ],
            "payment_statuses": ["1", "2", "3", "4", "5", "6"],  # 待送审到付款成功
        }
        
        # 场景配置
        self.scenarios = {
            "normal": {"success_rate": 1.0, "delay_ms": 100},
            "slow": {"success_rate": 1.0, "delay_ms": 3000},
            "flaky": {"success_rate": 0.7, "delay_ms": 500},
            "timeout": {"success_rate": 0.0, "timeout": True},
        }
        self.current_scenario = "normal"
    
    def set_scenario(self, scenario: str):
        """设置模拟场景"""
        if scenario not in self.scenarios:
            raise ValueError(f"未知场景：{scenario}，可用场景：{list(self.scenarios.keys())}")
        self.current_scenario = scenario
    
    def mock_request(self, tx_code: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成 Mock 响应
        
        Args:
            tx_code: 交易码
            request_data: 请求数据
        
        Returns:
            Mock 响应数据
        """
        scenario = self.scenarios[self.current_scenario]
        
        # 模拟超时
        if scenario.get("timeout"):
            time.sleep(31)  # 超过一般 timeout
            raise TimeoutError("请求超时")
        
        # 模拟延迟
        delay_ms = scenario.get("delay_ms", 100)
        time.sleep(delay_ms / 1000.0)
        
        # 随机失败
        if random.random() > scenario.get("success_rate", 1.0):
            return self._generate_error_response(tx_code, request_data)
        
        # 生成成功响应
        return self._generate_success_response(tx_code, request_data)
    
    def _generate_success_response(self, tx_code: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成成功响应"""
        if tx_code not in self.api_map:
            return self._generate_error_response(tx_code, request_data, "999990", f"未知交易码：{tx_code}")
        
        api = self.api_map[tx_code]
        tx_comm = request_data.get("txComm", {})
        
        # 公共响应头
        response = {
            "txComm": {
                "respCode": "0000000000000000",
                "respDesc": "交易成功"
            }
        }
        
        # 根据交易码生成具体响应
        if tx_code == "601118":
            # 账户余额实时查询
            response.update(self._mock_balance_query(request_data))
        
        elif tx_code == "601113":
            # 查询租户下直连账户列表
            response.update(self._mock_account_list(request_data))
        
        elif tx_code == "601119":
            # 查询明细
            response.update(self._mock_transaction_detail(request_data))
        
        elif tx_code == "601116":
            # 生成单笔支付申请单
            response.update(self._mock_payment_create(request_data))
        
        elif tx_code == "601117":
            # 单笔支付结果查询
            response.update(self._mock_payment_query(request_data))
        
        elif tx_code == "601114":
            # 批量工资代发
            response.update(self._mock_batch_payroll(request_data))
        
        elif tx_code == "601115":
            # 批量工资代发结果查询
            response.update(self._mock_batch_payroll_query(request_data))
        
        elif tx_code == "601203":
            # 明细关联回单信息查询
            response.update(self._mock_receipt_query(request_data))
        
        elif tx_code == "601304":
            # 手工下拨
            response.update(self._mock_manual_transfer(request_data))
        
        elif tx_code == "601732":
            # 手工下拨结果查询
            response.update(self._mock_manual_transfer_query(request_data))
        
        elif tx_code == "601383":
            # 获取免密登录令牌
            response.update(self._mock_token_query(request_data))
        
        else:
            # 通用响应
            response.update(self._mock_generic_response(tx_code, request_data))
        
        return response
    
    def _generate_error_response(self, tx_code: str, request_data: Dict[str, Any],
                                  error_code: Optional[str] = None, 
                                  error_msg: Optional[str] = None) -> Dict[str, Any]:
        """生成错误响应"""
        business_codes = self.response_codes.get("businessCodes", {})
        
        if error_code is None:
            # 随机选择一个错误码
            error_options = ["020302", "020300", "020301", "999990", "029999"]
            error_code = random.choice(error_options)
        
        code_info = business_codes.get(error_code, {})
        error_desc = error_msg or code_info.get("description", "未知错误")
        
        return {
            "txComm": {
                "respCode": "0000000000000000",
                "respDesc": "交易成功"
            },
            "txCode": request_data.get("txComm", {}).get("txCode", tx_code),
            "tenantID": request_data.get("tenantID", "unknown"),
            "sendTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "respCode": error_code,
            "respInfo": error_desc
        }
    
    # ==================== 具体接口 Mock 实现 ====================
    
    def _mock_balance_query(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock 余额查询响应"""
        business_req = self._decrypt_business_data(request_data)
        bank_accno = business_req.get("bankAccno", "")
        
        # 查找模拟账户
        account = next((a for a in self.mock_data["accounts"] if a["bankAccno"] == bank_accno), None)
        
        if account:
            return {
                "txCode": "100016",
                "tenantID": business_req.get("tenantID", ""),
                "sendTime": business_req.get("sendTime", ""),
                "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
                "respCode": "000000",
                "respInfo": "成功",
                "data": {
                    "bankAccno": account["bankAccno"],
                    "accBal": f"{account['accBal']:.2f}",
                    "accAvalBal": f"{account['avalBal']:.2f}"
                }
            }
        else:
            return self._generate_error_response("601118", request_data, "020302", "查询无记录")
    
    def _mock_account_list(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock 账户列表响应"""
        business_req = self._decrypt_business_data(request_data)
        
        accounts = []
        for acc in self.mock_data["accounts"]:
            accounts.append({
                "id": f"1914996334685585{random.randint(100, 999)}",
                "deptName": "总部",
                "deptNo": "13000001",
                "bankClsName": "中国邮政储蓄银行股份有限公司",
                "finInstName": f"中国邮政储蓄银行股份有限公司{acc['accName']}支行",
                "finInstNo": "403651000792",
                "accName": acc["accName"],
                "bankAccno": acc["bankAccno"],
                "createTime": "2025-01-01 00:00:00",
                "lastModTime": "2025-03-18 12:00:00",
                "accStatus": "2",
                "currCode": "156",
                "currCnName": "人民币",
                "openaccDate": "20250101",
                "accBal": acc["accBal"],
                "avalBal": acc["avalBal"],
                "detailUpdateTime": "2025-03-18 12:00:00",
                "openBedlFlag": "1",
                "accAttrNo": "ZH0002",
                "accAttrName": "一般存款账户",
                "balUpdateTime": "2025-03-18 12:00:00"
            })
        
        return {
            "txCode": "100011",
            "tenantID": business_req.get("tenantID", ""),
            "sendTime": business_req.get("sendTime", ""),
            "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "respCode": "000000",
            "respInfo": "success",
            "data": accounts,
            "pagingResult": {
                "pageIndex": business_req.get("pageIndex", 1),
                "pageSize": business_req.get("pageSize", 10),
                "total": str(len(accounts))
            }
        }
    
    def _mock_transaction_detail(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock 交易明细响应"""
        business_req = self._decrypt_business_data(request_data)
        
        transactions = []
        for i, tx in enumerate(self.mock_data["transactions"]):
            transactions.append({
                "tenantId": business_req.get("tenantID", ""),
                "id": f"1930825892292329{i}",
                "bankAccno": business_req.get("bankAccno", ""),
                "accName": "测试账户",
                "txDate": tx["txDate"],
                "txTime": tx["txTime"],
                "opsAccNo": "6217994660005800",
                "opsAccName": tx["opsAccName"],
                "dcFlag": "0" if tx["txAmt"] > 0 else "1",
                "currCode": "156",
                "currCnName": "人民币",
                "txAmt": tx["txAmt"],
                "accBal": 1000000.00,
                "txSriNo": f"{tx['txDate']}{tx['txTime']}806tJ8nD",
                "remark": "",
                "txSumm": tx["txSumm"],
                "batchNo": "BATCH001"
            })
        
        return {
            "txCode": "100017",
            "tenantId": business_req.get("tenantID", ""),
            "sendTime": business_req.get("sendTime", ""),
            "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "respCode": "000000",
            "respInfo": "success",
            "data": transactions,
            "pagingResult": {
                "pageIndex": business_req.get("pageIndex", 1),
                "pageSize": business_req.get("pageSize", 10),
                "total": str(len(transactions))
            }
        }
    
    def _mock_payment_create(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock 支付申请单创建响应"""
        business_req = self._decrypt_business_data(request_data)
        
        # 模拟余额不足
        if float(business_req.get("payAmt", 0)) > 10000000:
            return self._generate_error_response("601116", request_data, "029999", "付款账户余额不足")
        
        return {
            "txCode": "100014",
            "tenantID": business_req.get("tenantID", ""),
            "sendTime": business_req.get("sendTime", ""),
            "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "respCode": "000000",
            "respInfo": "成功"
        }
    
    def _mock_payment_query(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock 支付结果查询响应"""
        business_req = self._decrypt_business_data(request_data)
        
        return {
            "txCode": "100015",
            "tenantID": business_req.get("tenantID", ""),
            "sendTime": business_req.get("sendTime", ""),
            "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "respCode": "000000",
            "respInfo": "success",
            "data": {
                "payStatus": random.choice(self.mock_data["payment_statuses"]),
                "bankSriNo": f"20250318143022806tJ8nD",
                "finishDate": datetime.now().strftime("%Y%m%d%H%M%S")
            }
        }
    
    def _mock_batch_payroll(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock 批量工资代发响应"""
        business_req = self._decrypt_business_data(request_data)
        
        return {
            "txCode": "100012",
            "tenantID": business_req.get("tenantID", ""),
            "sendTime": business_req.get("sendTime", ""),
            "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "respCode": "000000",
            "respInfo": "成功"
        }
    
    def _mock_batch_payroll_query(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock 批量工资代发结果查询响应"""
        business_req = self._decrypt_business_data(request_data)
        
        return {
            "txCode": "100013",
            "tenantID": business_req.get("tenantID", ""),
            "sendTime": business_req.get("sendTime", ""),
            "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "respCode": "000000",
            "respInfo": "success",
            "data": {
                "importFileStsCd": random.choice(["2", "6", "b"]),
                "appFormStaCd": "6",
                "failMsg": "",
                "batchNo": business_req.get("batchNo", "")
            }
        }
    
    def _mock_receipt_query(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock 回单查询响应（安全级别 15，平铺模式）"""
        # 安全级别 15，业务报文平铺
        tenant_id = request_data.get("tenantID", "")
        
        return {
            "txComm": {
                "respCode": "0000000000000000",
                "respDesc": "交易成功"
            },
            "txCode": "100019",
            "tenantID": tenant_id,
            "sendTime": request_data.get("sendTime", ""),
            "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "respCode": "000000",
            "respInfo": "操作成功",
            "data": {
                "tenantId": tenant_id,
                "feedAckTime": int(datetime.now().timestamp() * 1000),
                "id": request_data.get("id", ""),
                "fileType": "pdf",
                "file": "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PC9Db2xvclNwYWNlL0RldmljZVJHQi9TdWJ0eXBlL0ltYWdlL0hlaWdodCAzMDAvRmlsdGVyL0RDVERlY29kZS9UeXBlL1hPYmplY3QvV2lkdGggNjA3L0JpdHNQZXJDb21wb25lbnQgOC9MZW5ndGggMzg5ODc+PnN0cmVhbQr/2P/gABBKRklGAAEBAQCWAJYAAP/tAFZQaG90b3Nob3AgMy4wADhCSU0EBAAAAAAAHRwBWgADGyVHHAIAAAIAAhwCUAAJ5Y2i5rSq5rWpADhCSU0EJQAAAAAAEF2fC+4ARFZdTWLwd7fQr8v/4RoKRXhpZgAATU0AKgAAAAgACQES"
            }
        }
    
    def _mock_manual_transfer(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock 手工下拨响应"""
        business_req = self._decrypt_business_data(request_data)
        
        return {
            "txCode": "100025",
            "tenantId": business_req.get("tenantID", ""),
            "sendTime": business_req.get("sendTime", ""),
            "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "respCode": "000000",
            "respInfo": "success",
            "data": {
                "bankAccno": business_req.get("bankAccno", ""),
                "opsAccNo": business_req.get("opsAccNo", ""),
                "txSriNo": f"20250318143022806tJ8nD",
                "applyNo": f"APPLY{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
        }
    
    def _mock_manual_transfer_query(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock 手工下拨结果查询响应"""
        business_req = self._decrypt_business_data(request_data)
        
        return {
            "txCode": "100032",
            "tenantID": business_req.get("tenantID", ""),
            "sendTime": business_req.get("sendTime", ""),
            "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "respCode": "000000",
            "respInfo": "success",
            "data": {
                "applyNo": business_req.get("applyNo", ""),
                "applyStatus": "4",
                "payStatus": "3",
                "finishDate": datetime.now().strftime("%Y%m%d%H%M%S")
            }
        }
    
    def _mock_token_query(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock 免密登录令牌响应"""
        business_req = self._decrypt_business_data(request_data)
        
        return {
            "txCode": "100027",
            "tenantId": business_req.get("tenantID", ""),
            "sendTime": business_req.get("sendTime", ""),
            "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "respCode": "000000",
            "respInfo": "success",
            "data": {
                "urlWithToken": f"https://treasury.psbc.com/sso/login?token=MOCK_{random.randint(100000, 999999)}_{datetime.now().timestamp()}"
            }
        }
    
    def _mock_generic_response(self, tx_code: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """通用 Mock 响应"""
        business_req = self._decrypt_business_data(request_data)
        
        return {
            "txCode": business_req.get("txCode", tx_code),
            "tenantID": business_req.get("tenantID", ""),
            "sendTime": business_req.get("sendTime", ""),
            "feedbackTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "respCode": "000000",
            "respInfo": "success",
            "data": {}
        }
    
    def _decrypt_business_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解密业务数据（Mock 模式下直接返回或解析平铺数据）
        实际使用时需要实现 SM4 解密
        """
        tx_comm = request_data.get("txComm", {})
        security_level = tx_comm.get("securityLevel", "10")
        
        if security_level == "15":
            # 安全级别 15，业务报文平铺
            return {k: v for k, v in request_data.items() if k != "txComm"}
        
        # 安全级别 10，Mock 模式下假设已解密
        # 实际应解密 encData
        enc_data = tx_comm.get("encData", "")
        if enc_data:
            # TODO: 实现 SM4 解密
            pass
        
        # 返回示例数据
        return {
            "txCode": tx_comm.get("txCode", ""),
            "tenantID": "eam_tenant_a_0001",
            "sendTime": datetime.now().strftime("%Y%m%d%H%M%S"),
        }


# ==================== 命令行交互模式 ====================
def interactive_mock():
    """交互式 Mock 模式"""
    print("=" * 60)
    print("邮储银行财资管理系统 - Mock 响应生成器")
    print("=" * 60)
    
    mock_server = PSBCMockServer()
    
    print("\n可用场景:")
    for name, config in mock_server.scenarios.items():
        print(f"  {name}: 延迟{config.get('delay_ms', 0)}ms, 成功率{config.get('success_rate', 1.0)*100:.0f}%")
    
    print("\n当前场景：normal")
    print("\n请输入交易码（或输入 'q' 退出）: ", end="")
    tx_code = input().strip()
    
    if tx_code.lower() == 'q':
        return
    
    print("\n请输入请求报文 JSON（多行，空行结束）:")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    
    try:
        request_data = json.loads("\n".join(lines))
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误：{e}")
        return
    
    print("\n生成 Mock 响应...")
    try:
        response = mock_server.mock_request(tx_code, request_data)
        print("\n响应结果:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
    except TimeoutError as e:
        print(f"\n❌ 请求超时：{e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mock()
    else:
        # 示例：生成余额查询 Mock 响应
        mock_server = PSBCMockServer()
        
        request_data = {
            "txComm": {
                "sysTrackNo": "20250318143022997116600036518473",
                "reqSysCode": "99711940001",
                "txCode": "601118",
                "txTime": "20250318143022714",
                "securityLevel": "10",
                "sign": "xxx",
                "bankCertSN": "xxx",
                "userCertSN": "xxx",
                "encData": "xxx",
                "encKey": "xxx"
            }
        }
        
        response = mock_server.mock_request("601118", request_data)
        print("Mock 响应示例:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
