#!/usr/bin/env python3
"""
Skills Firewall Check - Validate and filter skills based on security rules.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum


class ActionType(Enum):
    ALLOW = (0, "allow")
    WARN = (1, "warn")
    BLOCK = (2, "block")
    QUARANTINE = (3, "quarantine")
    
    def __init__(self, priority: int, value: str):
        self._priority = priority
        self._value_ = value
    
    @property
    def priority(self) -> int:
        return self._priority
    
    def __gt__(self, other):
        if isinstance(other, ActionType):
            return self._priority > other._priority
        return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, ActionType):
            return self._priority < other._priority
        return NotImplemented


@dataclass
class FirewallRule:
    name: str
    description: str
    patterns: List[str]
    action: ActionType
    enabled: bool = True


@dataclass
class FirewallConfig:
    default_action: ActionType
    rules: List[FirewallRule]
    allowed_skills: Set[str]
    blocked_skills: Set[str]
    quarantine_dir: str


@dataclass
class FirewallDecision:
    skill_name: str
    action: str
    reason: str
    matched_rules: List[str]
    confidence: float


DEFAULT_RULES = [
    FirewallRule(
        name="block_code_injection",
        description="Block skills with code injection patterns",
        patterns=["eval(", "exec(", "__import__(", "compile("],
        action=ActionType.BLOCK,
        enabled=True
    ),
    FirewallRule(
        name="block_hardcoded_secrets",
        description="Block skills with hardcoded credentials",
        patterns=["password", "api_key", "apikey", "secret", "token"],
        action=ActionType.BLOCK,
        enabled=True
    ),
    FirewallRule(
        name="block_shell_true",
        description="Block skills using shell=True",
        patterns=["shell=True", "shell = True", "shell= True", "shell =True"],
        action=ActionType.BLOCK,
        enabled=True
    ),
    FirewallRule(
        name="warn_network_access",
        description="Warn on network access patterns",
        patterns=["requests.", "urllib", "socket.", "http://", "https://"],
        action=ActionType.WARN,
        enabled=True
    ),
    FirewallRule(
        name="warn_file_operations",
        description="Warn on file modification patterns",
        patterns=["shutil.rmtree", "os.remove", "os.unlink", "open(", "write("],
        action=ActionType.WARN,
        enabled=True
    ),
    FirewallRule(
        name="warn_subprocess",
        description="Warn on subprocess usage",
        patterns=["subprocess.", "os.system", "os.popen", "Popen("],
        action=ActionType.WARN,
        enabled=True
    ),
    FirewallRule(
        name="block_privilege_escalation",
        description="Block privilege escalation attempts",
        patterns=["sudo ", "su ", "chmod 777", "chown "],
        action=ActionType.BLOCK,
        enabled=True
    ),
    FirewallRule(
        name="block_remote_download",
        description="Block remote download commands",
        patterns=["curl ", "wget ", "Invoke-WebRequest", "DownloadFile"],
        action=ActionType.BLOCK,
        enabled=True
    ),
    FirewallRule(
        name="warn_obfuscation",
        description="Warn on potential obfuscation",
        patterns=["base64.b64decode", "base64.decode", "marshal.loads", "pickle.loads"],
        action=ActionType.WARN,
        enabled=True
    ),
]


class SkillsFirewall:
    def __init__(self, config: Optional[FirewallConfig] = None):
        self.config = config or self._default_config()
        self._scan_cache: Dict[str, FirewallDecision] = {}
    
    def _default_config(self) -> FirewallConfig:
        return FirewallConfig(
            default_action=ActionType.WARN,
            rules=DEFAULT_RULES,
            allowed_skills=set(),
            blocked_skills=set(),
            quarantine_dir="./quarantine"
        )
    
    def _read_skill_content(self, skill_path: str) -> str:
        content_parts = []
        skill_path = Path(skill_path)
        
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                if file.endswith(('.py', '.sh', '.js', '.ts', '.ps1', '.md')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content_parts.append(f.read())
                    except Exception:
                        pass
        
        return "\n".join(content_parts)
    
    def _check_patterns(self, content: str, patterns: List[str]) -> List[str]:
        matched = []
        content_lower = content.lower()
        
        for pattern in patterns:
            if pattern.lower() in content_lower:
                matched.append(pattern)
        
        return matched
    
    def check_skill(self, skill_path: str) -> FirewallDecision:
        skill_path = Path(skill_path)
        skill_name = skill_path.name
        
        if skill_name in self.config.allowed_skills:
            return FirewallDecision(
                skill_name=skill_name,
                action=ActionType.ALLOW.value,
                reason="Skill is in allowed list",
                matched_rules=[],
                confidence=1.0
            )
        
        if skill_name in self.config.blocked_skills:
            return FirewallDecision(
                skill_name=skill_name,
                action=ActionType.BLOCK.value,
                reason="Skill is in blocked list",
                matched_rules=["blocked_list"],
                confidence=1.0
            )
        
        content = self._read_skill_content(str(skill_path))
        matched_rules = []
        highest_action = ActionType.ALLOW
        reasons = []
        
        for rule in self.config.rules:
            if not rule.enabled:
                continue
            
            matched_patterns = self._check_patterns(content, rule.patterns)
            
            if matched_patterns:
                matched_rules.append(rule.name)
                reasons.append(f"{rule.name}: matched {matched_patterns}")
                
                if rule.action > highest_action:
                    highest_action = rule.action
        
        if not matched_rules:
            final_action = ActionType.ALLOW
            reason = "No security rules matched - skill appears safe"
        else:
            final_action = highest_action
            reason = "; ".join(reasons[:3])
        
        confidence = len(matched_rules) / max(len(self.config.rules), 1)
        
        return FirewallDecision(
            skill_name=skill_name,
            action=final_action.value,
            reason=reason,
            matched_rules=matched_rules,
            confidence=min(confidence, 1.0)
        )
    
    def filter_skills(self, skills_dir: str) -> Dict[str, List[str]]:
        results = {
            "allowed": [],
            "warned": [],
            "blocked": [],
            "quarantined": []
        }
        
        skills_path = Path(skills_dir)
        
        if not skills_path.exists():
            return results
        
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                decision = self.check_skill(str(skill_dir))
                
                if decision.action == ActionType.ALLOW.value:
                    results["allowed"].append(skill_dir.name)
                elif decision.action == ActionType.WARN.value:
                    results["warned"].append(skill_dir.name)
                elif decision.action == ActionType.BLOCK.value:
                    results["blocked"].append(skill_dir.name)
                elif decision.action == ActionType.QUARANTINE.value:
                    results["quarantined"].append(skill_dir.name)
        
        return results
    
    def add_allowed_skill(self, skill_name: str):
        self.config.allowed_skills.add(skill_name)
        if skill_name in self.config.blocked_skills:
            self.config.blocked_skills.remove(skill_name)
    
    def add_blocked_skill(self, skill_name: str):
        self.config.blocked_skills.add(skill_name)
        if skill_name in self.config.allowed_skills:
            self.config.allowed_skills.remove(skill_name)
    
    def create_rule(self, name: str, description: str, patterns: List[str], 
                    action: ActionType, enabled: bool = True) -> FirewallRule:
        rule = FirewallRule(
            name=name,
            description=description,
            patterns=patterns,
            action=action,
            enabled=enabled
        )
        self.config.rules.append(rule)
        return rule
    
    def export_config(self, output_path: str):
        config_dict = {
            "default_action": self.config.default_action.value,
            "allowed_skills": list(self.config.allowed_skills),
            "blocked_skills": list(self.config.blocked_skills),
            "quarantine_dir": self.config.quarantine_dir,
            "rules": [
                {
                    "name": r.name,
                    "description": r.description,
                    "patterns": r.patterns,
                    "action": r.action.value,
                    "enabled": r.enabled
                }
                for r in self.config.rules
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, default_flow_style=False)
    
    def import_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            config_dict = yaml.safe_load(f)
        
        self.config.default_action = ActionType(config_dict.get("default_action", "warn"))
        self.config.allowed_skills = set(config_dict.get("allowed_skills", []))
        self.config.blocked_skills = set(config_dict.get("blocked_skills", []))
        self.config.quarantine_dir = config_dict.get("quarantine_dir", "./quarantine")
        
        rules = []
        for r in config_dict.get("rules", []):
            rules.append(FirewallRule(
                name=r["name"],
                description=r["description"],
                patterns=r["patterns"],
                action=ActionType(r["action"]),
                enabled=r.get("enabled", True)
            ))
        
        self.config.rules = rules if rules else DEFAULT_RULES


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Skills Firewall - Check and filter skills")
    parser.add_argument("path", help="Path to skill directory or skills folder")
    parser.add_argument("--config", "-c", help="Path to firewall config file")
    parser.add_argument("--export-config", help="Export current config to file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--allow", action="store_true", help="Add skill to allowed list")
    parser.add_argument("--block", action="store_true", help="Add skill to blocked list")
    
    args = parser.parse_args()
    
    firewall = SkillsFirewall()
    
    if args.config:
        firewall.import_config(args.config)
    
    path = Path(args.path)
    
    if args.allow:
        firewall.add_allowed_skill(path.name)
        print(f"Added '{path.name}' to allowed skills list")
        return
    
    if args.block:
        firewall.add_blocked_skill(path.name)
        print(f"Added '{path.name}' to blocked skills list")
        return
    
    if args.export_config:
        firewall.export_config(args.export_config)
        print(f"Config exported to {args.export_config}")
        return
    
    if path.is_file() or (path.is_dir() and (path / "SKILL.md").exists()):
        decision = firewall.check_skill(str(path))
        
        if args.json:
            print(json.dumps(asdict(decision), indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"Skill: {decision.skill_name}")
            print(f"Action: {decision.action.upper()}")
            print(f"Reason: {decision.reason}")
            print(f"Confidence: {decision.confidence:.2%}")
            
            if decision.matched_rules:
                print(f"\nMatched Rules:")
                for rule in decision.matched_rules:
                    print(f"  - {rule}")
    else:
        results = firewall.filter_skills(str(path))
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"\n{'='*60}")
            print("Skills Firewall Filter Results")
            print(f"{'='*60}")
            
            print(f"\nAllowed ({len(results['allowed'])}):")
            for s in results["allowed"]:
                print(f"  [OK] {s}")
            
            print(f"\nWarnings ({len(results['warned'])}):")
            for s in results["warned"]:
                print(f"  [WARN] {s}")
            
            print(f"\nBlocked ({len(results['blocked'])}):")
            for s in results["blocked"]:
                print(f"  [BLOCK] {s}")
            
            print(f"\nQuarantined ({len(results['quarantined'])}):")
            for s in results["quarantined"]:
                print(f"  [QUAR] {s}")


if __name__ == "__main__":
    main()
