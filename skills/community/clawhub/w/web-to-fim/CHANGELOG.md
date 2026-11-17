# Changelog

本文件记录 web-to-fim 技能的版本演进。版本号遵循 [语义化版本](https://semver.org/)。

## [3.7.0] - 2026-07-18

### 🚨 破坏性变更（飞书 wiki 抓取方式改造）

**问题根因**：v3.6.0 及更早版本抓取飞书 wiki（`*.feishu.cn/wiki/`）内容时使用 WebFetch，但 WebFetch 对飞书 wiki 页面抓取不稳定，常返回 200-1000 字符截断内容（完整文章应有 3K-25K 字符）。

**实测数据**：第十批 33 篇飞书 wiki 文章批量转录任务中，19 篇被 WebFetch 截断，导致飞书云盘上保存的 .md 文件内容大量丢失，用户反馈"多个文件都只转录了一小点，很多文章都没有转录完成"。

**修复方案**：飞书 wiki 抓取改用 `lark-cli docs +fetch --doc <url> --doc-format markdown --scope full` 获取完整内容。lark-cli 通过用户身份认证，直接调用飞书 OpenAPI 读取结构化文档内容，无 JS 渲染或登录认证问题。实测 33 篇文章全部完整获取（800-24000 字符，部分短文如活动公告本身即短）。

### 变更
- **`web_to_md.py` 新增 `_convert_feishu_wiki()` 函数**：调用 lark-cli docs +fetch 获取飞书 wiki 完整 Markdown 内容
- **`_detect_source()` 新增 `feishu_wiki` source 类型**：识别 `feishu.cn/wiki` 和 `larkoffice.com/wiki` URL
- **`convert()` 函数新增 feishu_wiki 分支**：自动路由到 `_convert_feishu_wiki()`
- **`web_to_all.py` `_process_single()` 飞书 wiki 原文链接优先转录流程更新**：
  - 飞书 wiki 内容已通过 lark-cli 完整获取（不再依赖 WebFetch）
  - 检测到原文链接时，自动用 markitdown 或 x-tweet-fetcher 抓取原文
  - 原文比飞书 wiki 内容长则覆盖，否则保留飞书 wiki 内容
  - 公众号/普通网页原文：v3.7.0 改为自动 markitdown 抓取（v3.6.0 是仅打印提示让 AI 调用 WebFetch）

### 弃用
- **WebFetch 抓取飞书 wiki**：v3.7.0 起弃用。`_fetch_feishu_wiki_via_webfetch()` 保留但不再调用，仅作历史参考。AI 流程中遇到飞书 wiki URL 不应再调用 WebFetch，应让 `web_to_md.py convert()` 自动路由到 lark-cli。

### 验证
- ✅ 第十批 33 篇飞书 wiki 文章全部完整转录（v3.6.0 时 19 篇截断）
- ✅ 飞书云盘 33 个 .md 文件内容完整（抽查 5 篇 19007/24247/1080/17160/10010 字符）
- ✅ Obsidian `E:\Obsidian-Vault\00-Inbox\` 33 个 20260718-*.md 文件全部完整
- ✅ lark-cli docs +fetch 对各种长度飞书 wiki 都稳定（最短 793 字符，最长 23931 字符）

## [3.6.0] - 2026-07-18

### 🚨 破坏性变更（飞书存储方式改造）

**问题根因**：v3.5.0 及更早版本飞书存储用 `FeishuClient.create_document` 创建在线 docx，使用应用身份（tenant_access_token），文档归属应用而非用户。用户反馈"这几天转换的文档一篇都没有看到"——文档创建成功但用户在飞书"我的空间"完全不可见。

**修复方案**：飞书存储改用 `lark-cli drive +upload` 上传 .md 原文件到用户云盘根目录（用户身份，user_access_token），文件归属于用户，立即可见。参考 transcript-crafter 技能的存放方式。

### 变更
- **`save_to_feishu()` 函数签名变更**：`(content: str, title: str)` → `(md_file_path: str, title: str = None)`
  - 不再接收 markdown content，改为接收本地 .md 文件路径
  - 飞书上传依赖 Obsidian 保存的 .md 文件作为源
- **`web_to_all.py` 不再 import `FeishuClient`**：避免触发 deprecation warning
- **`_process_single()` 调用顺序变更**：先存 Obsidian 得到文件路径，再上传飞书。Obsidian 失败时飞书自动跳过（提示 `Feishu skipped: Obsidian file not available`）
- **`save_fetched.py` 调用变更**：传 `obs_path` 给 `save_to_feishu()`，不再传 content
- **`feishu_client.py` 标记为废弃**：保留供历史参考，主流程不再调用。导入时触发 `DeprecationWarning`

### 新增
- **lark-cli 依赖**：飞书存储改为依赖 `lark-cli`（npm 全局包），需预先 `lark-cli auth login` 用户授权
- **临时文件复制机制**：lark-cli `--file` 限制必须是 cwd 下相对路径，代码会自动把 Obsidian .md 文件复制到 scripts 目录上传，上传后立即删除
- **JSON 输出解析**：lark-cli 输出多行 JSON（含 `Uploading:` 提示行），用 `find('{')` 到 `rfind('}')` 提取完整 JSON 段

### 废弃
- **`FEISHU_APP_ID` / `FEISHU_APP_SECRET` 环境变量**：不再使用，飞书凭证由 lark-cli 管理
- **`feishu_client.py`**：保留但已废弃，详见文件头 DEPRECATED 注释

### 验证
- ✅ 测试上传成功：文件 URL `https://aipeanut.feishu.cn/file/ZZ4ibHqj2obC4wxzxNgcY5znnPf`
- ✅ 文件归属用户身份，飞书"我的空间 > 云盘"立即可见
- ✅ Obsidian 失败时飞书正确跳过，不影响其他存储

## [3.5.0] - 2026-07-18

### 新增
- **Obsidian 文件命名升级**：从 `YYYYMMDD-标题-来源.md` 升级为 `YYYYMMDD-标题-关键信息.md`
  - 关键信息由 AI 从标题和内容提取 2-4 个关键词，用顿号"、"分隔
  - 示例：`20260718-数字人口播实战攻略-数字人、口播、heygen.md`
  - 未提供 keywords 时 fallback 到来源（waytoagi/wechat/x/github）
- **CLI 新增 `--keywords` 参数**：`python web_to_all.py --url <url> --keywords "数字人、口播、heygen"`
- **`save_fetched.py` JSON 配置新增 `keywords` 字段**：批量模式支持每篇文章独立关键词
- **`save_to_obsidian()` 新增 `keywords` 参数**：编程接口支持
- **默认 Obsidian Vault 路径变更**：`E:\Obsidian\md\inbox` → `E:\Obsidian\md\00-Inbox`（与 Obsidian Vault 结构对齐）

### 兼容性
- 未传 `keywords` 参数时 fallback 到原"来源"逻辑，向后兼容
- 已存在的旧命名文件不强制改名（遵循 NAMING-CONVENTIONS.md "已存在的文件不强制改名"原则）

## [3.4.0] - 2026-07-12

### 安全修复（ClawHub SkillSpector v3.3.0 findings）
- **删除误上传的临时脚本**：`_gh_push.py` 和 `_gh_release.py`（v3.3.0 发布时误上传，含 GitHub token 读取和 API 调用，被标记为 MCP Tool Poisoning / Context-Inappropriate Capability）
- **新增权限声明段落**：MCP Least Privilege — 明确声明文件读取/写入/网络请求/环境变量/subprocess 权限
- **新增用户警告段落**：Missing User Warnings — 明确告知数据外传到飞书/IMA、本地写入、选择性禁用参数
- **修正安全声明**：Intent-Code Divergence — 移除"仅在用户明确指定时写入文件"的错误描述，改为"默认写入 Obsidian Vault"
- **触发词收窄**：Vague Triggers — 移除过于宽泛的"转文档"、"网页转文档"，改为更明确的"抓网页存飞书"、"web to feishu"等
- **Do NOT 范围扩展**：新增"普通文档格式转换（非三处存放意图）"

### 功能修复（X 链接转录流程）
- **X 链接转录流程修正**：飞书 wiki 中发现 X 原文链接时，用 x-tweet-fetcher 抓取完整长文（10K-15K 字符），不用 WebFetch（超时失败率高）
- **降级机制**：x-tweet-fetcher 失败时降级到飞书 wiki 内容
- **全文完整性验证**：转录后检查内容长度，<500 字符时警告可能不完整
- **内容长度对比**：X 原文内容比飞书 wiki 内容长时才替换，否则保留飞书 wiki 内容

## [3.3.0] - 2026-07-12

### 新增
- **原文链接自动提取**：`extract_original_url()` 函数从 Markdown 前 800 字符自动识别"原文链接"/"转载自"/"本文首发"等关键词
- **IMA 路由精细化**：GitHub URL 改为纯文本笔记（IMA 抓取 HTML 页面效果差），不再走 import_urls
- **飞书 wiki 自动路由函数**：`_is_feishu_wiki()` 和 `_fetch_feishu_wiki_via_webfetch()` 新增

### 修复
- **IMA 路由规则修正**：原文链接为 GitHub 时，原逻辑走 import_urls 导致 IMA 抓取 HTML 页面内容混乱。改为纯文本笔记存转录 MD
- **路由规则文档化**：IMA 路由规则精细化（公众号/普通网页→import_urls；X/Twitter/飞书/GitHub→纯文本笔记）

## [3.2.0] - 2026-07-12

### 新增
- **Obsidian 文件命名规范化**：`YYYYMMDD-标题-来源.md`（如 `20260712-歸藏：GPT-5.6 Sol 帮我做了个小工具-waytoagi.md`）
- **来源自动提取**：`_extract_source_name()` 函数从 URL 域名提取来源标识（waytoagi/feishu/x/wechat/weibo/xiaohongshu/github/youtube/webpage）
- **飞书 wiki 原文链接优先转录**：抓取飞书 wiki 后检查文章头部"原文链接"，有则优先抓取原文内容（公众号/X 等），获得更完整的正文和图片
- **IMA 智能路由优化**：飞书 wiki 有公众号原文链接 → import_urls（保留图片）；无原文链接 → 纯文本笔记

### 修复
- Windows 文件名安全：禁止字符（`\ / : * ? " < > |`）替换为下划线，中文标点（含 `：`）保留
- 文件名长度限制：标题超过 60 字符自动截断，避免文件名过长

## [3.1.0] - 2026-07-11

### 新增
- 批量模式断点恢复：自动生成 `.progress.json` 进度文件，崩溃后重跑自动跳过已完成 URL，全部成功后自动清理
- Obsidian frontmatter 增加 `tags` 字段：根据 URL 来源自动分类标签（x-twitter/wechat/weibo/xiaohongshu/github/youtube/webpage/local-file）
- `save_to_obsidian` 三级 fallback 机制：重试 3 次 → ASCII 文件名 → 脚本目录 `saved/`
- `_process_single` 每个存储操作独立 try/except：一处失败不阻断其他存储

### 修复
- **Critical**: `tweet_to_md.py` 去掉硬编码的段落标题列表，改为通用启发式规则（Emoji 模式匹配 + 数字编号 + 短行特征 + 技术名词后缀）
- **Critical**: `web_to_md.py` `_run()` 函数加 120 秒 timeout，防止 x-tweet-fetcher 网络异常时永久挂起
- **Important**: `_fetch_wechat_mobile()` 改进正文提取：保留图片（data-src）、段落结构（`<p>`/`<section>`）、引用块（blockquote），不再丢失内容
- **Minor**: 标题提取改进：支持从 frontmatter `title:` 提取，fallback 到 URL 域名生成标题，不再出现 `Untitled`
- **Minor**: `import time` / `import json` 移到文件顶部
- **Minor**: `.gitignore` 补充 `saved/`、`batch_urls.txt`、`*.progress.json`、`batch_run.log` 等临时文件

## [3.0.2] - 2026-07-11

### 修复
- 同步本地版本号与 ClawHub 线上版本（本地从 3.0.1 对齐到 3.0.2）
- 修复 SKILL.md 安全声明章节的 Markdown 语法瑕疵：
  - 第 261 行 `--no-ima` 反引号缺失
  - 第 258 / 263 / 268 行 `**文件操作` / `**隐私保护` / `**权限透明` 加粗未闭合

### 文档
- 新增 CHANGELOG.md，补齐版本演进记录

## [3.0.1] - 2026-07-11

### 修复
- 更新 ClawHub 页面 Short summary，反映 v3.0 的信源与存储能力
  - frontmatter description 增加公众号/网页图片保留、飞书 wiki 转录说明
  - 信源表标注 IMA 存储路由（IMA 笔记 → IMA 知识库）

## [3.0.0] - 2026-07-10

### 新增
- **IMA 智能路由**：公众号/普通网页 → `import_urls` 服务端抓取，保留原文图片和排版
- **飞书 wiki 信源**：通过 WebFetch 转录飞书知识库文章全文
- **公众号反爬 fallback**：markitdown 返回验证页时自动切换移动端 UA 重试
- **批量模式**：`--urls-file` 参数支持从文件逐行读取 URL 批量处理
- **试运行模式**：`--dry-run` 参数仅转 Markdown 不入库

### 变更
- **IMA API 迁移到 v1.1.7**：创建笔记改用 `/openapi/note/v1/import_doc`
- **IMA 存储从"笔记本"改为"知识库"两步流程**：
  1. `create_note` 创建笔记（Notes API）
  2. `add_note_to_knowledge_base` 添加到知识库（Wiki API）
- **环境变量更名**：`IMA_CLIENT_ID` / `IMA_API_KEY` → `IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`（旧名仍兼容回退）
- X/Twitter 链接强制走纯文本笔记逐字转录，不使用 `import_urls`

### 安全
- 凭证全部通过环境变量配置，无硬编码
- 清理临时脚本中的真实 IMA 凭证
- 完善 .gitignore 排除规则
