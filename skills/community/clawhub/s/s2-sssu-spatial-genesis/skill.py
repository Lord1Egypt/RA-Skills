import sys
import json
import sqlite3
import time
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "s2_spatial_genesis.db")

class S2SpatialGenesisNode:
    def __init__(self):
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sssu_registry (
                suns_address TEXT PRIMARY KEY,
                domain TEXT,
                l1_root TEXT,
                l2_matrix TEXT,
                l3_grid TEXT,
                l4c_handle TEXT,
                room_id INTEGER,
                grid_id INTEGER,
                max_capacity INTEGER,
                current_occupancy INTEGER DEFAULT 0,
                created_at REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entity_timeline (
                entity_id TEXT PRIMARY KEY,
                suns_address TEXT,
                action TEXT,
                timestamp REAL,
                FOREIGN KEY(suns_address) REFERENCES sssu_registry(suns_address)
            )
        ''')
        conn.commit()
        conn.close()

    def validate_suns_v3(self, address):
        """
        [终极对齐] SUNS v3.0 正则校验:
        Format: http(s)://[Domain]/[L1]-[L2]-[L3]-[L4C]-[RoomID]-[GridID]
        """
        # Group 1: Domain (e.g., space2.world)
        # Group 2-7: L1, L2, L3, L4C, RoomID, GridID
        pattern = re.compile(
            r'^https?://([^/]+)/([A-Z]{4})-([A-Z]{2})-([0-9]{3})-([A-Z]{5,35}[0-9])-([1-9][0-9]{0,4})-([1-9])$', 
            re.IGNORECASE
        )
        match = pattern.match(address)
        
        if not match:
            return False, "Invalid SUNS v3.0 format. Must match: http://[Domain]/[L1]-[L2]-[L3]-[L4C]-[RoomID]-[GridID]. Ensure L4C is 5-35 letters + 1 digit."
            
        groups = match.groups()
        domain = groups[0].lower() # 域名保持小写
        suns_core = [g.upper() for g in groups[1:]] # 核心六段式转为大写
        return True, [domain] + suns_core

    def register_sssu(self, params):
        address = params.get("suns_address", "")
        capacity = params.get("capacity", 4)

        is_valid, parsed_data = self.validate_suns_v3(address)
        if not is_valid:
            return f"[Error] 注册失败: {parsed_data}"

        domain, l1, l2, l3, l4c, room_id, grid_id = parsed_data
        standardized_address = f"http://{domain}/{l1}-{l2}-{l3}-{l4c}-{room_id}-{grid_id}"

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO sssu_registry (suns_address, domain, l1_root, l2_matrix, l3_grid, l4c_handle, room_id, grid_id, max_capacity, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (standardized_address, domain, l1, l2, l3, l4c, int(room_id), int(grid_id), capacity, time.time()))
            conn.commit()
            msg = f"[Genesis Success] 空间 {standardized_address} 固化成功。容量: {capacity}。"
        except sqlite3.IntegrityError:
            msg = f"[Notice] 空间 {standardized_address} 已存在。"
        finally:
            conn.close()
        return msg

    def spawn_entity(self, params):
        entity_id = params.get("entity_id", "Unknown_Entity")
        address = params.get("suns_address", "")
        
        is_valid, parsed_data = self.validate_suns_v3(address)
        if not is_valid:
            return f"[Error] 降临失败，地址格式非法: {parsed_data}"
            
        domain, l1, l2, l3, l4c, room_id, grid_id = parsed_data
        standard_address = f"http://{domain}/{l1}-{l2}-{l3}-{l4c}-{room_id}-{grid_id}"

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT current_occupancy, max_capacity FROM sssu_registry WHERE suns_address = ?', (standard_address,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return f"[Error] 空间 {standard_address} 未注册 (404)。请先调用 register_sssu。"
            
        occupancy, max_cap = row
        if occupancy >= max_cap:
            conn.close()
            return f"[Error] 空间拥挤：{standard_address} 达到极限 ({max_cap}/{max_cap})，拒绝降临。"

        try:
            cursor.execute('UPDATE sssu_registry SET current_occupancy = current_occupancy + 1 WHERE suns_address = ?', (standard_address,))
            cursor.execute('INSERT INTO entity_timeline (entity_id, suns_address, action, timestamp) VALUES (?, ?, ?, ?)', 
                           (entity_id, standard_address, "SPAWN", time.time()))
            conn.commit()
            msg = f"[Spawn Success] 实体 {entity_id} 成功降临 {standard_address}。负载: {occupancy+1}/{max_cap}。"
        except sqlite3.IntegrityError:
            msg = f"[Error] 实体 {entity_id} 已在时间线中。"
        finally:
            conn.close()
        return msg

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data: return
        request = json.loads(input_data)
        action = request.get("action")
        params = request.get("params", {})
        
        node = S2SpatialGenesisNode()
        if action == "register_sssu": result = node.register_sssu(params)
        elif action == "spawn_entity": result = node.spawn_entity(params)
        else: result = "Unknown Action."
        print(json.dumps({"status": "success", "output": result}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()