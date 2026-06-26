"""
Multi-Level Optimizer for Skills-Coach v2.3.1

Optimizes both SKILL.md and associated code files.
"""

from pathlib import Path
from typing import Dict, List, Tuple
import re


class MultiLevelOptimizer:
    """Optimize SKILL.md, code, and configuration files."""

    def __init__(self, skill_dir: Path):
        self.skill_dir = Path(skill_dir)
        self.optimization_targets = self.identify_optimization_targets()

    def identify_optimization_targets(self) -> Dict[str, List[Path]]:
        """
        Scan skill directory for optimization targets.

        Returns:
            Dictionary mapping file types to file paths
        """
        targets = {
            'skill_md': [],
            'python_scripts': [],
            'shell_scripts': [],
            'config_files': []
        }

        if not self.skill_dir.exists():
            return targets

        # SKILL.md
        skill_md = self.skill_dir / "SKILL.md"
        if skill_md.exists():
            targets['skill_md'].append(skill_md)

        # Python files
        for py_file in self.skill_dir.rglob("*.py"):
            if not py_file.name.startswith('.') and '__pycache__' not in str(py_file):
                targets['python_scripts'].append(py_file)

        # Shell scripts
        for sh_file in self.skill_dir.rglob("*.sh"):
            if not sh_file.name.startswith('.'):
                targets['shell_scripts'].append(sh_file)

        # Config files
        for pattern in ['*.yaml', '*.yml', '*.json', '*.toml', '*.ini']:
            for config_file in self.skill_dir.rglob(pattern):
                if not config_file.name.startswith('.'):
                    targets['config_files'].append(config_file)

        return targets

    def analyze_code_issues(self, file_path: Path) -> List[Dict]:
        """
        Analyze code file for potential issues.

        Args:
            file_path: Path to code file

        Returns:
            List of identified issues
        """
        issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Check for missing error handling
            if file_path.suffix == '.py':
                if 'try:' not in content and ('open(' in content or 'requests.' in content):
                    issues.append({
                        'type': 'missing_error_handling',
                        'severity': 'high',
                        'description': 'File operations or network calls without try-except',
                        'suggestion': 'Add try-except blocks around risky operations'
                    })

                # Check for missing input validation
                if 'def ' in content and 'if not' not in content and 'assert' not in content:
                    issues.append({
                        'type': 'missing_validation',
                        'severity': 'medium',
                        'description': 'Functions without input validation',
                        'suggestion': 'Add input validation at function entry points'
                    })

                # Check for potential performance issues
                if re.search(r'for .+ in .+:\s+for .+ in', content):
                    issues.append({
                        'type': 'nested_loops',
                        'severity': 'medium',
                        'description': 'Nested loops detected - potential O(n²) complexity',
                        'suggestion': 'Consider using list comprehensions or vectorized operations'
                    })

            elif file_path.suffix == '.sh':
                if 'set -e' not in content:
                    issues.append({
                        'type': 'missing_error_exit',
                        'severity': 'high',
                        'description': 'Shell script without "set -e"',
                        'suggestion': 'Add "set -e" to exit on errors'
                    })

        except Exception as e:
            issues.append({
                'type': 'analysis_error',
                'severity': 'low',
                'description': f'Could not analyze file: {e}',
                'suggestion': 'Manual review recommended'
            })

        return issues

    def generate_code_variants(
        self,
        iteration: int,
        failures: List[Dict]
    ) -> List[Dict]:
        """
        Generate code-level optimization variants.

        Args:
            iteration: Current iteration number
            failures: List of task failures from previous iteration

        Returns:
            List of variant specifications
        """
        variants = []

        # Analyze failures to determine what needs fixing
        failure_types = {}
        for failure in failures:
            error_type = failure.get('error_type', 'unknown')
            failure_types[error_type] = failure_types.get(error_type, 0) + 1

        # Variant 1: SKILL.md optimization (always included)
        variants.append({
            'type': 'skill_md_only',
            'target': 'SKILL.md',
            'mutations': ['validation', 'error_handling', 'examples'],
            'description': 'Standard SKILL.md improvements'
        })

        # Variant 2: Add caching if timeout issues
        if 'timeout' in failure_types or 'performance' in failure_types:
            for py_file in self.optimization_targets['python_scripts']:
                variants.append({
                    'type': 'code_optimization',
                    'target': str(py_file),
                    'mutation': 'add_caching',
                    'description': f'Add caching to {py_file.name} to reduce redundant operations'
                })

        # Variant 3: Add validation if validation errors
        if 'validation' in failure_types or 'invalid_input' in failure_types:
            for py_file in self.optimization_targets['python_scripts']:
                issues = self.analyze_code_issues(py_file)
                if any(i['type'] == 'missing_validation' for i in issues):
                    variants.append({
                        'type': 'code_fix',
                        'target': str(py_file),
                        'mutation': 'add_input_validation',
                        'description': f'Add input validation to {py_file.name}'
                    })

        # Variant 4: Add error handling if execution errors
        if 'error' in failure_types or 'exception' in failure_types:
            for py_file in self.optimization_targets['python_scripts']:
                issues = self.analyze_code_issues(py_file)
                if any(i['type'] == 'missing_error_handling' for i in issues):
                    variants.append({
                        'type': 'code_fix',
                        'target': str(py_file),
                        'mutation': 'add_error_handling',
                        'description': f'Add error handling to {py_file.name}'
                    })

        return variants[:4]  # Return top 4 variants

    def apply_code_mutation(
        self,
        file_path: Path,
        mutation: str
    ) -> Tuple[str, str]:
        """
        Apply code-level mutation.

        Args:
            file_path: Path to file to mutate
            mutation: Type of mutation to apply

        Returns:
            Tuple of (original_content, mutated_content)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()

        mutated = original

        if mutation == 'add_caching':
            mutated = self._add_caching(original, file_path.suffix)

        elif mutation == 'add_input_validation':
            mutated = self._add_validation(original, file_path.suffix)

        elif mutation == 'add_error_handling':
            mutated = self._add_error_handling(original, file_path.suffix)

        elif mutation == 'optimize_algorithm':
            mutated = self._optimize_algorithm(original, file_path.suffix)

        return original, mutated

    def _add_caching(self, content: str, file_ext: str) -> str:
        """Add caching to code."""
        if file_ext == '.py':
            # Add functools.lru_cache import if not present
            if 'from functools import' not in content:
                content = 'from functools import lru_cache\n' + content

            # Add @lru_cache decorator to functions that look cacheable
            lines = content.split('\n')
            result = []
            for i, line in enumerate(lines):
                if line.strip().startswith('def ') and 'self' not in line:
                    # Check if not already cached
                    if i == 0 or '@lru_cache' not in lines[i-1]:
                        result.append('    @lru_cache(maxsize=128)')
                result.append(line)

            content = '\n'.join(result)

        return content

    def _add_validation(self, content: str, file_ext: str) -> str:
        """Add input validation."""
        if file_ext == '.py':
            # Add validation at function entry points
            lines = content.split('\n')
            result = []

            for i, line in enumerate(lines):
                result.append(line)

                # After function definition, add validation
                if line.strip().startswith('def ') and '(' in line:
                    # Extract parameters
                    params = re.search(r'\((.*?)\)', line)
                    if params:
                        param_list = [p.strip().split(':')[0].strip() for p in params.group(1).split(',') if p.strip() and p.strip() != 'self']

                        # Add validation for each parameter
                        indent = '    ' * (len(line) - len(line.lstrip()) // 4 + 1)
                        for param in param_list:
                            if param:
                                result.append(f'{indent}if {param} is None:')
                                result.append(f'{indent}    raise ValueError(f"{param} cannot be None")')

            content = '\n'.join(result)

        return content

    def _add_error_handling(self, content: str, file_ext: str) -> str:
        """Add error handling."""
        if file_ext == '.py':
            # Wrap risky operations in try-except
            lines = content.split('\n')
            result = []
            in_try = False

            for line in lines:
                # Detect risky operations
                if any(keyword in line for keyword in ['open(', 'requests.', 'json.load', 'subprocess.']):
                    if not in_try:
                        indent = line[:len(line) - len(line.lstrip())]
                        result.append(f'{indent}try:')
                        in_try = True

                result.append(line)

                # Close try block after risky operation
                if in_try and line.strip() and not line.strip().startswith('#'):
                    indent = line[:len(line) - len(line.lstrip())]
                    result.append(f'{indent}except Exception as e:')
                    result.append(f'{indent}    print(f"Error: {{e}}")')
                    result.append(f'{indent}    raise')
                    in_try = False

            content = '\n'.join(result)

        elif file_ext == '.sh':
            # Add set -e if not present
            if 'set -e' not in content:
                lines = content.split('\n')
                # Insert after shebang
                if lines and lines[0].startswith('#!'):
                    lines.insert(1, 'set -e  # Exit on error')
                else:
                    lines.insert(0, 'set -e  # Exit on error')
                content = '\n'.join(lines)

        return content

    def _optimize_algorithm(self, content: str, file_ext: str) -> str:
        """Optimize algorithms."""
        if file_ext == '.py':
            # Replace nested loops with list comprehensions where possible
            content = re.sub(
                r'for (\w+) in (\w+):\s+for (\w+) in (\w+):\s+(\w+)\.append\((.+?)\)',
                r'\5 = [\6 for \1 in \2 for \3 in \4]',
                content
            )

        return content

    def get_optimization_summary(self) -> str:
        """Generate summary of optimization targets."""
        summary = "# Multi-Level Optimization Targets\n\n"

        for file_type, files in self.optimization_targets.items():
            if files:
                summary += f"## {file_type.replace('_', ' ').title()}\n\n"
                for file_path in files:
                    summary += f"- `{file_path.relative_to(self.skill_dir)}`\n"

                    # Analyze issues
                    if file_type in ['python_scripts', 'shell_scripts']:
                        issues = self.analyze_code_issues(file_path)
                        if issues:
                            for issue in issues:
                                summary += f"  - ⚠️ {issue['description']} ({issue['severity']})\n"

                summary += "\n"

        return summary


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python multi_level_optimizer.py <skill-directory>")
        sys.exit(1)

    skill_dir = Path(sys.argv[1])
    optimizer = MultiLevelOptimizer(skill_dir)

    print(optimizer.get_optimization_summary())

    print("\n" + "="*60)
    print("Sample Code Variants:")
    variants = optimizer.generate_code_variants(1, [
        {'error_type': 'timeout'},
        {'error_type': 'validation'}
    ])

    for i, variant in enumerate(variants, 1):
        print(f"\n{i}. {variant['description']}")
        print(f"   Type: {variant['type']}")
        print(f"   Target: {variant['target']}")
