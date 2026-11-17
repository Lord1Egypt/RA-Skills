# 百度知道回答自动发布 CLI 标准

将 `{baseDir}` 替换为技能根目录（含 `SKILL.md`、`scripts/` 的目录）。所有命令通过 `python {baseDir}/scripts/main.py` 调用。

## 最小命令

```bash
python {baseDir}/scripts/main.py health
python {baseDir}/scripts/main.py config-path
python {baseDir}/scripts/main.py version
```

## 标准行为

- **任意 CLI 启动前**执行 `bootstrap_skill_config()`（`main.py` 与 `cli.app.main()` 均触发）。
- **`health`**：只读 runtime 诊断，**不下载、不修复 media-assets，不执行业务动作**；不输出敏感值。
- **`config-path`**：输出 JSON，包含 `skill`、`env_path`、`example_path`。
- **`version`**：输出 JSON（`version`、`skill`）。
- **`run`**：长时间无 stdout **不代表卡死**；应通过 `logs` / `log-get` 排查。
- **任务完成后**若有 video artifact，CLI 应打印录屏路径、录屏日志、视频/音频诊断（见 `task_run_support._print_video_summary`）。

## config-path（配置路径）

```json
{
  "skill": "publish-answer-baidu-know",
  "env_path": "{DATA_ROOT}/{USER_ID}/publish-answer-baidu-know/.env",
  "example_path": "{skill_root}/.env.example"
}
```

## health 标准输出（runtime diagnostics）

`health` 委托 `jiangchang_skill_core.collect_runtime_diagnostics`，典型字段：

- `python_executable` — 当前 Python 解释器路径
- `platform_kit_version` / `platform_kit_min_version` / `platform_kit_version_ok`
- `jiangchang_skill_core_file` — 公共库加载来源（若来自技能目录副本会报 warning）
- `media_assets_root`、`ffmpeg_path`、`ffmpeg_available`、`background_music_mp3_count`
- `runtime_issue[warning|error]` — 非致命/致命问题列表
- `env_path` / `env_exists` / `example_path` — 用户 `.env` 与仓库模板路径

## 业务命令

```bash
python {baseDir}/scripts/main.py run \
  --question-url https://zhidao.baidu.com/question/XXXXXXX \
  --input-id D:\answers\demo.md \
  [--target ACCOUNT_HINT] \
  [--idempotency-key KEY]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--question-url` / `-u` | 是 | 百度知道问题页 URL，必须以 `https://zhidao.baidu.com/question/` 开头 |
| `--input-id` / `-i` | 是 | 本地回答文稿文件路径（.md / .txt） |
| `--target` / `-t` | 否 | 指定账号 ID；省略时由 account-manager 自动挑选 |
| `--idempotency-key` | 否 | 幂等键，重复运行同一键不会重复发布 |

### 成功输出（stdout JSON）

```json
{
  "ok": true,
  "account_id": "12",
  "question_url": "https://zhidao.baidu.com/question/123",
  "answer_path": "D:\\answers\\demo.md",
  "status": "success",
  "platform_message": "提交成功",
  "publish_record_id": 1,
  "duplicate": false,
  "error": null
}
```

### 失败输出（stdout JSON，rc=1）

```json
{
  "ok": false,
  "account_id": "12",
  "question_url": "https://zhidao.baidu.com/question/123",
  "answer_path": "D:\\answers\\demo.md",
  "status": "failed",
  "platform_message": "滑块验证码未在 300 秒内完成",
  "publish_record_id": 2,
  "duplicate": false,
  "error": {
    "code": "SLIDER_VERIFICATION_TIMEOUT",
    "message": "滑块验证码未在 300 秒内完成，任务已停止。",
    "stage": "before_publish"
  }
}
```

### 幂等命中输出（stdout JSON，rc=0）

```json
{
  "ok": true,
  "account_id": "12",
  "question_url": "https://zhidao.baidu.com/question/123",
  "answer_path": "D:\\answers\\demo.md",
  "status": "success",
  "platform_message": "提交成功",
  "publish_record_id": 1,
  "duplicate": true
}
```

### status 枚举

| status | 含义 |
|--------|------|
| `success` | 发布成功 |
| `pending_review` | 已提交，平台审核中 |
| `failed` | 发布失败（见 `error.code`） |

### 常见 error.code

| code | 说明 |
|------|------|
| `QUESTION_URL_EMPTY` | 未提供 `--question-url` |
| `QUESTION_URL_INVALID` | 问题 URL 格式不正确 |
| `ANSWER_PATH_EMPTY` | 未提供 `--input-id` |
| `ANSWER_FILE_NOT_FOUND` | 回答文稿文件不存在 |
| `INVALID_BODY` | 回答文稿内容为空 |
| `REQUIRE_LOGIN` | 未在规定时间内完成登录 |
| `CAPTCHA_NEED_HUMAN` | 触发滑块/短信验证码，需人工处理 |
| `SLIDER_VERIFICATION_TIMEOUT` | 滑块验证码超时 |
| `SMS_VERIFICATION_TIMEOUT` | 短信验证码超时 |
| `QUESTION_NOT_FOUND` | 问题页未就绪或 URL 无效 |
| `EDITOR_NOT_READY` | 回答编辑器未出现 |
| `PUBLISH_BUTTON_DISABLED` | 发布按钮被禁用 |
| `PUBLISH_TIMEOUT` | 发布结果未在规定时间内出现 |
| `ACCOUNT_SETUP_REQUIRED` | 未在 account-manager 注册百度知道账号 |
| `LEASE_CONFLICT` | 账号被其他任务占用 |
| `MISSING_BROWSER` | 未检测到 Chrome / Edge |

## 适配器档位

由 `OPENCLAW_TEST_TARGET` 环境变量控制：

| 值 | 行为 |
|----|------|
| 未设置 / `unit` / `mock` | mock 档位：不触网，模拟成功，写发布记录，用于 CI |
| `simulator_rpa` | 仿真浏览器档位：本地仿真页联调 |
| `real_rpa` | 生产档位：真实百度知道页面 |

生产运行时无需显式设置（默认 mock）；真实发布需显式 `OPENCLAW_TEST_TARGET=real_rpa`。

## 日志查询命令

```bash
python {baseDir}/scripts/main.py logs
python {baseDir}/scripts/main.py logs --task-type publish --status failed
python {baseDir}/scripts/main.py log-get <log_id>
```

| 命令 | 用途 |
|------|------|
| `logs` | 列出最近 N 条任务日志 |
| `log-get` | 按 log_id 查看单条任务日志（JSON） |

## 兄弟技能依赖

- **account-manager**：通过 `service/account_client.py` 以 subprocess CLI 调用，不 import 内部模块。
- 首次使用前需在 account-manager 注册平台：
  ```
  account platform ensure --key baidu_zhidao --display-name "百度知道" \
    --domain content --url "https://zhidao.baidu.com" --auth-strategy qr_code_manual
  ```

## 手工排查命令（推荐）

**建议使用宿主共享 python-runtime**，避免技能目录内临时 venv 加载不到公共库：

```text
Windows:
  {JIANGCHANG_DATA_ROOT}\python-runtime\.venv\Scripts\python.exe {baseDir}\scripts\main.py health

通用:
  <shared-python> {baseDir}/scripts/main.py health
```

`<shared-python>` 通常位于 `{JIANGCHANG_DATA_ROOT}/python-runtime/.venv`。

**不建议**在生产/测试机使用技能目录内 `uv run python`，以免加载不到共享 runtime 中的 `jiangchang-platform-kit` / `playwright`。
