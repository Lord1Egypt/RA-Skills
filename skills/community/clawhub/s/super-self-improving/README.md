# 超级自我优化智能体 / Super Self-Improving Agent

基于 self-improving 的增强版，增加多模态记忆、反馈循环、元学习、置信度校准等功能。

## 功能对比

| 特性 | 原版 | 增强版 |
|------|------|--------|
| 记忆类型 | 文本 | 多模态 |
| 反馈来源 | 显式 | 显式+隐式+合成 |
| 错误处理 | 记录 | 分析+预防 |
| 置信度 | 无 | 完整校准 |
| 性能追踪 | 无 | 完整指标 |

## 快速开始

```bash
# 查看统计
python super_self_improving.py stats

# 添加反馈
python super_self_improving.py feedback --explicit "偏好列表而非表格"

# 查看指标
python super_self_improving.py metrics

# 校准
python super_self_improving.py calibrate
```

## 目录结构

```
~/.super-self-improving/
├── memory/      # 记忆存储
├── feedback/    # 反馈收集
├── errors/      # 错误分析
└── meta/       # 元数据
```

## 安全

- 不存储敏感信息
- 不修改系统配置
- 定期清理过期数据
