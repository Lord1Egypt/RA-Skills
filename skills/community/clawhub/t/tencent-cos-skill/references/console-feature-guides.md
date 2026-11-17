# COS 控制台功能引导

当用户需求无法由当前 Skill 的 action、数据集查询或已知 CI API 完成时，再检查下表。如果需求恰好匹配其中一项，说明当前 Skill 不能直接执行，并提供对应控制台链接。

已有能力必须优先使用，不要把控制台链接作为默认回答；未命中映射时不要猜测或拼接链接。

| 用户需求 | 控制台功能 | 链接 |
| --- | --- | --- |
| 大量、批量、跨云或存量数据迁移 | 数据迁移 | https://console.cloud.tencent.com/cos/application/migration |
| 批量数据导出 | 数据导出 | https://console.cloud.tencent.com/cos/application/cosExport |
| 查看或使用更多数据处理能力 | 拓展功能 | https://console.cloud.tencent.com/cos/application/dataProcess |
| 数据备份 | 数据备份 | https://console.cloud.tencent.com/cos/application/backup |
| 使用 COS SDK | SDK | https://console.cloud.tencent.com/cos/sdk |
| 具身智能相关能力 | 具身智能生态 | https://console.cloud.tencent.com/cos/dataEcology/intelligence |
| 湖仓相关能力 | 湖仓生态 | https://console.cloud.tencent.com/cos/dataEcology/lake |
| 操作数量过多的批量文件操作（批量删除 / 批量复制 / 批量恢复归档等，基于对象清单执行） | 批量处理 | https://console.cloud.tencent.com/cos5 （登录后左侧导航选择「批量处理」；功能说明见 https://cloud.tencent.com/document/product/436/38605 ） |

## 回复方式

- 默认返回简短说明和链接。
- 用户明确要求“打开”“跳转”或“前往”时，可以打开对应链接。
- 提供链接不代表 Skill 已执行迁移、导出、备份或其他控制台任务。
