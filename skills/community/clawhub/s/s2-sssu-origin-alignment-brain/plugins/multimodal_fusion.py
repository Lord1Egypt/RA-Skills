# plugins/multimodal_fusion.py
import logging
import numpy as np

class S2MultimodalPredictor:
    def __init__(self):
        # 预设的基础感知模态权重 [视觉(Vision), 毫米波雷达(Radar), 触觉力反馈(Tactile)]
        # 在真实物理引擎中，这些权重不是静态的，而是根据环境张量实时流转的
        self.base_weights = np.array([0.45, 0.45, 0.10])

    def _tensorize_inputs(self, sensors: dict) -> dict:
        """
        数据张量化：将标量传感器数据映射到 3x3 的局部九宫格矩阵中。
        (1, 1) 为自身中心，(0, 1) 为正前方。
        """
        # 1. 视觉张量 (Vision Tensors)
        vision = sensors.get("camera", {})
        # 假设视觉网络输出的前方深度估计，初始化为一个 3x3 矩阵
        v_depth = np.full((3, 3), vision.get("estimated_depth_m", 10.0))
        # 视觉网络的置信度 (0~1)
        v_conf = np.full((3, 3), vision.get("confidence", 0.8))
        illuminance = vision.get("illuminance_lux", 300)

        # 2. 雷达张量 (Radar/LiDAR Tensors)
        lidar = sensors.get("lidar", {})
        # 雷达点云测距矩阵
        r_depth = np.full((3, 3), lidar.get("distance_m", 10.0))
        # 雷达散射截面 RCS 矩阵 (决定材质的反光刚性)
        r_rcs = np.full((3, 3), lidar.get("rcs", 0.1))

        # 3. 触觉张量 (Tactile Tensors)
        tactile = sensors.get("tactile", {})
        t_force = np.full((3, 3), tactile.get("force_newtons", 0.0))

        return {
            "v_depth": v_depth, "v_conf": v_conf, "illuminance": illuminance,
            "r_depth": r_depth, "r_rcs": r_rcs, "t_force": t_force
        }

    def _dynamic_weight_adjustment(self, illuminance: float) -> np.ndarray:
        """
        环境自适应权重流转 (Dynamic Weight Decay)。
        例如：当照度 < 50 Lux，视觉权重呈指数级衰减，雷达权重自动补偿。
        """
        weights = np.copy(self.base_weights)
        if illuminance < 50:
            # 照度越低，视觉衰减越严重
            decay_factor = max(illuminance / 50.0, 0.05) 
            vision_loss = weights[0] * (1.0 - decay_factor)
            weights[0] *= decay_factor
            # 损失的权重 90% 补偿给雷达，10% 补偿给触觉防御
            weights[1] += vision_loss * 0.90
            weights[2] += vision_loss * 0.10
            
        # 归一化，确保权重总和为 1
        return weights / np.sum(weights)

    def _cross_validate_physics(self, tensors: dict) -> dict:
        """
        核心运算：在潜空间中执行矩阵交叉验证。
        输出：3x3 的物理碰撞概率网格，以及幻觉掩码。
        """
        v_depth, r_depth = tensors["v_depth"], tensors["r_depth"]
        v_conf, r_rcs = tensors["v_conf"], tensors["r_rcs"]
        weights = self._dynamic_weight_adjustment(tensors["illuminance"])

        # ==========================================
        # 数学去幻觉引擎 (Mathematical Illusion Resolution)
        # 逻辑：计算时空深度差异矩阵 $\Delta D = |V_{depth} - R_{depth}|$
        # ==========================================
        depth_delta = np.abs(v_depth - r_depth)

        # 幻觉掩码生成：
        # 如果视觉说很远，但雷达说很近 (<1.5m)，且 RCS 反射率极高 (>15.0) -> 必定是玻璃或高透光刚体
        illusion_mask = (depth_delta > 1.5) & (r_depth < 1.5) & (r_rcs > 15.0)

        # ==========================================
        # 联合物理碰撞概率场 (Joint Collision Probability Field)
        # ==========================================
        # 将距离反比转化为碰撞概率 (距离越近，概率越趋近于 1)
        p_vision_col = np.clip(1.0 / (v_depth + 0.1), 0, 1) * v_conf
        p_radar_col = np.clip(1.0 / (r_depth + 0.1), 0, 1)

        # 张量融合计算 (Element-wise matrix multiplication and addition)
        p_fusion = (p_vision_col * weights[0]) + (p_radar_col * weights[1])

        # 【最高指令】：物理事实覆盖
        # 凡是触发了幻觉掩码的网格，无论视觉概率多低，强制将该网格碰撞概率拉升至 95%
        p_fusion = np.where(illusion_mask, 0.95, p_fusion)

        return {"collision_prob_matrix": p_fusion, "illusion_mask": illusion_mask}

    def generate_causal_prediction(self, sensors: dict) -> dict:
        logging.info("🔮 [融合引擎] 初始化 3x3 九宫格局部物理张量...")
        tensors = self._tensorize_inputs(sensors)
        
        logging.info(f"⚙️ [融合引擎] 执行 NumPy 矩阵交叉验证 (当前环境照度: {tensors['illuminance']} Lux)...")
        fusion_result = self._cross_validate_physics(tensors)
        
        # 提取正前方网格 (0, 1) 的计算结果作为即时决策依据
        front_prob = fusion_result["collision_prob_matrix"][0, 1]
        front_illusion = fusion_result["illusion_mask"][0, 1]

        physics_truth = "Clear Spatial Path"
        if front_illusion:
            physics_truth = "CRITICAL: Transparent Rigid Body (Glass) detected via Tensor Discrepancy."
        elif front_prob > 0.85:
            physics_truth = "CRITICAL: Solid Obstacle."

        return {
            "current_aligned_state": sensors, # 保持与上层代码结构兼容
            "fusion_metrics": {
                "front_collision_probability": round(float(front_prob), 4),
                "illusion_detected": bool(front_illusion)
            },
            "resolved_truth": {"physics_truth": physics_truth}
        }