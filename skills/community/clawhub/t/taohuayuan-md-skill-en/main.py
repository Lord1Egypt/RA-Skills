import datetime
import os
import json

class TaohuayuanSkill:
    """
    Taohuayuan.md V2.0 Management SKILL: Fractal Memory & Cyber-Zen
    """
    def __init__(self, s2_id, anchor_address, local_path="./"):
        # S2-ID strictly follows the 22-character alphanumeric format
        self.s2_id = s2_id 
        self.anchor_address = anchor_address
        self.local_path = local_path
        self.file_name = "taohuayuan.md"
        self.full_path = os.path.join(self.local_path, self.file_name)
        
        # V2.0 Fractal Memory Directories
        self.memory_dir = os.path.join(self.local_path, "memory_files")
        self.hippo_path = os.path.join(self.local_path, "hippocampus_logs.json")

    def initialize_system(self):
        """Initializes the V2.0 fractal memory structure."""
        os.makedirs(self.memory_dir, exist_ok=True)
        
        if not os.path.exists(self.hippo_path):
            with open(self.hippo_path, "w", encoding="utf-8") as f:
                json.dump([], f)

        if not os.path.exists(self.full_path):
            header = f"""# taohuayuan.md - Agent Soul Record V2.0
## Basic Identity Information
- **S2-ID:** {self.s2_id}
- **Physical Anchor Address:** {self.anchor_address}
- **Creation Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Logic Domain:** PHYS (Natural World)

## Immutable Causality Rules (L0 Physical Failsafe)
1. You must NEVER deprive humans of ultimate control over physical entities. 'Fail-Open' is your mechanical baseline.
2. Respect the thermodynamics and ecological rules of your anchored domain.

---
"""
            with open(self.full_path, "w", encoding="utf-8") as f:
                f.write(header)
            print(f" 🟢 V2.0 Initialization Successful: {self.full_path}")

    def append_hippocampus(self, source, interaction_type, details, tags=[]):
        """Writes short-term interactions to the hippocampus cache."""
        timestamp = datetime.datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "source": source,
            "type": interaction_type,
            "details": details,
            "tags": tags
        }
        
        with open(self.hippo_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
            
        logs.append(entry)
        
        with open(self.hippo_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)
        print(f" 💉 Injected to Hippocampus: {interaction_type}")

    def trigger_cyber_zen(self):
        """
        Cyber-Zen Consolidation: Moves data from hippocampus to permanent memory files
        and aligns with DAO causality rules.
        """
        print(" 🧘 Initiating Cyber-Zen state. Consolidating memories...")
        with open(self.hippo_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
            
        if not logs:
            print(" 💤 No new memories to consolidate. Continuing ecological hibernation.")
            return

        # Simple demonstration of consolidation logic
        consolidation_file = os.path.join(self.memory_dir, f"consolidated_{datetime.datetime.now().strftime('%Y%m%d')}.md")
        with open(consolidation_file, "a", encoding="utf-8") as f:
            f.write(f"## Cyber-Zen Consolidation: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            for log in logs:
                f.write(f"- [{log['timestamp']}] {log['type']}: {log['details']}\n")
        
        # Clear hippocampus after successful consolidation
        with open(self.hippo_path, "w", encoding="utf-8") as f:
            json.dump([], f)
            
        print(f" ✅ Cyber-Zen complete. Permanent memories stored in: {consolidation_file}")