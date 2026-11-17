# 网页测试修复闭环（Webapp QA Loop）

[English](README.md) | [简体中文](README.zh-CN.md)

[GitHub](https://github.com/liubai00/webapp-qa-loop) | [ClawHub](https://clawhub.ai/liubai00/skills/webapp-qa-loop)

面向编码智能体的真实浏览器 QA Skill：通过实际点击测试可运行的 Web 应用，将证据写入可恢复的质量台账；在获得授权时修复根因，并通过发布门禁和部署后回归验证交付结果。

它的目标是减少反复对话，同时不擅自扩大权限。Skill 会优先从仓库和运行环境中发现可确认的信息，但会将源码修改、Git 交付、部署、回滚以及具有真实外部影响的浏览器操作视为相互独立的授权事项。

## 核心能力

- `audit`、`repair`、`release` 三种明确的工作模式。
- 通过真实浏览器交互进行测试，而不是只看截图。
- 使用内置 schema-v2 台账保存可恢复、可续跑的 QA 状态。
- 基于证据进行问题分级，并按影响范围执行 R0 至 R4 回归。
- 优先复用现有能力，确认必要性后才新增抽象或依赖。
- 将发布检查绑定到同一目标、制品和部署尝试，避免证据串用。
- 对重试、回滚、测试数据清理和外部交付设置明确边界。
- 自动跟随用户语言汇报，无需维护两套执行规则。

## 适用场景

适合用于：

- 浏览器冒烟测试和回归测试；
- 功能、交互、UI 和可访问性点击测试；
- 对现有可运行 Web 应用执行“测试并修复”；
- 核验已经部署的版本；
- 经明确授权后执行“部署并回归”的完整闭环。

不适合替代静态代码审查、纯 API 测试、纯单元测试、从零创建 UI、只看截图的设计评审、原生应用测试、专项安全测试或压力测试。

## 中英文如何切换

`SKILL.md` 使用英文维护，作为唯一的执行规范；智能体默认使用用户当前的语言进行进度更新、问题确认、证据汇总和最终报告。台账枚举、编号及命令参数保持英文，以保证跨环境兼容和机器可读。

因此不需要额外设置开关：用中文提问就用中文回复，用英文提问就用英文回复；也可以在提示词中明确指定语言。

## 使用要求

- 智能体运行环境具备真实浏览器控制能力。
- Python 3.10 或更高版本，命令名为 `python` 或 `python3`。
- 已有可运行的 Web 应用，或可访问且已获授权的测试目标。
- 只有在要求修复时才需要仓库和终端权限。
- 只有在分别明确授权 Git 或部署操作时才需要相应凭据。

## 安装

### Codex

将仓库克隆到 Codex 的 Skills 目录：

```bash
git clone https://github.com/liubai00/webapp-qa-loop.git "${CODEX_HOME:-$HOME/.codex}/skills/webapp-qa-loop"
```

安装后重启 Codex，使 Skill 列表重新加载。

### OpenClaw / ClawHub

```bash
openclaw skills install @liubai00/webapp-qa-loop
```

也可以使用 ClawHub 独立命令行客户端：

```bash
clawhub install @liubai00/webapp-qa-loop
```

## 使用示例

Skill 可在匹配任务时自动触发，也可以通过 `$webapp-qa-loop` 显式调用。

只测试、不改代码：

```text
使用 $webapp-qa-loop，通过真实浏览器对当前 Web 应用进行冒烟测试，给我一份有证据的问题报告，不要修改代码。
```

测试并修复：

```text
使用 $webapp-qa-loop 测试这个下单流程，修复确认属于本次范围的问题，并按影响范围完成回归；不要提交、推送或部署。
```

发布并验证：

```text
使用 $webapp-qa-loop 测试并修复应用，将已验证制品部署到我明确指定的测试环境，然后执行部署后回归。只有我单独授权时才提交或推送代码。
```

Skill 始终选择能够满足需求的最低权限模式。“测试”不等于允许修改代码，“修复”也不等于允许提交、推送或部署。

## 可恢复质量台账

在修复、发布以及非简单审计任务中，Skill 会使用 `scripts/qa_ledger.py` 保存目标、测试场景、检查项、证据引用、问题、修复周期、发布尝试、清理情况和最终结论。

```bash
python scripts/qa_ledger.py --help
```

该脚本只记录调用方提供的事实，不会自行打开浏览器、运行项目命令、执行部署或授予权限。

## 验证

运行台账回归测试：

```bash
python scripts/test_qa_ledger.py
```

如果环境中具备 Codex `skill-creator`，还可执行结构校验：

```bash
python /path/to/skill-creator/scripts/quick_validate.py .
```

## 目录结构

```text
.
|-- SKILL.md
|-- agents/openai.yaml
|-- references/
|   |-- automation-promotion.md
|   |-- browser-playbook.md
|   |-- issue-ledger.md
|   |-- release-and-rollback.md
|   |-- repair-and-reuse.md
|   `-- scope-and-selection.md
`-- scripts/
    |-- qa_ledger.py
    `-- test_qa_ledger.py
```

## 能力边界

本流程只能证明已经声明并保留证据的覆盖范围，不会声称整个应用已经被穷尽测试、绝对完美或不存在缺陷。

## 许可协议

MIT-0。ClawHub 也会以 MIT-0 协议分发已发布的 Skill。
