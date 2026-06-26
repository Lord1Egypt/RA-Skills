# Requirements - wechat-lead-generation 技能

## 技能依赖

### 必备 OpenClaw 技能
- `wechat-md-publish` 或 `bb-browser-openclaw` - 微信数据抓取
- `agentmemory` (插件) - 客户画像存储
- `trendradar` (可选) - 行业热点关联分析

### 系统要求
- Python 3.10+
- Node.js 18+
- 微信 cookie 或登录态（用于抓取数据）

## 安装清单

```bash
# 1. 确保技能目录可执行
chmod +x ~/.openclaw/workspace/.agents/skills/wechat-lead-generation/bin/run

# 2. 在 openclaw.json 中启用技能
# 添加 "wechat-lead-generation" 到 skills.enabled 列表

# 3. 配置微信抓取凭据（可选，用于真实抓取）
export WECHAT_COOKIE="your_wechat_cookie_here"

# 4. 重启网关
openclaw gateway restart
```

## 权限要求

该技能需要以下工具权限：
- `wechat-md-publish` 相关工具（抓取微信内容）
- `memory_save` - 存储客户画像
- `ctx_execute` - 运行分析引擎

## 配置项

```json
{
  "plugins": {
    "entries": {
      "wechat-lead-generation": {
        "enabled": true,
        "config": {
          "default_source": "groups",
          "default_days_back": 7,
          "auto_reply_threshold": 70,
          "max_keywords": 10,
          "enable_memory": true
        }
      }
    }
  }
}
```

## 安全注意事项

⚠️ **微信自动化风险**：
- 频繁抓取可能导致账号被封
- 建议使用小号或测试账号
- 设置合理的时间间隔（≥ 30 秒）
- 优先使用半自动模式（`--auto_reply false`）

## 成本预估

- **本地运行**：免费（仅计算电费）
- **LLM 分析**：如果集成 AI 分析，约 10-20k tokens / 100 条消息
- **存储**：agentmemory 存储按量计费（通常免费额度足够）

## 测试建议

首次使用请先用模拟模式测试：

```bash
# 测试命令（使用模拟数据）
.agents/skills/wechat-lead-generation/bin/run \
  --source groups \
  --days_back 1 \
  --keywords "AI" \
  --auto_reply false

# 查看生成的报告
cat output/wechat-lead-generation/leads-report-*.md
```

## Roadmap

- [ ] 真实微信抓取（wechat-md-publish 集成）
- [ ] AI 深度分析（使用 LLM 生成客户画像）
- [ ] 多语言支持
- [ ] 可视化仪表盘
- [ ] CRM 导出功能
