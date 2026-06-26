#!/usr/bin/env python3
"""
Command Optimizer for Skills with Executable Commands

Extends Training-Free GRPO to optimize not just markdown documentation,
but also the executable commands within skills.

Key capabilities:
1. Extract and analyze commands from SKILL.md
2. Execute commands and analyze failures
3. Use LLM to generate improved command variants
4. Test variants and select best performing ones
5. Update SKILL.md with optimized commands
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


@dataclass
class CommandInfo:
    """Information about a command found in SKILL.md."""
    original_text: str
    line_start: int
    line_end: int
    context: str  # Surrounding text for context
    execution_result: Optional[Dict] = None


class CommandOptimizer:
    """Optimizes executable commands within skills."""

    def __init__(self, skill_path: Path, work_dir: Path):
        self.skill_path = skill_path
        self.work_dir = work_dir
        self.skill_md_path = skill_path / "SKILL.md"

        # Initialize Anthropic client
        self.client = None
        if ANTHROPIC_AVAILABLE:
            # Support both API key and auth token
            auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
            base_url = os.environ.get("ANTHROPIC_BASE_URL")
            api_key = os.environ.get("ANTHROPIC_API_KEY")

            if auth_token:
                # Use auth token with custom base URL
                self.client = anthropic.Anthropic(
                    api_key=auth_token,
                    base_url=base_url if base_url else None,
                    timeout=120.0  # 2 minutes timeout
                )
            elif api_key:
                # Use standard API key
                self.client = anthropic.Anthropic(api_key=api_key, timeout=120.0)

        self.commands = []
        self.skill_content = ""

    def extract_commands(self) -> List[CommandInfo]:
        """Extract executable commands from SKILL.md."""
        with open(self.skill_md_path, 'r', encoding='utf-8') as f:
            self.skill_content = f.read()

        commands = []
        lines = self.skill_content.split('\n')

        # Find code blocks with bash/shell commands
        in_code_block = False
        code_block_start = -1
        code_block_lines = []

        for i, line in enumerate(lines):
            if line.strip().startswith('```bash') or line.strip().startswith('```sh'):
                in_code_block = True
                code_block_start = i
                code_block_lines = []
            elif line.strip() == '```' and in_code_block:
                # End of code block
                if code_block_lines:
                    # Get context (5 lines before)
                    context_start = max(0, code_block_start - 5)
                    context = '\n'.join(lines[context_start:code_block_start])

                    command_text = '\n'.join(code_block_lines)

                    # Skip commands with placeholders or multiple commands
                    if '<' in command_text or '>' in command_text or len(code_block_lines) > 3:
                        # These are example/template commands, not executable
                        in_code_block = False
                        code_block_lines = []
                        continue

                    commands.append(CommandInfo(
                        original_text=command_text,
                        line_start=code_block_start + 1,
                        line_end=i,
                        context=context
                    ))

                in_code_block = False
                code_block_lines = []
            elif in_code_block:
                code_block_lines.append(line)

        self.commands = commands
        return commands

    def execute_command(self, command: str, timeout: int = 30) -> Dict:
        """Execute a command and capture results."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.work_dir
            )

            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'output_length': len(result.stdout) + len(result.stderr)
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'returncode': -1,
                'stdout': '',
                'stderr': 'Command timed out',
                'output_length': 0
            }
        except Exception as e:
            return {
                'success': False,
                'returncode': -1,
                'stdout': '',
                'stderr': str(e),
                'output_length': 0
            }

    def analyze_command_failure(self, cmd_info: CommandInfo) -> str:
        """Use LLM to analyze why a command failed or produced poor output."""
        if not self.client:
            return "LLM not available for analysis"

        exec_result = cmd_info.execution_result

        prompt = f"""Analyze this command from a skill documentation and its execution result.

**Context from SKILL.md:**
{cmd_info.context}

**Command:**
```bash
{cmd_info.original_text}
```

**Execution Result:**
- Success: {exec_result['success']}
- Return Code: {exec_result['returncode']}
- Output Length: {exec_result['output_length']} bytes
- Stdout: {exec_result['stdout'][:500]}
- Stderr: {exec_result['stderr'][:500]}

**Analysis Required:**
1. Is this command appropriate for testing/demonstrating the skill?
2. Why did it produce minimal/invalid output?
3. What would be a better command to demonstrate the skill's capabilities?

Provide a concise analysis (3-4 sentences):"""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Warning: Failed to analyze command (attempt {attempt + 1}/{max_retries}): {e}")
                    import time
                    time.sleep(2)
                else:
                    print(f"Error: Failed to analyze command after {max_retries} attempts: {e}")
                    return None

    def generate_improved_command(self, cmd_info: CommandInfo, analysis: str) -> str:
        """Use LLM to generate an improved command."""
        if not self.client:
            return cmd_info.original_text

        prompt = f"""Generate an improved command for this skill documentation.

**Context:**
{cmd_info.context}

**Original Command:**
```bash
{cmd_info.original_text}
```

**Analysis of Issues:**
{analysis}

**Requirements:**
1. The command should demonstrate the skill's core functionality
2. It should produce meaningful, verifiable output
3. It should be safe to execute in a test environment
4. Keep it simple and focused on one clear task

Provide ONLY the improved bash command (no explanation):"""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Warning: Failed to generate improved command (attempt {attempt + 1}/{max_retries}): {e}")
                    import time
                    time.sleep(2)
                else:
                    print(f"Error: Failed to generate improved command after {max_retries} attempts: {e}")
                    return None
            )
            improved = response.content[0].text.strip()
            # Remove markdown code blocks if present
            improved = re.sub(r'```bash\n?', '', improved)
            improved = re.sub(r'```\n?', '', improved)
            return improved.strip()
        except Exception as e:
            print(f"Failed to generate improved command: {e}")
            return cmd_info.original_text

    def optimize_commands(self) -> Dict:
        """Main optimization loop for commands."""
        print("\n" + "="*60)
        print("Command Optimization")
        print("="*60)

        # Extract commands
        commands = self.extract_commands()
        print(f"✓ Found {len(commands)} command blocks")

        if not commands:
            print("⚠ No commands found to optimize")
            return {'improved': False, 'commands_optimized': 0}

        # Test each command
        print("\n=== Testing Original Commands ===")
        improvements = []

        for i, cmd_info in enumerate(commands, 1):
            print(f"\nCommand {i}/{len(commands)}:")
            print(f"  {cmd_info.original_text[:60]}...")

            # Execute original
            result = self.execute_command(cmd_info.original_text)
            cmd_info.execution_result = result

            print(f"  Result: {'✓' if result['success'] else '✗'} "
                  f"({result['output_length']} bytes output)")

            # Analyze if output is poor
            if result['output_length'] < 100 or not result['success']:
                print("  → Analyzing failure...")
                analysis = self.analyze_command_failure(cmd_info)

                if analysis is None:
                    print("  ✗ Failed to analyze command, skipping improvement")
                    continue

                print(f"  Analysis: {analysis[:100]}...")

                # Generate improved version
                print("  → Generating improved command...")
                improved_cmd = self.generate_improved_command(cmd_info, analysis)

                if improved_cmd is None:
                    print("  ✗ Failed to generate improved command, skipping")
                    continue

                # Test improved version
                improved_result = self.execute_command(improved_cmd)
                print(f"  Improved: {'✓' if improved_result['success'] else '✗'} "
                      f"({improved_result['output_length']} bytes output)")

                # Keep if better
                if improved_result['output_length'] > result['output_length']:
                    improvements.append({
                        'original': cmd_info.original_text,
                        'improved': improved_cmd,
                        'line_start': cmd_info.line_start,
                        'line_end': cmd_info.line_end,
                        'original_output': result['output_length'],
                        'improved_output': improved_result['output_length']
                    })
                    print("  ✓ Improvement accepted")
                else:
                    print("  ✗ No improvement, keeping original")

        # Apply improvements to SKILL.md
        if improvements:
            print(f"\n=== Applying {len(improvements)} Improvements ===")
            self._apply_improvements(improvements)

        return {
            'improved': len(improvements) > 0,
            'commands_optimized': len(improvements),
            'total_commands': len(commands),
            'improvements': improvements
        }

    def _apply_improvements(self, improvements: List[Dict]):
        """Apply command improvements to SKILL.md."""
        lines = self.skill_content.split('\n')

        # Sort by line number (descending) to avoid offset issues
        improvements.sort(key=lambda x: x['line_start'], reverse=True)

        for imp in improvements:
            # Replace the command lines
            start = imp['line_start']
            end = imp['line_end']

            # Keep the code block markers
            new_lines = [imp['improved']]
            lines[start:end-1] = new_lines

        # Write back
        new_content = '\n'.join(lines)
        with open(self.skill_md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✓ Updated {self.skill_md_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: command_optimizer.py <skill_path> <work_dir>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    work_dir = Path(sys.argv[2])

    optimizer = CommandOptimizer(skill_path, work_dir)
    result = optimizer.optimize_commands()

    print("\n" + "="*60)
    print("Command Optimization Complete")
    print("="*60)
    print(f"Commands optimized: {result['commands_optimized']}/{result['total_commands']}")

    sys.exit(0 if result['improved'] else 1)


if __name__ == "__main__":
    main()
