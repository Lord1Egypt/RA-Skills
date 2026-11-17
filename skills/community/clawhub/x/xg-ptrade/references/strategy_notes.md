使用说明
1. 快速上手步骤

登录 Ptrade 终端，点击 “策略” → “新建策略”
复制 scripts/dual_ma_strategy.py 的完整代码粘贴到编辑器
点击 “保存”（快捷键：Ctrl+S）
点击 “新建回测”，设置回测参数
点击 “回测” 运行

2. 修改策略参数
表格修改项位置修改方法股票代码initialize() 中 g.security修改为其他股票代码均线周期initialize() 中 g.ma_short 和 g.ma_long修改数值佣金费率initialize() 中 set_commission()取消注释并修改滑点initialize() 中 set_slippage()取消注释并修改
3. 使用策略模板

复制 assets/strategy_template.py 到编辑器
修改 STRATEGY_CONFIG 字典中的参数
在 generate_signal() 函数中添加自定义交易逻辑
保存并运行

4. 查看日志

在回测/交易界面的 “日志” 区域查看运行记录
日志级别：DEBUG < INFO < WARNING < ERROR < CRITICAL
使用 log.info() 输出关键信息