# Worklog 自动记录功能说明

**创建时间:** 2026-03-08 12:00  
**功能:** 每小时播报后自动更新 worklog.txt

---

## 📁 文件位置

**Worklog 文件夹:** `桌面\worklog\`

**文件命名:** `2026wXX-worklog.txt`（年 + 周数）

**示例:** `2026w11-worklog.txt`

---

## 🔄 工作流程

### 每小时播报自动执行

1. **读取任务** - 从 active-tasks.md 和 projects/*.md
2. **生成播报** - 创建 hourly-reminder-output.md
3. **发送飞书** - TTS 语音 + 文字消息
4. **本地播放** - 自动播放 MP3
5. **更新 worklog** - 追加今日完成和进展中内容

---

## 📝 Worklog 格式

### 文件头
```markdown
# 工作日志

**周期:** 2026w11
**开始日期:** 2026-03-03
**结束日期:** 2026-03-09

---
```

### 阿福记录（每小时追加）
```markdown
#### 2026-03-08 12:08 -- 阿福

**✅ 今天完成:**
- 知识图谱搭建完成（4 个项目卡片 + skills README + MEMORY 索引）
**📄 生成 HTML 专家点评:**
  - [expert-review-2026-03-08-data-governance.html](file://...)
  - [expert-review-2026-03-08-html-index.html](file://...)
  - ... (8 个 HTML 链接)

**🔄 进展中:**
- 数据治理（小米汽车项目）- 问题诊断阶段

**📊 当前任务状态:**
- P0 紧急重要：1 个
- P1 重要不紧急：4 个
- 总计：5 个任务

**📝 备注:** 每小时播报自动记录

---
```

### 用户记录（人工）
```markdown
#### 2026-03-08

今天去了公司，讨论了项目进度...

---
```

---

## 🎯 分工约定

| 角色 | 职责 | 记录方式 |
|------|------|----------|
| **阿福** | 从豆包 session 原文抽象提炼知识点 | MD 文件记录结构化知识 + TXT 记一笔 |
| **你** | 人工记录日常工作内容 | 直接写日期标题 + 内容 |

---

## 📅 周期规则

**按周分割**（避免文件太大）：
- **周期:** 周四 → 下周三（非自然周）
- **命名:** 2026w10-worklog.txt、2026w11-worklog.txt
- **自动创建:** 如果文件夹中没有当前周文件，自动新建

---

## 🔧 脚本配置

**脚本位置:** `scripts/hourly-priority-reminder.ps1`

**Step 6 代码:**
```powershell
# 计算当前周数
$desktop = [Environment]::GetFolderPath("Desktop")
$date = Get-Date
$weekNum = [Math]::Ceiling($date.DayOfYear / 7)
$year = $date.ToString("yyyy")
$worklogFileName = "$($year)w$($weekNum.ToString("00"))-worklog.txt"
$worklogFilePath = "$desktop\worklog\$worklogFileName"

# 创建文件（如不存在）
if (!(Test-Path $worklogFilePath)) {
    # 创建文件头
}

# 生成摘要内容
$summaryContent = @"
#### $timestamp -- 阿福
**✅ 今天完成:** ...
**🔄 进展中:** ...
**📊 当前任务状态:** ...
"@

# 追加到文件最上方
$existingContent = Get-Content $worklogFilePath -Raw
$summaryContent + $existingContent | Out-File $worklogFilePath
```

---

## ✅ 功能特点

1. ✅ **不删除原有内容** - 只在最上方插入增量
2. ✅ **标题带"--阿福"** - 方便识别系统记录
3. ✅ **按周分割文件** - 避免文件太大
4. ✅ **自动创建文件** - 如当前周文件不存在
5. ✅ **每小时更新** - 与播报同步
6. ✅ **HTML 链接自动附加** - 如当天生成 HTML 专家点评，自动附加链接列表

---

## 📊 当前状态

- **文件夹:** ✅ 已创建（桌面\worklog\）
- **当前文件:** ✅ 2026w11-worklog.txt
- **自动更新:** ✅ 已集成到 hourly-priority-reminder.ps1
- **下次播报:** 每小时整点后 1 分钟

---

## 🚀 下一步优化（可选）

1. 支持用户自定义"今天完成"和"进展中"内容
2. 每天 23:59 自动归档当周文件
3. 支持从 worklog 提取任务到 active-tasks.md
4. 生成周报时自动读取 worklog 内容

---

_最后更新：2026-03-08 12:00_
