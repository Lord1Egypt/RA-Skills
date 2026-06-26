# TKSeller - 自动带货

AI 自动带货工具。装上 → 登录 → 开始带货，零配置。

## 安装

```bash
clawhub install tkseller
```

## 配置 Discord

TKSeller 通过 Discord 跟你交互（发审核卡片、按钮操作等）。

1. 按教程配置 Discord：https://docs.openclaw.ai/channels/discord
2. 配置完重启网关：`openclaw gateway restart`

## 使用

### 1. 启动

在 Discord 或 webchat 里输入：

- `/tkseller` — Discord 斜杠命令
- `带货` — 纯文字触发
- `/tkseller url:https://...` — 指定视频

### 2. 首次登录

按提示输入：

```
登录 你的用户名 你的密码
```

例如：`登录 beeos 123456`

登录一次后自动保存，不需要重复登录。

### 3. 选择数字人

登录后会弹出数字人选择卡片，点按钮选一个形象（或自定义）。

### 4. 开始带货

选完数字人后，系统自动推荐热门视频或分析你指定的视频，发审核卡片给你：

- ✅ 做 — 开始生成视频
- ⏭️ 换一个 — 跳过，推荐下一个
- 🔄 换商品 — 重新匹配商品

后续流程（分镜确认 → 视频生成 → 发布）都通过 Discord 按钮操作。

## 常见问题

**Q: 提示"还没有配置 Discord 渠道"**
A: 按上面的教程配置 Discord，配完重启网关。

**Q: 提示"Discord 已配置但连接失败"**
A: 检查 Bot Token 是否正确、Bot 是否已加入服务器、网络是否正常。确认后 `openclaw gateway restart`。

**Q: `/tkseller` 命令在 Discord 里看不到**
A: 先发一次纯文字 `带货` 触发自动注册，之后就能用 `/tkseller` 了。

**Q: 登录失败**
A: 确认格式：`登录 用户名 密码`（三个词，空格隔开）。
