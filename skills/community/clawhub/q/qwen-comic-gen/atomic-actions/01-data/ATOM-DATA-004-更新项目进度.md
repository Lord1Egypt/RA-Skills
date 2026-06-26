# ATOM-DATA-004 - 更新项目进度

> 版本：V1.0  
> 状态：🟡 待规范  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 更新项目进度  
**分类：** 数据层（Data Layer）  
**编号：** ATOM-DATA-004

**一句话描述：** 将新进展追加到项目卡片中，更新项目状态

---

## 🎯 输入输出

### 输入
- **类型：** 文本
- **内容：** 项目名 + 工作进展
- **格式：** 项目名称 + 进展描述（带日期）

### 输出
- **类型：** 文件更新
- **路径：** `knowledge-base/projects/项目名/项目卡片.md`
- **模式：** 追加（不覆盖）

---

## ⚙️ 偏好设置

### 进展格式
```markdown
### 2026-03-07 (周六) 09:00
- 🟡 进行中：新增进展描述
- ✅ 完成：完成的工作
```

### 状态标识
- 🟢 正常（绿色）
- 🟡 进行中（黄色）
- 🔴 风险（红色）

### 日期标注
- **格式：** `YYYY-MM-DD (周 X) HH:mm`
- **位置：** 每条进展开头

---

## 📝 操作步骤

```powershell
# 1. 读取项目卡片
$projectPath = "knowledge-base/projects/$projectName/项目卡片.md"
$content = Get-Content $projectPath -Raw -Encoding UTF8

# 2. 生成新进展
$newProgress = @"

### $(Get-Date -Format 'yyyy-MM-dd (ddd) HH:mm')
- $status $progress
"@

# 3. 追加内容
$newContent = $content + $newProgress

# 4. 保存文件
$newContent | Set-Content $projectPath -Encoding UTF8
```

---

## 🔄 使用场景

### 场景 1：项目进展更新
```
触发：完成一项项目工作
  ↓
调用：ATOM-DATA-004
  ↓
输出：项目卡片追加新进展
```

---

## 🔗 关联动作

### 前置动作
- ATOM-DATA-003：读取项目卡片

### 常组合使用
- ATOM-DATA-003 + ATOM-DATA-004
  （读取 → 更新）

---

_模块化定义 | 可独立调用 | 2026-03-07_
