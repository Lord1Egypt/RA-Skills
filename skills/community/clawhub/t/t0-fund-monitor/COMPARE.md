# 多平台对比测试指南

## 🎯 测试目标

验证 `fund-monitor` 在不同 OpenClaw 平台上的输出一致性。

---

## 📋 测试准备

### 1. 统一配置

在所有平台上使用相同的配置：

```yaml
# config/default.yaml
monitor:
  interval: 60
  fast_mode: true
  
signals:
  buy:
    kdj_max: 20
    kdj_early: 30
    volume_ratio: 1.2
```

### 2. 统一监控列表

```bash
# 在所有平台执行相同的命令
python3 monitor.py add 512880,513050,159915,513310,513080
```

### 3. 清理旧数据

```bash
# 在每个平台运行
./tools/clean_data.sh
```

---

## 🧪 测试用例

### 用例 1: 数据获取一致性

**目的**: 验证同一时间的数据是否一致

**步骤**:
1. 同时在多个平台执行
2. 记录同一时间的基金价格
3. 对比差异

**命令**:
```bash
python3 -c "
from data_fetch import get_fund_realtime
import datetime
r = get_fund_realtime('512880')
print(f'{datetime.datetime.now()} - 512880: {r[\"price\"]}')
"
```

**预期**: 价格差异 < 0.5%（允许延迟）

---

### 用例 2: 指标计算一致性

**目的**: 验证指标计算结果是否一致

**步骤**:
1. 使用相同的 K 线数据
2. 在多个平台计算指标
3. 对比 MACD、KDJ、RSI 值

**命令**:
```bash
python3 -c "
from data_fetch import get_fund_1min_kline
from indicators import calculate_indicators, get_latest_indicators

kline = get_fund_1min_kline('512880')
kline_ind = calculate_indicators(kline, fast_mode=True)
ind = get_latest_indicators(kline_ind)

print(f'MACD DIF: {ind[\"macd_dif\"]:.6f}')
print(f'MACD DEA: {ind[\"macd_dea\"]:.6f}')
print(f'KDJ K: {ind[\"kdj_k\"]:.1f}')
print(f'RSI: {ind[\"rsi\"]:.1f}')
"
```

**预期**: 指标值完全一致（浮点数误差 < 0.0001）

---

### 用例 3: 信号生成一致性

**目的**: 验证信号生成逻辑是否一致

**步骤**:
1. 使用相同的指标数据
2. 在多个平台生成信号
3. 对比信号类型和数量

**预期**: 信号完全一致

---

### 用例 4: 性能对比

**目的**: 对比不同平台的执行性能

**步骤**:
1. 同时启动监控
2. 记录每次检查耗时
3. 统计 1 小时的平均耗时

**命令**:
```bash
# 监控日志中的执行时间
tail -f logs/monitor.log | grep "检查完成"
```

**记录表**:

| 平台 | 平均耗时 | 最快 | 最慢 | 内存 |
|------|----------|------|------|------|
| 平台 A | ___秒 | ___秒 | ___秒 | ___MB |
| 平台 B | ___秒 | ___秒 | ___秒 | ___MB |
| 平台 C | ___秒 | ___秒 | ___秒 | ___MB |

---

### 用例 5: 健壮性对比

**目的**: 验证异常处理能力

**测试项**:

| 测试 | 平台 A | 平台 B | 平台 C |
|------|--------|--------|--------|
| 断网恢复 | ✅/❌ | ✅/❌ | ✅/❌ |
| 数据源异常 | ✅/❌ | ✅/❌ | ✅/❌ |
| 重复启动 | ✅/❌ | ✅/❌ | ✅/❌ |
| 配置错误 | ✅/❌ | ✅/❌ | ✅/❌ |

---

## 📊 结果记录模板

### 每日对比报告

```markdown
# 对比测试报告 - 2026-03-18

## 测试环境
- 平台 A: [描述]
- 平台 B: [描述]
- 平台 C: [描述]

## 信号对比

| 时间 | 平台 A | 平台 B | 平台 C | 一致性 |
|------|--------|--------|--------|--------|
| 10:15 | 512880 买入 | 512880 买入 | 512880 买入 | ✅ |
| 10:32 | 无 | 无 | 无 | ✅ |
| 11:05 | 513050 卖出 | 513050 卖出 | 513050 卖出 | ✅ |

## 性能对比

| 平台 | 平均耗时 | 信号数 | 成功率 |
|------|----------|--------|--------|
| 平台 A | 18.5 秒 | 3 | 100% |
| 平台 B | 22.3 秒 | 3 | 100% |
| 平台 C | 19.1 秒 | 3 | 98% |

## 结论
- 信号一致性：✅ 一致
- 性能差异：平台 B 较慢（+20%）
- 建议：[建议内容]
```

---

## 🔧 自动化对比脚本

```bash
#!/bin/bash
# compare_platforms.sh

PLATFORMS=("平台 A" "平台 B" "平台 C")
CODES="512880,513050,159915"

echo "=== 多平台对比测试 ==="
echo "时间：$(date)"
echo ""

for platform in "${PLATFORMS[@]}"; do
    echo "测试 $platform..."
    # SSH 执行或本地执行
    # ssh user@$platform "cd ~/.openclaw/skills/fund-monitor && python3 monitor.py status"
done
```

---

## ⚠️ 注意事项

1. **时间同步**: 确保所有平台时间一致（NTP 同步）
2. **网络环境**: 尽量使用相似的网络环境
3. **数据源**: 确认所有平台访问相同的数据源
4. **时区设置**: 统一设置为 Asia/Shanghai
5. **Python 版本**: 建议使用相同的 Python 版本

---

## 📈 成功标准

| 指标 | 标准 |
|------|------|
| 信号一致性 | ≥ 95% |
| 指标计算 | 完全一致 |
| 性能差异 | < 30% |
| 健壮性 | 所有平台通过 |

---

**祝对比测试顺利！** 🎯
