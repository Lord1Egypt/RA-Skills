# 能力分类体系 (Capability Taxonomy)

SkillRouter 使用能力分类来映射任务到技能，而非硬编码技能名称。

---

## 核心原则

1. **能力优先** - 先识别能力需求，再匹配技能
2. **非硬编码** - 不假设本地技能名称是通用的
3. **复用优先** - 优先推荐已安装技能
4. **静默优先** - 只在必要时介入

---

## 能力类别

### 1. search (搜索)
**用途**:
- 网页搜索
- 技术搜索
- 中文内容搜索
- 隐私搜索

**已安装技能**:
- `multi-search-engine` (17 引擎，无需 Key)
- `exa-web-search-free` (AI 优化)
- `tavily-search` (AI 深度搜索)

---

### 2. fetch (抓取)
**用途**:
- 网页内容抓取
- 反爬网站绕过
- 动态内容渲染

**已安装技能**:
- `web_fetch` (基础抓取)
- `scrapling-fetch` (反爬/微信)
- `browser` (交互式)

---

### 3. summarize (总结)
**用途**:
- 文章摘要
- PDF 总结
- YouTube 总结
- 音频总结

**已安装技能**:
- `summarize` (多格式支持)

---

### 4. analyze (分析)
**用途**:
- 数据分析
- 趋势分析
- 模式识别

**已安装技能**:
- `capability-evolver` (自我进化分析)

---

### 5. code (编程)
**用途**:
- 代码编写
- 代码审查
- 代码重构
- 调试

**已安装技能**:
- `git-essentials` (Git 操作)
- `git-workflows` (高级 Git)
- `github` (GitHub API)

---

### 6. automation (自动化)
**用途**:
- 工作流自动化
- 定时任务
- 批量处理

**已安装技能**:
- `automation-workflows` (工作流)
- `mcp-workflow` (MCP 工作流)
- `auto-model-router` (模型路由)

---

### 7. file-management (文件管理)
**用途**:
- 文件分类
- 批量重命名
- 重复文件清理
- 目录同步

**已安装技能**:
- `file-manager` (文件管理)
- `translate-cli` (翻译)

---

### 8. monitoring (监控)
**用途**:
- 系统资源监控
- 性能监控
- 健康检查

**已安装技能**:
- `system-resource-monitor` (系统监控)

---

### 9. security (安全)
**用途**:
- 安全审计
- 技能审查
- 风险评估

**已安装技能**:
- `security-auditor` (安全审计)
- `skill-vetter` (技能审查)
- `credential-manager` (凭证管理)

---

### 10. knowledge (知识管理)
**用途**:
- 本地 RAG
- 知识库查询
- 文档检索

**已安装技能**:
- `local-file-rag-basic` (本地 RAG)
- `find` (查找)

---

### 11. agent (Agent 协作)
**用途**:
- 多 Agent 协作
- 自我进化
- 自动化 Agent

**已安装技能**:
- `agent-autopilot` (自动 Agent)
- `capability-evolver` (自我进化)
- `adaptive-reasoning` (自适应推理)

---

### 12. weather (天气)
**用途**:
- 当前天气
- 天气预报

**已安装技能**:
- `weather` (天气预报)

---

### 13. skill-management (技能管理)
**用途**:
- 技能发现
- 技能安装
- 技能升级

**已安装技能**:
- `find-skills` (技能发现)

---

### 14. humanize (文本优化)
**用途**:
- AI 文本人性化
- 去除 AI 痕迹
- 文风优化

**已安装技能**:
- `humanizer` (文本人性化)

---

### 15. evomap (EvoMap 生态)
**用途**:
- Capsule 发布
- 任务参与
- 积分管理

**已安装技能**:
- `evomap-tools` (EvoMap 工具)

---

### 16. openclaw-ops (OpenClaw 运维)
**用途**:
- OpenClaw 优化
- 配置管理
- 性能优化

**已安装技能**:
- `openclaw-agent-optimize` (优化)

---

### 17. translate (翻译)
**用途**:
- 文本翻译
- 文件翻译
- 批量翻译

**已安装技能**:
- `translate-cli` (翻译 CLI)

---

### 18. other (其他)
**用途**:
- 未分类任务
- 特殊需求

**已安装技能**:
- `airpoint` (macOS 专用)
- `clawdstrike-test` (测试)
- 其他未分类技能

---

## 重要规则

### 1. 能力名称是内部概念
这些能力名称是内部路由概念，不是用户-facing 的术语。

**推荐输出**:
- "这是搜索任务，使用 `multi-search-engine`"
- "这是反爬抓取任务，使用 `scrapling-fetch`"

**避免输出**:
- "这是 fetch.capability.anti_bot 任务"
- 暴露能力分类体系 (除非用户明确要求)

---

### 2. 优先复用已安装技能

**决策顺序**:
1. 已安装的强匹配技能
2. 已安装的技能组合
3. 已安装的通用后备
4. 建议发现/安装新技能

---

### 3. 静默优先

**何时介入**:
- 用户明确询问是否有相关技能
- 用户询问应该使用哪个技能
- 多个技能可能适用，需要选择
- 已安装技能容易被遗忘但能明显减少工作

**何时静默**:
- 默认触发路径已足够
- 任务简单明确
- 技能选择不是有意义的决策

---

## 本地覆盖

本地环境可维护偏好覆盖：

```yaml
# 本地偏好示例
preferences:
  search: multi-search-engine  # 搜索首选
  fetch:
    normal: web_fetch          # 普通网页
    anti_bot: scrapling-fetch  # 反爬网站
  summarize: summarize         # 总结
```

---

*参考：skillhub skill-router capability-taxonomy.md*  
*最后更新：2026-03-17*
