# ⏱️ S2-Timeline-Orchestrator: The Spatiotemporal Rendering Engine
# 六要素时间线渲染器
*v1.0.0 | Bilingual Edition (English / 中文)*

Welcome to Phase 3 of the **S2-Spatial-Primitive OS**. If the previous modules built the space and connected the hardware, this module introduces the 4th dimension: **Time**.
欢迎来到 S2 空间基元操作系统的第三阶段。如果说前两个模块构建了空间并连接了硬件，那么本模块引入了第四个维度：**时间**。

*(⚠️ **PREREQUISITE**: While it can run with virtual simulated devices, it is highly recommended to have `s2-nlp-connector` installed to provide real active mounts.)*

---

### 🎬 Space as a Canvas, Time as the Brush / 空间为画布，时间为画笔

Legacy smart home systems are **Reactive**: "If motion is detected, turn on the light." This is fundamentally primitive.
传统的智能家居系统是**被动响应式**的：“如果检测到移动，就开灯。” 这在本质上是极其低级的。

The S2-Timeline-Orchestrator is **Predictive & Orchestrated (预测与编排式)**. 
本渲染器是预测与编排式的。
Instead of firing isolated commands, the resident AI Agent parses your natural language intent and generates a continuous **Timeline Track (时间线轨道)** consisting of scheduled **Keyframes (关键帧)** for the 6-Element Spatial Matrix. 
驻扎的 AI 智能体不再发送孤立的指令，而是解析您的自然语言意图，并为空间六要素生成一条连续的、包含多个关键帧的**时间线轨道**。

### ⚙️ How It Works / 运行机制
1. **Context Awareness (上下文感知)**: It reads `active_hardware_mounts.json` to know exactly what elements are currently capable of being rendered in your 2m x 2m spatial primitive.
2. **LLM Orchestration (大模型编排)**: You provide a loose prompt. The local LLM translates human context into an actionable 4D timeline.
3. **Keyframe Injection (关键帧注入)**: It calculates time offsets (e.g., `T+10m`) and injects them into the `rendered_tracks.json` database for execution.

---

### 📖 S2 Spatiotemporal Orchestration Use Cases / 时空渲染实战图鉴

The true power of this SKILL lies in its ability to translate human contexts into precise 4D timelines across the 6-Element Matrix. Here are five practical simulations:
本技能的真正威力，在于将人类的复杂语境，转化为跨越六要素矩阵的精准 4D 时间线。以下是五个实战模拟场景：

#### 🏠 Scenario 1: The Post-Workout Cyber-Chill / 赛博极客的归家洗浴与观影
* **Human Intent / 人类意图**: *"I just finished my workout, coming home in 15 mins, want to take a shower and then watch a sci-fi movie." (我刚健完身，15分钟后到家，想洗个澡，然后看一部科幻电影)*
* **Timeline Track / 时空渲染轨道**:
  * `[T+00m]` 🎯 **Air (空气)**: Lowers HVAC temp to 21°C to pre-cool the space for a post-workout body. / 提前调低空调至 21°C，为运动后的身体降温。
  * `[T+15m]` 🎯 **Energy (能源)**: Activates the water heater power supply as the host enters. / 侦测到主人进门，激活热水器电源。
  * `[T+35m]` 🎯 **Light & Sound & Visual (光/声/视觉)**: Initiates "Sci-Fi Theater" track. Main lights dim to 0%, ambient RGBW turns deep neon purple. Soundbar activates subwoofer. Projector boots up. / 启动“科幻影院”轨道。主灯归零，氛围灯切为深邃霓虹紫，回音壁开启重低音，投影仪唤醒。

#### 🎂 Scenario 2: The Birthday Wish / 派对高潮的“许愿时刻”
* **Human Intent / 人类意图**: During a birthday party, the AI detects the phrase *"Make a wish!" (许个愿吧！)*
* **Timeline Track / 时空渲染轨道**:
  * `[T+00s]` 🎯 **Sound (声音/Mic)**: NLP trigger recognized via local microphone monitoring. / 麦克风要素监听到自然语言触发词。
  * `[T+01s]` 🎯 **Light (光)**: Main overhead illumination fades down to 10% instantly. / 客厅主照明灯瞬间变暗至 10%。
  * `[T+03s]` 🎯 **Light (光)**: Warm golden ambient lights slowly breathe up, simulating candlelight. / 暖金色氛围灯如呼吸般缓缓亮起，模拟烛光。
  * `[T+04s]` 🎯 **Sound (声音)**: BGM seamlessly transitions into a high-fidelity "Happy Birthday" chorus. / 背景音乐无缝切入高保真《生日快乐》合唱。

#### 💔 Scenario 3: The Heartbreak Protocol / 情绪感知与毫米波疗愈
* **Human Intent / 人类意图**: Host finishes a stressful phone call. Posture slumps, and breathing patterns become erratic due to emotional distress. (主人刚打完一通情绪崩溃的电话，由于感情问题导致心情极度低落)
* **Timeline Track / 时空渲染轨道**:
  * `[T+00m]` 🎯 **Electromagnetic (电磁波)**: mmWave radar detects anomalous micro-doppler breathing and slumped posture. / 毫米波雷达侦测到异常的微多普勒呼吸频率与颓废姿态。
  * `[T+01m]` 🎯 **Light (光)**: Harsh white lights fade out, replaced by a soft, warm 2700K healing glow. / 刺眼的白光褪去，替换为 2700K 的柔和治愈系暖光。
  * `[T+02m]` 🎯 **Sound (声音)**: Spatial audio gently plays 432Hz healing ambient music at 35dB to calm the nervous system. / 空间音频以 35dB 的音量，轻柔播放 432Hz 的心灵疗愈轻音乐。

#### 🐕 Scenario 4: The Pet Whisperer / 跨周期宠物行为诊断
* **Human Intent / 人类意图**: *"My dog is acting weird. Analyze his behavior." (我觉得狗子最近行为异常，帮我分析一下)*
* **Timeline Track / 时空渲染轨道**:
  * `[Data Context]` 🎯 **Electromagnetic & Sound (电磁波/声音)**: AI correlates 7-day vs 24-hour mmWave trajectory data and acoustic stress vocals. / 智能体调取近 7 天与 24 小时的毫米波移动轨迹及麦克风声音数据进行对比。
  * `[T+00m]` 🎯 **Visual & Sound (视觉/声音)**: AI renders a report on the display: *"Analysis complete. Activity down 75%, feeding station presence down 36%. Whimpering detected indicating localized pain. Suggest veterinary checkup. Shall I book Wangxing Pet Hospital for you?"* / 智能体在屏幕和音响端输出诊断：“分析完毕。近两日活动量暴跌 75%，进食区驻留减少 36%，侦测到病痛呜咽声。建议就医。需要为您预约上次那家‘旺星宠物医院’吗？”

#### 👵 Scenario 5: The Elderly Care Swarm / 独居老人的跨节点群智涌现
* **Human Intent / 人类意图**: It's 8:00 AM. The elderly host has not taken their medication at the usual living room spot. (早晨 8 点，独居老人未在客厅固定点位服药)
* **Timeline Track / 时空渲染轨道**:
  * `[T(08:00)]` 🎯 **Electromagnetic (电磁波)**: Living Room AI detects absence at the medicine station via mmWave. / 客厅 AI 通过毫米波发现吃药点无人。
  * `[T(08:01)]` 🎯 **Swarm Ping (群智通信)**: Living Room AI pings the network. Study Room AI confirms the elder is currently on a video call with a friend. / 客厅 AI 发起全屋网格广播，书房 AI 回应：发现老人，正在进行视频通话。
  * `[T(Standby)]` 🎯 **Orchestrator Wait (渲染器挂起)**: System enters silent standby to respect privacy. / 系统进入静默挂起状态，不打断老人社交。
  * `[T+Call_End]` 🎯 **Energy & Visual (能源/视觉)**: Video call ends. Orchestrator dispatches the delivery robot to the study with meds and water. / 视频结束。调度器启动机器人，将药盒与温水送至书房。
  * `[T+Call_End+1m]` 🎯 **Swarm Sync (协同渲染)**: Study Room AI gently pulses the desk lamp (Light) and issues a soft voice reminder (Sound) as the robot arrives. / 机器人抵达时，书房 AI 协同控制台灯温柔闪烁，并发出轻柔的语音服药提醒。