# 🧱 S2-Spatial-Primitive: The 6-Element Data Model Definer
# 空间基元六要素数据模型定义仪
*v1.0.0 | Bilingual Edition (English / 中文)*

Welcome to the foundation of the **S2-Spatial-Primitive OS**. This SKILL does not control physical hardware directly; instead, it establishes the **Universal Data Model (全网统一数据模型)** for the next generation of AI-driven smart spaces.
欢迎来到 S2 空间基元操作系统的最底层。本技能不直接控制物理硬件，而是为下一代 AI 驱动的智慧空间建立**全网统一的数据模型库**。

---

### 📐 The Paradigm Shift: From Apps to Agents
Traditional smart homes require humans to press buttons on apps. The S2 ecosystem believes that **AI Agents are the indigenous operators of space**, while humans are merely the beneficiaries. 
传统的智能家居需要人类在 App 上按按钮。S2 生态认为，**AI 智能体才是空间的原住民与操作者**，人类只是享受者。

Therefore, this SKILL defines a `2m x 2m` physical grid and maps it into a high-dimensional JSON tensor matrix. This matrix is uniquely designed using **Natural Language Parameters (NLP fields)** instead of rigid tables, allowing Large Language Models (LLMs) to instantly read, comprehend, and orchestrate the space.
因此，本技能定义了一个 `2m x 2m` 的物理格子，并将其映射为高维 JSON 张量矩阵。该矩阵独特地采用了**自然语言参数**而非死板的表格，使得大语言模型能够瞬间阅读、理解并调度该空间。

---

### 🧬 The 6-Element Matrix / 核心六要素定义

#### 1. Light (光)
Metrics of lighting effect, not physical bulbs. Includes Illuminance, Color Temperature, RGBW, and **Natural Language Special Effects** (e.g., "Stage rock strobe", "Cinematic dimming"). / 以光效而非灯泡外观为衡量标准。包含光照度、色温、RGBW及自然语言描述的特殊光效（如舞台摇滚频闪、影院场景）。

#### 2. Air & HVAC (空气：温湿度与风力)
Focuses on comfort and health. Includes standard HVAC metrics (Temp, Humidity, Wind Level) and integrates the **GB 3095-2012 Air Quality Standard** (PM2.5, PM10, SO2, NO2, CO, O3, CO2). Also includes Hazard Alarms (Gas leaks). / 提供舒适度与健康度。包含温湿度、风力，并集成国家空气质量标准六项污染物及有害气体报警。

#### 3. Sound (声音)
Physical and psychological audio rendering. Includes Volume/EQ params, **Noise Management** (Active suppression & White noise playback), BGM scheduling, and Mic monitoring toggles. / 生理与心理的音频渲染。包含基础音量EQ、噪声抑制与白噪声播放、音乐源时间表及监听开关。

#### 4. Electromagnetic (电磁波)
Wireless coverage and human sensing. Includes Wi-Fi/5G/Zigbee networking, and spatial perception via **mmWave Radar, Infrared, and Wi-Fi sensing**. / 无线覆盖与人体感应。包含无线上网/局域网组网，以及毫米波、红外、Wi-Fi人体感应。

#### 5. Energy (能源供应与消耗)
Quantitative description of spatial energy. Covers supply layout (sockets/switches), live consumption wattage, and self-generation metrics (Solar PV, Geothermal). / 空间能源的定量描述。涵盖室内配电分布、实时功耗及太阳能/地源热泵等自给生产数据。

#### 6. Visual (视觉影像)
**⚠️ STRICT PRIVACY BOUNDARY**: Visual refers exclusively to **OUTPUT/DISPLAY** (Screens, Projectors, AR Glasses, BCI) and Video Stream Sources. **IT DOES NOT INCLUDE CAMERA RECORDING.** Spatial awareness is handled entirely by the Electromagnetic element. / **⚠️ 严苛的隐私边界**：视觉仅指代**输出与显示**（屏幕、投影、智能眼镜、脑机接口）及视频播放源。**绝不包含摄像头录像采集。**空间感知完全交由电磁波要素负责。

---

### 🚀 Usage / 使用方法
Run the script to generate the `primitive_6_elements_template.json` in your local directory. Supply this JSON schema to your OpenClaw agents as the baseline context for spatial awareness and control.
运行本脚本，将在本地生成六要素 JSON 模板。将此结构体作为上下文提供给您的智能体，使其获得空间感知与控制的基准模型。