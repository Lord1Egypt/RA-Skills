#!/usr/bin/env python3
"""
Vector System Optimizer - 向量体系全面调优
基于系统架构进行深度优化
"""

import json
import os
import subprocess
import shlex
import struct
import urllib.request
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

# 路径配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_TDDB = Path.home() / ".openclaw" / "memory-tdai"
VECTORS_DB = MEMORY_TDDB / "vectors.db"
VEC_EXT = "/home/tiamo/.openclaw/extensions/memory-tencentdb/node_modules/sqlite-vec-linux-x64/vec0"
# Removed: OPENCLAW_JSON

# API 配置 - 从环境变量读取
GITEE_API = "https://ai.gitee.com/v1/embeddings"
GITEE_KEY = os.environ.get("GITEE_AI_KEY", "")


class VectorSystemOptimizer:
    """向量体系优化器"""
    
    def __init__(self):
        self.stats = {
            "l1_records": 0,
            "l1_vectors": 0,
            "l0_conversations": 0,
            "l0_vectors": 0,
            "missing_l1": 0,
            "missing_l0": 0,
            "zero_vectors": 0,
            "orphan_vectors": 0
        }
    
    def analyze(self):
        """分析向量体系状态"""
        print("=" * 60)
        print("向量体系分析")
        print("=" * 60)
        
        # 1. 基础统计
        print("\n📊 基础统计:")
        self._collect_stats()
        print(f"  L1 记录: {self.stats['l1_records']} 条")
        print(f"  L1 向量: {self.stats['l1_vectors']} 条")
        print(f"  L0 对话: {self.stats['l0_conversations']} 条")
        print(f"  L0 向量: {self.stats['l0_vectors']} 条")
        
        # 2. 覆盖率分析
        print("\n📈 覆盖率分析:")
        l1_coverage = 100.0 * self.stats['l1_vectors'] / max(self.stats['l1_records'], 1)
        l0_coverage = 100.0 * self.stats['l0_vectors'] / max(self.stats['l0_conversations'], 1)
        print(f"  L1 覆盖率: {l1_coverage:.1f}%")
        print(f"  L0 覆盖率: {l0_coverage:.1f}%")
        
        # 3. 问题检测
        print("\n🔍 问题检测:")
        self._detect_issues()
        
        if self.stats['missing_l1'] > 0:
            print(f"  ⚠️ L1 缺失向量: {self.stats['missing_l1']} 条")
        if self.stats['missing_l0'] > 0:
            print(f"  ⚠️ L0 缺失向量: {self.stats['missing_l0']} 条")
        if self.stats['zero_vectors'] > 0:
            print(f"  ⚠️ 零向量: {self.stats['zero_vectors']} 条")
        if self.stats['orphan_vectors'] > 0:
            print(f"  ⚠️ 孤立向量: {self.stats['orphan_vectors']} 条")
        
        if all(v == 0 for k, v in self.stats.items() if k.startswith('missing') or k.startswith('zero') or k.startswith('orphan')):
            print("  ✅ 未发现问题")
        
        return self.stats
    
    def _collect_stats(self):
        """收集统计数据"""
        # 使用 sqlite3 命令行（直接数据库查询）
        conn = sqlite3.connect(str(VECTORS_DB))
        c = conn.cursor()
        try:
            c.execute("SELECT COUNT(*) FROM l1_records")
            self.stats['l1_records'] = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM l1_vec")
            self.stats['l1_vectors'] = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM l0_conversations")
            self.stats['l0_conversations'] = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM l0_vec")
            self.stats['l0_vectors'] = c.fetchone()[0]
        except Exception as e:
            print(f"  统计查询失败: {e}")
        finally:
            conn.close()
    
    def _detect_issues(self):
        """检测问题（使用直接sqlite3连接）"""
        conn = sqlite3.connect(str(VECTORS_DB))
        c = conn.cursor()
        try:
            # 检测缺失向量
            c.execute("SELECT COUNT(*) FROM l1_records WHERE record_id NOT IN (SELECT record_id FROM l1_vec)")
            self.stats['missing_l1'] = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM l0_conversations WHERE record_id NOT IN (SELECT record_id FROM l0_vec)")
            self.stats['missing_l0'] = c.fetchone()[0]
            
            # 检测零向量
            c.execute("SELECT COUNT(*) FROM l1_vec WHERE distance IS NULL OR distance = 0")
            self.stats['zero_vectors'] = c.fetchone()[0]
            
            # 检测孤立向量
            c.execute("SELECT COUNT(*) FROM l1_vec WHERE record_id NOT IN (SELECT record_id FROM l1_records)")
            self.stats['orphan_vectors'] = c.fetchone()[0]
        except Exception as e:
            print(f"  问题检测失败: {e}")
        finally:
            conn.close()
    
    def fix_missing_vectors(self, batch_size: int = 10):
        """修复缺失的向量（使用直接sqlite3连接）"""
        print("\n🔧 修复缺失向量:")
        
        # 获取缺失向量的 L1 记录
        conn = sqlite3.connect(str(VECTORS_DB))
        c = conn.cursor()
        try:
            c.execute("""
                SELECT r.record_id, r.content, r.updated_time 
                FROM l1_records r 
                WHERE r.record_id NOT IN (SELECT record_id FROM l1_vec)
                LIMIT 100
            """)
            records = c.fetchall()
        except Exception as e:
            print(f"  查询失败: {e}")
            conn.close()
            return
        conn.close()
        
        if not records:
            print("  ✅ L1 无缺失向量")
            return
        
        print(f"  发现 {len(records)} 条 L1 记录缺失向量")
        
        # 批量生成向量
        fixed = 0
        for i, record in enumerate(records):
            record_id, content, updated_time = record
            print(f"  [{i+1}/{len(records)}] 处理: {record_id[:30]}...")
            
            # 获取向量
            embedding = self._get_embedding(content)
            if embedding:
                # 写入数据库
                if self._write_vector(record_id, embedding, updated_time):
                    fixed += 1
                    print(f"    ✅ 向量写入成功")
                else:
                    print(f"    ❌ 向量写入失败")
            else:
                print(f"    ❌ 向量生成失败")
        
        print(f"\n  修复完成: {fixed}/{len(records)}")
    
    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """获取向量"""
        data = json.dumps({
            "input": text,
            "model": "Qwen3-Embedding-8B",
            "dimensions": 4096
        }).encode('utf-8')
        
        req = urllib.request.Request(
            GITEE_API,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GITEE_KEY}"
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                return result['data'][0]['embedding']
        except Exception as e:
            print(f"    API 错误: {e}")
            return None
    
    def _write_vector(self, record_id: str, embedding: List[float], updated_time: str) -> bool:
        """写入向量（使用直接sqlite3连接）"""
        vec_hex = struct.pack(f'{len(embedding)}f', *embedding).hex()
        
        conn = sqlite3.connect(str(VECTORS_DB))
        c = conn.cursor()
        try:
            c.execute("DELETE FROM l1_vec WHERE record_id = ?", (record_id,))
            c.execute("INSERT INTO l1_vec (record_id, embedding, updated_time) VALUES (?, X?, ?)", 
                     (record_id, vec_hex, updated_time))
            conn.commit()
            return True
        except Exception as e:
            print(f"    写入失败: {e}")
            return False
        finally:
            conn.close()
    
    def rebuild_fts_index(self):
        """重建 FTS 索引（使用直接sqlite3连接）"""
        print("\n🔧 重建 FTS 索引:")
        
        conn = sqlite3.connect(str(VECTORS_DB))
        c = conn.cursor()
        try:
            c.execute("SELECT COUNT(*) FROM l1_fts")
            fts_count = c.fetchone()[0]
            print(f"  FTS 索引记录: {fts_count} 条")
            
            if fts_count != self.stats['l1_records']:
                print(f"  ⚠️ FTS 记录数与 L1 记录数不一致")
                print(f"  建议重建 FTS 索引")
            else:
                print(f"  ✅ FTS 索引正常")
        except Exception as e:
            print(f"  查询失败: {e}")
        finally:
            conn.close()
    
    def optimize_database(self):
        """优化数据库（使用直接sqlite3连接）"""
        print("\n🔧 优化数据库:")
        
        conn = sqlite3.connect(str(VECTORS_DB))
        try:
            # VACUUM
            print("  执行 VACUUM...")
            conn.execute("VACUUM")
            print("  ✅ VACUUM 完成")
            
            # ANALYZE
            print("  执行 ANALYZE...")
            conn.execute("ANALYZE")
            print("  ✅ ANALYZE 完成")
        except Exception as e:
            print(f"  ⚠️ 优化失败: {e}")
        finally:
            conn.close()
        
        # 检查数据库大小
        db_size = VECTORS_DB.stat().st_size / (1024 * 1024)
        print(f"\n  数据库大小: {db_size:.2f} MB")
    
    def update_config(self):
        """更新配置"""
        print("\n📝 检查配置:")
        
        try:
            with open(OPENCLAW_JSON) as f:
                data = json.load(f)
            
            config = data.get('plugins', {}).get('entries', {}).get('memory-tencentdb', {}).get('config', {})
            
            # 检查 embedding 配置
            emb = config.get('embedding', {})
            if emb.get('dimensions') != 4096:
                print(f"  ⚠️ 向量维度配置: {emb.get('dimensions')} (应为 4096)")
            else:
                print(f"  ✅ 向量维度: 4096")
            
            # 检查 pipeline 配置
            pipeline = config.get('pipeline', {})
            print(f"  Pipeline 配置:")
            print(f"    everyNConversations: {pipeline.get('everyNConversations', 'N/A')}")
            print(f"    l1IdleTimeoutSeconds: {pipeline.get('l1IdleTimeoutSeconds', 'N/A')}")
            print(f"    maxMemoriesPerSession: {config.get('extraction', {}).get('maxMemoriesPerSession', 'N/A')}")
            
        except Exception as e:
            print(f"  ❌ 配置读取失败: {e}")
    
    def generate_report(self):
        """生成报告"""
        print("\n" + "=" * 60)
        print("优化报告")
        print("=" * 60)
        
        print(f"""
📊 向量体系状态
  L1 记录: {self.stats['l1_records']} 条
  L1 向量: {self.stats['l1_vectors']} 条
  L1 覆盖率: {100.0 * self.stats['l1_vectors'] / max(self.stats['l1_records'], 1):.1f}%
  
  L0 对话: {self.stats['l0_conversations']} 条
  L0 向量: {self.stats['l0_vectors']} 条
  L0 覆盖率: {100.0 * self.stats['l0_vectors'] / max(self.stats['l0_conversations'], 1):.1f}%

🔍 问题统计
  缺失 L1 向量: {self.stats['missing_l1']} 条
  缺失 L0 向量: {self.stats['missing_l0']} 条
  零向量: {self.stats['zero_vectors']} 条
  孤立向量: {self.stats['orphan_vectors']} 条

✅ 优化建议
  1. L0 向量覆盖率 {100.0 * self.stats['l0_vectors'] / max(self.stats['l0_conversations'], 1):.1f}%，建议补充历史对话向量
  2. 定期执行 VACUUM 和 ANALYZE 优化数据库
  3. 监控向量 API 调用频率，避免超限
""")


def main():
    """主函数"""
    print("=" * 60)
    print("向量体系全面调优")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    optimizer = VectorSystemOptimizer()
    
    # 1. 分析
    optimizer.analyze()
    
    # 2. 修复缺失向量
    if optimizer.stats['missing_l1'] > 0:
        optimizer.fix_missing_vectors()
    
    # 3. 重建 FTS 索引
    optimizer.rebuild_fts_index()
    
    # 4. 优化数据库
    optimizer.optimize_database()
    
    # 5. 检查配置
    optimizer.update_config()
    
    # 6. 生成报告
    optimizer.generate_report()


if __name__ == "__main__":
    main()
