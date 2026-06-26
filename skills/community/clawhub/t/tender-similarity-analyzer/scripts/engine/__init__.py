# -*- coding: utf-8 -*-
"""
查重引擎模块
"""

from .checker import PlagiarismChecker
from .text_cleaner import TextCleaner
from .paragraph_splitter import ParagraphSplitter
from .ngram_checker import NgramChecker
from .tfidf_checker import TFIDFChecker
from .simhash_checker import SimHashChecker

__all__ = [
    'PlagiarismChecker',
    'TextCleaner',
    'ParagraphSplitter',
    'NgramChecker',
    'TFIDFChecker',
    'SimHashChecker'
]
