#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDCA循环核心引擎
实现Plan-Do-Check-Act四阶段的全流程管理
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from .utils import (
    load_config, save_config, generate_id, get_current_time, 
    ensure_dir, save_json_file, load_json_file, logger,
    validate_smart_target, send_notification
)
class PDCAPhase(Enum):
    """PDCA阶段枚举"""
    PLAN = "plan"
    DO = "do"
    CHECK = "check"
    ACT = "act"
    COMPLETED = "completed"
class ProjectStatus(Enum):
    """项目状态枚举"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"
@dataclass
class Project:
    """项目数据结构"""
    id: str
    name: str
    type: str
    description: str
    owner: str
    created_at: str
    updated_at: str
    current_phase: PDCAPhase
    status: ProjectStatus
    plan_data: Dict[str, Any]
    do_data: Dict[str, Any]
    check_data: Dict[str, Any]
    act_data: Dict[str, Any]
    quality_score: float
    risk_level: str
    tags: List[str]
    metadata: Dict[str, Any]
class PDCAEngine:
    """PDCA循环核心引擎类"""
    def __init__(self):
        self.config = load_config()
        self.data_dir = os.path.join(os.path.dirname(__file__), '../data')
        self.knowledge_base_dir = os.path.join(os.path.dirname(__file__), '../knowledge_base')
        ensure_dir(self.data_dir)
        ensure_dir(self.knowledge_base_dir)
        logger.info("PDCA引擎初始化完成")
    def init_project(self, name: str, type: str, description: str = "", owner: str = "default") -> Project:
        """
        初始化新项目
        Args:
            name: 项目名称
            type: 项目类型（project/task/decision等）
            description: 项目描述
            owner: 项目负责人
        Returns:
            初始化后的项目对象
        """
        project_id = generate_id('proj')
        now = get_current_time()
        project = Project(
            id=project_id,
            name=name,
            type=type,
            description=description,
            owner=owner,
            created_at=now,
            updated_at=now,
            current_phase=PDCAPhase.PLAN,
            status=ProjectStatus.NOT_STARTED,
            plan_data={},
            do_data={},
            check_data={},
            act_data={},
            quality_score=0.0,
            risk_level="low",
            tags=[],
            metadata={}
        )
        # 保存项目
        self._save_project(project)
        logger.info(f"项目初始化成功: {name} (ID: {project_id})")
        send_notification(f"新项目已创建: {name}", "info")
        return project
    def get_project(self, project_id: str) -> Optional[Project]:
        """
        根据ID获取项目
        Args:
            project_id: 项目ID
        Returns:
            项目对象，不存在返回None
        """
        project_path = os.path.join(self.data_dir, f"{project_id}.json")
        if not os.path.exists(project_path):
            logger.error(f"项目不存在: {project_id}")
            return None
        data = load_json_file(project_path)
        if not data:
            return None
        # 转换枚举类型
        data['current_phase'] = PDCAPhase(data['current_phase'])
        data['status'] = ProjectStatus(data['status'])
        return Project(**data)
    def list_projects(self, status_filter: Optional[ProjectStatus] = None) -> List[Project]:
        """
        列出所有项目
        Args:
            status_filter: 状态过滤，可选
        Returns:
            项目列表
        """
        projects = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json') and filename.startswith('proj_'):
                project_id = filename[:-5]
                project = self.get_project(project_id)
                if project and (status_filter is None or project.status == status_filter):
                    projects.append(project)
        # 按创建时间倒序排列
        projects.sort(key=lambda x: x.created_at, reverse=True)
        return projects
    def update_project(self, project: Project) -> bool:
        """
        更新项目信息
        Args:
            project: 项目对象
        Returns:
            是否更新成功
        """
        project.updated_at = get_current_time()
        return self._save_project(project)
    def _save_project(self, project: Project) -> bool:
        """
        保存项目到文件
        Args:
            project: 项目对象
        Returns:
            是否保存成功
        """
        project_path = os.path.join(self.data_dir, f"{project.id}.json")
        data = asdict(project)
        # 转换枚举为字符串
        data['current_phase'] = data['current_phase'].value
        data['status'] = data['status'].value
        return save_json_file(data, project_path)
    # ==================== Plan阶段方法 ====================
    def set_plan(self, project_id: str, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        设置项目策划信息
        Args:
            project_id: 项目ID
            plan_data: 策划数据，包含target、risk_assessment、quality_standard、resource_plan等
        Returns:
            验证结果
        """
        project = self.get_project(project_id)
        if not project:
            return {"success": False, "message": "项目不存在"}
        if project.current_phase != PDCAPhase.PLAN:
            return {"success": False, "message": f"当前阶段为{project.current_phase.value}，无法修改策划信息"}
        # 验证SMART目标
        target = plan_data.get('target', '')
        smart_result = validate_smart_target(target)
        if not smart_result['passed']:
            return {
                "success": False,
                "message": "目标不符合SMART原则",
                "issues": smart_result['issues'],
                "score": smart_result['score']
            }
        # 验证策划阶段必填项
        required_fields = self.config['pdca']['phase_requirements']['plan']
        missing_fields = []
        for field in required_fields:
            if field == 'target_smart_compliant' and not smart_result['passed']:
                missing_fields.append("目标不符合SMART原则")
            elif field not in plan_data:
                missing_fields.append(field)
        if missing_fields:
            return {
                "success": False,
                "message": "策划信息不完整",
                "missing_fields": missing_fields
            }
        # 保存策划信息
        project.plan_data = plan_data
        project.status = ProjectStatus.PENDING_REVIEW
        self.update_project(project)
        logger.info(f"项目 {project_id} 策划信息已保存，待审核")
        send_notification(f"项目 {project.name} 策划完成，待审核", "info")
        return {
            "success": True,
            "message": "策划信息保存成功",
            "smart_score": smart_result['score'],
            "requires_review": self.config['pdca']['require_review_before_next_phase']
        }
    def approve_plan(self, project_id: str, approved_by: str, comment: str = "") -> Dict[str, Any]:
        """
        审核通过策划阶段
        Args:
            project_id: 项目ID
            approved_by: 审核人
            comment: 审核意见
        Returns:
            审核结果
        """
        project = self.get_project(project_id)
        if not project:
            return {"success": False, "message": "项目不存在"}
        if project.status != ProjectStatus.PENDING_REVIEW or project.current_phase != PDCAPhase.PLAN:
            return {"success": False, "message": "项目当前状态不允许审核"}
        project.plan_data['approved_by'] = approved_by
        project.plan_data['approved_at'] = get_current_time()
        project.plan_data['approval_comment'] = comment
        project.current_phase = PDCAPhase.DO
        project.status = ProjectStatus.IN_PROGRESS
        self.update_project(project)
        logger.info(f"项目 {project_id} 策划阶段审核通过，进入执行阶段")
        send_notification(f"项目 {project.name} 策划审核通过，进入执行阶段", "info")
        return {"success": True, "message": "策划阶段审核通过，已进入执行阶段"}
    def reject_plan(self, project_id: str, rejected_by: str, reason: str) -> Dict[str, Any]:
        """
        驳回策划阶段
        Args:
            project_id: 项目ID
            rejected_by: 驳回人
            reason: 驳回原因
        Returns:
            驳回结果
        """
        project = self.get_project(project_id)
        if not project:
            return {"success": False, "message": "项目不存在"}
        if project.status != ProjectStatus.PENDING_REVIEW or project.current_phase != PDCAPhase.PLAN:
            return {"success": False, "message": "项目当前状态不允许驳回"}
        project.plan_data['rejected_by'] = rejected_by
        project.plan_data['rejected_at'] = get_current_time()
        project.plan_data['rejection_reason'] = reason
        project.status = ProjectStatus.IN_PROGRESS  # 返回修改
        self.update_project(project)
        logger.info(f"项目 {project_id} 策划阶段被驳回: {reason}")
        send_notification(f"项目 {project.name} 策划被驳回: {reason}", "warning")
        return {"success": True, "message": "策划阶段已驳回，请修改后重新提交"}
    # ==================== Do阶段方法 ====================
    def record_execution(self, project_id: str, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        记录执行信息
        Args:
            project_id: 项目ID
            execution_data: 执行数据，包含tasks、progress、records、exceptions等
        Returns:
            记录结果
        """
        project = self.get_project(project_id)
        if not project:
            return {"success": False, "message": "项目不存在"}
        if project.current_phase != PDCAPhase.DO:
            return {"success": False, "message": f"当前阶段为{project.current_phase.value}，无法记录执行信息"}
        # 合并执行数据
        if 'execution_records' not in project.do_data:
            project.do_data['execution_records'] = []
        # 添加时间戳
        execution_data['recorded_at'] = get_current_time()
        project.do_data['execution_records'].append(execution_data)
        # 更新进度
        if 'progress' in execution_data:
            project.do_data['current_progress'] = execution_data['progress']
        # 异常处理
        if 'exceptions' in execution_data and execution_data['exceptions']:
            project.do_data['has_exceptions'] = True
            project.do_data['exceptions'] = project.do_data.get('exceptions', []) + execution_data['exceptions']
            send_notification(f"项目 {project.name} 执行中发现异常: {len(execution_data['exceptions'])}个", "warning")
        # 检查是否完成执行阶段
        required_fields = self.config['pdca']['phase_requirements']['do']
        all_completed = True
        for field in required_fields:
            if field not in project.do_data:
                all_completed = False
                break
        if all_completed:
            project.status = ProjectStatus.PENDING_REVIEW
        self.update_project(project)
        logger.info(f"项目 {project_id} 执行信息已记录")
        return {
            "success": True,
            "message": "执行信息记录成功",
            "current_progress": project.do_data.get('current_progress', 0),
            "pending_review": project.status == ProjectStatus.PENDING_REVIEW
        }
    def complete_execution(self, project_id: str, summary: str) -> Dict[str, Any]:
        """
        完成执行阶段
        Args:
            project_id: 项目ID
            summary: 执行总结
        Returns:
            完成结果
        """
        project = self.get_project(project_id)
        if not project:
            return {"success": False, "message": "项目不存在"}
        if project.current_phase != PDCAPhase.DO:
            return {"success": False, "message": f"当前阶段为{project.current_phase.value}，无法完成执行阶段"}
        project.do_data['completion_summary'] = summary
        project.do_data['completed_at'] = get_current_time()
        project.status = ProjectStatus.PENDING_REVIEW
        self.update_project(project)
        logger.info(f"项目 {project_id} 执行阶段完成，待审核")
        send_notification(f"项目 {project.name} 执行阶段完成，待审核", "info")
        return {"success": True, "message": "执行阶段已完成，待审核进入检查阶段"}
    def approve_execution(self, project_id: str, approved_by: str, comment: str = "") -> Dict[str, Any]:
        """
        审核通过执行阶段，进入检查阶段
        """
        project = self.get_project(project_id)
        if not project:
            return {"success": False, "message": "项目不存在"}
        if project.status != ProjectStatus.PENDING_REVIEW or project.current_phase != PDCAPhase.DO:
            return {"success": False, "message": "项目当前状态不允许审核"}
        project.do_data['approved_by'] = approved_by
        project.do_data['approved_at'] = get_current_time()
        project.do_data['approval_comment'] = comment
        project.current_phase = PDCAPhase.CHECK
        project.status = ProjectStatus.IN_PROGRESS
        self.update_project(project)
        logger.info(f"项目 {project_id} 执行阶段审核通过，进入检查阶段")
        send_notification(f"项目 {project.name} 执行审核通过，进入检查阶段", "info")
        return {"success": True, "message": "执行阶段审核通过，已进入检查阶段"}
    # ==================== Check阶段方法 ====================
    def record_check(self, project_id: str, check_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        记录检查结果
        Args:
            project_id: 项目ID
            check_data: 检查数据，包含quality_checks、deviations、root_causes、quality_score等
        Returns:
            记录结果
        """
        project = self.get_project(project_id)
        if not project:
            return {"success": False, "message": "项目不存在"}
        if project.current_phase != PDCAPhase.CHECK:
            return {"success": False, "message": f"当前阶段为{project.current_phase.value}，无法记录检查信息"}
        # 保存检查数据
        project.check_data = check_data
        # 更新质量评分
        if 'quality_score' in check_data:
            project.quality_score = check_data['quality_score']
        # 更新风险等级
        if 'risk_level' in check_data:
            project.risk_level = check_data['risk_level']
        # 问题清单
        if 'problems' in check_data and check_data['problems']:
            project.check_data['problem_count'] = len(check_data['problems'])
            send_notification(f"项目 {project.name} 检查发现 {len(check_data['problems'])} 个问题", "warning")
        # 检查是否完成检查阶段
        required_fields = self.config['pdca']['phase_requirements']['check']
        missing_fields = [field for field in required_fields if field not in check_data]
        if not missing_fields:
            project.status = ProjectStatus.PENDING_REVIEW
        self.update_project(project)
        logger.info(f"项目 {project_id} 检查信息已记录")
        return {
            "success": True,
            "message": "检查信息记录成功",
            "quality_score": project.quality_score,
            "problem_count": project.check_data.get('problem_count', 0),
            "pending_review": project.status == ProjectStatus.PENDING_REVIEW
        }
    def approve_check(self, project_id: str, approved_by: str, comment: str = "") -> Dict[str, Any]:
        """
        审核通过检查阶段，进入处置阶段
        """
        project = self.get_project(project_id)
        if not project:
            return {"success": False, "message": "项目不存在"}
        if project.status != ProjectStatus.PENDING_REVIEW or project.current_phase != PDCAPhase.CHECK:
            return {"success": False, "message": "项目当前状态不允许审核"}
        project.check_data['approved_by'] = approved_by
        project.check_data['approved_at'] = get_current_time()
        project.check_data['approval_comment'] = comment
        project.current_phase = PDCAPhase.ACT
        project.status = ProjectStatus.IN_PROGRESS
        self.update_project(project)
        logger.info(f"项目 {project_id} 检查阶段审核通过，进入处置阶段")
        send_notification(f"项目 {project.name} 检查审核通过，进入处置阶段", "info")
        return {"success": True, "message": "检查阶段审核通过，已进入处置阶段"}
    # ==================== Act阶段方法 ====================
    def record_improvement(self, project_id: str, improvement_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        记录改进措施
        Args:
            project_id: 项目ID
            improvement_data: 改进数据，包含correction_plan、improvement_measures、lessons_learned等
        Returns:
            记录结果
        """
        project = self.get_project(project_id)
        if not project:
            return {"success": False, "message": "项目不存在"}
        if project.current_phase != PDCAPhase.ACT:
            return {"success": False, "message": f"当前阶段为{project.current_phase.value}，无法记录改进信息"}
        # 保存改进数据
        project.act_data = improvement_data
        # 检查是否完成处置阶段
        required_fields = self.config['pdca']['phase_requirements']['act']
        missing_fields = [field for field in required_fields if field not in improvement_data]
        if not missing_fields:
            project.status = ProjectStatus.PENDING_REVIEW
        self.update_project(project)
        logger.info(f"项目 {project_id} 改进信息已记录")
        return {
            "success": True,
            "message": "改进信息记录成功",
            "pending_review": project.status == ProjectStatus.PENDING_REVIEW
        }
    def complete_project(self, project_id: str, approved_by: str, comment: str = "") -> Dict[str, Any]:
        """
        完成整个PDCA循环，关闭项目
        Args:
            project_id: 项目ID
            approved_by: 审核人
            comment: 审核意见
        Returns:
            完成结果
        """
        project = self.get_project(project_id)
        if not project:
            return {"success": False, "message": "项目不存在"}
        if project.status != ProjectStatus.PENDING_REVIEW or project.current_phase != PDCAPhase.ACT:
            return {"success": False, "message": "项目当前状态不允许完成"}
        project.act_data['approved_by'] = approved_by
        project.act_data['approved_at'] = get_current_time()
        project.act_data['approval_comment'] = comment
        project.current_phase = PDCAPhase.COMPLETED
        project.status = ProjectStatus.COMPLETED
        project.updated_at = get_current_time()
        self.update_project(project)
        # 自动归档到知识库
        if self.config['pdca']['auto_archive_on_complete']:
            self._archive_to_knowledge_base(project)
        logger.info(f"项目 {project_id} 已完成，PDCA循环结束")
        send_notification(f"项目 {project.name} 已成功完成！质量评分: {project.quality_score}", "info")
        return {
            "success": True,
            "message": "项目已成功完成",
            "project_summary": self._generate_project_summary(project)
        }
    def _archive_to_knowledge_base(self, project: Project) -> bool:
        """
        将完成的项目归档到知识库
        Args:
            project: 项目对象
        Returns:
            是否归档成功
        """
        try:
            archive_data = {
                "project_id": project.id,
                "name": project.name,
                "type": project.type,
                "description": project.description,
                "completed_at": project.updated_at,
                "quality_score": project.quality_score,
                "lessons_learned": project.act_data.get('lessons_learned', ''),
                "best_practices": project.act_data.get('best_practices', []),
                "improvement_measures": project.act_data.get('improvement_measures', []),
                "tags": project.tags
            }
            archive_path = os.path.join(self.knowledge_base_dir, 'experience_lib', f"{project.id}.json")
            save_json_file(archive_data, archive_path)
            logger.info(f"项目 {project.id} 已归档到知识库")
            return True
        except Exception as e:
            logger.error(f"归档项目到知识库失败: {e}")
            return False
    def _generate_project_summary(self, project: Project) -> Dict[str, Any]:
        """
        生成项目摘要
        Args:
            project: 项目对象
        Returns:
            项目摘要字典
        """
        return {
            "id": project.id,
            "name": project.name,
            "type": project.type,
            "duration": f"{project.created_at} 至 {project.updated_at}",
            "quality_score": project.quality_score,
            "risk_level": project.risk_level,
            "problem_count": project.check_data.get('problem_count', 0),
            "lessons_learned": project.act_data.get('lessons_learned', ''),
            "key_achievements": project.act_data.get('key_achievements', [])
        }
    def get_project_progress(self, project_id: str) -> Dict[str, Any]:
        """
        获取项目进度
        Args:
            project_id: 项目ID
        Returns:
            进度信息
        """
        project = self.get_project(project_id)
        if not project:
            return {"success": False, "message": "项目不存在"}
        phase_progress = {
            PDCAPhase.PLAN: 25,
            PDCAPhase.DO: 50,
            PDCAPhase.CHECK: 75,
            PDCAPhase.ACT: 90,
            PDCAPhase.COMPLETED: 100
        }
        overall_progress = phase_progress.get(project.current_phase, 0)
        # 执行阶段取实际进度
        if project.current_phase == PDCAPhase.DO:
            execution_progress = project.do_data.get('current_progress', 0)
            overall_progress = 25 + (execution_progress * 0.25)  # 执行阶段占25%总进度
        return {
            "success": True,
            "current_phase": project.current_phase.value,
            "status": project.status.value,
            "overall_progress": round(overall_progress, 1),
            "quality_score": project.quality_score,
            "risk_level": project.risk_level,
            "updated_at": project.updated_at
        }
