#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SQLite schema for the WeChat Article Assistant skill."""

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS login_session (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  token TEXT NOT NULL DEFAULT '',
  cookie_json TEXT NOT NULL DEFAULT '[]',
  cookie_header TEXT NOT NULL DEFAULT '',
  nickname TEXT NOT NULL DEFAULT '',
  head_img TEXT NOT NULL DEFAULT '',
  source TEXT NOT NULL DEFAULT '',
  valid INTEGER NOT NULL DEFAULT 0,
  last_validated_at INTEGER,
  expires_at INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS login_qrcode_session (
  sid TEXT PRIMARY KEY,
  status INTEGER NOT NULL DEFAULT 0,
  status_text TEXT NOT NULL DEFAULT '',
  cookie_json TEXT NOT NULL DEFAULT '[]',
  qr_path TEXT NOT NULL DEFAULT '',
  notify_channel TEXT NOT NULL DEFAULT '',
  notify_target TEXT NOT NULL DEFAULT '',
  notify_account TEXT NOT NULL DEFAULT '',
  created_at INTEGER NOT NULL,
  expires_at INTEGER,
  updated_at INTEGER NOT NULL,
  completed_at INTEGER
);

CREATE TABLE IF NOT EXISTS proxy_config (
  name TEXT PRIMARY KEY,
  enabled INTEGER NOT NULL DEFAULT 0,
  proxy_url TEXT NOT NULL DEFAULT '',
  apply_article_fetch INTEGER NOT NULL DEFAULT 1,
  apply_sync INTEGER NOT NULL DEFAULT 0,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS account (
  fakeid TEXT PRIMARY KEY,
  nickname TEXT NOT NULL DEFAULT '',
  alias TEXT NOT NULL DEFAULT '',
  avatar TEXT NOT NULL DEFAULT '',
  service_type INTEGER NOT NULL DEFAULT 0,
  signature TEXT NOT NULL DEFAULT '',
  processing_mode TEXT NOT NULL DEFAULT 'sync_only',
  categories_json TEXT NOT NULL DEFAULT '[]',
  auto_export_markdown INTEGER NOT NULL DEFAULT 0,
  enabled INTEGER NOT NULL DEFAULT 1,
  total_count INTEGER NOT NULL DEFAULT 0,
  articles_synced INTEGER NOT NULL DEFAULT 0,
  last_sync_at INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS sync_config (
  fakeid TEXT PRIMARY KEY,
  enabled INTEGER NOT NULL DEFAULT 1,
  sync_hour INTEGER NOT NULL DEFAULT 8,
  sync_minute INTEGER NOT NULL DEFAULT 0,
  last_sync_at INTEGER,
  last_sync_status TEXT NOT NULL DEFAULT '',
  last_sync_message TEXT NOT NULL DEFAULT '',
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS article (
  id TEXT PRIMARY KEY,
  fakeid TEXT NOT NULL,
  aid TEXT NOT NULL,
  title TEXT NOT NULL DEFAULT '',
  link TEXT NOT NULL DEFAULT '',
  digest TEXT NOT NULL DEFAULT '',
  cover TEXT NOT NULL DEFAULT '',
  author_name TEXT NOT NULL DEFAULT '',
  create_time INTEGER,
  update_time INTEGER,
  is_deleted INTEGER NOT NULL DEFAULT 0,
  detail_fetched INTEGER NOT NULL DEFAULT 0,
  payload_json TEXT NOT NULL DEFAULT '{}',
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_article_fakeid ON article(fakeid);
CREATE INDEX IF NOT EXISTS idx_article_aid ON article(aid);
CREATE INDEX IF NOT EXISTS idx_article_link ON article(link);
CREATE INDEX IF NOT EXISTS idx_article_create_time ON article(create_time);

CREATE TABLE IF NOT EXISTS article_detail (
  article_id TEXT PRIMARY KEY,
  fakeid TEXT NOT NULL DEFAULT '',
  aid TEXT NOT NULL DEFAULT '',
  link TEXT NOT NULL DEFAULT '',
  account_name TEXT NOT NULL DEFAULT '',
  markdown_content TEXT NOT NULL DEFAULT '',
  html_content TEXT NOT NULL DEFAULT '',
  text_content TEXT NOT NULL DEFAULT '',
  image_json TEXT NOT NULL DEFAULT '[]',
  saved_json_path TEXT NOT NULL DEFAULT '',
  saved_md_path TEXT NOT NULL DEFAULT '',
  saved_html_path TEXT NOT NULL DEFAULT '',
  fetched_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_article_detail_fakeid ON article_detail(fakeid);

CREATE TABLE IF NOT EXISTS sync_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fakeid TEXT NOT NULL,
  nickname TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT '',
  message TEXT NOT NULL DEFAULT '',
  articles_synced INTEGER NOT NULL DEFAULT 0,
  started_at INTEGER,
  finished_at INTEGER,
  created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sync_log_fakeid ON sync_log(fakeid);
CREATE INDEX IF NOT EXISTS idx_sync_log_time ON sync_log(created_at);
"""
