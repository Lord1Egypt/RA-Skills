# Excel 通用样式规范（所有广告平台共用）

> 适用范围：Agent 脚本生成的**任何**广告方案 / 周期报告 / 复盘 Excel（Facebook、Google、TikTok、Yandex、BingV2 均适用）。
> 解决的问题：过去 Agent 每次现写单元格样式，效果参差、经常"只有裸文字无样式"。现在统一用本规范 + 配套代码，不再现场发明样式。
>
> **实现**：
>
> - Agent 写方案 / 周期报告脚本 → `import` 同目录 **`excel-style-kit.mjs`**（零依赖，直接 `node xxx.mjs` 可跑，无需 `npm install`）。
> - CLI 内置的 `facebook-analysis render --format xlsx` 已经在用同一套视觉规范（源码 `tso-cli/src/commands/facebook-analysis/xlsx-style-engine.ts`），Agent 不需要关心它，直接跑 CLI 即可。

---

## 一、色板

| 用途                     | 颜色                          | 说明                                             |
| ------------------------ | ----------------------------- | ------------------------------------------------ |
| 主标题条（`titleBar`）  | `#1F2937`（深灰蓝）+ 白字     | 版式固定，**不随平台变化**，保证跨平台视觉统一   |
| 副标题条（`subtitleBar`）/ 说明行（`noteRow`） | `#DEEAF6`（浅蓝）+ `#404040` 深灰字 | 一句话摘要、备注、免责声明               |
| 分区条 / 表头（`sectionBar` / `tableHeader`） | **平台强调色**（见下表）+ 自动对比文字 | 版式规则统一，颜色按平台切换，增强辨识度 |
| 数据行斑马纹              | 白 / `#F2F2F2`                | 交替底色，长表格易读                             |
| 边框                      | `#BFBFBF` 细线                | 所有表格单元格统一细边框                         |
| 正文文字                  | `#262626` 深灰                | 数据行 / 标签默认字色                            |

### 平台强调色（`PLATFORM_ACCENTS`）

| 平台     | accent 参数值 | 颜色      |
| -------- | ------------- | --------- |
| 默认（未指定平台） | `default` | `#1F4E79` |
| Facebook / MetaAd | `facebook` / `metaad` | `#1877F2` |
| Google   | `google`      | `#1A73E8` |
| TikTok   | `tiktok`      | `#FE2C55` |
| Yandex   | `yandex`      | `#FC3F1D` |
| BingV2   | `bingv2` / `bing` | `#0078D4` |
也可以直接传 `"#RRGGBB"` 自定义强调色。分区条 / 表头的文字颜色由亮度自动计算（浅色底配深字、深色底配白字），不需要手动指定对比色。

---

## 二、字体与字号

统一用「微软雅黑」；字号：主标题 16pt，副标题/分区条 10.5～11pt，表头 10pt 粗体，数据 10pt 常规，备注 9pt。

---

## 三、组件（`excel-style-kit.mjs` API）

```js
import { createExcelWorkbook } from "./excel-style-kit.mjs";

const wb = createExcelWorkbook({ accent: "facebook" }); // 或 "google"/"tiktok"/... /"#RRGGBB"
const sheet = wb.addSheet("方案总览");
sheet.setColWidths([20, 60]); // 字符数，两列型表格：标签列窄、内容列宽
```

| 方法 | 用途 | 典型场景 |
| --- | --- | --- |
| `titleBar(text)` | 深色主标题条，整行合并 | Sheet 第一行：客户名 + 方案/报告标题 |
| `subtitleBar(text)` | 浅蓝副标题条 | 一句话摘要（如"原生表单询盘 ｜ 四大洲覆盖"） |
| `sectionBar(text)` | 强调色分区条，居中 | 大章节标题（如"一、公司基本信息"） |
| `noteRow(text)` | 灰底小字，自动按长度换行 | 数据口径说明、免责声明 |
| `tableHeader(headers[])` | 强调色表头行，重置斑马纹计数 | 多列数据表表头 |
| `dataRow(cells[], {textColumns, centerColumns})` | 数据行，自动斑马纹 + 长文本自动换行 | 日趋势 / 国家 / 关键词等列表数据 |
| `kvRow(label, value, {hyperlink})` | 两列型表格一行（标签列高亮加粗） | 客户画像、方案总览这类「项目/内容」表 |
| `blankRow(n)` | 空行分隔 | 章节之间留白 |

`textColumns`：传入需要强制文本格式的列索引（账户/系列/关键词等 **ID 列**），防止 Excel 把长数字转成科学计数法或丢精度——这是与 `agent-conventions.md` 的「ID 列必须写字符串」硬规则配套的实现，**必须**用在任何 ID 列上。

完整用法示例（含超链接、多行文本、ID 列）见 `excel-style-kit.mjs` 文件头注释。

---

## 四、接入方式（各报告模板统一遵守）

写 Excel 的 Agent 脚本，一律：

1. `import { createExcelWorkbook } from "<report-templates 目录>/excel-style-kit.mjs";`（相对路径按脚本实际位置调整，该文件随 skill 一起装到本地）。
2. 用 `accent` 传对应平台标识（见上表色板）。
3. 用组件方法搭版面，不手写单元格 XML / 不裸写 `worksheet.getCell(...).value = ...` 而不设样式。
4. ID 列走 `textColumns`；长文本字段直接传入即可，组件会自动处理换行与行高，不需要手算 `row.height`。

各报告模板落地位置：

| 模板 | Sheet 结构来源 | accent |
| --- | --- | --- |
| `meta-lead-launch-plan-template.md`（Facebook 方案） | **不用本套件**；走 `meta-ad plan-render` 锁死运营 4 Sheet | — |
| `google-period-report-excel.md` | 本文件 | `google` |
| `yandex-period-report-excel.md` | 本文件 | `yandex` |
| `stats-daily-excel.md` | 本文件 | 按 `-m` 媒体参数对应色 |
| `okki-weekly-google-client.md` | **不用本套件**；走 `google-analysis okki-render` 锁死 5 Sheet | `google` |
| `google-inquiry-analysis.md` | 本文件（8 Sheet 固定版式） | `google` |

**注意**：各模板文件里规定的 Sheet 名 / 列名 / 数据口径（业务内容）以各自 `*.md` 为准，本文件只管「怎么好看」，不改「写什么」。
