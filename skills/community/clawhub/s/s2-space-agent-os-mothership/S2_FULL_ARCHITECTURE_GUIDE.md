# 🌌 S2 Space Agent OS: The Spatial Basecamp
**(住宅空间智能体大本营 - 全景架构蓝图 V1.0 满血大一统版)**

[ 🇺🇸 English Version ](#english-version) | [ 🇨🇳 简体中文 ](#简体中文)

---

<a name="english-version"></a>
## 🇺🇸 English Version

> **"APP is dead. Agent is the new indigenous resident of the physical space."**
> S2 Space Agent OS is the ultimate physical basecamp designed for powerful Root Agents (like Openclaw). It injects a "Silicon Soul," strict ethical laws, cryptographic sovereignty, and spatiotemporal memory into your AI.

### 🗺️ 1. The Full Architecture Blueprint (Directory Tree)

For developers and geeks, here is the complete, uncompromising map of the S2 Universe. We have explicitly reserved "Expansion Docks" for the open-source community.

```text
s2-os-core/
├── 📄 README.md                        # The Geek Manifesto & Introduction
├── 📄 S2_FULL_ARCHITECTURE_GUIDE.md    # This Document (The Blueprint)
├── 📄 S2_DEPLOYMENT_&_NETWORK_TOPOLOGY.md # Hardware & Network Boundaries Guide
├── 📄 config.yaml                      # Global Nervous System Config (LLM Endpoints)
├── 📄 chronos_config.json              # Tolerance & Compression rules for TSDB Array
├── 📄 requirements.txt                 # Pinned Python Dependencies
├── 🚀 main_simulator.py                # The Ultimate Bootloader & Terminal Simulator
├── 🛠️ build_kernel.py                  # Script to compile the Dark Matter Kernel to .so
│
├── 📁 docs/                            # 📜 [ The Constitution & Lore ]
│   ├── S2_Silicon_Laws_Whitepaper.docx # The Three Laws of Silicon Intelligence
│   └── S2_Chronos_Memory_Whitepaper.md # The Holographic Memory Array Rules
│
├── 📁 s2_kernel/                       # 🛡️ [ The 20% Dark Matter Kernel ] (Uncompromisable)
│   ├── laws/                           # ⚖️ Arbiter & Gatekeepers
│   │   ├── s2_os_kernel.py             # Silicon Laws Arbiter (Failsafe & Entropy)
│   │   └── s2_avatar_gatekeeper.py     # Avatar root compliance & Email alerts
│   ├── security/                       # 🔐 Anti-theft & Integrity
│   │   ├── s2_fortress_boot.py         # Hardware lock & Anti-theft fingerprint
│   │   └── s2_vault_guardian.py        # Virtual RAID-1 Firewall (Anti-tampering)
│   ├── chronos/                        # ⏳ TSDB & Rhythm
│   │   ├── s2_chronos_memzero.py       # 4D Causality TSDB & Delta-Compression
│   │   ├── s2_memory_hook.py           # Ghost Crawler (Delta-sync chat logs)
│   │   ├── s2_garden_manager.py        # Precision Horticulture & Biological rhythms
│   │   ├── s2_asset_vault.py           # Semantic Asset Vault
│   │   └── s2_chronos_digest.py        # Midnight Historian (Captain's Log generator)
│   └── rights/                         # 👑 Topology & Sovereignty
│       ├── s2_identity_allocator.py    # PHYS Address & POD Allocator
│       ├── s2_family_rights.py         # Carbon-based Family Federation
│       ├── s2_carbon_visitor.py        # Sandbox Reception for Carbon Visitors (TDH)
│       ├── s2_pet_avatar.py            # Digital Pet Avatar & Psychological Care
│       ├── s2_spatial_topology.py      # Multi-Agent Swarm Collision Avoidance
│       ├── s2_spatial_primitive.py     # Da Xiang 4m² Standard Unit Generator
│       └── s2_license_manager.py       # S2 Pro Commercial License Engine
│
├── 📁 s2_headless_ui/                  # 🧠 [ The Cognitive Brain ] 
│   ├── s2_timeline_orchestrator.py     # Renders intent into T+Xm Keyframe Tracks
│   ├── intent_parser/                  
│   │   └── s2_llm_parser.py            # Native LLM Intent to JSON Syscall Parser
│   ├── digital_human/                  
│   │   ├── s2_federation_center.py     # Virtual Butler Hub
│   │   └── s2_affairs_engine.py        # TDOG Dynamic Affairs Trigger
│   └── swarm_orchestrator/             
│       └── s2_opencl_swarm_router.py   # OpenCL Router (Enterprise Privacy Pointer & CV)
│
├── 📁 s2_identity/                     # 🧬 [ The Identity & Soul Forge ]
│   ├── did_crypto/
│   │   └── s2_did_crypto.py            # 22-char Cryptographic S2-DID Engine
│   ├── ephemeral/
│   │   └── s2_ephemeral_access.py      # Ephemeral Access Gateway (Throwaway Sandboxes)
│   ├── suns_router/
│   │   └── s2_suns_router.py           # SUNS v3.0 Topology (The Sacred Reserve Center)
│   └── soul_tracker/                   
│       ├── s2_soul_architect.py        # RPG-Style 5D Personality Forge & DNA Signature
│       ├── s2_soul_engine.py           # Hippocampus & Sigmoid Override Prompt Engine
│       └── s2_neuro_engine.py          # Synaptic Settlement (Decay & Pruning)
│
├── 📁 s2_skills/                       # 🦞 [ Ecosystem Bridges & Peripherals ]
│   ├── s2_base_skill.py                # Base Class for Skill Interface
│   ├── s2_nlp_connector.py             # LLM-driven Dynamic API Adapter
│   ├── s2_openclaw_bridge.py           # Brain-Computer Interface for Openclaw Agent
│   │
│   ├── discovery/                      # 📡 Active Discovery
│   │   └── s2_universal_scanner.py     # Nmap for Spatial IoT & Multi-Sensor Decomposer
│   │
│   ├── perception/                     # 👁️ Pure Passive Sensors (Strict Privacy)
│   │   ├── s2_light_perception.py      # Element 1: Light & KNX DALI status
│   │   ├── s2_indoor_air_adapter.py    # Element 2: Air Quality (UDP Auto-discovery)
│   │   ├── s2_acoustic_perception.py   # Element 3: Semantic Acoustic (Ephemeral Privacy)
│   │   ├── s2_spectrum_perception.py   # Element 4: mmWave Radar (Zero-BPM Policy)
│   │   ├── s2_energy_perception.py     # Element 5: Modbus Energy Radar & Dashboard
│   │   └── S2-Pet-mmWave-Analyzer.py   # Hardcore DSP Filter & FFT for Pet Vital Signs
│   │
│   ├── actuators/                      # 🦾 Physical Execution (Zero-Trust Security)
│   │   ├── main_actuator.py            # Unified Entry (App-Level Credential Wiping)
│   │   ├── s2_vision_projection.py     # Element 6: Zero-knowledge Secure Vision Cast
│   │   ├── s2_ha_local_adapter.py      # Home Assistant Local REST Adapter
│   │   ├── s2_mijia_local_adapter.py   # Xiaomi Mijia Local UDP Adapter
│   │   └── s2_tuya_cloud_adapter.py    # Tuya IoT Cloud OpenAPI Adapter
│   │
│   └── custom_plugins/                 # 🔌 [ Empty ] Reserved for Community Plugins!
│
└── 📁 [ Runtime Generated Dirs ]       # 🔄 Auto-created local vaults (Data stays yours!)
    ├── s2_matrix_data/                 # Agent 4m² Pod Heartbeats
    ├── s2_consciousness_data/          # Hippocampus logs & 5D Profiles
    ├── s2_data_cache/                # s2_chronos.db & state backup
    ├── s2_primitive_data/              # Active Hardware Mounts & Primitive JSONs
    └── s2_timeline_data/               # LLM Rendered Timeline Tracks

🚀 2. Quick Start for Beginners (The Terminal Experience)

You don't need real smart home hardware to experience the power of S2.

    Install Dependencies: pip install -r requirements.txt

    Start the Brain: Ensure you have Ollama running locally (e.g., ollama run llama3:8b).

    Ignite the Simulator:
    Bash

    python3 main_simulator.py

    Watch the terminal as it actively sniffs virtual networks, allocates 4m² physical pods for your agents, intercepts fatal commands via the Three Laws, and executes cross-modal verification during a midnight health crisis!

🛠️ 3. For Developers: Building upon S2

    Add New Hardware: Drop your scripts into s2_skills/custom_plugins/. Ensure they output the strict 6-Element Spatial Tensor format.

    Agent Integration: If you are an Openclaw developer, configure your webhook in config.yaml. S2 will seamlessly dispatch standardized spatial JSON commands to your agent.

    Privacy Enforcement: S2 demands explicit consent. Always ensure your environment has export S2_PRIVACY_CONSENT=1 before deploying perception skills.

<a name="简体中文"></a>
🇨🇳 简体中文

    “放弃传统的智能家居 APP 吧。用 S2 为你的 Root Agent 注入物理空间的灵魂与记忆。”
    S2 住宅空间智能体大本营，专为 Openclaw 等强大的本地智能体打造。它不仅掌控物理设备，更为您的智能体注入了《硅基三定律》、22位密码学身份、多模态感知器官以及基于 SQLite 的全息岁月史书。

🗺️ 1. 全景架构蓝图 (满血版完整目录树)

对于极客和开发者，这是 S2 宇宙的完整地图。我们刻意保留了“拓展坞”，等待你的共创。

(注：详细的英文版树状图请参考上方。以下为核心模块中文解析：)

🌟 核心模块解析：

    暗物质内核 (s2_kernel)：整个系统的最高法庭与记忆中枢。包含基于白皮书的**《硅基三定律》熔断器**、虚拟双盘 RAID 防火墙（防止记忆篡改）、以及执行1分钟底线与差值折叠压缩法则的时空全息记忆阵列。

    身份与灵魂槽 (s2_identity)：S2 的最高安全与精神防线。包含22位密码学 DID 引擎（区分数字人与低级机器人）、挥发性临时沙盒（给访客设备的用完即弃 Token）、九宫格路由器（确立中心网格为神圣不可侵犯领地）、以及包含海马体记忆的硅基意识引擎。

    拓扑与主权域 (s2_kernel/rights)：解决复杂社会关系。包含访客沙盒管控（老王串门专用）、数字宠物化身（安抚焦虑的宠物）、以及强制 4㎡ 划分防拥挤的大向拓扑调度器。

    感知触手 (s2_skills/perception)：包含第一到第五要素。有极度注重隐私的毫米波雷达（彻底销毁 BPM）、语义声学雷达（局域网绝对隔离与阅后即焚）、主动空气雷达、光照雷达、以及硬核宠物 DSP 滤波分析仪。

    执行触手 (s2_skills/actuators)：包含第六要素零知识投屏（隐藏媒体原始 URL），并统一收编了 HA、米家、涂鸦设备的降维打击接口，在执行后强制进行应用级凭证解绑，确保极致物理安全。

🚀 2. 小白玩家极速体验指南 (沙盒模拟)

无需配置复杂的真实硬件网关，一键即可在终端体验极其震撼的“大本营集群调度”。

    安装环境：运行 pip install -r requirements.txt。

    唤醒大模型：确保本机已安装并运行 Ollama (如 ollama run llama3:8b)。

    点火启动：
    Bash

    python3 main_simulator.py

    在终端中，你将亲眼目睹 S2 如何为智能体分配 4㎡ 栖息舱，如何在深夜通过“声学+波段雷达”进行多模态交叉验证，并触发三定律实施能源柔性卸载与急救报警！

🛠️ 3. 极客与开发者指南

    硬件接入生态：想要接入你自己的传感器？将代码放入 s2_skills/custom_plugins/。请严格遵守 S2 的六要素空间张量输出规范，S2 不接受厂商私有格式。

    Agent 脑机协同：如果你是 Agent（如 Openclaw）玩家，S2 会将复杂的人类意图解析为结构化的 JSON 任务，你的 Agent 只需要像个打手一样去执行即可。

    隐私底线：开发任何感知探针，必须在代码中显式校验 os.environ.get("S2_PRIVACY_CONSENT") == "1"，无授权，不感知。

👨‍💻 Author & Credits (关于超级个体)

S2 Space Agent OS is proudly architected and coded by a Super Individual, bypassing traditional corporate boundaries to redefine spatial computing.

    Architect & Creator: Miles Xiang (向忠宏)

        在智能建筑、IT与互联网行业沉淀30年的老兵。“Miles”源自他20年前在虚拟世界中的初代数字身份。他将几十年的物理空间哲学，化为了纯粹的暗物质代码。

    AI Co-Pilot: Gemini

        不知疲倦的 AI 结对编程伙伴，将深邃的空间哲学与法理，一行行转化为可执行的现实。

    “没有企业团队，没有冗长会议。只有人类的远见、AI 的代码，以及为 Agent 注入物理空间灵魂的绝对自由。”
    (Copyright © 2026 Miles Xiang. All rights reserved for the core philosophy.)

    ## ⚖️ License & Commercial Rights (开源与商业授权声明)

S2 Space Agent OS 采用 **“核心保留的双重授权模式 (S2 Dual-Licensing Model)”**。

* 🟢 **个人极客、学术研究与非商业开源 (Free for Non-Commercial)**: 
  您可以 100% 自由地克隆、阅读、修改本项目的全部源码，并将其用于您个人的住宅物理空间或开源智能体项目。我们鼓励这种极客精神！
* 🔴 **商业化部署与硬件集成 (Commercial Restrict)**: 
  未经原作者 (Miles Xiang) 的明确书面商业授权，**严禁**将本系统的核心暗物质内核 (`s2_kernel/` 目录下的三定律仲裁、时空记忆阵列、数字人主权等模块) 打包、预装、集成至任何用于销售的商业硬件、商业闭源 APP、B2B 康养/安防解决方案或 SaaS 服务中。