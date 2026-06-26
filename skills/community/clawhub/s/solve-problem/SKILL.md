---
name: solve-problem
description: Search knowledge base and research solutions
description_zh: "搜索知识库并研究解决方案"
compatibility: opencode
metadata:
  trigger: "solve problem"
  core: learn-expand
  source: db/capabilities_clawhub.py
  function: intelligent_problem_solver
---

# Solve Problem

## Description
Search knowledge base and research solutions

## Trigger
When user says or types: **"solve problem"**

## Core Association
This capability belongs to **learn-expand** core.

## Implementation
Calls `intelligent_problem_solver()` from `capabilities_clawhub.py`

## Usage
```python
from capability_executor import execute_capability
execute_capability("solve problem")
```


## 中文说明
搜索知识库并研究解决方案

## 触发方式
用户说"solve problem"时触发
## Dependencies
- capabilities_clawhub.py in D:\\coze-local\\db
- capability_executor.py (registration + dispatch)

## Linkage
- Reports failures to skill_evolver (MetaClaw) and seal_coevolution (SEAL)
- Confidence tracked via capability_executor

## 触发场景
- 用户说"解决问题"、"怎么办"、"如何解决"
- 用户说"搜索知识库"、"查方案"
- 用户说"遇到问题"、"故障处理"


## B站学习
> 学习时间: 2026-06-01 20:57

- **北京蜂巢智创**: Problem Solving_ 6 Skills needed to solve any problem
  - 关键词: Problem, Solving_, Skills, needed, to
- **Wangqing19910913**: 【计算器教程】Solve求解方程，零点法最全合集
  - 关键词: 计算器教程, Solve求解方程, 零点法最全合集

## B站学习
> 学习时间: 2026-06-01 21:02

- **北京蜂巢智创**: Problem Solving_ 6 Skills needed to solve any problem
- **Wangqing19910913**: 【计算器教程】Solve求解方程，零点法最全合集
- **电脑维修达人小锦**: win11系统 a problem has been蓝屏怎么解决

## 融合来源: solve-problem-bd4e6f
> 融合时间: 自动合并

> 学习时间: 2026-06-01 21:08
- **应无所住Drrrake**: 用python解微分方程（导入scipy.integrate库的solve_ivp)
- **远程修电脑-2416976775**: 开机黑屏Your device ran into a problem and needs to restart 0% complete解决方法
- **Wangqing19910913**: 【计算器教程】Solve求解方程，零点法最全合集
> 融合时间: 自动合并
> 学习时间: 2026-06-02 07:53
- **bili_93184898726**: G6-G9-2-4（中英文字幕）Solve Problems with Ratios and Proportions
- **海俊频道**: 发现问题解决问题_Find Problem Solve Problem_Ariana Glantz_20230805
- **长江三夜**: Solve problem

## B站学习 (第1轮)
> 学习时间: 2026-06-02 09:21

- **北京蜂巢智创**: Problem Solving_ 6 Skills needed to solve any problem
  https://www.bilibili.com/video/BV1QL4y1g73r
- **电脑维修达人小锦**: win11系统 a problem has been蓝屏怎么解决
  https://www.bilibili.com/video/BV1Pk4y1h7X2
- **投胎钱的记忆1020**: No boyfriend, no problem, no girlfriend, no problem, no money.Big problem.
  https://www.bilibili.com/video/BV1DWZ6B3E5w

## B站学习 (第2轮)
> 学习时间: 2026-06-02 09:35

- **北京蜂巢智创**: Problem Solving_ 6 Skills needed to solve any problem
  https://www.bilibili.com/video/BV1QL4y1g73r
- **电脑维修达人小锦**: win11系统 a problem has been蓝屏怎么解决
  https://www.bilibili.com/video/BV1Pk4y1h7X2
- **投胎钱的记忆1020**: No boyfriend, no problem, no girlfriend, no problem, no money.Big problem.
  https://www.bilibili.com/video/BV1DWZ6B3E5w
