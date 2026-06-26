# 解决顺序 (Resolution Order)

当多个已安装技能可能适用时的决策顺序。

---

## 核心原则

**SkillRouter 存在是为了改善已安装技能的复用，而非扩展技能集。**

---

## 决策顺序

### 1. 已安装的强匹配 (优先)

检查是否有已安装技能能强匹配当前任务。

**强匹配标准**:
- 技能描述明确覆盖任务
- 能力标签匹配需求
- 历史成功率 >80%

**示例**:
- 中文搜索 → `multi-search-engine`
- 微信文章 → `scrapling-fetch`
- GitHub 操作 → `github`

---

### 2. 已安装的技能组合

如果单个技能不足，考虑技能组合。

**示例**:
- 搜索 + 总结 → `multi-search-engine` + `summarize`
- 抓取 + 分析 → `scrapling-fetch` + 分析技能

---

### 3. 已安装的通用后备

如果无专门技能，使用通用技能。

**示例**:
- 无专门搜索 → `multi-search-engine` (多引擎)
- 无专门抓取 → `web_fetch` (基础)

---

### 4. 发现/安装新技能 (最后)

只有已安装技能明显不足时，才建议发现/安装。

**触发条件**:
- 无已安装技能覆盖任务
- 通用技能失败率高
- 任务频繁出现，值得专门技能

---

## 本地偏好覆盖

本地环境可维护偏好：

```yaml
# 本地偏好示例
local_preferences:
  # 类别 → 首选技能
  search: multi-search-engine
  fetch:
    normal: web_fetch
    anti_bot: scrapling-fetch
  summarize: summarize
  
  # 特定场景覆盖
  scenarios:
    wechat_article: scrapling-fetch
    technical_search: exa-web-search-free
    chinese_content: multi-search-engine
```

---

## 能力→技能映射

| 能力需求 | 首选技能 | 备选技能 |
|---------|---------|---------|
| search.chinese | multi-search-engine | - |
| search.technical | exa-web-search-free | multi-search-engine |
| fetch.normal | web_fetch | scrapling-fetch |
| fetch.anti_bot | scrapling-fetch | browser |
| summarize.text | summarize | - |
| summarize.pdf | summarize | - |
| code.git | git-essentials | github |
| code.github | github | git-workflows |
| automation.workflow | automation-workflows | mcp-workflow |
| monitoring.system | system-resource-monitor | - |
| security.audit | security-auditor | skill-vetter |

---

## 重要规则

### 1. 不假装能力存在

如果无强匹配技能，不假装存在。

**良好**: "我没看到已安装的强匹配技能，先走 `find-skills`。"
**不良**: "我用 `xxx` 帮你..." (实际不匹配)

---

### 2. 本地偏好仅用于打破平局

本地偏好是偏好，不是通用假设。

**正确用法**:
- 两个技能同等匹配 → 使用本地偏好
- 一个技能明显更优 → 使用更优的

**错误用法**:
- 忽略明显更优的技能
- 假设本地偏好是通用真理

---

### 3. 公共路由基于能力

公共路由逻辑应基于能力，而非硬编码技能名称。

**正确**: "这是搜索任务，使用搜索类技能"
**错误**: "这是 multi-search-engine 任务"

---

*参考：skillhub skill-router resolution-order.md*  
*最后更新：2026-03-17*
