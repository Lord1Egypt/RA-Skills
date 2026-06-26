---
name: pwsh-encoding-fix
description: "Fix PowerShell file encoding corruption (backtick, dollar sign, Chinese char mangling) when writing Node.js files on Windows."
---

# PowerShell 文件编码修复

在 Windows PowerShell 中写入含特殊字符的 Node.js/JS 文件时，PowerShell 会破坏文件内容。此 Skill 提供诊断和修复方法。

## 现象

| 问题 | 表现 | 原因 |
|------|------|------|
| 反引号被吞 | 模板字符串 `` `hello ${name}` `` → `"hello ${name}"` | PowerShell 把 `` ` `` 当转义符 |
| $ 变量被展开 | `${var}` 变空字符串 | PowerShell 展开 `$var` 变量 |
| 中文变乱码 | 汉字变垃圾字符（如 `å·²æŸ¥åˆ°`） | UTF-8 被 GBK 重编码 |
| 文件体积暴增 | 13KB → 20MB | 乱码字符被反复替换 |

## 根本原因

PowerShell 管道命令会修改文件编码：
```powershell
# ❌ 这些命令会破坏文件：
Set-Content file.js "content"         # 吞反引号
Out-File file.js                       # 吞反引号
Get-Content | Set-Content             # 管道 → 重编码
Write-Output "`$var" > file.js        # 展开 $ 变量
```

## 使用诊断修复工具

本 Skill 附带一个可执行脚本 `pwsh-encoding-fix.js`，可以在任何有 Node.js 的 Windows 机器上运行：

```bash
# 诊断文件编码问题
node pwsh-encoding-fix.js <文件路径>

# 诊断并自动修复（仅 GBK 乱码可自动修复）
node pwsh-encoding-fix.js <文件路径> --fix
```

### 工具的诊断能力

| 严重度 | 检测类型 | 说明 |
|--------|----------|------|
| !! CRITICAL | BACKTICK_LOST | 模板字符串反引号被 PowerShell 吞掉 |
| !! CRITICAL | DOLLAR_EXPANDED | `${var}` 变量被展开为空 |
| !! CRITICAL | GBK_CORRUPT | 中文 UTF-8 被 GBK 重编码损坏（可自动修复） |
| !! CRITICAL | SYNTAX_ERROR | JS 语法检查失败，可能是编码损坏导致 |
| WW WARNING | BACKTICK_PARTIAL | 部分模板可能受损 |
| WW WARNING | GBK_CORRUPT (mild) | 部分中文可能受损 |
| II LOW | BOM | 文件含 UTF-8 BOM 头（不影响运行但不够干净） |

### 工具输出示例

```
========================================================
  PowerShell Encoding Damage Report
========================================================
  File:    C:\project\server.js
  Size:    17.9 KB  (408 lines)
  Backtick: 0
  Dollar{}: 15 total
  Suspicious lines: 12 / 12
  Chinese: 1257 valid / 242 GBK residual
  Syntax:  FAIL
--------------------------------------------------------
  Found 3 issue(s):

  !! [CRITICAL] BACKTICK_LOST
     12 lines use ${} without backticks. Template literals stripped.
  !! [CRITICAL] GBK_CORRUPT
     GBK residual: 242 chars / valid Chinese: 1257 (ratio 0.2)
  !! [CRITICAL] SYNTAX_ERROR
     Unexpected token ...
--------------------------------------------------------
  Critical issues found. Use --fix to attempt repair.
```

## 安全写入方法

### 方法 1：Node.js writeFileSync（最安全）
```powershell
node -e "fs.writeFileSync('file.js', 'content', 'utf8')"
```
注意：`-e` 字符串中的 `$` 仍会被 PowerShell 展开，需要用单引号包裹或转义。

### 方法 2：OpenClaw write 工具（推荐）
直接使用 `write` 工具创建文件，不走 PowerShell 管道。

### 方法 3：hex 编码写入（万无一失）
在干净机器上生成 hex：
```bash
node -e "const fs=require('fs');const h=fs.readFileSync('file.js').toString('hex');console.log(h)" > file.hex
```
在目标机器上恢复：
```bash
node -e "const fs=require('fs');fs.writeFileSync('file.js',Buffer.from(fs.readFileSync('file.hex','utf8').trim(),'hex'))"
```

## 诊断命令（手动）

```powershell
# 检查语法
node --check file.js

# 检查 BOM 头（正确的文件头应是 63 6f 6e = "con"）
node -e "const fs=require('fs');const b=fs.readFileSync('file.js');console.log(b[0].toString(16),b[1].toString(16),b[2].toString(16))"

# 检查反引号数量
node -e "const fs=require('fs');const c=fs.readFileSync('file.js','utf8');const bt=String.fromCharCode(96);console.log('Backtick count:',c.split(bt).length-1)"
```

## 修复步骤

1. **不要用 PowerShell 管道修复！** 不要 `Get-Content | Set-Content`
2. 用 Node.js 读取原文件：`fs.readFileSync('file.js', 'utf8')` 
3. 检查编码损坏类型（反引号缺失 / 中文乱码 / 体积暴增）
4. 如果只是中文乱码：用 `--fix` 模式自动修复，或用 find/replace 映射
5. 如果反引号也被吃了：必须从原始源码重写
6. 最稳妥：用 `write` 工具直接从原始源码完整重写

## 预防措施

- 用 OpenClaw `write` 工具代替 PowerShell 写文件
- 改完文件后立刻 `node --check` 验证语法
- 复杂 JS 文件用 Node.js `writeFileSync` 或 hex 编码写入

## 文件

| 路径 | 说明 |
|------|------|
| `SKILL.md` | 本文档 |
| `pwsh-encoding-fix.js` | 可执行诊断修复工具（Node.js脚本） |

## 在其他机器上部署

只需将 `pwsh-encoding-fix.js` 拷贝到目标机器（任何 Windows 系统），确保已安装 Node.js：

```bash
# 从本目录复制到目标机器
# 然后在目标机器上运行
node pwsh-encoding-fix.js 需要检查的文件.js
node pwsh-encoding-fix.js 需要检查的文件.js --fix
```

无需安装任何 npm 包。GBK 修复需要 `iconv-lite`（自动检测，无则回退到内置 TextDecoder）。
