# REQUIREMENTS — publish-answer-baidu-know

## 1. 标识

| 项 | 值 |
|----|-----|
| slug | `publish-answer-baidu-know` |
| 中文 name | 百度知道回答自动发布 |
| 中文 description | 在百度知道 Web 指定问题下将本地回答文稿发布为回答 |
| account-manager platform_key | `baidu_zhidao`（**需先** `platform ensure` 注册，当前非内置平台） |
| 建议 default_url | `https://zhidao.baidu.com` 【C: F12 确认】 |
| 技能数据库 | `{JIANGCHANG_DATA_ROOT}/{JIANGCHANG_USER_ID}/publish-answer-baidu-know/publish-answer-baidu-know.db` |
| 技能类型 | **real_browser_rpa**（无第三方发布 API） |

**account-manager 预置（实现前一次性执行）：**

```bash
python <account-manager>/scripts/main.py platform ensure \
  --key baidu_zhidao \
  --display-name "百度知道" \
  --domain content \
  --url "https://zhidao.baidu.com" \
  --auth-strategy qr_code_manual
```

---

## 2. 业务说明

运营需在 **百度知道** 指定问题下发布回答，人工重复打开问题页、填写回答、提交，效率低且不可追踪。

本技能通过 **Playwright RPA** 完成：**打开目标问题 → 填写回答 → 提交**。

**v1 主路径：**

1. 获取 `baidu_zhidao` 账号租约
2. 打开 CLI 提供的 **问题 URL**（或解析 question_id）
3. 执行 **三步**：进入回答编辑器 → 填写正文 → 提交
4. 记录 success / pending_review / failed

**范围边界：**

| 包含 | 不包含 |
|------|--------|
| 已有问题下的 **PC Web** 回答发布 | 提问、评论、非知道站点 |
| 本地回答文稿（文件/sidecar） | 非页面 API 回答捷径 |
| 登录态 + HITL | 自动搜索/匹配问题（v1 需用户提供 URL） |
| mock / simulator / real_rpa | 回答内多图/引用（v1） |

**硬约束：必须走浏览器页面操作**。

幂等：同 `account_id` + 同 `question_url` 已成功 → `duplicate:true`。

---

## 3. CLI 与输出 JSON

### 命令

```bash
python scripts/main.py run \
  [--target ACCOUNT_HINT] \
  --question-url QUESTION_URL \
  [--input-id ANSWER_FILE] \
  [--idempotency-key KEY]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--question-url` | 是 | 目标问题页 URL 【C: 格式因平台而异】 |
| `--input-id` / `-i` | 否* | 回答正文文件（txt/md） |
| `--target` | 否 | 账号 hint |
| `--idempotency-key` | 否 | 幂等键 |

\* 至少提供回答正文（文件或 `--content`，见 `references/CLI.md`）。

### 成功 stdout JSON

```json
{
  "ok": true,
  "account_id": "12",
  "question_url": "https://example.com/question/123",
  "answer_path": "D:\\answers\\demo.md",
  "status": "success",
  "platform_message": "提交成功",
  "publish_record_id": 1,
  "duplicate": false
}
```

### task_logs

| 字段 | 取值 |
|------|------|
| `task_type` | `publish` |
| `target_id` | `account_id` |
| `input_id` | `question_url` 或 idempotency_key |
| `input_title` | 问题标题摘要 **C** |
| `status` | `success` / `failed` |

---

## 4. URL

| 页 | URL | 可信度 |
|----|-----|--------|
| 站点入口 | `https://zhidao.baidu.com` | B |
| 目标问题页 | CLI `--question-url` | B（用户给定） |
| 回答编辑器 | 问题页内 **写回答** / **我来回答** | **C: F12 确认** |

---

## 5. 数据库与匠厂数据管理

### `answer_publish_records`

| 物理字段 | 中文 display_name | 来源 |
|----------|-------------------|------|
| id | 编号 | |
| idempotency_key | 幂等键 | CLI |
| account_id | 账号 ID | account-manager |
| question_url | 问题 URL | CLI |
| answer_path | 回答文稿路径 | CLI |
| status | 状态 | success / pending_review / failed |
| platform_message | 平台反馈 | toast |
| published_at | 提交时间 | |
| created_at / updated_at | | Unix 秒级 |

---

## 6. RPA 步骤

### 6.1 账号、浏览器与进入问题页（1～14）

| 步 | 动作 | URL / 定位 | 操作细节 | 等待 / 断言 | 可信度 |
|----|------|------------|----------|-------------|--------|
| 1 | 获取租约 | account-manager | `pick-web --platform baidu_zhidao --lease` | 得 `profile_dir` | A |
| 2 | 启动浏览器 | Playwright | 有头 Chrome | | A |
| 3 | 打开问题 URL | CLI `--question-url` | `goto` | `ERROR:QUESTION_NOT_FOUND` | B |
| 4 | 登录门 | **登录** | HITL ≤300s | `ERROR:REQUIRE_LOGIN` | C |
| 5 | 验证码/滑块 | 风控 UI | 不自动破解 | `ERROR:CAPTCHA_NEED_HUMAN` | A |
| 6 | 问题页就绪 | 问题标题区 | visible | **C** | C |
| 7 | 幂等预检 | SQLite | duplicate 则结束 | | A |
| 8 | 加载回答 | answer 文件 | `--input-id` 路径 | | A |
| 9 | 校验正文 | — | 非空 | `ERROR:INVALID_BODY` | B |
| 10 | 打开回答框 | **写回答 / 我来回答** | click | **C** | C |
| 11 | 编辑器就绪 | 正文编辑区 | visible | `ERROR:EDITOR_NOT_READY` | B |
| 12 | 录屏 | RpaVideoSession | 可选 | | A |
| 13 | task_logs | — | status=running | | A |
| 14 | 随机延迟 | — | 1～2s 拟人 | | A |
### 6.2 v1 三步发布（15～25）

| 步 | 动作 | URL / 定位 | 操作细节 | 等待 / 断言 | 可信度 |
|----|------|------------|----------|-------------|--------|
| 15 | Step1 正文 | 回答编辑区 | 粘贴/逐字 | | B/C |
| 16 | 正文就绪 | — | 可见 | | B |
| 17 | Step2 提交 | **发布回答** / **提交** | click | `ERROR:PUBLISH_BUTTON_DISABLED` | C |
| 18 | 二次确认 | **确认** 弹窗 | 若有则 click | | C |
| 19 | 等待结果 | toast / 跳转 | | `ERROR:PUBLISH_TIMEOUT` | C |
| 20 | 解析状态 | — | pending_review/success | | B |
| 21 | 写 DB | `answer_publish_records` | | | A |
| 22 | 写 task_logs | `publish` | | | A |
| 23 | stdout JSON | §3 | exit 0 | | A |
| 24 | 释放租约 | account-manager | 若适用 | | A |
| 25 | 关闭浏览器 | finally | | | A |
### 6.3 目标路径（v1 不强制）

T1 回答配图；T2 引用/代码块；T3 匿名/付费回答选项。

---## 7. 失败处理

| 现象 | 处理 |
|------|------|
| 无账号 | `ERROR: 账号库中没有任何 baidu_zhidao 记录…` |
| 问题不存在/无权限 | `ERROR:QUESTION_NOT_FOUND` |
| 未登录/验证码 | `ERROR:REQUIRE_LOGIN` / `ERROR:CAPTCHA_NEED_HUMAN` |
| 正文无效 | `ERROR:INVALID_BODY` |
| 编辑器不可用 | `ERROR:EDITOR_NOT_READY` |
| 重复 | `duplicate:true` |

---

## 8. 验收

```powershell
$env:OPENCLAW_TEST_TARGET = "mock"
python scripts/main.py run --question-url "https://..." --input-id D:\answer.md
```

---

## 9. 变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-07-06 | v1.0.4：Wave A～D 优化 §6（拆合并步/批次回环/列对齐/表头统一） |
| 2026-07-06 | v1.0.4：优化 §6（批次回环/拆合并步/关闭浏览器/POI keyword 批量） |
| 2026-07-06 | Wave 3 初版：百度知道 问答 RPA；无 API |
