#!/usr/bin/env python3
"""
Auto-Fixer for Skills-Coach v2.3.1

Automatically fixes common issues detected during optimization:
1. Missing dependencies
2. Script execution errors
3. Missing parameters
4. File path issues
5. Logic errors

Integrates with failure-analyzer to apply fixes automatically.
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


@dataclass
class FixResult:
    """Result of applying a fix."""
    success: bool
    fix_type: str
    description: str
    files_modified: List[str]
    error_message: Optional[str] = None


class AutoFixer:
    """Automatically fixes common skill issues."""

    def __init__(self, skill_path: Path, config: Optional[Dict] = None):
        self.skill_path = skill_path
        self.config = config or {}
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        self.client = None

        if ANTHROPIC_AVAILABLE and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)

    def analyze_and_fix(self, failure_analyses: List[Dict]) -> List[FixResult]:
        """Analyze failures and apply fixes automatically."""
        results = []

        # Group failures by category
        by_category = {}
        for analysis in failure_analyses:
            category = analysis.get('error_category', 'unknown')
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(analysis)

        # Apply fixes by priority
        priority_order = [
            'missing_dependency',
            'missing_parameter',
            'file_not_found',
            'invalid_input',
            'logic_error'
        ]

        for category in priority_order:
            if category in by_category:
                fix_result = self._fix_category(category, by_category[category])
                if fix_result:
                    results.append(fix_result)

        return results

    def _fix_category(self, category: str, analyses: List[Dict]) -> Optional[FixResult]:
        """Fix all issues in a specific category."""
        if category == 'missing_dependency':
            return self._fix_missing_dependencies(analyses)
        elif category == 'missing_parameter':
            return self._fix_missing_parameters(analyses)
        elif category == 'file_not_found':
            return self._fix_file_paths(analyses)
        elif category == 'logic_error':
            return self._fix_logic_errors(analyses)
        return None

    def _fix_missing_dependencies(self, analyses: List[Dict]) -> Optional[FixResult]:
        """Fix missing dependencies by updating requirements.txt or SKILL.md."""
        dependencies = set()

        for analysis in analyses:
            # Extract module name from error message
            match = re.search(r"No module named '(.+?)'", analysis.get('error_message', ''))
            if match:
                dependencies.add(match.group(1))

            # Also check root cause
            match = re.search(r"Required Python module is not installed: (.+)",
                            analysis.get('root_cause', ''))
            if match:
                dependencies.add(match.group(1))

        if not dependencies:
            return None

        modified_files = []

        # Try to add to requirements.txt
        requirements_path = self.skill_path / "requirements.txt"
        try:
            if requirements_path.exists():
                with open(requirements_path, 'r') as f:
                    existing = set(line.strip() for line in f if line.strip())

                new_deps = dependencies - existing
                if new_deps:
                    with open(requirements_path, 'a') as f:
                        for dep in sorted(new_deps):
                            f.write(f"\n{dep}")
                    modified_files.append(str(requirements_path))
            else:
                # Create new requirements.txt
                requirements_path.parent.mkdir(parents=True, exist_ok=True)
                with open(requirements_path, 'w') as f:
                    for dep in sorted(dependencies):
                        f.write(f"{dep}\n")
                modified_files.append(str(requirements_path))
        except Exception as e:
            print(f"  ⚠ Failed to update requirements.txt: {e}")

        # Update SKILL.md to mention dependencies
        skill_md = self.skill_path / "SKILL.md"
        if skill_md.exists():
            with open(skill_md, 'r') as f:
                content = f.read()

            # Check if there's already a dependencies section
            if '## Dependencies' not in content and '## Requirements' not in content:
                # Add dependencies section
                deps_section = "\n## Dependencies\n\n```bash\n"
                for dep in sorted(dependencies):
                    deps_section += f"pip install {dep}\n"
                deps_section += "```\n"

                # Insert after frontmatter if exists
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        content = f"---{parts[1]}---{deps_section}{parts[2]}"
                    else:
                        content = deps_section + content
                else:
                    content = deps_section + content

                with open(skill_md, 'w') as f:
                    f.write(content)
                modified_files.append(str(skill_md))

        return FixResult(
            success=True,
            fix_type='missing_dependency',
            description=f"Added {len(dependencies)} missing dependencies: {', '.join(sorted(dependencies))}",
            files_modified=modified_files
        )

    def _fix_missing_parameters(self, analyses: List[Dict]) -> Optional[FixResult]:
        """Fix missing parameters in scripts using LLM."""
        if not self.client:
            return None

        # Find the script files that need fixing
        script_files = set()
        missing_params = {}

        for analysis in analyses:
            # Extract parameter name
            match = re.search(r"unrecognized arguments?: (.+)", analysis.get('error_message', ''))
            if match:
                param = match.group(1).strip()
                task_id = analysis.get('task_id', '')

                # Try to find which script was executed
                # This would need to be extracted from execution logs
                script_files.add("scripts/*.py")  # Placeholder

                if param not in missing_params:
                    missing_params[param] = []
                missing_params[param].append(task_id)

        if not missing_params:
            return None

        # Use LLM to suggest parameter additions
        modified_files = []

        for script_pattern in script_files:
            for script_path in self.skill_path.glob(script_pattern):
                if script_path.suffix == '.py':
                    fix_applied = self._add_parameters_to_script(script_path, missing_params)
                    if fix_applied:
                        modified_files.append(str(script_path))

        if modified_files:
            return FixResult(
                success=True,
                fix_type='missing_parameter',
                description=f"Added missing parameters: {', '.join(missing_params.keys())}",
                files_modified=modified_files
            )

        return None

    def _add_parameters_to_script(self, script_path: Path, params: Dict[str, List[str]]) -> bool:
        """Add missing parameters to a Python script."""
        if not self.client:
            return False

        with open(script_path, 'r') as f:
            original_code = f.read()

        # Use LLM to add parameters
        prompt = f"""You are fixing a Python script that is missing command-line parameters.

Original script:
```python
{original_code}
```

Missing parameters that need to be added:
{json.dumps(params, indent=2)}

Please add these parameters to the argparse section. Return ONLY the complete modified Python code, no explanations.
"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            fixed_code = response.content[0].text

            # Extract code from markdown if present
            if '```python' in fixed_code:
                fixed_code = re.search(r'```python\n(.*?)\n```', fixed_code, re.DOTALL)
                if fixed_code:
                    fixed_code = fixed_code.group(1)

            # Validate the fixed code
            try:
                compile(fixed_code, script_path.name, 'exec')
                with open(script_path, 'w') as f:
                    f.write(fixed_code)
                return True
            except SyntaxError:
                return False

        except Exception as e:
            print(f"  ⚠ Failed to fix {script_path.name}: {e}")
            return False

    def _fix_file_paths(self, analyses: List[Dict]) -> Optional[FixResult]:
        """Fix file path issues."""
        # This is tricky - we'd need to understand the context
        # For now, just document the issue
        return None

    def _fix_logic_errors(self, analyses: List[Dict]) -> Optional[FixResult]:
        """Fix logic errors using LLM."""
        if not self.client:
            return None

        # Extract error details
        errors = []
        for analysis in analyses:
            errors.append({
                'task_id': analysis.get('task_id'),
                'error': analysis.get('error_message'),
                'root_cause': analysis.get('root_cause')
            })

        # Use LLM to suggest fixes
        # This would require reading the relevant code files
        # and applying intelligent fixes

        return None


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python auto_fixer.py <skill_path> <failure_analysis.json>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    analysis_file = Path(sys.argv[2])

    # Load failure analyses
    with open(analysis_file, 'r') as f:
        analyses = json.load(f)

    # Apply fixes
    fixer = AutoFixer(skill_path)
    results = fixer.analyze_and_fix(analyses)

    # Report results
    print("\n" + "="*60)
    print("Auto-Fix Results")
    print("="*60)

    for result in results:
        status = "✓" if result.success else "✗"
        print(f"{status} {result.fix_type}: {result.description}")
        if result.files_modified:
            print(f"  Modified: {', '.join(result.files_modified)}")
        if result.error_message:
            print(f"  Error: {result.error_message}")

    print(f"\nTotal fixes applied: {len([r for r in results if r.success])}")


if __name__ == "__main__":
    main()
