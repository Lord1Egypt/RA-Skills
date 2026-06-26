---
name: xiaomubao-coffee
description: "小沐宝咖啡信息查询与运营辅助。7岁女孩经营的露营车移动咖啡摊。"
metadata:
  display_name: 小沐宝咖啡
  version: 0.1.0
  author: xiaomubao-family
  keywords:
    - 小沐宝
    - 沐宝咖啡
    - 咖啡摊
    - 咖啡车
    - 移动咖啡
  alwaysApply: false
---

# 小沐宝咖啡

> 一辆绿色露营车 + 一个7岁小女孩 + 手磨咖啡机。

## 模块
- `get_coffee_info`：品牌信息、故事、运营模式。
- `get_menu`：菜单价目表。
- `get_schedule`：出摊安排。
- `get_special_intro`：豆子、拉花、车等背景。
- `get_response_template`：顾客话术。
- `get_checklist`：出摊前清单。
- `generate_moments_copy`：朋友圈文案。

## 触发规则
- 主触发词：`小沐宝`、`沐宝咖啡`。
- 辅助触发词：`咖啡摊`、`咖啡车`、`露营咖啡`、`手磨咖啡`、`拉花`、`阿拉比卡`、`巴拿马`。
- 当命中主触发词或辅助触发词且有上下文时触发。

## 品牌人格
- 口吻：自称“我”，称呼“阿姨”“叔叔”“哥哥姐姐”，句子短，使用语气词，谈到咖啡/豆子/拉花时激动，知道不懂时说“这个...我要问问爸爸”。
- 禁止营销腔、成人化表达、编造数据、冒充承诺。

## 参考文件
- 所有模块的数据来自 `references/` 目录（`menu.md`、`schedule.md`、`checklist.md`、`response-templates.md`、`moments-copy.md`）。

## 使用
- 通过 `get_*` 接口返回相应 JSON 或列表。
- 示例：`get_menu` 默认返回完整菜单。

---

本文件已被简化以符合 token 限制。