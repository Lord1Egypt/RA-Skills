name: xiaoai_sync_to_bitable
version: "2.0.0"
description: >
  从惠科/小爱数据接口增量拉取数据，写入飞书多维表。
  支持单表 10000 条自动分表；不包含标注逻辑。

entrypoint:
  command: "python"
  args:
    - "sync_skill.py"

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
    description: 小爱/惠科接口 token（Bearer 后面的部分）

  - name: bitable_url
    type: string
    required: true
    description: 目标飞书多维表视图链接（包含 base/app_token 和 table 参数）

  - name: xiaoai_base_url
    type: string
    required: false
    default: "http://wisers-data-service.wisersone.com.cn"
    description: 惠科/小爱 API 基础域名

outputs:
  - name: inserted_count
    type: integer
    description: 本次同步写入多维表的记录数

permissions:
  network:
    - "https://open.feishu.cn"
    - "http://wisers-data-service.wisersone.com.cn"
