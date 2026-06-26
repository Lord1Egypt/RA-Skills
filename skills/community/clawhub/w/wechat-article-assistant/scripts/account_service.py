#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Facade exports for account-related services."""

from account_management_service import add_account, add_account_by_keyword, add_account_by_url, resolve_account_by_url, search_account
from account_query_service import delete_account, list_account_articles, list_accounts, list_sync_targets, set_account_config, set_sync_target

__all__ = [
    "add_account",
    "add_account_by_keyword",
    "add_account_by_url",
    "delete_account",
    "list_account_articles",
    "list_accounts",
    "list_sync_targets",
    "resolve_account_by_url",
    "search_account",
    "set_account_config",
    "set_sync_target",
]
