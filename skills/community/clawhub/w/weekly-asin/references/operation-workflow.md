# Amazon ASIN 周报简报 专属运营工作流

固定契约：`weekly/asin` → `ops_weekly`。不得改成任意 prompt 或其他 focus。

1. `operations capabilities` 验证服务端能力。
2. `operations profile --asin <ASIN> --site <站点>` 检查商品字段。
3. `operations quote --asin <ASIN> --site <站点>` 返回报价与 requestId。
4. 用户明确确认后，以同一 requestId 执行 `operations run ... --confirm`。
5. 流中断后只运行 `operations status --request-id <原值>`，不得直接重跑。

## 不适用

- 未经确认自动调用付费 LLM
- 免费确定性 watch digest 或小时级监控
- 实时价格、销量、库存、广告、订单或真实退货率
