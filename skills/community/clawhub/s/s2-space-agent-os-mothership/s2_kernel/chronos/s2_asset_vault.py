#!/usr/bin/env python3
import time
import uuid
import logging
import sqlite3
import json
import os
from enum import Enum
from datetime import datetime
from typing import List, Optional

# =====================================================================
# 🌌 S2-SP-OS: Semantic Data Asset Vault (V1.1 SQL Hardened)
# 家庭语义数据资产保险柜：基于本地 SQLite 的持久化存储与防注入设计
# =====================================================================

class AssetType(Enum):
    AUDIO = "AUDIO"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    DOCUMENT = "DOCUMENT"
    SNAPSHOT = "SNAPSHOT"

class S2AssetVault:
    def __init__(self, db_path: str = "s2_data_cache/s2_assets.db"):
        self.logger = logging.getLogger("S2_Asset_Vault")
        
        # 确保数据库目录存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # 连接本地 SQLite 数据库 (启用多线程访问支持与超时锁等待)
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=10.0)
        self._init_database()

    def _init_database(self):
        """初始化 SQL 数据表结构"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS s2_assets (
                asset_id TEXT PRIMARY KEY,
                owner_did TEXT NOT NULL,
                asset_type TEXT NOT NULL,
                storage_uri TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                semantic_tags JSON NOT NULL,
                spatial_anchor TEXT NOT NULL
            )
        ''')
        # 为高频查询字段建立索引，提升性能
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_owner ON s2_assets(owner_did)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON s2_assets(asset_type)')
        self.conn.commit()
        self.logger.info(f"🗄️ SQL 底座初始化完成: {self.db_path}")

    def ingest_asset(self, uploader_did: str, asset_type: AssetType, storage_uri: str, semantic_description: str, spatial_zone: str = "Global") -> str:
        """[入库网关]：带有防注入参数化查询的落盘逻辑"""
        asset_id = f"ASSET-{uuid.uuid4().hex[:12].upper()}"
        timestamp = datetime.now().isoformat()
        
        # 简单分词打标签 (生产环境将由本地 LLM 完成)
        extracted_tags = [tag.strip() for tag in semantic_description.replace("，", ",").split(",")]
        tags_json = json.dumps(extracted_tags, ensure_ascii=False)

        cursor = self.conn.cursor()
        # ⚠️ 极客防线：严格使用 `?` 参数化绑定，绝不使用 f-string 拼接 SQL，防死 SQL 注入！
        cursor.execute('''
            INSERT INTO s2_assets (asset_id, owner_did, asset_type, storage_uri, timestamp, semantic_tags, spatial_anchor)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (asset_id, uploader_did, asset_type.value, storage_uri, timestamp, tags_json, spatial_zone))
        
        self.conn.commit()
        self.logger.info(f"📥 资产已物理落盘 [{asset_id}] -> SQL DB")
        return asset_id

    def intent_based_search(self, requester_did: str, natural_language_query: str, target_type: Optional[AssetType] = None) -> list:
        """[出库网关]：基于 SQL 查询与 Python 内存结合的语义检索"""
        query_keywords = natural_language_query.replace("，", "").replace("的", "").split(" ")
        cursor = self.conn.cursor()
        
        # 1. 第一层 SQL 物理过滤：权限与类型
        # 这里模拟主人的 D-OWNER-DH 最高越权
        if requester_did.startswith("D-OWNER-DH"):
            if target_type:
                cursor.execute('SELECT * FROM s2_assets WHERE asset_type = ?', (target_type.value,))
            else:
                cursor.execute('SELECT * FROM s2_assets')
        else:
            if target_type:
                cursor.execute('SELECT * FROM s2_assets WHERE (owner_did = ? OR owner_did = "FAMILY_PUBLIC") AND asset_type = ?', 
                               (requester_did, target_type.value))
            else:
                cursor.execute('SELECT * FROM s2_assets WHERE owner_did = ? OR owner_did = "FAMILY_PUBLIC"', 
                               (requester_did,))
        
        rows = cursor.fetchall()
        
        # 2. 第二层 Python 内存语义匹配 (弥补 SQLite 原生不支持向量检索的短板)
        results = []
        for row in rows:
            # 解析 SQL 记录 (asset_id, owner_did, asset_type, storage_uri, timestamp, semantic_tags, spatial_anchor)
            asset_data = {
                "asset_id": row[0], "owner_did": row[1], "asset_type": row[2], 
                "storage_uri": row[3], "timestamp": row[4], 
                "semantic_tags": json.loads(row[5]), "spatial_anchor": row[6]
            }
            
            match_score = 0
            for keyword in query_keywords:
                if any(keyword in tag for tag in asset_data["semantic_tags"]) or keyword in asset_data["spatial_anchor"]:
                    match_score += 1
                    
            if match_score > 0:
                results.append((match_score, asset_data))
                
        results.sort(key=lambda x: x[0], reverse=True)
        return [res[1] for res in results]

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    vault = S2AssetVault()
    vault.ingest_asset("FAMILY_PUBLIC", AssetType.AUDIO, "file:///nas/music.mp3", "客厅, 派对, 欢快", "Living_Room")
    res = vault.intent_based_search("D-OWNER-DH-001", "派对 欢快", AssetType.AUDIO)
    print(f"搜索结果: {res[0]['storage_uri'] if res else 'None'}")

    # ==============================================================================
# ⚠️ LEGAL WARNING & DUAL-LICENSING NOTICE / 法律与双重授权声明
# Copyright (c) 2026 Miles Xiang (Space2.world). All rights reserved.
# ==============================================================================
# [ ENGLISH ]
# This file is a core "Dark Matter" asset of the S2 Space Agent OS.
# It is licensed STRICTLY for personal study, code review, and non-commercial 
# open-source exploration. 
# 
# Without explicit written consent from the original author (Miles Xiang), 
# it is STRICTLY PROHIBITED to use these algorithms (including but not limited 
# to the Silicon Three Laws, Chronos Memory Array, and State Validator ) for ANY 
# commercial monetization, closed-source product integration, hardware pre-installation, 
# or enterprise-level B2B deployment. Violators will face severe intellectual 
# property prosecution.
# 
# For S2 Pro Enterprise Commercial Licenses, please contact the author.
# 
# ------------------------------------------------------------------------------
# [ 简体中文 ]
# 本文件属于 S2 Space Agent OS 的核心“暗物质”资产。
# 仅供个人学习、代码审查与非商业性质的开源探索使用。
# 
# 未经原作者 (Miles Xiang) 明确的书面授权，严禁将本算法（包括但不限于
# 《硅基三定律》、时空全息记忆阵列、虚拟防篡改防火墙等）用于任何形式的
# 商业变现、闭源产品集成、硬件预装或企业级 B2B 部署。违者必将面临极其
# 严厉的知识产权追责。
# 
# 如需获取 S2 Pro 企业级商用授权，请联系原作者洽谈。
# ==============================================================================