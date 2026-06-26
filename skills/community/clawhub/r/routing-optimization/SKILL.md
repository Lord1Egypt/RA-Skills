# Routing Optimization Skill

**版本**: v1.0
**创建日期**: 2026-03-26
**作者**: 象腿 (main agent)
**用途**: 基于实际使用数据优化routing规则，提升调度准确性

---

## 🎯 核心功能

Routing Optimization skill负责：
1. **数据收集**: 收集routing命中率和准确率数据
2. **规则分析**: 分析哪些规则频繁命中/未命中
3. **A/B测试**: 对比不同routing策略的效果
4. **规则优化**: 基于数据优化routing规则
5. **动态调整**: 支持动态优先级调整

---

## 📋 优化策略

### 策略1: 命中率分析

**目标**: 识别高命中率和低命中率的规则

**方法**:
```python
def analyze_hit_rate(dispatch_logs):
    """
    分析routing规则的命中率

    Args:
        dispatch_logs: 调度日志列表

    Returns:
        dict: 各规则的命中率统计
    """
    rule_stats = {}

    for log in dispatch_logs:
        rule_name = log.get('matched_rule')
        if not rule_name:
            continue

        if rule_name not in rule_stats:
            rule_stats[rule_name] = {
                'hits': 0,
                'success': 0,
                'patterns': set()
            }

        rule_stats[rule_name]['hits'] += 1
        if log.get('success'):
            rule_stats[rule_name]['success'] += 1
        rule_stats[rule_name]['patterns'].add(log.get('matched_pattern'))

    # 计算成功率
    for rule_name in rule_stats:
        stats = rule_stats[rule_name]
        stats['success_rate'] = stats['success'] / stats['hits'] if stats['hits'] > 0 else 0

    return rule_stats
```

**输出示例**:
```json
{
  "coder": {
    "hits": 50,
    "success": 48,
    "success_rate": 0.96,
    "patterns": ["debug", "code", "github"]
  },
  "danao": {
    "hits": 30,
    "success": 28,
    "success_rate": 0.93,
    "patterns": ["search", "research", "study"]
  },
  "self": {
    "hits": 20,
    "success": 18,
    "success_rate": 0.90,
    "patterns": [".*"]
  }
}
```

---

### 策略2: 准确率分析

**目标**: 识别routing规则的准确性

**方法**:
```python
def analyze_routing_accuracy(dispatch_logs):
    """
    分析routing规则的准确性

    Args:
        dispatch_logs: 调度日志列表

    Returns:
        dict: 各规则的准确率统计
    """
    rule_accuracy = {}

    for log in dispatch_logs:
        rule_name = log.get('matched_rule')
        if not rule_name:
            continue

        if rule_name not in rule_accuracy:
            rule_accuracy[rule_name] = {
                'correct': 0,
                'incorrect': 0,
                'fallback': 0
            }

        # 判断是否正确路由
        if log.get('user_satisfied'):
            rule_accuracy[rule_name]['correct'] += 1
        elif log.get('fallback'):
            rule_accuracy[rule_name]['fallback'] += 1
        else:
            rule_accuracy[rule_name]['incorrect'] += 1

    # 计算准确率
    for rule_name in rule_accuracy:
        stats = rule_accuracy[rule_name]
        total = stats['correct'] + stats['incorrect'] + stats['fallback']
        stats['accuracy'] = stats['correct'] / total if total > 0 else 0

    return rule_accuracy
```

---

### 策略3: A/B测试

**目标**: 对比不同routing策略的效果

**方法**:
```python
def ab_test_routing(routing_a, routing_b, test_queries):
    """
    A/B测试两个routing策略

    Args:
        routing_a: 策略A的routing规则
        routing_b: 策略B的routing规则
        test_queries: 测试查询列表

    Returns:
        dict: A/B测试结果
    """
    results_a = []
    results_b = []

    for query in test_queries:
        # 使用策略A路由
        route_a = match_route(query, routing_a)
        results_a.append({
            'query': query,
            'route': route_a,
            'user_rating': None  # 待用户评分
        })

        # 使用策略B路由
        route_b = match_route(query, routing_b)
        results_b.append({
            'query': query,
            'route': route_b,
            'user_rating': None
        })

    # 对比结果
    comparison = {
        'strategy_a': {
            'avg_accuracy': calculate_avg_accuracy(results_a),
            'avg_dispatch_time': calculate_avg_time(results_a)
        },
        'strategy_b': {
            'avg_accuracy': calculate_avg_accuracy(results_b),
            'avg_dispatch_time': calculate_avg_time(results_b)
        },
        'winner': None  # 待确定
    }

    # 确定优胜者
    if comparison['strategy_b']['avg_accuracy'] > comparison['strategy_a']['avg_accuracy']:
        comparison['winner'] = 'B'
    elif comparison['strategy_b']['avg_accuracy'] < comparison['strategy_a']['avg_accuracy']:
        comparison['winner'] = 'A'
    else:
        # 准确率相同，对比速度
        if comparison['strategy_b']['avg_dispatch_time'] < comparison['strategy_a']['avg_dispatch_time']:
            comparison['winner'] = 'B'
        else:
            comparison['winner'] = 'A'

    return comparison
```

---

### 策略4: 动态优先级

**目标**: 根据实时数据动态调整routing优先级

**方法**:
```python
def adjust_routing_priority(rule_stats):
    """
    根据统计数据调整routing优先级

    Args:
        rule_stats: 规则统计字典

    Returns:
        list: 调整后的routing规则列表
    """
    adjusted_rules = []

    for rule_name, stats in rule_stats.items():
        # 基础优先级
        base_priority = get_base_priority(rule_name)

        # 根据成功率调整
        if stats['success_rate'] > 0.95:
            # 高成功率，降低优先级（更快匹配）
            adjusted_priority = base_priority - 1
        elif stats['success_rate'] < 0.85:
            # 低成功率，提高优先级（给更多机会）
            adjusted_priority = base_priority + 1
        else:
            # 正常成功率，保持不变
            adjusted_priority = base_priority

        adjusted_rules.append({
            'rule_name': rule_name,
            'original_priority': base_priority,
            'adjusted_priority': adjusted_priority,
            'reason': f"Success rate: {stats['success_rate']:.2f}"
        })

    # 按调整后的优先级排序
    adjusted_rules.sort(key=lambda x: x['adjusted_priority'])

    return adjusted_rules
```

---

## 🛠️ PowerShell实现

### PowerShell命中率分析

```powershell
function Analyze-RoutingHitRate {
    param(
        [array]$DispatchLogs
    )

    $ruleStats = @{}

    foreach ($log in $DispatchLogs) {
        $ruleName = $log.matched_rule
        if (-not $ruleName) {
            continue
        }

        if (-not $ruleStats.ContainsKey($ruleName)) {
            $ruleStats[$ruleName] = @{
                Hits = 0
                Success = 0
                Patterns = @{}
            }
        }

        $ruleStats[$ruleName].Hits++
        if ($log.success) {
            $ruleStats[$ruleName].Success++
        }

        $pattern = $log.matched_pattern
        if ($pattern) {
            if (-not $ruleStats[$ruleName].Patterns.ContainsKey($pattern)) {
                $ruleStats[$ruleName].Patterns[$pattern] = 0
            }
            $ruleStats[$ruleName].Patterns[$pattern]++
        }
    }

    # 计算成功率
    foreach ($ruleName in $ruleStats.Keys) {
        $stats = $ruleStats[$ruleName]
        $successRate = $stats.Success / $stats.Hits
        $ruleStats[$ruleName]['SuccessRate'] = [math]::Round($successRate, 2)
    }

    return $ruleStats
}
```

---

### PowerShell规则优化

```powershell
function Optimize-RoutingRules {
    param(
        [hashtable]$RuleStats,
        [string]$ConfigPath = "C:\Users\Administrator\.openclaw\workspace-main\skills\agent-dispatch\config.json"
    )

    # 加载当前配置
    $config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
    $currentRules = $config.routing

    $optimizedRules = @()

    foreach ($rule in $currentRules) {
        $ruleName = $rule.target
        $stats = $RuleStats[$ruleName]

        if (-not $stats) {
            # 没有统计数据，保持不变
            $optimizedRules += $rule
            continue
        }

        # 根据命中率优化
        if ($stats.Hits -gt 50 -and $stats.SuccessRate -gt 0.95) {
            # 高命中率规则，考虑添加更多关键词
            Write-Host "Rule '$ruleName' has high hit rate ( $($stats.Hits) hits, $($stats.SuccessRate) success rate)" -ForegroundColor Green
            Write-Host "  Top patterns: $($stats.Patterns.Keys | Sort-Object value -Descending | Select-Object -First 3)"

            # 保持原规则
            $optimizedRules += $rule

        } elseif ($stats.Hits -lt 10) {
            # 低命中率规则，考虑移除或降低优先级
            Write-Host "Rule '$ruleName' has low hit rate ( $($stats.Hits) hits)" -ForegroundColor Yellow
            Write-Host "  Consider removing or lowering priority"

            # 保持原规则（需要人工决策）
            $optimizedRules += $rule

        } elseif ($stats.SuccessRate -lt 0.85) {
            # 低成功率规则，需要优化pattern
            Write-Host "Rule '$ruleName' has low success rate ( $($stats.SuccessRate) )" -ForegroundColor Red
            Write-Host "  Consider optimizing pattern: $($rule.pattern)"

            # 保持原规则（需要人工决策）
            $optimizedRules += $rule

        } else {
            # 正常规则，保持不变
            $optimizedRules += $rule
        }
    }

    # 返回优化建议
    return @{
        OptimizedRules = $optimizedRules
        Suggestions = Generate-OptimizationSuggestions -RuleStats $RuleStats
    }
}

function Generate-OptimizationSuggestions {
    param(
        [hashtable]$RuleStats
    )

    $suggestions = @()

    foreach ($ruleName in $RuleStats.Keys) {
        $stats = $RuleStats[$ruleName]

        # 建议添加的关键词
        if ($stats.Hits -gt 50) {
            $topPatterns = $stats.Patterns.Keys | Sort-Object value -Descending | Select-Object -First 5
            $suggestions += @{
                Rule = $ruleName
                Type = "add_keywords"
                Reason = "High hit rate"
                Keywords = $topPatterns
            }
        }

        # 建议移除的规则
        if ($stats.Hits -lt 5 -and $stats.SuccessRate -lt 0.5) {
            $suggestions += @{
                Rule = $ruleName
                Type = "remove_rule"
                Reason = "Very low hit rate and success rate"
            }
        }

        # 建议优化pattern
        if ($stats.SuccessRate -lt 0.85 -and $stats.Hits -gt 10) {
            $suggestions += @{
                Rule = $ruleName
                Type = "optimize_pattern"
                Reason = "Low success rate despite decent hit rate"
            }
        }
    }

    return $suggestions
}
```

---

## 📊 优化效果评估

### 评估指标

```yaml
metrics:
  - name: "routing_accuracy"
    description: "Routing规则准确率"
    formula: "正确路由数 / 总路由数"
    target: "> 0.9"

  - name: "routing_coverage"
    description: "Routing规则覆盖率"
    formula: "被路由的任务数 / 总任务数"
    target: "> 0.95"

  - name: "avg_routing_time"
    description: "平均路由耗时"
    formula: "总路由时间 / 路由次数"
    target: "< 2s"

  - name: "user_satisfaction"
    description: "用户满意度"
    formula: "满意的路由 / 总路由"
    target: "> 0.9"
```

---

## 🎓 使用示例

### 示例1: 基础优化

```python
# 加载调度日志
dispatch_logs = load_dispatch_logs(days=7)

# 分析命中率
hit_rate = analyze_hit_rate(dispatch_logs)

# 分析准确率
accuracy = analyze_routing_accuracy(dispatch_logs)

# 生成优化建议
suggestions = generate_optimization_suggestions(hit_rate, accuracy)

# 输出报告
print("Routing优化报告:")
for rule_name, stats in hit_rate.items():
    print(f"\n{rule_name}:")
    print(f"  命中率: {stats['hits']} 次")
    print(f"  成功率: {stats['success_rate']:.2%}")
```

### 示例2: A/B测试

```python
# 定义两个routing策略
routing_a = load_routing_config("config-v1.json")
routing_b = load_routing_config("config-v2.json")

# 加载测试查询
test_queries = load_test_queries()

# 运行A/B测试
results = ab_test_routing(routing_a, routing_b, test_queries)

# 输出结果
print(f"策略A准确率: {results['strategy_a']['avg_accuracy']:.2%}")
print(f"策略B准确率: {results['strategy_b']['avg_accuracy']:.2%}")
print(f"优胜者: 策略{results['winner']}")
```

---

## ⚙️ 配置文件

### routing-optimization-config.json

```json
{
  "version": "1.0",
  "config": {
    "data_collection_days": 7,
    "optimization_interval": 604800,
    "enable_ab_testing": true,
    "enable_auto_optimization": false
  },
  "optimization_strategies": {
    "hit_rate_analysis": {
      "enabled": true,
      "high_hit_threshold": 50,
      "low_hit_threshold": 10
    },
    "accuracy_analysis": {
      "enabled": true,
      "min_accuracy": 0.85
    },
    "ab_testing": {
      "enabled": true,
      "sample_size": 100,
      "min_confidence": 0.95
    },
    "dynamic_priority": {
      "enabled": false,
      "adjustment_interval": 86400
    }
  },
  "keywords": {
    "coder": [
      "debug", "code", "github", "pr", "git", "api",
      "编程", "代码", "调试", "开发"
    ],
    "danao": [
      "search", "research", "study", "learn", "总结",
      "搜索", "研究", "学习", "调研"
    ],
    "writer": [
      "write", "article", "content", "公众号", "小红书",
      "写作", "文章", "文案", "创作"
    ],
    "engineer": [
      "design", "architecture", "方案", "系统",
      "设计", "架构", "技术方案"
    ],
    "manager": [
      "schedule", "task", "manage", "飞书", "日程",
      "日程", "任务", "管理", "协作"
    ]
  }
}
```

---

## 🚀 未来优化

### 短期 (1-2周)
- [ ] 添加更多中文关键词
- [ ] 实现自动化A/B测试
- [ ] 添加用户反馈收集

### 中期 (1个月)
- [ ] 实现机器学习优化routing
- [ ] 添加上下文感知routing
- [ ] 实现个性化routing规则

### 长期 (3个月)
- [ ] 引入强化学习优化策略
- [ ] 实现自适应routing调整
- [ ] 构建routing知识库

---

*Skill版本: v1.0*
*最后更新: 2026-03-26*
*维护者: 象腿 (main agent)*
