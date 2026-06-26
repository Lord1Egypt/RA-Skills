#!/usr/bin/env python3
import random
import json
from s2_skills.s2_base_skill import S2BaseSkill

# =====================================================================
# 🌊 S2-SP-OS: Spectrum Perception Skill (波段雷达积木)
# 职责：探测 2m*2m 网格内的人体占位、心率、呼吸与睡眠状态
# =====================================================================

class S2SpectrumRadarSkill(S2BaseSkill):
    def __init__(self, room_id: int, grid_id: int):
        # 继承基类插槽，注册技能名称
        super().__init__(skill_name="s2-spectrum-perception", room_id=room_id, grid_id=grid_id)
        
        # 模拟雷达硬件的 IP 或串口地址
        self.hardware_endpoint = f"192.168.1.1{grid_id}:8080"

    def read_sensor_data(self) -> dict:
        """
        覆盖基类方法：通过局域网或 RS485 获取真实的毫米波雷达点云数据
        这里我们模拟生成空间网格内的生物体征数据。
        """
        # 模拟：神圣保留地(Grid 1)通常有人(数字人或主人在沙发)，其他区域随机
        is_occupied = True if self.grid_id == 1 else random.choice([True, False])
        
        if not is_occupied:
            return {
                "occupancy": False,
                "bio_presence": "None"
            }
            
        # 如果有人，计算呼吸和心率推演其微观状态
        heart_rate = random.randint(50, 100)
        respiration_rate = random.randint(12, 20)
        
        # 根据心率推断当前网格内硅基/碳基主人的状态 (静坐、睡眠、运动)
        activity_state = "Awake_Resting"
        if heart_rate < 60:
            activity_state = "Deep_Sleep"
        elif heart_rate > 90:
            activity_state = "Active_Motion"

        return {
            "occupancy": True,
            "heart_rate_bpm": heart_rate,
            "respiration_rpm": respiration_rate,
            "activity_state": activity_state,
            "posture": random.choice(["Sitting", "Lying", "Standing"])
        }

    def execute_command(self, action_intent: str, **kwargs) -> bool:
        """毫米波雷达通常是只读的，但也可能支持调整扫描灵敏度"""
        if action_intent == "Increase_Sensitivity":
            print(f"[雷达硬件 {self.suns_locator}] 灵敏度已上调至 100%")
            return True
        elif action_intent == "Sleep_Mode_Scan":
            print(f"[雷达硬件 {self.suns_locator}] 已切换至微动睡眠探测模式")
            return True
        else:
            print(f"Unsupported command for Spectrum Radar: {action_intent}")
            return False

# ================= 单元测试 =================
if __name__ == "__main__":
    print("🌊 Booting S2 Spectrum Radar Skill...\n")
    
    # 实例化一个负责监控客厅 (Room 101) 核心沙发区 (Grid 1) 的雷达积木
    radar_skill = S2SpectrumRadarSkill(room_id=101, grid_id=1)
    
    # OS Kernel 调用探针，获取标准的 Memzero 记忆帧
    memzero_frame = radar_skill.generate_memzero_payload()
    
    print("📦 发送给 OS Kernel (Hypervisor) 的标准数据帧：")
    print(json.dumps(memzero_frame, indent=2, ensure_ascii=False))