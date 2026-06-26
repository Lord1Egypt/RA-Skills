# 部署前检查清单

所有检查项由 `html_lint` 管线自动执行，无需手动操作。

## body stage 规则（extract_body 后自动运行）

| Rule | 检查内容 | 修复方式 |
|------|----------|----------|
| BodyNotEmpty | 内容不为空 | ❌ 无法修复，阻断部署 |
| DivBalance | div 开闭平衡（排除 script/style） | 尾部移除多余 / 补充缺失 |
| NoDuplicateWrapper | 无重复 report-wrap/page-body | 剥离多余 wrapper（保留第一个） |
| NoFrameworkChrome | 无模板 chrome（header/footer/toc/等） | 正则移除 |
| ImgPathAbsolute | 图片 src 为绝对路径 /images/ | `../images/` → `/images/` |
| ScriptSafety | 无危险 script（cookie/localStorage/eval） | 移除危险 script 标签 |
| TagBalance | 非语义标签闭合平衡 | 尾部补充闭合标签 |
| StyleConflict | 无全局样式覆盖模板 | 冲突选择器加 .page-body 前缀 |

## page stage 规则（generate_page_html 后自动运行）

| Rule | 检查内容 | 修复方式 |
|------|----------|----------|
| PageStructure | html/head/body/report-wrap/page-body/footer/css/js | ❌ 无法修复，阻断部署 |
| PageDivBalance | 完整页面 div 平衡 | </body> 前补充/移除 |
| PageImgIntegrity | 图片文件存在于 dist | 缺失图片替换为 SVG 占位图 |

## 手动补充检查（agent 侧）

- 深色背景配深色文字（视觉检查）
- 配色使用 base.css 变量而非硬编码颜色
- 图表 data-option 声明完整