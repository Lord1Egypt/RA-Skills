# plugins/boundary_scanner.py
import logging
import numpy as np

class S2BoundaryScanner:
    def __init__(self):
        # 九宫格物理尺寸设定 (中心到边界的距离，单位：米)
        self.grid_size_m = 2.0 

    def _polar_to_cartesian(self, r: np.ndarray, theta_deg: np.ndarray) -> tuple:
        """数学降维：将雷达的极坐标 (距离, 角度) 转化为机器人自我中心的笛卡尔坐标 (X, Y)"""
        theta_rad = np.radians(theta_deg)
        x = r * np.cos(theta_rad) # 前方为正 X
        y = r * np.sin(theta_rad) # 左侧为正 Y
        return x, y

    def _simulate_raw_point_cloud(self) -> np.ndarray:
        """
        模拟底层硬件驱动传来的真实点云张量矩阵 (N x 3)
        格式: [距离(m), 角度(度), RCS反射率]
        """
        # 假设前方 0.8m 处有一堵高反光墙，右侧 1.5m 有障碍物
        return np.array([
            [0.8, 0.0, 25.5],   [0.85, 5.0, 24.0],  [0.82, -5.0, 26.1], # 正前方点云群
            [1.5, -90.0, 5.0],  [1.55, -85.0, 4.8],                     # 正右侧点云群
            [5.0, 90.0, 1.0],   [4.8, 180.0, 0.5]                       # 远端安全点云
        ])

    def execute_boundary_scan(self, center_hex_code: str, heading_vector: str, step_size_mm: int) -> dict:
        logging.info(f"📡 [感知层] 读取底层雷达高频点云，执行九宫格空间拓扑投影...")
        
        # 1. 获取底层点云张量
        pcd_tensor = self._simulate_raw_point_cloud()
        r, theta, rcs = pcd_tensor[:, 0], pcd_tensor[:, 1], pcd_tensor[:, 2]
        
        # 2. 坐标系转换
        x, y = self._polar_to_cartesian(r, theta)
        
        collision_warnings = []
        peripheral_grids_state = {}

        # 3. 空间切片与汇聚计算 (Spatial Binning & Pooling)
        # 以正前方 (Grid_Front) 为例：X > 0 且 |Y| < 1.0 米
        front_mask = (x > 0) & (x <= self.grid_size_m) & (np.abs(y) <= 1.0)
        
        if np.any(front_mask):
            # 提取正前方所有的点，找到最近的一个点作为物理边界入侵极限
            min_dist = np.min(r[front_mask])
            max_rcs = np.max(rcs[front_mask])
            
            intrusion_pct = np.clip(((self.grid_size_m - min_dist) / self.grid_size_m) * 100, 0, 100)
            
            if intrusion_pct > 50.0:
                collision_warnings.append(f"CRITICAL: Grid_Front 物理侵入度高达 {intrusion_pct:.1f}%！距离仅 {min_dist:.2f}m")
                
            peripheral_grids_state["Grid_Front"] = {
                "distance_to_boundary_m": round(float(min_dist), 2),
                "intrusion_percentage": round(float(intrusion_pct), 1),
                "max_rcs": round(float(max_rcs), 1)
            }
        else:
            peripheral_grids_state["Grid_Front"] = {"distance_to_boundary_m": 99.0, "intrusion_percentage": 0.0, "max_rcs": 0.0}

        return {"peripheral_grids_state": peripheral_grids_state, "collision_warnings": collision_warnings}