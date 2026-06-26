# ATOM-IO-021 - 保存 HTML 文件

> 版本：V1.0  
> 状态：🟡 新建  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 保存 HTML 文件  
**分类：** IO 层（Input/Output Layer）  
**编号：** ATOM-IO-021

**一句话描述：** 将 HTML 内容保存到文件系统

---

## 🎯 输入输出

### 输入
- **类型：** 文本 + 文件路径
- **内容：** HTML 内容 + 保存路径
- **格式：** UTF-8 编码字符串

### 输出
- **类型：** 文件
- **路径：** 保存的绝对路径
- **大小：** 文件大小（字节）

---

## ⚙️ 偏好设置

### 文件命名
- **格式：** `expert-review-YYYY-MM-DD-主题.html`
- **目录：** `workspace/` 或 `workspace/expert-reviews/`
- **编码：** UTF-8

### 目录创建
- **自动创建：** 如果目录不存在
- **模式：** `New-Item -ItemType Directory -Force`

---

## 📝 操作步骤

```powershell
# 1. 准备文件路径
$savePath = "C:\Users\Xiabi\.openclaw\workspace\expert-review-2026-03-07-感知与行动中心.html"

# 2. 确保目录存在
$dir = Split-Path $savePath -Parent
if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

# 3. 保存文件
$htmlContent | Set-Content $savePath -Encoding UTF8

# 4. 确认
Write-Host "✅ HTML 文件已保存：$savePath"
Write-Host "  大小：$((Get-Item $savePath).Length) 字节"

# 5. 返回路径
return $savePath
```

---

## 🔄 使用场景

### 场景 1：专家点评 HTML 生成
```
触发：ATOM-IO-020 写入内容完成
  ↓
调用：ATOM-IO-021
  ↓
输出：HTML 文件保存成功
  ↓
下一步：ATOM-VISUAL-009 Chrome 打开
```

### 场景 2：批量报告保存
```
触发：多个 HTML 内容需要保存
  ↓
循环：每个 HTML 内容
  ↓
调用：ATOM-IO-021
  ↓
输出：多个 HTML 文件
```

---

## 🔗 关联动作

### 前置动作
- ATOM-IO-020：写入 HTML 内容

### 后置动作
- ATOM-VISUAL-009：Chrome 打开文件

### 常组合使用
- ATOM-IO-019 + ATOM-IO-020 + ATOM-IO-021
  （读取 → 写入 → 保存）

---

## ✅ 检查清单

执行前确认：
- [ ] HTML 内容非空
- [ ] 保存路径正确
- [ ] 目录可写
- [ ] 编码 UTF-8

---

## ⚠️ 常见错误

### 错误 1：目录不存在
```
❌ 错误：直接保存到不存在的目录
✅ 正确：先用 New-Item 创建目录
```

### 错误 2：编码错误
```
❌ 错误：中文乱码
✅ 正确：使用 -Encoding UTF8
```

---

_模块化定义 | 可独立调用 | 2026-03-07_
