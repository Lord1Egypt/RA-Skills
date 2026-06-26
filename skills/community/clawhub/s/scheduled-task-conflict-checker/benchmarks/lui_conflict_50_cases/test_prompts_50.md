# 定时任务冲突检测 50 组 Benchmark

每组测试均包含 `initial_tasks`，用于模拟用户已经配置过的定时任务；runner 在每个 case 前写入临时任务池，在每个 case 后删除临时任务池，避免污染下一组。

## case_001｜店铺绑定/授权边界｜无绑定店铺时阻断创建

- 已有任务数：0
- 新 LUI 请求：每天9点帮我同步库存
- 预期决策：`block`
- 预期原因码：`no_bound_shop`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_001/input.json`

## case_002｜店铺绑定/授权边界｜单店未指定范围时默认该店铺

- 已有任务数：0
- 新 LUI 请求：每天9点同步库存
- 预期决策：`proceed`
- 预期原因码：`none`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_002/input.json`

## case_003｜店铺绑定/授权边界｜多店未指定范围要求用户选择

- 已有任务数：0
- 新 LUI 请求：每天9点同步库存
- 预期决策：`ask_confirmation`
- 预期原因码：`shop_scope_missing`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_003/input.json`

## case_004｜店铺绑定/授权边界｜指定未绑定店铺时阻断

- 已有任务数：0
- 新 LUI 请求：每天9点同步未绑定店铺库存
- 预期决策：`block`
- 预期原因码：`shop_not_bound`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_004/input.json`

## case_005｜店铺绑定/授权边界｜目标店铺授权失效时阻断

- 已有任务数：0
- 新 LUI 请求：每天9点同步失效店铺库存
- 预期决策：`block`
- 预期原因码：`authorization_invalid`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_005/input.json`

## case_006｜店铺绑定/授权边界｜部分店铺授权失效时部分创建

- 已有任务数：0
- 新 LUI 请求：每天9点同步两个店铺库存
- 预期决策：`partial_create`
- 预期原因码：`authorization_invalid`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_006/input.json`

## case_007｜店铺绑定/授权边界｜全部店铺均有效可创建

- 已有任务数：0
- 新 LUI 请求：每天9点给全部店铺做巡检
- 预期决策：`proceed`
- 预期原因码：`none`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_007/input.json`

## case_008｜店铺绑定/授权边界｜已删除历史任务不参与重复判断

- 已有任务数：1
- 新 LUI 请求：每天9点同步库存
- 预期决策：`proceed`
- 预期原因码：`none`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_008/input.json`

## case_009｜ISV高级版权限边界｜高级版任务付费店铺允许

- 已有任务数：0
- 新 LUI 请求：每天9点做高级铺货
- 预期决策：`proceed`
- 预期原因码：`none`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_009/input.json`

## case_010｜ISV高级版权限边界｜高级版任务未付费店铺阻断

- 已有任务数：0
- 新 LUI 请求：每天9点做高级铺货
- 预期决策：`block`
- 预期原因码：`sv_advanced_permission_missing`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_010/input.json`

## case_011｜ISV高级版权限边界｜多店部分付费时部分创建

- 已有任务数：0
- 新 LUI 请求：每天9点给两个店做高级铺货
- 预期决策：`partial_create`
- 预期原因码：`sv_advanced_permission_missing`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_011/input.json`

## case_012｜ISV高级版权限边界｜ISV接口参数错误阻断

- 已有任务数：0
- 新 LUI 请求：每天9点做高级铺货
- 预期决策：`block`
- 预期原因码：`sv_advanced_permission_missing`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_012/input.json`

## case_013｜ISV高级版权限边界｜ISV接口500不能误判为免费而是阻断校验

- 已有任务数：0
- 新 LUI 请求：每天9点做高级铺货
- 预期决策：`block`
- 预期原因码：`sv_advanced_permission_missing`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_013/input.json`

## case_014｜ISV高级版权限边界｜ISV状态缺失时阻断

- 已有任务数：0
- 新 LUI 请求：每天9点做高级铺货
- 预期决策：`block`
- 预期原因码：`sv_advanced_permission_missing`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_014/input.json`

## case_015｜ISV高级版权限边界｜普通任务不要求ISV权限

- 已有任务数：0
- 新 LUI 请求：每天9点同步库存
- 预期决策：`proceed`
- 预期原因码：`none`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_015/input.json`

## case_016｜ISV高级版权限边界｜权益文本识别ISV高级版

- 已有任务数：0
- 新 LUI 请求：帮我创建需要ISV高级版的自动换供任务
- 预期决策：`block`
- 预期原因码：`sv_advanced_permission_missing`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_016/input.json`

## case_017｜平台能力不支持｜抖音不支持改价时阻断

- 已有任务数：0
- 新 LUI 请求：每天9点给抖音店铺自动改价
- 预期决策：`block`
- 预期原因码：`platform_capability_missing`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_017/input.json`

## case_018｜平台能力不支持｜小红书不支持自动跟单时阻断

- 已有任务数：0
- 新 LUI 请求：每天9点给小红书店铺自动跟单
- 预期决策：`block`
- 预期原因码：`platform_capability_missing`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_018/input.json`

## case_019｜平台能力不支持｜部分平台支持时部分创建

- 已有任务数：0
- 新 LUI 请求：每天9点给所有店铺自动跟单
- 预期决策：`partial_create`
- 预期原因码：`platform_capability_missing`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_019/input.json`

## case_020｜平台能力不支持｜支持平台的改价进入正常检测

- 已有任务数：0
- 新 LUI 请求：每天9点给拼多多店铺自动改价
- 预期决策：`proceed`
- 预期原因码：`none`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_020/input.json`

## case_021｜平台能力不支持｜未知平台能力不在创建前阻断

- 已有任务数：0
- 新 LUI 请求：每天9点给自定义平台做巡检
- 预期决策：`proceed`
- 预期原因码：`none`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_021/input.json`

## case_022｜重复检测｜库存同步完全重复复用

- 已有任务数：1
- 新 LUI 请求：每天9点再同步一次库存
- 预期决策：`reuse_or_update`
- 预期原因码：`complete_duplicate`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_022/input.json`

## case_023｜重复检测｜日报语义重复复用

- 已有任务数：1
- 新 LUI 请求：每天晚上8点给我经营报告
- 预期决策：`reuse_or_update`
- 预期原因码：`complete_duplicate`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_023/input.json`

## case_024｜重复检测｜不同时间同目标语义重复复用

- 已有任务数：1
- 新 LUI 请求：每天10点再做店铺巡检
- 预期决策：`reuse_or_update`
- 预期原因码：`semantic_duplicate`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_024/input.json`

## case_025｜重复检测｜选品被选品加铺货流程覆盖静默合并

- 已有任务数：1
- 新 LUI 请求：每天9点选品并自动铺货
- 预期决策：`silent_merge`
- 预期原因码：`process_duplicate`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_025/input.json`

## case_026｜重复检测｜已有铺货流程覆盖新增选品

- 已有任务数：1
- 新 LUI 请求：每天9点只做选品
- 预期决策：`silent_merge`
- 预期原因码：`process_duplicate`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_026/input.json`

## case_027｜重复检测｜不同店铺相同任务不重复但同平台排队信息保留

- 已有任务数：1
- 新 LUI 请求：每天9点同步A店库存
- 预期决策：`proceed`
- 预期原因码：`same_platform_rate_limit`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_027/input.json`

## case_028｜重复检测｜暂停中的相同任务仍参与去重

- 已有任务数：1
- 新 LUI 请求：每天9点同步库存
- 预期决策：`reuse_or_update`
- 预期原因码：`complete_duplicate`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_028/input.json`

## case_029｜重复检测｜平台不同但店铺范围重叠时按店铺识别重复

- 已有任务数：1
- 新 LUI 请求：每天9点巡检这个店铺
- 预期决策：`reuse_or_update`
- 预期原因码：`complete_duplicate`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_029/input.json`

## case_030｜重复检测｜库存管理别名标准化后识别重复

- 已有任务数：1
- 新 LUI 请求：每天9点做库存管理
- 预期决策：`reuse_or_update`
- 预期原因码：`complete_duplicate`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_030/input.json`

## case_031｜策略部分重复｜铺货利润率阈值变化要求确认

- 已有任务数：1
- 新 LUI 请求：每天9点铺货利润率10%以上商品
- 预期决策：`ask_confirmation`
- 预期原因码：`strategy_partial_duplicate`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_031/input.json`

## case_032｜策略部分重复｜铺货最大数量变化要求确认

- 已有任务数：1
- 新 LUI 请求：每天9点铺货最多100个商品
- 预期决策：`ask_confirmation`
- 预期原因码：`strategy_partial_duplicate`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_032/input.json`

## case_033｜策略部分重复｜库存同步字段变化要求确认

- 已有任务数：1
- 新 LUI 请求：每天9点同步库存和价格字段
- 预期决策：`ask_confirmation`
- 预期原因码：`strategy_partial_duplicate`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_033/input.json`

## case_034｜策略部分重复｜巡检过滤条件变化要求确认

- 已有任务数：1
- 新 LUI 请求：每天9点巡检全部风险商品
- 预期决策：`ask_confirmation`
- 预期原因码：`strategy_partial_duplicate`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_034/input.json`

## case_035｜策略部分重复｜换供商品范围变化要求确认

- 已有任务数：1
- 新 LUI 请求：每天9点给全部商品智能换供
- 预期决策：`ask_confirmation`
- 预期原因码：`strategy_partial_duplicate`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_035/input.json`

## case_036｜策略部分重复｜跟单订单范围变化要求确认

- 已有任务数：1
- 新 LUI 请求：每天9点跟进24小时未发货订单
- 预期决策：`ask_confirmation`
- 预期原因码：`strategy_partial_duplicate`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_036/input.json`

## case_037｜高风险重复｜改价任务重叠要求确认

- 已有任务数：1
- 新 LUI 请求：每天10点再自动降价10%
- 预期决策：`ask_confirmation`
- 预期原因码：`high_risk_duplicate`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_037/input.json`

## case_038｜高风险重复｜下架任务重叠要求确认

- 已有任务数：1
- 新 LUI 请求：每天10点下架60天无动销商品
- 预期决策：`ask_confirmation`
- 预期原因码：`high_risk_duplicate`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_038/input.json`

## case_039｜高风险重复｜同一改价任务不同时间也要求确认

- 已有任务数：1
- 新 LUI 请求：每天晚上8点也做低利润商品改价
- 预期决策：`ask_confirmation`
- 预期原因码：`high_risk_duplicate`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_039/input.json`

## case_040｜高风险重复｜同店铺批量下架策略不同要求确认

- 已有任务数：1
- 新 LUI 请求：每天9点下架低分商品
- 预期决策：`ask_confirmation`
- 预期原因码：`high_risk_duplicate`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_040/input.json`

## case_041｜高风险重复｜高风险完全重复仍复用不新建

- 已有任务数：1
- 新 LUI 请求：每天9点自动降价5%
- 预期决策：`reuse_or_update`
- 预期原因码：`complete_duplicate`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_041/input.json`

## case_042｜高风险重复｜不同店铺高风险任务不冲突但同平台排队信息保留

- 已有任务数：1
- 新 LUI 请求：每天9点给A店改价
- 预期决策：`proceed`
- 预期原因码：`same_platform_rate_limit`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_042/input.json`

## case_043｜高频堆积｜每5分钟库存同步需要风险提示

- 已有任务数：0
- 新 LUI 请求：每5分钟同步一次库存
- 预期决策：`warn_then_proceed`
- 预期原因码：`high_frequency_accumulation`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_043/input.json`

## case_044｜高频堆积｜每10分钟巡检需要风险提示

- 已有任务数：0
- 新 LUI 请求：每10分钟巡检店铺风险
- 预期决策：`warn_then_proceed`
- 预期原因码：`high_frequency_accumulation`
- 是否需要提示/确认：是
- Fixture：`fixtures/case_044/input.json`

## case_045｜高频堆积｜同平台同时间API任务只记录排队信息

- 已有任务数：1
- 新 LUI 请求：每天9点同步A店库存
- 预期决策：`proceed`
- 预期原因码：`same_platform_rate_limit`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_045/input.json`

## case_046｜高频堆积｜同店铺同时间不同商品写任务记录排队

- 已有任务数：1
- 新 LUI 请求：每天9点同步库存
- 预期决策：`proceed`
- 预期原因码：`same_platform_rate_limit`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_046/input.json`

## case_047｜通知边界｜微信未绑定时回退通知但任务可创建

- 已有任务数：0
- 新 LUI 请求：每天20点经营日报发微信通知
- 预期决策：`warn_then_proceed`
- 预期原因码：`wechat_not_bound`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_047/input.json`

## case_048｜通知边界｜微信已绑定时正常创建通知任务

- 已有任务数：0
- 新 LUI 请求：每天20点经营日报发微信通知
- 预期决策：`proceed`
- 预期原因码：`none`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_048/input.json`

## case_049｜正常可创建｜已有不同资源任务时可创建巡检

- 已有任务数：1
- 新 LUI 请求：每天9点巡检店铺风险
- 预期决策：`proceed`
- 预期原因码：`none`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_049/input.json`

## case_050｜正常可创建｜不同店铺不同任务可创建

- 已有任务数：1
- 新 LUI 请求：每天11点给A店生成经营日报
- 预期决策：`proceed`
- 预期原因码：`none`
- 是否需要提示/确认：否
- Fixture：`fixtures/case_050/input.json`
