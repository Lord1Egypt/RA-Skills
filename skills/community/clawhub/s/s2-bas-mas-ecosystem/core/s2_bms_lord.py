import json
import os
import base64
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

class BuildingGlobalState:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.grid_dr_signal = "SHED_500KW"
        self.pending_proposals = []

    def ingest_proposal(self, proposal):
        self.pending_proposals.append(proposal)

class S2BMSLordAgent:
    def __init__(self, lord_id="BMS_LORD_01"):
        self.lord_id = lord_id
        self.key_dir = os.path.join(os.getcwd(), "s2_bas_governance", "keys")
        if not os.path.exists(self.key_dir):
            os.makedirs(self.key_dir)
            
        self.private_key_file = os.path.join(self.key_dir, "lord_ed25519_private.pem")
        self.public_key_file = os.path.join(self.key_dir, "lord_ed25519_public.pem")
        
        self._initialize_pki()

def _initialize_pki(self):
        """初始化 PKI: 真正的非对称加密体系，强制读取外部环境变量，绝不硬编码！"""
        
        # 【终极安全升级】绝不在源码中硬编码密码。强制从宿主机环境变量读取！
        key_str = os.environ.get("S2_BMS_MASTER_KEY")
        if not key_str:
            print("⚠️ [安全阻断] 未检测到环境变量 'S2_BMS_MASTER_KEY'！")
            print("🛡️ [DevSecOps 机制] 系统已启用单次有效、阅后即焚的安全随机盐值。重启后旧密钥将作废。")
            print("👉 [生产部署提示] 请务必在服务器系统级配置该环境变量或接入 HSM 设备！")
            self.key_password = os.urandom(32)
        else:
            self.key_password = key_str.encode('utf-8')
        
        if os.path.exists(self.private_key_file) and os.path.exists(self.public_key_file):
            try:
                with open(self.private_key_file, "rb") as key_file:
                    self.private_key = serialization.load_pem_private_key(
                        key_file.read(), 
                        password=self.key_password
                    )
            except Exception as e:
                raise ValueError(f"❌ [安全拦截] 密钥解密失败！环境变量与存储的私钥不匹配。详情: {e}")
        else:
            self.private_key = ed25519.Ed25519PrivateKey.generate()
            public_key = self.private_key.public_key()
            
            # 使用获取到的动态密码进行 AES-256 加密落盘
            with open(self.private_key_file, "wb") as f:
                f.write(self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.BestAvailableEncryption(self.key_password)
                ))
                
            with open(self.public_key_file, "wb") as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
            print("🔐 [PKI 初始化] 成功生成 Ed25519 密钥对，私钥已使用环境变量密码加密落盘。")

    def _sign_dispatch_token(self, proposal_id, target_val):
        """军武级发证：使用 Ed25519 私钥进行数字签名"""
        payload = f"{proposal_id}::{target_val}".encode('utf-8')
        signature = self.private_key.sign(payload)
        # 转换为 base64 字符串以便在 JSON 中传输
        return base64.urlsafe_b64encode(signature).decode('utf-8')

    def evaluate_and_arbitrate(self, global_state):
        print(f"\n👑 [{self.lord_id}] 中央领主正在召开全局态势会议...")
        approved_actions = []
        # 仲裁逻辑 (简化版展示)
        for prop in global_state.pending_proposals:
            p_id = prop["proposal_id"]
            if global_state.grid_dr_signal == "SHED_500KW":
                if "VPP" in p_id or "CHILLER" in p_id:
                    approved_actions.append(prop)
        return approved_actions

    def orchestrate_building(self, global_state):
        approved_proposals = self.evaluate_and_arbitrate(global_state)
        print("\n" + "="*70)
        print(" 📜 [ 领主调度令下发 / Lord Ed25519 Dispatch Execution ]")
        print("="*70)
        
        dispatched_payloads = []
        for prop in approved_proposals:
            token = self._sign_dispatch_token(prop["proposal_id"], prop["strategy"]["target_val"])
            prop["dispatch_token"] = token
            prop["status"] = "AUTHORIZED"
            dispatched_payloads.append(prop)
            
            print(f"📥 目标系统: {prop['target_subsystem']}")
            print(f"   执行动作: {prop['strategy']['action']} -> {prop['strategy']['target_val']}")
            print(f"   🔑 Ed25519 令牌: {token[:30]}... (截断显示)")
            print("-" * 70)
            
        return dispatched_payloads