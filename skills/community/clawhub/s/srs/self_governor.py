#!/usr/bin/env python3
"""
SRS 自我治理模块
负责SRS自身能力提升、角色挖掘、持续学习
"""

import os
import json
from datetime import datetime
from typing import Dict, List

class SelfGovernor:
    """🧠 自我治理者 - 负责SRS自身能力提升"""
    
    def __init__(self):
        self.base_dir = os.path.expanduser("~/.openclaw/workspace/srs")
        self.capability_file = os.path.join(self.base_dir, "capabilities.json")
        self.roles_dir = os.path.join(self.base_dir, "roles")
        self._ensure_files()
        
    def _ensure_files(self):
        os.makedirs(self.roles_dir, exist_ok=True)
        if not os.path.exists(self.capability_file):
            self._init_capabilities()
            
    def _init_capabilities(self):
        """初始化能力记录"""
        capabilities = {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "roles": {},
            "skills": {},
            "improvements": [],
            "gaps": [],
            "learned_patterns": []
        }
        with open(self.capability_file, 'w') as f:
            json.dump(capabilities, f, indent=2)
            
    def scan_project_for_roles(self, project_dir: str = None) -> List[Dict]:
        """从项目中扫描角色模板"""
        if project_dir is None:
            project_dirs = [
                os.path.expanduser("~/ai-security/research"),
                os.path.expanduser("~/.openclaw/workspace/skills"),
                os.path.expanduser("~/.openclaw/workspace"),
            ]
        else:
            project_dirs = [project_dir]
            
        roles = []
        keywords = ["role", "agent", "skill", "capability", "职责", "能力"]
        
        for pdir in project_dirs:
            if not os.path.exists(pdir):
                continue
                
            for root, dirs, files in os.walk(pdir):
                # 跳过隐藏目录
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for f in files:
                    if f.endswith(('.md', '.yaml', '.json')):
                        path = os.path.join(root, f)
                        try:
                            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                                content = fp.read().lower()
                                # 检查关键词
                                for kw in keywords:
                                    if kw in content:
                                        roles.append({
                                            "file": path,
                                            "name": f,
                                            "type": self._detect_type(f, content),
                                            "keywords": self._extract_keywords(content)
                                        })
                                        break
                        except:
                            pass
                        
        return roles
        
    def _detect_type(self, filename: str, content: str) -> str:
        """检测类型"""
        filename = filename.lower()
        content_lower = content
        
        if "security" in filename or "security" in content_lower:
            return "security"
        elif "research" in filename or "研究" in content_lower:
            return "research"
        elif "manage" in filename or "管理" in content_lower:
            return "management"
        elif "ops" in filename or "运营" in content_lower:
            return "operations"
        elif "skill" in filename:
            return "skill"
        elif "agent" in filename:
            return "agent"
        else:
            return "general"
            
    def _extract_keywords(self, content: str) -> List[str]:
        """提取关键词"""
        keywords = []
        patterns = [
            "security", "research", "analysis", "monitor",
            "scan", "detect", "protect", "response",
            "audit", "compliance", "threat", "vulnerability"
        ]
        for p in patterns:
            if p in content:
                keywords.append(p)
        return keywords[:5]
        
    def evaluate_capabilities(self) -> Dict:
        """评估当前能力"""
        # 加载当前能力
        with open(self.capability_file, 'r') as f:
            caps = json.load(f)
            
        # 扫描项目获取新角色
        discovered_roles = self.scan_project_for_roles()
        
        # 评估差距
        gaps = []
        current_role_count = len(caps.get("roles", {}))
        
        if current_role_count < len(discovered_roles):
            gaps.append(f"角色库需要扩展: 当前{current_role_count}个, 发现{len(discovered_roles)}个")
            
        # 检查核心能力
        core_capabilities = ["security_researcher", "secops", "knowledge_manager", "explorer"]
        for cap in core_capabilities:
            if cap not in caps.get("roles", {}):
                gaps.append(f"缺少核心角色: {cap}")
                
        return {
            "current_roles": current_role_count,
            "discovered_roles": len(discovered_roles),
            "gaps": gaps,
            "discovered": discovered_roles[:10],  # 只返回前10个
            "capabilities": caps
        }
        
    def create_role_from_template(self, role_info: Dict) -> str:
        """从模板创建新角色"""
        role_name = role_info.get("name", "new_role")
        role_file = os.path.join(self.roles_dir, f"{role_name}.json")
        
        role_template = {
            "name": role_name,
            "emoji": role_info.get("emoji", "📦"),
            "description": role_info.get("description", ""),
            "capabilities": role_info.get("capabilities", []),
            "auto_tasks": role_info.get("auto_tasks", []),
            "source": role_info.get("source", "discovered"),
            "source_file": role_info.get("source_file", ""),
            "created_at": datetime.now().isoformat()
        }
        
        with open(role_file, 'w') as f:
            json.dump(role_template, f, indent=2)
            
        # 更新能力记录
        with open(self.capability_file, 'r') as f:
            caps = json.load(f)
            
        caps["roles"][role_name] = role_template
        caps["last_updated"] = datetime.now().isoformat()
        caps["improvements"].append({
            "action": "create_role",
            "role": role_name,
            "time": datetime.now().isoformat()
        })
        
        with open(self.capability_file, 'w') as f:
            json.dump(caps, f, indent=2)
            
        return role_file
        
    def auto_improve(self) -> Dict:
        """自动改进"""
        # 1. 评估能力
        eval_result = self.evaluate_capabilities()
        
        improvements = []
        
        # 2. 识别差距并创建角色
        for gap in eval_result.get("gaps", []):
            if "缺少核心角色" in gap:
                role_name = gap.split(":")[1].strip()
                # 创建缺失的角色
                role_info = {
                    "name": role_name,
                    "emoji": self._get_role_emoji(role_name),
                    "description": f"自动发现并创建的角色: {role_name}",
                    "capabilities": self._get_default_capabilities(role_name),
                    "auto_tasks": self._get_default_tasks(role_name),
                    "source": "auto_improve"
                }
                self.create_role_from_template(role_info)
                improvements.append(f"创建角色: {role_name}")
                
        # 3. 记录改进
        with open(self.capability_file, 'r') as f:
            caps = json.load(f)
            
        caps["last_updated"] = datetime.now().isoformat()
        
        with open(self.capability_file, 'w') as f:
            json.dump(caps, f, indent=2)
            
        return {
            "evaluation": eval_result,
            "improvements": improvements,
            "timestamp": datetime.now().isoformat()
        }
        
    def _get_role_emoji(self, role_name: str) -> str:
        """获取角色emoji"""
        mapping = {
            "security_researcher": "🔴",
            "secops": "🛡️",
            "knowledge_manager": "📖",
            "explorer": "🚀",
            "project_manager": "🎯",
            "domain_researcher": "📚",
            "qa": "🧪",
            "developer": "💻"
        }
        return mapping.get(role_name, "📦")
        
    def _get_default_capabilities(self, role_name: str) -> List[str]:
        """获取默认能力"""
        mapping = {
            "security_researcher": ["漏洞分析", "威胁评估", "风险评级"],
            "secops": ["监控", "告警", "响应"],
            "knowledge_manager": ["文档整理", "知识沉淀", "报告生成"],
            "explorer": ["扫描", "发现", "趋势洞察"]
        }
        return mapping.get(role_name, ["通用能力"])
        
    def _get_default_tasks(self, role_name: str) -> List[str]:
        """获取默认任务"""
        mapping = {
            "security_researcher": ["cve_scan", "threat_analysis"],
            "secops": ["monitor", "alert", "respond"],
            "knowledge_manager": ["organize", "document", "report"],
            "explorer": ["scan", "discover", "trend"]
        }
        return mapping.get(role_name, ["general_task"])
        
    def get_status(self) -> Dict:
        """获取治理状态"""
        if os.path.exists(self.capability_file):
            with open(self.capability_file, 'r') as f:
                caps = json.load(f)
                return {
                    "version": caps.get("version"),
                    "roles_count": len(caps.get("roles", {})),
                    "improvements_count": len(caps.get("improvements", [])),
                    "last_updated": caps.get("last_updated"),
                    "gaps": caps.get("gaps", [])
                }
        return {}

# CLI
if __name__ == "__main__":
    import sys
    
    sg = SelfGovernor()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "status":
            print(json.dumps(sg.get_status(), indent=2, ensure_ascii=False))
            
        elif cmd == "scan":
            roles = sg.scan_project_for_roles()
            print(f"发现 {len(roles)} 个角色模板:")
            for r in roles[:5]:
                print(f"  - {r['name']} ({r['type']})")
                
        elif cmd == "evaluate":
            result = sg.evaluate_capabilities()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif cmd == "improve":
            result = sg.auto_improve()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        else:
            print("用法: self_governor.py {status|scan|evaluate|improve}")
    else:
        print("🧠 SRS 自我治理模块")
        print("用法: self_governor.py {status|scan|evaluate|improve}")
