# ATOM-IO-020 - 写入 HTML 内容

> 版本：V1.0  
> 状态：🟡 新建  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 写入 HTML 内容  
**分类：** IO 层（Input/Output Layer）  
**编号：** ATOM-IO-020

**一句话描述：** 将内容写入 HTML 模板的占位符位置

---

## 🎯 输入输出

### 输入
- **类型：** 文本 + 字典
- **内容：** HTML 模板 + 内容字典
- **格式：** 模板字符串 + @{key=value}

### 输出
- **类型：** 文本
- **内容：** 填充后的完整 HTML
- **格式：** UTF-8 编码字符串

---

## ⚙️ 偏好设置

### 占位符格式
- **语法：** `{{key}}`
- **示例：** `{{title}}`, `{{content}}`, `{{chart}}`

### 内容替换
- **模式：** 全部替换（-replace）
- **编码：** UTF-8
- **保留：** 原始模板结构

---

## 📝 操作步骤

```powershell
# 1. 准备模板和内容
$template = Get-Content "template.html" -Raw
$data = @{
    title = "专家点评 - 感知与行动中心"
    content = "<div>核心内容...</div>"
    chart = "<div class='mermaid'>...</div>"
}

# 2. 替换占位符
$htmlContent = $template
foreach ($kv in $data.GetEnumerator()) {
    $htmlContent = $htmlContent -replace "\{\{$($kv.Key)\}\}", $kv.Value
}

# 3. 返回完整 HTML
return $htmlContent
```

---

## 🔄 使用场景

### 场景 1：专家点评 HTML 生成
```
触发：ATOM-IO-019 读取模板完成
  ↓
调用：ATOM-IO-020
  ↓
输入：模板 + 专家评分/洞察/图表
  ↓
输出：完整 HTML 内容
```

### 场景 2：批量报告生成
```
触发：多个数据需要生成报告
  ↓
循环：每个数据集
  ↓
调用：ATOM-IO-020
  ↓
输出：多个 HTML 内容
```

---

## 🔗 关联动作

### 前置动作
- ATOM-IO-019：读取 HTML 模板

### 后置动作
- ATOM-IO-021：保存 HTML 文件

### 常组合使用
- ATOM-IO-019 + ATOM-IO-020 + ATOM-IO-021
  （读取 → 写入 → 保存）

---

## ✅ 检查清单

执行前确认：
- [ ] 模板内容非空
- [ ] 数据字典完整
- [ ] 占位符匹配
- [ ] 特殊字符转义

---

## ⚠️ 常见错误

### 错误 1：占位符不匹配
```
❌ 错误：{{title}} 但数据是 {title}
✅ 正确：统一使用 {{key}} 格式
```

### 错误 2：特殊字符未转义
```
❌ 错误：HTML 内容包含 < > &
✅ 正确：使用 WebUtility.HtmlEncode
```

---

_模块化定义 | 可独立调用 | 2026-03-07_
