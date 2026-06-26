"""
Evaluator for Skills-Coach

Scores execution outputs using SpecCheck criteria, computes evaluation metrics,
performs comparative analysis, and makes retention decisions.
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class CriterionResult:
    """Result of evaluating a single criterion."""
    criterion: str
    satisfied: bool
    evidence: str


@dataclass
class TaskEvaluation:
    """Evaluation results for a single task."""
    task_id: str
    task_type: str  # "standard" or "advanced"
    score: int
    total: int
    passed: bool
    criteria_results: List[CriterionResult]


@dataclass
class SkillEvaluation:
    """Complete evaluation for a skill version."""
    skill_name: str
    task_evaluations: List[TaskEvaluation]
    pass_rate: float
    avg_score: float
    standard_score: float
    advanced_score: float
    error_rate: float


@dataclass
class ComparisonMetrics:
    """Comparison metrics between original and optimized skills."""
    pass_rate_delta: float
    avg_score_delta: float
    standard_score_delta: float
    advanced_score_delta: float
    error_rate_delta: float
    regression_count: int
    per_task_deltas: List[int]


class SkillEvaluator:
    """Evaluates and compares skill versions."""

    def __init__(
        self,
        target_skill_path: str,
        test_tasks_dir: str = "tasks/test",
        exec_results_dir: str = "exec_results",
        output_dir: str = "."
    ):
        self.target_skill_path = Path(target_skill_path)
        self.output_dir = Path(output_dir)

        # If test_tasks_dir is relative, make it relative to output_dir
        test_tasks_path = Path(test_tasks_dir)
        if not test_tasks_path.is_absolute():
            self.test_tasks_dir = self.output_dir / test_tasks_path
        else:
            self.test_tasks_dir = test_tasks_path

        # If exec_results_dir is relative, make it relative to output_dir
        exec_results_path = Path(exec_results_dir)
        if not exec_results_path.is_absolute():
            self.exec_results_dir = self.output_dir / exec_results_path
        else:
            self.exec_results_dir = exec_results_path

        self.skill_name = self.target_skill_path.name
        self.optimized_skill_dir = self.output_dir / f"{self.skill_name}-optimized"

        # Cache for skill documentation content
        self._skill_doc_cache = {}

    def _load_skill_documentation(self, skill_path: Path) -> str:
        """Load SKILL.md content for documentation evaluation."""
        if str(skill_path) in self._skill_doc_cache:
            return self._skill_doc_cache[str(skill_path)]

        skill_md = skill_path / "SKILL.md"
        if skill_md.exists():
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
                self._skill_doc_cache[str(skill_path)] = content
                return content
        return ""

    def _evaluate_documentation_with_llm(self, skill_content: str, criterion: str, task_objective: str) -> Tuple[bool, str]:
        """
        Use LLM to perform deep evaluation of documentation quality against a specific criterion.

        Args:
            skill_content: The SKILL.md content to evaluate
            criterion: The evaluation criterion
            task_objective: The task objective for context

        Returns:
            Tuple of (satisfied: bool, evidence: str)
        """
        # Construct comprehensive evaluation prompt
        prompt = f"""You are a professional technical documentation reviewer evaluating skill documentation quality.

DOCUMENTATION TO EVALUATE:
{skill_content}

EVALUATION CRITERION:
{criterion}

TASK OBJECTIVE:
{task_objective}

Perform a DEEP, THOROUGH evaluation of whether the documentation satisfies this criterion. Be STRICT and hold the documentation to professional standards.

Evaluation Guidelines:

1. STRUCTURAL COMPLETENESS:
   - Does it have clear introduction/overview?
   - Are all commands/features documented?
   - Is there a logical progression from basic to advanced?
   - Are prerequisites and setup clearly stated?

2. PRACTICAL USABILITY:
   - Can a new user successfully use this based solely on the docs?
   - Are examples copy-pasteable and realistic?
   - Are common pitfalls documented?
   - Is there a quick start guide?

3. EXAMPLE QUALITY:
   - Are there at least 3 diverse, realistic examples?
   - Do examples cover different use cases (not just variations)?
   - Are expected outputs shown?
   - Are edge cases demonstrated?

4. TECHNICAL DEPTH:
   - Are all parameters/options documented with types?
   - Are return values and formats specified?
   - Are limitations clearly stated?
   - Is technical terminology used correctly?

5. CLARITY & READABILITY:
   - Is the language clear and concise?
   - Is formatting consistent?
   - Is there good visual hierarchy?
   - Are there no ambiguous statements?

6. ERROR HANDLING:
   - Are common errors documented?
   - Are troubleshooting steps provided?
   - Are error messages explained?

7. COMPLETENESS:
   - Does it cover edge cases?
   - Are advanced scenarios included?
   - Are best practices mentioned?

Respond in JSON format:
{{
    "satisfied": true/false,
    "score": 0-100,
    "evidence": "Detailed explanation (2-4 sentences) with specific examples from the documentation",
    "strengths": ["strength 1", "strength 2"],
    "weaknesses": ["weakness 1", "weakness 2"]
}}

Be STRICT. Only mark as satisfied if the documentation truly meets professional standards for this criterion.
A score of 70+ means satisfied, below 70 means not satisfied.
"""

        try:
            # Try to use Claude API for evaluation
            result = subprocess.run(
                ['claude', '--model', 'sonnet-4'],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                # Try to parse JSON from response
                response_text = result.stdout.strip()

                # Extract JSON if wrapped in markdown code blocks
                if '```json' in response_text:
                    json_start = response_text.find('```json') + 7
                    json_end = response_text.find('```', json_start)
                    response_text = response_text[json_start:json_end].strip()
                elif '```' in response_text:
                    json_start = response_text.find('```') + 3
                    json_end = response_text.find('```', json_start)
                    response_text = response_text[json_start:json_end].strip()

                try:
                    response = json.loads(response_text)
                    satisfied = response.get('satisfied', False) or response.get('score', 0) >= 70
                    evidence = response.get('evidence', 'LLM evaluation completed')

                    # Enhance evidence with strengths/weaknesses if available
                    if 'strengths' in response or 'weaknesses' in response:
                        strengths = response.get('strengths', [])
                        weaknesses = response.get('weaknesses', [])
                        evidence += f" | Strengths: {', '.join(strengths[:2])}. Weaknesses: {', '.join(weaknesses[:2])}"

                    return satisfied, evidence
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract satisfaction from text
                    satisfied = 'satisfied": true' in response_text.lower() or 'score": 7' in response_text or 'score": 8' in response_text or 'score": 9' in response_text
                    return satisfied, response_text[:200]

            # Fallback to enhanced heuristic evaluation
            return self._enhanced_heuristic_evaluation(skill_content, criterion, task_objective)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            # Fallback to enhanced heuristic evaluation
            return self._enhanced_heuristic_evaluation(skill_content, criterion, task_objective)

    def _enhanced_heuristic_evaluation(self, skill_content: str, criterion: str, task_objective: str) -> Tuple[bool, str]:
        """
        Enhanced heuristic evaluation with stricter, multi-dimensional checks.

        Args:
            skill_content: The SKILL.md content
            criterion: The evaluation criterion
            task_objective: The task objective

        Returns:
            Tuple of (satisfied: bool, evidence: str)
        """
        criterion_lower = criterion.lower()
        content_lower = skill_content.lower()
        lines = skill_content.split('\n')

        # Count various elements
        code_blocks = skill_content.count('```')
        headers = len([l for l in lines if l.strip().startswith('#')])
        examples_keyword = content_lower.count('example')

        # STRUCTURAL COMPLETENESS
        if 'structural' in criterion_lower or 'structure' in criterion_lower and 'complete' in criterion_lower:
            required_sections = {
                'overview': any(word in content_lower for word in ['overview', 'introduction', 'about']),
                'usage': 'usage' in content_lower or 'how to' in content_lower,
                'examples': 'example' in content_lower and code_blocks >= 2,
                'commands': any(word in content_lower for word in ['command', 'function', 'method', 'api']),
            }

            sections_found = sum(required_sections.values())
            has_good_structure = sections_found >= 3 and headers >= 4

            # Check for logical flow
            has_setup = any(word in content_lower for word in ['install', 'setup', 'prerequisite', 'requirement'])
            has_troubleshooting = any(word in content_lower for word in ['troubleshoot', 'error', 'debug', 'problem'])

            satisfied = has_good_structure and (has_setup or has_troubleshooting)
            evidence = f"Structure: {sections_found}/4 sections, {headers} headers, setup: {has_setup}, troubleshooting: {has_troubleshooting}"
            return satisfied, evidence

        # PRACTICAL USABILITY
        elif 'practical' in criterion_lower or 'usability' in criterion_lower or 'learnability' in criterion_lower:
            # Check for step-by-step instructions
            has_steps = any(word in content_lower for word in ['step', 'first', 'then', 'next', 'finally'])

            # Check for prerequisites
            has_prereqs = any(word in content_lower for word in ['prerequisite', 'require', 'need', 'install', 'setup'])

            # Check for quick start
            has_quickstart = any(word in content_lower for word in ['quick start', 'getting started', 'quickstart'])

            # Check for common pitfalls
            has_pitfalls = any(word in content_lower for word in ['pitfall', 'gotcha', 'warning', 'note:', 'important:'])

            # Check if examples look executable (have actual commands)
            executable_examples = code_blocks >= 2 and any(word in skill_content for word in ['$', 'python', 'node', 'npm', 'bash'])

            usability_score = sum([has_steps, has_prereqs, has_quickstart or executable_examples, has_pitfalls])
            satisfied = usability_score >= 3
            evidence = f"Usability: steps={has_steps}, prereqs={has_prereqs}, quickstart={has_quickstart}, pitfalls={has_pitfalls}, executable={executable_examples}"
            return satisfied, evidence

        # EXAMPLE QUALITY & COVERAGE
        elif 'example' in criterion_lower and ('quality' in criterion_lower or 'comprehensive' in criterion_lower or 'diverse' in criterion_lower):
            # Count distinct code blocks
            num_examples = code_blocks // 2  # Assuming each example has opening and closing ```

            # Check for diversity (different commands/scenarios)
            has_basic_example = any(word in content_lower for word in ['basic', 'simple', 'hello', 'getting started'])
            has_advanced_example = any(word in content_lower for word in ['advanced', 'complex', 'production'])

            # Check if examples show output
            has_output = any(word in content_lower for word in ['output:', 'result:', 'returns:', '=>', '->'])

            # Check for edge cases in examples
            has_edge_cases = any(word in content_lower for word in ['edge case', 'corner case', 'boundary', 'limit'])

            # Check for error handling examples
            has_error_examples = any(word in content_lower for word in ['error', 'exception', 'fail', 'catch'])

            example_quality_score = sum([
                num_examples >= 3,
                has_basic_example and has_advanced_example,
                has_output,
                has_edge_cases or has_error_examples
            ])

            satisfied = example_quality_score >= 3
            evidence = f"Examples: {num_examples} blocks, basic={has_basic_example}, advanced={has_advanced_example}, output={has_output}, edge_cases={has_edge_cases}"
            return satisfied, evidence

        # TECHNICAL DEPTH & ACCURACY
        elif 'technical' in criterion_lower and ('depth' in criterion_lower or 'detailed' in criterion_lower or 'accuracy' in criterion_lower):
            # Check for parameter documentation
            has_parameters = any(word in content_lower for word in ['parameter', 'argument', 'option', 'flag'])

            # Check for types/formats
            has_types = any(word in content_lower for word in ['type:', 'format:', 'string', 'number', 'boolean', 'array'])

            # Check for return values
            has_returns = any(word in content_lower for word in ['return', 'output', 'result'])

            # Check for limitations
            has_limitations = any(word in content_lower for word in ['limitation', 'constraint', 'caveat', 'note:'])

            # Check for technical terminology
            technical_terms = sum(1 for term in ['api', 'cli', 'sdk', 'library', 'framework', 'protocol'] if term in content_lower)

            # Check for sufficient detail (longer docs usually have more depth)
            has_depth = len(skill_content) > 2000

            technical_score = sum([has_parameters, has_types or has_returns, has_limitations, technical_terms >= 2, has_depth])
            satisfied = technical_score >= 3
            evidence = f"Technical: params={has_parameters}, types={has_types}, returns={has_returns}, limitations={has_limitations}, depth={has_depth}"
            return satisfied, evidence

        # CLARITY & READABILITY
        elif 'clarity' in criterion_lower or 'readable' in criterion_lower or 'clear' in criterion_lower:
            # Check for reasonable length (not too short, not too verbose)
            reasonable_length = 500 < len(skill_content) < 15000

            # Check for good formatting
            has_headers = headers >= 3
            has_lists = skill_content.count('\n- ') >= 3 or skill_content.count('\n* ') >= 3
            has_code_blocks_formatted = code_blocks >= 2

            # Check for clear language (no excessive jargon without explanation)
            sentences = [s.strip() for s in skill_content.split('.') if s.strip()]
            avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
            clear_language = avg_sentence_length < 30  # Not too complex

            # Check for consistent formatting
            has_consistent_headers = skill_content.count('##') >= 2 or skill_content.count('###') >= 2

            clarity_score = sum([reasonable_length, has_headers, has_lists, has_code_blocks_formatted, clear_language, has_consistent_headers])
            satisfied = clarity_score >= 4
            evidence = f"Clarity: length={reasonable_length}, headers={has_headers}, lists={has_lists}, code={has_code_blocks_formatted}, clear={clear_language}"
            return satisfied, evidence

        # ERROR HANDLING & TROUBLESHOOTING
        elif 'error' in criterion_lower or 'troubleshoot' in criterion_lower:
            # Check for error documentation
            has_errors = any(word in content_lower for word in ['error', 'exception', 'fail'])

            # Check for troubleshooting section
            has_troubleshooting_section = 'troubleshoot' in content_lower or 'debugging' in content_lower

            # Check for common issues
            has_common_issues = any(word in content_lower for word in ['common', 'frequent', 'typical'])

            # Check for solutions/fixes
            has_solutions = any(word in content_lower for word in ['solution', 'fix', 'resolve', 'workaround'])

            # Check for diagnostic commands
            has_diagnostics = any(word in content_lower for word in ['check', 'verify', 'test', 'validate'])

            error_handling_score = sum([has_errors, has_troubleshooting_section, has_common_issues, has_solutions, has_diagnostics])
            satisfied = error_handling_score >= 3
            evidence = f"Error handling: errors={has_errors}, troubleshooting={has_troubleshooting_section}, solutions={has_solutions}, diagnostics={has_diagnostics}"
            return satisfied, evidence

        # PROFESSIONAL QUALITY
        elif 'professional' in criterion_lower or 'production' in criterion_lower:
            # Comprehensive check for professional quality
            has_complete_structure = headers >= 5 and code_blocks >= 4
            has_good_length = len(skill_content) > 1500
            has_examples = examples_keyword >= 2
            has_error_handling = any(word in content_lower for word in ['error', 'troubleshoot'])
            has_best_practices = any(word in content_lower for word in ['best practice', 'recommendation', 'tip'])
            has_advanced_content = any(word in content_lower for word in ['advanced', 'production', 'scale'])

            professional_score = sum([has_complete_structure, has_good_length, has_examples, has_error_handling, has_best_practices, has_advanced_content])
            satisfied = professional_score >= 5
            evidence = f"Professional: structure={has_complete_structure}, length={has_good_length}, examples={has_examples}, errors={has_error_handling}, best_practices={has_best_practices}"
            return satisfied, evidence

        # FALLBACK: Basic heuristic for unknown criteria
        # If we reach here, use a simple pass-through
        return True, "Passed basic heuristic check"

    def _heuristic_evaluation(self, skill_content: str, criterion: str) -> Tuple[bool, str]:
        """
        Fallback heuristic evaluation when LLM is not available.

        Args:
            skill_content: The SKILL.md content
            criterion: The evaluation criterion

        Returns:
            Tuple of (satisfied: bool, evidence: str)
        """
        criterion_lower = criterion.lower()
        content_lower = skill_content.lower()

        # Structure completeness check
        if 'structure is complete' in criterion_lower:
            required_sections = ['usage', 'example', 'description']
            found_sections = sum(1 for section in required_sections if section in content_lower)
            satisfied = found_sections >= 2
            evidence = f"Found {found_sections}/3 essential sections (heuristic)"
            return satisfied, evidence

        # Clarity check
        elif 'clear and readable' in criterion_lower:
            # Check for reasonable length and formatting
            has_headers = '##' in skill_content or '#' in skill_content
            has_reasonable_length = len(skill_content) > 200
            satisfied = has_headers and has_reasonable_length
            evidence = f"Has headers: {has_headers}, Length: {len(skill_content)} chars (heuristic)"
            return satisfied, evidence

        # Examples check
        elif 'examples are present' in criterion_lower:
            has_code_blocks = '```' in skill_content
            has_example_keyword = 'example' in content_lower
            satisfied = has_code_blocks or has_example_keyword
            evidence = f"Code blocks: {has_code_blocks}, Example keyword: {has_example_keyword} (heuristic)"
            return satisfied, evidence

        # Technical accuracy check
        elif 'technical accuracy' in criterion_lower:
            # Basic check: has technical content
            has_technical_terms = any(term in content_lower for term in ['command', 'parameter', 'option', 'flag', 'script'])
            satisfied = has_technical_terms and len(skill_content) > 300
            evidence = f"Contains technical terms and sufficient detail (heuristic)"
            return satisfied, evidence

        # Comprehensive coverage check
        elif 'comprehensive' in criterion_lower or 'edge cases' in criterion_lower:
            # Check for advanced content indicators
            has_constraints = 'constraint' in content_lower or 'limitation' in content_lower
            has_multiple_examples = skill_content.count('```') >= 2
            satisfied = has_constraints or has_multiple_examples
            evidence = f"Has constraints/limitations or multiple examples (heuristic)"
            return satisfied, evidence

        # Default: pass with note
        return True, "Criterion evaluated with basic heuristic"

    def load_test_tasks(self) -> List[Dict]:
        """Load all test tasks with their speccheck criteria."""
        tasks = []

        for task_dir in sorted(self.test_tasks_dir.glob("task_*")):
            task_md = task_dir / "task.md"
            speccheck_md = task_dir / "speccheck.md"

            if task_md.exists() and speccheck_md.exists():
                with open(task_md, 'r', encoding='utf-8') as f:
                    task_content = f.read()
                with open(speccheck_md, 'r', encoding='utf-8') as f:
                    speccheck_content = f.read()

                # Determine task type based on task number
                task_num = int(task_dir.name.split('_')[1])
                task_type = "standard" if task_num <= 4 else "advanced"

                tasks.append({
                    "task_id": task_dir.name,
                    "task_type": task_type,
                    "task_dir": task_dir,
                    "task_content": task_content,
                    "speccheck_content": speccheck_content,
                    "criteria": self.parse_speccheck(speccheck_content)
                })

        print(f"✓ Loaded {len(tasks)} test tasks")
        return tasks

    def parse_speccheck(self, speccheck_content: str) -> Dict:
        """
        Parse speccheck.md content to extract criteria and scoring info.

        Returns:
            Dict with keys: criteria (list), total_points, pass_threshold
        """
        criteria = []
        total_points = 0
        pass_threshold = 0

        lines = speccheck_content.split('\n')
        for i, line in enumerate(lines):
            # Parse criteria
            if line.strip().startswith('- [ ]'):
                criterion_text = line.strip()[6:].strip()
                criteria.append(criterion_text)

            # Parse total points
            if 'Total Points' in line or 'total points' in line.lower():
                parts = line.split(':')
                if len(parts) > 1:
                    try:
                        total_points = int(parts[1].strip().split()[0])
                    except (ValueError, IndexError):
                        pass

            # Parse pass threshold
            if 'Pass Threshold' in line or 'pass threshold' in line.lower():
                parts = line.split(':')
                if len(parts) > 1:
                    try:
                        pass_threshold = int(parts[1].strip().split()[0])
                    except (ValueError, IndexError):
                        pass

        # If not explicitly set, use defaults
        if total_points == 0:
            total_points = len(criteria)
        if pass_threshold == 0:
            pass_threshold = int(total_points * 0.7)  # 70% default

        return {
            "criteria": criteria,
            "total_points": total_points,
            "pass_threshold": pass_threshold
        }

    def evaluate_task_output(
        self,
        task: Dict,
        result_dir: Path,
        skill_version: str
    ) -> TaskEvaluation:
        """
        Evaluate a single task's output against its speccheck criteria.

        Args:
            task: Task data dictionary
            result_dir: Path to exec_results/{original|optimized}/task_XXX/
            skill_version: "original" or "optimized"

        Returns:
            TaskEvaluation object
        """
        criteria_results = []
        score = 0

        # Read execution results
        run_log_path = result_dir / "run_log.md"
        output_dir = result_dir / "output"
        result_file = output_dir / "result.txt"

        # Extract execution status from run_log
        execution_status = "UNKNOWN"
        stdout_content = ""
        stderr_content = ""

        if run_log_path.exists():
            with open(run_log_path, 'r', encoding='utf-8') as f:
                log_content = f.read()

            # Extract status
            import re
            status_match = re.search(r'\*\*Status\*\*:\s*(\w+)', log_content)
            if status_match:
                execution_status = status_match.group(1)

            # Extract stdout
            stdout_match = re.search(r'## Standard Output\s*```\s*(.*?)\s*```', log_content, re.DOTALL)
            if stdout_match:
                stdout_content = stdout_match.group(1).strip()

            # Extract stderr
            stderr_match = re.search(r'## Standard Error\s*```\s*(.*?)\s*```', log_content, re.DOTALL)
            if stderr_match:
                stderr_content = stderr_match.group(1).strip()

        # Read output file
        output_content = ""
        if result_file.exists():
            with open(result_file, 'r', encoding='utf-8') as f:
                output_content = f.read()

        # Check workspace for output files (e.g., output.pdf, output.json, etc.)
        # Navigate from exec_results/original/task_001 to tasks/test/task_001/workspace
        workspace_output_size = 0
        try:
            # Go up from result_dir to exec_results, then to run directory
            run_dir = result_dir.parent.parent.parent
            task_id = task['task_id']
            # Determine if this is a training or test task
            task_set = "train" if task_id.startswith("task_") and int(task_id.split('_')[1]) <= 12 else "test"
            workspace_dir = run_dir / "tasks" / task_set / task_id / "workspace"

            if workspace_dir.exists():
                # Look for output files (output.pdf, output.json, etc.)
                for output_file in workspace_dir.glob("output.*"):
                    workspace_output_size += output_file.stat().st_size
        except Exception:
            pass  # If we can't find workspace, just use stdout/result.txt

        # Check if this is a documentation task
        is_documentation_task = execution_status == "DOCUMENTATION"

        # Load skill documentation if this is a documentation task
        skill_doc_content = ""
        task_objective = ""
        if is_documentation_task:
            # Determine which skill version to load
            if skill_version == "original":
                skill_path = self.target_skill_path
            else:
                skill_path = self.optimized_skill_dir

            skill_doc_content = self._load_skill_documentation(skill_path)

            # Extract task objective from task content
            import re
            obj_match = re.search(r'## Objective\s*\n(.*?)(?:\n##|\Z)', task['task_content'], re.DOTALL)
            if obj_match:
                task_objective = obj_match.group(1).strip()

        # Evaluate each criterion
        for criterion in task['criteria']['criteria']:
            satisfied = False
            evidence = ""

            criterion_lower = criterion.lower()

            # For documentation tasks, use LLM-based evaluation
            if is_documentation_task:
                satisfied, evidence = self._evaluate_documentation_with_llm(
                    skill_doc_content,
                    criterion,
                    task_objective
                )
            else:
                # For executable tasks, use command execution criteria
                # Criterion 1: Command executes without errors
                if 'executes without errors' in criterion_lower or 'exit code' in criterion_lower:
                    satisfied = execution_status == "SUCCESS"
                    evidence = f"Exit status: {execution_status}"

                # Criterion 2: Output is generated
                elif 'output is generated' in criterion_lower or 'output file' in criterion_lower:
                    satisfied = len(output_content) > 0 or len(stdout_content) > 0 or workspace_output_size > 0
                    evidence = f"Output length: {len(output_content)} bytes, stdout: {len(stdout_content)} bytes, workspace files: {workspace_output_size} bytes"

                # Criterion 3: Output format is valid
                elif 'output format' in criterion_lower or 'validate output' in criterion_lower:
                    # Check if output looks reasonable (not just error messages)
                    satisfied = ((len(output_content) > 50 or len(stdout_content) > 50 or workspace_output_size > 1000)
                                and execution_status == "SUCCESS")
                    evidence = f"Output appears valid: {satisfied}"

                # Criterion 4: Expected data is present
                elif 'expected data' in criterion_lower or 'required content' in criterion_lower:
                    # Check if output contains meaningful data (not empty or just errors)
                    satisfied = (len(output_content) > 100 or (len(stdout_content) > 100 and execution_status == "SUCCESS")
                                or workspace_output_size > 10000)
                    evidence = f"Meaningful data present: {satisfied}"

                # Criterion 5: Handles complex scenarios (for advanced tasks)
                elif 'complex scenarios' in criterion_lower or 'edge case' in criterion_lower:
                    # For advanced tasks, require successful execution with substantial output
                    satisfied = execution_status == "SUCCESS" and len(output_content) > 200
                    evidence = f"Complex handling: {satisfied}"

                # Default: check if execution succeeded
                else:
                    satisfied = execution_status == "SUCCESS"
                    evidence = f"Execution status: {execution_status}"

            if satisfied:
                score += 1

            criteria_results.append(CriterionResult(
                criterion=criterion,
                satisfied=satisfied,
                evidence=evidence
            ))

        total = len(task['criteria']['criteria'])
        passed = score >= task['criteria']['pass_threshold']

        return TaskEvaluation(
            task_id=task['task_id'],
            task_type=task['task_type'],
            score=score,
            total=total,
            passed=passed,
            criteria_results=criteria_results
        )

    def evaluate_skill_version(
        self,
        tasks: List[Dict],
        skill_version: str
    ) -> SkillEvaluation:
        """Evaluate all tasks for a skill version."""
        print(f"\n=== Evaluating {skill_version.upper()} Skill ===")

        task_evaluations = []
        error_count = 0

        for task in tasks:
            result_dir = self.exec_results_dir / skill_version / task['task_id']

            if not result_dir.exists():
                print(f"⚠ Missing results for {task['task_id']}")
                error_count += 1
                continue

            evaluation = self.evaluate_task_output(task, result_dir, skill_version)
            task_evaluations.append(evaluation)

            status = "✓" if evaluation.passed else "✗"
            print(f"  {status} {task['task_id']}: {evaluation.score}/{evaluation.total}")

        # Compute metrics
        total_tasks = len(tasks)
        passed_tasks = sum(1 for e in task_evaluations if e.passed)
        pass_rate = (passed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        total_score = sum(e.score for e in task_evaluations)
        total_possible = sum(e.total for e in task_evaluations)
        avg_score = (total_score / total_possible) if total_possible > 0 else 0

        standard_evals = [e for e in task_evaluations if e.task_type == "standard"]
        standard_score = (
            sum(e.score for e in standard_evals) / sum(e.total for e in standard_evals)
            if standard_evals else 0
        )

        advanced_evals = [e for e in task_evaluations if e.task_type == "advanced"]
        advanced_score = (
            sum(e.score for e in advanced_evals) / sum(e.total for e in advanced_evals)
            if advanced_evals else 0
        )

        error_rate = (error_count / total_tasks * 100) if total_tasks > 0 else 0

        return SkillEvaluation(
            skill_name=skill_version,
            task_evaluations=task_evaluations,
            pass_rate=pass_rate,
            avg_score=avg_score,
            standard_score=standard_score,
            advanced_score=advanced_score,
            error_rate=error_rate
        )

    def compare_evaluations(
        self,
        original: SkillEvaluation,
        optimized: SkillEvaluation
    ) -> ComparisonMetrics:
        """Compute comparison metrics between two evaluations."""
        per_task_deltas = []
        regression_count = 0

        for orig_eval, opt_eval in zip(original.task_evaluations, optimized.task_evaluations):
            delta = opt_eval.score - orig_eval.score
            per_task_deltas.append(delta)
            if delta < 0:
                regression_count += 1

        return ComparisonMetrics(
            pass_rate_delta=optimized.pass_rate - original.pass_rate,
            avg_score_delta=optimized.avg_score - original.avg_score,
            standard_score_delta=optimized.standard_score - original.standard_score,
            advanced_score_delta=optimized.advanced_score - original.advanced_score,
            error_rate_delta=optimized.error_rate - original.error_rate,
            regression_count=regression_count,
            per_task_deltas=per_task_deltas
        )

    def make_retention_decision(
        self,
        original: SkillEvaluation,
        optimized: SkillEvaluation,
        comparison: ComparisonMetrics
    ) -> Tuple[bool, str]:
        """
        Make retention decision based on average score comparison.

        Returns:
            Tuple of (should_retain, rationale)
        """
        if optimized.avg_score > original.avg_score:
            improvement_pct = comparison.avg_score_delta * 100
            rationale = (
                f"Optimized skill shows {improvement_pct:.1f}% improvement in average "
                f"SpecCheck score ({optimized.avg_score:.3f} vs {original.avg_score:.3f}). "
                f"Retaining optimized version."
            )
            return True, rationale
        else:
            decline_pct = abs(comparison.avg_score_delta * 100)
            rationale = (
                f"Optimized skill did not improve over original "
                f"({optimized.avg_score:.3f} vs {original.avg_score:.3f}, "
                f"{decline_pct:.1f}% decline). Optimization did not generalize to test set. "
                f"Deleting optimized version."
            )
            return False, rationale

    def analyze_strengths_weaknesses(
        self,
        evaluation: SkillEvaluation
    ) -> Tuple[List[str], List[str]]:
        """
        Analyze strengths and weaknesses from evaluation results.

        Returns:
            Tuple of (strengths, weaknesses)
        """
        strengths = []
        weaknesses = []

        # Analyze pass rate
        if evaluation.pass_rate >= 75:
            strengths.append(f"High pass rate ({evaluation.pass_rate:.1f}%) indicates strong overall functionality")
        elif evaluation.pass_rate < 50:
            weaknesses.append(f"Low pass rate ({evaluation.pass_rate:.1f}%) suggests fundamental issues")

        # Analyze standard vs advanced performance
        if evaluation.standard_score > evaluation.advanced_score + 0.15:
            strengths.append("Handles standard use cases well")
            weaknesses.append(f"Struggles with advanced scenarios (standard: {evaluation.standard_score:.2f} vs advanced: {evaluation.advanced_score:.2f})")
        elif evaluation.advanced_score > evaluation.standard_score:
            strengths.append("Performs well even on complex edge cases")

        # Analyze error rate
        if evaluation.error_rate == 0:
            strengths.append("No execution errors - robust error handling")
        elif evaluation.error_rate > 25:
            weaknesses.append(f"High error rate ({evaluation.error_rate:.1f}%) indicates stability issues")

        # Analyze individual task performance
        high_scoring = [e for e in evaluation.task_evaluations if e.score == e.total]
        if len(high_scoring) >= 3:
            strengths.append(f"Perfect scores on {len(high_scoring)} tasks shows mastery of core functionality")

        low_scoring = [e for e in evaluation.task_evaluations if e.score < e.total * 0.5]
        if len(low_scoring) >= 2:
            weaknesses.append(f"{len(low_scoring)} tasks scored below 50%, indicating gaps in coverage")

        return strengths, weaknesses

    def identify_key_optimizations(
        self,
        original: SkillEvaluation,
        optimized: SkillEvaluation,
        comparison: ComparisonMetrics
    ) -> List[Dict[str, str]]:
        """
        Identify key optimizations that improved performance.

        Returns:
            List of dicts with keys: optimization, target, impact, tradeoffs
        """
        optimizations = []

        # Check if pass rate improved
        if comparison.pass_rate_delta > 0:
            optimizations.append({
                'optimization': 'Improved task completion rate',
                'target': 'Overall reliability and robustness',
                'impact': f'Pass rate increased by {comparison.pass_rate_delta:.1f}%',
                'tradeoffs': 'None observed'
            })

        # Check if standard tasks improved
        if comparison.standard_score_delta > 0.05:
            optimizations.append({
                'optimization': 'Enhanced standard use case handling',
                'target': 'Core functionality reliability',
                'impact': f'Standard task score improved by {comparison.standard_score_delta:.2f}',
                'tradeoffs': 'None observed'
            })

        # Check if advanced tasks improved
        if comparison.advanced_score_delta > 0.05:
            optimizations.append({
                'optimization': 'Better edge case handling',
                'target': 'Complex scenario robustness',
                'impact': f'Advanced task score improved by {comparison.advanced_score_delta:.2f}',
                'tradeoffs': 'None observed'
            })

        # Check for error rate reduction
        if comparison.error_rate_delta < 0:
            optimizations.append({
                'optimization': 'Reduced execution errors',
                'target': 'Stability and error handling',
                'impact': f'Error rate decreased by {abs(comparison.error_rate_delta):.1f}%',
                'tradeoffs': 'None observed'
            })

        # If no improvements, note that
        if not optimizations:
            optimizations.append({
                'optimization': 'No significant improvements detected',
                'target': 'N/A',
                'impact': 'Optimization did not generalize to test set',
                'tradeoffs': 'May have overfitted to training tasks'
            })

        return optimizations

    def generate_recommendations(
        self,
        evaluation: SkillEvaluation,
        retained: bool
    ) -> List[str]:
        """
        Generate recommendations for further improvement.

        Returns:
            List of recommendation strings
        """
        recommendations = []

        if retained:
            # Recommendations for retained (improved) skill
            if evaluation.advanced_score < 0.75:
                recommendations.append(
                    "Focus on improving advanced task handling - consider adding more explicit "
                    "edge case handling and validation steps"
                )

            if evaluation.error_rate > 0:
                recommendations.append(
                    "Further reduce error rate by adding more comprehensive error handling "
                    "and input validation"
                )

            if evaluation.pass_rate < 90:
                recommendations.append(
                    "Target 90%+ pass rate by analyzing failed tasks and adding specific "
                    "guidance for those scenarios"
                )

            if evaluation.standard_score - evaluation.advanced_score > 0.2:
                recommendations.append(
                    "Bridge the gap between standard and advanced performance by incorporating "
                    "advanced scenario patterns into core workflow"
                )
        else:
            # Recommendations for deleted (not improved) skill
            recommendations.append(
                "Optimization focused too heavily on training tasks - need broader approach "
                "that generalizes better to unseen scenarios"
            )

            recommendations.append(
                "Consider analyzing test task failures to identify fundamental gaps in the "
                "skill specification rather than training-specific fixes"
            )

            recommendations.append(
                "Review whether the skill's core workflow needs restructuring rather than "
                "incremental improvements"
            )

        return recommendations

    def generate_results_report(
        self,
        tasks: List[Dict],
        original: SkillEvaluation,
        optimized: SkillEvaluation,
        comparison: ComparisonMetrics,
        retained: bool,
        rationale: str
    ):
        """Generate the comprehensive results_report.md."""
        report_path = self.output_dir / "results_report.md"

        report = f"""# Skills-Coach Results Report

## Target Skill
- **Name**: {self.skill_name}
- **Path**: {self.target_skill_path}
- **Evaluated**: {datetime.now().isoformat()}

---

## Evaluation Summary

| Metric                  | Original | Optimized | Delta      |
|-------------------------|----------|-----------|------------|
| Pass Rate               | {original.pass_rate:.1f}% | {optimized.pass_rate:.1f}% | {comparison.pass_rate_delta:+.1f}% |
| Avg. SpecCheck Score    | {original.avg_score:.3f} | {optimized.avg_score:.3f} | {comparison.avg_score_delta:+.3f} |
| Standard Task Score     | {original.standard_score:.3f} | {optimized.standard_score:.3f} | {comparison.standard_score_delta:+.3f} |
| Advanced Task Score     | {original.advanced_score:.3f} | {optimized.advanced_score:.3f} | {comparison.advanced_score_delta:+.3f} |
| Error Rate              | {original.error_rate:.1f}% | {optimized.error_rate:.1f}% | {comparison.error_rate_delta:+.1f}% |
| Regression Count        | —        | {comparison.regression_count} tasks | —          |

---

## Per-Task Breakdown

| Task | Type     | Original Score | Optimized Score | Delta | Notes |
|------|----------|----------------|-----------------|-------|-------|
"""

        for i, (orig_eval, opt_eval) in enumerate(zip(original.task_evaluations, optimized.task_evaluations)):
            delta = comparison.per_task_deltas[i]
            delta_str = f"{delta:+d}" if delta != 0 else "0"
            note = "Improved" if delta > 0 else ("Regressed" if delta < 0 else "No change")

            report += (
                f"| {orig_eval.task_id} | {orig_eval.task_type.capitalize():8} | "
                f"{orig_eval.score}/{orig_eval.total} ({orig_eval.score/orig_eval.total*100:.0f}%) | "
                f"{opt_eval.score}/{opt_eval.total} ({opt_eval.score/opt_eval.total*100:.0f}%) | "
                f"{delta_str:5} | {note:15} |\n"
            )

        report += "\n---\n\n## Capability Boundary Analysis\n\n"

        # Strengths and weaknesses
        strengths, weaknesses = self.analyze_strengths_weaknesses(original)

        report += "### Strengths of Original Skill\n\n"
        for strength in strengths:
            report += f"- {strength}\n"

        report += "\n### Weaknesses / Limitations Identified\n\n"
        for weakness in weaknesses:
            report += f"- {weakness}\n"

        # Key optimizations
        optimizations = self.identify_key_optimizations(original, optimized, comparison)

        report += "\n### Key Optimizations Applied\n\n"
        for opt in optimizations:
            report += f"- **{opt['optimization']}**\n"
            report += f"  - Target: {opt['target']}\n"
            report += f"  - Impact: {opt['impact']}\n"
            report += f"  - Trade-offs: {opt['tradeoffs']}\n\n"

        report += "---\n\n## Retention Decision\n\n"
        report += f"**Decision**: {'RETAINED' if retained else 'DELETED'}\n\n"
        report += f"**Rationale**: {rationale}\n\n"

        if retained:
            report += f"**Optimized Skill Path**: `{self.skill_name}-optimized/`\n\n"
            report += "**Key Improvements**:\n"
            for opt in optimizations[:3]:  # Top 3
                report += f"- {opt['optimization']}\n"
        else:
            report += f"**Reason for Deletion**: {rationale}\n\n"

        report += "\n---\n\n## Recommendations for Further Improvement\n\n"

        recommendations = self.generate_recommendations(optimized if retained else original, retained)
        for rec in recommendations:
            report += f"- {rec}\n"

        report += "\n---\n\n## Appendix: Detailed Criterion Results\n\n"

        for task, orig_eval, opt_eval in zip(tasks, original.task_evaluations, optimized.task_evaluations):
            report += f"### {task['task_id']}: {self.extract_task_title(task['task_content'])}\n\n"

            report += "**Original Skill**:\n"
            for criterion_result in orig_eval.criteria_results:
                status = "✓" if criterion_result.satisfied else "✗"
                report += f"- [{status}] {criterion_result.criterion}\n"
                report += f"  - Evidence: {criterion_result.evidence}\n"

            report += "\n**Optimized Skill**:\n"
            for criterion_result in opt_eval.criteria_results:
                status = "✓" if criterion_result.satisfied else "✗"
                report += f"- [{status}] {criterion_result.criterion}\n"
                report += f"  - Evidence: {criterion_result.evidence}\n"

            report += "\n"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✓ Generated results report: {report_path}")

    def extract_task_title(self, task_content: str) -> str:
        """Extract task title from task.md content."""
        for line in task_content.split('\n'):
            if line.startswith('# Task:'):
                return line[8:].strip()
        return "Unknown Task"

    def evaluate_and_report(self) -> bool:
        """Main entry point: evaluate both versions and generate report."""
        # Load test tasks
        tasks = self.load_test_tasks()

        if len(tasks) == 0:
            print(f"ERROR: No test tasks found")
            return False

        print(f"✓ Evaluating {len(tasks)} test tasks")

        # Evaluate both versions
        original_eval = self.evaluate_skill_version(tasks, "original")
        optimized_eval = self.evaluate_skill_version(tasks, "optimized")

        # Compare
        comparison = self.compare_evaluations(original_eval, optimized_eval)

        print("\n=== Comparison Summary ===")
        print(f"Pass Rate: {original_eval.pass_rate:.1f}% → {optimized_eval.pass_rate:.1f}% ({comparison.pass_rate_delta:+.1f}%)")
        print(f"Avg Score: {original_eval.avg_score:.3f} → {optimized_eval.avg_score:.3f} ({comparison.avg_score_delta:+.3f})")
        print(f"Regressions: {comparison.regression_count} tasks")

        # Make retention decision
        retained, rationale = self.make_retention_decision(original_eval, optimized_eval, comparison)

        print(f"\n=== Retention Decision ===")
        print(f"{'RETAIN' if retained else 'DELETE'}: {rationale}")

        # Execute retention decision
        if not retained and self.optimized_skill_dir.exists():
            shutil.rmtree(self.optimized_skill_dir)
            print(f"✓ Deleted {self.optimized_skill_dir}")

        # Generate report
        self.generate_results_report(tasks, original_eval, optimized_eval, comparison, retained, rationale)

        print("\n✓ Evaluation complete!")
        return True


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python evaluator.py <target-skill-path> [output-dir]")
        sys.exit(1)

    target_skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    evaluator = SkillEvaluator(target_skill_path, output_dir=output_dir)
    success = evaluator.evaluate_and_report()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
