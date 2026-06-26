import sys
import json

def match_resume_jd(resume_json, jd_text):
    """计算简历和JD的匹配度（严格版）"""
    prompt = f"""
请严格按照以下规则分析简历和岗位JD，计算匹配度并生成分析报告，必须客观公正，禁止过度美化：

### 匹配规则（严格执行）
1. 先从JD中提取「核心要求」（标注为必须/要求/需具备的内容）和「加分要求」
2. 核心要求占80%权重，加分要求占20%权重
3. 核心要求只要有1项不满足，整体评分上限不超过60分；2项及以上不满足，上限不超过40分
4. 各维度权重：核心技能匹配40%，岗位职责匹配30%，经验匹配15%，学历匹配15%
5. 评分标准：
   - 90-100分：完全匹配，所有核心要求100%满足，加分要求满足80%以上
   - 70-89分：基本匹配，核心要求全部满足，加分要求满足50%以上
   - 60-69分：勉强匹配，核心要求基本满足，仅1项非关键核心要求不满足
   - <60分：不匹配，核心要求有2项及以上不满足，或1项关键核心要求不满足
6. 必须明确说明是否匹配，禁止模糊表述
7. 所有分析必须完全基于简历和JD的内容，不得编造信息

### 返回格式（严格遵循）
{{
  "overall_score": 0-100,
  "match_result": "完全匹配/基本匹配/勉强匹配/不匹配",
  "dimensions": [
    {{
      "name": "核心技能匹配",
      "score": 0-100,
      "weight": 0.4,
      "matched": ["匹配的核心技能列表"],
      "missing": ["缺失的核心技能列表"],
      "analysis": "详细分析说明，必须明确差距"
    }},
    {{
      "name": "岗位职责匹配",
      "score": 0-100,
      "weight": 0.3,
      "matched": ["匹配的职责经验"],
      "gap": "职责差距描述",
      "analysis": "详细分析说明"
    }},
    {{
      "name": "经验/资历匹配",
      "score": 0-100,
      "weight": 0.15,
      "matched": ["匹配的经验点"],
      "gap": "经验差距描述",
      "analysis": "详细分析说明"
    }},
    {{
      "name": "学历/背景匹配",
      "score": 0-100,
      "weight": 0.15,
      "matched": "匹配结果描述",
      "gap": "背景差距描述（如果有）",
      "analysis": "详细分析说明"
    }}
  ],
  "core_requirements_analysis": {{
    "total_core": 核心要求总数,
    "met_core": 满足的核心要求数量,
    "missing_core": ["未满足的核心要求列表"]
  }},
  "overall_analysis": "整体匹配情况总结，必须客观公正",
  "strengths": ["简历优势列表"],
  "weaknesses": ["简历不足列表，必须明确核心差距"],
  "suggestions": ["具体的优化建议列表"]
}}

### 简历内容
{json.dumps(resume_json, ensure_ascii=False, indent=2)}

### 岗位JD
{jd_text}

要求：只返回JSON，不要任何解释性文字，严格遵守上述规则。
"""
    
    return {
        "status": "success",
        "prompt": prompt,
        "note": "请将上述提示词传入大模型获取匹配度分析结果"
    }

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python match_jd.py <resume-json-path> <jd-text-path>")
        sys.exit(1)
    
    resume_path = sys.argv[1]
    jd_path = sys.argv[2]
    
    try:
        with open(resume_path, 'r', encoding='utf-8') as f:
            resume_json = json.load(f)
        with open(jd_path, 'r', encoding='utf-8') as f:
            jd_text = f.read()
        
        result = match_resume_jd(resume_json, jd_text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
