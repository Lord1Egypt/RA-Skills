name: xiaoai_to_bitable
version: "1.0.0"
description: >
  从小爱数据接口增量拉取数据，并写入飞书多维表（支持 case_id 自增、入库时间为写入时间、按字段自动创建/映射）。

entrypoint:
  command: "python"
  args:
    - "xiaoai_to_bitable_skill.py"

inputs:
  - name: minutes
    type: integer
    required: false
    default: 60
    description: 往前补偿的分钟数（基于当前时间，默认 60 分钟）

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

  - name: bitable_url
    type: string
    required: false
    description: >
      目标飞书多维表视图链接（包含 base/app_token 和 table 参数）。
      若不提供，则使用脚本中内置的 BITABLE_URL。

outputs:
  - name: inserted_count
    type: integer
    description: 本次实际写入到多维表的记录数

permissions:
  network:
    - "https://open.feishu.cn"
    - "http://wisers-data-service.wisersone.com.cn"

