#!/usr/bin/env python3
"""
Test Template Generator for Skill Scripts

This script analyzes Python scripts in a skill's scripts/ directory
and generates test case templates covering normal, edge, and error cases.

Usage:
    python test_template.py <path/to/skill-directory>

Output:
    Prints test case documentation in markdown format
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional


class ScriptAnalyzer:
    """Analyzes a Python script to extract function signatures and docstrings."""
    
    def __init__(self, script_path: str):
        self.script_path = script_path
        self.script_name = os.path.basename(script_path)
        self.functions: List[Dict[str, Any]] = []
        self.has_main = False
        self.argparse_usage = False
        
    def analyze(self) -> None:
        """Parse the script and extract relevant information."""
        try:
            with open(self.script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Check for argparse usage
            if 'argparse' in content or 'ArgumentParser' in content:
                self.argparse_usage = True
            
            # Check for main block
            if "if __name__ == '__main__':" in content or 'if __name__ == "__main__":' in content:
                self.has_main = True
            
            # Extract function definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = self._extract_function_info(node)
                    if func_info:
                        self.functions.append(func_info)
                        
        except SyntaxError as e:
            print(f"Warning: Syntax error in {self.script_path}: {e}")
        except Exception as e:
            print(f"Warning: Could not analyze {self.script_path}: {e}")
    
    def _extract_function_info(self, node: ast.FunctionDef) -> Optional[Dict[str, Any]]:
        """Extract information about a function."""
        # Skip private functions (starting with _)
        if node.name.startswith('_'):
            return None
            
        args_info = []
        
        # Extract arguments
        args = node.args
        defaults_start = len(args.args) - len(args.defaults)
        
        for i, arg in enumerate(args.args):
            arg_info = {
                'name': arg.arg,
                'has_default': i >= defaults_start,
                'annotation': None
            }
            if arg.annotation and isinstance(arg.annotation, ast.Name):
                arg_info['annotation'] = arg.annotation.id
            args_info.append(arg_info)
        
        # Extract docstring
        docstring = ast.get_docstring(node)
        
        return {
            'name': node.name,
            'args': args_info,
            'docstring': docstring,
            'line_number': node.lineno
        }
    
    def generate_test_cases(self) -> List[Dict[str, Any]]:
        """Generate test case templates based on script analysis."""
        test_cases = []
        
        # If script uses argparse, generate CLI test cases
        if self.argparse_usage or self.has_main:
            test_cases.extend(self._generate_cli_test_cases())
        
        # Generate test cases for each public function
        for func in self.functions:
            test_cases.extend(self._generate_function_test_cases(func))
        
        return test_cases
    
    def _generate_cli_test_cases(self) -> List[Dict[str, Any]]:
        """Generate test cases for CLI scripts."""
        base_name = self.script_name.replace('.py', '')
        
        return [
            {
                'id': f'{base_name}_001',
                'type': 'Normal',
                'description': f'Run {self.script_name} with valid arguments',
                'input': 'Valid arguments/parameters',
                'expected': 'Script executes successfully',
                'command': f'python scripts/{self.script_name} [ARGS]'
            },
            {
                'id': f'{base_name}_002',
                'type': 'Edge',
                'description': f'Run {self.script_name} with minimal/empty input',
                'input': 'Empty or minimal arguments',
                'expected': 'Graceful handling, appropriate message',
                'command': f'python scripts/{self.script_name}'
            },
            {
                'id': f'{base_name}_003',
                'type': 'Error',
                'description': f'Run {self.script_name} with invalid/missing required arguments',
                'input': 'Missing or invalid arguments',
                'expected': 'Error message, non-zero exit code',
                'command': f'python scripts/{self.script_name} --invalid-arg'
            },
            {
                'id': f'{base_name}_004',
                'type': 'Error',
                'description': f'Run {self.script_name} with non-existent file path',
                'input': 'Invalid file path',
                'expected': 'File not found error',
                'command': f'python scripts/{self.script_name} /nonexistent/path'
            }
        ]
    
    def _generate_function_test_cases(self, func: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate test cases for a specific function."""
        func_name = func['name']
        args = func['args']
        required_args = [a for a in args if not a['has_default']]
        optional_args = [a for a in args if a['has_default']]
        
        test_cases = []
        base_id = f"{self.script_name.replace('.py', '')}_{func_name}"
        
        # Normal case - all required args
        test_cases.append({
            'id': f'{base_id}_001',
            'type': 'Normal',
            'description': f'Call {func_name}() with valid required arguments',
            'input': f'Required args: {[a["name"] for a in required_args]}',
            'expected': 'Function returns expected result',
            'command': f'# In Python: {func_name}({", ".join([a["name"] for a in required_args])})'
        })
        
        # Edge case - empty/minimal inputs
        if required_args:
            test_cases.append({
                'id': f'{base_id}_002',
                'type': 'Edge',
                'description': f'Call {func_name}() with empty/minimal inputs',
                'input': 'Empty strings, zero values, empty collections',
                'expected': 'Graceful handling or appropriate error',
                'command': f'# Test with minimal valid inputs'
            })
        
        # Error case - missing required args
        if required_args:
            test_cases.append({
                'id': f'{base_id}_003',
                'type': 'Error',
                'description': f'Call {func_name}() without required arguments',
                'input': 'Missing required args',
                'expected': 'TypeError: missing required argument',
                'command': f'# In Python: {func_name}()  # Should raise TypeError'
            })
        
        # Normal case - with optional args
        if optional_args:
            test_cases.append({
                'id': f'{base_id}_004',
                'type': 'Normal',
                'description': f'Call {func_name}() with all optional arguments',
                'input': f'All args including optional: {[a["name"] for a in args]}',
                'expected': 'Function handles all parameters correctly',
                'command': f'# In Python: {func_name}({", ".join([a["name"] for a in args])})'
            })
        
        return test_cases


def generate_test_documentation(skill_path: str) -> str:
    """Generate complete test documentation for a skill."""
    skill_path = Path(skill_path)
    scripts_dir = skill_path / 'scripts'
    
    if not scripts_dir.exists():
        return f"# Test Documentation\n\nNo scripts/ directory found in {skill_path}"
    
    output = ["# Test Documentation\n"]
    output.append(f"## Skill: {skill_path.name}\n")
    output.append("Auto-generated test cases for skill scripts.\n")
    
    # Find all Python scripts
    python_scripts = list(scripts_dir.glob('*.py'))
    shell_scripts = list(scripts_dir.glob('*.sh'))
    all_scripts = python_scripts + shell_scripts
    
    if not all_scripts:
        output.append("\nNo executable scripts found in scripts/ directory.\n")
        return '\n'.join(output)
    
    output.append(f"\n## Scripts Overview\n")
    output.append(f"Found {len(all_scripts)} script(s):\n")
    for script in all_scripts:
        output.append(f"- `{script.name}`\n")
    
    output.append("\n---\n")
    
    # Analyze each Python script
    for script_path in python_scripts:
        analyzer = ScriptAnalyzer(str(script_path))
        analyzer.analyze()
        test_cases = analyzer.generate_test_cases()
        
        if test_cases:
            output.append(f"\n## {script_path.name}\n")
            
            # Write test case table
            output.append("\n| ID | Type | Description | Input | Expected Output | Command |\n")
            output.append("|----|------|-------------|-------|-----------------|---------|\n")
            
            for tc in test_cases:
                output.append(f"| {tc['id']} | {tc['type']} | {tc['description']} | {tc['input']} | {tc['expected']} | `{tc['command']}` |\n")
    
    # Shell scripts get generic test cases
    for script_path in shell_scripts:
        output.append(f"\n## {script_path.name}\n")
        output.append("\n| ID | Type | Description | Input | Expected Output | Command |\n")
        output.append("|----|------|-------------|-------|-----------------|---------|\n")
        
        base_name = script_path.name.replace('.sh', '')
        test_cases = [
            (f'{base_name}_001', 'Normal', 'Execute with valid arguments', 'Valid args', 'Success', f'bash scripts/{script_path.name} [ARGS]'),
            (f'{base_name}_002', 'Edge', 'Execute with no arguments', 'None', 'Help message or usage', f'bash scripts/{script_path.name}'),
            (f'{base_name}_003', 'Error', 'Execute with invalid arguments', 'Invalid args', 'Error message', f'bash scripts/{script_path.name} --invalid'),
        ]
        
        for tc_id, tc_type, desc, inp, exp, cmd in test_cases:
            output.append(f"| {tc_id} | {tc_type} | {desc} | {inp} | {exp} | `{cmd}` |\n")
    
    output.append("\n---\n")
    output.append("\n## Test Execution\n")
    output.append("\nRun individual tests using the commands above.\n")
    output.append("\n### Prerequisites\n")
    output.append("- Ensure the skill directory is the current working directory\n")
    output.append("- Install any required dependencies\n")
    output.append("- Prepare test data files if needed\n")
    
    return ''.join(output)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python test_template.py <path/to/skill-directory>")
        print("\nGenerates test case documentation for skill scripts.")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    
    if not os.path.isdir(skill_path):
        print(f"Error: {skill_path} is not a valid directory")
        sys.exit(1)
    
    documentation = generate_test_documentation(skill_path)
    print(documentation)


if __name__ == '__main__':
    main()