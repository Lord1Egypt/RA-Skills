name: xiaoai_sync_and_label
version: "2.1.0"
description: >
  先从小爱数据接口增量拉取数据写入飞书多维表，再对多维表做增量标注：
  类型（机器）、评价情感（机器）、是否提及竞品(机器)、端(机器)、品牌安全(AI)、内容安全(AI)。
  可选开启标注：设置 run_labeling=true，标注由 OpenClaw 内置大模型提供（通过 stdin 或内置模型调用传入模型输出）。

entrypoint:
  command: "python"
  args:
    - "sync_and_label_skill.py"

inputs:
  - name: minutes
    type: integer
    required: false
    default: 60
    description: 同步时间窗口，往前补偿的分钟数（基于当前时间）

  - name: folder_id
    type: integer
    required: false
    default: 763579
    description: 小爱接口 folder_id

  - name: customer_id
    type: string
    required: false
    default: "xmxa"
    description: 小爱接口 customer_id

  - name: app_id
    type: string
    required: true
    description: 飞书开放平台应用 APP_ID

  - name: app_secret
    type: string
    required: true
    description: 飞书开放平台应用 APP_SECRET

  - name: xiaoai_token
    type: string
    required: true
    description: 小爱接口 token（Bearer 后面的部分）

  - name: bitable_url
    type: string
    required: true
    description: 目标飞书多维表视图链接（包含 base/app_token 和 table 参数）

  - name: xiaoai_base_url
    type: string
    required: false
    default: "http://wisers-data-service.wisersone.com.cn"
    description: 小爱 API 基础域名

  - name: run_labeling
    type: boolean
    required: false
    default: false
    description: 同步完成后是否执行多维表增量标注（类型（机器）、评价情感（机器）、是否提及竞品(机器)、端(机器)、品牌安全(AI)、内容安全(AI)）

  - name: labeling_limit
    type: integer
    required: false
    default: 100
    description: 本次标注最多处理的记录数

outputs:
  - name: inserted_count
    type: integer
    description: 本次同步写入多维表的记录数

  - name: labeling_updated_count
    type: integer
    description: 本次标注写回的记录数（未开启标注时为 0）

permissions:
  network:
    - "https://open.feishu.cn"
    - "http://wisers-data-service.wisersone.com.cn"
