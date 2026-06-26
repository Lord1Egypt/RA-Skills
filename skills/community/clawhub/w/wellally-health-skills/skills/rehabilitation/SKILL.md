---
name: rehabilitation
description: Rehabilitation training management - track exercises, functional assessments (ROM, strength, balance), progress monitoring, and goal achievement
argument-hint: <操作类型+信息，如：start acl-surgery, exercise slr 3x15 pain2, assess rom knee_flexion 120>
allowed-tools: Read, Write
schema: rehabilitation/schema.json
---

# 康复训练管理技能

全面的康复训练管理系统，帮助记录康复进展、评估功能改善和达成康复目标。

## 核心流程

```
用户输入 -> 识别操作类型 -> 提取参数信息 -> 检查完整性 -> [需补充] 询问用户
                                                      |
                                                   [信息完整]
                                                      |
                                              生成JSON -> 保存数据 -> 输出确认
```

## 步骤 1: 解析用户输入

### 操作类型识别

| 输入关键词 | 操作类型 | 说明 |
|-----------|---------|------|
| start | start_rehab | 开始康复追踪 |
| exercise | exercise_log | 记录康复训练 |
| assess | functional_assessment | 功能评估 |
| progress | progress_report | 查看康复进展 |
| goals | goal_management | 康复目标管理 |
| plan | phase_management | 康复阶段管理 |

### 康复类型关键词

#### 骨科康复
| Input Keywords | Type Value |
|---------------|-------------|
| acl, acl-surgery, acl_reconstruction | acl_reconstruction |
| meniscus | meniscus_surgery |
| fracture | fracture |
| replacement, joint | joint_replacement |
| spine | spine_surgery |

#### 运动损伤
| Input Keywords | Type Value |
|---------------|-------------|
| ankle, sprain | ankle_sprain |
| knee | knee_injury |
| shoulder | shoulder_injury |
| elbow, tennis elbow | tennis_elbow |
| strain, muscle | muscle_strain |

#### 神经康复
| Input Keywords | Type Value |
|---------------|-------------|
| stroke | stroke |
| spinal, spinal cord | spinal_cord_injury |
| parkinsons | parkinsons |
| ms, multiple_sclerosis | multiple_sclerosis |

#### 心肺康复
| Input Keywords | Type Value |
|---------------|-------------|
| cardiac | cardiac_surgery |
| copd | copd |
| pneumonia | pneumonia |
| covid | covid_rehab |

### 训练类型关键词

| Input Keywords | Exercise Type |
|---------------|----------------|
| rom | rom_exercises |
| slr, straight leg raise | straight_leg_raise |
| quad, quadriceps | quadriceps_sets |
| hamstring | hamstring_curls |
| calf | calf_raises |
| balance | balance_training |
| single leg | single_leg_stance |
| gait | gait_training |
| stairs | stairs_training |
| sit to stand | sit_to_stand |

### 评估类型关键词

| Input Keywords | Assessment Type |
|---------------|----------------|
| rom | rom_assessment |
| strength | strength_assessment |
| balance | balance_assessment |
| pain | pain_assessment |
| gait | gait_assessment |
| functional | functional_assessment |

### 关节关键词

| Input Keywords | Joint |
|---------------|-------|
| knee | knee |
| hip | hip |
| ankle | ankle |
| shoulder | shoulder |
| elbow | elbow |
| wrist | wrist |

### 活动类型关键词

| 输入关键词 | 活动 |
|-----------|------|
| flexion, 屈曲 | flexion |
| extension, 伸展 | extension |
| abduction, 外展 | abduction |
| rotation, 旋转 | rotation |

### 疼痛评分
- 0-10数字或pain0-pain10

### 目标状态关键词

| 输入关键词 | 状态 |
|-----------|------|
| add, 添加 | add_goal |
| list, 列表 | list_goals |
| active, 进行中 | active_goals |
| completed, 已完成 | completed_goals |
| update, 更新 | update_goal |
| complete, 达成 | complete_goal |
| delete, 删除 | delete_goal |

## 步骤 2: 检查信息完整性

### 开始康复必填:
- 康复类型

### 记录训练必填:
- 训练名称
- 组数和次数 或 时长

### 功能评估必填:
- 评估类型
- 评估结果

## 步骤 3: 交互式询问（如需要）

### 场景 A: 康复类型缺失
```
请选择康复类型：

骨科康复:
- ACL重建术后 (acl)
- 半月板手术 (meniscus)
- 骨折康复 (fracture)
- 关节置换 (replacement)
- 脊柱手术 (spine)

运动损伤:
- 踝关节扭伤 (ankle)
- 膝关节损伤 (knee)
- 肩关节损伤 (shoulder)
- 网球肘 (tennis_elbow)

神经康复:
- 脑卒中 (stroke)
- 脊髓损伤 (spinal)
- 帕金森 (parkinsons)

心肺康复:
- 心脏手术 (cardiac)
- COPD (copd)
```

### 场景 B: 训练信息不完整
```
请提供完整的训练信息：
- 训练名称
- 组数x次数 (如: 3x15)
- 疼痛评分 (0-10)
- 其他备注（可选）
```

### 场景 C: 评估参数缺失
```
请提供评估详情：
- 关节/肌肉
- 活动类型
- 测量值

例如: rom knee_flexion 120
例如: strength quadriceps 4/5
```

## 步骤 4: 生成 JSON

### 康复档案
```json
{
  "rehabilitation_management": {
    "user_profile": {
      "condition": "acl_reconstruction",
      "injury_date": "2025-05-01",
      "surgery_date": "2025-05-15",
      "current_phase": "3",
      "phase_start_date": "2025-06-01"
    },
    "rehabilitation_goals": [
      {
        "goal_id": "goal_001",
        "category": "rom",
        "description": "full_knee_extension",
        "baseline": -10,
        "current": 0,
        "target": 0,
        "unit": "degrees",
        "status": "achieved"
      }
    ],
    "exercise_log": [],
    "functional_assessments": []
  }
}
```

### 训练记录
```json
{
  "id": "ex_20250620080000001",
  "date": "2025-06-20",
  "time": "08:00",
  "exercise_name": "straight_leg_raise",
  "sets": 3,
  "reps": 15,
  "duration_minutes": 10,
  "resistance": "bodyweight",
  "pain_level": 2,
  "rpe": 10,
  "notes": "完成良好，无明显疼痛"
}
```

### 功能评估
```json
{
  "assessment_date": "2025-06-20",
  "rom": {
    "knee_flexion": 120,
    "knee_extension": 0,
    "target_range": "0-135"
  },
  "muscle_strength": {
    "quadriceps": "4/5",
    "hamstrings": "4+/5"
  },
  "pain_assessment": {
    "vas_at_rest": 0,
    "vas_with_activity": 2,
    "location": "anterior_knee"
  },
  "balance": {
    "test_type": "single_leg_stance",
    "duration_seconds": 30,
    "notes": "stable"
  }
}
```

完整 Schema 定义参见 [schema.json](schema.json)。

## 步骤 5: 保存数据

1. 读取 `data/rehabilitation-tracker.json`
2. 根据操作类型更新相应段
3. 更新统计数据
4. 写回文件

## 执行指令

```
1. 识别操作类型 (start/exercise/assess/progress/goals/plan)
2. 提取参数信息
3. 检查必填字段完整性
4. 如有缺失，询问用户补充
5. 生成符合 schema.json 的 JSON
6. 保存到 data/rehabilitation-tracker.json
7. 输出确认信息和康复建议
```

## 示例交互

### 示例 1: 开始康复追踪
```
用户: start acl-surgery 2025-05-01

AI: 已开始康复追踪
━━━━━━━━━━━━━━━━━━━━━━━━
损伤类型: ACL重建术后
损伤日期: 2025-05-01
当前阶段: Phase 1 (保护期)

康复目标:
- 控制肿胀、疼痛
- 恢复伸膝
- 股四头肌激活

注意事项:
- 遵循康复师指导
- 循序渐进，避免过度训练
- 训练时疼痛控制在4/10以下
```

### 示例 2: 记录训练
```
用户: exercise slr 3x15 pain2

AI: 已记录训练
━━━━━━━━━━━━━━━━━━━━━━━━
训练: 直腿抬高
日期: 2025-06-20
组数x次数: 3x15
疼痛评分: 2/10

训练完成良好！疼痛在可接受范围内

今日训练: 1项
本周训练: 5项
```

### 示例 3: 功能评估
```
用户: assess rom knee_flexion 120

AI: 已记录功能评估
━━━━━━━━━━━━━━━━━━━━━━━━
评估类型: 关节活动度
关节: 膝关节
活动: 屈曲
当前角度: 120度
目标范围: 0-135度

进展: 达到目标的 89%
状态: 进展良好

继续努力！目标还差15度
```

### 示例 4: 查看进展
```
用户: progress

AI: 康复进展报告
━━━━━━━━━━━━━━━━━━━━━━━━
康复时长: 50天
当前阶段: Phase 3 (强化期)

功能改善:
- 膝关节屈曲: -10度 -> 120度 (+130度)
- 膝关节伸展: -10度 -> 0度 (已达目标)
- 股四头肌肌力: 3/5 -> 4/5

疼痛控制:
- 静息痛: 0/10
- 活动痛: 2/10

训练依从性: 85% (34/40次计划训练)

目标达成: 2/3 (67%)

评价: 康复进展良好，继续保持！
```

更多示例参见 [examples.md](examples.md)。

## 医学安全边界

### 不能做的事:
- 替代康复师的专业指导和治疗方案
- 给出具体的康复训练处方
- 诊断损伤程度或并发症
- 判断康复预后或恢复时间

### 能做的事:
- 提供康复训练记录和进展追踪
- 提供功能评估记录和趋势分析
- 提供康复目标管理和达成追踪
- 提供训练依从性统计和疼痛监测
- 提供一般性康复建议和专业就医提醒

### 安全原则:
- 循序渐进，不超越当前康复阶段
- 避免过度训练和再次损伤
- 训练时疼痛控制在可接受范围（<4/10）
- 训练后疼痛应在24小时内恢复到基线

### 紧急就医指征:
- 剧烈疼痛（>7/10）
- 关节明显肿胀或变形
- 完全无法负重或活动
- 出现麻木、无力等神经症状
- 伤口红肿、渗出、发热
