# 数据结构参考

以下结构用于约束会话状态、单轮记录和最终报告。

## SessionConfig

```json
{
  "target_role": "算法工程师实习生",
  "interviewer_style": "professional",
  "min_rounds": 4,
  "max_round_limit": 8,
  "language": "zh-CN"
}
```

## TurnRecord

```json
{
  "round_id": 1,
  "question_type": "self_intro",
  "interviewer_question": "请先做一个简短的自我介绍，并说明你为什么想应聘这个岗位？",
  "user_audio_path": "xxx.wav",
  "asr_text": "您好，我目前是...",
  "evaluation": {
    "relevance": 4,
    "clarity": 3,
    "specificity": 2,
    "persuasiveness": 3,
    "brief_comment": "回答基本贴题，但与岗位匹配度表达不够突出。"
  },
  "decision": {
    "action": "follow_up",
    "reason": "用户提到了项目经历，但未说明具体贡献。"
  }
}
```

## SessionState

```json
{
  "session_id": "uuid",
  "config": {},
  "current_round": 3,
  "covered_question_types": ["self_intro", "motivation", "project_experience"],
  "turns": [],
  "status": "running"
}
```

## FinalReport

```json
{
  "overall_score": 78,
  "dimension_scores": {
    "relevance": 4.2,
    "clarity": 3.8,
    "specificity": 3.1,
    "persuasiveness": 3.5
  },
  "strengths": [
    "表达自然，能快速进入主题",
    "回答总体贴近问题"
  ],
  "weaknesses": [
    "项目贡献描述不够具体",
    "缺乏量化结果与实例"
  ],
  "round_summaries": [
    {
      "round_id": 1,
      "comment": "自我介绍完整，但岗位匹配度可以更突出。"
    }
  ],
  "improvement_suggestions": [
    "回答项目经历时使用背景-任务-行动-结果结构",
    "强调个人贡献而不是泛泛描述团队工作"
  ],
  "sample_better_answer": "例如在介绍项目时，可以明确说明你负责的模块、采取的方案以及最终结果。"
}
```

## 字段约束

- `action` 仅允许：`follow_up`、`new_question`、`end`
- `interviewer_style` 仅允许：`friendly`、`professional`、`stress`
- 四维评分建议使用 `1-5`
- `overall_score` 可聚合为 `0-100`
