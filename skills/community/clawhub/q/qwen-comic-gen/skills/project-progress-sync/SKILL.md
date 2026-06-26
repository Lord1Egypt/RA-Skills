# Project Progress Sync - 项目进度同步

## 技能描述

自动同步 worklog.txt 和豆包会话内容到项目知识库，刷新项目 workload 和进度状态。

## 触发条件

- **自动触发**：worklog.txt 更新后
- **手动触发**：用户说"同步项目进度"、"刷新项目 workload"
- **定时触发**：每日 18:00（可选）

## 核心能力

1. **worklog 解析** - 提取项目相关工作内容
2. **项目识别** - 匹配项目卡片
3. **进度更新** - 添加本周工作到项目卡片
4. **workload 刷新** - 更新项目工作量统计
5. **状态同步** - 更新项目状态（进行中/已完成/待启动）

## 成功案例（2026-03-06）

### 感知与行动中心项目

**输入：**
```markdown
### 2026-03-06 (周五)
- [完成] 感知与行动中心 v2.1 版本修订
- [完成] 补充工单闭环流程（5 阶段）
- [完成] 补充风险预警规则（红黄绿阈值）
```

**输出：**
```markdown
### 项目进度

**2026-03-06 更新：**
- ✅ 完成 v2.1 版本修订（23:55）
- ✅ 补充工单闭环流程：创建→派发→执行→验收→关闭
- ✅ 补充风险预警规则：🔴<60%/🟡60-80%/🟢≥80%
- ✅ 补充供应商分级标准：A/B/C 三类 (15/30/70 家)
- ✅ 添加版本记录表

**当前版本：** v2.1
**最后更新：** 2026-03-06 23:55
**状态：** 🟡 进行中（第 2 轮批注待处理）
```

---

### 豆包自动化系统项目

**输入：**
```markdown
### 2026-03-05 (周四)
- [完成] 豆包专家点评 Skill 创建
- [完成] HTML 专家点评格式标准定义
- [完成] Chrome 自动打开集成
```

**输出：**
```markdown
### 项目进度

**2026-03-05 更新：**
- ✅ 创建豆包专家点评 Skill
- ✅ 定义 HTML 专家点评格式标准（科学杂志 + 小红书风格）
- ✅ 集成 Chrome 自动打开功能
- ✅ 实现 TTS 语音自动播放（0 步操作）

**当前状态：** ✅ 已完成
**完成率：** 100%
```

---

## 工作流程

### 完整流程

```
1. 读取 worklog.txt - 提取本周记录
2. 识别项目关键词 - 匹配项目卡片
3. 读取项目卡片 - tasks/projects/*.md
4. 解析现有进度 - 读取「项目进度」章节
5. 添加新工作 - 追加本周工作内容
6. 更新统计 - 刷新 workload、完成率
7. 更新状态 - 根据进展更新项目状态
8. 保存文件 - 写回项目卡片
9. 发送通知 - 飞书同步完成消息
```

### 项目识别规则

**关键词匹配：**
```powershell
$projectKeywords = @{
    "感知与行动中心" = @("感知", "行动中心", "交付域", "风险管控")
    "豆包自动化" = @("豆包", "会话自动化", "专家点评")
    "产能监控系统" = @("产能", "SDC", "GP9", "LCR")
    "地理知识库" = @("地理", "地图", "KML", "Google Earth")
    "周报系统" = @("周报", "worklog", "workreport")
    "数据治理" = @("数据", "元数据", "字段", "CSV")
    "飞书集成" = @("飞书", "OAuth", "任务 API", "文档 API")
}
```

---

## 项目卡片结构

### 标准结构

```markdown
# 项目名称

## 项目基本信息

| 字段 | 内容 |
|------|------|
| 项目编号 | XM-2026-001 |
| 项目类别 | 数据治理 + 产能监控 |
| 项目经理 | 待明确 |
| 应用部门 | 供应链管理部 |
| 预期上线时间 | 2026-06-30（一期） |

## 项目进度

**2026-03-06 更新：**
- [工作内容 1]
- [工作内容 2]

**当前状态：** 🟡 进行中
**完成率：** 55%
**最后更新：** 2026-03-06 23:55

## 📚 项目知识库

### 业务规则
- [日期] 规则描述

### 技术决策
- [日期] 决策描述

### 关键指标
- [日期] 指标描述

### 风险与问题
- [日期] 问题描述

### 经验教训
- [日期] 经验描述

## 任务清单

- [x] 任务 1
- [ ] 任务 2

---

_最后更新：2026-03-06 23:55_
```

---

## 进度更新规则

### 增量更新

**规则：**
- ✅ 追加模式 - 不覆盖已有进度
- ✅ 按日期组织 - 每次更新标注日期
- ✅ 保留历史 - 所有历史更新都保留

**示例：**
```markdown
## 项目进度

**2026-03-07 更新：**
- ✅ 创建项目进度同步 Skill
- ✅ 定义进度更新规则

**2026-03-06 更新：**
- ✅ 完成 v2.1 版本修订
- ✅ 补充工单闭环流程

**2026-03-05 更新：**
- ✅ 创建项目卡片
```

### 状态标识

**项目状态：**
- 🟢 未启动 - 尚未开始
- 🟡 进行中 - 正在执行
- 🟠 待确认 - 等待用户确认
- 🔴 有风险 - 遇到问题
- ✅ 已完成 - 全部完成

**完成率计算：**
```powershell
$totalTasks = (Get-Content $projectFile -Raw) | Select-String "- \[.\]"
$completedTasks = (Get-Content $projectFile -Raw) | Select-String "- \[x\]"
$completionRate = [math]::Round(($completedTasks.Count / $totalTasks.Count) * 100, 0)
```

---

## 技术实现

### 同步脚本（PowerShell）

```powershell
param(
    [string]$WorklogPath = "C:\Users\Xiabi\.openclaw\workspace\worklog.txt",
    [string]$ProjectsDir = "C:\Users\Xiabi\.openclaw\workspace\tasks\projects"
)

# 读取 worklog
$worklog = Get-Content $worklogPath -Raw -Encoding UTF8

# 提取本周记录
$thisWeek = Get-Date -AddDays(-(Get-Date).DayOfWeek)
$weekStart = $thisWeek.ToString("yyyy-MM-dd")
$weekRecords = $worklog -split "`n" | Where-Object {
    $_ -match "### \d{4}-\d{2}-\d{2}" -and
    $_ -ge $weekStart
}

# 项目关键词匹配
$projectMap = @{
    "感知与行动中心" = @("感知", "行动中心", "交付域")
    "豆包自动化" = @("豆包", "会话自动化")
    "产能监控系统" = @("产能", "SDC", "GP9")
}

foreach ($project in $projectMap.Keys) {
    $projectFile = Join-Path $ProjectsDir "$project.md"
    if (Test-Path $projectFile) {
        # 读取项目卡片
        $content = Get-Content $projectFile -Raw -Encoding UTF8
        
        # 提取相关工作
        $relatedWork = $weekRecords | Where-Object {
            $_ -match ($projectMap[$project] -join "|")
        }
        
        if ($relatedWork) {
            # 更新项目进度
            $today = Get-Date -Format "yyyy-MM-dd"
            $updateSection = @"

**$today 更新：**
$($relatedWork -join "`n")

"@
            # 插入到「项目进度」章节
            $content = $content.Replace("## 项目进度", "## 项目进度$updateSection")
            
            # 保存
            $content | Set-Content $projectFile -Encoding UTF8
            Write-Host "✅ 项目同步：$project"
        }
    }
}
```

---

## 输出格式

### 飞书通知（同步完成）

```markdown
## 📊 项目进度同步完成

**时间：** 2026-03-07 01:10
**来源：** worklog.txt

### 同步的项目

| 项目 | 更新内容 | 状态 |
|------|----------|------|
| **感知与行动中心** | +3 项工作 | 🟡 进行中 |
| **豆包自动化** | +2 项工作 | ✅ 已完成 |
| **产能监控系统** | +1 项工作 | 🟡 进行中 |

**总计：** 3 个项目，6 项更新

[查看项目卡片](file://tasks/projects/)
```

---

## 用户偏好

- ✅ **自动同步** - worklog 更新后自动执行
- ✅ **增量更新** - 保留历史进度
- ✅ **项目识别** - 准确匹配关键词
- ✅ **状态标识** - 清晰的项目状态
- ✅ **完成率统计** - 自动计算百分比

---

## 示例用法

**场景 1：worklog 更新后**
```
用户更新 worklog.txt
  ↓
自动触发项目进度同步
  ↓
识别项目 → 读取卡片 → 添加工作 → 保存
  ↓
飞书通知："同步完成，3 个项目更新"
```

**场景 2：手动触发**
```
用户："同步项目进度"
AI: 
1. 读取本周 worklog
2. 识别 3 个项目
3. 更新项目卡片
4. 发送完成通知
```

**场景 3：查看项目状态**
```
用户："感知与行动中心进展如何？"
AI: 
1. 读取项目卡片
2. 提取「项目进度」章节
3. 回复最新进展
```

---

## 与周报 Skill 的协作

**流程：**
```
worklog 更新
  ↓
项目进度同步 ← 本项目
  ↓
周报生成 ← 周报 Skill
```

**数据流：**
- worklog.txt → 项目卡片 → workreport.txt
- 项目进度作为周报的输入源之一

---

## 注意事项

1. **增量模式** - 只追加，不覆盖历史进度
2. **项目识别** - 准确匹配关键词，避免误判
3. **日期标注** - 每次更新标注日期
4. **状态更新** - 根据实际进展更新状态
5. **编码格式** - UTF-8，避免中文乱码

---

## 参考文档

- 项目卡片目录：`tasks/projects/`
- 工作日志：`worklog.txt`
- 周报 Skill：`skills/weekly-report-generator/SKILL.md`

---

_最后更新：2026-03-07 01:10 - 创建 Skill（参考 2026-03-06 感知与行动中心同步案例）_
