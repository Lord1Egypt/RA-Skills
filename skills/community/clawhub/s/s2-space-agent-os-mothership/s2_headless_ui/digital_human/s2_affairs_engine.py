#!/usr/bin/env python3
import time
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Optional

# 导入底层依赖 (假设)
from s2_kernel.rights.s2_family_rights import S2FamilyFederation, S2CarbonProfile
from s2_kernel.chronos.s2_asset_vault import S2AssetVault, AssetType

# =====================================================================
# 🌌 S2-SP-OS: Spatial Affairs & Schedule Engine (V1.0 Prototype)
# 基于 TDOG 理论的家庭日程、空间留言与纪事演化框架
# =====================================================================

class AffairType:
    SPATIAL_MESSAGE = "SPATIAL_MESSAGE"   # 空间触发留言 (走到哪播到哪)
    CHRONOS_TASK = "CHRONOS_TASK"         # 时序触发任务 (到点执行)
    MILESTONE = "MILESTONE"               # 家庭重大纪事 (永久存档)

class S2AffairObject:
    """动态事务对象：在 SSSU 标准空间内动态生成的服务实例"""
    def __init__(self, creator_id: str, affair_type: str, content: str):
        self.affair_id = f"AFF-{uuid.uuid4().hex[:8].upper()}"
        self.creator_id = creator_id
        self.affair_type = affair_type
        self.content = content
        
        # 触发条件池
        self.target_carbon_id: Optional[str] = None  # 针对特定家庭成员
        self.trigger_zone: Optional[str] = None      # 空间触发条件 (SSSU 网格)
        self.trigger_time: Optional[float] = None    # 时间触发条件
        
        self.is_completed = False
        self.created_at = time.time()

class S2AffairsManager:
    def __init__(self, family_federation: S2FamilyFederation, asset_vault: S2AssetVault):
        self.logger = logging.getLogger("S2_Affairs_Manager")
        self.federation = family_federation
        self.vault = asset_vault
        self.active_affairs: List[S2AffairObject] = []

    # ---------------------------------------------------------
    # 模块 1：无感/自然语言的意图解析与事务生成
    # ---------------------------------------------------------
    def parse_natural_language_affair(self, speaker_id: str, nlp_text: str, current_zone: str):
        """
        [大模型意图提炼层]
        将随口的一句闲聊，转化为结构化的空间事务对象。
        """
        self.logger.info(f"🎙️ 捕捉到事务意图 [{speaker_id}]: '{nlp_text}'")
        
        # 模拟 LLM 的动态解析逻辑
        if "告诉" in nlp_text and "回来" in nlp_text:
            # 例如："告诉小明回来记得喝桌上的牛奶"
            # 提取目标人物、内容，自动推断触发空间（餐厅/玄关）
            target_nickname = "小明"  # 真实中由 LLM 提取
            target_profile = self._find_member_by_nickname(target_nickname)
            
            if target_profile:
                affair = S2AffairObject(speaker_id, AffairType.SPATIAL_MESSAGE, "记得喝桌上的牛奶")
                affair.target_carbon_id = target_profile.carbon_id
                affair.trigger_zone = "Dining_Room" # AI 智能推断的 SSSU 网格
                self.active_affairs.append(affair)
                self._vibe_feedback("Success_Chime", f"好的，等{target_nickname}到餐厅时我会提醒他。")
                
        elif "提醒" in nlp_text and "点" in nlp_text:
            # 例如："提醒我明早8点带宠物去体检"
            affair = S2AffairObject(speaker_id, AffairType.CHRONOS_TASK, "带宠物去体检")
            affair.target_carbon_id = speaker_id
            affair.trigger_time = time.time() + 36000 # 模拟解析出的未来时间戳
            self.active_affairs.append(affair)
            self._vibe_feedback("Success_Chime", "已为您加入明日时序日程。")
            
        elif "记录一下" in nlp_text:
            # 例如："记录一下，今天旺财终于学会握手了"
            self._archive_milestone(speaker_id, nlp_text.replace("记录一下，", ""), current_zone)

    def _find_member_by_nickname(self, nickname: str) -> Optional[S2CarbonProfile]:
        for profile in self.federation.family_db.values():
            if profile.nickname == nickname:
                return profile
        return None

    # ---------------------------------------------------------
    # 模块 2：基于空间漫游的触发机制 (Spatial Triggering)
    # ---------------------------------------------------------
    def evaluate_spatial_triggers(self, current_carbon_id: str, current_zone: str):
        """
        当感知雷达发现某人进入某网格时，不断调用此方法，检查是否有属于TA的“悬浮留言”。
        """
        for affair in self.active_affairs:
            if not affair.is_completed and affair.affair_type == AffairType.SPATIAL_MESSAGE:
                # 如果人对了，且空间对了
                if affair.target_carbon_id == current_carbon_id and affair.trigger_zone == current_zone:
                    self._deliver_spatial_message(affair)
                    affair.is_completed = True

    def _deliver_spatial_message(self, affair: S2AffairObject):
        """通过无头交互 (声/光) 自然地传达信息"""
        creator = self.federation.family_db.get(affair.creator_id)
        creator_name = creator.relation if creator else "家人"
        
        print(f"\n✨ [空间对象解冻触发] 目标人物进入 {affair.trigger_zone}。")
        print(f"   🔊 柔和播报: '您好，您的{creator_name}给您留了言：{affair.content}'")

    # ---------------------------------------------------------
    # 模块 3：家庭纪事与时空胶囊 (Milestones)
    # ---------------------------------------------------------
    def _archive_milestone(self, creator_id: str, content: str, zone: str):
        """将重大纪事转化为永久的数据资产，存入 Semantic Vault"""
        print(f"\n📦 [家庭纪事归档] 正在生成时空胶囊...")
        
        # 联动数据资产保险柜
        asset_id = self.vault.ingest_asset(
            uploader_did="FAMILY_PUBLIC",
            asset_type=AssetType.DOCUMENT,
            storage_uri="virtual_vault://milestones/text_record.md",
            semantic_description=f"{zone}, 纪念日, 家庭纪事, 珍贵回忆, {content}",
            spatial_zone=zone
        )
        self._vibe_feedback("Warm_Chime", "这段珍贵的记忆已为您永久锁入家庭时空胶囊。")

    def _vibe_feedback(self, vibe_type: str, text: str):
        print(f"   [Vibe UI] ({vibe_type}) -> {text}")


# ================= 场景演示 =================
if __name__ == "__main__":
    print("🌌 Booting Spatial Affairs & Schedule Engine...\n")
    
    # 模拟底座
    federation = S2FamilyFederation()
    vault = S2AssetVault()
    
    # 初始化成员
    wife_id = federation.register_family_member("D-OWNER-001", "wife@s2.local", "王美丽", "美丽", "妻子")
    son_id = federation.register_family_member("D-OWNER-001", "son@s2.local", "李小明", "小明", "儿子")
    
    manager = S2AffairsManager(federation, vault)
    
    print("--- 场景 1: 自然语言生成【空间触发型留言】 ---")
    # 妻子在卧室化妆时随口一说，不需要点开任何 App
    manager.parse_natural_language_affair(
        speaker_id=wife_id, 
        nlp_text="告诉小明回来记得喝桌上的牛奶", 
        current_zone="Master_Bedroom"
    )
    
    print("\n--- 场景 2: 儿子回家漫游至餐厅，触发空间留言 ---")
    # 儿子回家，先到了玄关，没有触发
    manager.evaluate_spatial_triggers(current_carbon_id=son_id, current_zone="Entrance_Porch")
    
    # 儿子走到餐厅网格，环境雷达锁定，立刻触发播报！
    manager.evaluate_spatial_triggers(current_carbon_id=son_id, current_zone="Dining_Room")
    
    print("\n--- 场景 3: 生成【家庭重大纪事】并永久入库 ---")
    manager.parse_natural_language_affair(
        speaker_id=wife_id,
        nlp_text="记录一下，今天小明第一次自己做熟了煎鸡蛋",
        current_zone="Kitchen"
    )