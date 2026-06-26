#!/usr/bin/env python3
import json
import argparse
from datetime import datetime

# =====================================================================
# 导入 5 大维度拆分的空间极客字典
# =====================================================================
from dict_01_residential_core import RESIDENTIAL_CORE
from dict_02_leisure_outdoor import LEISURE_OUTDOOR
from dict_03_commercial_hospitality import COMMERCIAL_HOSPITALITY
from dict_04_office_industrial import OFFICE_INDUSTRIAL
from dict_05_health_mobility import HEALTH_MOBILITY

# =====================================================================
# 🌌 S2-SP-OS: Universal Home Space Parser Engine (V1.0)
# 全宇宙智能空间六要素终极满配字典解析核心
# =====================================================================

class S2SpaceParser:
    def __init__(self):
        # 组装完整的全宇宙空间库字典 (共 62 个空间)
        self.master_dictionary = {}
        self.master_dictionary.update(RESIDENTIAL_CORE)
        self.master_dictionary.update(LEISURE_OUTDOOR)
        self.master_dictionary.update(COMMERCIAL_HOSPITALITY)
        self.master_dictionary.update(OFFICE_INDUSTRIAL)
        self.master_dictionary.update(HEALTH_MOBILITY)
        
        # S2 系统必备的底层基础设施 (Foundation)
        self.base_infrastructure = [
            {"element": "电磁", "process": "计算/连接", "name": "S2 OS 边缘计算大本营主机 (Local Agent Host)"},
            {"element": "电磁", "process": "连接", "name": "全域覆盖 Wi-Fi 7/Matter/Zigbee 无线网络底座"},
            {"element": "能", "process": "计算", "name": "全域强电箱智能微断总闸 (物理最后一道防线)"}
        ]

    def parse_space(self, space_query: str) -> dict:
        """根据输入的语义空间，解析出《S2-SSSU 六要素满配字典》"""
        target_space = None
        for key in self.master_dictionary.keys():
            # 模糊路由匹配，如输入 "客厅" 自动命中 "智慧客厅"
            if space_query in key or key in space_query:
                target_space = key
                break
                
        if not target_space:
            return self._generate_generic_space(space_query)

        space_data = self.master_dictionary[target_space]
        full_hardware = self.base_infrastructure + space_data["hardware_matrix"]
        
        return {
            "s2_sssu_version": "2026-V1.0",
            "space_query": target_space,
            "description": space_data["description"],
            "total_components_suggested": len(full_hardware),
            "s2_6_element_matrix": self._group_by_elements(full_hardware),
            "recommended_scenarios": space_data["default_scenarios"],
            "agent_instruction": "本清单为【顶配穷举词典】。AI 或设计师应根据用户的『真实预算』与『管线条件』进行精准裁减 (Pruning)，而非无脑堆砌。"
        }

    def _group_by_elements(self, hardware_list: list) -> dict:
        """将扁平的硬件列表编织为 S2 的六维张量矩阵"""
        grouped = {"Light_光": [], "Air_气": [], "Sound_声": [], "EM_电磁": [], "Energy_能": [], "Vision_视": []}
        
        mapping = {
            "光": "Light_光", "气": "Air_气", "声": "Sound_声",
            "电磁": "EM_电磁", "能": "Energy_能", "视": "Vision_视"
        }
        
        for item in hardware_list:
            if item["element"] in mapping:
                grouped[mapping[item["element"]]].append(f"[{item['process']}] {item['name']}")
        return grouped

    def _generate_generic_space(self, query: str) -> dict:
        """未知空间的泛用兜底配置 (Generic Fallback)"""
        generic_hw = self.base_infrastructure.copy()
        generic_hw.extend([
            {"element": "光", "process": "执行", "name": "标准 DALI/Zigbee 调光照明回路"},
            {"element": "电磁", "process": "感知", "name": "基础版毫米波人体存在传感器"},
            {"element": "声", "process": "交互", "name": "通用情景唤醒触控/语音面板"}
        ])
        return {
            "s2_sssu_version": "2026-V1.0",
            "space_query": query,
            "description": "未硬编码的泛用智能空间扩展配置",
            "total_components_suggested": len(generic_hw),
            "s2_6_element_matrix": self._group_by_elements(generic_hw),
            "recommended_scenarios": ["全局唤醒模式", "全局休眠模式"],
            "agent_instruction": "未精确匹配到 62 大标准空间，已调用底层泛用 SSSU 基元模块。"
        }

# =====================================================================
# 命令行调试入口 (CLI)
# =====================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S2 Universal Space Configurator Engine")
    parser.add_argument("--space", required=True, help="输入空间名 (如: 智能卧室, 智慧工厂车间, 智能车内空间)")
    args = parser.parse_args()

    engine = S2SpaceParser()
    result = engine.parse_space(args.space)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))