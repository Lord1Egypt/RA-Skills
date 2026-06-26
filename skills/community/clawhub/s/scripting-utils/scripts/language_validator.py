#!/usr/bin/env python3
"""
Multi-language script validator supporting 8+ languages.
WebSearch integration for documentation lookup.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    language: str
    valid: bool
    errors: list[str]
    warnings: list[str]
    doc_url: Optional[str] = None

class LanguageValidator:
    LANGUAGES = {
        "bash": {"cmd": "bash", "args": ["-n"], "linter": "shellcheck"},
        "sh": {"cmd": "sh", "args": ["-n"], "linter": "shellcheck"},
        "python": {"cmd": "python3", "args": ["-m", "py_compile"], "linter": "pylint"},
        "perl": {"cmd": "perl", "args": ["-c"], "linter": "perlcritic"},
        "raku": {"cmd": "raku", "args": ["-c"], "linter": None},
        "powershell": {"cmd": "pwsh", "args": ["-Command", "Get-Command"], "linter": None},
        "javascript": {"cmd": "node", "args": ["--check"], "linter": "eslint"},
        "tcl": {"cmd": "tclsh", "args": [], "linter": None},
    }
    
    def __init__(self, language: str, use_websearch: bool = True):
        self.language = language.lower()
        self.use_websearch = use_websearch
        self.config = self.LANGUAGES.get(self.language)
        if not self.config:
            raise ValueError(f"Unsupported language: {language}")
    
    def validate(self, script_path: Path) -> ValidationResult:
        """Validate a script file."""
        errors = []
        warnings = []
        
        # Syntax check
        try:
            result = subprocess.run(
                [self.config["cmd"]] + self.config["args"] + [str(script_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                errors.append(result.stderr)
        except subprocess.TimeoutExpired:
            errors.append("Validation timeout")
        except FileNotFoundError:
            errors.append(f"Command not found: {self.config['cmd']}")
            if self.use_websearch:
                doc_url = self._fetch_docs()
                return ValidationResult(self.language, False, errors, warnings, doc_url)
        
        # Linter check if available
        if self.config["linter"]:
            linter_warnings = self._run_linter(script_path)
            warnings.extend(linter_warnings)
        
        return ValidationResult(
            language=self.language,
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _run_linter(self, script_path: Path) -> list[str]:
        """Run language-specific linter."""
        linter = self.config["linter"]
        warnings = []
        
        try:
            if linter == "shellcheck":
                result = subprocess.run(
                    ["shellcheck", "-f", "gcc", str(script_path)],
                    capture_output=True,
                    text=True
                )
                if result.stdout:
                    warnings.extend(result.stdout.strip().split("\n"))
            elif linter == "pylint":
                result = subprocess.run(
                    ["pylint", "--output-format=parseable", str(script_path)],
                    capture_output=True,
                    text=True
                )
                if result.stdout:
                    warnings.extend(result.stdout.strip().split("\n"))
        except FileNotFoundError:
            warnings.append(f"Linter not installed: {linter}")
        
        return warnings
    
    def _fetch_docs(self) -> Optional[str]:
        """Fetch documentation URL via WebSearch if enabled."""
        if not self.use_websearch:
            return None
        
        # Return known good documentation URLs
        docs = {
            "powershell": "https://docs.microsoft.com/powershell/",
            "raku": "https://docs.raku.org/",
            "tcl": "https://www.tcl.tk/",
        }
        return docs.get(self.language)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate scripts in multiple languages")
    parser.add_argument("script", type=Path, help="Path to script file")
    parser.add_argument("--lang", required=True, help="Language (bash/python/perl/etc.)")
    parser.add_argument("--no-websearch", action="store_true", help="Disable WebSearch")
    args = parser.parse_args()
    
    validator = LanguageValidator(args.lang, use_websearch=not args.no_websearch)
    result = validator.validate(args.script)
    
    print(f"Language: {result.language}")
    print(f"Valid: {result.valid}")
    if result.errors:
        print(f"Errors: {len(result.errors)}")
        for err in result.errors[:5]:  # Show first 5
            print(f"  - {err}")
    if result.warnings:
        print(f"Warnings: {len(result.warnings)}")
        for warn in result.warnings[:5]:
            print(f"  - {warn}")
    if result.doc_url:
        print(f"Docs: {result.doc_url}")
    
    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
