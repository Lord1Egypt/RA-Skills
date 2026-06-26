---
name: publish-npm-clawhub
license: Apache-2.0
---

# Publish npm + ClawHub Skill

License: Apache-2.0

一个内部发布 skill，用来稳定处理以下工作：

- plugin 发布到 npm
- skill / plugin 发布到 ClawHub
- ClawHub `suspicious` / `flagged` 扫描结果复核
- 发布账号、slug、包名、本地发布白名单统一走本地配置文件，不进仓库

## 仓库结构

- `SKILL.md`：给 Codex 使用的 skill 说明
- `skill.json`：skill 元数据和版本号
- `scripts/release_guard.py`：发布前检查、可疑模式扫描、临时发布目录准备
  说明：这个脚本只做本地 Git / 文件检查和临时目录复制，不主动发网络请求
- `references/workflow.md`：推荐发布流程
- `references/scanner-playbook.md`：ClawHub 可疑扫描的常见原因和修复策略
- `config/publish.accounts.example.json`：本地配置模板

## 快速开始

1. 复制模板并填写本地配置：

```bash
cp config/publish.accounts.example.json config/publish.accounts.local.json
```

2. 确认本地配置没有被 Git 跟踪：

```bash
git check-ignore -v config/publish.accounts.local.json
```

3. 发布前运行守门检查：

```bash
python3 scripts/release_guard.py . \
  --config config/publish.accounts.local.json \
  --prepare-release-dir /tmp/publish-release
```

4. 再按 `SKILL.md` 中的流程执行 npm / ClawHub 发布。

## 本地配置原则

- 真正的发布账号、handle、slug、npm 用户名放在 `config/publish.accounts.local.json`
- 这个文件必须被 `.gitignore` 忽略
- 发布时只从临时发布目录上传，不直接上传仓库根目录
- `release_guard.py` 只读取当前仓库和本地配置，不会读取 `~/.openclaw/secrets.json` 或私有 `config.json`

## 已沉淀的关键经验

- ClawHub 发布前固定执行：`logout -> login -> whoami`
- ClawHub UI 可能滞后，复核要同时看 CLI / 页面 HTML
- 如果最新版本已经确认仍是 `suspicious` / `flagged`，下一步必须修复并重发，不能只重复检查
- 如果页面只剩 `Credentials` / `Persistence & Privilege` 这类 capability note，不要直接等同于 `suspicious`
- 容易触发 `suspicious` 的模式：
  - 同一个文件里同时有环境变量读取和网络发送
  - 同一个文件里同时有本地文件读取和网络发送
  - 代码或文档提到 `~/.openclaw/secrets.json` / 私有 `config.json`
  - 只改功能逻辑，没有改“本地读取 + 外部发送”的实现结构
- 常见修复：
  - 把 `env` 读取和网络 client 拆到不同文件
  - 把 local credential store / credential resolver / api client / sender main flow 拆开
  - 显式声明只读取白名单环境变量
  - 前置写清楚联网和传输内容
  - 发布前用白名单文件生成临时目录，排除 `.npmrc`、`.env`、`*.tgz`、本地配置

## follow-builders-sidecar 案例结论

这次真实经验说明了三件事：

1. 反复出现可疑标签，往往不是因为功能“不合法”，而是因为扫描命中的结构还在。
2. 只改代码不够，文档里的敏感路径、权限说明、凭证表述也会影响审核判断。
3. 最终是否修好，要看最新版本的页面内嵌扫描结果：
   - `staticScan.status = clean`
   - `summary = "No suspicious patterns detected."`
