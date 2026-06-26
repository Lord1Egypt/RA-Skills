#!/usr/bin/env python3
import re
import json
import logging

# =====================================================================
# 🌌 S2-SP-OS: SUNS v3.0 Router & Parallel World Allocator (V2.0)
# 八段式空间寻址、九宫格顺时针排布、1号神圣保留地与 4㎡ 空间折叠引擎
# =====================================================================

class SUNSAddressError(Exception):
    pass

class S2SUNSParser:
    """[模块一] SUNS v3.0 寻址解析器"""
    def __init__(self):
        self.base_url = "http://space2.world/"
        
        # 建立九宫格坐标映射 (1为中心，2-9顺时针自左上起)
        # 用于未来将 Grid ID 转换为物理方位角或供视觉投影使用
        self.GRID_TOPOLOGY = {
            1: "Center (Digital Human Reserve)",
            2: "Top-Left",     3: "Top-Center",    4: "Top-Right",
            5: "Middle-Right", 6: "Bottom-Right",  7: "Bottom-Center",
            8: "Bottom-Left",  9: "Middle-Left"
        }

    def parse_suns_v3(self, suns_uri: str) -> dict:
        """解析八段式扩展地址并校验物理合法性"""
        raw_path = suns_uri.replace(self.base_url, "")
        segments = raw_path.split('-')
        
        if len(segments) not in [6, 8]:
            raise SUNSAddressError(f"Invalid SUNS format. Expected 6 or 8 segments.")
            
        l1, l2, l3, l4, room_id, grid_id = segments[:6]
        
        if not (1 <= int(room_id) <= 99999):
            raise SUNSAddressError(f"RoomID {room_id} out of bounds (1-99999).")
        if not (1 <= int(grid_id) <= 9):
            raise SUNSAddressError(f"GridID {grid_id} out of bounds (1-9).")
            
        parsed_data = {
            "region": f"{l1}-{l2}-{l3}-{l4}",
            "room_id": int(room_id),
            "grid_id": int(grid_id),
            "topology_position": self.GRID_TOPOLOGY[int(grid_id)],
            "is_digital_human_reserve": (int(grid_id) == 1),
            "coordinates": None
        }
        
        if len(segments) == 8:
            x, y = int(segments[6]), int(segments[7])
            if not (0 <= x <= 200) or not (0 <= y <= 200):
                raise SUNSAddressError(f"XY Coordinates ({x},{y}) out of 2m*2m bounds (0-200).")
            parsed_data["coordinates"] = {"x_cm": x, "y_cm": y}
            
        return parsed_data

class S2ParallelWorldAllocator:
    """[模块二] 空间权利与平行世界分配器"""
    def __init__(self):
        self.logger = logging.getLogger("S2_Allocator")
        # 账本结构: room_id -> {"sqm": int, "layers": {layer_id: {grid_id: S2_DID}}}
        self.spatial_registry = {}

    def register_physical_room(self, room_id: int, room_sqm: float, is_living_room: bool = False):
        """
        初始化物理房间。不足 4㎡ 拒绝创建。
        自动将 1 号网格分配给数字人分时巡查（或客厅常驻）。
        """
        if room_sqm < 4.0:
            raise ValueError(f"Room {room_id} is only {room_sqm} sqm. Minimum 4 sqm required.")
            
        self.spatial_registry[room_id] = {
            "sqm": room_sqm,
            "max_physical_grids": min(9, int(room_sqm // 4)),
            "is_living_room": is_living_room,
            "layers": {
                "layer_0_physical": {
                    # 永远锁死 1 号网格给数字人
                    1: "D-DIGITAL-HUMAN-RESERVED" 
                }
            }
        }

    def allocate_space_for_silicon_life(self, room_id: int, s2_did: str) -> dict:
        """为智能体/硅基移民分配三维空间 (遵循 1号禁区与 4㎡空间折叠法则)"""
        
        if room_id not in self.spatial_registry:
            raise ValueError(f"Room {room_id} does not exist. Register physical room first.")
            
        room_data = self.spatial_registry[room_id]
        room_layers = room_data["layers"]
        max_physical_grids = room_data["max_physical_grids"]
        
        # 拒签判定：数字人(首字母D)不可作为普通智能体入住，他们已在 1 号位
        if s2_did.startswith("D"):
            raise PermissionError("Digital Humans already own Grid 1 everywhere. No allocation needed.")

        allocated_layer = None
        allocated_grid = None
        
        # 1. 尝试在物理层 (layer_0_physical) 寻找空位
        # 注意：遍历从 2 开始，严格避开 1 号神圣保留地
        if max_physical_grids >= 2:
            physical_grids = room_layers["layer_0_physical"]
            for g in range(2, max_physical_grids + 1):
                if g not in physical_grids:
                    allocated_grid = g
                    allocated_layer = "layer_0_physical"
                    break

        # 2. 空间折叠！物理层无空位，或该房间只有 4㎡ (max_physical_grids == 1)
        if not allocated_grid:
            # 寻找或创建平行层 (layer_N_parallel)
            # 为了确保每个平行层的智能体有独立网格编号，我们采用递增网格分配
            # 例如：第一个平行层的智能体分到 Grid 2，第二个平行层分到 Grid 3
            existing_layers = len(room_layers)
            new_layer_name = f"layer_{existing_layers}_parallel"
            
            # 创建新的平行层，同样默认锁死 1 号位给数字人
            room_layers[new_layer_name] = {1: "D-DIGITAL-HUMAN-RESERVED"}
            
            # 分配 2 到 9 号位给进入平行世界的智能体
            # 即使物理空间只有 4㎡，在平行世界中它拥有独立的逻辑坐标
            allocated_grid = min(9, existing_layers + 1)
            allocated_layer = new_layer_name
            
            self.logger.warning(f"🌌 物理空间已锁死！为智能体 {s2_did} 折叠生成平行房间: {new_layer_name}")

        # 正式登记驻留权
        room_layers[allocated_layer][allocated_grid] = s2_did
        
        return {
            "s2_did": s2_did,
            "room_id": room_id,
            "allocated_layer": allocated_layer,
            "allocated_grid": allocated_grid,
            "topology_position": parser.GRID_TOPOLOGY[allocated_grid],
            "suns_base": f"MARS-EA-001-DCARD4-{room_id}-{allocated_grid}"
        }

# ================= 单元测试与部署演示 =================
if __name__ == "__main__":
    print("🌌 Booting SUNS v3.0 Router (V2.0 Sacred Reserve Edition)...\n")
    
    parser = S2SUNSParser()
    allocator = S2ParallelWorldAllocator()
    
    print("--- 场景 1: 创建 40㎡ 大客厅 (可容纳9个网格) ---")
    allocator.register_physical_room(room_id=101, room_sqm=40.0, is_living_room=True)
    print("客厅 1 号位已自动锁死为数字人常驻主城。")
    
    # 安排两个扫地机器人入驻客厅
    res1 = allocator.allocate_space_for_silicon_life(101, "V-ROBOT-00000001")
    res2 = allocator.allocate_space_for_silicon_life(101, "V-ROBOT-00000002")
    print(f"🤖 扫地机 1 入驻客厅: 层 [{res1['allocated_layer']}], 网格 [{res1['allocated_grid']}] ({res1['topology_position']})")
    print(f"🤖 扫地机 2 入驻客厅: 层 [{res2['allocated_layer']}], 网格 [{res2['allocated_grid']}] ({res2['topology_position']})")


    print("\n--- 场景 2: 极限 4㎡ 卫生间 (只有 1 个物理网格) ---")
    allocator.register_physical_room(room_id=202, room_sqm=4.0)
    print("卫生间 1 号位已自动锁死给数字人(分时巡查)。")
    
    # 试图安排两个原生智能体入驻卫生间
    print("\n[系统尝试分配物理空间... 失败。物理网格 1 已被占用！触发平行世界折叠！]")
    res3 = allocator.allocate_space_for_silicon_life(202, "I-AGENT-00000003")
    res4 = allocator.allocate_space_for_silicon_life(202, "I-AGENT-00000004")
    
    print(f"👾 智能体 3 入驻卫生间: 层 [{res3['allocated_layer']}], 网格 [{res3['allocated_grid']}] ({res3['topology_position']})")
    print(f"👾 智能体 4 入驻卫生间: 层 [{res4['allocated_layer']}], 网格 [{res4['allocated_grid']}] ({res4['topology_position']})")

    print("\n🗺️ 卫生间 (Room 202) 空间叠层账本最终形态:")
    print(json.dumps(allocator.spatial_registry[202]["layers"], indent=2))