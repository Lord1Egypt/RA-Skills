# Amazon 评论证据文案规划 专属运营工作流

固定契约：`listing/full` → `ops_listing`。不得改成任意 prompt 或其他 focus。

1. `operations capabilities` 验证服务端能力。
2. `operations profile --asin <ASIN> --site <站点>` 检查商品字段。
3. `operations quote --asin <ASIN> --site <站点>` 返回报价与 requestId。
4. 用户明确确认后，以同一 requestId 执行 `operations run ... --confirm`。
5. 流中断后只运行 `operations status --request-id <原值>`，不得直接重跑。

## 不适用

- 没有商品和评论数据的自由创作
- 广告投放与关键词竞价
- 自动修改或发布 Amazon 页面
