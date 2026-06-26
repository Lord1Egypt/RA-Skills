# 链上数据分析指南

## 核心指标

### 1. 持有者分析

#### 持有者分布
```
健康分布标准:
- 前 10 持有者 < 30%
- 前 50 持有者 < 60%
- 持有者总数持续增长

危险信号:
- 单个地址 > 20%
- 前 5 地址合计 > 50%
- 持有者数量持续下降
```

#### 持有者增长曲线
```python
def analyze_holder_growth(data):
    """
    分析持有者增长质量
    
    正常模式:
    - 初期快速增长 (FOMO阶段)
    - 中期稳定增长 (建设阶段)
    - 长期平稳或缓慢下降 (成熟阶段)
    
    危险模式:
    - 突然暴增后迅速下降 → 可能是刷单
    - 持续下降无反弹 → 项目已死
    - 波浪式增长 → 可能是操纵
    """
    growth_rate = calculate_growth_rate(data['holders'])
    
    if growth_rate['7d'] > 100 and growth_rate['30d'] < 0:
        return "⚠️ 刷单嫌疑 - 短期暴涨后快速下跌"
    elif growth_rate['30d'] < -20:
        return "🔴 项目衰退 - 持有者持续流失"
    elif growth_rate['7d'] > 50 and growth_rate['30d'] > 100:
        return "🟢 健康增长 - 持续吸引新持有者"
    else:
        return "🟡 平稳发展"
```

### 2. 资金流分析

#### 净流量计算
```
净流入 = 大额买入 - 大额卖出

解读:
净流入 > 0: 资金流入，看涨信号
净流入 < 0: 资金流出，看跌信号
```

#### 聪明钱指标
```
聪明钱 = 历史收益率高的钱包

监测指标:
1. 聪明钱持仓变化
2. 聪明钱买入/卖出时机
3. 新聪明钱入场

信号:
- 聪明钱持续买入 → 强烈看涨
- 聪明钱开始卖出 → 警惕顶部
- 新聪明钱入场 → 项目受关注
```

### 3. 交易行为分析

#### 买卖压力
```python
def analyze_buy_sell_pressure(transactions):
    """
    分析买卖压力
    
    买单压力指标:
    - 大单买入数量
    - 买入金额占比
    - 限价买单深度
    
    卖单压力指标:
    - 大单卖出数量  
    - 卖出金额占比
    - 限价卖单深度
    """
    buy_volume = sum(t['amount'] for t in transactions if t['type'] == 'buy')
    sell_volume = sum(t['amount'] for t in transactions if t['type'] == 'sell')
    
    ratio = buy_volume / sell_volume if sell_volume > 0 else float('inf')
    
    if ratio > 2:
        return "🟢 强烈买入压力"
    elif ratio > 1.2:
        return "🟡 温和买入压力"
    elif ratio > 0.8:
        return "⚪ 买卖平衡"
    elif ratio > 0.5:
        return "🟠 温和卖出压力"
    else:
        return "🔴 强烈卖出压力"
```

#### 交易频率
```
高交易频率 + 价格稳定 = 健康换手
高交易频率 + 价格下跌 = 恐慌抛售  
低交易频率 + 价格上涨 = 筹码锁定
低交易频率 + 价格下跌 = 无人问津
```

## 巨鲸钱包数据库

### 已知巨鲸分类

#### Tier 1 巨鲸 ($10M+)
```
特征:
- 持仓价值超过 1000 万美元
- 交易频率低，单次金额大
- 对市场有显著影响力

监控重点:
- 任何大额转账都是重要信号
- 持仓变化预示趋势转折

Solana 知名巨鲸:
- ... (需要持续更新)
```

#### Tier 2 聪明钱 ($1M - $10M)
```
特征:
- 历史收益率高
- 交易有明确逻辑
- 通常提前市场一步

监控重点:
- 新买入的代币
- 加仓/减仓时机
```

### 巨鲸行为模式

#### 积累模式
```
特征:
1. 持续小额买入，避免引起注意
2. 价格下跌时加大买入力度
3. 持仓时间通常较长
4. 伴随持有者数量增长

识别方法:
- 监控特定价格区间的买入订单
- 分析钱包历史交易模式
- 观察与其他钱包的关联
```

#### 派发模式
```
特征:
1. 价格上涨时逐步卖出
2. 可能使用多个钱包分散卖出
3. 伴随社交媒体炒作
4. 持有者增长停滞或下降

识别方法:
- 监控大额转账到交易所
- 分析持有者集中度变化
- 观察链上活跃度与价格背离
```

## 合约安全分析

### 安全检查清单

#### 基础检查
```
✓ 合约是否开源验证
✓ 是否有增发功能 (Mint Authority)
✓ 是否有冻结功能 (Freeze Authority)
✓ 是否有黑名单功能
✓ 税费是否合理 (<10% 为佳)
```

#### 高级检查
```
✓ 合约代码是否经过审计
✓ 是否存在已知漏洞模式
✓ 创建者钱包历史记录
✓ 关联钱包分析
```

### 常见漏洞模式

#### 1. 无限增发
```rust
// 危险代码示例
pub fn mint_token(ctx: Context<MintToken>, amount: u64) -> Result {
    // 没有最大供应量限制
    token::mint_to(ctx.accounts.mint_to_context(), amount)?;
    Ok(())
}
```

#### 2. 隐藏后门
```rust
// 危险代码示例
pub fn transfer_from(ctx: Context<TransferFrom>, amount: u64) -> Result {
    // 允许特定地址无限制转移他人代币
    if ctx.accounts.authority.key() == ADMIN_KEY {
        token::transfer(ctx.accounts.transfer_context(), amount)?;
    }
    Ok(())
}
```

#### 3. 税费陷阱
```rust
// 危险代码示例 - 税费可动态调整至 100%
pub fn update_fee(ctx: Context<UpdateFee>, new_fee: u64) -> Result {
    // 没有费率上限检查
    ctx.accounts.token_data.fee = new_fee; // 可能设置为 100%
    Ok(())
}
```

## 流动性分析

### 流动性健康度

#### 流动性深度
```
健康标准:
- 流动性/市值 比率 > 0.1
- 单笔 1 万美元交易滑点 < 2%
- 单笔 10 万美元交易滑点 < 5%

危险信号:
- 流动性/市值 比率 < 0.05
- 小额交易即产生显著滑点
- 流动性集中在单一池子
```

#### 流动性变化监控
```python
def monitor_liquidity_changes(pool_data):
    """
    监控流动性异常变化
    
    正常模式:
    - 随价格波动正常增减
    - 新增流动性与交易量匹配
    
    危险模式:
    - 突然大额撤出 → Rug Pull 预警
    - 流动性增长但交易量停滞 → 虚假流动性
    """
    current_liquidity = pool_data['liquidity_usd']
    previous_liquidity = pool_data['liquidity_usd_24h_ago']
    
    change_pct = (current_liquidity - previous_liquidity) / previous_liquidity * 100
    
    if change_pct < -50:
        return f"🚨 流动性骤降 {change_pct:.1f}% - 可能 Rug Pull"
    elif change_pct > 100:
        return f"⚠️ 流动性激增 {change_pct:.1f}% - 验证真实性"
    else:
        return f"✓ 流动性变化正常 ({change_pct:+.1f}%)"
```

## 网络健康度

### Solana 链上指标

#### TPS (每秒交易数)
```
正常: 2000+ TPS
拥堵: 1000-2000 TPS
严重拥堵: <1000 TPS

影响:
- 高 TPS = 网络健康，交易确认快
- 低 TPS = 可能拥堵，交易延迟/失败
```

#### 交易成功率
```
健康: > 95%
警告: 90-95%
危险: < 90%

失败原因分析:
1. 滑点设置过低
2. 网络拥堵
3. 交易超时
4. 智能合约错误
```

#### 活跃地址数
```
增长 = 新用户入场，生态扩张
下降 = 用户流失，生态萎缩

注意区分:
- 真实活跃用户 vs 机器人地址
- 新增地址质量
```
