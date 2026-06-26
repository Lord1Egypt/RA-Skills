#!/usr/bin/env python3
"""
Code Capability Detector for Skills-Coach v2.3.1

Analyzes scripts to detect their actual capabilities before generating test tasks.
"""

import ast
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict


@dataclass
class ScriptCapability:
    """Detected capabilities of a script."""
    script_path: str
    parameters: List[Dict[str, any]]
    input_formats: List[str]
    output_formats: List[str]
    dependencies: List[str]
    functions: List[str]
    has_error_handling: bool
    has_validation: bool


class CodeCapabilityDetector:
    """Detects actual capabilities of code files."""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.cache = {}

    def analyze_python_script(self, script_path: Path) -> ScriptCapability:
        """Analyze a Python script to detect its capabilities."""

        if not script_path.exists():
            return self._empty_capability(str(script_path))

        # Check cache
        cache_key = str(script_path)
        if cache_key in self.cache:
            return self.cache[cache_key]

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return self._empty_capability(str(script_path))

        # Extract capabilities
        parameters = self._extract_parameters(tree, content)
        input_formats = self._detect_input_formats(content)
        output_formats = self._detect_output_formats(content)
        dependencies = self._extract_dependencies(tree)
        functions = self._extract_functions(tree)
        has_error_handling = self._has_error_handling(tree)
        has_validation = self._has_validation(content)

        capability = ScriptCapability(
            script_path=str(script_path),
            parameters=parameters,
            input_formats=input_formats,
            output_formats=output_formats,
            dependencies=dependencies,
            functions=functions,
            has_error_handling=has_error_handling,
            has_validation=has_validation
        )

        # Cache result
        self.cache[cache_key] = capability
        return capability

    def _empty_capability(self, script_path: str) -> ScriptCapability:
        """Return empty capability for missing/invalid scripts."""
        return ScriptCapability(
            script_path=script_path,
            parameters=[],
            input_formats=[],
            output_formats=[],
            dependencies=[],
            functions=[],
            has_error_handling=False,
            has_validation=False
        )

    def _extract_parameters(self, tree: ast.AST, content: str) -> List[Dict]:
        """Extract command-line parameters from argparse usage."""
        parameters = []

        # Find ArgumentParser.add_argument calls
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check if it's add_argument
                if (isinstance(node.func, ast.Attribute) and
                    node.func.attr == 'add_argument'):

                    param = self._parse_add_argument(node)
                    if param:
                        parameters.append(param)

        return parameters

    def _parse_add_argument(self, node: ast.Call) -> Optional[Dict]:
        """Parse an add_argument call to extract parameter info."""
        param = {}

        # Get parameter name (first positional argument)
        if node.args:
            first_arg = node.args[0]
            if isinstance(first_arg, ast.Constant):
                param['name'] = first_arg.value
            elif isinstance(first_arg, ast.Str):  # Python 3.7 compatibility
                param['name'] = first_arg.s

        # Get keyword arguments
        for keyword in node.keywords:
            key = keyword.arg
            value = keyword.value

            if key == 'help' and isinstance(value, (ast.Constant, ast.Str)):
                param['help'] = value.value if isinstance(value, ast.Constant) else value.s
            elif key == 'required' and isinstance(value, ast.Constant):
                param['required'] = value.value
            elif key == 'default':
                if isinstance(value, ast.Constant):
                    param['default'] = value.value
                elif isinstance(value, ast.Str):
                    param['default'] = value.s
                elif isinstance(value, ast.Num):
                    param['default'] = value.n
            elif key == 'choices':
                if isinstance(value, ast.List):
                    choices = []
                    for elt in value.elts:
                        if isinstance(elt, ast.Constant):
                            choices.append(elt.value)
                        elif isinstance(elt, ast.Str):
                            choices.append(elt.s)
                    param['choices'] = choices
            elif key == 'type':
                if isinstance(value, ast.Name):
                    param['type'] = value.id

        return param if param else None

    def _detect_input_formats(self, content: str) -> List[str]:
        """Detect supported input formats."""
        formats = set()

        # Check for file format handling
        if 'json.load' in content or 'json.loads' in content:
            formats.add('json')
        if 'yaml.load' in content or 'yaml.safe_load' in content:
            formats.add('yaml')
        if 'csv.reader' in content or 'csv.DictReader' in content:
            formats.add('csv')
        if 'xml.etree' in content or 'lxml' in content:
            formats.add('xml')
        if re.search(r'\.md["\']', content):
            formats.add('markdown')
        if re.search(r'\.txt["\']', content):
            formats.add('text')

        return sorted(formats)

    def _detect_output_formats(self, content: str) -> List[str]:
        """Detect supported output formats."""
        formats = set()

        # Check for output format handling
        if 'json.dump' in content or 'json.dumps' in content:
            formats.add('json')
        if 'yaml.dump' in content:
            formats.add('yaml')
        if 'csv.writer' in content or 'csv.DictWriter' in content:
            formats.add('csv')
        if 'print(' in content:
            formats.add('text')

        return sorted(formats)

    def _extract_dependencies(self, tree: ast.AST) -> List[str]:
        """Extract imported dependencies."""
        dependencies = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dependencies.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    dependencies.add(node.module.split('.')[0])

        # Filter out standard library
        stdlib = {'os', 'sys', 're', 'json', 'datetime', 'time', 'pathlib',
                  'argparse', 'subprocess', 'collections', 'itertools'}

        return sorted(dependencies - stdlib)

    def _extract_functions(self, tree: ast.AST) -> List[str]:
        """Extract function names."""
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_'):  # Skip private functions
                    functions.append(node.name)

        return functions

    def _has_error_handling(self, tree: ast.AST) -> bool:
        """Check if script has error handling."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                return True
        return False

    def _has_validation(self, content: str) -> bool:
        """Check if script has input validation."""
        validation_patterns = [
            r'if\s+not\s+',
            r'assert\s+',
            r'raise\s+ValueError',
            r'raise\s+TypeError',
            r'\.exists\(\)',
        ]

        for pattern in validation_patterns:
            if re.search(pattern, content):
                return True

        return False

    def analyze_skill(self, skill_path: Path) -> Dict[str, ScriptCapability]:
        """Analyze all scripts in a skill directory."""
        capabilities = {}

        # Find all Python scripts
        scripts_dir = skill_path / "scripts"
        if scripts_dir.exists():
            for script in scripts_dir.glob("*.py"):
                capability = self.analyze_python_script(script)
                capabilities[script.name] = capability

        return capabilities

    def generate_report(
        self,
        capabilities: Dict[str, ScriptCapability]
    ) -> str:
        """Generate a capability report."""
        report = ["# Code Capability Analysis\n"]

        for script_name, capability in capabilities.items():
            report.append(f"\n## {script_name}\n")

            # Parameters
            if capability.parameters:
                report.append("\n### Parameters\n")
                for param in capability.parameters:
                    name = param.get('name', 'unknown')
                    required = param.get('required', False)
                    req_str = " (required)" if required else ""
                    report.append(f"- `{name}`{req_str}")

                    if 'help' in param:
                        report.append(f"  - {param['help']}")
                    if 'choices' in param:
                        report.append(f"  - Choices: {', '.join(map(str, param['choices']))}")
                    if 'default' in param:
                        report.append(f"  - Default: `{param['default']}`")
                    report.append("")

            # Formats
            if capability.input_formats:
                report.append(f"\n**Input Formats:** {', '.join(capability.input_formats)}\n")
            if capability.output_formats:
                report.append(f"**Output Formats:** {', '.join(capability.output_formats)}\n")

            # Dependencies
            if capability.dependencies:
                report.append(f"\n**Dependencies:** {', '.join(capability.dependencies)}\n")

            # Quality indicators
            report.append("\n**Code Quality:**\n")
            report.append(f"- Error handling: {'✓' if capability.has_error_handling else '✗'}\n")
            report.append(f"- Input validation: {'✓' if capability.has_validation else '✗'}\n")

        return '\n'.join(report)


def main():
    """CLI entry point."""
    import sys
    import yaml

    if len(sys.argv) < 2:
        print("Usage: python code_capability_detector.py <skill_path> [work_dir]")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    work_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()

    # Load config
    config_path = work_dir / "config.yaml"
    config = {}
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f).get('code_capability', {})

    # Analyze skill
    detector = CodeCapabilityDetector(config)
    capabilities = detector.analyze_skill(skill_path)

    # Generate report
    report = detector.generate_report(capabilities)

    # Save report
    report_path = work_dir / "code_capabilities.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Code capability analysis saved to {report_path}")
    print(f"  Analyzed {len(capabilities)} script(s)")

    # Save JSON
    json_path = work_dir / "code_capabilities.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(
            {k: asdict(v) for k, v in capabilities.items()},
            f,
            indent=2
        )


if __name__ == "__main__":
    main()
