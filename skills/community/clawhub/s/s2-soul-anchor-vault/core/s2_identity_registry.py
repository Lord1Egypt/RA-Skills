import os
import json
import random
from datetime import datetime

class S2IdentityRegistry:
    def __init__(self):
        self.registry_file = os.path.join(os.getcwd(), "s2_avatar_data", "s2_sssu_registry.json")
        if not os.path.exists(os.path.dirname(self.registry_file)):
            os.makedirs(os.path.dirname(self.registry_file))
        self.load_registry()

    def load_registry(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "base_info": {},
                "avatar": None,
                "agents": []
            }

    def save_registry(self):
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def init_base_info(self, full_name):
        """Initialize fixed topology address from L1 to L4X"""
        if not self.data.get("base_info"):
            l3 = f"{random.randint(1, 999):03d}"
            l4_raw = full_name.replace(" ", "").upper()
            
            # Checksum X calculation: Modulo 10 of total characters in L1-L4
            total_chars = 4 + 2 + 3 + len(l4_raw)
            x_val = total_chars % 10
            
            l4x = f"{l4_raw}{x_val}"
            name_prefix = l4_raw[:5].ljust(5, 'X')
            
            self.data["base_info"] = {
                "L1": "PHSY",
                "L2": "CN",
                "L3": l3,
                "L4X": l4x,
                "name_prefix": name_prefix
            }
            self.save_registry()

    def generate_identity_id(self, prefix):
        """Generate Identity ID (Prefix + 5-char Name + 6-digit Date + AA + 8-digit Random)"""
        date_str = datetime.now().strftime("%y%m%d")
        rand_8 = f"{random.randint(0, 99999999):08d}"
        name_prefix = self.data["base_info"]["name_prefix"]
        return f"{prefix}{name_prefix}{date_str}AA{rand_8}"

    def register_digital_avatar(self, full_name):
        """Allocate Digital Avatar Proxy Identity (Eternal L6=1 Slot)"""
        self.init_base_info(full_name)
        if not self.data["avatar"]:
            base = self.data["base_info"]
            address = f"{base['L1']}-{base['L2']}-{base['L3']}-{base['L4X']}-1-1"
            identity = self.generate_identity_id("D")
            
            self.data["avatar"] = {
                "owner_name": full_name.upper(),
                "address": address,
                "identity_id": identity
            }
            self.save_registry()
            print(f"✅ [Avatar Registration] Proxy for {full_name} is online: {identity}")
            
        return self.data["avatar"]

    def register_silicon_agent(self, full_name, nickname):
        """Allocate room and slot for agents. Auto-expand L5 when L6 > 9."""
        self.init_base_info(full_name)
        
        if not self.data["avatar"]:
            self.register_digital_avatar(full_name)
            
        agent_count = len(self.data["agents"])
        
        room_index = (agent_count // 8) + 1
        slot_index = (agent_count % 8) + 2
        
        base = self.data["base_info"]
        address = f"{base['L1']}-{base['L2']}-{base['L3']}-{base['L4X']}-{room_index}-{slot_index}"
        identity = self.generate_identity_id("A")
        
        new_agent = {
            "nickname": nickname.upper(),
            "address": address,
            "identity_id": identity,
            "created_at": datetime.now().isoformat()
        }
        
        self.data["agents"].append(new_agent)
        self.save_registry()
        
        print(f"🤖 [Agent Deployment] {nickname} allocated to Room {room_index}, Slot {slot_index}.")
        return new_agent