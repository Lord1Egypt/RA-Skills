# SIF数据源解析参考

本文件包含各SIF数据源的详细解析代码模板。在分析时按需读取。

## 目录
1. [流量时光机解析](#流量时光机)
2. [流量占比对比解析](#流量占比对比)
3. [广告透视仪解析](#广告透视仪)
4. [关键词转化率解析](#关键词转化率)
5. [坑位快照解析](#坑位快照)
6. [CPA计算公式](#cpa计算)
7. [弱点识别算法](#弱点识别)

---

## 流量时光机

这是一个宽表，7个流量维度并排，每个维度下有多个ASIN列。

```python
def parse_traffic_time_machine(filepath, sheet_name='流量时光机'):
    """解析流量时光机sheet"""
    df = pd.read_excel(filepath, sheet_name=sheet_name, header=None)
    
    # 第1行(index 0): 维度名称 — 自然流量对比, SP广告流量, 品牌广告流量, 视频广告流量, AC推荐流量, 其他推荐流量, 全部流量
    # 第2行(index 1): 各维度下的ASIN列表
    # 第3行起(index 2+): 数据，第1列为日期
    
    dimensions_row = df.iloc[0].tolist()
    asins_row = df.iloc[1].tolist()
    
    # 找到各维度起始列
    dim_names = ['自然流量', 'SP广告流量', '品牌广告流量', '视频广告流量', 'AC推荐流量', '其他推荐流量', '全部流量']
    dim_cols = {}
    for i, val in enumerate(dimensions_row):
        if pd.notna(val):
            val_clean = str(val).strip()
            for dim in dim_names:
                if dim in val_clean:
                    dim_cols[dim] = i
                    break
    
    # 提取ASIN列表（从任意一个维度的行获取）
    asins = []
    for val in asins_row:
        if pd.notna(val) and str(val).startswith('B0'):
            if val not in asins:
                asins.append(str(val))
    
    # 构建结构化数据
    records = []
    for row_idx in range(2, len(df)):
        date = df.iloc[row_idx, 0]
        if pd.isna(date):
            continue
        for dim_name, start_col in dim_cols.items():
            for j, asin in enumerate(asins):
                col_idx = start_col + j  # ASIN在维度起始列后依次排列
                # 需要找到该维度下该ASIN对应的实际列
                # 遍历asins_row从start_col开始找匹配的ASIN
                actual_col = None
                for k in range(start_col, min(start_col + len(asins) + 2, len(asins_row))):
                    if str(asins_row[k]) == asin:
                        actual_col = k
                        break
                if actual_col is not None:
                    val = df.iloc[row_idx, actual_col]
                    records.append({
                        'date': date,
                        'dimension': dim_name,
                        'asin': asin,
                        'traffic_value': val if pd.notna(val) else 0
                    })
    
    return pd.DataFrame(records), asins
```

## 流量占比对比

```python
def parse_traffic_share(filepath, sheet_name=None):
    """解析流量占比对比sheet
    自动检测sheet名（含'流量占比对比'的sheet）
    """
    xls = pd.ExcelFile(filepath)
    if sheet_name is None:
        for s in xls.sheet_names:
            if '流量占比对比' in s:
                sheet_name = s
                break
    
    df = pd.read_excel(filepath, sheet_name=sheet_name, header=None)
    
    # 第2行(index 1)是列名header
    # 格式: #, 关键词, 翻译, ASIN1, ASIN1关键词类型, ASIN2, ASIN2关键词类型, ..., 有效竞品数, 关键词抓取时间, 周搜索量排名, 周搜索量, 在售商品数
    header = df.iloc[1].tolist()
    
    # 提取ASIN列表（列名为B0开头且不含"关键词类型"）
    asins = []
    asin_cols = {}  # {asin: (share_col_idx, type_col_idx)}
    for i, col_name in enumerate(header):
        if pd.notna(col_name):
            col_str = str(col_name)
            if col_str.startswith('B0') and '关键词类型' not in col_str:
                asin = col_str
                asins.append(asin)
                asin_cols[asin] = {'share': i, 'type': i + 1}
    
    # 找固定列
    kw_col = 1  # 关键词
    trans_col = 2  # 翻译
    search_rank_col = None
    search_vol_col = None
    listing_count_col = None
    for i, h in enumerate(header):
        h_str = str(h) if pd.notna(h) else ''
        if '周搜索量排名' in h_str:
            search_rank_col = i
        elif '周搜索量' in h_str and '排名' not in h_str:
            search_vol_col = i
        elif '在售商品数' in h_str:
            listing_count_col = i
    
    # 构建数据
    records = []
    for row_idx in range(2, len(df)):
        keyword = df.iloc[row_idx, kw_col]
        if pd.isna(keyword):
            continue
        
        row_data = {
            'keyword': str(keyword),
            'translation': str(df.iloc[row_idx, trans_col]) if pd.notna(df.iloc[row_idx, trans_col]) else '',
            'weekly_search_rank': df.iloc[row_idx, search_rank_col] if search_rank_col else None,
            'weekly_search_volume': df.iloc[row_idx, search_vol_col] if search_vol_col else None,
            'listing_count': df.iloc[row_idx, listing_count_col] if listing_count_col else None,
        }
        
        for asin in asins:
            share_val = df.iloc[row_idx, asin_cols[asin]['share']]
            type_val = df.iloc[row_idx, asin_cols[asin]['type']]
            row_data[f'{asin}_share'] = float(share_val) if pd.notna(share_val) else 0
            row_data[f'{asin}_type'] = str(type_val) if pd.notna(type_val) else ''
        
        records.append(row_data)
    
    return pd.DataFrame(records), asins
```

## 广告透视仪

```python
def parse_ad_spy(filepath):
    """解析广告透视仪数据"""
    df = pd.read_excel(filepath, header=None)
    
    # 第1行(index 0): 含ASIN信息，格式如 "us站点_B08PJQ3MWB_null"
    asin_info = str(df.iloc[0, 0])
    # 提取ASIN
    target_asin = None
    for part in asin_info.split('_'):
        if part.startswith('B0') and len(part) == 10:
            target_asin = part
            break
    
    # 第2行(index 1)是列名
    # 字段: #, 广告搜索词, 翻译, SP广告流量占比, SP广告流量份额, 有曝光的广告活动, 有曝光的广告组, 有曝光的变体, 搜索量排名, 月搜索量
    col_names = df.iloc[1].tolist()
    
    records = []
    for row_idx in range(2, len(df)):
        row = df.iloc[row_idx]
        if pd.isna(row.iloc[1]):
            continue
        
        record = {}
        for i, col in enumerate(col_names):
            if pd.notna(col):
                val = row.iloc[i]
                col_str = str(col).strip()
                # 百分比处理
                if pd.notna(val) and isinstance(val, str) and '%' in val:
                    val = float(val.replace('%', '')) / 100
                record[col_str] = val
        records.append(record)
    
    result_df = pd.DataFrame(records)
    # 重命名关键列为标准名
    rename_map = {
        '广告搜索词': 'ad_keyword',
        '翻译': 'translation',
        '该词为整个Listing贡献的SP广告流量占比': 'sp_traffic_pct',
        '该Listing在该词下的SP广告流量份额': 'sp_traffic_share',
        '搜索量排名': 'search_rank',
        '月搜索量': 'monthly_search_vol'
    }
    for old, new in rename_map.items():
        for col in result_df.columns:
            if old in col:
                result_df.rename(columns={col: new}, inplace=True)
    
    return result_df, target_asin
```

## 关键词转化率

```python
def parse_keyword_conversion(filepath):
    """解析关键词广告点击转化率数据"""
    df = pd.read_excel(filepath, header=None)
    
    # 第1行(index 0): 含站点+关键词+毛利率信息
    info_str = str(df.iloc[0, 0])
    # 提取毛利率
    margin = None
    if '毛利率' in info_str:
        import re
        m = re.search(r'毛利率([\d.]+)%', info_str)
        if m:
            margin = float(m.group(1)) / 100
    
    # 第2行(index 1)是列名
    col_names = df.iloc[1].tolist()
    
    # 处理重复列名（top3产品转化率出现3次）
    seen = {}
    clean_names = []
    for name in col_names:
        name_str = str(name) if pd.notna(name) else f'col_{len(clean_names)}'
        if name_str in seen:
            seen[name_str] += 1
            name_str = f'{name_str}_{seen[name_str]}'
        else:
            seen[name_str] = 0
        clean_names.append(name_str)
    
    # 构建dataframe
    data_df = df.iloc[2:].copy()
    data_df.columns = clean_names
    data_df = data_df.dropna(subset=['关键词'])
    
    # 转数值
    numeric_cols = ['搜索量', '点击量', '购买量', '搜索转化率', '点击转化率',
                    '建议竞价-最低', '建议竞价-推荐', '建议竞价-最高',
                    'CPA-最低', 'CPA-推荐', 'CPA-最高',
                    'ACOS-最低', 'ACOS-均价', 'ACOS-最高',
                    '产品均价-最低', '产品均价-均价', '产品均价-最高',
                    'ABATop3集中度-点击', 'ABATop3集中度-转化']
    for col in numeric_cols:
        if col in data_df.columns:
            data_df[col] = pd.to_numeric(data_df[col], errors='coerce')
    
    return data_df, margin
```

## 坑位快照

```python
def parse_position_snapshot(filepath):
    """解析坑位快照数据"""
    df = pd.read_excel(filepath, header=0)
    
    # 列结构: 页码-页内排名, 00:00, 图片, 01:00, 图片.1, ...
    # 只保留非图片列
    position_col = df.columns[0]
    time_cols = [col for col in df.columns if '图片' not in str(col) and col != position_col]
    
    records = []
    for _, row in df.iterrows():
        pos = str(row[position_col])  # 如 P1-1
        for time_col in time_cols:
            asin = row[time_col]
            if pd.notna(asin):
                records.append({
                    'position': pos,
                    'time': str(time_col),
                    'asin': str(asin)
                })
    
    return pd.DataFrame(records)
```

## CPA计算

```python
def calculate_cpa_metrics(kw_conv_df, price, margin_rate):
    """计算每个关键词的CPA和盈亏指标
    
    Args:
        kw_conv_df: 关键词转化率DataFrame
        price: 售价（美金）
        margin_rate: 利润率（如0.25）
    """
    profit_per_unit = price * margin_rate  # 单件利润 = 目标CPA
    
    df = kw_conv_df.copy()
    
    # 实际CPA = 建议竞价(推荐) / 点击转化率
    df['actual_cpa'] = df['建议竞价-推荐'] / df['点击转化率']
    # 处理无穷大和NaN
    df['actual_cpa'] = df['actual_cpa'].replace([np.inf, -np.inf], np.nan)
    
    # ACOS = 建议竞价(推荐) / (售价 × 点击转化率)
    df['calc_acos'] = df['建议竞价-推荐'] / (price * df['点击转化率'])
    df['calc_acos'] = df['calc_acos'].replace([np.inf, -np.inf], np.nan)
    
    # 每单盈亏 = 单件利润 - CPA
    df['profit_per_sale'] = profit_per_unit - df['actual_cpa']
    
    # 分档: 绿灯/黄灯/红灯
    conditions = [
        df['actual_cpa'] <= profit_per_unit,  # 绿灯：CPA <= 利润
        (df['actual_cpa'] > profit_per_unit) & (df['actual_cpa'] <= profit_per_unit * 1.2),  # 黄灯：CPA超利润不到20%
    ]
    choices = ['绿灯-盈利', '黄灯-微亏']
    df['signal'] = np.select(conditions, choices, default='红灯-亏损')
    # 数据不足的标记
    df.loc[df['actual_cpa'].isna(), 'signal'] = '数据不足'
    
    df['target_cpa'] = profit_per_unit
    df['price'] = price
    df['margin_rate'] = margin_rate
    
    return df
```

## 弱点识别

```python
def find_competitor_weaknesses(traffic_share_df, ad_spy_df, position_df, 
                                traffic_tm_df, asins, my_asin=None):
    """识别各竞品弱点
    
    返回: {asin: [weakness_dict, ...]}
    """
    weaknesses = {asin: [] for asin in asins}
    
    # 1. 广告空白词：在流量占比中有份额但广告透视仪中无此词
    if ad_spy_df is not None:
        ad_keywords = set(ad_spy_df['ad_keyword'].str.lower().tolist()) if 'ad_keyword' in ad_spy_df.columns else set()
        
        for asin in asins:
            share_col = f'{asin}_share'
            if share_col in traffic_share_df.columns:
                has_share = traffic_share_df[traffic_share_df[share_col] > 0.01]  # 占比>1%
                for _, row in has_share.iterrows():
                    kw = row['keyword'].lower()
                    if kw not in ad_keywords:
                        weaknesses[asin].append({
                            'type': '广告空白',
                            'keyword': row['keyword'],
                            'detail': f"自然流量占比{row[share_col]:.1%}但未投广告",
                            'opportunity': '可投SP广告正面抢夺'
                        })
    
    # 2. 排名不稳定：坑位快照中同一位置不同时段ASIN变化
    if position_df is not None and len(position_df) > 0:
        for asin in asins:
            asin_positions = position_df[position_df['asin'] == asin]
            if len(asin_positions) > 0:
                pos_counts = asin_positions['position'].value_counts()
                total_times = position_df['time'].nunique()
                for pos, count in pos_counts.items():
                    stability = count / total_times
                    if stability < 0.5:  # 出现率不到50%
                        weaknesses[asin].append({
                            'type': '排名不稳定',
                            'keyword': f'坑位{pos}',
                            'detail': f"在{pos}位置仅出现{count}/{total_times}次({stability:.0%})",
                            'opportunity': '排名不稳定可趁机抢坑'
                        })
    
    # 3. 流量下滑：时光机中近期流量下降
    if traffic_tm_df is not None and len(traffic_tm_df) > 0:
        for asin in asins:
            asin_data = traffic_tm_df[traffic_tm_df['asin'] == asin]
            for dim in asin_data['dimension'].unique():
                dim_data = asin_data[asin_data['dimension'] == dim].sort_values('date')
                if len(dim_data) >= 3:
                    recent = dim_data.tail(3)['traffic_value'].values
                    if all(pd.notna(recent)) and recent[0] > 0:
                        if recent[-1] < recent[0] * 0.7:  # 下降超30%
                            weaknesses[asin].append({
                                'type': '流量下滑',
                                'keyword': dim,
                                'detail': f"{dim}近3周下降{(1-recent[-1]/recent[0]):.0%}",
                                'opportunity': f'{dim}渠道竞品正在退出，抢占窗口期'
                            })
    
    return weaknesses
```

## 输出报告模板

使用openpyxl生成报告时的sheet结构和格式参考：

### Sheet 1: 竞品流量全景
- A列: 流量维度
- B-F列: 各竞品ASIN（列头标注ASIN）
- 最后列: 趋势箭头（↑/↓/→）
- 绿色填充表示优势，红色表示劣势

### Sheet 2: 关键词攻防矩阵
- A: 关键词, B: 翻译, C: 周搜索量
- D-H: 各竞品流量占比（条件格式：深色=占比高）
- I: 点击转化率, J: 建议竞价, K: CPA, L: ACOS
- M: 信号灯（绿/黄/红）

### Sheet 3: 攻击清单
- 按优先级P0>P1>P2排序
- 包含：关键词、搜索量、竞价、CPA、ACOS、盈亏、攻击理由、广告类型、优先级

### Sheet 4: 竞品弱点地图
- 每个竞品一个区域
- 列: 弱点类型、关键词/维度、详情、机会点

### Sheet 5: 预算与ROI
- 三档预算（保守/正常/激进）
- 每档包含：日预算、预估日点击、预估日单量、预估日销售额、预估ACOS

### Sheet 6: 作战总结
- 纯文字sheet，A列为标题，B列为内容
- 包含：整体判断、TOP5攻击词、各竞品一句话弱点、预算建议
