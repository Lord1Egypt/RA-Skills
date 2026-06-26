# X 运营辅助 Skill v4.2

完整的 X/Twitter 运营辅助方案。默认走 Browser Relay + 人工确认，不安装后台持久任务。

Browser Relay 仓库：
`https://github.com/jasonCodeSpace/browser-relay`

## 特性

- ✅ 完整 Onboarding 流程
- ✅ Persona 学习（抓取100条推文）
- ✅ 自然节奏与确认（先建议，后执行）
- ✅ 记忆系统（评论历史、用户事实、避免矛盾）
- ✅ 手动提醒模板（不改 crontab）
- ✅ 智能评论生成（语言匹配、风格应用）
- ✅ Browser Relay 集成（使用自有运行时）

## 快速开始

### 1. 准备 Browser Relay 运行时

```bash
npx browser-relay-cli version
npx browser-relay-cli extension-path
npx browser-relay-cli relay-start
```

如果需要查看 Browser Relay 源码或本地开发，请使用仓库：
`https://github.com/jasonCodeSpace/browser-relay`

### 2. 首次运行

```
用户: 刷推
Bot: 开始 Onboarding...
```

### 3. 后续使用

```
用户: 刷推半小时
Bot: 读取配置... 先给出互动建议，确认后执行...
```

## 文档

| 文档 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | 主入口 |
| [docs/onboarding.md](docs/onboarding.md) | Onboarding 流程 |
| [docs/human-behavior.md](docs/human-behavior.md) | 自然节奏与确认 |
| [docs/memory-system.md](docs/memory-system.md) | 记忆系统 |
| [docs/cron-jobs.md](docs/cron-jobs.md) | 手动提醒与维护 |
| [docs/comment-generation.md](docs/comment-generation.md) | 评论生成 |

## 目录结构

```
x-engagement/
├── SKILL.md                    # 主入口
├── README.md                   # 说明文档
├── docs/                       # 详细文档
│   ├── onboarding.md
│   ├── human-behavior.md
│   ├── memory-system.md
│   ├── cron-jobs.md
│   └── comment-generation.md
├── templates/                  # 模板文件
│   ├── persona.md
│   ├── config.json
│   └── daily-log.md
└── scripts/                    # 脚本
    ├── setup-cron.sh
    ├── check-cron.sh
    └── cleanup-memory.sh
```

## 核心功能

### 1. Onboarding

首次运行自动引导：
- 浏览器连接 + 登录检查
- 选择 Persona（自己或其他账号）
- 学习 Persona（抓取100条）
- 配置刷推习惯

### 2. 自然节奏与确认

保留自然阅读节奏，但不做规避检测设计：
- 评论前给出候选内容
- 发送前必须再次确认
- 点赞 / 关注也建议确认
- 保留频率建议

### 3. 记忆系统

三层记忆：
- 评论历史（避免重复、矛盾）
- 用户事实（记住用户说过的话）
- 每日日志（活动记录）

### 4. 手动维护

- 手动热点总结
- 手动记忆清理预览
- 手动记忆清理执行（`--apply`）
- 手动提醒模板生成

默认不直接安装 cron，也不修改用户 `crontab`。

### 5. 智能评论

- 语言匹配（中文/英文）
- Persona 风格应用
- 历史检查（避免矛盾）
- 用户事实检查

## 使用示例

### 示例 1：正常评论

```
推文: "今天市场大涨！"
评论: "确实，趋势起来了。"
```

### 示例 2：避免矛盾

```
用户昨天说: "出去吃饭了"
推文: "最近都在家做饭"
评论: "做饭不错，偶尔出去换换口味也好"（避免说"你都在家"）
```

### 示例 3：跳过政治

```
推文: "特朗普最新政策"
结果: 跳过（政治内容）
```

## 配置

### 刷推习惯

```json
{
  "forYou": {
    "followNewAccounts": true,
    "followCriteria": ["views_1m+", "crypto", "ai"]
  },
  "following": {
    "commentWithin": "2h",
    "avoidTopics": ["politics", "war"]
  }
}
```

### 频率限制

| 操作 | 每小时上限 |
|------|-----------|
| 关注 | 10 |
| 点赞 | 30 |
| 评论 | 10 |

## 故障排除

### 浏览器连接失败

```
1. 运行 `npx browser-relay-cli relay-start`
2. 在 Chrome 加载 Browser Relay 扩展
3. 运行 `npx browser-relay-cli status`
```

### 不希望自动发送评论

```
1. 保持默认确认流
2. 先生成候选评论
3. 用户确认后再点发送
```

### 记忆系统不工作

```
1. 检查目录是否存在: memory/daily/hotspots/
2. 检查文件权限
3. 运行: ./scripts/check-cron.sh
```

## 更新日志

### v4.2.0-local (2026-04-14)
- 移除自动 cron / crontab 修改
- 清理脚本改成默认 dry-run
- Browser Relay 替代 OpenClaw
- 评论改成先建议后确认

### v4.0.0 (2026-03-02)
- 结构化设计
- 记忆系统（评论历史、用户事实）
- 定时任务（每日热点）
- 人类行为模拟规范
- 智能评论生成

### v3.0.0 (2026-03-01)
- 完整 Onboarding 流程
- Persona 学习

### v2.0.0 (2026-02-28)
- 人类行为模拟
- 频率限制

### v1.0.0 (2026-02-27)
- 初始版本

## 许可证

MIT

---

*版本: 4.0.0*
*更新: 2026-03-02*
