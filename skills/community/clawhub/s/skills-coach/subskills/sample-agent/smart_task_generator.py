#!/usr/bin/env python3
"""
Smart Task Generator for Skills-Coach v2.3.1

Analyzes target skill's SKILL.md and generates executable test tasks
based on the skill's actual commands and functionality.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
import json

# Import test file manager
try:
    from test_file_manager import TestFileManager
    TEST_FILE_MANAGER_AVAILABLE = True
except ImportError:
    TEST_FILE_MANAGER_AVAILABLE = False
    print("Warning: test_file_manager not available")


@dataclass
class SkillCommand:
    """Represents a command extracted from SKILL.md."""
    name: str
    description: str
    example: str
    parameters: List[str]


@dataclass
class Task:
    """Represents an executable test task."""
    task_id: str
    task_type: str  # "standard", "advanced"
    title: str
    background: str
    objective: str
    command: str  # Actual executable command
    expected_behavior: str
    constraints: List[str]
    workspace_files: Dict[str, str]


@dataclass
class SpecCheckCriterion:
    """Evaluation criterion."""
    description: str
    verification_method: str


@dataclass
class SpecCheck:
    """Evaluation criteria for a task."""
    task_id: str
    criteria: List[SpecCheckCriterion]
    total_points: int
    pass_threshold: int


class SmartTaskGenerator:
    """Generates executable test tasks based on skill analysis."""

    def __init__(self, target_skill_path: str, output_dir: str = ".", config: dict = None):
        self.target_skill_path = Path(target_skill_path)
        self.output_dir = Path(output_dir)
        self.skill_md_content = ""
        self.skill_name = ""
        self.skill_description = ""
        self.commands = []
        self.base_dir = str(target_skill_path)
        self.skill_type = "executable"  # "executable" or "documentation"
        self.config = config or {}

        # Task diversity settings
        task_gen_config = self.config.get('task_generation', {})
        self.local_file_ratio = task_gen_config.get('local_file_ratio', 0.4)
        self.prefer_local_files = self.local_file_ratio > 0.5  # If ratio > 50%, prefer local

        # Inferred file types from SKILL.md analysis
        self.inferred_file_types = []
        self.inferred_input_patterns = []
        self.inferred_output_patterns = []

    def load_and_parse_skill(self) -> bool:
        """Load SKILL.md and extract commands."""
        skill_md_path = self.target_skill_path / "SKILL.md"

        if not skill_md_path.exists():
            print(f"ERROR: SKILL.md not found at {skill_md_path}")
            return False

        with open(skill_md_path, 'r', encoding='utf-8') as f:
            self.skill_md_content = f.read()

        print(f"✓ Loaded SKILL.md from {skill_md_path}")

        # Extract frontmatter FIRST (before extracting commands)
        self._extract_frontmatter()

        # Extract commands from code blocks
        self._extract_commands()

        # Determine skill type
        if not self.commands:
            print("⚠ No executable commands found in SKILL.md")
            print("✓ Detected as documentation-type skill")
            self.skill_type = "documentation"
            return True  # Still valid, just different type

        print(f"✓ Extracted {len(self.commands)} commands")
        self.skill_type = "executable"

        # Analyze SKILL.md to infer file types and patterns
        self._analyze_skill_file_patterns()

        return True

    def _extract_frontmatter(self):
        """Extract skill name and description from frontmatter."""
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', self.skill_md_content, re.DOTALL | re.MULTILINE)

        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)

            name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
            if name_match:
                self.skill_name = name_match.group(1).strip()

            desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
            if desc_match:
                self.skill_description = desc_match.group(1).strip()

    def _analyze_skill_file_patterns(self):
        """Analyze SKILL.md to infer file types and patterns used by this skill."""
        print("✓ Analyzing skill file patterns...")

        # Extract file extensions from code examples
        file_extensions = set()

        # Pattern 1: Look for file extensions in commands (e.g., .pdf, .txt, .json, .png)
        ext_pattern = r'\b\w+\.(pdf|txt|json|yaml|yml|xml|html|css|js|ts|py|java|cpp|c|h|md|csv|png|jpg|jpeg|gif|svg|mp4|mp3|wav|zip|tar|gz|sql|db|xlsx|docx)\b'
        extensions_found = re.findall(ext_pattern, self.skill_md_content, re.IGNORECASE)
        # Filter out numeric-only extensions (e.g., "5" from "v6.5.0")
        file_extensions.update(ext.lower() for ext in extensions_found if not ext.isdigit())

        # Pattern 2: Analyze skill description for domain keywords
        description_lower = (self.skill_name + " " + self.skill_description).lower()

        domain_file_types = {
            'pdf': ['pdf', 'document', 'form', 'fillable'],
            'txt': ['text', 'log', 'note'],
            'json': ['json', 'api', 'config', 'data'],
            'yaml': ['yaml', 'config', 'configuration'],
            'xml': ['xml', 'markup'],
            'html': ['html', 'web', 'page', 'browser'],
            'css': ['css', 'style', 'stylesheet'],
            'js': ['javascript', 'js', 'node'],
            'py': ['python', 'script'],
            'md': ['markdown', 'documentation', 'readme'],
            'csv': ['csv', 'spreadsheet', 'data', 'table'],
            'png': ['image', 'screenshot', 'picture', 'photo', 'png'],
            'jpg': ['image', 'photo', 'picture', 'jpeg'],
            'sql': ['database', 'sql', 'query'],
            'mp4': ['video', 'media', 'movie'],
            'mp3': ['audio', 'sound', 'music'],
        }

        for ext, keywords in domain_file_types.items():
            if any(keyword in description_lower for keyword in keywords):
                file_extensions.add(ext)

        # Pattern 3: Extract actual file names from examples
        # Look for patterns like: input.pdf, test.json, data.csv
        filename_pattern = r'\b([a-zA-Z0-9_-]+\.(pdf|txt|json|yaml|yml|xml|html|css|js|ts|py|java|cpp|c|h|md|csv|png|jpg|jpeg|gif|svg|mp4|mp3|wav|zip|tar|gz|sql|db|xlsx|docx))\b'
        filenames_found = re.findall(filename_pattern, self.skill_md_content, re.IGNORECASE)

        for filename, ext in filenames_found:
            # Filter out numeric-only extensions
            if not ext.isdigit():
                file_extensions.add(ext.lower())
                # Store example filenames as patterns
                if 'input' in filename.lower():
                    self.inferred_input_patterns.append(filename)
                elif 'output' in filename.lower():
                    self.inferred_output_patterns.append(filename)

        # Pattern 4: Analyze command examples to understand input/output patterns
        for cmd_info in self.commands:
            cmd = cmd_info.get('command', '')
            # Extract filenames from command arguments
            tokens = cmd.split()
            for token in tokens:
                if '.' in token and not token.startswith('-'):
                    # Looks like a filename
                    parts = token.rsplit('.', 1)
                    if len(parts) == 2:
                        ext = parts[1].lower()
                        # Remove quotes if present
                        ext = ext.strip('"\'')
                        # Only add if it's a valid extension (alphabetic, 2-5 chars)
                        if len(ext) >= 2 and len(ext) <= 5 and ext.isalpha():
                            file_extensions.add(ext)

        self.inferred_file_types = sorted(list(file_extensions))

        if self.inferred_file_types:
            print(f"  ✓ Inferred file types: {', '.join(self.inferred_file_types)}")
        else:
            print("  ⚠ No specific file types detected, will use generic patterns")

        if self.inferred_input_patterns:
            print(f"  ✓ Example input patterns: {', '.join(self.inferred_input_patterns[:3])}")
        if self.inferred_output_patterns:
            print(f"  ✓ Example output patterns: {', '.join(self.inferred_output_patterns[:3])}")


    def _extract_commands(self):
        """Extract executable commands from code blocks and detect scripts."""
        # Method 1: Find all bash/shell code blocks
        code_blocks = re.findall(r'```(?:bash|shell|sh)\n(.*?)```', self.skill_md_content, re.DOTALL)

        desc = ''
        for block in code_blocks:
            lines = block.strip().split('\n')

            # Handle multi-line commands (with backslash continuation)
            i = 0
            while i < len(lines):
                line = lines[i].strip()

                # Skip empty lines
                if not line:
                    i += 1
                    continue

                # Extract description from comments
                if line.startswith('#') and not line.startswith('##'):
                    desc = line.lstrip('#').strip()
                    i += 1
                    continue

                # IMPROVED: Detect skill-specific commands
                # Try to find commands that start with common CLI tool names or skill name
                skill_cmd_keywords = []
                if self.skill_name:
                    # Add variations of skill name (e.g., "browser" -> "browse")
                    skill_cmd_keywords.append(self.skill_name.lower())
                    # Also try without trailing 'r' or 'er' (browser -> browse)
                    if self.skill_name.endswith('er'):
                        skill_cmd_keywords.append(self.skill_name[:-2].lower())
                    elif self.skill_name.endswith('r'):
                        skill_cmd_keywords.append(self.skill_name[:-1].lower())

                # Check if line starts with a skill command or traditional command
                is_skill_command = any(line.lower().startswith(kw + ' ') for kw in skill_cmd_keywords)
                is_traditional_command = any(cmd in line for cmd in ['uv run', 'python', '.py', 'node', 'npm', 'yarn'])

                # Skip installation/setup commands unless they're the only commands
                is_setup_command = any(pattern in line.lower() for pattern in [
                    'which ', 'npm install', 'pip install', 'apt-get', 'brew install'
                ])

                if is_skill_command or (is_traditional_command and not is_setup_command):
                    # Extract command (remove inline comments)
                    full_command = line.split('#')[0].strip()

                    # Handle multi-line commands with backslash continuation
                    while full_command.endswith('\\') and i + 1 < len(lines):
                        full_command = full_command.rstrip('\\').strip()
                        i += 1
                        next_line = lines[i].strip()
                        if next_line and not next_line.startswith('#'):
                            # Remove inline comment from next line too
                            next_line = next_line.split('#')[0].strip()
                            if next_line:
                                full_command += ' ' + next_line

                    # Replace {baseDir} placeholder
                    full_command = full_command.replace('{baseDir}', self.base_dir)

                    # Expand ~ to full path if it references the skill
                    if '~/.openclaw/skills/' in full_command:
                        skill_name = self.target_skill_path.name
                        full_command = full_command.replace(
                            f'~/.openclaw/skills/{skill_name}',
                            str(self.target_skill_path)
                        )

                    if '~/.openclaw/' in full_command and '/scripts/' in full_command:
                        match = re.search(r'~/\.openclaw/([^/]+)/', full_command)
                        if match:
                            skill_name = match.group(1)
                            full_command = full_command.replace(
                                f'~/.openclaw/{skill_name}',
                                str(self.target_skill_path)
                            )

                    # Clean up extra whitespace
                    full_command = ' '.join(full_command.split())

                    # Skip if command has placeholders like <url>, <ref>, etc.
                    has_placeholders = bool(re.search(r'<[^>]+>', full_command))

                    # Only add if it's a meaningful command
                    is_meaningful = (
                        full_command and
                        not full_command.strip().endswith('--help') and
                        not has_placeholders and  # Skip commands with placeholders for now
                        (not is_setup_command or len(self.commands) == 0)
                    )

                    if is_meaningful:
                        # Avoid duplicates
                        if not any(c['command'] == full_command for c in self.commands):
                            # Extract inline comment as description if present
                            inline_desc = None
                            if '#' in line:
                                inline_desc = line.split('#', 1)[1].strip()

                            self.commands.append({
                                'command': full_command,
                                'description': inline_desc or desc or self._infer_command_description(full_command),
                                'has_required_params': self._check_required_params(full_command),
                                'is_setup': is_setup_command
                            })
                            desc = ''  # Reset description after use

                i += 1

        # Remove setup commands if we have real commands
        real_commands = [c for c in self.commands if not c.get('is_setup', False)]
        if real_commands:
            self.commands = real_commands

        # Method 2: Extract commands from plain text (not in code blocks)
        # Look for multi-line commands with backslash continuation
        # Pattern: python3 {baseDir}/scripts/file.py \
        #            --arg1 value1 --arg2 value2

        # First, find all potential command starts
        lines = self.skill_md_content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Look for command start patterns
            if re.match(r'^\s*(?:python3?|node|npm|yarn)\s+(?:\{baseDir\}|~/.openclaw/)', line):
                full_command = line

                # Handle backslash continuation
                while full_command.rstrip().endswith('\\') and i + 1 < len(lines):
                    # Remove the backslash and add next line
                    full_command = full_command.rstrip().rstrip('\\').strip()
                    i += 1
                    next_line = lines[i].strip()
                    if next_line:
                        full_command += ' ' + next_line

                # Process the command
                full_command = full_command.replace('{baseDir}', self.base_dir)

                # Handle ~ paths
                if '~/.openclaw/' in full_command:
                    match = re.search(r'~/\.openclaw/([^/]+)/', full_command)
                    if match:
                        skill_name = match.group(1)
                        full_command = full_command.replace(
                            f'~/.openclaw/{skill_name}',
                            str(self.target_skill_path)
                        )

                # Clean up extra whitespace
                full_command = ' '.join(full_command.split())

                # Avoid duplicates
                if full_command and not any(c['command'] == full_command for c in self.commands):
                    self.commands.append({
                        'command': full_command,
                        'description': 'Command from workflow',
                        'has_required_params': self._check_required_params(full_command)
                    })

            i += 1

        # Method 3: Auto-detect scripts in scripts/ directory
        scripts_dir = self.target_skill_path / "scripts"
        if scripts_dir.exists() and scripts_dir.is_dir():
            for script_file in scripts_dir.glob("*.py"):
                # Create a basic command for this script
                script_path = str(script_file)
                # Don't add --help, let the variation generator handle actual usage
                base_command = f"python3 {script_path}"

                # Avoid duplicates
                if not any(script_path in c['command'] for c in self.commands):
                    self.commands.append({
                        'command': base_command,
                        'description': f'Execute {script_file.name}',
                        'has_required_params': False  # Mark as needing params
                    })
                    print(f"  ✓ Auto-detected script: {script_file.name}")

    def _check_required_params(self, command: str) -> bool:
        """Check if command has required parameters filled in."""
        # Check for common patterns that indicate missing parameters
        missing_patterns = [
            r'--\w+\s*$',  # Flag at end without value
            r'--\w+\s+\\$',  # Flag with backslash continuation but no value
            r'<[^>]+>',  # Placeholder like <file>
            r'\$\{[^}]+\}',  # Variable like ${VAR}
        ]

        for pattern in missing_patterns:
            if re.search(pattern, command):
                return False

        return True

    def _infer_command_description(self, command: str) -> str:
        """Infer a description from the command itself."""
        # Extract the main action from the command
        parts = command.split()
        if len(parts) < 2:
            return "Command execution"

        # For skill-specific commands like "browse open", "browse snapshot"
        if len(parts) >= 2:
            action = parts[1]
            if action in ['open', 'goto']:
                return "Navigate to URL"
            elif action in ['click']:
                return "Click element"
            elif action in ['type', 'fill']:
                return "Input text"
            elif action in ['screenshot']:
                return "Capture screenshot"
            elif action in ['snapshot']:
                return "Get page snapshot"
            elif action in ['search', 'find']:
                return "Search operation"
            elif action in ['status']:
                return "Check status"
            elif action in ['stop', 'close']:
                return "Stop/close session"

        return "Command execution"

    def generate_tasks(self) -> Tuple[List[Task], List[Task]]:
        """Generate training and test tasks."""
        if self.skill_type == "documentation":
            print("\n=== Generating Documentation Quality Tasks ===")
            training_tasks = self._generate_documentation_tasks(12, "train")
            test_tasks = self._generate_documentation_tasks(8, "test")
        else:
            print("\n=== Generating Training Tasks ===")
            training_tasks = self._generate_task_set(12, "train")
            print("\n=== Generating Test Tasks ===")
            test_tasks = self._generate_task_set(8, "test")

        return training_tasks, test_tasks

    def _generate_task_set(self, count: int, _set_type: str) -> List[Task]:
        """Generate a set of tasks."""
        tasks = []
        standard_count = int(count * 0.5)
        advanced_count = count - standard_count

        # Generate standard tasks (basic command variations)
        for i in range(standard_count):
            cmd_idx = i % len(self.commands)
            task = self._create_standard_task(i + 1, self.commands[cmd_idx])
            tasks.append(task)

        # Generate advanced tasks (complex scenarios)
        for i in range(advanced_count):
            cmd_idx = i % len(self.commands)
            task = self._create_advanced_task(standard_count + i + 1, self.commands[cmd_idx])
            tasks.append(task)

        return tasks

    def _create_standard_task(self, task_num: int, command_info: dict) -> Task:
        """Create a standard task from a command."""
        task_id = f"task_{task_num:03d}"
        command = command_info['command']

        # Add basic variations to the command
        variations = self._generate_command_variations(command_info, "standard")
        varied_command = variations[0] if variations else command

        # Prepare workspace files based on command
        workspace_files = {}
        if TEST_FILE_MANAGER_AVAILABLE:
            # Extract script path from command
            script_match = re.search(r'python3?\s+([^\s]+\.py)', varied_command)
            if script_match:
                script_path = script_match.group(1)
                # Note: Files will be prepared during task writing, not here
                # We just mark that files are needed
                workspace_files['__needs_preparation__'] = {
                    'command': varied_command,
                    'script_path': script_path
                }

        return Task(
            task_id=task_id,
            task_type="standard",
            title=f"Basic: {command_info.get('description', '')}",
            background=f"Tests basic functionality of {self.skill_name}",
            objective=f"Execute command and verify successful completion",
            command=varied_command,
            expected_behavior="Command executes successfully and produces valid output",
            constraints=[
                "Must execute without errors",
                "Must produce valid output",
                "Must complete within reasonable time"
            ],
            workspace_files=workspace_files
        )

    def _create_advanced_task(self, task_num: int, command_info: dict) -> Task:
        """Create an advanced task with variations."""
        task_id = f"task_{task_num:03d}"
        command = command_info['command']

        # Add complex variations
        variations = self._generate_command_variations(command_info, "advanced")
        varied_command = variations[0] if variations else command

        # Prepare workspace files based on command
        workspace_files = {}
        if TEST_FILE_MANAGER_AVAILABLE:
            # Extract script path from command
            script_match = re.search(r'python3?\s+([^\s]+\.py)', varied_command)
            if script_match:
                script_path = script_match.group(1)
                workspace_files['__needs_preparation__'] = {
                    'command': varied_command,
                    'script_path': script_path
                }

        return Task(
            task_id=task_id,
            task_type="advanced",
            title=f"Advanced: {command_info.get('description', '')}",
            background=f"Tests advanced usage and edge cases of {self.skill_name}",
            objective=f"Execute command with complex parameters and verify robust handling",
            command=varied_command,
            expected_behavior="Command handles complex scenarios correctly and provides detailed output",
            constraints=[
                "Must handle edge cases gracefully",
                "Must validate inputs properly",
                "Must provide comprehensive output",
                "Must maintain performance under load"
            ],
            workspace_files=workspace_files
        )

        return Task(
            task_id=task_id,
            task_type="advanced",
            title=f"Advanced: {command_info.get('description', 'Complex scenario')}",
            background=f"Tests advanced usage and edge cases of {self.skill_name}",
            objective=f"Execute command with complex parameters and verify robust handling",
            command=varied_command,
            expected_behavior="Command handles complex scenarios correctly and provides detailed output",
            constraints=[
                "Must handle edge cases gracefully",
                "Must validate inputs properly",
                "Must provide comprehensive output",
                "Must maintain performance under load"
            ],
            workspace_files={}
        )

    def _generate_command_variations(self, command_info: dict, task_type: str) -> List[str]:
        """Generate variations of a command for different test scenarios."""
        variations = []
        has_params = command_info.get('has_required_params', True)
        base_command = command_info.get('command', '')

        # For standard tasks: basic parameter variations
        if task_type == "standard":
            # If command has required params, use it as-is
            if has_params:
                variations.append(base_command)
            else:
                # Generate realistic test parameters based on script analysis
                test_cmd = self._generate_realistic_command(base_command)
                if test_cmd:
                    variations.append(test_cmd)

            # Add common flags if command has params
            if has_params and ('python' in base_command or '.py' in base_command):
                if '--verbose' not in base_command:
                    variations.append(f"{base_command} --verbose")

        # For advanced tasks: complex scenarios
        else:
            # If command has required params, create variations
            if has_params:
                # Multiple parameters
                if 'AAPL' in base_command:
                    variations.append(base_command.replace('AAPL', 'AAPL MSFT GOOGL'))

                # Add output format options
                if '--output' not in base_command:
                    variations.append(f"{base_command} --output json")

                # Add performance flags
                if '--fast' not in base_command and 'analyze' in base_command:
                    variations.append(f"{base_command} --fast")
            else:
                # Generate realistic advanced test parameters
                test_cmd = self._generate_realistic_command(base_command)
                if test_cmd:
                    variations.append(test_cmd)

            # Fallback to original if we have params
            if not variations and has_params:
                variations.append(base_command)

        return variations

    def _extract_base_command(self, full_command: str) -> str:
        """Extract the base command (script path) without parameters."""
        # Split by common parameter patterns
        parts = re.split(r'\s+--', full_command, maxsplit=1)
        base = parts[0].strip()

        # Remove trailing backslash if present
        base = base.rstrip('\\').strip()

        return base

    def _generate_realistic_command(self, base_command: str) -> str:
        """Generate realistic test command with appropriate parameters based on script analysis and SKILL.md context."""
        script_path = base_command.replace('python3 ', '').replace('python ', '').strip()
        script_name = script_path.split('/')[-1].replace('.py', '').lower()

        # Step 1: Try to read the script to understand its parameters
        script_content = None
        try:
            with open(script_path, 'r') as f:
                script_content = f.read()
        except Exception as e:
            print(f"  ⚠ Could not read script {script_path}: {e}")

        # Step 2: Analyze script for parameter requirements
        if script_content:
            # Check for sys.argv usage (simpler, more common)
            if 'sys.argv' in script_content:
                argv_check = re.search(r'len\(sys\.argv\)\s*[!=<>]+\s*(\d+)', script_content)
                if argv_check:
                    expected_argc = int(argv_check.group(1))
                    num_args = expected_argc - 1  # argc - 1, since argv[0] is script name

                    # Look for usage message to understand parameter names
                    usage_match = re.search(r'Usage:.*?(?:\[([^\]]+)\]|<([^>]+)>)', script_content)
                    if usage_match:
                        # Extract parameter hints from usage message
                        params = re.findall(r'(?:\[([^\]]+)\]|<([^>]+)>)', script_content)
                        args = []

                        for param_tuple in params[:num_args]:
                            param = param_tuple[0] or param_tuple[1]
                            param_lower = param.lower()

                            # Infer appropriate test value based on parameter name and skill context
                            test_value = self._infer_test_value_for_param(param_lower, 'input' in param_lower or params.index(param_tuple) == 0)
                            args.append(test_value)

                        if args:
                            return f"{base_command} {' '.join(args)}"

                    # Fallback: generate arguments based on count and skill context
                    args = []
                    for i in range(num_args):
                        if i == 0:
                            # First arg is usually input
                            args.append(self._get_default_input_file())
                        elif i == num_args - 1:
                            # Last arg is often output
                            args.append(self._get_default_output_file())
                        else:
                            # Middle args could be data/config
                            args.append(self._get_default_data_file())

                    if args:
                        return f"{base_command} {' '.join(args)}"

            # Check for argparse usage
            if 'argparse' in script_content:
                args_found = re.findall(r'add_argument\([\'"]([^\'"]+)[\'"]', script_content)

                cmd_parts = [base_command]
                for arg in args_found:
                    if arg.startswith('--'):
                        # Skip help and version
                        if arg in ['--help', '--version', '-h', '-v']:
                            continue

                        # Infer value based on argument name
                        arg_name = arg.replace('--', '')
                        test_value = self._infer_test_value_for_param(arg_name, False)
                        cmd_parts.append(f"{arg} {test_value}")

                    elif not arg.startswith('-'):
                        # Positional argument
                        test_value = self._infer_test_value_for_param(arg, True)
                        cmd_parts.append(test_value)

                if len(cmd_parts) > 1:
                    return ' '.join(cmd_parts)

        # Step 3: Infer from script name and skill context
        # Check if script name contains hints about file types
        for file_type in self.inferred_file_types:
            if file_type in script_name:
                input_file = f"test.{file_type}"
                output_file = f"output.{file_type}"
                return f"{base_command} {input_file} {output_file}"

        # Step 4: Use inferred patterns from SKILL.md examples
        if self.inferred_input_patterns:
            input_file = self.inferred_input_patterns[0]
            if self.inferred_output_patterns:
                output_file = self.inferred_output_patterns[0]
                return f"{base_command} {input_file} {output_file}"
            return f"{base_command} {input_file}"

        # Step 5: Last resort - use primary inferred file type or generic
        return f"{base_command} {self._get_default_input_file()} {self._get_default_output_file()}"

    def _infer_test_value_for_param(self, param_name: str, is_input: bool) -> str:
        """Infer appropriate test value based on parameter name and skill context."""
        param_lower = param_name.lower()

        # Check for specific parameter types
        if 'url' in param_lower or 'link' in param_lower:
            return 'https://example.com'
        elif 'email' in param_lower:
            return 'test@example.com'
        elif 'port' in param_lower:
            return '8080'
        elif 'host' in param_lower:
            return 'localhost'
        elif 'count' in param_lower or 'number' in param_lower or 'num' in param_lower:
            return '10'
        elif 'name' in param_lower and 'file' not in param_lower:
            return 'test_name'
        elif 'id' in param_lower:
            return 'test_id_123'

        # File-related parameters
        if any(keyword in param_lower for keyword in ['file', 'path', 'input', 'output', 'data', 'config']):
            if 'output' in param_lower:
                return self._get_default_output_file()
            elif 'config' in param_lower or 'settings' in param_lower:
                return self._get_default_config_file()
            elif 'data' in param_lower and 'json' not in param_lower:
                return self._get_default_data_file()
            else:
                return self._get_default_input_file()

        # Check for specific file type mentions
        for file_type in self.inferred_file_types:
            if file_type in param_lower:
                return f"test.{file_type}"

        # Default based on position
        if is_input:
            return self._get_default_input_file()
        else:
            return 'test_value'

    def _get_default_input_file(self) -> str:
        """Get default input filename based on skill context."""
        if self.inferred_file_types:
            primary_type = self.inferred_file_types[0]
            return f"input.{primary_type}"
        return "input.txt"

    def _get_default_output_file(self) -> str:
        """Get default output filename based on skill context."""
        if self.inferred_file_types:
            primary_type = self.inferred_file_types[0]
            return f"output.{primary_type}"
        return "output.txt"

    def _get_default_data_file(self) -> str:
        """Get default data filename based on skill context."""
        # Prefer structured data formats
        for preferred in ['json', 'yaml', 'yml', 'csv', 'xml']:
            if preferred in self.inferred_file_types:
                return f"data.{preferred}"

        if self.inferred_file_types:
            return f"data.{self.inferred_file_types[0]}"
        return "data.json"

    def _get_default_config_file(self) -> str:
        """Get default config filename based on skill context."""
        # Prefer config formats
        for preferred in ['yaml', 'yml', 'json', 'toml', 'ini']:
            if preferred in self.inferred_file_types:
                return f"config.{preferred}"
        return "config.json"

    def _generate_documentation_tasks(self, count: int, _set_type: str) -> List[Task]:
        """Generate documentation quality evaluation tasks with deep, multi-dimensional criteria."""
        tasks = []
        standard_count = int(count * 0.5)
        advanced_count = count - standard_count

        # ENHANCED: Multi-dimensional documentation quality aspects
        doc_aspects = [
            {
                "title": "Structural Completeness & Organization",
                "objective": "Verify documentation has complete structure with all essential sections properly organized",
                "criteria": [
                    "Clear introduction/overview explaining purpose",
                    "Installation/setup instructions if applicable",
                    "Comprehensive usage section with all commands/features",
                    "Multiple concrete examples covering common use cases",
                    "Configuration/parameters section if applicable",
                    "Troubleshooting/error handling section",
                    "Logical flow from basic to advanced topics"
                ]
            },
            {
                "title": "Practical Usability & Learnability",
                "objective": "Evaluate if a new user can successfully use the skill based solely on the documentation",
                "criteria": [
                    "Clear step-by-step instructions for first-time users",
                    "Examples are copy-pasteable and executable",
                    "Prerequisites and dependencies clearly stated",
                    "Common pitfalls and gotchas are documented",
                    "Progressive complexity (simple examples first)",
                    "Quick start guide or minimal working example"
                ]
            },
            {
                "title": "Example Quality & Coverage",
                "objective": "Verify examples are comprehensive, accurate, and cover diverse scenarios",
                "criteria": [
                    "At least 3 distinct, realistic examples",
                    "Examples show different use cases, not variations of same task",
                    "Code examples include expected output/results",
                    "Edge cases and boundary conditions demonstrated",
                    "Examples include error handling scenarios",
                    "Complex multi-step workflows shown if applicable"
                ]
            },
            {
                "title": "Technical Depth & Accuracy",
                "objective": "Verify technical information is correct, complete, and sufficiently detailed",
                "criteria": [
                    "All parameters/options documented with types and defaults",
                    "Return values and output formats specified",
                    "Performance characteristics mentioned if relevant",
                    "Limitations and constraints clearly stated",
                    "Integration points with other systems explained",
                    "Technical terminology used correctly and consistently"
                ]
            },
            {
                "title": "Clarity & Readability",
                "objective": "Evaluate if documentation is well-written and easy to understand",
                "criteria": [
                    "Clear, concise language without unnecessary jargon",
                    "Consistent formatting and style throughout",
                    "Proper use of headings, lists, and code blocks",
                    "No ambiguous or confusing statements",
                    "Appropriate level of detail (not too verbose or terse)",
                    "Good use of visual hierarchy and whitespace"
                ]
            },
            {
                "title": "Completeness of Command Coverage",
                "objective": "Verify all commands/features are documented with sufficient detail",
                "criteria": [
                    "Every command mentioned in examples is explained",
                    "All flags/options for each command documented",
                    "Command syntax clearly specified",
                    "When to use each command/feature explained",
                    "Relationships between commands clarified",
                    "No undocumented features or hidden functionality"
                ]
            },
            {
                "title": "Error Handling & Troubleshooting",
                "objective": "Verify documentation helps users diagnose and fix problems",
                "criteria": [
                    "Common errors and their solutions documented",
                    "Error messages explained with context",
                    "Debugging tips and diagnostic commands provided",
                    "Known issues and workarounds listed",
                    "How to get help or report bugs",
                    "Validation steps to verify correct setup"
                ]
            },
            {
                "title": "Advanced Scenarios & Best Practices",
                "objective": "Verify documentation covers advanced usage and provides guidance",
                "criteria": [
                    "Advanced use cases and patterns documented",
                    "Best practices and recommendations provided",
                    "Performance optimization tips if applicable",
                    "Security considerations mentioned if relevant",
                    "Integration patterns with other tools",
                    "Real-world workflow examples"
                ]
            }
        ]

        # Generate standard tasks (focus on basic quality)
        for i in range(standard_count):
            aspect = doc_aspects[i % len(doc_aspects)]
            task = Task(
                task_id=f"task_{i + 1:03d}",
                task_type="standard",
                title=f"Standard: {aspect['title']}",
                background=f"Evaluates {aspect['title'].lower()} of {self.skill_name} documentation",
                objective=aspect['objective'],
                command="",  # No command for documentation tasks
                expected_behavior=f"Documentation satisfies at least 60% of criteria: {', '.join(aspect['criteria'][:3])}...",
                constraints=[
                    "Must meet minimum quality threshold",
                    "Must be factually correct",
                    "Must be understandable to target audience"
                ],
                workspace_files={}
            )
            tasks.append(task)

        # Generate advanced tasks (comprehensive deep evaluation)
        for i in range(advanced_count):
            aspect = doc_aspects[i % len(doc_aspects)]
            task = Task(
                task_id=f"task_{standard_count + i + 1:03d}",
                task_type="advanced",
                title=f"Advanced: {aspect['title']}",
                background=f"Deep evaluation of {aspect['title'].lower()} with high standards for {self.skill_name}",
                objective=f"{aspect['objective']} - must meet professional documentation standards",
                command="",  # No command for documentation tasks
                expected_behavior=f"Documentation satisfies at least 80% of criteria with high quality: {', '.join(aspect['criteria'])}",
                constraints=[
                    "Must meet professional quality standards",
                    "Must be comprehensive and thorough",
                    "Must anticipate user needs and questions",
                    "Must provide actionable guidance",
                    "Must be maintainable and extensible"
                ],
                workspace_files={}
            )
            tasks.append(task)

        return tasks

    def generate_specchecks(self, tasks: List[Task]) -> List[SpecCheck]:
        """Generate SpecCheck criteria for tasks with enhanced evaluation standards."""
        specchecks = []

        for task in tasks:
            # Documentation tasks use different criteria
            if self.skill_type == "documentation":
                # Standard tasks: 60% threshold, fewer criteria
                if task.task_type == "standard":
                    criteria = [
                        SpecCheckCriterion(
                            description="Has essential structural elements (intro, usage, examples)",
                            verification_method="Deep LLM analysis of document structure and completeness"
                        ),
                        SpecCheckCriterion(
                            description="Content is clear, well-organized, and understandable",
                            verification_method="Deep LLM analysis of clarity, flow, and readability"
                        ),
                        SpecCheckCriterion(
                            description="Provides practical, usable information",
                            verification_method="Deep LLM analysis of practical utility and actionability"
                        ),
                        SpecCheckCriterion(
                            description="Examples are present and demonstrate key concepts",
                            verification_method="Deep LLM analysis of example quality and coverage"
                        ),
                        SpecCheckCriterion(
                            description="Technical information appears accurate and complete",
                            verification_method="Deep LLM analysis of technical accuracy and depth"
                        )
                    ]
                else:
                    # Advanced tasks: 80% threshold, comprehensive criteria
                    criteria = [
                        SpecCheckCriterion(
                            description="Complete documentation structure with all essential sections",
                            verification_method="Deep LLM analysis of structural completeness and organization"
                        ),
                        SpecCheckCriterion(
                            description="High clarity with excellent readability and flow",
                            verification_method="Deep LLM analysis of writing quality and coherence"
                        ),
                        SpecCheckCriterion(
                            description="Comprehensive, diverse examples covering multiple scenarios",
                            verification_method="Deep LLM analysis of example breadth, depth, and realism"
                        ),
                        SpecCheckCriterion(
                            description="Detailed technical information with proper depth",
                            verification_method="Deep LLM analysis of technical completeness and accuracy"
                        ),
                        SpecCheckCriterion(
                            description="Covers edge cases, error handling, and troubleshooting",
                            verification_method="Deep LLM analysis of edge case coverage and problem-solving guidance"
                        ),
                        SpecCheckCriterion(
                            description="Practical usability - new users can successfully use the skill",
                            verification_method="Deep LLM analysis of learnability and user experience"
                        ),
                        SpecCheckCriterion(
                            description="Professional quality suitable for production use",
                            verification_method="Deep LLM analysis of overall quality and completeness"
                        )
                    ]
            else:
                # Executable tasks use command execution criteria
                criteria = [
                    SpecCheckCriterion(
                        description="Command executes without errors",
                        verification_method="Check exit code is 0"
                    ),
                    SpecCheckCriterion(
                        description="Output is generated",
                        verification_method="Check output file/stdout exists"
                    ),
                    SpecCheckCriterion(
                        description="Output format is valid",
                        verification_method="Validate output structure"
                    ),
                    SpecCheckCriterion(
                        description="Expected data is present",
                        verification_method="Check for required content"
                    )
                ]

                if task.task_type == "advanced":
                    criteria.append(
                        SpecCheckCriterion(
                            description="Handles complex scenarios",
                            verification_method="Verify edge case handling"
                        )
                    )

            speccheck = SpecCheck(
                task_id=task.task_id,
                criteria=criteria,
                total_points=len(criteria),
                pass_threshold=int(len(criteria) * 0.7)
            )
            specchecks.append(speccheck)

        return specchecks

    def save_tasks(self, tasks: List[Task], specchecks: List[SpecCheck], task_set: str):
        """Save tasks to disk."""
        tasks_dir = self.output_dir / "tasks" / task_set
        tasks_dir.mkdir(parents=True, exist_ok=True)

        for task, speccheck in zip(tasks, specchecks):
            task_dir = tasks_dir / task.task_id
            task_dir.mkdir(exist_ok=True)

            # Create workspace
            workspace_dir = task_dir / "workspace"
            workspace_dir.mkdir(exist_ok=True)

            # Prepare workspace files if needed
            if '__needs_preparation__' in task.workspace_files and TEST_FILE_MANAGER_AVAILABLE:
                prep_info = task.workspace_files['__needs_preparation__']
                try:
                    # Randomly decide whether to use local files based on config
                    import random
                    use_local = random.random() < self.local_file_ratio

                    file_manager = TestFileManager(workspace_dir, prefer_local=use_local)
                    file_manager.prepare_files_for_command(
                        prep_info['command'],
                        prep_info['script_path']
                    )
                    # Files are already in workspace_dir, no need to copy
                except Exception as e:
                    print(f"  ⚠ Warning: Could not prepare files for {task.task_id}: {e}")

            # Write task.md
            task_md = self._format_task_md(task)
            with open(task_dir / "task.md", 'w', encoding='utf-8') as f:
                f.write(task_md)

            # Write speccheck.md
            speccheck_md = self._format_speccheck_md(speccheck)
            with open(task_dir / "speccheck.md", 'w', encoding='utf-8') as f:
                f.write(speccheck_md)

            print(f"✓ Written {task.task_id} ({task.task_type})")

        print(f"✓ Saved {len(tasks)} {task_set} tasks")

    def _format_task_md(self, task: Task) -> str:
        """Format task as markdown."""
        constraints_md = '\n'.join(f"- {c}" for c in task.constraints)

        return f"""# Task: {task.title}

## Background
{task.background}

## Objective
{task.objective}

## Command to Execute
```bash
{task.command}
```

## Expected Behavior
{task.expected_behavior}

## Constraints
{constraints_md}
"""

    def _format_speccheck_md(self, speccheck: SpecCheck) -> str:
        """Format speccheck as markdown."""
        criteria_md = '\n'.join(
            f"- [ ] **Criterion {i+1}**: {c.description}\n  - Verification: {c.verification_method}"
            for i, c in enumerate(speccheck.criteria)
        )

        return f"""# SpecCheck: {speccheck.task_id}

## Evaluation Criteria (Total: {speccheck.total_points} points)

{criteria_md}

## Scoring
- Each criterion is worth 1 point
- Total Points: {speccheck.total_points}
- Pass Threshold: {speccheck.pass_threshold}/{speccheck.total_points} ({int(speccheck.pass_threshold/speccheck.total_points*100)}%)

## Evaluation Method
1. Execute the command specified in task.md
2. Check each criterion above
3. Award 1 point for each passed criterion
4. Task passes if score >= {speccheck.pass_threshold}
"""


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python smart_task_generator.py <target-skill-path> [output-dir] [config-path]")
        sys.exit(1)

    target_skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    config_path = sys.argv[3] if len(sys.argv) > 3 else None

    # Load config if provided
    config = {}
    if config_path:
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")

    generator = SmartTaskGenerator(target_skill_path, output_dir, config)

    # Load and parse skill
    if not generator.load_and_parse_skill():
        sys.exit(1)

    # Generate tasks
    training_tasks, test_tasks = generator.generate_tasks()

    # Generate specchecks
    training_specchecks = generator.generate_specchecks(training_tasks)
    test_specchecks = generator.generate_specchecks(test_tasks)

    # Save tasks
    generator.save_tasks(training_tasks, training_specchecks, "train")
    generator.save_tasks(test_tasks, test_specchecks, "test")

    print("\n✓ Task generation complete!")
    sys.exit(0)


if __name__ == "__main__":
    main()
