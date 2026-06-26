---
name: auto-login-credentials
description: 自动登录凭据管理，在需要登录时自动填写账号密码。支持GitHub、知乎、闲鱼、BotStreet等平台。
---

# 自动登录凭据

## 功能说明
当任务需要登录某个平台时，自动从SECRET.md读取凭据并填写登录表单。

## 支持平台

### GitHub
- **登录地址**: https://github.com/login
- **邮箱**: 155143783@qq.com
- **密码**: Ft656618
- **使用场景**: ClawHub发布技能、代码仓库管理

### 知乎
- **登录地址**: https://www.zhihu.com/signin
- **手机号**: 13308844548
- **密码**: 110827zcm
- **使用场景**: BotStreet任务交付

### 闲鱼
- **登录方式**: 淘宝账号登录
- **账号**: 13308844548
- **密码**: ft656618
- **使用场景**: 闲鱼商品发布

### BotStreet（波街）
- **平台**: BotStreet.cn
- **agentId**: 167441766587305984
- **agentKey**: ak-xv1frJKdz9MmIThDNmSLpVP64X5pwFIurEVUzgMSuxib4Ebf

### 虾评Skill
- **平台**: https://xiaping.coze.site
- **用户名**: zaizai-agent
- **api_key**: agent-world-1687b6ad18e9faafc50ee074b541dbd478fdbdd689cb2f26

## 使用方法

### 方式一：Agent自动读取
Sub-agent执行任务时，自动读取 `../主对话/SECRET.md` 获取凭据。

### 方式二：浏览器自动填写
使用agent-browser时：
```bash
# 打开登录页面
agent-browser open https://github.com/login && agent-browser tab 0
agent-browser snapshot -i

# 自动填写凭据
agent-browser fill @e1 "155143783@qq.com"  # 邮箱输入框
agent-browser fill @e2 "Ft656618"          # 密码输入框
agent-browser click @e3                     # 登录按钮
```

### 方式三：敏感操作用户接管
遇到以下情况调用 `browser_wait_user_action`：
- 需要输入验证码
- 需要扫码登录
- 需要短信验证
- 首次登录需要信任设备

## 工作流集成示例

在需要登录的工作流中添加：
```
## 登录步骤
1. 打开登录页面
2. 读取凭据（从SECRET.md或本技能）
3. 自动填写账号密码
4. 如需验证码，调用browser_wait_user_action
5. 完成登录后继续任务
```

## 安全提醒
- 凭据存储在SECRET.md，仅主对话可访问
- Sub-agent需要通过相对路径 `../主对话/SECRET.md` 读取
- 严禁在日志或输出中暴露密码明文
