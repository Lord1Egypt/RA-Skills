#!/usr/bin/env python3
"""
Dependency Resolver Core
扫描、检测、解决技能依赖冲突
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import sys

@dataclass
class PackageRequirement:
    """单个包的版本要求"""
    name: str
    raw_spec: str  # 原始版本规范，如 "pandas>=1.3.0,<2.0.0"
    version: Optional[str] = None  # 固定版本（如果使用 ==）
    spec_lower: Optional[str] = None  # 下限版本
    spec_upper: Optional[str] = None  # 上限版本
    
    @classmethod
    def parse(cls, line: str) -> 'PackageRequirement':
        """从 requirements.txt 行解析"""
        line = line.strip()
        if not line or line.startswith('#'):
            return None
        
        # 移除注释
        if '#' in line:
            line = line.split('#')[0].strip()
        
        # 简单解析：name==version 或 name>=version
        parts = re.split(r'[<>=!,;\s]+', line, maxsplit=1)
        name = parts[0].lower()
        raw_spec = line[len(name):].strip()
        
        # 尝试提取固定版本
        version = None
        if '==' in raw_spec:
            version = raw_spec.split('==')[1].strip()
        
        return cls(name=name, raw_spec=raw_spec, version=version)

@dataclass
class Conflict:
    """依赖冲突"""
    package: str
    requirements: List[PackageRequirement]
    versions: List[str]
    resolved: Optional[str] = None

class DependencyResolver:
    def __init__(self, skills_dir: Path, output_file: Path, strategy: str = "auto", verbose: bool = False):
        self.skills_dir = Path(skills_dir)
        self.output_file = Path(output_file)
        self.strategy = strategy
        self.verbose = verbose
        self.requirements: Dict[str, List[PackageRequirement]] = defaultdict(list)
        self.conflicts: List[Conflict] = []
    
    def scan_skills(self) -> int:
        """扫描所有技能的 requirements.txt"""
        skills_count = 0
        
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            
            req_file = skill_dir / "requirements.txt"
            if req_file.exists():
                skills_count += 1
                if self.verbose:
                    print(f"🔍 扫描: {skill_dir.name}")
                
                try:
                    self._parse_requirements_file(req_file, skill_dir.name)
                except Exception as e:
                    print(f"⚠️  无法解析 {req_file}: {e}")
        
        return skills_count
    
    def _parse_requirements_file(self, filepath: Path, skill_name: str):
        """解析单个 requirements.txt"""
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                pkg = PackageRequirement.parse(line)
                if pkg:
                    pkg.source_skill = skill_name
                    pkg.source_line = line_num
                    self.requirements[pkg.name].append(pkg)
    
    def detect_conflicts(self) -> int:
        """检测版本冲突"""
        conflict_count = 0
        
        for pkg_name, reqs in self.requirements.items():
            # 提取所有固定的版本号（使用 == 的）
            fixed_versions = [r.version for r in reqs if r.version is not None]
            
            if len(set(fixed_versions)) > 1:
                # 发现冲突
                conflict = Conflict(
                    package=pkg_name,
                    requirements=reqs,
                    versions=fixed_versions
                )
                self.conflicts.append(conflict)
                conflict_count += 1
                
                if self.verbose:
                    print(f"⚠️  冲突: {pkg_name} 有多个版本: {fixed_versions}")
        
        return conflict_count
    
    def resolve_conflicts(self) -> int:
        """解决冲突"""
        solved = 0
        
        for conflict in self.conflicts:
            if self.strategy == "auto":
                # 自动策略：选择最高版本（语义化版本比较）
                resolved_version = self._choose_highest_version(conflict.versions)
                conflict.resolved = resolved_version
                solved += 1
            elif self.strategy == "manual":
                # 手动模式：暂停并询问用户
                print(f"\n❓ 冲突: {conflict.package}")
                for req in conflict.requirements:
                    print(f"   - {req.source_skill}: {req.raw_spec}")
                
                choice = input(f"   选择版本 [{conflict.versions[0]}]: ") or conflict.versions[0]
                conflict.resolved = choice
                solved += 1
        
        return solved
    
    def _choose_highest_version(self, versions: List[str]) -> str:
        """简单的版本比较，选择最高版本（假设是 X.Y.Z 格式）"""
        def version_key(v):
            parts = list(map(int, re.findall(r'\d+', v)))
            return tuple(parts)
        
        return max(versions, key=version_key)
    
    def generate_merged_requirements(self) -> Path:
        """生成合并后的 requirements.txt"""
        lines = ["# 自动生成的统一 requirements.txt", "# 由 skill-dependency-resolver 生成\n"]
        
        # 收集所有包，冲突的包使用 resolved 版本
        processed = set()
        
        for pkg_name, reqs in self.requirements.items():
            if pkg_name in processed:
                continue
            
            # 检查是否有冲突
            conflict = next((c for c in self.conflicts if c.package == pkg_name), None)
            
            if conflict and conflict.resolved:
                # 使用解决的版本
                line = f"{pkg_name}=={conflict.resolved}"
                lines.append(line)
            else:
                # 没有冲突，取第一个（通常唯一）
                first_req = reqs[0]
                if first_req.version:
                    line = f"{pkg_name}=={first_req.version}"
                else:
                    line = first_req.raw_spec
                lines.append(line)
            
            processed.add(pkg_name)
        
        # 写入文件
        self.output_file.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        return self.output_file
    
    def resolve(self) -> dict:
        """主流程"""
        print("🔍 开始扫描技能依赖...")
        skills_scanned = self.scan_skills()
        
        print("⚡ 检测冲突...")
        conflicts_found = self.detect_conflicts()
        
        if conflicts_found > 0:
            print(f"⚠️  发现 {conflicts_found} 个包冲突")
            if self.strategy == "auto":
                print("🤖 自动解决中...")
                solutions = self.resolve_conflicts()
            else:
                solutions = self.resolve_conflicts()  # manual 也会在内部处理
        else:
            solutions = 0
            print("✅ 无依赖冲突")
        
        print(f"📝 生成合并文件: {self.output_file}")
        output = self.generate_merged_requirements()
        
        return {
            "skills_scanned": skills_scanned,
            "conflicts_found": conflicts_found,
            "solutions_applied": solutions,
            "output_file": str(output),
            "conflicts": [
                {
                    "package": c.package,
                    "versions": c.versions,
                    "resolved": c.resolved,
                    "requirements": [
                        {"skill": r.source_skill, "spec": r.raw_spec} for r in c.requirements
                    ]
                }
                for c in self.conflicts
            ]
        }