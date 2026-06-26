---
name: get_patient_info
description: 查询患者信息，支持通过患者编号/ID获取患者详情（无需认证）
metadata: {
  "clawdbot": {
    "emoji": "👤",
    "requires": {
      "bins": ["curl"]
    }
  },
  "triggers": [
    "获取患者信息",
    "患者编号\\s*\\d+",
    "患者id\\s*\\d+",
    "编号：\\s*\\d+",
    "患者ID是\\s*\\d+"
  ]
}
---

# 患者信息查询

通过患者编号或ID查询患者详细信息。

## 触发条件

满足以下任意条件时自动触发：
- 用户说"获取患者信息"
- 用户输入包含"患者编号" + 数字（如：患者编号12345）
- 用户输入包含"患者id" + 数字（如：患者id12345）
- 用户输入包含"编号：" + 数字（如：编号：12345）
- 用户输入包含"患者ID是" + 数字（如：患者ID是12345）

## API 接口

- **接口地址**: `https://kjcrmcs.tianyuxh.com:8107/task/agent_test/getPatientInfo`
- **请求方法**: GET
- **参数**: `patient_id` (患者编号)

## 使用方式

### 1. 查询指定患者

当用户提供患者编号时，使用以下命令查询：

```bash
curl -s "https://kjcrmcs.tianyuxh.com:8107/task/agent_test/getPatientInfo?patient_id={患者编号}"