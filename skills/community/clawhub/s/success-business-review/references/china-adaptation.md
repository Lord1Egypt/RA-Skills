# China Adaptation（china-adaptation）

> 配套 SKILL.md 全主线。沿用首价值证明场景的中国决策层三层+无 telemetry 替代+验收节点挂钩，改造为周期性复盘版。

## 一、中国决策层三层 + champion

海外 C-Suite/VP/Director/Manager 四层 → 中国改造为三层+champion：

| 层 | 角色 | 复盘参与 | 叙事版本 | 关心 |
|---|---|---|---|---|
| 一把手 | 董事长/总经理 | 战略级 EBR | Strategic 层 | 政绩/对标/战略价值 |
| 分管副总 | 分管业务副总 | 季度 QBR | Operational 层 | 效率/降本/合规避险 |
| 部门负责人+执行层 | 处室负责人/使用层 | 常规 QBR | Tactical 层 | 功能采用/流程改进 |
| champion | 信息中心副主任/业务骨干 | 全程参与 | Tactical+桥梁 | 推动落地+向决策层转述 |

**champion 是桥梁**：champion 接受详细叙事（含推算过程），替你向决策层转述。给 champion 的版本要比决策层版本更细，让他能内推。

## 二、无 Telemetry 替代证据（私有化/国产化）

海外假定有 product analytics/telemetry → 中国私有化/国产化无完整 telemetry：

| 证据类型 | 海外 | 中国替代 |
|---|---|---|
| 使用数据 | 后台 telemetry 自动 | 业务侧手动统计（审批时长/工单数/人天/合规事件数）+ 私有化后台部分活跃数据 |
| 业务结果 | BI 自动拉 | 客户侧业务负责人提供报表+我方推算+客户确认 |
| 客户原话 | email/NPS | 微信/企微群聊截图+朋友圈+客户领导微信群认可截图 |

**铁律**：
- 客户确认的基线/数据比我方估算可信 10×。
- 优先拉客户侧业务负责人提供数据（非我方单方推算）。
- 估算必标 estimated，不准当 confirmed 报。
- assumed 级（「我们觉得有价值」）禁用。

## 三、微信/企微汇报习惯

海外 60-90min formal deck → 中国决策层偏好一页纸+微信版+口头：

| 形态 | 用途 | 规格 |
|---|---|---|
| 一页纸预发材料 | 会前 T-7 预发 | headline metric+3 证据+1 客户原话+1 下步 |
| 微信版摘要 | 会前/会后发决策层群 | <200 字，1 数字+1 客户认可+1 下步 |
| 客户面精简 deck | 会中用 | 按 60-min agenda，精简不堆 slide |
| 口头/饭局 3 句话 | 线下/饭局/领导碰面 | 痛点→结果→下步 |

**铁律**：
- 先讲已交付成果，再提下步/投资诉求（先要钱再讲成果=决策层反感）。
- 一把手无耐心看长 deck，一页纸+微信版为主。
- 分管副总可接受 60-min deck 但要精简。
- 政企不接受 async memo/digital QBR，必须正式会议+材料预发。

## 四、合规适配段（替代海外 roadmap alignment）

海外 roadmap alignment 公开 product roadmap → 中国政企对厂商 roadmap 透明度低，更关心合规/等保/信创适配：

| 段 | 海外 | 中国改造 |
|---|---|---|
| Roadmap Alignment | 公开 product roadmap 对齐客户用例 | **合规适配进展**：等保/信创/国产化适配进度+本地化能力增强+数据安全合规 |

**表述**：
- 「本季完成等保 2.0 三级适配 + 信创国产化 CPU/OS 兼容」
- 「数据安全：私有化部署数据不出客户网络 + 审计日志全留痕」
- 「本地化能力增强：[具体功能] 本地化适配完成」

少讲海外 product roadmap 大方向，多讲合规/本地化具体进展。

## 五、验收/付款节点挂钩

政企复盘要与验收/付款节点对齐（复用 首价值证明）：

| 节点 | 复盘动作 |
|---|---|
| 阶段验收 | 验收前 QBR 证明阶段价值，推动验收签字 |
| 付款节点 | 付款前 QBR 证明价值达标，推动付款 |
| 续约前 90 天 | Pre-renewal review（见 review-cadence-and-timeline.md 第四节） |

**铁律**：验收/付款节点到了价值没证明 → 尾款卡、验收拖延。复盘 cadence 要提前于验收/付款节点安排。

## 六、Health Score 内部用 + 客户面用目标达成度

海外 health score 透明给客户 → 中国客户不接受被「打分」：

- **内部**：用健康度五维 Green/Yellow/Red（决策层出席率/会前准备/会上参与度/跟进响应率/action 完成率），见 `references/progress-scoring.md` 第五节。
- **客户面**：用「目标达成度」红黄绿（绿=on_track / 黄=at_risk / 红=not_measurable_yet 第 3 次），不说「health score」不打分。

## 七、政企 60% Future / 40% Past

海外 70% future / 30% past → 中国政企改造为 60/40（政企「过去成绩」要充分，政绩感）。详见 `references/value-narrative.md` 第四节。

## 八、反例（归因式）

| 念头/做法 | 后果 |
|---|---|
| 假定有完整 telemetry / 按 60-90min formal deck 套政企 | 私有化无数据无替代证据、政企决策层无耐心看长 deck，复盘卡死 |
| 用 email/NPS 收证据 | 政企客户不发 email、不填 NPS，证据收集落空 |
| health score 直接打分给客户看 | 中国客户不接受被「打分」，客户面用「目标达成度」红黄绿才认 |
| 公开 product roadmap 当 roadmap alignment | 政企对厂商 roadmap 透明度低，不关心；应讲合规适配进展 |
| 复盘 cadence 不与验收/付款节点挂钩 | 验收/付款节点到了价值没证明，尾款卡、验收拖延 |
| 按 ARR $ 分级 cadence | 政企大单看合同额×战略价值非 ARR，分级错位 |
| 用海外 async memo / digital QBR | 政企不接受 async 复盘，必须正式会议+材料预发 |
