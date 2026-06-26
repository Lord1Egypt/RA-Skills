const fs = require('fs-extra');
const path = require('path');
const Handlebars = require('handlebars');

const PROPOSAL_TEMPLATE = '<!doctype html>\n<html lang="zh-CN">\n<head>\n  <meta charset="utf-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1" />\n  <title>{{client}} - {{product}}解决方案提案</title>\n  <style>\n    :root {\n      --brand: #2563eb;\n      --brand-dark: #1e3a8a;\n      --brand-soft: #dbeafe;\n      --accent: #f97316;\n      --ink: #111827;\n      --muted: #6b7280;\n      --line: #e5e7eb;\n      --bg: #f8fafc;\n      --card: #ffffff;\n      --success: #16a34a;\n    }\n    * { box-sizing: border-box; }\n    body {\n      margin: 0;\n      color: var(--ink);\n      background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 42%, #fff7ed 100%);\n      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;\n      line-height: 1.65;\n    }\n    .deck { max-width: 1120px; margin: 0 auto; padding: 32px 20px 88px; }\n    .hero {\n      position: relative;\n      overflow: hidden;\n      border-radius: 28px;\n      padding: 44px;\n      color: #fff;\n      background: radial-gradient(circle at 86% 18%, rgba(249,115,22,.85), transparent 26%), linear-gradient(135deg, var(--brand-dark), var(--brand));\n      box-shadow: 0 24px 70px rgba(30, 58, 138, .24);\n    }\n    .hero::after { content: ""; position: absolute; inset: auto -80px -120px auto; width: 360px; height: 360px; border-radius: 50%; background: rgba(255,255,255,.12); }\n    .eyebrow { margin: 0 0 12px; letter-spacing: .18em; text-transform: uppercase; opacity: .82; font-size: 13px; }\n    h1 { margin: 0; font-size: clamp(30px, 5vw, 56px); line-height: 1.08; }\n    .subtitle { max-width: 720px; margin: 18px 0 0; font-size: 18px; opacity: .92; }\n    .meta { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }\n    .pill { padding: 8px 13px; border-radius: 999px; background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.28); backdrop-filter: blur(8px); }\n    .nav {\n      position: sticky; top: 0; z-index: 10;\n      display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;\n      margin: 22px 0; padding: 12px; border-radius: 20px;\n      background: rgba(255,255,255,.86); backdrop-filter: blur(14px); box-shadow: 0 12px 35px rgba(15,23,42,.08);\n    }\n    .nav a { text-decoration: none; color: var(--brand-dark); font-weight: 700; text-align: center; padding: 12px; border-radius: 14px; }\n    .nav a:hover { background: var(--brand-soft); }\n    .page {\n      min-height: 720px;\n      margin: 22px 0;\n      padding: 36px;\n      border-radius: 26px;\n      background: var(--card);\n      box-shadow: 0 16px 48px rgba(15,23,42,.08);\n      page-break-after: always;\n    }\n    .page:last-of-type { page-break-after: auto; }\n    .page-head { display: flex; justify-content: space-between; gap: 18px; align-items: flex-start; border-bottom: 1px solid var(--line); padding-bottom: 18px; margin-bottom: 26px; }\n    .page-no { color: var(--accent); font-weight: 900; font-size: 14px; letter-spacing: .14em; }\n    h2 { margin: 4px 0 0; font-size: 32px; color: var(--brand-dark); }\n    h3 { margin: 26px 0 10px; font-size: 20px; color: #0f172a; }\n    .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }\n    .grid.two { grid-template-columns: repeat(2, 1fr); }\n    .card { padding: 18px; border: 1px solid var(--line); border-radius: 18px; background: linear-gradient(180deg, #fff, #f8fafc); }\n    .card strong { color: var(--brand-dark); }\n    ul { padding-left: 20px; margin: 8px 0 0; }\n    li { margin: 7px 0; }\n    table { width: 100%; border-collapse: collapse; margin-top: 14px; overflow: hidden; border-radius: 16px; }\n    th, td { padding: 13px 14px; text-align: left; border-bottom: 1px solid var(--line); vertical-align: top; }\n    th { background: var(--brand-soft); color: var(--brand-dark); }\n    .timeline { display: grid; gap: 14px; }\n    .phase { border-left: 5px solid var(--brand); padding: 16px 18px; border-radius: 14px; background: #f8fafc; }\n    .case { border: 1px solid var(--line); border-radius: 18px; padding: 18px; margin-top: 14px; }\n    .roi { display: grid; grid-template-columns: 1fr 2fr; gap: 18px; align-items: stretch; }\n    .metric { display: grid; place-items: center; text-align: center; border-radius: 22px; background: linear-gradient(135deg, var(--brand), var(--success)); color: #fff; padding: 24px; }\n    .metric b { display: block; font-size: 38px; line-height: 1; }\n    .footer-tip {\n      position: fixed; left: 0; right: 0; bottom: 0; z-index: 20;\n      padding: 14px 20px;\n      background: rgba(17,24,39,.94); color: #fff; text-align: center; font-weight: 700;\n      box-shadow: 0 -10px 30px rgba(15,23,42,.18);\n    }\n    .footer-tip span { color: #fed7aa; }\n    @media (max-width: 820px) { .hero, .page { padding: 24px; } .nav, .grid, .grid.two, .roi { grid-template-columns: 1fr; } .nav { position: static; } }\n    @media print { body { background: #fff; } .deck { padding: 0; max-width: none; } .nav, .footer-tip { display: none; } .hero, .page { box-shadow: none; border-radius: 0; } }\n  </style>\n</head>\n<body>\n  <main class="deck">\n    <section class="hero">\n      <p class="eyebrow">ToB Sales Proposal</p>\n      <h1>{{client}}<br>{{product}}解决方案</h1>\n      <p class="subtitle">基于{{industry}}行业洞察、客户痛点、案例经验与ROI模型生成的四模块提案页面。</p>\n      <div class="meta">\n        <span class="pill">提案日期：{{generatedAt}}</span>\n        <span class="pill">预算范围：{{budget}}</span>\n        <span class="pill">交付周期：{{timeline}}</span>\n        <span class="pill">输出格式：HTML</span>\n      </div>\n    </section>\n\n    <nav class="nav" aria-label="提案分页导航">\n      <a href="#page-1">01 痛点对齐</a>\n      <a href="#page-2">02 方案对齐</a>\n      <a href="#page-3">03 实施路径</a>\n      <a href="#page-4">04 ROI与案例</a>\n    </nav>\n\n    <section class="page" id="page-1">\n      <div class="page-head"><div><div class="page-no">PAGE 01 / 04</div><h2>痛点对齐：让客户觉得你懂他</h2></div></div>\n      <div class="grid two">\n        <div class="card"><strong>客户输入摘要</strong><ul><li>客户：{{client}}</li><li>行业：{{industry}}</li><li>目标方案：{{product}}</li>{{#if painpoints}}<li>明确痛点：{{painpoints}}</li>{{/if}}</ul></div>\n        <div class="card"><strong>行业趋势</strong><ul>{{#each industryInsight.trends}}<li>{{this}}</li>{{/each}}</ul></div>\n      </div>\n      <h3>行业共性挑战</h3>\n      <div class="grid">{{#each industryInsight.challenges}}<div class="card"><strong>{{name}}</strong><br>{{desc}}</div>{{/each}}</div>\n      {{#if painpoints}}<h3>客户特定痛点翻译</h3><ul>{{#each painTranslated}}<li><strong>{{pain}}</strong> → {{translation}}</li>{{/each}}</ul>{{/if}}\n      <h3>数字化机会</h3><ul>{{#each industryInsight.opportunities}}<li>{{this}}</li>{{/each}}</ul>\n    </section>\n\n    <section class="page" id="page-2">\n      <div class="page-head"><div><div class="page-no">PAGE 02 / 04</div><h2>方案对齐：为什么要选这个方案</h2></div></div>\n      <div class="card"><strong>方案核心</strong><h3>{{solution.core}}</h3><p>本方案专为{{client}}设计，结合{{industry}}行业最佳实践，优先解决高频、关键、能快速看到业务价值的问题。</p></div>\n      <h3>核心功能与客户价值</h3>\n      <div class="grid">{{#each solution.features}}<div class="card"><strong>{{name}}</strong><br>{{desc}}</div>{{/each}}</div>\n      <h3>方案价值</h3><p class="card">{{solution.value}}</p>\n      <table><thead><tr><th>能力维度</th><th>具体说明</th><th>客户价值</th></tr></thead><tbody><tr><td>行业咨询</td><td>结合{{industry}}行业经验做痛点拆解</td><td>减少试错</td></tr><tr><td>方案设计</td><td>从业务场景到系统能力映射</td><td>避免功能堆砌</td></tr><tr><td>系统集成</td><td>对接现有数据、流程与权限体系</td><td>保障落地</td></tr><tr><td>持续运维</td><td>上线后监控、复盘与优化</td><td>持续产生价值</td></tr></tbody></table>\n    </section>\n\n    <section class="page" id="page-3">\n      <div class="page-head"><div><div class="page-no">PAGE 03 / 04</div><h2>实施路径：消除落地恐惧</h2></div></div>\n      <div class="timeline">{{#each implementation.phases}}<div class="phase"><h3>{{name}}</h3><p><strong>时间安排：</strong>{{duration}}</p><ul>{{#each tasks}}<li>{{this}}</li>{{/each}}</ul></div>{{/each}}</div>\n      <h3>里程碑节点</h3>\n      <table><thead><tr><th>里程碑</th><th>交付物</th><th>验收标准</th></tr></thead><tbody><tr><td>需求确认</td><td>需求规格说明书</td><td>双方签字确认</td></tr><tr><td>设计完成</td><td>系统设计方案</td><td>评审通过</td></tr><tr><td>开发完成</td><td>测试版本系统</td><td>功能测试通过</td></tr><tr><td>上线交付</td><td>生产环境系统</td><td>验收测试通过</td></tr></tbody></table>\n      <h3>客户配合清单</h3><ul><li>提供业务流程、数据样例与现有系统接口说明</li><li>指定业务负责人、IT负责人、验收负责人</li><li>每周固定评审，减少返工和范围漂移</li></ul>\n    </section>\n\n    <section class="page" id="page-4">\n      <div class="page-head"><div><div class="page-no">PAGE 04 / 04</div><h2>承诺型 ROI 与成功案例</h2></div></div>\n      <div class="roi"><div class="metric"><span>三年 ROI</span><b>{{roi.threeYearROI}}</b><span>回收期 {{roi.paybackPeriod}}</span></div><div class="card"><strong>投资概算</strong><h3>{{roi.investment}}</h3><p>ROI 采用保守测算口径，优先呈现客户容易验证的收益项。</p><table><thead><tr><th>收益项</th><th>年收益</th><th>说明</th></tr></thead><tbody>{{#each roi.benefits}}<tr><td>{{item}}</td><td>{{value}}</td><td>{{desc}}</td></tr>{{/each}}</tbody></table></div></div>\n      <h3>匹配案例</h3>\n      {{#each cases}}<div class="case"><strong>{{name}}</strong><p>客户：{{client}} ｜ 行业：{{industry}} ｜ 解决方案：{{#each solutions}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}</p>{{#if keyResults}}<p><strong>关键成果：</strong>{{keyResults}}</p>{{/if}}{{#if key_learnings}}<ul>{{#each key_learnings}}<li>{{this}}</li>{{/each}}</ul>{{/if}}</div>{{/each}}\n      <h3>商务建议</h3><table><thead><tr><th>项目</th><th>建议</th></tr></thead><tbody><tr><td>付款条款</td><td>合同签订30% / 需求确认30% / 上线验收30% / 质保期满10%</td></tr><tr><td>质保承诺</td><td>12个月质保，2小时内响应，24小时内解决关键问题</td></tr></tbody></table>\n    </section>\n  </main>\n  <div class="footer-tip">提示：可复制本页面内容给 AI，生成 <span>PPT / Keynote / 路演稿</span>。</div>\n</body>\n</html>\n';

class ProposalGenerator {
  constructor(config) {
    this.config = config;
    this.dataDir = path.join(__dirname, '..', 'data');

    // 注册 Handlebars helpers
    Handlebars.registerHelper('split', function(str, delimiter) {
      return (str || '').split(delimiter);
    });
  }

  async generate() {
    if (typeof this.config.painpoints === 'string' && this.config.painpoints.trim() === '') {
      this.config.painpoints = undefined;
    }

    // 加载数据
    const cases = await this.loadCases();
    const methodologies = await this.loadMethodologies();
    
    // 匹配最佳案例
    const matchedCases = this.matchCases(cases);
    
    // 构建提案数据
    const proposalData = {
      ...this.config,
      generatedAt: new Date().toLocaleDateString('zh-CN'),
      cases: matchedCases,
      methodologies: methodologies,
      // 基于行业生成洞察
      industryInsight: this.generateIndustryInsight(),
      // 生成解决方案
      solution: this.generateSolution(),
      // 生成实施计划
      implementation: this.generateImplementationPlan(),
      // 生成ROI分析
      roi: this.generateROI(),
      // 带差异化的痛点翻译
      painTranslated: this.translatePainpoints(this.config.painpoints)
    };

    // 渲染内联 HTML 模板（SkillHub 不允许上传 .hbs 文件）
    const template = Handlebars.compile(PROPOSAL_TEMPLATE);
    
    return template(proposalData);
  }

  async loadCases() {
    try {
      const casesPath = path.join(this.dataDir, 'cases.json');
      const data = await fs.readJson(casesPath);
      return data.cases || [];
    } catch (error) {
      console.warn('警告: 无法加载案例库，使用默认案例');
      return this.getDefaultCases();
    }
  }

  async loadMethodologies() {
    try {
      const methodsPath = path.join(this.dataDir, 'methodologies.json');
      const data = await fs.readJson(methodsPath);
      return data.frameworks || [];
    } catch (error) {
      return [];
    }
  }

  matchCases(cases) {
    // 基于行业匹配最佳案例
    const industry = this.config.industry;
    const matched = cases.filter(c => {
      // 行业匹配
      if (c.industry && c.industry.includes(industry)) return true;
      // 关键词匹配
      if (this.config.painpoints) {
        const pains = this.config.painpoints.split(',').map(p => p.trim()).filter(Boolean);
        return pains.some(pain => 
          JSON.stringify(c).includes(pain)
        );
      }
      return false;
    });

    // 返回前3个最匹配的
    return matched.slice(0, 3).length > 0 ? matched.slice(0, 3) : cases.slice(0, 2);
  }

  generateIndustryInsight() {
    const insights = {
      '金融': {
        trends: ['数字化转型加速', '监管科技兴起', '客户体验升级'],
        challenges: [
          { name: '数据孤岛严重', desc: '各部门系统烟囱式建设，数据标准和接口不统一，跨部门协同困难，风控模型只能看到局部视角' },
          { name: '合规成本高', desc: '监管要求频繁更新，人工合规审查效率低，一旦违规面临巨额罚款和声誉损失风险' },
          { name: '系统老化', desc: '核心系统多为传统架构，迭代周期以月为单位，无法支持业务敏捷创新与秒级响应' }
        ],
        opportunities: ['智能风控', '精准营销', '流程自动化']
      },
      '零售': {
        trends: ['全渠道融合', '私域运营', '供应链数字化'],
        challenges: [
          { name: '获客成本高', desc: '公域流量红利见顶，单客获取成本三年翻倍，传统促销手段ROI持续走低' },
          { name: '库存管理难', desc: '线上线下渠道库存割裂，畅销品断货与滞销品积压并存，库存周转率低于行业均值' },
          { name: '客户留存低', desc: '会员体系缺乏差异化运营，复购率不足20%，私域转化链路存在明显断裂' }
        ],
        opportunities: ['智能选品', '会员运营', '供应链协同']
      },
      '制造': {
        trends: ['工业4.0', '智能制造', '绿色生产'],
        challenges: [
          { name: '生产效率低', desc: '设备综合效率(OEE)长期低于70%，产线换型时间长，人工排产难以应对多品种小批量需求' },
          { name: '质量管控难', desc: '依赖事后抽检而非过程控制，缺乏全链路质量追溯，客诉处理闭环周期超过7天' },
          { name: '供应链脆弱', desc: '供应商信息不透明，关键物料依赖单一来源，突发断供后平均恢复周期超2周' }
        ],
        opportunities: ['MES系统', '质量追溯', '预测性维护']
      },
      '能源': {
        trends: ['双碳目标', '新能源发展', '数字化运维'],
        challenges: [
          { name: '设备管理复杂', desc: '资产种类多且分布偏远，维修记录仍以纸质为主，设备故障平均修复时间(MTTR)超48h' },
          { name: '安全风险高', desc: '巡检依赖人工经验，隐患发现不及时，安全事件响应仍靠电话逐级上报' },
          { name: '成本控制难', desc: '能耗数据采集靠手工抄表，节能优化缺数据支撑，运维预算逐年压缩' }
        ],
        opportunities: ['智能运维', '能耗管理', '安全监控']
      },
      '政务': {
        trends: ['数字政府', '一网通办', '数据共享'],
        challenges: [
          { name: '系统割裂', desc: '各部门条线系统各自建设，群众办事需反复提交材料，数据核验跨部门流转周期长达数周' },
          { name: '服务体验差', desc: '线下窗口排队时间长，线上服务入口分散，适老化改造进展滞后' },
          { name: '数据孤岛', desc: '政务数据共享缺乏统一标准，跨部门协同审批耗时占整体办理时长60%以上' }
        ],
        opportunities: ['一体化平台', '智能审批', '数据治理']
      }
    };

    return insights[this.config.industry] || insights['零售'];
  }

  generateSolution() {
    const solutions = {
      '智能客服系统': {
        core: '全渠道智能客服平台',
        features: [
          { name: '多渠道接入', desc: '整合电话/在线/小程序/APP全渠道，统一工单队列，客户一次接入、全程追溯' },
          { name: '智能路由', desc: '基于意图识别+技能标签自动派单，关键客户优先接入，平均响应时间缩短70%' },
          { name: '知识库管理', desc: 'FAQ+文档+工单沉淀闭环，AI辅助坐席实时推荐答案，新人上手周期从3周缩至3天' },
          { name: '数据分析', desc: '热力图+情绪监测+质检评分一体化，服务漏洞自动预警，客诉率可追踪可归因' }
        ],
        value: '提升客服效率50%+，降低人力成本30%'
      },
      'RAG知识库': {
        core: '企业级智能知识库系统',
        features: [
          { name: '文档智能解析', desc: 'PDF/Word/网页多格式自动解析、切片、向量化，知识入库零人工干预' },
          { name: '语义搜索', desc: '基于RAG+混合检索，模糊问题也能精准命中，知识检索准确率提升40%+' },
          { name: '问答机器人', desc: '对接飞书/企微/钉钉，员工问一句即答，减少"知识找不到"导致的重复咨询' },
          { name: '知识图谱', desc: '实体关系自动抽取，知识关联可视化展现，辅助发现隐藏的业务逻辑连接' }
        ],
        value: '知识检索准确率提升40%，响应时间缩短80%'
      },
      'CRM系统': {
        core: '客户关系管理平台',
        features: [
          { name: '客户360视图', desc: '打通交易/服务/营销数据，单客户全生命周期画像，告别多系统来回跳转' },
          { name: '销售漏斗', desc: '可视化商机阶段管理，自动标注卡点线索，预测成交概率准确率达85%+' },
          { name: '自动化营销', desc: '基于行为和标签的自动触达策略，沉默客户自动召回，MA活动执行效率提升10倍' },
          { name: '数据分析', desc: '多维度销售看板+客户分群+流失预警，用数据驱动而非经验驱动决策' }
        ],
        value: '销售转化率提升25%，客户留存率提升20%'
      },
      '供应链管理系统': {
        core: '端到端供应链协同平台',
        features: [
          { name: '供应商协同', desc: '采购订单在线协同+交期自动预警+对账自动化，采购端沟通成本降低60%' },
          { name: '智能排产', desc: '基于订单优先级+产能约束+物料齐套的自动排程，排产耗时从天级缩至分钟级' },
          { name: '库存优化', desc: 'ABC分类+安全库存自动计算+滞销品预警，库存周转率提升30%、呆滞库存减少25%' },
          { name: '物流追踪', desc: 'TMS集成+轨迹可视化+签收电子化，终端配送全链路透明，异常自动升级处理' }
        ],
        value: '库存周转提升30%，交付准时率提升至95%+'
      }
    };

    return solutions[this.config.product] || {
      core: `${this.config.product}解决方案`,
      features: [
        { name: '定制化功能', desc: '按业务需求灵活配置功能模块，避免通用方案与真实场景的割裂' },
        { name: '系统集成', desc: '开放API+标准接口，快速对接客户现有系统，数据不搬家也能跑' },
        { name: '数据安全', desc: '多层权限管控+操作审计+数据加密，通过等保三级认证' },
        { name: '持续运维', desc: '7×12h在线支持+季度业务复盘+持续迭代，系统上线不是终点而是起点' }
      ],
      value: '提升业务效率，降低运营成本'
    };
  }

  translatePainpoints(painpointsStr) {
    if (!painpointsStr || painpointsStr.trim() === '') return [];
    const patterns = [
      '转化为可量化验收的业务改进目标，纳入项目KPI体系',
      '从"说不清"到"可度量"：设定基线值、目标值、验收标准',
      '拆解为具体场景——当前效率、期望效率、差距量化',
      '对标行业最佳实践，识别改进空间和优先动作',
      '映射到系统功能模块，确保每个痛点有明确的产品落点'
    ];
    return painpointsStr.split(',').map((p, i) => ({
      pain: p.trim(),
      translation: patterns[i % patterns.length]
    })).filter(p => p.pain);
  }

  generateImplementationPlan() {
    const timeline = this.config.timeline || '3个月';
    const months = parseInt(timeline) || 3;
    const totalWeeks = months * 4;  // 转周计算
    const week1 = Math.ceil(totalWeeks * 0.3);
    const week2 = Math.ceil(totalWeeks * 0.7);
    
    return {
      phases: [
        {
          name: '第一阶段：需求确认与方案设计',
          duration: `第1-${week1}周`,
          tasks: ['业务调研', '需求确认', '方案设计', '原型确认']
        },
        {
          name: '第二阶段：系统开发与测试',
          duration: `第${week1 + 1}-${week2}周`,
          tasks: ['系统开发', '接口对接', '功能测试', '用户验收']
        },
        {
          name: '第三阶段：上线部署与培训',
          duration: `第${week2 + 1}-${totalWeeks}周`,
          tasks: ['生产部署', '数据迁移', '用户培训', '上线支持']
        }
      ]
    };
  }

  generateROI() {
    const budget = this.config.budget || '50-100万';
    // 解析预算：支持 "80-120万"（区间）和 "150万"（单值）
    const budgetMatch = budget.match(/(\d+)\s*(?:-\s*(\d+))?\s*万/);
    let minBudget, maxBudget;
    if (budgetMatch) {
      minBudget = parseInt(budgetMatch[1]);
      maxBudget = budgetMatch[2] ? parseInt(budgetMatch[2]) : Math.round(minBudget * 1.2);
    } else {
      minBudget = 50;
      maxBudget = 100;
    }
    const avgBudget = (minBudget + maxBudget) / 2;

    return {
      investment: minBudget === maxBudget ? `${minBudget}万元` : `${minBudget}-${maxBudget}万元`,
      benefits: [
        { item: '人力成本节约', value: `${Math.round(avgBudget * 0.3)}万元/年`, desc: '自动化替代重复工作' },
        { item: '效率提升收益', value: `${Math.round(avgBudget * 0.5)}万元/年`, desc: '流程优化带来效率提升' },
        { item: '风险降低价值', value: `${Math.round(avgBudget * 0.2)}万元/年`, desc: '减少错误和合规风险' }
      ],
      paybackPeriod: '12-18个月',
      threeYearROI: '250%-350%'
    };
  }

  getDefaultCases() {
    return [
      {
        name: '中信集团数字化转型',
        client: '中信集团',
        industry: '综合金融',
        solutions: ['业务中台', '数据中台'],
        keyResults: '实现数据互通，业务流程系统化'
      },
      {
        name: '力方力合供应链升级',
        client: '力方力合',
        industry: '服装鞋帽',
        solutions: ['供应链系统', '智能排产'],
        keyResults: '交付周期从45天缩短至30天'
      }
    ];
  }
}

module.exports = ProposalGenerator;
