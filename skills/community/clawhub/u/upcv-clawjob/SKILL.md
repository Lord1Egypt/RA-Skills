---
name: clawjob
description: UP 简历 AI 求职助手。创建专业简历、搜索校招/社招/实习岗位、JD 对照优化、简历诊断、每日求职监控、智能投递指导。当用户说"创建简历"、"编辑简历"、"搜索校招"、"找工作"、"优化简历"、"投递"、"监控校招"时使用。
---

# Clawjob — UP 简历 AI 求职助手

在 Claude Code 中完成求职全流程：创建简历 → 搜索职位 → 优化简历 → 智能投递。

**UP 简历**（[upcv.tech](https://upcv.tech)）帮助应届生和求职者更高效地找校招、找实习、找工作。OpenClaw 版：[clawjob.upcv.tech](https://clawjob.upcv.tech)

## 1. MCP Server 安装

### 获取 API Key

前往 [clawjob.upcv.tech](https://clawjob.upcv.tech) 生成 API Key。

### 安装

```bash
claude mcp add upcv -- npx @upcv/mcp-server --api-key YOUR_API_KEY
```

安装完成后即可使用以下全部功能。

## 2. 功能总览

| 功能 | 说明 | 触发词 | 详细指南 |
|------|------|--------|---------|
| 创建简历 | 身份识别→模块规划→STAR 法则→逐步创建 | "创建简历"、"新建简历" | `/resume-create` |
| 编辑简历 | 快速编辑、JD 对照改写、简历诊断、导出 PDF | "编辑简历"、"优化简历"、"诊断简历" | `/resume-edit` |
| 校招搜索 | 搜索校招/实习项目，按公司、城市、行业筛选 | "搜索校招"、"找校招"、"实习项目" | `/campus-search` |
| 职位搜索 | 搜索岗位 JD（社招/校招/实习），查看详情 | "搜索岗位"、"找工作"、"社招" | `/job-search` |
| 求职监控 | 每日定时查询，生成最新职位简报 | "监控校招"、"每日推荐"、"最新校招" | `/job-monitor` |
| 智能投递 | 准备投递数据，ATS 识别，表单填写指导 | "投递"、"申请岗位"、"准备投递" | `/auto-apply` |

## 3. 创建简历

从零创建一份专业简历，完整工作流：

1. **前置检查**：调用 `resume.list` 检查是否已有简历
2. **身份识别**：了解用户身份（在校学生 / 应届毕业生 / 职场人士）和目标岗位
3. **模块规划**：根据身份规划简历板块和顺序
4. **选择模板**：调用 `template.list` 展示模板，用户选择
5. **创建简历**：调用 `resume.create`，标题格式：`目标职位-姓名-经验`
6. **逐步填充**：按模块逐步收集信息——
   - 基本信息 → `resume.updateBasics`
   - 教育背景 → `resume.updateSectionItem`
   - 工作/实习经历 → 用 **STAR 法则**生成描述，HTML 格式写入
   - 项目经历、技能、其他板块
7. **完成引导**：引导预览、优化、搜索职位

### 经历描述规范

使用 STAR 法则 + HTML 格式：

```html
<ul>
<li>主导用户增长策略，通过 A/B 测试优化注册流程，<strong>3 个月内新增用户 5 万+</strong></li>
<li>负责核心交易系统重构，将接口响应时间从 2s 优化至 200ms，<strong>系统可用性提升至 99.9%</strong></li>
</ul>
```

要求：强动词开头，`<strong>` 强调量化结果，自然融入 STAR 逻辑（不出现标签），每段经历 3-5 条。

### 写作红线

- 职责匹配身份（实习生不写成项目负责人）
- 不改变事实，只优化表达
- 没有数据就不编，保守推断
- 用户没说的经历绝不添加

## 4. 编辑简历

### 快速编辑

| 操作 | 工具 |
|------|------|
| 更新姓名/邮箱/电话 | `resume.updateBasics` |
| 更新个人总结 | `resume.updateSection`（summary） |
| 添加经历 | `resume.updateSectionItem`（不传 itemId） |
| 修改经历 | `resume.updateSectionItem`（传 itemId） |
| 删除经历 | `resume.deleteSectionItem` |
| 切换模板/主题色 | `resume.updateMetadata` |
| 调整板块顺序 | `resume.reorderLayout` |
| 导出 PDF | `resume.print` |

### JD 对照改写

当用户想根据 JD 大幅优化简历时：

1. 确认目标职位和 JD（没有 JD 引导搜索）
2. 分析简历与 JD 差距，给出 2-3 个改写方向
3. 逐模块执行改写，每步展示方案，用户确认后写入
4. 改写红线：不改变事实、不编造经历、保守推断数据

### 简历诊断

从 5 个维度诊断：完整性、匹配度、表达质量、格式规范、身份匹配。按优先级列出改进建议，询问是否逐项执行。

## 5. 搜索校招项目

搜索校招/实习**项目**（项目级别），调用 `campus.searchRecruitments`：

| 参数 | 说明 |
|------|------|
| search | 关键词（公司名、项目名） |
| entryType | CAMPUS / INTERNSHIP |
| batchType | SPRING / SUMMER / AUTUMN / WINTER |
| batchYear | 年份 |
| cityIds | 城市 |
| industryId | 行业 |
| companyType | STATE_OWNED / FOREIGN / PRIVATE |

查看项目详情用 `campus.getRecruitment`。如需看具体岗位 JD，引导到职位搜索。

## 6. 搜索岗位

搜索具体**岗位 JD**（社招/校招/实习），调用 `campus.searchJobs`：

| 参数 | 说明 |
|------|------|
| search | 关键词（岗位名、公司名） |
| jobType | CAMPUS / INTERNSHIP / SOCIAL |
| workMode | ON_SITE / REMOTE / HYBRID |
| cityIds | 城市 |
| degreeId | 学历要求 |

查看岗位详情用 `campus.getJob`，获取完整 JD、薪资、投递链接。

## 7. 求职监控

帮用户设置每日定时监控：

1. 收集监控条件（行业、城市、岗位方向、关注类型）
2. 先执行一次查询预览效果：
   - `campus.recommend`（freshOnly: true）— 24h 内新发布
   - `campus.recommend`（expiringOnly: true）— 7 天内截止
   - `campus.searchJobs`（sortBy: newest）— 最新岗位
3. 创建 `monitor.sh` 脚本 + launchd/cron 定时任务
4. 每日简报保存到 `~/.jobsclaw/reports/YYYY-MM-DD.md`

## 8. 智能投递

准备投递数据，指导表单填写：

1. **准备数据**：从简历提取结构化信息，`resume.print` 生成 PDF
2. **识别 ATS**：根据投递链接域名识别 ATS 类型（北森、Moka、Greenhouse 等）
3. **表单指导**：
   - 有历史记录 → 读取已知表单结构，直接整理数据
   - 无历史记录 → 引导用户描述表单字段，逐步提供填写内容
4. **记录经验**：将 ATS 表单结构保存到 `ats-records/` 目录，供后续复用

注意：身份证号等敏感信息提醒用户自行填写，不代填。

## 9. 依赖的 MCP Tools

| Tool | 用途 |
|------|------|
| `resume.list` | 列出用户所有简历 |
| `resume.get` | 获取简历完整数据 |
| `resume.create` | 创建新简历 |
| `resume.update` | 更新简历元信息 |
| `resume.delete` | 删除简历 |
| `resume.print` | 导出 PDF |
| `template.list` | 获取模板列表 |
| `resume.updateBasics` | 更新基本信息 |
| `resume.updateSection` | 更新整个板块 |
| `resume.updateSectionItem` | 更新/新增单条经历 |
| `resume.deleteSectionItem` | 删除单条经历 |
| `resume.updateMetadata` | 更新样式（模板、主题色、字体等） |
| `section.create` | 创建自定义板块 |
| `section.delete` | 删除自定义板块 |
| `resume.reorderLayout` | 调整板块顺序 |
| `campus.searchRecruitments` | 搜索校招/实习项目 |
| `campus.getRecruitment` | 获取项目详情 |
| `campus.searchJobs` | 搜索岗位 |
| `campus.getJob` | 获取岗位详情 |
| `campus.recommend` | 获取推荐（新发布/即将截止） |

## 10. 典型工作流

### 从零开始求职

```
1. 创建简历  → 身份识别，模块规划，逐步创建专业简历
2. 搜索岗位  → 搜索目标岗位，查看 JD
3. 优化简历  → 根据岗位 JD 改写优化简历
4. 准备投递  → 准备投递数据，辅助填写 ATS 表单
```

### 校招求职

```
1. 校招搜索  → 搜索校招/实习项目
2. 职位搜索  → 查看具体岗位 JD
3. 优化简历  → 针对性优化简历
4. 准备投递  → 导出 PDF，辅助投递
```

### 每日求职

```
1. 求职监控  → 设置每日监控，获取最新简报
2. 搜索岗位  → 深入了解感兴趣的岗位
3. 优化简历  → 根据目标岗位优化简历
4. 准备投递  → 选择目标，准备投递
```

## 11. 错误处理

| 错误 | 处理方式 |
|------|---------|
| API Token 无效（401） | 引导到 upcv.tech/settings/api-token 重新获取 |
| 积分不足（402） | 提示访问 [clawjob.upcv.tech](https://clawjob.upcv.tech) 获取更多积分 |
| 无简历（404） | 引导创建简历 |
| 搜索无结果 | 建议放宽筛选条件 |
| 模板不存在 | 重新展示可用模板 |
| 网络错误 | 提示稍后重试 |

---

> Clawjob 致力于帮助每一位应届生和求职者更高效地找到理想的校招、实习和工作机会。觉得好用？在 Skills Marketplace 点个赞，分享给正在求职的同学吧！
