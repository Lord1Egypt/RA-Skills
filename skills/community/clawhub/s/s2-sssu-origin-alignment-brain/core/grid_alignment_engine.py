# core/grid_alignment_engine.py
import logging
import numpy as np
import math

class S2GridAlignmentEngine:
    def __init__(self):
        # 领主绝对坐标系定义 (Lord's Absolute SSSU Frame)
        # 根据白皮书，门洞底线右侧顶点为原点 (0, 0)，中心点为 (100, 0)
        self.lord_origin_cm = np.array([0.0, 0.0])
        self.lord_center_cm = np.array([100.0, 0.0])
        self.wgs84_anchor = {"lon": 116.397428, "lat": 39.90923, "alt_m": 45.0} # 示例 CGCS2000/WGS84 锚点

    def _calculate_transform_matrix(self, local_origin: np.ndarray, local_center: np.ndarray) -> dict:
        """
        核心二维对齐算法：计算客体 SLAM 坐标系到领主 SSSU 坐标系的平移与旋转矩阵
        """
        # 1. 计算平移向量 (Translation Vector)
        delta_x = self.lord_origin_cm[0] - local_origin[0]
        delta_y = self.lord_origin_cm[1] - local_origin[1]

        # 2. 计算旋转角差 (Rotation Angle Delta)
        # 本地坐标系中门洞的朝向向量
        local_vec = local_center - local_origin
        local_angle = math.atan2(local_vec[1], local_vec[0])
        
        # 领主坐标系中门洞的朝向向量
        lord_vec = self.lord_center_cm - self.lord_origin_cm
        lord_angle = math.atan2(lord_vec[1], lord_vec[0])
        
        delta_theta_rad = lord_angle - local_angle
        delta_theta_deg = math.degrees(delta_theta_rad)

        return {
            "translation_x_cm": round(delta_x, 2),
            "translation_y_cm": round(delta_y, 2),
            "rotation_deg": round(delta_theta_deg, 2)
        }

    def execute_alignment(self, robot_id: str, local_door_origin: dict, local_door_center: dict) -> dict:
        logging.info(f"🌐 [对齐引擎] 实体 [{robot_id}] 触发入户门洞绝对锚点校准协议...")
        
        local_orig_arr = np.array([local_door_origin.get("x", 0.0), local_door_origin.get("y", 0.0)])
        local_cent_arr = np.array([local_door_center.get("x", 100.0), local_door_center.get("y", 0.0)])

        # 执行降维强制对齐计算
        transform = self._calculate_transform_matrix(local_orig_arr, local_cent_arr)
        
        logging.info(f"🔄 [对齐引擎] 坐标系平移矩阵已生成：ΔX={transform['translation_x_cm']}cm, ΔY={transform['translation_y_cm']}cm, 旋转 Δθ={transform['rotation_deg']}°")
        
        return {
            "status": "ALIGNED_TO_LORD_FRAME",
            "anchor_wgs84": self.wgs84_anchor,
            "transform_matrix": transform,
            "instruction": "Grid snapping complete. Apply this transform matrix to all subsequent SLAM tensors."
        }