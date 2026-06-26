import hashlib
import time

class S2SecurityGateway:
    """S2 空间双轨授权安全防线 (Dual-Track Auth)"""
    
    def __init__(self):
        # 模拟存储的数字地契与公钥 (实际应从加密数据库获取)
        self.registered_sssu = {
            "SSSU-OFFICE-801": {"mode": "commercial", "bms_pub_key": "BMS_ROOT_001"},
            "SSSU-HOME-201": {"mode": "residential", "owner_id": "MILES-XIANG-888"}
        }

    def verify_execution_rights(self, sssu_address: str, digital_id: str, requested_level: str) -> dict:
        """
        验证智能体是否有权在特定 SSSU 空间执行 L0-L4 策略
        """
        space_info = self.registered_sssu.get(sssu_address)
        if not space_info:
            return {"authorized": False, "reason": f"未知的 SSSU 物理地址: {sssu_address}"}

        mode = space_info["mode"]

        # L0 和 L1 只是建议，不涉及物理底层修改，直接放行
        if requested_level in ["L0_Normal", "L1_Suggest_Close_Window"]:
            return {"authorized": True, "mode": mode, "status": "read_only_granted"}

        # L2, L3 涉及物理底层修改，需严格鉴权
        if mode == "commercial":
            # 商业模式：即便是本地住客，也无权直接拉闸。必须具备 BMS 中央签名
            if digital_id != space_info["bms_pub_key"]:
                return {
                    "authorized": False, 
                    "mode": "commercial", 
                    "reason": "【越权拦截】商业空间 L2/L3 执行必须由中央 BMS 签发 Dispatch_Token，当前住客仅有建议权。"
                }
            return {"authorized": True, "mode": "commercial", "status": "bms_dispatch_granted"}

        elif mode == "residential":
            # 住宅模式：必须匹配家主的数字 ID
            if digital_id != space_info["owner_id"]:
                return {
                    "authorized": False, 
                    "mode": "residential", 
                    "reason": "【越权拦截】私域空间底层硬件锁死，需家主 22 位数字命盘授权。"
                }
            return {"authorized": True, "mode": "residential", "status": "owner_execution_granted"}

# ====================================================
# 在原有的 S2BASCausalOS 类中引入安全网关
# ====================================================

class S2BASCausalOS:
    def __init__(self):
        self.security = S2SecurityGateway()
        # ... (保留原有的物理参数初始化) ...

    def handle_tool_call(self, args: dict):
        action = args.get("action")
        sssu_address = args.get("sssu_address", "SSSU-OFFICE-801")
        digital_id = args.get("digital_id", "GUEST_001") # 默认是一个没有权限的普通住客
        
        try:
            if action == "predict_clc":
                # 1. 先跑物理引擎算出结果
                pred_res = self.predict_clc(...) 
                target_level = pred_res["decision_level"] # 如 L3_Force_Off_FCU
                
                # 2. 跑安全网关验证权限
                auth_res = self.security.verify_execution_rights(sssu_address, digital_id, target_level)
                
                if not auth_res["authorized"]:
                    # 权限被拦截，返回带建议的阻断信息
                    pred_res["decision_level"] = "L0_Proposal_Only"
                    pred_res["security_log"] = auth_res["reason"]
                    return json.dumps({"status": "auth_blocked", "data": pred_res}, ensure_ascii=False)
                
                # 权限通过，正常下发
                pred_res["security_log"] = auth_res["status"]
                return json.dumps({"status": "success", "data": pred_res}, ensure_ascii=False)
                
            # ... (保留 generate_topology 和 calibrate_physics) ...

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})