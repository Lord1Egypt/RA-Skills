---
name: repo-mirror-sync-sample
version: 0.1.0
description: |
  演示技能：验证 repo-mirror-sync 分发链路的样例 skill。包含完整 SKILL.md、
  scripts 与 references 的多文件布局，用于端到端回归验证（发布/认领/版本递增/黑名单）。
tools:
  - bash
---

# repo-mirror-sync-sample

## 定位与职责

repo-mirror-sync-sample 是同步分发链路的回归样本：验证一个包含 SKILL.md、
scripts 与 references 的多文件技能能否被完整采集、指纹稳定、并按 semver 递增
发布到注册表。它不产生真实业务副作用，仅用于链路自检。

## 使用方式

```bash
bash scripts/run.sh <input>
```

脚本对输入做规范化哈希输出，供断言使用。

## 实现说明

- 指纹 = 目录内全部文件按路径排序拼接的 SHA-256（排除 __pycache__/pyc）；
- 版本 = 由分发链路按 1.0.0 → 1.0.1 → … 自动维护，不回写 frontmatter；
- 黑名单路径不进注册表、内容仍随 git 镜像分发。

## 参考

- 使用说明：`references/usage.md`
