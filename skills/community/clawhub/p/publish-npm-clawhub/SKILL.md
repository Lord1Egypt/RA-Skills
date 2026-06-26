---
name: publish-npm-clawhub
description: Publish OpenClaw skills or plugins to npm and ClawHub with a guarded workflow. Use this whenever the user asks to release, publish, ship, or republish a skill/plugin, investigate ClawHub suspicious or flagged results, prepare a sanitized release directory, or verify release metadata, versions, accounts, slugs, and scanner status. Always use this skill when publish accounts must come from a local config file and must not be uploaded.
---

# Publish npm + ClawHub

> Version: 1.0.6 · License: Apache-2.0 · Author: jianghaibo
>
> Required tools: Read, Write, Bash · Requires: python3, git, clawhub, curl

这个 skill 用来把“容易出错的发布流程”变成固定动作。

先读：

- `references/workflow.md`
- `references/scanner-playbook.md`

如果仓库里存在 `scripts/release_guard.py`，发布前优先运行它。
这个脚本只做本地文件、Git 和发布目录检查；真正的联网发布发生在后续显式执行 `clawhub` / `npm` 命令时。

## 核心原则

1. 发布账号、handle、slug、npm 用户名统一放在本地配置文件，不写进仓库，不上传。
2. ClawHub 发布不要直接拿仓库根目录上传，先生成临时发布目录。
3. 对 skill / plugin 分别判断是否需要 npm：
   - 有 `package.json` 的 plugin 才走 npm
   - 纯 skill 通常只走 ClawHub
4. ClawHub 每次发布前固定执行：
   - `clawhub logout`
   - `clawhub login`
   - `clawhub whoami`
5. 发布完成后一定复核线上状态，不能只看命令退出码。

## 本地配置

默认使用：

```text
config/publish.accounts.local.json
```

如果文件不存在：

- 先从 `config/publish.accounts.example.json` 复制一份
- 填真实账号
- 用 `git check-ignore` 确认它被忽略

如果该文件已被 Git 跟踪，先停止发布，先修复仓库。

## 建议流程

### 1. 识别发布对象

判断当前对象属于哪类：

- skill
- plugin
- skill + plugin 组合

检查这些文件：

- `SKILL.md`
- `skill.json`
- `package.json`
- `openclaw.plugin.json`
- `.codex-plugin/plugin.json`

### 2. 对齐版本和元数据

发布前确认：

- 所有 manifest 里的版本一致
- 代码里硬编码的版本号和 manifest 一致
- ClawHub 所需的 `config` / `primaryEnv` / 联网说明存在
- 不把真实账号写进 README / SKILL / JSON

### 3. 运行发布前守门检查

优先执行：

```bash
python3 scripts/release_guard.py . \
  --config config/publish.accounts.local.json \
  --prepare-release-dir /tmp/publish-release
```

如果脚本报错：

- `FAIL` 必须先修
- `WARN` 需要人工判断，尤其是可疑扫描相关 warning

### 4. npm 发布

仅在下面条件成立时执行：

- 存在 `package.json`
- 本地配置里 `npm.enabled = true`

发布前确认：

- `npm whoami`
- 包名正确
- 版本号已递增
- `npm pack --dry-run` 结果干净

### 5. ClawHub 发布

使用临时发布目录，不要直接发仓库根目录。

发布命令结构：

```bash
clawhub publish /tmp/publish-release \
  --slug <slug> \
  --name "<display-name>" \
  --version <semver> \
  --changelog "<changelog>"
```

### 6. ClawHub 闭环复核

发布后必须进入闭环，不要只做一次检查。

固定动作：

1. 先确认 `clawhub inspect <slug>` 已经指向最新版本。
2. 再确认页面版本也已经更新。
3. 再看扫描结果是不是已经 clean / benign。

如果最新版本还在 `pending`：

- 可以等待并复核
- 但每一轮等待都必须以“扫描状态变化”为目标

如果最新版本仍然是 `suspicious` / `flagged`：

- 不要只重复执行同一组检查
- 不要在没有代码、文档或 manifest 变化的前提下反复重看页面
- 必须立即进入修复动作
- 修复后必须递增版本并重新发布

停止条件：

- `clawhub inspect <slug>` 指向最新版本
- 最新页面或页面内嵌数据不再显示 `suspicious` / `flagged`
- `staticScan.status = clean`
- `OpenClaw = Benign` 或更好

## 可疑扫描复核

如果页面出现 `suspicious` / `flagged`：

1. 同时看：
   - `clawhub inspect <slug>`
   - ClawHub 页面
   - `curl` 抓页面 HTML
2. 区分是页面缓存，还是最新版本真的还没过扫描。
3. 如果静态规则命中，优先看：
   - 同文件 `env` 读取 + 网络发送
   - 同文件 文件读取 + 网络发送
   - 提到 `~/.openclaw/secrets.json`
   - 提到私有 `config.json`
4. 修复后递增版本重新发，不要原地重发同版本。
5. 如果已经确认“同一个版本仍然可疑”，下一步必须是修复，不是继续重复检查。

### 真实踩坑：为什么改了很多次还是会继续可疑

以 `follow-builders-sidecar` 为例，反复命中可疑标签，通常不是因为“功能本身不该存在”，而是因为下面几件事没有一起处理：

1. 只改了功能，没有改触发扫描的代码结构。
   - 例如把“读取本地 OpenClaw/Feishu 配置”和“调用 Feishu API 发网络请求”继续放在同一个文件里。
   - 从功能视角看只是正常发消息；从扫描器视角看，这仍然像“读取本地敏感信息后外发”。
2. 只改了代码，没有改文档和元数据里的敏感表述。
   - 如果 `SKILL.md` / `README` 里继续高频出现“私有 config / 本地 credentials / secret 路径”等字眼，扫描和 LLM 审核仍可能持续提高风险判断。
3. 把能力标签误当成可疑标签。
   - 页面里的 `Credentials` / `Persistence & Privilege` 经常只是 capability note，不等于 `suspicious` / `flagged`。
   - 真正要看的是最新版本的 `staticScan.status`、summary、页面内嵌数据，而不是看到 capability note 就误判“还没修好”。
4. 没有区分“扫描 pending / 页面缓存 / 真正仍然 flagged”。
   - 刚发布完时，`inspect` 可能还看不到，页面也可能还是旧内容。
   - 如果不先确认“最新版本是不是已经切过去”，就很容易把旧结果当成新结果。

### 最终真正起作用的修复

在 `follow-builders-sidecar` 这次案例里，最终让标签消失的不是单点文案修改，而是一组结构性修复：

1. 发布时只上传白名单临时目录，不直接发仓库根目录。
2. 把“凭证/本地配置读取”和“网络调用”拆到不同文件：
   - credential resolver
   - local credential storage
   - Feishu API client
   - sender main flow
3. 本地直连凭证保留在用户本机路径，且不上传仓库、不进入发布目录。
4. 文档里明确说明：
   - 会联网到哪些端点
   - 哪些配置是本地存储
   - 为什么需要这些本地权限
   - 不会读取哪些无关 secrets
5. 发布后以“最新版本页面内嵌扫描结果”为最终准绳，而不是凭页面顶部零散文案判断。

## 优先修复策略

命中可疑时，优先按这个顺序改：

1. 把配置读取拆到单独文件
2. 把网络 client 拆到单独文件
3. 显式限制只读取白名单环境变量
4. 删除代码和文档里对 `secrets.json` / 私有 `config.json` 的依赖
5. 在 `SKILL.md` / `README` / `SECURITY` 中补清楚联网说明和发送字段
6. 如果文档里必须提到这些敏感路径，明确写成“不会读取 / 已移除依赖 / 高风险关键词示例”，避免歧义
7. 如果业务确实需要“本地凭证 + 外部发送”，优先做职责拆分，不要把“读取本地凭证”和“发网络请求”继续放在同一个实现文件里
8. 如果页面只剩 `Credentials` / `Persistence` note，但最新版本 `staticScan.status = clean`，不要把 note 误判成仍然 `suspicious`

## 结果汇报格式

最终汇报时至少覆盖：

- 发布对象
- npm 版本和 dist-tag
- ClawHub slug 和最新版本
- 扫描状态是否 clean / benign / pending
- 是否还存在可疑标签
- 若还有问题，下一步阻塞点是什么
