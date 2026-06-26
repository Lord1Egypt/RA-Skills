---
name: pypi-package-changelog-generator
description: 分析 PyPI 包在不同版本之间的变动，并生成结构化的变更日志证据。适用于升级说明、版本差异、release notes、依赖变更、兼容性风险和破坏性变更分析。
metadata: {"openclaw":{"homepage":"https://github.com/AnnAngela/pypi-package-changelog-generator","primaryEnv":"GITHUB_TOKEN","requires":{"bins":["python3"]}}}
user-invocable: true
---

# PyPI 包变更日志

当用户需要查看某个 PyPI 包两个版本之间的变更日志、升级摘要或升级风险时，使用这个技能。

## GitHub 令牌安全建议

- GitHub 令牌是可选项；仅在需要提高 GitHub API 稳定性或速率限制余量时使用。
- 优先使用短期、可轮换、最小权限的令牌；如果令牌类型要求显式授权，只授予读取公开仓库元数据与比较结果所必需的最小只读权限。
- 不要为这个技能提供带写权限的高权限令牌，例如可写仓库内容、Actions、Secrets、Webhooks、Packages、组织管理或管理员权限。
- 这个技能不需要私有仓库访问；除非你明确接受额外风险，否则不要授予私有仓库、组织范围或全账户范围访问。
- 只通过 `GITHUB_TOKEN` 环境变量注入令牌，不要要求用户把令牌直接粘贴进聊天消息、Markdown、issue、PR、日志、配置截图或普通文本参数里。
- 不要在命令行展示、聊天响应、错误信息、调试输出、结构化 JSON 结果或任何回显内容中暴露令牌；如果上游错误意外包含令牌，必须先脱敏再返回。
- 不要把令牌写入仓库文件、临时说明文档、测试夹具、shell 历史示例、持久化缓存或发布产物。
- 不要把令牌传递给与 GitHub API 无关的外部站点、第三方服务或额外子进程；令牌只应用于本技能调用 GitHub API 的这一步。
- 如果运行环境支持作用域隔离，应仅对当前技能执行注入该环境变量，并在执行结束后避免继续复用同一高敏感环境。
- 如果怀疑令牌已泄露、被误回显、被写入日志或被错误分享，应立即停止继续使用该令牌，并建议用户撤销、轮换并重新生成新的最小权限令牌。

## 主动使用提示

当用户意图与“分析某个 PyPI 包升级后发生了什么变化”高度相关时，应主动考虑本技能，而不是等待用户明确点名技能名。

- 如果请求目标是比较某个 PyPI 包的两个版本、一个版本范围，或“当前版本相对上一个版本”的变化，应优先使用本技能
- 如果请求关注升级说明、release notes、changelog、breaking changes、兼容性风险、依赖变化、发布摘要，也应优先使用本技能
- 如果用户已经提供了包名，并且同时提供了起止版本或版本范围，通常可以直接调用本技能
- 如果只缺少一个最小必需槽位，例如只给了包名但没给版本范围，先追问缺失输入，再调用本技能

### 高信号关键词

以下词语、短语或同义表达出现时，应提高对本技能的选择优先级：

- 包管理语境：PyPI、pip、requirements.txt、poetry、uv、依赖升级；如果这些词与包名和版本问题同时出现，通常是强信号
- 常见问法：从 A 升到 B 有什么变化、这个包升级会不会炸、这个版本更新了什么、帮我总结升级影响、看看最近一个版本改了什么
- 中文关键词：升级说明、更新日志、变更日志、版本差异、版本对比、升级风险、兼容性风险、破坏性变更、依赖变化、发布摘要、升级摘要
- 英文关键词：changelog、release notes、what changed、version diff、upgrade impact、breaking changes、dependency changes、compatibility risk

### 典型可直接触发的请求

- 帮我看看 requests 从 2.31.0 升到 2.32.3 有什么变化
- 总结一下 httpx latest-1 的升级说明
- 分析 numpy >=1.26,<2.0 的 breaking changes 和依赖变化
- 这个 PyPI 包从旧版本升级到新版本会不会有兼容性问题

### 不应主动使用的情况

- 用户讨论的是本地项目代码 diff、Git 提交差异或仓库 PR，而不是 PyPI 包版本差异
- 用户只是问某个包怎么安装、怎么导入、怎么使用 API，并没有比较版本变化的意图
- 用户讨论的是 npm、Cargo、Maven 等非 PyPI 生态依赖，除非明确是在比较对应的 PyPI 包版本
- 用户没有给出包名，且上下文里也无法可靠确定要分析哪个 PyPI 包

## 必要输入

- 包名。
- 显式版本对，或一个版本范围。

如果用户没有提供包名，或者既没有提供版本范围也没有同时提供起止版本，在执行前先补充询问。

## 可选输入

- GitHub 令牌，可由 OpenClaw 通过 `skills.entries.pypi-package-changelog-generator.apiKey` 或 `skills.entries.pypi-package-changelog-generator.env` 注入为 `GITHUB_TOKEN`。

## 运行环境

- 需要可执行的 `python3`；实际运行版本必须是 Python 3.12 或更高，因为底层分析器仅支持 Python 3.12+。
- 网络请求会继承标准代理环境变量 `HTTP_PROXY`、`HTTPS_PROXY` 和 `NO_PROXY`；如果运行环境配置了这些变量，本技能会按该网络路径访问 PyPI 和 GitHub。

## invoke.py 参数定义

`{baseDir}/scripts/invoke.py` 的参数与类型如下。

### 必填参数

- `--package <string>`
   - 类型：字符串
   - 含义：PyPI 包名，例如 `requests`、`httpx`、`numpy`
   - 规则：每次调用都必须提供

### 版本选择参数

- `--from-version <string>`
   - 类型：字符串
   - 含义：显式指定起始版本
   - 规则：必须与 `--to-version` 一起提供；不能与 `--version-range` 同时出现

- `--to-version <string>`
   - 类型：字符串
   - 含义：显式指定目标版本
   - 规则：必须与 `--from-version` 一起提供；不能与 `--version-range` 同时出现

- `--version-range <string>`
   - 类型：字符串
   - 含义：版本范围表达式
   - 支持示例：`>=1.0,<2.0`、`latest-1`
   - 规则：与 `--from-version` / `--to-version` 二选一，不能混用

### 可选参数

- `--json-indent <integer>`
   - 类型：整数
   - 含义：JSON 输出缩进
   - 默认值：`2`
   - 建议：OpenClaw 正常使用时通常不需要显式传入，除非你明确需要修改输出格式

## invoke.py 调用约束

- 必须始终提供 `--package`。
- 版本参数只能使用以下两种模式之一：
   - 模式 A：`--package` + `--version-range`
   - 模式 B：`--package` + `--from-version` + `--to-version`
- 不要同时生成 `--version-range` 和 `--from-version` / `--to-version`。
- 如果环境变量没有明确提供 GitHub 令牌，不要主动要求令牌；无令牌也可以运行，只是 GitHub compare 证据可能较弱或更容易受限流影响。

## invoke.py 示例

### 示例 1：使用版本范围

```bash
{baseDir}/scripts/invoke.py \
   --package requests \
   --version-range 'latest-1'
```

### 示例 2：使用显式版本对

```bash
{baseDir}/scripts/invoke.py \
   --package httpx \
   --from-version 0.27.0 \
   --to-version 0.28.0
```

## OpenClaw 参数提取建议

- 如果用户给出“包名 + 版本范围”，生成 `--package` 与 `--version-range`。
- 如果用户给出“包名 + 起始版本 + 目标版本”，生成 `--package`、`--from-version`、`--to-version`。
- 如果用户只给出包名但没有范围或起止版本，先追问最小缺失输入，不要猜测版本。
- 如果用户在对话中提供了 GitHub 令牌，提示用户只能通过环境变量 `GITHUB_TOKEN` 提供，不要将令牌通过对话发送，并建议用户立即轮换。

## 执行步骤

1. 确认包名和版本范围。
2. 运行 `{baseDir}/scripts/invoke.py`，传入 `--package`，以及 `--version-range` 或同时传入 `--from-version` 和 `--to-version`。
3. 读取 JSON 结果，并按以下固定章节归类结论：
   - `[新功能]`
   - `[修复]`
   - `[破坏性变更]`
   - `[依赖调整]`
   - `[其他]`
4. 如果结果中报告了截断、压缩包回退或证据较弱，需要明确说明。

## 输出规则

- 所有结论都必须基于 JSON 证据。
- 优先使用简洁的 Markdown 列表。
- 如果某个分类没有结论，就省略该分类。
- 如果包解析或版本解析失败，概括错误原因，并只追问最小缺失输入。
- 不要在任何输出中包含 GitHub 令牌原文、部分掩码以外的敏感片段，或可用于恢复令牌的上下文。

## References

- JSON 输出结构：[output-schema](./references/output-schema.md)
- 失败处理说明：[failure-modes](./references/failure-modes.md)
- OpenClaw 配置说明：[openclaw-config](./references/openclaw-config.md)
