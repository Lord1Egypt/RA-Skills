#!/usr/bin/env python3
"""
Task Decomposer - Task Decomposition Script
Decomposes natural language goals into a structured task tree
"""

import argparse
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional

class TaskDecomposer:
    """Task Decomposer"""
    
    def __init__(self):
        self.task_counter = 0
        self.tasks = []
    
    def decompose(self, goal: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Decompose a goal into a task tree
        
        Args:
            goal: User goal description
            context: Additional context information
            
        Returns:
            Structured task tree
        """
        self.task_counter = 0
        self.tasks = []
        
        # Parse goal
        main_tasks = self._parse_goal(goal)
        
        # Build task tree
        for task in main_tasks:
            self._add_task(task, parent_id=None)
        
        return {
            "main_goal": goal,
            "created_at": datetime.now().isoformat(),
            "total_tasks": len(self.tasks),
            "tasks": self.tasks
        }
    
    def _parse_goal(self, goal: str) -> List[Dict]:
        """Parse goal into task list"""
        # Identify key action words
        action_patterns = [
            r'(write|draft|create|design|develop|complete|prepare|organize|analyze)',
            r'(test|verify|check|review|optimize|modify|update|delete)',
            r'(publish|deploy|push|send|share|display)'
        ]
        
        # Identify parallel structures (commas, and, also, etc.)
        split_patterns = r'[,，、;；]|and|also|meanwhile|additionally'
        
        # Simple decomposition logic
        parts = re.split(split_patterns, goal)
        
        tasks = []
        for i, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue
            
            # Determine if it's an independent task
            is_task = any(re.search(p, part) for p in action_patterns)
            
            if is_task or len(part) > 4:
                task = self._create_task_structure(part, i)
                tasks.append(task)
        
        # If no tasks identified, treat the entire goal as a single task
        if not tasks:
            tasks.append(self._create_task_structure(goal, 0))
        
        return tasks
    
    def _create_task_structure(self, description: str, index: int) -> Dict:
        """Create task structure"""
        # Estimate time (simple heuristic)
        estimated_time = self._estimate_time(description)
        
        # Determine priority
        priority = self._determine_priority(description)
        
        # Infer required skills
        required_skills = self._infer_skills(description)
        
        return {
            "description": description,
            "priority": priority,
            "estimated_time": estimated_time,
            "required_skills": required_skills,
            "subtasks": []
        }
    
    def _add_task(self, task_data: Dict, parent_id: Optional[str] = None) -> str:
        """Add task to task list"""
        self.task_counter += 1
        task_id = f"T{self.task_counter}"
        
        # Handle subtasks
        subtasks = task_data.pop("subtasks", [])
        
        task = {
            "id": task_id,
            "parent_id": parent_id,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            **task_data
        }
        
        self.tasks.append(task)
        
        # Recursively process subtasks
        for subtask_data in subtasks:
            self._add_task(subtask_data, parent_id=task_id)
        
        return task_id
    
    def _estimate_time(self, description: str) -> str:
        """Estimate task time"""
        # Simple estimation based on keywords
        time_indicators = {
            'document': 2,
            'report': 3,
            'PPT': 2,
            'code': 4,
            'test': 2,
            'analysis': 3,
            'design': 3,
            'poster': 1,
            'video': 4,
            'demo': 3
        }
        
        hours = 1  # Default 1 hour
        for keyword, h in time_indicators.items():
            if keyword in description:
                hours = h
                break
        
        return f"{hours}h"
    
    def _determine_priority(self, description: str) -> str:
        """Determine task priority"""
        high_priority_keywords = ['urgent', 'immediately', 'right away', 'today', 'tomorrow', 'important', 'critical']
        low_priority_keywords = ['later', 'not urgent', 'when available', 'sometime']
        
        for kw in high_priority_keywords:
            if kw in description:
                return "high"
        
        for kw in low_priority_keywords:
            if kw in description:
                return "low"
        
        return "medium"
    
    def _infer_skills(self, description: str) -> List[str]:
        """Infer required skills"""
        skill_mapping = {
            'document': ['doc-writing-skill'],
            'report': ['doc-writing-skill'],
            'PPT': ['ppt-parser-local', 'doc-writing-skill'],
            'code': [],
            'test': [],
            'analysis': ['deep-search-skill', 'web-search'],
            'search': ['web-search', 'deep-search-skill'],
            'poster': ['image_generation'],
            'image': ['image_generation'],
            'video': ['video-script-generation-skill'],
            'Xiaohongshu': ['redbook', 'weavefox-xhs-intel'],
            'Official Account': ['wechat-article-generator'],
            'translation': []
        }
        
        skills = []
        for keyword, skill_list in skill_mapping.items():
            if keyword in description:
                skills.extend(skill_list)
        
        return list(set(skills))  # Deduplicate


def main():
    parser = argparse.ArgumentParser(description='Task Decomposition Tool')
    parser.add_argument('--goal', '-g', required=True, help='User goal description')
    parser.add_argument('--output', '-o', default='tasks.json', help='Output file path')
    parser.add_argument('--context', '-c', help='Additional context (JSON format)')
    
    args = parser.parse_args()
    
    decomposer = TaskDecomposer()
    
    context = None
    if args.context:
        try:
            context = json.loads(args.context)
        except json.JSONDecodeError:
            print(f"Warning: Unable to parse context JSON, will ignore")
    
    result = decomposer.decompose(args.goal, context)
    
    # Output to file
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Task decomposition complete, total {result['total_tasks']} task(s)")
    print(f"✓ Results saved to: {args.output}")
    
    # Print task preview
    print("\nTask List:")
    for task in result['tasks']:
        indent = "  " if task.get('parent_id') else ""
        print(f"{indent}[{task['id']}] {task['description'][:50]}... (Priority: {task['priority']}, Estimated: {task['estimated_time']})")


if __name__ == '__main__':
    main()