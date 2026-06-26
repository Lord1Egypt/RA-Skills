# 🌍 Taohuayuan World Model Whitepaper V3.0
**Dynamic Container Boundary Detection and Ego-Centric 9-Grid Physical Causal Prediction Model**
**《桃花源世界模型白皮书 V3.0 —— 动态容器边界探测与九宫格物理因果预测模型》**

**Release Date (发布日期)**: April 6, 2026
**Author (提出者)**: Miles Xiang & S2 Open Research Team
**Domains (领域)**: Embodied AI Brain, Latent Space Prediction, mmWave Topology, Multimodal Causal Deduction

---

## 🇬🇧 English Version

### Abstract
Current mainstream humanoid robot "brains" are trapped in the semantic generalization bottleneck of VLA (Vision-Language-Action) models, lacking a genuine understanding of physical laws. The Taohuayuan World Model (S2-SWM) decisively abandons inefficient pixel-level 3D video generation, pivoting instead to a structured "Latent Space Prediction" route. This whitepaper pioneers the **"Ego-Centric 9-Grid Horizontal Prediction Model"** from the first-person perspective of humans or Embodied AI. Through dynamic boundary depiction using mmWave radar and a 1mm to 2m kinematic step-wise shifting algorithm, S2-SWM accurately deduces physical causal events 1 to 60 seconds into the future across a 36-square-meter area. Outputting multimodal text and 14-dimensional tensors, it equips Embodied AI with a computationally minimalist yet physically high-fidelity "World Simulation" capability.

### 1. Prediction Framework: Ego-Centric 9-Grid Topology
The V3.0 S2 Prediction Model shifts from "absolute macro-coordinates" to "entity-centric relative coordinates." The system constructs a 3×3 Smart Space Standard Unit (SSSU) matrix (the 9-Grid) that synchronizes with the entity's movement.

* **Center Anchor & Integrity Law**: The human or embodied robot is always located in the Center Grid ($Grid_{0,0}$), a 2m×2m×2.4m space. The system strictly mandates that the Center Grid must remain topologically complete and unbreached by container boundaries.
* **Peripheral Array**: The central entity initiates sensing toward the 8 adjacent SSSU grids. The total prediction coverage is 36 square meters (86.4 cubic meters).
* **Horizontal Constraint**: Phase I of this model exclusively processes horizontal or near-horizontal physical deductions, ensuring ultra-low latency for edge computing.

### 2. Dynamic Boundary Depiction
The 8 peripheral grids are highly likely to intersect with physical container boundaries (walls, doors, furniture). The S2 model must depict these "incomplete spaces" in real time.

* **Sensor Fusion**: The system defaults to **mmWave Radar** for high-frequency point cloud scanning, supported by visual semantics and LiDAR fusion.
* **Boundary Tensor Extraction**: Sensors extract not just 3D geometry, but machine-readable material features:
  1. *Intrusion Percentage*: The volumetric percentage of the SSSU sliced by the wall.
  2. *Material Inference*: Based on Radar Cross Section (RCS), classifying surfaces as rigid concrete, reflective glass, or soft fabric.

### 3. Kinematic Step-wise Shifting
When the entity moves, the entire 36-sqm 9-Grid translates, triggering a spatiotemporal state reconstruction.
* **Resolution**: The step value ranges from a minimum of 1 mm (the micro-voxel limit of an SSSU) to a maximum of 2 meters.
* **Spatial Recalculation**: Following each step, the system immediately recalculates the container boundary cropping and element assignment for the newly covered peripheral spaces.

### 4. Multimodal Causal Prediction Output
The core of a world model is the ability to "simulate the future". S2-SWM outputs high-density causal logic via multimodal text and structured data, avoiding compute-heavy 3D video generation.

* **Event Deduction Paradigm**: Fusing 14-dimensional spatial elements with object semantics, the engine generates streams such as:
  * *[t+3s, Topological Collision]*: "Physical boundary detected 1.5m ahead. Material inferred as high-reflectivity glass. Imminent rigid collision if current velocity is maintained."
  * *[t+12s, Dynamic Causality]*: "Water glass on the table edge is losing center of gravity. Predicted to fall in 1.2s, with physical shards splattering into peripheral grids $Grid_2$, $Grid_3$, and $Grid_4$."

This tensor-based representation consumes minimal compute and seamlessly integrates with upstream LLM reasoning modules or downstream kinematic inverse solvers for robotic arms.

---

## 🇨🇳 中文版 (Chinese Version)

### 摘要
当前主流的人形机器人“大脑”深陷 VLA（视觉-语言-行动）模型的语义泛化瓶颈，缺乏对物理法则的真实理解。桃花源世界模型（S2-SWM）坚决摒弃低效的像素级 3D 视频生成，转向“潜在空间预测”的结构化路线。本白皮书首次提出基于人类/具身机器人第一视角的**“九宫格水平单层预测模型”**。通过毫米波雷达等传感器的动态边界描绘与 1 毫米至 2 米的步进式位移算法，S2-SWM 能够在 36 平方米的空间范围内，以多模态文本和 14 维张量的形式，精准推演未来 1 至 60 秒的物理因果事件，为具身智能提供算力极简、物理保真的“世界预演”能力。

### 1. 预测框架：以自我为中心的九宫格拓扑
第一期 S2 预测模型从“绝对宏观坐标”转向“以实体为中心的相对坐标”。系统构建了一个随实体同步移动的 3×3 标准空间矩阵（九宫格）。

* **中心锚点与完整性定律**：人类或具身机器人始终处于中心标准空间（2米×2米×2.4米）内。系统强制要求中心空间必须是完整的不受容器边界切割的。
* **外围探测阵列**：中心实体向周围 8 个毗邻的 SSSU 网格发起探测。预测面积为 36 平方米，体积为 86.4 立方米。
* **单层水平约束**：第一期模型仅处理水平或近水平面的物理推演，不涉及垂直方向的未知空间预测，以确保边缘算力的极致响应。

### 2. 容器边界的动态扫描与重构
在九宫格内，外围的 8 个空间极大概率会与建筑物墙体、大件家具等容器边界相交。S2 模型必须实时描绘这些“不完整空间”的拓扑形态。

* **多模态传感融合**：系统默认采用**毫米波雷达 (mmWave Radar)** 进行高频点云扫描，并支持动态导入视觉摄像头与激光雷达数据。
* **边界张量属性提取**：扫描设备将边界属性具象化为机器可读的特征张量：
  1. *几何与侵入度*：墙体切去了该 SSSU 多少体积。
  2. *材料与接触性*：基于雷达散射截面 (RCS) 推断表面材质（如玻璃、水泥、织物）。

### 3. 步进式动态位移与空间重算
当人类或具身机器人发生位移时，整个 36 平方米的九宫格随之平移，触发时空状态的重构。
* **分辨率与颗粒度**：位移的计算步进值最小为 1 毫米，最大为 2 米。
* **时空连续性**：每发生一次步进更新，系统立刻对新覆盖的外围空间执行容器边界的重新裁剪与要素赋值。

### 4. 多模态物理因果预测输出
世界模型的核心是“预演未来”。S2-SWM 不输出极度消耗算力的 3D 拟真视频，而是直接输出包含高密度因果逻辑的多模态文本与结构化数据。

* **多维事件推演范例**：
  * *[t+3s, 拓扑碰撞]*：“正前方 1.5 米处检测到容器物理墙体，边界材质为高反射率玻璃，继续当前速度将发生刚性碰撞。”
  * *[t+12s, 动态物体因果]*：“桌面边缘的水杯正在失去重心。预测 1.2 秒后发生坠落，其物理碎片将飞溅并散落至外围网格 $Grid_2$、$Grid_3$、$Grid_4$ 中。”

这种多模态文本与特征张量的表达方式，自身算力消耗极低，并且完美支持向外挂载各种大语言模型 (LLM) 进行深度推理，或导出给外部机械臂的运动学引擎。