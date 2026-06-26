#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Facade exports for article-related services."""

from article_detail_service import article_detail
from article_metadata_service import get_article_row, normalize_remote_article, query_local_articles, recent_articles, upsert_articles
from article_report_service import export_account_report_markdown, export_recent_combined_report_markdown, fetch_account_details

__all__ = [
    "article_detail",
    "export_account_report_markdown",
    "export_recent_combined_report_markdown",
    "fetch_account_details",
    "get_article_row",
    "normalize_remote_article",
    "query_local_articles",
    "recent_articles",
    "upsert_articles",
]
