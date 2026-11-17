"""Narrative / required-gap needle catalogs (declarative).

narrative-scan 用：章节定位（section_patterns 或直接用 meta.sections 的 anchor key）
+ 行文锚词 needles。needle 命中 → 自动 found（quote+page）；未命中 → 生成 agent_tasks
证据包供 Agent 终审（程序不越权判 not_disclosed）。

needles 命中策略：优先正文行（非表格行），无命中再扫表格行；行文本去空白子串匹配。
"""
from __future__ import annotations

# 通用 MD&A 叙述（4 项，所有行业适用；q1/q3 由 catalog 判 not_applicable）
NARRATIVE_SPECS: dict[str, dict] = {
    "mda_business": {
        "section_keys": ["mda_business", "mda_overview"],
        "section_patterns": [r"经营情况讨论与分析", r"管理层讨论与分析", r"报告期内公司从事的业务"],
        "needles": ["主营业务", "核心竞争力", "经营模式", "主营业务为", "主要业务为"],
    },
    "mda_industry": {
        "section_keys": ["mda_industry"],
        "section_patterns": [r"所处行业", r"行业格局", r"行业情况", r"市场格局"],
        "needles": ["行业格局", "市场竞争", "供需", "行业地位", "市场份额", "行业集中度"],
    },
    "mda_outlook": {
        "section_keys": ["mda_outlook"],
        "section_patterns": [r"未来发展的展望", r"经营计划", r"发展战略"],
        "needles": ["展望", "发展规划", "经营计划", "发展战略", "重点工作"],
    },
    "risk_factors": {
        "section_keys": ["risk_factors"],
        "section_patterns": [r"可能面对的风险", r"风险因素", r"面对的主要风险", r"风险管理"],
        "needles": ["风险", "风险提示", "不确定性"],
    },
}

# 行业叙述 needles（挂 INDUSTRY_EXT_GROUPS[industry].narratives 的 id）
INDUSTRY_NARRATIVE_SPECS: dict[str, dict[str, dict]] = {
    "fossil_energy": {
        "commodity_price": {"needles": ["煤价", "动力煤", "年度长协", "月度长协", "市场煤价", "煤炭价格", "现货价"]},
        "unit_cost": {"needles": ["吨煤成本", "单位生产成本", "自产煤单位", "单位销售成本"]},
    },
    "energy": {
        "power_price": {"needles": ["上网电价", "市场化交易电价", "电价", "结算电价"]},
        "fuel_cost": {"needles": ["燃料成本", "标煤单价", "入炉标煤", "燃煤成本"]},
    },
    "bank": {
        "nim_drivers": {"needles": ["净息差", "净利差", "生息资产收益率", "计息负债成本"]},
    },
    "insurance": {
        "underwriting_profit": {"needles": ["承保利润", "综合成本率", "赔付率", "COR"]},
        "spread_income": {"needles": ["利差", "投资收益率", "资产负债匹配", "再投资"]},
    },
    "broker": {
        "trading_volume_drivers": {"needles": ["市场成交", "股基成交", "日均成交", "两融余额"]},
    },
    "real_estate": {
        "sell_through": {"needles": ["去化", "签约金额", "签约面积", "销售回款"]},
        "project_financing": {"needles": ["开发贷", "融资成本", "三道红线", "有息负债"]},
    },
    "pharma": {
        "pipeline_progress": {"needles": ["临床", "管线", "注册申请", "批准上市", "获批"]},
        "vbp_policy_impact": {"needles": ["集采", "带量采购", "医保目录", "中标"]},
    },
    "consumer": {
        "pricing_volume": {"needles": ["出厂价", "提价", "终端价", "价格带"]},
        "channel_reform": {"needles": ["渠道改革", "经销商", "直销", "渠道结构"]},
    },
    "transport_infrastructure": {
        "traffic_volume_drivers": {"needles": ["车流量", "通行量", "吞吐量", "货车流量"]},
        "tariff_policy": {"needles": ["收费标准", "通行费", "装卸费", "收费政策"]},
    },
    "nonferrous": {
        "project_progress": {"needles": ["在建项目", "投产", "项目建设", "达产"]},
        "unit_cost": {"needles": ["单位成本", "加工费", "冶炼加工费", "C1成本"]},
    },
    "automobile": {
        "brand_sales": {"needles": ["销量", "市占率", "新能源车型", "出海"]},
        "dealer_network": {"needles": ["经销商", "门店", "渠道网络", "直营"]},
    },
    "auto_electronics": {
        "design_win_pipeline": {"needles": ["定点", "定点项目", "获得定点", "量产项目"]},
        "aso_price_trend": {"needles": ["均价", "ASP", "产品价格"]},
    },
    "building_materials": {},
    "machinery": {},
    "manufacturing": {},
    # ---- 2025A 新增行业（E3）----
    "steel": {
        "steel_price": {"needles": ["钢价", "钢材价格", "吨钢价格", "现货价格"]},
        "raw_material_cost": {"needles": ["铁矿石", "焦炭", "原料成本", "废钢"]},
    },
    "chemicals": {
        "product_spread": {"needles": ["价差", "产品价格", "均价"]},
        "feedstock_cost": {"needles": ["原料成本", "煤炭", "石脑油"]},
    },
    "telecom": {
        "arpu_drivers": {"needles": ["ARPU", "用户价值", "DOU"]},
    },
    "internet_consumer_electronics": {
        "user_growth": {"needles": ["用户增长", "MAU", "月活跃"]},
        "hardware_asp": {"needles": ["出货量", "均价", "ASP"]},
    },
    "agriculture": {
        "hog_cycle": {"needles": ["猪价", "生猪价格", "猪周期"]},
        "feed_cost": {"needles": ["饲料成本", "玉米", "豆粕"]},
    },
    "semiconductor": {
        "fab_capacity_outlook": {"needles": ["产能爬坡", "扩产", "资本开支"]},
    },
}

# required_gaps needles（同扫：命中即 found，未命中进 agent_tasks）
INDUSTRY_GAP_NEEDLES: dict[str, dict[str, list[str]]] = {
    "fossil_energy": {
        "equity_vs_attributable_output": ["商品煤产量", "权益产量", "归属产量"],
        "railway_port_shipment": ["铁路周转量", "装船量", "外运量", "自有铁路"],
        "coal_washing_yield": ["洗选", "入洗", "洗选率"],
        "refining_chemical_margin": ["煤化工", "化工品毛利率", "聚乙烯", "聚丙烯"],
        "proved_vs_probable_reserves": ["证实储量", "可采储量", "保有资源量", "可信储量"],
    },
    "bank": {
        "cost_income_ratio": ["成本收入比", "业务及管理费"],
        "retail_aum": ["零售AUM", "管理零售客户资产", "财富管理资产"],
    },
    "insurance": {
        "ifrs17_csm": ["合同服务边际", "CSM"],
        "persistency_surrender_rate": ["继续率", "退保率"],
        "combined_ratio_text": ["综合成本率", "COR"],
    },
    "broker": {
        "client_funds_custody": ["客户资金", "托管规模", "客户存款"],
    },
    "real_estate": {
        "land_acquisition": ["拿地", "新增土储", "土地购置"],
        "equity_vs_full_scope": ["权益口径", "全口径", "权益比例"],
    },
    "energy": {
        "capacity_under_construction": ["在建装机", "核准装机", "新投产机组"],
        "controlling_vs_equity_capacity": ["控股装机", "权益装机"],
        "installed_capacity_text": ["装机容量", "并网容量"],
        "utilization_hours_text": ["利用小时", "发电小时"],
        "hydrology_text": ["来水", "水库", "蓄能"],
    },
    "pharma": {
        "key_product_pricing": ["挂网价", "中标价", "出厂价"],
        "market_share_estimate": ["市场份额", "竞争格局"],
        "sales_force_scale": ["销售人员", "医药代表"],
        "innovative_vs_generic_mix": ["创新药收入", "仿制药收入"],
        "cdmo_order_visibility": ["CDMO", "在手订单"],
    },
    "consumer": {
        "dealer_inventory": ["渠道库存", "社会库存", "库存周期"],
        "same_store_sales_text": ["同店", "同店增长"],
        "shipment_vs_revenue": ["发货量", "动销"],
        "member_metrics": ["会员数", "复购率", "会员"],
    },
    "transport_infrastructure": {
        "equity_vs_consolidated_throughput": ["权益口径", "并表口径"],
        "operating_revenue_vs_accounting": ["通行费收入", "装卸收入", "经营收入"],
        "concession_remaining_years": ["收费年限", "特许经营期", "剩余年限"],
        "capacity_under_construction": ["在建", "改扩建"],
        "etc_traffic_mix": ["ETC", "车型结构"],
        "toll_per_vehicle_text": ["单车通行费", "单公里"],
        "berth_utilization": ["泊位利用率", "泊位数"],
        "hinterland_economy": ["腹地", "货源"],
    },
    "automobile": {},
    "nonferrous": {},
    "auto_electronics": {
        "market_share_multi_source": ["市场份额", "装机量", "出货量"],
        "design_win_vs_sop": ["定点", "SOP", "量产"],
    },
    "building_materials": {},
    "machinery": {},
    "manufacturing": {},
}
