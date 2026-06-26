-- SalesClaw Complete MySQL Schema
-- 138 tables

CREATE TABLE action_results (
    result_id             VARCHAR(50) PRIMARY KEY,
    action_id             VARCHAR(50),
    outcome               TEXT,
    feedback              TEXT,
    next_action_id        VARCHAR(50),
    closed_at             DATETIME,
    FOREIGN KEY (action_id) REFERENCES actions(action_id)
);

CREATE TABLE actions (
    action_id             VARCHAR(50) PRIMARY KEY,
    action_type           VARCHAR(50) NOT NULL,
    title                 VARCHAR(500) NOT NULL,
    description           TEXT,
    entity_type            VARCHAR(30),
    entity_id             VARCHAR(50),
    entity_name           VARCHAR(200),
    priority              VARCHAR(20), 
    status                VARCHAR(20) DEFAULT 'pending', -- pending/in_progress/completed/cancelled
    assigned_to           VARCHAR(100),
    due_date              DATE,
    completed_at          DATETIME,
    conclusion_id         VARCHAR(50),
    reasoning             TEXT,
    expected_outcome      TEXT,
    actual_outcome        TEXT,
    result_evaluation     TEXT,
    parent_action_id      VARCHAR(50),
    depends_on            VARCHAR(500),    -- JSON array
    tags                  VARCHAR(500),
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by            VARCHAR(100),
    FOREIGN KEY (conclusion_id) REFERENCES conclusions(conclusion_id)
);

CREATE TABLE alert_rules (
    rule_id               VARCHAR(50) PRIMARY KEY,
    rule_name             VARCHAR(200) NOT NULL,
    rule_type             VARCHAR(30),     -- alert/approval/traffic_light
    entity_type           VARCHAR(30),     -- doctor/hospital/product/rep/territory
    condition_pattern     TEXT,            -- JSON DSL
    condition_description TEXT,
    threshold             FLOAT,
    severity              VARCHAR(20),     -- critical/high/medium/low/info
    consequence_type      VARCHAR(30),     -- alert/block/approve
    consequence_action   VARCHAR(200),
    auto_trigger         TINYINT(1) DEFAULT 1,
    enabled               TINYINT(1) DEFAULT 1,
    priority              INT DEFAULT 0,
    ttl                   INT,             -- days
    tags                  VARCHAR(500),     -- JSON array
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE annual_plans (
    plan_id               VARCHAR(50) PRIMARY KEY,
    plan_type             VARCHAR(30),     -- annual/quarterly/monthly
    plan_year             INT,
    plan_quarter          VARCHAR(10),
    plan_month            VARCHAR(7),
    entity_type           VARCHAR(30),
    entity_id             VARCHAR(50),
    entity_name           VARCHAR(200),
    target_revenue        DECIMAL(16,2),
    target_volume         BIGINT,
    target_market_share   FLOAT,
    actual_revenue        DECIMAL(16,2),
    actual_volume         BIGINT,
    achievement_rate      FLOAT,
    budget_allocated      DECIMAL(16,2),
    status                VARCHAR(20) DEFAULT 'active',
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by            VARCHAR(100)
);

CREATE TABLE audit_log (
    log_id          VARCHAR(50) PRIMARY KEY,
    action          VARCHAR(100) NOT NULL,
    entity_type     VARCHAR(30),
    entity_id       VARCHAR(50),
    entity_name     VARCHAR(200),
    user_id         VARCHAR(50),
    user_name       VARCHAR(100),
    `timestamp`       DATETIME DEFAULT CURRENT_TIMESTAMP,
    details         TEXT,
    previous_value  TEXT,
    new_value       TEXT,
    ip_address      VARCHAR(50)
);

CREATE TABLE budget_categories (
    budget_id          VARCHAR(50) PRIMARY KEY,
    budget_type        VARCHAR(50),    -- 销售费用/市场费用/管理费用
    budget_category    VARCHAR(100),   -- 人力/差旅/招待/学术活动/市场推广
    allocation_amount  DECIMAL(16,2),
    used_amount        DECIMAL(16,2) DEFAULT 0,
    remaining_amount   DECIMAL(16,2),
    execution_rate     FLOAT,
    holder_type        VARCHAR(30),    -- rep/territory/region/headquarter
    holder_id          VARCHAR(50),
    holder_name        VARCHAR(100),
    period_type        VARCHAR(20),    -- annual/quarterly/monthly
    period_value       VARCHAR(20),    -- 2026/2026-Q1/2026-01
    budget_status      VARCHAR(30),    -- approved/pending/exceeded
    approval_status    VARCHAR(30),
    created_at         DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at         DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_messages (
    message_id      VARCHAR(50) PRIMARY KEY,
    thread_id      VARCHAR(50),
    role           VARCHAR(20),   -- user/assistant/system
    content        TEXT NOT NULL,
    `timestamp`      DATETIME DEFAULT CURRENT_TIMESTAMP,
    entity_id      VARCHAR(50),
    entity_type    VARCHAR(30),
    time_range     VARCHAR(50),
    intent         VARCHAR(100),
    sql_used       TEXT,
    FOREIGN KEY (thread_id) REFERENCES chat_threads(thread_id)
);

CREATE TABLE chat_threads (
    thread_id           VARCHAR(50) PRIMARY KEY,
    user_id             VARCHAR(50),
    current_entity_id   VARCHAR(50),
    current_entity_type VARCHAR(30),
    current_entity_name VARCHAR(200),
    current_time_range  VARCHAR(50),
    context_summary     TEXT,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE competitors (
    competitor_id   VARCHAR(50) PRIMARY KEY,
    product_id      VARCHAR(50),  -- 我方品种
    competitor_name VARCHAR(200),
    competitor_product VARCHAR(200),
    competitive_advantage TEXT,
    competitive_disadvantage TEXT,
    market_share    FLOAT,
    price           DECIMAL(12,2),
    status          VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE compliance_alerts (
    alert_id            VARCHAR(50) PRIMARY KEY,
    severity            VARCHAR(20),     -- critical/high/medium/low
    risk_type           VARCHAR(50),
    alert_description   TEXT,
    alert_status        VARCHAR(20) DEFAULT 'pending', -- pending/resolved/dismissed
    entity_id           VARCHAR(50),
    entity_type         VARCHAR(30),
    entity_name         VARCHAR(200),
    source_rule_id      VARCHAR(50),
    created_by          VARCHAR(30) DEFAULT 'agent',
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at         DATETIME,
    resolution          TEXT
);

CREATE TABLE conclusions (
    conclusion_id         VARCHAR(50) PRIMARY KEY,
    conclusion_type       VARCHAR(50),     -- diagnosis/prediction/evaluation/cause_analysis
    title                 VARCHAR(500) NOT NULL,
    entity_type           VARCHAR(30),
    entity_id             VARCHAR(50),
    entity_name           VARCHAR(200),
    conclusion_text       TEXT NOT NULL,
    confidence            FLOAT,
    evidence_ids          VARCHAR(500),    -- JSON array
    reasoning_chain       TEXT,            -- Chain-of-Thought
    alternative_hypotheses TEXT,
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by            VARCHAR(30),      -- agent/human
    model                 VARCHAR(100),
    status                VARCHAR(20) DEFAULT 'active',
    valid_from            DATETIME,
    valid_to              DATETIME,
    related_conclusion_ids VARCHAR(500),   -- JSON array
    tags                  VARCHAR(500)
);

CREATE TABLE cost_drivers (
    driver_id          VARCHAR(50) PRIMARY KEY,
    driver_type        VARCHAR(50),    -- 规模型/效率型/战略型
    driver_name        VARCHAR(200),
    impact_factor      FLOAT,
    related_expenses   TEXT,
    calculation_logic  TEXT,
    status             VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE departments (
    department_id     VARCHAR(50) PRIMARY KEY,
    hospital_id       VARCHAR(50),
    department_name   VARCHAR(100),
    bed_count         INT,
    outpatient_volume INT,
    competitor_share  FLOAT,
    our_share         FLOAT,
    growth_potential  FLOAT,
    key_doctors       VARCHAR(500),       -- JSON array of doctor_ids
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
);

CREATE TABLE dim_alert_rules (
    rule_id               VARCHAR(50) PRIMARY KEY,
    rule_name             VARCHAR(200),
    rule_type             VARCHAR(50),
    entity_type           VARCHAR(30),
    metric                VARCHAR(100),
    condition_type        VARCHAR(30),
    threshold             DECIMAL(12,2),
    severity              VARCHAR(20),
    notification_template TEXT,
    auto_action           VARCHAR(100),
    enabled               TINYINT(1) DEFAULT 1,
    status                VARCHAR(20) DEFAULT 'active',
    created_at            DATETIME,
    updated_at            DATETIME
);

CREATE TABLE dim_channel_strategy (
    channel_id          VARCHAR(50) PRIMARY KEY,
    channel_name        VARCHAR(100),
    channel_type        VARCHAR(50),
    distributor_id      VARCHAR(50),
    region              VARCHAR(50),
    coverage_target     DECIMAL(5,4),
    delivery_days_target INT,
    stock_rate_target   DECIMAL(5,4),
    commission_rate     DECIMAL(6,4),
    status              VARCHAR(20) DEFAULT 'active',
    created_at          DATETIME
);

CREATE TABLE dim_clinical_pathway (
    pathway_id      VARCHAR(50) PRIMARY KEY,
    disease         VARCHAR(100) NOT NULL,
    disease_code    VARCHAR(50),
    hospital_id     VARCHAR(50),
    hospital_name   VARCHAR(200),
    department      VARCHAR(100),
    pathway_name    VARCHAR(200),
    pathway_version VARCHAR(20),
    effective_date  DATE,
    pathway_stage   VARCHAR(100),
    stage_order     INT,
    recommended_product VARCHAR(50),
    product_name    VARCHAR(200),
    dosage_regimen TEXT,
    duration_days   INT,
    expected_cost   DECIMAL(10,2),
    outcome_metrics TEXT,
    compliance_rate DECIMAL(6,2),
    notes           TEXT,
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME
);

CREATE TABLE dim_compliance_rules (
    rule_id           VARCHAR(50) PRIMARY KEY,
    rule_name         VARCHAR(200) NOT NULL,
    rule_category     VARCHAR(50) NOT NULL,  -- expense/visit/activity/disclosure/anti-corruption
    rule_type         VARCHAR(30) NOT NULL,  -- prohibition/limit/requirement/approval
    severity          VARCHAR(20) NOT NULL, -- critical/high/medium/low
    description       TEXT,
    legal_reference   VARCHAR(200),          -- 对应法规条款
    scope             VARCHAR(50),            -- national/regional/product_line
    applicable_roles  TEXT,                  -- JSON: ["rep","manager","director"]
    applicable_zones  TEXT,                  -- JSON: ["华东","华南"]
    conditions        TEXT,                  -- JSON DSL 条件表达式
    threshold_value   DECIMAL(16,4),
    threshold_unit    VARCHAR(30),
    penalty_type     VARCHAR(30),            -- warning/fine/termination/review
    penalty_amount    DECIMAL(12,2),
    enforcement_start DATE,
    enforcement_end   DATE,
    auto_enforce      TINYINT(1) DEFAULT 0,
    exception_allowed TINYINT(1) DEFAULT 0,
    exception_approval_level VARCHAR(30),
    related_policy_ids TEXT,                 -- JSON array
    tags              TEXT,
    status            VARCHAR(20) DEFAULT 'active',
    created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by        VARCHAR(50),
    updated_at        DATETIME,
    updated_by        VARCHAR(50)
);

CREATE TABLE dim_cost_standards (
    standard_id     VARCHAR(50) PRIMARY KEY,
    cost_type       VARCHAR(50),
    category        VARCHAR(50),
    sub_category    VARCHAR(50),
    region          VARCHAR(50),
    city_tier       VARCHAR(20),
    unit_cost       DECIMAL(10,2),
    max_cost        DECIMAL(10,2),
    currency        VARCHAR(10) DEFAULT 'CNY',
    effective_date   DATE,
    expiry_date      DATE,
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME
);

CREATE TABLE dim_distributors (
    distributor_id   VARCHAR(50) PRIMARY KEY,
    distributor_name VARCHAR(200),
    distributor_type VARCHAR(50),
    province        VARCHAR(50),
    city            VARCHAR(50),
    credit_level    VARCHAR(20),
    cooperation_years INT,
    annual_capacity DECIMAL(16,2),
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME
);

CREATE TABLE dim_doctor_segmentation (
    segment_id       VARCHAR(50) PRIMARY KEY,
    doctor_id        VARCHAR(50),
    segment_name     VARCHAR(50),
    segment_level    VARCHAR(10),
    kpi_weight       DECIMAL(5,4),
    avg_prescription DECIMAL(12,2),
    growth_rate      DECIMAL(8,4),
    potential        VARCHAR(20),
    risk_level       VARCHAR(20),
    status           VARCHAR(20) DEFAULT 'active',
    created_at       DATETIME
);

CREATE TABLE dim_doctors (
    doctor_id            VARCHAR(50) PRIMARY KEY,
    doctor_name          VARCHAR(100) NOT NULL,
    gender               VARCHAR(10),
    age                  INT,
    hospital_id          VARCHAR(50),
    hospital_name        VARCHAR(200),
    department           VARCHAR(100),
    title                VARCHAR(50),
    specialty            VARCHAR(100),
    province             VARCHAR(50),
    city                 VARCHAR(50),
    city_tier            VARCHAR(20),
    prescription_volume  DECIMAL(12,2),
    prescription_growth  DECIMAL(8,4),
    patient_count        INT,
    key_patient_types    TEXT,
    influence_score      DECIMAL(5,2),
    academic_influence   DECIMAL(5,2),
    product_affinity     TEXT,
    prescription_trend   VARCHAR(20),
    last_visit_date      DATE,
    visit_frequency      VARCHAR(20),
    engagement_level     VARCHAR(20),
    segment              VARCHAR(30),
    priority             VARCHAR(20),
    status               VARCHAR(20),
    kpi_weight           DECIMAL(5,4),
    contract_type       VARCHAR(50),
    updated_at           DATETIME,
    created_at           DATETIME,
    email                VARCHAR(100),
    phone                VARCHAR(50),
    birthday             DATE,
    education            VARCHAR(50),
    research_area        TEXT,
    publications         INT,
    meeting_frequency   VARCHAR(20)
);

CREATE TABLE dim_evidence (
    evidence_id    VARCHAR(50) PRIMARY KEY,
    evidence_type  VARCHAR(50),
    entity_type    VARCHAR(30),
    entity_id      VARCHAR(50),
    source_system  VARCHAR(100),
    event_date     DATE,
    description    TEXT,
    raw_data       TEXT,
    confidence     DECIMAL(5,4),
    status         VARCHAR(20) DEFAULT 'active',
    created_at     DATETIME
);

CREATE TABLE dim_hospital_access (
    access_id     VARCHAR(50) PRIMARY KEY,
    hospital_id   VARCHAR(50),
    product_id    VARCHAR(50),
    access_status VARCHAR(30),
    access_date   DATE,
    purchase_type VARCHAR(50),
    stock_status  VARCHAR(20),
    price         DECIMAL(10,2),
    reimbursement VARCHAR(20),
    notes         TEXT,
    status        VARCHAR(20) DEFAULT 'active',
    created_at    DATETIME
);

CREATE TABLE dim_hospital_competitive (
    competitive_id     VARCHAR(50) PRIMARY KEY,
    hospital_id        VARCHAR(50),
    product_id         VARCHAR(50),
    competitor_product VARCHAR(100),
    market_share       DECIMAL(5,4),
    competitor_share   DECIMAL(5,4),
    win_rate           DECIMAL(5,4),
    avg_price_ratio   DECIMAL(6,3),
    key_advantage      TEXT,
    status             VARCHAR(20) DEFAULT 'active',
    created_at         DATETIME
);

CREATE TABLE dim_hospital_departments (
    department_id   VARCHAR(50) PRIMARY KEY,
    hospital_id     VARCHAR(50),
    department_name VARCHAR(100),
    department_type VARCHAR(30),
    bed_count       INT,
    doctor_count    INT,
    annual_revenue  DECIMAL(16,2),
    key_products    TEXT,
    revenue_ratio   DECIMAL(5,4),
    growth_rate     DECIMAL(8,4),
    priority_level  VARCHAR(20),
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME
);

CREATE TABLE dim_hospital_segment (
    segment_id       VARCHAR(50) PRIMARY KEY,
    hospital_id      VARCHAR(50) NOT NULL,
    hospital_name    VARCHAR(200) NOT NULL,
    hospital_level   VARCHAR(20),
    segment_type     VARCHAR(50) NOT NULL,   -- strategic/target/core/growth/at_risk
    segment_reason   TEXT,
    annual_revenue   DECIMAL(16,2),
    annual_rx_volume DECIMAL(12,2),
    key_products     TEXT,                    -- JSON array
    accessibility    VARCHAR(20),  -- 容易/困难/受限
    competitive_pressure VARCHAR(20), -- high/medium/low
    resource_priority VARCHAR(20), -- high/medium/low
    account_manager_id VARCHAR(50),
    account_manager_name VARCHAR(100),
    development_potential DECIMAL(6,2),
    churn_risk       DECIMAL(5,4),
    last_review_date DATE,
    next_review_date DATE,
    status           VARCHAR(20) DEFAULT 'active',
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE dim_hospital_tender (
    tender_id       VARCHAR(50) PRIMARY KEY,
    hospital_id     VARCHAR(50),
    product_id      VARCHAR(50),
    tender_batch    VARCHAR(100),
    bidding_price   DECIMAL(10,2),
    winning_price   DECIMAL(10,2),
    tender_status   VARCHAR(30),
    tender_date     DATE,
    contract_start  DATE,
    contract_end    DATE,
    volume_commit   DECIMAL(16,2),
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME
);

CREATE TABLE dim_hospitals (
    hospital_id        VARCHAR(50) PRIMARY KEY,
    hospital_name      VARCHAR(200) NOT NULL,
    alias_name         VARCHAR(200),
    level              VARCHAR(20),
    type               VARCHAR(50),
    province           VARCHAR(50),
    city               VARCHAR(50),
    district           VARCHAR(50),
    address            VARCHAR(300),
    bed_count          INT,
    outpatient_volume  INT,
    annual_revenue     DECIMAL(16,2),
    employee_count     INT,
    department_count   INT,
    purchase_mode      VARCHAR(50),
    access_status      VARCHAR(50),
    access_date        DATE,
    contract_ratio     FLOAT,
    sales_ratio        FLOAT,
    territory_id       VARCHAR(50),
    territory_name     VARCHAR(100),
    market_potential   DECIMAL(16,2),
    status             VARCHAR(20) DEFAULT 'active',
    created_at         DATETIME,
    updated_at         DATETIME,
    key_departments    TEXT,
    hospital_strategy  VARCHAR(100)
);

CREATE TABLE dim_inference_rules (
    rule_id       VARCHAR(50) PRIMARY KEY,
    rule_name     VARCHAR(200),
    rule_pattern  TEXT,
    antecedent    TEXT,
    consequent    TEXT,
    confidence    DECIMAL(5,4),
    priority      INT,
    status        VARCHAR(20) DEFAULT 'active',
    created_at    DATETIME
);

CREATE TABLE dim_kol_network (
    kol_id           VARCHAR(50) PRIMARY KEY,
    doctor_id        VARCHAR(50) NOT NULL,
    doctor_name      VARCHAR(100) NOT NULL,
    hospital_id      VARCHAR(50),
    hospital_name    VARCHAR(200),
    department       VARCHAR(100),
    title            VARCHAR(50),
    specialty        VARCHAR(100),
    kol_level        VARCHAR(20) NOT NULL,   -- international/national/regional/local
    influence_scope  VARCHAR(50),            -- 影响力范围
    influence_area   TEXT,                   -- JSON array of therapeutic areas
    academic_title   VARCHAR(100),           -- 学术职务（主任/委员等）
    society_roles    TEXT,                   -- JSON array
    publication_count INT,
    h_index          INT,
    key_opinions     TEXT,                   -- 主要学术观点
    network_position VARCHAR(30),            -- hub/bridge/peripheral
    connected_kols   TEXT,                   -- JSON array of kol_ids
    connected_doctors TEXT,                  -- JSON array of doctor_ids
    connected_hospitals TEXT,                -- JSON array of hospital_ids
    related_products TEXT,                   -- JSON array
    engagement_status VARCHAR(20),
    engagement_cost  DECIMAL(12,2),
    activity_response_rate DECIMAL(5,2),
    notes            TEXT,
    status           VARCHAR(20) DEFAULT 'active',
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE dim_medical_insurance (
    insurance_id        VARCHAR(50) PRIMARY KEY,
    insurance_type      VARCHAR(50),
    province            VARCHAR(50),
    city                VARCHAR(50),
    product_id          VARCHAR(50),
    reimbursement_type  VARCHAR(30),
    reimbursement_rate  DECIMAL(5,4),
    reimbursement_price DECIMAL(10,2),
    category            VARCHAR(50),
    status              VARCHAR(20) DEFAULT 'active',
    effective_date      DATE,
    expiry_date         DATE,
    created_at          DATETIME
);

CREATE TABLE dim_national_policy (
    policy_id              VARCHAR(50) PRIMARY KEY,
    policy_name            VARCHAR(200),
    policy_type            VARCHAR(50),
    issuer                 VARCHAR(200),
    issued_date            DATE,
    effective_date         DATE,
    impact_area            VARCHAR(200),
    impact_description     TEXT,
    status                 VARCHAR(20) DEFAULT 'active',
    created_at             DATETIME
);

CREATE TABLE dim_patient_program (
    program_id           VARCHAR(50) PRIMARY KEY,
    program_name         VARCHAR(200),
    product_id           VARCHAR(50),
    program_type         VARCHAR(50),
    start_date           DATE,
    end_date             DATE,
    target_enrollment    INT,
    status               VARCHAR(20) DEFAULT 'active',
    created_at           DATETIME
);

CREATE TABLE dim_policy (
    policy_id     VARCHAR(50) PRIMARY KEY,
    policy_name   VARCHAR(200),
    policy_type   VARCHAR(50),
    issuer        VARCHAR(200),
    issued_date   DATE,
    effective_date DATE,
    expiry_date   DATE,
    region        VARCHAR(100),
    impact_scope  TEXT,
    key_points    TEXT,
    status        VARCHAR(20) DEFAULT 'active',
    created_at    DATETIME
);

CREATE TABLE dim_product_category (
    category_id   VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    parent_id     VARCHAR(50),
    level         INT,
    description   TEXT,
    status        VARCHAR(20) DEFAULT 'active',
    created_at    DATETIME
);

CREATE TABLE dim_product_competition (
    competition_id    VARCHAR(50) PRIMARY KEY,
    product_id        VARCHAR(50),
    competitor_id     VARCHAR(50),
    competitor_name   VARCHAR(200),
    brand_name        VARCHAR(100),
    therapeutic_area  VARCHAR(100),
    advantage         TEXT,
    weakness          TEXT,
    market_share      DECIMAL(5,4),
    price_ratio       DECIMAL(6,3),
    status            VARCHAR(20) DEFAULT 'active',
    created_at        DATETIME
);

CREATE TABLE dim_product_distribution (
    distribution_id  VARCHAR(50) PRIMARY KEY,
    product_id      VARCHAR(50),
    distributor_id   VARCHAR(50),
    region          VARCHAR(100),
    channel_type    VARCHAR(50),
    coverage_rate   DECIMAL(5,4),
    delivery_days   INT,
    stock_rate      DECIMAL(5,4),
    status          VARCHAR(20) DEFAULT 'active',
    contract_start   DATE,
    contract_end     DATE,
    created_at      DATETIME
);

CREATE TABLE dim_product_formulation (
    formulation_id       VARCHAR(50) PRIMARY KEY,
    product_id           VARCHAR(50),
    formulation_type     VARCHAR(50),
    specification        VARCHAR(100),
    unit                 VARCHAR(20),
    conversion_ratio     DECIMAL(6,3),
    storage_conditions   VARCHAR(100),
    shelf_life_months   INT,
    manufacturer_site   VARCHAR(200),
    status               VARCHAR(20) DEFAULT 'active',
    created_at           DATETIME
);

CREATE TABLE dim_product_market (
    market_id        VARCHAR(50) PRIMARY KEY,
    product_id       VARCHAR(50) NOT NULL,
    product_name    VARCHAR(200),
    market_name     VARCHAR(200),
    therapeutic_area VARCHAR(100),
    market_size     DECIMAL(16,2),
    market_size_unit VARCHAR(20),
    `year`            INT NOT NULL,
    quarter         VARCHAR(10),
    our_share       DECIMAL(6,2),
    competitor_share TEXT,          -- JSON: {competitor: share}
    growth_rate     DECIMAL(8,4),
    price_elasticity DECIMAL(6,2),
    patient_count   INT,
    treatment_rate  DECIMAL(6,2),
    diagnosis_rate  DECIMAL(6,2),
    pipeline_volume DECIMAL(12,2),
    market_trend    VARCHAR(20),   -- growing/stable/declining
    entry_barrier   VARCHAR(30),
    key_success_factors TEXT,
    data_source     VARCHAR(100),
    data_period      VARCHAR(50),
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_product_pricing (
    pricing_id      VARCHAR(50) PRIMARY KEY,
    product_id     VARCHAR(50),
    price_type     VARCHAR(30),
    price          DECIMAL(10,2),
    province       VARCHAR(50),
    city           VARCHAR(50),
    hospital_tier  VARCHAR(10),
    effective_date  DATE,
    expiry_date     DATE,
    status         VARCHAR(20) DEFAULT 'active',
    created_at     DATETIME
);

CREATE TABLE dim_products (
    product_id            VARCHAR(50) PRIMARY KEY,
    product_name          VARCHAR(200) NOT NULL,
    generic_name          VARCHAR(200),
    brand_name            VARCHAR(100),
    approval_number       VARCHAR(50),
    manufacturer          VARCHAR(200),
    manufacturer_name     VARCHAR(200),
    therapeutic_category  VARCHAR(100),
    indication_1          VARCHAR(100),
    indication_2          VARCHAR(100),
    dosage_form           VARCHAR(50),
    specification         VARCHAR(100),
    unit                  VARCHAR(20),
    retail_price          DECIMAL(10,2),
    contract_price        DECIMAL(10,2),
    conversion_ratio      DECIMAL(6,3),
    reimbursement_type    VARCHAR(20),
    reimbursement_rate    DECIMAL(5,4),
    reimbursement_price   DECIMAL(10,2),
    status                VARCHAR(20) DEFAULT 'active',
    launch_date           DATE,
    offpatent_date        DATE,
    market_segment        VARCHAR(50),
    core_indications     TEXT,
    annual_sales         DECIMAL(16,2),
    market_potential      DECIMAL(16,2),
    sales_model           VARCHAR(30),
    product_status        VARCHAR(20),
    updated_at            DATETIME,
    created_at            DATETIME,
    last_visit_date       DATE
);

CREATE TABLE dim_reimbursement (
    reimb_id         VARCHAR(50) PRIMARY KEY,
    expense_category VARCHAR(50) NOT NULL,   -- travel/accommodation/meal/entertainment
    expense_subcategory VARCHAR(100),        -- flight/train/hotel/restaurant
    level            VARCHAR(20) NOT NULL,  -- rep/manager/director/national
    region           VARCHAR(50),            -- national/specific province
    product_line     VARCHAR(50),
    standard_amount  DECIMAL(10,2),
    max_amount       DECIMAL(10,2),
    currency         VARCHAR(10) DEFAULT 'CNY',
    unit             VARCHAR(20),            -- per_day/per_visit/per_event
    quantity_limit   INT,
    requires_receipt TINYINT(1) DEFAULT 1,
    requires_pre_approval TINYINT(1) DEFAULT 0,
    approval_level   VARCHAR(30),
    eligible_vendor_types TEXT,              -- JSON array
    ineligible_items TEXT,
    compliance_notes TEXT,
    effective_date   DATE NOT NULL,
    expiration_date  DATE,
    policy_reference VARCHAR(100),
    status           VARCHAR(20) DEFAULT 'active',
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by       VARCHAR(50),
    updated_at       DATETIME,
    updated_by       VARCHAR(50)
);

CREATE TABLE dim_rep_credential (
    credential_id   VARCHAR(50) PRIMARY KEY,
    rep_id          VARCHAR(50) NOT NULL,
    rep_name        VARCHAR(100),
    credential_type VARCHAR(50) NOT NULL,  -- certification/license/training/certificate
    credential_name VARCHAR(200),
    issuer         VARCHAR(100),
    issue_date      DATE,
    expiry_date     DATE,
    status          VARCHAR(20),   -- valid/expired/pending_renewal/suspended
    renewal_required TINYINT(1) DEFAULT 0,
    renewal_date     DATE,
    training_hours  DECIMAL(6,2),
    exam_score      DECIMAL(5,2),
    certificate_number VARCHAR(100),
    attachment_urls TEXT,
    verification_url VARCHAR(200),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME
);

CREATE TABLE dim_rep_doctor_mapping (
    mapping_id         VARCHAR(50) PRIMARY KEY,
    rep_id             VARCHAR(50),
    doctor_id          VARCHAR(50),
    last_visit_date    DATE,
    visit_count        INT,
    prescription_count INT,
    status             VARCHAR(20) DEFAULT 'active',
    created_at         DATETIME
);

CREATE TABLE dim_rep_hospital_mapping (
    mapping_id      VARCHAR(50) PRIMARY KEY,
    rep_id          VARCHAR(50),
    hospital_id     VARCHAR(50),
    access_level    VARCHAR(20),
    visit_frequency VARCHAR(20),
    is_primary      TINYINT(1),
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME
);

CREATE TABLE dim_rep_performance (
    performance_id      VARCHAR(50) PRIMARY KEY,
    rep_id              VARCHAR(50),
    rep_name            VARCHAR(100),
    period              VARCHAR(20),
    sales_amount        DECIMAL(16,2),
    sales_target        DECIMAL(16,2),
    achievement_rate    DECIMAL(6,4),
    visit_count         INT,
    visit_target        INT,
    doctor_count        INT,
    new_doctor_count    INT,
    hospital_count      INT,
    product_knowledge_score DECIMAL(5,2),
    compliance_rate     DECIMAL(5,4),
    training_hours      DECIMAL(6,2),
    status              VARCHAR(20) DEFAULT 'active',
    created_at          DATETIME,
    updated_at          DATETIME
);

CREATE TABLE dim_rep_territory (
    territory_id    VARCHAR(50) PRIMARY KEY,
    territory_name  VARCHAR(100),
    region          VARCHAR(50),
    province        VARCHAR(50),
    city            VARCHAR(50),
    hospital_count  INT,
    doctor_count    INT,
    target_sales    DECIMAL(16,2),
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME
);

CREATE TABLE dim_representative_doctor (
    relation_id      VARCHAR(50) PRIMARY KEY,
    rep_id           VARCHAR(50) NOT NULL,
    rep_name         VARCHAR(100),
    doctor_id        VARCHAR(50) NOT NULL,
    doctor_name      VARCHAR(100),
    hospital_id      VARCHAR(50),
    hospital_name    VARCHAR(200),
    product_id       VARCHAR(50),
    product_name     VARCHAR(200),
    relationship_type VARCHAR(30),  -- prescribing/advocate/neutral/at_risk/churned
    engagement_level VARCHAR(20),
    visit_frequency_target INT,     -- 每月目标频次
    visit_frequency_actual INT,     -- 每月实际频次
    last_visit_date  DATE,
    last_call_date   DATE,
    last_call_type   VARCHAR(30),
    last_call_outcome VARCHAR(50),
    last_rx_volume   DECIMAL(12,2),
    rx_trend         VARCHAR(20),   -- rising/stable/falling
    priority_flag    VARCHAR(20),  -- VIP/regular/watch
    churn_probability DECIMAL(5,4),
    is_key_doctor    TINYINT(1) DEFAULT 0,
    is_kol           TINYINT(1) DEFAULT 0,
    next_visit_suggested DATE,
    call_plan_notes  TEXT,
    status           VARCHAR(20) DEFAULT 'active',
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE dim_representative_hospital (
    relation_id      VARCHAR(50) PRIMARY KEY,
    rep_id           VARCHAR(50) NOT NULL,
    rep_name         VARCHAR(100),
    hospital_id      VARCHAR(50) NOT NULL,
    hospital_name    VARCHAR(200),
    product_id       VARCHAR(50),
    product_name     VARCHAR(200),
    access_level     VARCHAR(20),  -- primary/secondary/observation
    visit_frequency_target INT,    -- 每月目标拜访频次
    visit_frequency_actual INT,   -- 每月实际拜访频次
    last_visit_date  DATE,
    next_visit_plan  DATE,
    hospital_value_class VARCHAR(20), -- A/B/C/D 四类
    development_stage VARCHAR(30),     -- initial/prospecting/negotiating/contracted
    potential_revenue DECIMAL(16,2),   -- 潜力收入
    actual_revenue   DECIMAL(16,2),
    competitive_intensity VARCHAR(20), -- high/medium/low
    key_competitors  TEXT,            -- JSON array of competitor names
    status           VARCHAR(20) DEFAULT 'active',
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE dim_reps (
    rep_id              VARCHAR(50) PRIMARY KEY,
    rep_name            VARCHAR(100) NOT NULL,
    gender              VARCHAR(10),
    age                 INT,
    territory_id        VARCHAR(50),
    territory_name      VARCHAR(100),
    province            VARCHAR(50),
    city                VARCHAR(50),
    hire_date           DATE,
    dim_date            DATE,
    product_ids         TEXT,
    title               VARCHAR(50),
    compliance_score    DECIMAL(5,2),
    status              VARCHAR(20),
    performance_tier    VARCHAR(20),
    updated_at          DATETIME,
    created_at          DATETIME,
    last_visit_date      DATE,
    email               VARCHAR(100),
    phone               VARCHAR(50),
    manager_id          VARCHAR(50),
    region              VARCHAR(50),
    product_line        VARCHAR(50),
    qualification       VARCHAR(50),
    updated_by          VARCHAR(50)
);

CREATE TABLE dim_rws_study (
    study_id              VARCHAR(50) PRIMARY KEY,
    study_name            VARCHAR(200),
    product_id            VARCHAR(50),
    study_type            VARCHAR(50),
    principal_investigator VARCHAR(100),
    hospital_ids          TEXT,
    start_date            DATE,
    end_date              DATE,
    sample_size           INT,
    status                VARCHAR(20) DEFAULT 'active',
    created_at            DATETIME
);

CREATE TABLE dim_secondary_hospital (
    hospital_id      VARCHAR(50) PRIMARY KEY,
    hospital_name    VARCHAR(200) NOT NULL,
    hospital_type    VARCHAR(50) NOT NULL,   -- community/private/clinic
    parent_hospital_id VARCHAR(50),          -- 关联上级医院
    level            VARCHAR(20),
    location         VARCHAR(100),
    province         VARCHAR(50),
    city             VARCHAR(50),
    district         VARCHAR(50),
    address          VARCHAR(300),
    bed_count        INT,
    established_date DATE,
    owner_type       VARCHAR(30),  -- state/private/nonprofit
    insurance定点    TINYINT(1) DEFAULT 0,
    insurance_types  TEXT,         -- JSON array
    specialty        VARCHAR(100),
    key_departments  TEXT,
    daily_patient_volume INT,
    monthly_rx_volume DECIMAL(12,2),
    drug_budget      DECIMAL(12,2),
    procurement_channel VARCHAR(50),
    access_status    VARCHAR(20),
    rep_id           VARCHAR(50),
    rep_name         VARCHAR(100),
    development_stage VARCHAR(30),
    potential        DECIMAL(10,2),
    priority         VARCHAR(20),
    last_contact_date DATE,
    contact_frequency INT,          -- 每年接触频次
    notes            TEXT,
    status           VARCHAR(20) DEFAULT 'active',
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE dim_system_config (
    config_id       VARCHAR(50) PRIMARY KEY,
    config_category VARCHAR(50) NOT NULL,  -- kpi/alert/workflow/integration
    config_key      VARCHAR(100) NOT NULL UNIQUE,
    config_value    TEXT NOT NULL,
    value_type      VARCHAR(30),          -- string/number/boolean/json
    description     TEXT,
    effective_date  DATE,
    expiration_date DATE,
    is_encrypted    TINYINT(1) DEFAULT 0,
    is_system       TINYINT(1) DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by      VARCHAR(50),
    updated_at      DATETIME,
    updated_by      VARCHAR(50)
);

CREATE TABLE dim_territories (
    territory_id    VARCHAR(50) PRIMARY KEY,
    territory_name  VARCHAR(200),
    region          VARCHAR(50),
    province        VARCHAR(50),
    city            VARCHAR(50),
    city_tier       VARCHAR(20),
    hospital_count  INT,
    doctor_count    INT,
    rep_count       INT,
    target_sales    DECIMAL(16,2),
    actual_sales    DECIMAL(16,2),
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME
);

CREATE TABLE dim_territory_mapping (
    mapping_id       VARCHAR(50) PRIMARY KEY,
    region_id        VARCHAR(50),
    region_name      VARCHAR(100),
    zone_id          VARCHAR(50),
    zone_name        VARCHAR(100),
    province_id      VARCHAR(50),
    province_name    VARCHAR(100),
    city_id          VARCHAR(50),
    city_name        VARCHAR(100),
    district_id      VARCHAR(50),
    district_name    VARCHAR(100),
    territory_id     VARCHAR(50),
    territory_name   VARCHAR(100),
    hospital_id      VARCHAR(50),
    hospital_name    VARCHAR(200),
    hospital_level   VARCHAR(20),
    product_id       VARCHAR(50),
    product_name     VARCHAR(200),
    rep_id           VARCHAR(50),
    rep_name         VARCHAR(100),
    is_primary       TINYINT(1) DEFAULT 0,  -- 主负责代表
    is_coverage      TINYINT(1) DEFAULT 1,  -- 是否覆盖
    coverage_level   VARCHAR(20),           -- full/partial/seasonal
    start_date       DATE,
    end_date         DATE,
    status           VARCHAR(20) DEFAULT 'active',
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by       VARCHAR(50),
    updated_at       DATETIME
);

CREATE TABLE dim_traffic_light_rules (
    rule_id          VARCHAR(50) PRIMARY KEY,
    indicator        VARCHAR(100),
    green_threshold  DECIMAL(6,4),
    yellow_threshold DECIMAL(6,4),
    entity_type      VARCHAR(30),
    period_type      VARCHAR(20),
    description      TEXT,
    status           VARCHAR(20) DEFAULT 'active',
    created_at       DATETIME
);

CREATE TABLE dim_vbp_policy (
    policy_id         VARCHAR(50) PRIMARY KEY,
    batch             VARCHAR(50),
    region            VARCHAR(100),
    product_id        VARCHAR(50),
    winning_price     DECIMAL(10,2),
    price_reduction   DECIMAL(6,4),
    impact_level      VARCHAR(20),
    execution_date    DATE,
    contract_end_date DATE,
    status            VARCHAR(20) DEFAULT 'active',
    created_at        DATETIME
);

CREATE TABLE dim_vbp_status (
    vbp_id               VARCHAR(50) PRIMARY KEY,
    product_id           VARCHAR(50),
    tender_batch         VARCHAR(100),
    region               VARCHAR(100),
    vbp_status           VARCHAR(30),
    bidding_price        DECIMAL(12,2),
    winning_price        DECIMAL(12,2),
    price_reduction_rate FLOAT,
    execution_start_date DATE,
    execution_end_date   DATE,
    contract_volume      DECIMAL(16,2),
    contract_amount      DECIMAL(16,2),
    leftover_volume      DECIMAL(16,2),
    impact_assessment    TEXT,
    status               VARCHAR(20) DEFAULT 'active',
    created_at           DATETIME
);

CREATE TABLE distributors (
    distributor_id       VARCHAR(50) PRIMARY KEY,
    distributor_name     VARCHAR(200),
    region               VARCHAR(100),
    hospital_ids         VARCHAR(1000),   -- JSON array
    reliability_score   FLOAT,
    avg_delivery_days   FLOAT,
    on_time_rate        FLOAT,
    status               VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE doctors (
    doctor_id                 VARCHAR(50) PRIMARY KEY,
    doctor_name               VARCHAR(100) NOT NULL,
    title                     VARCHAR(50),   -- 主任医师/副主任医师/主治医师/住院医师
    department                VARCHAR(100),
    specialty                 VARCHAR(200),
    hospital_id               VARCHAR(50),
    hospital_name             VARCHAR(200),
    prescription_power        INT,            -- 1-100
    influence_score          INT,            -- 1-100 学术影响力
    prescription_potential    INT,            -- 1-100
    current_patient_volume   INT,
    target_product            VARCHAR(50),
    prescription_volume       INT,            -- 直近处方量
    prescription_trend        VARCHAR(20),    -- rising/falling/stable
    sentiment                 VARCHAR(20),    -- positive/neutral/negative
    engagement_level          VARCHAR(20), 
    last_visit_date          DATE,
    next_recommended_visit   DATE,
    visit_frequency_actual   INT,            -- 次/月
    visit_frequency_recommended INT,         -- 次/月
    lifecycle_stage           VARCHAR(30),    -- new/prospecting/converting/mature/at_risk/churned
    churn_probability        FLOAT DEFAULT 0,
    key_insights              TEXT,
    status                    VARCHAR(20) DEFAULT 'active',
    created_at                DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at                DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
);

CREATE TABLE events (
    event_id              VARCHAR(50) PRIMARY KEY,
    event_type            VARCHAR(50) NOT NULL,
    event_category        VARCHAR(50),
    entity_type           VARCHAR(30),
    entity_id             VARCHAR(50),
    entity_name           VARCHAR(200),
    related_entity_type   VARCHAR(30),
    related_entity_id     VARCHAR(50),
    related_entity_name   VARCHAR(200),
    `timestamp`             DATETIME NOT NULL,
    description           TEXT,
    details               TEXT,            -- JSON
    location              VARCHAR(200),
    participant_ids       VARCHAR(500),    -- JSON array
    participant_names    VARCHAR(500),
    outcome               TEXT,
    impact_score          FLOAT,
    source                VARCHAR(100),
    verified              TINYINT(1) DEFAULT 0,
    status                VARCHAR(20) DEFAULT 'active',
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evidence (
    evidence_id           VARCHAR(50) PRIMARY KEY,
    evidence_type         VARCHAR(30),     -- report/policy/literature/minutes/journal
    title                 VARCHAR(500) NOT NULL,
    content               TEXT,
    source                VARCHAR(200),
    url                   VARCHAR(500),
    published_date        DATE,
    effective_date        DATE,
    expiration_date       DATE,
    applicable_regions     VARCHAR(500),
    applicable_products   VARCHAR(1000),   -- JSON array
    applicable_entities   VARCHAR(1000),   -- JSON array
    impact_assessment     TEXT,
    key_points            TEXT,
    compliance_requirements TEXT,
    related_rules         VARCHAR(500),    -- JSON array
    tags                  VARCHAR(500),    -- JSON array
    vector_embedding      TEXT,
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by            VARCHAR(100)
);

CREATE TABLE expense_records (
    expense_id         VARCHAR(50) PRIMARY KEY,
    expense_type       VARCHAR(50),    -- C1总部活动/C2A区域活动/C3代表活动
    amount             DECIMAL(12,2) NOT NULL,
    expense_date       DATE NOT NULL,
    rep_id             VARCHAR(50),
    rep_name           VARCHAR(100),
    hospital_id        VARCHAR(50),
    hospital_name      VARCHAR(200),
    doctor_id          VARCHAR(50),
    doctor_name        VARCHAR(100),
    activity_type      VARCHAR(100),
    activity_id        VARCHAR(50),
    description        TEXT,
    vendor             VARCHAR(200),
    attendee_count     INT,
    cost_per_person    DECIMAL(12,2),
    compliance_check    VARCHAR(50),
    approval_status    VARCHAR(30) DEFAULT 'pending',
    approved_by       VARCHAR(100),
    approved_at        DATETIME,
    receipt_url        VARCHAR(500),
    status             VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id),
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
);

CREATE TABLE expense_rois (
    roi_id             VARCHAR(50) PRIMARY KEY,
    expense_amount     DECIMAL(16,2),
    revenue_generated  DECIMAL(16,2),
    roi_ratio          FLOAT,
    attribution_model  VARCHAR(100),
    calculation_period VARCHAR(20),
    rep_id             VARCHAR(50),
    hospital_id        VARCHAR(50),
    product_id         VARCHAR(50),
    activity_type      VARCHAR(100),
    status             VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id),
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE fct_academic_activities (
    activity_id      VARCHAR(50) PRIMARY KEY,
    activity_type   VARCHAR(50),
    activity_name   VARCHAR(200),
    rep_id          VARCHAR(50),
    hospital_id     VARCHAR(50),
    hospital_name   VARCHAR(200),
    department      VARCHAR(100),
    product_id      VARCHAR(50),
    speaker_name    VARCHAR(100),
    event_date      DATE,
    attendee_count  INT,
    doctor_count    INT,
    total_amount    DECIMAL(12,2),
    cost_per_person DECIMAL(10,2),
    venue           VARCHAR(200),
    content_summary TEXT,
    feedback_score  DECIMAL(3,1),
    compliance_check VARCHAR(50),
    approval_status VARCHAR(30),
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME
);

CREATE TABLE fct_academic_activity (
    activity_id     VARCHAR(50) PRIMARY KEY,
    activity_name   VARCHAR(200) NOT NULL,
    activity_type   VARCHAR(50) NOT NULL,  -- conference/CME/seminar/symposium/workshop
    product_id      VARCHAR(50),
    product_name   VARCHAR(200),
    activity_date   DATE NOT NULL,
    end_date        DATE,
    duration_days   INT,
    location        VARCHAR(200),
    province        VARCHAR(50),
    city            VARCHAR(50),
    organizer_type  VARCHAR(30),  -- company/medical_society/third_party
    organizer_name  VARCHAR(200),
    target_audience VARCHAR(100),
    expected_attendees INT,
    actual_attendees INT,
    attendee_ids    TEXT,         -- JSON array
    attendee_names  TEXT,
    speaker_ids     TEXT,
    speaker_names   TEXT,
    topic           VARCHAR(200),
    scientific_content TEXT,
    budget_approved DECIMAL(14,2),
    budget_spent   DECIMAL(14,2),
    cost_per_attendee DECIMAL(10,2),
    key_outcomes   TEXT,
    post_activity_survey TEXT,
    reach          INT,           -- 覆盖人数
    impact_score   DECIMAL(5,2),
    roi_estimate   DECIMAL(6,2),
    status         VARCHAR(20) DEFAULT 'planned',
    created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME
);

CREATE TABLE fct_action_results (
    result_id    VARCHAR(50) PRIMARY KEY,
    action_id    VARCHAR(50),
    result_type  VARCHAR(50),
    result_value DECIMAL(12,2),
    result_date  DATE,
    notes        TEXT,
    status       VARCHAR(20) DEFAULT 'active',
    created_at   DATETIME
);

CREATE TABLE fct_actions (
    action_id           VARCHAR(50) PRIMARY KEY,
    action_type         VARCHAR(50),
    action_name         VARCHAR(200),
    rep_id              VARCHAR(50),
    doctor_id           VARCHAR(50),
    hospital_id         VARCHAR(50),
    product_id          VARCHAR(50),
    plan_date           DATE,
    actual_date         DATE,
    channel             VARCHAR(50),
    topic               VARCHAR(200),
    outcome             TEXT,
    follow_up_required  TINYINT(1),
    follow_up_date      DATE,
    status              VARCHAR(20) DEFAULT 'active',
    created_at          DATETIME,
    updated_at          DATETIME
);

CREATE TABLE fct_annual_plan (
    plan_id         VARCHAR(50) PRIMARY KEY,
    plan_year       INT,
    rep_id          VARCHAR(50),
    product_id      VARCHAR(50),
    territory_id    VARCHAR(50),
    sales_target    DECIMAL(16,2),
    visit_target    INT,
    doctor_target   INT,
    hospital_target INT,
    budget_target   DECIMAL(16,2),
    strategy        TEXT,
    key_actions     TEXT,
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME
);

CREATE TABLE fct_anomaly_detection (
    anomaly_id      VARCHAR(50) PRIMARY KEY,
    anomaly_type    VARCHAR(50) NOT NULL,   -- prescription/expense/inventory/visit
    detection_model  VARCHAR(50),
    entity_type     VARCHAR(50) NOT NULL,   -- doctor/hospital/rep/product
    entity_id       VARCHAR(50) NOT NULL,
    entity_name     VARCHAR(200),
    province         VARCHAR(50),
    period_type      VARCHAR(20),
    period_value     VARCHAR(20),
    metric_name      VARCHAR(100),
    metric_value     DECIMAL(16,4),
    baseline_value   DECIMAL(16,4),
    expected_value   DECIMAL(16,4),
    deviation_pct    DECIMAL(8,4),
    anomaly_score    DECIMAL(5,2),          -- 0-100
    alert_level      VARCHAR(10),           -- red/yellow/green
    delta_weight     DECIMAL(8,4),          -- PPT
    statistical_method VARCHAR(50),        -- z_score/pct/isolation_forest
    p_value          DECIMAL(6,4),
    confidence_interval TEXT,
    possible_causes  TEXT,                  -- JSON array
    priority         INT,
    status           VARCHAR(20) DEFAULT 'detected', -- detected/investigating/resolved/false_alarm
    investigated_by  VARCHAR(50),
    investigation_notes TEXT,
    resolved_date    DATE,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fct_ap_ar (
    arap_id       VARCHAR(50) PRIMARY KEY,
    type          VARCHAR(10),
    entity_name   VARCHAR(200),
    product_id    VARCHAR(50),
    invoice_no    VARCHAR(100),
    invoice_date  DATE,
    due_date      DATE,
    amount        DECIMAL(16,2),
    paid_amount   DECIMAL(16,2),
    outstanding   DECIMAL(16,2),
    status        VARCHAR(20),
    payment_date  DATE,
    created_at    DATETIME
);

CREATE TABLE fct_attribution_analysis (
    attr_id         VARCHAR(50) PRIMARY KEY,
    analysis_type   VARCHAR(50) NOT NULL,  -- sales_decline/growth/spent_roi
    target_entity_type VARCHAR(50) NOT NULL,
    target_entity_id VARCHAR(50) NOT NULL,
    target_entity_name VARCHAR(200),
    period_type     VARCHAR(20),
    period_value    VARCHAR(20),
    base_value      DECIMAL(16,4),
    current_value   DECIMAL(16,4),
    change_value    DECIMAL(16,4),
    change_pct      DECIMAL(8,4),
    attribution_model VARCHAR(50),          -- linear/shapley/fallback
    -- 结构归因
    structure_contribution DECIMAL(10,4),
    structure_factors    TEXT,             -- JSON array
    structure_contributors TEXT,
    -- 行为归因
    behavior_contribution DECIMAL(10,4),
    behavior_factors      TEXT,
    behavior_contributors TEXT,
    -- 决策归因
    decision_contribution DECIMAL(10,4),
    decision_factors      TEXT,
    decision_contributors TEXT,
    external_factors      TEXT,
    confidence           DECIMAL(5,2),
    conclusion           TEXT,
    recommendation       TEXT,
    model_version        VARCHAR(20),
    created_at           DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at           DATETIME
);

CREATE TABLE fct_audit_log (
    audit_id          VARCHAR(50) PRIMARY KEY,
    audit_type        VARCHAR(50) NOT NULL,  -- data_change/permission/login/report_access
    actor_type        VARCHAR(30) NOT NULL,  -- user/system/api/agent
    actor_id          VARCHAR(50) NOT NULL,
    actor_name        VARCHAR(100),
    actor_role        VARCHAR(50),
    target_type       VARCHAR(50),
    target_id         VARCHAR(50),
    target_name       VARCHAR(200),
    action            VARCHAR(100) NOT NULL,  -- create/update/delete/export/login
    changes           TEXT,                   -- JSON: before/after for updates
    ip_address        VARCHAR(50),
    device_id         VARCHAR(100),
    session_id        VARCHAR(100),
    result            VARCHAR(20) DEFAULT 'success', -- success/failure/partial
    error_message     TEXT,
    `timestamp`         DATETIME DEFAULT CURRENT_TIMESTAMP,
    related_entity_type VARCHAR(50),
    related_entity_id   VARCHAR(50),
    module            VARCHAR(50),           -- expense/visit/performance/budget
    reason            VARCHAR(200),
    approval_chain    TEXT,                  -- JSON: approvers and decisions
    tags              TEXT
);

CREATE TABLE fct_budget_allocation (
    budget_id         VARCHAR(50) PRIMARY KEY,
    period            VARCHAR(20),
    product_id         VARCHAR(50),
    rep_id             VARCHAR(50),
    territory_id       VARCHAR(50),
    region             VARCHAR(50),
    budget_type        VARCHAR(50),
    budget_amount      DECIMAL(16,2),
    allocated_amount   DECIMAL(16,2),
    spent_amount       DECIMAL(16,2),
    commitment_amount  DECIMAL(16,2),
    available_amount  DECIMAL(16,2),
    utilization_rate   DECIMAL(6,4),
    start_date         DATE,
    end_date           DATE,
    status             VARCHAR(20) DEFAULT 'active',
    created_at         DATETIME,
    updated_at         DATETIME
);

CREATE TABLE fct_call_conversation (
    conversation_id  VARCHAR(50) PRIMARY KEY,
    visit_id         VARCHAR(50) NOT NULL,
    rep_id           VARCHAR(50) NOT NULL,
    doctor_id        VARCHAR(50),
    call_date        DATE NOT NULL,
    call_type        VARCHAR(30),
    segments         TEXT,                  -- JSON: [{"role":"rep","text":"..."},{"role":"doctor","text":"..."}]
    sentiment_score  DECIMAL(5,2),         -- 整体情感评分 0-100
    doctor_sentiment DECIMAL(5,2),
    topics_mentioned TEXT,                  -- JSON array of topic keywords
    product_mentioned TEXT,                 -- JSON array
    competitor_mentioned TEXT,              -- JSON array
    objection_raised TEXT,                  -- JSON array
    objection_handled TINYINT(1),
    key_insights     TEXT,
    ai_quality_score DECIMAL(5,2),          -- AI 质检评分
    compliance_check_result VARCHAR(30),    -- pass/warning/fail
    compliance_violations TEXT,              -- JSON array of violation types
    reviewed         TINYINT(1) DEFAULT 0,
    reviewed_by      VARCHAR(50),
    reviewed_at      DATETIME,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fct_campaign (
    campaign_id      VARCHAR(50) PRIMARY KEY,
    campaign_name    VARCHAR(200) NOT NULL,
    campaign_type    VARCHAR(50) NOT NULL,   -- launch/promotion/seasonal/competitive
    campaign_subtype  VARCHAR(50),
    product_id       VARCHAR(50),
    product_name     VARCHAR(200),
    target_segments   TEXT,                   -- JSON array of target segments
    target_regions   TEXT,                   -- JSON array of provinces
    target_hospitals TEXT,                   -- JSON array of hospital_ids
    target_doctors   TEXT,                   -- JSON array of doctor_ids
    start_date       DATE NOT NULL,
    end_date         DATE,
    duration_days    INT,
    total_budget     DECIMAL(14,2),
    spent_budget     DECIMAL(14,2),
    budget_execution_rate DECIMAL(6,2),
    expected_output   TEXT,                  -- JSON: {rx_volume, market_share, awareness}
    actual_output    TEXT,
    expected_roi     DECIMAL(6,2),
    actual_roi       DECIMAL(6,2),
    kpis             TEXT,                    -- JSON array of KPI metrics
    status           VARCHAR(20) DEFAULT 'planning', -- planning/running/completed/terminated
    owner            VARCHAR(50),
    team_members     TEXT,                   -- JSON array of rep_ids
    related_policies TEXT,                   -- JSON array
    tags             TEXT,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by       VARCHAR(50),
    updated_at       DATETIME,
    updated_by       VARCHAR(50)
);

CREATE TABLE fct_campaign_response (
    response_id      VARCHAR(50) PRIMARY KEY,
    campaign_id      VARCHAR(50) NOT NULL,
    campaign_name    VARCHAR(200),
    campaign_type    VARCHAR(50),
    activity_id      VARCHAR(50),
    activity_name    VARCHAR(200),
    patient_id       VARCHAR(50),
    doctor_id        VARCHAR(50),
    doctor_name      VARCHAR(100),
    hospital_id      VARCHAR(50),
    hospital_name    VARCHAR(200),
    rep_id           VARCHAR(50),
    rep_name         VARCHAR(100),
    patient_segment  VARCHAR(30),   -- new/start/switch/maintain
    product_id       VARCHAR(50),
    product_name     VARCHAR(200),
    response_type    VARCHAR(30),  -- enrolled/completed/dropped/converted
    enrollment_date  DATE,
    completion_date   DATE,
    therapy_duration INT,          -- 天数
    persistence_rate  DECIMAL(5,2),
   疗效评价           VARCHAR(30),
    adverse_event     TINYINT(1) DEFAULT 0,
    switch_product   VARCHAR(50),
    switch_reason    TEXT,
    roi_attribution  DECIMAL(6,4),
    cost_per_patient  DECIMAL(10,2),
    period_value      VARCHAR(20),
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE fct_campaign_result (
    result_id        VARCHAR(50) PRIMARY KEY,
    campaign_id      VARCHAR(50) NOT NULL,
    campaign_name    VARCHAR(200),
    period_type      VARCHAR(20),
    period_value     VARCHAR(20),
    province         VARCHAR(50),
    territory_id     VARCHAR(50),
    hospital_id      VARCHAR(50),
    hospital_name    VARCHAR(200),
    doctor_id        VARCHAR(50),
    doctor_name      VARCHAR(100),
    rep_id           VARCHAR(50),
    rep_name         VARCHAR(100),
    product_id       VARCHAR(50),
    product_name     VARCHAR(200),
    target_volume    DECIMAL(12,2),
    actual_volume    DECIMAL(12,2),
    achievement_rate DECIMAL(6,2),
    incremental_sales DECIMAL(14,2),
    incremental_rx  DECIMAL(12,2),
    market_share_gain DECIMAL(6,2),
    awareness_rate   DECIMAL(6,2),
    consideration_rate DECIMAL(6,2),
    trial_rate       DECIMAL(6,2),
    conversion_rate  DECIMAL(6,2),
    cost_per_rx      DECIMAL(10,2),
    cost_per_conversion DECIMAL(10,2),
    roi_ratio        DECIMAL(6,2),
    qualitative_feedback TEXT,
    lessons_learned  TEXT,
    next_campaign_recommendations TEXT,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE fct_commission_detail (
    commission_id    VARCHAR(50) PRIMARY KEY,
    rep_id           VARCHAR(50) NOT NULL,
    rep_name         VARCHAR(100),
    manager_id       VARCHAR(50),
    manager_name     VARCHAR(100),
    territory_id     VARCHAR(50),
    territory_name   VARCHAR(100),
    product_id       VARCHAR(50),
    product_name     VARCHAR(200),
    period_type      VARCHAR(20) NOT NULL,
    period_value     VARCHAR(20) NOT NULL,
    transaction_type VARCHAR(30),   -- sales/return/adjustment
    transaction_id   VARCHAR(50),
    transaction_date DATE,
    sales_amount     DECIMAL(14,2),
    sales_volume     DECIMAL(10,2),
    target_amount    DECIMAL(14,2),
    achievement_rate DECIMAL(6,2),
    commission_rate  DECIMAL(8,4),
    commission_amount DECIMAL(12,2),
    accelerator_applied TINYINT(1) DEFAULT 0,
    accelerator_amount  DECIMAL(12,2),
    quality_adjustment DECIMAL(10,2),  -- 合规/满意度调整
    final_payout     DECIMAL(12,2),
    payout_status     VARCHAR(20) DEFAULT 'pending', -- pending/approved/paid
    approved_by      VARCHAR(50),
    approved_at      DATETIME,
    paid_date        DATE,
    notes            TEXT,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fct_competitive_intelligence (
    intel_id         VARCHAR(50) PRIMARY KEY,
    competitor_product_id VARCHAR(50) NOT NULL,
    competitor_product_name VARCHAR(200) NOT NULL,
    competitor_company VARCHAR(100),
    product_id       VARCHAR(50),
    our_product_name VARCHAR(200),
    intel_type       VARCHAR(50) NOT NULL,  -- pricing/promotion/pipeline/access/strategy
    intel_source     VARCHAR(100),
    region           VARCHAR(50),
    hospital_id      VARCHAR(50),
    hospital_name    VARCHAR(200),
    intelligence_date DATE NOT NULL,
    title            VARCHAR(200),
    content          TEXT,
    impact_assessment VARCHAR(30), -- high/medium/low
    strategic_response TEXT,
    action_required  TINYINT(1) DEFAULT 0,
    action_deadline  DATE,
    assigned_to      VARCHAR(50),
    status           VARCHAR(20) DEFAULT 'active',
    confidence_level VARCHAR(20),   -- confirmed/probable/possible
    related_events   TEXT,
    tags             TEXT,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by       VARCHAR(50),
    updated_at       DATETIME
);

CREATE TABLE fct_complaint_feedback (
    complaint_id    VARCHAR(50) PRIMARY KEY,
    complaint_type  VARCHAR(50) NOT NULL,  -- product/ service/compliance/quality
    source          VARCHAR(50),            -- doctor/patient/hospital/rep/internal
    source_id       VARCHAR(50),
    source_name     VARCHAR(100),
    hospital_id     VARCHAR(50),
    hospital_name   VARCHAR(200),
    product_id      VARCHAR(50),
    product_name   VARCHAR(200),
    complaint_date  DATE NOT NULL,
    complaint_detail TEXT,
    severity        VARCHAR(20),
    status          VARCHAR(20) DEFAULT 'open', -- open/investigating/resolved/closed
    assigned_to     VARCHAR(50),
    assigned_date   DATE,
    resolution_date DATE,
    resolution_detail TEXT,
    customer_satisfaction DECIMAL(3,2),
    related_expense DECIMAL(12,2),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME
);

CREATE TABLE fct_compliance_violations (
    violation_id          VARCHAR(50) PRIMARY KEY,
    rule_id               VARCHAR(50) NOT NULL,
    violation_type        VARCHAR(50) NOT NULL,
    entity_type           VARCHAR(30) NOT NULL, -- rep/doctor/hospital/activity
    entity_id             VARCHAR(50) NOT NULL,
    entity_name           VARCHAR(200),
    period_type           VARCHAR(20),
    period_value          VARCHAR(20),
    province              VARCHAR(50),
    city                  VARCHAR(50),
    territory_id          VARCHAR(50),
    territory_name        VARCHAR(100),
    product_id            VARCHAR(50),
    product_name          VARCHAR(200),
    activity_id           VARCHAR(50),
    activity_name         VARCHAR(200),
    violation_date        DATE NOT NULL,
    detected_date         DATE NOT NULL,
    detection_method      VARCHAR(30), -- auto/manual/audit/complaint
    violation_detail      TEXT,
    evidence_urls         TEXT,        -- JSON array of evidence
    amount_involved       DECIMAL(14,2),
    participants_count    INT,
   违规严重程度            VARCHAR(20),
    status                VARCHAR(20) DEFAULT 'open', -- open/investigating/resolved/closed
    investigation_outcome TEXT,
    action_taken          VARCHAR(200),
    resolved_date         DATE,
    resolved_by           VARCHAR(50),
    penalty_decision      VARCHAR(200),
    penalty_amount        DECIMAL(12,2),
    related_violation_ids TEXT,        -- JSON array for linked violations
    notes                 TEXT,
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by            VARCHAR(50)
);

CREATE TABLE fct_conclusions (
    conclusion_id      VARCHAR(50) PRIMARY KEY,
    conclusion_type    VARCHAR(50),
    subject            VARCHAR(200),
    entity_type        VARCHAR(30),
    entity_id          VARCHAR(50),
    entity_name        VARCHAR(100),
    analysis_text      TEXT,
    confidence_score   DECIMAL(5,4),
    related_event_ids  TEXT,
    reasoning_chain    TEXT,
    contributing_factors TEXT,
    inference_method   VARCHAR(50),
    llm_model          VARCHAR(50),
    tags               TEXT,
    status             VARCHAR(20) DEFAULT 'active',
    created_at         DATETIME,
    updated_at         DATETIME
);

CREATE TABLE fct_data_quality (
    dq_id           VARCHAR(50) PRIMARY KEY,
    check_type      VARCHAR(50) NOT NULL,   -- completeness/accuracy/timeliness/consistency
    entity_type     VARCHAR(50),
    entity_id       VARCHAR(50),
    check_date      DATE NOT NULL,
    period_covered  VARCHAR(20),
    total_records   INT,
    valid_records   INT,
    invalid_records INT,
    quality_score   DECIMAL(5,2),           -- 0-100
    completeness    DECIMAL(6,2),           -- %
    accuracy        DECIMAL(6,2),
    timeliness      DECIMAL(6,2),
    consistency     DECIMAL(6,2),
    issues_found    TEXT,                   -- JSON array
    issue_details   TEXT,
    root_cause      TEXT,
    remediation_actions TEXT,
    resolved_date   DATE,
    resolved_by     VARCHAR(50),
    data_source     VARCHAR(100),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fct_distribution (
    distribution_id VARCHAR(50) PRIMARY KEY,
    product_id     VARCHAR(50),
    distributor_id  VARCHAR(50),
    hospital_id     VARCHAR(50),
    order_date      DATE,
    delivery_date   DATE,
    quantity        DECIMAL(12,2),
    unit_price      DECIMAL(10,2),
    total_amount    DECIMAL(16,2),
    batch_no        VARCHAR(50),
    expiry_date     DATE,
    invoice_no      VARCHAR(100),
    payment_status  VARCHAR(20),
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME
);

CREATE TABLE fct_events (
    event_id         VARCHAR(50) PRIMARY KEY,
    event_type       VARCHAR(50),
    event_name       VARCHAR(200),
    entity_type      VARCHAR(30),
    entity_id        VARCHAR(50),
    event_date       DATE,
    description      TEXT,
    impact_level     VARCHAR(20),
    related_products TEXT,
    related_doctors  TEXT,
    status           VARCHAR(20) DEFAULT 'active',
    created_at       DATETIME
);

CREATE TABLE fct_expense_c1 (
    expense_id         VARCHAR(50) PRIMARY KEY,
    rep_id             VARCHAR(50),
    rep_name           VARCHAR(100),
    hospital_id        VARCHAR(50),
    hospital_name      VARCHAR(200),
    product_id         VARCHAR(50),
    activity_type      VARCHAR(50),
    activity_name      VARCHAR(200),
    event_date         DATE,
    venue              VARCHAR(200),
    attendee_count     INT,
    doctor_count       INT,
    total_amount       DECIMAL(12,2),
    cost_per_person    DECIMAL(10,2),
    speaker_fee        DECIMAL(12,2),
    venue_fee          DECIMAL(12,2),
    materials_cost     DECIMAL(12,2),
    meal_cost          DECIMAL(12,2),
    travel_cost        DECIMAL(12,2),
    other_cost         DECIMAL(12,2),
    receipt_url        VARCHAR(500),
    compliance_check   VARCHAR(50),
    approval_status    VARCHAR(30) DEFAULT 'pending',
    approved_by        VARCHAR(100),
    approved_at        DATETIME,
    status             VARCHAR(20) DEFAULT 'active',
    created_at         DATETIME
);

CREATE TABLE fct_expense_c2 (
    expense_id         VARCHAR(50) PRIMARY KEY,
    rep_id             VARCHAR(50),
    rep_name           VARCHAR(100),
    hospital_id        VARCHAR(50),
    hospital_name      VARCHAR(200),
    product_id         VARCHAR(50),
    expense_type       VARCHAR(50),
    expense_date       DATE,
    amount             DECIMAL(12,2),
    category           VARCHAR(50),
    sub_category       VARCHAR(50),
    description        TEXT,
    vendor             VARCHAR(200),
    receipt_no         VARCHAR(100),
    receipt_url        VARCHAR(500),
    invoice_type       VARCHAR(30),
    tax_rate           DECIMAL(5,4),
    tax_amount         DECIMAL(12,2),
    compliance_check   VARCHAR(50),
    approval_status    VARCHAR(30) DEFAULT 'pending',
    approved_by        VARCHAR(100),
    approved_at        DATETIME,
    status             VARCHAR(20) DEFAULT 'active',
    created_at         DATETIME
);

CREATE TABLE fct_expense_c3 (
    expense_id              VARCHAR(50) PRIMARY KEY,
    rep_id                  VARCHAR(50),
    rep_name                VARCHAR(100),
    hospital_id             VARCHAR(50),
    hospital_name           VARCHAR(200),
    product_id              VARCHAR(50),
    travel_type             VARCHAR(50),
    travel_date             DATE,
    origin                  VARCHAR(100),
    destination             VARCHAR(100),
    transportation          VARCHAR(50),
    ticket_cost             DECIMAL(10,2),
    accommodation_cost      DECIMAL(10,2),
    daily_allowance         DECIMAL(10,2),
    other_costs             DECIMAL(10,2),
    total_cost              DECIMAL(12,2),
    receipt_url             VARCHAR(500),
    compliance_check        VARCHAR(50),
    approval_status         VARCHAR(30) DEFAULT 'pending',
    approved_by             VARCHAR(100),
    approved_at             DATETIME,
    status                  VARCHAR(20) DEFAULT 'active',
    created_at              DATETIME
);

CREATE TABLE fct_expense_reconciliation (
    recon_id         VARCHAR(50) PRIMARY KEY,
    expense_id       VARCHAR(50) NOT NULL,
    rep_id           VARCHAR(50) NOT NULL,
    rep_name         VARCHAR(100),
    manager_id       VARCHAR(50),
    manager_name     VARCHAR(100),
    province         VARCHAR(50),
    period_value     VARCHAR(20),
    expense_type     VARCHAR(50),
    expense_category VARCHAR(50),
    amount_claimed   DECIMAL(12,2),
    amount_approved  DECIMAL(12,2),
    amount_rejected  DECIMAL(12,2),
    rejection_reason TEXT,
    receipt_count    INT,
    receipt_amount   DECIMAL(12,2),
    supporting_docs  TEXT,                  -- JSON array of doc URLs
    standard_amount  DECIMAL(10,2),
    variance_amount  DECIMAL(12,2),
    variance_rate    DECIMAL(6,2),
    compliance_check  VARCHAR(30),
    compliance_issues TEXT,
    tax处理          VARCHAR(30),
    tax_amount       DECIMAL(10,2),
    recon_status     VARCHAR(20) DEFAULT 'pending', -- pending/approved/rejected/adjusted
    submitted_date   DATE,
    reviewed_date    DATE,
    reviewed_by     VARCHAR(50),
    final_approved_by VARCHAR(50),
    final_approved_at DATETIME,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes            TEXT
);

CREATE TABLE fct_incentive_plan (
    plan_id          VARCHAR(50) PRIMARY KEY,
    plan_name        VARCHAR(200) NOT NULL,
    plan_type        VARCHAR(50) NOT NULL,  -- sales/incentive/spiff/override
    product_id       VARCHAR(50),
    product_name     VARCHAR(200),
    territory_id     VARCHAR(50),
    effective_year   INT NOT NULL,
    effective_quarter VARCHAR(10),
    target_metric    VARCHAR(50),           -- sales/volume/market_share
    target_value     DECIMAL(14,2),
    target_unit      VARCHAR(20),
    payout_model     VARCHAR(30),           -- linear/stepped/capped
    payout_rate      DECIMAL(8,4),          -- 每单位提成
    accelerator_rate DECIMAL(5,2),          -- 加速系数（超量部分）
    accelerator_threshold DECIMAL(14,2),
    cap_amount       DECIMAL(14,2),
    floor_amount     DECIMAL(14,2),
    qualifiers       TEXT,                  -- JSON: 资质条件
    conditions       TEXT,                  -- JSON: 额外条件
    status           VARCHAR(20) DEFAULT 'active',
    approved_by      VARCHAR(50),
    approved_at      DATETIME,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by       VARCHAR(50),
    updated_at       DATETIME
);

CREATE TABLE fct_inventory (
    inventory_id   VARCHAR(50) PRIMARY KEY,
    product_id     VARCHAR(50),
    distributor_id VARCHAR(50),
    warehouse_id   VARCHAR(50),
    quantity       DECIMAL(12,2),
    unit_cost      DECIMAL(10,2),
    total_value    DECIMAL(16,2),
    batch_no       VARCHAR(50),
    expiry_date    DATE,
    inventory_date DATE,
    turnover_days  INT,
    status         VARCHAR(20) DEFAULT 'active',
    created_at     DATETIME
);

CREATE TABLE fct_kol_interaction (
    interaction_id   VARCHAR(50) PRIMARY KEY,
    kol_id            VARCHAR(50) NOT NULL,
    doctor_id         VARCHAR(50),
    doctor_name       VARCHAR(100),
    interaction_type  VARCHAR(50) NOT NULL,  -- meeting/speech/advisory/consultation
    activity_id       VARCHAR(50),
    activity_name     VARCHAR(200),
    rep_id            VARCHAR(50),
    rep_name          VARCHAR(100),
    interaction_date  DATE NOT NULL,
    interaction_place VARCHAR(200),
    duration_minutes  INT,
    topics            TEXT,                   -- JSON array
    kol_opinions      TEXT,
    agreements        TEXT,                   -- JSON array
    disagreements     TEXT,
    action_items      TEXT,
    follow_up_required TINYINT(1) DEFAULT 0,
    follow_up_date    DATE,
    cost              DECIMAL(12,2),
    outcome           VARCHAR(50),
    participant_count INT,
    satisfaction_score DECIMAL(5,2),
    impact_level      VARCHAR(20),
    created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME
);

CREATE TABLE fct_meeting_minutes (
    minutes_id    VARCHAR(50) PRIMARY KEY,
    meeting_type  VARCHAR(50),
    topic         VARCHAR(200),
    attendees     TEXT,
    meeting_date  DATE,
    venue         VARCHAR(200),
    content       TEXT,
    decisions     TEXT,
    action_items  TEXT,
    status        VARCHAR(20) DEFAULT 'active',
    created_at    DATETIME
);

CREATE TABLE fct_patient_enrollment (
    enrollment_id      VARCHAR(50) PRIMARY KEY,
    program_id         VARCHAR(50),
    patient_id         VARCHAR(50),
    doctor_id          VARCHAR(50),
    hospital_id        VARCHAR(50),
    enrollment_date    DATE,
    disease_type       VARCHAR(100),
    medication         VARCHAR(100),
    follow_up_count    INT,
    last_follow_up_date DATE,
    status             VARCHAR(20) DEFAULT 'active',
    created_at         DATETIME
);

CREATE TABLE fct_patient_program (
    program_id      VARCHAR(50) PRIMARY KEY,
    program_name    VARCHAR(200) NOT NULL,
    program_type    VARCHAR(50) NOT NULL,   -- compliance/patient_support/disease_management
    product_id      VARCHAR(50),
    product_name   VARCHAR(200),
    target_disease  VARCHAR(100),
    target_patient_segment VARCHAR(50),
    eligibility_criteria TEXT,
    enrollment_start DATE,
    enrollment_end   DATE,
    program_duration INT,       -- 天数
    total_patient_target INT,
    total_patients_enrolled INT,
    active_patients   INT,
    completed_patients INT,
    dropout_patients  INT,
    dropout_rate     DECIMAL(6,2),
    program_cost_total DECIMAL(14,2),
    cost_per_patient  DECIMAL(10,2),
    support_services  TEXT,    -- JSON array of service types
    intervention_type VARCHAR(50),
    outcome_metrics   TEXT,    -- JSON: adherence/complication/satisfaction
    outcome_summary   TEXT,
    monthly_tracking  TEXT,    -- JSON: monthly enrollment data
    created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME
);

CREATE TABLE fct_pdca_plan (
    pdca_id       VARCHAR(50) PRIMARY KEY,
    plan_id       VARCHAR(50),
    period        VARCHAR(20),
    check_date    DATE,
    plan_value    DECIMAL(16,2),
    do_value      DECIMAL(16,2),
    check_gap     DECIMAL(16,2),
    action_plan   TEXT,
    owner         VARCHAR(50),
    status        VARCHAR(20) DEFAULT 'active',
    created_at    DATETIME
);

CREATE TABLE fct_pnl (
    pnl_id        VARCHAR(50) PRIMARY KEY,
    period        VARCHAR(20),
    product_id    VARCHAR(50),
    region        VARCHAR(50),
    revenue       DECIMAL(16,2),
    cogs          DECIMAL(16,2),
    gross_profit DECIMAL(16,2),
    sga          DECIMAL(16,2),
    rd_expense   DECIMAL(16,2),
    net_profit   DECIMAL(16,2),
    gp_margin    DECIMAL(6,4),
    np_margin    DECIMAL(6,4),
    status       VARCHAR(20) DEFAULT 'active',
    created_at   DATETIME
);

CREATE TABLE fct_prescription_capacity (
    capacity_id     VARCHAR(50) PRIMARY KEY,
    doctor_id        VARCHAR(50) NOT NULL,
    doctor_name      VARCHAR(100),
    hospital_id      VARCHAR(50),
    hospital_name    VARCHAR(200),
    province         VARCHAR(50),
    product_id       VARCHAR(50),
    product_name    VARCHAR(200),
    evaluation_date  DATE NOT NULL,
    prescription_capacity_score DECIMAL(5,2),  -- 0-100
    prescription_level  VARCHAR(20),        
    current_rx_volume  DECIMAL(12,2),
    max_rx_capacity     DECIMAL(12,2),
    utilization_rate    DECIMAL(6,2),
    rx_growth_rate      DECIMAL(8,4),
    patient_pool_size   INT,
    patient_growth_rate DECIMAL(8,4),
    diagnosis_accuracy  DECIMAL(5,2),
    treatment_guideline_adherence DECIMAL(6,2),
    competitive_pressure VARCHAR(20),
    opportunity_gaps    TEXT,
    growth_recommendations TEXT,
    priority_score      DECIMAL(5,2),
    status              VARCHAR(20) DEFAULT 'active',
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME
);

CREATE TABLE fct_prescription_flow (
    flow_id                VARCHAR(50) PRIMARY KEY,
    product_id             VARCHAR(50),
    doctor_id              VARCHAR(50),
    hospital_id            VARCHAR(50),
    prescription_month     VARCHAR(7),
    prescription_volume    DECIMAL(12,2),
    prescription_amount    DECIMAL(16,2),
    patient_count          INT,
    avg_dosage             DECIMAL(10,2),
    new_patient_count      INT,
    repeat_patient_count   INT,
    status                 VARCHAR(20) DEFAULT 'active',
    created_at             DATETIME
);

CREATE TABLE fct_pricing_analysis (
    price_id         VARCHAR(50) PRIMARY KEY,
    product_id       VARCHAR(50) NOT NULL,
    product_name    VARCHAR(200) NOT NULL,
    hospital_id      VARCHAR(50),
    hospital_name    VARCHAR(200),
    province         VARCHAR(50),
    city             VARCHAR(50),
    price_type       VARCHAR(50) NOT NULL,  -- retail/contract/tender/vbp/reimbursement
    current_price    DECIMAL(10,4) NOT NULL,
    price_unit       VARCHAR(20),
    price_effective_date DATE,
    previous_price   DECIMAL(10,4),
    price_change     DECIMAL(10,4),
    price_change_pct DECIMAL(6,2),
    reimbursement_price DECIMAL(10,4),
    reimbursement_rate DECIMAL(5,4),
    patient_out_of_pocket DECIMAL(10,2),
    vs_local_avg     DECIMAL(6,2),          -- vs 全国均价 %
    vs_competitor    DECIMAL(6,2),          -- vs 竞品 %
    price_elasticity_index DECIMAL(6,2),
    affordability_index DECIMAL(6,2),
    market_price_band VARCHAR(20),
    period_value     VARCHAR(20),
    data_source      VARCHAR(100),
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE fct_procurement_flow (
    flow_id              VARCHAR(50) PRIMARY KEY,
    product_id           VARCHAR(50),
    hospital_id          VARCHAR(50),
    procurement_month    VARCHAR(7),
    procurement_volume   DECIMAL(12,2),
    procurement_amount   DECIMAL(16,2),
    avg_price            DECIMAL(10,2),
    stock_level          DECIMAL(12,2),
    consumption_rate     DECIMAL(6,4),
    status               VARCHAR(20) DEFAULT 'active',
    created_at           DATETIME
);

CREATE TABLE fct_product_plan (
    plan_id               VARCHAR(50) PRIMARY KEY,
    product_id            VARCHAR(50),
    period                VARCHAR(20),
    target_sales          DECIMAL(16,2),
    actual_sales          DECIMAL(16,2),
    achievement           DECIMAL(6,4),
    target_market_share   DECIMAL(5,4),
    actual_market_share   DECIMAL(5,4),
    status                VARCHAR(20) DEFAULT 'active',
    created_at            DATETIME
);

CREATE TABLE fct_rep_activity_score (
    score_id        VARCHAR(50) PRIMARY KEY,
    rep_id          VARCHAR(50) NOT NULL,
    rep_name        VARCHAR(100),
    territory_id    VARCHAR(50),
    territory_name  VARCHAR(100),
    province        VARCHAR(50),
    period_type     VARCHAR(20) NOT NULL,
    period_value    VARCHAR(20) NOT NULL,
    product_id      VARCHAR(50),
    product_name    VARCHAR(200),
    -- 覆盖维度
    coverage_score  DECIMAL(6,2),           -- 医院覆盖
    coverage_target INT,
    coverage_actual INT,
    coverage_rate   DECIMAL(6,2),
    -- 拜访维度
    visit_score     DECIMAL(6,2),
    visit_target    INT,
    visit_actual    INT,
    visit_rate      DECIMAL(6,2),
    visit_quality_score DECIMAL(6,2),
    -- 学术维度
    academic_score  DECIMAL(6,2),
    academic_activities INT,
    kol_interactions INT,
    -- 合规维度
    compliance_score DECIMAL(6,2),
    compliance_rate DECIMAL(6,2),
    -- 综合
    total_score     DECIMAL(8,2),
    rank_in_region  INT,
    rank_nationally  INT,
    tier            VARCHAR(20),
    kpi_status      VARCHAR(20),            -- on_track/at_risk/off_track
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE fct_rep_contribution (
    contribution_id    VARCHAR(50) PRIMARY KEY,
    rep_id             VARCHAR(50),
    product_id         VARCHAR(50),
    period             VARCHAR(20),
    contribution_rate  DECIMAL(6,4),
    attributed_sales   DECIMAL(16,2),
    status             VARCHAR(20) DEFAULT 'active',
    created_at         DATETIME
);

CREATE TABLE fct_reports (
    report_id    VARCHAR(50) PRIMARY KEY,
    report_type  VARCHAR(50),
    report_name  VARCHAR(200),
    period       VARCHAR(20),
    author_id    VARCHAR(50),
    author_name  VARCHAR(100),
    content      TEXT,
    summary      TEXT,
    status       VARCHAR(20) DEFAULT 'active',
    created_at   DATETIME,
    updated_at   DATETIME
);

CREATE TABLE fct_roi_analysis (
    roi_id                    VARCHAR(50) PRIMARY KEY,
    rep_id                    VARCHAR(50),
    product_id                VARCHAR(50),
    period                    VARCHAR(20),
    investment_amount         DECIMAL(16,2),
    sales_amount              DECIMAL(16,2),
    gross_profit              DECIMAL(16,2),
    roi_ratio                 DECIMAL(8,4),
    roi_level                 VARCHAR(20),
    cost_per_doctor           DECIMAL(10,2),
    cost_per_visit            DECIMAL(10,2),
    sales_per_representative  DECIMAL(16,2),
    payback_months            DECIMAL(6,2),
    status                    VARCHAR(20) DEFAULT 'active',
    created_at                DATETIME
);

CREATE TABLE fct_rws_data (
    data_id            VARCHAR(50) PRIMARY KEY,
    study_id           VARCHAR(50),
    patient_id         VARCHAR(50),
    visit_date         DATE,
    visit_window       VARCHAR(20),
    efficacy_indicator TEXT,
    safety_indicator  TEXT,
    lab_result         TEXT,
    notes              TEXT,
    status             VARCHAR(20) DEFAULT 'active',
    created_at         DATETIME
);

CREATE TABLE fct_sales_forecast (
    forecast_id     VARCHAR(50) PRIMARY KEY,
    entity_type     VARCHAR(50) NOT NULL,  -- product/hospital/rep/territory
    entity_id       VARCHAR(50) NOT NULL,
    entity_name     VARCHAR(200),
    product_id      VARCHAR(50),
    product_name    VARCHAR(200),
    period_type     VARCHAR(20) NOT NULL,
    period_value    VARCHAR(20) NOT NULL,
    forecast_method VARCHAR(50),            -- moving_avg/linear_regression/arima/agent
    forecast_value  DECIMAL(16,2),
    forecast_volume DECIMAL(12,2),
    confidence_low  DECIMAL(16,2),
    confidence_high DECIMAL(16,2),
    confidence_level DECIMAL(5,2),
    actual_value    DECIMAL(16,2),
    accuracy_pct    DECIMAL(6,2),
    target_value    DECIMAL(16,2),
    target_achievement_rate DECIMAL(6,2),
    bias_pct        DECIMAL(6,2),
    contributing_factors TEXT,
    assumptions      TEXT,
    model_version    VARCHAR(20),
    model_params     TEXT,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE fct_speaker_program (
    program_id      VARCHAR(50) PRIMARY KEY,
    program_name    VARCHAR(200) NOT NULL,
    program_type    VARCHAR(50),           -- international/national/regional/local
    product_id      VARCHAR(50),
    product_name   VARCHAR(200),
    topic          VARCHAR(200),
    speaker_id     VARCHAR(50),
    speaker_name   VARCHAR(100),
    speaker_hospital VARCHAR(200),
    speaker_title  VARCHAR(100),
    audience_size  INT,
    audience_segment VARCHAR(50),
    event_date      DATE NOT NULL,
    event_location  VARCHAR(200),
    event_type     VARCHAR(50),           -- conference/symposium/seminar/webinar
    organizer      VARCHAR(100),
    organizer_type VARCHAR(30),           -- company/agency/third_party
    budget_approved DECIMAL(12,2),
    budget_spent   DECIMAL(12,2),
    speaker_fee    DECIMAL(12,2),
    travel_expense DECIMAL(10,2),
    satisfaction_score DECIMAL(5,2),
    feedback_summary TEXT,
    outcomes       TEXT,                   -- JSON: key outcomes
    created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME
);

CREATE TABLE fct_tender_contract (
    contract_id      VARCHAR(50) PRIMARY KEY,
    hospital_id      VARCHAR(50) NOT NULL,
    hospital_name    VARCHAR(200) NOT NULL,
    product_id       VARCHAR(50) NOT NULL,
    product_name    VARCHAR(200) NOT NULL,
    tender_batch     VARCHAR(100),
    contract_number  VARCHAR(100),
    bid_price        DECIMAL(10,4),
    winning_price    DECIMAL(10,4),
    price_reduction_rate DECIMAL(6,2),
    contract_volume  DECIMAL(12,2),
    delivered_volume DECIMAL(12,2),
    remaining_volume DECIMAL(12,2),
    fulfillment_rate DECIMAL(6,2),
    contract_start   DATE,
    contract_end     DATE,
    delivery_schedule TEXT,
    payment_terms    VARCHAR(100),
    payment_status   VARCHAR(20),   -- pending/partial/completed/overdue
    invoice_amount   DECIMAL(14,2),
    paid_amount      DECIMAL(14,2),
    outstanding_amount DECIMAL(14,2),
    status           VARCHAR(20) DEFAULT 'active',
    renewal_needed   TINYINT(1) DEFAULT 0,
    renewal_deadline DATE,
    notes            TEXT,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE fct_territory_assignment (
    assignment_id    VARCHAR(50) PRIMARY KEY,
    rep_id           VARCHAR(50) NOT NULL,
    rep_name         VARCHAR(100),
    territory_id     VARCHAR(50) NOT NULL,
    territory_name   VARCHAR(100),
    hospital_id      VARCHAR(50),
    hospital_name    VARCHAR(200),
    product_id       VARCHAR(50),
    product_name     VARCHAR(200),
    assignment_type  VARCHAR(30) NOT NULL,  -- new/transfer/coverage/add/remove
    effective_date   DATE NOT NULL,
    end_date         DATE,
    reason           VARCHAR(200),
    transfer_from    VARCHAR(50),           -- 前任代表ID
    transfer_to      VARCHAR(50),           -- 接收代表ID
    approved_by      VARCHAR(50),
    status           VARCHAR(20) DEFAULT 'active',
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes            TEXT
);

CREATE TABLE fct_territory_performance (
    perf_id         VARCHAR(50) PRIMARY KEY,
    region_id       VARCHAR(50),
    region_name     VARCHAR(100),
    zone_id         VARCHAR(50),
    zone_name       VARCHAR(100),
    province_id     VARCHAR(50),
    province_name   VARCHAR(100),
    territory_id    VARCHAR(50),
    territory_name  VARCHAR(100),
    period_type     VARCHAR(20) NOT NULL,
    period_value    VARCHAR(20) NOT NULL,
    product_id      VARCHAR(50),
    product_name    VARCHAR(200),
    sales_target    DECIMAL(16,2),
    sales_actual    DECIMAL(16,2),
    achievement_rate DECIMAL(6,2),
    yoy_growth      DECIMAL(8,4),
    market_share    DECIMAL(6,2),
    share_change    DECIMAL(6,2),
    hosp_count_target INT,
    hosp_count_actual INT,
    doctor_count_target INT,
    doctor_count_actual INT,
    visit_count_target INT,
    visit_count_actual INT,
    expense_budget  DECIMAL(14,2),
    expense_actual  DECIMAL(14,2),
    expense_rate    DECIMAL(6,2),
    roi             DECIMAL(6,2),
    quality_score   DECIMAL(6,2),
    red_flags       TEXT,                   -- JSON array
    yellow_flags    TEXT,
    overall_status  VARCHAR(20),            -- green/yellow/red
    rank_in_zone    INT,
    rank_in_region   INT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME
);

CREATE TABLE fct_territory_plan (
    plan_id          VARCHAR(50) PRIMARY KEY,
    territory_id     VARCHAR(50),
    period           VARCHAR(20),
    target_sales     DECIMAL(16,2),
    actual_sales     DECIMAL(16,2),
    achievement       DECIMAL(6,4),
    target_visits     INT,
    actual_visits     INT,
    status           VARCHAR(20) DEFAULT 'active',
    created_at        DATETIME
);

CREATE TABLE fct_traffic_light_status (
    tl_id         VARCHAR(50) PRIMARY KEY,
    entity_type   VARCHAR(30),
    entity_id     VARCHAR(50),
    period        VARCHAR(20),
    indicator     VARCHAR(50),
    actual_value  DECIMAL(12,2),
    target_value  DECIMAL(12,2),
    achievement   DECIMAL(6,4),
    traffic_light VARCHAR(10),
    trend         VARCHAR(20),
    last_updated  DATETIME,
    status        VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE fct_training (
    training_id     VARCHAR(50) PRIMARY KEY,
    training_name   VARCHAR(200) NOT NULL,
    training_type   VARCHAR(50) NOT NULL,   -- product/competency/compliance/onboarding
    training_mode   VARCHAR(30),  -- online/offline/hybrid
    target_audience VARCHAR(50),   -- rep/manager/director/all
    product_id      VARCHAR(50),
    product_name   VARCHAR(200),
    trainer_id      VARCHAR(50),
    trainer_name    VARCHAR(100),
    training_date   DATE NOT NULL,
    duration_hours  DECIMAL(5,2),
    location        VARCHAR(200),
    attendee_count  INT,
    attendee_ids    TEXT,          -- JSON array of rep_ids
    attendee_names  TEXT,
    completion_rate DECIMAL(6,2),
    pass_rate       DECIMAL(6,2),
    avg_score       DECIMAL(5,2),
    max_score       DECIMAL(5,2),
    content_modules  TEXT,          -- JSON array
    assessment_results TEXT,       -- JSON array of scores
    certificate_issued TINYINT(1) DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME
);

CREATE TABLE fct_visit_detail (
    visit_id         VARCHAR(50) PRIMARY KEY,
    rep_id           VARCHAR(50) NOT NULL,
    rep_name         VARCHAR(100),
    territory_id     VARCHAR(50),
    territory_name   VARCHAR(100),
    doctor_id        VARCHAR(50),
    doctor_name      VARCHAR(100),
    hospital_id      VARCHAR(50),
    hospital_name    VARCHAR(200),
    department       VARCHAR(100),
    province         VARCHAR(50),
    city             VARCHAR(50),
    product_id       VARCHAR(50),
    product_name     VARCHAR(200),
    visit_date       DATE NOT NULL,
    visit_time       VARCHAR(10),           -- 08:30
    visit_type       VARCHAR(30) NOT NULL,  -- in_patient/out_patient/rounds/phone/wechat
    visit_purpose    VARCHAR(50),           -- detailing/sampling/follow_up/education
    call_type        VARCHAR(30),           -- first_call/repeat_call/group_call
    duration_minutes INT,
    call_outcome     VARCHAR(50),           -- positive/negative/neutral/no_response
    call_response    VARCHAR(30),           -- 接受/拒绝/待跟进
    rx_intent        VARCHAR(20),  -- none
    rx_commitment    DECIMAL(10,2),         -- 处方承诺盒数
    topics_discussed TEXT,                  -- JSON array
    materials_used   TEXT,                  -- JSON array
    sample_given     DECIMAL(8,2),
    sample_value     DECIMAL(10,2),
    venue_type       VARCHAR(50),          -- hospital/clinic/online/other
    attendees_count  INT,
    key_feedback     TEXT,
    follow_up_action TEXT,
    next_visit_plan  DATE,
    kpi_credited     TINYINT(1) DEFAULT 0, -- 是否计入KPI
    compliance_flag  TINYINT(1) DEFAULT 0, -- 合规标识
    gps_latitude     DECIMAL(10,6),
    gps_longitude    DECIMAL(10,6),
    gps_address      VARCHAR(200),
    check_in_photo_url VARCHAR(300),
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE fct_visit_summary (
    summary_id       VARCHAR(50) PRIMARY KEY,
    rep_id           VARCHAR(50) NOT NULL,
    rep_name         VARCHAR(100),
    territory_id     VARCHAR(50),
    territory_name   VARCHAR(100),
    province         VARCHAR(50),
    product_id       VARCHAR(50),
    product_name     VARCHAR(200),
    period_type      VARCHAR(20) NOT NULL,  -- monthly/quarterly
    period_value     VARCHAR(20) NOT NULL,   -- 2026-05 / 2026-Q1
    target_visits    INT,
    actual_visits    INT,
    visit_achievement_rate DECIMAL(6,2),
    target_calls     INT,
    actual_calls     INT,
    call_achievement_rate DECIMAL(6,2),
    target_doctors   INT,
    active_doctors   INT,
    doctor_coverage_rate DECIMAL(6,2),
    avg_calls_per_day DECIMAL(5,2),
    avg_duration     DECIMAL(5,2),
    positive_rate    DECIMAL(5,2),         -- 正面反馈率
    negative_rate    DECIMAL(5,2),
    neutral_rate     DECIMAL(5,2),
    sample_cost      DECIMAL(12,2),
    activity_cost    DECIMAL(12,2),
    compliance_score DECIMAL(5,2),
    kpi_total_score  DECIMAL(8,2),
    rank_in_territory INT,
    rank_in_region   INT,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME
);

CREATE TABLE hospital_access (
    access_id            VARCHAR(50) PRIMARY KEY,
    hospital_id         VARCHAR(50),
    hospital_name       VARCHAR(200),
    product_id          VARCHAR(50),
    product_name        VARCHAR(200),
    access_type         VARCHAR(50),
    application_date    DATE,
    approval_date       DATE,
    access_status       VARCHAR(30),     -- approved/rejected/pending
    procurement_price   DECIMAL(12,2),
    procurement_volume  INT,
    contract_start      DATE,
    contract_end        DATE,
    tender_batch        VARCHAR(50),
    remarks             TEXT,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE hospitals (
    hospital_id           VARCHAR(50) PRIMARY KEY,
    hospital_name         VARCHAR(200) NOT NULL,
    level                 VARCHAR(20),     -- 三甲/三乙/二甲/二乙/社区
    type                  VARCHAR(50),     -- 综合/专科/中医/民营
    location              VARCHAR(100),    -- 省/市/区
    address               VARCHAR(300),
    bed_count             INT,
    department_count      INT,
    annual_revenue        DECIMAL(16,2),
    purchase_mode         VARCHAR(50),     -- 集中采购/招标/挂网
    access_status         VARCHAR(50),     -- 已准入/待准入/未准入
    access_date           DATE,
    contract_ratio        FLOAT,
    sales_ratio           FLOAT,
    vacancy_rate          FLOAT,
    consumption_progress  FLOAT,
    target_products       VARCHAR(1000),  -- JSON array
    actual_products       VARCHAR(1000),  -- JSON array
    key_departments       VARCHAR(500),    -- JSON array
    competitor_share       FLOAT,
    our_share             FLOAT,
    market_potential      DECIMAL(16,2),
    growth_opportunity    DECIMAL(16,2),
    overlapping_hospitals INT,
    flow_direction        VARCHAR(20),    -- inbound/outbound
    development_stage     VARCHAR(50),     -- negotiation/contracted/developing/established
    success_rate          FLOAT,
    resource_allocation   DECIMAL(16,2),
    timeline              VARCHAR(50),
    strategy_type         VARCHAR(50),     -- 学术引领/客情深度/覆盖广度
    territory             VARCHAR(100),
    status                VARCHAR(20) DEFAULT 'active',
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inference_results (
    result_id             VARCHAR(50) PRIMARY KEY,
    rule_id               VARCHAR(50),
    rule_name             VARCHAR(200),
    result_type           VARCHAR(50),
    source_entity_id      VARCHAR(50),
    target_entity_id     VARCHAR(50),
    inferred_link_type   VARCHAR(100),
    inferred_property    VARCHAR(100),
    inferred_value       TEXT,
    confidence            FLOAT,
    evidence              TEXT,
    valid_from            DATETIME,
    valid_to              DATETIME,
    status                VARCHAR(20) DEFAULT 'active',
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rule_id) REFERENCES inference_rules(rule_id)
);

CREATE TABLE inference_rules (
    rule_id               VARCHAR(50) PRIMARY KEY,
    name                  VARCHAR(200) NOT NULL,
    description           TEXT,
    rule_type             VARCHAR(30),     -- deduction/abduction/induction
    enabled               TINYINT(1) DEFAULT 1,
    priority              INT DEFAULT 0,
    ttl                   INT,
    auto_apply            TINYINT(1) DEFAULT 0,
    condition_pattern     VARCHAR(200),
    condition_filters     TEXT,
    condition_description TEXT,
    conclusion_type       VARCHAR(50),
    conclusion_source_pattern VARCHAR(100),
    conclusion_target_pattern VARCHAR(100),
    conclusion_link_type  VARCHAR(100),
    conclusion_strength_formula VARCHAR(200),
    conclusion_entity_pattern VARCHAR(100),
    conclusion_property   VARCHAR(100),
    conclusion_value_formula VARCHAR(200),
    conclusion_alert_type VARCHAR(100),
    conclusion_alert_message_template TEXT,
    conclusion_alert_severity VARCHAR(20),
    conclusion_tag_entity_pattern VARCHAR(100),
    conclusion_tag        VARCHAR(100),
    confidence_base       FLOAT,
    confidence_modifiers  TEXT,
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    author                VARCHAR(100),
    tags                  VARCHAR(500)
);

CREATE TABLE inventory (
    inventory_id           VARCHAR(50) PRIMARY KEY,
    product_id             VARCHAR(50),
    product_name           VARCHAR(200),
    hospital_id            VARCHAR(50),
    hospital_name          VARCHAR(200),
    batch_number           VARCHAR(50),
    quantity               INT,
    unit                   VARCHAR(20),
    warehouse_location     VARCHAR(100),
    stock_level            VARCHAR(20),    -- high/normal/low/critical
    safety_stock           INT,
    reorder_point          INT,
    last_replenishment_date DATE,
    expiration_date        DATE,
    status                 VARCHAR(20) DEFAULT 'active',
    updated_at             DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
);

CREATE TABLE labor_payments (
    payment_id         VARCHAR(50) PRIMARY KEY,
    payment_type       VARCHAR(50),
    total_persons      INT,
    total_amount       DECIMAL(16,2),
    payment_date       DATE,
    period             VARCHAR(20)
);

CREATE TABLE notifications (
    notification_id VARCHAR(50) PRIMARY KEY,
    user_id         VARCHAR(50),
    `type`            VARCHAR(50),
    title           VARCHAR(200) NOT NULL,
    message         TEXT,
    priority        VARCHAR(20),
    entity_id       VARCHAR(50),
    entity_type     VARCHAR(30),
    `read`            TINYINT(1) DEFAULT 0,
    `timestamp`       DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE object_links (
    link_id       INTEGER PRIMARY KEY AUTO_INCREMENT,
    source_type   VARCHAR(30) NOT NULL,
    source_id     VARCHAR(50) NOT NULL,
    source_name   VARCHAR(200),
    link_type     VARCHAR(50) NOT NULL,
    target_type   VARCHAR(30) NOT NULL,
    target_id     VARCHAR(50) NOT NULL,
    target_name   VARCHAR(200),
    link_strength FLOAT,                  -- 关系强度 0-1
    link_frequency VARCHAR(30),        
    link_volume   INT,
    confidence    FLOAT,
    valid_from    DATE,
    valid_to      DATE,
    provenance    VARCHAR(100),          -- 数据来源
    created_at     DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pdca_plans (
    pdca_id               VARCHAR(50) PRIMARY KEY,
    plan_type             VARCHAR(100),
    plan_content          TEXT,            -- P 阶段
    do_actions            TEXT,            -- D 阶段
    check_results         TEXT,            -- C 阶段
    act_improvements      TEXT,            -- A 阶段
    related_entity_type   VARCHAR(30),
    related_entity_id     VARCHAR(50),
    related_entity_name   VARCHAR(200),
    cycle_status          VARCHAR(30),     -- planning/doing/checking/acting
    cycle_start_date      DATE,
    cycle_end_date        DATE,
    owner                 VARCHAR(100),
    status                VARCHAR(20) DEFAULT 'active',
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE policies (
    policy_id             VARCHAR(50) PRIMARY KEY,
    policy_type           VARCHAR(50) NOT NULL, -- national_policy/local_policy/vbp_policy/medical_insurance等
    policy_name           VARCHAR(500) NOT NULL,
    issuing_authority     VARCHAR(200),
    document_number       VARCHAR(100),
    published_date        DATE,
    effective_date        DATE,
    applicable_scope      VARCHAR(200),
    applicable_regions    VARCHAR(500),
    applicable_products   VARCHAR(1000),   -- JSON array
    applicable_hospitals  VARCHAR(1000),  -- JSON array
    key_content           TEXT,
    impact_analysis       TEXT,
    compliance_requirements TEXT,
    related_policies      VARCHAR(500),    -- JSON array
    status                VARCHAR(20) DEFAULT 'active',
    version               VARCHAR(20),
    summary               TEXT,
    full_text_url         VARCHAR(500),
    tags                  VARCHAR(500),
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_flows (
    flow_id              VARCHAR(50) PRIMARY KEY,
    product_id           VARCHAR(50),
    product_name         VARCHAR(200),
    source_type          VARCHAR(50),    -- shipment/transfer/return
    source_id            VARCHAR(50),
    hospital_id          VARCHAR(50),
    hospital_name        VARCHAR(200),
    department           VARCHAR(100),
    flow_date            DATE,
    flow_quantity        INT,
    flow_value           DECIMAL(16,2),
    period_type          VARCHAR(20),    -- monthly/quarterly
    period_value         VARCHAR(20),    -- YYYY-MM / YYYY-QN
    month                VARCHAR(7),
    quarter              VARCHAR(10),
    `year`                 INT,
    distribution_channel VARCHAR(100),
    rep_id               VARCHAR(50),
    rep_name             VARCHAR(100),
    status               VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id),
    FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id)
);

CREATE TABLE products (
    product_id         VARCHAR(50)   PRIMARY KEY,
    product_name       VARCHAR(200)  NOT NULL,
    generic_name       VARCHAR(200),
    brand_name         VARCHAR(200),
    dosage_form        VARCHAR(100),
    spec               VARCHAR(100),
    manufacturer       VARCHAR(200),
    approval_number    VARCHAR(50),
    category           VARCHAR(100),
    therapeutic_area   VARCHAR(200),
    indications        TEXT,
    vbp_status         VARCHAR(50),   -- 未中选/中选/备选/非VBP
    vbp_price          DECIMAL(12,2),
    medical_insurance  TINYINT(1) DEFAULT 0,
    medical_insurance_type VARCHAR(20), -- 甲类/乙类/无
    reimbursement_rate FLOAT,
    market_status      VARCHAR(50) DEFAULT 'active', -- active/suspended/restricted
    launch_date        DATE,
    patent_expiry      DATE,
    competitive_intensity VARCHAR(20), -- high/medium/low
    strategic_importance VARCHAR(20),  -- core/potential/maintenance
    target_specialty   VARCHAR(500),
    target_patient_population BIGINT,
    current_market_share FLOAT,
    growth_rate        FLOAT,
    price              DECIMAL(12,2),
    status             VARCHAR(20) DEFAULT 'active',
    created_at         DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at         DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reminders (
    reminder_id     VARCHAR(50) PRIMARY KEY,
    user_id         VARCHAR(50),
    reminder_type   VARCHAR(50),  -- urgent/important/routine/predictive/opportunity
    title           VARCHAR(200) NOT NULL,
    description     TEXT,
    due_date        DATETIME,
    priority        VARCHAR(20),
    status          VARCHAR(20) DEFAULT 'active',
    entity_id       VARCHAR(50),
    entity_type     VARCHAR(30),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE reports (
    report_id             VARCHAR(50) PRIMARY KEY,
    report_type           VARCHAR(50) NOT NULL,
    report_category       VARCHAR(50),
    title                 VARCHAR(500) NOT NULL,
    summary               TEXT,
    content               TEXT,
    period_covered        VARCHAR(50),
    entity_type           VARCHAR(30),
    entity_id             VARCHAR(50),
    entity_name           VARCHAR(200),
    author                VARCHAR(100),
    review_status         VARCHAR(30),
    approved_by           VARCHAR(100),
    key_findings          TEXT,
    recommendations       TEXT,
    attachments           TEXT,            -- JSON array
    tags                  VARCHAR(500),
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales_flows (
    flow_id               VARCHAR(50) PRIMARY KEY,
    flow_type             VARCHAR(30),
    product_id            VARCHAR(50),
    product_name          VARCHAR(200),
    hospital_id           VARCHAR(50),
    hospital_name         VARCHAR(200),
    rep_id                VARCHAR(50),
    rep_name              VARCHAR(100),
    territory             VARCHAR(100),
    period_type           VARCHAR(20),
    period_value          VARCHAR(20),
    target_value          DECIMAL(16,2),
    actual_value          DECIMAL(16,2),
    achievement_rate      FLOAT,
    yoy_growth            FLOAT,
    mom_growth            FLOAT,
    volume                DECIMAL(16,2),
    amount                DECIMAL(16,2),
    status                VARCHAR(20) DEFAULT 'active',
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id),
    FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id)
);

CREATE TABLE sales_reps (
    rep_id                    VARCHAR(50) PRIMARY KEY,
    rep_name                  VARCHAR(100) NOT NULL,
    region                    VARCHAR(100),
    territory                 VARCHAR(100),
    position                  VARCHAR(50),   -- 代表/高级代表/主管/经理
    rank_level                VARCHAR(20),
    hire_date                 DATE,
    product_responsibilities  VARCHAR(500),  -- JSON array of product_ids
    hospital_ids              VARCHAR(1000),   -- JSON array of hospital_ids
    doctor_ids                VARCHAR(1000),  -- JSON array of doctor_ids
    performance_score         FLOAT,
    quota_achievement         FLOAT,
    ytd_sales                 DECIMAL(16,2),
    qtd_sales                 DECIMAL(16,2),
    visit_compliance_rate     FLOAT,
    kpi_metrics               TEXT,          -- JSON
    training_completed        TINYINT(1) DEFAULT 0,
    compliance_status         VARCHAR(30) DEFAULT 'compliant',
    status                    VARCHAR(20) DEFAULT 'active',
    created_at                DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at                DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales_targets (
    target_id             VARCHAR(50) PRIMARY KEY,
    target_type           VARCHAR(50),     -- revenue/volume/penetration
    dimension             VARCHAR(30),      -- product/hospital/rep/territory/doctor
    dimension_id          VARCHAR(50),
    dimension_name        VARCHAR(200),
    product_id            VARCHAR(50),
    product_name          VARCHAR(200),
    period_type           VARCHAR(20),
    period_value          VARCHAR(20),
    target_value          DECIMAL(16,2),
    actual_value          DECIMAL(16,2),
    forecast_value        DECIMAL(16,2),
    achievement_rate      FLOAT,
    yoy_growth            FLOAT,
    mom_growth            FLOAT,
    risk_level            VARCHAR(20),
    confidence_interval_low DECIMAL(16,2),
    confidence_interval_high DECIMAL(16,2),
    baseline_value        DECIMAL(16,2),
    delta                 FLOAT,
    status                VARCHAR(20) DEFAULT 'active',
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE time_series_data (
    series_id     INTEGER PRIMARY KEY AUTO_INCREMENT,
    entity_type   VARCHAR(30) NOT NULL,
    entity_id     VARCHAR(50) NOT NULL,
    entity_name   VARCHAR(200),
    series_name   VARCHAR(100) NOT NULL,  -- prescriptionVolume/visitFrequency/marketShare等
    `timestamp`     VARCHAR(20) NOT NULL,   -- YYYY-MM 或 YYYY-QN
    `value`         FLOAT NOT NULL,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE traffic_light_rules (
    rule_id               VARCHAR(50) PRIMARY KEY,
    dimension             VARCHAR(30),     -- product/hospital/rep/territory
    metric                VARCHAR(100),
    green_threshold       FLOAT,
    yellow_threshold      FLOAT,
    red_threshold         FLOAT,
    calculation_method   VARCHAR(100),
    period                VARCHAR(20),
    enabled               TINYINT(1) DEFAULT 1,
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    user_id         VARCHAR(50) PRIMARY KEY,
    username        VARCHAR(100) UNIQUE NOT NULL,
    password_hash   VARCHAR(200) NOT NULL,
    display_name    VARCHAR(100),
    role            VARCHAR(30),   -- admin/manager/rep/compliance/agent
    region          VARCHAR(100),
    territory       VARCHAR(100),
    status          VARCHAR(20) DEFAULT 'active',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login_at   DATETIME
);

