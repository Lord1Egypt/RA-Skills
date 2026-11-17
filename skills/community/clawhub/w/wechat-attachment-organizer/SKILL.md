---
name: wechat-attachment-organizer
version: 1.0.0
display_name: 微信附件整理（合规版）
display_name_en: WeChat Attachment Organizer (Compliance)
description_zh: 整理 PC 端微信（3.x/4.x，Windows/macOS/Linux 自动探测）聊天附件，按类型或客户分类、去重后复制到指定目录，并可导入资料库全文检索。仅读取本地文件，不解密、不访问聊天数据库。
description_en: Organize PC WeChat (3.x/4.x, auto-detected on Windows/macOS/Linux) chat attachments — classify by type or customer, deduplicate, then copy to a chosen directory and optionally import into the knowledge base for full-text search. Filesystem-only; never decrypts or accesses the chat database.
description: 整理 PC 端微信（Windows/macOS/Linux，3.x 与 4.x 自动探测）聊天中的附件（文档/图片/视频），按类型或客户分类、去重后复制到指定目录，并可导入资料库全文检索。合规版——仅读取本地文件，绝不解密或访问聊天数据库。当用户说"整理微信附件/微信文件分类/把微信收到的文件归类/微信重复文件去重"时使用。
---

# 微信附件整理（合规版）

把微信 PC 端本地存储的附件，按「类型」或「客户」分类，复制到操作者指定的目录。
**合规边界：本 skill 只做文件系统读取与复制，不读取、不解密、不导出聊天数据库（MSGx.db），不解析聊天内容。**

## 适用前提
- 平台：**Windows / macOS / Linux 均自动探测**（微信 3.x 与 4.x 按目录结构自动区分，无需手动指定版本）。若装在非默认位置导致自动探测失败，用 `scan.py --root <账号目录>` 直接指定。
  - Windows 4.x：`%USERPROFILE%\Documents\xwechat_files\<账号>\msg\`；3.x：`...\WeChat Files\<账号>\FileStorage\`
  - macOS 4.x：`~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/<账号>/msg/`；3.x：`.../Application Support/com.tencent.xinWeChat/<版本>/<账号>/FileStorage/`
  - Linux 原生 4.x：`~/Documents/xwechat_files` 或 `~/.xwechat/xwechat_files`；Wine/深度：`~/.wine` 或 `~/.deepinwine` 下的 `drive_c\...\Documents\xwechat_files`
- 源数据：微信本地 `xwechat_files` / `WeChat Files` 下的 `msg/file`、`msg/attach`、图片 `.dat` 等。
- 目标：操作者指定的任意目录（整理结果写在这里，源文件不动）。

## 关键安全规则（必须遵守）
- **复制不移动、不删除源文件。** 默认只做 dry-run 预览，必须显式 `--apply` 才复制。
- 任何"删除/清理原文件"操作都不在本 skill 内自动执行；如需，必须另起对话、明确告知用户风险并走回收站。
- 只写入用户指定的目标目录，绝不在其他位置落盘。
- 涉及个人文件，先扫描预览、让用户确认计划后再执行。

## 第一步：定位与扫描
1. 询问用户微信文件位置；若用户不确定，直接运行扫描脚本自动探测：
   ```
   python3 <本skill目录>/scripts/scan.py --out <工作目录>/wxa_manifest.json
   ```
   多账号时脚本会列出全部账号，用 `--account-filter <子串>` 收窄。
2. 若用户给了自定义根目录：`--root <目录>`。
3. 扫描产出 `wxa_manifest.json`：每条含源路径、真实类型（`.dat` 已 XOR 解码还原）、大小、修改时间、sha256。
4. **可选开关（按场景用）**：
   - `--no-hash`：跳过 sha256 计算，仅做分类/解码/体积统计，速度快几倍。**此模式下 `--dedup` 无法做内容去重**（脚本会跳过无哈希的条目）。适合先出"清单/体积报告"再决定要不要跑完整哈希扫描。
   - `--exclude <doc,image,video>`：跳过某些原始分类。微信 4.x 的 `msg/attach` 图像缓存是哈希分桶、含数百万小文件，全量枚举常耗时数小时；先 `--exclude image` 出文档/视频的报告与整理计划，图像单独后台跑。
   - `--progress-every N`：每 N 个文件向 stderr 打印进度（文件数/体积/速率）。

## 第二步：首次运行询问分类方法
首次运行时，**必须**向用户询问分类方法（之后可记忆到 `<本skill目录>/config.json` 避免重复问）：
- **按类型**：文档/表格/图片/视频/压缩包/音频/其他 + 年-月子目录。最稳，推荐默认。
- **按客户**：需要用户指定一个"目标文档目录"，其下每个子文件夹名即一个客户名。脚本用文件名(L1)+文档正文(L2)匹配；未命中进 `__未归类__/`。
- **自定义**：用户提供规则 JSON（`[{pattern, folder}]`，按文件名/扩展名/路径子串匹配）。

确认后写入 `config.json`：`{"mode": "...", "dest": "...", "custom_rules": "..."}`。

## 第三步：预览（dry-run）
```
python3 <本skill目录>/scripts/organize.py \
  --manifest <工作目录>/wxa_manifest.json \
  --dest <目标目录> --mode <type|customer|custom> \
  [--custom-rules <规则.json>] [--suggest-new] [--dedup]
```
默认只打印计划（每类数量、目标路径树），不写文件。把计划读给用户看。
- **`--dedup`（推荐常开）**：按 sha256 去重。**仅当两个文件哈希值相同才视为重复，绝不比较文件名**。同内容只保留一份（保留非 `.dat` 解码态、修改时间最早者），其余列入 `dedup_report.json`，并提示可节省的空间。**源文件绝不删除**，仅跳过复制。

## 第四步：执行复制
用户确认后加 `--apply` 再跑一次上一条命令（建议同样带 `--dedup`）。脚本会：
- 复制（`.dat` 解码为真实格式后写入，扩展名还原）。去重开启时只复制唯一份。
- 用目标目录 `.wxa_state.json` 记录已处理 sha256，支持增量重跑。
- 生成 `wxa_upload_manifest.json`（本次复制的文件清单，含绝对路径/哈希/类型），供下一步导入资料库。
- 去重开启时额外生成 `dedup_report.json`（重复组：保留哪份、其余原路径在哪）。

## 第五步：新客户确认（仅 customer 模式）
1. 先带 `--suggest-new` 跑一次，列出未归类文件名中的候选新客户名（人工甄别，避免误建）。
2. **发现疑似新客户时，必须问用户是否确认**，确认后才在目标目录建对应子文件夹，并重新运行分类把相关文件归入。
3. 绝不在未经用户确认的情况下自动创建客户目录。

## 第六步：导入资料库全文检索（可选，强烈推荐）
整理+去重后的文件如需跨设备检索、全文搜索（搜文件名/正文关键词），导入 WorkBuddy 资料库最省事：
1. 上一步已生成 `<目标目录>/wxa_upload_manifest.json`，含每个文件的 `abs_path`、哈希、类型、真实扩展名。
2. **加载 `library` skill**，用 `LibraryUpload` 把清单里的文件逐个上传到用户的资料库（个人空间或指定团队空间）。
   - 文本类（pdf/docx/xlsx/txt/md/csv）可被资料库**全文检索**；图片/音视频按文件留存，检索能力取决于资料库对它们的处理。
   - 文件量大时**分批上传**（每批 ≤ 50 个），避免单次过长；上传失败的不阻断其余。
3. 上传完成后告知用户：在资料库内可用文件名或正文关键词搜索；本地的 `wxa_upload_manifest.json` 可作为"已入库清单"留存，便于日后增量比对（已入库的哈希可跳过）。
4. 若用户希望"仅把某类/某客户"入库，先用 `--mode` 整理出对应子目录，再只上传该子目录的文件即可。

> 注意：资料库上传走 WorkBuddy 内置能力，本 skill 不自己实现上传网络请求；是否上传、上传到哪个空间，必须由用户确认。

## 第七步：交付
- 告知用户目标目录结构、文件总数、未归类数量、去重节省的空间（若开启 `--dedup`）。
- 提示：`wxa_manifest.json` 为完整索引（含哈希）；`dedup_report.json` 为重复线索；`wxa_upload_manifest.json` 为入库清单。三者均可留存。
- 提醒源文件仍在原处，清理需另行手动处理。

## 进阶（可选，不在本 skill 内自动做）
- 若需要"按真实发送者归类"而非按文件名/正文猜测，那必须解密聊天数据库——属于另一私有 skill `wechat-db-decrypt`，且不应随本 skill 公开。
