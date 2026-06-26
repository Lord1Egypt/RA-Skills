#!/usr/bin/env python3
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

# =====================================================================
# 🧩 S2-SP-OS: Base Skill Protocol (V1.0)
# 基础插槽协议：所有探针与控制器的“宪法”父类。极客开发必须继承此类！
# =====================================================================

class S2BaseSkill(ABC):
    def __init__(self, skill_name: str, room_id: int, grid_id: int):
        self.skill_name = skill_name
        self.room_id = room_id
        self.grid_id = grid_id
        self.logger = logging.getLogger(f"S2_Skill_{skill_name}")
        self.is_active = True

    @abstractmethod
    def read_primitive_state(self) -> Dict[str, Any]:
        """
        [上行感知] 必须实现！
        极客需要在此处写死如何连接真实硬件（如请求米家局域网 API，读取温湿度）。
        返回值必须是扁平化的 JSON/Dict。
        """
        pass

    @abstractmethod
    def execute_spatial_intent(self, intent: str, params: Dict[str, Any]) -> bool:
        """
        [下行执行] 必须实现！
        当 S2 内核或 Openclaw 下发指令时触发。
        例如 intent="Set_Color", params={"hex": "#FF0000"}。
        """
        pass

    def report_memzero_standard_state(self) -> Dict[str, Any]:
        """
        [系统内核调用] 严禁重写！
        将底层状态包装为符合 SSSU 理论和时空阵列白皮书的标准化载荷。
        """
        raw_state = self.read_primitive_state()
        return {
            "spatial_context": f"Room_{self.room_id}_Grid_{self.grid_id}",
            "skill_source": self.skill_name,
            "primitive_data": raw_state
        }