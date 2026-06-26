# Skills Auto Manager - Implementation Guide

本文件是 skill 的实现指南，供 AI 执行时使用。

---

## 核心流程

### Phase 1: 检查当前状态

```bash
# 1. 检查已安装 skills
openclaw skills check

# 2. 列出所有 skills
openclaw skills list

# 3. 记录状态
- 总数
- 需要更新的数量
- 需要修复的数量
- 有问题的 skills
```

### Phase 2: 浏览 ClawHub 市场

```bash
# 使用 web_fetch 获取 ClawHub 数据
web_fetch https://clawhub.ai/skills

# 搜索关键词
- quantitative, trading, stock
- data, analysis
- automation, auto
- chart, visualization
- finance, investment

# 解析页面
- 提取 skill 名称和描述
- 获取评分和下载量
- 检查更新频率
- 查看维护者信誉
```

### Phase 3: 智能筛选

基于配置文件 `config.json`：

```javascript
// 评分算法
function scoreSkill(skill, userProfile) {
  let score = 0;

  // 匹配用户关注领域
  if (userProfile.focusAreas.includes(skill.category)) {
    score += priorities[skill.category];
  }

  // 社区指标
  score += skill.rating * 10;
  score += Math.log(skill.downloads + 1);

  // 维护活跃度
  const daysSinceUpdate = (Date.now() - skill.lastUpdated) / 86400000;
  if (daysSinceUpdate < 30) score += 5;
  else if (daysSinceUpdate < 90) score += 2;

  return score;
}

// 排序并取 Top 10
const recommendations = skills
  .map(s => ({ skill: s, score: scoreSkill(s, userProfile) }))
  .sort((a, b) => b.score - a.score)
  .slice(0, maxRecommendations);
```

### Phase 4: 风险评估

```javascript
function assessRisk(skill) {
  const riskFactors = [];

  // 高风险指标
  if (skill.requiresApiKey) riskFactors.push('requires-api-key');
  if (skill.beta || skill.experimental) riskFactors.push('experimental');
  if (skill.financialOperations) riskFactors.push('financial-operations');

  // 低风险指标
  if (skill.official) return 'low';
  if (skill.dependencies.length === 0) return 'low';
  if (skill.rating >= 4.5 && skill.downloads > 1000) return 'low';

  // 中风险
  if (riskFactors.length === 1) return 'medium';

  // 高风险
  return 'high';
}
```

### Phase 5: 安装决策

```javascript
function decideInstall(skill, risk, config) {
  if (risk === 'low' && config.auto_install_low_risk) {
    return 'auto';
  }

  if (risk === 'high' && config.auto_install_high_risk) {
    return 'auto';
  }

  return 'confirm';
}
```

### Phase 6: 执行安装

```bash
# 安装前备份
if (config.backup_before_install) {
  openclaw skills backup
}

# 安装 skill
openclaw skills install <skill-name>

# 记录日志
echo "$(date): Installed <skill-name>" >> skills-auto-install.log
```

### Phase 7: 生成报告

```markdown
# Skills Auto Manager Report - {date}

## 🔍 当前状态
- 已安装: {total}
- 有更新: {updates}
- 需修复: {fixes}

## 📦 推荐安装 (Top {max_recommendations})

### 1. {skill-name} - ⭐⭐⭐⭐⭐
- **分类**: {category}
- **评分**: {rating}/5.0
- **下载**: {downloads}
- **理由**: {reason}
- **风险**: {risk_level}
- **建议**: {recommendation}

## ✅ 已自动安装
{auto_installed_list}

## ⚠️ 等待确认
{confirm_required_list}

## 📋 执行摘要
- 自动安装: {auto_count} 个
- 等待确认: {confirm_count} 个
- 跳过: {skip_count} 个

## 🔧 技术细节
- 执行时间: {duration}
- ClawHub 版本: {version}
- 配置文件: {config_hash}
```

---

## Cron Job 管理

### 创建 Cron Job

```javascript
{
  "name": "skills-auto-manager-weekly",
  "schedule": {
    "kind": "cron",
    "expr": config.settings.frequency_cron,
    "tz": config.settings.timezone
  },
  "payload": {
    "kind": "agentTurn",
    "message": "执行 Skills Auto Manager 每周检查任务",
    "timeoutSeconds": 600
  },
  "delivery": {
    "mode": "announce",
    "channel": "current"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

### Cron Job 命令

```bash
# 列出 cron jobs
openclaw cron list

# 添加 cron job
openclaw cron add skills-auto-manager-weekly --config ... (参考 cron 工具文档)

# 运行 cron job
openclaw cron run skills-auto-manager-weekly

# 更新 cron job
openclaw cron update skills-auto-manager-weekly ...

# 删除 cron job
openclaw cron remove skills-auto-manager-weekly
```

---

## 文件结构

```
skills-auto-manager/
├── SKILL.md                    # 主 skill 文件（已完成）
├── config.json                 # 配置文件（已完成）
├── implementation.md           # 本文件（实现指南）
├── logs/
│   ├── install-2026-04-21.log  # 安装日志
│   └── error-2026-04-21.log    # 错误日志
└── reports/
    └── skills-auto-2026-04-21.md  # 每次检查的报告（自动生成）
```

---

## 错误处理

### 网络错误
- 重试 3 次
- 记录错误日志
- 使用缓存数据继续

### 安装失败
- 记录失败的 skill
- 提供错误详情
- 尝试回滚备份

### ClawHub 不可用
- 使用本地缓存
- 通知用户稍后重试
- 跳过市场浏览

---

## 优化建议

### 性能优化
- 并行检查多个 skills
- 缓存 ClawHub 数据（24小时有效）
- 增量检查（只检查变化的）

### 用户体验
- 提供 skill 分类浏览
- 支持 skill 搜索功能
- 允许用户自定义推荐

### 安全性
- 验证 skill 签名
- 检查恶意代码
- 隔离沙箱安装

---

## 示例执行流程

```
1. 读取 config.json
2. 执行 openclaw skills check
3. 获取 ClawHub 数据（web_fetch）
4. 基于用户画像筛选 skills
5. 评分和排序
6. 风险评估
7. 低风险 skills 自动安装
8. 高风险 skills 请求确认
9. 生成报告到 memory/skills-auto-2026-04-21.md
10. 发送通知到当前会话
```

---

## 维护和更新

### 定期维护
- 每月检查算法有效性
- 根据用户反馈调整评分权重
- 更新风险分类规则

### 版本更新
- 修改 version 字段
- 记录更改日志
- 通知用户新功能

---

## FAQ

### Q: 如何更改检查频率？
A: 修改 config.json 中的 frequency 和 frequency_cron，然后更新 cron job。

### Q: 如何添加新的关注领域？
A: 修改 config.json 中的 user_profile.focusAreas 数组。

### Q: 如何完全禁用自动安装？
A: 设置 config.json 中的 auto_install_low_risk 和 auto_install_high_risk 为 false。

### Q: 如何查看历史报告？
A: 报告保存在 memory/skills-auto-*.md 文件中。

---

## 联系和支持

- Issue: 在 GitHub 上提交问题
- Feature: 请求新功能
- Feedback: 提供使用反馈

---

**Version**: 1.0.0
**Last Updated**: 2026-04-21
