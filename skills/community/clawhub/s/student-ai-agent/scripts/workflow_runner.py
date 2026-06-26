"""
Student AI Agent - 项目工作流主控脚本
======================================
完整7步工作流:
1. 分析作业要求
2. 扩展想法 (头脑风暴 + 方案设计)
3. 写代码 (Python原型)
4. 检查代码 + 生成output图片
5. 生成docx报告
6. 生成PPT + 演讲稿
7. 模拟Q&A

使用方法: 把作业要求文本放入 input/assignment.md，运行此脚本
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

def ensure_dirs():
    """Create all necessary directories"""
    for d in [INPUT_DIR, OUTPUT_DIR, OUTPUT_DIR / "code", 
              OUTPUT_DIR / "figures", OUTPUT_DIR / "report",
              OUTPUT_DIR / "presentation", OUTPUT_DIR / "qa"]:
        d.mkdir(parents=True, exist_ok=True)

def read_assignment():
    """Read assignment requirements"""
    assignment_file = INPUT_DIR / "assignment.md"
    if not assignment_file.exists():
        print("❌ Error: 请把作业要求放入 input/assignment.md")
        sys.exit(1)
    return assignment_file.read_text(encoding='utf-8')

def step1_analyze(assignment_text):
    """Step 1: 分析作业要求"""
    print("\n" + "="*60)
    print("📋 Step 1: 分析作业要求")
    print("="*60)
    
    analysis = {
        "raw_requirements": assignment_text,
        "parsed": {
            "course": "",          # 课程名
            "topic": "",           # 主题
            "deliverables": [],    # 需要交付的东西
            "constraints": [],     # 约束条件（字数、格式等）
            "deadline": "",        # 截止日期
            "grading_criteria": [],# 评分标准
            "key_questions": [],   # 需要回答的核心问题
            "technical_requirements": []  # 技术要求
        }
    }
    
    # Save analysis template
    output_file = OUTPUT_DIR / "01_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ 分析模板已生成: {output_file}")
    return analysis

def step2_brainstorm(analysis):
    """Step 2: 扩展想法"""
    print("\n" + "="*60)
    print("💡 Step 2: 扩展想法 & 方案设计")
    print("="*60)
    
    brainstorm = {
        "approaches": [],      # 可能的方案
        "selected_approach": "",  # 选定的方案
        "architecture": "",    # 技术架构
        "methodology": "",     # 方法论
        "data_sources": [],    # 数据来源
        "expected_results": "", # 预期结果
        "innovation_points": [] # 创新点
    }
    
    output_file = OUTPUT_DIR / "02_brainstorm.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(brainstorm, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ 方案设计已生成: {output_file}")
    return brainstorm

def step3_code(brainstorm):
    """Step 3: 写代码"""
    print("\n" + "="*60)
    print("💻 Step 3: 写代码")
    print("="*60)
    
    code_dir = OUTPUT_DIR / "code"
    
    # Generate main.py template
    main_py = code_dir / "main.py"
    main_py.write_text('''#!/usr/bin/env python3
"""
Project: [PROJECT_NAME]
Course: [COURSE_NAME]
Student: [STUDENT_NAME]
Date: {date}

Description: [DESCRIPTION]
"""

import os
import sys
import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# =============================================
# Configuration
# =============================================
OUTPUT_DIR = Path("../figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================
# Core Implementation
# =============================================

def main():
    """Main entry point"""
    print("=" * 50)
    print("  [PROJECT_NAME] - Running...")
    print("=" * 50)
    
    # TODO: Implement core logic
    
    print("\\n✅ All tasks completed successfully!")
    print(f"📁 Output saved to: {{OUTPUT_DIR}}")

if __name__ == "__main__":
    main()
'''.format(date=datetime.now().strftime('%Y-%m-%d')), encoding='utf-8')
    
    # Generate requirements.txt
    req_file = code_dir / "requirements.txt"
    req_file.write_text('''numpy>=1.21
matplotlib>=3.5
pandas>=1.3
python-docx>=0.8.11
Pillow>=9.0
''', encoding='utf-8')
    
    print(f"  ✅ 代码模板已生成: {code_dir}")
    return code_dir

def step4_check_and_visualize(code_dir):
    """Step 4: 检查代码 + 生成图片"""
    print("\n" + "="*60)
    print("🔍 Step 4: 代码检查 & 生成Output图片")
    print("="*60)
    
    figures_dir = OUTPUT_DIR / "figures"
    
    checklist = {
        "syntax_check": False,
        "runs_without_error": False,
        "output_generated": False,
        "figures_saved": [],
        "errors_found": [],
        "warnings": []
    }
    
    output_file = OUTPUT_DIR / "04_check_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(checklist, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ 检查清单已生成: {output_file}")
    print(f"  📊 图片输出目录: {figures_dir}")
    return checklist

def step5_report(analysis, brainstorm, checklist):
    """Step 5: 生成docx报告"""
    print("\n" + "="*60)
    print("📄 Step 5: 生成Word报告 (.docx)")
    print("="*60)
    
    report_dir = OUTPUT_DIR / "report"
    
    # Report structure template
    report_structure = {
        "title": "",
        "sections": [
            {"heading": "1. Introduction", "content": "Background and objectives"},
            {"heading": "2. Methodology", "content": "Approach and methods used"},
            {"heading": "3. Implementation", "content": "Technical details and code"},
            {"heading": "4. Results", "content": "Findings and output"},
            {"heading": "5. Discussion", "content": "Analysis and interpretation"},
            {"heading": "6. Conclusion", "content": "Summary and future work"},
            {"heading": "References", "content": "Academic references"},
            {"heading": "Appendix", "content": "Code listing and additional output"}
        ]
    }
    
    output_file = report_dir / "report_structure.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report_structure, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ 报告结构已生成: {output_file}")
    return report_structure

def step6_presentation(report_structure):
    """Step 6: 生成PPT + 演讲稿"""
    print("\n" + "="*60)
    print("🎬 Step 6: 生成PPT & 演讲稿")
    print("="*60)
    
    pres_dir = OUTPUT_DIR / "presentation"
    
    # Presentation outline
    pres_outline = {
        "slides": [
            {"type": "title", "title": "", "subtitle": ""},
            {"type": "outline", "title": "Outline", "points": []},
            {"type": "content", "title": "Background", "content": ""},
            {"type": "content", "title": "Problem Statement", "content": ""},
            {"type": "content", "title": "Methodology", "content": ""},
            {"type": "content", "title": "Architecture", "content": ""},
            {"type": "content", "title": "Implementation", "content": ""},
            {"type": "chart", "title": "Results", "content": ""},
            {"type": "content", "title": "Demo", "content": ""},
            {"type": "content", "title": "Discussion", "content": ""},
            {"type": "content", "title": "Conclusion", "content": ""},
            {"type": "qa", "title": "Q&A", "content": "Thank you!"}
        ],
        "speaker_notes": {},  # slide_index -> notes text
        "design": {
            "theme": "dark_modern",
            "primary_color": "1E2761",
            "secondary_color": "CADCFC",
            "accent_color": "FFFFFF"
        }
    }
    
    output_file = pres_dir / "presentation_outline.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(pres_outline, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ PPT大纲已生成: {output_file}")
    print(f"  🎙️ 演讲稿将保存到: {pres_dir / 'speaker_notes.md'}")
    return pres_outline

def step7_qa_simulation(report_structure, pres_outline):
    """Step 7: 模拟Q&A"""
    print("\n" + "="*60)
    print("❓ Step 7: 模拟Q&A")
    print("="*60)
    
    qa_dir = OUTPUT_DIR / "qa"
    
    qa_template = {
        "categories": [
            {
                "category": "Technical Questions",
                "questions": [
                    {"q": "Why did you choose this approach?", "a": ""},
                    {"q": "How does your system handle edge cases?", "a": ""},
                    {"q": "What are the limitations of your implementation?", "a": ""}
                ]
            },
            {
                "category": "Methodology Questions",
                "questions": [
                    {"q": "How did you validate your results?", "a": ""},
                    {"q": "What alternatives did you consider?", "a": ""},
                    {"q": "How would you improve this with more time?", "a": ""}
                ]
            },
            {
                "category": "Challenging Questions",
                "questions": [
                    {"q": "What happens if the input data is noisy?", "a": ""},
                    {"q": "How does this scale to larger datasets?", "a": ""},
                    {"q": "Can you compare your approach to state-of-the-art?", "a": ""}
                ]
            }
        ],
        "tips": [
            "先复述问题确认理解",
            "结构化回答：先给结论，再解释",
            "承认局限性展示诚实",
            "准备好 'I don't know, but...' 的回答策略"
        ]
    }
    
    output_file = qa_dir / "qa_preparation.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(qa_template, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ Q&A准备已生成: {output_file}")
    return qa_template

def main():
    """Run the complete workflow"""
    print("🚀 Student AI Agent - 项目工作流")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    ensure_dirs()
    assignment = read_assignment()
    
    # Run all steps
    analysis = step1_analyze(assignment)
    brainstorm = step2_brainstorm(analysis)
    code_dir = step3_code(brainstorm)
    checklist = step4_check_and_visualize(code_dir)
    report = step5_report(analysis, brainstorm, checklist)
    presentation = step6_presentation(report)
    qa = step7_qa_simulation(report, presentation)
    
    # Summary
    print("\n" + "="*60)
    print("🎉 工作流完成！")
    print("="*60)
    print(f"\n📁 所有输出保存在: {OUTPUT_DIR}")
    print("""
文件结构:
  output/
  ├── 01_analysis.json        # 作业分析
  ├── 02_brainstorm.json      # 方案设计
  ├── 04_check_results.json   # 代码检查
  ├── code/                   # 源代码
  │   ├── main.py
  │   └── requirements.txt
  ├── figures/                # 输出图片
  ├── report/                 # Word报告
  │   └── report_structure.json
  ├── presentation/           # PPT + 演讲稿
  │   └── presentation_outline.json
  └── qa/                     # Q&A准备
      └── qa_preparation.json
""")

if __name__ == "__main__":
    main()
