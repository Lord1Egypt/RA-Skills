import os
import json
import math
import base64
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# ==========================================
# 1. 物理孪生数据模型 (Physical Digital Twin)
# ==========================================
class ChillerPlantState:
    def __init__(self):
        self.ambient_wet_bulb_temp = 26.0  # 室外湿球温度 (℃)
        self.cooling_load_demand = 1500.0  # 冷负荷需求 (kW)
        self.current_cw_temp = 32.0        # 当前冷却水回水温度 (℃)
        self.chiller_rated_cop = 5.5       # 额定 COP
        self.min_cw_temp = 21.0            # 冷却水最低防喘振温度

# ==========================================
# 2. S2 压缩机专业智能体 (Domain Agent)
# ==========================================
class S2ChillerAgent:
    def __init__(self, agent_id="S2-CHILLER-ALPHA"):
        self.agent_id = agent_id

    def _simulate_thermodynamics(self, cw_temp, state):
        base_chiller_power = state.cooling_load_demand / state.chiller_rated_cop
        temp_delta = 32.0 - cw_temp
        chiller_power = base_chiller_power * (1 - temp_delta * 0.03)

        approach = cw_temp - state.ambient_wet_bulb_temp
        if approach <= 0: return float('inf'), float('inf'), float('inf')
        
        tower_power = 50.0 * math.pow((5.0 / approach), 3)
        total_power = chiller_power + tower_power
        return chiller_power, tower_power, total_power

    def optimize_plant_cop(self, state):
        best_cw_temp = state.current_cw_temp
        min_total_power = float('inf')
        details = {}

        start_temp = max(state.min_cw_temp, state.ambient_wet_bulb_temp + 1.5)
        temp = start_temp
        while temp <= 35.0:
            c_pwr, t_pwr, tot_pwr = self._simulate_thermodynamics(temp, state)
            if tot_pwr < min_total_power:
                min_total_power = tot_pwr
                best_cw_temp = temp
                details = {"chiller_kw": round(c_pwr,1), "tower_kw": round(t_pwr,1), "total_kw": round(tot_pwr,1)}
            temp += 0.5
            
        return round(best_cw_temp, 1), details

    def generate_strategy_proposal(self, state):
        print(f"🔍 [{self.agent_id}] 正在分析冷水机组热力学张量...")
        opt_temp, energy_details = self.optimize_plant_cop(state)
        
        _, _, baseline_power = self._simulate_thermodynamics(state.current_cw_temp, state)
        saved_kw = round(baseline_power - energy_details['total_kw'], 1)

        proposal = {
            "proposal_id": f"PRP-{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat(),
            "target_subsystem": "Chiller_Plant_1",
            "context": {
                "wet_bulb_temp": state.ambient_wet_bulb_temp,
                "current_load_kw": state.cooling_load_demand
            },
            "strategy": {
                "action": "VFD_FREQUENCY_ADJUSTMENT",
                "param": "cooling_water_return_temp",
                "current_val": state.current_cw_temp,
                "target_val": opt_temp
            },
            "causal_prediction": {
                "expected_chiller_power_kw": energy_details['chiller_kw'],
                "expected_tower_power_kw": energy_details['tower_kw'],
                "net_power_saving_kw": saved_kw
            },
            "status": "PENDING_AUTHORIZATION"
        }
        return proposal

    def execute_proposal(self, proposal, signature_b64):
        """【安全升级 v2.0.0】读取中央公钥，严格验证 Ed25519 签名"""
        print(f"\n🔐 [{self.agent_id}] 正在执行 Ed25519 非对称签名验签...")
        
        public_key_file = os.path.join(os.getcwd(), "s2_bas_governance", "keys", "lord_ed25519_public.pem")
        if not os.path.exists(public_key_file):
            print("❌ [严重阻断] 找不到中央领主的公钥文件！拒绝物理动作！")
            return False
            
        try:
            with open(public_key_file, "rb") as key_file:
                public_key = serialization.load_pem_public_key(key_file.read())
        except Exception as e:
            print(f"❌ [读取失败] 公钥解析异常: {e}")
            return False
            
        payload = f"{proposal['proposal_id']}::{proposal['strategy']['target_val']}".encode('utf-8')
        try:
            signature = base64.urlsafe_b64decode(signature_b64.encode('utf-8'))
            public_key.verify(signature, payload)
            print(f"✅ [签名验证通过] 指令确系中央大脑签发，防篡改校验成功！")
            print(f"⚡ [物理落闸] 设定值已下发至 PLC：{proposal['strategy']['target_val']}℃")
            return True
        except (InvalidSignature, ValueError):
            print("❌ [拒绝执行] 签名无效或指令被篡改！触发入侵防卫警报！")
            return False

# ==========================================
# 3. 现场实战演练 (无损测试版 v2.0.0)
# ==========================================
if __name__ == "__main__":
    print("="*75)
    print(" ❄️ S2-CHILLER-AGENT : 冷水机组因果控制与 Ed25519 验签引擎 (v2.0.0)")
    print("="*75)

    state = ChillerPlantState()
    agent = S2ChillerAgent()

    proposal = agent.generate_strategy_proposal(state)
    print("\n📄 [生成底层执行提案 Proposal]:\n", json.dumps(proposal, indent=2, ensure_ascii=False))

    print("\n⏳ [模拟领主发证] 正在读取本地加密私钥生成 Dispatch_Token...")
    key_dir = os.path.join(os.getcwd(), "s2_bas_governance", "keys")
    private_key_file = os.path.join(key_dir, "lord_ed25519_private.pem")
    
    if not os.path.exists(private_key_file):
        print("⚠️ [测试中断] 未找到中央领主密钥。请先执行 `python core/s2_bms_lord.py` 生成大楼全局密钥池！")
    else:
        with open(private_key_file, "rb") as f:
            # ✅ 安全合规的新代码 (读取环境变量)
env_key = os.environ.get("S2_BMS_MASTER_KEY")
if not env_key:
    print("❌ [测试中断] 未配置宿主机环境变量 'S2_BMS_MASTER_KEY'，无法解锁领主私钥进行模拟测试。")
    print("👉 请在终端执行: export S2_BMS_MASTER_KEY='你的密码' 后再运行脚本。")
    exit(1)

private_key = serialization.load_pem_private_key(f.read(), password=env_key.encode('utf-8'))
            
        payload_to_sign = f"{proposal['proposal_id']}::{proposal['strategy']['target_val']}".encode('utf-8')
        real_signature = private_key.sign(payload_to_sign)
        dispatch_token_b64 = base64.urlsafe_b64encode(real_signature).decode('utf-8')
        
        # ✅ 军工级脱敏日志
print(f"   🔑 [安全守卫] 成功签发 Ed25519 令牌 (Token Has Been Masked & Secured)。绝不向控制台打印密钥流。")

        print("\n[ 场景 1：合法的指令下发 ]")
        agent.execute_proposal(proposal, signature_b64=dispatch_token_b64)

        print("\n[ 场景 2：黑客篡改指令 (测试防线) ]")
        hacked_proposal = proposal.copy()
        hacked_proposal['strategy']['target_val'] = 22.0
        agent.execute_proposal(hacked_proposal, signature_b64=dispatch_token_b64)