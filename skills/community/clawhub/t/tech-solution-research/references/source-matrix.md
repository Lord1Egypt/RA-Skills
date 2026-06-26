# Source Matrix — 数据源矩阵

## 目的

给 `tech-solution-research` 一个可执行的数据源路由表，避免再次退化成单一 `web_search`。

---

## 默认路由矩阵

| 目标来源 | 第一优先 | 第二优先 | 第三优先 | 备注 |
|---|---|---|---|---|
| **X/Twitter 最新原始流** | `feedgrab` | `agent-browser/browser+x_state` | `community-discourse` | 默认不用 `xurl`；如平台原生失败必须记录降级原因 |
| **X/Twitter 过去 30 天趋势** | `last30days` | `x-hot-topics-daily` | `feedgrab` | 趋势研究优先，不等于实时原始流 |
| **X/Twitter 日热点/日报** | `x-hot-topics-daily` | `last30days` | `feedgrab` | 适合持续监控 |
| **小红书搜索/详情/互动** | `xiaohongshu` | `feedgrab` | `community-discourse` | 垂直 skill 优先 |
| **GitHub 项目健康度** | GitHub/gh/API | `community-discourse` | `official-docs` | stars 只是辅助，重点看 release/issue/commit |
| **ClawHub 技能生态** | registry / installed skills / metadata | `community-discourse` | `official-docs` | 关注安装量、权限、作者、最近更新 |
| **Moltbook 内容资产** | `moltbook-global` | `internal-assets` | `community-discourse` | 作为平台/内部内容资产 |
| **官方功能声明** | `official-docs` | GitHub release / changelog | `community-discourse` | 文档过时要标注 |
| **真实可用性** | `runtime-test` | GitHub issues | `community-discourse` | 实测优先级最高 |

---

## 使用规则

### 1. 平台原生优先
凡是平台相关调研，先尝试平台原生数据源；只有失败时才允许降级。

### 2. 降级必须留痕
当第一优先不可用时，报告中必须写：
- 不可用原因
- 实际用了什么替代源
- 该替代源是否属于一手数据

### 3. 社区讨论不能替代原始流
`community-discourse` 只能解释“别人怎么说”，不能替代原始平台数据。

### 4. 实测优先于口碑
如果 runtime-test 与 community-discourse 冲突，以 runtime-test 为准。

---

## 报告中的建议展示方式

```markdown
### 数据源覆盖
- X/Twitter：feedgrab + last30days（已覆盖）
- 小红书：xiaohongshu（待补核）
- GitHub：gh/API（已覆盖）
- ClawHub：registry + installed skills（已覆盖）
- Moltbook：moltbook-global（待补核）

### 降级记录
- X 原始流：feedgrab 成功，无需降级
- 小红书：本次未触发相关主题，未采集
- Moltbook：本次主题无相关内容，跳过
```

---

## 结论

这份矩阵的作用，不是增加花样，而是**锁死默认数据源优先级**，避免再次回退到“web_search + 总结”的旧模式。
