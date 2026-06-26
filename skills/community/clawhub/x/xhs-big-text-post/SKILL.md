---
name: xhs-big-text-post
description: 小红书大字图全流程制作技能。当用户需要制作小红书配图（带文字的大图、卖点图）时触发。完整流程：理解需求 → 精炼文案 → 用 AI 生成底图 → 叠加文字 → 通过飞书发出。所有图片存 /workspace/xhs/。
author: cleanbing (cleanbing@qq.com) (AI生产力廖老师)
---

# XHS 大字图制作

## 工作目录
`/workspace/xhs/`（所有图片存此处）

## 流程（5步）

### Step 1 — 理解需求
用户发来一段文字，用最简洁的方式提炼核心文案，控制在20字以内。
> 原则：一个卖点，一句话，一个认知

### Step 2 — 设计视觉隐喻
根据文案设计视觉概念（不要直接照搬字面）。

**常见模式：**
| 主题 | 视觉隐喻 |
|------|---------|
| 对比/不是一回事 | 左右分栏，箭头区隔 |
| 警告/禁止 | 红色警告框，叉号 |
| 层级/阶梯 | 蛋糕/阶梯/金字塔 |
| 变身/进化 | 破壳/蜕变/光效 |
| 组合/打包 | 拼图/盒子/容器 |

### Step 3 — 生成底图
调用 `image_synthesize`，描述画面：
```
小红书配图风格，[描述视觉概念]，深色背景，整体简约高级
```
输出路径：`/workspace/xhs/xhs_[序号]_base.png`

### Step 4 — 叠加文字
用 `images_understand` 确认底图效果。
然后调用 `image_synthesize`，以底图为参考图（input_files），在图片中下方叠加文字。

输出路径：`/workspace/xhs/xhs_[序号]_final.png`

### Step 5 — 发送飞书
调用 `message(action=send, channel=feishu, media=图片CDN路径)`，把最终成品发给廖老师。

## 参考文档
详细工具说明和工作流见 `references/workflow.md`
