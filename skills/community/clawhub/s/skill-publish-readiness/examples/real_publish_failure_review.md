# 真实案例：三次“看似能发”的发布失败

这个案例来自一条真实的 GitHub Actions → ClawHub 发布链路，并做了必要脱敏。它包含跨层证据与冲突信号，因此 auto 选择 deep；仅通过本地 dry-run 不足以判断一次发布已经准备好。

## 候选版本

- 目标目录：`skills/clawhub-launch-checklist/`
- 本地文件：`SKILL.md`、`CHANGELOG.md`、`.clawhubignore`、`examples/`、`references/`、`templates/`
- 本地 dry-run：通过
- GitHub 推送：成功
- 预期结果：ClawHub 出现新版本，并可独立安装

## 第一轮证据

| 层级 | 观察 | 初步判断 |
|---|---|---|
| 本地 | 文件齐全，dry-run 通过 | 只能证明内容可被解析 |
| GitHub | commit 已到远端 | 只能证明源码已同步 |
| Actions | workflow 启动后失败 | 发布链路存在阻塞 |
| ClawHub | 找不到目标 slug | 尚未上架 |

关键日志指出目标 slug 使用了 `clawhub-` 前缀。该命名空间受保护，因此即使文件完整，仍不能完成首次发布。

### 审查结论

- 发布结论：`先别发`
- 阻塞项：slug 使用受保护前缀
- 根因：目录名直接成为 registry slug，但预检没有禁止保留命名空间
- 最小修复：将目录和 slug 改为 `skill-launch-checklist`
- 防复发：在 pull request 阶段增加 protected slug 校验

## 第二轮证据

改名后，ClawHub 已能读取目标 skill，但 Actions 仍显示失败。workflow 把 `pending-publication` 当成未知错误处理。

| 层级 | 观察 | 初步判断 |
|---|---|---|
| Actions | 返回 `pending-publication` 后退出失败 | 流水线结论可疑 |
| ClawHub inspect | 已能读取目标 slug | registry 已接收发布 |
| Moderation | 扫描处理中 | 不是内容发布失败 |
| Install | 暂不可用 | 尚未达到可下载结论 |

### 审查结论

- 发布结论：`补完再发，且不能宣称可下载`
- 阻塞项：workflow 状态映射错误
- 根因：把合法中间态当成终态失败
- 最小修复：将 `pending-publication` 记录为独立结果，不直接判定发布失败
- 验收要求：等待 moderation 完成，再执行 `inspect` 和隔离安装

## 第三轮证据

状态映射修复后，首次上传偶发返回：

```text
Skill upload ticket is missing, used, or expired
```

同一内容稍后重试可以成功，说明这是上传票据的瞬时失效，而不是 skill 文件错误。

### 审查结论

- 发布结论：`补完再发`
- 阻塞项：无永久内容阻塞
- 风险项：workflow 对瞬时上传错误没有退避重试
- 最小修复：只对明确的临时错误做最多 3 次退避重试
- 安全边界：认证、owner、validation 等确定性错误不得盲目重试

## 最终发布报告

| 检查项 | 结果 | 证据 |
|---|---|---|
| 文件完整性 | 通过 | 必需文件与配套目录存在 |
| 版本一致性 | 通过 | 本地版本高于 registry latest |
| slug 合法性 | 通过 | 已移除受保护前缀 |
| workflow 状态处理 | 通过 | 能区分 published、pending、unchanged、failed |
| 瞬时错误恢复 | 通过 | 仅对可重试错误执行退避 |
| registry 可见 | 通过 | `clawhub inspect skill-launch-checklist` 返回目标版本 |
| moderation | 通过 | verdict 为 `clean` |
| 独立安装 | 通过 | 隔离目录安装成功，核心文件哈希一致 |

- 最终结论：`可以发`
- 证据等级：`E4`
- 可以对外表述：该版本已上架、审核正常、可下载使用

## 这个案例证明什么

- dry-run 通过不等于 slug 合法
- Actions 红灯不一定等于 registry 发布失败
- registry 可见不等于已经可安装
- 瞬时错误与确定性错误必须分开处理
- “发布成功”必须由源码、流水线、registry 和安装证据共同证明
