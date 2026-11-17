---
name: wechat-file-organizer
slug: wechat-file-organizer
displayName: 微信文件自动归类
version: 2.1.0
category: office-efficiency
subCategories: [office-automation, office-doc]
license: MIT
platforms: [WorkBuddy, Claude Code, Codex]
description: 微信文件自动归类（无头版）——扫描微信接收文件目录，按类型/月份归类、去重、生成报告。零依赖、默认只读（dry-run）、绝不永久删除源文件。扫描逻辑与 GUI 应用 wechat-file-organizer-gui（main.py）同步。
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
- **安全优先**：默认 `dry-run`（只读），**绝不改动任何源文件**；只有显式加 `--apply` 才复制。
- **清理可恢复**：`--trash` 只会把源文件移入回收站/废纸篓（可恢复），**绝不永久删除**；Linux 不支持则跳过不删。
- **多账号合并扫描**：自动探测本机所有微信文件根目录（新版 `xwechat_files` 与旧版 `WeChat Files` 可并存），
  一次扫齐全部账号，报告与 JSON 标注每个文件属于哪个账号。
- **多平台**：Windows / macOS / Linux；macOS 自动探测微信沙盒目录（`com.tencent.xinWeChat` 容器）。
- **实用能力**：按类型/月份归类、内容去重（sha256）、最大文件排行、老旧文件统计、JSON 输出。

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
| `--lang zh\|en` | 报告语言；CLI > 环境变量 `WFO_LANG` / `WECHAT_ORG_LANG` > 系统语言 > 中文 |

### 多语言（简体中文 / English）

报告、`--help`、JSON 字段与归类出来的子目录名（`文档/` ↔ `Documents/`）全部走 `scripts/i18n.py`
词条包。新增语言只需在 `STRINGS` 中补一列 + `join_list()` 提供本地分隔符。

```bash
python scripts/organize.py --lang en   # English
WFO_LANG=en python scripts/organize.py # 或用环境变量
```

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
| 源文件被误改？ | 不会发生——`--apply` 是复制；`--trash` 是移入回收站（可恢复），任何平台都不永久删除 |

## 安全与隐私

- 完全本地运行，**不上网、不读任何凭据、不访问微信账号**。
- 只读扫描 + 复制输出；清理源文件一律走回收站/废纸篓（可恢复），绝不永久删除。
- 适合在任何环境下分发使用。

## 与 GUI 版的关系（保持同步）

| 能力 | 无头脚本 `organize.py` | GUI 应用 `main.py` |
|---|---|---|
| 目录探测（多根/新版/旧版/mac 沙盒） | ✅ | ✅ |
| 多账号合并扫描 + 账号归属 | ✅ | ✅ |
| 按类型/月份归类、去重 | ✅ | ✅ |
| 清理源文件移入回收站（可恢复） | ✅ `--trash` | ✅ 界面勾选 |
| 图片缩略图预览 / 向导式界面 / 检查更新 | ❌ | ✅（GUI 独有） |
| 微信加密文件备份（收藏/附件） | ❌ | ✅（GUI 独有） |

> 两边的扫描/归类/回收站逻辑需保持一致；改动时优先同步 `main.py`，再回填本脚本。

## 复建依据

若 `scripts/organize.py` 丢失，本 SKILL.md 已完整描述接口与参数；最稳妥的方式是从
源仓库 `oracis/wechat-file-organizer-gui` 的 `main.py` 中提取扫描逻辑重建（见上面
「与 GUI 版的关系」对照表）。
