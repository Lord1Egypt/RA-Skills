# 平台输入与执行边界

- TEMU：每个货号至少五张图、英文标题和产品模板，按店铺分别建任务。
- Ozon POD：按已确认模板拆批，核对俄文标题、价格与图片；使用同一模板的商品须匹配其类目和属性。
- Ozon 标品：逐商品准备完整 ozon_item_json、类目/类型、俄文标题、售价、包装尺寸重量、真实类目属性及图片。
- Wildberries（WB）：逐商品准备完整 wb_request_json，包括类目、variants、价格/折扣、仓库与库存；合法属性值从当前平台响应读取。

先调用 ptj_listing_reference，再预检；客户端创建任务不代表平台上架成功。结果未知先查任务，不能盲目重提。详细字段见 [统一数据包](data-contract.md) 和 [工具契约](mcp-contract.md)。
