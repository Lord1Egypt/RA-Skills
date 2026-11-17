# 来源分歧调查报告（2026-07-25）

> 审计发现 2 项 CRITICAL 级别 SOURCE_DIVERGENCE，以下为逐项分析和处理记录。

---

## 1. computer-use

**来源类型**：`codex_plugin_cache`（不可编辑）
**当前版本**：26.721.41059

### 分歧详情

| 来源 | 路径 | description |
|---|---|---|
| 插件缓存（当前使用） | `D:\codex\plugins\cache\openai-bundled\computer-use\26.721.41059\skills\computer-use\SKILL.md` | `Windows 操作 → 控制桌面应用·执行界面任务`（中文） |
| 市场打包版 | `D:\codex\.tmp\bundled-marketplaces\openai-bundled\plugins\computer-use\skills\computer-use\SKILL.md` | `Control Windows apps from ChatGPT`（英文） |
| 旧缓存版本 | `D:\codex\.tmp\skill-visible-verify-20260723\plugins\cache\openai-bundled\computer-use\26.715.72359\skills\computer-use\SKILL.md` | 同当前缓存（中文） |

### 分歧性质

插件缓存已被本地化为中文，而市场打包版为原始英文。内容是汉化 vs 原版的差异，**不是同一来源的静默内容篡改**。

### 处理方案

- 该技能来自 `openai-bundled` 插件 cache，**不可编辑**
- 用户 UI 实际使用的是插件缓存版本（中文），如无异常则不需干预
- 若需要英文原版，需通过 Codex 插件管理刷新或重新安装该插件
- **建议**：下次插件升级时比对是否仍然存在差异，或联系插件发布方确认本地化策略

---

## 2. visualize

**来源类型**：`codex_plugin_cache`（不可编辑）
**当前版本**：1.0.15

### 分歧详情

| 来源 | 路径 | description |
|---|---|---|
| 插件缓存（当前使用） | `D:\codex\plugins\cache\openai-bundled\visualize\1.0.15\skills\visualize\SKILL.md` | `可视化创建 → 图表·交互工具·模拟器·数据探索`（中文） |
| 市场打包版 | `D:\codex\.tmp\bundled-marketplaces\openai-bundled\plugins\visualize\skills\visualize\SKILL.md` | `Create visualizations and interactive tools directly in conversation...`（英文） |
| 旧缓存版本 | `D:\codex\.tmp\skill-visible-verify-20260723\plugins\cache\openai-bundled\visualize\1.0.14\skills\visualize\SKILL.md` | 同当前缓存（中文） |

### 分歧性质

同 computer-use，插件 cache 被本地化为中文，市场版为英文。**非恶意篡改**，是正常的本地化版本差异。

### 处理方案

- 插件 cache **不可编辑**
- 当前使用的 1.0.15 中文版可正常使用
- 如希望改用英文版，可通过 Codex 插件管理操作

---

## 小结

两项 SOURCE_DIVERGENCE **均为插件本地化缓存与市场版的正常差异，非安全或数据一致性问题**。当前 UI 使用的中文版无异常，标记为 `observed` 关闭，等待下次插件升级时复查。
