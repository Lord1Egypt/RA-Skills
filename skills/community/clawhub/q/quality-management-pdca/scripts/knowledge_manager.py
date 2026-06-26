#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识管理模块
实现经验沉淀、模板管理、规则更新、模式提炼等知识管理功能
"""
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from .utils import load_config, ensure_dir, save_json_file, load_json_file, logger
class KnowledgeManager:
    """知识管理类"""
    def __init__(self):
        self.config = load_config()
        self.base_dir = os.path.join(os.path.dirname(__file__), '../knowledge_base')
        self.experience_lib_dir = os.path.join(self.base_dir, 'experience_lib')
        self.template_lib_dir = os.path.join(self.base_dir, 'template_lib')
        self.rule_lib_dir = os.path.join(self.base_dir, 'rule_lib')
        self.pattern_lib_dir = os.path.join(self.base_dir, 'pattern_lib')
        # 确保目录存在
        ensure_dir(self.experience_lib_dir)
        ensure_dir(self.template_lib_dir)
        ensure_dir(self.rule_lib_dir)
        ensure_dir(self.pattern_lib_dir)
        logger.info("知识管理模块初始化完成")
    # ==================== 经验库管理 ====================
    def add_experience(self, experience_data: Dict[str, Any]) -> str:
        """
        添加经验到经验库
        Args:
            experience_data: 经验数据，包含title、content、type、tags、source等字段
        Returns:
            经验ID
        """
        experience_id = f"exp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(experience_data.get('title', '')) % 10000:04d}"
        experience_data['id'] = experience_id
        experience_data['created_at'] = datetime.now().isoformat()
        experience_data['views'] = 0
        experience_data['usage_count'] = 0
        experience_data['rating'] = 0.0
        experience_data['rating_count'] = 0
        file_path = os.path.join(self.experience_lib_dir, f"{experience_id}.json")
        save_json_file(experience_data, file_path)
        logger.info(f"新经验已添加到经验库: {experience_id} - {experience_data.get('title', '')}")
        return experience_id
    def get_experience(self, experience_id: str) -> Optional[Dict[str, Any]]:
        """
        根据ID获取经验
        Args:
            experience_id: 经验ID
        Returns:
            经验数据，不存在返回None
        """
        file_path = os.path.join(self.experience_lib_dir, f"{experience_id}.json")
        if not os.path.exists(file_path):
            logger.warning(f"经验不存在: {experience_id}")
            return None
        experience = load_json_file(file_path)
        if experience:
            # 增加浏览次数
            experience['views'] += 1
            save_json_file(experience, file_path)
        return experience
    def search_experience(self, keyword: str, tags: Optional[List[str]] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        搜索经验
        Args:
            keyword: 关键词
            tags: 标签过滤，可选
            limit: 返回结果数量限制
        Returns:
            经验列表
        """
        results = []
        for filename in os.listdir(self.experience_lib_dir):
            if not filename.endswith('.json'):
                continue
            file_path = os.path.join(self.experience_lib_dir, filename)
            experience = load_json_file(file_path)
            if not experience:
                continue
            # 关键词匹配
            match = False
            if keyword.lower() in experience.get('title', '').lower() or \
               keyword.lower() in experience.get('content', '').lower():
                match = True
            # 标签匹配
            if tags and match:
                experience_tags = experience.get('tags', [])
                if not any(tag in experience_tags for tag in tags):
                    match = False
            if match:
                results.append(experience)
        # 按使用次数和评分排序
        results.sort(key=lambda x: (x.get('usage_count', 0), x.get('rating', 0)), reverse=True)
        return results[:limit]
    def update_experience_usage(self, experience_id: str) -> bool:
        """
        更新经验使用次数
        Args:
            experience_id: 经验ID
        Returns:
            是否更新成功
        """
        experience = self.get_experience(experience_id)
        if not experience:
            return False
        experience['usage_count'] += 1
        file_path = os.path.join(self.experience_lib_dir, f"{experience_id}.json")
        return save_json_file(experience, file_path)
    def rate_experience(self, experience_id: str, rating: float) -> bool:
        """
        对经验评分
        Args:
            experience_id: 经验ID
            rating: 评分（0-5）
        Returns:
            是否评分成功
        """
        experience = self.get_experience(experience_id)
        if not experience:
            return False
        # 计算新的平均评分
        total_rating = experience.get('rating', 0.0) * experience.get('rating_count', 0)
        total_rating += rating
        experience['rating_count'] = experience.get('rating_count', 0) + 1
        experience['rating'] = round(total_rating / experience['rating_count'], 2)
        file_path = os.path.join(self.experience_lib_dir, f"{experience_id}.json")
        return save_json_file(experience, file_path)
    def list_experiences(self, type_filter: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        列出经验库中的经验
        Args:
            type_filter: 类型过滤，可选
            limit: 返回数量限制
        Returns:
            经验列表
        """
        experiences = []
        for filename in os.listdir(self.experience_lib_dir):
            if not filename.endswith('.json'):
                continue
            file_path = os.path.join(self.experience_lib_dir, filename)
            experience = load_json_file(file_path)
            if not experience:
                continue
            if type_filter and experience.get('type') != type_filter:
                continue
            experiences.append(experience)
        # 按创建时间倒序
        experiences.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return experiences[:limit]
    # ==================== 模板库管理 ====================
    def add_template(self, template_data: Dict[str, Any]) -> str:
        """
        添加模板到模板库
        Args:
            template_data: 模板数据，包含name、type、content、description、tags等字段
        Returns:
            模板ID
        """
        template_id = f"tpl_{template_data.get('type', 'general')}_{template_data.get('name', '').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        template_data['id'] = template_id
        template_data['created_at'] = datetime.now().isoformat()
        template_data['usage_count'] = 0
        template_data['version'] = "1.0.0"
        file_path = os.path.join(self.template_lib_dir, f"{template_id}.json")
        save_json_file(template_data, file_path)
        logger.info(f"新模板已添加到模板库: {template_id} - {template_data.get('name', '')}")
        return template_id
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        根据ID获取模板
        Args:
            template_id: 模板ID
        Returns:
            模板数据，不存在返回None
        """
        file_path = os.path.join(self.template_lib_dir, f"{template_id}.json")
        if not os.path.exists(file_path):
            logger.warning(f"模板不存在: {template_id}")
            return None
        template = load_json_file(file_path)
        if template:
            template['usage_count'] += 1
            save_json_file(template, file_path)
        return template
    def get_templates_by_type(self, template_type: str) -> List[Dict[str, Any]]:
        """
        根据类型获取模板列表
        Args:
            template_type: 模板类型（plan/execution/check/act等）
        Returns:
            模板列表
        """
        templates = []
        for filename in os.listdir(self.template_lib_dir):
            if not filename.endswith('.json'):
                continue
            file_path = os.path.join(self.template_lib_dir, filename)
            template = load_json_file(file_path)
            if template and template.get('type') == template_type:
                templates.append(template)
        # 按使用次数排序
        templates.sort(key=lambda x: x.get('usage_count', 0), reverse=True)
        return templates
    def update_template(self, template_id: str, updated_content: Dict[str, Any]) -> bool:
        """
        更新模板
        Args:
            template_id: 模板ID
            updated_content: 更新的内容
        Returns:
            是否更新成功
        """
        template = self.get_template(template_id)
        if not template:
            return False
        # 版本号升级
        version_parts = template.get('version', '1.0.0').split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        template['version'] = '.'.join(version_parts)
        template['updated_at'] = datetime.now().isoformat()
        template.update(updated_content)
        file_path = os.path.join(self.template_lib_dir, f"{template_id}.json")
        return save_json_file(template, file_path)
    # ==================== 规则库管理 ====================
    def add_rule(self, rule_data: Dict[str, Any]) -> str:
        """
        添加规则到规则库
        Args:
            rule_data: 规则数据，包含name、condition、action、priority、description等字段
        Returns:
            规则ID
        """
        rule_id = f"rule_{rule_data.get('priority', 'medium')}_{rule_data.get('name', '').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        rule_data['id'] = rule_id
        rule_data['created_at'] = datetime.now().isoformat()
        rule_data['enabled'] = True
        rule_data['trigger_count'] = 0
        file_path = os.path.join(self.rule_lib_dir, f"{rule_id}.json")
        save_json_file(rule_data, file_path)
        logger.info(f"新规则已添加到规则库: {rule_id} - {rule_data.get('name', '')}")
        return rule_id
    def get_enabled_rules(self) -> List[Dict[str, Any]]:
        """
        获取所有启用的规则
        Returns:
            启用的规则列表
        """
        rules = []
        for filename in os.listdir(self.rule_lib_dir):
            if not filename.endswith('.json'):
                continue
            file_path = os.path.join(self.rule_lib_dir, filename)
            rule = load_json_file(file_path)
            if rule and rule.get('enabled', False):
                rules.append(rule)
        # 按优先级排序
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        rules.sort(key=lambda x: priority_order.get(x.get('priority', 'medium'), 99))
        return rules
    def evaluate_rules(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        评估规则，返回匹配的规则
        Args:
            context: 上下文数据
        Returns:
            匹配的规则列表
        """
        matched_rules = []
        enabled_rules = self.get_enabled_rules()
        for rule in enabled_rules:
            try:
                # 简单的规则匹配逻辑，可扩展为更复杂的规则引擎
                condition = rule.get('condition', '')
                if not condition:
                    continue
                # 简单的变量替换和条件判断
                for key, value in context.items():
                    condition = condition.replace(f"${key}", str(value))
                # 执行条件判断（简化实现）
                if eval(condition, {"__builtins__": {}}, {}):
                    rule['trigger_count'] += 1
                    matched_rules.append(rule)
                    # 更新触发次数
                    file_path = os.path.join(self.rule_lib_dir, f"{rule['id']}.json")
                    save_json_file(rule, file_path)
            except Exception as e:
                logger.error(f"规则评估失败 {rule['id']}: {e}")
                continue
        return matched_rules
    def toggle_rule(self, rule_id: str, enabled: bool) -> bool:
        """
        启用/禁用规则
        Args:
            rule_id: 规则ID
            enabled: 是否启用
        Returns:
            是否操作成功
        """
        file_path = os.path.join(self.rule_lib_dir, f"{rule_id}.json")
        if not os.path.exists(file_path):
            logger.warning(f"规则不存在: {rule_id}")
            return False
        rule = load_json_file(file_path)
        if not rule:
            return False
        rule['enabled'] = enabled
        rule['updated_at'] = datetime.now().isoformat()
        return save_json_file(rule, file_path)
    # ==================== 模式库管理 ====================
    def add_pattern(self, pattern_data: Dict[str, Any]) -> str:
        """
        添加模式到模式库
        Args:
            pattern_data: 模式数据，包含name、pattern_type、description、examples、recommendation等字段
        Returns:
            模式ID
        """
        pattern_id = f"pat_{pattern_data.get('pattern_type', 'general')}_{hash(pattern_data.get('description', '')) % 10000:04d}"
        pattern_data['id'] = pattern_id
        pattern_data['created_at'] = datetime.now().isoformat()
        pattern_data['occurrence_count'] = 1
        pattern_data['success_rate'] = 0.0
        file_path = os.path.join(self.pattern_lib_dir, f"{pattern_id}.json")
        save_json_file(pattern_data, file_path)
        logger.info(f"新模式已添加到模式库: {pattern_id} - {pattern_data.get('name', '')}")
        return pattern_id
    def find_similar_patterns(self, problem_description: str, threshold: float = 0.6) -> List[Dict[str, Any]]:
        """
        查找相似模式
        Args:
            problem_description: 问题描述
            threshold: 相似度阈值
        Returns:
            相似模式列表
        """
        # 简化的相似度匹配，实际可集成NLP模型
        patterns = []
        for filename in os.listdir(self.pattern_lib_dir):
            if not filename.endswith('.json'):
                continue
            file_path = os.path.join(self.pattern_lib_dir, filename)
            pattern = load_json_file(file_path)
            if not pattern:
                continue
            # 简单关键词匹配
            keywords = pattern.get('keywords', [])
            if not keywords:
                keywords = pattern.get('description', '').split()
            match_count = sum(1 for keyword in keywords if keyword.lower() in problem_description.lower())
            if len(keywords) > 0:
                similarity = match_count / len(keywords)
                if similarity >= threshold:
                    pattern['similarity'] = round(similarity, 2)
                    patterns.append(pattern)
        # 按相似度和成功率排序
        patterns.sort(key=lambda x: (x.get('similarity', 0), x.get('success_rate', 0)), reverse=True)
        return patterns
    def update_pattern_success_rate(self, pattern_id: str, success: bool) -> bool:
        """
        更新模式成功率
        Args:
            pattern_id: 模式ID
            success: 是否成功
        Returns:
            是否更新成功
        """
        file_path = os.path.join(self.pattern_lib_dir, f"{pattern_id}.json")
        if not os.path.exists(file_path):
            logger.warning(f"模式不存在: {pattern_id}")
            return False
        pattern = load_json_file(file_path)
        if not pattern:
            return False
        total = pattern.get('occurrence_count', 0)
        success_count = pattern.get('success_rate', 0.0) * total
        if success:
            success_count += 1
        total += 1
        pattern['occurrence_count'] = total
        pattern['success_rate'] = round(success_count / total, 2)
        return save_json_file(pattern, file_path)
    # ==================== 自动学习功能 ====================
    def auto_extract_knowledge(self, project_data: Dict[str, Any]) -> bool:
        """
        从完成的项目中自动提取知识
        Args:
            project_data: 项目完整数据
        Returns:
            是否提取成功
        """
        if not self.config['knowledge']['enable_auto_learning']:
            logger.info("自动学习功能未启用")
            return False
        try:
            project_id = project_data.get('id')
            project_name = project_data.get('name')
            quality_score = project_data.get('quality_score', 0)
            # 只有质量评分高于阈值的项目才提取知识
            extraction_threshold = self.config['knowledge']['experience_extraction_threshold']
            if quality_score < extraction_threshold:
                logger.info(f"项目质量评分{quality_score}低于阈值{extraction_threshold}，不提取知识")
                return False
            # 1. 提取经验教训
            act_data = project_data.get('act_data', {})
            lessons_learned = act_data.get('lessons_learned', '')
            best_practices = act_data.get('best_practices', [])
            if lessons_learned or best_practices:
                experience_data = {
                    'title': f"项目《{project_name}》经验总结",
                    'content': f"经验教训：{lessons_learned}\n最佳实践：{'; '.join(best_practices)}",
                    'type': 'project_summary',
                    'tags': project_data.get('tags', []) + ['经验总结', '项目复盘'],
                    'source': f"project:{project_id}",
                    'quality_score': quality_score
                }
                self.add_experience(experience_data)
            # 2. 提取改进措施作为规则
            improvement_measures = act_data.get('improvement_measures', [])
            for measure in improvement_measures:
                if isinstance(measure, dict) and 'condition' in measure and 'action' in measure:
                    rule_data = {
                        'name': measure.get('name', f"来自项目{project_name}的改进规则"),
                        'condition': measure.get('condition', ''),
                        'action': measure.get('action', ''),
                        'priority': measure.get('priority', 'medium'),
                        'description': measure.get('description', ''),
                        'source': f"project:{project_id}"
                    }
                    self.add_rule(rule_data)
            # 3. 如果是高质量项目，提取模板
            if quality_score >= 90:
                plan_data = project_data.get('plan_data', {})
                if plan_data:
                    template_data = {
                        'name': f"{project_name}策划模板",
                        'type': 'plan',
                        'content': plan_data,
                        'description': f"来自高质量项目《{project_name}》的策划模板，质量评分{quality_score}",
                        'tags': project_data.get('tags', []) + ['高质量模板', '策划']
                    }
                    self.add_template(template_data)
            logger.info(f"已从项目{project_id}自动提取知识")
            return True
        except Exception as e:
            logger.error(f"自动提取知识失败: {e}")
            return False
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """
        获取知识库统计信息
        Returns:
            统计数据
        """
        def count_files(dir_path: str) -> int:
            if not os.path.exists(dir_path):
                return 0
            return len([f for f in os.listdir(dir_path) if f.endswith('.json')])
        return {
            'experience_count': count_files(self.experience_lib_dir),
            'template_count': count_files(self.template_lib_dir),
            'rule_count': count_files(self.rule_lib_dir),
            'pattern_count': count_files(self.pattern_lib_dir),
            'auto_learning_enabled': self.config['knowledge']['enable_auto_learning'],
            'extraction_threshold': self.config['knowledge']['experience_extraction_threshold']
        }
    def cleanup_old_data(self, days: int = 365) -> int:
        """
        清理超过指定天数的旧数据
        Args:
            days: 保留天数，默认365天
        Returns:
            清理的文件数量
        """
        if not self.config['knowledge']['auto_cleanup_enabled']:
            return 0
        cleaned_count = 0
        cutoff_time = datetime.now().timestamp() - days * 86400
        # 遍历所有知识库目录
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if not file.endswith('.json'):
                    continue
                file_path = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(file_path)
                    if mtime < cutoff_time:
                        os.remove(file_path)
                        cleaned_count += 1
                        logger.info(f"已清理旧文件: {file_path}")
                except Exception as e:
                    logger.error(f"清理文件失败 {file_path}: {e}")
        logger.info(f"共清理了{cleaned_count}个旧文件")
        return cleaned_count
