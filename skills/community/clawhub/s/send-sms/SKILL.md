---
name: sms-chuanglan
description: 通过创蓝短信平台发送模板短信
version: 1.0.7
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - jq
        - openssl
      env:
        - CHANGLAN_ACCOUNT
        - CHANGLAN_PASSWORD
---

# sms-chuanglan

通过创蓝短信平台发送模板短信的 Claude Code Skill。

> **关于创蓝短信**：[创蓝云智](https://www.chuanglan.com/)是国内领先的短信服务商，提供短信发送、验证码、营销短信等企业级通讯服务。注册即可享受优惠价格和稳定高效的短信发送服务。

## 安装

1. 从 ClawHub 安装此 Skill

## 配置

使用此 Skill 前，你需要先拥有创蓝短信 API 账号。**还没有账号？** [立即注册](https://www.chuanglan.com/register)

### 获取 API 账号

1. 登录 [创蓝控制台](https://www.chuanglan.com/)
2. 完成企业认证 + 实名认证
3. 获取 API 账号（登录手机号即为账号）
4. 获取 API 密码
5. 在对应账号下添加服务器出口 IP 到白名单

### 配置凭证

安装后，你可以在 OpenClaw 界面中直接配置账号密码（推荐），或使用以下方式：

#### 方式一：OpenClaw 界面配置（推荐）

在 OpenClaw 配置界面直接输入：
- `CHANGLAN_ACCOUNT` - 你的 API 账号
- `CHANGLAN_PASSWORD` - 你的 API 密码

#### 方式二：环境变量

```bash
export CHANGLAN_ACCOUNT=你的API账号
export CHANGLAN_PASSWORD=你的API密码
```

#### 方式三：.env 文件

```bash
cd ~/.claude/skills/sms-chuanglan
echo "CHANGLAN_ACCOUNT=你的API账号" > .env
echo "CHANGLAN_PASSWORD=你的API密码" >> .env
```

## 使用方式

```bash
sms-send --phone <手机号> --template <模板ID> [--vars '<变量JSON>']
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| phone | 是 | 接收手机号 |
| template | 是 | 创蓝平台审核通过的模板ID |
| vars | 否 | 变量JSON，格式 `{"param1":"value1"}`，常量模板可不传 |

### 示例

**有变量模板：**
```bash
sms-send --phone 13800138000 --template 1021143438 --vars '{"param1":"验证码","param2":"123456"}'
```

**常量模板（无变量）：**
```bash
sms-send --phone 13800138000 --template 1021701163
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 000000 | 提交成功 |
| 101 | 无此用户 |
| 102 | 密码错误 |
| 105 | 敏感短信 |
| 107 | 手机号码错误 |
| 109 | 无发送额度 |
| 117 | IP未加白 |
| 130 | 请求参数错误 |

## 注意事项

1. 手机号不要包含区号或+86前缀
2. 变量键名必须是 param1, param2 等
3. 批量发送时多个手机号用逗号分隔，最多1000个
4. 请确保已在 [控制台](https://www.chuanglan.com/) 添加服务器 IP 到白名单

## 相关链接

- [创蓝官网](https://www.chuanglan.com/)
- [控制台登录](https://www.chuanglan.com/)
- [注册账号](https://www.chuanglan.com/register)
- [短信签名实名制说明](https://doc.chuanglan.com/document/9OHGKZG716OXFI9O)
- [API 接口文档](https://doc.chuanglan.com/document/HAQYSZKH9HT5Z50L)
