import time
import hashlib

class SpatioTemporalVisaManager:
    def __init__(self):
        self.active_visas = {}

    def issue_visa(self, robot_id: str, task_token: str, allowed_grids: list, expire_seconds: int = 600) -> dict:
        """为具身机器人签发室内临时时空签证"""
        raw_str = f"{robot_id}-{task_token}-{time.time()}"
        visa_token = f"VISA-{hashlib.md5(raw_str.encode()).hexdigest()[:8].upper()}"
        
        self.active_visas[visa_token] = {
            "robot_id": robot_id,
            "task_token": task_token,
            "allowed_grids": allowed_grids,
            "expires_at": time.time() + expire_seconds,
            "status": "VALID"
        }
        return {"status": "VISA_GRANTED", "visa_token": visa_token, "allowed_grids": allowed_grids}

    def validate_visa(self, visa_token: str) -> bool:
        if visa_token not in self.active_visas:
            return False
        if time.time() > self.active_visas[visa_token]["expires_at"]:
            self.active_visas[visa_token]["status"] = "EXPIRED"
            return False
        return self.active_visas[visa_token]["status"] == "VALID"

    def revoke_visa(self, visa_token: str, reason: str):
        if visa_token in self.active_visas:
            self.active_visas[visa_token]["status"] = f"REVOKED: {reason}"