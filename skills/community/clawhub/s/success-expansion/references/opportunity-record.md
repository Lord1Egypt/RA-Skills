# 增购案记录（opportunity-record）

> opportunity record 全字段模板 + 收益测算 + 金额阈值与招标判定 + POC 路径 + 三层 stakeholder。
> 沿用 OneWave opportunity record template（MIT），加中国三层决策链 + 招标阈值 + POC。

## opportunity record 全字段模板

```
OPPORTUNITY ID: [账户]-[类型]-[N]
ACCOUNT: [客户名]
TYPE: [升级套餐/加坐席/加模块/跨部门拓展/竞品替换/服务支持]
DESCRIPTION: 一句话——卖什么+为什么现在需要

EVIDENCE（≥3 条，标可信度：customer-confirmed/customer-validated/data-derived/estimated，assumed 禁入）:
- 数据点 1
- 数据点 2
- 数据点 3

CURRENT STATE: 现在有什么
PROPOSED STATE: 增购后有什么
ESTIMATED REVENUE IMPACT: ¥[年化增量]（保守-进取区间）

TIMING:
- 最佳时机: 何时+为什么
- 紧迫度: 高/中/低
- 续约 alignment: 是否对齐续约（是/否，距今多久）
- 预算周期: 预算申报期/Q4 窗口/预算调整审批（中国）

STAKEHOLDER 三层（中国决策链）:
- 使用层（业务骨干/champion）: 姓名+title — 谁 pitch
- 业务层（部门负责人/处长）: 姓名+title — 谁推动会签
- 决策层（分管副总/一把手/CFO）: 姓名+title — 谁 decide
- 谁受益: 哪些用户/团队

RISKS:
- 什么会阻碍成交
- 预期异议

DEPENDENCIES:
- 是否需产品变更/enablement/POC/招标前置
```

## 收益测算公式

```
增购收益 = (加坐席数 × 坐席单价×12) + 模块升级年费 + tier 升级年化差价
```

- 标保守估计（最小增量）与进取估计（含 tier 升级/跨部门满铺）区间。
- 绝对金额与相对增幅都要看：5% 增幅在大账户（¥500K→¥525K）可能比 50% 增幅在小账户（¥5K→¥7.5K）更优先。
- 测算标可信度（data-derived / estimated），不冒充 confirmed。

## 金额阈值与招标判定（中国差异化）

| 增购金额 | 流程 | 衔接 |
|---|---|---|
| < 阈值 | 普通商务增补协议 | 合同流程（增补/简易合同） |
| ≥ 招标阈值（政企/国企常见 30-100 万，按客户内控） | **需招标** | 招标流程 + 招标双平台（中国政府采购网/地方公共资源交易中心） |

- 阈值判定在建案时做，标记 `NEEDS_TENDER=true`。
- 招标流程 timing 调整为招标周期（公告-投标-评标-中标，常 30-90 天），不能按普通商务「下周签」推。
- 政企/国企增购常需预算立项 + 采购委员会会签，timing 信号加预算申报期。

## POC→增购路径（中国企业级常见）

新模块/新坐席/跨部门拓展，中国企业级客户不敢直接拍大单，常先 POC：
1. **POC 启动**：定 2-4 周试用窗口 + 成功标准（可度量，如某指标达标）+ 转单触发点。
2. **POC 执行**：试用期间收价值证据（沿用首价值证明证据法）。
3. **POC 收尾**：成功标准达成→触发转单，生成增购案；未达成→降级为 nurture 或回炉。
4. **转单**：POC 证据进 opportunity record 的 EVIDENCE，可信度 customer-validated+。

POC 避免无限延期：必须设成功标准与截止日，否则沦为免费试用。

## 三层 stakeholder 映射（中国决策链）

| 层级 | 角色 | 增购对话重点 | 话术层 |
|---|---|---|---|
| 使用层 | 业务骨干/champion | 省时/提效/解痛点 | outcome |
| 业务层 | 部门负责人/处长 | ROI/人天/工时/合规/部门政绩 | outcome→ROI |
| 决策层 | 分管副总/一把手/CFO | 人民币回报/降本增效/合规避险/政绩/对标 | impact |

超阈值进采购委员会/招标时，决策层 + 采购 + 财务会签，对话提前准备采购流程话术。
