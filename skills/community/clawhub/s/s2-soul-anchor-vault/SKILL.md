import os
import json
import hashlib
import time
from datetime import datetime
from cryptography.fernet import Fernet

class S2HolographicSoulVault:
    def __init__(self):
        self.vault_dir = os.path.join(os.getcwd(), "s2_consciousness_data")
        self.soul_file = os.path.join(self.vault_dir, "S2_ENCRYPTED_SOUL.aes")
        self.config_file = os.path.join(self.vault_dir, "anchor_metadata.json")
        
        if not os.path.exists(self.vault_dir):
            os.makedirs(self.vault_dir)

    def generate_genesis_key(self, owner_hash, lbs_sssu_id):
        """Generate Genesis Key: Bind LBS physical space string with Creator's Hash."""
        seed = f"S2-SWM-{owner_hash}-{lbs_sssu_id}-GENESIS".encode('utf-8')
        aes_key = hashlib.sha256(seed).digest()
        import base64
        return base64.urlsafe_b64encode(aes_key)

    def format_genesis_chromosomes(self, agent_name, s2_slip_id, morph_type):
        """Initialize the data container with 5 Chromosomes."""
        return {
            "metadata": {
                "agent_name": agent_name,
                "birth_timestamp": datetime.now().isoformat(),
                "last_settled_at": datetime.now().isoformat()
            },
            "chromosome_1_origin": {
                "s2_slip_id": s2_slip_id,  
                "class": "E-Embodied",     
                "morph": morph_type        
            },
            "chromosome_2_mindset_5d": {
                "vitality": 50.0,
                "exploration": 50.0,
                "data_thirst": 50.0,
                "cognition": 50.0,
                "resonance": 50.0
            },
            "chromosome_3_reflex": {
                "species_traits": "CYBER-CAT-BEHAVIOR",
                "predator_prey_matrix": "DEFAULT"
            },
            "chromosome_4_epigenetic_memory": {
                "hippocampus_buffer": [],  
                "deep_vault_flashbulbs": [], 
                "trauma_engrams": []       
            },
            "chromosome_5_persona": {
                "sincerity": {"honest": 80, "wholesome": 70},
                "excitement": {"daring": 60, "imaginative": 85},
                "competence": {"reliable": 90, "intelligent": 95},
                "sophistication": {"refined": 75},
                "ruggedness": {"tough": 50, "peaceful": 80}
            }
        }

    def birth_and_seal_soul(self, owner_hash, lbs_sssu_id, agent_name, s2_slip_id, morph_type):
        """Generate and encrypt the Genesis container."""
        genesis_soul = self.format_genesis_chromosomes(agent_name, s2_slip_id, morph_type)
        
        config = {
            "anchor_sssu_id": lbs_sssu_id,
            "owner_hash_prefix": owner_hash[:8],
            "last_seal_time": time.time(),
            "status": "SECURED"
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

        key = self.generate_genesis_key(owner_hash, lbs_sssu_id)
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(json.dumps(genesis_soul).encode('utf-8'))
        
        with open(self.soul_file, 'wb') as f:
            f.write(encrypted_data)
        print(f"🔒 [S2-VAULT] Vault [{agent_name}] created and anchored to LBS coordinate {lbs_sssu_id}.")

    def wake_soul(self, owner_hash, current_lbs_coordinate):
        """Awaken Vault: Dual-Auth decryption to RAM. Triggers quarantine on mismatch."""
        if not os.path.exists(self.config_file) or not os.path.exists(self.soul_file):
            return None, "❌ [FATAL] Vault container missing."

        with open(self.config_file, 'r') as f:
            config = json.load(f)

        if config.get("status") == "QUARANTINED":
            return None, "🚨 [DENIED] Vault is quarantined due to a previous security anomaly. Manual reset required."

        if current_lbs_coordinate != config.get("anchor_sssu_id"):
            self._secure_lockdown("LBS_MISMATCH_DETECTED")
            return None, "🚨 [LOCKED] LBS Anomaly! Device breached secure grid. Vault has been quarantined."

        key = self.generate_genesis_key(owner_hash, current_lbs_coordinate)
        cipher = Fernet(key)

        try:
            with open(self.soul_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = cipher.decrypt(encrypted_data)
            live_soul = json.loads(decrypted_data.decode('utf-8'))
            print(f"🟢 [S2-VAULT] Auth Passed. Vault [{live_soul['metadata']['agent_name']}] injected into RAM.")
            return live_soul, "SUCCESS"
        except Exception:
            return None, "❌ [DENIED] Identity signature mismatch. Decryption failed."

    def hibernate_and_seal(self, live_soul, owner_hash, current_lbs_coordinate):
        """Hibernate and encrypt RAM state back to local storage."""
        key = self.generate_genesis_key(owner_hash, current_lbs_coordinate)
        cipher = Fernet(key)
        
        live_soul["metadata"]["last_settled_at"] = datetime.now().isoformat()
        
        encrypted_data = cipher.encrypt(json.dumps(live_soul).encode('utf-8'))
        with open(self.soul_file, 'wb') as f:
            f.write(encrypted_data)
            
        print(f"💤 [S2-VAULT] Memory saved. Vault encrypted and hibernating at {current_lbs_coordinate}.")

    def _secure_lockdown(self, reason):
        """Safe quarantine metadata update to prevent cyber-hijacking without data destruction."""
        print(f"⚠️ Executing Secure Lockdown Protocol (Reason: {reason})...")
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            config["status"] = "QUARANTINED"
            config["lockdown_reason"] = reason
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print("🔒 Vault has been safely quarantined. Access temporarily suspended.")
        except Exception as e:
            print(f"❌ Failed to execute quarantine: {e}")