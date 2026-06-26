#!/usr/bin/env python3
"""
单SKU门店分析 Skill
分析单个商品在指定门店的销售表现、库存状态、导购贡献和AIoT转化数据

API字段说明：
- dealAmount/dealAvgAmount/qty/giftQty/contributeRate: 统计周期内数据
- inventory: 当前库存数据量
- inStockDays: 统计期间SKU绑定信标在架的天数
- binding: AIoT绑定状态（1=绑定，2=未绑定）
- transFrequency: 上市以来成交频次 = (当前时间-上市时间)/总有效成交件数
- goodsShape: 包型

AIoT performance字段说明：
- inStockDays: 统计期间SKU绑定信标在架的天数
- transGroup: 绑定状态成交的客户组数
- deepTrialGroup: 绑定状态深度试用的组数（意向客户组数）
- trialGroup: 绑定状态累计试用组数（潜在客户组数）
- deepTrialTransRate: 深度试用→成交转化率
- sellThroughRate: 售罄率（已加%，前端展示用）
- sellThroughRateFloat: 售罄率原值
  售罄率公式 = 1 - 期末库存 / (期初库存 + 期间增加库存)
"""

import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# 添加 API 客户端路径
sys.path.insert(0, '/Users/yangguangwei/.openclaw/workspace-front-door')
from api_client import get_copilot_data


@dataclass
class Finding:
    """发现数据类"""
    title: str
    type: str  # fact, anomaly, hypothesis, recommendation
    metric: str
    evidence: str
    confidence: str  # high, medium, low
    implication: str


def fetch_sku_data(store_id: str, goods_base_id: str, from_date: str, to_date: str) -> Dict:
    """获取单SKU门店基础数据"""
    endpoint = f'/api/v1/store/dashboard/bi/goods/detail?storeId={store_id}&fromDate={from_date}&toDate={to_date}&goodsBaseId={goods_base_id}'
    return get_copilot_data(endpoint)


def fetch_sku_performance(store_id: str, goods_base_id: str, from_date: str, to_date: str) -> Dict:
    """获取单SKU导购表现和AIoT数据（仅AIoT门店可用）"""
    endpoint = f'/api/v1/store/dashboard/bi/goods/performance?storeId={store_id}&fromDate={from_date}&toDate={to_date}&goodsBaseId={goods_base_id}'
    return get_copilot_data(endpoint)


def analyze(
    store_id: str,
    goods_base_id: str,
    from_date: str,
    to_date: str,
    store_name: str = "",
    is_aiot_store: bool = True
) -> Dict:
    """
    单SKU门店分析入口
    
    Args:
        store_id: 门店ID
        goods_base_id: 商品基础ID
        from_date: 分析开始日期 (YYYY-MM-DD)
        to_date: 分析结束日期 (YYYY-MM-DD)
        store_name: 门店名称（可选）
        is_aiot_store: 是否为AIoT门店（决定是否获取AIoT数据）
    
    Returns:
        Dict: 分析结果
    """
    
    print(f"\n{'='*70}")
    print(f"单SKU门店分析")
    if store_name:
        print(f"门店: {store_name}")
    print(f"商品ID: {goods_base_id}")
    print(f"分析周期: {from_date} 至 {to_date}")
    print(f"AIoT门店: {'是' if is_aiot_store else '否'}")
    print(f"{'='*70}\n")
    
    # 获取基础数据
    print("【获取SKU基础数据】")
    data = fetch_sku_data(store_id, goods_base_id, from_date, to_date)
    
    if not data or 'goods' not in data:
        return {
            'status': 'error',
            'message': '无法获取SKU数据'
        }
    
    goods = data['goods']
    
    # 获取导购表现数据（AIoT门店）
    performance_data = None
    if is_aiot_store:
        print("【获取导购表现数据】")
        try:
            performance_data = fetch_sku_performance(store_id, goods_base_id, from_date, to_date)
        except Exception as e:
            print(f"  警告: 无法获取AIoT数据 - {e}")
    
    # 解析核心指标
    print("【解析核心指标】")
    metrics = parse_metrics(goods, performance_data)
    
    # 生成发现
    print("【生成分析发现】")
    findings = generate_findings(goods, metrics, performance_data)
    
    # 生成建议
    print("【生成行动建议】")
    recommendations = generate_recommendations(goods, metrics, findings, performance_data)
    
    # 组装结果
    result = {
        'status': 'ok',
        'subject_type': 'sku_store',
        'store_id': store_id,
        'store_name': store_name,
        'goods_base_id': goods_base_id,
        'analysis_period': f"{from_date} 至 {to_date}",
        'is_aiot_store': is_aiot_store,
        'goods_info': {
            'name': goods.get('goodsName', ''),
            'model_code': goods.get('goodsModelCode', ''),
            'color': goods.get('goodsColor', ''),
            'size': goods.get('goodsSize', ''),
            'bag_type': goods.get('goodsShape', ''),  # 包型
            'standard_price': goods.get('standardPrice', 0),
            'launch_date': goods.get('goodsLauchDate', ''),
            'image_url': goods.get('imageUrl', ''),
            'aiot_binding': goods.get('binding', 0),  # AIoT绑定状态
            'aiot_in_stock_days': goods.get('inStockDays', 0)  # AIoT在架天数
        },
        'core_metrics': metrics,
        'findings': [f.__dict__ for f in findings],
        'recommendations': recommendations,
        'raw_data': {
            'goods': goods,
            'performance': performance_data
        }
    }
    
    # 打印分析结果
    print_analysis_result(result)
    
    print(f"\n{'='*70}")
    print("分析完成")
    print(f"{'='*70}\n")
    
    return result


def parse_metrics(goods: Dict, performance_data: Optional[Dict] = None) -> Dict:
    """
    解析核心指标
    
    字段映射：
    - dealAmount/dealAvgAmount/qty/giftQty: 统计周期内数据
    - inventory: 当前库存
    - inStockDays: AIoT在架天数
    - binding: AIoT绑定状态（1=绑定，2=未绑定）
    - transFrequency: 上市以来成交频次
    - contributeRate: 占门店销售额百分比（已加%）
    """
    
    standard_price = goods.get('standardPrice', 0)
    deal_avg_amount = goods.get('dealAvgAmount', 0)
    
    # 计算实际折扣率
    discount_rate = 0
    if standard_price > 0:
        discount_rate = round((1 - deal_avg_amount / standard_price) * 100, 1)
    
    # 计算库销比（当前库存/统计周期销量）
    inventory = goods.get('inventory', 0)
    qty = goods.get('qty', 0)
    inventory_turnover = round(inventory / qty, 1) if qty > 0 else float('inf')
    
    # AIoT绑定状态解读
    binding_state = goods.get('binding', 0)
    binding_desc = {1: '已绑定', 2: '未绑定'}.get(binding_state, '未知')
    
    metrics = {
        'sales': {
            'amount': goods.get('dealAmount', 0),  # 统计周期销售额
            'qty': goods.get('qty', 0),  # 统计周期销量
            'gift_qty': goods.get('giftQty', 0),  # 赠品数量（金额=0的成交）
            'avg_price': deal_avg_amount,  # 统计周期成交均价
            'contribute_rate': goods.get('contributeRate', 0),  # 销售贡献率(%)
            'contribute_rate_float': goods.get('contributeRateFloat', 0),  # 贡献率原值
            'lifetime_frequency': float(goods.get('transFrequency', 0) or 0)  # 上市以来成交频次
        },
        'price': {
            'standard': standard_price,
            'avg_actual': deal_avg_amount,
            'discount_rate': discount_rate
        },
        'inventory': {
            'current': inventory,  # 当前库存
            'turnover_ratio': inventory_turnover  # 库销比
        },
        'aiot': {
            'binding_state': binding_state,  # 1=绑定, 2=未绑定
            'binding_desc': binding_desc,
            'in_stock_days': goods.get('inStockDays', 0)  # AIoT在架天数
        },
        'ranking': {
            'sales_rank': goods.get('dealMoneyTotalRank', 0),
            'share_rank': goods.get('dealMoneyShareRank', 0)
        }
    }
    
    # 解析导购表现数据（AIoT门店）
    if performance_data:
        metrics['clerks'] = parse_clerk_performance(performance_data)
        metrics['vips'] = parse_vip_distribution(performance_data)
        metrics['aiot_performance'] = parse_aiot_performance(performance_data)
    
    return metrics


def parse_clerk_performance(performance_data: Dict) -> Dict:
    """解析导购销售表现"""
    clerks_data = performance_data.get('clerks', {})
    clerks_list = clerks_data.get('list', [])
    
    if not clerks_list:
        return {'list': [], 'total_sales': 0}
    
    # 过滤有销售的导购
    active_clerks = [c for c in clerks_list if c.get('salesAmount', 0) > 0]
    
    # 按销售额排序
    sorted_clerks = sorted(active_clerks, key=lambda x: x.get('salesAmount', 0), reverse=True)
    
    # 计算集中度
    total_sales = clerks_data.get('salesAmountTotal', 0)
    if total_sales > 0 and len(sorted_clerks) > 0:
        top1_share = sorted_clerks[0].get('salesPercentageFloat', 0)
        top3_sales = sum(c.get('salesAmount', 0) for c in sorted_clerks[:3])
        top3_share = top3_sales / total_sales if total_sales > 0 else 0
    else:
        top1_share = 0
        top3_share = 0
    
    return {
        'list': [
            {
                'name': c.get('clerkName', '').strip(),
                'sales_amount': c.get('salesAmount', 0),
                'sales_share': c.get('salesPercentage', '0'),
                'sales_share_float': c.get('salesPercentageFloat', 0),
                'orders': c.get('effectiveOrderCount', 0),
                'qty': c.get('effectiveQtyCount', 0),
                'attach_ratio': c.get('attachQtyRatio', 0),
                # AIoT数据
                'trans_group': c.get('transGroup', 0),
                'deep_trial_group': c.get('deepTrialGroup', 0),
                'trial_group': c.get('trialGroup', 0),
                'deep_trial_trans_rate': c.get('deepTrialTransRate', 0)
            }
            for c in sorted_clerks
        ],
        'total_sales': total_sales,
        'total_qty': clerks_data.get('effectiveQtyCount', 0),
        'concentration': {
            'top1_share': round(top1_share * 100, 1),
            'top3_share': round(top3_share * 100, 1)
        }
    }


def parse_vip_distribution(performance_data: Dict) -> Dict:
    """解析新老客购买分布"""
    vips_data = performance_data.get('vips', {})
    vips_list = vips_data.get('list', [])
    
    new_vip = None
    old_vip = None
    
    for vip in vips_list:
        is_new = vip.get('isNewVip', 0)
        if is_new == 1:
            new_vip = {
                'sales_amount': vip.get('salesAmount', 0),
                'sales_share': vip.get('salesPercentage', '0'),
                'sales_share_float': vip.get('salesPercentageFloat', 0),
                'qty': vip.get('effectiveQtyCount', 0)
            }
        elif is_new == 2:
            old_vip = {
                'sales_amount': vip.get('salesAmount', 0),
                'sales_share': vip.get('salesPercentage', '0'),
                'sales_share_float': vip.get('salesPercentageFloat', 0),
                'qty': vip.get('effectiveQtyCount', 0)
            }
    
    return {
        'new_vip': new_vip,
        'old_vip': old_vip,
        'total_sales': vips_data.get('salesAmountTotal', 0)
    }


def parse_aiot_performance(performance_data: Dict) -> Dict:
    """
    解析AIoT表现数据
    
    字段说明：
    - inStockDays: 统计期间SKU绑定信标在架的天数
    - transGroup: 绑定状态成交的客户组数
    - deepTrialGroup: 绑定状态深度试用的组数（意向客户组数）
    - trialGroup: 绑定状态累计试用组数（潜在客户组数）
    - deepTrialTransRate: 深度试用→成交转化率
    - sellThroughRate: 售罄率（已加%，前端展示用）
    - sellThroughRateFloat: 售罄率原值
      公式: 售罄率 = 1 - 期末库存 / (期初库存 + 期间增加库存)
    """
    perf = performance_data.get('performances', {})
    
    return {
        'in_stock_days': perf.get('inStockDays', 0),  # 统计期间在架天数
        'trans_group': perf.get('transGroup', 0),  # 绑定状态成交客户组数
        'deep_trial_group': perf.get('deepTrialGroup', 0),  # 绑定状态深度试用组数（意向客户）
        'trial_group': perf.get('trialGroup', 0),  # 绑定状态累计试用组数（潜在客户）
        'deep_trial_trans_rate': perf.get('deepTrialTransRate', 0),  # 深度试用→成交转化率
        'sell_through_rate': perf.get('sellThroughRate', '0'),  # 售罄率（%格式）
        'sell_through_rate_float': perf.get('sellThroughRateFloat', 0),  # 售罄率原值
        'level': perf.get('level', '--')  # 等级
    }


def generate_findings(goods: Dict, metrics: Dict, performance_data: Optional[Dict] = None) -> List[Finding]:
    """生成分析发现"""
    findings = []
    
    # 1. 销售额贡献
    contribute_rate = metrics['sales']['contribute_rate']
    if contribute_rate >= 5:
        findings.append(Finding(
            title=f"高贡献SKU，销售占比{contribute_rate}%",
            type="fact",
            metric="contribute_rate",
            evidence=f"该商品销售额¥{metrics['sales']['amount']:,.2f}，占门店总销售的{contribute_rate}%",
            confidence="high",
            implication="核心销售单品，需确保库存充足"
        ))
    elif contribute_rate < 1:
        findings.append(Finding(
            title="销售贡献偏低",
            type="anomaly",
            metric="contribute_rate",
            evidence=f"销售占比仅{contribute_rate}%，低于1%",
            confidence="high",
            implication="可能需要促销或调整陈列位置"
        ))
    
    # 2. 折扣情况
    discount_rate = metrics['price']['discount_rate']
    if discount_rate > 20:
        findings.append(Finding(
            title=f"折扣力度较大（{discount_rate}%）",
            type="anomaly",
            metric="discount_rate",
            evidence=f"标准价¥{metrics['price']['standard']:.0f}，实际成交均价¥{metrics['price']['avg_actual']:.0f}",
            confidence="high",
            implication="高折扣可能压缩利润空间，需评估促销效果"
        ))
    elif discount_rate < 5:
        findings.append(Finding(
            title="价格坚挺，折扣率低",
            type="fact",
            metric="discount_rate",
            evidence=f"平均折扣仅{discount_rate}%，接近正价销售",
            confidence="high",
            implication="商品议价能力强，品牌价值高"
        ))
    
    # 3. 库存状态
    inventory = metrics['inventory']['current']
    qty = metrics['sales']['qty']
    
    if inventory == 0:
        findings.append(Finding(
            title="库存为零，已断货",
            type="anomaly",
            metric="inventory",
            evidence="当前库存为0，无法继续销售",
            confidence="high",
            implication="需立即补货，避免销售损失"
        ))
    elif inventory <= 2 and qty > 0:
        findings.append(Finding(
            title=f"库存偏低（仅剩{inventory}件）",
            type="anomaly",
            metric="inventory",
            evidence=f"库存{inventory}件，本期销量{qty}件",
            confidence="high",
            implication="存在断货风险，建议补货"
        ))
    elif inventory > qty * 3:
        findings.append(Finding(
            title=f"库存积压（{inventory}件）",
            type="anomaly",
            metric="inventory",
            evidence=f"库存{inventory}件，约为本期销量的{inventory/qty:.1f}倍",
            confidence="medium",
            implication="库存周转慢，可能需要促销清理"
        ))
    
    # 4. AIoT绑定状态 + TOP20库存未绑定告警
    aiot_binding = metrics['aiot']['binding_state']
    sales_rank = metrics['ranking']['sales_rank']
    
    if aiot_binding == 2:
        if inventory > 0 and sales_rank <= 20:
            # TOP20商品有库存但未绑定 - 告警
            findings.append(Finding(
                title=f"🔔 告警: TOP{sales_rank}商品库存未绑定AIoT",
                type="anomaly",
                metric="aiot_binding_alert",
                evidence=f"该商品销售排名第{sales_rank}，库存{inventory}件，但未绑定AIoT信标",
                confidence="high",
                implication="TOP商品缺少行为数据追踪，建议立即绑定信标以获取试用、转化数据"
            ))
        elif inventory == 0:
            # 库存为零 - 断货告警
            findings.append(Finding(
                title="🔔 告警: 库存断货且未绑定AIoT",
                type="anomaly",
                metric="stockout_alert",
                evidence="该商品库存为0已断货，且未绑定AIoT信标",
                confidence="high",
                implication="需立即补货并绑定信标，避免销售损失和数据缺失"
            ))
        else:
            findings.append(Finding(
                title="AIoT未绑定",
                type="anomaly",
                metric="aiot_binding",
                evidence="该商品未绑定AIoT信标，无法追踪客户行为数据",
                confidence="high",
                implication="建议绑定AIoT以获取试用、转化等行为数据"
            ))
    
    # 5. 成交频次（上市以来）
    lifetime_freq = metrics['sales']['lifetime_frequency']
    if lifetime_freq > 0:
        if lifetime_freq < 7:
            findings.append(Finding(
                title="高频销售商品",
                type="fact",
                metric="lifetime_frequency",
                evidence=f"上市以来平均每{lifetime_freq:.1f}天成交一次",
                confidence="high",
                implication="动销速度快，是门店畅销款"
            ))
        elif lifetime_freq > 30:
            findings.append(Finding(
                title="动销较慢",
                type="hypothesis",
                metric="lifetime_frequency",
                evidence=f"上市以来平均每{lifetime_freq:.1f}天成交一次",
                confidence="medium",
                implication="可能需要促销或调整陈列以加快周转"
            ))
    
    # 6. 销售排名
    sales_rank = metrics['ranking']['sales_rank']
    if sales_rank == 1:
        findings.append(Finding(
            title="门店销售冠军",
            type="fact",
            metric="sales_rank",
            evidence="该商品销售额排名门店第1",
            confidence="high",
            implication="明星单品，可作为门店主打款推广"
        ))
    elif sales_rank <= 3:
        findings.append(Finding(
            title=f"销售表现优异（排名第{sales_rank}）",
            type="fact",
            metric="sales_rank",
            evidence=f"销售额排名门店前3",
            confidence="high",
            implication="重点SKU，保持库存和陈列"
        ))
    
    # 7. 赠品情况
    gift_qty = metrics['sales']['gift_qty']
    if gift_qty > 0:
        findings.append(Finding(
            title=f"有赠品成交（{gift_qty}单）",
            type="fact",
            metric="gift_qty",
            evidence=f"统计周期内有{gift_qty}单为赠品（金额=0）",
            confidence="high",
            implication="可能用于促销活动或会员礼品"
        ))
    
    # 8. AIoT在架天数（统计期间绑定信标在架天数）
    # 注意：这是统计期间SKU绑定信标在架的天数，不是上市以来的天数
    aiot_in_stock_days = metrics['aiot']['in_stock_days']
    if aiot_in_stock_days > 180:
        findings.append(Finding(
            title=f"老款商品（在架{aiot_in_stock_days}天）",
            type="hypothesis",
            metric="aiot_in_stock_days",
            evidence=f"AIoT系统记录在架{aiot_in_stock_days}天",
            confidence="medium",
            implication="老款可能需要促销清仓，为新款让位"
        ))
    
    # 9. 导购表现分析（AIoT门店）
    if performance_data and 'clerks' in metrics:
        clerks = metrics['clerks']
        if clerks.get('list'):
            # 集中度分析
            top3_share = clerks['concentration']['top3_share']
            if top3_share > 80:
                findings.append(Finding(
                    title=f"销售高度集中（TOP3占{top3_share}%）",
                    type="anomaly",
                    metric="clerk_concentration",
                    evidence=f"该商品销售主要由{len([c for c in clerks['list'] if c['sales_amount'] > 0])}位导购完成，TOP3占比{top3_share}%",
                    confidence="high",
                    implication="销售过于依赖少数导购，存在风险；需培养更多导购销售能力"
                ))
            
            # 零销售导购
            zero_sales_clerks = [c for c in clerks['list'] if c['sales_amount'] == 0]
            if zero_sales_clerks:
                findings.append(Finding(
                    title=f"{len(zero_sales_clerks)}位导购零销售",
                    type="hypothesis",
                    metric="zero_sales_clerks",
                    evidence=f"{', '.join([c['name'] for c in zero_sales_clerks[:3]])}等未售出该商品",
                    confidence="medium",
                    implication="可能存在导购对该商品不熟悉或缺乏销售动力"
                ))
    
    # 10. AIoT转化分析（AIoT门店）
    if performance_data and 'aiot_performance' in metrics:
        aiot_perf = metrics['aiot_performance']
        
        # 深度试用转化率
        deep_trial_trans_rate = aiot_perf.get('deep_trial_trans_rate', 0)
        if deep_trial_trans_rate > 0:
            if deep_trial_trans_rate >= 0.5:
                findings.append(Finding(
                    title=f"深度试用转化率高（{deep_trial_trans_rate:.0%}）",
                    type="fact",
                    metric="deep_trial_trans_rate",
                    evidence=f"深度试用客户中{deep_trial_trans_rate:.0%}最终成交",
                    confidence="high",
                    implication="商品体验后转化效果好，可鼓励导购引导客户深度试用"
                ))
            elif deep_trial_trans_rate < 0.2:
                findings.append(Finding(
                    title=f"深度试用转化率偏低（{deep_trial_trans_rate:.0%}）",
                    type="anomaly",
                    metric="deep_trial_trans_rate",
                    evidence=f"深度试用客户仅{deep_trial_trans_rate:.0%}成交，存在高试用低转化问题",
                    confidence="high",
                    implication="需分析试用后未成交原因，可能是价格、款式或导购跟进不足"
                ))
        
        # 售罄率
        sell_through_rate = aiot_perf.get('sell_through_rate_float', 0)
        if sell_through_rate > 0.8:
            findings.append(Finding(
                title=f"售罄率高（{sell_through_rate:.0%}）",
                type="fact",
                metric="sell_through_rate",
                evidence=f"该商品售罄率达到{sell_through_rate:.0%}",
                confidence="high",
                implication="商品受欢迎，需及时补货"
            ))
    
    # 11. 新老客分布
    if performance_data and 'vips' in metrics:
        vips = metrics['vips']
        new_vip = vips.get('new_vip')
        old_vip = vips.get('old_vip')
        
        if new_vip and old_vip:
            new_share = new_vip.get('sales_share_float', 0)
            old_share = old_vip.get('sales_share_float', 0)
            if new_share > 0.5:
                findings.append(Finding(
                    title="新客购买占比高",
                    type="fact",
                    metric="new_vip_share",
                    evidence=f"新客购买占比{new_share:.0%}，该商品对新客吸引力强",
                    confidence="high",
                    implication="可作为新客引流款，放在显眼位置"
                ))
            elif old_share > 0.8:
                findings.append(Finding(
                    title="老客复购为主",
                    type="fact",
                    metric="old_vip_share",
                    evidence=f"老客购买占比{old_share:.0%}，该商品老客认可度高",
                    confidence="high",
                    implication="可作为老客维护款，通过会员活动推广"
                ))
    
    return findings


def generate_recommendations(goods: Dict, metrics: Dict, findings: List[Finding], performance_data: Optional[Dict] = None) -> List[Dict]:
    """生成行动建议"""
    recommendations = []
    
    # 基于发现生成建议
    finding_metrics = {f.metric: f for f in findings}
    
    # 库存相关建议
    if 'inventory' in finding_metrics and finding_metrics['inventory'].evidence.startswith('库存为零'):
        recommendations.append({
            'priority': 'high',
            'action': '立即补货',
            'details': '该SKU已断货，需紧急补货以避免销售损失',
            'owner': '门店经理/采购'
        })
    elif 'inventory' in finding_metrics and '偏低' in finding_metrics['inventory'].title:
        recommendations.append({
            'priority': 'medium',
            'action': '补充库存',
            'details': f'库存紧张，建议补货至安全库存水平',
            'owner': '门店经理'
        })
    elif 'inventory' in finding_metrics and '积压' in finding_metrics['inventory'].title:
        recommendations.append({
            'priority': 'medium',
            'action': '促销清理库存',
            'details': '库存周转慢，建议通过促销或搭配销售加快周转',
            'owner': '门店经理'
        })
    
    # AIoT绑定建议
    if 'aiot_binding' in finding_metrics:
        recommendations.append({
            'priority': 'medium',
            'action': '绑定AIoT信标',
            'details': '绑定后可获取客户试用、转化等行为数据，支持更精准的分析',
            'owner': '门店经理/技术'
        })
    
    # 折扣相关建议
    if 'discount_rate' in finding_metrics and '折扣力度较大' in finding_metrics['discount_rate'].title:
        recommendations.append({
            'priority': 'medium',
            'action': '评估促销ROI',
            'details': '高折扣销售需评估是否带来足够客流和连带销售',
            'owner': '门店经理'
        })
    
    # 贡献度相关建议
    if 'contribute_rate' in finding_metrics:
        if '高贡献' in finding_metrics['contribute_rate'].title:
            recommendations.append({
                'priority': 'high',
                'action': '确保核心SKU不断货',
                'details': '该商品是门店销售主力，需优先保障库存和陈列',
                'owner': '门店经理'
            })
        elif '偏低' in finding_metrics['contribute_rate'].title:
            recommendations.append({
                'priority': 'low',
                'action': '优化陈列或促销',
                'details': '销售贡献低，可尝试调整陈列位置或限时促销',
                'owner': '门店经理'
            })
    
    # 动销建议
    if 'lifetime_frequency' in finding_metrics and '较慢' in finding_metrics['lifetime_frequency'].title:
        recommendations.append({
            'priority': 'medium',
            'action': '加快动销',
            'details': '上市以来动销较慢，建议通过促销或搭配销售提升周转',
            'owner': '门店经理'
        })
    
    # 导购培训建议
    if 'clerk_concentration' in finding_metrics:
        recommendations.append({
            'priority': 'medium',
            'action': '导购销售培训',
            'details': '销售过于集中，需培训更多导购掌握该商品销售技巧',
            'owner': '门店经理'
        })
    
    if 'zero_sales_clerks' in finding_metrics:
        recommendations.append({
            'priority': 'medium',
            'action': '零销售导购跟进',
            'details': '了解零销售原因，提供商品知识和销售话术培训',
            'owner': '门店经理'
        })
    
    # AIoT转化建议
    if 'deep_trial_trans_rate' in finding_metrics and '偏低' in finding_metrics['deep_trial_trans_rate'].title:
        recommendations.append({
            'priority': 'high',
            'action': '优化试用转化流程',
            'details': '分析试用后未成交原因，改进导购跟进策略或调整价格',
            'owner': '门店经理/导购'
        })
    
    return recommendations


def print_analysis_result(result: Dict):
    """打印分析结果"""
    goods_info = result['goods_info']
    metrics = result['core_metrics']
    
    print(f"\n{'='*70}")
    print(f"商品信息")
    print(f"{'='*70}")
    print(f"名称: {goods_info['name']}")
    print(f"款号: {goods_info['model_code']}")
    print(f"颜色: {goods_info['color']} | 尺寸: {goods_info['size']} | 包型: {goods_info['bag_type']}")
    print(f"上市日期: {goods_info['launch_date']}")
    print(f"AIoT状态: {metrics['aiot']['binding_desc']} | 在架天数: {goods_info['aiot_in_stock_days']}天")
    
    print(f"\n{'='*70}")
    print(f"销售指标（统计周期）")
    print(f"{'='*70}")
    print(f"销售额: ¥{metrics['sales']['amount']:,.2f} (占比{metrics['sales']['contribute_rate']}%)")
    print(f"销量: {metrics['sales']['qty']}件")
    if metrics['sales']['gift_qty'] > 0:
        print(f"赠品: {metrics['sales']['gift_qty']}单")
    print(f"成交均价: ¥{metrics['sales']['avg_price']:.2f}")
    print(f"标准价: ¥{metrics['price']['standard']:.2f}")
    print(f"折扣率: {metrics['price']['discount_rate']}%")
    print(f"销售排名: 第{metrics['ranking']['sales_rank']}名")
    
    print(f"\n{'='*70}")
    print(f"库存指标")
    print(f"{'='*70}")
    print(f"当前库存: {metrics['inventory']['current']}件")
    print(f"库销比: {metrics['inventory']['turnover_ratio']}")
    
    print(f"\n{'='*70}")
    print(f"生命周期指标")
    print(f"{'='*70}")
    if metrics['sales']['lifetime_frequency'] > 0:
        print(f"成交频次: 每{metrics['sales']['lifetime_frequency']:.1f}天一次")
    
    # 导购表现（AIoT门店）
    if 'clerks' in metrics and metrics['clerks'].get('list'):
        print(f"\n{'='*70}")
        print(f"导购销售表现")
        print(f"{'='*70}")
        clerks = metrics['clerks']
        print(f"总销售额: ¥{clerks['total_sales']:,.2f} | 总销量: {clerks['total_qty']}件")
        print(f"TOP1占比: {clerks['concentration']['top1_share']}% | TOP3占比: {clerks['concentration']['top3_share']}%")
        print(f"\n{'排名':<4} {'导购':<10} {'销售额':>10} {'占比':>8} {'订单':>4} {'连带率':>6}")
        print(f"{'-'*60}")
        for i, c in enumerate(clerks['list'][:5], 1):
            print(f"#{i:<3} {c['name']:<10} ¥{c['sales_amount']:>8,.0f} {c['sales_share']:>7} {c['orders']:>4}单 {c['attach_ratio']:>6.2f}")
    
    # 新老客分布
    if 'vips' in metrics:
        print(f"\n{'='*70}")
        print(f"新老客购买分布")
        print(f"{'='*70}")
        vips = metrics['vips']
        if vips.get('new_vip'):
            nv = vips['new_vip']
            print(f"新客: ¥{nv['sales_amount']:,.2f} ({nv['sales_share']}) - {nv['qty']}件")
        if vips.get('old_vip'):
            ov = vips['old_vip']
            print(f"老客: ¥{ov['sales_amount']:,.2f} ({ov['sales_share']}) - {ov['qty']}件")
    
    # AIoT表现
    if 'aiot_performance' in metrics:
        print(f"\n{'='*70}")
        print(f"AIoT表现数据（绑定信标期间）")
        print(f"{'='*70}")
        aiot = metrics['aiot_performance']
        print(f"统计期间在架: {aiot['in_stock_days']}天")
        print(f"潜在客户（试用）: {aiot['trial_group']}组")
        print(f"意向客户（深度试用）: {aiot['deep_trial_group']}组")
        print(f"成交客户: {aiot['trans_group']}组")
        print(f"深度试用→成交转化率: {aiot['deep_trial_trans_rate']:.0%}")
        print(f"售罄率: {aiot['sell_through_rate']}")
    
    if result['findings']:
        print(f"\n{'='*70}")
        print(f"关键发现 ({len(result['findings'])}项)")
        print(f"{'='*70}")
        for i, finding in enumerate(result['findings'], 1):
            emoji = {"fact": "📊", "anomaly": "⚠️", "hypothesis": "💡", "recommendation": "✅"}.get(finding['type'], "•")
            print(f"\n{i}. {emoji} {finding['title']}")
            print(f"   类型: {finding['type']} | 置信度: {finding['confidence']}")
            print(f"   证据: {finding['evidence']}")
            print(f"   影响: {finding['implication']}")
    
    if result['recommendations']:
        print(f"\n{'='*70}")
        print(f"行动建议")
        print(f"{'='*70}")
        for rec in result['recommendations']:
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec['priority'], "•")
            print(f"\n{priority_emoji} {rec['action']}")
            print(f"   详情: {rec['details']}")
            print(f"   负责人: {rec['owner']}")


if __name__ == "__main__":
    # 测试 - AIoT门店
    result = analyze(
        store_id="416759_1714379448487",
        goods_base_id="34311",
        from_date="2026-03-01",
        to_date="2026-03-26",
        store_name="正义路60号店",
        is_aiot_store=True
    )
