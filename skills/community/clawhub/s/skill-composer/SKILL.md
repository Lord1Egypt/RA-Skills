---
name: skill-composer
description: 编排多个OpenClaw技能成自动化工作流，一次命令完成复杂任务。
homepage: https://github.com/utopiabenben/ai-skills
version: 1.0.0
# 首次发布时间：2026-03-16
# 作者：小叮当（智脑）
# 许可证：MIT
---

# Skill Composer - 技能组合器

把多个OpenClaw技能串联成自动化工作流，一个命令完成多步操作！

## 为什么需要？

单个技能只能解决一步问题。真实场景往往需要多步：
- **视频处理**：整理 → 提取字幕 → 发布到公众号
- **内容创作**：搜索素材 → 总结 → 多平台裁剪 → 发布
- **数据流程**：下载数据 → 分析 → 生成图表 → 插入报告

Skill Composer 让你用 YAML 定义工作流，一键执行！

## 快速开始

### 1. 创建工作流文件

创建 `workflow.yaml`：

```yaml
name: "示例：视频处理流程"
steps:
  - name: "整理视频"
    skill: video-organizer
    args:
      - --input
      - /path/to/videos
      - --output
      - /tmp/organized
    output: organized

  - name: "生成字幕"
    skill: auto-subtitle
    args:
      - --input
      - "{{organized}}"
      - --output
      - /tmp/subtitles
    output: subtitles

  - name: "发布到公众号"
    skill: social-publisher
    args:
      - --input
      - "{{subtitles}}"
      - --platform
      - wechat
```

### 2. 运行工作流

```bash
python3 {baseDir}/scripts/composer.py run workflow.yaml
```

### 3. 预览（不实际执行）

```bash
python3 {baseDir}/scripts/composer.py preview workflow.yaml
```

## 工作流语法

### 结构
- `name`: 工作流名称（可选）
- `steps`: 步骤列表
- 每个 step 包含：
  - `name`: 步骤名称（可选，用于日志）
  - `skill`: 要调用的技能名称
  - `args`: 参数列表（字符串数组）
  - `output`: 输出引用名（用于后续步骤引用）
  - `if`: 条件表达式（可选）

### 变量插值
使用 `{{变量名}}` 引用前一步的输出目录/文件。

示例：
```yaml
args:
  - --input
  - "{{organized}}"  # 引用名为 'organized' 的前一步输出
```

### 条件执行
```yaml
- name: "只在有错误时执行"
  skill: error-notifier
  if: "{{previous_step.status}} == 'failed'"
```

## 命令行接口

```bash
# 运行工作流
python3 {baseDir}/scripts/composer.py run <workflow.yaml>

# 预览
python3 {baseDir}/scripts/composer.py preview <workflow.yaml>

# 验证语法
python3 {baseDir}/scripts/composer.py validate <workflow.yaml>

# 列出可用示例
python3 {baseDir}/scripts/composer.py examples
```

## 示例工作流

### 示例1：内容创作流程
```yaml
name: "公众号文章创作"
steps:
  - skill: content-researcher
    args: ["--topic", "AI技能开发", "--count", "10"]
    output: research

  - skill: ai-content-tailor
    args: ["--input", "{{research}}", "--platform", "wechat"]
    output: article

  - skill: wechat-formatter
    args: ["--input", "{{article}}", "--output", "./final.md"]
```

### 示例2：数据仪表板生成
```yaml
name: "每周股票报告"
steps:
  - skill: tushare-finance
    args: ["--get", "daily", "--code", "000001.SZ", "--start", "2025-01-01"]
    output: raw_data

  - skill: data-chart-tool
    args: ["--input", "{{raw_data}}", "--type", "line", "--output", "chart.png"]
    output: chart

  - skill: social-publisher
    args: ["--input", "{{chart}}", "--template", "weekly-report"]
```

## 错误处理

- 默认：任何步骤失败则停止整个工作流
- 可配置：`continue-on-error: true` 在 workflow 级别
- 每个步骤状态可用：`{{step_name.status}}`（success/failed）

## 限制

- 当前仅支持串行步骤（下一步依赖前一步完成）
- 不支持并行执行（未来版本）
- 步骤间传递的是文件路径，不是内容

## 与现有技能配合

Skill Composer 不重复造轮子，它是指挥官：
- 复用所有已安装的技能
- 专注于步骤编排
- 让单个技能的价值加倍

**示例技能组合**：
- `video-organizer` + `auto-subtitle` + `social-publisher` → 完整视频发布流水线
- `content-researcher` + `ai-content-tailor` + `wechat-formatter` → 内容生产流水线
- `data-chart-tool` + `social-publisher` → 数据报告自动化

## 技术实现

- Python 3 + PyYAML
- 调用 OpenClaw exec 工具运行每个技能
- 自动处理依赖顺序
- 详细日志输出

## 开发状态

- [ ] 核心 YAML 解析
- [ ] 步骤顺序执行
- [ ] 变量插值 {{output}}
- [ ] 错误处理和状态跟踪
- [ ] 示例工作流
- [ ] 单元测试
- [ ] skill-creator 验证
- [ ] clawhub 发布

## 待办

未来增强：
- [ ] 并行步骤支持（无依赖的步骤可以同时执行）
- [ ] 可视化工作流编辑器
- [ ] 工作flow模板库
- [ ] 步骤结果缓存（避免重复执行）
- [ ] 更好的错误恢复机制

---

## 📞 支持

- GitHub Issues: https://github.com/utopiabenben/ai-skills/issues
- 作品集网站: https://utopiabenben.github.io/ai-skills/