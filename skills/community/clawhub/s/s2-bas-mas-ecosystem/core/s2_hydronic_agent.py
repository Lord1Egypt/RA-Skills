import os
import json
import math
import base64
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# ==========================================
# 1. 管网物理孪生数据模型
# ==========================================
class HydronicNetworkState:
    def __init__(self):
        self.valves_feedback = {
            "SSSU-801": 45.0, 
            "SSSU-802": 30.0,
            "SSSU-905": 60.0,  # 最不利末端
            "SSSU-1002": 25.0
        }
        self.current_pump_freq = 50.0      # 当前水泵频率 (Hz)
        self.pump_rated_power_kw = 110.0   # 额定功率 (kW)
        self.min_pump_freq = 30.0          # 最低安全频率 (Hz)

# ==========================================
# 2. S2 输配专业智能体
# ==========================================
class S2HydronicAgent:
    def __init__(self, agent_id="S2-HYDRONIC-BETA"):
        self.agent_id = agent_id

    def _simulate_hydraulics(self, target_freq, state):
        freq_ratio = target_freq / 50.0
        pump_power = state.pump_rated_power_kw * math.pow(freq_ratio, 3)
        
        critical_valve_current = max(state.valves_feedback.values())
        expected_critical_valve = critical_valve_current * (state.current_pump_freq / target_freq)
        
        return pump_power, expected_critical_valve

    def optimize_pump_pressure(self, state):
        target_valve_position = 95.0
        critical_valve = max(state.valves_feedback.values())
        
        if critical_valve >= target_valve_position:
            return state.current_pump_freq, {}

        opt_freq = state.current_pump_freq * (critical_valve / target_valve_position)
        opt_freq = max(state.min_pump_freq, opt_freq)
        
        opt_power, _ = self._simulate_hydraulics(opt_freq, state)
        return round(opt_freq, 1), {"optimized_power_kw": round(opt_power, 1), "critical_valve": target_valve_position}

    def generate_strategy_proposal(self, state):
        print(f"🔍 [{self.agent_id}] 正在全楼扫描末端阀门阵列，执行流体力学寻优...")
        opt_freq, details = self.optimize_pump_pressure(state)
        
        current_power, _ = self._simulate_hydraulics(state.current_pump_freq, state)
        saved_kw = round(current_power - details.get('optimized_power_kw', current_power), 1)

        proposal = {
            "proposal_id": f"HYD-{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat(),
            "target_subsystem": "Secondary_Chilled_Water_Pump_Group",
            "context": {
                "max_valve_opening_percent": max(state.valves_feedback.values()),
                "current_pump_freq_hz": state.current_pump_freq
            },
            "strategy": {
                "action": "DYNAMIC_PRESSURE_RESET",
                "param": "pump_vfd_frequency",
                "current_val": state.current_pump_freq,
                "target_val": opt_freq
            },
            "causal_prediction": {
                "expected_pump_power_kw": details.get('optimized_power_kw', current_power),
                "expected_max_valve_opening": details.get('critical_valve', max(state.valves_feedback.values())),
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
            print(f"🌊 [物理落闸] S2-Hydronic-Agent 将水泵频率重置为：{proposal['strategy']['target_val']}Hz")
            return True
        except (InvalidSignature, ValueError):
            print("❌ [拒绝执行] 签名无效或指令被篡改！触发入侵防卫警报！")
            return False

# ==========================================
# 3. 现场实战演练 (无损测试版 v2.0.0)
# ==========================================
if __name__ == "__main__":
    print("="*75)
    print(" 🚰 S2-HYDRONIC-AGENT : 输配管网因果控制与 Ed25519 验签引擎 (v2.0.0)")
    print("="*75)

    state = HydronicNetworkState()
    agent = S2HydronicAgent()

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
        hacked_proposal['strategy']['target_val'] = 50.0 # 篡改频率
        agent.execute_proposal(hacked_proposal, signature_b64=dispatch_token_b64)