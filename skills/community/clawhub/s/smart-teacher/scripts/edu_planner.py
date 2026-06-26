#!/usr/bin/env python3
"""
Smart Teacher — Education planning CLI.
No dependencies beyond stdlib.

Usage:
  python3 edu_planner.py <command> [args]

Commands:
  lesson <topic> [--grade N] [--duration N] [--standard std]
  curriculum <subject> [--grade N] [--weeks N] [--standard std]
  schedule [--subjects "A,B,C"] [--hours N] [--days N] [--exam-date YYYY-MM-DD]
  objectives <topic> [--grade N] [--levels "list"]
  rubric <assignment> [--criteria N] [--levels N]
  assess <topic> [--grade N] [--type quiz|test|exam] [--questions N]
"""

import json
import sys
import os
from datetime import datetime, timedelta

BLOOMS_LEVELS = {
    "remember": {
        "order": 1,
        "verbs": ["define", "list", "recall", "identify", "name", "state", "label", "match", "describe", "outline"],
        "description": "Recall facts and basic concepts"
    },
    "understand": {
        "order": 2,
        "verbs": ["explain", "summarize", "interpret", "classify", "compare", "contrast", "discuss", "paraphrase"],
        "description": "Explain ideas or concepts"
    },
    "apply": {
        "order": 3,
        "verbs": ["use", "solve", "demonstrate", "calculate", "implement", "execute", "apply", "illustrate"],
        "description": "Use information in new situations"
    },
    "analyze": {
        "order": 4,
        "verbs": ["analyze", "examine", "compare", "contrast", "differentiate", "organize", "deconstruct", "question"],
        "description": "Draw connections among ideas"
    },
    "evaluate": {
        "order": 5,
        "verbs": ["evaluate", "judge", "critique", "defend", "justify", "assess", "recommend", "prioritize"],
        "description": "Justify a stand or decision"
    },
    "create": {
        "order": 6,
        "verbs": ["create", "design", "develop", "compose", "construct", "propose", "formulate", "invent"],
        "description": "Produce new or original work"
    }
}

GRADE_LABELS = {
    "K": "Kindergarten", "1": "Grade 1", "2": "Grade 2", "3": "Grade 3",
    "4": "Grade 4", "5": "Grade 5", "6": "Grade 6", "7": "Grade 7",
    "8": "Grade 8", "9": "Grade 9", "10": "Grade 10", "11": "Grade 11",
    "12": "Grade 12"
}

def grade_label(grade):
    return GRADE_LABELS.get(str(grade), f"Grade {grade}")

# --- Commands ---

def cmd_lesson(topic, options):
    """Generate a structured lesson plan."""
    grade = options.get("grade", "8")
    duration = options.get("duration", 45)
    standard = options.get("standard", "")
    
    # Time breakdown
    intro = max(5, int(duration * 0.15))
    instruction = max(10, int(duration * 0.35))
    practice = max(10, int(duration * 0.30))
    wrap = max(5, int(duration * 0.20))
    
    grade_str = grade_label(grade)
    
    print(f"\n📝 Lesson Plan: {topic}")
    print(f"   Grade: {grade_str} | Duration: {duration} minutes")
    if standard:
        print(f"   Standards: {standard}")
    print(f"   Created: {datetime.now().strftime('%Y-%m-%d')}")
    print()
    
    print("━" * 50)
    print(f"1. INTRODUCTION ({intro} min)")
    print("━" * 50)
    print(f"   • Hook/Engagement: Pose a question about {topic}")
    print(f"   • Activate prior knowledge: What do students already know?")
    print(f"   • State learning objectives")
    print(f"   • Preview key vocabulary")
    print()
    
    print("━" * 50)
    print(f"2. DIRECT INSTRUCTION ({instruction} min)")
    print("━" * 50)
    print(f"   • Introduce core concepts of {topic}")
    print(f"   • Use visual aids and examples")
    print(f"   • Model problem-solving or demonstration")
    print(f"   • Check for understanding (mini-assessments)")
    print(f"   • Guided note-taking")
    print()
    
    print("━" * 50)
    print(f"3. GUIDED PRACTICE ({practice} min)")
    print("━" * 50)
    print(f"   • Collaborative activity or worksheet")
    print(f"   • Small group problem-solving")
    print(f"   • Teacher circulates, provides feedback")
    print(f"   • Differentiated support for struggling learners")
    print()
    
    print("━" * 50)
    print(f"4. WRAP-UP & ASSESSMENT ({wrap} min)")
    print("━" * 50)
    print(f"   • Exit ticket: 3 key takeaways")
    print(f"   • Address common misconceptions")
    print(f"   • Preview next lesson")
    print(f"   • Assign homework/extension activity")
    print()
    
    print("📋 Materials Needed:")
    print(f"   • Whiteboard/projector")
    print(f"   • Student handouts")
    print(f"   • Assessment rubric")
    print()

def cmd_curriculum(subject, options):
    """Create a multi-week curriculum map."""
    grade = options.get("grade", "9")
    weeks = int(options.get("weeks", 12))
    standard = options.get("standard", "")
    
    grade_str = grade_label(grade)
    
    print(f"\n📚 Curriculum Map: {subject}")
    print(f"   Grade: {grade_str} | Duration: {weeks} weeks")
    if standard:
        print(f"   Standards: {standard}")
    print()
    
    # Generate unit structure
    units_per_phase = max(1, weeks // 3)
    
    phases = [
        ("Phase 1: Foundation", "Introduce core concepts and vocabulary"),
        ("Phase 2: Development", "Deepen understanding through application"),
        ("Phase 3: Mastery", "Synthesize, evaluate, and create")
    ]
    
    week_num = 1
    for phase_name, phase_desc in phases:
        print(f"{'━' * 50}")
        print(f"  {phase_name}")
        print(f"  {phase_desc}")
        print(f"{'━' * 50}")
        
        phase_weeks = min(units_per_phase, weeks - week_num + 1)
        if phase_weeks < 1:
            break
            
        for w in range(phase_weeks):
            if week_num > weeks:
                break
            print(f"  Week {week_num}: Unit {week_num} — {subject} Topic {week_num}")
            print(f"    • Learning focus: Introduction to key concepts")
            print(f"    • Activities: Lecture, discussion, practice")
            print(f"    • Assessment: Formative check")
            week_num += 1
        print()
    
    print(f"📊 Assessment Schedule:")
    print(f"   • Formative: Weekly quizzes")
    print(f"   • Benchmark: End of each phase")
    print(f"   • Summative: Final week {weeks}")
    print()

def cmd_schedule(options):
    """Build a weekly study schedule."""
    subjects = options.get("subjects", "Math,Science,English").split(",")
    hours = int(options.get("hours", 3))
    days = int(options.get("days", 5))
    exam_date = options.get("exam_date", "")
    
    subjects = [s.strip() for s in subjects]
    total_minutes = hours * 60
    per_subject = total_minutes // len(subjects)
    
    print(f"\n📅 Weekly Study Schedule")
    print(f"   Subjects: {', '.join(subjects)}")
    print(f"   {hours} hours/day × {days} days/week")
    if exam_date:
        print(f"   Target exam: {exam_date}")
    print()
    
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for d in range(days):
        day = day_names[d % 7]
        print(f"{'━' * 50}")
        print(f"  {day}")
        print(f"{'━' * 50}")
        
        # Rotate subjects
        start_idx = d % len(subjects)
        for i, subj in enumerate(subjects):
            subj_idx = (start_idx + i) % len(subjects)
            start_h = 9 + (i * per_subject // 60)
            end_h = start_h + (per_subject // 60)
            start_m = (i * per_subject) % 60
            end_m = (start_m + per_subject) % 60
            print(f"  {start_h:02d}:{start_m:02d}–{end_h:02d}:{end_m:02d}  {subjects[subj_idx]}")
        
        print()
    
    print("💡 Tips:")
    print("   • Take 5-min breaks between subjects")
    print("   • Review notes within 24 hours")
    print("   • Use active recall, not passive re-reading")
    print("   • Prioritize weak subjects first")
    print()

def cmd_objectives(topic, options):
    """Generate learning objectives using Bloom's taxonomy."""
    grade = options.get("grade", "8")
    levels_str = options.get("levels", "remember,understand,apply,analyze")
    levels = [l.strip().lower() for l in levels_str.split(",")]
    
    grade_str = grade_label(grade)
    
    print(f"\n🎯 Learning Objectives: {topic}")
    print(f"   Grade: {grade_str}")
    print()
    
    for level_name in levels:
        level = BLOOMS_LEVELS.get(level_name)
        if not level:
            print(f"  ⚠️ Unknown level: {level_name}")
            continue
        
        verbs = level["verbs"]
        desc = level["description"]
        
        print(f"{'━' * 50}")
        print(f"  Level {level['order']}: {level_name.upper()}")
        print(f"  {desc}")
        print(f"{'━' * 50}")
        
        # Generate 3 objectives per level
        for i, verb in enumerate(verbs[:3]):
            print(f"  • Students will be able to {verb} {topic.lower()} concepts")
            print(f"    using appropriate vocabulary and examples.")
        
        print()
    
    print("📝 Assessment Alignment:")
    for level_name in levels:
        level = BLOOMS_LEVELS.get(level_name)
        if level:
            verbs = ", ".join(level["verbs"][:4])
            print(f"  • {level_name.title()}: {verbs}")
    print()

def cmd_rubric(assignment, options):
    """Create an assessment rubric."""
    criteria_count = int(options.get("criteria", 4))
    levels_count = int(options.get("levels", 4))
    
    level_labels = {
        4: ["Excellent (4)", "Proficient (3)", "Developing (2)", "Beginning (1)"],
        3: ["Proficient (3)", "Developing (2)", "Beginning (1)"],
        5: ["Exemplary (5)", "Accomplished (4)", "Proficient (3)", "Developing (2)", "Beginning (1)"]
    }
    
    generic_criteria = [
        ("Content Knowledge", "Demonstrates understanding of core concepts"),
        ("Organization", "Presents ideas in a logical, coherent structure"),
        ("Evidence & Support", "Uses relevant examples and evidence"),
        ("Critical Thinking", "Analyzes and evaluates information"),
        ("Communication", "Expresses ideas clearly and effectively"),
        ("Creativity", "Demonstrates original thinking"),
        ("Accuracy", "Factual correctness and precision"),
        ("Completion", "All required components are present")
    ]
    
    criteria = generic_criteria[:criteria_count]
    labels = level_labels.get(levels_count, level_labels[4])[:levels_count]
    
    print(f"\n📊 Rubric: {assignment}")
    print()
    
    # Header
    header = f"  {'Criteria':<25}"
    for label in labels:
        header += f" | {label:<15}"
    print(header)
    print("  " + "─" * (25 + (18 * len(labels))))
    
    # Rows
    for crit_name, crit_desc in criteria:
        row = f"  {crit_name:<25}"
        for i, label in enumerate(labels):
            score = levels_count - i
            row += f" | Score {score:<10}"
        print(row)
        print(f"    {crit_desc}")
        print("  " + "─" * (25 + (18 * len(labels))))
    
    print()
    max_score = criteria_count * levels_count
    print(f"  Total: /{max_score}")
    print()

def cmd_assess(topic, options):
    """Generate a quiz or test."""
    grade = options.get("grade", "10")
    assess_type = options.get("type", "quiz")
    num_questions = int(options.get("questions", 10))
    
    grade_str = grade_label(grade)
    
    # Question type distribution
    if assess_type == "quiz":
        types = {"multiple_choice": 5, "short_answer": 3, "true_false": 2}
    elif assess_type == "test":
        types = {"multiple_choice": 6, "short_answer": 3, "essay": 1}
    else:  # exam
        types = {"multiple_choice": 8, "short_answer": 5, "essay": 2}
    
    # Scale to requested question count
    total_weight = sum(types.values())
    scaled = {k: max(1, round(v * num_questions / total_weight)) for k, v in types.items()}
    diff = num_questions - sum(scaled.values())
    while diff != 0:
        if diff > 0:
            scaled["multiple_choice"] = scaled.get("multiple_choice", 0) + 1
            diff -= 1
        else:
            for k in list(scaled.keys()):
                if scaled[k] > 1:
                    scaled[k] -= 1
                    diff += 1
                    break
            break
    
    print(f"\n📋 {assess_type.title()}: {topic}")
    print(f"   Grade: {grade_str} | Questions: {num_questions}")
    print(f"   Time: {num_questions * 2} minutes (recommended)")
    print()
    
    q_num = 1
    
    if "multiple_choice" in scaled:
        print(f"{'━' * 50}")
        print(f"  Section A: Multiple Choice ({scaled['multiple_choice']} questions)")
        print(f"{'━' * 50}")
        for i in range(scaled["multiple_choice"]):
            print(f"  {q_num}. Which of the following best describes {topic.lower()}?")
            print(f"     a) Option A    b) Option B    c) Option C    d) Option D")
            print()
            q_num += 1
    
    if "true_false" in scaled:
        print(f"{'━' * 50}")
        print(f"  Section B: True or False ({scaled['true_false']} questions)")
        print(f"{'━' * 50}")
        for i in range(scaled["true_false"]):
            print(f"  {q_num}. Statement about {topic.lower()}. (T/F)")
            print()
            q_num += 1
    
    if "short_answer" in scaled:
        print(f"{'━' * 50}")
        print(f"  Section C: Short Answer ({scaled['short_answer']} questions)")
        print(f"{'━' * 50}")
        for i in range(scaled["short_answer"]):
            print(f"  {q_num}. Explain one key concept related to {topic.lower()}.")
            print(f"     _______________________________________________")
            print()
            q_num += 1
    
    if "essay" in scaled:
        print(f"{'━' * 50}")
        print(f"  Section D: Essay ({scaled['essay']} questions)")
        print(f"{'━' * 50}")
        for i in range(scaled["essay"]):
            print(f"  {q_num}. Analyze and evaluate the significance of {topic.lower()}.")
            print(f"     Use specific examples to support your argument.")
            print(f"     _______________________________________________")
            print(f"     _______________________________________________")
            print(f"     _______________________________________________")
            print()
            q_num += 1
    
    print(f"📊 Scoring Guide:")
    print(f"   Multiple Choice: 1 point each")
    print(f"   True/False: 1 point each")
    print(f"   Short Answer: 3 points each")
    print(f"   Essay: 10 points each")
    print()

# --- CLI ---

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "lesson" and len(sys.argv) >= 3:
        topic = sys.argv[2]
        options = {}
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--grade" and i + 1 < len(args):
                options["grade"] = args[i + 1]; i += 2
            elif args[i] == "--duration" and i + 1 < len(args):
                options["duration"] = int(args[i + 1]); i += 2
            elif args[i] == "--standard" and i + 1 < len(args):
                options["standard"] = args[i + 1]; i += 2
            else:
                i += 1
        cmd_lesson(topic, options)
    
    elif cmd == "curriculum" and len(sys.argv) >= 3:
        subject = sys.argv[2]
        options = {}
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--grade" and i + 1 < len(args):
                options["grade"] = args[i + 1]; i += 2
            elif args[i] == "--weeks" and i + 1 < len(args):
                options["weeks"] = args[i + 1]; i += 2
            elif args[i] == "--standard" and i + 1 < len(args):
                options["standard"] = args[i + 1]; i += 2
            else:
                i += 1
        cmd_curriculum(subject, options)
    
    elif cmd == "schedule":
        options = {}
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i] == "--subjects" and i + 1 < len(args):
                options["subjects"] = args[i + 1]; i += 2
            elif args[i] == "--hours" and i + 1 < len(args):
                options["hours"] = args[i + 1]; i += 2
            elif args[i] == "--days" and i + 1 < len(args):
                options["days"] = args[i + 1]; i += 2
            elif args[i] == "--exam-date" and i + 1 < len(args):
                options["exam_date"] = args[i + 1]; i += 2
            else:
                i += 1
        cmd_schedule(options)
    
    elif cmd == "objectives" and len(sys.argv) >= 3:
        topic = sys.argv[2]
        options = {}
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--grade" and i + 1 < len(args):
                options["grade"] = args[i + 1]; i += 2
            elif args[i] == "--levels" and i + 1 < len(args):
                options["levels"] = args[i + 1]; i += 2
            else:
                i += 1
        cmd_objectives(topic, options)
    
    elif cmd == "rubric" and len(sys.argv) >= 3:
        assignment = sys.argv[2]
        options = {}
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--criteria" and i + 1 < len(args):
                options["criteria"] = args[i + 1]; i += 2
            elif args[i] == "--levels" and i + 1 < len(args):
                options["levels"] = args[i + 1]; i += 2
            else:
                i += 1
        cmd_rubric(assignment, options)
    
    elif cmd == "assess" and len(sys.argv) >= 3:
        topic = sys.argv[2]
        options = {}
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--grade" and i + 1 < len(args):
                options["grade"] = args[i + 1]; i += 2
            elif args[i] == "--type" and i + 1 < len(args):
                options["type"] = args[i + 1]; i += 2
            elif args[i] == "--questions" and i + 1 < len(args):
                options["questions"] = args[i + 1]; i += 2
            else:
                i += 1
        cmd_assess(topic, options)
    
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
