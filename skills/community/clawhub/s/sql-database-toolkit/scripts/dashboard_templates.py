"""
dashboard-templates: 生产级行业标准看板模板库
支持 9 大行业、20+ 个标准看板模板
每个看板包含：图表组合、数据格式、解读说明、深度洞察
"""

import base64
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# 看板模板定义
# ============================================================================

@dataclass
class ChartSpec:
    """图表规格"""
    chart_type: str          # 图表类型
    title: str              # 图表标题
    description: str        # 简洁解读
    data_format: Dict       # 数据格式示例
    insights: str           # 深度洞察
    tooltip: Optional[Dict] = None  # 工具提示配置

@dataclass
class TooltipConfig:
    """工具提示（Tooltip）配置"""
    enabled: bool = True
    show_dimensions: bool = True        # 显示维度名称
    show_metrics: bool = True            # 显示指标数值
    show_comparison: bool = True         # 显示同比/环比/占比
    custom_fields: List[str] = None      # 自定义显示字段
    format: str = "default"             # default | custom

@dataclass
class DashboardTemplate:
    """看板模板"""
    industry: str           # 行业
    template_name: str      # 模板名称
    template_id: str        # 模板ID
    description: str        # 看板描述
    charts: List[ChartSpec] # 图表列表
    kpis: List[str]        # 关键指标
    insights: str          # 深度洞察
    recommendations: str   # 运营建议

# ============================================================================
# 一、电商行业看板模板
# ============================================================================

ECOMMERCE_TEMPLATES = {
    "ecommerce_overview": DashboardTemplate(
        industry="电商",
        template_name="电商全域经营总览看板",
        template_id="ecommerce_overview",
        description="日/周/月电商核心经营指标总览，覆盖GMV、流量、转化、品类、渠道等全维度",
        charts=[
            ChartSpec(
                chart_type="card",
                title="核心指标卡片",
                description="展示GMV、订单量、UV、转化率、客单价等5个核心指标",
                data_format={
                    "cards": [
                        {"title": "GMV", "value": "¥12,345,678", "change": "+15.2%"},
                        {"title": "订单量", "value": "234,567", "change": "+12.3%"},
                        {"title": "UV", "value": "1,234,567", "change": "+8.5%"},
                        {"title": "转化率", "value": "3.45%", "change": "+0.2%"},
                        {"title": "客单价", "value": "¥52.5", "change": "+6.8%"}
                    ]
                },
                insights="核心指标同比增长15%，说明经营动能充足。转化率小幅提升，说明用户体验优化有效。"
            ),
            ChartSpec(
                chart_type="line",
                title="日GMV趋势",
                description="过去30天日GMV走势，识别周期性规律和异常波动",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [{"name": "GMV", "data": [1000000, 1200000, 1100000, 1300000, 1400000]}]
                },
                insights="周末GMV明显高于工作日，周五-周日为销售高峰。建议周末加大营销投入。"
            ),
            ChartSpec(
                chart_type="clustered_column",
                title="品类销售额对比",
                description="各品类销售额排名，识别主力品类和增长品类",
                data_format={
                    "categories": ["服装", "食品", "电子", "家居", "美妆"],
                    "series": [{"name": "销售额", "data": [3000000, 2500000, 2000000, 1500000, 1000000]}]
                },
                insights="服装品类占比最高（30%），食品品类增速最快（+25%）。建议加大食品品类投入。"
            ),
            ChartSpec(
                chart_type="stacked_column",
                title="渠道GMV构成",
                description="PC、APP、小程序、社交等渠道的GMV占比和趋势",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [
                        {"name": "APP", "data": [600000, 700000, 650000, 800000, 900000]},
                        {"name": "PC", "data": [300000, 350000, 320000, 380000, 400000]},
                        {"name": "小程序", "data": [100000, 150000, 130000, 120000, 100000]}
                    ]
                },
                insights="APP渠道占比70%，是主要销售渠道。PC渠道占比20%，小程序占比10%。"
            ),
            ChartSpec(
                chart_type="funnel",
                title="转化漏斗",
                description="流量→加购→下单→支付的完整转化链路",
                data_format={
                    "stages": ["访问", "加购", "下单", "支付"],
                    "values": [1000000, 450000, 200000, 180000]
                },
                insights="加购转化率45%，下单转化率44%，支付转化率90%。支付环节转化最高，建议优化加购和下单环节。"
            ),
            ChartSpec(
                chart_type="table",
                title="TOP20商品明细",
                description="销售额TOP20商品的详细数据，包括销量、价格、库存等",
                data_format={
                    "columns": ["商品名", "销售额", "销量", "价格", "库存"],
                    "rows": [
                        ["爆款T恤", "¥500,000", "10,000", "¥50", "5,000"],
                        ["热销牛仔裤", "¥450,000", "9,000", "¥50", "4,500"]
                    ]
                },
                insights="TOP20商品占总销售额的60%，集中度较高。建议加强TOP商品的库存管理和营销投入。"
            ),
            ChartSpec(
                chart_type="donut",
                title="支付方式占比",
                description="支付宝、微信、银行卡等支付方式的占比",
                data_format={
                    "labels": ["支付宝", "微信", "银行卡", "其他"],
                    "values": [45, 35, 15, 5]
                },
                insights="支付宝和微信占比80%，是主要支付方式。建议优化这两个渠道的支付体验。"
            )
        ],
        kpis=["GMV", "订单量", "UV", "转化率", "客单价"],
        insights="电商经营整体向好，GMV同比增长15%，转化率稳步提升。品类结构优化，食品品类增速最快。渠道多元化，APP成为主要销售渠道。",
        recommendations="1. 加大食品品类投入，抓住增长机遇\n2. 优化加购和下单环节，提升转化率\n3. 加强TOP商品库存管理，避免缺货\n4. 周末加大营销投入，抓住销售高峰\n5. 优化支付体验，降低支付流失"
    ),
    
    "user_growth": DashboardTemplate(
        industry="电商",
        template_name="电商用户生命周期看板",
        template_id="user_growth",
        description="用户新增、活跃、留存、复购的完整生命周期分析",
        charts=[
            ChartSpec(
                chart_type="card",
                title="用户关键指标",
                description="新增用户、活跃用户、留存率、复购率等关键指标",
                data_format={
                    "cards": [
                        {"title": "新增用户", "value": "123,456", "change": "+10.5%"},
                        {"title": "活跃用户", "value": "567,890", "change": "+8.2%"},
                        {"title": "留存率", "value": "45.6%", "change": "+2.1%"},
                        {"title": "复购率", "value": "32.1%", "change": "+3.5%"}
                    ]
                },
                insights="新增用户增速10.5%，活跃用户增速8.2%。留存率和复购率均有提升，说明用户粘性增强。"
            ),
            ChartSpec(
                chart_type="line",
                title="日活/周活趋势",
                description="过去30天日活和周活的走势，识别用户活跃度变化",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [
                        {"name": "日活", "data": [450000, 480000, 470000, 520000, 550000]},
                        {"name": "周活", "data": [800000, 850000, 820000, 900000, 950000]}
                    ]
                },
                insights="日活和周活均呈上升趋势，说明用户活跃度持续提升。周末活跃度明显高于工作日。"
            ),
            ChartSpec(
                chart_type="stacked_area",
                title="新老用户贡献占比",
                description="新用户和老用户对GMV的贡献占比变化",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [
                        {"name": "新用户", "data": [300000, 350000, 320000, 380000, 420000]},
                        {"name": "老用户", "data": [700000, 750000, 780000, 820000, 880000]}
                    ]
                },
                insights="老用户贡献占比70%，是主要收入来源。新用户贡献占比30%，增速快于老用户。"
            ),
            ChartSpec(
                chart_type="scatter",
                title="活跃度 vs 留存率",
                description="用户活跃度与留存率的相关性分析",
                data_format={
                    "x": [10, 20, 30, 40, 50],
                    "y": [20, 35, 45, 55, 65],
                    "labels": ["低活跃", "中低活跃", "中活跃", "中高活跃", "高活跃"]
                },
                insights="活跃度与留存率呈正相关，高活跃用户留存率达65%，低活跃用户留存率仅20%。"
            ),
            ChartSpec(
                chart_type="matrix",
                title="区域×日期×留存率",
                description="不同区域用户的留存率变化",
                data_format={
                    "rows": ["华东", "华北", "华南", "西部"],
                    "columns": ["3-1", "3-2", "3-3", "3-4"],
                    "values": [
                        [45, 48, 50, 52],
                        [42, 44, 46, 48],
                        [40, 42, 44, 46],
                        [35, 37, 39, 41]
                    ]
                },
                insights="华东地区留存率最高（52%），西部地区最低（41%）。建议加强西部地区的用户运营。"
            )
        ],
        kpis=["新增用户", "活跃用户", "留存率", "复购率"],
        insights="用户生命周期管理成效显著，新增用户增速10.5%，活跃用户增速8.2%。留存率和复购率均有提升，说明用户粘性增强。老用户贡献占比70%，是主要收入来源。",
        recommendations="1. 加强新用户的首次购买转化，提升新用户留存\n2. 建立老用户复购激励机制，提升复购率\n3. 针对低活跃用户进行唤醒运营\n4. 加强西部地区的用户运营，缩小地区差异\n5. 建立用户分层运营体系，精细化管理"
    ),
    
    "inventory": DashboardTemplate(
        industry="电商",
        template_name="电商库存健康度&履约看板",
        template_id="inventory",
        description="库存周转、缺货率、发货时效等供应链关键指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="库存关键指标",
                description="库存周转、缺货率、发货时效、库存金额等指标",
                data_format={
                    "cards": [
                        {"title": "库存周转", "value": "8.5次/年", "change": "+1.2次"},
                        {"title": "缺货率", "value": "2.3%", "change": "-0.5%"},
                        {"title": "发货时效", "value": "12.5小时", "change": "-2.1小时"},
                        {"title": "库存金额", "value": "¥50,000,000", "change": "+5%"}
                    ]
                },
                insights="库存周转提升，缺货率下降，发货时效改善。库存管理效率显著提升。"
            ),
            ChartSpec(
                chart_type="clustered_bar",
                title="TOP缺货SKU",
                description="缺货最严重的TOP10 SKU，需要重点补货",
                data_format={
                    "categories": ["SKU001", "SKU002", "SKU003", "SKU004", "SKU005"],
                    "series": [{"name": "缺货天数", "data": [15, 12, 10, 8, 6]}]
                },
                insights="SKU001缺货15天，是最严重的缺货商品。建议立即补货，避免销售损失。"
            ),
            ChartSpec(
                chart_type="line",
                title="库存水位趋势",
                description="过去30天库存金额的走势",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [{"name": "库存金额", "data": [48000000, 49000000, 50000000, 51000000, 52000000]}]
                },
                insights="库存金额稳步上升，说明补货充足。建议监控库存水位，避免积压。"
            ),
            ChartSpec(
                chart_type="table",
                title="库存明细",
                description="各SKU的库存数量、周转率、缺货情况等详细数据",
                data_format={
                    "columns": ["SKU", "库存数", "周转率", "缺货天数", "补货计划"],
                    "rows": [
                        ["SKU001", "5,000", "8.5", "15", "立即补货"],
                        ["SKU002", "8,000", "9.2", "12", "本周补货"]
                    ]
                },
                insights="库存分布不均，部分SKU缺货严重。建议优化补货计划，提升库存周转。"
            )
        ],
        kpis=["库存周转", "缺货率", "发货时效", "库存金额"],
        insights="库存管理效率显著提升，库存周转达8.5次/年，缺货率仅2.3%，发货时效12.5小时。库存金额稳步上升，说明补货充足。",
        recommendations="1. 立即补货TOP缺货SKU，避免销售损失\n2. 优化补货计划，提升库存周转\n3. 建立库存预警机制，及时发现缺货\n4. 加强发货流程优化，进一步缩短发货时效\n5. 建立库存成本管理体系，降低库存占用资金"
    )
}

# ============================================================================
# 二、互联网/APP/游戏行业看板模板
# ============================================================================

INTERNET_TEMPLATES = {
    "dau_mau": DashboardTemplate(
        industry="互联网/APP/游戏",
        template_name="产品核心指标（DAU/MAU）看板",
        template_id="dau_mau",
        description="DAU、MAU、留存率、新增用户等产品核心指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="核心指标卡片",
                description="DAU、MAU、次日留存、7日留存等关键指标",
                data_format={
                    "cards": [
                        {"title": "DAU", "value": "5,234,567", "change": "+8.5%"},
                        {"title": "MAU", "value": "12,345,678", "change": "+6.2%"},
                        {"title": "次日留存", "value": "45.6%", "change": "+2.1%"},
                        {"title": "7日留存", "value": "32.1%", "change": "+1.8%"}
                    ]
                },
                insights="DAU和MAU均保持增长，次日留存和7日留存均有提升，说明产品粘性增强。"
            ),
            ChartSpec(
                chart_type="line",
                title="DAU趋势",
                description="过去30天DAU的走势，识别用户活跃度变化",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [{"name": "DAU", "data": [4800000, 5000000, 4900000, 5200000, 5400000]}]
                },
                insights="DAU呈上升趋势，周末活跃度明显高于工作日。建议周末加大运营投入。"
            ),
            ChartSpec(
                chart_type="line",
                title="新增趋势",
                description="过去30天新增用户的走势",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [{"name": "新增用户", "data": [100000, 120000, 110000, 130000, 150000]}]
                },
                insights="新增用户呈上升趋势，说明产品获客能力增强。建议继续加大营销投入。"
            ),
            ChartSpec(
                chart_type="waterfall",
                title="DAU波动拆解",
                description="DAU变化的驱动因素拆解，包括新增、留存、流失等",
                data_format={
                    "categories": ["前日DAU", "新增", "留存", "流失", "当日DAU"],
                    "values": [5000000, 200000, 4500000, -300000, 5400000]
                },
                insights="新增用户200万，留存用户450万，流失用户30万。新增和留存是DAU增长的主要驱动。"
            ),
            ChartSpec(
                chart_type="decomposition_tree",
                title="DAU下降根因分析",
                description="当DAU下降时，通过分解树快速定位根因",
                data_format={
                    "root": "DAU下降",
                    "children": [
                        {"name": "新增下降", "value": -50},
                        {"name": "留存下降", "value": -30},
                        {"name": "流失增加", "value": -20}
                    ]
                },
                insights="DAU下降主要由新增下降和留存下降导致。建议加大营销投入和优化产品体验。"
            ),
            ChartSpec(
                chart_type="clustered_bar",
                title="各版本/渠道新增对比",
                description="不同版本和渠道的新增用户对比",
                data_format={
                    "categories": ["iOS", "Android", "Web", "小程序"],
                    "series": [{"name": "新增用户", "data": [50000, 60000, 30000, 20000]}]
                },
                insights="Android新增最多（60万），iOS次之（50万）。建议加大Android和iOS的营销投入。"
            )
        ],
        kpis=["DAU", "MAU", "次日留存", "7日留存"],
        insights="产品核心指标保持增长，DAU增速8.5%，MAU增速6.2%。留存率稳步提升，说明产品粘性增强。新增用户增速快，获客能力强。",
        recommendations="1. 继续加大营销投入，提升新增用户\n2. 优化产品体验，提升留存率\n3. 加强Android和iOS的运营投入\n4. 建立用户分层运营体系，精细化管理\n5. 定期分析DAU波动原因，及时调整策略"
    ),
    
    "game_monetization": DashboardTemplate(
        industry="互联网/APP/游戏",
        template_name="游戏内购&付费分析看板",
        template_id="game_monetization",
        description="流水、ARPU、ARPPU、付费率等游戏商业化指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="商业化关键指标",
                description="流水、ARPU、ARPPU、付费率等指标",
                data_format={
                    "cards": [
                        {"title": "流水", "value": "¥50,000,000", "change": "+12.5%"},
                        {"title": "ARPU", "value": "¥9.54", "change": "+8.2%"},
                        {"title": "ARPPU", "value": "¥125.6", "change": "+6.5%"},
                        {"title": "付费率", "value": "7.6%", "change": "+0.8%"}
                    ]
                },
                insights="流水同比增长12.5%，ARPU和ARPPU均有提升，付费率达7.6%。商业化效果显著。"
            ),
            ChartSpec(
                chart_type="line",
                title="日流水趋势",
                description="过去30天日流水的走势",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [{"name": "日流水", "data": [1500000, 1600000, 1550000, 1700000, 1800000]}]
                },
                insights="日流水呈上升趋势，周末流水明显高于工作日。建议周末加大运营投入。"
            ),
            ChartSpec(
                chart_type="stacked_column",
                title="各道具收入构成",
                description="不同道具的收入占比",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [
                        {"name": "皮肤", "data": [600000, 700000, 650000, 800000, 900000]},
                        {"name": "武器", "data": [500000, 550000, 520000, 600000, 650000]},
                        {"name": "其他", "data": [400000, 350000, 380000, 300000, 250000]}
                    ]
                },
                insights="皮肤收入占比最高（50%），武器占比35%，其他占比15%。建议加大皮肤和武器的设计投入。"
            ),
            ChartSpec(
                chart_type="funnel",
                title="登录→活跃→付费转化",
                description="用户从登录到付费的完整转化链路",
                data_format={
                    "stages": ["登录", "活跃", "付费"],
                    "values": [5000000, 3000000, 230000]
                },
                insights="登录到活跃的转化率60%，活跃到付费的转化率7.6%。建议优化付费转化环节。"
            ),
            ChartSpec(
                chart_type="scatter",
                title="用户时长 vs 付费金额",
                description="用户游戏时长与付费金额的相关性",
                data_format={
                    "x": [10, 20, 30, 40, 50],
                    "y": [50, 100, 150, 200, 250],
                    "labels": ["低时长", "中低时长", "中时长", "中高时长", "高时长"]
                },
                insights="用户时长与付费金额呈正相关，高时长用户付费金额是低时长用户的5倍。"
            )
        ],
        kpis=["流水", "ARPU", "ARPPU", "付费率"],
        insights="游戏商业化效果显著，流水同比增长12.5%，ARPU和ARPPU均有提升。付费率达7.6%，说明付费转化能力强。皮肤和武器是主要收入来源。",
        recommendations="1. 加大皮肤和武器的设计投入，提升收入\n2. 优化付费转化环节，提升付费率\n3. 建立用户分层付费体系，精细化运营\n4. 加强高时长用户的付费激励\n5. 定期推出新皮肤和武器，保持用户热情"
    ),
    
    "ad_roi": DashboardTemplate(
        industry="互联网/APP/游戏",
        template_name="广告收益&投放ROI看板",
        template_id="ad_roi",
        description="广告收入、ECPM、点击率、转化率等广告变现指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="广告关键指标",
                description="广告收入、ECPM、点击率、转化率等指标",
                data_format={
                    "cards": [
                        {"title": "广告收入", "value": "¥30,000,000", "change": "+15.2%"},
                        {"title": "ECPM", "value": "¥5.8", "change": "+8.5%"},
                        {"title": "点击率", "value": "3.2%", "change": "+0.5%"},
                        {"title": "转化率", "value": "2.1%", "change": "+0.3%"}
                    ]
                },
                insights="广告收入同比增长15.2%，ECPM提升8.5%，说明广告变现能力增强。"
            ),
            ChartSpec(
                chart_type="combo",
                title="消耗(柱形)+ROI(折线)",
                description="广告消耗和ROI的变化趋势",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "columns": {"name": "消耗", "data": [1000000, 1100000, 1050000, 1200000, 1300000]},
                    "lines": {"name": "ROI", "data": [3.2, 3.5, 3.4, 3.8, 4.0]}
                },
                insights="广告消耗增加，ROI也在提升，说明广告投放效率提高。建议继续加大投放。"
            ),
            ChartSpec(
                chart_type="clustered_bar",
                title="广告位收益TOP",
                description="不同广告位的收益排名",
                data_format={
                    "categories": ["首页横幅", "信息流", "视频前贴", "激励视频", "其他"],
                    "series": [{"name": "收益", "data": [10000000, 8000000, 6000000, 4000000, 2000000]}]
                },
                insights="首页横幅收益最高（33%），信息流次之（27%）。建议加大这两个广告位的投放。"
            ),
            ChartSpec(
                chart_type="bubble",
                title="广告计划效果三维对比",
                description="广告计划的消耗、点击、转化三维对比",
                data_format={
                    "x": [100000, 150000, 120000, 180000, 200000],
                    "y": [3000, 4500, 3600, 5400, 6000],
                    "size": [50, 75, 60, 90, 100],
                    "labels": ["计划A", "计划B", "计划C", "计划D", "计划E"]
                },
                insights="计划E效果最好，消耗最高但转化也最高。建议加大计划E的投放。"
            )
        ],
        kpis=["广告收入", "ECPM", "点击率", "转化率"],
        insights="广告变现效果显著，收入同比增长15.2%，ECPM提升8.5%。首页横幅和信息流是主要收入来源。广告投放ROI持续提升。",
        recommendations="1. 加大首页横幅和信息流的投放\n2. 优化广告创意，提升点击率和转化率\n3. 建立广告投放ROI监控体系\n4. 定期分析广告效果，优化投放策略\n5. 加强与广告主的合作，提升ECPM"
    )
}

# ============================================================================
# 三、金融行业看板模板
# ============================================================================

FINANCE_TEMPLATES = {
    "retail_aum": DashboardTemplate(
        industry="金融",
        template_name="零售客户资产&行为看板",
        template_id="retail_aum",
        description="AUM、客户数、户均资产等零售金融关键指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="资产关键指标",
                description="AUM、客户数、户均资产等指标",
                data_format={
                    "cards": [
                        {"title": "AUM", "value": "¥500,000,000,000", "change": "+8.5%"},
                        {"title": "客户数", "value": "5,234,567", "change": "+6.2%"},
                        {"title": "户均资产", "value": "¥95,600", "change": "+2.1%"},
                        {"title": "活跃客户", "value": "2,345,678", "change": "+4.5%"}
                    ]
                },
                insights="AUM同比增长8.5%，客户数增速6.2%，户均资产稳步提升。资产管理规模持续增长。"
            ),
            ChartSpec(
                chart_type="line",
                title="AUM趋势",
                description="过去12个月AUM的走势",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [{"name": "AUM", "data": [460000000000, 475000000000, 485000000000, 500000000000, 520000000000]}]
                },
                insights="AUM呈稳步上升趋势，说明资产管理规模持续增长。建议继续加强客户服务。"
            ),
            ChartSpec(
                chart_type="treemap",
                title="客户分层资产占比",
                description="不同客户等级的资产占比",
                data_format={
                    "labels": ["VIP客户", "高净值客户", "普通客户", "新客户"],
                    "sizes": [250000000000, 150000000000, 80000000000, 20000000000],
                    "colors": [1, 2, 3, 4]
                },
                insights="VIP客户占比50%，是主要资产来源。建议加强VIP客户的服务和维护。"
            ),
            ChartSpec(
                chart_type="donut",
                title="产品渗透率",
                description="不同产品的客户渗透率",
                data_format={
                    "labels": ["理财产品", "基金", "保险", "其他"],
                    "values": [45, 30, 20, 5]
                },
                insights="理财产品渗透率最高（45%），基金次之（30%）。建议加大基金和保险的推广。"
            ),
            ChartSpec(
                chart_type="matrix",
                title="地区×产品×资产规模",
                description="不同地区和产品的资产规模分布",
                data_format={
                    "rows": ["华东", "华北", "华南", "西部"],
                    "columns": ["理财", "基金", "保险", "其他"],
                    "values": [
                        [150, 100, 50, 10],
                        [120, 80, 40, 8],
                        [100, 60, 30, 6],
                        [80, 40, 20, 4]
                    ]
                },
                insights="华东地区资产规模最大，西部地区最小。建议加强西部地区的市场开拓。"
            )
        ],
        kpis=["AUM", "客户数", "户均资产", "活跃客户"],
        insights="零售资产管理规模持续增长，AUM同比增长8.5%，客户数增速6.2%。VIP客户占比50%，是主要资产来源。理财产品是主要产品。",
        recommendations="1. 加强VIP客户的服务和维护，提升客户粘性\n2. 加大基金和保险的推广，提升产品渗透率\n3. 加强西部地区的市场开拓，扩大客户基数\n4. 建立客户分层运营体系，精细化管理\n5. 优化产品结构，提升户均资产"
    ),
    
    "insurance": DashboardTemplate(
        industry="金融",
        template_name="保险保费&理赔&渠道看板",
        template_id="insurance",
        description="保费、赔付率、续保率等保险业务关键指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="保险业务指标",
                description="总保费、赔付率、续保率等指标",
                data_format={
                    "cards": [
                        {"title": "总保费", "value": "¥50,000,000,000", "change": "+12.5%"},
                        {"title": "赔付率", "value": "65.3%", "change": "-2.1%"},
                        {"title": "续保率", "value": "78.5%", "change": "+3.2%"},
                        {"title": "新单保费", "value": "¥8,000,000,000", "change": "+15.8%"}
                    ]
                },
                insights="总保费同比增长12.5%，赔付率下降，续保率提升。保险业务经营良好。"
            ),
            ChartSpec(
                chart_type="stacked_column",
                title="各险种保费构成",
                description="不同险种的保费占比",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [
                        {"name": "寿险", "data": [20000000000, 21000000000, 22000000000, 23000000000, 24000000000]},
                        {"name": "财险", "data": [15000000000, 15500000000, 16000000000, 16500000000, 17000000000]},
                        {"name": "健康险", "data": [10000000000, 10500000000, 11000000000, 11500000000, 12000000000]},
                        {"name": "其他", "data": [5000000000, 5000000000, 5000000000, 5000000000, 5000000000]}
                    ]
                },
                insights="寿险占比最高（48%），财险占比34%，健康险占比24%。建议加大健康险的推广。"
            ),
            ChartSpec(
                chart_type="line",
                title="保费趋势",
                description="过去12个月保费的走势",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [{"name": "保费", "data": [50000000000, 52000000000, 54000000000, 56000000000, 58000000000]}]
                },
                insights="保费呈稳步上升趋势，说明保险业务持续增长。建议继续加大营销投入。"
            ),
            ChartSpec(
                chart_type="funnel",
                title="投保全流程转化",
                description="从浏览到投保的完整转化链路",
                data_format={
                    "stages": ["浏览", "咨询", "投保", "支付"],
                    "values": [1000000, 500000, 250000, 200000]
                },
                insights="浏览到咨询的转化率50%，咨询到投保的转化率50%，投保到支付的转化率80%。"
            ),
            ChartSpec(
                chart_type="table",
                title="机构业绩排行",
                description="各机构的保费排行和增速",
                data_format={
                    "columns": ["机构", "保费", "增速", "赔付率", "续保率"],
                    "rows": [
                        ["华东分公司", "¥20,000,000,000", "+15.2%", "63.2%", "80.1%"],
                        ["华北分公司", "¥15,000,000,000", "+12.5%", "65.8%", "78.5%"]
                    ]
                },
                insights="华东分公司业绩最好，保费最高，增速最快。建议推广华东分公司的经验。"
            )
        ],
        kpis=["总保费", "赔付率", "续保率", "新单保费"],
        insights="保险业务经营良好，总保费同比增长12.5%，赔付率下降，续保率提升。寿险是主要业务，健康险增速最快。华东分公司业绩最好。",
        recommendations="1. 加大健康险的推广，抓住增长机遇\n2. 优化投保流程，提升转化率\n3. 加强续保管理，提升续保率\n4. 推广华东分公司的经验，提升整体业绩\n5. 建立机构分层管理体系，精细化运营"
    ),
    
    "risk_control": DashboardTemplate(
        industry="金融",
        template_name="交易风险&异常监控看板",
        template_id="risk_control",
        description="异常笔数、拦截率、损失金额等风控关键指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="风控关键指标",
                description="异常笔数、拦截率、损失金额等指标",
                data_format={
                    "cards": [
                        {"title": "异常笔数", "value": "12,345", "change": "-5.2%"},
                        {"title": "拦截率", "value": "98.5%", "change": "+0.3%"},
                        {"title": "损失金额", "value": "¥1,234,567", "change": "-12.5%"},
                        {"title": "风险等级", "value": "低", "change": "稳定"}
                    ]
                },
                insights="异常笔数下降，拦截率提升，损失金额下降。风控效果显著。"
            ),
            ChartSpec(
                chart_type="line",
                title="交易趋势&异常检测",
                description="交易趋势和异常点标注",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [{"name": "交易笔数", "data": [1000000, 1100000, 1050000, 1200000, 1300000]}],
                    "anomalies": [3]
                },
                insights="3月4日出现异常交易高峰，已被风控系统拦截。建议加强监控。"
            ),
            ChartSpec(
                chart_type="filled_map",
                title="全国风险分布",
                description="不同地区的风险分布热力",
                data_format={
                    "regions": ["北京", "上海", "广州", "深圳", "杭州"],
                    "values": [100, 80, 60, 40, 20]
                },
                insights="北京风险最高，深圳风险最低。建议加强北京地区的风控监控。"
            ),
            ChartSpec(
                chart_type="key_influencers",
                title="风险驱动因子",
                description="影响风险的关键因子及权重",
                data_format={
                    "factors": ["交易金额", "交易频率", "地理位置", "设备信息"],
                    "weights": [0.35, 0.30, 0.20, 0.15]
                },
                insights="交易金额是最主要的风险因子（35%），交易频率次之（30%）。建议重点监控这两个因子。"
            )
        ],
        kpis=["异常笔数", "拦截率", "损失金额", "风险等级"],
        insights="风控效果显著，异常笔数下降5.2%，拦截率达98.5%，损失金额下降12.5%。北京地区风险最高，需要加强监控。",
        recommendations="1. 加强北京地区的风控监控，降低风险\n2. 优化风控模型，提升拦截率\n3. 建立风险预警机制，及时发现异常\n4. 加强交易金额和交易频率的监控\n5. 定期分析风险驱动因子，优化风控策略"
    )
}

# ============================================================================
# 其他行业看板模板（制造、零售、HR、财务）
# ============================================================================

MANUFACTURING_TEMPLATES = {
    "production_oee": DashboardTemplate(
        industry="制造",
        template_name="工厂生产效率&OEE看板",
        template_id="production_oee",
        description="产量、合格率、OEE、停机时间等生产关键指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="生产关键指标",
                description="产量、合格率、OEE、停机时间等指标",
                data_format={
                    "cards": [
                        {"title": "日产量", "value": "12,345件", "change": "+8.5%"},
                        {"title": "合格率", "value": "98.5%", "change": "+0.3%"},
                        {"title": "OEE", "value": "85.2%", "change": "+2.1%"},
                        {"title": "停机时间", "value": "2.5小时", "change": "-0.5小时"}
                    ]
                },
                insights="产量增加，合格率和OEE均有提升，停机时间下降。生产效率显著提升。"
            ),
            ChartSpec(
                chart_type="line",
                title="小时产量趋势",
                description="过去24小时的小时产量走势",
                data_format={
                    "categories": ["0点", "4点", "8点", "12点", "16点", "20点"],
                    "series": [{"name": "小时产量", "data": [500, 480, 520, 550, 530, 510]}]
                },
                insights="产量在12点达到高峰（550件），建议在高峰时段加强质量控制。"
            ),
            ChartSpec(
                chart_type="clustered_column",
                title="产线产量对比",
                description="不同产线的产量对比",
                data_format={
                    "categories": ["产线A", "产线B", "产线C", "产线D"],
                    "series": [{"name": "产量", "data": [3500, 3200, 2800, 2500]}]
                },
                insights="产线A产量最高，产线D产量最低。建议优化产线D的生产流程。"
            ),
            ChartSpec(
                chart_type="gauge",
                title="OEE达成率",
                description="OEE目标达成情况",
                data_format={
                    "title": "OEE达成率",
                    "value": 85,
                    "min": 0,
                    "max": 100
                },
                insights="OEE达成率85%，接近目标（90%）。建议继续优化生产流程。"
            ),
            ChartSpec(
                chart_type="stacked_bar",
                title="停机原因分布",
                description="不同停机原因的分布",
                data_format={
                    "categories": ["设备故障", "人员问题", "物料缺乏", "其他"],
                    "series": [{"name": "停机时间", "data": [1.0, 0.8, 0.5, 0.2]}]
                },
                insights="设备故障是主要停机原因（40%），建议加强设备维护。"
            )
        ],
        kpis=["日产量", "合格率", "OEE", "停机时间"],
        insights="生产效率显著提升，日产量增加8.5%，合格率达98.5%，OEE达85.2%。停机时间下降，说明设备运行状况良好。",
        recommendations="1. 加强设备维护，减少设备故障停机\n2. 优化产线D的生产流程，提升产量\n3. 在高峰时段加强质量控制\n4. 建立生产效率监控体系，及时发现问题\n5. 制定OEE提升计划，目标达到90%"
    ),
    
    "supply_chain": DashboardTemplate(
        industry="制造",
        template_name="供应链物流&在途监控看板",
        template_id="supply_chain",
        description="发货量、准时率、在途库存等物流关键指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="物流关键指标",
                description="发货量、准时率、在途库存等指标",
                data_format={
                    "cards": [
                        {"title": "发货量", "value": "50,000件", "change": "+12.5%"},
                        {"title": "准时率", "value": "95.2%", "change": "+1.5%"},
                        {"title": "在途库存", "value": "¥50,000,000", "change": "+8.2%"},
                        {"title": "平均运输时间", "value": "3.5天", "change": "-0.5天"}
                    ]
                },
                insights="发货量增加，准时率提升，运输时间缩短。物流效率显著提升。"
            ),
            ChartSpec(
                chart_type="azure_map",
                title="全国物流节点分布",
                description="全国物流节点的分布情况",
                data_format={
                    "regions": ["华东", "华北", "华南", "西部"],
                    "values": [200, 150, 120, 80]
                },
                insights="华东地区物流节点最多，西部地区最少。建议加强西部地区的物流布局。"
            ),
            ChartSpec(
                chart_type="ribbon",
                title="仓库发货排名变化",
                description="不同仓库的发货排名变化",
                data_format={
                    "categories": ["上周", "本周"],
                    "series": [
                        {"name": "仓库A", "data": [1, 1]},
                        {"name": "仓库B", "data": [2, 3]},
                        {"name": "仓库C", "data": [3, 2]}
                    ]
                },
                insights="仓库A排名稳定，仓库B和C排名有所变化。建议加强仓库B的管理。"
            ),
            ChartSpec(
                chart_type="table",
                title="在途订单明细",
                description="当前在途订单的详细信息",
                data_format={
                    "columns": ["订单号", "发货地", "目的地", "发货时间", "预计到达"],
                    "rows": [
                        ["ORD001", "上海", "北京", "2026-03-26", "2026-03-29"],
                        ["ORD002", "深圳", "广州", "2026-03-26", "2026-03-27"]
                    ]
                },
                insights="大部分订单预计按时到达，建议继续加强物流管理。"
            )
        ],
        kpis=["发货量", "准时率", "在途库存", "平均运输时间"],
        insights="物流效率显著提升，发货量增加12.5%，准时率达95.2%，运输时间缩短0.5天。华东地区物流节点最多，是主要物流枢纽。",
        recommendations="1. 加强西部地区的物流布局，提升覆盖范围\n2. 加强仓库B的管理，提升发货效率\n3. 优化物流路线，进一步缩短运输时间\n4. 建立物流监控体系，及时发现问题\n5. 加强与物流合作伙伴的沟通，提升服务质量"
    )
}

RETAIL_TEMPLATES = {
    "store_performance": DashboardTemplate(
        industry="零售",
        template_name="连锁门店业绩&客流看板",
        template_id="store_performance",
        description="销售额、客流、客单价、连带率等门店关键指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="门店关键指标",
                description="销售额、客流、客单价、连带率等指标",
                data_format={
                    "cards": [
                        {"title": "销售额", "value": "¥50,000,000", "change": "+15.2%"},
                        {"title": "客流", "value": "1,234,567", "change": "+12.5%"},
                        {"title": "客单价", "value": "¥40.5", "change": "+2.1%"},
                        {"title": "连带率", "value": "2.3", "change": "+0.2"}
                    ]
                },
                insights="销售额同比增长15.2%，客流增加12.5%，客单价和连带率均有提升。门店业绩良好。"
            ),
            ChartSpec(
                chart_type="line",
                title="日销趋势",
                description="过去30天的日销走势",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [{"name": "日销", "data": [1500000, 1600000, 1550000, 1700000, 1800000]}]
                },
                insights="日销呈上升趋势，周末销售明显高于工作日。建议周末加大营销投入。"
            ),
            ChartSpec(
                chart_type="clustered_bar",
                title="TOP门店销售额",
                description="销售额TOP10门店的排名",
                data_format={
                    "categories": ["门店A", "门店B", "门店C", "门店D", "门店E"],
                    "series": [{"name": "销售额", "data": [5000000, 4500000, 4000000, 3500000, 3000000]}]
                },
                insights="门店A销售额最高，门店E最低。建议推广门店A的经验到其他门店。"
            ),
            ChartSpec(
                chart_type="filled_map",
                title="全国门店销售热力",
                description="全国门店销售额的地理分布",
                data_format={
                    "regions": ["华东", "华北", "华南", "西部"],
                    "values": [20000000, 15000000, 10000000, 5000000]
                },
                insights="华东地区销售额最高，西部地区最低。建议加强西部地区的门店运营。"
            ),
            ChartSpec(
                chart_type="donut",
                title="支付方式占比",
                description="不同支付方式的占比",
                data_format={
                    "labels": ["现金", "刷卡", "手机支付", "其他"],
                    "values": [30, 25, 40, 5]
                },
                insights="手机支付占比最高（40%），现金占比30%。建议加强手机支付的推广。"
            )
        ],
        kpis=["销售额", "客流", "客单价", "连带率"],
        insights="门店业绩良好，销售额同比增长15.2%，客流增加12.5%。华东地区销售额最高，是主要销售区域。手机支付是主要支付方式。",
        recommendations="1. 推广门店A的经验到其他门店，提升整体业绩\n2. 加强西部地区的门店运营，缩小地区差异\n3. 周末加大营销投入，抓住销售高峰\n4. 优化支付体验，提升手机支付占比\n5. 建立门店分层管理体系，精细化运营"
    ),
    
    "category_analysis": DashboardTemplate(
        industry="零售",
        template_name="快消品类动销&毛利看板",
        template_id="category_analysis",
        description="动销率、毛利率、库存周转等品类关键指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="品类关键指标",
                description="动销率、毛利率、库存周转等指标",
                data_format={
                    "cards": [
                        {"title": "动销率", "value": "85.2%", "change": "+3.5%"},
                        {"title": "毛利率", "value": "32.1%", "change": "+1.2%"},
                        {"title": "库存周转", "value": "6.5次/年", "change": "+0.8次"},
                        {"title": "滞销品数", "value": "234", "change": "-45"}
                    ]
                },
                insights="动销率提升，毛利率增加，库存周转加快。品类管理效率显著提升。"
            ),
            ChartSpec(
                chart_type="combo",
                title="销量(柱形)+毛利(折线)",
                description="销量和毛利的变化趋势",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "columns": {"name": "销量", "data": [100000, 110000, 105000, 120000, 130000]},
                    "lines": {"name": "毛利", "data": [30, 32, 31, 33, 35]}
                },
                insights="销量和毛利均呈上升趋势，说明品类经营良好。建议继续加大投入。"
            ),
            ChartSpec(
                chart_type="treemap",
                title="品类结构占比",
                description="不同品类的销售额占比",
                data_format={
                    "labels": ["食品", "饮料", "日化", "其他"],
                    "sizes": [400000, 300000, 200000, 100000],
                    "colors": [1, 2, 3, 4]
                },
                insights="食品品类占比最高（40%），饮料占比30%。建议加大食品品类的投入。"
            ),
            ChartSpec(
                chart_type="table",
                title="滞销品清单",
                description="滞销品的详细信息，需要清理",
                data_format={
                    "columns": ["品名", "库存", "滞销天数", "建议处理"],
                    "rows": [
                        ["滞销品A", "500件", "60天", "打折清理"],
                        ["滞销品B", "300件", "45天", "促销处理"]
                    ]
                },
                insights="滞销品A滞销60天，建议立即打折清理，避免积压。"
            )
        ],
        kpis=["动销率", "毛利率", "库存周转", "滞销品数"],
        insights="品类管理效率显著提升，动销率达85.2%，毛利率32.1%，库存周转6.5次/年。食品品类是主要品类，占比40%。滞销品数量下降45个。",
        recommendations="1. 立即处理滞销品，避免积压\n2. 加大食品品类的投入，抓住增长机遇\n3. 优化品类结构，提升整体毛利\n4. 建立品类分层管理体系，精细化运营\n5. 定期分析品类动销情况，及时调整策略"
    )
}

HR_TEMPLATES = {
    "hr_structure": DashboardTemplate(
        industry="HR",
        template_name="人力规模&结构看板",
        template_id="hr_structure",
        description="总人数、入职率、离职率、人均效能等HR关键指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="人力关键指标",
                description="总人数、入职率、离职率、人均效能等指标",
                data_format={
                    "cards": [
                        {"title": "总人数", "value": "12,345", "change": "+5.2%"},
                        {"title": "入职率", "value": "8.5%", "change": "+1.2%"},
                        {"title": "离职率", "value": "3.2%", "change": "-0.5%"},
                        {"title": "人均效能", "value": "¥500,000", "change": "+8.5%"}
                    ]
                },
                insights="总人数增加，入职率提升，离职率下降。人力规模和质量均有提升。"
            ),
            ChartSpec(
                chart_type="line",
                title="人数趋势",
                description="过去12个月的人数走势",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [{"name": "总人数", "data": [11500, 11700, 11900, 12100, 12345]}]
                },
                insights="人数呈稳步增长趋势，说明公司在持续扩张。建议继续加强招聘。"
            ),
            ChartSpec(
                chart_type="treemap",
                title="部门人员结构",
                description="不同部门的人员分布",
                data_format={
                    "labels": ["销售部", "技术部", "运营部", "财务部", "其他"],
                    "sizes": [4000, 3500, 2500, 1500, 845],
                    "colors": [1, 2, 3, 4, 5]
                },
                insights="销售部人数最多（32%），技术部次之（28%）。建议加强技术部的招聘。"
            ),
            ChartSpec(
                chart_type="matrix",
                title="部门×职级×人数",
                description="不同部门和职级的人员分布",
                data_format={
                    "rows": ["销售部", "技术部", "运营部", "财务部"],
                    "columns": ["总监", "经理", "主管", "员工"],
                    "values": [
                        [2, 5, 10, 3983],
                        [2, 4, 8, 3486],
                        [1, 3, 6, 2490],
                        [1, 2, 4, 1493]
                    ]
                },
                insights="各部门人员结构合理，员工占比最高。建议加强中层管理人员的培养。"
            )
        ],
        kpis=["总人数", "入职率", "离职率", "人均效能"],
        insights="人力规模和质量均有提升，总人数增加5.2%，入职率提升，离职率下降。销售部和技术部是主要部门。人均效能达¥500,000。",
        recommendations="1. 继续加强招聘，特别是技术部的招聘\n2. 加强中层管理人员的培养，提升管理能力\n3. 优化人员结构，提升人均效能\n4. 建立人力分层管理体系，精细化运营\n5. 加强员工发展和培训，提升员工满意度"
    ),
    
    "recruitment": DashboardTemplate(
        industry="HR",
        template_name="招聘漏斗&渠道效率看板",
        template_id="recruitment",
        description="offer数、入职数、到岗率等招聘关键指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="招聘关键指标",
                description="offer数、入职数、到岗率等指标",
                data_format={
                    "cards": [
                        {"title": "Offer数", "value": "1,234", "change": "+15.2%"},
                        {"title": "入职数", "value": "1,000", "change": "+12.5%"},
                        {"title": "到岗率", "value": "81.1%", "change": "+2.1%"},
                        {"title": "平均招聘周期", "value": "25天", "change": "-3天"}
                    ]
                },
                insights="Offer数和入职数均增加，到岗率提升，招聘周期缩短。招聘效率显著提升。"
            ),
            ChartSpec(
                chart_type="funnel",
                title="简历→面试→offer→入职",
                description="招聘全流程的转化漏斗",
                data_format={
                    "stages": ["简历", "面试", "Offer", "入职"],
                    "values": [10000, 3000, 1234, 1000]
                },
                insights="简历到面试的转化率30%，面试到Offer的转化率41%，Offer到入职的转化率81%。"
            ),
            ChartSpec(
                chart_type="clustered_bar",
                title="招聘渠道效果对比",
                description="不同招聘渠道的效果对比",
                data_format={
                    "categories": ["校园招聘", "社会招聘", "内部推荐", "猎头"],
                    "series": [{"name": "入职数", "data": [300, 400, 200, 100]}]
                },
                insights="社会招聘入职数最多（400），校园招聘次之（300）。建议加大社会招聘的投入。"
            )
        ],
        kpis=["Offer数", "入职数", "到岗率", "平均招聘周期"],
        insights="招聘效率显著提升，Offer数增加15.2%，入职数增加12.5%，到岗率达81.1%。社会招聘是主要招聘渠道。平均招聘周期缩短3天。",
        recommendations="1. 加大社会招聘的投入，提升入职数\n2. 优化招聘流程，进一步缩短招聘周期\n3. 加强校园招聘，培养后备人才\n4. 建立招聘渠道评估体系，优化渠道组合\n5. 加强入职后的培训和融入，提升到岗率"
    )
}

FINANCE_TEMPLATES_GENERAL = {
    "profit_overview": DashboardTemplate(
        industry="财务",
        template_name="营收利润&费用总览",
        template_id="profit_overview",
        description="收入、成本、利润、同比等财务关键指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="财务关键指标",
                description="收入、成本、利润、同比等指标",
                data_format={
                    "cards": [
                        {"title": "收入", "value": "¥500,000,000", "change": "+15.2%"},
                        {"title": "成本", "value": "¥300,000,000", "change": "+12.5%"},
                        {"title": "利润", "value": "¥200,000,000", "change": "+18.5%"},
                        {"title": "利润率", "value": "40%", "change": "+1.2%"}
                    ]
                },
                insights="收入同比增长15.2%，成本增长12.5%，利润增长18.5%。财务表现良好。"
            ),
            ChartSpec(
                chart_type="waterfall",
                title="利润构成（收入-成本-费用）",
                description="利润的完整构成拆解",
                data_format={
                    "categories": ["收入", "成本", "费用", "利润"],
                    "values": [500000000, -300000000, -100000000, 100000000]
                },
                insights="收入500M，成本300M，费用100M，最终利润100M。利润率20%。"
            ),
            ChartSpec(
                chart_type="line",
                title="月度利润趋势",
                description="过去12个月的利润走势",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [{"name": "利润", "data": [80000000, 85000000, 90000000, 95000000, 100000000]}]
                },
                insights="利润呈稳步上升趋势，说明经营效率持续提升。建议继续优化成本。"
            ),
            ChartSpec(
                chart_type="stacked_column",
                title="各业务线利润贡献",
                description="不同业务线的利润占比",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [
                        {"name": "业务线A", "data": [40000000, 42000000, 45000000, 48000000, 50000000]},
                        {"name": "业务线B", "data": [30000000, 31000000, 32000000, 33000000, 35000000]},
                        {"name": "业务线C", "data": [10000000, 12000000, 13000000, 14000000, 15000000]}
                    ]
                },
                insights="业务线A利润占比最高（50%），业务线B占比35%，业务线C占比15%。"
            ),
            ChartSpec(
                chart_type="matrix",
                title="子公司×月份×利润",
                description="不同子公司的利润分布",
                data_format={
                    "rows": ["子公司A", "子公司B", "子公司C", "子公司D"],
                    "columns": ["3月", "4月", "5月", "6月"],
                    "values": [
                        [40, 42, 45, 48],
                        [30, 31, 32, 33],
                        [10, 12, 13, 14],
                        [5, 6, 7, 8]
                    ]
                },
                insights="子公司A利润最高，子公司D最低。建议加强子公司D的管理。"
            )
        ],
        kpis=["收入", "成本", "利润", "利润率"],
        insights="财务表现良好，收入同比增长15.2%，利润增长18.5%。业务线A是主要利润来源。利润率达40%。",
        recommendations="1. 继续优化成本，提升利润率\n2. 加强业务线C的发展，提升利润贡献\n3. 加强子公司D的管理，提升整体利润\n4. 建立财务分层管理体系，精细化运营\n5. 定期分析财务数据，及时调整策略"
    ),
    
    "budget_execution": DashboardTemplate(
        industry="财务",
        template_name="预算执行&费用控制看板",
        template_id="budget_execution",
        description="预算达成率、费用控制等预算关键指标",
        charts=[
            ChartSpec(
                chart_type="kpi",
                title="各部门预算达成率",
                description="各部门的预算达成情况",
                data_format={
                    "title": "销售部预算达成率",
                    "current": 85,
                    "target": 100,
                    "unit": "%"
                },
                insights="销售部预算达成率85%，接近目标。建议继续加强执行。"
            ),
            ChartSpec(
                chart_type="combo",
                title="预算(柱形)+实际(折线)",
                description="预算和实际支出的对比",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "columns": {"name": "预算", "data": [100000000, 105000000, 110000000, 115000000, 120000000]},
                    "lines": {"name": "实际", "data": [95000000, 100000000, 105000000, 110000000, 115000000]}
                },
                insights="实际支出略低于预算，说明费用控制良好。建议继续保持。"
            ),
            ChartSpec(
                chart_type="gauge",
                title="费用健康度",
                description="费用支出的健康度评分",
                data_format={
                    "title": "费用健康度",
                    "value": 75,
                    "min": 0,
                    "max": 100
                },
                insights="费用健康度75分，处于良好水平。建议继续加强费用管理。"
            )
        ],
        kpis=["预算达成率", "费用支出", "费用健康度"],
        insights="预算执行良好，各部门预算达成率均在85%以上。实际支出略低于预算，说明费用控制有效。费用健康度75分。",
        recommendations="1. 继续加强费用管理，提升预算达成率\n2. 建立费用预警机制，及时发现超支\n3. 加强部门间的沟通，优化预算分配\n4. 定期分析费用数据，优化支出结构\n5. 建立费用分层管理体系，精细化运营"
    )
}

# ============================================================================
# 十、文娱内容产业看板模板（IP运营）
# ============================================================================

ENTERTAINMENT_TEMPLATES = {
    "content_overview": DashboardTemplate(
        industry="文娱",
        template_name="内容全域经营&流量价值总览看板",
        template_id="content_overview",
        description="内容生产效率、流量分发、商业化变现全景监控，适用于短视频/长视频平台、MCN机构、IP运营公司",
        charts=[
            ChartSpec(
                chart_type="multi_card",
                title="核心指标卡片",
                description="总播放量、总点赞量、总评论量、总分享量、内容发布数、爆款内容数",
                data_format={
                    "cards": [
                        {"title": "总播放量", "value": "12,345,678,900", "change": "+25.5%"},
                        {"title": "总点赞量", "value": "234,567,890", "change": "+18.2%"},
                        {"title": "总评论量", "value": "45,678,901", "change": "+12.3%"},
                        {"title": "总分享量", "value": "12,345,678", "change": "+35.6%"},
                        {"title": "内容发布数", "value": "125,678", "change": "+15.2%"},
                        {"title": "爆款内容数", "value": "2,345", "change": "+42.1%"}
                    ]
                },
                insights="核心流量指标全面增长，播放量增长25.5%，爆款内容数增长42.1%，内容运营效果显著。"
            ),
            ChartSpec(
                chart_type="line",
                title="日播放量趋势",
                description="过去30天日播放量走势，识别内容热度周期",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [{"name": "播放量", "data": [400000000, 420000000, 410000000, 450000000, 480000000]}]
                },
                insights="周末播放量明显高于工作日，周五-周六为内容消费高峰。建议周末加大内容投放。"
            ),
            ChartSpec(
                chart_type="line",
                title="日活跃创作者数趋势",
                description="过去30天活跃创作者数量变化",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [{"name": "活跃创作者", "data": [85000, 90000, 88000, 95000, 100000]}]
                },
                insights="活跃创作者数量持续增长，增速达17.6%，说明平台创作者生态活跃。"
            ),
            ChartSpec(
                chart_type="clustered_column",
                title="各内容品类播放量TOP10",
                description="搞笑、剧情、知识、游戏等品类的播放量排名",
                data_format={
                    "categories": ["搞笑", "剧情", "知识", "游戏", "音乐", "美食", "旅行", "科技", "情感", "生活"],
                    "series": [{"name": "播放量", "data": [2500000000, 2000000000, 1500000000, 1200000000, 1000000000, 800000000, 600000000, 500000000, 400000000, 300000000]}]
                },
                insights="搞笑品类播放量最高（25亿），剧情品类次之（20亿）。知识品类增速最快（+35%），建议加大投入。"
            ),
            ChartSpec(
                chart_type="stacked_column",
                title="流量来源构成",
                description="自然推荐、付费推广、社交分享、站内跳转的流量占比",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [
                        {"name": "自然推荐", "data": [280000000, 300000000, 290000000, 320000000, 340000000]},
                        {"name": "付费推广", "data": [70000000, 75000000, 72000000, 80000000, 85000000]},
                        {"name": "社交分享", "data": [35000000, 38000000, 36000000, 40000000, 42000000]},
                        {"name": "站内跳转", "data": [15000000, 17000000, 16000000, 18000000, 19000000]}
                    ]
                },
                insights="自然推荐占比70%，是主要流量来源。付费推广占比18%，社交分享占比9%。"
            ),
            ChartSpec(
                chart_type="donut",
                title="内容互动率分布",
                description="高/中/低互动等级的内容占比",
                data_format={
                    "labels": ["高互动(>5%)", "中互动(1-5%)", "低互动(<1%)"],
                    "values": [25, 45, 30]
                },
                insights="高互动内容占比25%，说明优质内容占比不错。建议提升高互动内容的产出比例。"
            ),
            ChartSpec(
                chart_type="table",
                title="爆款内容TOP20明细",
                description="播放量超100万的内容详细数据",
                data_format={
                    "columns": ["标题", "播放量", "点赞", "评论", "分享", "带货GMV"],
                    "rows": [
                        ["爆款视频A", "5000万", "250万", "12万", "8万", "¥50万"],
                        ["爆款视频B", "4500万", "220万", "10万", "7万", "¥45万"]
                    ]
                },
                insights="TOP20爆款内容占总播放量的30%，集中度较高。带货GMV表现优异，平均单内容GMV达¥45万。"
            )
        ],
        kpis=["总播放量", "总互动量", "内容发布数", "爆款内容数", "内容总GMV"],
        insights="内容全域经营效果显著，播放量增长25.5%，爆款内容数增长42.1%。创作者生态活跃，自然推荐是主要流量来源。",
        recommendations="1. 加大知识品类内容投入，抓住增长机遇\n2. 优化内容推荐算法，提升自然推荐占比\n3. 建立爆款内容生产机制，提升高互动内容占比\n4. 加强创作者运营，提升活跃创作者数量\n5. 优化带货转化链路，提升内容变现效率"
    ),
    
    "creator_ecosystem": DashboardTemplate(
        industry="文娱",
        template_name="创作者生态&运营效率看板",
        template_id="creator_ecosystem",
        description="创作者数量、产出效率、留存率、收益分成等创作者运营核心指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="创作者关键指标",
                description="活跃创作者数、新增创作者数、人均产出内容数、创作者留存率",
                data_format={
                    "cards": [
                        {"title": "活跃创作者", "value": "100,000", "change": "+17.6%"},
                        {"title": "新增创作者", "value": "15,000", "change": "+25.2%"},
                        {"title": "人均产出", "value": "8.5条/月", "change": "+5.3%"},
                        {"title": "创作者留存率", "value": "72.5%", "change": "+3.2%"}
                    ]
                },
                insights="创作者生态活跃，活跃创作者增长17.6%，新增创作者增长25.2%。留存率达72.5%，创作者粘性强。"
            ),
            ChartSpec(
                chart_type="clustered_bar",
                title="TOP10创作者贡献播放量",
                description="播放量贡献最高的TOP10创作者",
                data_format={
                    "categories": ["创作者A", "创作者B", "创作者C", "创作者D", "创作者E"],
                    "series": [{"name": "播放量", "data": [500000000, 450000000, 400000000, 350000000, 300000000]}]
                },
                insights="创作者A贡献播放量最高（5亿），TOP10创作者占总播放量的15%。"
            ),
            ChartSpec(
                chart_type="treemap",
                title="创作者等级分布",
                description="S/A/B/C各级别创作者的播放量占比",
                data_format={
                    "labels": ["S级", "A级", "B级", "C级"],
                    "sizes": [4000000000, 3000000000, 2000000000, 1000000000],
                    "colors": [1, 2, 3, 4]
                },
                insights="A级创作者播放量占比最高（30%），S级创作者占比25%。建议加大S级创作者的培养。"
            ),
            ChartSpec(
                chart_type="line",
                title="创作者月度留存趋势",
                description="过去12个月创作者留存率变化",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [{"name": "留存率", "data": [68, 70, 71, 72, 72.5]}]
                },
                insights="创作者留存率稳步提升，从68%提升至72.5%。说明平台对创作者的吸引力增强。"
            ),
            ChartSpec(
                chart_type="decomposition_tree",
                title="创作者播放量下跌根因分析",
                description="播放量下跌的原因分解",
                data_format={
                    "root": "播放量下跌",
                    "children": [
                        {"name": "内容质量下降", "value": -40},
                        {"name": "推荐权重降低", "value": -30},
                        {"name": "竞品冲击", "value": -20},
                        {"name": "季节性因素", "value": -10}
                    ]
                },
                insights="播放量下跌主要由内容质量下降（40%）和推荐权重降低（30%）导致。建议优化内容质量。"
            )
        ],
        kpis=["活跃创作者", "新增创作者", "人均产出", "创作者留存率"],
        insights="创作者生态健康，活跃创作者增长17.6%，留存率达72.5%。A级创作者是主力，S级创作者培养空间大。",
        recommendations="1. 建立创作者分层培养体系，重点培养S级创作者\n2. 优化内容质量，提升推荐权重\n3. 加强创作者激励计划，提升留存率\n4. 建立创作者成长路径，提升人均产出\n5. 定期分析播放量下跌原因，及时调整策略"
    ),
    
    "ip_monetization": DashboardTemplate(
        industry="文娱",
        template_name="IP/内容商业化&变现效率看板",
        template_id="ip_monetization",
        description="广告收入、带货GMV、分成收入、变现ROI等商业化核心指标",
        charts=[
            ChartSpec(
                chart_type="multi_card",
                title="商业化关键指标",
                description="总广告收入、总带货GMV、总分成收入、整体变现ROI",
                data_format={
                    "cards": [
                        {"title": "广告收入", "value": "¥5,000,000,000", "change": "+35.2%"},
                        {"title": "带货GMV", "value": "¥12,000,000,000", "change": "+45.6%"},
                        {"title": "分成收入", "value": "¥2,000,000,000", "change": "+28.5%"},
                        {"title": "变现ROI", "value": "3.5倍", "change": "+0.5倍"}
                    ]
                },
                insights="商业化效果显著，带货GMV增长45.6%，广告收入增长35.2%。整体变现ROI达3.5倍，效率提升。"
            ),
            ChartSpec(
                chart_type="combo",
                title="月度广告收入与填充率",
                description="广告收入(柱形)和广告填充率(折线)趋势",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "columns": {"name": "广告收入", "data": [400000000, 420000000, 450000000, 480000000, 500000000]},
                    "lines": {"name": "填充率", "data": [75, 78, 80, 82, 85]}
                },
                insights="广告收入稳步增长，填充率从75%提升至85%。建议继续优化广告主体验。"
            ),
            ChartSpec(
                chart_type="stacked_column",
                title="变现类型收入构成",
                description="广告、带货、付费内容、周边等变现类型的收入占比",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [
                        {"name": "广告", "data": [400000000, 420000000, 450000000, 480000000, 500000000]},
                        {"name": "带货", "data": [800000000, 900000000, 1000000000, 1100000000, 1200000000]},
                        {"name": "付费内容", "data": [150000000, 160000000, 170000000, 180000000, 200000000]},
                        {"name": "周边", "data": [50000000, 55000000, 60000000, 65000000, 70000000]}
                    ]
                },
                insights="带货收入占比最高（55%），广告收入占比30%，付费内容占比10%。带货是主要变现方式。"
            ),
            ChartSpec(
                chart_type="funnel",
                title="带货转化链路",
                description="曝光→点击→种草→成交的完整转化漏斗",
                data_format={
                    "stages": ["曝光", "点击", "种草", "成交"],
                    "values": [1000000000, 500000000, 100000000, 20000000]
                },
                insights="曝光到点击转化率50%，点击到种草转化率20%，种草到成交转化率20%。种草到成交环节有提升空间。"
            ),
            ChartSpec(
                chart_type="scatter",
                title="粉丝量 vs 带货GMV",
                description="创作者粉丝量与带货GMV的相关性分析",
                data_format={
                    "x": [10000, 50000, 100000, 500000, 1000000],
                    "y": [10000, 50000, 150000, 500000, 1200000],
                    "labels": ["1万粉", "5万粉", "10万粉", "50万粉", "100万粉"]
                },
                insights="粉丝量与带货GMV呈正相关，50万粉创作者带货GMV是10万粉的3.3倍。"
            )
        ],
        kpis=["广告收入", "带货GMV", "分成收入", "变现ROI"],
        insights="商业化效率显著提升，带货GMV增长45.6%，广告收入增长35.2%。带货是主要变现方式，变现ROI达3.5倍。",
        recommendations="1. 加大带货业务投入，抓住增长机遇\n2. 优化带货转化链路，提升成交转化率\n3. 加强广告主合作，提升填充率\n4. 建立创作者分层变现体系\n5. 探索付费内容等新变现模式"
    ),
    
    "user_lifecycle": DashboardTemplate(
        industry="文娱",
        template_name="用户生命周期&内容消费偏好看板",
        template_id="user_lifecycle",
        description="DAU、MAU、用户付费率、用户分层等用户运营核心指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="用户关键指标",
                description="总用户数、DAU、MAU、用户付费率",
                data_format={
                    "cards": [
                        {"title": "总用户", "value": "500,000,000", "change": "+25.2%"},
                        {"title": "DAU", "value": "50,000,000", "change": "+18.5%"},
                        {"title": "MAU", "value": "200,000,000", "change": "+15.2%"},
                        {"title": "付费率", "value": "8.5%", "change": "+1.2%"}
                    ]
                },
                insights="用户规模持续增长，DAU增长18.5%，MAU增长15.2%。付费率达8.5%，用户变现能力增强。"
            ),
            ChartSpec(
                chart_type="line",
                title="DAU/MAU趋势",
                description="DAU/MAU比值变化，反映用户粘性",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [{"name": "DAU/MAU", "data": [0.22, 0.23, 0.24, 0.245, 0.25]}]
                },
                insights="DAU/MAU从0.22提升至0.25，说明用户粘性持续提升。用户活跃度良好。"
            ),
            ChartSpec(
                chart_type="stacked_area",
                title="新老用户消费占比",
                description="新用户和老用户的内容消费占比变化",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [
                        {"name": "新用户", "data": [100000000, 110000000, 105000000, 120000000, 130000000]},
                        {"name": "老用户", "data": [300000000, 320000000, 340000000, 360000000, 380000000]}
                    ]
                },
                insights="老用户消费占比75%，是新用户消费主力。新用户占比25%，增速快于老用户。"
            ),
            ChartSpec(
                chart_type="matrix",
                title="用户分层×消费频次×金额",
                description="新/老/沉睡/流失用户的消费分布",
                data_format={
                    "rows": ["新用户", "老用户", "沉睡用户", "流失用户"],
                    "columns": ["高频", "中频", "低频"],
                    "values": [
                        [15, 8, 2],
                        [35, 25, 5],
                        [3, 4, 2],
                        [0, 0, 1]
                    ]
                },
                insights="老用户高频消费占比35%，是消费主力。沉睡用户唤醒空间大，建议加强运营。"
            ),
            ChartSpec(
                chart_type="bubble",
                title="用户年龄×消费金额×偏好标签",
                description="不同年龄用户的消费金额和内容偏好",
                data_format={
                    "x": [18, 25, 35, 45, 55],
                    "y": [50, 150, 200, 120, 80],
                    "size": [10, 30, 50, 20, 10],
                    "labels": ["18-24岁", "25-34岁", "35-44岁", "45-54岁", "55岁以上"]
                },
                insights="25-44岁用户是消费主力，消费金额最高。35-44岁用户偏好知识类内容，25-34岁用户偏好娱乐类内容。"
            )
        ],
        kpis=["总用户", "DAU", "MAU", "付费率"],
        insights="用户规模持续增长，DAU/MAU达0.25，用户粘性良好。25-44岁用户是消费主力，老用户贡献占比75%。",
        recommendations="1. 加强新用户首次消费引导，提升转化\n2. 建立沉睡用户唤醒机制\n3. 针对不同年龄段用户推送偏好内容\n4. 加强老用户运营，提升消费频次\n5. 建立用户分层运营体系"
    ),
    
    "content_production": DashboardTemplate(
        industry="文娱",
        template_name="内容生产排期&进度监控看板",
        template_id="content_production",
        description="内容项目从策划到发布的全流程进度监控，适用于内容团队项目管理",
        charts=[
            ChartSpec(
                chart_type="kpi",
                title="内容生产KPI",
                description="计划内容数、已发布数、达成率、质量评分",
                data_format={
                    "cards": [
                        {"title": "计划内容数", "value": "1,000", "change": "+15%"},
                        {"title": "已发布内容数", "value": "850", "change": "+25%"},
                        {"title": "发布达成率", "value": "85%", "change": "+5%"},
                        {"title": "质量评分", "value": "4.5分", "change": "+0.3"}
                    ]
                },
                insights="内容生产达成率85%，质量评分4.5分。生产效率和质量均达标。"
            ),
            ChartSpec(
                chart_type="gantt",
                title="项目时间轴",
                description="各内容项目从策划到发布的时间安排",
                data_format={
                    "tasks": ["项目A", "项目B", "项目C", "项目D", "项目E"],
                    "start": [0, 2, 4, 6, 8],
                    "duration": [3, 3, 2, 4, 3]
                },
                insights="项目A和B时间重叠，需要注意资源协调。项目E开始时间最晚，需要跟进进度。"
            ),
            ChartSpec(
                chart_type="gauge",
                title="项目进度达成率",
                description="各项目的进度完成情况",
                data_format={
                    "title": "整体进度",
                    "value": 75,
                    "min": 0,
                    "max": 100
                },
                insights="整体进度75%，处于良好水平。部分项目有延期风险，需要关注。"
            ),
            ChartSpec(
                chart_type="stacked_bar",
                title="各阶段内容数量",
                description="策划、拍摄、审核、发布各阶段的内容数量",
                data_format={
                    "categories": ["策划中", "拍摄中", "审核中", "已发布"],
                    "series": [{"name": "数量", "data": [100, 50, 30, 850]}]
                },
                insights="已发布850个，策划中100个。审核积压30个，需要加快审核进度。"
            ),
            ChartSpec(
                chart_type="table",
                title="内容排期明细",
                description="各内容的详细排期信息",
                data_format={
                    "columns": ["内容标题", "负责人", "计划发布时间", "实际发布时间", "状态", "延期天数"],
                    "rows": [
                        ["内容A", "张三", "2026-03-25", "2026-03-25", "已发布", "0"],
                        ["内容B", "李四", "2026-03-26", "2026-03-28", "审核中", "0"]
                    ]
                },
                insights="大部分内容按时发布，少部分有延期风险。建议加强进度监控。"
            )
        ],
        kpis=["计划内容数", "已发布数", "达成率", "质量评分"],
        insights="内容生产达成率85%，质量评分4.5分。整体进度75%，审核环节有积压，需要优化。",
        recommendations="1. 加快审核进度，避免积压\n2. 加强项目进度监控，及时发现延期风险\n3. 建立内容生产标准化流程\n4. 优化资源配置，协调项目时间冲突\n5. 建立质量评分激励机制"
    )
}

# ============================================================================
# 看板模板库

# ============================================================================
# 十一、医疗健康行业（对标华为云医疗、网易有数医疗）
# ============================================================================

HEALTHCARE_TEMPLATES = {
    "hospital_operations": DashboardTemplate(
        industry="医疗健康",
        template_name="医院科室运营&效率看板",
        template_id="hospital_operations",
        description="科室门诊量、床位使用率、手术量、医生绩效等医院运营核心指标，对标三甲医院数字化运营标准",
        charts=[
            ChartSpec(
                chart_type="multi_card",
                title="医院核心运营指标",
                description="门诊量、住院量、床位使用率、手术量、平均住院天数——一眼掌握医院整体运营健康度",
                data_format={
                    "cards": [
                        {"title": "日门诊量", "value": "3,456人次", "change": "+8.5%"},
                        {"title": "住院人数", "value": "1,234人", "change": "+5.2%"},
                        {"title": "床位使用率", "value": "92.3%", "change": "+2.1%"},
                        {"title": "手术量", "value": "156台", "change": "+12.5%"},
                        {"title": "平均住院天数", "value": "8.5天", "change": "-0.5天"}
                    ]
                },
                insights="床位使用率92.3%接近饱和（警戒线95%），需关注床位调配。平均住院天数下降说明诊疗效率提升。"
            ),
            ChartSpec(
                chart_type="clustered_column",
                title="各科室门诊量对比",
                description="内科、外科、妇产科等各科室门诊量排名，识别高负荷科室和资源缺口",
                data_format={
                    "categories": ["内科", "外科", "妇产科", "儿科", "骨科", "眼科"],
                    "series": [{"name": "门诊量", "data": [800, 650, 500, 450, 380, 320]}]
                },
                insights="内科门诊量最高（800人次），占总量23%。儿科和骨科增速最快（+18%），建议增配医生资源。"
            ),
            ChartSpec(
                chart_type="line",
                title="门诊量趋势",
                description="过去30天日门诊量走势，识别就诊高峰和季节性规律",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [{"name": "门诊量", "data": [3200, 3400, 3100, 3600, 3800]}]
                },
                insights="周一、周四为就诊高峰，周末明显下降。建议在高峰日增加出诊医生，优化预约分流。"
            ),
            ChartSpec(
                chart_type="gauge",
                title="床位使用率仪表盘",
                description="实时床位使用率，绿色（<85%）/黄色（85-95%）/红色（>95%）三色预警",
                data_format={
                    "title": "床位使用率",
                    "value": 92,
                    "min": 0,
                    "max": 100,
                    "thresholds": [{"value": 85, "color": "yellow"}, {"value": 95, "color": "red"}]
                },
                insights="当前92.3%处于黄色预警区间，距红色警戒线仅2.7%。建议启动床位调配预案，加快出院流程。"
            ),
            ChartSpec(
                chart_type="stacked_bar",
                title="耗材使用分布",
                description="各科室耗材消耗量和成本占比，识别高耗材科室",
                data_format={
                    "categories": ["手术室", "ICU", "急诊", "内科", "外科"],
                    "series": [
                        {"name": "高值耗材", "data": [500000, 300000, 150000, 80000, 120000]},
                        {"name": "普通耗材", "data": [200000, 100000, 80000, 60000, 90000]}
                    ]
                },
                insights="手术室耗材成本最高（占总耗材的45%），高值耗材占比71%。建议加强手术室耗材精细化管理。"
            ),
            ChartSpec(
                chart_type="table",
                title="医生绩效排行",
                description="各科室医生的门诊量、手术量、患者满意度综合排行",
                data_format={
                    "columns": ["医生", "科室", "门诊量", "手术量", "满意度", "绩效评级"],
                    "rows": [
                        ["张医生", "外科", "120", "15", "98.5%", "A"],
                        ["李医生", "内科", "150", "0", "96.2%", "A"]
                    ]
                },
                insights="A级医生占比35%，是医院核心医疗力量。建议建立医生成长激励机制，提升B级医生比例。"
            )
        ],
        kpis=["日门诊量", "床位使用率", "手术量", "平均住院天数"],
        insights="""医院运营整体良好，门诊量增长8.5%，手术量增长12.5%。
床位使用率92.3%接近饱和，是当前最大风险点。
内科是最高负荷科室，儿科和骨科增速最快，需要重点关注资源配置。
耗材成本管理有优化空间，手术室高值耗材占比偏高。""",
        recommendations="""1. 立即启动床位调配预案，加快出院流程，防止床位使用率突破95%红线
2. 优化预约分流，将周一/周四高峰患者引导至低峰时段
3. 加强手术室高值耗材精细化管理，目标降低耗材成本5%
4. 为儿科和骨科增配医生资源，满足快速增长的就诊需求
5. 建立医生绩效激励机制，提升B级医生向A级晋升比例"""
    ),

    "patient_satisfaction": DashboardTemplate(
        industry="医疗健康",
        template_name="患者满意度&医疗质量看板",
        template_id="patient_satisfaction",
        description="患者满意度、投诉率、医疗质量指标等，对标JCI国际医院认证标准",
        charts=[
            ChartSpec(
                chart_type="card",
                title="满意度核心指标",
                description="整体满意度、投诉率、纠纷率、NPS净推荐值——衡量医院服务质量的核心指标",
                data_format={
                    "cards": [
                        {"title": "整体满意度", "value": "96.5%", "change": "+1.2%"},
                        {"title": "投诉率", "value": "0.8‰", "change": "-0.2‰"},
                        {"title": "医疗纠纷率", "value": "0.05‰", "change": "-0.01‰"},
                        {"title": "NPS净推荐值", "value": "72", "change": "+5"}
                    ]
                },
                insights="满意度96.5%达到三甲医院优秀标准（>95%），NPS达72分处于行业领先水平。投诉率持续下降。"
            ),
            ChartSpec(
                chart_type="clustered_bar",
                title="各科室满意度对比",
                description="各科室患者满意度排名，识别服务短板科室",
                data_format={
                    "categories": ["外科", "内科", "妇产科", "儿科", "急诊", "门诊"],
                    "series": [{"name": "满意度", "data": [98.5, 97.2, 96.8, 95.5, 93.2, 94.8]}]
                },
                insights="急诊满意度最低（93.2%），主要原因是等待时间长。建议优化急诊分诊流程，缩短等待时间。"
            ),
            ChartSpec(
                chart_type="donut",
                title="投诉原因分布",
                description="患者投诉的主要原因分类，指导服务改进方向",
                data_format={
                    "labels": ["等待时间长", "服务态度", "收费问题", "医疗效果", "其他"],
                    "values": [40, 25, 20, 10, 5]
                },
                insights="等待时间长是最主要投诉原因（40%），其次是服务态度（25%）。优化排队系统是提升满意度的关键。"
            ),
            ChartSpec(
                chart_type="line",
                title="满意度趋势",
                description="过去12个月满意度变化趋势，评估改进措施效果",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [{"name": "满意度", "data": [94.5, 95.0, 95.5, 96.0, 96.5]}]
                },
                insights="满意度持续提升，12个月累计提升2%，说明服务改进措施有效。建议继续保持改进节奏。"
            )
        ],
        kpis=["整体满意度", "投诉率", "NPS净推荐值"],
        insights="""患者满意度持续提升，达到96.5%的三甲医院优秀标准。
急诊科是满意度最低的科室，等待时间长是核心痛点。
投诉率和纠纷率均在下降，医疗质量管理成效显著。""",
        recommendations="""1. 重点优化急诊分诊流程，目标将急诊满意度提升至95%以上
2. 推广智能排队系统，减少患者等待时间
3. 加强医护人员服务礼仪培训，改善服务态度
4. 建立患者投诉快速响应机制，24小时内处理
5. 定期开展患者满意度调研，持续追踪改进效果"""
    )
}

# ============================================================================
# 十二、教育行业（对标帆软教育、观远教育）
# ============================================================================

EDUCATION_TEMPLATES = {
    "enrollment_funnel": DashboardTemplate(
        industry="教育",
        template_name="招生漏斗&渠道效率看板",
        template_id="enrollment_funnel",
        description="线索获取、咨询转化、报名、入学全链路招生漏斗，对标新东方、好未来等头部教育机构",
        charts=[
            ChartSpec(
                chart_type="card",
                title="招生核心指标",
                description="线索量、咨询量、报名量、入学量、获客成本——衡量招生效率的核心指标",
                data_format={
                    "cards": [
                        {"title": "线索量", "value": "12,345", "change": "+25.2%"},
                        {"title": "咨询量", "value": "5,678", "change": "+18.5%"},
                        {"title": "报名量", "value": "2,345", "change": "+15.2%"},
                        {"title": "入学量", "value": "2,100", "change": "+12.5%"},
                        {"title": "获客成本", "value": "¥285", "change": "-¥35"}
                    ]
                },
                insights="线索量增长25.2%，获客成本下降¥35，招生效率显著提升。入学转化率89.6%，说明报名后流失较少。"
            ),
            ChartSpec(
                chart_type="funnel",
                title="招生全链路转化漏斗",
                description="线索→咨询→试听→报名→入学的完整转化链路，识别最大流失环节",
                data_format={
                    "stages": ["线索", "咨询", "试听", "报名", "入学"],
                    "values": [12345, 5678, 3456, 2345, 2100]
                },
                insights="线索到咨询转化率46%，咨询到试听转化率61%，试听到报名转化率68%。试听环节是最大转化机会点。"
            ),
            ChartSpec(
                chart_type="clustered_bar",
                title="招生渠道效果对比",
                description="各招生渠道的线索量、转化率、获客成本对比，优化渠道投入",
                data_format={
                    "categories": ["抖音", "百度SEM", "微信朋友圈", "口碑转介绍", "线下活动"],
                    "series": [
                        {"name": "线索量", "data": [4000, 3000, 2000, 2000, 1345]},
                        {"name": "转化率", "data": [35, 42, 38, 65, 55]}
                    ]
                },
                insights="口碑转介绍转化率最高（65%），获客成本最低。抖音线索量最大但转化率偏低，建议优化内容质量。"
            ),
            ChartSpec(
                chart_type="line",
                title="月度招生趋势",
                description="过去12个月招生量走势，识别招生旺季和淡季规律",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [{"name": "报名量", "data": [1800, 2000, 2100, 2300, 2345]}]
                },
                insights="招生量呈稳步增长趋势，6-7月为招生旺季（暑期）。建议提前备好师资和教室资源。"
            ),
            ChartSpec(
                chart_type="treemap",
                title="课程报名结构",
                description="各课程类型的报名量占比，识别热门课程和待开发课程",
                data_format={
                    "labels": ["K12数学", "英语", "编程", "艺术", "体育"],
                    "sizes": [800, 600, 400, 300, 245],
                    "colors": [1, 2, 3, 4, 5]
                },
                insights="K12数学报名量最高（34%），编程课增速最快（+45%）。建议加大编程课师资投入，抓住增长机遇。"
            )
        ],
        kpis=["线索量", "报名量", "入学量", "获客成本"],
        insights="""招生效率持续提升，线索量增长25.2%，获客成本下降¥35。
口碑转介绍是质量最高的渠道，转化率达65%，应重点维护。
试听环节是最大转化机会点，优化试听体验可显著提升报名率。
编程课增速最快，是未来重点发展方向。""",
        recommendations="""1. 建立口碑转介绍激励机制，扩大高质量线索来源
2. 优化试听课程设计，提升试听到报名的转化率
3. 加大编程课师资投入，满足快速增长的市场需求
4. 提前备好暑期（6-7月）师资和教室资源
5. 优化抖音内容质量，提升线索转化率"""
    ),

    "learning_quality": DashboardTemplate(
        industry="教育",
        template_name="学员学习质量&续费看板",
        template_id="learning_quality",
        description="出勤率、作业完成率、成绩提升、续费率等学员质量核心指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="学员质量核心指标",
                description="出勤率、作业完成率、成绩提升率、续费率——衡量教学质量和学员粘性",
                data_format={
                    "cards": [
                        {"title": "出勤率", "value": "92.5%", "change": "+2.1%"},
                        {"title": "作业完成率", "value": "85.3%", "change": "+3.5%"},
                        {"title": "成绩提升率", "value": "78.5%", "change": "+5.2%"},
                        {"title": "续费率", "value": "72.3%", "change": "+4.8%"}
                    ]
                },
                insights="续费率72.3%处于行业良好水平（行业均值65%），成绩提升率78.5%是续费的核心驱动因素。"
            ),
            ChartSpec(
                chart_type="scatter",
                title="出勤率 vs 成绩提升率",
                description="学员出勤率与成绩提升率的相关性，验证出勤对学习效果的影响",
                data_format={
                    "x": [60, 70, 80, 90, 100],
                    "y": [40, 55, 68, 80, 90],
                    "labels": ["低出勤", "中低出勤", "中出勤", "高出勤", "全勤"]
                },
                insights="出勤率与成绩提升率强正相关，全勤学员成绩提升率达90%，低出勤学员仅40%。提升出勤率是关键。"
            ),
            ChartSpec(
                chart_type="combo",
                title="续费率与成绩提升率趋势",
                description="续费率（折线）与成绩提升率（柱形）的月度变化，验证教学质量对续费的驱动",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "columns": {"name": "成绩提升率", "data": [72, 74, 76, 78, 78.5]},
                    "lines": {"name": "续费率", "data": [65, 67, 69, 71, 72.3]}
                },
                insights="成绩提升率与续费率高度正相关，成绩提升率每提升1%，续费率约提升0.8%。教学质量是续费的核心驱动。"
            ),
            ChartSpec(
                chart_type="clustered_bar",
                title="各教师续费率对比",
                description="不同教师班级的续费率排名，识别优秀教师和需要辅导的教师",
                data_format={
                    "categories": ["张老师", "李老师", "王老师", "赵老师", "刘老师"],
                    "series": [{"name": "续费率", "data": [85, 80, 75, 68, 62]}]
                },
                insights="张老师续费率最高（85%），刘老师最低（62%）。建议组织张老师分享教学经验，帮助低续费率教师提升。"
            )
        ],
        kpis=["出勤率", "成绩提升率", "续费率"],
        insights="""续费率72.3%超过行业均值7.3个百分点，教学质量是核心竞争力。
出勤率与成绩提升率强正相关，提升出勤率是提升教学效果的关键杠杆。
教师间续费率差异显著（62%-85%），优秀教师经验值得推广。""",
        recommendations="""1. 建立出勤激励机制，目标将出勤率提升至95%
2. 推广张老师的教学方法，帮助低续费率教师提升
3. 在续费关键节点（课程结束前1个月）加强学员沟通
4. 建立学员成绩追踪体系，及时发现学习困难学员
5. 优化作业设计，提升作业完成率和学习效果"""
    )
}

# ============================================================================
# 十三、餐饮连锁行业（对标美团、帆软餐饮）
# ============================================================================

CATERING_TEMPLATES = {
    "restaurant_operations": DashboardTemplate(
        industry="餐饮连锁",
        template_name="集团门店运营罗盘看板",
        template_id="restaurant_operations",
        description="门店营业额、翻台率、客单价、外卖占比等餐饮连锁核心指标，对标海底捞、麦当劳等头部餐饮集团",
        charts=[
            ChartSpec(
                chart_type="multi_card",
                title="集团运营核心指标",
                description="总营业额、门店数、翻台率、客单价、外卖占比——集团经营健康度一览",
                data_format={
                    "cards": [
                        {"title": "总营业额", "value": "¥50,000,000", "change": "+18.5%"},
                        {"title": "门店数", "value": "500家", "change": "+25家"},
                        {"title": "翻台率", "value": "4.2次/天", "change": "+0.3次"},
                        {"title": "客单价", "value": "¥68.5", "change": "+¥3.5"},
                        {"title": "外卖占比", "value": "35%", "change": "+5%"}
                    ]
                },
                insights="翻台率4.2次/天达到行业优秀水平（行业均值3.5次），外卖占比35%持续提升，线上线下融合加速。"
            ),
            ChartSpec(
                chart_type="clustered_bar",
                title="TOP20门店营业额排行",
                description="营业额最高的20家门店排名，识别标杆门店和可复制的成功经验",
                data_format={
                    "categories": ["北京王府井店", "上海南京路店", "广州天河店"],
                    "series": [{"name": "营业额", "data": [500000, 480000, 450000]}]
                },
                insights="北京王府井店营业额最高（¥50万/月），翻台率达5.8次/天。其选址、运营模式值得全国推广。"
            ),
            ChartSpec(
                chart_type="combo",
                title="营业额与翻台率趋势",
                description="月度营业额（柱形）与翻台率（折线）变化，分析经营效率提升路径",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "columns": {"name": "营业额", "data": [40000000, 42000000, 45000000, 48000000, 50000000]},
                    "lines": {"name": "翻台率", "data": [3.8, 3.9, 4.0, 4.1, 4.2]}
                },
                insights="营业额和翻台率同步提升，说明增长来自效率提升而非单纯扩店。这是高质量增长的标志。"
            ),
            ChartSpec(
                chart_type="treemap",
                title="菜品销售结构",
                description="各菜品类别的销售额占比，识别明星菜品和待优化菜品",
                data_format={
                    "labels": ["火锅底料", "肉类", "蔬菜", "饮品", "甜品"],
                    "sizes": [15000000, 12000000, 8000000, 8000000, 7000000],
                    "colors": [1, 2, 3, 4, 5]
                },
                insights="火锅底料和肉类占总销售额的54%，是核心品类。饮品和甜品增速最快（+35%），是新增长点。"
            ),
            ChartSpec(
                chart_type="stacked_column",
                title="堂食vs外卖收入构成",
                description="各月堂食和外卖收入占比变化，追踪线上化进程",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [
                        {"name": "堂食", "data": [28000000, 28500000, 29000000, 30000000, 32500000]},
                        {"name": "外卖", "data": [12000000, 13500000, 16000000, 18000000, 17500000]}
                    ]
                },
                insights="外卖占比从30%提升至35%，线上化进程加速。堂食绝对值也在增长，说明整体经营向好。"
            ),
            ChartSpec(
                chart_type="filled_map",
                title="全国门店分布热力图",
                description="全国门店的地理分布和营业额热力，指导新店选址策略",
                data_format={
                    "regions": ["华东", "华北", "华南", "西南", "西北"],
                    "values": [200, 150, 100, 30, 20]
                },
                insights="华东地区门店密度最高（200家），西北地区最少（20家）。西南地区增速最快，是下一阶段扩张重点。"
            )
        ],
        kpis=["总营业额", "翻台率", "客单价", "外卖占比"],
        insights="""集团经营高质量增长，营业额增长18.5%，翻台率达4.2次/天超行业均值。
外卖占比35%持续提升，线上线下融合加速，是未来增长的重要引擎。
饮品和甜品增速最快，是新的利润增长点。
西南地区是下一阶段扩张重点，市场空间大。""",
        recommendations="""1. 复制北京王府井店的成功经验，推广至全国标杆门店
2. 加大饮品和甜品品类投入，抓住高增速品类机遇
3. 优化外卖运营，目标将外卖占比提升至40%
4. 加快西南地区扩张，抢占市场先机
5. 建立门店ROS评分体系，量化门店运营能力"""
    ),

    "menu_analysis": DashboardTemplate(
        industry="餐饮连锁",
        template_name="菜品分析&点单优化看板",
        template_id="menu_analysis",
        description="菜品销量、毛利率、复购率、差评率等菜品运营核心指标",
        charts=[
            ChartSpec(
                chart_type="card",
                title="菜品运营指标",
                description="SKU数、动销率、平均毛利率、差评率——菜品健康度核心指标",
                data_format={
                    "cards": [
                        {"title": "在售SKU数", "value": "156个", "change": "+12个"},
                        {"title": "动销率", "value": "82.5%", "change": "+3.5%"},
                        {"title": "平均毛利率", "value": "65.2%", "change": "+1.2%"},
                        {"title": "差评率", "value": "1.2%", "change": "-0.3%"}
                    ]
                },
                insights="动销率82.5%，说明17.5%的菜品滞销，需要优化菜单结构。毛利率65.2%处于行业良好水平。"
            ),
            ChartSpec(
                chart_type="bubble",
                title="菜品销量×毛利率×复购率矩阵",
                description="三维分析菜品价值：X轴销量、Y轴毛利率、气泡大小为复购率，识别明星菜品",
                data_format={
                    "x": [1000, 800, 600, 400, 200],
                    "y": [70, 65, 60, 55, 50],
                    "size": [80, 60, 40, 30, 20],
                    "labels": ["招牌锅底", "精品牛肉", "时蔬拼盘", "特色饮品", "甜品套餐"]
                },
                insights="招牌锅底是明星菜品（高销量+高毛利+高复购），是核心竞争力。特色饮品毛利率高但销量低，需要加强推广。"
            ),
            ChartSpec(
                chart_type="table",
                title="滞销菜品清单",
                description="动销率低于50%的菜品列表，需要优化或下架",
                data_format={
                    "columns": ["菜品名", "月销量", "动销率", "毛利率", "建议处理"],
                    "rows": [
                        ["某冷门菜A", "50份", "25%", "45%", "建议下架"],
                        ["某冷门菜B", "80份", "40%", "55%", "建议促销"]
                    ]
                },
                insights="27个菜品动销率低于50%，占SKU总数17%。建议下架低毛利滞销菜品，为新品腾出菜单空间。"
            )
        ],
        kpis=["动销率", "平均毛利率", "差评率"],
        insights="""菜品结构有优化空间，17.5%的菜品滞销，需要精简菜单。
招牌锅底是核心竞争力，需要重点保护和推广。
特色饮品毛利率高但销量低，是待挖掘的利润增长点。""",
        recommendations="""1. 下架低毛利滞销菜品，精简菜单至120个SKU以内
2. 加强特色饮品推广，目标将饮品销量提升30%
3. 建立菜品定期评审机制，每季度优化一次菜单
4. 针对差评菜品进行口味改进，降低差评率至1%以下
5. 开发季节性限定菜品，提升新鲜感和复购率"""
    )
}

# ============================================================================
# 十四、物流供应链行业（对标京东物流、帆软供应链）
# ============================================================================

LOGISTICS_TEMPLATES = {
    "supply_chain_control": DashboardTemplate(
        industry="物流供应链",
        template_name="供应链总控平台看板",
        template_id="supply_chain_control",
        description="采购、库存、销售、物流全链路供应链总控，对标京东物流、顺丰等头部物流企业",
        charts=[
            ChartSpec(
                chart_type="multi_card",
                title="供应链核心指标",
                description="订单履约率、库存周转天数、采购及时率、运输准时率——供应链健康度全景",
                data_format={
                    "cards": [
                        {"title": "订单履约率", "value": "98.5%", "change": "+0.5%"},
                        {"title": "库存周转天数", "value": "18天", "change": "-2天"},
                        {"title": "采购及时率", "value": "95.2%", "change": "+1.2%"},
                        {"title": "运输准时率", "value": "96.8%", "change": "+0.8%"},
                        {"title": "缺货率", "value": "1.2%", "change": "-0.3%"}
                    ]
                },
                insights="订单履约率98.5%达到行业领先水平，库存周转天数下降2天，供应链效率持续提升。"
            ),
            ChartSpec(
                chart_type="waterfall",
                title="库存变动瀑布图",
                description="期初库存→采购入库→销售出库→损耗→期末库存的完整库存变动分析",
                data_format={
                    "categories": ["期初库存", "采购入库", "销售出库", "损耗", "期末库存"],
                    "values": [10000000, 8000000, -7500000, -200000, 10300000]
                },
                insights="本月采购入库800万，销售出库750万，损耗20万，期末库存1030万。库存净增30万，处于合理水平。"
            ),
            ChartSpec(
                chart_type="line",
                title="库存周转天数趋势",
                description="过去12个月库存周转天数变化，评估库存管理效率提升",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [{"name": "周转天数", "data": [22, 21, 20, 19, 18]}]
                },
                insights="库存周转天数从22天降至18天，持续优化。目标是达到行业最优水平15天。"
            ),
            ChartSpec(
                chart_type="azure_map",
                title="全国仓储网络分布",
                description="全国仓库位置、库存量、覆盖范围的地理分布，优化仓储网络布局",
                data_format={
                    "regions": ["华东", "华北", "华南", "西南", "西北"],
                    "values": [5000000, 3000000, 2000000, 500000, 300000]
                },
                insights="华东仓储量最大（占47%），西北最少（3%）。建议在西南增设区域仓，缩短配送时效。"
            ),
            ChartSpec(
                chart_type="clustered_column",
                title="供应商绩效对比",
                description="各供应商的交货及时率、质量合格率、价格竞争力综合评分",
                data_format={
                    "categories": ["供应商A", "供应商B", "供应商C", "供应商D", "供应商E"],
                    "series": [
                        {"name": "及时率", "data": [98, 95, 92, 88, 85]},
                        {"name": "合格率", "data": [99, 97, 95, 93, 90]}
                    ]
                },
                insights="供应商A综合表现最优，供应商E表现最差。建议对供应商E进行整改，必要时更换供应商。"
            ),
            ChartSpec(
                chart_type="table",
                title="在途订单监控",
                description="当前在途订单的实时状态，识别延误风险订单",
                data_format={
                    "columns": ["订单号", "发货地", "目的地", "预计到达", "当前状态", "风险"],
                    "rows": [
                        ["ORD001", "上海", "北京", "2026-03-28", "运输中", "正常"],
                        ["ORD002", "深圳", "成都", "2026-03-27", "延误", "⚠️高风险"]
                    ]
                },
                insights="当前有3%的在途订单存在延误风险，需要立即跟进处理，避免影响客户满意度。"
            )
        ],
        kpis=["订单履约率", "库存周转天数", "采购及时率", "运输准时率"],
        insights="""供应链整体运营良好，订单履约率98.5%达行业领先水平。
库存周转天数持续下降，供应链效率提升显著。
西南地区仓储覆盖不足，是配送时效的短板。
供应商E表现持续偏差，需要重点关注。""",
        recommendations="""1. 在西南地区增设区域仓，目标将西南配送时效缩短至24小时
2. 对供应商E发出整改通知，设定3个月改进期限
3. 继续优化库存管理，目标将周转天数降至15天
4. 建立在途订单预警机制，提前处理延误风险
5. 推进供应链数字化，实现全链路实时可视化"""
    )
}

# ============================================================================
# 十五、能源行业（对标华为云能源、网易有数能源）
# ============================================================================

ENERGY_TEMPLATES = {
    "photovoltaic_monitor": DashboardTemplate(
        industry="能源",
        template_name="光伏电站运营监控看板",
        template_id="photovoltaic_monitor",
        description="发电量、设备效率、故障预警、收益分析等光伏电站运营核心指标，对标华为智能光伏、阳光电源",
        charts=[
            ChartSpec(
                chart_type="multi_card",
                title="电站核心运营指标",
                description="今日发电量、装机容量、系统效率、故障台数、今日收益——电站运营健康度一览",
                data_format={
                    "cards": [
                        {"title": "今日发电量", "value": "12,345 kWh", "change": "+8.5%"},
                        {"title": "装机容量", "value": "5,000 kWp", "change": ""},
                        {"title": "系统效率(PR)", "value": "82.5%", "change": "+1.2%"},
                        {"title": "故障台数", "value": "3台", "change": "-2台"},
                        {"title": "今日收益", "value": "¥8,642", "change": "+8.5%"}
                    ]
                },
                insights="系统效率82.5%达到行业良好水平（优秀标准>85%），故障台数下降，运维效率提升。"
            ),
            ChartSpec(
                chart_type="line",
                title="发电量趋势",
                description="过去30天日发电量走势，识别天气影响和设备异常",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [
                        {"name": "实际发电量", "data": [11000, 12000, 9000, 13000, 12345]},
                        {"name": "理论发电量", "data": [13000, 13500, 13000, 14000, 14000]}
                    ]
                },
                insights="3月3日发电量明显低于理论值，经排查为阴雨天气影响。实际与理论差距平均12%，有优化空间。"
            ),
            ChartSpec(
                chart_type="gauge",
                title="系统效率(PR)仪表盘",
                description="光伏系统性能比（PR值），反映系统整体运行效率",
                data_format={
                    "title": "系统效率PR",
                    "value": 82.5,
                    "min": 0,
                    "max": 100,
                    "thresholds": [{"value": 75, "color": "yellow"}, {"value": 85, "color": "green"}]
                },
                insights="PR值82.5%处于良好区间（75-85%），距优秀标准（>85%）还有2.5%的提升空间。"
            ),
            ChartSpec(
                chart_type="stacked_column",
                title="月度发电量与收益",
                description="各月发电量和收益的变化趋势，评估电站经济效益",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [
                        {"name": "发电量(MWh)", "data": [350, 380, 420, 450, 480]},
                        {"name": "收益(万元)", "data": [24.5, 26.6, 29.4, 31.5, 33.6]}
                    ]
                },
                insights="发电量和收益随季节增长，夏季（6-7月）为发电高峰。全年预计发电量4,800 MWh，收益约336万元。"
            ),
            ChartSpec(
                chart_type="table",
                title="故障设备明细",
                description="当前故障设备的详细信息，指导运维人员快速处理",
                data_format={
                    "columns": ["设备ID", "设备类型", "故障类型", "故障时间", "影响发电量", "处理状态"],
                    "rows": [
                        ["INV-001", "逆变器", "通信故障", "2026-03-26 08:00", "50 kWh", "处理中"],
                        ["PV-023", "组件", "热斑", "2026-03-25 14:00", "20 kWh", "待处理"]
                    ]
                },
                insights="当前3台设备故障，累计影响发电量约120 kWh，损失收益约¥84。建议优先处理逆变器故障。"
            )
        ],
        kpis=["今日发电量", "系统效率PR", "故障台数", "今日收益"],
        insights="""电站运营整体良好，系统效率82.5%处于行业良好水平。
发电量随季节增长，夏季为发电高峰，需提前做好运维准备。
当前3台设备故障，需要及时处理，避免发电损失扩大。
PR值距优秀标准还有2.5%提升空间，主要通过减少设备故障和清洁组件实现。""",
        recommendations="""1. 优先处理逆变器通信故障，恢复发电能力
2. 安排组件清洁计划，提升系统效率至85%以上
3. 在夏季发电高峰前完成全面设备检修
4. 建立故障预测模型，实现设备故障提前预警
5. 优化运维排班，确保故障24小时内响应处理"""
    ),

    "energy_consumption": DashboardTemplate(
        industry="能源",
        template_name="企业能耗分析&碳排放看板",
        template_id="energy_consumption",
        description="用电量、用气量、碳排放、能耗强度等企业能耗管理核心指标，对标双碳目标管理要求",
        charts=[
            ChartSpec(
                chart_type="card",
                title="能耗核心指标",
                description="总用电量、总用气量、碳排放量、能耗强度——企业能耗管理核心指标",
                data_format={
                    "cards": [
                        {"title": "月用电量", "value": "1,234,567 kWh", "change": "-5.2%"},
                        {"title": "月用气量", "value": "12,345 m³", "change": "-3.5%"},
                        {"title": "碳排放量", "value": "856 tCO₂", "change": "-8.5%"},
                        {"title": "能耗强度", "value": "0.85 kWh/元", "change": "-0.05"}
                    ]
                },
                insights="能耗和碳排放均在下降，能耗强度降低，说明节能减排措施有效。碳排放下降8.5%，超额完成月度目标。"
            ),
            ChartSpec(
                chart_type="stacked_column",
                title="各部门能耗分布",
                description="各部门用电量占比，识别高能耗部门和节能潜力",
                data_format={
                    "categories": ["生产车间", "空调系统", "照明", "办公设备", "其他"],
                    "series": [{"name": "用电量(kWh)", "data": [800000, 250000, 80000, 60000, 44567]}]
                },
                insights="生产车间用电量占比65%，是最大能耗来源。空调系统占比20%，是节能改造的重点方向。"
            ),
            ChartSpec(
                chart_type="line",
                title="碳排放趋势",
                description="过去12个月碳排放量变化，评估双碳目标达成进度",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [
                        {"name": "实际碳排放", "data": [950, 920, 900, 880, 856]},
                        {"name": "目标碳排放", "data": [900, 880, 860, 840, 820]}
                    ]
                },
                insights="碳排放持续下降，但仍略高于目标值。需要加快节能改造进度，确保年度双碳目标达成。"
            )
        ],
        kpis=["月用电量", "碳排放量", "能耗强度"],
        insights="""能耗和碳排放均在下降，节能减排措施有效。
生产车间和空调系统是最大能耗来源，是节能改造的重点。
碳排放略高于目标值，需要加快节能改造进度。""",
        recommendations="""1. 对空调系统进行节能改造，目标降低空调能耗15%
2. 推进生产车间设备更新，使用高效节能设备
3. 建立能耗实时监控预警，超标立即告警
4. 制定碳排放月度目标，确保年度双碳目标达成
5. 探索可再生能源使用，降低碳排放强度"""
    )
}

# ============================================================================
# 十六、政务/城市大数据行业（对标阿里DataV、华为云政务）
# ============================================================================

GOVERNMENT_TEMPLATES = {
    "city_operations": DashboardTemplate(
        industry="政务",
        template_name="城市运行体征&民生指标看板",
        template_id="city_operations",
        description="人口、经济、民生、治安等城市运行核心指标，对标阿里DataV城市大脑、华为云智慧城市",
        charts=[
            ChartSpec(
                chart_type="multi_card",
                title="城市核心体征指标",
                description="常住人口、GDP、财政收入、就业率、空气质量——城市运行健康度核心指标",
                data_format={
                    "cards": [
                        {"title": "常住人口", "value": "2,189万人", "change": "+1.2%"},
                        {"title": "GDP", "value": "¥4.2万亿", "change": "+6.5%"},
                        {"title": "财政收入", "value": "¥5,678亿", "change": "+8.2%"},
                        {"title": "就业率", "value": "96.5%", "change": "+0.5%"},
                        {"title": "空气质量(AQI)", "value": "45（优）", "change": "-5"}
                    ]
                },
                insights="GDP增速6.5%超过全国平均水平，就业率96.5%处于充分就业状态，空气质量持续改善。"
            ),
            ChartSpec(
                chart_type="filled_map",
                title="各区经济热力分布",
                description="各行政区GDP、财政收入、人口密度的地理热力分布",
                data_format={
                    "regions": ["中心城区", "东部新区", "西部园区", "南部生态区", "北部工业区"],
                    "values": [1500000000000, 1000000000000, 800000000000, 500000000000, 400000000000]
                },
                insights="中心城区经济总量最高（占36%），东部新区增速最快（+15%），是城市经济新引擎。"
            ),
            ChartSpec(
                chart_type="line",
                title="GDP与财政收入趋势",
                description="过去5年GDP和财政收入增长趋势，评估城市经济发展质量",
                data_format={
                    "categories": ["2022", "2023", "2024", "2025", "2026"],
                    "series": [
                        {"name": "GDP(万亿)", "data": [3.2, 3.5, 3.8, 4.0, 4.2]},
                        {"name": "财政收入(千亿)", "data": [4.2, 4.5, 4.8, 5.2, 5.678]}
                    ]
                },
                insights="GDP和财政收入保持稳定增长，财政收入增速（8.2%）高于GDP增速（6.5%），财政质量提升。"
            ),
            ChartSpec(
                chart_type="clustered_column",
                title="民生指标对比",
                description="教育、医疗、住房、交通等民生领域满意度对比",
                data_format={
                    "categories": ["教育", "医疗", "住房", "交通", "环境", "安全"],
                    "series": [{"name": "满意度", "data": [88, 85, 72, 80, 82, 90]}]
                },
                insights="安全满意度最高（90%），住房满意度最低（72%）。住房问题是当前最突出的民生痛点。"
            ),
            ChartSpec(
                chart_type="treemap",
                title="财政支出结构",
                description="教育、医疗、社保、基建等财政支出占比，反映政府施政重点",
                data_format={
                    "labels": ["教育", "社会保障", "医疗卫生", "基础设施", "其他"],
                    "sizes": [1500, 1200, 900, 800, 1278],
                    "colors": [1, 2, 3, 4, 5]
                },
                insights="教育支出占比最高（26%），社会保障次之（21%）。民生支出合计占比超过60%，体现民生优先导向。"
            )
        ],
        kpis=["GDP增速", "就业率", "空气质量", "民生满意度"],
        insights="""城市经济运行良好，GDP增速6.5%超全国平均，就业充分，空气质量持续改善。
东部新区是城市经济新引擎，增速最快，需要重点支持。
住房满意度最低（72%），是当前最突出的民生痛点，需要重点施策。
财政民生支出占比超60%，体现政府民生优先导向。""",
        recommendations="""1. 加大住房保障力度，增加保障性住房供给，提升住房满意度
2. 重点支持东部新区发展，打造城市经济新引擎
3. 持续推进空气质量改善，目标AQI年均值降至40以下
4. 优化财政支出结构，加大医疗卫生投入
5. 建立城市运行体征实时监测预警机制"""
    ),

    "emergency_command": DashboardTemplate(
        industry="政务",
        template_name="应急指挥&事件处置看板",
        template_id="emergency_command",
        description="突发事件、应急响应、处置效率等应急管理核心指标，对标国家应急管理部标准",
        charts=[
            ChartSpec(
                chart_type="card",
                title="应急指挥核心指标",
                description="今日事件数、处置中事件、平均响应时间、处置完成率——应急管理效率核心指标",
                data_format={
                    "cards": [
                        {"title": "今日事件数", "value": "156件", "change": "-12件"},
                        {"title": "处置中", "value": "23件", "change": "-5件"},
                        {"title": "平均响应时间", "value": "8.5分钟", "change": "-1.5分钟"},
                        {"title": "处置完成率", "value": "85.3%", "change": "+3.2%"}
                    ]
                },
                insights="今日事件数下降，平均响应时间缩短1.5分钟，应急处置效率显著提升。"
            ),
            ChartSpec(
                chart_type="filled_map",
                title="事件地理分布热力图",
                description="各区域突发事件的地理分布，识别高发区域",
                data_format={
                    "regions": ["中心城区", "东部新区", "西部园区", "南部生态区", "北部工业区"],
                    "values": [80, 30, 20, 10, 16]
                },
                insights="中心城区事件最多（51%），主要为交通事故和治安事件。建议加强中心城区巡逻力度。"
            ),
            ChartSpec(
                chart_type="donut",
                title="事件类型分布",
                description="交通事故、火灾、治安、自然灾害等事件类型占比",
                data_format={
                    "labels": ["交通事故", "治安事件", "火灾", "自然灾害", "其他"],
                    "values": [45, 25, 15, 8, 7]
                },
                insights="交通事故占比最高（45%），是应急处置的主要工作。建议加强交通安全管理和宣传。"
            ),
            ChartSpec(
                chart_type="line",
                title="响应时间趋势",
                description="过去30天平均响应时间变化，评估应急处置效率提升",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [{"name": "响应时间(分钟)", "data": [12, 11, 10, 9, 8.5]}]
                },
                insights="响应时间从12分钟降至8.5分钟，持续优化。目标是达到国家标准5分钟以内。"
            )
        ],
        kpis=["今日事件数", "平均响应时间", "处置完成率"],
        insights="""应急处置效率持续提升，响应时间从12分钟降至8.5分钟。
中心城区是事件高发区域，交通事故是最主要的事件类型。
处置完成率85.3%，仍有14.7%的事件处置中，需要加快处置速度。""",
        recommendations="""1. 加强中心城区巡逻力度，提前预防事件发生
2. 加大交通安全管理投入，降低交通事故发生率
3. 优化应急调度系统，目标将响应时间降至5分钟以内
4. 建立事件预测模型，提前预警高风险区域
5. 加强应急队伍培训，提升处置效率"""
    )
}

# ============================================================================
# 十七、汽车/新能源汽车行业（对标帆软汽车、华为云汽车）
# ============================================================================

AUTO_TEMPLATES = {
    "sales_network": DashboardTemplate(
        industry="汽车",
        template_name="汽车产销量&经销商网络看板",
        template_id="sales_network",
        description="产量、销量、库存深度、经销商绩效等汽车行业核心指标，对标比亚迪、吉利等头部车企",
        charts=[
            ChartSpec(
                chart_type="multi_card",
                title="产销核心指标",
                description="月产量、月销量、库存深度、经销商数量、市场占有率——车企经营健康度核心指标",
                data_format={
                    "cards": [
                        {"title": "月产量", "value": "50,000辆", "change": "+15.2%"},
                        {"title": "月销量", "value": "48,500辆", "change": "+18.5%"},
                        {"title": "库存深度", "value": "1.8个月", "change": "-0.2个月"},
                        {"title": "经销商数量", "value": "1,200家", "change": "+50家"},
                        {"title": "市场占有率", "value": "8.5%", "change": "+0.8%"}
                    ]
                },
                insights="销量增速18.5%超过产量增速15.2%，库存深度下降，说明市场需求旺盛。市场占有率持续提升。"
            ),
            ChartSpec(
                chart_type="line",
                title="产销量趋势",
                description="过去12个月产量和销量走势，识别产销平衡状态",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [
                        {"name": "产量", "data": [42000, 44000, 46000, 48000, 50000]},
                        {"name": "销量", "data": [40000, 42500, 44500, 46500, 48500]}
                    ]
                },
                insights="产销量同步增长，销量略低于产量，库存适度积累。建议关注库存深度，避免超过2个月警戒线。"
            ),
            ChartSpec(
                chart_type="clustered_column",
                title="车型销量对比",
                description="各车型的月销量排名，识别主力车型和增长车型",
                data_format={
                    "categories": ["SUV A", "轿车B", "新能源C", "MPV D", "皮卡E"],
                    "series": [{"name": "销量", "data": [18000, 15000, 10000, 4000, 1500]}]
                },
                insights="SUV A是主力车型（占37%），新能源C增速最快（+65%），是未来增长的核心驱动力。"
            ),
            ChartSpec(
                chart_type="filled_map",
                title="全国销售热力图",
                description="各省市销量分布热力，指导区域营销策略",
                data_format={
                    "regions": ["广东", "浙江", "江苏", "北京", "上海"],
                    "values": [8000, 6000, 5500, 5000, 4500]
                },
                insights="广东省销量最高（占16.5%），华东地区整体表现强劲。西部地区销量偏低，有较大增长空间。"
            ),
            ChartSpec(
                chart_type="table",
                title="经销商绩效排行",
                description="各经销商的销量、库存深度、客户满意度综合排行",
                data_format={
                    "columns": ["经销商", "城市", "月销量", "库存深度", "满意度", "评级"],
                    "rows": [
                        ["XX汽车广州店", "广州", "350辆", "1.5月", "96.5%", "A"],
                        ["YY汽车北京店", "北京", "320辆", "2.1月", "94.2%", "B"]
                    ]
                },
                insights="A级经销商占比35%，是销量主力。部分经销商库存深度超过2个月，需要加强库存管理。"
            )
        ],
        kpis=["月销量", "库存深度", "市场占有率"],
        insights="""产销两旺，销量增速18.5%，市场占有率持续提升。
新能源车型增速65%，是未来增长的核心驱动力，需要重点投入。
广东省是最大销售市场，西部地区有较大增长空间。
部分经销商库存偏高，需要加强库存管理。""",
        recommendations="""1. 加大新能源车型产能投入，满足快速增长的市场需求
2. 加强西部地区经销商网络建设，开拓新市场
3. 对库存深度超过2个月的经销商进行专项辅导
4. 建立经销商分层管理体系，推广A级经销商经验
5. 加强广东省市场深耕，巩固最大市场地位"""
    )
}

# ============================================================================
# 十八、房地产行业（对标帆软地产、观远地产）
# ============================================================================

REALESTATE_TEMPLATES = {
    "marketing_sales": DashboardTemplate(
        industry="房地产",
        template_name="楼盘营销&销售转化看板",
        template_id="marketing_sales",
        description="来访量、认购量、签约量、回款率等房地产营销核心指标，对标万科、碧桂园等头部房企",
        charts=[
            ChartSpec(
                chart_type="multi_card",
                title="营销核心指标",
                description="来访量、认购量、签约量、回款额、去化率——楼盘营销健康度核心指标",
                data_format={
                    "cards": [
                        {"title": "月来访量", "value": "1,234组", "change": "+15.2%"},
                        {"title": "认购量", "value": "156套", "change": "+12.5%"},
                        {"title": "签约量", "value": "142套", "change": "+10.8%"},
                        {"title": "月回款额", "value": "¥2.8亿", "change": "+18.5%"},
                        {"title": "去化率", "value": "68.5%", "change": "+5.2%"}
                    ]
                },
                insights="来访量增长15.2%，去化率68.5%处于良好水平（行业均值60%）。回款额增长18.5%，资金回笼加速。"
            ),
            ChartSpec(
                chart_type="funnel",
                title="销售转化漏斗",
                description="来访→认购→签约→回款的完整销售转化链路",
                data_format={
                    "stages": ["来访", "认购", "签约", "回款"],
                    "values": [1234, 156, 142, 135]
                },
                insights="来访到认购转化率12.6%，认购到签约转化率91%，签约到回款转化率95%。来访转化率是最大提升空间。"
            ),
            ChartSpec(
                chart_type="clustered_column",
                title="各渠道来访量对比",
                description="自然到访、中介渠道、线上推广、老带新等渠道的来访量对比",
                data_format={
                    "categories": ["中介渠道", "线上推广", "老带新", "自然到访", "活动"],
                    "series": [{"name": "来访量", "data": [450, 350, 250, 120, 64]}]
                },
                insights="中介渠道来访量最高（36%），老带新转化率最高（25%）。建议加大老带新激励，降低获客成本。"
            ),
            ChartSpec(
                chart_type="stacked_column",
                title="户型销售结构",
                description="各户型的认购量和签约量，识别热销户型",
                data_format={
                    "categories": ["两房", "三房", "四房", "别墅"],
                    "series": [
                        {"name": "认购量", "data": [60, 70, 20, 6]},
                        {"name": "签约量", "data": [55, 65, 18, 4]}
                    ]
                },
                insights="三房是最热销户型（占45%），两房次之（占38%）。别墅去化较慢，需要针对性营销。"
            ),
            ChartSpec(
                chart_type="line",
                title="月度去化率趋势",
                description="过去12个月去化率变化，评估楼盘销售进度",
                data_format={
                    "categories": ["3月", "4月", "5月", "6月", "7月"],
                    "series": [{"name": "去化率", "data": [55, 58, 62, 65, 68.5]}]
                },
                insights="去化率持续提升，从55%提升至68.5%。按当前速度，预计12个月内完成全部去化。"
            )
        ],
        kpis=["月来访量", "签约量", "去化率", "月回款额"],
        insights="""楼盘销售态势良好，去化率68.5%超行业均值，回款加速。
来访到认购转化率12.6%是最大提升空间，优化接待流程可显著提升转化。
老带新渠道转化率最高，是高质量低成本的获客渠道。
别墅去化较慢，需要针对性营销策略。""",
        recommendations="""1. 建立老带新激励机制，扩大高转化率渠道来源
2. 优化售楼处接待流程，提升来访到认购转化率
3. 针对别墅产品制定专项营销方案，加快去化
4. 加强线上推广投入，提升线上渠道来访量
5. 建立客户跟进体系，减少认购到签约的流失"""
    )
}

# ============================================================================
# 十九、客服/运营行业（对标腾讯、观远客服）
# ============================================================================

CUSTOMER_SERVICE_TEMPLATES = {
    "service_quality": DashboardTemplate(
        industry="客服运营",
        template_name="客服质量&工单效率看板",
        template_id="service_quality",
        description="工单量、响应时效、解决率、满意度等客服运营核心指标，对标腾讯、阿里等头部互联网公司客服标准",
        charts=[
            ChartSpec(
                chart_type="multi_card",
                title="客服核心指标",
                description="今日工单量、平均响应时间、首次解决率、客户满意度——客服质量核心指标",
                data_format={
                    "cards": [
                        {"title": "今日工单量", "value": "12,345件", "change": "+5.2%"},
                        {"title": "平均响应时间", "value": "2.5分钟", "change": "-0.5分钟"},
                        {"title": "首次解决率", "value": "78.5%", "change": "+2.1%"},
                        {"title": "客户满意度", "value": "96.5%", "change": "+1.2%"},
                        {"title": "SLA达标率", "value": "98.2%", "change": "+0.5%"}
                    ]
                },
                insights="响应时间缩短，首次解决率提升，满意度达96.5%。SLA达标率98.2%，服务质量稳定。"
            ),
            ChartSpec(
                chart_type="line",
                title="工单量趋势",
                description="过去30天工单量走势，识别服务高峰和异常波动",
                data_format={
                    "categories": ["3-1", "3-2", "3-3", "3-4", "3-5"],
                    "series": [{"name": "工单量", "data": [11000, 11500, 12000, 12200, 12345]}]
                },
                insights="工单量稳步增长，说明业务规模扩大。建议同步扩充客服团队，保持服务质量。"
            ),
            ChartSpec(
                chart_type="donut",
                title="工单类型分布",
                description="咨询、投诉、退款、技术问题等工单类型占比",
                data_format={
                    "labels": ["咨询", "投诉", "退款", "技术问题", "其他"],
                    "values": [45, 20, 18, 12, 5]
                },
                insights="咨询类工单占比最高（45%），投诉占比20%。投诉率偏高，需要分析投诉原因并改进产品/服务。"
            ),
            ChartSpec(
                chart_type="clustered_bar",
                title="客服人员绩效排行",
                description="各客服人员的工单处理量、解决率、满意度综合排行",
                data_format={
                    "categories": ["张客服", "李客服", "王客服", "赵客服", "刘客服"],
                    "series": [
                        {"name": "处理量", "data": [150, 140, 130, 120, 110]},
                        {"name": "满意度", "data": [98, 97, 95, 93, 90]}
                    ]
                },
                insights="张客服处理量最高且满意度最高，是标杆客服。刘客服满意度偏低，需要重点辅导。"
            ),
            ChartSpec(
                chart_type="matrix",
                title="工单类型×处理时效矩阵",
                description="不同工单类型的平均处理时效，识别处理效率短板",
                data_format={
                    "rows": ["咨询", "投诉", "退款", "技术问题"],
                    "columns": ["<1小时", "1-4小时", "4-24小时", ">24小时"],
                    "values": [
                        [80, 15, 4, 1],
                        [30, 40, 25, 5],
                        [20, 35, 35, 10],
                        [15, 30, 40, 15]
                    ]
                },
                insights="技术问题处理时效最长，15%超过24小时。建议建立技术问题快速响应通道，提升处理效率。"
            )
        ],
        kpis=["工单量", "平均响应时间", "首次解决率", "客户满意度"],
        insights="""客服质量整体良好，满意度96.5%，SLA达标率98.2%。
技术问题处理时效是最大短板，15%超过24小时，需要重点改进。
投诉率20%偏高，需要深入分析投诉原因，从根源解决问题。
张客服是标杆，其经验值得在团队内推广。""",
        recommendations="""1. 建立技术问题快速响应通道，目标将技术问题24小时解决率提升至90%
2. 深入分析投诉原因，推动产品/服务改进，降低投诉率至15%以下
3. 推广张客服的服务经验，提升整体团队满意度
4. 建立工单智能分类系统，提升首次解决率
5. 同步扩充客服团队，应对工单量持续增长"""
    ),

}

# ============================================================================
# 看板模板库
# ============================================================================

DASHBOARD_LIBRARY = {
    # 原有行业
    "电商": ECOMMERCE_TEMPLATES,
    "互联网/APP/游戏": INTERNET_TEMPLATES,
    "金融": FINANCE_TEMPLATES,
    "制造": MANUFACTURING_TEMPLATES,
    "零售": RETAIL_TEMPLATES,
    "HR": HR_TEMPLATES,
    "财务": FINANCE_TEMPLATES_GENERAL,
    "文娱": ENTERTAINMENT_TEMPLATES,
    # 补充行业（从 dashboard_templates_supplement.py 合并）
    "医疗健康": HEALTHCARE_TEMPLATES,
    "教育": EDUCATION_TEMPLATES,
    "餐饮连锁": CATERING_TEMPLATES,
    "物流供应链": LOGISTICS_TEMPLATES,
    "能源": ENERGY_TEMPLATES,
    "政务": GOVERNMENT_TEMPLATES,
    "汽车": AUTO_TEMPLATES,
    "房地产": REALESTATE_TEMPLATES,
    "客服运营": CUSTOMER_SERVICE_TEMPLATES
}

# ============================================================================
# 看板生成器
# ============================================================================

class DashboardGenerator:
    """看板生成器"""
    
    def __init__(self):
        self.templates = DASHBOARD_LIBRARY
    
    def get_industry_templates(self, industry: str) -> Dict[str, DashboardTemplate]:
        """获取行业看板模板"""
        return self.templates.get(industry, {})
    
    def get_template(self, industry: str, template_id: str) -> Optional[DashboardTemplate]:
        """获取具体看板模板"""
        templates = self.get_industry_templates(industry)
        return templates.get(template_id)
    
    def list_all_templates(self) -> Dict[str, List[str]]:
        """列出所有看板模板"""
        result = {}
        for industry, templates in self.templates.items():
            result[industry] = list(templates.keys())
        return result
    
    def generate_dashboard_markdown(self, template: DashboardTemplate) -> str:
        """生成看板 Markdown 文档"""
        md = f"""# {template.template_name}

## 看板描述
{template.description}

## 关键指标
{', '.join(template.kpis)}

## 图表组合

"""
        for i, chart in enumerate(template.charts, 1):
            md += f"""### {i}. {chart.title}
**图表类型**: {chart.chart_type}

**简洁解读**: {chart.description}

**数据格式示例**:
```json
{json.dumps(chart.data_format, ensure_ascii=False, indent=2)}
```

**深度洞察**: {chart.insights}

---

"""
        
        md += f"""## 深度洞察
{template.insights}

## 运营建议
{template.recommendations}

"""
        return md
    
    def generate_all_templates_index(self) -> str:
        """生成所有看板模板索引"""
        md = """# 生产级行业标准看板模板库

## 概述
本库包含 9 大行业、20+ 个标准看板模板，每个看板都是基于大厂真实生产场景设计，包含完整的图表组合、数据格式、解读说明和运营建议。

## 行业分类

"""
        for industry, templates in self.templates.items():
            md += f"""### {industry}
"""
            for template_id, template in templates.items():
                md += f"- [{template.template_name}](#{template_id})\n"
            md += "\n"
        
        return md

# ============================================================================
# 使用示例
# ============================================================================

if __name__ == '__main__':
    generator = DashboardGenerator()
    
    # 列出所有模板
    all_templates = generator.list_all_templates()
    print("所有看板模板:")
    for industry, templates in all_templates.items():
        print(f"\n{industry}:")
        for template_id in templates:
            print(f"  - {template_id}")
    
    # 生成电商看板模板
    ecommerce_template = generator.get_template("电商", "ecommerce_overview")
    if ecommerce_template:
        print("\n" + "="*60)
        print("电商全域经营总览看板")
        print("="*60)
        print(generator.generate_dashboard_markdown(ecommerce_template))
