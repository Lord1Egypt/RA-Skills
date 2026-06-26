#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token Saver - 한국어 Context DB for AI Agents v2.0

토큰 절감 91% 달성을 위한 한국어 최적화 Context DB
신규 기능: 임베딩 기반 의미 검색, 중복 자동 병합, 자동 만료/아카이브, 메모리 계층화
"""

from token_saver.client import (
    TokenSaverKorean, 
    Context, 
    KoreanTokenizer, 
    MultilingualTokenizer,
    ContextStore,
    EmbeddingManager,
    SimilarityChecker,
    CategorySuggester,
    WALManager,
    SessionStateManager,
    EntityExtractor,
    VersionBackup,
    CacheManager
)

__version__ = "2.0.0"
__author__ = "ClawHub"
__all__ = [
    "TokenSaverKorean", 
    "Context", 
    "KoreanTokenizer", 
    "MultilingualTokenizer",
    "ContextStore",
    "EmbeddingManager",
    "SimilarityChecker",
    "CategorySuggester",
    "WALManager",
    "SessionStateManager",
    "EntityExtractor",
    "VersionBackup",
    "CacheManager"
]