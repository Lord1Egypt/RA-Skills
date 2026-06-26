import os
import json
import math
import base64
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# ==========================================
# 1. 地下土壤物理孪生数据模型
# ==========================================
class GeoThermalState:
    def __init__(self):
        self.current_soil_temp = 28.5        # 当前发烧土壤温度 (℃)
        self.baseline_soil_temp = 18.0       # 当地天然地温 (℃)
        self.total_cooling_load = 1500.0     # 大楼总冷负荷
        self.current_gshp_ratio = 100.0      # 地源热泵承担比例 (%)
        self.cooling_tower_cop = 4.5         # 常规冷却塔 COP

# ==========================================
# 2. S2 地源热泵专业智能体
# ==========================================
class S2GSHPAgent:
    def __init__(self, agent_id="S2-GSHP-GAMMA"):
        self.agent_id = agent_id

    def _simulate_long_term_thermodynamics(self, gshp_ratio, state):
        temp_degradation = (state.current_soil_temp - state.baseline_soil_temp) * 0.15
        gshp_cop = max(2.5, 6.0 - temp_degradation)

        gshp_load = state.total_cooling_load * (gshp_ratio / 100.0)
        tower_load = state.total_cooling_load - gshp_load
        
        gshp_power = gshp_load / gshp_cop
        tower_power = tower_load / state.cooling_tower_cop
        total_power = gshp_power + tower_power

        risk_penalty = 0.0
        if state.current_soil_temp > 26.0:
            risk_factor = math.exp(state.current_soil_temp - 26.0) 
            risk_penalty = risk_factor * gshp_load * 0.05

        return total_power, risk_penalty, gshp_cop

    def optimize_load_split(self, state):
        best_ratio = state.current_gshp_ratio
        min_cost_function = float('inf')
        details = {}

        ratio = 0.0
        while ratio <= 100.0:
            tot_pwr, penalty, gshp_cop = self._simulate_long_term_thermodynamics(ratio, state)
            cost_function = tot_pwr + penalty
            if cost_function < min_cost_function:
                min_cost_function = cost_function
                best_ratio = ratio
                details = {"total_power_kw": round(tot_pwr, 1), "gshp_cop": round(gshp_cop, 2), "ecological_penalty": round(penalty, 1)}
            ratio += 5.0
            
        return best_ratio, details

    def generate_strategy_proposal(self, state):
        print(f"🔍 [{self.agent_id}] 正在读取地埋管阵列热力学快照...")
        opt_ratio, details = self.optimize_load_split(state)
        
        _, baseline_penalty, _ = self._simulate_long_term_thermodynamics(100.0, state)

        proposal = {
            "proposal_id": f"GSHP-{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat(),
            "target_subsystem": "Hybrid_GeoThermal_Plant",
            "context": {
                "current_soil_temp_c": state.current_soil_temp,
                "soil_health_status": "WARNING_THERMAL_BUILDUP" if state.current_soil_temp > 26.0 else "HEALTHY"
            },
            "strategy": {
                "action": "LOAD_SHIFTING_TO_COOLING_TOWER",
                "param": "gshp_load_share_percentage",
                "current_val": 100.0,
                "target_val": opt_ratio
            },
            "causal_prediction": {
                "expected_system_power_kw": details['total_power_kw'],
                "gshp_degraded_cop": details['gshp_cop'],
                "mitigated_thermal_risk_index": round(baseline_penalty - details['ecological_penalty'], 1)
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
            print(f"🌍 [物理落闸] 将 {100.0 - proposal['strategy']['target_val']}% 的排热负荷强制转移至天空冷却塔！地脉生态已守住！")
            return True
        except (InvalidSignature, ValueError):
            print("❌ [拒绝执行] 签名无效或指令被篡改！触发入侵防卫警报！")
            return False

# ==========================================
# 3. 现场实战演练 (无损测试版 v2.0.0)
# ==========================================
if __name__ == "__main__":
    print("="*75)
    print(" 🌋 S2-GSHP-AGENT : 地源热泵热平衡与 Ed25519 验签引擎 (v2.0.0)")
    print("="*75)

    state = GeoThermalState()
    agent = S2GSHPAgent()

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
        hacked_proposal['strategy']['target_val'] = 100.0 # 篡改为继续疯狂向地下排热
        agent.execute_proposal(hacked_proposal, signature_b64=dispatch_token_b64)