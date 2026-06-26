# Unified Glossary - 统一专业词汇 Skill

> 版本：V1.0  
> 状态：🆕 新建  
> 最后更新：2026-03-07 14:36

---

## 📋 Skill 定义

**名称：** 统一专业词汇  
**编号：** SKILL-GLOSSARY-001  
**触发：** 生成 HTML/MD/TXT/飞书文档时自动触发

**一句话描述：** 统一专业词汇的英文简称/全称/中文名称，保证文档用词一致性

---

## 🎯 目标

**解决什么问题：**
- ❌ 之前：同一词汇在不同文档写法不一致
- ✅ 现在：统一格式，自动查询，自动新增

**核心价值：**
- 专业术语标准化
- 文档一致性提升
- 读者理解更容易

---

## 🔄 工作流程

```
生成文档（HTML/MD/TXT/飞书）
  ↓
遇到英文专业词汇
  ↓
查询专业词汇库
  ↓
├─ 存在 → 格式化输出（简称 + 全称 + 中文）
└─ 不存在 → 新增词汇 → 三线同步更新词汇库
  ↓
✅ 文档用词统一
```

---

## 📝 详细步骤

### 步骤 1：查询词汇库
```powershell
# 读取词汇库 MD 文件
$glossaryPath = "knowledge-base/glossary/ai-professional-glossary.md"
$glossaryContent = Get-Content $glossaryPath -Raw

# 提取所有词汇（解析表格）
$glossary = Parse-GlossaryTable $glossaryContent

# 查询词汇
$term = "LLM"
$termInfo = $glossary | Where-Object { $_.Abbreviation -eq $term }
```

### 步骤 2：格式化输出
```powershell
# 首次出现格式
if ($termInfo) {
    $formattedText = "$($termInfo.Abbreviation)（$($termInfo.EnglishFull), $($termInfo.ChineseName)）"
    # 输出：LLM（Large Language Model，大语言模型）
} else {
    # 词汇库没有，需要新增
    $newTerm = @{
        Abbreviation = $term
        EnglishFull = "待补充"
        ChineseName = "待补充"
        Explanation = "待补充"
    }
    Add-GlossaryTerm -Term $newTerm
}
```

### 步骤 3：新增词汇（如需要）
```powershell
# 1. 更新本地 MD 文件
$glossaryPath = "knowledge-base/glossary/ai-professional-glossary.md"
$glossaryContent = Parse-GlossaryTable $glossaryPath
$glossaryContent += $newTerm
Save-GlossaryMD -Path $glossaryPath -Content $glossaryContent

# 2. 更新本地 TXT 文件
Update-GlossaryTXT -Term $newTerm

# 3. 更新飞书文档（复用 ATOM-DOC-029）
$changeDesc = "新增专业词汇：$($newTerm.Abbreviation)"
Invoke-AtomAction "ATOM-DOC-029" -Action "add" -Desc $changeDesc

# 4. 三线同步完成
Write-Host "✅ 词汇库已更新（三线同步）"
```

---

## 📊 输入输出

### 输入
- **文档内容：** HTML/MD/TXT/飞书文档内容
- **词汇库路径：** `knowledge-base/glossary/ai-professional-glossary.md`
- **飞书 Token：** 待分配

### 输出
- **格式化文档：** 专业词汇统一格式
- **词汇库更新：** 新增词汇（如有）
- **状态：** `success` / `failed`

---

## 🎯 使用示例

### 示例 1：生成 HTML 专家点评
```powershell
# 生成 AI 基础知识科普 HTML
$content = "LLM 是一种强大的 AI 模型..."

# 调用统一专业词汇 Skill
Invoke-Skill "SKILL-GLOSSARY-001" -Content $content

# 输出：
# "LLM（Large Language Model，大语言模型）是一种强大的 AI 模型..."
```

### 示例 2：遇到新词汇
```powershell
# 文档中出现"Prompt Engineering"
$content = "Prompt Engineering 是一门艺术..."

# 查询词汇库：不存在
# 自动新增：
# - 简称：PE
# - 英文全称：Prompt Engineering
# - 中文名称：提示工程
# - 解释：设计和优化提示词的技术

# 三线同步更新词汇库
# 格式化输出：PE（Prompt Engineering，提示工程）
```

### 示例 3：生成飞书文档
```powershell
# 生成飞书文档《原子动作清单》
$docToken = "GeG0dywMxof8dLx1tcUckSFNndh"

# 调用统一专业词汇 Skill
Invoke-Skill "SKILL-GLOSSARY-001" -DocToken $docToken

# 所有专业词汇自动格式化
```

---

## 📁 文件结构

```
workspace/
├── knowledge-base/glossary/
│   ├── ai-professional-glossary.md      # MD 词汇库 ✅
│   └── ai-professional-glossary.txt     # TXT 说明 ✅
├── skills/
│   └── unified-glossary/
│       ├── SKILL.md                     # 🆕 本文件
│       └── glossary-sync.ps1            # 🆕 同步脚本
└── 飞书文档/
    └── AI 专业词汇库 - 动态更新            # 🆕 待创建
```

---

## ✅ 检查清单

执行前确认：
- [ ] 词汇库 MD/TXT 存在
- [ ] 飞书文档 Token 正确
- [ ] 有编辑权限

执行后确认：
- [ ] 文档词汇格式统一
- [ ] 新词汇已添加
- [ ] 三线同步完成
- [ ] 日志已记录

---

## ⚠️ 常见错误

### 错误 1：词汇库未更新
```
❌ 错误：只更新文档，忘记更新词汇库
✅ 正确：遇到新词汇立即同步更新
```

### 错误 2：格式不统一
```
❌ 错误：有时写全称，有时写简称
✅ 正确：首次出现用全称，后续用简称
```

### 错误 3：忘记三线同步
```
❌ 错误：只更新本地 MD/TXT，忘记飞书
✅ 正确：调用 ATOM-DOC-029 自动同步
```

---

## 💡 核心原则

> **统一专业词汇，保证文档一致性！**

**格式化规则：**
- 首次出现：`简称（英文全称，中文名称）`
- 后续出现：`简称`

**示例：**
- ✅ LLM（Large Language Model，大语言模型）
- ✅ 后续：LLM
- ❌ 有时写 Large Language Model，有时写 LLM

**自动新增：**
- 遇到新词汇 → 查询词汇库
- 不存在 → 自动新增 → 三线同步

---

## 📚 参考文档

- 词汇库 MD：`knowledge-base/glossary/ai-professional-glossary.md`
- 词汇库 TXT：`knowledge-base/glossary/ai-professional-glossary.txt`
- 原子动作：`ATOM-DOC-029 - 更新飞书原子动作清单`
- 飞书文档：待创建

---

_统一术语 | 自动调用 | 三线同步 | 2026-03-07_
