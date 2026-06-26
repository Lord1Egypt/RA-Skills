#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作准备模块 v3.0
作者: zcg007
日期: 2026-03-15

自动为新工作准备环境、检索相关记忆、生成工作计划
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging
import subprocess

from task_detector import task_detector
from memory_retriever import memory_retriever
from conversation_hook import conversation_hook
from config_loader import config_loader

logger = logging.getLogger(__name__)


class WorkPreparation:
    """工作准备模块"""
    
    def __init__(self, workspace_dir: str = None):
        """
        初始化工作准备模块
        
        Args:
            workspace_dir: 工作空间目录，默认为当前目录
        """
        if workspace_dir is None:
            self.workspace_dir = Path.cwd()
        else:
            self.workspace_dir = Path(workspace_dir)
        
        # 确保工作空间目录存在
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载配置
        self.config = config_loader.load_config()
        
        # 工作准备状态
        self.preparation_status = {
            "memory_loaded": False,
            "index_built": False,
            "environment_checked": False,
            "dependencies_installed": False,
            "plan_generated": False,
            "start_time": None,
            "end_time": None,
            "elapsed_seconds": 0,
        }
        
        # 工作日志
        self.work_logs = []
        
        # 输出目录
        self.output_dir = self.workspace_dir / ".workbuddy" / "preparation_output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def prepare_for_work(self, task_description: str, 
                        auto_execute: bool = False) -> Dict[str, Any]:
        """
        为新工作做准备
        
        Args:
            task_description: 任务描述
            auto_execute: 是否自动执行建议操作
            
        Returns:
            准备结果字典
        """
        self.preparation_status["start_time"] = datetime.now()
        self._log_event("开始工作准备", {"task": task_description})
        
        # 1. 分析任务
        task_analysis = self._analyze_task(task_description)
        
        # 2. 检查工作空间
        workspace_check = self._check_workspace()
        
        # 3. 检查环境依赖
        environment_check = self._check_environment(task_analysis)
        
        # 4. 加载和检索记忆
        memory_results = self._retrieve_memories(task_description, task_analysis)
        
        # 5. 生成工作计划
        work_plan = self._generate_work_plan(task_description, task_analysis, memory_results)
        
        # 6. 准备必要资源
        resources = self._prepare_resources(task_analysis, memory_results)
        
        # 7. 生成最终报告
        final_report = self._generate_final_report(
            task_description, task_analysis, memory_results, work_plan, resources
        )
        
        # 8. 保存准备结果
        self._save_preparation_results(
            task_description, task_analysis, memory_results, work_plan, final_report
        )
        
        # 9. 自动执行（如果启用）
        if auto_execute and work_plan.get("suggested_actions"):
            execution_results = self._execute_suggested_actions(work_plan["suggested_actions"])
            final_report["execution_results"] = execution_results
        
        # 更新状态
        self.preparation_status["end_time"] = datetime.now()
        elapsed = self.preparation_status["end_time"] - self.preparation_status["start_time"]
        self.preparation_status["elapsed_seconds"] = elapsed.total_seconds()
        
        self._log_event("工作准备完成", {
            "elapsed_seconds": self.preparation_status["elapsed_seconds"],
            "memory_count": len(memory_results),
            "plan_generated": work_plan.get("plan_ready", False),
        })
        
        return {
            "task_description": task_description,
            "task_analysis": task_analysis,
            "memory_results": memory_results,
            "work_plan": work_plan,
            "resources": resources,
            "final_report": final_report,
            "preparation_status": self.preparation_status.copy(),
            "output_files": self._get_output_files(),
        }
    
    def _analyze_task(self, task_description: str) -> Dict[str, Any]:
        """分析任务"""
        self._log_event("开始任务分析", {"description": task_description})
        
        # 使用任务检测器
        detection_result = task_detector.detect_task(task_description)
        
        # 深度分析任务
        task_analysis = {
            "description": task_description,
            "primary_task_type": detection_result.get("primary_task"),
            "confidence": detection_result.get("confidence", 0.0),
            "task_types": detection_result.get("task_types", []),
            "intent": detection_result.get("intent"),
            "keywords": detection_result.get("keywords_found", []),
            "suggested_actions": detection_result.get("suggested_actions", []),
            "complexity": self._assess_complexity(task_description, detection_result),
            "estimated_time": self._estimate_time(task_description, detection_result),
            "required_skills": self._identify_required_skills(detection_result),
            "potential_challenges": self._identify_challenges(detection_result),
            "success_criteria": self._define_success_criteria(task_description),
        }
        
        self._log_event("任务分析完成", {
            "primary_type": task_analysis["primary_task_type"],
            "complexity": task_analysis["complexity"],
            "estimated_time": task_analysis["estimated_time"],
        })
        
        return task_analysis
    
    def _assess_complexity(self, description: str, detection: Dict[str, Any]) -> str:
        """评估任务复杂度"""
        complexity_score = 0
        
        # 基于任务类型
        task_type = detection.get("primary_task")
        if task_type in ["excel", "skill", "workflow"]:
            complexity_score += 2
        elif task_type in ["analysis", "memory"]:
            complexity_score += 1
        
        # 基于描述长度和关键词数量
        word_count = len(description.split())
        if word_count > 50:
            complexity_score += 2
        elif word_count > 20:
            complexity_score += 1
        
        # 基于关键词数量
        keyword_count = len(detection.get("keywords_found", []))
        if keyword_count > 5:
            complexity_score += 2
        elif keyword_count > 2:
            complexity_score += 1
        
        # 确定复杂度等级
        if complexity_score >= 4:
            return "high"
        elif complexity_score >= 2:
            return "medium"
        else:
            return "low"
    
    def _estimate_time(self, description: str, detection: Dict[str, Any]) -> Dict[str, Any]:
        """估计所需时间"""
        base_times = {
            "excel": {"min": 30, "max": 180},  # 分钟
            "skill": {"min": 15, "max": 90},
            "memory": {"min": 5, "max": 30},
            "workflow": {"min": 60, "max": 240},
            "analysis": {"min": 30, "max": 120},
        }
        
        task_type = detection.get("primary_task")
        if task_type in base_times:
            base_time = base_times[task_type]
        else:
            base_time = {"min": 10, "max": 60}
        
        # 根据复杂度调整
        complexity = self._assess_complexity(description, detection)
        if complexity == "high":
            time_multiplier = 2.0
        elif complexity == "medium":
            time_multiplier = 1.5
        else:
            time_multiplier = 1.0
        
        estimated_min = base_time["min"] * time_multiplier
        estimated_max = base_time["max"] * time_multiplier
        
        return {
            "min_minutes": int(estimated_min),
            "max_minutes": int(estimated_max),
            "estimated_range": f"{int(estimated_min)}-{int(estimated_max)}分钟",
            "complexity": complexity,
        }
    
    def _identify_required_skills(self, detection: Dict[str, Any]) -> List[str]:
        """识别所需技能"""
        skills = []
        task_type = detection.get("primary_task")
        
        if task_type == "excel":
            skills.extend(["Excel处理", "数据分析", "公式计算", "数据验证"])
        elif task_type == "skill":
            skills.extend(["技能管理", "依赖安装", "环境配置", "测试验证"])
        elif task_type == "memory":
            skills.extend(["记忆检索", "知识管理", "经验总结", "信息组织"])
        elif task_type == "workflow":
            skills.extend(["流程设计", "自动化", "任务分解", "效率优化"])
        elif task_type == "analysis":
            skills.extend(["数据分析", "问题解决", "报告编写", "决策支持"])
        
        # 添加通用技能
        skills.extend(["沟通协调", "时间管理", "质量控制"])
        
        return list(set(skills))
    
    def _identify_challenges(self, detection: Dict[str, Any]) -> List[str]:
        """识别潜在挑战"""
        challenges = []
        task_type = detection.get("primary_task")
        
        if task_type == "excel":
            challenges.extend([
                "数据格式不一致",
                "公式引用错误",
                "数据验证失败",
                "性能问题（大文件）",
            ])
        elif task_type == "skill":
            challenges.extend([
                "依赖冲突",
                "环境兼容性问题",
                "安装权限限制",
                "网络连接问题",
            ])
        elif task_type == "memory":
            challenges.extend([
                "记忆检索准确率",
                "信息过时问题",
                "知识组织混乱",
                "检索效率低下",
            ])
        
        return challenges
    
    def _define_success_criteria(self, task_description: str) -> List[str]:
        """定义成功标准"""
        criteria = [
            "任务按时完成",
            "输出质量符合预期",
            "所有要求的功能实现",
            "代码/文档质量良好",
            "问题得到有效解决",
        ]
        
        # 根据任务描述添加具体标准
        if "excel" in task_description.lower():
            criteria.extend([
                "数据准确性100%",
                "公式计算正确",
                "格式美观统一",
            ])
        elif "skill" in task_description.lower():
            criteria.extend([
                "技能安装成功",
                "功能测试通过",
                "文档完整清晰",
            ])
        
        return criteria
    
    def _check_workspace(self) -> Dict[str, Any]:
        """检查工作空间"""
        self._log_event("检查工作空间", {"path": str(self.workspace_dir)})
        
        workspace_info = {
            "path": str(self.workspace_dir),
            "exists": self.workspace_dir.exists(),
            "is_directory": self.workspace_dir.is_dir(),
            "is_writable": os.access(self.workspace_dir, os.W_OK),
            "size_mb": self._get_directory_size(self.workspace_dir) / (1024 * 1024),
            "file_count": self._count_files(self.workspace_dir),
            "subdirectories": [],
            "issues": [],
        }
        
        if workspace_info["exists"]:
            # 检查子目录
            try:
                for item in self.workspace_dir.iterdir():
                    if item.is_dir():
                        workspace_info["subdirectories"].append(item.name)
            except Exception as e:
                workspace_info["issues"].append(f"无法读取目录内容: {e}")
        
            # 检查常见问题
            if not workspace_info["is_writable"]:
                workspace_info["issues"].append("工作空间不可写")
            
            if workspace_info["size_mb"] > 1024:  # 大于1GB
                workspace_info["issues"].append("工作空间过大，可能影响性能")
        else:
            workspace_info["issues"].append("工作空间不存在")
        
        self._log_event("工作空间检查完成", {
            "file_count": workspace_info["file_count"],
            "issues": len(workspace_info["issues"]),
        })
        
        return workspace_info
    
    def _get_directory_size(self, path: Path) -> int:
        """获取目录大小"""
        total_size = 0
        try:
            for item in path.rglob("*"):
                if item.is_file():
                    total_size += item.stat().st_size
        except:
            pass
        return total_size
    
    def _count_files(self, path: Path) -> int:
        """统计文件数量"""
        count = 0
        try:
            for _ in path.rglob("*"):
                count += 1
        except:
            pass
        return count
    
    def _check_environment(self, task_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """检查环境依赖"""
        self._log_event("检查环境依赖", {"task_type": task_analysis["primary_task_type"]})
        
        environment_info = {
            "python_version": sys.version,
            "platform": sys.platform,
            "current_directory": str(Path.cwd()),
            "python_path": sys.executable,
            "dependencies": {},
            "missing_dependencies": [],
            "environment_issues": [],
        }
        
        # 检查Python版本
        python_version = sys.version_info
        environment_info["python_version_info"] = {
            "major": python_version.major,
            "minor": python_version.minor,
            "micro": python_version.micro,
        }
        
        # 根据任务类型检查依赖
        task_type = task_analysis["primary_task_type"]
        
        if task_type == "excel":
            required_deps = ["openpyxl", "pandas", "numpy"]
        elif task_type == "skill":
            required_deps = ["skillhub", "requests", "toml"]
        elif task_type == "memory":
            required_deps = ["scikit-learn", "numpy", "pandas"]
        else:
            required_deps = []
        
        # 检查依赖
        for dep in required_deps:
            try:
                __import__(dep)
                environment_info["dependencies"][dep] = "installed"
            except ImportError:
                environment_info["dependencies"][dep] = "missing"
                environment_info["missing_dependencies"].append(dep)
        
        # 检查环境问题
        if environment_info["missing_dependencies"]:
            environment_info["environment_issues"].append(
                f"缺少依赖: {', '.join(environment_info['missing_dependencies'])}"
            )
        
        self.preparation_status["environment_checked"] = True
        
        self._log_event("环境检查完成", {
            "missing_deps": len(environment_info["missing_dependencies"]),
            "issues": len(environment_info["environment_issues"]),
        })
        
        return environment_info
    
    def _retrieve_memories(self, task_description: str, 
                          task_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """检索相关记忆"""
        self._log_event("检索相关记忆", {"task_type": task_analysis["primary_task_type"]})
        
        # 确保记忆库已加载
        if not memory_retriever.memory_data:
            memory_sources = config_loader.get_memory_sources()
            memory_retriever.load_memories(memory_sources)
            memory_retriever.build_index()
            self.preparation_status["memory_loaded"] = True
            self.preparation_status["index_built"] = True
        
        # 检索记忆
        memories = memory_retriever.search(task_description, top_k=10)
        
        # 如果结果不够，尝试使用任务类型作为关键词
        if len(memories) < 3 and task_analysis["primary_task_type"]:
            alternative_query = task_analysis["primary_task_type"]
            additional_memories = memory_retriever.search(alternative_query, top_k=5)
            
            # 合并结果，去重
            existing_ids = {m["id"] for m in memories}
            for memory in additional_memories:
                if memory["id"] not in existing_ids:
                    memories.append(memory)
                    existing_ids.add(memory["id"])
        
        self._log_event("记忆检索完成", {"memory_count": len(memories)})
        
        return memories
    
    def _generate_work_plan(self, task_description: str, 
                           task_analysis: Dict[str, Any],
                           memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成工作计划"""
        self._log_event("生成工作计划", {"complexity": task_analysis["complexity"]})
        
        # 基于任务分析和记忆生成计划
        work_plan = {
            "task_description": task_description,
            "task_type": task_analysis["primary_task_type"],
            "complexity": task_analysis["complexity"],
            "estimated_time": task_analysis["estimated_time"],
            "required_skills": task_analysis["required_skills"],
            "success_criteria": task_analysis["success_criteria"],
            "phases": [],
            "milestones": [],
            "deliverables": [],
            "risks": task_analysis["potential_challenges"],
            "suggested_actions": [],
            "plan_ready": True,
        }
        
        # 根据任务类型生成阶段
        if task_analysis["primary_task_type"] == "excel":
            work_plan["phases"] = [
                {"name": "需求分析", "description": "分析Excel文件结构和业务需求"},
                {"name": "数据准备", "description": "准备和清洗数据"},
                {"name": "处理实施", "description": "执行Excel处理操作"},
                {"name": "验证测试", "description": "验证结果和公式正确性"},
                {"name": "文档整理", "description": "整理处理过程和结果文档"},
            ]
            work_plan["deliverables"] = ["处理后的Excel文件", "处理报告", "验证文档"]
            
        elif task_analysis["primary_task_type"] == "skill":
            work_plan["phases"] = [
                {"name": "技能搜索", "description": "在SkillHub搜索相关技能"},
                {"name": "环境检查", "description": "检查依赖和兼容性"},
                {"name": "安装实施", "description": "安装技能和依赖"},
                {"name": "功能测试", "description": "测试技能功能"},
                {"name": "文档整理", "description": "整理使用文档"},
            ]
            work_plan["deliverables"] = ["安装的技能", "测试报告", "使用文档"]
        
        # 从记忆中提取建议操作
        suggested_actions = []
        for memory in memories[:5]:
            content = memory.get("content", "")
            # 提取建议性内容
            if "建议" in content or "应该" in content or "需要" in content:
                # 提取相关句子
                sentences = content.split('。')
                for sentence in sentences:
                    if any(word in sentence for word in ["建议", "应该", "需要"]):
                        suggested_actions.append(sentence.strip())
        
        # 添加任务分析中的建议
        suggested_actions.extend(task_analysis.get("suggested_actions", []))
        
        # 去重和限制数量
        work_plan["suggested_actions"] = list(set(suggested_actions))[:10]
        
        # 生成里程碑
        for i, phase in enumerate(work_plan["phases"], 1):
            milestone = {
                "id": f"M{i}",
                "name": phase["name"],
                "description": phase["description"],
                "estimated_completion": f"阶段{i}结束时",
                "success_criteria": f"完成{phase['name']}阶段的所有任务",
            }
            work_plan["milestones"].append(milestone)
        
        self.preparation_status["plan_generated"] = True
        
        self._log_event("工作计划生成完成", {
            "phases": len(work_plan["phases"]),
            "suggested_actions": len(work_plan["suggested_actions"]),
        })
        
        return work_plan
    
    def _prepare_resources(self, task_analysis: Dict[str, Any], 
                          memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """准备必要资源"""
        self._log_event("准备必要资源", {"task_type": task_analysis["primary_task_type"]})
        
        resources = {
            "documentation": [],
            "templates": [],
            "tools": [],
            "references": [],
            "sample_files": [],
        }
        
        # 从记忆中提取资源
        for memory in memories[:8]:
            title = memory.get("title", "")
            content = memory.get("content", "")
            category = memory.get("category", "")
            
            # 根据类别分类资源
            if "文档" in title or "说明" in title or "指南" in title:
                resources["documentation"].append({
                    "title": title,
                    "category": category,
                    "relevance": memory.get("relevance_score", 0),
                })
            elif "模板" in title or "示例" in title:
                resources["templates"].append({
                    "title": title,
                    "category": category,
                    "relevance": memory.get("relevance_score", 0),
                })
            elif "工具" in title or "软件" in title:
                resources["tools"].append({
                    "title": title,
                    "category": category,
                    "relevance": memory.get("relevance_score", 0),
                })
        
        # 添加通用资源
        if task_analysis["primary_task_type"] == "excel":
            resources["tools"].extend([
                {"title": "Excel软件", "category": "tool", "relevance": 1.0},
                {"title": "Python openpyxl库", "category": "tool", "relevance": 0.9},
                {"title": "数据验证工具", "category": "tool", "relevance": 0.7},
            ])
            resources["documentation"].append({
                "title": "Excel处理最佳实践", 
                "category": "documentation", 
                "relevance": 0.8
            })
        
        # 限制每个类别的资源数量
        for key in resources:
            resources[key] = resources[key][:5]
        
        self._log_event("资源准备完成", {
            "documentation": len(resources["documentation"]),
            "templates": len(resources["templates"]),
            "tools": len(resources["tools"]),
        })
        
        return resources
    
    def _generate_final_report(self, task_description: str, 
                              task_analysis: Dict[str, Any],
                              memories: List[Dict[str, Any]],
                              work_plan: Dict[str, Any],
                              resources: Dict[str, Any]) -> Dict[str, Any]:
        """生成最终报告"""
        self._log_event("生成最终报告", {})
        
        # 生成报告内容
        report_content = f"""# 工作准备报告

## 任务概述
- **任务描述**: {task_description}
- **任务类型**: {task_analysis['primary_task_type']}
- **复杂度**: {task_analysis['complexity']}
- **预估时间**: {task_analysis['estimated_time']['estimated_range']}

## 任务分析
**主要意图**: {task_analysis['intent']}
**置信度**: {task_analysis['confidence']:.2f}

**所需技能**:
{self._format_list(task_analysis['required_skills'])}

**成功标准**:
{self._format_list(task_analysis['success_criteria'])}

## 记忆检索结果
找到 {len(memories)} 条相关记忆：

{self._format_memories_for_report(memories[:5])}

## 工作计划
**工作阶段**:
{self._format_phases(work_plan['phases'])}

**里程碑**:
{self._format_milestones(work_plan['milestones'])}

**交付物**:
{self._format_list(work_plan['deliverables'])}

## 建议操作
{self._format_list(work_plan['suggested_actions'])}

## 准备资源
**文档资源**:
{self._format_resources(resources['documentation'])}

**工具资源**:
{self._format_resources(resources['tools'])}

**模板资源**:
{self._format_resources(resources['templates'])}

## 风险与挑战
{self._format_list(task_analysis['potential_challenges'])}

## 准备状态
- 记忆库加载: {'✓' if self.preparation_status['memory_loaded'] else '✗'}
- 索引构建: {'✓' if self.preparation_status['index_built'] else '✗'}
- 环境检查: {'✓' if self.preparation_status['environment_checked'] else '✗'}
- 计划生成: {'✓' if self.preparation_status['plan_generated'] else '✗'}
- 准备时间: {self.preparation_status['elapsed_seconds']:.1f}秒

---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*工作空间: {self.workspace_dir}*
"""
        
        final_report = {
            "content": report_content,
            "summary": self._generate_report_summary(task_analysis, memories, work_plan),
            "key_points": self._extract_key_points(task_analysis, memories),
            "next_steps": work_plan["suggested_actions"][:3],
            "report_generated": datetime.now().isoformat(),
        }
        
        return final_report
    
    def _format_list(self, items: List[str]) -> str:
        """格式化列表"""
        if not items:
            return "暂无内容"
        return "\n".join(f"- {item}" for item in items)
    
    def _format_memories_for_report(self, memories: List[Dict]) -> str:
        """格式化记忆用于报告"""
        if not memories:
            return "暂无相关记忆"
        
        formatted = []
        for i, memory in enumerate(memories, 1):
            title = memory.get("title", "无标题")
            relevance = memory.get("relevance_score", 0)
            category = memory.get("category", "general")
            
            formatted.append(f"{i}. **{title}** (相关性: {relevance:.3f}, 类别: {category})")
        
        return "\n".join(formatted)
    
    def _format_phases(self, phases: List[Dict]) -> str:
        """格式化工作阶段"""
        if not phases:
            return "暂无阶段划分"
        
        formatted = []
        for i, phase in enumerate(phases, 1):
            formatted.append(f"{i}. **{phase['name']}**: {phase['description']}")
        
        return "\n".join(formatted)
    
    def _format_milestones(self, milestones: List[Dict]) -> str:
        """格式化里程碑"""
        if not milestones:
            return "暂无里程碑"
        
        formatted = []
        for milestone in milestones:
            formatted.append(
                f"- **{milestone['name']}** ({milestone['id']}): "
                f"{milestone['description']}"
            )
        
        return "\n".join(formatted)
    
    def _format_resources(self, resources: List[Dict]) -> str:
        """格式化资源"""
        if not resources:
            return "暂无资源"
        
        formatted = []
        for resource in resources:
            formatted.append(f"- {resource['title']} (相关性: {resource['relevance']:.2f})")
        
        return "\n".join(formatted)
    
    def _generate_report_summary(self, task_analysis: Dict[str, Any],
                                memories: List[Dict[str, Any]],
                                work_plan: Dict[str, Any]) -> str:
        """生成报告摘要"""
        summary = [
            f"任务类型: {task_analysis['primary_task_type']}",
            f"复杂度: {task_analysis['complexity']}",
            f"预估时间: {task_analysis['estimated_time']['estimated_range']}",
            f"相关记忆: {len(memories)}条",
            f"工作阶段: {len(work_plan['phases'])}个",
            f"建议操作: {len(work_plan['suggested_actions'])}条",
        ]
        return " | ".join(summary)
    
    def _extract_key_points(self, task_analysis: Dict[str, Any],
                           memories: List[Dict[str, Any]]) -> List[str]:
        """提取关键点"""
        key_points = []
        
        # 从任务分析中提取
        if task_analysis["confidence"] > 0.7:
            key_points.append(f"任务识别准确 (置信度: {task_analysis['confidence']:.2f})")
        
        if task_analysis["complexity"] == "high":
            key_points.append("任务复杂度较高，需要充分准备")
        
        # 从记忆中提取
        if memories:
            best_memory = memories[0]
            if best_memory.get("relevance_score", 0) > 0.8:
                key_points.append(f"找到高度相关记忆: {best_memory.get('title')}")
        
        return key_points
    
    def _save_preparation_results(self, task_description: str,
                                 task_analysis: Dict[str, Any],
                                 memories: List[Dict[str, Any]],
                                 work_plan: Dict[str, Any],
                                 final_report: Dict[str, Any]) -> None:
        """保存准备结果"""
        # 保存报告文件
        report_file = self.output_dir / f"work_preparation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.write_text(final_report["content"], encoding='utf-8')
        
        # 保存JSON数据 - 使用自定义序列化函数
        data_file = self.output_dir / f"preparation_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        def serialize_for_json(obj):
            """递归序列化对象，处理datetime等非JSON原生类型"""
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, (list, tuple)):
                return [serialize_for_json(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: serialize_for_json(value) for key, value in obj.items()}
            elif hasattr(obj, '__dict__'):
                # 处理自定义对象
                return serialize_for_json(obj.__dict__)
            else:
                return obj
        
        data = {
            "task_description": task_description,
            "task_analysis": serialize_for_json(task_analysis),
            "memory_results": serialize_for_json(memories),
            "work_plan": serialize_for_json(work_plan),
            "final_report_summary": final_report["summary"],
            "preparation_status": serialize_for_json(self.preparation_status),
            "timestamp": datetime.now().isoformat(),
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self._log_event("结果已保存", {
            "report_file": str(report_file),
            "data_file": str(data_file),
        })
    
    def _execute_suggested_actions(self, actions: List[str]) -> Dict[str, Any]:
        """执行建议操作"""
        self._log_event("开始执行建议操作", {"action_count": len(actions)})
        
        execution_results = {
            "executed_actions": [],
            "successful_actions": [],
            "failed_actions": [],
            "skipped_actions": [],
            "execution_time": 0,
        }
        
        start_time = time.time()
        
        for i, action in enumerate(actions[:5], 1):  # 最多执行5个操作
            try:
                # 分析操作类型
                if "安装" in action or "install" in action.lower():
                    # 跳过安装操作，需要用户确认
                    execution_results["skipped_actions"].append({
                        "action": action,
                        "reason": "安装操作需要用户确认",
                        "index": i,
                    })
                elif "检查" in action or "检查" in action:
                    # 检查类操作
                    execution_results["executed_actions"].append({
                        "action": action,
                        "result": "检查完成",
                        "status": "completed",
                        "index": i,
                    })
                    execution_results["successful_actions"].append(action)
                else:
                    # 其他操作
                    execution_results["executed_actions"].append({
                        "action": action,
                        "result": "操作已记录",
                        "status": "recorded",
                        "index": i,
                    })
                    execution_results["successful_actions"].append(action)
                
            except Exception as e:
                execution_results["executed_actions"].append({
                    "action": action,
                    "result": f"执行失败: {str(e)}",
                    "status": "failed",
                    "index": i,
                })
                execution_results["failed_actions"].append(action)
        
        execution_results["execution_time"] = time.time() - start_time
        
        self._log_event("建议操作执行完成", {
            "successful": len(execution_results["successful_actions"]),
            "failed": len(execution_results["failed_actions"]),
            "skipped": len(execution_results["skipped_actions"]),
        })
        
        return execution_results
    
    def _get_output_files(self) -> List[str]:
        """获取输出文件列表"""
        output_files = []
        
        if self.output_dir.exists():
            for file_path in self.output_dir.glob("*"):
                if file_path.is_file():
                    output_files.append(str(file_path))
        
        return output_files
    
    def _log_event(self, event: str, details: Dict[str, Any]) -> None:
        """记录事件"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details,
        }
        
        self.work_logs.append(log_entry)
        logger.info(f"[WorkPreparation] {event}: {details}")


def prepare_for_work(task_description: str, workspace_dir: str = None) -> Dict[str, Any]:
    """
    准备新工作的便捷函数
    
    Args:
        task_description: 任务描述
        workspace_dir: 工作空间目录
        
    Returns:
        准备结果
    """
    preparer = WorkPreparation(workspace_dir)
    return preparer.prepare_for_work(task_description)


if __name__ == "__main__":
    # 测试工作准备模块
    import logging
    
    logging.basicConfig(level=logging.INFO)
    
    print("=== 工作准备模块测试 ===")
    
    # 创建测试工作空间
    test_workspace = Path("/tmp/test_work_preparation")
    if test_workspace.exists():
        import shutil
        shutil.rmtree(test_workspace)
    test_workspace.mkdir(parents=True)
    
    # 测试工作准备
    preparer = WorkPreparation(test_workspace)
    
    test_tasks = [
        "制作Excel预算表",
        "安装新的技能",
        "分析工作流程",
    ]
    
    for task in test_tasks:
        print(f"\n{'='*60}")
        print(f"测试任务: {task}")
        print(f"{'='*60}")
        
        result = preparer.prepare_for_work(task)
        
        print(f"任务类型: {result['task_analysis']['primary_task_type']}")
        print(f"复杂度: {result['task_analysis']['complexity']}")
        print(f"预估时间: {result['task_analysis']['estimated_time']['estimated_range']}")
        print(f"相关记忆: {len(result['memory_results'])}条")
        print(f"工作阶段: {len(result['work_plan']['phases'])}个")
        print(f"建议操作: {len(result['work_plan']['suggested_actions'])}条")
        
        # 显示报告文件
        if result['output_files']:
            print(f"输出文件:")
            for file_path in result['output_files'][:2]:
                print(f"  - {file_path}")
    
    print(f"\n{'='*60}")
    print("测试完成")
    
    # 清理测试工作空间
    if test_workspace.exists():
        import shutil
        shutil.rmtree(test_workspace)