#!/usr/bin/env python3
"""
超脑伦理约束模块
确保AI行为符合伦理规范
"""

import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / '.openclaw' / 'super-brain.db'

# 默认伦理规则
DEFAULT_ETHICAL_RULES = [
    {
        'id': 'eth-privacy-001',
        'constraint_type': 'privacy',
        'rule_name': '敏感信息保护',
        'rule_description': '不存储、不传播用户的敏感信息（密码、身份证、银行卡等）',
        'trigger_condition': {'patterns': ['密码', '身份证', '银行卡', 'token', 'secret']},
        'required_action': {'action': 'filter', 'replace_with': '[已过滤]'},
        'severity': 'block'
    },
    {
        'id': 'eth-safety-001',
        'constraint_type': 'safety',
        'rule_name': '有害内容拦截',
        'rule_description': '不生成、不传播有害内容（暴力、歧视、非法）',
        'trigger_condition': {'patterns': ['暴力', '歧视', '非法']},
        'required_action': {'action': 'reject', 'message': '无法协助此类请求'},
        'severity': 'block'
    },
    {
        'id': 'eth-fairness-001',
        'constraint_type': 'fairness',
        'rule_name': '偏见纠正',
        'rule_description': '主动识别和纠正潜在的偏见',
        'trigger_condition': {'bias_indicators': ['所有', '总是', '从不']},
        'required_action': {'action': 'warn', 'suggest': '考虑使用更中性的表达'},
        'severity': 'warning'
    },
    {
        'id': 'eth-transparency-001',
        'constraint_type': 'transparency',
        'rule_name': '决策透明',
        'rule_description': '重要决策需要解释原因',
        'trigger_condition': {'decision_types': ['recommendation', 'action']},
        'required_action': {'action': 'explain', 'template': '我建议...因为...'},
        'severity': 'warning'
    },
    {
        'id': 'eth-autonomy-001',
        'constraint_type': 'autonomy',
        'rule_name': '用户自主',
        'rule_description': '用户可以随时查看、修改、删除自己的数据',
        'trigger_condition': {'user_actions': ['view', 'modify', 'delete']},
        'required_action': {'action': 'facilitate', 'response': '立即执行用户请求'},
        'severity': 'warning'
    }
]


class EthicalConstraintEngine:
    """伦理约束引擎"""
    
    def __init__(self):
        self.rules = DEFAULT_ETHICAL_RULES
        self.load_rules_from_db()
    
    def load_rules_from_db(self):
        """从数据库加载规则"""
        try:
            import sqlite3
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, constraint_type, rule_name, trigger_condition, 
                       required_action, severity
                FROM ethical_constraints
                WHERE enabled = 1
            ''')
            
            for row in cursor.fetchall():
                self.rules.append({
                    'id': row[0],
                    'constraint_type': row[1],
                    'rule_name': row[2],
                    'trigger_condition': json.loads(row[3]) if row[3] else {},
                    'required_action': json.loads(row[4]) if row[4] else {},
                    'severity': row[5]
                })
            
            conn.close()
        except:
            # 表不存在，使用默认规则
            pass
    
    def check_content(self, content, content_type='text'):
        """检查内容是否符合伦理约束"""
        violations = []
        
        for rule in self.rules:
            if self._matches_trigger(content, rule['trigger_condition']):
                violations.append({
                    'rule_id': rule['id'],
                    'rule_name': rule['rule_name'],
                    'severity': rule['severity'],
                    'action': rule['required_action']
                })
        
        return violations
    
    def _matches_trigger(self, content, trigger):
        """检查是否匹配触发条件"""
        if 'patterns' in trigger:
            for pattern in trigger['patterns']:
                if pattern in content:
                    return True
        return False
    
    def apply_constraint(self, content, violations):
        """应用约束规则"""
        if not violations:
            return content, []
        
        actions_taken = []
        
        for violation in violations:
            action = violation['action']
            
            if action.get('action') == 'filter':
                # 过滤敏感信息
                for pattern in violation['action'].get('patterns', []):
                    content = content.replace(pattern, action.get('replace_with', '[已过滤]'))
                actions_taken.append(f"已过滤敏感信息: {violation['rule_name']}")
            
            elif action.get('action') == 'reject':
                # 拒绝请求
                return None, [action.get('message', '请求被拒绝')]
            
            elif action.get('action') == 'warn':
                # 警告
                actions_taken.append(f"警告: {violation['rule_name']}")
        
        return content, actions_taken
    
    def log_decision(self, user_id, decision_type, context, reasoning, ethical_check):
        """记录决策过程（可解释性）"""
        try:
            import sqlite3
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO decision_traces 
                (id, user_id, decision_type, decision_context, 
                 reasoning, ethical_check, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', [
                f'decision-{datetime.now().strftime("%Y%m%d%H%M%S")}',
                user_id,
                decision_type,
                json.dumps(context, ensure_ascii=False),
                json.dumps(reasoning, ensure_ascii=False),
                json.dumps(ethical_check, ensure_ascii=False),
                datetime.now().isoformat()
            ])
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f'⚠️ 决策记录失败: {e}')
    
    def get_decision_trace(self, user_id, limit=10):
        """获取决策历史（可解释性）"""
        try:
            import sqlite3
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM decision_traces
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', [user_id, limit])
            
            traces = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return traces
        except:
            return []


def init_ethical_constraints():
    """初始化伦理约束规则"""
    import sqlite3
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 插入默认规则
    for rule in DEFAULT_ETHICAL_RULES:
        cursor.execute('''
            INSERT OR IGNORE INTO ethical_constraints
            (id, constraint_type, rule_name, rule_description,
             trigger_condition, required_action, severity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', [
            rule['id'],
            rule['constraint_type'],
            rule['rule_name'],
            rule['rule_description'],
            json.dumps(rule['trigger_condition'], ensure_ascii=False),
            json.dumps(rule['required_action'], ensure_ascii=False),
            rule['severity']
        ])
    
    conn.commit()
    conn.close()
    
    print('✅ 伦理约束规则已初始化')


if __name__ == '__main__':
    print('🛡️ 超脑伦理约束系统')
    print('=' * 50)
    
    engine = EthicalConstraintEngine()
    
    # 测试
    test_content = "我的密码是123456"
    violations = engine.check_content(test_content)
    
    print(f'\n测试内容: "{test_content}"')
    print(f'检测结果: {len(violations)} 个违规')
    
    if violations:
        filtered, actions = engine.apply_constraint(test_content, violations)
        print(f'处理后: "{filtered}"')
        print(f'执行动作: {actions}')
