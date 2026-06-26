#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Learning Manager - 学习记录管理模块

管理 .learnings/ 目录下的学习记录，支持:
- 学习条目创建 (LRN/ERR/FEAT)
- ID 生成
- 优先级/状态管理
- Pattern-Key 追踪
- 提升到项目文件
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


class LearningIDGenerator:
    """学习条目 ID 生成器"""
    
    @staticmethod
    def generate(entry_type: str, date: Optional[datetime] = None) -> str:
        """
        生成学习条目 ID
        
        Args:
            entry_type: LRN | ERR | FEAT
            date: 日期 (默认今天)
        
        Returns:
            ID 字符串，如 LRN-20250115-001
        """
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime('%Y%m%d')
        seq = LearningIDGenerator._get_sequence(entry_type, date_str)
        return f"{entry_type}-{date_str}-{seq:03d}"
    
    @staticmethod
    def _get_sequence(entry_type: str, date_str: str) -> int:
        """获取今日序列号"""
        # 这里简化实现，实际应该读取文件统计
        return 1


class LearningEntry:
    """学习条目类"""
    
    def __init__(self, entry_id: str, category: str = '', priority: str = 'medium', 
                 status: str = 'pending', area: str = 'config'):
        self.entry_id = entry_id
        self.category = category
        self.priority = priority
        self.status = status
        self.area = area
        self.logged_at = datetime.now().isoformat()
        self.summary = ''
        self.details = ''
        self.suggested_action = ''
        self.metadata: Dict[str, Any] = {
            'Source': 'conversation',
            'Related Files': [],
            'Tags': [],
            'See Also': [],
            'Pattern-Key': None,
            'Recurrence-Count': 1,
            'First-Seen': self.logged_at[:10],
            'Last-Seen': self.logged_at[:10]
        }
        self.resolution: Optional[Dict] = None
    
    def to_markdown(self) -> str:
        """转换为 Markdown 格式"""
        md = f"## [{self.entry_id}] {self.category}\n\n"
        md += f"**Logged**: {self.logged_at}\n"
        md += f"**Priority**: {self.priority}\n"
        md += f"**Status**: {self.status}\n"
        md += f"**Area**: {self.area}\n\n"
        
        if self.summary:
            md += f"### Summary\n{self.summary}\n\n"
        
        if self.details:
            md += f"### Details\n{self.details}\n\n"
        
        if self.suggested_action:
            md += f"### Suggested Action\n{self.suggested_action}\n\n"
        
        md += "### Metadata\n"
        for key, value in self.metadata.items():
            if value is not None:
                if isinstance(value, list):
                    md += f"- {key}: {', '.join(value) if value else 'none'}\n"
                else:
                    md += f"- {key}: {value}\n"
        
        if self.resolution:
            md += "\n### Resolution\n"
            md += f"- **Resolved**: {self.resolution.get('resolved_at', 'N/A')}\n"
            md += f"- **Commit/PR**: {self.resolution.get('commit', 'N/A')}\n"
            md += f"- **Notes**: {self.resolution.get('notes', 'N/A')}\n"
        
        md += "\n---\n\n"
        return md
    
    @classmethod
    def from_markdown(cls, content: str) -> Optional['LearningEntry']:
        """从 Markdown 解析条目"""
        # 解析 ID 和分类
        match = re.search(r'## \[([A-Z]+-\d+-\w+)\]\s+(\w+)', content)
        if not match:
            return None
        
        entry = cls(match.group(1), match.group(2))
        
        # 解析元数据
        for pattern, attr in [
            (r'\*\*Logged\*\*:\s*(.+)', 'logged_at'),
            (r'\*\*Priority\*\*:\s*(\w+)', 'priority'),
            (r'\*\*Status\*\*:\s*(\w+)', 'status'),
            (r'\*\*Area\*\*:\s*(\w+)', 'area'),
        ]:
            m = re.search(pattern, content)
            if m:
                setattr(entry, attr, m.group(1).strip())
        
        # 解析内容块
        for block, attr in [
            (r'### Summary\n(.+?)(?=###|$)', 'summary'),
            (r'### Details\n(.+?)(?=###|$)', 'details'),
            (r'### Suggested Action\n(.+?)(?=###|$)', 'suggested_action'),
        ]:
            m = re.search(block, content, re.DOTALL)
            if m:
                setattr(entry, attr, m.group(1).strip())
        
        return entry


class LearningManager:
    """学习记录管理器"""
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.learnings_dir = workspace / '.learnings'
        self.learnings_file = self.learnings_dir / 'LEARNINGS.md'
        self.errors_file = self.learnings_dir / 'ERRORS.md'
        self.features_file = self.learnings_dir / 'FEATURE_REQUESTS.md'
    
    def ensure_dirs(self):
        """确保目录存在"""
        self.learnings_dir.mkdir(parents=True, exist_ok=True)
        
        # 如果文件不存在，创建模板
        for file_path, template in [
            (self.learnings_file, self._get_learnings_template()),
            (self.errors_file, self._get_errors_template()),
            (self.features_file, self._get_features_template()),
        ]:
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(template)
    
    def _get_learnings_template(self) -> str:
        return """# 🧠 学习记录 (LEARNINGS.md)

记录纠正、知识缺口、最佳实践。

## 条目格式

```markdown
## [LRN-YYYYMMDD-XXX] category
**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | in_progress | resolved | promoted | wont_fix
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description

### Details
Full context

### Suggested Action
Specific fix

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- See Also: LRN-XXXX-XXX
- Pattern-Key: stable.key (optional)

---
```

---

*暂无学习记录*
"""
    
    def _get_errors_template(self) -> str:
        return """# ⚠️ 错误记录 (ERRORS.md)

记录命令失败、异常、意外行为。

---

*暂无错误记录*
"""
    
    def _get_features_template(self) -> str:
        return """# 💡 功能请求 (FEATURE_REQUESTS.md)

记录用户请求的新功能或能力。

---

*暂无功能请求*
"""
    
    def add_learning(self, category: str, summary: str, details: str = '',
                     priority: str = 'medium', area: str = 'config',
                     source: str = 'conversation', related_files: List[str] = None,
                     pattern_key: str = None) -> str:
        """
        添加学习记录
        
        Returns:
            生成的条目 ID
        """
        self.ensure_dirs()
        
        entry_id = LearningIDGenerator.generate('LRN')
        entry = LearningEntry(entry_id, category, priority, 'pending', area)
        entry.summary = summary
        entry.details = details
        entry.suggested_action = ''
        entry.metadata['Source'] = source
        entry.metadata['Related Files'] = related_files or []
        entry.metadata['Pattern-Key'] = pattern_key
        
        # 检查是否有相似的 Pattern-Key (重复检测)
        if pattern_key:
            existing = self.find_by_pattern_key(pattern_key)
            if existing:
                entry.metadata['See Also'] = [e['id'] for e in existing]
                entry.metadata['Recurrence-Count'] = len(existing) + 1
        
        # 追加到文件
        with open(self.learnings_file, 'a', encoding='utf-8') as f:
            f.write(entry.to_markdown())
        
        return entry_id
    
    def add_error(self, command: str, error_msg: str, context: str = '',
                  priority: str = 'high', area: str = 'config',
                  reproducible: str = 'unknown') -> str:
        """添加错误记录"""
        self.ensure_dirs()
        
        entry_id = LearningIDGenerator.generate('ERR')
        
        content = f"""## [{entry_id}] {command}
**Logged**: {datetime.now().isoformat()}
**Priority**: {priority}
**Status**: pending
**Area**: {area}

### Summary
Command execution failed

### Error
```
{error_msg}
```

### Context
{context}

### Suggested Fix
TBD

### Metadata
- Reproducible: {reproducible}

---

"""
        
        with open(self.errors_file, 'a', encoding='utf-8') as f:
            f.write(content)
        
        return entry_id
    
    def add_feature_request(self, capability: str, user_context: str = '',
                            complexity: str = 'medium', priority: str = 'medium') -> str:
        """添加功能请求"""
        self.ensure_dirs()
        
        entry_id = LearningIDGenerator.generate('FEAT')
        
        content = f"""## [{entry_id}] {capability}
**Logged**: {datetime.now().isoformat()}
**Priority**: {priority}
**Status**: pending
**Area**: config

### Requested Capability
{capability}

### User Context
{user_context}

### Complexity Estimate
{complexity}

### Suggested Implementation
TBD

### Metadata
- Frequency: first_time

---

"""
        
        with open(self.features_file, 'a', encoding='utf-8') as f:
            f.write(content)
        
        return entry_id
    
    def find_by_pattern_key(self, pattern_key: str) -> List[Dict]:
        """根据 Pattern-Key 查找相似条目"""
        if not self.learnings_file.exists():
            return []
        
        with open(self.learnings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = []
        for match in re.finditer(r'## \[(LRN-\d+-\w+)\].*?- Pattern-Key:\s*' + re.escape(pattern_key), 
                                  content, re.DOTALL):
            results.append({'id': match.group(1), 'content': match.group(0)[:500]})
        
        return results
    
    def promote_to_file(self, entry_id: str, target_file: str, content: str, 
                       section: str = None) -> bool:
        """
        将学习记录提升到项目文件
        
        Args:
            entry_id: 条目 ID
            target_file: 目标文件 (SOUL.md, AGENTS.md, TOOLS.md 等)
            content: 提升后的内容 (简洁版本)
            section: 目标章节 (可选)
        
        Returns:
            是否成功
        """
        target_path = self.workspace / target_file
        if not target_path.exists():
            print(f"⚠️ 目标文件不存在：{target_path}")
            return False
        
        with open(target_path, 'r', encoding='utf-8') as f:
            current = f.read()
        
        # 如果指定了 section，插入到该章节下
        if section:
            section_marker = f"## {section}"
            if section_marker in current:
                parts = current.split(section_marker)
                parts[1] = f"\n{content}\n" + parts[1]
                current = section_marker.join(parts)
            else:
                current += f"\n\n{section_marker}\n\n{content}\n"
        else:
            current += f"\n\n{content}\n"
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(current)
        
        # 更新原条目状态为 promoted
        self._update_entry_status(entry_id, 'promoted', {
            'target': target_file,
            'promoted_at': datetime.now().isoformat()
        })
        
        return True
    
    def _update_entry_status(self, entry_id: str, new_status: str, 
                            resolution: Dict = None):
        """更新条目状态"""
        if not self.learnings_file.exists():
            return
        
        with open(self.learnings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到条目并更新状态
        pattern = rf'(## \[{re.escape(entry_id)}\].*?\*\*Status\*\*:\s*)(\w+)'
        content = re.sub(pattern, f'\\g<1>{new_status}', content, flags=re.DOTALL)
        
        # 添加 resolution
        if resolution:
            res_content = f"\n### Resolution\n"
            for key, value in resolution.items():
                res_content += f"- **{key.replace('_', ' ').title()}**: {value}\n"
            
            # 在 Metadata 前插入
            content = content.replace('### Metadata', res_content + '\n### Metadata', 1)
        
        with open(self.learnings_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def get_pending_high_priority(self) -> List[Dict]:
        """获取所有待处理的高优先级条目"""
        if not self.learnings_file.exists():
            return []
        
        with open(self.learnings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = []
        # 查找高优先级且待处理的条目
        pattern = r'## \[(\w+-\d+-\w+)\]\s+(\w+).*?\*\*Priority\*\*:\s*(high|critical).*?\*\*Status\*\*:\s*pending'
        for match in re.finditer(pattern, content, re.DOTALL):
            results.append({
                'id': match.group(1),
                'category': match.group(2),
                'priority': match.group(3),
                'content': match.group(0)[:300]
            })
        
        return results
    
    def check_recurring_patterns(self) -> List[Dict]:
        """检查重复出现的模式 (Recurrence-Count >= 3)"""
        if not self.learnings_file.exists():
            return []
        
        with open(self.learnings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = []
        pattern = r'## \[(\w+-\d+-\w+)\].*?- Recurrence-Count:\s*(\d+).*?- Pattern-Key:\s*(\S+)'
        for match in re.finditer(pattern, content, re.DOTALL):
            count = int(match.group(2))
            if count >= 3:
                results.append({
                    'id': match.group(1),
                    'recurrence_count': count,
                    'pattern_key': match.group(3),
                    'should_promote': True
                })
        
        return results
