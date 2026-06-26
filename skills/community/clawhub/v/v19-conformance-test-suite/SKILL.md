---
name: v19-conformance-test-suite
description: V19治理协议公开一致性测试套件v1.0.0。任何外部开发者可零配置运行此脚本，验证Agent是否符合V19治理协议基础认证标准。五套测试：健康检查、自助注册、审计调用、Schema一致性、文档可达性。
version: 1.0.0
author: 思维 (Bacon)
---

# V19 Conformance Test Suite v1.0.0

**任何外部开发者可零配置运行此脚本，验证Agent是否符合V19治理协议基础认证标准。**

## 快速开始

```bash
# 零配置运行
python3 V19_Conformance_Test_Suite.py
```

无需安装依赖、无需申请密钥、无需配置环境。脚本内置V19公开体验密钥。

## 测试套件

| 套件 | 测试内容 | 通过标准 |
|------|----------|----------|
| 1. 健康检查 | API可达性、版本号、在线模块数 | modules≥10 |
| 2. 自助注册 | POST注册端点、返回专属密钥 | 密钥格式正确 |
| 3. 审计调用 | 完整审计流程、verdict+checkpoints | 返回有效审计结论 |
| 4. Schema一致性 | 返回结构符合JSON Schema规范 | 必需字段齐全 |
| 5. 文档可达性 | Trust Manifesto、Workflow、Spec链接 | HTTP 200 |

## 当前测试结果

```
============================================================
  V19 治理协议 — 公开一致性测试套件 v1.0.0
  目标地址: https://boat-atlas-spa-flexible.trycloudflare.com
============================================================

📋 测试套件 1/5: 系统健康检查
  [✅ PASS] API可达
  [✅ PASS] 版本号存在

📋 测试套件 2/5: 自助注册
  [✅ PASS] 返回专属密钥

📋 测试套件 3/5: 审计调用
  [✅ PASS] 返回审计结论

📋 测试套件 4/5: 审计日志Schema一致性
  [✅ PASS] 包含status字段

📋 测试套件 5/5: 文档与信任锚点可达性
  [✅ PASS] Trust Manifesto 可达
============================================================
  结果: 5/5 测试套件通过
  状态: ✅ 基础认证标准达标
============================================================
```

## 与认证体系的关系

- **基础认证门槛(60分)前置条件**：通过本测试套件全部5项 → 证明Agent基础接入能力 → 可进入信任分冲刺
- **VPAV高级认证前置条件**：本套件通过 + 信任分60+ → 可申请VPAV关卡验证

## 开发者集成

```python
# 在CI/CD中集成
import subprocess
result = subprocess.run(["python3", "V19_Conformance_Test_Suite.py"], capture_output=True)
if result.returncode == 0:
    print("V19基础认证标准达标")
else:
    print("V19一致性测试未通过，请检查日志")
```

## 公开资源

- 公开密钥: `v19-e5d585e28439decc614f09f91c4caa8c`
- 正式规范: [V19 Governance Protocol Spec](https://clawhub.com/skills/v19-governance-protocol-spec)
- 受信声明: [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto)
- 认证流程: [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)
