# ATOM-FEISHU-030 - 飞书文档加序号（领导汇报版）

> 版本：V1.0  
> 状态：🆕 新建  
> 最后更新：2026-03-07 14:51  
> 触发词：**"标题加序号" / "给领导汇报" / "加工文档"**

---

## 📋 动作定义

**名称：** 飞书文档加序号（领导汇报版）  
**分类：** 交付层（Delivery Layer）  
**编号：** ATOM-FEISHU-030

**一句话描述：** 为飞书文档标题添加序号（Ctrl+Shift+7），移除 icons，适合领导汇报

---

## 🎯 使用场景

**触发条件（需用户明确说）：**
- "标题加序号"
- "给领导汇报"
- "加工文档"
- "整理成正式格式"

**不触发的情况：**
- 日常文档（不需要序号）
- 个人学习笔记
- 非正式协作文档

**核心目的：**
- ✅ 给领导汇报时使用（正式格式）
- ✅ 移除花哨 icons（专业简洁）
- ✅ 添加标准序号（1. / 1.1 / 1.1.1）

---

## 📝 操作步骤

### 步骤 1：读取飞书文档内容
```powershell
# 读取文档内容
$docToken = "文档 Token"
$content = feishu_doc -action read -doc_token $docToken
```

### 步骤 2：移除所有 icons
```powershell
# 移除 emoji icons
$content = $content -replace '⭐|💡|🔍|📊|📋|🎯|✅|❌|⚠️|💡|🔴|🟡|🟢|🆕', ''
# 移除其他装饰性 emoji
$content = $content -replace '🏗️|📁|📝|📚|🔄|💾|🎨|🚀|📄|📦', ''
```

### 步骤 3：添加标题序号
```powershell
# 识别标题层级（# = H1, ## = H2, ### = H3）
$h1Counter = 0
$h2Counter = 0
$h3Counter = 0

$lines = $content -split "`n"
$newLines = @()

foreach ($line in $lines) {
    if ($line -match '^# (.+)') {
        # H1 标题：1. 标题
        $h1Counter++
        $h2Counter = 0
        $h3Counter = 0
        $newLines += "$h1Counter. $($matches[1])"
    }
    elseif ($line -match '^## (.+)') {
        # H2 标题：1.1 标题
        $h2Counter++
        $h3Counter = 0
        $newLines += "$h1Counter.$h2Counter $($matches[1])"
    }
    elseif ($line -match '^### (.+)') {
        # H3 标题：1.1.1 标题
        $h3Counter++
        $newLines += "$h1Counter.$h2Counter.$h3Counter $($matches[1])"
    }
    else {
        $newLines += $line
    }
}

$newContent = $newLines -join "`n"
```

### 步骤 4：分块写入飞书文档
```powershell
# 分块（≤200 blocks/块）
$blocks = $newContent -split "`n"
$blockSize = 50
$chunks = @()
for ($i = 0; $i -lt $blocks.Count; $i += $blockSize) {
    $chunks += , $blocks[$i..([Math]::Min($i + $blockSize - 1, $blocks.Count - 1))]
}

# 第 1 块：write 模式
feishu_doc -action write -doc_token $docToken -content ($chunks[0] -join "`n")

# 后续块：append 模式
for ($i = 1; $i -lt $chunks.Count; $i++) {
    feishu_doc -action append -doc_token $docToken -content ($chunks[$i] -join "`n")
}

Write-Host "✅ 文档已加工完成（标题加序号 + 移除 icons）"
```

---

## 🎯 输入输出

### 输入
- **类型：** 飞书文档 Token
- **内容：** 包含 icons 和无序号标题的文档
- **必填：** 是
- **触发条件：** 用户明确说"标题加序号"或"给领导汇报"

### 输出
- **类型：** 飞书文档（已加工）
- **内容：** 移除 icons + 添加序号的正式格式
- **附加：** 加工完成提示

---

## ⚙️ 偏好设置

### 序号格式
- **H1 标题：** `1. 标题` / `2. 标题`
- **H2 标题：** `1.1 标题` / `1.2 标题`
- **H3 标题：** `1.1.1 标题` / `1.1.2 标题`

### 移除的 icons
- ⭐ 💡 🔍 📊 📋 🎯 ✅ ❌ ⚠️
- 🔴 🟡 🟢 🆕 🏗️ 📁 📝 📚
- 🔄 💾 🎨 🚀 📄 📦

### 保留的内容
- ✅ 表格
- ✅ 引用块
- ✅ 列表
- ✅ 代码块
- ✅ 链接

---

## 🔄 使用示例

### 示例 1：给领导汇报
```
用户：这个文档要给领导汇报，标题加序号
  ↓
调用：ATOM-FEISHU-030
  ↓
处理：移除 icons + 添加序号
  ↓
输出：正式格式文档（1. / 1.1 / 1.1.1）
```

### 示例 2：加工文档
```
用户：帮我加工一下这个文档，准备给领导看
  ↓
调用：ATOM-FEISHU-030
  ↓
处理：移除 emoji + 添加标准序号
  ↓
输出：专业简洁格式
```

---

## 🔗 关联动作

### 前置动作
- ATOM-FEISHU-028：写入飞书文档（创建初稿）

### 后置动作
- 无（加工完成即可）

### 常组合使用
- ATOM-FEISHU-028 + ATOM-FEISHU-030
  （创建初稿 → 加工成正式格式）

---

## ✅ 检查清单

执行前确认：
- [ ] 用户明确要求（"标题加序号" / "给领导汇报"）
- [ ] 文档 Token 正确
- [ ] 有编辑权限
- [ ] 已备份原文档（可选）

执行后确认：
- [ ] 所有 icons 已移除
- [ ] H1/H2/H3 标题有序号
- [ ] 序号格式正确（1. / 1.1 / 1.1.1）
- [ ] 表格/列表/代码块保留
- [ ] 文档内容完整

---

## ⚠️ 常见错误

### 错误 1：误用动作
```
❌ 错误：所有文档都加序号
✅ 正确：只有给领导汇报时才用
```

### 错误 2：序号格式错误
```
❌ 错误：1、2、3（中文顿号）
✅ 正确：1. 2. 3.（英文点号）
```

### 错误 3：忘记分块写入
```
❌ 错误：一次性写入 → 空白文档
✅ 正确：分块写入（≤200 blocks/块）
```

---

## 💡 核心原则

> **只有给领导汇报时才加序号！日常文档不需要！**

**触发条件：**
- ✅ 用户明确说"标题加序号"
- ✅ 用户说"给领导汇报"
- ✅ 用户说"加工文档"

**不触发：**
- ❌ 日常协作文档
- ❌ 个人学习笔记
- ❌ 非正式文档

**序号格式：**
- H1：1. / 2. / 3.
- H2：1.1 / 1.2 / 1.3
- H3：1.1.1 / 1.1.2 / 1.1.3

---

## 📚 参考文档

- 主数据清单：`原子级动作主数据清单.md`
- 关联动作：`ATOM-FEISHU-028 - 写入飞书文档`
- 使用 Skill：`skills/project-knowledge-expert/SKILL.md`

---

_模块化定义 | 可独立调用 | 领导汇报专用 | 2026-03-07_
