---
name: modify-draft
description: "修改 VectCut 草稿基础信息（草稿名与封面图）。当草稿内容整理完成、需要把默认 dfd_xxx 名称改成可读名称，或用户明确要求修改草稿名/封面时，务必使用本技能。官网接口文档：https://docs.vectcut.com/429210482e"
---

# Modify Draft Skill

用于修改草稿的基础信息，支持：
- 修改草稿名称 `name`
- 修改草稿封面 `cover`

官网接口文档：
- https://docs.vectcut.com/429210482e

## 适用场景

- 草稿内容已整理完成，需要把默认 `dfd_xxx` 编码名改成可读名称
- 用户明确要求“改草稿名”“换封面”“设置封面图”
- 发布前需要补齐草稿展示信息

## 前置条件

- Python 3
- 已安装 `requests`
- 先检查环境变量 `VECTCUT_API_KEY`；若未设置，必须先调用 `vectcut-login` skill 完成登录与 token 校验，再继续本技能

## 执行方式

至少传入 `--name` 或 `--cover` 之一：

```bash
python <skill-path>/scripts/modify_draft.py "<draft_id>" --name "测试草稿100"
```

```bash
python <skill-path>/scripts/modify_draft.py "<draft_id>" --cover "https://example.com/cover.png"
```

```bash
python <skill-path>/scripts/modify_draft.py "<draft_id>" --name "测试草稿100" --cover "https://example.com/cover.png"
```

## 输出

脚本返回结构化 JSON，包含：
- `success`
- `draft_id`
- `draft_url`
- `name`（若接口返回）
- `cover`（若接口返回）

## 参数说明

| 参数 | 必填 | 说明 |
|---|---|---|
| `draft_id` | 是 | 草稿 ID |
| `name` | 否 | 草稿名称 |
| `cover` | 否 | 封面图 URL |

## 错误处理

- 若 `VECTCUT_API_KEY` 缺失：先调用 `vectcut-login`，登录成功后重试
