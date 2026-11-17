"""
SkillGate Rule Engine — 用户可配置的 YAML 规则系统。
仿照 Semgrep 的规则格式。
"""
import re
from pathlib import Path
from typing import List, Dict, Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class SkillGateRule:
    """A single scan rule."""

    def __init__(self, rule_dict: Dict[str, Any]):
        self.id = rule_dict.get("id", "UNKNOWN")
        self.description = rule_dict.get("description", "")
        self.severity = rule_dict.get("severity", "MEDIUM")
        self.patterns = rule_dict.get("patterns", [])
        self.languages = rule_dict.get("languages", ["*"])
        self.fix = rule_dict.get("fix", None)

    def matches(self, content: str, file_ext: str) -> List[Dict]:
        """Check if this rule matches the content."""
        # Check language
        if "*" not in self.languages:
            ext_map = {
                ".py": "python", ".js": "javascript", ".ts": "typescript",
                ".go": "go", ".rs": "rust", ".java": "java",
            }
            lang = ext_map.get(file_ext, "")
            if lang and lang not in self.languages:
                return []

        findings = []
        lines = content.splitlines()

        for pattern in self.patterns:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    findings.append({
                        "rule_id": self.id,
                        "severity": self.severity,
                        "message": self.description,
                        "line": i,
                        "match": line.strip()
                    })

        return findings


class RuleEngine:
    """Load and run user-defined rules."""

    def __init__(self):
        self.rules: List[SkillGateRule] = []

    def load_rules(self, rules_dir: str):
        """Load rules from a directory of YAML files."""
        rules_path = Path(rules_dir)

        if not HAS_YAML:
            print("⚠️  PyYAML not installed, skipping custom rules")
            return

        for yaml_file in rules_path.glob("*.yml"):
            try:
                with open(yaml_file, encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                if "rules" in data:
                    for rule_dict in data["rules"]:
                        self.rules.append(SkillGateRule(rule_dict))
            except Exception as e:
                print(f"⚠️  Failed to load {yaml_file}: {e}")

    def scan(self, filepath: Path) -> List[Dict]:
        """Run all rules against a file."""
        try:
            content = filepath.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return []

        all_findings = []
        ext = filepath.suffix

        for rule in self.rules:
            findings = rule.matches(content, ext)
            all_findings.extend(findings)

        return all_findings


# Example rule format (YAML):
"""
rules:
  - id: my-custom-rule-001
    description: "Found dangerous function call"
    severity: HIGH
    languages: [python]
    patterns:
      - "eval\\("
      - "exec\\("
    fix: "Use ast.literal_eval() instead"
"""


if __name__ == "__main__":
    engine = RuleEngine()
    # engine.load_rules("./rules/")
    print("Rule Engine ready")
