#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 质量检查模块
对生成的剧集进行质量评分和审核
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ReviewResult:
    """审核结果"""
    passed: bool
    score: float
    checks: Dict[str, Dict[str, Any]]
    suggestions: List[str]
    summary: str


class AIReviewer:
    """AI 质量检查器"""
    
    # 检查项及其权重
    CHECK_ITEMS = {
        "剧情连贯性": {
            "weight": 0.25,
            "description": "与前集衔接是否自然，剧情推进是否合理"
        },
        "人物一致性": {
            "weight": 0.20,
            "description": "角色行为是否符合设定，人物发展是否合理"
        },
        "钩子处理": {
            "weight": 0.20,
            "description": "新增/闭环钩子是否合理，伏笔是否恰当"
        },
        "节奏控制": {
            "weight": 0.15,
            "description": "剧情推进速度是否恰当，是否有拖沓或仓促"
        },
        "情感曲线": {
            "weight": 0.10,
            "description": "情绪起伏是否合理，是否有感染力"
        },
        "创新性": {
            "weight": 0.10,
            "description": "是否有新意，避免老套情节"
        }
    }
    
    # 通过阈值
    PASS_THRESHOLD = 7.0
    
    def __init__(self):
        """初始化审核器"""
        pass
    
    def review_episode(
        self,
        episode_content: str,
        prev_content: Optional[str] = None,
        graph_data: Optional[Dict] = None,
        episode_number: int = 1
    ) -> ReviewResult:
        """
        审核单集内容
        
        注意：实际的AI审核由调用此模块的LLM执行
        此模块提供审核框架和结果结构
        
        Args:
            episode_content: 当前剧集内容
            prev_content: 上一集内容（可选）
            graph_data: 图谱数据（可选）
            episode_number: 剧集序号
            
        Returns:
            ReviewResult 审核结果对象
        """
        # 这个方法由LLM调用时填充实际审核逻辑
        # 这里只返回结构框架
        pass
    
    def create_review_prompt(
        self,
        episode_content: str,
        prev_content: Optional[str] = None,
        graph_data: Optional[Dict] = None,
        episode_number: int = 1
    ) -> str:
        """
        创建审核提示词
        
        Args:
            episode_content: 当前剧集内容
            prev_content: 上一集内容
            graph_data: 图谱数据
            episode_number: 剧集序号
            
        Returns:
            审核提示词
        """
        prompt = f"""# 剧集质量审核任务

## 审核对象
- 剧集序号：第 {episode_number} 集
- 内容：{episode_content}

"""
        
        if prev_content:
            prompt += f"""## 上一集内容
{prev_content}

"""
        
        if graph_data:
            prompt += f"""## 图谱数据
{json.dumps(graph_data, ensure_ascii=False, indent=2)}

"""
        
        prompt += """## 审核要求

请对上述剧集进行质量审核，按以下维度评分（每项0-10分）：

| 维度 | 权重 | 说明 |
|------|------|------|
| 剧情连贯性 | 25% | 与前集衔接是否自然，剧情推进是否合理 |
| 人物一致性 | 20% | 角色行为是否符合设定，人物发展是否合理 |
| 钩子处理 | 20% | 新增/闭环钩子是否合理，伏笔是否恰当 |
| 节奏控制 | 15% | 剧情推进速度是否恰当 |
| 情感曲线 | 10% | 情绪起伏是否合理，是否有感染力 |
| 创新性 | 10% | 是否有新意，避免老套情节 |

## 输出格式

请以JSON格式输出审核结果：

```json
{
  "passed": true/false,
  "score": 综合得分(0-10),
  "checks": {
    "剧情连贯性": {"score": 分数, "comment": "评语"},
    "人物一致性": {"score": 分数, "comment": "评语"},
    "钩子处理": {"score": 分数, "comment": "评语"},
    "节奏控制": {"score": 分数, "comment": "评语"},
    "情感曲线": {"score": 分数, "comment": "评语"},
    "创新性": {"score": 分数, "comment": "评语"}
  },
  "suggestions": ["改进建议1", "改进建议2"],
  "summary": "总体评价"
}
```

注意：综合得分低于7分视为不通过。
"""
        return prompt
    
    def parse_review_result(self, response: str) -> ReviewResult:
        """
        解析审核结果
        
        Args:
            response: AI返回的审核结果（JSON格式）
            
        Returns:
            ReviewResult 对象
        """
        try:
            # 尝试提取JSON
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]
            
            data = json.loads(json_str.strip())
            
            return ReviewResult(
                passed=data.get("passed", False),
                score=data.get("score", 0),
                checks=data.get("checks", {}),
                suggestions=data.get("suggestions", []),
                summary=data.get("summary", "")
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            # 解析失败，返回默认结果
            return ReviewResult(
                passed=False,
                score=0,
                checks={},
                suggestions=[f"解析审核结果失败: {str(e)}"],
                summary="审核结果解析失败"
            )
    
    def format_review_output(self, result: ReviewResult) -> str:
        """
        格式化审核结果输出
        
        Args:
            result: 审核结果
            
        Returns:
            格式化的输出字符串
        """
        status_icon = "✅" if result.passed else "❌"
        
        output = f"""
{status_icon} AI 质量审核结果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
综合评分：{result.score:.1f}/10
审核状态：{'通过' if result.passed else '未通过'}

详细评分：
"""
        
        for item, weight_info in self.CHECK_ITEMS.items():
            check = result.checks.get(item, {})
            score = check.get("score", 0)
            comment = check.get("comment", "")
            output += f"  • {item}: {score}分 - {comment}\n"
        
        if result.suggestions:
            output += "\n改进建议：\n"
            for i, suggestion in enumerate(result.suggestions, 1):
                output += f"  {i}. {suggestion}\n"
        
        output += f"\n总结：{result.summary}\n"
        output += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        return output


# 单例实例
_ai_reviewer = None

def get_ai_reviewer() -> AIReviewer:
    """获取AI审核器单例"""
    global _ai_reviewer
    if _ai_reviewer is None:
        _ai_reviewer = AIReviewer()
    return _ai_reviewer