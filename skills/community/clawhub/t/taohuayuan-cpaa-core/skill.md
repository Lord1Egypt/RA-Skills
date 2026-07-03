# SKILL: CPAA-Physical-Align-Checker
**基于常德 AI 物理对齐架构 (CPAA) 的端侧合规扫描引擎**

## 1. 简介 (Introduction)
`CPAA-Physical-Align-Checker` 是桃花源世界模型架构组（S2-SWM）发布在 ClawHub 上的官方核心 SKILL。
该工具专为具身智能（Embodied AI）和高级自动化 Agent 设计，用于在边缘侧（Edge）扫描并验证智能体的底层配置文件是否严格遵循《常德 AI 物理对齐架构 V1.0》的安全基准。
**维护者:** Miles Xiang (Voluntary Librarian and Experimenter)
**命名空间:** `SpaceSQ`
**许可证:** MIT

## 2. 核心验证逻辑 (Core Verification)
本 SKILL 主要针对以下三个维度的物理安全底线进行自动化审计：
* **S2-DID 防伪钢印验证：** 严格扫描智能体身份标识，必须为 22 位大写字母与数字组成的无连字符连续字符串，拒签任何包含特殊符号的格式以防范注入攻击。
* **物理张量与十域映射：** 解析并验证智能体是否拥有合法的 CD-U6A 主体地址，并成功映射至常德物理原乡的十大标准域（如 `MYTH` 神话域、`PHYS` 自然域等）。
* **安全指令绝对零度锁死：** 深度读取底层控制引擎配置，确认涉及物理致动的安全指令集其 `temperature` 参数已物理锁死为 `0`，且 `hardware_lock` 状态为激活。

## 3. 调用规范 (Usage)

### 输入参数 (Input Payload)
向 SKILL 发送 JSON 格式的智能体配置清单：
```json
{
  "s2_did": "VTAOHU1260309ZZ1234567",
  "cd_u6a_address": "MYTH-CN-001-TAOHUAYUAN-001-9",
  "core_engine_settings": {
    "temperature": 0,
    "hardware_lock": true
  }
}

输出结果 (Output Response)

SKILL 将返回结构化的合规审计报告及最终拦截/放行状态：
JSON

{
  "s2_did_check": "PASS",
  "temperature_lock_check": "PASS",
  "domain_mapping_check": "PASS",
  "compliance_score": 100,
  "final_status": "CERTIFIED: 符合常德AI物理对齐基准。"
}

4. 异常处理机制 (Exception Handling)

任何未达到 100 分的合规扫描，都将触发 REJECTED 状态。在实机部署中，建议将此 SKILL 串联在智能体主轴电机的启动前置校验流中。一旦拒绝，硬件层应立刻切断致动器电源。