> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# 三种执行模式 v1.0

> 借鉴 ShotFunClaw `execution-modes.md` 设计，提供快速/标准/完整三种执行模式

---

## 核心理念

不同项目有不同的时间/质量/成本约束。Seedancer v8.0 提供三种执行模式，让用户可以根据实际需求选择合适的执行策略。

---

## 1. 快速模式 (Fast Mode)

### 适用场景
- 时间紧迫（< 2小时交付）
- 原型验证/概念演示
- 内部测试/预演
- 预算有限

### 执行策略
```
1. 跳过 P0-P2 预生产管线
2. 直接进入分镜生成
3. 使用默认参数（无需确认）
4. 批量生成（减少交互轮次）
5. 简化 QA 检查（仅核心项）
```

### 配置参数
```json
{
  "mode": "fast",
  "skipPreProduction": true,
  "defaultModel": "seedance-2.0",
  "batchSize": 10,
  "qaLevel": "minimal",
  "confirmBeforeGenerate": false,
  "estimatedTime": "30-60 min"
}
```

### 优点
- ✅ 速度快（30-60分钟完成）
- ✅ 成本低（使用默认模型）
- ✅ 交互少（减少确认轮次）

### 缺点
- ❌ 质量可能不稳定
- ❌ 可能需要多次迭代
- ❌ 不适合最终交付

---

## 2. 标准模式 (Standard Mode) ⭐ 默认

### 适用场景
- 常规项目（2-4小时交付）
- 客户交付
- 商业项目
- 平衡质量与效率

### 执行策略
```
1. 执行 P0-P1 预生产（简化版）
2. 生成资产清单（需确认）
3. 逐组生成分镜
4. 每组生成后 QA 检查
5. 用户确认后继续下一组
6. 最终汇总交付
```

### 配置参数
```json
{
  "mode": "standard",
  "skipPreProduction": false,
  "preProductionLevel": "simplified",
  "defaultModel": "seedance-2.5",
  "batchSize": 5,
  "qaLevel": "standard",
  "confirmBeforeGenerate": true,
  "estimatedTime": "2-4 hours"
}
```

### 优点
- ✅ 质量稳定
- ✅ 可控性好
- ✅ 适合大多数场景

### 缺点
- ❌ 需要较多交互
- ❌ 时间较长

---

## 3. 完整模式 (Full Mode)

### 适用场景
- 高质量交付项目（4-8小时）
- 重要客户/商业项目
- 需要最高质量保证
- 预算充足

### 执行策略
```
1. 完整执行 P0-P2 预生产管线
2. 详细资产清单（含依赖图）
3. 多轮资产确认
4. 逐组生成 + 详细 QA
5. 多次迭代优化
6. 最终质量检查
7. 完整文档交付
```

### 配置参数
```json
{
  "mode": "full",
  "skipPreProduction": false,
  "preProductionLevel": "complete",
  "defaultModel": "kling-3.0-omni",
  "batchSize": 3,
  "qaLevel": "comprehensive",
  "confirmBeforeGenerate": true,
  "iterationCount": 3,
  "estimatedTime": "4-8 hours"
}
```

### 优点
- ✅ 质量最高
- ✅ 可控性最强
- ✅ 文档完整

### 缺点
- ❌ 时间长
- ❌ 成本高
- ❌ 交互多

---

## 4. 模式选择决策树

```
用户需求
  ├─ 时间 < 2小时？
  │   └─ YES → 快速模式
  ├─ 预算有限？
  │   └─ YES → 快速模式
  ├─ 内部测试/原型？
  │   └─ YES → 快速模式
  ├─ 客户交付？
  │   ├─ 高质量要求？ → 完整模式
  │   └─ 标准质量？ → 标准模式
  ├─ 商业项目？
  │   ├─ 重要客户？ → 完整模式
  │   └─ 一般客户？ → 标准模式
  └─ 默认 → 标准模式
```

---

## 5. 模式切换

### 运行时切换
用户可以在任何时候切换执行模式：

```
用户：切换到快速模式
Agent：
  1. 确认切换意图
  2. 更新配置
  3. 继续执行（使用新模式参数）
```

### 切换注意事项
- ✅ 可以在任务执行中途切换
- ✅ 已完成的任务不会重复
- ⚠️ 切换后配置参数立即生效
- ⚠️ 已确认的资产保持不变

---

## 6. 模式对比表

| 特性 | 快速模式 | 标准模式 | 完整模式 |
|------|---------|---------|---------|
| 执行时间 | 30-60 min | 2-4 hours | 4-8 hours |
| 预生产 | 跳过 | 简化版 | 完整版 |
| 默认模型 | seedance-2.0 | seedance-2.5 | kling-3.0-omni |
| QA 级别 | 最小化 | 标准 | 全面 |
| 批次大小 | 10 | 5 | 3 |
| 确认轮次 | 少 | 中 | 多 |
| 迭代次数 | 1 | 2 | 3 |
| 成本控制 | 低 | 中 | 高 |
| 质量保证 | 基础 | 良好 | 最佳 |

---

## 7. 实施检查清单

### 7.1 SKILL.md 更新
- [ ] 在执行流程章节添加模式选择入口
- [ ] 说明三种模式的适用场景
- [ ] 提供决策树
- [ ] 说明模式切换方法

### 7.2 配置文件
- [ ] 创建 `.seedancer/config.json` 模板
- [ ] 包含三种模式的预设配置
- [ ] 支持运行时修改

### 7.3 流程适配
- [ ] P0-P2 预生产支持跳过/简化/完整
- [ ] 分镜生成支持批次大小配置
- [ ] QA 检查支持不同级别
- [ ] 确认流程支持自动/手动

---

## 8. 参考

- ShotFunClaw `execution-modes.md` - 三种执行模式设计
- Seedancer `references/modes-and-recipes.md` - 现有模式系统

---

**版本**: v1.0  
**创建时间**: 2026-09-10  
**来源**: ShotFunClaw 执行模式设计
