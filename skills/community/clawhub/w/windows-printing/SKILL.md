---
name: windows-printing
description: 在 Windows 上列出可用打印机并执行本地文件打印，支持让用户从可用打印机中选择，并配置黑白/彩色、份数、单面/双面、沿长边翻转、沿短边翻转、纸张大小。用户提到“打印”“打印机”“单面/双面”“长边翻转”“短边翻转”“A4”“黑白/彩色”“打印 PDF/文档/图片”时使用。
---

# Windows Printing

在 Windows 上处理本地打印任务时，优先复用本 skill，而不是每次临时拼 PowerShell。

## 工作流

1. 如果用户说“桌面上的 xxx”“下载里的 xxx”“那个测试 PDF”之类的模糊文件名，先运行 `scripts/resolve_file.ps1` 查候选文件。
2. 运行 `scripts/list_printers.ps1` 列出当前可用打印机，并带出默认打印机及当前配置。
3. 把打印机名称按序号或清单展示给用户，让用户明确选择；如果只有一台明显目标打印机，也仍然优先复述确认。
4. 收集或确认这些参数：
   - `printer`：打印机名称
   - `file`：要打印的本地文件路径
   - `color_mode`：`keep` / `color` / `grayscale`
   - `copies`：正整数
   - `duplex_mode`：`keep` / `one-sided` / `long-edge` / `short-edge`
   - `paper_size`：如 `A4` / `A3` / `Letter`
5. 正式打印前，先用 `scripts/print_file.ps1 -WhatIfOnly` 生成“将要提交”的配置摘要；如果用户话里已经足够明确，可直接执行，否则先把摘要复述给用户确认。
6. 调用 `scripts/print_file.ps1` 执行打印。
7. 打印后优先直接读取脚本输出里的 `receipt` 字段作为回执来源，不要每次手工重组。
8. `receipt` 字段当前由脚本稳定输出 ASCII 值（如 `grayscale`、`one-sided`、`submitted-queue-empty`）；在对用户展示时，再翻译成自然中文回执。
9. 如果 `receipt` 缺失，再按模板兜底组装回执，至少包含：文件名、打印机、颜色、份数、单双面/翻转、纸张、队列状态、是否有错误。
10. 如果队列为空，说明任务通常已被系统接收或快速完成，不要硬说“百分百已打印完成”。

## 默认规则

- 如果用户没有指定打印机：必须先列出可用打印机并让用户选。
- 如果用户只说“用上次那台”“测试打印机”之类的模糊称呼：列出匹配项并让用户按序号确认，不要自作主张。
- 如果用户没有给完整路径但文件名足够明显：先用 `resolve_file.ps1` 在桌面、文档、下载目录中找候选；唯一高置信命中时可直接复述确认，多命中时必须让用户选。
- 如果用户没有指定颜色：默认 `keep`，保持当前打印机配置，不要擅自改。
- 如果用户没有指定份数：默认 `1`。
- 如果用户没有指定单双面：默认 `keep`；但如果用户明确说“单面/双面”，必须显式设置。
- 如果用户说“双面打印”但没说翻转方式：默认 `long-edge`，并在回复里点明是“沿长边翻转”。
- 如果用户指定纸张大小：尽量设置；如果打印机或驱动不接受该纸张，明确告诉用户是驱动限制。
- 除非用户说得极明确，否则正式打印前先给一条简短确认：打印机、文件、颜色、份数、单双面/翻转、纸张大小。

## 参数映射

把用户语言映射到脚本参数：

- 黑白、灰度、仅黑白 → `grayscale`
- 彩色 → `color`
- 单面 → `one-sided`
- 双面、双面打印、长边翻转 → `long-edge`
- 短边翻转 → `short-edge`

把脚本参数映射到 Windows 打印配置：

- `one-sided` → `OneSided`
- `long-edge` → `TwoSidedLongEdge`
- `short-edge` → `TwoSidedShortEdge`
- `color` → `Color=$true`
- `grayscale` → `Color=$false`

## 执行方式

解析模糊文件名：

```powershell
powershell -ExecutionPolicy Bypass -File "<skill-dir>\scripts\resolve_file.ps1" -Query "测试.pdf"
```

列出打印机：

```powershell
powershell -ExecutionPolicy Bypass -File "<skill-dir>\scripts\list_printers.ps1"
```

打印前预演：

```powershell
powershell -ExecutionPolicy Bypass -File "<skill-dir>\scripts\print_file.ps1" \
  -FilePath "D:\path\file.pdf" \
  -PrinterName "打印机 1" \
  -ColorMode grayscale \
  -Copies 2 \
  -DuplexMode one-sided \
  -PaperSize A4 \
  -WhatIfOnly
```

正式打印：

```powershell
powershell -ExecutionPolicy Bypass -File "<skill-dir>\scripts\print_file.ps1" \
  -FilePath "D:\path\file.pdf" \
  -PrinterName "打印机 1" \
  -ColorMode grayscale \
  -Copies 2 \
  -DuplexMode one-sided \
  -PaperSize A4
```

## 确认话术模板

正式提交前，优先用这种简洁格式复述：

- 我将打印：`测试.pdf`
- 打印机：`打印机 1`
- 颜色：黑白
- 份数：2
- 方式：双面（沿长边翻转）
- 纸张：A4

如果用户直接回复“确认 / 打 / 可以”，再执行正式打印。

## 打印后回执模板

正式打印后，优先按这个结构回报：

- 打印回执
- 文件：`测试.pdf`
- 打印机：`打印机 1`
- 颜色：黑白
- 份数：2
- 方式：双面（沿长边翻转）
- 纸张：A4
- 队列状态：空 / 仍有 1 个任务 / 有异常
- 结果：已提交到系统 / 提交失败

脚本输出中的 `receipt` 字段应作为首选回执来源，建议直接读取其字段：
- `title`
- `fileName`
- `printer`
- `color`
- `copies`
- `duplex`
- `paperSize`
- `queueStatus`
- `result`
- `errorSummary`（有错误时）

如果脚本返回 `errors` 非空：
- 明确写“结果：提交失败”
- 把最关键的一条报错翻成人话

如果脚本返回 `queueCount = 0`：
- 可以写“任务已提交，当前队列为空，通常表示已被系统接收或快速处理”
- 不要写成“已确定打印完成”

## 注意事项

- 这个脚本优先面向 `PDF`；对其它格式依赖系统默认关联程序是否支持静默打印。
- 多份打印目前通过循环提交任务实现；因此大份数时要提醒用户别手滑填太大。
- `Set-PrintConfiguration` 会修改打印机当前配置；脚本会尽量恢复原配置，但如果关联程序长期占用或驱动异常，恢复可能失败，要把这一点说清楚。
- `-WhatIfOnly` 不会真正打印，只用于生成预演配置，适合打印前确认。
- 如果第一次打印失败，优先检查：文件路径、打印机关联名、驱动是否在线、默认 PDF 打开程序是否支持 `PrintTo`。
