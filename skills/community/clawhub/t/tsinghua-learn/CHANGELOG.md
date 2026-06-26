# tsinghua-learn — Release History

## v1.0.16 (2026-05-03)
- `auto_mark_read=true` 时 `--mark-read` 跳过 `--confirm`，但纯查待办永不自动标
- `login_supervised.py`：先 headless，仅 2FA 时弹浏览器
- `install_playwright.py`：内置 npmmirror.com 镜像，解决国内下载超时
- 删除 `todos_dom.py`（DOM 备用，已被 `todos_api.py` 替代）
- 3 个安全扫描全部 Staff Cleared（ClawHub #1984 申诉通过）

## v1.0.15 (2026-05-03)
- `todos_api.py --mark-read` 加 `--confirm` 脚本级强制确认
- `auto_mark_read` 不再自动执行，改为 suggestions 提示 AI 加 `--confirm`
- ClawScan: `auto_mark_read` Concern → Note

## v1.0.14 (2026-05-03)
- `login_supervised.py` 重写：先 headless，检测到 2FA 再弹浏览器
- 验证 `chromium-1169` ↔ `playwright==1.52.0` 版本对齐

## v1.0.13 (2026-05-03)
- `login_manager.py --reset` 默认 `auto_mark_read: true`（匹配 `config.json`）

## v1.0.12 (2026-05-03)
- 2FA 提示改 plain text（去 ASCII art）
- fingerPrint 文件缺失时不崩溃
- `auto_mark_read` 默认值改为 `true`
- ClawScan 从 5 个 findings 降到 4 个

## v1.0.10 (2026-05-02)
- 前置换页改用 `primaryEnv` + `os: [windows]`（ClawHub 识别）
- `ops.py upload` 加 `--confirm` 脚本级强制确认（无 `--confirm` 返回 pending）
- ClawScan: `submit_homework` Concern → Note；static analysis → Benign

## v1.0.9 (2026-05-02)
- 前置换页加 `credentialScope`、窄化密码描述（去"清华信息门户也用同一密码"）

## v1.0.8 (2026-05-02)
- SKILL.md 加 YAML 前置换页，声明 `primaryCredential: cas_password`

## v1.0.7 (2026-05-02)
- `install_deps.py` 依赖改为精确 `==` pin（不再 `>=`）
- 密码/用户名掩码改为全 `***`（不再泄露前 N 字符）
- stdin 方式从 `echo | pipe` 改为临时文件重定向
- 铁律 0 加例外条款（用户知情披露）
- 去掉 `ignore_https_errors=True` 全部 3 处（`login_auto.py`、`login_supervised.py`、`todos_dom.py`）
- 去掉非 Windows base64 fallback——仅支持 DPAPI
- ClawScan 从 7 个 findings 降到 4 个

## v1.0.6 (2026-05-02)
- 凭据存储从 base64 编码改为 Windows DPAPI（`CryptProtectData`）
- 修复 DPAPI 加密中文文本的字节长度 bug
- ClawScan: static analysis → Benign

## v1.0.5 (2026-05-02)
- 修复 `config.json` `auto_mark_read: true` → `false`
- 修改铁律 5 措辞（密码仅在初始化时收集）

## v1.0.3 (2026-05-02)
- 全面启用 TLS 验证：去掉 `learn_api.py`、`login_manager.py` 等 6 个脚本的 `verify=False`
- 新增 `--cred-stdin`：凭据通过 stdin JSON 传入，避免密码上命令行
- `install_deps.py` 依赖 pin 最低版本号
- SKILL.md 新增铁律 6（提交确认）+ "数据与安全"章节
- 清理 44 个 `_test_*` 调试脚本
- ClawScan 从 21+ 降到 6 个 findings

## v1.0.2 (2026-05-02)
- ClawHub 显示名从 "Clawhub" 改为 "清华网络学堂"
- 请求安全重扫

## v1.0.1 (2026-05-02)
- ClawHub 首次发布

## v1.0.0 之前
- 从 30+ 个散乱脚本重构为 10 个核心脚本
- 新建 `login_manager.py`（中央认证网关）
- 新建 `ops.py`（文件操作统一入口）
- 修复 `learn_api.py` 多个 API 端点
- 学期从 API 自动检测
- 文件名乱码修复（latin-1 → UTF-8）
- 提交日志机制（`submissions_log.json`）
- SKILL.md 分人类 / AI 两部分
- 创建三版发布（clawhub / github-full / github-cas）
