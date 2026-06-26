#!/usr/bin/env python3
"""
Skill Analyzer - Comprehensive skill analysis tool
Analyzes OpenClaw skills across multiple dimensions
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


class SkillAnalyzer:
    """Comprehensive skill analyzer for OpenClaw skills."""
    
    DIMENSIONS = {
        "functionality": {
            "weight": 0.25,
            "checks": [
                "check_skill_md_exists",
                "check_description",
                "check_scripts",
                "check_cli_interface"
            ]
        },
        "security": {
            "weight": 0.25,
            "checks": [
                "check_no_hardcoded_secrets",
                "check_safe_file_operations",
                "check_input_validation"
            ]
        },
        "usability": {
            "weight": 0.20,
            "checks": [
                "check_installation_guide",
                "check_examples",
                "check_error_messages"
            ]
        },
        "documentation": {
            "weight": 0.15,
            "checks": [
                "check_skill_md_complete",
                "check_tags",
                "check_readme"
            ]
        },
        "best_practices": {
            "weight": 0.15,
            "checks": [
                "check_code_structure",
                "check_error_handling",
                "check_config_handling"
            ]
        }
    }
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_data = {}
        self.results = {}
        self.issues = []
        self.strengths = []
    
    def analyze(self) -> Dict[str, Any]:
        """Run complete analysis."""
        print(f"Analyzing skill: {self.skill_path.name}")
        
        # Load SKILL.md
        self._load_skill_md()
        
        # Run all checks
        self._run_functionality_checks()
        self._run_security_checks()
        self._run_usability_checks()
        self._run_documentation_checks()
        self._run_best_practices_checks()
        
        # Calculate scores
        scores = self._calculate_scores()
        
        return {
            "skill_name": self.skill_path.name,
            "overall_score": self._weighted_average(scores),
            "dimension_scores": scores,
            "strengths": self.strengths,
            "issues": self.issues,
            "risk_level": self._assess_risk(scores)
        }
    
    def _load_skill_md(self):
        """Load and parse SKILL.md."""
        skill_md = self.skill_path / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text(encoding="utf-8")
            
            # Parse YAML frontmatter manually
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    self.skill_data["content"] = parts[2]
                    
                    # Parse simple YAML key-value pairs
                    for line in frontmatter.split("\n"):
                        line = line.strip()
                        if ":" in line and not line.startswith("#"):
                            key, value = line.split(":", 1)
                            self.skill_data[key.strip()] = value.strip()
                else:
                    self.skill_data = {"content": content}
            else:
                self.skill_data = {"content": content}
    
    # Functionality Checks
    def _run_functionality_checks(self):
        """Run functionality analysis."""
        score = 0
        max_score = 10
        
        # Check SKILL.md exists
        if (self.skill_path / "SKILL.md").exists():
            score += 2
        else:
            self.issues.append("SKILL.md not found")
        
        # Check description
        if self.skill_data.get("description"):
            score += 3
        else:
            self.issues.append("No description in frontmatter")
        
        # Check scripts directory
        scripts_dir = self.skill_path / "scripts"
        if scripts_dir.exists() and list(scripts_dir.iterdir()):
            score += 3
            self.strengths.append("Scripts directory with executable files")
        else:
            # Skills without scripts are valid (documentation-only skills)
            score += 2
        
        # Check CLI interface
        if self._has_cli():
            score += 2
        
        self.results["functionality"] = score
    
    def _has_cli(self) -> bool:
        """Check if skill has CLI interface."""
        content = self.skill_data.get("content", "")
        return "python3" in content or "--" in content or "usage:" in content.lower()
    
    # Security Checks
    def _run_security_checks(self):
        """Run security analysis."""
        score = 10
        
        # Check for hardcoded secrets
        if self._has_hardcoded_secrets():
            score -= 5
            self.issues.append("Potential hardcoded credentials found")
        else:
            self.strengths.append("No obvious hardcoded secrets")
        
        # Check scripts for security
        # Only flag eval/exec when combined with dynamic input (dangerous pattern)
        scripts_dir = self.skill_path / "scripts"
        if scripts_dir.exists():
            for script in scripts_dir.glob("*.py"):
                content = script.read_text(encoding="utf-8")
                # Only flag if: eval/exec + (user input functions or variable injection risk)
                dangerous = False
                if "eval(" in content or "exec(" in content:
                    # Check for variable injection patterns: eval(x), exec(f.read()), etc.
                    if re.search(r'(eval|exec)\s*\(\s*(f["\'(]|open\(|request|json\.loads|argv\[)', content):
                        dangerous = True
                if dangerous:
                    score -= 3
                    self.issues.append(f"Potentially unsafe operation in {script.name}")
        
        self.results["security"] = max(0, score)
    
    def _has_hardcoded_secrets(self) -> bool:
        """Check for hardcoded secrets in code."""
        patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]
        
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return False
        
        for script in scripts_dir.glob("*.py"):
            content = script.read_text(encoding="utf-8")
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return True
        return False
    
    # Usability Checks
    def _run_usability_checks(self):
        """Run usability analysis."""
        score = 0
        content = self.skill_data.get("content", "")
        
        # Check for examples
        if "```" in content or "example" in content.lower():
            score += 4
            self.strengths.append("Usage examples provided")
        
        # Check for installation guide
        if "install" in content.lower() or "setup" in content.lower():
            score += 3
        
        # Check for clear structure
        if len(content) > 500:
            score += 3
        
        self.results["usability"] = min(10, score)
    
    # Documentation Checks
    def _run_documentation_checks(self):
        """Run documentation analysis."""
        score = 0
        
        # Check SKILL.md completeness
        content = self.skill_data.get("content", "")
        if len(content) > 300:
            score += 4
        elif len(content) > 100:
            score += 2
        
        # Check name and description
        if self.skill_data.get("name"):
            score += 2
        if self.skill_data.get("description"):
            score += 2
        
        # Check tags
        if self.skill_data.get("tags"):
            score += 2
        
        self.results["documentation"] = min(10, score)
    
    # Best Practices Checks
    def _run_best_practices_checks(self):
        """Run best practices analysis."""
        score = 5
        
        # Check code structure
        scripts_dir = self.skill_path / "scripts"
        if scripts_dir.exists():
            py_files = list(scripts_dir.glob("*.py"))
            if py_files:
                score += 2
                # Check for proper main entry point
                for script in py_files:
                    content = script.read_text(encoding="utf-8")
                    if "if __name__" in content and "__main__" in content:
                        score += 1
                        break
        
        # Check error handling
        content = self.skill_data.get("content", "")
        if "error" in content.lower() or "exception" in content.lower():
            score += 1
        
        # Check configuration
        if (self.skill_path / "references").exists():
            score += 1
        
        self.results["best_practices"] = min(10, score)
    
    def _calculate_scores(self) -> Dict[str, float]:
        """Calculate weighted scores."""
        scores = {}
        for dimension, config in self.DIMENSIONS.items():
            score = self.results.get(dimension, 0)
            scores[dimension] = score * config["weight"] * 10
        return scores
    
    def _weighted_average(self, scores: Dict[str, float]) -> float:
        """Calculate weighted average."""
        return sum(scores.values())
    
    def _assess_risk(self, scores: Dict[str, float]) -> str:
        """Assess overall risk level."""
        overall = sum(scores.values())
        if overall >= 7.5:
            return "LOW"
        elif overall >= 5:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def print_report(self, results: Dict[str, Any]):
        """Print formatted report."""
        print("\n" + "=" * 44)
        print(f"Skill Analysis Report: {results['skill_name']}")
        print("=" * 44)
        
        print(f"\nOverall Score: {results['overall_score']:.1f}/10")
        
        print("\nDimension Scores:")
        dimension_names = {
            "functionality": "Functionality",
            "security": "Security",
            "usability": "Usability",
            "documentation": "Documentation",
            "best_practices": "Best Practices"
        }
        
        for dim, score in results["dimension_scores"].items():
            bar_len = int(score / 10 * 10)
            bar = "█" * bar_len + "░" * (10 - bar_len)
            name = dimension_names.get(dim, dim)
            print(f"  {name:20s} {score:.1f}/10 {bar}")
        
        if results["strengths"]:
            print("\nStrengths:")
            for s in results["strengths"]:
                print(f"  ✓ {s}")
        
        if results["issues"]:
            print("\nIssues:")
            for i in results["issues"]:
                print(f"  ✗ {i}")
        
        print(f"\nRisk Level: {results['risk_level']}")
        print("=" * 44)


def main():
    parser = argparse.ArgumentParser(description="Skill Analyzer - Analyze OpenClaw skills")
    parser.add_argument("--path", required=True, help="Path to skill directory")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--output", help="Output JSON file")
    parser.add_argument("--compare", nargs=2, metavar=("SKILL1", "SKILL2"), help="Compare two skills")
    
    args = parser.parse_args()
    
    if args.compare:
        # Compare mode
        skill1 = SkillAnalyzer(args.compare[0]).analyze()
        skill2 = SkillAnalyzer(args.compare[1]).analyze()
        
        print("\n" + "=" * 44)
        print("Skill Comparison")
        print("=" * 44)
        print(f"\n{args.compare[0]}: {skill1['overall_score']:.1f}/10")
        print(f"{args.compare[1]}: {skill2['overall_score']:.1f}/10")
        
        diff = skill1['overall_score'] - skill2['overall_score']
        if diff > 0:
            print(f"\n{args.compare[0]} is {diff:.1f} points higher")
        elif diff < 0:
            print(f"\n{args.compare[1]} is {-diff:.1f} points higher")
        else:
            print("\nBoth skills have the same score")
    else:
        # Single analysis mode
        if not os.path.isdir(args.path):
            print(f"Error: {args.path} is not a directory")
            sys.exit(1)
        
        analyzer = SkillAnalyzer(args.path)
        results = analyzer.analyze()
        
        analyzer.print_report(results)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Report saved to {args.output}")


if __name__ == "__main__":
    main()
