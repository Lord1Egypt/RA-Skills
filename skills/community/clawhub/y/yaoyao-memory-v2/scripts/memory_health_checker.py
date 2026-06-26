#!/usr/bin/env python3
"""
记忆健康检查器 - 深度检测系统健康状态

功能：
- 数据库完整性检查
- 向量一致性检查
- 数据一致性验证
- 性能衰退检测
- 存储空间分析
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class MemoryHealthChecker:
    """记忆健康检查器"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.memory_base = get_memory_base()
        self.conn = None
        self._connect()
    
    def _connect(self):
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def check_database_integrity(self) -> Dict:
        """检查数据库完整性"""
        issues = []
        
        # PRAGMA 检查
        cursor = self.conn.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        
        if result[0] != 'ok':
            issues.append({
                'severity': 'critical',
                'type': 'integrity_error',
                'message': f"数据库完整性错误: {result[0]}"
            })
        
        # 表存在性检查
        required_tables = ['l1_records', 'l0_conversations', 'embedding_meta']
        cursor = self.conn.execute("""
            SELECT name FROM sqlite_master WHERE type='table'
        """)
        existing_tables = {row['name'] for row in cursor.fetchall()}
        
        for table in required_tables:
            if table not in existing_tables:
                issues.append({
                    'severity': 'critical',
                    'type': 'missing_table',
                    'message': f"缺少必要表: {table}"
                })
        
        return {
            'status': 'ok' if not issues else 'error',
            'issues': issues,
            'tables_found': list(existing_tables)
        }
    
    def check_data_consistency(self) -> Dict:
        """检查数据一致性"""
        issues = []
        
        # 1. 无内容的记忆
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count FROM l1_records
            WHERE content IS NULL OR content = '' OR length(content) < 5
        """)
        empty_count = cursor.fetchone()['count']
        
        if empty_count > 0:
            issues.append({
                'severity': 'medium',
                'type': 'empty_content',
                'count': empty_count,
                'message': f"发现 {empty_count} 条内容为空或过短的记忆"
            })
        
        # 2. 无类型的记忆
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count FROM l1_records
            WHERE type IS NULL OR type = '' OR type = 'unknown'
        """)
        no_type_count = cursor.fetchone()['count']
        
        if no_type_count > 10:
            issues.append({
                'severity': 'low',
                'type': 'missing_type',
                'count': no_type_count,
                'message': f"发现 {no_type_count} 条缺少类型标记的记忆"
            })
        
        # 3. 异常优先级
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count FROM l1_records
            WHERE priority < 0 OR priority > 100 OR priority IS NULL
        """)
        bad_priority = cursor.fetchone()['count']
        
        if bad_priority > 0:
            issues.append({
                'severity': 'medium',
                'type': 'invalid_priority',
                'count': bad_priority,
                'message': f"发现 {bad_priority} 条优先级异常的记忆"
            })
        
        # 4. 重复记忆检测
        cursor = self.conn.execute("""
            SELECT content, COUNT(*) as count
            FROM l1_records
            WHERE content IS NOT NULL
            GROUP BY content
            HAVING count > 1
            LIMIT 10
        """)
        duplicates = cursor.fetchall()
        
        if duplicates:
            issues.append({
                'severity': 'low',
                'type': 'duplicate_content',
                'count': len(duplicates),
                'samples': [dict(row) for row in duplicates[:3]],
                'message': f"发现 {len(duplicates)} 组重复内容"
            })
        
        # 5. 孤立记忆（没有时间戳）
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count FROM l1_records
            WHERE created_time IS NULL OR created_time = ''
        """)
        orphan_count = cursor.fetchone()['count']
        
        if orphan_count > 0:
            issues.append({
                'severity': 'medium',
                'type': 'orphan_records',
                'count': orphan_count,
                'message': f"发现 {orphan_count} 条缺少时间戳的记忆"
            })
        
        return {
            'status': 'ok' if not issues else 'warning',
            'issues': issues,
            'total_checks': 5
        }
    
    def check_vector_consistency(self) -> Dict:
        """检查向量一致性"""
        issues = []
        
        try:
            # 检查向量表是否存在
            cursor = self.conn.execute("""
                SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%vec%'
            """)
            vec_tables = [row['name'] for row in cursor.fetchall()]
            
            if not vec_tables:
                issues.append({
                    'severity': 'medium',
                    'type': 'no_vector_tables',
                    'message': "未找到向量表，可能未启用向量功能"
                })
            
            # 检查向量记录数与记忆记录数一致性
            cursor = self.conn.execute("SELECT COUNT(*) as count FROM l1_records")
            memory_count = cursor.fetchone()['count']
            
            # 检查 l1_vec 表
            if 'l1_vec' in vec_tables:
                cursor = self.conn.execute("SELECT COUNT(*) as count FROM l1_vec")
                vec_count = cursor.fetchone()['count']
                
                if vec_count != memory_count:
                    issues.append({
                        'severity': 'low',
                        'type': 'vector_count_mismatch',
                        'memory_count': memory_count,
                        'vector_count': vec_count,
                        'message': f"记忆数({memory_count})与向量数({vec_count})不一致"
                    })
        except sqlite3.OperationalError as e:
            issues.append({
                'severity': 'low',
                'type': 'vector_check_error',
                'message': f"向量功能未启用: {str(e)[:50]}"
            })
        
        return {
            'status': 'ok' if not issues else 'warning',
            'issues': issues,
            'vector_tables': vec_tables if 'vec_tables' in dir() else []
        }
    
    def check_performance_degradation(self) -> Dict:
        """检测性能衰退"""
        issues = []
        
        # 1. 数据库膨胀检测
        db_path = Path(self.db_path)
        if db_path.exists():
            size_mb = db_path.stat().st_size / 1024 / 1024
            cursor = self.conn.execute("SELECT COUNT(*) as count FROM l1_records")
            record_count = cursor.fetchone()['count']
            
            if record_count > 0:
                avg_size_per_record = size_mb * 1024 / record_count
                
                # 正常应该 < 50KB/条
                if avg_size_per_record > 100:
                    issues.append({
                        'severity': 'medium',
                        'type': 'database_bloat',
                        'size_mb': round(size_mb, 2),
                        'avg_size_per_record_kb': round(avg_size_per_record, 2),
                        'message': f"数据库膨胀: {size_mb}MB, 平均{avg_size_per_record:.1f}KB/条(期望<50KB)"
                    })
        
        # 2. 索引效率检测
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count FROM l1_records
            WHERE created_time < datetime('now', '-30 days')
        """)
        old_records = cursor.fetchone()['count']
        
        if record_count > 0 and old_records > record_count * 0.5:
            issues.append({
                'severity': 'low',
                'type': 'old_records_ratio',
                'old_records': old_records,
                'total': record_count,
                'ratio': round(old_records / max(record_count, 1) * 100, 1),
                'message': f"30天前记录占 {old_records/record_count*100:.1f}%，可能需要归档"
            })
        
        return {
            'status': 'ok' if not issues else 'warning',
            'issues': issues
        }
    
    def check_storage_space(self) -> Dict:
        """检查存储空间"""
        issues = []
        
        db_path = Path(self.db_path)
        if db_path.exists():
            size_mb = db_path.stat().st_size / 1024 / 1024
            
            if size_mb > 100:
                issues.append({
                    'severity': 'high',
                    'type': 'large_database',
                    'size_mb': round(size_mb, 2),
                    'message': f"数据库超过 100MB，可能影响性能"
                })
            
            if size_mb > 500:
                issues.append({
                    'severity': 'critical',
                    'type': 'very_large_database',
                    'size_mb': round(size_mb, 2),
                    'message': f"数据库超过 500MB，性能会严重下降，建议归档或清理"
                })
        
        return {
            'status': 'ok' if not issues else 'warning',
            'issues': issues
        }
    
    def generate_health_report(self) -> str:
        """生成健康报告"""
        lines = ["# 🩺 记忆健康检查报告", ""]
        lines.append(f"**检查时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # 1. 数据库完整性
        lines.append("## 🗄️ 数据库完整性")
        integrity = self.check_database_integrity()
        status_emoji = "✅" if integrity['status'] == 'ok' else "❌"
        lines.append(f"{status_emoji} 状态：{integrity['status'].upper()}")
        if integrity['issues']:
            for issue in integrity['issues']:
                lines.append(f"- **{issue['type']}**: {issue['message']}")
        lines.append("")
        
        # 2. 数据一致性
        lines.append("## 🔍 数据一致性")
        consistency = self.check_data_consistency()
        status_emoji = "✅" if consistency['status'] == 'ok' else "⚠️"
        lines.append(f"{status_emoji} 状态：{consistency['status'].upper()}")
        if consistency['issues']:
            for issue in consistency['issues']:
                lines.append(f"- **{issue['type']}** ({issue['severity']}): {issue['message']}")
        lines.append("")
        
        # 3. 向量一致性
        lines.append("## 🔢 向量一致性")
        vectors = self.check_vector_consistency()
        status_emoji = "✅" if vectors['status'] == 'ok' else "⚠️"
        lines.append(f"{status_emoji} 状态：{vectors['status'].upper()}")
        if vectors['issues']:
            for issue in vectors['issues']:
                lines.append(f"- **{issue['type']}**: {issue['message']}")
        lines.append("")
        
        # 4. 性能衰退
        lines.append("## 📉 性能衰退检测")
        perf = self.check_performance_degradation()
        status_emoji = "✅" if perf['status'] == 'ok' else "⚠️"
        lines.append(f"{status_emoji} 状态：{perf['status'].upper()}")
        if perf['issues']:
            for issue in perf['issues']:
                lines.append(f"- **{issue['type']}** ({issue['severity']}): {issue['message']}")
        lines.append("")
        
        # 5. 存储空间
        lines.append("## 💾 存储空间")
        storage = self.check_storage_space()
        status_emoji = "✅" if storage['status'] == 'ok' else "⚠️"
        lines.append(f"{status_emoji} 状态：{storage['status'].upper()}")
        if storage['issues']:
            for issue in storage['issues']:
                lines.append(f"- **{issue['type']}** ({issue['severity']}): {issue['message']}")
        lines.append("")
        
        return "\n".join(lines)
    
    def close(self):
        if self.conn:
            self.conn.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='记忆健康检查')
    parser.add_argument('--full', '-f', action='store_true', help='完整报告')
    parser.add_argument('--integrity', '-i', action='store_true', help='完整性检查')
    parser.add_argument('--consistency', '-c', action='store_true', help='一致性检查')
    parser.add_argument('--performance', '-p', action='store_true', help='性能检查')
    args = parser.parse_args()
    
    checker = MemoryHealthChecker()
    
    if args.integrity:
        result = checker.check_database_integrity()
        print(f"# 🗄️ 数据库完整性: {result['status']}")
        for issue in result['issues']:
            print(f"- {issue['message']}")
    
    elif args.consistency:
        result = checker.check_data_consistency()
        print(f"# 🔍 数据一致性: {result['status']}")
        for issue in result['issues']:
            print(f"- {issue['message']}")
    
    elif args.performance:
        result = checker.check_performance_degradation()
        print(f"# 📉 性能衰退: {result['status']}")
        for issue in result['issues']:
            print(f"- {issue['message']}")
    
    else:
        print(checker.generate_health_report())
    
    checker.close()


if __name__ == '__main__':
    main()
