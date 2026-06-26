# ATOM-DATA-002 - 更新 worklog

> 版本：V1.0  
> 状态：✅ 已固化  
> 最后更新：2026-03-06

---

## 📋 动作定义

**名称：** 更新 worklog  
**分类：** 数据层（Data Layer）  
**编号：** ATOM-DATA-002

**一句话描述：** 将工作内容追加到 worklog.txt 的今日记录中

---

## 🎯 输入输出

### 输入
- **类型：** 文本列表
- **内容：** 工作内容（带状态标记）
- **格式：** `[完成]/[进行中]/[待办] 工作描述`
- **必填：** 是

### 输出
- **类型：** 文件更新
- **路径：** `worklog.txt`
- **模式：** 追加（不覆盖）

---

## ⚙️ 偏好设置

### 记录格式
```markdown
### 2026-03-07 (周六)
- [完成] 工作内容 1
- [完成] 工作内容 2
- [进行中] 工作内容 3
- [待办] 工作内容 4
```

### 日期分组
- **格式：** `### YYYY-MM-DD (周 X)`
- **位置：** 按日期倒序排列（最新日期在最前）

### 状态标记
- `[完成]` - 已完成的工作
- `[进行中]` - 当前进行的工作
- `[待办]` - 计划要做的工作
- `[规划]` - 未来规划的工作

### 编码格式
- **编码：** UTF-8
- **换行：** Windows (CRLF)

---

## 📝 操作步骤

```powershell
# 1. 读取 worklog.txt
$worklogPath = "worklog.txt"
$content = Get-Content $worklogPath -Raw -Encoding UTF8

# 2. 生成今日记录头
$today = Get-Date -Format "yyyy-MM-dd"
$weekday = Get-Date -Format "ddd"
$todayHeader = "### $today ($weekday)"

# 3. 检查今日记录是否存在
if ($content -match [regex]::Escape($todayHeader)) {
    # 今日记录已存在，追加内容
    $newLines = $workItems | ForEach-Object { "- $_" }
    $newContent = $content.Replace($todayHeader, "$todayHeader`n$($newLines -join "`n")")
} else {
    # 创建今日记录
    $newSection = @"

$todayHeader
$($workItems | ForEach-Object { "- $_" } | Out-String)
"@
    $newContent = $content + $newSection
}

# 4. 保存文件
$newContent | Set-Content $worklogPath -Encoding UTF8

# 5. 确认
Write-Host "✅ worklog 已更新：$todayHeader"
```

---

## 🔄 使用场景

### 场景 1：豆包会话后更新
```
触发：豆包会话保存完成
  ↓
提取：[完成]/[进行中]/[待办] 内容
  ↓
调用：ATOM-DATA-002
  ↓
输出：worklog.txt 追加今日记录
```

### 场景 2：手动记录工作
```
触发：用户说"记一下今天的工作..."
  ↓
调用：ATOM-DATA-002
  ↓
输出：worklog.txt 追加内容
```

---

## 🔗 关联动作

### 前置动作
- ATOM-ANALYSIS-016：提取工作内容（从豆包会话提取）

### 后置动作
- ATOM-DATA-004：更新项目进度（同步到项目卡片）

### 常组合使用
- ATOM-ANALYSIS-016 + ATOM-DATA-002 + ATOM-DATA-004
  （提取内容 → 更新 worklog → 同步项目）

---

## ✅ 检查清单

执行前确认：
- [ ] worklog.txt 存在
- [ ] 状态标记正确（[完成]/[进行中]/[待办]）
- [ ] 编码 UTF-8
- [ ] 追加模式（不覆盖历史）

---

## 📚 参考文档

- 主数据清单：`原子级动作主数据清单.md`
- 工作日志：`worklog.txt`
- 使用 Skill：`skills/weekly-report-generator/SKILL.md`

---

_模块化定义 | 可独立调用 | 2026-03-07_
