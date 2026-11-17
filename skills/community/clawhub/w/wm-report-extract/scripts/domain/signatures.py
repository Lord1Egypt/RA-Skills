"""Table/section signature constants for wm-report-extract."""
from __future__ import annotations

import re

CHAPTER_RE = re.compile(
    r"^#{1,3}\s*第([一二三四五六七八九十\d]+)\s*[节章]\s*[、.．:]?\s*(.{2,24})\s*$"
)

CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}

SUBSECTION_ANCHORS: list[tuple[str, str, re.Pattern]] = [
    ("key_financials", "主要会计数据和财务指标", re.compile(r"主要会计数据|会计数据(?:和|及)财务指标|主要財務[数數]?據")),
    # 港式 IFRS 报表标题（## 合併損益表 / ## 合併財務狀況表 / ## 合併現金流量表 / 中期簡明合併…）
    ("balance_sheet", "合并资产负债表", re.compile(
        r"^#{1,3}\s*(?:中期簡明)?(?:合併|合并)?(?:资产负债表|財務狀況表|财务状况表)(?:\s*及其他全面收益表?)?(?:\s*附[注註].*)?$")),
    ("income_stmt", "合并利润表", re.compile(
        r"^#{1,3}\s*(?:中期簡明)?(?:合併|合并)?(?:利润表|損益表|损益表)(?:及其他全面收益表?)?(?:\s*附[注註].*)?$")),
    ("cashflow_stmt", "合并现金流量表", re.compile(
        r"^#{1,3}\s*(?:中期簡明)?(?:合併|合并)?(?:现金流量表|現金流量表)(?:\s*附[注註].*)?$")),
    ("equity_stmt", "所有者权益变动表", re.compile(r"所有者权益(?:变动|权益)变动?表|權益變動表")),
    ("mda_overview", "经营情况讨论与分析", re.compile(
        r"(?:经营情况|经营业绩)(?:的)?讨论与分析|总体经营情况|管理層[讨討][论論][与與]及?分析")),
    # 不匹配「未来计划」：重要提示里的前瞻性免责声明会误中。
    ("mda_outlook", "未来发展的展望", re.compile(
        r"(?:公司关于)?(?:公司)?未来发展的讨论与分析|未来发展的?展望|前景展望|^#{1,3}\s*未来展望"
    )),
    ("mda_business", "经营模式/从事的业务", re.compile(r"经营模式|从事的业务情况|报告期内公司从事的业务|^#{1,3}\s*業務$")),
    ("mda_industry", "所处行业情况", re.compile(r"所处行业情况|报告期内公司所处行业|所处行业|行業概[览覽]")),
    ("segments", "主营业务分行业/分产品", re.compile(r"主营业务?分(?:行业|产品|地区)|分部信息|分部資料|经营分部|經營分部")),
    ("top_holders", "前十大股东", re.compile(r"前\s*10\s*名股东|前十(?:大)?股东|主要股东持股情况|主要股東於股份")),
    ("holder_count", "股东总数/户数", re.compile(r"股东(?:总)?数|股东户数")),
    ("dividend", "利润分配与分红", re.compile(r"利润分配|分红?(?:方案|情况|政策)|每\s*10\s*股|股息")),
    ("buyback", "股份回购", re.compile(r"回购(?:股份|实施情况)|購回[股股]份")),
    ("related_txn", "关联交易", re.compile(r"(?:重大)?关联交易|關連交易|持續關連交易")),
    ("guarantees", "重大担保", re.compile(r"(?:重大)?担保|擔保")),
    ("litigation", "重大诉讼仲裁", re.compile(r"(?:重大)?诉讼|仲裁|法律程序")),
    ("commitments", "承诺事项履行", re.compile(r"承诺(?:事项)?(?:履行|情况)")),
    ("audit_report", "审计报告", re.compile(r"(?:审计报告|审计意见|核數師[报報]告)")),
    ("key_policies", "关键会计政策", re.compile(r"(?:重要|关键)会计政策(?:及会计估计)?|主要會計政策")),
    ("contingencies", "或有事项", re.compile(r"或有(?:事项|负债)")),
    ("subsequent", "资产负债表日后事项", re.compile(r"日(?:后|后事项)事项|资产负债表日后|日後事項")),
    ("employees", "员工情况", re.compile(r"员工(?:情况|人数)|在职员工|僱員")),
    ("executives", "董事监事高管", re.compile(r"董事(?:、|和)?监事(?:和|、)?高级管理人员|董监高|董事及高級管理層")),
    ("risk_factors", "风险因素/重大风险提示", re.compile(r"(?:可能面对的)?风险|风险(?:因素|提示)|風險(?:因素|提示)|重大風險提示")),
    ("ppe", "重大资产变化", re.compile(r"主要资产(?:重大)?变化|重大资产(?:购置|处置)")),
    ("pledge", "股权质押/冻结", re.compile(r"质押|冻结")),
]

HIGH_CONFIDENCE_SIGNATURES: list[tuple[str, list[str]]] = [
    ("key_financials", ["归属于上市公司股东的净利润", "营业收入"]),
    ("key_financials", ["每股收益", "增减"]),
    ("non_recurring", ["非经常性损益"]),
    ("top_holders", ["前十", "持股"]),
    ("dividend", ["每10股", "分红"]),
    ("dividend", ["分红", "股利"]),
    ("segments", ["分行业", "营业收入"]),
    ("segments", ["分产品", "毛利率"]),
    ("segments", ["分地区", "营业收入"]),
    ("segments", ["分行业", "分产品"]),
    ("segments", ["分地区", "毛利率"]),
    ("production_sales", ["生产量", "销售量", "库存量"]),
    ("variance_reasons", ["变动幅度", "原因说明"]),
    ("variance_reasons", ["变动比例", "情况说明"]),
    ("variance_reasons", ["变动比例", "变动原因"]),
    ("mda_ratios", ["毛利率", "占营业收入"]),
    ("pledge", ["质押", "股份数量"]),
]

TYPE_HINT_SIGNATURES: list[tuple[str, list[str]]] = [
    ("employees", ["员工", "专业构成"]),
    ("employees", ["在职员工", "数量"]),
    ("rd_investment", ["研发投入", "占营业收入"]),
    ("rd_investment", ["研发支出", "资本化"]),
    ("related_txn", ["关联交易", "金额"]),
    ("related_txn", ["关联交易", "定价"]),
    ("related_txn", ["关联方", "关联交易内容"]),  # fitz 轨道版式：表头无「金额」字样
    ("guarantees", ["对外担保", "余额"]),
    ("guarantees", ["担保", "担保总额"]),
    ("equity_incentive", ["股权激励", "限制性股票"]),
    ("equity_incentive", ["股票期权", "授予"]),
    ("nev_sales", ["新能源", "销量"]),
    ("capacity_util", ["产能利用率"]),
    ("capacity_util", ["产能", "利用率"]),
    ("overseas_ops", ["海外", "销量"]),
    ("overseas_ops", ["海外", "收入"]),
    ("overseas_ops", ["出口", "销量"]),
    ("reserves", ["资源量", "储量"]),
    ("reserves", ["矿石量", "品位"]),
    ("reserves", ["保有", "金属量"]),
    ("construction_projects", ["工程进度", "预算"]),
    ("construction_projects", ["投入占预算", "工程进度"]),
    ("hedging", ["衍生品", "报告期实际损益"]),
    ("hedging", ["套期保值", "合约"]),
    ("hedging", ["衍生品投资", "期末投资金额"]),
    # 变动分析表（项目/本期/上期/变化%）：形态匹配 variance_reasons 目录，作晋升候选
    ("variance_reasons", ["变动分析", "营业收入"]),
    ("variance_reasons", ["变动分析", "现金流量"]),
    # insurance
    ("premium_income", ["原保险保费收入", "保险业务收入"]),
    ("premium_income", ["已赚保费", "保费收入"]),
    # 平安式渠道/险种保费表：表头直接给「原保险保费收入」列，无「保险业务收入」同现
    ("premium_income", ["销售渠道", "原保险保费收入"]),
    ("premium_income", ["保险金额", "原保险保费收入"]),
    ("claims_payout", ["赔付支出", "退保金"]),
    ("claims_payout", ["赔付支出", "已决赔款"]),
    ("solvency", ["综合偿付能力充足率", "核心偿付能力充足率"]),
    ("solvency", ["偿付能力充足率", "最低资本"]),
    ("investment_assets", ["投资资产", "债权投资"]),
    ("investment_assets", ["投资资产", "股权投资"]),
    ("nbv_ev", ["新业务价值", "内含价值"]),
    ("nbv_ev", ["新业务价值", "NBV"]),
    ("nbv_ev", ["内含价值", "有效业务价值"]),
    ("channel_mix", ["个险", "银保"]),
    ("channel_mix", ["个人代理", "银行保险"]),
    ("channel_mix", ["经代", "银保渠道"]),
    # broker
    ("brokerage_income", ["经纪业务", "手续费及佣金"]),
    ("brokerage_income", ["代理买卖证券", "佣金收入"]),
    ("ib_underwriting", ["投行业务", "承销"]),
    ("ib_underwriting", ["投资银行", "保荐"]),
    ("am_aum", ["资产管理业务", "管理费"]),
    ("am_aum", ["资管", "受托管理"]),
    ("risk_indicators", ["净资本", "风险覆盖率"]),
    ("risk_indicators", ["风险控制指标", "净资本"]),
    ("margin_trading", ["融资融券", "两融余额"]),
    ("margin_trading", ["融资余额", "融券余额"]),
    ("margin_trading", ["信用业务", "融资融券"]),
    ("prop_trading", ["自营业务", "投资收益"]),
    ("prop_trading", ["证券投资", "公允价值变动"]),
    ("prop_trading", ["自营", "衍生品"]),
    # real_estate
    ("contracted_sales", ["签约金额", "签约面积"]),
    ("contracted_sales", ["销售面积", "签约"]),
    ("land_bank", ["土地储备", "总建筑面积"]),
    ("land_bank", ["土储", "权益面积"]),
    ("delivery_completion", ["竣工面积", "交付面积"]),
    ("delivery_completion", ["竣工", "结转面积"]),
    ("contract_liabilities", ["合同负债", "预收账款"]),
    ("contract_liabilities", ["合同负债", "结转"]),
    ("three_red_lines", ["净负债率", "现金短债比"]),
    ("three_red_lines", ["剔除预收后的资产负债率", "净负债率"]),
    ("three_red_lines", ["三道红线", "净负债率"]),
    # energy
    ("installed_capacity", ["装机容量", "千瓦"]),
    ("installed_capacity", ["装机", "兆瓦"]),
    ("power_generation", ["发电量", "上网电量"]),
    ("power_generation", ["售电量", "发电量"]),
    ("utilization_hours", ["利用小时", "平均利用小时"]),
    ("utilization_hours", ["利用小时数", "设备利用"]),
    ("hydrology", ["来水", "水库"]),
    ("hydrology", ["来水", "蓄能"]),
    ("hydrology", ["入库流量", "水位"]),
    ("power_price_mix", ["中长期", "现货"]),
    ("power_price_mix", ["市场化交易", "电价"]),
    ("power_price_mix", ["中长期合同", "现货市场"]),
    # bank
    ("capital_adequacy", ["核心一级资本充足率", "资本充足率"]),
    ("capital_adequacy", ["一级资本充足率", "资本充足率"]),
    ("capital_adequacy", ["资本充足率", "杠杆率"]),
    ("asset_quality", ["不良贷款率", "拨备覆盖率"]),
    ("asset_quality", ["不良贷款", "五级分类"]),
    # 招行式资产质量分布表：贷款和垫款余额/不良贷款余额/关注贷款余额（无五级分类字样）
    ("asset_quality", ["贷款和垫款余额", "不良贷款余额"]),
    ("asset_quality", ["拨备覆盖率", "拨贷比"]),
    ("nim_spread", ["净息差", "净利差"]),
    ("nim_spread", ["净息差", "生息资产"]),
    ("nim_spread", ["净利息收益率", "净利差"]),
    ("nim_spread", ["净利息收益率", "生息资产"]),
    ("deposit_loan", ["吸收存款", "发放贷款和垫款"]),
    ("deposit_loan", ["客户存款", "客户贷款"]),
    ("deposit_loan", ["存款余额", "贷款余额"]),
    ("deposit_loan", ["客户存款总额", "贷款和垫款总额"]),
    ("deposit_loan", ["客户存款", "贷款和垫款"]),
    # pharma
    ("rd_pipeline", ["在研项目", "适应症"]),
    ("rd_pipeline", ["研发项目", "临床阶段"]),
    ("rd_pipeline", ["累计投入", "项目进度"]),
    # 恒瑞附表5 式表头（在研创新药主要临床研发管线）：表头无「在研项目」，靠 药品名称+靶点+适应症 三词同现
    ("rd_pipeline", ["药品名称", "靶点", "适应症"]),
    ("rd_pipeline", ["在研创新药", "临床研发管线"]),
    ("sales_channel_mix", ["销售渠道", "医院"]),
    ("sales_channel_mix", ["终端", "占比"]),
    ("sales_channel_mix", ["配送", "零售"]),
    ("regulatory_milestones", ["一致性评价", "通过"]),
    ("regulatory_milestones", ["注册证", "批准"]),
    ("regulatory_milestones", ["纳入", "国家医保目录"]),
    ("capacity_gmp", ["GMP", "生产基地"]),
    ("capacity_gmp", ["设计产能", "产能利用率"]),
    # consumer（retail_channel_mix 避开与 insurance.channel_mix 冲突）
    ("retail_channel_mix", ["渠道", "销售收入"]),
    ("retail_channel_mix", ["分渠道", "占比"]),
    ("dealer_network", ["经销商", "数量"]),
    ("dealer_network", ["经销商", "区域"]),
    ("store_operations", ["门店", "新开"]),
    ("store_operations", ["门店", "关闭"]),
    ("store_operations", ["经营面积", "门店"]),
    ("same_store_sales", ["同店", "增长"]),
    ("same_store_sales", ["坪效", "门店"]),
    # transport
    ("highway_toll_traffic", ["通行量", "通行费"]),
    ("highway_toll_traffic", ["车流量", "收费"]),
    ("highway_toll_traffic", ["客车流量", "货车流量"]),
    ("highway_toll_traffic", ["日均收入", "客车流量"]),
    ("highway_toll_traffic", ["通行费收入", "日均"]),
    ("concession_network_assets", ["收费公路里程", "特许经营权"]),
    ("concession_network_assets", ["收费年限", "经营期限"]),
    ("concession_network_assets", ["公路经营权", "特许经营"]),
    ("concession_network_assets", ["收费里程", "经营权"]),
    ("port_throughput", ["货物吞吐量", "集装箱"]),
    ("port_throughput", ["吞吐量", "TEU"]),
    ("port_throughput", ["集装箱吞吐量", "货物吞吐量"]),
    ("port_berth_assets", ["泊位", "港区"]),
    ("port_berth_assets", ["泊位", "码头"]),
    # fossil
    ("coal_production", ["原煤产量", "商品煤"]),
    ("coal_production", ["煤炭", "销量"]),
    ("coal_production", ["外运量", "产量"]),
    ("coal_reserves", ["煤炭资源量", "可采储量"]),
    ("coal_reserves", ["查明资源储量", "煤种"]),
    ("coal_reserves", ["矿井", "保有资源量"]),
    ("coal_cost_price", ["吨煤", "完全成本"]),
    ("coal_cost_price", ["吨煤", "销售成本"]),
    ("coal_cost_price", ["长协", "市场煤"]),
    ("hydrocarbon_production", ["原油产量", "天然气"]),
    ("hydrocarbon_production", ["油气当量", "产量"]),
    ("hydrocarbon_production", ["石油液体", "天然气"]),
    ("hydrocarbon_reserves", ["证实储量", "探明"]),
    ("hydrocarbon_reserves", ["剩余经济可采", "原油"]),
    ("hydrocarbon_reserves", ["天然气", "证实储量"]),
    ("lifting_cost", ["桶油", "成本"]),
    ("lifting_cost", ["油气", "单位完全成本"]),
    ("lifting_cost", ["操作成本", "每桶"]),
    # auto_electronics（智驾/汽车电子方案商，简繁并收）
    ("ad_shipments", ["出貨量", "平均售價"]),
    ("ad_shipments", ["出货量", "平均售价"]),
    ("ad_shipments", ["處理硬件", "交付量"]),
    ("ad_shipments", ["处理硬件", "交付量"]),
    ("customer_concentration", ["前五大客戶", "總收入"]),
    ("customer_concentration", ["前五大客户", "总收入"]),
    ("customer_concentration", ["五大客戶", "佔"]),
    # 港式研发占收入比表（研发开支/研发费用占比）
    ("rd_investment", ["研發開支", "佔收入"]),
    # ---- 2025A 新增行业表 hints（E3）----
    ("steel_production", ["钢材", "产量"]),
    ("steel_production", ["粗钢", "销量"]),
    ("steel_cost_price", ["吨钢", "成本"]),
    ("chemical_output", ["化工", "产能"]),
    ("chemical_price_cost", ["价差", "成本"]),
    ("subscriber_base", ["移动用户", "ARPU"]),
    ("subscriber_base", ["用户数", "ARPU"]),
    ("user_metrics", ["MAU", "用户"]),
    ("device_shipments", ["出货量", "智能手机"]),
    ("device_shipments", ["IoT", "出货量"]),
    ("livestock_output", ["出栏", "存栏"]),
    ("wafer_capacity", ["晶圆", "产能"]),
    ("wafer_capacity", ["晶圆", "良率"]),
]

TABLE_SIGNATURES = HIGH_CONFIDENCE_SIGNATURES + TYPE_HINT_SIGNATURES

SUBSIDIARY_HEADER_TOKS = ("持股比例", "注册资本", "业务性质", "表决权", "年末资产",
                          "公司类型", "主要业务", "注册地")

STMT_TITLE_TOKS = {
    "balance_sheet": ("资产负债表", "財務狀況表", "财务状况表"),
    "income_stmt": ("利润表", "損益表", "损益表"),
    "cashflow_stmt": ("现金流量表", "現金流量表"),
}

# 分析类标题否决：MD&A「主要项目变动分析」类表含报表名与科目词但不是报表本体
# （神华 p020「利润表及现金流量表主要项目变动分析」误定型 cashflow_stmt 实证）
ANALYSIS_TITLE_RE = re.compile(
    r"变动分析|變動分析|变动原因|變動原因|主要项目变动|增减变动|增減變動|同比变动|同比變動|摘要")

# 港式 IFRS 科目（實測地平線年報）：資產總值/負債總額/權益總額、年內虧損/期內虧損、
# 經營活動產生的現金流量（亦有 所得現金淨額 寫法）、融資活動（非 籌資活動）
STRUCTURAL_RULES: list[tuple[str, list[tuple[str, ...]]]] = [
    ("balance_sheet", [("资产总计", "资产合计", "資產總值"),
                       ("负债合计", "负债和所有者权益总计", "负债和股东权益总计", "负债及所有者权益总计",
                        "負債總額", "權益總額")]),
    ("income_stmt", [("净利润", "年內虧損", "年內溢利", "期內虧損", "期內溢利", "年度溢利",
                      "╱利潤", "／利潤", "/利润", "利潤╱", "溢利╱", "利潤／"),  # 港式双写法两种序：「年內 (虧損) ╱利潤」「年內利潤╱ (虧損)」
                     ("营业收入", "营业总收入", "來自客戶合同的收入", "保险业务收入",
                      "保险业务收益")]),  # 保险公司利润表首行科目为「保险业务收入」（平安实证）
    ("cashflow_stmt", [("经营活动产生的现金流量净额", "经营活动产生的现金流量",
                        "经营活动产生/(使用)的现金流量", "一、经营活动产生的现金流量",
                        "一、经营活动产生/(使用)的现金流量",
                        "經營活動產生的現金流量", "經營活動所得現金淨額"),
                       ("投资活动", "筹资活动", "投資活動", "融資活動")]),
]

