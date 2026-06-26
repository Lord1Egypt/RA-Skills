# 缺陷等级定义规范

> 文档编号：L3-DEF-001  
> 版本：v1.0  
> 生效日期：2026-04-18  
> 适用范围：全公司测试团队及开发团队

## 1. 目的

统一缺陷严重程度的判定标准，明确各等级缺陷的处理时限与升级机制，确保缺陷管理流程高效、可追溯。

## 2. 缺陷等级定义

### 2.1 P0 — 致命（Critical）

**定义：** 系统完全不可用、核心业务流程中断、造成或可能造成资金损失、数据丢失或严重安全漏洞。

**判断标准：**
- 系统崩溃、无法启动或主流程完全阻断
- 交易数据错误导致资金计算偏差
- 客户资金账户余额显示错误或资金划转异常
- 数据库数据丢失或损坏且无法恢复
- 安全漏洞可被外部利用（如SQL注入导致数据泄露）
- 清算/结算流程异常导致交收失败

**处理时限：**
- 发现后 **15分钟内** 通知项目负责人及技术负责人
- **1小时内** 组建应急修复小组并启动修复
- **4小时内** 提交修复方案或临时规避方案
- **8小时内** 完成修复并提交验证
- 超过4小时未修复，自动升级至部门总监

**升级机制（工程实现）：**
```
// 缺陷管理系统自动升级逻辑
if (defect.level == P0 && defect.status == CONFIRMED) {
    // 创建后15分钟未指派 → 短信+企业微信通知项目经理
    scheduler.addTask(defect.id, 15min, () -> {
        if (defect.assignee == null) {
            notify(PROJECT_MANAGER, SMS | WECHAT, defect);
            notify(TECH_LEAD, SMS | WECHAT, defect);
        }
    });
    // 创建后4小时未修复 → 升级至部门总监
    scheduler.addTask(defect.id, 4hour, () -> {
        if (defect.status != FIXED) {
            escalate(DEPT_DIRECTOR, defect);
            notify(DEPT_DIRECTOR, PHONE_CALL, defect);
        }
    });
    // 创建后8小时未关闭 → 升级至CTO
    scheduler.addTask(defect.id, 8hour, () -> {
        if (defect.status != CLOSED) {
            escalate(CTO, defect);
        }
    });
}
```

**券商业务示例：**
- 客户委托买入100手某股票，系统实际下单1000手，导致资金超额占用
- 清算系统计算错误，T日交收金额与实际成交不符
- 银证转账功能完全不可用，客户无法出入金
- 行情系统全面宕机，所有客户无法查看实时行情

### 2.2 P1 — 严重（Major）

**定义：** 核心功能存在严重缺陷但系统仍可运行，影响主要业务流程的正确性或完整性，存在数据一致性风险。

**判断标准：**
- 核心业务功能异常但有替代路径可用
- 数据展示错误但不涉及资金计算
- 性能严重下降（响应时间超过SLA阈值3倍以上）
- 权限控制失效（越权访问但未造成实际损失）
- 批量业务处理失败率超过5%

**处理时限：**
- 发现后 **30分钟内** 通知开发负责人
- **4小时内** 确认修复方案
- **1个工作日内** 完成修复并提交验证
- 超过1个工作日未修复，升级至项目负责人

**升级机制（工程实现）：**
```
if (defect.level == P1 && defect.status == CONFIRMED) {
    scheduler.addTask(defect.id, 30min, () -> {
        if (defect.assignee == null) {
            notify(DEV_LEAD, WECHAT, defect);
        }
    });
    scheduler.addTask(defect.id, 1workday, () -> {
        if (defect.status != FIXED) {
            escalate(PROJECT_MANAGER, defect);
            notify(PROJECT_MANAGER, WECHAT | EMAIL, defect);
        }
    });
}
```

**券商业务示例：**
- 融资融券担保比例计算偏差，但未触发强制平仓
- 客户持仓查询偶发性显示为空，刷新后恢复
- 新股申购功能在特定条件下失败，但手动补单可完成
- 交易密码修改后旧密码仍可登录（安全隐患）

### 2.3 P2 — 一般（Minor）

**定义：** 非核心功能存在缺陷，不影响主要业务流程，但影响用户体验或操作效率。

**判断标准：**
- 非核心功能异常或显示错误
- 界面布局错乱但不影响操作
- 提示信息不准确或缺失
- 操作流程不便但可完成业务
- 日志记录不完整或格式错误
- 报表导出格式异常但数据正确

**处理时限：**
- **1个工作日内** 确认并指派
- **3个工作日内** 完成修复
- **5个工作日内** 完成验证并关闭
- 超过5个工作日未修复，纳入下一迭代优先处理

**券商业务示例：**
- 交割单PDF导出时表格列宽不一致
- 自选股排序功能在特定排序条件下失效
- 资讯模块图片加载缓慢（超过3秒但不超过10秒）
- 客户风险评估问卷提交后缺少成功提示

### 2.4 P3 — 建议（Suggestion）

**定义：** 不影响功能和使用的轻微问题，包括界面美化建议、文案优化、易用性改进等。

**判断标准：**
- 界面文案错别字或表述不当
- 颜色、字体、间距等视觉细节问题
- 操作便捷性优化建议
- 兼容性问题（非主流浏览器/设备）
- 代码规范类问题（不影响运行）

**处理时限：**
- **3个工作日内** 确认并评估
- 纳入产品待办列表，按迭代计划安排
- 无强制修复时限，但每季度清理一次积压P3缺陷

**券商业务示例：**
- 登录页面"忘记密码"链接颜色与整体风格不统一
- K线图缩放操作建议增加双指手势支持
- 交易确认弹窗建议增加键盘快捷键支持
- 帮助文档中部分术语解释不够通俗

## 3. 缺陷等级判定矩阵

| 维度 | P0 致命 | P1 严重 | P2 一般 | P3 建议 |
|------|---------|---------|---------|---------|
| 影响范围 | 全部用户/核心业务 | 大部分用户/主要功能 | 部分用户/次要功能 | 极少用户/边缘场景 |
| 资金影响 | 有资金损失风险 | 有资金展示错误 | 无资金影响 | 无资金影响 |
| 替代方案 | 无 | 有但成本高 | 有且可接受 | 不需要 |
| 发生频率 | 必现 | 高频（>50%） | 偶发（10%~50%） | 罕见（<10%） |
| 安全影响 | 高危漏洞 | 中危漏洞 | 低危漏洞 | 无安全影响 |

## 4. 缺陷状态流转

### 4.1 状态定义

| 状态 | 说明 | 责任人 |
|------|------|--------|
| 新建（New） | 测试人员提交缺陷 | 测试人员 |
| 确认（Confirmed） | 开发确认为有效缺陷 | 开发负责人 |
| 修复中（In Progress） | 开发正在修复 | 开发人员 |
| 已修复（Fixed） | 开发完成修复并提交代码 | 开发人员 |
| 验证中（Verifying） | 测试人员回归验证 | 测试人员 |
| 已关闭（Closed） | 验证通过，缺陷关闭 | 测试人员 |
| 重新打开（Reopened） | 验证未通过，重新打开 | 测试人员 |
| 挂起（Suspended） | 因外部依赖暂停处理 | 项目经理 |
| 已拒绝（Rejected） | 非缺陷或不予修复 | 开发负责人 |

### 4.2 状态流转图

```
新建(New)
  │
  ├──→ 确认(Confirmed) ──→ 修复中(In Progress) ──→ 已修复(Fixed)
  │                                                      │
  │                                                      ▼
  │                                                验证中(Verifying)
  │                                                   │       │
  │                                                   ▼       ▼
  │                                              已关闭    重新打开
  │                                             (Closed)  (Reopened)
  │                                                          │
  │                                                          ▼
  │                                                   修复中(In Progress)
  │
  ├──→ 已拒绝(Rejected)
  │
  └──→ 挂起(Suspended) ──→ 确认(Confirmed)
```

### 4.3 状态流转规则

1. **新建 → 确认**：开发负责人在收到缺陷后，P0缺陷15分钟内、P1缺陷30分钟内、P2/P3缺陷1个工作日内完成确认。
2. **新建 → 已拒绝**：需填写拒绝理由，测试人员有权申诉，申诉由项目经理仲裁。
3. **已修复 → 验证中**：开发提交修复后，须在缺陷系统中关联代码提交记录（commit hash）。
4. **验证中 → 重新打开**：须填写验证失败的具体描述和复现步骤，重新打开次数纳入缺陷质量统计。
5. **挂起 → 确认**：挂起缺陷每周由项目经理审查，外部依赖解除后立即恢复。
6. **重新打开次数限制**：同一缺陷重新打开超过3次，自动升级一个等级处理。

### 4.4 工程实现要点

```java
// 缺陷状态机实现（Spring StateMachine 示例）
@Configuration
@EnableStateMachine
public class DefectStateMachineConfig extends StateMachineConfigurerAdapter<DefectState, DefectEvent> {

    @Override
    public void configure(StateMachineTransitionConfigurer<DefectState, DefectEvent> transitions) throws Exception {
        transitions
            .withExternal().source(NEW).target(CONFIRMED).event(CONFIRM)
                .guard(assigneeNotNullGuard())
            .and()
            .withExternal().source(CONFIRMED).target(IN_PROGRESS).event(START_FIX)
            .and()
            .withExternal().source(IN_PROGRESS).target(FIXED).event(SUBMIT_FIX)
                .action(requireCommitHashAction())
            .and()
            .withExternal().source(FIXED).target(VERIFYING).event(START_VERIFY)
            .and()
            .withExternal().source(VERIFYING).target(CLOSED).event(VERIFY_PASS)
            .and()
            .withExternal().source(VERIFYING).target(REOPENED).event(VERIFY_FAIL)
                .action(incrementReopenCountAction())
            .and()
            .withExternal().source(REOPENED).target(IN_PROGRESS).event(START_FIX)
                .guard(reopenCountLessThan3Guard())
            .and()
            .withExternal().source(NEW).target(REJECTED).event(REJECT)
                .action(requireRejectReasonAction())
            .and()
            .withExternal().source(NEW).target(SUSPENDED).event(SUSPEND)
            .and()
            .withExternal().source(SUSPENDED).target(CONFIRMED).event(RESUME);
    }
}
```

## 5. 缺陷等级变更规则

1. **升级条件**：
   - 缺陷影响范围扩大（如从部分用户扩展到全部用户）
   - 同一缺陷重新打开超过3次
   - 处理超时未完成修复
2. **降级条件**：
   - 经复现确认影响范围小于初始判断
   - 找到有效的临时规避方案
3. **变更审批**：P0/P1等级变更需项目经理审批，P2/P3等级变更由测试负责人审批。

## 6. 附则

- 本规范自发布之日起执行，由测试管理部负责解释和修订。
- 各项目组可在本规范基础上制定补充细则，但不得降低处理时限要求。
- 缺陷等级争议由项目经理组织评审会议裁定，裁定结果为最终结论。
