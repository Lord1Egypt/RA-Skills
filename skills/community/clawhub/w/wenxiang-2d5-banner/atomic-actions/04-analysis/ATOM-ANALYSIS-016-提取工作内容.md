# ATOM-ANALYSIS-016 - 提取工作内容

> 版本：V1.0  
> 状态：🟡 待规范  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 提取工作内容  
**分类：** 分析层（Analysis Layer）  
**编号：** ATOM-ANALYSIS-016

**一句话描述：** 从文本中提取工作内容，按状态分类（完成/进行中/待办）

---

## 🎯 输入输出

### 输入
- **类型：** 文本
- **内容：** 待分析的文本

### 输出
- **类型：** 文本列表
- **内容：** [完成]/[进行中]/[待办] 列表

---

## ⚙️ 偏好设置

### 状态识别
| 标记 | 含义 | 颜色 |
|------|------|------|
| [完成] | 已完成 | 🟢 绿色 |
| [进行中] | 当前进行 | 🟡 黄色 |
| [待办] | 计划要做 | ⚪ 白色 |
| [规划] | 未来规划 | 🔵 蓝色 |

### 提取规则
- **正则匹配：** `\[.*?\]\s*(.*)`
- **分组：** 按日期分组
- **去重：** 去除重复内容

---

## 📝 操作步骤

```powershell
# 1. 定义状态标记
$statusPatterns = @(
    "\[完成\]\s*(.*)",
    "\[进行中\]\s*(.*)",
    "\[待办\]\s*(.*)",
    "\[规划\]\s*(.*)"
)

# 2. 提取工作内容
$text = Get-Content "worklog.txt" -Raw
$workItems = @{
    Completed = @()
    InProgress = @()
    Todo = @()
    Planned = @()
}

foreach ($line in $text.Split("`n")) {
    if ($line -match "\[完成\]\s*(.*)") { $workItems.Completed += $matches[1] }
    elseif ($line -match "\[进行中\]\s*(.*)") { $workItems.InProgress += $matches[1] }
    elseif ($line -match "\[待办\]\s*(.*)") { $workItems.Todo += $matches[1] }
    elseif ($line -match "\[规划\]\s*(.*)") { $workItems.Planned += $matches[1] }
}

# 3. 返回结果
return $workItems
```

---

## 🔄 使用场景

### 场景 1：豆包会话后更新 worklog
```
触发：豆包会话完成
  ↓
调用：ATOM-ANALYSIS-016
  ↓
输出：[完成]/[进行中]/[待办] 列表
  ↓
下一步：ATOM-DATA-002 更新 worklog
```

### 场景 2：周报生成
```
触发：每周三 15:00
  ↓
调用：ATOM-ANALYSIS-016
  ↓
输出：本周工作项列表
  ↓
下一步：生成 workreport.txt
```

---

## 🔗 关联动作

### 前置动作
- 无（可独立执行）

### 后置动作
- ATOM-DATA-002：更新 worklog

### 常组合使用
- ATOM-ANALYSIS-016 + ATOM-DATA-002
  （提取内容 → 更新 worklog）

---

## ✅ 检查清单

执行前确认：
- [ ] 文本非空
- [ ] 状态标记正确
- [ ] 分类完整

---

_模块化定义 | 可独立调用 | 2026-03-07_
