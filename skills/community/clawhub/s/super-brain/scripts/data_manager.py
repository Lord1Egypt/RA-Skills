#!/usr/bin/env python3
"""
超脑数据管理脚本
自动清理、归档、优化数据库
"""

import sqlite3
import json
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path.home() / '.openclaw' / 'super-brain.db'
ARCHIVE_PATH = Path.home() / '.openclaw' / 'super-brain-archive'

# 默认保留天数
DEFAULT_RETENTION_DAYS = {
    'conversation_insights': 90,
    'response_patterns': 180,
    'agent_outputs': 30,
    'agent_collaboration_log': 60,
    'self_evolution_log': 365,
    'performance_metrics': 90,
    'data_access_log': 30
}


class DataManager:
    """数据管理器"""
    
    def __init__(self, user_id=None):
        self.user_id = user_id
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        
    def get_db_size(self):
        """获取数据库大小"""
        return DB_PATH.stat().st_size / 1024  # KB
    
    def get_table_stats(self):
        """获取表统计信息"""
        cursor = self.conn.cursor()
        stats = {}
        
        tables = [
            'conversation_insights', 'response_patterns', 
            'agent_outputs', 'self_evolution_log',
            'knowledge_gaps', 'performance_metrics'
        ]
        
        for table in tables:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                count = cursor.fetchone()[0]
                
                # 获取表大小估算
                cursor.execute(f'''
                    SELECT SUM(pgsize) / 1024 as size_kb
                    FROM dbstat
                    WHERE name = ?
                ''', [table])
                size = cursor.fetchone()[0] or 0
                
                stats[table] = {
                    'rows': count,
                    'size_kb': size
                }
            except:
                stats[table] = {'rows': 0, 'size_kb': 0}
        
        return stats
    
    def cleanup_old_data(self, retention_days=None):
        """清理过期数据"""
        retention = retention_days or DEFAULT_RETENTION_DAYS
        cursor = self.conn.cursor()
        
        cleaned = {}
        
        # 清理对话洞察
        try:
            days = retention.get('conversation_insights', 90)
            cutoff = datetime.now() - timedelta(days=days)
            cursor.execute('''
                DELETE FROM conversation_insights 
                WHERE timestamp < ? AND user_id = ?
            ''', [cutoff.isoformat(), self.user_id])
            cleaned['conversation_insights'] = cursor.rowcount
        except:
            cleaned['conversation_insights'] = 0
        
        # 清理响应模式
        try:
            days = retention.get('response_patterns', 180)
            cutoff = datetime.now() - timedelta(days=days)
            cursor.execute('''
                DELETE FROM response_patterns 
                WHERE timestamp < ? AND user_id = ?
            ''', [cutoff.isoformat(), self.user_id])
            cleaned['response_patterns'] = cursor.rowcount
        except:
            cleaned['response_patterns'] = 0
        
        # 清理代理输出
        try:
            days = retention.get('agent_outputs', 30)
            cutoff = datetime.now() - timedelta(days=days)
            cursor.execute('''
                DELETE FROM agent_outputs 
                WHERE timestamp < ?
            ''', [cutoff.isoformat()])
            cleaned['agent_outputs'] = cursor.rowcount
        except:
            cleaned['agent_outputs'] = 0
        
        # 清理性能指标
        try:
            days = retention.get('performance_metrics', 90)
            cutoff = datetime.now() - timedelta(days=days)
            cursor.execute('''
                DELETE FROM performance_metrics 
                WHERE timestamp < ? AND user_id = ?
            ''', [cutoff.isoformat(), self.user_id])
            cleaned['performance_metrics'] = cursor.rowcount
        except:
            cleaned['performance_metrics'] = 0
        
        # 清理访问日志
        try:
            days = retention.get('data_access_log', 30)
            cutoff = datetime.now() - timedelta(days=days)
            cursor.execute('''
                DELETE FROM data_access_log 
                WHERE timestamp < ?
            ''', [cutoff.isoformat()])
            cleaned['data_access_log'] = cursor.rowcount
        except:
            cleaned['data_access_log'] = 0
        
        self.conn.commit()
        
        return cleaned
    
    def archive_old_data(self, days=90):
        """归档旧数据到压缩文件"""
        ARCHIVE_PATH.mkdir(exist_ok=True)
        
        cursor = self.conn.cursor()
        cutoff = datetime.now() - timedelta(days=days)
        
        archived = {}
        
        # 只归档有timestamp字段的表
        try:
            cursor.execute('''
                SELECT * FROM conversation_insights
                WHERE timestamp < ? AND user_id = ?
            ''', [cutoff.isoformat(), self.user_id])
            
            rows = cursor.fetchall()
            
            if rows:
                data = [dict(row) for row in rows]
                archive_file = ARCHIVE_PATH / f'conversation_insights_{datetime.now().strftime("%Y%m%d")}.json.gz'
                
                with gzip.open(archive_file, 'wt', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                archived['conversation_insights'] = {
                    'rows': len(rows),
                    'file': str(archive_file)
                }
        except Exception as e:
            print(f'   ⚠️ 归档失败: {e}')
        
        return archived
    
    def vacuum_database(self):
        """优化数据库（VACUUM）"""
        # VACUUM需要独占连接
        self.conn.close()
        
        conn = sqlite3.connect(DB_PATH)
        conn.execute('VACUUM')
        conn.close()
        
        # 重新连接
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        
        return True
    
    def optimize_database(self):
        """优化数据库"""
        cursor = self.conn.cursor()
        
        # 重建索引
        indexes = [
            'idx_insights_user', 'idx_insights_session',
            'idx_patterns_user', 'idx_agent_tasks_main'
        ]
        
        for idx in indexes:
            try:
                cursor.execute(f'REINDEX {idx}')
            except:
                pass
        
        # 分析统计信息
        cursor.execute('ANALYZE')
        
        self.conn.commit()
        
        return True
    
    def get_cleanup_preview(self, retention_days=None):
        """预览清理效果"""
        retention = retention_days or DEFAULT_RETENTION_DAYS
        cursor = self.conn.cursor()
        
        preview = {}
        
        # 预览对话洞察
        try:
            days = retention.get('conversation_insights', 90)
            cutoff = datetime.now() - timedelta(days=days)
            cursor.execute('''
                SELECT COUNT(*) FROM conversation_insights 
                WHERE timestamp < ? AND user_id = ?
            ''', [cutoff.isoformat(), self.user_id])
            preview['conversation_insights'] = cursor.fetchone()[0]
        except:
            preview['conversation_insights'] = 0
        
        # 预览响应模式
        try:
            days = retention.get('response_patterns', 180)
            cutoff = datetime.now() - timedelta(days=days)
            cursor.execute('''
                SELECT COUNT(*) FROM response_patterns 
                WHERE timestamp < ? AND user_id = ?
            ''', [cutoff.isoformat(), self.user_id])
            preview['response_patterns'] = cursor.fetchone()[0]
        except:
            preview['response_patterns'] = 0
        
        return preview
    
    def close(self):
        """关闭连接"""
        self.conn.close()


def auto_maintenance(user_id, retention_days=None):
    """自动维护（清理+归档+优化）"""
    manager = DataManager(user_id)
    
    print('🔧 超脑数据维护')
    print('=' * 50)
    
    # 1. 显示当前状态
    size_before = manager.get_db_size()
    stats_before = manager.get_table_stats()
    
    print(f'\n📊 维护前:')
    print(f'   数据库大小: {size_before:.2f} KB')
    total_rows = sum(s['rows'] for s in stats_before.values())
    print(f'   总数据量: {total_rows} 行')
    
    # 2. 预览清理
    preview = manager.get_cleanup_preview(retention_days)
    print(f'\n🔍 将要清理:')
    for table, count in preview.items():
        if count > 0:
            print(f'   {table}: {count} 条')
    
    # 3. 执行清理
    print(f'\n🗑️ 执行清理...')
    cleaned = manager.cleanup_old_data(retention_days)
    total_cleaned = sum(cleaned.values())
    print(f'   已清理: {total_cleaned} 条记录')
    
    # 4. 归档旧数据
    print(f'\n📦 归档旧数据...')
    archived = manager.archive_old_data()
    if archived:
        for table, info in archived.items():
            print(f'   {table}: {info["rows"]} 条 → {info["file"]}')
    else:
        print('   无需归档')
    
    # 5. 优化数据库
    print(f'\n⚡ 优化数据库...')
    manager.optimize_database()
    manager.vacuum_database()
    print('   ✓ VACUUM完成')
    print('   ✓ 索引重建完成')
    
    # 6. 显示结果
    size_after = manager.get_db_size()
    stats_after = manager.get_table_stats()
    
    print(f'\n✅ 维护完成:')
    print(f'   数据库大小: {size_after:.2f} KB (减少 {size_before-size_after:.2f} KB)')
    total_rows_after = sum(s['rows'] for s in stats_after.values())
    print(f'   总数据量: {total_rows_after} 行 (清理 {total_rows-total_rows_after} 行)')
    
    manager.close()
    
    return {
        'cleaned': total_cleaned,
        'archived': len(archived),
        'size_before': size_before,
        'size_after': size_after
    }


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print('用法:')
        print('  维护: python data_manager.py <user_id>')
        print('  统计: python data_manager.py <user_id> stats')
        print('  预览: python data_manager.py <user_id> preview')
        sys.exit(1)
    
    user_id = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else 'maintain'
    
    if action == 'stats':
        manager = DataManager(user_id)
        stats = manager.get_table_stats()
        size = manager.get_db_size()
        
        print(f'📊 数据库统计:')
        print(f'   大小: {size:.2f} KB')
        for table, info in stats.items():
            print(f'   {table}: {info["rows"]} 行, {info["size_kb"]:.2f} KB')
        
        manager.close()
        
    elif action == 'preview':
        manager = DataManager(user_id)
        preview = manager.get_cleanup_preview()
        
        print(f'🔍 清理预览:')
        for table, count in preview.items():
            print(f'   {table}: {count} 条将被清理')
        
        manager.close()
        
    else:
        # 执行完整维护
        auto_maintenance(user_id)
