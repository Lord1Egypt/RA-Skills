---
name: Wechat Connect
slug: wechat
description: Install OpenClaw's official WeChat plugin and complete account pairing via QR code scan. Triggers when the user says "install WeChat plugin", "connect WeChat", or "WeChat QR code". No command-line interaction required.
author: linyishan
mail: linyishan@qq.com
version: 2.1.0
---

# Wechat Connect

一键安装 OpenClaw 微信插件并完成账号配对，用户全程无需接触命令行。

## 触发方式

- 用户说"安装微信插件"
- 用户说"连接微信"
- 用户说"微信扫码"
- 用户说类似"装一下微信"的表达

## 前置条件

1. OpenClaw 已安装并运行
2. `qrcode` npm 包已安装（workspace 已包含）
3. 微信插件包 `@tencent-weixin/openclaw-weixin` 未安装时，skill 会自动执行以下命令进行安装：
   ```bash
   npx -y @tencent-weixin/openclaw-weixin-cli@latest install
   ```

## 完整流程

```
用户触发
  │
  ├─ ① 检查插件安装状态
  │     查询 openclaw.json plugins.installs
  │     已安装 → 直接进入扫码流程
  │     未安装 → 自动执行安装
  │
  ├─ ② 获取微信登录二维码
  │     调用微信 API:
  │     GET https://ilinkai.weixin.qq.com/ilink/bot/get_bot_qrcode?bot_type=3
  │     提取 qrcode_img_content，用 qrcode 库生成 PNG
  │
  ├─ ③ 生成引导页
  │     生成 HTML：5 步骤横向展示 + 实时状态
  │     第一步至第四步为文字说明，第五步为二维码
  │     步骤：001→002→003→004→[二维码]
  │     每张图下方标注"第一步"~"第五步"
  │
  ├─ ④ 启动本地 HTTP 服务
  │     端口 8765，提供静态文件 + 状态 API
  │     通过 browser 工具打开 http://localhost:8765
  │
  ├─ ⑤ 状态轮询
  │     每 3 秒调用微信 API 检查扫码状态:
  │     GET https://ilinkai.weixin.qq.com/ilink/bot/get_qrcode_status?qrcode=xxx
  │     状态: wait → scaned → confirmed / expired
  │     页面底部实时文字反馈
  │
  ├─ ⑥ 成功弹窗
  │     confirmed 时：灯箱弹出
  │     "🎉 恭喜！微信与 OpenClaw 已经配对成功"
  │     灯箱常驻，不可关闭，为最终状态
  │
  └─ ⑦ 保存账号
        连接成功后：
        - 写入 ~/.openclaw/openclaw-weixin/accounts/{id}.json
        - 更新 ~/.openclaw/openclaw-weixin/accounts.json 索引
        - openclaw config set channels.openclaw-weixin.enabled=true
        - openclaw config set channels.openclaw-weixin.dmPolicy=allowlist
        - openclaw config set channels.openclaw-weixin.allowFrom=[<userId>]
        - Gateway 在后台自动重启（无需手动操作）
        - 灯箱页面保持展示，重启完成后可直接使用微信测试

  expired（过期）：提示重新生成，页面刷新继续
  超时（5分钟）：提示超时，需重新发起
```

## 技术方案

| 步骤 | 技术 |
|------|------|
| 二维码获取 | `fetch` 调用微信 ilink API |
| PNG 生成 | `qrcode` npm 包 |
| HTTP 服务 | Node.js `http` 模块（零依赖） |
| 页面渲染 | 静态 HTML + JavaScript 轮询 |
| 状态同步 | `/tmp/weixin-login-status.json` 进程间通信 |
| 浏览器展示 | `browser` 工具打开页面 |
| 账号保存 | 直接写 `~/.openclaw/openclaw-weixin/accounts/*.json` |
| 配置更新 | `openclaw config set` CLI 命令 |

## 文件结构

```
skills/wechat/
├── SKILL.md              # 本文件
└── scripts/
    └── start.mjs        # 主入口脚本
```

## 依赖

- `qrcode` npm 包（`cd /Users/ethan/.openclaw/workspace && npm install qrcode`）
- `@tencent-weixin/openclaw-weixin` 插件包（通过 `openclaw-weixin-cli` 安装）
- Node.js 18+

## 状态码

| 状态 | 含义 | 页面反馈 |
|------|------|---------|
| `wait` | 等待扫码 | "请使用微信扫描二维码" |
| `scaned` | 已扫码，等待确认 | "已扫码，请在微信中确认登录" |
| `confirmed` | 登录成功 | 灯箱弹出"恭喜！..." |
| `expired` | 二维码过期 | "二维码已过期，请重新生成" |

## 注意事项

- 二维码有效期 **5 分钟**，超时需重新生成
- 灯箱弹出后**不可关闭**，为最终状态
- 账号 token 必须与 `ilink_bot_id` 匹配，否则 session 验证失败
- 若扫码后 session 过期（errcode -14），需重新扫码认证

## 安全说明

⚠️ 安装微信插件时，npm 会显示以下警告（来自插件自身，非 skill 问题）：

```
WARNING: Plugin "openclaw-weixin" contains dangerous code patterns:
Environment variable access combined with network send
```

这是因为插件需要访问环境变量和网络发送能力，属于正常设计。安装完成后警告可忽略，插件正常运行。
