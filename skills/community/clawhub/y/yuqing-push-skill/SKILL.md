name: bitable_to_feishu_webhook
version: "1.1.0"
description: >
  从飞书多维表中按用户规则筛选记录，自动将格式化后的内容推送到指定的群机器人 Webhook（飞书群消息）。
  内部使用字段「是否推送」作为推送状态：
  - 空：尚未判断
  - 不推送：已判断，不符合推送条件
  - 待推送：本次命中推送条件，准备推送
  - 已推送：已成功推送
  本 Skill 仅扫描「是否推送」为空的记录。

entrypoint:
  command: "python"
  args:
    - "push_skill.py"

inputs:
  - name: bitable_url
    type: string
    required: true
    description: 目标飞书多维表视图链接（包含 base/app_token 和 table 参数）

  - name: app_id
    type: string
    required: true
    description: 飞书开放平台应用 APP_ID（用于获取 tenant_access_token）

  - name: app_secret
    type: string
    required: true
    description: 飞书开放平台应用 APP_SECRET

  - name: webhook_url
    type: string
    required: true
    description: 飞书群机器人的 Webhook 地址（例如 https://open.feishu.cn/open-apis/bot/v2/hook/xxx）

  - name: rule_expression
    type: string
    required: true
    description: |
      触发条件表达式（Python 表达式），返回 True/False。
      使用 fields['字段名'] 访问多维表字段，例如：
      "('负向' in fields.get('评价情感（机器）','')) and ('小米' in fields.get('正文',''))"

  - name: message_template
    type: string
    required: true
    description: |
      推送内容模版，使用 {字段名} 占位，如：
      "【负向舆情预警]\n标题：{标题}\n情感：{评价情感（机器）}\n正文：{正文}\n链接：{原文 URL}"

  - name: limit
    type: integer
    required: false
    default: 50
    description: 本次最多检查并推送的记录条数（按多维表视图排序）

outputs:
  - name: pushed_count
    type: integer
    description: 本次实际推送的消息条数

permissions:
  network:
    - "https://open.feishu.cn"

