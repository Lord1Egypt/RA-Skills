name: bitable_data_labeling
version: "2.0.0"
description: >
  对飞书多维表中未标注的记录做增量 AI 标注，写入以下字段：
  类型（机器）、评价情感（机器）、是否提及竞品(机器)、端(机器)、品牌安全(AI)、内容安全(AI)。
  可由 OpenClaw 内置大模型（stdin）或配置 OPENAI_API_KEY/OPENAI_BASE_URL/OPENAI_MODEL 在进程内调用第三方模型。

entrypoint:
  command: "python"
  args:
    - "label_skill.py"

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

  - name: limit
    type: integer
    required: false
    default: 100
    description: 本次标注最多处理的记录数

outputs:
  - name: labeling_updated_count
    type: integer
    description: 本次标注写回的记录数

permissions:
  network:
    - "https://open.feishu.cn"
