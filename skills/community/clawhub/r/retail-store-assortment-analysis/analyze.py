#!/usr/bin/env python3
"""
门店陈列货盘分析 Skill
核心：分析引起客户意向的商品，以及客户对意向商品的试用行为变化

分析框架：
1. 引起意向的商品变化（深度触达+成交SKU）
2. 客户对意向商品的试用深度变化（深度试用次数/有深度交互SKU）
3. 客户意向分散度变化（深度试用次数/有深度交互客户数）
4. 货盘成交效率变化（成交SKU/陈列SKU，成交客户/有深度交互客户）

数据源：
- displayFunnel: 引起意向的SKU数（深度触达+成交）
- behaviorFunnel: 深度试用次数（客户意向行为）
- customerFunnel: 有深度交互的客户数（意向+成交）
- unreachedSkuCount: 未引起任何意向的SKU
"""

import sys
sys.path.insert(0, '/Users/yangguangwei/.openclaw/workspace-front-door')
from api_client import get_copilot_data


def analyze(store_id: str, from_date: str, to_date: str, store_name: str = ""):
    """陈列货盘分析 - 关注引起客户意向的商品和试用行为变化"""
    
    print("=" * 70)
    print(f"陈列货盘分析报告 - {store_name or store_id}")
    print(f"分析周期: {from_date} 至 {to_date}")
    print("=" * 70)
    print()
    
    # ========== 第一步：获取数据 ==========
    print("【第一步：获取数据】")
    print("API: /api/v1/store/dashboard/bi")
    print(f"参数: storeId={store_id}, fromDate={from_date}, toDate={to_date}")
    print()
    
    data = get_copilot_data(f'/api/v1/store/dashboard/bi?storeId={store_id}&fromDate={from_date}&toDate={to_date}')
    
    # ========== 第二步：提取核心指标 ==========
    print("【第二步：提取核心指标】")
    print()
    
    # 解析三个漏斗
    df = {item['code']: item for item in data.get('displayFunnel', [])}
    bf = {item['code']: item for item in data.get('behaviorFunnel', [])}
    cf = {item['code']: item for item in data.get('customerFunnel', [])}
    
    # 本期数据
    陈列SKU总数 = df['display_sku_count']['value']
    深度触达SKU = df['deep_trial_sku_count']['value']
    成交SKU = df['deal_sku_count']['value']
    未触达SKU = data.get('unreachedSkuCount', 0)
    
    深度试用次数 = bf['deep_trial_times']['value']
    成交件数 = bf['deal_times']['value']
    
    意向客户 = cf['intent_groups']['value']
    成交客户 = cf['deal_groups']['value']
    
    # 上期数据
    陈列SKU总数_上期 = int(df['display_sku_count']['linkRelativeValue'])
    深度触达SKU_上期 = int(df['deep_trial_sku_count']['linkRelativeValue'])
    成交SKU_上期 = int(df['deal_sku_count']['linkRelativeValue'])
    未触达SKU_上期 = data.get('compareUnreachedSkuCount', 0)
    
    深度试用次数_上期 = int(bf['deep_trial_times']['linkRelativeValue'])
    成交件数_上期 = int(bf['deal_times']['linkRelativeValue'])
    
    意向客户_上期 = int(cf['intent_groups']['linkRelativeValue'])
    成交客户_上期 = int(cf['deal_groups']['linkRelativeValue'])
    
    # 计算核心指标
    引起意向的SKU = 深度触达SKU + 成交SKU
    引起意向的SKU_上期 = 深度触达SKU_上期 + 成交SKU_上期
    
    有深度交互的客户 = 意向客户 + 成交客户
    有深度交互的客户_上期 = 意向客户_上期 + 成交客户_上期
    
    print("核心指标提取:")
    print(f"  【货盘】陈列SKU: {陈列SKU总数_上期}→{陈列SKU总数}, 未触达: {未触达SKU_上期}→{未触达SKU}")
    print(f"  【意向商品】引起意向的SKU: {引起意向的SKU_上期}→{引起意向的SKU} (深度触达+成交)")
    print(f"  【意向客户】有深度交互的客户: {有深度交互的客户_上期}→{有深度交互的客户} (意向+成交)")
    print(f"  【意向行为】深度试用次数: {深度试用次数_上期}→{深度试用次数}")
    print()
    
    # ========== 第三步：交叉分析 ==========
    print("【第三步：交叉分析 - 引起意向的商品与试用行为】")
    print()
    
    # 分析1: 引起意向的商品变化
    print("1. 引起客户意向的商品变化:")
    引起意向SKU变化率 = (引起意向的SKU - 引起意向的SKU_上期) / 引起意向的SKU_上期 * 100 if 引起意向的SKU_上期 > 0 else 0
    引起意向SKU占比 = 引起意向的SKU / 陈列SKU总数 * 100 if 陈列SKU总数 > 0 else 0
    引起意向SKU占比_上期 = 引起意向的SKU_上期 / 陈列SKU总数_上期 * 100 if 陈列SKU总数_上期 > 0 else 0
    print(f"   引起意向的SKU数: {引起意向的SKU_上期}个 → {引起意向的SKU}个 ({引起意向SKU变化率:+.1f}%)")
    print(f"   占陈列SKU比例: {引起意向SKU占比_上期:.1f}% → {引起意向SKU占比:.1f}%")
    if 引起意向的SKU < 引起意向的SKU_上期:
        print(f"   ⚠️  能引起客户深度兴趣的商品在变少")
    print()
    
    # 分析2: 客户对意向商品的试用深度
    print("2. 客户对意向商品的试用深度:")
    平均试用深度 = 深度试用次数 / 引起意向的SKU if 引起意向的SKU > 0 else 0
    平均试用深度_上期 = 深度试用次数_上期 / 引起意向的SKU_上期 if 引起意向的SKU_上期 > 0 else 0
    试用深度变化率 = (平均试用深度 - 平均试用深度_上期) / 平均试用深度_上期 * 100 if 平均试用深度_上期 > 0 else 0
    print(f"   平均每个引起意向的SKU被深度试用: {平均试用深度_上期:.2f}次 → {平均试用深度:.2f}次 ({试用深度变化率:+.1f}%)")
    if 平均试用深度 < 平均试用深度_上期:
        print(f"   ⚠️  客户对每个感兴趣商品的体验深度下降")
    print()
    
    # 分析3: 客户意向分散度
    print("3. 客户意向分散度（选择范围）:")
    客户意向分散度 = 深度试用次数 / 有深度交互的客户 if 有深度交互的客户 > 0 else 0
    客户意向分散度_上期 = 深度试用次数_上期 / 有深度交互的客户_上期 if 有深度交互的客户_上期 > 0 else 0
    分散度变化 = 客户意向分散度 - 客户意向分散度_上期
    print(f"   平均每个意向客户深度试用SKU数: {客户意向分散度_上期:.2f}个 → {客户意向分散度:.2f}个 ({分散度变化:+.2f})")
    if 客户意向分散度 < 客户意向分散度_上期:
        print(f"   ✅ 客户选择更集中，意向更明确")
    else:
        print(f"   ⚠️ 客户选择更分散，决策困难")
    print()
    
    # 分析4: 货盘成交效率
    print("4. 货盘成交效率:")
    货盘成交率 = 成交SKU / 陈列SKU总数 * 100 if 陈列SKU总数 > 0 else 0
    货盘成交率_上期 = 成交SKU_上期 / 陈列SKU总数_上期 * 100 if 陈列SKU总数_上期 > 0 else 0
    客户成交率 = 成交客户 / 有深度交互的客户 * 100 if 有深度交互的客户 > 0 else 0
    客户成交率_上期 = 成交客户_上期 / 有深度交互的客户_上期 * 100 if 有深度交互的客户_上期 > 0 else 0
    print(f"   货盘成交率(成交SKU/陈列SKU): {货盘成交率_上期:.1f}% → {货盘成交率:.1f}%")
    print(f"   客户成交率(成交客户/意向客户): {客户成交率_上期:.1f}% → {客户成交率:.1f}%")
    if 货盘成交率 < 货盘成交率_上期:
        print(f"   ⚠️  大量陈列商品无法转化为成交")
    print()
    
    # ========== 第四步：综合诊断 ==========
    print("【第四步：综合诊断】")
    print()
    
    findings = []
    
    # 诊断1: 引起意向的商品减少
    if 引起意向的SKU < 引起意向的SKU_上期 * 0.9:
        findings.append(f"⚠️  引起客户意向的商品大幅减少（{引起意向SKU变化率:.1f}%），货盘吸引力下降")
    
    # 诊断2: 试用深度下降
    if 平均试用深度 < 平均试用深度_上期 * 0.9:
        findings.append(f"⚠️  客户对意向商品的试用深度下降（{试用深度变化率:.1f}%），体验变浅")
    
    # 诊断3: 成交效率恶化
    if 货盘成交率 < 货盘成交率_上期 * 0.8:
        findings.append(f"⚠️  货盘成交率大幅下滑，大量陈列商品无效")
    
    # 诊断4: 客户成交转化
    if 客户成交率 > 客户成交率_上期:
        findings.append(f"✅  客户成交转化率提升，意向客户更容易成交")
    elif 客户成交率 < 客户成交率_上期 * 0.9:
        findings.append(f"⚠️  客户成交转化率下降，意向客户流失")
    
    if findings:
        print("核心发现:")
        for finding in findings:
            print(f"  {finding}")
    else:
        print("  货盘状态稳定")
    print()
    
    # ========== 第五步：行动建议 ==========
    print("【第五步：行动建议】")
    print()
    
    if 引起意向的SKU < 引起意向的SKU_上期 * 0.9:
        print("🔴 优化货盘结构:")
        print("   - 分析上期引起意向的商品特征，引进相似款式")
        print("   - 清理长期未引起任何意向的SKU，释放货盘空间")
        print()
    
    if 平均试用深度 < 平均试用深度_上期 * 0.9:
        print("🟡 提升试用体验:")
        print("   - 培训导购引导客户深度试用，展示商品核心卖点")
        print("   - 优化陈列方式，让客户更容易接触和体验商品")
        print()
    
    if 货盘成交率 < 货盘成交率_上期 * 0.8:
        print("🔴 提高货盘效率:")
        print("   - 识别高潜力SKU重点陈列，低潜力SKU淘汰或促销")
        print("   - 建立SKU动销监控机制，及时清理滞销款")
        print()
    
    print("💡 提示: 统计周期天数会直接影响SKU触达情况")
    print()
    
    print("=" * 70)
    print("分析完成")
    print("=" * 70)


if __name__ == "__main__":
    analyze(
        store_id="416759_1714379448487",
        from_date="2026-03-01",
        to_date="2026-03-26",
        store_name="正义路60号店"
    )
