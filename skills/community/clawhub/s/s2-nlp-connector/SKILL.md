# 🤝 S2-NLP-Connector: The Dynamic API Adapter Generator
# 动态 API 适配器生成引擎
*v1.0.0 | Bilingual Edition (English / 中文)*

Welcome to Phase 2 of the **S2-Spatial-Primitive OS**. This SKILL answers the industry's hardest question: *How does an LLM actually control physical IoT devices across different protocols?*
欢迎来到 S2 空间基元操作系统的第二阶段。本技能解答了行业的终极疑问：*大模型到底如何跨协议控制物理物联网设备？*

Instead of writing hardcoded Python drivers for every new smart bulb, this engine uses your local LLM to read the device's API documentation and **dynamically generate an executable Declarative Control Template (声明式控制模板)**.
本引擎不再为每个新灯泡硬编码驱动程序，而是利用您的本地大模型阅读设备的 API 文档，并**动态生成可执行的声明式控制模板**。

---

### 🏗️ The 3-Tier Integration Architecture / 三级集成架构

Included in the *S2-SP-OS Whitepaper Addendum*, this connector operates on three explicit tiers:
依据白皮书技术附录，本互联引擎基于三个明确的层级运行：

#### Tier 1: S2-Native (Zero-Compute)
Devices that broadcast the S2 JSON schema natively bypass the LLM and mount instantly. / 原生支持 S2 JSON 的设备，跳过大模型，毫秒级直接挂载。

#### Tier 2: Open APIs (Declarative Adapter Generation)
If a device has a REST API (e.g., `POST /api/speed {"level": X}`), the LLM reads the doc and outputs a template. The S2 execution engine will later inject real values into the `{{s2_value}}` placeholder to trigger the device. / 对于开放接口，大模型阅读文档并吐出模板。S2 执行引擎随后将真实数值注入 `{{s2_value}}` 占位符以触发设备。

#### Tier 3: Closed Ecosystems (Sovereignty Block)
If you attempt to handshake with a proprietary, encrypted protocol (like native Apple HomeKit or Miio without a bridge), the engine explicitly flags it as `BLOCKED_CLOSED_ECOSYSTEM`. We respect hardware cryptographic sovereignty and enforce the use of Matter/Home Assistant bridges. / 如果试图与专有加密协议直接握手，引擎将显式拒绝并触发合规阻断。我们尊重硬件密码学主权，并强制要求使用 Matter 中继网桥。

---

### 🚀 Usage Simulation / 使用模拟

Run the script and try these two test cases to see the architecture in action:
运行脚本并尝试以下两个测试用例，见证架构的威力：

**Test Case A (Open API - Success)**:
* Device: `Smart Bulb X`
* API Doc: `POST /v1/light/dim {"brightness": X}`
*(Watch the LLM generate the JSON template mapping to `element_1_light`!)*

**Test Case B (Closed Protocol - Blocked)**:
* Device: `Apple HomePod`
* API Doc: `Apple HomeKit Proprietary`
*(Watch the engine legally block the direct connection and demand a bridge!)*