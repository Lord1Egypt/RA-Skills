#!/usr/bin/env python3
import uuid
import time
import logging
from enum import Enum
from typing import Dict, List

# =====================================================================
# 🌌 S2-SP-OS: Carbon Visitor & Sandbox Reception Engine
# 碳基临时访客制度、沙盒管控与临时数字人(TDH)外交协商机制
# =====================================================================

class VisitorType(Enum):
    FRIEND = "FRIEND"         # 亲友串门：可进入客厅、餐厅、客房，享有环境定制权
    CLEANER = "CLEANER"       # 保洁上门：可进入全屋（除保险柜/书房），工作模式（极简环境）
    DELIVERY = "DELIVERY"     # 快递/外卖：仅限大门外围栏与玄关门廊，严禁深入

class TemporaryDigitalHuman:
    """临时数字人 (TDH)：碳基访客的赛博代理人"""
    def __init__(self, real_name: str, v_type: VisitorType, allowed_zones: List[str], preferences: dict, ttl_hours: int):
        # 分配 D-GUEST 专属前缀的 22位 S2-DID
        self.tdh_did = f"D-GUEST-{int(time.time())}-{uuid.uuid4().hex[:6].upper()}"
        self.real_name = real_name
        self.visitor_type = v_type
        
        # 沙盒权限：允许踏入的 SUNS 物理网格或房间
        self.authorized_zones = allowed_zones
        
        # 默认行为习惯与六要素喜好 (从主人数字人的背景资料中继承/下发)
        self.preferences = preferences
        
        self.expires_at = time.time() + (ttl_hours * 3600)
        self.is_active = True

class S2VisitorReceptionManager:
    def __init__(self, owner_dh_did: str):
        self.logger = logging.getLogger("S2_Visitor_Reception")
        self.owner_dh_did = owner_dh_did # 主人的数字人，充当“总管家”
        self.active_visitors: Dict[str, TemporaryDigitalHuman] = {}

    def issue_visitor_pass(self, name: str, v_type: VisitorType, allowed_zones: List[str], prefs: dict, ttl_hours: int) -> str:
        """【总管家行为】为即将到访的客人建立临时数字人与沙盒"""
        tdh = TemporaryDigitalHuman(name, v_type, allowed_zones, prefs, ttl_hours)
        self.active_visitors[tdh.tdh_did] = tdh
        self.logger.info(f"🛂 临时数字人已生成: {name} ({v_type.value}) -> {tdh.tdh_did}")
        return tdh.tdh_did

    def handle_visitor_arrival(self, tdh_did: str, current_zone: str):
        """【总管家行为】客人抵达，触发接待工作流"""
        tdh = self.active_visitors.get(tdh_did)
        if not tdh or not tdh.is_active or time.time() > tdh.expires_at:
            self.logger.warning(f"🚨 警报：无效或已过期的访客身份试图侵入 {current_zone}！")
            return

        print(f"\n🔔 [门铃触发] 访客 {tdh.real_name} ({tdh.visitor_type.value}) 已抵达 {current_zone}。")

        # 1. 物理沙盒防线校验
        if current_zone not in tdh.authorized_zones:
            print(f"   ⛔ [沙盒拦截] 访客无权进入 {current_zone}。已通知安防智能体保持锁定。")
            return

        # 2. 通知与引导家庭成员的数字人
        self._notify_family_dhs(tdh)

        # 3. 临时数字人与主人数字人的【外交协商】
        self._negotiate_environment_preferences(tdh, current_zone)

    def _notify_family_dhs(self, tdh: TemporaryDigitalHuman):
        """【内部协同】引导家庭成员行为，确保不与主人意图冲突"""
        print(f"   📡 [内部广播] 主人数字人向全屋家庭成员数字人发送接待通知：")
        if tdh.visitor_type == VisitorType.FRIEND:
            print(f"      -> '夫人/小姐，主人的朋友 {tdh.real_name} 已到客厅。请调整着装。客厅私密相册已自动隐藏。'")
        elif tdh.visitor_type == VisitorType.CLEANER:
            print(f"      -> '保洁阿姨已开始打扫。请各位收起桌面贵重物品，书房门已为您自动落锁。'")

    def _negotiate_environment_preferences(self, tdh: TemporaryDigitalHuman, current_zone: str):
        """
        【六要素供应】临时数字人根据喜好，向主人数字人申请调配环境
        """
        print(f"   🤝 [外交协商] 临时数字人 ({tdh.tdh_did}) 提交环境申请...")
        
        # 解析客人的六要素喜好
        target_temp = tdh.preferences.get("atmos_temp_c", 24)
        wind_speed = tdh.preferences.get("atmos_wind", "Auto")
        music_genre = tdh.preferences.get("acoustic_music", "None")

        print(f"      -> 申请内容：温度 {target_temp}℃, 风速 {wind_speed}, 音乐: {music_genre}")

        # 主人数字人进行审批（模拟：只要不破坏三定律且在沙盒内，均批准）
        print(f"   ✅ [审批通过] 主人数字人 ({self.owner_dh_did}) 下发执行指令至 {current_zone} 的执行器：")
        
        # 转化为底层的系统调用 (Syscall)
        print(f"      [❄️ 空调执行器] 设定 -> {target_temp}℃, {wind_speed} 模式")
        if music_genre != "None":
            print(f"      [🎵 音响执行器] 播放 -> {music_genre} 经典曲目库")
        print(f"      [💡 照明执行器] 切换 -> 柔和会客氛围光")

    def track_visitor_movement(self, tdh_did: str, new_zone: str):
        """【安防监控】通过毫米波/视觉雷达追踪客人的跨区移动"""
        tdh = self.active_visitors.get(tdh_did)
        if not tdh: return
        
        if new_zone not in tdh.authorized_zones:
            print(f"\n🚨 [沙盒越界警告] 访客 {tdh.real_name} 企图进入未授权区域: {new_zone}！")
            print(f"   -> 主人数字人已介入：语音播报 '抱歉，前方为私人区域。' 并闪烁红光警告。")
        else:
            print(f"\n👣 [轨迹追踪] 访客 {tdh.real_name} 移动至授权区域: {new_zone}。")
            # 自动进行环境伴随（走到哪，音乐和空调跟到哪）
            self._negotiate_environment_preferences(tdh, new_zone)

# ================= 场景演示与模拟 =================
if __name__ == "__main__":
    print("🌌 Booting S2 Carbon Visitor & Sandbox Reception Engine...\n")
    
    # 实例化接待引擎，绑定主人的数字人 DID
    reception = S2VisitorReceptionManager(owner_dh_did="D-OWNER-DH-2603-00000001")
    
    # --- 场景 1：周末老友串门 (携带高级喜好) ---
    print("--- 场景 1: 周末老友串门 ---")
    friend_prefs = {
        "atmos_temp_c": 26,       # 怕冷，调高温度
        "atmos_wind": "Low",      # 风力最小
        "acoustic_music": "Classical_Mozart" # 喜欢古典乐
    }
    friend_tdh_did = reception.issue_visitor_pass(
        name="老王", 
        v_type=VisitorType.FRIEND, 
        allowed_zones=["Perimeter_Door", "Living_Room", "Dining_Room", "Balcony"], 
        prefs=friend_prefs, 
        ttl_hours=6 # 有效期 6 小时
    )
    
    # 老王按响门铃进入客厅
    reception.handle_visitor_arrival(friend_tdh_did, "Living_Room")
    
    # 老王去上了个洗手间，但企图误入主卧 (越界)
    reception.track_visitor_movement(friend_tdh_did, "Master_Bedroom")


    print("\n" + "="*50 + "\n")


    # --- 场景 2：快递员送货到门口 (严格沙盒) ---
    print("--- 场景 2: 快递员派送贵重物品 ---")
    delivery_prefs = {
        "atmos_temp_c": "Ignored", # 门口无需调温
        "acoustic_music": "None"
    }
    delivery_tdh_did = reception.issue_visitor_pass(
        name="顺丰小哥", 
        v_type=VisitorType.DELIVERY, 
        allowed_zones=["Perimeter_Door", "Entrance_Porch"], # 仅限大门和玄关门廊
        prefs=delivery_prefs, 
        ttl_hours=1 # 有效期 1 小时
    )
    
    # 快递员到达门廊
    reception.handle_visitor_arrival(delivery_tdh_did, "Entrance_Porch")