# Printing Options Reference

## 常用参数

- `ColorMode`
  - `keep`：保持当前打印机设置
  - `color`：彩色
  - `grayscale`：黑白/灰度

- `Copies`
  - 1-99

- `DuplexMode`
  - `keep`：保持当前打印机设置
  - `one-sided`：单面
  - `long-edge`：双面，沿长边翻转
  - `short-edge`：双面，沿短边翻转

- `PaperSize`
  - 常见值：`A4`、`A3`、`Letter`
  - 最终是否生效取决于驱动和打印机支持

## 默认补全策略

- 未指定打印机 → 必须列清单让用户选
- 未指定文件完整路径 → 先用 `resolve_file.ps1` 查桌面 / 文档 / 下载
- 未指定颜色 → `keep`
- 未指定份数 → `1`
- 未指定单双面 → `keep`
- 指定“双面”但没说翻转 → `long-edge`

## 建议回复模板

当用户没指定打印机时：

1. 列出可用打印机
2. 让用户回复名称或序号
3. 如果缺少其它关键参数，一并补问

示例：

- 可用打印机有：1) 打印机 1  2) 打印机 2
- 你回我序号就行；如果你还要黑白/彩色、份数、单双面、纸张大小，也可以一起说。

当文件名不完整时：

- 我找到这些候选文件：1) 桌面\测试.pdf  2) 下载\测试(1).pdf
- 你回我序号，或者直接把完整路径发我。

打印前确认示例：

- 我将打印 `测试.pdf` 到 `打印机 1`，黑白，2 份，双面（沿长边翻转），A4。你回我“确认”我就提交。

## 建议执行后回报

优先读取脚本输出里的 `receipt` 字段；统一使用“打印回执”格式，至少包含：

- 文件名
- 打印机
- 颜色
- 份数
- 单双面 / 翻转方式
- 纸张大小
- 队列状态
- 结果（已提交 / 提交失败）
- `errorSummary`（有错误时）

当前脚本为规避 Windows PowerShell 编码问题，`receipt` 内部优先输出稳定的 ASCII 值：

- `color`: `grayscale` / `color` / `keep`
- `duplex`: `one-sided` / `long-edge` / `short-edge` / `keep`
- `queueStatus`: `preview-not-submitted` / `empty` / `1-job` / `N-jobs` / `error`
- `result`: `preview-only` / `submitted` / `submitted-queue-empty` / `failed`

展示给用户时，再翻译成中文自然语言。

示例：

- 打印回执
- 文件：`文档.pdf`
- 打印机：`打印机 1`
- 颜色：黑白
- 份数：1
- 方式：单面
- 纸张：A4
- 队列状态：空
- 结果：任务已提交，当前队列为空，通常表示已被系统接收或快速处理

如果失败：

- 打印回执
- 文件：`文档.pdf`
- 打印机：`打印机 1`
- 结果：提交失败
- 原因：系统没有把任务成功发送到打印机，优先检查文件关联程序或打印机驱动
