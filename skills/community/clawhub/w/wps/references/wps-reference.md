# WPS Reference

## 常见文件格式

- 文字：`.doc/.docx`、`.wps`
- 表格：`.xls/.xlsx`、`.et`
- 演示：`.ppt/.pptx`、`.dps`
- 交付：`.pdf`

## 排版优先级（中文文档）

1. 页面设置（纸张、边距、页眉页脚）
2. 样式系统（标题、正文、列表）
3. 字体与字号（中英文字体分离）
4. 分页与目录
5. 图表/图片/批注

## 兼容排查顺序

1. 字体缺失或替换
2. 样式冲突（手工格式覆盖样式）
3. 分页符/分节符异常
4. 对象锚点或文本环绕变化
5. 打印机驱动差异导致分页变化

## 交付检查清单

- 是否保留原始可编辑版本
- 是否导出 PDF 并逐页预览
- 是否清理批注/修订（按交付要求）
- 是否校对目录、页码、页眉页脚一致性

## Headless 转换命令速查

前提：已安装 LibreOffice，且 `soffice` 在 PATH 中（Windows 常见路径为 `C:\Program Files\LibreOffice\program\soffice.exe`）。

```bash
# 单文件转 PDF（输出到当前目录）
soffice --headless --convert-to pdf 报告.docx

# 指定输出目录
soffice --headless --convert-to pdf --outdir ./out 报告.docx

# 批量转换（通配符，Windows 下注意引号与 shell 差异）
soffice --headless --convert-to pdf --outdir ./out *.docx

# docx → pdf 之外，也可互转常见格式
soffice --headless --convert-to docx 旧文档.doc
```

注意：`xlsx → csv` 时 `--convert-to csv` 只导出第一个工作表；多表需逐个处理或改用脚本。
更稳妥的封装（含路径探测、批量、结果汇总）见 `scripts/convert.py`。

## Excel 与 WPS 表格函数兼容差异

| 函数/场景 | Microsoft Excel | WPS 表格 | 建议 |
| --- | --- | --- | --- |
| 动态数组函数（FILTER/SORT/UNIQUE） | 365/2021+ 原生支持 | 旧版本不支持，新版逐步跟进 | 交付前确认对方版本；旧版 WPS 用辅助列 + 传统函数替代 |
| XLOOKUP | 365/2021+ 支持 | 旧版本不支持 | 兼容场景改用 `INDEX + MATCH` |
| LET / LAMBDA | 365 支持 | 支持滞后，多数版本不可用 | 避免在跨软件交付的文件中使用 |
| TEXT 等格式代码 | 跟随系统/区域设置，英文格式码（`yyyy-mm-dd`） | 中文区域下格式码可能不同（如 `e-mm-dd`、`aaaa` 表示星期） | 跨软件/跨区域交付时验证 TEXT 结果，或改用拼接构造文本 |
| 宏 | VBA | 支持 VBA（需专业版/插件）及 WPS JS 宏（JSA） | 含宏文件优先用 `.xlsm` 并注明运行环境；跨软件时重写为 JS 宏需单独验证 |

## 常见中文字体替换映射

| 中文常用叫法 | 实际字体名（文件内引用名） | 备注 |
| --- | --- | --- |
| 宋体 | SimSun / 中易宋体 | Windows 标配 |
| 黑体 | SimHei | Windows 标配 |
| 微软雅黑 | Microsoft YaHei | Windows 标配 |
| 楷体 | KaiTi | Windows 标配 |
| 仿宋 | FangSong | 公文常用 |

Linux 下缺少上述字体时，常被替换为 Noto Sans CJK / 文泉驿（WenQuanYi）系列；
替换后字面宽度不同，会导致分页与换行漂移。交付 PDF 前务必在目标环境逐页预览，或改用嵌入字体导出。
