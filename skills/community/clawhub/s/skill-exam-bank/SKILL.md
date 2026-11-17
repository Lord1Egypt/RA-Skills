---
name: exam-bank-convert
description: 试卷转题库：真题 PDF/图片 → 内网 exam-ocr(:8000, RapidOCR) 解析 → 抽取成 17 列表头题库 Excel。适用于"把真题转成题库/excel""整理试卷成题库""PDF 真题入库"。来源：OpenClaw「真题转题库」技能的本地化版本（2026-09-08 生成，2026-09-09 迁移到 WorkBuddy）。
version: 1.4.0
updated: 2026-09-09
---

## 版本记录
- **1.4.0**（2026-09-09）归档路径参数化：新增 `archive.py`，归档目录由调用方用 `--to` 或环境变量 `EXAM_BANK_ARCHIVE_DIR` 指定，未指定则跳过归档；技能不再内置任何固定路径，便于分发给外部用户
- **1.3.0**（2026-09-09）OCR 改走异步队列：`/parse-async` + 轮询 `/task/{id}`，`--owner` 跨用户公平轮转（单用户上限 20、结果保留 1h、并发不阻塞）；`--sync` 可退回同步 `/parse`；新增 NAS 题库归档规范
- **1.2.0**（2026-09-09）解析列必填：客观题写依据+干扰项错因，主观题写得分要点；知识点与年份规则沿用
- **1.1.0**（2026-09-09）年份列改填具体考期 `2026年4月` 格式（原为纯年份 2026）；auto_run 的 `--month` 参数接通
- **1.0.0**（2026-09-08）初版：PDF → exam-ocr OCR → LLM 抽取 → 17 列 Excel，含漏题自检

# 试卷转题库（真题 PDF → 17 列 Excel 题库）

## 环境（已就绪，2026-09-09 验证）
- OCR/写表服务：exam-ocr（Docker，提供 `/parse-async`/`/task/{id}`/`/write-excel`）；**地址由环境变量 `EXAM_OCR_URL` 提供**，示例 `http://<服务IP>:8000`（本技能不内置固定地址）
- Python：`C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`（venv 已装 requests）
- 脚本在本技能目录：`parse_ocr.py` / `write_excel.py` / `check_missing.py` / `auto_run.py` / `archive.py`（可选归档）
- **排队机制（v0.4.0，2026-09-09 起服务端已支持）**：`parse_ocr.py` 默认走异步 `/parse-async` + 轮询 `/task/{id}`，多智能体并发时按 owner 公平轮转、不阻塞；`--owner <名>` 标识调用方（本机建议 `--owner workbuddy`）；加 `--sync` 退回同步 `/parse`。单 owner 队列上限 20（超了返回 429），结果保留 1 小时

## 17 列表头（锁死，与题库系统模板一致）
```
课程 | 知识点 | 题型 | 题目内容 | 选项A | 选项B | 选项C | 选项D | 选项E
正确答案 | 难度 | 状态 | 是否真题 | 是否模拟试卷 | 是否考前押题 | 年份 | 解析
```
- 题型：单选/多选/判断/填空/简答/计算/论述；客观题填选项与正确答案，主观题留空选项、正确答案写要点
- 是否真题=是；状态=启用；是否模拟试卷/是否考前押题=否；**年份列填具体考期「2026年4月」格式**（同课程同年 4/10 两套卷需能区分，禁止只填纯年份；auto_run 用 --year 2026 --month 4）
- **解析列必填，不得留空**：客观题写 1~3 句——说明正确项为什么成立 + 主要干扰项错在哪；主观题写得分要点（3~5 条）；不照抄题干原文，不写"见教材第X页"这类无信息量的话
- 抽取时每条额外带整数 `题号`（供漏题自检，写 xlsx 时自动丢弃）

## 方式 A：WorkBuddy 自己抽取（推荐，无需 DeepSeek key）
1. OCR：
   ```
   EXAM_OCR_URL="$EXAM_OCR_URL" <python> parse_ocr.py <试卷> <试卷>.ocr.md --owner <你的标识>
   ```
   （默认异步排队，脚本自动提交并轮询；要退回同步加 `--sync`）
2. 语义抽取：由 WorkBuddy（当前对话中的 LLM）直接读 OCR markdown 完成——
   - 按下方【抽取 Prompt】把每题抽成 JSON 记录（含 题号，全局连续编号），写 `<试卷>.json`
   - 注意答案在卷尾"参考答案"区，务必关联；跨页大题按阅读顺序合并
   - OCR 双栏交错时先按题号重排阅读顺序再抽
3. 写 Excel：
   ```
   <python> write_excel.py <试卷>.json <输出.xlsx> --url "$EXAM_OCR_URL"
   ```
4. 漏题自检（强制）：`<venv python> check_missing.py <试卷>.json <试卷>.ocr.md`，退出码 1=缺题
5. 缺题则带着缺失列表（题型+题号）重新抽取补齐、重写，最多 3 轮；仍缺报人工
6. 交付前抽查 10%~20% 字段

## 方式 B：auto_run.py 一键脚本（需 DeepSeek key）
```
DEEPSEEK_API_KEY=sk-xxx <venv python> auto_run.py <pdf> <out.xlsx> \
  --course 马克思主义基本原理 --year 2026 [--month 4] \
  --url "$EXAM_OCR_URL" [--ocr-md out.md]
```
内部自动完成 OCR→deepseek 抽取→写表→自检→补题（≤3 轮）。key 用调用方自己的，不共用 OpenClaw 的。`--month 4` 会拼进年份列写成 `2026年4月`；同课程同年多考期务必带上。

## 抽取 Prompt（方式 A 用）
```
你是自考题库整理助手。下面是一份真题 OCR 文本。请按以下字段把每道题抽成一条 JSON 记录，
并额外给每条加一个整数 题号（全局连续编号：单选从1起、简答续编、论述续编；若原卷分节编号也请按阅读顺序编成全局连续号）。
输出 JSON 数组，每条字段顺序：
["题号","课程","知识点","题型","题目内容","选项A","选项B","选项C","选项D","选项E","正确答案","难度","状态","是否真题","是否模拟试卷","是否考前押题","年份","解析"]
规则：
- 选择题答案通常在试卷末尾"参考答案"区，请把正确选项字母关联到对应题目；找不到答案填 ""。
- 选项只填 A~E 有内容的；无则空字符串。
- 题型从"单选/多选/判断/填空/简答/计算/论述"中归类。
- 年份列填试卷考期（从页首标题提取，如"2026年4月高等教育自学考试…"则填 2026年4月），格式固定"XXXX年X月"；是否真题=是；状态=启用；是否模拟试卷/是否考前押题=否。
- 题目内容保留完整题干（含题号文字），去掉页码/页眉页脚噪点。
- 解析列必填（重点）：客观题写 1~3 句，讲清正确项成立的依据，并点明主要干扰项为什么错；主观题写 3~5 条得分要点；判断题说明正确的表述应该是什么。禁止留空、禁止只写"略"、禁止照抄题干。
只输出 JSON 数组，不要任何解释文字。
```

## exam-ocr 接口速查
- `GET  /health` → 健康检查（含队列状态 queued/tasks/users）
- `POST /parse`（multipart file）→ `{ok, pages, markdown, blocks}`（同步，会阻塞）
- `POST /parse-async`（file, `?owner=`）→ 异步提交，立即返回 `{task_id, status}`（**推荐**）
- `GET  /task/{task_id}` → 任务状态 `queued→running→done/failed`，done 带完整 result
- `GET  /tasks?limit=20&owner=xx` → 任务列表（可按 owner 过滤，倒序）
- `POST /write-excel`（json `{schema, records}`）→ 返回 .xlsx 文件流

## 产物归档（可选，归档目录由使用者自己指定）
本技能**不内置任何固定归档路径**——部署环境不同，归档位置由调用方给出：

```bash
# 方式1：显式指定归档根目录
python archive.py <xlsx> <原卷.pdf> <.ocr.md> <.json> <.json.check.json> \
       --to "<你的归档根目录>" --subject "<课程代码><科目名>"

# 方式2：预先设置环境变量，之后省略 --to
export EXAM_BANK_ARCHIVE_DIR="<你的归档根目录>"
python archive.py <文件...> --subject "15044马克思主义基本原理"
```

- **归档根目录**：本地文件夹、NAS 挂载盘、网盘同步目录、项目目录均可，随意
- **子目录命名**：`--subject "<课程代码><科目名>"`，如 `06869实验室管理学`；不给 subject 则直接放根目录
- **未指定归档目录时自动跳过**（打印提示、退出码 0，不算失败）；同名文件覆盖前会留一份 `.bak`
- **归档内容建议**：题库 xlsx + 原卷 PDF + `.ocr.md` + `.json` + `.json.check.json`（漏题自检报告）
- 归档前确认目标目录可写；网络盘/网盘未挂载时先挂载再归档

## 已验证案例（84:/root/.openclaw/真题/）
- 15043 中国近现代史纲要 2026年4月真题卷 → 15043.xlsx（OpenClaw 跑通）
- 15044 马克思主义基本原理 2026年4月真题卷 → 15044.xlsx（OpenClaw 跑通；本机 OCR 链路 2026-09-09 实测通过）

## 排错
- 连不上服务：确认 `$EXAM_OCR_URL` 填对、exam-ocr 容器在跑、端口可达
- 提交报 429：该 owner 队列已满（上限 20），等一等或用别的 `--owner`
- 异步任务卡住：`curl "$EXAM_OCR_URL/task/<task_id>"` 查状态；结果只保留 1 小时
- OCR 乱码：扫描件先二值化/纠偏；公式题人工补 LaTeX
- 双栏排版题序错乱：抽取前先按题号重排
