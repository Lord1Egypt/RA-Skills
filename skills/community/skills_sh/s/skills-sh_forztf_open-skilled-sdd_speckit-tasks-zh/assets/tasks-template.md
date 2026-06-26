# Tasks Template

# {{FEATURE_NAME}} 实施任务

## 概述

本文档包含 {{FEATURE_NAME}} 功能的详细实施任务，按阶段组织以确保有序执行。

## 阶段 1: 设置任务（项目初始化）

### 目标
建立项目基础结构和配置。

### 任务
- [ ] T001 {{TASK_001_DESCRIPTION}}
- [ ] T002 {{TASK_002_DESCRIPTION}}
- [ ] T003 {{TASK_003_DESCRIPTION}}

## 阶段 2: 基础任务（阻塞先决条件）

### 目标
完成所有用户故事的阻塞先决条件。

### 任务
- [ ] T004 {{TASK_004_DESCRIPTION}}
- [ ] T005 {{TASK_005_DESCRIPTION}}
- [ ] T006 {{TASK_006_DESCRIPTION}}

## 阶段 3: 用户故事 1 {{USER_STORY_1_TITLE}}

### 目标
{{USER_STORY_1_GOAL}}

### 独立测试标准
{{USER_STORY_1_TEST_CRITERIA}}

### 任务
- [ ] T007 [P] [US1] {{US1_TASK_001}}
- [ ] T008 [US1] {{US1_TASK_002}}
- [ ] T009 [US1] {{US1_TASK_003}}

## 阶段 4: 用户故事 2 {{USER_STORY_2_TITLE}}

### 目标
{{USER_STORY_2_GOAL}}

### 独立测试标准
{{USER_STORY_2_TEST_CRITERIA}}

### 任务
- [ ] T010 [P] [US2] {{US2_TASK_001}}
- [ ] T011 [US2] {{US2_TASK_002}}
- [ ] T012 [US2] {{US2_TASK_003}}

## {{ADDITIONAL_PHASES}}

## 最终阶段: 完善和横切关注点

### 目标
完成所有最终优化和系统级改进。

### 任务
- [ ] T{{FINAL_TASK_ID}} [P] {{FINAL_TASK_001}}
- [ ] T{{FINAL_TASK_ID+1}} {{FINAL_TASK_002}}
- [ ] T{{FINAL_TASK_ID+2}} {{FINAL_TASK_003}}

## 依赖关系

### 故事完成顺序
1. 用户故事 1 {{USER_STORY_1_TITLE}} (P1)
2. 用户故事 2 {{USER_STORY_2_TITLE}} (P2)
{{ADDITIONAL_DEPENDENCIES}}

## 并行执行机会

### 用户故事 1
以下任务可以并行执行：
- {{PARALLEL_TASKS_US1}}

### 用户故事 2
以下任务可以并行执行：
- {{PARALLEL_TASKS_US2}}

## 实施策略

### MVP方法
建议首先实施用户故事1以实现MVP功能。

### 增量交付
- 第1增量: 用户故事1完成
- 第2增量: 用户故事2完成
{{ADDITIONAL_INCREMENTS}}

## 验证检查表

- [ ] 所有任务遵循正确的格式规范
- [ ] 每个任务都有明确的文件路径
- [ ] 用户故事可以独立测试
- [ ] 依赖关系已明确标识
- [ ] 并行机会已最大化