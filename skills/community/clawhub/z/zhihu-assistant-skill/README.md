# 知乎助手 - OpenClaw Skill

自动抓取知乎热榜、生成回答草稿并推送到飞书审核的 OpenClaw Skill。

## 功能特性

- ⏰ **定时抓取**：每小时自动抓取知乎热榜前10条
- 🧠 **智能生成**：使用 Kimi AI 生成优质回答草稿
- 📋 **审核队列**：推送到飞书，人工确认后手动发布
- 📝 **记忆去重**：自动过滤已回答过的问题
- 📊 **操作日志**：完整记录所有操作

## 安装

```bash
openclaw skills install zhihu-assistant
```

## 配置

安装后需要配置以下参数：

### 1. 知乎 Cookie（必需）

从浏览器开发者工具复制知乎 Cookie：

1. 登录知乎网页版
2. 按 F12 打开开发者工具 → Network
3. 刷新页面，找到任意请求
4. 复制 Request Headers 中的 Cookie

```bash
openclaw config set skills.zhihu-assistant.zhihu_cookie "your_zhihu_cookie_here"
```

### 2. Kimi API Key（必需）

从 [Kimi 开放平台](https://platform.moonshot.cn/) 获取 API Key：

```bash
openclaw config set skills.zhihu-assistant.kimi_api_key "your_api_key_here"
```

### 3. 飞书用户 ID（可选）

用于接收推送通知：

```bash
openclaw config set skills.zhihu-assistant.feishu_user_id "your_feishu_user_id"
```

### 4. 其他配置（可选）

```bash
# 每次抓取数量（默认10）
openclaw config set skills.zhihu-assistant.fetch_limit 10

# 最小热度过滤，单位万（默认10）
openclaw config set skills.zhihu-assistant.min_heat 10
```

## 使用

### 快捷命令

```bash
# 抓取热榜并生成草稿
openclaw zhihu fetch --limit 10

# 查看统计信息
openclaw zhihu stats

# 推送到飞书
openclaw zhihu notify

# 查看操作日志
openclaw zhihu logs

# 拒绝草稿
openclaw zhihu reject --id P20260301...
```

## 定时任务

安装后会自动创建以下定时任务：

| 任务 | 时间 | 功能 |
|------|------|------|
| zhihu-fetch | 每小时 0 分 | 抓取热榜并生成草稿 |
| zhihu-notify | 每小时 5 分 | 推送待审核项到飞书 |

## 注意事项

1. **Cookie 有效期**：知乎 Cookie 会过期，通常 1-3 个月，过期后需要重新获取
2. **API 调用限制**：Kimi API 有速率限制（免费版 20 RPM），请勿频繁调用
3. **内容质量**：AI 生成的内容仅供参考，发布前请人工审核
4. **账号安全**：请勿将 Cookie 和 API Key 提交到代码仓库
5. **合规使用**：遵守知乎社区规范，不要发布违规内容

## License

MIT

## 作者

- GitHub: [@naiveKid](https://github.com/naiveKid)
