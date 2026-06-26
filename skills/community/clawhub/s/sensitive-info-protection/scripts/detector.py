import json
import os
from typing import List, Optional
from models import DetectionRule, DetectionResult, ScanResult


class SensitiveDetector:
    """Main sensitive information detection engine"""

    def __init__(self):
        self.rules: List[DetectionRule] = []
        self._load_default_rules()

    def _load_default_rules(self) -> None:
        """Load built-in default rules"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_rules_path = os.path.join(script_dir, 'default_rules.json')

        if os.path.exists(default_rules_path):
            with open(default_rules_path, 'r', encoding='utf-8') as f:
                rules_data = json.load(f)
                for rule_data in rules_data:
                    rule = DetectionRule(**rule_data)
                    rule.compile()
                    self.rules.append(rule)

        # Sort by priority
        self.rules.sort(key=lambda x: -x.priority)

    def load_config(self, config_path: str) -> None:
        """Load rules from configuration file"""
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.endswith('.json'):
                rules_data = json.load(f)
            else:
                raise ValueError("Only JSON configuration is supported currently")

        for rule_data in rules_data:
            rule = DetectionRule(**rule_data)
            rule.compile()
            self.rules.append(rule)

        # Re-sort by priority
        self.rules.sort(key=lambda x: -x.priority)

    def add_rule(self, rule: DetectionRule) -> None:
        """Add a new detection rule"""
        rule.compile()
        self.rules.append(rule)
        self.rules.sort(key=lambda x: -x.priority)

    def remove_rule(self, rule_name: str) -> bool:
        """Remove a rule by name"""
        original_count = len(self.rules)
        self.rules = [r for r in self.rules if r.name != rule_name]
        return len(self.rules) < original_count

    def enable_rule(self, rule_name: str) -> bool:
        """Enable a rule by name"""
        for rule in self.rules:
            if rule.name == rule_name:
                rule.enabled = True
                return True
        return False

    def disable_rule(self, rule_name: str) -> bool:
        """Disable a rule by name"""
        for rule in self.rules:
            if rule.name == rule_name:
                rule.enabled = False
                return True
        return False

    def scan(self, content: str) -> ScanResult:
        """Scan content for sensitive information"""
        result = ScanResult(content=content)

        for rule in self.rules:
            if not rule.enabled:
                continue

            matches = rule.match(content)
            for match in matches:
                detection = DetectionResult(
                    rule=rule,
                    match=match,
                    start=match.start(),
                    end=match.end(),
                    text=match.group()
                )
                result.add_detection(detection)

        result.sort_by_priority()
        return result

    def desensitize(self, content: str, replacement: str = "***") -> str:
        """Desensitize all detected sensitive information"""
        result = self.scan(content)
        if not result.has_sensitive:
            return content

        # Sort detections by start position descending to avoid offset issues
        sorted_detections = sorted(result.detections, key=lambda x: -x.start)
        content_list = list(content)

        for detection in sorted_detections:
            # Replace the sensitive text with replacement
            del content_list[detection.start:detection.end]
            content_list.insert(detection.start, replacement)

        return ''.join(content_list)

    def print_results(self, result: ScanResult) -> None:
        """Print detection results in standard format"""
        print(result.to_markdown())
