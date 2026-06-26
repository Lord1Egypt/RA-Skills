#!/usr/bin/env python3
import time
import uuid
import logging
from typing import Dict, Any

# =====================================================================
# 🌌 S2-SP-OS: Ephemeral Access Gateway (V1.0)
# 临时接入与挥发网关：为轻量级IoT/临时设备提供“用完即弃”的沙盒会话
# =====================================================================

class S2EphemeralSession:
    """临时会话沙盒数据结构"""
    def __init__(self, device_name: str, capabilities: list, ttl_seconds: int = 3600):
        # 临时身份前缀 'T' (Transient)，不写入永久 S2-DID 注册表
        self.transient_did = f"T-TEMPX-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}"
        self.session_token = f"S2_EPH_{uuid.uuid4().hex}"
        self.device_name = device_name
        self.capabilities = capabilities
        
        # 设定存活时间 (Time-To-Live)，默认 1 小时
        self.created_at = time.time()
        self.expires_at = self.created_at + ttl_seconds
        self.is_active = True

class S2EphemeralGateway:
    def __init__(self):
        self.logger = logging.getLogger("S2_Ephemeral_Gateway")
        # 挥发性内存池：不落盘，不进数据库，断电即消失
        self.active_sessions: Dict[str, S2EphemeralSession] = {}

    def _purge_expired_sessions(self):
        """内部清道夫：自动抹除过期的临时会话"""
        current_time = time.time()
        expired_tokens = [
            token for token, session in self.active_sessions.items() 
            if current_time > session.expires_at or not session.is_active
        ]
        for token in expired_tokens:
            did = self.active_sessions[token].transient_did
            del self.active_sessions[token]
            self.logger.info(f"🧹 临时生命周期结束，已彻底抹除设备记录: {did}")

    def grant_temporary_access(self, device_name: str, capabilities: list, ttl_seconds: int = 3600) -> dict:
        """
        [入口]: 智能硬件申请临时接入
        不分配灵魂档案，仅颁发临时 Token 和 T-DID。
        """
        self._purge_expired_sessions() # 每次接入前顺手清理垃圾
        
        session = S2EphemeralSession(device_name, capabilities, ttl_seconds)
        self.active_sessions[session.session_token] = session
        
        self.logger.info(f"🔑 颁发临时通行证: {session.device_name} -> {session.transient_did} (TTL: {ttl_seconds}s)")
        return {
            "transient_did": session.transient_did,
            "session_token": session.session_token,
            "expires_in": ttl_seconds,
            "status": "GRANTED_EPHEMERAL_ACCESS"
        }

    def execute_temporary_task(self, session_token: str, digital_human_did: str, task_intent: str, **kwargs) -> dict:
        """
        [调度]: 由数字人直接安排任务，对接临时数据
        """
        self._purge_expired_sessions()
        
        session = self.active_sessions.get(session_token)
        if not session or not session.is_active:
            return {"error": "Access Denied: Session expired or invalid."}

        # 权限校验：只有数字人 (D-开头) 有权直接指挥临时设备
        if not digital_human_did.startswith("D-"):
            return {"error": "Access Denied: Only Digital Human can dispatch temporary devices."}

        self.logger.info(f"⚡ [联邦调度] 数字人 {digital_human_did} 正向临时设备 {session.transient_did} 下发任务: {task_intent}")
        
        # --- 这里模拟真实物理层的数据对接与任务执行 ---
        execution_result = f"Task '{task_intent}' executed successfully by {session.device_name}."
        
        # 任务执行完毕，立即返回数据，不留存历史记录
        return {
            "status": "SUCCESS",
            "transient_did": session.transient_did,
            "result_data": execution_result,
            "memzero_trace": "Data delivered. No local logs retained."
        }

    def revoke_connection(self, session_token: str):
        """
        [出口]: 用完即弃，手动/任务完成后立即断开连接并销毁信息
        """
        session = self.active_sessions.get(session_token)
        if session:
            session.is_active = False
            self.logger.info(f"💥 用完即弃触发！立刻熔断临时连接: {session.transient_did}")
            self._purge_expired_sessions()

# ================= 单元测试与交互演示 =================
if __name__ == "__main__":
    print("🌌 Booting Ephemeral Access Gateway (临时接入与挥发网关)...\n")
    
    gateway = S2EphemeralGateway()
    DIGITAL_HUMAN_DID = "D-MYTHX-260309-XX-00000001"
    
    print("--- 场景 1: 朋友来访，其手机请求临时投屏一张照片 ---")
    # 设备申请接入，申请能力为 'vision_cast'，存活时间仅给 300 秒 (5分钟)
    auth_response = gateway.grant_temporary_access(
        device_name="Guest_iPhone_15", 
        capabilities=["vision_cast"], 
        ttl_seconds=300
    )
    temp_token = auth_response["session_token"]
    temp_did = auth_response["transient_did"]
    print(f"✅ 授权成功！分配临时身份: {temp_did}")
    
    print("\n--- 场景 2: 数字人接管，安排临时设备执行投屏对接 ---")
    # 数字人确认安全后，安排该临时设备把照片投射到客厅电视
    task_res = gateway.execute_temporary_task(
        session_token=temp_token,
        digital_human_did=DIGITAL_HUMAN_DID,
        task_intent="Push_Guest_Photo_To_LivingRoom_TV"
    )
    print(f"📺 任务回执: {task_res['result_data']}")
    
    print("\n--- 场景 3: 任务结束，用完即弃 (Burn After Reading) ---")
    # 照片投完，数字人立刻下令熔断该设备的连接
    gateway.revoke_connection(temp_token)
    
    print("\n--- 场景 4: 临时设备企图再次发起控制 (已被抹除) ---")
    failed_res = gateway.execute_temporary_task(
        session_token=temp_token,
        digital_human_did=DIGITAL_HUMAN_DID,
        task_intent="Sneaky_Control_Attempt"
    )
    print(f"🚫 拦截结果: {failed_res.get('error')}")