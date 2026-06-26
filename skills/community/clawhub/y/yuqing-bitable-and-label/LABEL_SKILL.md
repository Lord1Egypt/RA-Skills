name: bitable_data_labeling
version: "1.0.0"
description: >
  在飞书多维表中通过特定提示词的逻辑，每条记录标注「类型（机器）」的值

entrypoint:
  command: "python"
  args:
    - "bitable_labeling_skill.py"

inputs:
  - name: bitable_url
    type: string
    required: true
    description: >
      目标飞书多维表视图链接（包含 base/app_token 和 table 参数）。
      建议使用带过滤/视图的链接，只包含需要做标注的记录。

  - name: label_status
    type: string
    required: false
    default: "待机器标注"
    description: 写入到「类型（机器）」字段的默认值。

  - name: limit
    type: integer
    required: false
    default: 100
    description: 本次最多生成标注提示词的记录条数（避免一次性处理太多）。

outputs:
  - name: updated_count
    type: integer
    description: 本次实际写回标注提示词的记录数。

permissions:
  network:
    - "https://open.feishu.cn"