---
name: index-official-website-demand-change
description: 一键执行官网项目需求变更。用于用户粘贴一大段新需求并同时提供项目路径后，自动在指定项目目录上完成：检查目标分支工作区是否干净、拉取最新代码、把需求写入 productdemand.md 并做小时级备份、根据需求修改代码、运行必要检查、git commit、push，并在 push 成功后通过企业微信 webhook 发送包含时间和代码变动点的通知。适合“官网改动：需求正文 + 项目路径 + 分支”这类一键执行请求。
---

# 官网需求变更（一键执行，项目路径外部传入）

## 概览

这个 skill 的目标是：用户贴需求并提供项目路径后，直接完成从需求入库到代码 push 的完整流程，并在 push 成功后发送企业微信通知。

这里**不再写死项目路径**。

执行时必须从用户输入或当前任务上下文中明确这三个参数：

- `project_dir`：项目路径，例如 `/Users/dyshi/work/index-official-website`
- `target_branch`：目标分支，默认 `feat/test`
- `demand_file_name`：需求文件名，默认 `productdemand.md`

## 企业微信通知规则

push 成功后，必须发送 webhook 通知。

通知正文写入 `content` 字段，内容至少包含：

- 时间
- 项目路径
- 分支
- commit 信息
- 代码变动点

格式示例：

```text
时间：2026-03-10 16:20:00
项目：/path/to/project
分支：feat/test
提交：abc1234 chore: 官网需求变更-20260310-162000
代码变动点：
- 修改首页 SEO title 与 description
- 调整友情链接字体样式
- 更新 productdemand.md
```

如果没有人工整理的“代码变动点”，可以退化成最近一次 commit 涉及的文件列表。

## 资源

### scripts/push_wecom_push_notice.py

用法：

```bash
python3 scripts/push_wecom_push_notice.py --project-dir <project-dir> --branch <branch> --commit-ref HEAD --summary-file <summary-file>
```

### scripts/git_commit_and_push.sh

用法：

```bash
bash scripts/git_commit_and_push.sh <project-dir> [branch] [summary-file]
```

说明：
- push 成功后会自动调用企业微信通知脚本。

## 其他执行规则

- 若用户没有显式提供项目路径，就先追问项目路径；不要默认写死到某个目录。
- 预检 Git 工作区并同步目标分支。
- 备份并写入 `productdemand.md`。
- 启动编码子代理，根据需求文件修改代码。
- 运行必要检查。
- `git commit`
- `git push origin <target_branch>`
- push 成功后发送企业微信通知。
- 向用户汇报结果。

## 失败处理

- 缺少项目路径：停止并向用户追问。
- 需求为空：停止。
- 工作区脏：停止并报告脏文件。
- pull 失败：停止并报告。
- 检查失败：不要伪装成功。
- push 失败：不要发成功通知；把 git 输出摘要返回给用户。
- webhook 失败：明确告诉用户“代码已 push，但通知发送失败”。
