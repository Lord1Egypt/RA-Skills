---
name: xuexitong-homework-submit
description: "学习通/超星作业自动化（v1.1.2）：扫描作业、抓题模板、暂存/交卷、手写图答案流水线。致谢 HandWrite、学习通 API（mooc1-api.chaoxing.com）与超星图床上传接口（notice.chaoxing.com）。"
version: 1.1.2
homepage: "https://github.com/smallwhiteman/xuexitong-homework-submit-skill"
metadata:
  author: smallwhiteman
  openclaw:
    emoji: "📚"
---

# 学习通（超星）作业自动化 Skill

把「手动点网页」变成「可复用命令流程」：
- 列作业入口（taskrefId）
- 解析到 doHomeWork URL
- 抓题并生成可编辑答案模板
- 暂存（save）/交卷（submit）
- 手写图答案流水线：文本答案 → 手写 PNG → 图床 URL → HTML `<img>` → 暂存

**当前版本：v1.1.2**

## 致谢

感谢本 Skill 使用到的三个核心依赖/服务：
- **HandWrite**（手写渲染能力）
- **学习通 API**：`mooc1-api.chaoxing.com`
- **超星图床上传接口**：`notice.chaoxing.com/pc/files/uploadNoticeFile`

## 安全约束

- 默认 Cookie 文件：`~/.openclaw/credentials/xuexitong_cookie.txt`
- `save` 是安全操作（暂存）
- `submit` 是高风险操作（交卷），必须显式 `--confirm`

## 快速开始

> 目录变量：`{baseDir}` 指当前 skill 根目录。

```bash
# 1) 列出作业入口
python3 {baseDir}/scripts/xuexitong_submit.py list

# 2) 解析 task 链接 -> doHomeWork URL
python3 {baseDir}/scripts/xuexitong_submit.py resolve \
  --task-url "<mtaskmsgspecial url>"

# 3) 抓题 + 生成答案模板
python3 {baseDir}/scripts/xuexitong_submit.py fetch \
  --dohomework-url "<doHomeWork url>" \
  --out work.json

python3 {baseDir}/scripts/xuexitong_submit.py template \
  --work-json work.json \
  --out answers.json

# 4) 暂存（推荐先走这步）
python3 {baseDir}/scripts/xuexitong_submit.py save \
  --dohomework-url "<doHomeWork url>" \
  --answers answers.json \
  --work-json work.json

# 5) 交卷（必须显式确认）
python3 {baseDir}/scripts/xuexitong_submit.py submit \
  --dohomework-url "<doHomeWork url>" \
  --answers answers.json \
  --work-json work.json \
  --confirm
```

## 手写图答案流水线

```bash
# A. 初始化：抓题并生成可编辑 answers_text.json
python3 {baseDir}/scripts/xuexitong_hw_pipeline.py init \
  --dohomework-url "<doHomeWork url>" \
  --outdir runs/run1

# 手动编辑 runs/run1/answers_text.json 的 answer 字段

# B. 执行：渲染->上传->生成 HTML 答案->暂存
python3 {baseDir}/scripts/xuexitong_hw_pipeline.py run \
  --dohomework-url "<doHomeWork url>" \
  --rundir runs/run1
```

## 扫描“疑似新作业且未填写”

```bash
python3 {baseDir}/scripts/xuexitong_scan_pending.py \
  --limit 80 \
  --out runs/pending_scan.json
```

输出包含：
- `candidates[]`：候选作业（疑似未交且未写）
- `resolveFailures[]`：解析失败的任务入口

## 自动更新检查（已内置）

每次运行主脚本都会去 GitHub 检查最新版本（读取仓库 `VERSION`）：
- 若有新版本，会打印更新提示
- 不会阻塞主流程（网络失败时静默跳过）

更新命令：
```bash
clawhub update xuexitong-homework-submit
```

临时关闭更新检查：
```bash
XUEXITONG_SKIP_UPDATE_CHECK=1 python3 {baseDir}/scripts/xuexitong_submit.py list
```

## 常见故障

- 401/403 或页面异常：Cookie 过期，重新抓取 Cookie。
- 单题提交成功但多题空白：请传 `--work-json`，脚本会逐题提取隐藏字段。
- 服务器偶发 EOF/限流：重试或加 `--sleep-ms 200` 降速。
