#!/usr/bin/env python3
"""
Priority Calculator - Priority Calculation Script
Calculates task priority based on multi-dimensional evaluation
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

class PriorityCalculator:
    """Priority Calculator"""
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize Priority Calculator
        
        Args:
            weights: Custom weight configuration
        """
        self.weights = weights or {
            "urgency": 0.30,      # Urgency
            "value": 0.40,        # Value
            "cost": 0.20,         # Cost (inverse)
            "risk": 0.10          # Risk
        }
    
    def calculate(self, tasks: List[Dict]) -> List[Dict]:
        """
        Calculate task priority scores and sort
        
        Args:
            tasks: Task list
            
        Returns:
            Sorted task list (including priority scores)
        """
        scored_tasks = []
        
        for task in tasks:
            score = self._calculate_score(task)
            task_with_score = {**task, "priority_score": score}
            scored_tasks.append(task_with_score)
        
        # Sort by score in descending order
        scored_tasks.sort(key=lambda x: x["priority_score"], reverse=True)
        
        # Update priority labels
        for i, task in enumerate(scored_tasks):
            if i < len(scored_tasks) * 0.3:
                task["priority"] = "high"
            elif i > len(scored_tasks) * 0.7:
                task["priority"] = "low"
            else:
                task["priority"] = "medium"
        
        return scored_tasks
    
    def _calculate_score(self, task: Dict) -> float:
        """Calculate priority score for a single task"""
        urgency_score = self._evaluate_urgency(task)
        value_score = self._evaluate_value(task)
        cost_score = self._evaluate_cost(task)
        risk_score = self._evaluate_risk(task)
        
        total = (
            urgency_score * self.weights["urgency"] +
            value_score * self.weights["value"] +
            cost_score * self.weights["cost"] +
            risk_score * self.weights["risk"]
        )
        
        return round(total, 2)
    
    def _evaluate_urgency(self, task: Dict) -> float:
        """Evaluate urgency (0-100)"""
        score = 50  # Base score
        
        # Based on deadline
        deadline = task.get("deadline")
        if deadline:
            try:
                deadline_dt = datetime.fromisoformat(deadline)
                hours_until = (deadline_dt - datetime.now()).total_seconds() / 3600
                
                if hours_until < 0:
                    score = 100  # Overdue
                elif hours_until < 24:
                    score = 95   # Within 24 hours
                elif hours_until < 72:
                    score = 80   # Within 3 days
                elif hours_until < 168:
                    score = 65   # Within a week
                else:
                    score = 40   # Over a week
            except:
                pass
        
        # Based on keywords
        description = task.get("description", "").lower()
        urgency_keywords = {
            "urgent": 30, "immediately": 30, "right away": 30,
            "today": 25, "tomorrow": 20, "asap": 15,
            "important": 10, "critical": 10
        }
        
        for kw, bonus in urgency_keywords.items():
            if kw in description:
                score = min(100, score + bonus)
        
        # Increase urgency when blocked by other tasks
        if task.get("blocked_tasks"):
            score = min(100, score + 15)
        
        return score
    
    def _evaluate_value(self, task: Dict) -> float:
        """Evaluate value (0-100)"""
        score = 50  # Base score
        
        description = task.get("description", "").lower()
        
        # Based on business value keywords
        value_keywords = {
            "core": 25, "key": 20, "important": 15,
            "revenue": 30, "client": 25, "user": 20,
            "launch": 20, "release": 20, "deliver": 15,
            "innovation": 10, "optimization": 10
        }
        
        for kw, bonus in value_keywords.items():
            if kw in description:
                score = min(100, score + bonus)
        
        # Tasks with dependents have higher value
        dependents = task.get("dependents", [])
        if dependents:
            score = min(100, score + len(dependents) * 5)
        
        return score
    
    def _evaluate_cost(self, task: Dict) -> float:
        """
        Evaluate cost (inverse metric, lower cost = higher score)
        Converts to 0-100 scale
        """
        # Parse estimated time
        estimated_time = task.get("estimated_time", "1h")
        
        try:
            hours = float(estimated_time.replace("h", "").replace("H", ""))
        except:
            hours = 1
        
        # Shorter time yields higher score (inverse)
        if hours <= 0.5:
            score = 100
        elif hours <= 1:
            score = 90
        elif hours <= 2:
            score = 75
        elif hours <= 4:
            score = 60
        elif hours <= 8:
            score = 40
        else:
            score = 20
        
        return score
    
    def _evaluate_risk(self, task: Dict) -> float:
        """
        Evaluate risk (high-risk tasks need prioritization to allow buffer time)
        Returns 0-100 scale
        """
        score = 50  # Base score
        
        description = task.get("description", "").lower()
        
        # High-risk keywords
        high_risk_keywords = ["new", "first", "experimental", "uncertain", "complex", "integration"]
        for kw in high_risk_keywords:
            if kw in description:
                score = min(100, score + 15)
        
        # Tasks with dependencies carry higher risk
        dependencies = task.get("dependencies", [])
        if dependencies:
            score = min(100, score + len(dependencies) * 10)
        
        return score
    
    def suggest_order(self, tasks: List[Dict]) -> List[Dict]:
        """
        Suggest execution order, considering dependencies
        
        Args:
            tasks: Task list
            
        Returns:
            Task list in suggested execution order
        """
        # First sort by priority
        scored_tasks = self.calculate(tasks)
        
        # Topological sort considering dependencies
        ordered = []
        task_map = {t["id"]: t for t in scored_tasks}
        completed = set()
        
        while scored_tasks:
            # Find all tasks with satisfied dependencies
            ready = [
                t for t in scored_tasks
                if not t.get("dependencies") or 
                   all(d in completed for d in t.get("dependencies", []))
            ]
            
            if not ready:
                # Circular dependency exists, take the highest priority
                ready = [scored_tasks[0]]
            
            # Sort by priority score
            ready.sort(key=lambda x: x["priority_score"], reverse=True)
            
            # Select the highest priority task
            next_task = ready[0]
            ordered.append(next_task)
            completed.add(next_task["id"])
            scored_tasks.remove(next_task)
        
        return ordered


def main():
    parser = argparse.ArgumentParser(description='Priority Calculation Tool')
    parser.add_argument('--input', '-i', required=True, help='Task JSON file path')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--weights', '-w', help='Custom weights (JSON format)')
    parser.add_argument('--show-order', action='store_true', help='Display suggested execution order')
    
    args = parser.parse_args()
    
    # Read tasks
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tasks = data.get("tasks", data)
    
    # Parse weights
    weights = None
    if args.weights:
        try:
            weights = json.loads(args.weights)
        except:
            print("Warning: Unable to parse weight JSON, using default weights")
    
    calculator = PriorityCalculator(weights)
    
    if args.show_order:
        result = calculator.suggest_order(tasks)
        print("\nSuggested Execution Order:")
        for i, task in enumerate(result, 1):
            print(f"{i}. [{task['id']}] {task['description'][:40]}... (Score: {task['priority_score']})")
    else:
        result = calculator.calculate(tasks)
        print("\nPriority Sorting:")
        for task in result:
            print(f"[{task['id']}] Priority: {task['priority']}, Score: {task['priority_score']}")
    
    # Output
    output_path = args.output or args.input.replace('.json', '_prioritized.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Results saved to: {output_path}")


if __name__ == '__main__':
    main()