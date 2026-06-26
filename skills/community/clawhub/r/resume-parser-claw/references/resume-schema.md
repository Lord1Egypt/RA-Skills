# 简历标准字段定义

## 候选人数据结构（JSON Schema）

```json
{
  "candidate_id": "string (自动生成，手机号或邮箱的哈希)",
  "parse_time": "YYYY-MM-DD HH:mm",
  "quality_score": "integer (0-100)",

  "basic": {
    "name": "string",
    "gender": "男 | 女 | 未知",
    "age": "integer | null",
    "phone": "string",
    "email": "string",
    "city": "string",
    "photo_url": "string | null"
  },

  "intention": {
    "target_position": "string",
    "expected_salary": "string (如 '15k-20k')",
    "available_date": "string (如 '随时到岗' 或 'YYYY-MM')"
  },

  "education": [
    {
      "school": "string",
      "major": "string",
      "degree": "本科 | 硕士 | 博士 | 专科 | 高中",
      "start": "YYYY-MM",
      "end": "YYYY-MM",
      "gpa": "string | null"
    }
  ],

  "work_experience": [
    {
      "company": "string",
      "position": "string",
      "start": "YYYY-MM",
      "end": "YYYY-MM | 至今",
      "description": "string",
      "achievements": ["string"]
    }
  ],

  "work_years": "integer (自动计算)",
  "highest_degree": "本科 | 硕士 | 博士 | 专科 | 高中",

  "skills": {
    "tech": ["string"],
    "soft": ["string"],
    "languages": ["string"],
    "certifications": ["string"]
  },

  "projects": [
    {
      "name": "string",
      "role": "string",
      "tech_stack": ["string"],
      "description": "string",
      "outcome": "string"
    }
  ],

  "confidence": {
    "name": "integer (0-100)",
    "phone": "integer (0-100)",
    "email": "integer (0-100)"
  }
}
```

## 飞书多维表格建表结构

创建候选人数据库时，推荐以下字段配置：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 姓名 | 文本（主字段） | candidate.basic.name |
| 手机 | 文本 | candidate.basic.phone |
| 邮箱 | 文本 | candidate.basic.email |
| 所在城市 | 文本 | candidate.basic.city |
| 期望职位 | 文本 | candidate.intention.target_position |
| 期望薪资 | 文本 | candidate.intention.expected_salary |
| 工作年限 | 数字 | candidate.work_years |
| 最高学历 | 单选 | 本科/硕士/博士/专科/高中 |
| 技能标签 | 多选 | candidate.skills.tech |
| 简历质量分 | 数字 | candidate.quality_score |
| 解析时间 | 日期 | candidate.parse_time |
| 原始简历 | 附件 | 可选，上传原始文件 |
| 状态 | 单选 | 待筛选/已邀约/已面试/已录用/已淘汰 |
| 备注 | 文本 | 人工补充信息 |

## 必填字段

解析时以下字段为核心字段，缺失时降低质量分：
- `basic.name`（缺失 -40 分）
- `basic.phone` 或 `basic.email`（缺失 -30 分）
- `work_experience` 或 `education`（缺失 -20 分）
