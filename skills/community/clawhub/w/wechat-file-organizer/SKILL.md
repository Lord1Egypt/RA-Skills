---
name: wechat-file-organizer
slug: wechat-file-organizer
displayName: 微信文件自动归类
version: 2.3.0
category: office-efficiency
subCategories: [office-automation, office-doc]
license: MIT
platforms: [WorkBuddy, Claude Code, Codex]
allowed-tools: Bash Read Write env
description: 微信文件自动归类（无头版）——扫描微信接收文件目录，按类型/月份归类、去重、生成报告；支持 JSON 规则自定义归类（按文件名/路径/扩展名）与单文件 HTML 可视化报告（内嵌 CSS+SVG，无外部依赖）。零依赖、默认只读（dry-run）；清理源文件优先移入系统回收站/废纸篓，不提供永久删除选项。扫描逻辑与 GUI 应用 wechat-file-organizer-gui（main.py）同步。
type: skill
---

# 微信文件自动归类 (wechat-file-organizer) — 无头版

## 何时使用

当用户表达以下意图时加载本 skill：
- 「整理微信接收的文件」「微信文件太乱了」「微信文件归类」
- 「微信里重复文件好多」「清理微信下载的文件」
- 「帮我看看微信都收了些什么文件 / 占了多少空间」

本 skill 调用随附的 `scripts/organize.py` 完成，无需安装任何第三方依赖。

> **有图形界面版本**：`wechat-file-organizer-gui`（GitHub `oracis/wechat-file-organizer-gui`，
> Releases 提供 Windows `exe` 与 macOS `.pkg`/`.zip`）。用户只想「点一点」就用 GUI；
> 本脚本用于**无头/定时任务/自动化**场景，两者扫描与归类逻辑已同步到同一版本。

## 核心特性

- **零依赖**：仅用 Python 标准库，无 `pip install`。
- **安全优先**：默认 `dry-run`（只读，不改动任何源文件）；只有显式加 `--apply` 才复制。
- **清理走回收站**：`--trash` 通过系统回收站/废纸篓语义删除源文件（Windows `SHFileOperationW` 带 `FOF_ALLOWUNDO`、macOS Finder delete），
  脚本不调用任何永久删除 API；操作失败会明确报告、不再继续。Linux 无可靠回收站接口则跳过不删。
  注意：回收站能否最终恢复取决于操作系统与目标卷（如部分网络位置可能不支持回收站），重要文件请先自行备份。
- **多账号合并扫描**：自动探测本机所有微信文件根目录（新版 `xwechat_files` 与旧版 `WeChat Files` 可并存），
  一次扫齐全部账号，报告与 JSON 标注每个文件属于哪个账号。
- **多平台**：Windows / macOS / Linux；macOS 自动探测微信沙盒目录（`com.tencent.xinWeChat` 容器）。
- **实用能力**：按类型/月份归类、内容去重（sha256）、最大文件排行、老旧文件统计、JSON 输出。
- **自定义规则（v2.2.0+）**：`--rules rules.json` 按文件名 glob / 正则 / 全路径 / 扩展名映射到任意目录，
  先命中先生效；支持 `{month}` `{year}` `{account}` `{cat}` `{ext}` `{name}` 占位符。
- **HTML 可视化报告（v2.2.0+，v2.3.0 全新改版）**：`--html report.html` 生成单文件报告，
  数据新闻（Fathom）风格版式——暖纸底/深墨底双主题自适应、衬线大数字、章节编号与细线分隔，
  内嵌 CSS + 内联 SVG 柱状图，含 6 数字带、类型分布、扩展名排行、月份趋势、重复明细、规则命中、Top N；
  无 CDN、无外部 JS/字体，断网可开。

## 如何运行

脚本位置：`scripts/organize.py`（本 skill 目录内）。

```bash
# 1) 先看报告（默认只读，安全，自动多账号合并扫描）
python scripts/organize.py

# 2) 按「类型 + 月份」归类并复制（不动源文件，复制到新目录）
python scripts/organize.py --apply --scheme type-month

# 3) 去重后归类（相同内容只留一份）
python scripts/organize.py --apply --dedupe

# 4) 归类后顺手清理源文件（移入回收站，可恢复；Linux 自动跳过）
python scripts/organize.py --apply --trash

# 5) 机器可读输出（定时任务/脚本消费，含账号归属）
python scripts/organize.py --json

# 指定目录（不自动探测时）
python scripts/organize.py --source "/path/to/xwechat_files" --apply

# 按自定义规则归类（先复制 rules.example.json 再改）
python scripts/organize.py --apply --rules rules.example.json

# 生成单文件 HTML 可视化报告（可与任意模式组合，不改动源文件）
python scripts/organize.py --html report.html
python scripts/organize.py --apply --rules rules.example.json --html report.html
```

### 参数速查

| 参数 | 说明 |
|---|---|
| `--source DIR` | 微信根目录；默认自动探测本机**所有**微信目录（多账号合并） |
| `--dest DIR` | 归类输出目录；默认在 source 同级建 `WeChatFiles_Organized` |
| `--scheme` | `type`（默认）/ `month` / `type-month` |
| `--apply` | 真正复制归类（**不加则只出报告**） |
| `--trash` | 配合 `--apply`：复制成功后把源文件移入回收站/废纸篓（可恢复，Linux 跳过） |
| `--dedupe` | 去重，相同内容只保留一份（配合 `--apply`） |
| `--include-media` | 连 Image/Video 的 `.dat` 也处理（默认跳过） |
| `--scan-all` | 扫描 FileStorage 全部子目录（图片/视频/语音等） |
| `--top N` | 列出最大的前 N 个文件（默认 10，0 关闭） |
| `--old-days N` | 超过 N 天的文件计为老旧（默认 365） |
| `--json` | 输出 JSON（含 `accounts` 账号列表与逐文件账号归属） |
| `--rules FILE` | 自定义归类规则 JSON 文件（见下节），命中规则时覆盖 `--scheme` |
| `--html FILE` | 生成单文件 HTML 可视化报告（纯输出，不改动源文件） |
| `--lang zh\|en` | 报告语言；CLI > 环境变量 `WFO_LANG` / `WECHAT_ORG_LANG` > 系统语言 > 中文 |

### 多语言（简体中文 / English）

报告、`--help`、JSON 字段与归类出来的子目录名（`文档/` ↔ `Documents/`）全部走 `scripts/i18n.py`
词条包。新增语言只需在 `STRINGS` 中补一列 + `join_list()` 提供本地分隔符。

```bash
python scripts/organize.py --lang en   # English
WFO_LANG=en python scripts/organize.py # 或用环境变量
```

## 自定义归类规则（`--rules`）

随 skill 附带 `rules.example.json`，复制后按需修改。**先命中先生效**，未命中任何规则的文件仍按
`--scheme` 归类。规则文件是 UTF-8 JSON：

```json
{
  "version": 1,
  "rules": [
    {
      "name": "财务发票",
      "match": {"glob": ["*发票*", "*invoice*"]},
      "dest": "财务/发票/{month}"
    },
    {
      "name": "合同协议",
      "match": {"regex": "(?i).*(合同|协议|contract).*", "ext": ["pdf", "doc", "docx"]},
      "dest": "法务/合同/{year}"
    },
    {
      "name": "项目A",
      "match": {"path_glob": "*项目A*"},
      "dest": "项目/项目A/{account}/{month}"
    }
  ]
}
```

**`match` 字段**（同一规则内多个字段取 AND，同字段内多个值取 OR）：

| 字段 | 匹配对象 | 说明 |
|---|---|---|
| `glob` | 文件名 | `fnmatch` 通配符，如 `*发票*`、`*.pdf` |
| `regex` | 文件名 | Python 正则，支持 `(?i)` 忽略大小写 |
| `path_glob` | 完整路径（小写 + `/` 分隔） | 按路径归类，如 `*项目A*` |
| `ext` | 扩展名 | 不带点或带点均可，大小写不敏感 |

**`dest` 占位符**：`{month}`（YYYY-MM）、`{year}`、`{account}`、`{cat}`（当前语言的原类别名）、
`{ext}`、`{name}`（去掉扩展名的文件名）。

**安全**：`dest` 中 `..`、绝对路径、Windows 非法字符会被清洗，产物始终位于 `--dest` 目录内。
规则文件 JSON 非法 / 格式错误 / 正则无效会立即报错并退出（exit 2），不会开始归类。

## HTML 可视化报告（`--html`）

`--html report.html` 生成单文件报告，可单独用，也可与 `--json`、`--apply`、`--rules` 任意组合。

**版式（v2.3.0 起）**：数据新闻 / Fathom Information Design 风格——报头（kicker + 衬线大标题 +
斜体副标题 + 元信息）、6 格数字带（重复组与可回收空间用朱红强调）、6 个带编号章节（01–06）
以细分隔线串联，拒绝圆角卡片堆叠。字体走系统栈（衬线标题 + 无衬线正文 + 等宽路径），
不加载任何在线字体。跟随系统 `prefers-color-scheme` 自动切换暖纸浅色 / 深墨深色双主题。

内容：6 数字带（文件数/总大小/账号数/重复组/可回收空间/老旧文件）、类型分布条形、
**扩展名排行**（从实际文件动态统计，按数量排序，含每个扩展名的文件数/大小/大小占比；
大小写自动归一，中文扩展名与无扩展名文件也能正确归类，无预设清单，适配任何人的文件集）、
月份柱状图（内联 SVG，双行标注「数量 · 体积」）、重复文件明细（每组可展开看全部路径）、
规则命中统计（使用 `--rules` 时显示）、Top N 大文件。所有路径都做 HTML 转义，**无任何外部资源引用**。

**搜索**：报告顶部有搜索框，输入关键词实时过滤所有表格行（文件名/路径/扩展名/账号），
匹配文本高亮并显示命中行数；命中的重复文件组自动展开。按 `/` 快速聚焦、`Esc` 清空。纯前端实现。

**点击打开文件**：重复明细与 Top N 里的路径是 `file://` 链接，在浏览器里直接双击 HTML 打开时，
点击即可用系统默认程序打开源文件（中文/空格/`#` 自动编码）。每个路径旁的「复制」按钮可复制原始路径。
注意：若通过 http 预览面板（如 WorkBuddy 右侧预览）查看，浏览器**禁止 http 页面打开 file://**，
报告会自动显示提示条，此时需用「复制」按钮粘贴到资源管理器地址栏，或把 HTML 下载后用浏览器直接打开。

## 路径发现逻辑

1. 若设了 `WECHAT_FILES_DIR` 且存在，优先用。
2. 否则自动探测**所有**微信文件根目录，覆盖：
   - 新版微信：`~/Documents/xwechat_files`（文件在 `<账号>/msg/file/YYYY-MM`）
   - 传统微信：`~/Documents/WeChat Files`、`Weixin Files`（文件在 `<账号>/FileStorage/File`）
   - macOS 沙盒：`~/Library/Containers/com.tencent.xinWeChat/.../com.tencent.xinWeChat/<版本>/<账号哈希>`（文件在 `Message/MessageTemp/<会话>/File|Image|Video|Audio`）
   - 自定义路径：有限深度扫描 `~/Documents` 下含 `FileStorage`/`msg` 特征的目录
3. 多账号会全部处理，且每个文件标注所属账号。

> 微信把接收文件按 `File/YYYY-MM/文件名`（新版为 `msg/file/YYYY-MM`）平铺存放，
> 所有发送者混在一起，这正是本 skill 要解决的痛点。图片/视频在 `Image/`、`Video/`
> 里是加密的 `.dat`，默认跳过（可用 `--include-media` / `--scan-all` 纳入）。

## 故障处置

| 现象 | 原因 / 处理 |
|---|---|
| `[FAIL] 找不到微信文件目录` | 微信不在默认位置，用 `--source` 指定，或设 `WECHAT_FILES_DIR` |
| 报告里没有图片/视频 | 默认跳过 `.dat`；加 `--scan-all` 或 `--include-media` |
| 想真正移动（而非复制）以腾空间 | 用 `--apply --trash`：先复制归类，确认无误后再把源文件移入回收站（可恢复） |
| 源文件被误改？ | `--apply` 只复制不改源文件；`--trash` 走系统回收站语义，失败会报告，重要文件建议先自行备份 |

## 安全与隐私

- 完全本地运行，**不上网、不读任何凭据、不访问微信账号**。
- 只读扫描 + 复制输出；`--trash` 清理走系统回收站/废纸篓语义，脚本不调用永久删除 API，失败会报告。
  能否从回收站恢复取决于操作系统与目标卷，重要文件请先自行备份。
- 使用的本地能力：读取环境变量（`WECHAT_FILES_DIR` / `WFO_LANG`）、读写文件与目录、调用系统命令
  （仅 macOS 回收站 `osascript` / Windows `ctypes` 回收站接口）；不联网、不读取微信凭据。已在 frontmatter
  `allowed-tools` 中声明 `Bash`（shell）、`Read`（file_read）、`Write`（file_write）、`env`（env）。
- 适合在任何环境下分发使用。

## 与 GUI 版的关系（保持同步）

| 能力 | 无头脚本 `organize.py` | GUI 应用 `main.py` |
|---|---|---|
| 目录探测（多根/新版/旧版/mac 沙盒） | ✅ | ✅ |
| 多账号合并扫描 + 账号归属 | ✅ | ✅ |
| 按类型/月份归类、去重 | ✅ | ✅ |
| 清理源文件移入回收站（可恢复） | ✅ `--trash` | ✅ 界面勾选 |
| 自定义规则归类（glob/正则/路径） | ✅ `--rules`（v2.2.0+） | ❌（无头版独有） |
| HTML 可视化报告 | ✅ `--html`（v2.2.0+） | ❌（无头版独有） |
| 图片缩略图预览 / 向导式界面 / 检查更新 | ❌ | ✅（GUI 独有） |
| 微信加密文件备份（收藏/附件） | ❌ | ✅（GUI 独有） |

> 两边的扫描/归类/回收站逻辑需保持一致；改动时优先同步 `main.py`，再回填本脚本。

## 复建依据

若 `scripts/organize.py` 丢失，本 SKILL.md 已完整描述接口与参数；最稳妥的方式是从
源仓库 `oracis/wechat-file-organizer-gui` 的 `main.py` 中提取扫描逻辑重建（见上面
「与 GUI 版的关系」对照表）。
