import time
import hashlib
import json

class SpatialLedger:
    def __init__(self):
        self.chain = []

    def log_event(self, sssu_id: str, actor_id: str, event_type: str, payload: dict) -> str:
        """将物理世界的动态对象变化写入不可篡改账本"""
        record = {
            "timestamp": time.time(),
            "sssu_id": sssu_id,
            "actor": actor_id,
            "event_type": event_type,
            "payload": payload
        }
        # 简易区块哈希模拟
        record_string = json.dumps(record, sort_keys=True).encode()
        tx_hash = hashlib.sha256(record_string).hexdigest()
        
        entry = {"tx_hash": tx_hash, "record": record}
        self.chain.append(entry)
        return tx_hash

    def dump_ledger(self):
        return json.dumps(self.chain, indent=2, ensure_ascii=False)