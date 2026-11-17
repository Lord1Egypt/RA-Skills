# system/ 系统层 - SPL-Virtual-World-Base 的实现载体
# ============================================================
# 职责：承载虚拟世界的"实际运行"能力，取代 constitution.py /
# constitution_rules.py 中 blockchain / multi_agent 的占位桩。
#
# 分层边界：
#   constitution_rules.py  宪法规则（只读、不可变）
#   audit_engine.py        第二视角审计引擎（元层裁判）
#   system/                系统实现（本包）
#   virtual_world.py       演示运行时客户端
#
# 约束：本包暴露的状态必须可被 audit_engine.SecondPerspectiveAuditor
# 的 25 项审计检查；创世（GenesisCondition.initiate_genesis）所需的
# 组件全部由本包真实创建并注入。
#
# 模块规划（地平线一·地基）：
#   ledger.py              状态账本：SoulLedger / HistoryLedger / EconomicReserve
#   consensus.py           共识：节点注册、提案、公投计票
#   agent_engine.py        智能体：决策 + 记忆封存 + Gas 计量
#   runtime.py             无头运行时：tick 循环 + 快照 + 审计上报
#   api.py                 服务接口：REST/WebSocket + 鉴权
#
# 地平线二·跨数据中心底座：
#   hlc.py                 混合逻辑时钟预言机（NTP 底座 + Lamport 计数）
#   spatial_sharding.py    空间分片路由 + 跨域迁移手协
#   aoi_sync.py            AOI 关注域 + WAN 增量复制器
#   partition_guard.py     网络分区检测 + 局部自治 + Merkle 差分合并
#   hierarchical_consensus.py 分层双环共识（Intra-DC 快环 + Inter-DC 慢环）
#   cluster.py              集群接线层：拓扑配置 + 后台心跳线程 + 入站 op 白名单
#
# 两套分片路由并存，职责不可混用（接线时务必分清）：
#   ledger.ShardRouter           存储分片：按 soul_hash 路由账本（账户/凭证/会话）
#   spatial_sharding.ShardRouter 仿真分片：按空间坐标路由实体（AOI / 跨域迁移）
#   运行时（runtime.World）只用后者；前者由存储后端自行消费。
