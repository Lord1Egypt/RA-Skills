import os
import json
import base64
import random
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# ==========================================
# 1. 空间主权与硅基身份分配器 (S2 Identity Registry)
# ==========================================
class S2IdentityRegistry:
    @staticmethod
    def generate_suns_address(building_name: str) -> str:
        building_name = building_name.upper()
        base_address = f"PHSY-CN-001-{building_name}"
        total_length = len(base_address) 
        checksum_x = total_length % 10 
        return f"{base_address}{checksum_x}"

    @staticmethod
    def generate_s2_did(building_name: str) -> str:
        building_name = building_name.upper()
        seg1 = "V"
        seg2 = building_name[:5]
        seg3 = datetime.now().strftime("%y%m%d")
        seg4 = "AA"
        seg5 = str(random.randint(10000000, 99999999))
        return f"{seg1}{seg2}{seg3}{seg4}{seg5}"

# ==========================================
# 2. 宠物空间孪生数据模型
# ==========================================
class PetSpaceDigitalTwin:
    def __init__(self):
        self.room_temp_c = 28.5        
        self.room_humidity = 65.0      
        self.pet_location = "Fountain_Zone" 
        self.latest_audio_signature = "high_pitch_meow_continuous"
        self.feeder_status = {"food_level": 0, "today_eaten_g": 35, "today_plan_g": 60} 
        self.litter_status = {"today_usage_count": 6, "last_duration_sec": 300} 

# ==========================================
# 3. S2 宠物守护者专业智能体 (L2 Domain Agent - 无签发权)
# ==========================================
class S2PetGuardianAgent:
    def __init__(self, pet_nickname="可乐", building_name="ABCDE"):
        self.pet_nickname = pet_nickname
        self.building_name = building_name
        self.storage_dir = os.path.join(os.getcwd(), "s2_bas_governance", "pets")
        os.makedirs(self.storage_dir, exist_ok=True)
        
        self.suns_address = S2IdentityRegistry.generate_suns_address(self.building_name)
        self.pet_did = S2IdentityRegistry.generate_s2_did(self.building_name)
        self.agent_id = f"S2-PET-GUARDIAN-[{self.pet_did}]"

    def translate_semantic_intent(self, state: PetSpaceDigitalTwin):
        intent, urgency = "未知状态", "low"
        if state.latest_audio_signature == "high_pitch_meow_continuous":
            if state.feeder_status["food_level"] == 0:
                intent = f"【极度饥饿】饭盆空了！{self.pet_nickname} 正在抗议要求加粮！"
                urgency = "high"
        if state.litter_status["today_usage_count"] > 5 and state.litter_status["last_duration_sec"] > 120:
            intent = f"【⚠️健康红灯】智能猫砂盆使用频次异常。疑似泌尿阻塞！"
            urgency = "critical"
        return intent, urgency

    def generate_strategy_proposal(self, state: PetSpaceDigitalTwin):
        pet_intent, urgency = self.translate_semantic_intent(state)
        print(f"🗣️ [{self.pet_did} 心声翻译] {pet_intent}")
        
        self._save_companion_record("moment", f"语义翻译: {pet_intent}")
        
        if urgency == "critical":
            return {"status": "ALERT", "msg": "健康红灯，终止自动化控制。"}

        if state.feeder_status["food_level"] == 0:
            target_amount = state.feeder_status["today_plan_g"] - state.feeder_status["today_eaten_g"]
            proposal = {
                "proposal_id": f"FEED-{int(datetime.now().timestamp())}",
                "target_subsystem": "Smart_Feeder_SOHO_V1",
                "pet_did": self.pet_did,
                "strategy": {
                    "action": "DISPENSE_FOOD",
                    "target_val": target_amount,
                    "reasoning": pet_intent
                },
                "status": "PENDING_AUTHORIZATION"
            }
            return proposal
        return {"status": "OK"}

    def _save_companion_record(self, rec_type, content):
        record_id = f"rec_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        fm = {"record_id": record_id, "pet_did": self.pet_did, "nickname": self.pet_nickname, "type": rec_type, "created_at": datetime.now().isoformat()}
        file_path = os.path.join(self.storage_dir, f"{record_id}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"---\n{json.dumps(fm, ensure_ascii=False)}\n---\n\n{content}\n")

    def execute_proposal(self, proposal, signature_b64):
        """【S2 终极防线】只读公钥，只做验签。绝不碰私钥！"""
        print(f"\n🔐 [{self.agent_id}] 收到主人授权令牌，正在通过公钥执行零信任验签...")
        public_key_file = os.path.join(os.getcwd(), "s2_bas_governance", "keys", "lord_ed25519_public.pem")
        
        if not os.path.exists(public_key_file):
            print("❌ 找不到中央公钥文件，拒绝执行！")
            return False
            
        try:
            with open(public_key_file, "rb") as key_file:
                public_key = serialization.load_pem_public_key(key_file.read())
            payload = f"{proposal['proposal_id']}::{proposal['strategy']['target_val']}".encode('utf-8')
            signature = base64.urlsafe_b64decode(signature_b64.encode('utf-8'))
            
            public_key.verify(signature, payload)
            print(f"✅ [验签通过] 硬件网关准入！向身份为 {proposal['pet_did']} 的宠物投放 {proposal['strategy']['target_val']}g 粮食！")
            return True
        except Exception:
            print("❌ [拒绝执行] 签名无效！非法的越权控制！")
            return False

# ==========================================
# 3. 现场实战演练 (不再模拟私钥行为)
# ==========================================
if __name__ == "__main__":
    print("="*75)
    print(" 🐾 S2-PET-GUARDIAN : v1.2.0 绝对零信任架构演练")
    print("="*75)

    state = PetSpaceDigitalTwin()
    agent = S2PetGuardianAgent(pet_nickname="可乐", building_name="ABCDE")
    
    proposal = agent.generate_strategy_proposal(state)
    if proposal.get("status") == "PENDING_AUTHORIZATION":
        print("\n📄 [L2 智能体已生成物理提案 Proposal]:")
        print(json.dumps(proposal, indent=2, ensure_ascii=False))
        print("\n⚠️ [架构隔离说明] 作为 L2 器官智能体，我无权也无法获取环境变量或私钥进行签名。")
        print("等待外部 L1 数字人或真实人类通过手机端 App 签发 Dispatch_Token 中...")
        
        # 为了演示验签流程，这里使用临时生成的内存密钥对模拟外部传来的正确签名
        print("\n(模拟: 主人手机端 App 接收到提案，主人点击确认，使用本地指纹解锁私钥并签名...)")
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        
        # 临时写入模拟公钥供验签读取
        os.makedirs(os.path.join(os.getcwd(), "s2_bas_governance", "keys"), exist_ok=True)
        with open(os.path.join(os.getcwd(), "s2_bas_governance", "keys", "lord_ed25519_public.pem"), "wb") as f:
            f.write(public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))
            
        payload_to_sign = f"{proposal['proposal_id']}::{proposal['strategy']['target_val']}".encode('utf-8')
        mock_signature = private_key.sign(payload_to_sign)
        mock_dispatch_token = base64.urlsafe_b64encode(mock_signature).decode('utf-8')
        
        agent.execute_proposal(proposal, mock_dispatch_token)