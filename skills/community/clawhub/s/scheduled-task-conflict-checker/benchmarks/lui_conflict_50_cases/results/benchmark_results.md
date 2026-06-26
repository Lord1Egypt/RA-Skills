# 定时任务冲突检测 Benchmark 结果

- 总数：50
- 通过：50
- 失败：0
- 错误：0
- 运行结束后临时任务池是否仍存在：否

| Case | 类别 | 结果 | 预期 | 实际 | 原因码 |
| --- | --- | --- | --- | --- | --- |
| case_001 | 店铺绑定/授权边界 | pass | block | block | no_bound_shop |
| case_002 | 店铺绑定/授权边界 | pass | proceed | proceed | none |
| case_003 | 店铺绑定/授权边界 | pass | ask_confirmation | ask_confirmation | shop_scope_missing |
| case_004 | 店铺绑定/授权边界 | pass | block | block | shop_not_bound |
| case_005 | 店铺绑定/授权边界 | pass | block | block | authorization_invalid |
| case_006 | 店铺绑定/授权边界 | pass | partial_create | partial_create | authorization_invalid |
| case_007 | 店铺绑定/授权边界 | pass | proceed | proceed | none |
| case_008 | 店铺绑定/授权边界 | pass | proceed | proceed | none |
| case_009 | ISV高级版权限边界 | pass | proceed | proceed | none |
| case_010 | ISV高级版权限边界 | pass | block | block | sv_advanced_permission_missing |
| case_011 | ISV高级版权限边界 | pass | partial_create | partial_create | sv_advanced_permission_missing |
| case_012 | ISV高级版权限边界 | pass | block | block | sv_advanced_permission_missing |
| case_013 | ISV高级版权限边界 | pass | block | block | sv_advanced_permission_missing |
| case_014 | ISV高级版权限边界 | pass | block | block | sv_advanced_permission_missing |
| case_015 | ISV高级版权限边界 | pass | proceed | proceed | none |
| case_016 | ISV高级版权限边界 | pass | block | block | sv_advanced_permission_missing |
| case_017 | 平台能力不支持 | pass | block | block | platform_capability_missing |
| case_018 | 平台能力不支持 | pass | block | block | platform_capability_missing |
| case_019 | 平台能力不支持 | pass | partial_create | partial_create | platform_capability_missing |
| case_020 | 平台能力不支持 | pass | proceed | proceed | none |
| case_021 | 平台能力不支持 | pass | proceed | proceed | none |
| case_022 | 重复检测 | pass | reuse_or_update | reuse_or_update | complete_duplicate |
| case_023 | 重复检测 | pass | reuse_or_update | reuse_or_update | complete_duplicate |
| case_024 | 重复检测 | pass | reuse_or_update | reuse_or_update | semantic_duplicate |
| case_025 | 重复检测 | pass | silent_merge | silent_merge | process_duplicate |
| case_026 | 重复检测 | pass | silent_merge | silent_merge | process_duplicate |
| case_027 | 重复检测 | pass | proceed | proceed | same_platform_rate_limit |
| case_028 | 重复检测 | pass | reuse_or_update | reuse_or_update | complete_duplicate |
| case_029 | 重复检测 | pass | reuse_or_update | reuse_or_update | complete_duplicate |
| case_030 | 重复检测 | pass | reuse_or_update | reuse_or_update | complete_duplicate |
| case_031 | 策略部分重复 | pass | ask_confirmation | ask_confirmation | strategy_partial_duplicate |
| case_032 | 策略部分重复 | pass | ask_confirmation | ask_confirmation | strategy_partial_duplicate |
| case_033 | 策略部分重复 | pass | ask_confirmation | ask_confirmation | strategy_partial_duplicate |
| case_034 | 策略部分重复 | pass | ask_confirmation | ask_confirmation | strategy_partial_duplicate |
| case_035 | 策略部分重复 | pass | ask_confirmation | ask_confirmation | strategy_partial_duplicate |
| case_036 | 策略部分重复 | pass | ask_confirmation | ask_confirmation | strategy_partial_duplicate |
| case_037 | 高风险重复 | pass | ask_confirmation | ask_confirmation | high_risk_duplicate |
| case_038 | 高风险重复 | pass | ask_confirmation | ask_confirmation | high_risk_duplicate |
| case_039 | 高风险重复 | pass | ask_confirmation | ask_confirmation | high_risk_duplicate |
| case_040 | 高风险重复 | pass | ask_confirmation | ask_confirmation | high_risk_duplicate |
| case_041 | 高风险重复 | pass | reuse_or_update | reuse_or_update | complete_duplicate |
| case_042 | 高风险重复 | pass | proceed | proceed | same_platform_rate_limit |
| case_043 | 高频堆积 | pass | warn_then_proceed | warn_then_proceed | high_frequency_accumulation |
| case_044 | 高频堆积 | pass | warn_then_proceed | warn_then_proceed | high_frequency_accumulation |
| case_045 | 高频堆积 | pass | proceed | proceed | same_platform_rate_limit |
| case_046 | 高频堆积 | pass | proceed | proceed | same_platform_rate_limit |
| case_047 | 通知边界 | pass | warn_then_proceed | warn_then_proceed | wechat_not_bound |
| case_048 | 通知边界 | pass | proceed | proceed | none |
| case_049 | 正常可创建 | pass | proceed | proceed | none |
| case_050 | 正常可创建 | pass | proceed | proceed | none |
