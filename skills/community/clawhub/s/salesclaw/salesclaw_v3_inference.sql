
-- 推理会话：每次告警触发一次结构化诊断
CREATE TABLE fct_diagnosis_session (
    session_id       VARCHAR(50) PRIMARY KEY,
    -- 触发源
    trigger_type     VARCHAR(30) NOT NULL,  -- alert/ scheduled/ manual
    trigger_rule_id  VARCHAR(50),
    trigger_alert_id VARCHAR(50),
    -- 诊断对象
    entity_type      VARCHAR(30) NOT NULL,  -- product/ doctor/ hospital/ rep/ territory
    entity_id        VARCHAR(50) NOT NULL,
    entity_name      VARCHAR(200),
    -- 诊断上下文
    metric_name      VARCHAR(100),
    metric_value     DECIMAL(16,4),
    baseline_value   DECIMAL(16,4),
    deviation_pct    DECIMAL(8,4),
    alert_level      VARCHAR(10),           -- red/yellow/green
    period_type      VARCHAR(20),
    period_value     VARCHAR(20),
    province         VARCHAR(50),
    -- 诊断状态
    current_phase    VARCHAR(20) DEFAULT 'structure',  -- structure/ behavior/ decision/ concluded
    status           VARCHAR(20) DEFAULT 'active',    -- active/ paused/ concluded/ cancelled
    priority         INT DEFAULT 5,
    -- 推理结论（汇总）
    conclusion_id    VARCHAR(50),
    confidence       DECIMAL(5,2),
    -- 时间戳
    started_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    concluded_at     DATETIME,
    created_by       VARCHAR(50)            -- agent/human
);

-- 推理步骤：三层归因的每一步记录
CREATE TABLE fct_reasoning_step (
    step_id          VARCHAR(50) PRIMARY KEY,
    session_id       VARCHAR(50) NOT NULL,
    step_order       INT NOT NULL,           -- 1=结构 2=行为 3=决策
    phase            VARCHAR(20) NOT NULL,  -- structure/ behavior/ decision
    step_name        VARCHAR(100) NOT NULL, -- 如：定位失血省区
    step_question    TEXT NOT NULL,         -- 这个步骤要回答什么问题
    sql_query        TEXT,                   -- 执行的SQL
    sql_result       TEXT,                   -- SQL结果摘要（JSON）
    finding          TEXT NOT NULL,          -- 发现（回答step_question）
    confidence       DECIMAL(5,2),          -- 本步置信度
    data_evidence    TEXT,                   -- 支撑数据（JSON）
    alternative_hypothesis TEXT,             -- 备选假设（如本步不确定）
    conclusion_flag  BOOLEAN DEFAULT FALSE, -- 是否形成最终结论
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES fct_diagnosis_session(session_id)
);

-- 诊断规则：从扁平预警升级为结构化诊断流程
CREATE TABLE dim_diagnosis_rules (
    rule_id          VARCHAR(50) PRIMARY KEY,
    rule_name        VARCHAR(200) NOT NULL,
    -- 触发条件（原有预警规则内容）
    entity_type      VARCHAR(30) NOT NULL,
    metric           VARCHAR(100) NOT NULL,
    condition_type   VARCHAR(30) NOT NULL,  -- gt/ lt/ drop_pct/ rise_pct
    threshold_value  DECIMAL(16,4),
    severity         VARCHAR(20) NOT NULL,   -- critical/high/medium/low
    -- 诊断流程（新增）
    diagnosis_type   VARCHAR(50) NOT NULL,  -- sales_decline/ expense_anomaly/ compliance_risk/ market_share_loss
    phase1_template  TEXT NOT NULL,         -- 结构归因的问题模板（JSON）
    phase2_template  TEXT NOT NULL,         -- 行为归因的问题模板（JSON）
    phase3_template  TEXT NOT NULL,         -- 决策归因的问题模板（JSON）
    required_data_phases TEXT NOT NULL,     -- 每个phase需要哪些数据表（JSON array）
    output_format    TEXT NOT NULL,         -- 结论输出格式模板
    -- 关联预警规则（可关联到dim_alert_rules的rule_id）
    linked_alert_rule_ids TEXT,              -- JSON array
    -- 调度
    enabled          BOOLEAN DEFAULT TRUE,
    auto_trigger     BOOLEAN DEFAULT TRUE,
    priority         INT DEFAULT 5,
    tags             TEXT,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

-- 预置诊断规则（覆盖主要业务场景）
INSERT INTO dim_diagnosis_rules (rule_id, rule_name, entity_type, metric, condition_type, threshold_value, severity, diagnosis_type, phase1_template, phase2_template, phase3_template, required_data_phases, output_format, linked_alert_rule_ids, priority) VALUES

-- 场景1：品种处方量下滑
('DR001', '品种处方量下滑三维诊断', 'product', 'prescription_volume', 'drop_pct', 0.15, 'high', 'sales_decline',
 -- 结构归因：定位失血结构单元
 '{"questions":["失血发生在哪个省区？","失血发生在哪个医院？","失血发生在哪个医生？","失血发生在哪个时间段？"],"dimensions":["province","hospital","doctor","time"],"tables":["fct_prescription_flow","dim_territories","dim_hospitals"]}',
 -- 行为归因：理解驱动因素
 '{"questions":["覆盖医生数是否下降？","代表拜访频次是否下降？","竞品是否有学术活动？","医院准入是否有变化？"],"behavior_types":["coverage","visit","competitor","access"],"tables":["fct_visit_detail","fct_campaign","dim_hospital_access","dim_competitive_intelligence"]}',
 -- 决策归因：确定责任归属
 '{"questions":["哪个代表应该负责？","区域经理是否尽到管理责任？","总部策略是否有问题？"],"attribution_levels":["rep","manager","director"],"tables":["dim_reps","dim_rep_performance","fct_budget_allocation"]}',
 '["fct_prescription_flow","dim_territories","dim_hospitals","dim_doctors","fct_visit_detail","fct_campaign","dim_reps","fct_budget_allocation"]',
 '{"conclusion_format":"品种{product_name}处方量下降{pct}%，根本原因：{root_cause}，责任归属：{owner}，置信度：{confidence}%","required_fields":["root_cause","owner","confidence","contributing_factors"]}',
 '["R001","R002"]', 5),

-- 场景2：省区费用超限
('DR002', '省区费用异常三维诊断', 'province', 'expense_ratio', 'gt', 1.3, 'high', 'expense_anomaly',
 '{"questions":["超支集中在哪个费用类型？","超支发生在哪个代表？","超支发生在哪个时间段？"],"dimensions":["expense_type","rep","time"],"tables":["fct_expense_c2","dim_reps"]}',
 '{"questions":["是否有异常大额单笔？","费用类型结构是否合理？","是否存在虚报风险？"],"behavior_types":["amount_anomaly","structure","compliance"],"tables":["fct_expense_c2","dim_compliance_rules","fct_compliance_violations"]}',
 '{"questions":["代表本人是否知情？","区域经理是否审批？","总部预算是否合理？"],"attribution_levels":["rep","manager","director"],"tables":["dim_reps","fct_budget_allocation","dim_cost_standards"]}',
 '["fct_expense_c2","dim_reps","dim_expense_rules","fct_compliance_violations","fct_budget_allocation"]',
 '{"conclusion_format":"省区{province}费用{expense_type}超支{amount}元（{pct}%），DeltaWeight={delta_weight}ppt，原因：{root_cause}，建议：{action}","required_fields":["expense_type","amount","delta_weight","root_cause","action"]}',
 '["R004","R006"]', 5),

-- 场景3：代表绩效下滑
('DR003', '代表绩效下滑三维诊断', 'rep', 'achievement_rate', 'lt', 0.75, 'high', 'performance_decline',
 '{"questions":["下滑集中在哪个品种？","下滑发生在哪个省区/医院？","下滑从哪个时间段开始？"],"dimensions":["product","province","hospital","time"],"tables":["fct_prescription_flow","dim_reps","dim_territories"]}',
 '{"questions":["拜访频次是否下降？","拜访质量是否下降？","医生关系是否疏远？","费用投入是否减少？"],"behavior_types":["visit_frequency","visit_quality","doctor_relationship","expense_investment"],"tables":["fct_visit_detail","fct_visit_summary","dim_representative_doctor","fct_expense_c2"]}',
 '{"questions":["代表本人是否主动改变？","区域经理是否及时介入？","是否需要资源支持？"],"attribution_levels":["rep","manager","director"],"tables":["dim_reps","dim_rep_performance"]}',
 '["fct_prescription_flow","fct_visit_detail","fct_visit_summary","dim_reps","dim_rep_performance","fct_expense_c2"]',
 '{"conclusion_format":"代表{rep_name}绩效下滑，达成率{achievement_rate}%，主因：{root_cause}，建议：{action}，预计修复时间：{timeline}","required_fields":["achievement_rate","root_cause","action","timeline"]}',
 '["R001","R006"]', 4),

-- 场景4：医院采购量下滑
('DR004', '医院采购量下滑三维诊断', 'hospital', 'purchase_volume', 'drop_pct', 0.2, 'high', 'purchase_decline',
 '{"questions":["下滑集中在哪个品种？","下滑发生在哪个科室？","下滑从哪个时间段开始？"],"dimensions":["product","department","time"],"tables":["fct_procurement_flow","dim_hospital_departments"]}',
 '{"questions":["是否有库存积压？","竞品是否有入院动作？","医生处方是否下降？"],"behavior_types":["inventory","competitor","prescription"],"tables":["fct_inventory","dim_competitive_intelligence","fct_prescription_flow"]}',
 '{"questions":["代表是否及时跟进？","区域经理是否重视？","总部支持是否到位？"],"attribution_levels":["rep","manager","director"],"tables":["dim_reps","dim_hospital_access"]}',
 '["fct_procurement_flow","fct_inventory","dim_competitive_intelligence","fct_prescription_flow","dim_hospitals","dim_reps"]',
 '{"conclusion_format":"医院{hospital_name}采购量下滑{pct}%，品种{product_name}，主因：{root_cause}，建议：{action}","required_fields":["hospital_name","product_name","pct","root_cause","action"]}',
 '["R005"]', 4),

-- 场景5：合规风险预警
('DR005', '合规风险三维诊断', 'rep', 'compliance_score', 'lt', 0.85, 'critical', 'compliance_risk',
 '{"questions":["风险集中在哪个费用类型？","风险发生在哪个医院？","风险持续了多长时间？"],"dimensions":["expense_type","hospital","time"],"tables":["fct_expense_c2","dim_compliance_rules"]}',
 '{"questions":["是否存在虚假报销？","是否存在超标送礼？","是否存在学术活动违规？"],"behavior_types":["expense_fraud","gift_overdue","activity_violation"],"tables":["fct_compliance_violations","dim_compliance_rules"]}',
 '{"questions":["代表是否故意为之？","区域经理是否知情？","是否系统漏洞？"],"attribution_levels":["rep","manager","system"],"tables":["dim_reps","fct_audit_log"]}',
 '["fct_expense_c2","fct_compliance_violations","fct_audit_log","dim_compliance_rules","dim_reps"]',
 '{"conclusion_format":"代表{rep_name}合规风险等级：{severity}，风险点：{risk_points}，建议：{action}，影响范围：{impact_scope}","required_fields":["severity","risk_points","action","impact_scope"]}',
 '["R004"]', 5);

-- 更新告警规则：增加关联诊断规则ID字段（扩展原有dim_alert_rules）
ALTER TABLE dim_alert_rules ADD COLUMN diagnosis_rule_id VARCHAR(50);
ALTER TABLE dim_alert_rules ADD COLUMN auto_escalate_to_diagnosis BOOLEAN DEFAULT FALSE;

-- 将现有告警规则关联到诊断规则
UPDATE dim_alert_rules SET diagnosis_rule_id = 'DR001' WHERE rule_id IN ('R001', 'R002');
UPDATE dim_alert_rules SET diagnosis_rule_id = 'DR002' WHERE rule_id IN ('R004', 'R006');
UPDATE dim_alert_rules SET diagnosis_rule_id = 'DR005' WHERE rule_id = 'R003';

-- 推理会话索引
CREATE INDEX idx_diagnosis_session_entity ON fct_diagnosis_session(entity_type, entity_id);
CREATE INDEX idx_diagnosis_session_status ON fct_diagnosis_session(status, alert_level);
CREATE INDEX idx_reasoning_step_session ON fct_reasoning_step(session_id, step_order);
CREATE INDEX idx_diagnosis_rules_entity ON dim_diagnosis_rules(entity_type, enabled);