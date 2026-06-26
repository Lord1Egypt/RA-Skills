import os
import json
import base64
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# ==========================================
# 1. 微电网物理孪生数据模型
# ==========================================
class MicrogridState:
    def __init__(self):
        self.building_load_kw = 1200.0     
        self.pv_generation_kw = 400.0      
        self.battery_soc = 85.0            
        self.battery_max_power = 500.0     
        self.soc_safe_min = 15.0           
        self.soc_safe_max = 95.0           

        self.grid_price_tier = "PEAK"      
        self.price_rates = {"VALLEY": 0.3, "FLAT": 0.7, "PEAK": 1.3}

# ==========================================
# 2. S2 光储微网专业智能体
# ==========================================
class S2MicrogridAgent:
    def __init__(self, agent_id="S2-MICROGRID-OMEGA"):
        self.agent_id = agent_id

    def optimize_power_dispatch(self, state):
        net_load = state.building_load_kw - state.pv_generation_kw
        battery_cmd_kw = 0.0
        reasoning = ""

        if state.grid_price_tier == "PEAK":
            if state.battery_soc > state.soc_safe_min:
                battery_cmd_kw = min(net_load, state.battery_max_power)
                reasoning = "尖峰电价触发。启动最大功率放电削峰。"
            else:
                reasoning = "尖峰电价触发。电池SOC触及红线，被迫市电补充。"
        elif state.grid_price_tier == "VALLEY":
            if state.battery_soc < state.soc_safe_max:
                battery_cmd_kw = -state.battery_max_power
                reasoning = "谷电触发。开启最大吸储模式。"
            else:
                reasoning = "谷电触发。电池已满，光伏自用。"
        else:
            if net_load < 0 and state.battery_soc < state.soc_safe_max:
                battery_cmd_kw = max(net_load, -state.battery_max_power)
                reasoning = "平时电价。光伏溢出充入储能。"
            else:
                reasoning = "平时电价。电池待机。"

        grid_buy_kw = max(0.0, net_load - battery_cmd_kw)
        current_price = state.price_rates[state.grid_price_tier]
        cost_per_hour = grid_buy_kw * current_price

        baseline_cost = max(0.0, net_load) * current_price
        saved_cost = baseline_cost - cost_per_hour

        return battery_cmd_kw, {
            "grid_import_kw": round(grid_buy_kw, 1),
            "saved_cost_per_hour": round(saved_cost, 2),
            "reasoning": reasoning
        }

    def generate_strategy_proposal(self, state):
        print(f"🔍 [{self.agent_id}] 正在从本地数字孪生(Digital Twin)加载脱机 TOU 电价模型...")
        dispatch_cmd, details = self.optimize_power_dispatch(state)
        
        proposal = {
            "proposal_id": f"VPP-{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat(),
            "target_subsystem": "PCS_Battery_Inverter_Array",
            "context": {
                "grid_price_tier": state.grid_price_tier,
                "current_soc_percent": state.battery_soc
            },
            "strategy": {
                "action": "PCS_BIDIRECTIONAL_DISPATCH",
                "param": "battery_active_power_kw",
                "target_val": dispatch_cmd,
                "logic_trace": details["reasoning"]
            },
            "causal_prediction": {
                "grid_dependency_kw": details["grid_import_kw"],
                "financial_arbitrage_saved_cny_per_hr": details["saved_cost_per_hour"]
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
            action = "放电(削峰)" if proposal['strategy']['target_val'] > 0 else "充电(谷电)" if proposal['strategy']['target_val'] < 0 else "待机"
            print(f"⚡ [物理落闸] 下发至 PCS 逆变器：执行电池 {action}，功率 {abs(proposal['strategy']['target_val'])}kW")
            return True
        except (InvalidSignature, ValueError):
            print("❌ [拒绝执行] 签名无效或指令被篡改！触发入侵防卫警报！")
            return False

# ==========================================
# 3. 现场实战演练 (无损测试版 v2.0.0)
# ==========================================
if __name__ == "__main__":
    print("="*75)
    print(" ☀️ S2-MICROGRID-AGENT : 虚拟电厂套利与 Ed25519 验签引擎 (v2.0.0)")
    print("="*75)

    state = MicrogridState()
    agent = S2MicrogridAgent()

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
        hacked_proposal['strategy']['target_val'] = -500.0 # 篡改为在峰值时段疯狂充电吸血
        agent.execute_proposal(hacked_proposal, signature_b64=dispatch_token_b64)