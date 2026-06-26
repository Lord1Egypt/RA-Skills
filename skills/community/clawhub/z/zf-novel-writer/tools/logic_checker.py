#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple logic checker for novel chapters
"""

import re
from pathlib import Path


class LogicChecker:
    """Logic checker class"""

    def __init__(self, file_path=None):
        self.file_path = file_path
        self.content = None
        self.issues = []
        self.warnings = []

    def load_file(self, file_path=None):
        """Load chapter file"""
        if file_path:
            self.file_path = file_path

        if not self.file_path:
            self.issues.append("No file path specified")
            return False

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except Exception as e:
            self.issues.append(f"Cannot read file: {e}")
            return False

    def check_finance_logic(self):
        """Check finance logic consistency"""
        issues = []
        warnings = []

        if not self.content:
            return ["Content is empty"], []

        # Extract all money amounts
        money_pattern = r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:元|万|亿)'
        money_matches = re.findall(money_pattern, self.content)

        # Check if there are finance calculation errors
        finance_calc = re.search(r'(\d+\.?\d*)\s*[\*×]\s*([\d\.]+)\s*=\s*(\d+\.?\d*)', self.content)
        if finance_calc:
            left = float(finance_calc.group(1)) * float(finance_calc.group(2))
            right = float(finance_calc.group(3))
            if abs(left - right) > 0.01:
                issues.append(f"Calculation error: {finance_calc.group(1)} × {finance_calc.group(2)} = {left}, not {right}")

        # Check for negative balance warnings
        negative_balance = re.search(r'余额[：:]\s*-?\d+', self.content)
        if negative_balance and '-' in negative_balance.group():
            warnings.append("Balance is negative")

        return issues, warnings

    def check_all(self):
        """Run all checks"""
        self.issues = []
        self.warnings = []

        if not self.content:
            if not self.load_file():
                return {"issues": self.issues, "warnings": self.warnings}

        # Check finance logic
        finance_issues, finance_warnings = self.check_finance_logic()
        self.issues.extend(finance_issues)
        self.warnings.extend(finance_warnings)

        return {
            "issues": self.issues,
            "warnings": self.warnings
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        checker = LogicChecker(sys.argv[1])
        result = checker.check_all()
        print("Logic Check Results:")
        print(f"Issues: {result['issues']}")
        print(f"Warnings: {result['warnings']}")
