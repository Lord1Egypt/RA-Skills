#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Story Pipeline Skill
剧情生成管道流技能
"""

from .pipeline import (
    get_pipeline,
    create_pipeline,
    start_generation,
    submit_episode,
    process_ai_review,
    user_confirm,
    get_status,
    list_pipelines,
    resume_pipeline
)

from .graph_manager import get_graph_manager, GraphManager
from .ai_reviewer import get_ai_reviewer, AIReviewer
from .episode_generator import get_episode_generator, EpisodeGenerator

__all__ = [
    # 主控函数
    'get_pipeline',
    'create_pipeline',
    'start_generation',
    'submit_episode',
    'process_ai_review',
    'user_confirm',
    'get_status',
    'list_pipelines',
    'resume_pipeline',
    
    # 管理器
    'get_graph_manager',
    'GraphManager',
    'get_ai_reviewer',
    'AIReviewer',
    'get_episode_generator',
    'EpisodeGenerator',
]

__version__ = '1.0.0'