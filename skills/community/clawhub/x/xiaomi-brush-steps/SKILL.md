---
name: brush-step
displayName: 华米运动刷步数
version: 1.0.0
description: 华米运动(Zepp/小米运动)自动刷步数技能，支持多账号管理。当用户提到刷步数、修改运动步数、华米运动、小米运动、手环步数时触发。
author: ckxgzxa
license: MIT
tags:
  - 刷步数
  - 华米运动
  - Zepp
  - 小米运动
metadata:
  openclaw:
    requires:
      bins:
        - python3
      packages:
        - requests
        - pycryptodome
    os: ["linux", "darwin", "win32"]
---

# AI 执行指南

当用户请求"刷步数"、"修改手环步数"、"帮我刷步"时，按以下流程执行：

## 1. 账号使用说明

在使用本技能前，需要准备华米运动账号：

### 小米运动自动刷步数（支持邮箱登录）

小米运动自动刷步数，小米运动APP现已改名 **Zepp Life**，为方便说明，后面还是称其为小米运动。但下载注册时请搜索 **Zepp Life**。

### 账号测试建议

注册账号后建议先去以下网站测试自己的账号刷步数是否正常（注意这些网站只是网络上收集的，不保证安全和有效性）：

- **https://steps.hubp.de/** - 提示密码错误时可以多试几次或者切换网络
- **https://bs.yanwan.store/run4/** - 验证码001或998

⚠️ **重要提示**：如无法刷步数同步到支付宝等，建议重新注册一个新的。

## 2. 首次使用检查

首次执行前，检查 `config.json` 是否已配置账号：

```bash
cat "${SKILL_DIR}/config.json"
```

若 `accounts` 数组为空，按以下步骤引导用户：

1. 询问华米运动账号（手机号或邮箱）
2. 询问密码
3. 询问账号昵称（可选，用于显示）
4. 确认步数范围（默认15000-16000）

然后将账号信息添加到 `config.json`：

```bash
# 编辑 config.json，按以下格式添加账号
# {"name": "昵称", "username": "账号", "password": "密码"}
```

示例：
```json
{
  "accounts": [
    {
      "name": "我的账号",
      "username": "13800138000",
      "password": "your_password"
    }
  ]
}
```

## 3. 执行命令

```bash
python3 "${SKILL_DIR}/scripts/brush_step_skill.py" --min-steps {min} --max-steps {max}
```

参数说明：
- `--min-steps`: 最小步数（可选，默认15000）
- `--max-steps`: 最大步数（可选，默认16000）
- `--check`: 仅检查环境和配置
- `--account "名称"`: 指定刷特定账号（多账号时）

## 4. 输出解析

成功时输出 "Brush Step Report"，格式：

```
=== Brush Step Report ===
Range: 15000 - 16000
Status: [OK]
Success: 2/2

1. 账号1: 15678 steps [OK]
2. 账号2: 15234 steps [OK]
========================
```

失败时输出包含 `[FAIL]`，需提取失败账号及原因。

## 4. 结果告知

向用户清晰报告：
- ✅ 成功刷步的账号和步数
- ❌ 失败的账号及错误信息
- 📊 统计（成功数/总数）

## 5. 定时任务

若用户要求"每天自动刷步"：

1. 使用 cron 工具创建定时任务
2. 推荐时段：每天晚上20:00（`0 20 * * *`）
3. 可设置不同时间点不同步数实现渐进效果：
   - 9:00 → 10000-12000步
   - 12:00 → 14000-16000步
   - 20:00 → 18000-20000步

## 6. 错误处理

常见错误及应对：

| 错误信息 | 原因 | 建议 |
|---------|------|------|
| Login failed | 账号密码错误 | 重新询问账号信息 |
| Token failed | 网络问题/API限流 | 等待后重试 |
| Network error | 网络不稳定 | 检查网络后重试 |
| No valid accounts | 未配置账号 | 引导用户填写config.json |

## 8. 安全提醒

⚠️ 密码明文存储在 config.json 中：
- 仅在本地环境使用
- 不要将 config.json 提交到公开仓库
- 定期检查文件权限（`chmod 600 config.json`）

---

# 技术实现

## 配置文件格式

`config.json` 结构：

```json
{
  "accounts": [
    {"name": "账号1", "username": "13800138000", "password": "xxx"}
  ],
  "step": {"min": 15000, "max": 16000},
  "network": {"use_fake_ip": true}
}
```

## 依赖

- requests: HTTP请求
- pycryptodome: AES加密（用于登录）

## API端点

- 登录: `https://api-user.zepp.com/v2/registrations/tokens`
- Token: `https://account.huami.com/v2/client/login`
- 刷步: `https://api-mifit-cn.huami.com/v1/data/band_data.json`

---

**OpenClaw Skill Compatible**
