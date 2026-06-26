---
name: python-ysddata-keliu
description: 查询客流数据，输出JSON，适合直接导入 Bitable 或其它数据可视化工具
---

# 技能:查询客流数据

# 用法（聊天框直接说）
  -查询2026年4月1日到4月10日客流

# 例子
  - 查询{start}到{end}客流
  - 查{start}至{end}客流
  - 获取{start}至{end}客流
  - 拉取{start}到{end}客流数据
params:
  start:
    type: date
    help: 开始日期，例如 2026-04-01
  end:
    type: date
    help: 结束日期，例如 2026-04-10

# 运行
```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\python-ysddata-keliu\commands
python query.py --start 2026-04-01 --end 2026-04-10
```