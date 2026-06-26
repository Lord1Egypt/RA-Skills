#!/usr/bin/env python3
import time
import json
import logging
from typing import List

# 导入底层暗物质内核与积木插槽
from s2_kernel.security.s2_fortress_boot import S2FortressEngine, FortressState
from s2_kernel.laws.s2_os_kernel import S2KernelHypervisor, S2SiliconLawViolation
from s2_skills.s2_base_skill import S2BaseSkill
from s2_headless_ui.intent_parser.s2_llm_parser import S2IntentParser

# =====================================================================
# 🌌 S2-SP-OS: Digital Human Federation Dispatch Center
# 联邦调度中心：统管 Memzero 融合、内核法律审查与物理世界反馈
# =====================================================================

class S2DigitalHumanFederation:
    def __init__(self, digital_human_did: str, kernel: S2KernelHypervisor, fortress: S2FortressEngine):
        self.dh_did = digital_human_did # e.g., "D-MYTHX-260309-XX-00000001"
        self.kernel = kernel
        self.fortress = fortress
        self.parser = S2IntentParser()
        self.loaded_skills: List[S2BaseSkill] = []
        self.logger = logging.getLogger("S2_Federation_Center")

    def register_skills(self, skills: List[S2BaseSkill]):
        """将加载好的 80% 积木探针插入调度中心"""
        self.loaded_skills.extend(skills)
        self.logger.info(f"Federation Center registered {len(skills)} peripheral skills.")

    def _gather_global_memzero(self) -> dict:
        """【空间感知融合】收集所有 2m*2m 标准网格单元内的六要素切片"""
        context = {}
        for skill in self.loaded_skills:
            # 统一调用积木的 generate_memzero_payload 方法
            context[skill.skill_name] = skill.generate_memzero_payload()
        return context

    def process_human_voice_command(self, voice_text: str, room_id: int, grid_id: int, is_physical_override: bool = False):
        """
        核心事件流：处理人类指令
        """
        print(f"\n[{self.dh_did}] 接收到指令输入 (Room:{room_id}, Grid:{grid_id}): '{voice_text}'")

        # 1. 堡垒自检：防盗锁死状态下拒绝一切交互
        if self.fortress.state == FortressState.HARD_LOCK:
            self._vibe_feedback("Error_Tone", "系统处于防盗锁定状态，拒绝执行。请通过虚拟空间发起双重认证解锁。")
            return

        # 2. 收集当前物理空间状态 (Memzero)
        current_context = self._gather_global_memzero()

        # 3. 意图解析 (动态生成对象命令)
        intent_payload = self.parser.parse_to_syscall(voice_text, current_context)
        
        if not intent_payload["is_valid"]:
            self._vibe_feedback("Confusion_Tone", "抱歉主人，我没有完全理解您的意图，空间状态保持不变。")
            return

        # 4. 执行与内核审查 (Federation Dispatch)
        success_count = 0
        for task in intent_payload["target_skills"]:
            target_skill_name = task["skill"]
            specific_intent = task["intent"]
            params = task["params"]

            # 寻找对应的硬件插槽
            target_skill = next((s for s in self.loaded_skills if s.skill_name == target_skill_name), None)
            if not target_skill:
                continue

            try:
                # 🛡️ 过内核安全门：三定律、产权校验
                # 这里必须携带数字人的 DID 和 物理越权标志
                self.kernel.execute_skill_action(
                    zone=f"Room_{room_id}", 
                    grid=f"Grid_{grid_id}", 
                    agent_token=self.dh_did, 
                    action_intent=specific_intent,
                    human_override=is_physical_override
                )
                
                # ⚡ 内核放行，真实触发积木底层的 HA/BACnet/KNX 代码！
                executed = target_skill.execute_command(specific_intent, **params)
                if executed: success_count += 1

            except S2SiliconLawViolation as law_e:
                self._vibe_feedback("Warning_Flash", f"指令被硅基定律拦截：{law_e}")
                return # 熔断后续操作

        # 5. 无头交互反馈 (Headless Vibe UI)
        if success_count > 0:
            self._vibe_feedback("Success_Chime", intent_payload["verbal_feedback"])


    def _vibe_feedback(self, vibe_type: str, spoken_words: str):
        """无头反馈层：通过声学模块和光环境传达状态，取代屏幕 UI"""
        print(f"   ✨ [Vibe UI 反馈]: ({vibe_type}) -> 🔊 '{spoken_words}'")
        
        # 在真实环境中，这里会反向调用 s2-acoustic 播放音效与 TTS
        # 反向调用 s2-light 让主灯柔和呼吸闪烁一次


# ================= 联邦指挥中心联调测试 =================
if __name__ == "__main__":
    from s2_skills.perception.s2_hvac_perception import S2HVACSkill
    from s2_skills.perception.s2_light_perception import S2LightSkill
    from s2_kernel.security.s2_fortress_boot import S2FortressEngine
    
    # 假设这段代码是主入口 main()
    print("🌌 Booting S2-SP-OS Digital Human Federation Center...\n")
    
    # 初始化核心暗物质 (Kernel & Fortress)
    import hashlib
    master_gps = hashlib.sha256(b"39.9,116.4,S2_SALT").hexdigest()
    kernel = S2KernelHypervisor(boot_gps_hash=master_gps)
    fortress = S2FortressEngine()
    fortress.state = FortressState.SECURE # 假定主机安全
    
    # 注册数字人的最高管理权 (在 101 号房间的沙发区)
    DH_DID = "D-MYTHX-260309-XX-88888888"
    kernel.rights.register_grid_owner("Room_101", "Grid_1", DH_DID)
    
    # 启动联邦中心
    federation = S2DigitalHumanFederation(DH_DID, kernel, fortress)
    
    # 载入积木 (开启仿真模式跑通流程)
    federation.register_skills([
        S2HVACSkill(room_id=101, grid_id=1, simulation_mode=True),
        S2LightSkill(room_id=101, grid_id=1, simulation_mode=True)
    ])
    
    print("-" * 50)
    # 模拟主人的自然交互 1：舒适度模糊指令
    federation.process_human_voice_command("感觉屋里有点太闷热了", room_id=101, grid_id=1)
    
    print("-" * 50)
    # 模拟主人的自然交互 2：物理越权冲突测试 (假定雷达侦测到主人正在手动关灯)
    federation.process_human_voice_command("睡觉吧", room_id=101, grid_id=1, is_physical_override=True)