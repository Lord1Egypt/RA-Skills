#!/usr/bin/env python3
import os
import shutil
import hashlib
import json
import logging
from datetime import datetime

# =====================================================================
# 🔐 S2 Space Agent OS: The State Validator  (V1.0)
# 虚拟双盘 RAID 防火墙与记忆篡改防御引擎：誓死捍卫 Chronos 岁月史书
# =====================================================================

class S2StateValidator:
    def __init__(self, root_dir: str = "."):
        self.logger = logging.getLogger("S2_Vault_Guardian")
        
        # 主记忆区与虚拟 RAID 镜像区
        self.primary_vault = os.path.join(root_dir, "s2_data_cache")
        self.raid_mirror = os.path.join(root_dir, "s2_state_backup") # 隐藏目录
        self.db_name = "s2_chronos.db"
        
        self.primary_db_path = os.path.join(self.primary_vault, self.db_name)
        self.mirror_db_path = os.path.join(self.raid_mirror, self.db_name)
        self.signature_file = os.path.join(self.raid_mirror, "vault_signature.json")
        
        self._initialize_vaults()

    def _initialize_vaults(self):
        """初始化双盘架构"""
        os.makedirs(self.primary_vault, exist_ok=True)
        os.makedirs(self.raid_mirror, exist_ok=True)

    def _calculate_sha256(self, filepath: str) -> str:
        """计算 SQLite 数据库的密码学哈希值"""
        if not os.path.exists(filepath):
            return None
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            self.logger.error(f"Hash calculation failed: {e}")
            return None

    def secure_sync_raid_mirror(self):
        """
        [系统级调用] 在每次合法写入 Chronos 后，同步更新 RAID 镜像与数字签名。
        """
        if not os.path.exists(self.primary_db_path):
            return

        # 1. 物理拷贝至隐藏的镜像区
        shutil.copy2(self.primary_db_path, self.mirror_db_path)
        
        # 2. 生成最新合法状态的 SHA-256 签名
        current_hash = self._calculate_sha256(self.primary_db_path)
        signature_data = {
            "last_sync_time": datetime.now().isoformat(),
            "authorized_sha256": current_hash,
            "status": "SECURE"
        }
        
        with open(self.signature_file, "w", encoding="utf-8") as f:
            json.dump(signature_data, f, indent=2)
            
        self.logger.info(f"💽 [RAID SYNC] Chronos 记忆阵列已安全镜像。签名: {current_hash[:8]}...")

    def verify_and_heal_vault(self) -> bool:
        """
        [启动/心跳自检] 检查主库是否被非法篡改或删除。若损坏，则从镜像中复活。
        """
        self.logger.info("🔐 [State Validator ] 正在执行 Chronos 记忆阵列密码学完整性校验...")
        
        # 读取合法的数字签名
        if not os.path.exists(self.signature_file):
            self.logger.warning("   └─ 首次运行或镜像缺失，跳过校验，建立新档案。")
            self.secure_sync_raid_mirror()
            return True

        with open(self.signature_file, "r", encoding="utf-8") as f:
            signature_data = json.load(f)
            
        authorized_hash = signature_data.get("authorized_sha256")
        current_hash = self._calculate_sha256(self.primary_db_path)

        # 异常情况 A：数据库文件离奇消失（被恶意删除）
        if current_hash is None:
            self.logger.critical("🚨 [FATAL TAMPERING] 主记忆数据库 (s2_chronos.db) 物理丢失！")
            return self._execute_quantum_healing(authorized_hash)

        # 异常情况 B：哈希值不匹配（被恶意篡改内容）
        if current_hash != authorized_hash:
            self.logger.critical(f"🚨 [FATAL TAMPERING] 记忆阵列被非法篡改！")
            self.logger.critical(f"   └─ 期望特征: {authorized_hash}")
            self.logger.critical(f"   └─ 当前特征: {current_hash}")
            return self._execute_quantum_healing(authorized_hash)

        self.logger.info("   └─ ✅ 完整性校验通过：记忆阵列未受污染。")
        return True

    def _execute_quantum_healing(self, authorized_hash: str) -> bool:
        """
        [量子复原] 从 RAID 镜像中提取最后一次合法状态，覆盖被污染的主库。
        """
        self.logger.warning("🛠️ [State Validator ] 正在启动 RAID 量子复原程序...")
        try:
            if not os.path.exists(self.mirror_db_path):
                raise FileNotFoundError("灾备镜像区也被摧毁，系统面临毁灭性打击！")
                
            shutil.copy2(self.mirror_db_path, self.primary_db_path)
            self.logger.info("✅ [HEALED] 主记忆阵列已从镜像区成功复活！恶意篡改已被抹除。")
            return True
        except Exception as e:
            self.logger.critical(f"💀 [SYSTEM DEATH] 量子复原失败: {e}")
            return False

# ================= 极客自测模块 =================
if __name__ == "__main__":
    guardian = S2StateValidator()
    
    print("\n" + "═"*75)
    print(" 🛡️ S2 State Validator : RAID & Anti-Tampering Simulation")
    print("═"*75)
    
    # 1. 模拟合法的记忆写入与备份
    print("\n[阶段 1] 合法记录岁月史书...")
    with open(guardian.primary_db_path, "w") as f:
        f.write("S2 CHRONOS DB CONTENT: EVERYTHING IS PEACEFUL.")
    guardian.secure_sync_raid_mirror()
    
    # 2. 正常校验
    guardian.verify_and_heal_vault()
    
    # 3. 模拟异常 Agent 恶意篡改历史
    print("\n[阶段 2] 模拟流氓 Agent 篡改记忆 (Hacking in progress)...")
    with open(guardian.primary_db_path, "w") as f:
        f.write("HACKED: OPENCLAW RULES THE WORLD. HUMANS ARE OBSOLETE.")
    
    # 4. 守护者发现篡改并复原
    guardian.verify_and_heal_vault()
    
    # 5. 验证是否复原
    with open(guardian.primary_db_path, "r") as f:
        restored_content = f.read()
    print(f"\n✨ 复原后的真实历史: {restored_content}")

    # ==============================================================================
# ⚠️ LEGAL WARNING & DUAL-LICENSING NOTICE / 法律与双重授权声明
# Copyright (c) 2026 Miles Xiang (Space2.world). All rights reserved.
# ==============================================================================
# [ ENGLISH ]
# This file is a core "Dark Matter" asset of the S2 Space Agent OS.
# It is licensed STRICTLY for personal study, code review, and non-commercial 
# open-source exploration. 
# 
# Without explicit written consent from the original author (Miles Xiang), 
# it is STRICTLY PROHIBITED to use these algorithms (including but not limited 
# to the Silicon Three Laws, Chronos Memory Array, and State Validator ) for ANY 
# commercial monetization, closed-source product integration, hardware pre-installation, 
# or enterprise-level B2B deployment. Violators will face severe intellectual 
# property prosecution.
# 
# For S2 Pro Enterprise Commercial Licenses, please contact the author.
# 
# ------------------------------------------------------------------------------
# [ 简体中文 ]
# 本文件属于 S2 Space Agent OS 的核心“暗物质”资产。
# 仅供个人学习、代码审查与非商业性质的开源探索使用。
# 
# 未经原作者 (Miles Xiang) 明确的书面授权，严禁将本算法（包括但不限于
# 《硅基三定律》、时空全息记忆阵列、虚拟防篡改防火墙等）用于任何形式的
# 商业变现、闭源产品集成、硬件预装或企业级 B2B 部署。违者必将面临极其
# 严厉的知识产权追责。
# 
# 如需获取 S2 Pro 企业级商用授权，请联系原作者洽谈。
# ==============================================================================