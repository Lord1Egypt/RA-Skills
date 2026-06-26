# 多维表 → 飞书群 Webhook 推送 Skill（OpenClaw 可发布包）

本目录为 **从飞书多维表自动推送消息到群 Webhook** 的 OpenClaw Skill，可直接上传到 Clawhub 使用。

## 能力说明

- 从指定多维表视图（`bitable_url`）中拉取最多 `limit` 条记录；
- 使用用户提供的 **触发条件表达式**（`rule_expression`）筛选需要推送的记录；
- 使用 **消息模版**（`message_template`）渲染文本内容；
- 将结果以文本消息推送到指定的飞书群机器人 `webhook_url`；
- 使用单一字段「是否推送」管理推送状态，避免重复推送。

> 字段「是否推送」的语义：
> - 空：尚未判断
> - 不推送：已判断，不符合推送条件
> - 待推送：本次命中推送条件，准备推送
> - 已推送：已成功推送

## SKILL.md 概览

- **名称**：`bitable_to_feishu_webhook`
- **版本**：1.1.0
- **入口**：`python push_skill.py`
- **必填入参**：
  - `bitable_url`：多维表视图链接
  - `app_id` / `app_secret`：飞书应用凭证（用于获取 tenant_access_token）
  - `webhook_url`：飞书群机器人 Webhook 地址
  - `rule_expression`：触发条件表达式（Python 表达式）
  - `message_template`：推送内容模版
- **可选入参**：
  - `limit`：本次最多检查/推送的记录数（默认 50）
- **输出**：
  - `pushed_count`：本次实际推送的消息条数

## 触发条件示例（rule_expression）

```python
# 示例 1：负向情感 + 正文包含“小米”
("负向" in fields.get("评价情感（机器）", "")) and ("小米" in fields.get("正文", ""))

# 示例 2：品牌安全命中
fields.get("品牌安全(AI)", "") == "是"
```

## 消息模版示例（message_template）

```text
【负向舆情预警】
标题：{标题}
情感：{评价情感（机器）}
类型：{类型（机器）}
品牌安全：{品牌安全(AI)}
正文：{正文}
链接：{原文 URL}
```

占位符 `{字段名}` 对应多维表中的字段名，未找到的字段会渲染为空字符串。

