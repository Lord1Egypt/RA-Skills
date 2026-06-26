---
name: index-official-website-demand-dev
description: 修改官网项目代码并同步需求文档。用于用户提供一大段产品需求、项目路径和可选分支后，将其写入指定项目目录下的 productdemand.md、先做小时级备份、切换并更新目标分支、按需求修改项目代码、执行基础校验、最后 git commit、git push 到远端分支，并在 push 成功后通过企业微信 webhook 发送包含时间和代码变动点的通知。适用于官网需求变更、页面调整、文案/交互更新、组件改造、SEO/展示内容修改等开发任务。
---

# 官网需求开发（项目路径外部传入）

## 概览

这个 skill 用于把用户给的一大段需求落地到**指定项目路径**中，并强制留下需求快照、git 变更记录，以及 push 成功后的企业微信通知。

这里**不再写死项目路径**。

执行时必须明确：

- `project_dir`：项目路径
- `branch`：目标分支，默认 `feat/test`
- `demand_file_name`：需求文件名，默认 `productdemand.md`

## 企业微信通知规则

push 成功后，必须发送 webhook 通知。

通知 `content` 字段至少包含：

- 时间
- 项目路径
- 分支
- commit 信息
- 代码变动点

如果没有单独整理摘要，允许自动回退为最近一次 commit 的文件列表。

## 推荐命令

更新需求文档：

```bash
bash scripts/update_productdemand.sh <project-dir> /tmp/productdemand-input.md
```

运行 git + push + 通知：

```bash
bash scripts/run_git_flow.sh <project-dir> <branch> <summary-file> <file1> [file2 ...]
```

## 资源

### scripts/push_wecom_push_notice.py

作用：
- 读取最近一次 commit
- 组合时间 + 代码变动点
- 调用企业微信 webhook 发送通知

### scripts/run_git_flow.sh

作用：
- 更新目标分支
- 生成提交时间戳
- 执行 add / commit / push
- push 成功后自动发送企业微信通知

## 失败处理

- 缺少项目路径：停止并追问。
- `git pull --ff-only` 失败：停止并告诉用户分支存在冲突或本地分叉。
- 校验失败：不要强推；先汇报失败项和日志摘要。
- push 失败：不要发成功通知；报告远端拒绝原因。
- webhook 失败：明确告诉用户“代码已 push，但通知发送失败”。
