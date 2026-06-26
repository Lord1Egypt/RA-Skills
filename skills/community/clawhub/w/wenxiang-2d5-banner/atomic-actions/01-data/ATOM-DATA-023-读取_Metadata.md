# ATOM-DATA-023 - 读取 Metadata

> 版本：V1.0  
> 状态：🟡 新建  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 读取 Metadata  
**分类：** 数据层（Data Layer）  
**编号：** ATOM-DATA-023

**一句话描述：** 从 Metadata 文件中读取指定键的值

---

## 🎯 输入输出

### 输入
- **类型：** 文本
- **内容：** 键名
- **必填：** 是

### 输出
- **类型：** 任意类型
- **内容：** 键对应的值
- **格式：** 字符串/数字/布尔/数组/对象

---

## ⚙️ 偏好设置

### Metadata 文件
- **路径：** `knowledge-base/metadata.md`
- **格式：** YAML Front Matter + Markdown
- **编码：** UTF-8

### 读取模式
- **单键读取：** 返回单个值
- **多键读取：** 返回字典
- **全部读取：** 返回完整 Metadata

### 错误处理
- **键不存在：** 返回 $null
- **文件不存在：** 返回 $null 并提示

---

## 📝 操作步骤

```powershell
# 1. 准备 Metadata 文件路径
$metadataPath = "C:\Users\Xiabi\.openclaw\workspace\knowledge-base\metadata.md"

# 2. 检查文件存在
if (-not (Test-Path $metadataPath)) {
    Write-Host "❌ Metadata 文件不存在：$metadataPath"
    return $null
}

# 3. 读取文件内容
$content = Get-Content $metadataPath -Raw

# 4. 解析 YAML 格式（简单实现）
$metadata = @{}
$lines = $content -split "`n"
foreach ($line in $lines) {
    if ($line -match "^(\w+):\s*(.*)$") {
        $metadata[$matches[1]] = $matches[2]
    }
}

# 5. 读取指定键
$key = "project_name"
if ($metadata.ContainsKey($key)) {
    Write-Host "✅ 读取成功：$key = $($metadata[$key])"
    return $metadata[$key]
} else {
    Write-Host "❌ 键不存在：$key"
    return $null
}
```

---

## 🔄 使用场景

### 场景 1：读取项目信息
```
触发：需要项目元数据
  ↓
调用：ATOM-DATA-023
  ↓
输入：project_name
  ↓
输出：感知与行动中心
```

### 场景 2：读取系统配置
```
触发：系统初始化
  ↓
调用：ATOM-DATA-023
  ↓
输入：system_version
  ↓
输出：V1.0
```

---

## 🔗 关联动作

### 前置动作
- ATOM-DATA-022：创建 Metadata

### 后置动作
- 无（终端动作）

### 常组合使用
- ATOM-DATA-022 + ATOM-DATA-023
  （创建 → 读取验证）

---

## ✅ 检查清单

执行前确认：
- [ ] Metadata 文件存在
- [ ] 键名正确
- [ ] 编码 UTF-8
- [ ] 返回值类型正确

---

## ⚠️ 常见错误

### 错误 1：键不存在
```
❌ 错误：直接访问不存在的键
✅ 正确：先用 ContainsKey 检查
```

### 错误 2：文件不存在
```
❌ 错误：直接读取不存在的文件
✅ 正确：先用 Test-Path 检查
```

---

_模块化定义 | 可独立调用 | 2026-03-07_
