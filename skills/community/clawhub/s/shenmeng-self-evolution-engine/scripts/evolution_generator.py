#!/usr/bin/env python3
"""
进化生成器 - 基于监控数据生成Skill改进方案

用法:
    # 分析并生成改进方案
    python evolution_generator.py --skill my-skill --analyze
    
    # 查看待审核的进化方案
    python evolution_generator.py --skill my-skill --list-pending
    
    # 应用进化方案（需人类确认）
    python evolution_generator.py --skill my-skill --apply --id evolution_001
"""

import argparse
import json
import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class EvolutionGenerator:
    """进化生成器"""
    
    def __init__(self, skill_name: str, workspace_dir: str = "/root/.openclaw/workspace/skills"):
        self.skill_name = skill_name
        self.skill_dir = Path(workspace_dir) / skill_name
        self.evolution_dir = self.skill_dir / ".evolutions"
        self.evolution_dir.mkdir(exist_ok=True)
        
        self.backup_dir = self.skill_dir / ".backups"
        self.backup_dir.mkdir(exist_ok=True)
    
    def analyze_and_generate(self) -> Dict:
        """
        分析Skill并生成进化方案
        """
        evolution = {
            "id": f"evol_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "created_at": datetime.now().isoformat(),
            "skill_name": self.skill_name,
            "changes": [],
            "rationale": "",
            "risk_level": "low",
            "requires_approval": True
        }
        
        # 1. 检查代码结构
        code_analysis = self._analyze_code_structure()
        if code_analysis.get('issues'):
            evolution['changes'].append({
                "type": "refactor",
                "target": "code_structure",
                "description": "优化代码结构",
                "details": code_analysis['issues']
            })
        
        # 2. 检查依赖
        deps_analysis = self._analyze_dependencies()
        if deps_analysis.get('outdated'):
            evolution['changes'].append({
                "type": "update",
                "target": "dependencies",
                "description": "更新依赖版本",
                "details": deps_analysis['outdated']
            })
        
        # 3. 检查文档
        doc_analysis = self._analyze_documentation()
        if doc_analysis.get('missing'):
            evolution['changes'].append({
                "type": "docs",
                "target": "documentation",
                "description": "完善文档",
                "details": doc_analysis['missing']
            })
        
        # 4. 生成改进代码
        if evolution['changes']:
            evolution['patches'] = self._generate_patches(evolution['changes'])
            evolution['rationale'] = self._generate_rationale(evolution['changes'])
            evolution['risk_level'] = self._assess_risk(evolution['changes'])
        
        # 保存进化方案
        self._save_evolution(evolution)
        
        return evolution
    
    def _analyze_code_structure(self) -> Dict:
        """分析代码结构"""
        issues = []
        
        # 检查脚本目录
        scripts_dir = self.skill_dir / "scripts"
        if scripts_dir.exists():
            py_files = list(scripts_dir.glob("*.py"))
            
            for py_file in py_files:
                content = py_file.read_text(encoding='utf-8')
                
                # 检查是否有异常处理
                if 'try:' not in content and 'except' not in content:
                    issues.append({
                        "file": py_file.name,
                        "issue": "缺少异常处理",
                        "suggestion": "添加try-except块处理潜在错误"
                    })
                
                # 检查是否有文档字符串
                if '"""' not in content and "'''" not in content:
                    issues.append({
                        "file": py_file.name,
                        "issue": "缺少文档字符串",
                        "suggestion": "添加模块和函数的文档说明"
                    })
                
                # 检查硬编码路径
                if '/root/' in content or 'C:\\' in content:
                    issues.append({
                        "file": py_file.name,
                        "issue": "存在硬编码路径",
                        "suggestion": "使用相对路径或配置化路径"
                    })
        
        return {"issues": issues}
    
    def _analyze_dependencies(self) -> Dict:
        """分析依赖"""
        outdated = []
        
        req_file = self.skill_dir / "requirements.txt"
        if req_file.exists():
            # 这里可以接入 PyPI API 检查最新版本
            # 简化版本：检查是否有版本限制
            content = req_file.read_text()
            lines = content.strip().split('\n')
            
            for line in lines:
                if line and not line.startswith('#'):
                    if '==' not in line and '>=' not in line:
                        outdated.append({
                            "package": line.strip(),
                            "issue": "未指定版本",
                            "suggestion": "建议添加版本约束"
                        })
        
        return {"outdated": outdated}
    
    def _analyze_documentation(self) -> Dict:
        """分析文档"""
        missing = []
        
        required_docs = ["SKILL.md", "README.md"]
        for doc in required_docs:
            doc_file = self.skill_dir / doc
            if not doc_file.exists():
                missing.append({
                    "file": doc,
                    "issue": "缺少必要文档",
                    "suggestion": f"创建 {doc} 文件"
                })
        
        # 检查SKILL.md是否完整
        skill_md = self.skill_dir / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text()
            required_sections = ["##", "用法", "示例"]
            for section in required_sections:
                if section not in content:
                    missing.append({
                        "file": "SKILL.md",
                        "issue": f"缺少 {section} 部分",
                        "suggestion": f"添加 {section} 说明"
                    })
        
        return {"missing": missing}
    
    def _generate_patches(self, changes: List[Dict]) -> List[Dict]:
        """生成补丁"""
        patches = []
        
        for change in changes:
            if change['type'] == 'refactor':
                for detail in change.get('details', []):
                    patch = self._create_refactor_patch(detail)
                    if patch:
                        patches.append(patch)
            
            elif change['type'] == 'docs':
                for detail in change.get('details', []):
                    patch = self._create_docs_patch(detail)
                    if patch:
                        patches.append(patch)
        
        return patches
    
    def _create_refactor_patch(self, detail: Dict) -> Optional[Dict]:
        """创建重构补丁"""
        file_name = detail['file']
        issue = detail['issue']
        
        if '缺少异常处理' in issue:
            return {
                "target_file": f"scripts/{file_name}",
                "change_type": "add_exception_handling",
                "description": "添加异常处理",
                "code_template": """
try:
    # 原有代码
    pass
except Exception as e:
    print(f"[Error] {e}")
    raise
"""
            }
        
        elif '缺少文档字符串' in issue:
            return {
                "target_file": f"scripts/{file_name}",
                "change_type": "add_docstring",
                "description": "添加文档字符串",
                "code_template": '''
"""
功能描述

用法:
    示例代码
"""
'''
            }
        
        return None
    
    def _create_docs_patch(self, detail: Dict) -> Optional[Dict]:
        """创建文档补丁"""
        file_name = detail['file']
        
        return {
            "target_file": file_name,
            "change_type": "create_doc",
            "description": f"创建 {file_name}",
            "content_template": f"# {self.skill_name}\n\n待完善文档..."
        }
    
    def _generate_rationale(self, changes: List[Dict]) -> str:
        """生成改进理由"""
        rationales = []
        
        for change in changes:
            rationales.append(f"- {change['description']}: {change['target']}")
        
        return "\n".join(rationales)
    
    def _assess_risk(self, changes: List[Dict]) -> str:
        """评估风险等级"""
        risk_score = 0
        
        for change in changes:
            if change['type'] == 'refactor':
                risk_score += 2
            elif change['type'] == 'update':
                risk_score += 1
            elif change['type'] == 'docs':
                risk_score += 0
        
        if risk_score >= 3:
            return "high"
        elif risk_score >= 1:
            return "medium"
        else:
            return "low"
    
    def _save_evolution(self, evolution: Dict):
        """保存进化方案"""
        evol_file = self.evolution_dir / f"{evolution['id']}.json"
        with open(evol_file, 'w', encoding='utf-8') as f:
            json.dump(evolution, f, indent=2, ensure_ascii=False)
    
    def list_pending_evolutions(self) -> List[Dict]:
        """列出待审核的进化方案"""
        evolutions = []
        
        for evol_file in self.evolution_dir.glob("evol_*.json"):
            with open(evol_file, 'r', encoding='utf-8') as f:
                evol = json.load(f)
                if evol.get('requires_approval') and not evol.get('applied'):
                    evolutions.append(evol)
        
        return sorted(evolutions, key=lambda x: x['created_at'], reverse=True)
    
    def apply_evolution(self, evolution_id: str, confirmed: bool = False) -> Dict:
        """应用进化方案"""
        if not confirmed:
            return {
                "status": "pending",
                "message": "⚠️ 这是高风险操作，请确认：",
                "action_required": "添加 --confirm 参数确认应用",
                "backup_info": f"备份将保存到: {self.backup_dir}"
            }
        
        evol_file = self.evolution_dir / f"{evolution_id}.json"
        if not evol_file.exists():
            return {"status": "error", "message": "进化方案不存在"}
        
        with open(evol_file, 'r', encoding='utf-8') as f:
            evolution = json.load(f)
        
        # 创建备份
        backup_id = self._create_backup()
        
        # 应用补丁
        results = []
        for patch in evolution.get('patches', []):
            result = self._apply_patch(patch)
            results.append(result)
        
        # 标记为已应用
        evolution['applied'] = True
        evolution['applied_at'] = datetime.now().isoformat()
        evolution['backup_id'] = backup_id
        self._save_evolution(evolution)
        
        return {
            "status": "success",
            "backup_id": backup_id,
            "results": results
        }
    
    def _create_backup(self) -> str:
        """创建备份"""
        backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.backup_dir / backup_id
        backup_path.mkdir(exist_ok=True)
        
        # 复制关键文件
        import shutil
        for pattern in ["*.py", "*.md", "*.json", "*.txt"]:
            for file in self.skill_dir.rglob(pattern):
                if '.evolutions' not in str(file) and '.backups' not in str(file):
                    rel_path = file.relative_to(self.skill_dir)
                    dest = backup_path / rel_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file, dest)
        
        return backup_id
    
    def _apply_patch(self, patch: Dict) -> Dict:
        """应用单个补丁"""
        return {
            "file": patch.get('target_file'),
            "status": "simulated",
            "message": "补丁已生成，等待人工审核后应用"
        }


def main():
    parser = argparse.ArgumentParser(description='进化生成器')
    parser.add_argument('--skill', type=str, required=True, help='Skill名称')
    parser.add_argument('--analyze', action='store_true', help='分析并生成进化方案')
    parser.add_argument('--list-pending', action='store_true', help='列出待审核方案')
    parser.add_argument('--apply', action='store_true', help='应用进化方案')
    parser.add_argument('--id', type=str, help='进化方案ID')
    parser.add_argument('--confirm', action='store_true', help='确认应用')
    
    args = parser.parse_args()
    
    generator = EvolutionGenerator(args.skill)
    
    if args.analyze:
        evolution = generator.analyze_and_generate()
        print(json.dumps(evolution, indent=2, ensure_ascii=False))
    
    elif args.list_pending:
        pending = generator.list_pending_evolutions()
        print(f"[*] 找到 {len(pending)} 个待审核方案")
        for evol in pending:
            print(f"  - {evol['id']}: {evol['rationale'][:50]}...")
    
    elif args.apply and args.id:
        result = generator.apply_evolution(args.id, args.confirm)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(f"[*] 进化生成器已初始化: {args.skill}")
        print("[*] 使用 --analyze 生成改进方案")
        print("[*] 使用 --list-pending 查看待审核方案")
        print("[*] 使用 --apply --id XXX --confirm 应用方案")


if __name__ == '__main__':
    main()
