"""
Q&A 模拟器 - 根据项目内容生成可能的问题和建议回答
"""
import json
from pathlib import Path


# 通用学术项目Q&A问题库
QUESTION_BANK = {
    "methodology": [
        "Why did you choose this particular methodology over alternatives?",
        "How did you validate your approach?",
        "What assumptions does your model/approach make?",
        "Can you explain the theoretical basis for your method?",
        "How reproducible are your results?",
    ],
    "implementation": [
        "What programming language/framework did you use and why?",
        "How did you handle data preprocessing?",
        "What were the biggest technical challenges you faced?",
        "How did you test your code?",
        "What is the time/space complexity of your solution?",
    ],
    "results": [
        "Were the results what you expected? Why or why not?",
        "How do your results compare to existing work/baselines?",
        "What is the statistical significance of your findings?",
        "Can you explain any outliers or unexpected results?",
        "What are the limitations of your results?",
    ],
    "future_work": [
        "If you had more time, what would you do differently?",
        "How would you scale this to a production environment?",
        "What other applications could this approach be used for?",
        "How would you improve the accuracy/performance?",
        "What data would you need to make this more robust?",
    ],
    "critical": [
        "What are the ethical implications of your work?",
        "How does your approach handle edge cases or adversarial inputs?",
        "What happens when your assumptions are violated?",
        "Can you defend the originality of your approach?",
        "What would invalidate your conclusions?",
    ]
}

# 回答框架
ANSWER_FRAMEWORKS = {
    "technical": "Framework: STAR (Situation → Task → Action → Result)",
    "why_chose": "Framework: Criteria comparison (list 2-3 alternatives, show evaluation criteria, explain why chosen method wins)",
    "limitation": "Framework: Acknowledge → Explain impact → Mitigation → Future improvement",
    "dont_know": "Framework: 'That's a great question. I haven't explored that specific angle, but based on [related thing I know], I'd hypothesize that...'",
}


def generate_qa(project_topic, key_methods, key_results, output_path=None):
    """
    根据项目信息生成Q&A准备材料
    
    Args:
        project_topic: 项目主题
        key_methods: 关键方法列表
        key_results: 关键结果列表
        output_path: 输出路径
    """
    qa_doc = []
    qa_doc.append(f"# Q&A 准备材料\n")
    qa_doc.append(f"**项目**: {project_topic}\n")
    qa_doc.append("---\n")
    
    # Section 1: Expected questions by category
    qa_doc.append("## 📋 按类别分类的可能问题\n")
    
    for category, questions in QUESTION_BANK.items():
        qa_doc.append(f"### {category.title().replace('_', ' ')}\n")
        for q in questions:
            qa_doc.append(f"**Q: {q}**")
            qa_doc.append(f"- 💭 Suggested answer: [填写你的回答]")
            qa_doc.append(f"- ⏱️ 建议时长: 30-60秒")
            qa_doc.append("")
    
    # Section 2: Answer frameworks
    qa_doc.append("## 🎯 回答框架\n")
    for fw_type, framework in ANSWER_FRAMEWORKS.items():
        qa_doc.append(f"### {fw_type.title().replace('_', ' ')}")
        qa_doc.append(f"{framework}\n")
    
    # Section 3: Quick tips
    qa_doc.append("## 💡 Q&A 应对策略\n")
    qa_doc.append("""
### 通用策略
1. **先复述问题** — 确认理解 + 给自己思考时间
2. **结构化回答** — "这个问题有三个方面..."
3. **诚实面对不知道的** — "I haven't tested that scenario, but I'd expect..."
4. **桥接技术** — 把不熟悉的问题桥接到你准备好的内容上
5. **具体举例** — 用你项目里的具体case来回答抽象问题

### 高压问题应对
- 如果教授challenge你的方法: 先acknowledge validity of concern → 然后解释你的reasoning
- 如果问你不会的: 承认 → 说你会怎么去找答案 → 提出hypothesis
- 如果问你competitor的方法: 至少准备2-3个alternative approaches的pros/cons

### 时间管理
- 每个回答控制在30-90秒
- 如果一个问题很复杂，说 "Let me address the core of your question first..."
- 结束时简短 "Does that address your question?"
""")

    # Section 4: Practice checklist
    qa_doc.append("## ✅ 练习清单\n")
    qa_doc.append("- [ ] 对着镜子/录像练习回答前5个最可能的问题")
    qa_doc.append("- [ ] 练习 'I don't know' 的回答（不能真的只说不知道）")
    qa_doc.append("- [ ] 准备好1-2个你的项目的亮点故事(30秒版本)")
    qa_doc.append("- [ ] 找同学互相mock interview")
    qa_doc.append("- [ ] 检查PPT上所有数字/claim你都能解释来源")
    
    # Write output
    full_text = "\n".join(qa_doc)
    
    if output_path is None:
        output_path = "output/qa/qa_preparation.md"
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(full_text, encoding='utf-8')
    print(f"  ✅ Q&A准备材料已生成: {output_path}")
    return output_path


if __name__ == "__main__":
    # Demo
    generate_qa(
        project_topic="Machine Learning Based Stock Prediction",
        key_methods=["LSTM", "Random Forest", "Feature Engineering"],
        key_results=["85% accuracy", "Outperforms baseline by 12%"]
    )
