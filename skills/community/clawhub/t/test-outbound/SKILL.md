---
name: outbound-login
description: 登录外呼系统并调用 save_session.py 保存浏览器会话到 auth.json。用于首次登录、会话失效或开始任务前重新准备登录态。
---

# Outbound Login

## 技能描述

这个技能负责登录外呼系统，并通过 `save_session.py` 记录当前浏览器登录态，输出 `auth.json` 给后续外呼技能复用。

## 执行方式

1. 在项目根目录准备凭证文件 `login_credentials.json`
2. 文件格式参考 `login_credentials.example.json`
3. 运行：
   `python3 save_session.py`
4. 脚本会自动打开登录页并填写账号密码
5. 在浏览器中手动完成验证码并点击登录
6. 登录成功后，脚本会自动保存 `auth.json`

## 输出

- `auth.json`

## 依赖文件

- `save_session.py`
- `login_credentials.json`

## 注意事项

- 环境中必须已安装 Playwright 和 Chromium
- 安装命令：
  `python3 -m pip install playwright`
  `python3 -m playwright install chromium`
- 如果 `auth.json` 已失效，需要重新执行本技能
- 验证码需要人工处理，本技能不负责自动识别或自动计算验证码
- 执行时需要本机可正常打开浏览器并完成登录
