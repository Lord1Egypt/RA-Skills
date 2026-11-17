---
name: Release Proof Builder
slug: release-proof-builder
description: Build verifiable proof that a ClawHub release is live and installable. 在发布后核验 GitHub、Actions、registry、公开元数据和安装结果，避免把推送成功误当成上架成功。
version: 1.0.3
metadata:
  openclaw:
    os: [macos]
    emoji: "🔎"
    requires:
      bins:
        - git
        - clawhub
    homepage: https://github.com/bonniegeng-max/openclaw-publisher
    install:
      - kind: node
        package: clawhub
        bins: [clawhub]
---

# Release Proof Builder

“代码已经 push”不等于“skill 已经可以下载”。

ClawHub 发布链路通常跨过多个系统：本地仓库、GitHub 远端、GitHub Actions、ClawHub registry、公开元数据和最终安装目录。任何一层成功，都不能单独证明整条链路完成。

`release-proof-builder` 会把这些分散信号整理成一份可核验的发布证据包，明确告诉你已经证明了什么、还缺什么，以及当前能不能对外说“已上线可用”。

## 一句话卖点

Turn “the publish probably worked” into evidence that the release is live, clean, and installable.

## 适合谁

- 已经 push 到 GitHub，但不确定 ClawHub 是否真正上架的人
- Actions 显示成功或失败，却和 registry 状态对不上的人
- 需要确认版本、展示名、topics 和公开页是否同步正确的人
- 想在发布后留下可复查证据，而不是凭印象判断的人

## 不适合谁

- 还没有执行发布的人
- 只想做发布前内容审核的人
- 想伪造公开页、下载量或工作流结果的人

## 四层证据

### 1. 源码证据

- 本地 HEAD 与 GitHub 远端 HEAD 是否一致
- 目标 skill 目录和 `SKILL.md` 是否包含在该提交中
- catalog metadata 是否与目标 skill 对应

### 2. 流水线证据

- 目标提交是否触发发布 workflow
- 目标发布 workflow 是否已完成且结论为成功
- 失败、跳过、取消或仍在运行均不能达到 E2
- 失败发生在发现、验证、上传还是 registry 返回阶段

### 3. Registry 证据

- `clawhub inspect` 是否能找到目标 slug
- `latest` 是否指向预期版本
- 展示名、summary、topics 是否符合预期
- `moderation.verdict` 是否明确为 `clean`；待审核、缺失或非 `clean` 均不能达到 E3

### 4. 安装证据

- 是否能安装指定 slug 或指定版本
- 安装后的文件是否齐全
- 实际 `SKILL.md` 是否与预期版本一致
- 是否记录本次主动安装的时间、slug、版本和原因，并标记受污染的指标观察区间

## 证据等级

- `E0 未发布`：只有本地文件，没有远端提交
- `E1 已推送`：GitHub 远端包含提交，但没有发布证据
- `E2 流水线成功`：目标发布 workflow 已完成且结论为成功，但 registry 尚未确认
- `E3 已上架且审核正常`：registry 可读取正确版本与公开元数据，且 moderation verdict 为 `clean`
- `E4 可安装`：已完成指定版本的独立安装验证，文件与源码一致，并记录安装造成的指标污染

只有达到 `E4`，才建议对外表述为“已上线、可下载使用”。

## 你可以这样让我工作

- `帮我证明这个 skill 已经真正发布成功`
- `检查 GitHub 推送、Actions 和 ClawHub 状态是不是一致`
- `给我一份发布证据包，不要只看 workflow 绿灯`
- `确认这个 slug 现在是否真的可安装`

## 我理想中的输出

1. 发布结论：未完成 / 已推送 / 已上架 / 可安装
2. 当前证据等级：`E0-E4`
3. 已验证证据：每项附来源与结果
4. 缺失证据：还不能证明的部分
5. 冲突信号：例如 Actions 红灯但 registry 已上架
6. 下一步动作：补齐证据最短的一步

## 一个真实场景

用户说：

`GitHub 已经 push 成功，为什么 ClawHub 还是查不到？`

我不会直接回答“再等等”，而会按顺序确认：

- 远端 HEAD 是否真的是这次提交
- workflow 是否触发并处理了目标目录
- publish 返回的是失败、pending 还是 published
- `clawhub inspect` 是否能读到 slug
- 如果可见，再做隔离目录安装验证

## 工作原则

- 不用单一绿灯证明整条链路成功
- 优先使用机器可读取的状态，而不是截图或主观描述
- 对“尚未证明”和“明确失败”做区分
- 安装验证使用隔离目录，避免污染现有环境
- 主动安装仍会污染 downloads / installs 观察；必须记录时间、slug、版本和原因，重建自然观察起点，验收时段及紧随其后的增量不得归因为自然用户
- 不输出 token、cookie 或其他敏感凭据

## 配套文件

- `examples/green_action_missing_registry.md`
  GitHub 成功但 ClawHub 查不到的典型证据冲突
- `references/evidence_levels.md`
  `E0-E4` 证据等级定义与判断标准
- `references/verification_commands.md`
  发布后常用的只读核验命令
- `templates/release_proof_report.md`
  发布证据报告模板
- `CHANGELOG.md`
  版本记录

如果你需要解决“为什么发布失败”，用 `github-actions-clawhub-doctor`；如果你需要证明“现在到底上线没有”，用这个 skill。

## 同系列 · skill 工程线（Skill Engineering Line）

本 skill 属于「skill 工程方法论」系列 —— 六件工具覆盖一个 skill 从定位到上线的完整链路，按需组合：

- `skill-positioning-audit` — 定方向：该卖给谁、差异化够不够
- `skill-summary-rewriter` — 写门面：摘要/简介改成能带来安装的版本
- `skill-publish-readiness` — 上线前：发布自查（结构 / 版本 / 页面 / 安全 / 值不值得发）
- `github-actions-clawhub-doctor` — 发不出去：定位 Actions / registry 到底卡在哪一层
- **`release-proof-builder`** — 上线后：证明「现在到底上线没有、能不能装」**（本 skill）**
- `skill-portfolio-growth-audit` — 看全局：整个作品集下一步押注什么

安装任意一个：`clawhub install @bonniegeng-max/<slug>`
