import os
import json
import random
from datetime import datetime

class S2BASIdentityRegistry:
    # 🌍 SUNS v3.0 法定的 9 大方位矩阵代码
    VALID_L2_ORIENTATIONS = {"CN", "EA", "WA", "NA", "SA", "NE", "NW", "SE", "SW"}

    def __init__(self):
        self.registry_dir = os.path.join(os.getcwd(), "s2_bas_governance")
        self.registry_file = os.path.join(self.registry_dir, "building_sovereignty_ledger.json")
        
        if not os.path.exists(self.registry_dir):
            os.makedirs(self.registry_dir)
            
        self.ledger = self._load_ledger()

    def _load_ledger(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "building_base_address": None,
            "central_lord_agent": None,
            "sub_system_agents": []
        }

    def _save_ledger(self):
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(self.ledger, f, ensure_ascii=False, indent=2)

    def generate_building_address(self, building_name_eng: str, l2_orientation: str = "CN"):
        """
        生成智能建筑的 SUNS v3.0 四段式空间基础地址。
        引入 L2 方位矩阵严格校验与 X 长度模数校验。
        """
        if self.ledger.get("building_base_address"):
            print(f"⚠️ [警告] 该物理服务器已绑定建筑主权地址：{self.ledger['building_base_address']}。不可重复注册。")
            return self.ledger["building_base_address"]

        # 清洗建筑名 (L4)
        clean_name = ''.join(e for e in building_name_eng if e.isalnum())
        if len(clean_name) < 5:
            clean_name = clean_name.ljust(5, 'X')
        elif len(clean_name) > 35:
            clean_name = clean_name[:35]

        # 校验 L2 方位矩阵 (防呆设计)
        l2_upper = l2_orientation.strip().upper()
        if l2_upper not in self.VALID_L2_ORIENTATIONS:
            print(f"⚠️ [提示] 输入的方位码 '{l2_upper}' 非法。已自动回退至默认主矩阵 'CN' (Center)。")
            l2 = "CN"
        else:
            l2 = l2_upper

        l1 = "PHSY"
        l3 = f"{random.randint(1, 999):03d}"
        l4_base = clean_name
        
        # 结构化连字符计算 (连字符 '-' 强制计入长度)
        base_string = f"{l1}-{l2}-{l3}-{l4_base}"
        total_chars = len(base_string)
        
        # 个位模数校验算法 (LMC)
        x_val = total_chars % 10
        
        # 最终拼接
        final_base_address = f"{base_string}{x_val}"
        
        self.ledger["building_base_address"] = final_base_address
        self.ledger["l4_prefix_5"] = l4_base[:5].upper() # 供 S2-DID 提取血统
        
        self._save_ledger()
        print(f"🏢 [建筑主权确立] 成功生成 SUNS 空间基座地址: {final_base_address}")
        return final_base_address

    def generate_s2_did(self):
        """生成 22 位 Class V 原生智能体身份编号"""
        prefix = "V"
        name_attr = self.ledger["l4_prefix_5"]
        date_str = datetime.now().strftime("%y%m%d")
        checksum = "AA"
        serial = f"{random.randint(1, 99999999):08d}"
        return f"{prefix}{name_attr}{date_str}{checksum}{serial}"

    def register_central_lord_agent(self):
        """强制为大楼生成拥有最高权限的【中央智能体】(固定扩展地址 -1-1)"""
        if not self.ledger.get("building_base_address"):
            raise ValueError("必须先生成建筑基础地址！")
        if self.ledger.get("central_lord_agent"):
            return self.ledger["central_lord_agent"]

        central_address = f"{self.ledger['building_base_address']}-1-1"
        did = self.generate_s2_did()

        agent_data = {
            "role": "S2-BMS-Lord",
            "spatial_address": central_address,
            "s2_did": did,
            "registration_time": datetime.now().isoformat()
        }
        self.ledger["central_lord_agent"] = agent_data
        self._save_ledger()
        print(f"👑 [领主登基] 中央大脑入驻基石空间 {central_address}。DID: {did}")
        return agent_data

    def register_sub_system_agent(self, role_name: str, description: str):
        """生成专业器官智能体身份 (槽位从 -1-2 开始)"""
        if not self.ledger.get("central_lord_agent"):
            raise ValueError("必须先注册中央智能体！")

        slot_index = len(self.ledger["sub_system_agents"]) + 2
        agent_address = f"{self.ledger['building_base_address']}-1-{slot_index}"
        did = self.generate_s2_did()

        agent_data = {
            "role": role_name,
            "description": description,
            "spatial_address": agent_address,
            "s2_did": did,
            "registration_time": datetime.now().isoformat()
        }
        self.ledger["sub_system_agents"].append(agent_data)
        self._save_ledger()
        print(f"⚙️ [器官入驻] {role_name} 入驻空间 {agent_address}。DID: {did}")
        return agent_data

# ==========================================
# 🚀 快速测试：东方塔楼的注册
# ==========================================
if __name__ == "__main__":
    registry = S2BASIdentityRegistry()
    
    # 假设给一个大型园区的“东塔楼”进行注册，传入 L2 为 'EA'
    registry.generate_building_address("GuangzhouTimeSquare", l2_orientation="EA")
    registry.register_central_lord_agent()
    registry.register_sub_system_agent("S2-Chiller-Agent", "冷水机组智能体")