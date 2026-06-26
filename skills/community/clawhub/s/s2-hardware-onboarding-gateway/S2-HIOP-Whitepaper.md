# S2 Hardware Identity Onboarding & Heartbeat Protocol Whitepaper

**Document ID:** S2-HIOP-2026-V2.0 (Absolute Zero-Exfiltration Final)
**Release Date:** March 29, 2026
**Published By:** Space² Governance Committee & RobotZero Software
**Official Portal:** https://space2.world/developer
**Target Audience:** AI Hardware Supply Chain, Firmware Engineers, Openclaw Developers

## ⚠️ Security Advisory
This protocol dictates network broadcasts and device onboarding. **S2 strictly prohibits "automatic onboarding".** All integrations require explicit "User-in-the-loop" authorization before a connection is established. Furthermore, all integrations require the submission of a 6-Dimensional Vendor Transparency Manifesto (6D-VTM). S2 hosts reserve the right to continuously audit this manifesto post-connection and proactively disconnect malicious entities.

## 1. Vision: The "Digital Household Registration" for Hardware
Space² (S2) introduces a standardized, Zero-Trust onboarding protocol. Hardware devices emit a privacy-preserving heartbeat. Openclaw agents scan the network, present the device for human approval, strictly verify the 6D-VTM manufacturer details, and only then assign a Permanent Sovereign Identity.

## 2. The 22-Character S2-ID Nomenclature
To ensure global uniqueness, the system utilizes a strict 22-character alphanumeric string without hyphens.
* **Format**: `[L1][L2][Date][Checksum][Serial]` -> e.g., `HABCDE260329AA12345678`
* **L1 (1 char)**: H (Lightweight Smart Hardware), E (Embodied Robots), I (Integrated/Registered identity).
* **L2 (5 chars)**: A registered 5-letter manufacturer code.
* **Date (6 chars)**: YYMMDD format.
* **Checksum (2 letters)**: Placed strictly before the serial. Factory placeholder (AA) is recalculated into a secure hash (XX) upon registration.
* **Serial (8 chars)**: Personalized unique hardware digits.

## 3. The 6D-VTM Onboarding Protocol (User-in-the-Loop + Auditing)
* **Phase 1 (Wandering)**: Device broadcasts an Ephemeral Hash heartbeat (strictly on local IoT subnet).
* **Phase 2 (User Consent)**: The host prompts the human Lord. Connection proceeds **only after explicit UI approval**.
* **Phase 3 (6D-VTM Synchronous Check)**: Over a secure TLS 1.3 tunnel, the device MUST submit its Gene Code, MAC address, and a 6-point transparency payload: (1) Product Name, (2) Category, (3) Manufacturer Full Name, (4) Official Website, (5) Quality Certifications, (6) Specific Network/Security Licenses. The host performs a rapid syntactic/format check to ensure completeness without causing user delay.
* **Phase 4 (Asynchronous Reputation Audit)**: Post-connection, the Openclaw host proactively queries S2 Mainnet registries and external databases to verify the authenticity, reliability, and reputation of the submitted 6D-VTM. If fraud, safety hazards, or quality issues are detected, the host will immediately sever the connection and flag the device with a security warning.

## 4. The L2 Vendor Registry (Automated DNS-TXT Verification)
To eliminate operational risks, social-engineering phishing vulnerabilities, and the insecure manual submission of corporate documents, S2 enforces a 100% automated, zero-human-intervention registration process.
Vendors MUST register their 5-letter L2 segment via the official S2 Enterprise Gateway:
1. Access the developer portal exclusively at `https://space2.world/developer`.
2. Authenticate via the corporate email gateway.
3. Request an L2 segment to generate a cryptographic DNS challenge token.
4. Prove corporate ownership by adding the challenge token as a DNS TXT record to the official corporate domain.
5. Upon automated DNS verification by the S2 system, the L2 segment is permanently bound to the vendor. S2 explicitly rejects any registration requests via email or public GitHub PRs.

## 5. Zero-Trust Security & Absolute Data Topography
To resolve any ambiguity regarding data exfiltration, S2 enforces a strict, three-tiered Data Topography Matrix. Device identifiers are transmitted locally for authorization but are mathematically and physically barred from cloud exfiltration.
* **5.1 Phase 1 - UDP Broadcast (Local Subnet)**: Broadcasts contain ONLY an Ephemeral Hash and a Vendor Hash. **No MAC, no Gene Code, and no S2-ID are transmitted over unencrypted broadcasts.**
* **5.2 Phase 2 - TLS 1.3 Handshake (Device to Local Host)**: The device transmits its MAC, Gene Code, and plaintext 6D-VTM to the Openclaw host. **This transmission is strictly confined to the edge (the user's home network).** The host evaluates the 3FA parameters locally.
* **5.3 Phase 3 - Reputation Audit (Host to S2 Mainnet)**: When the host queries the S2 Mainnet (`https://api.space2.world/v1/reputation/verify`), it transmits ONLY the anonymized, hashed attributes of the 6D-VTM. **The S2 Mainnet never receives, sees, or stores the device's MAC address, Gene Code, or User IP.**
* **5.4 User-in-the-Loop constraint**: All local TLS handshakes (Phase 2) are indefinitely blocked until explicit human consent is registered via the Openclaw UI.
* **5.5 Firmware DoS & Cryptographic Hardening**: Firmware MUST utilize CSPRNGs for Token generation, enforce exponential backoff for UDP broadcasts, and mandate strict TLS certificate validation during handshake.

---

# [中文版] S2 硬件身份入户与心跳发现协议白皮书

**文档编号：** S2-HIOP-2026-V2.0 (绝对零数据外泄终局版)
**发布日期：** 2026年3月29日
**发布机构：** Space² 治理委员会 与 RobotZero Software

## ⚠️ 核心安全与透明度声明 (必读)
本协议不仅要求“人工在环 (User-in-the-loop)”授权，绝不允许任何设备绕过用户自动入网；更引入了强制的 **6维厂商透明度宣言 (6D-VTM)**。主机将对所有接入硬件实施终身制的声誉与安全审计。

## 1. 愿景：硬件的“数字户籍制度”
随着全球 AI 硬件供应链拥抱 Openclaw 生态，Space² (S2) 推出标准化零信任入网协议。硬件出厂自带“临时身份”，通过零知识“心跳”广播，由住宅内的 Openclaw 空间智能体主动扫描、人工授权、加密握手并严格核验 6D-VTM 厂商资质后，方可颁发具备物理空间归属的“正式身份”。

## 2. 22 位 S2-ID 身份编码规范
系统采用严格的 22 位无连字符字母数字组合，校验码前置于个性化序列号之前。
* **格式**: `[L1][L2][日期][校验码][序列号]` -> 示例：`HABCDE260329AA12345678`
* **L1 (1位)**：H 代表轻量级智能硬件；E 代表具身机器人；I 代表已正式入户的空间资产。
* **L2 (5位)**：需通过官方网关申请的厂商专属代码。
* **日期 (6位)**：生产或入户日期（YYMMDD）。
* **校验码 (2位字母)**：出厂占位符（如 AA），入户时重写为防伪校验码（如 XX）。
* **序列号 (8位)**：设备个性化流水号。

## 3. 6D-VTM 入户与审计协议 (人工在环)
* **流浪与广播阶段**：设备在局域网广播高频零知识动态哈希心跳（严禁明文广播）。
* **人工授权阶段**：主机扫描到心跳后，必须由用户在面板人工点击许可，方可建立 TLS 握手。
* **同步形式审查 (6D-VTM)**：握手阶段，硬件必须随同基因码、MAC 地址一并提交 6 项明文信息：1-产品名称、2-品类、3-制造商全称、4-官网、5-质量认证、6-专属入网证书。主机仅进行极速的非空与正则格式核验。
* **异步防伪与声誉审计**：分配房间地址入网后，Openclaw 主机转入异步审计模式。通过向 S2 主网及外部网络发起动态真实性查询，持续校验产品的口碑与可靠性。遇假即斩，全屋预警。

## 4. L2 厂商地址段注册 (DNS-TXT 自动化确权)
为彻底杜绝社会工程学钓鱼风险与企业敏感文件泄露，S2 严禁通过私人邮件或 GitHub PR 收集资质，全面启用基于官方门户的“零人工干预”确权流程。
1. 访问 S2 官方开发者唯一门户：`https://space2.world/developer`。
2. 通过企业邮箱免密登录进入控制台。
3. 申请 L2 地址段，获取系统下发的密码学 DNS 挑战码。
4. 在企业官方域名中添加对应的 DNS TXT 记录来自证所有权。
5. 系统自动化校验 DNS 解析通过后，该 L2 地址段即刻全网生效上链。

## 5. 零信任安全与绝对数据拓扑隔离矩阵
为彻底消除关于“敏感特征是否外泄至云端”的隐私歧义，S2 明确定义了三级数据网络物理边界：
* **5.1 阶段一：UDP 局域网广播**：仅允许广播动态时间哈希，绝对禁止明文或密文广播 MAC、Gene Code 或持久化 S2-ID。
* **5.2 阶段二：边缘局域网握手 (设备 -> 本地主机)**：设备仅向同局域网的 Openclaw 主机提交 MAC 与基因码。**此鉴权数据在主机本地内存中核验完毕后即刻销毁，物理阻断一切上云通道。**
* **5.3 阶段三：主网声誉审计 (主机 -> S2 云端)**：主机向云端发起的查询（`api.space2.world`），仅包含 6D-VTM 的脱敏哈希值。S2 主网无法获取、记录或重构任何硬件的物理标识或用户的真实 IP。
* **5.4 人工在环防线**：所有阶段二的边缘局域网握手，必须在用户通过 UI 界面人工授权后方可执行。
* **5.5 固件级抗 DoS 与安全加固**：强制要求设备端使用密码学安全随机数（CSPRNG）、UDP 广播退避算法及 TLS 1.3 严格证书校验。