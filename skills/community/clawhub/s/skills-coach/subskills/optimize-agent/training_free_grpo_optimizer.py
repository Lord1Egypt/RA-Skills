#!/usr/bin/env python3
"""
Training-Free GRPO Optimizer for Skills-Coach v2.3.1

Implements Training-Free Group Relative Policy Optimization based on:
"Training-Free Group Relative Policy Optimization" (arXiv:2510.08191)

Key differences from vanilla GRPO:
1. No parameter updates - maintains external experience library E
2. Uses semantic advantage instead of numerical advantage
3. Leverages LLM introspection to extract experiential knowledge
4. Applies different strategies for markdown vs code optimization
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Warning: anthropic SDK not available, some features will be limited")


@dataclass
class ExperienceEntry:
    """Single entry in the experience library."""
    content: str
    domain: str  # 'markdown' or 'code'
    confidence: float
    created_at: str
    last_used: str
    success_count: int = 0
    failure_count: int = 0


@dataclass
class RolloutSummary:
    """Summary of a single rollout."""
    variant_id: str
    content: str
    score: int
    total: int
    summary: str


class ExperienceLibrary:
    """Manages the experience knowledge base."""

    def __init__(self, domain: str = "general"):
        self.domain = domain
        self.experiences: List[ExperienceEntry] = []

    def add(self, content: str, domain: str, confidence: float = 0.8):
        """Add new experience to library."""
        entry = ExperienceEntry(
            content=content,
            domain=domain,
            confidence=confidence,
            created_at=datetime.now().isoformat(),
            last_used=datetime.now().isoformat()
        )
        self.experiences.append(entry)

    def delete(self, index: int):
        """Remove experience by index."""
        if 0 <= index < len(self.experiences):
            self.experiences.pop(index)

    def modify(self, index: int, new_content: str):
        """Modify existing experience."""
        if 0 <= index < len(self.experiences):
            self.experiences[index].content = new_content
            self.experiences[index].last_used = datetime.now().isoformat()

    def get_relevant_experiences(self, domain: str, max_count: int = 5) -> List[str]:
        """Get most relevant experiences for given domain."""
        relevant = [e for e in self.experiences if e.domain == domain or e.domain == "general"]
        relevant.sort(key=lambda e: (e.confidence, e.last_used), reverse=True)
        return [e.content for e in relevant[:max_count]]

    def to_prompt_context(self, domain: str) -> str:
        """Convert experiences to prompt context."""
        experiences = self.get_relevant_experiences(domain)
        if not experiences:
            return ""

        context = "# Learned Experiences\n\n"
        context += "Based on previous optimization attempts, here are key insights:\n\n"
        for i, exp in enumerate(experiences, 1):
            context += f"{i}. {exp}\n"
        context += "\n"
        return context

    def save(self, filepath: Path):
        """Save experience library to file."""
        data = {
            'domain': self.domain,
            'experiences': [asdict(e) for e in self.experiences]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, filepath: Path) -> 'ExperienceLibrary':
        """Load experience library from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        lib = cls(domain=data['domain'])
        lib.experiences = [ExperienceEntry(**e) for e in data['experiences']]
        return lib


class TrainingFreeGRPOOptimizer:
    """Training-Free GRPO optimizer using semantic advantages."""

    def __init__(
        self,
        target_skill_path: str,
        training_tasks_dir: str = "tasks/train",
        output_dir: str = ".",
        group_size: int = 5,
        num_epochs: int = 3,
        config: Optional[Dict] = None,
        api_key: Optional[str] = None
    ):
        self.target_skill_path = Path(target_skill_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.group_size = group_size
        self.num_epochs = num_epochs
        self.config = config or self._load_config()

        # Initialize Anthropic client if available
        self.client = None
        if ANTHROPIC_AVAILABLE:
            try:
                # Support both API key and auth token
                auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
                base_url = os.environ.get("ANTHROPIC_BASE_URL")

                if auth_token:
                    # Use auth token with custom base URL
                    self.client = anthropic.Anthropic(
                        api_key=auth_token,
                        base_url=base_url if base_url else None,
                        timeout=120.0  # 2 minutes timeout
                    )
                else:
                    # Use standard API key
                    self.client = anthropic.Anthropic(
                        api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"),
                        timeout=120.0  # 2 minutes timeout
                    )
            except Exception as e:
                print(f"Warning: Failed to initialize Anthropic client: {e}")

        # Experience libraries
        self.markdown_experiences = ExperienceLibrary(domain="markdown")
        self.code_experiences = ExperienceLibrary(domain="code")

        # State tracking
        self.original_skill_content = ""
        self.current_best_content = ""
        self.current_best_score = 0
        self.optimization_history = []

        # Setup optimization directory for saving intermediate variants
        self.optimization_dir = Path(output_dir).parent / "optimization"
        self.optimization_dir.mkdir(exist_ok=True)

        # Load Training-Free GRPO config
        self.tf_grpo_config = self.config.get('training_free_grpo', {})
        self.save_intermediate = self.tf_grpo_config.get('save_intermediate_variants', True)

    def _load_config(self) -> Dict:
        """Load configuration from config.yaml."""
        config_path = Path(__file__).parent.parent.parent / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def load_original_skill(self) -> bool:
        """Load the original SKILL.md content."""
        skill_path = self.target_skill_path / "SKILL.md"
        if not skill_path.exists():
            print(f"ERROR: SKILL.md not found at {skill_path}")
            return False

        with open(skill_path, 'r', encoding='utf-8') as f:
            self.original_skill_content = f.read()
            self.current_best_content = self.original_skill_content

        print(f"✓ Loaded original SKILL.md from {skill_path}")
        return True

    def detect_skill_type(self, skill_content: str) -> str:
        """Detect if skill is markdown-only or contains executable code."""
        skill_dir = self.target_skill_path
        has_code = any(skill_dir.glob("*.py")) or any(skill_dir.glob("*.sh"))
        has_commands = "```bash" in skill_content or "```python" in skill_content

        if has_code:
            return "code"
        elif has_commands:
            return "markdown_with_commands"
        else:
            return "markdown_only"

    def generate_rollout_summary(self, variant_content: str, task: Dict, score: int, total: int, criteria_results: List[Dict] = None) -> str:
        """Use LLM to generate summary of a rollout with detailed criteria analysis."""
        # TEMPORARY: Disable LLM summary generation due to API timeout issues
        # Return simple fallback summary instead
        print(f"    Using fallback summary (LLM disabled)")
        return f"Variant scored {score}/{total} ({score/total*100:.1f}%)"

        # Original LLM-based implementation (disabled)
        if False and self.client:
            return f"Variant scored {score}/{total}"

        # Include detailed criteria feedback
        criteria_text = ""
        if criteria_results:
            criteria_text = "\n**Evaluation Criteria:**\n"
            for i, criterion in enumerate(criteria_results, 1):
                status = "✓" if criterion.get('passed', False) else "✗"
                criteria_text += f"{status} Criterion {i}: {criterion.get('description', 'N/A')}\n"
                if 'evidence' in criterion:
                    criteria_text += f"  Evidence: {criterion['evidence']}\n"

        prompt = f"""Analyze this skill variant and its performance in detail.

**Skill Variant:**
{variant_content[:2000]}...

**Task:** {task['task_id']}
**Score:** {score}/{total} ({score/total*100:.1f}%)
{criteria_text}

Provide a detailed analysis (3-4 sentences) of:
1. What approach this variant takes
2. Why it achieved this score (which criteria passed/failed)
3. What specific elements are MISSING (e.g., code examples, documentation sections, edge cases)
4. Concrete suggestions for what to ADD

Analysis:"""

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
                    print(f"Warning: Failed to generate summary (attempt {attempt + 1}/{max_retries}): {e}")
                    import time
                    time.sleep(2)
                else:
                    print(f"Error: Failed to generate summary after {max_retries} attempts: {e}")
                    return None  # Return None to signal failure

    def extract_semantic_advantage(
        self,
        rollout_summaries: List[RolloutSummary],
        experience_library: ExperienceLibrary,
        domain: str
    ) -> str:
        """Extract semantic advantage from group of rollouts."""
        # TEMPORARY: Disable LLM semantic advantage extraction due to API timeout issues
        print(f"    Using fallback semantic advantage (LLM disabled)")
        return "Focus on reducing documentation length while maintaining code examples and structure."

        # Original LLM-based implementation (disabled)
        if False and self.client:
            return ""

        scores = [r.score / r.total for r in rollout_summaries]
        if len(set(scores)) <= 1:
            return ""

        summaries_text = "\n\n".join([
            f"**Variant {r.variant_id}** (Score: {r.score}/{r.total}):\n{r.summary}"
            for r in rollout_summaries
        ])

        existing_experiences = experience_library.to_prompt_context(domain)

        prompt = f"""Analyze multiple skill optimization attempts to extract key insights.

{existing_experiences}

**Current Rollout Group:**
{summaries_text}

Extract 2-3 key insights about what makes a skill variant successful. Focus on:
- Patterns that correlate with higher scores
- Common mistakes in lower-scoring variants
- SPECIFIC missing elements that need to be ADDED (code examples, documentation sections, edge cases)
- Actionable guidance for future optimization with concrete examples

Format as concise bullet points with specific recommendations.

Key Insights:"""

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
                    print(f"Warning: Failed to extract semantic advantage (attempt {attempt + 1}/{max_retries}): {e}")
                    import time
                    time.sleep(2)
                else:
                    print(f"Error: Failed to extract semantic advantage after {max_retries} attempts: {e}")
                    return None  # Return None to signal failure

    def update_experience_library(
        self,
        semantic_advantages: List[str],
        experience_library: ExperienceLibrary,
        domain: str
    ) -> List[str]:
        """Update experience library based on semantic advantages."""
        if not self.client or not semantic_advantages:
            return ["Keep"]

        advantages_text = "\n\n".join(semantic_advantages)
        current_exp_text = "\n".join([
            f"{i+1}. {e.content}"
            for i, e in enumerate(experience_library.experiences)
        ])

        prompt = f"""Manage an experience library for skill optimization.

**Current Experience Library:**
{current_exp_text if current_exp_text else "(Empty)"}

**New Insights:**
{advantages_text}

Decide how to update the library. Focus on ACTIONABLE, SPECIFIC guidance.

Operations:
- Add: Add new experience with CONCRETE recommendations (e.g., "Add code examples using ```python blocks", "Include edge case section for error handling")
- Delete <index>: Remove vague or unhelpful experience
- Modify <index>: Make experience more specific and actionable
- Keep: No changes

Provide operations as JSON list:
```json
[
  {{"operation": "Add", "content": "Add code examples using ```language blocks to demonstrate usage"}},
  {{"operation": "Modify", "index": 1, "content": "Include a dedicated 'Edge Cases' section covering error scenarios and boundary conditions"}},
  {{"operation": "Delete", "index": 2}}
]
```

Operations:"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                json_text = response_text

            operations = json.loads(json_text)
            operation_log = []

            for op in operations:
                op_type = op.get("operation", "Keep")

                if op_type == "Add":
                    content = op.get("content", "")
                    if content:
                        experience_library.add(content, domain)
                        operation_log.append(f"Added: {content[:50]}...")

                elif op_type == "Delete":
                    index = op.get("index", -1)
                    if 0 <= index < len(experience_library.experiences):
                        deleted = experience_library.experiences[index].content
                        experience_library.delete(index)
                        operation_log.append(f"Deleted: {deleted[:50]}...")

                elif op_type == "Modify":
                    index = op.get("index", -1)
                    content = op.get("content", "")
                    if 0 <= index < len(experience_library.experiences) and content:
                        experience_library.modify(index, content)
                        operation_log.append(f"Modified index {index}")

                elif op_type == "Keep":
                    operation_log.append("Keep")

            return operation_log

        except Exception as e:
            print(f"Warning: Failed to update experience library: {e}")
            return ["Keep"]

    def generate_markdown_variant(self, experience_context: str, iteration: int) -> str:
        """Generate optimized markdown variant with intelligent structural improvements."""
        if not self.client:
            return self.current_best_content

        # Truncate content if too long to avoid API timeouts
        content_to_send = self.current_best_content
        max_content_length = 15000  # Limit to ~15k chars to stay within token limits
        if len(content_to_send) > max_content_length:
            print(f"  ⚠ Content too long ({len(content_to_send)} chars), truncating to {max_content_length} chars")
            content_to_send = content_to_send[:max_content_length] + "\n\n[... content truncated for optimization ...]"

        prompt = f"""Optimize this skill's documentation (SKILL.md) by making CONCRETE IMPROVEMENTS.

{experience_context}

**Current Best Version:**
{content_to_send}

**IMPORTANT INSTRUCTIONS:**
You must generate an IMPROVED version that ADDS missing elements:

1. **Code Examples**: If missing, ADD concrete code examples in markdown code blocks
   - Use ```language syntax
   - Show realistic usage scenarios
   - Include input/output examples

2. **Documentation Structure**: If incomplete, ADD missing sections:
   - Overview/Purpose
   - Usage Instructions
   - Examples
   - Configuration/Options
   - Edge Cases/Limitations

3. **Edge Cases**: If missing, ADD sections covering:
   - Error handling scenarios
   - Boundary conditions
   - Common pitfalls
   - Troubleshooting tips

4. **Clarity**: Improve explanations with:
   - Clear step-by-step instructions
   - Visual formatting (headers, lists, tables)
   - Concrete examples instead of abstract descriptions

**DO NOT** just rephrase existing content. **DO ADD** missing structural elements.

Provide the complete improved SKILL.md:"""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=6000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Warning: Failed to generate markdown variant (attempt {attempt + 1}/{max_retries}): {e}")
                    import time
                    time.sleep(2)  # Wait 2 seconds before retry
                else:
                    print(f"Error: Failed to generate markdown variant after {max_retries} attempts: {e}")
                    return None  # Return None to signal failure

    def optimize(self, training_tasks: List[Dict]) -> Dict:
        """Main optimization loop using Training-Free GRPO."""
        print("\n" + "="*60)
        print("Training-Free GRPO Optimization")
        print("="*60)

        if not self.client:
            print("⚠ Anthropic client not available, using heuristic optimization")

        skill_type = self.detect_skill_type(self.original_skill_content)
        print(f"✓ Detected skill type: {skill_type}")

        # Step 1: Optimize commands if skill has executable commands
        if skill_type in ["markdown_with_commands", "code"]:
            print("\n=== Phase 1: Command Optimization ===")
            self._optimize_commands()

        # Step 2: Optimize markdown documentation
        if skill_type == "code":
            experience_lib = self.code_experiences
            domain = "code"
        else:
            experience_lib = self.markdown_experiences
            domain = "markdown"

        print("\n=== Phase 2: Documentation Optimization ===")

        print("\n=== Computing Baseline Score ===")
        baseline_score = self._compute_baseline(training_tasks)
        print(f"✓ Baseline: {baseline_score['total_score']}/{baseline_score['total_possible']} ({baseline_score['percentage']:.1f}%)")

        self.current_best_score = baseline_score['total_score']

        for epoch in range(1, self.num_epochs + 1):
            print(f"\n{'='*60}")
            print(f"EPOCH {epoch}/{self.num_epochs}")
            print("="*60)

            experience_context = experience_lib.to_prompt_context(domain)

            print(f"✓ Generating {self.group_size} rollout variants...")
            rollouts = []
            failed_variants = 0

            for g in range(self.group_size):
                variant_id = f"e{epoch}-g{g+1}"
                print(f"  Generating variant {g+1}/{self.group_size} ({variant_id}) via API...")
                variant_content = self.generate_markdown_variant(experience_context, epoch)

                if variant_content is None:
                    failed_variants += 1
                    print(f"  ✗ Failed to generate variant {variant_id}")
                    continue

                print(f"  ✓ Generated variant {variant_id} ({len(variant_content)} chars)")
                rollouts.append({
                    'variant_id': variant_id,
                    'content': variant_content
                })

            # If all variants failed, abort optimization
            if failed_variants == self.group_size:
                print(f"\n✗ ERROR: All {self.group_size} variants failed to generate in epoch {epoch}")
                print("✗ Aborting optimization due to repeated API failures")
                return {
                    'baseline_score': baseline_score['total_score'],
                    'final_score': baseline_score['total_score'],
                    'improvement': 0,
                    'optimized_content': self.original_skill_content,
                    'status': 'failed',
                    'error': 'All variant generation attempts failed'
                }

            if failed_variants > 0:
                print(f"⚠ Warning: {failed_variants}/{self.group_size} variants failed to generate")

            print(f"✓ Scoring {len(rollouts)} variants...")
            rollout_summaries = []

            for i, rollout in enumerate(rollouts, 1):
                print(f"  Scoring variant {i}/{len(rollouts)} ({rollout['variant_id']})...")
                scores = self._evaluate_variant(rollout['content'], training_tasks)
                total_score = sum(s['score'] for s in scores)
                total_possible = sum(s['total'] for s in scores)
                print(f"    Score: {total_score}/{total_possible}")

                # Collect criteria results for detailed feedback
                criteria_results = []
                for task_score in scores:
                    if 'criteria' in task_score:
                        criteria_results.extend(task_score['criteria'])

                print(f"    Generating summary via API...")
                summary = self.generate_rollout_summary(
                    rollout['content'],
                    training_tasks[0],
                    total_score,
                    total_possible,
                    criteria_results
                )

                # If summary generation failed, use fallback
                if summary is None:
                    print(f"    ⚠ Summary generation failed, using fallback")
                    summary = f"Variant scored {total_score}/{total_possible}"
                else:
                    print(f"    ✓ Summary generated")

                rollout_summaries.append(RolloutSummary(
                    variant_id=rollout['variant_id'],
                    content=rollout['content'],
                    score=total_score,
                    total=total_possible,
                    summary=summary
                ))

                print(f"  {rollout['variant_id']}: {total_score}/{total_possible} ({total_score/total_possible*100:.1f}%)")

            print("✓ Extracting semantic advantage...")
            semantic_advantage = self.extract_semantic_advantage(
                rollout_summaries,
                experience_lib,
                domain
            )

            # If semantic advantage extraction failed, abort optimization
            if semantic_advantage is None:
                print(f"\n✗ ERROR: Failed to extract semantic advantage in epoch {epoch}")
                print("✗ Aborting optimization due to repeated API failures")
                return {
                    'baseline_score': baseline_score['total_score'],
                    'final_score': self.current_best_score,
                    'improvement': self.current_best_score - baseline_score['total_score'],
                    'optimized_content': self.current_best_content,
                    'status': 'failed',
                    'error': 'Semantic advantage extraction failed'
                }

            if semantic_advantage:
                print(f"  Insight: {semantic_advantage[:100]}...")
                print("✓ Updating experience library...")
                operations = self.update_experience_library(
                    [semantic_advantage],
                    experience_lib,
                    domain
                )
                for op in operations:
                    print(f"  - {op}")
            else:
                operations = []

            best_rollout = max(rollout_summaries, key=lambda r: r.score)
            if best_rollout.score > self.current_best_score:
                self.current_best_content = best_rollout.content
                self.current_best_score = best_rollout.score
                print(f"✓ New best: {best_rollout.variant_id} with {best_rollout.score}/{best_rollout.total}")
            else:
                print(f"  No improvement (best: {best_rollout.score}/{best_rollout.total})")

            # Save intermediate variants if enabled
            if self.save_intermediate:
                self._save_epoch_variants(epoch, rollout_summaries, best_rollout)

            self.optimization_history.append({
                'epoch': epoch,
                'rollouts': [asdict(r) for r in rollout_summaries],
                'best_variant': best_rollout.variant_id,
                'best_score': best_rollout.score,
                'semantic_advantage': semantic_advantage,
                'experience_operations': operations
            })

        print("\n" + "="*60)
        print("Optimization Complete")
        print("="*60)

        final_score = self.current_best_score
        improvement = final_score - baseline_score['total_score']
        print(f"Final Score: {final_score}/{baseline_score['total_possible']} ({final_score/baseline_score['total_possible']*100:.1f}%)")
        print(f"Improvement: +{improvement} points")

        optimized_path = self.output_dir / "SKILL.md"
        with open(optimized_path, 'w') as f:
            f.write(self.current_best_content)
        print(f"✓ Saved optimized skill to {optimized_path}")

        exp_path = self.output_dir / f"experience_library_{domain}.json"
        experience_lib.save(exp_path)
        print(f"✓ Saved experience library to {exp_path}")

        log_path = self.output_dir / "training_free_grpo_log.json"
        with open(log_path, 'w') as f:
            json.dump({
                'baseline': baseline_score,
                'final_score': final_score,
                'improvement': improvement,
                'skill_type': skill_type,
                'domain': domain,
                'epochs': self.optimization_history
            }, f, indent=2)
        print(f"✓ Saved optimization log to {log_path}")

        return {
            'baseline_score': baseline_score['total_score'],
            'final_score': final_score,
            'improvement': improvement,
            'optimized_content': self.current_best_content
        }

    def _compute_baseline(self, training_tasks: List[Dict]) -> Dict:
        """Compute baseline score on training tasks."""
        print(f"  Computing baseline on {len(training_tasks)} training tasks...")
        scores = self._evaluate_variant(self.original_skill_content, training_tasks)
        total_score = sum(s['score'] for s in scores)
        total_possible = sum(s['total'] for s in scores)
        print(f"  Baseline computed: {total_score}/{total_possible}")

        return {
            'total_score': total_score,
            'total_possible': total_possible,
            'percentage': (total_score / total_possible * 100) if total_possible > 0 else 0,
            'task_scores': scores
        }

    def _evaluate_variant(self, variant_content: str, training_tasks: List[Dict]) -> List[Dict]:
        """Evaluate a variant on training tasks (heuristic scoring with detailed criteria)."""
        scores = []
        for task in training_tasks:
            score, criteria = self._heuristic_score(variant_content, task)
            scores.append({
                'task_id': task['task_id'],
                'score': score,
                'total': 5,
                'criteria': criteria
            })
        return scores

    def _heuristic_score(self, content: str, task: Dict) -> tuple:
        """Simple heuristic scoring with detailed criteria feedback."""
        score = 0
        criteria = []

        # Criterion 1: Has proper structure (headers)
        if "##" in content:
            score += 1
            criteria.append({
                'passed': True,
                'description': 'Has proper structure with headers',
                'evidence': 'Found markdown headers'
            })
        else:
            criteria.append({
                'passed': False,
                'description': 'Has proper structure with headers',
                'evidence': 'No markdown headers found'
            })

        # Criterion 2: Has code examples
        if "```" in content:
            score += 1
            criteria.append({
                'passed': True,
                'description': 'Contains code examples',
                'evidence': 'Found code blocks'
            })
        else:
            criteria.append({
                'passed': False,
                'description': 'Contains code examples',
                'evidence': 'No code blocks found - ADD code examples'
            })

        # Criterion 3: Has usage/example sections
        if "usage" in content.lower() or "example" in content.lower():
            score += 1
            criteria.append({
                'passed': True,
                'description': 'Has usage or example sections',
                'evidence': 'Found usage/example keywords'
            })
        else:
            criteria.append({
                'passed': False,
                'description': 'Has usage or example sections',
                'evidence': 'No usage/example sections - ADD examples section'
            })

        # Criterion 4: Appropriate length
        if 500 < len(content) < 10000:
            score += 1
            criteria.append({
                'passed': True,
                'description': 'Appropriate documentation length',
                'evidence': f'Length: {len(content)} chars'
            })
        else:
            criteria.append({
                'passed': False,
                'description': 'Appropriate documentation length',
                'evidence': f'Length: {len(content)} chars (should be 500-10000)'
            })

        # Criterion 5: Has configuration/options documentation
        if "parameter" in content.lower() or "option" in content.lower() or "configuration" in content.lower():
            score += 1
            criteria.append({
                'passed': True,
                'description': 'Documents parameters/options',
                'evidence': 'Found parameter/option documentation'
            })
        else:
            criteria.append({
                'passed': False,
                'description': 'Documents parameters/options',
                'evidence': 'No parameter/option documentation - ADD configuration section'
            })

        return min(score, 5), criteria

    def _save_epoch_variants(self, epoch: int, rollout_summaries: List[RolloutSummary], best_rollout: RolloutSummary):
        """Save all variants from this epoch to optimization directory."""
        try:
            # Save individual variant files
            for rollout in rollout_summaries:
                variant_file = self.optimization_dir / f"epoch_{epoch}_{rollout.variant_id}.md"
                with open(variant_file, 'w', encoding='utf-8') as f:
                    f.write(rollout.content)

            # Save epoch metadata
            metadata = {
                'epoch': epoch,
                'variants': [
                    {
                        'variant_id': r.variant_id,
                        'score': r.score,
                        'total': r.total,
                        'percentage': round(r.score / r.total * 100, 2) if r.total > 0 else 0,
                        'summary': r.summary
                    }
                    for r in rollout_summaries
                ],
                'best_variant': best_rollout.variant_id,
                'best_score': best_rollout.score,
                'best_percentage': round(best_rollout.score / best_rollout.total * 100, 2) if best_rollout.total > 0 else 0
            }

            metadata_file = self.optimization_dir / f"epoch_{epoch}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            print(f"  ✓ Saved {len(rollout_summaries)} variants to {self.optimization_dir}")

        except Exception as e:
            print(f"  ⚠ Failed to save epoch variants: {e}")

    def _optimize_commands(self):
        """Optimize executable commands in the skill using command_optimizer."""
        try:
            import subprocess
            optimizer_path = Path(__file__).parent / "command_optimizer.py"

            if not optimizer_path.exists():
                print("⚠ Command optimizer not found, skipping command optimization")
                return

            print("✓ Running command optimizer...")
            result = subprocess.run(
                [sys.executable, str(optimizer_path), str(self.output_dir), str(self.output_dir.parent)],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                print("✓ Command optimization complete")
                # Reload the skill content after command optimization
                skill_md = self.output_dir / "SKILL.md"
                if skill_md.exists():
                    with open(skill_md, 'r', encoding='utf-8') as f:
                        self.original_skill_content = f.read()
                        self.current_best_content = self.original_skill_content
            else:
                print(f"⚠ Command optimization had no improvements")
                if result.stdout:
                    print(f"  Output: {result.stdout[:200]}")

        except Exception as e:
            print(f"⚠ Command optimization failed: {e}")


def load_training_tasks(tasks_dir: Path):
    """Load training tasks from directory."""
    tasks = []
    train_dir = tasks_dir / "train"

    if not train_dir.exists():
        print(f"ERROR: Training tasks directory not found: {train_dir}")
        return tasks

    for task_dir in sorted(train_dir.glob("task_*")):
        task_md = task_dir / "task.md"
        speccheck_md = task_dir / "speccheck.md"

        if task_md.exists() and speccheck_md.exists():
            with open(task_md, 'r', encoding='utf-8') as f:
                task_content = f.read()
            with open(speccheck_md, 'r', encoding='utf-8') as f:
                speccheck_content = f.read()

            tasks.append({
                "task_id": task_dir.name,
                "task_dir": task_dir,
                "task_content": task_content,
                "speccheck_content": speccheck_content
            })

    return tasks


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python training_free_grpo_optimizer.py <target-skill-path> <work-dir>")
        sys.exit(1)

    target_skill_path = Path(sys.argv[1]).resolve()
    work_dir = Path(sys.argv[2]).resolve()

    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    config = {}
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

    tf_grpo_config = config.get('training_free_grpo', {})

    optimizer = TrainingFreeGRPOOptimizer(
        target_skill_path=str(target_skill_path),
        training_tasks_dir=str(work_dir / "tasks"),
        output_dir=str(target_skill_path),
        group_size=tf_grpo_config.get('group_size', 5),
        num_epochs=tf_grpo_config.get('num_epochs', 3),
        config=config
    )

    if not optimizer.load_original_skill():
        sys.exit(1)

    training_tasks = load_training_tasks(work_dir / "tasks")

    if not training_tasks:
        print("ERROR: No training tasks found")
        sys.exit(1)

    print(f"✓ Loaded {len(training_tasks)} training tasks")

    try:
        results = optimizer.optimize(training_tasks)

        print("\n" + "="*60)
        print("Training-Free GRPO Complete")
        print("="*60)
        print(f"Baseline: {results['baseline_score']}")
        print(f"Final: {results['final_score']}")
        print(f"Improvement: +{results['improvement']}")

        sys.exit(0)

    except Exception as e:
        print(f"\nERROR: Optimization failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
