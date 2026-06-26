#!/usr/bin/env python3
"""
AI智能家教 - 学生档案管理系统
记录学生学习轨迹，实现个性化教学
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 配置
DATA_DIR = Path("/Users/josephauto/.openclaw/workspace/tutor_data")
DATA_DIR.mkdir(exist_ok=True)

class StudentProfile:
    """学生档案类"""
    
    def __init__(self, student_id):
        self.student_id = student_id
        self.file_path = DATA_DIR / f"{student_id}.json"
        self.data = self._load()
    
    def _load(self):
        """加载档案"""
        if self.file_path.exists():
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._default()
    
    def _default(self):
        """默认档案"""
        return {
            "student_id": self.student_id,
            "created_at": datetime.now().isoformat(),
            "grade": None,  # 年级
            "subjects": [],  # 学习科目
            "knowledge_graph": {},  # 知识图谱
            "weak_points": [],  # 薄弱点
            "learning_history": [],  # 学习历史
            "progress": {}  # 进度
        }
    
    def save(self):
        """保存档案"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def update_grade(self, grade):
        """更新年级"""
        self.data["grade"] = grade
        self.save()
    
    def add_subject(self, subject):
        """添加学习科目"""
        if subject not in self.data["subjects"]:
            self.data["subjects"].append(subject)
            self.data["knowledge_graph"][subject] = {}
            self.save()
    
    def record_lesson(self, subject, topic, understanding=3):
        """记录课程"""
        self.data["learning_history"].append({
            "timestamp": datetime.now().isoformat(),
            "subject": subject,
            "topic": topic,
            "understanding": understanding  # 1-5分
        })
        
        # 更新知识图谱
        if subject not in self.data["knowledge_graph"]:
            self.data["knowledge_graph"][subject] = {}
        
        self.data["knowledge_graph"][subject][topic] = {
            "last_studied": datetime.now().isoformat(),
            "understanding": understanding
        }
        
        self.save()
    
    def add_weak_point(self, subject, topic, reason=None):
        """添加薄弱点"""
        wp = {
            "subject": subject,
            "topic": topic,
            "reason": reason,
            "added_at": datetime.now().isoformat()
        }
        if wp not in self.data["weak_points"]:
            self.data["weak_points"].append(wp)
            self.save()
    
    def get_summary(self):
        """获取学习摘要"""
        return {
            "年级": self.data.get("grade", "未设置"),
            "学习科目": self.data.get("subjects", []),
            "学习历史": len(self.data.get("learning_history", [])),
            "薄弱点数量": len(self.data.get("weak_points", []))
        }
    
    def get_review_topics(self):
        """获取需要复习的知识点"""
        review = []
        for subject, topics in self.data.get("knowledge_graph", {}).items():
            for topic, info in topics.items():
                if info.get("understanding", 3) < 3:
                    review.append({
                        "subject": subject,
                        "topic": topic,
                        "understanding": info.get("understanding")
                    })
        return review


def create_student(grade, subjects):
    """创建新学生档案"""
    import uuid
    student_id = str(uuid.uuid4())[:8]
    profile = StudentProfile(student_id)
    profile.update_grade(grade)
    for subject in subjects:
        profile.add_subject(subject)
    return student_id


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI家教学生档案管理')
    parser.add_argument('--create', action='store_true', help='创建新学生')
    parser.add_argument('--grade', type=str, help='年级')
    parser.add_argument('--subjects', type=str, help='科目（逗号分隔）')
    parser.add_argument('--list', action='store_true', help='列出所有学生')
    parser.add_argument('--id', type=str, help='学生ID')
    
    args = parser.parse_args()
    
    if args.create:
        student_id = create_student(args.grade, args.subjects.split(','))
        print(f"✅ 学生档案创建成功！")
        print(f"📋 学生ID: {student_id}")
    
    elif args.list:
        for f in DATA_DIR.glob("*.json"):
            with open(f, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
                print(f"ID: {data['student_id']} | 年级: {data.get('grade', '未设置')} | 科目: {data.get('subjects', [])}")
    
    elif args.id:
        profile = StudentProfile(args.id)
        print(f"📊 学生档案: {args.id}")
        print(json.dumps(profile.get_summary(), ensure_ascii=False, indent=2))
        print("\n需要复习的内容:")
        for topic in profile.get_review_topics():
            print(f"  - {topic['subject']}: {topic['topic']} (理解度: {topic['understanding']})")


if __name__ == "__main__":
    main()
