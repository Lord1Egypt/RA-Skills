---
name: shike-autoresearch
description: "CPU-based autonomous optimization loop for skill quality improvement. Runs experiments, evaluates results, keeps improvements. Use when: 自主优化, skill optimization, 达尔文优化, autoresearch."
version: "1.0.0"
author: "Shike"
license: "MIT-0"
tags: [optimization, autoresearch, darwin, skill-quality]
---

# Shike Autoresearch - 自主优化循环

> 基于 Karpathy autoresearch 的 CPU 版本自主优化循环

---

## 核心理念

**评估 → 改进 → 实测验证 → 人类确认 → 保留或回滚**

---

## 必需依赖

- **git** - 版本控制和代码回滚
- **python3** - 运行实验代码
- **subprocess** - 执行实验脚本

---

## 权限说明

本技能需要以下权限（均为功能需求，限制在工作目录内）：
- 修改 `experiment.py` 文件
- 运行 `subprocess` 执行实验
- 写入 `results.tsv` 记录结果
- 执行 `git commit` 和 `git revert`

---

## 三文件架构

| 文件 | 作用 | 谁修改 |
|------|------|--------|
| `config.py` | 配置参数、评估指标 | 只读（人类维护） |
| `experiment.py` | 实验代码、测试逻辑 | Agent 自主修改 |
| `results.tsv` | 实验记录 | 自动追加 |

---

## 自主循环流程

```
LOOP:
1. 查看当前配置状态
2. [检查点1] 确认优化方向
3. 修改 experiment.py
4. [检查点2] 确认改动内容
5. 运行实验
6. 提取结果
7. [检查点3] 确认是否继续
8. 判断：改进 → 保留 / 未改进 → reset
9. 记录到 results.tsv
10. [检查点4] 每10轮复盘
11. 重复
```

---

## 适用场景

### 1. 技能包优化
- 自动测试不同 prompt 配置
- 自动评估技能成功率
- 找到最优技能结构

### 2. 策略回测
- 自动测试不同参数组合
- 自动评估收益率
- 找到最优策略配置

### 3. 内容创作测试
- 自动测试不同写作风格
- 自动评估内容质量
- 找到最优内容策略

---

## 关键检查点

### 检查点1：确认优化方向
触发时机：评估skill前
用户确认：当前最优配置、拟改进方向

### 检查点2：确认改动内容
触发时机：代码修改后，运行前
用户确认：git diff、改动说明

### 检查点3：结果验收
触发时机：优化完成后
用户确认：前后分数对比、是否保留

### 检查点4：定期复盘
触发时机：每10轮迭代后
用户确认：整体进度、趋势、资源消耗

---

## 停止条件

### 自动停止
- 达到最大迭代次数（默认100次）
- 连续10次无改进
- 资源耗尽

### 人工干预
- Ctrl+C - 优雅停止，保存当前状态
- SIGTERM/SIGINT - 接收信号停止

---

## 使用方式

```bash
cd /path/to/skill-directory
python3 run_loop.py --mode skill --target ./my-skill
```

### 参数说明
- `--mode` - 优化模式（skill/strategy/content）
- `--target` - 目标路径
- `--iterations` - 迭代次数（默认100）
- `--timeout` - 单次实验超时（秒，默认60）

---

## 示例输出

```
Round 1: 评估基线 - 62.8分
Round 2: 改进维度1 - 67.6分（+4.8分）
Round 3: 改进维度3 - 72.6分（+5.0分）
Round 4: 改进维度8 - 76.6分（+4.0分）

最终结果：
- 基线分数: 62.8
- 最终分数: 76.6
- 总提升: +13.8分（+22%）
- 成功率: 100%（4/4轮keep）
```

---

## 技术支持

**免费版**：当前版本（MIT-0 license）

**付费服务**：
- 定制优化：¥500-2000/项目
- 企业部署：$500-2000
- 技术咨询：¥300/小时

**联系方式**：
- Email：sijj888@qq.com
- 微信：ailvyou88999

---

## 参考资源

- Karpathy autoresearch: https://github.com/karpathy/autoresearch
- OpenClaw Skills: https://github.com/openclaw/skills