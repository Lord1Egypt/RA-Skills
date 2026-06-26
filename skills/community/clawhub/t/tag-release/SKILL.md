---
name: tag-release
version: 1.0.1
description: "按日期规则为一个或多个微服务基于指定分支创建并推送远程 release tag。适用于用户明确要求打 release tag、批量打 tag、按日期生成 tag、或基于 test/master 等分支给服务发布 tag 的场景。模型只负责整理服务、分支、日期或 tag 名，实际执行必须调用本 skill 自带脚本。"
metadata:
  requires:
    bins: ["python3", "git"]
---

# tag-release

把“按分支给一个或多个服务打远程 release tag”的流程交给固定脚本处理；**不要让模型自己临时拼 git 命令批量打 tag**。

> 当前默认行为：**打 tag 时，同时创建同名 GitHub Release**。

## 何时使用

只有默认行为：
- 打 release tag
- **同时创建同名 GitHub Release**
- 按需返回 tag / release / PR 信息

以下情况不要触发本 skill：

- 只是讨论发版流程
- 只是查询当前 tag
- 只是要求部署，但没有要求打 tag
- 只是让你看 tag 脚本或评审实现

## 模型职责

模型只做这些事：

1. 判断用户是不是在明确要求“打 tag”
2. 提取服务列表
3. 判断目标分支
4. 判断是否要按日期生成 tag，还是使用指定 tag 名
5. 若用户给了 release 描述，则作为 tag message 传入；没给则自动用最新 PR 信息生成描述
6. 默认同时创建 **同名 GitHub Release**，标题与 tag 名一致
7. 需要预演时加 `--dry-run`
8. 调用固定脚本
9. 汇报结果

模型不要：

- 自己循环执行 git tag / git push
- 自己手写 tag 命名规则
- 跳过脚本直接对多个仓库执行危险命令

## 执行方式

脚本路径：`scripts/tag_release.py`

基础调用：

```bash
python3 <skill_dir>/scripts/tag_release.py \
  --services cloud-device cloud-data \
  --branch master
```

指定日期：

```bash
python3 <skill_dir>/scripts/tag_release.py \
  --services cloud-device \
  --branch master \
  --date 2026-05-18
```

指定完整 tag：

```bash
python3 <skill_dir>/scripts/tag_release.py \
  --services cloud-device \
  --branch master \
  --tag release-2.5.18
```

指定 release 描述：

```bash
python3 <skill_dir>/scripts/tag_release.py \
  --services cloud-device \
  --branch master \
  --message '修复设备分页和版本展示'
```

预演：

```bash
python3 <skill_dir>/scripts/tag_release.py \
  --services cloud-device cloud-data \
  --branch master \
  --dry-run
```

## 参数整理规则

- `--services`：直接使用 config.json 里的仓库键名；如果用户只说了模糊服务名，可先做一次合理匹配，但匹配到多个时要报错
- `--branch`：优先使用用户指定分支；**未指定时固定使用 `master`**
- `--date`：格式必须是 `YYYY-MM-DD`；未指定时默认今天
- `--tag`：若用户明确给出完整 tag，则直接使用，不再按日期规则生成
- `--message`：若用户明确给了 release 描述，则直接作为 annotated tag message；未给时自动用**最新 PR 信息**生成描述；若 PR 信息也拿不到，则回退为 `tag from origin/<branch>`
- `--dry-run`：当用户说“先看看/先预览/别真的打”时使用
- 如果用户只说“打 release tag”但没给服务范围，脚本默认会对 config.json 中全部 repos 生效；这种场景下最好先确认一次，避免误打全量

## 输出说明

成功时重点汇报：

- 实际处理了哪些服务
- 基于哪个分支打 tag
- 使用了哪个 tag 名
- 哪些服务成功创建/推送
- 哪些服务因 tag 已存在而跳过
- 是否只是 dry-run
- **最新合入 PR**（如果能拿到）
- **PR 提交人信息**（如果能拿到）
- **Tag 链接**
- **Release 链接**
- **Tag 描述 / tag message**

失败时直接汇报失败服务和原因，例如：

- 远程分支不存在
- tag 已存在但指向不同 commit
- git push 失败
- repo 目录不存在

## 额外返回信息

脚本执行成功后，回复里应尽量补充以下信息：

- 最新合入 PR 编号与标题（若 GitHub API 可获取）
- PR 提交人 / 作者
- Tag 链接
- Release 链接
- Tag 描述 / tag message
- 分支信息

如果 GitHub API 查询失败，不要因此阻塞打 tag 主流程；应明确说明“tag 已完成，但 PR 信息获取失败”。

## tag 规则说明

默认 tag 规则由脚本内置：

```text
release-{year_index}.{month}.{day:02d}
```

其中：

- `year_index = year - base_year`
- 默认 `base_year = 2024`

例如：

- 2025-05-18 → `release-1.5.18`
- 2026-05-18 → `release-2.5.18`

## 资源说明

- 脚本：`scripts/tag_release.py`
- 配置：`assets/config.json`

## 安全说明

- 该脚本会对远程仓库创建并 push tag，属于真实写操作
- 当用户未明确说明服务范围时，不要默认全量执行，先确认一次
- 当前 skill 使用的 `github_token` 允许用于这条固定链路：查询目标分支 commit、查询最新合入 PR、检查远程 tag / release、创建 annotated tag、创建 tag ref、创建 release
- **禁止**把这个 token 挪作他用，例如：通用 GitHub 浏览、PR 批量操作、issue 操作、仓库管理、权限变更、任意 GitHub API 探测
- 如果任务超出“为服务打 release tag”范围，即使能复用这个 token，也不要使用；应改走别的 skill / 别的凭据
- 不要在聊天里复述 token、仓库凭据等敏感信息
