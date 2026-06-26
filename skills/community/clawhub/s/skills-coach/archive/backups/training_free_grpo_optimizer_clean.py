"""
Training-Free GRPO Optimizer for Skills-Coach v2.0.0

Implements Training-Free Group Relative Policy Optimization based on:
"Training-Free Group Relative Policy Optimization" (arXiv:2510.08191)

Key differences from vanilla GRPO:
1. No parameter updates - maintains external experience library E
2. Uses semantic advantage instead of numerical advantage
3. Leverages LLM introspection to extract experiential knowledge
4. Applies different strategies for markdown vs code optimization

Core Algorithm:
- For each iteration:
  1. Generate G rollouts (variants) for each query
  2. Score each rollout with reward model
  3. Use LLM to generate summaries for each rollout
  4. Extract semantic advantage (experiential knowledge) from group comparison
  5. Update experience library E via Add/Delete/Modify/Keep operations
  6. Use E as token prior in next iteration
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import anthropic


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
    summary: str  # LLM-generated summary


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
        # Sort by confidence and recency
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

        # Training-Free GRPO parameters
        self.group_size = group_size
        self.num_epochs = num_epochs

        # Load config
        self.config = config or self._load_config()

        # Initialize Anthropic client for LLM introspection
        self.client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

        # Experience libraries for different domains
        self.markdown_experiences = ExperienceLibrary(domain="markdown")
        self.code_experiences = ExperienceLibrary(domain="code")

        # State tracking
        self.original_skill_content = ""
        self.current_best_content = ""
        self.current_best_score = 0
        self.optimization_history = []

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
        # Check for executable commands or code files
        skill_dir = self.target_skill_path

        # Check for Python/shell scripts
        has_code = any(skill_dir.glob("*.py")) or any(skill_dir.glob("*.sh"))

        # Check SKILL.md for command patterns
        has_commands = "```bash" in skill_content or "```python" in skill_content

        if has_code:
            return "code"
        elif has_commands:
            return "markdown_with_commands"
        else:
            return "markdown_only"

    def generate_rollout_summary(self, variant_content: str, task: Dict, score: int, total: int) -> str:
        """Use LLM to generate summary of a rollout."""
        prompt = f"""Analyze this skill variant and its performance on a task.

**Skill Variant:**
{variant_content[:2000]}...

**Task:** {task['task_id']}
**Score:** {score}/{total} ({score/total*100:.1f}%)

Provide a concise summary (2-3 sentences) of:
1. What approach this variant takes
2. Why it achieved this score
3. Key strengths or weaknesses

Summary:"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"Warning: Failed to generate summary: {e}")
            return f"Variant scored {score}/{total}"

    def extract_semantic_advantage(
        self,
        rollout_summaries: List[RolloutSummary],
        experience_library: ExperienceLibrary,
        domain: str
    ) -> str:
        """Extract semantic advantage from group of rollouts using LLM introspection."""

        # Only extract if there are clear winners and losers
        scores = [r.score / r.total for r in rollout_summaries]
        if len(set(scores)) <= 1:  # All identical
            return ""

        # Build prompt for experience extraction
        summaries_text = "\n\n".join([
            f"**Variant {r.variant_id}** (Score: {r.score}/{r.total}):\n{r.summary}"
            for r in rollout_summaries
        ])

        existing_experiences = experience_library.to_prompt_context(domain)

        prompt = f"""You are analyzing multiple attempts at optimizing a skill to extract experiential knowledge.

{existing_experiences}

**Current Rollout Group:**
{summaries_text}

Based on comparing these variants, extract 1-2 key insights about what makes a skill variant successful or unsuccessful. Focus on:
- Patterns that correlate with higher scores
- Common mistakes in lower-scoring variants
- Actionable guidance for future optimization

Format as concise bullet points. Be specific and actionable.

Key Insights:"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"Warning: Failed to extract semantic advantage: {e}")
            return ""

    def update_experience_library(
        self,
        semantic_advantages: List[str],
        experience_library: ExperienceLibrary,
        domain: str
    ) -> List[str]:
        """Update experience library based on semantic advantages."""

        if not semantic_advantages:
            return ["Keep"]

        # Combine all semantic advantages
        advantages_text = "\n\n".join(semantic_advantages)

        # Get current experiences
        current_exp_text = "\n".join([
            f"{i+1}. {e.content}"
            for i, e in enumerate(experience_library.experiences)
        ])

        prompt = f"""You are managing an experience library for skill optimization.

**Current Experience Library:**
{current_exp_text if current_exp_text else "(Empty)"}

**New Insights from Recent Optimization:**
{advantages_text}

Decide how to update the experience library. You can perform multiple operations:
- **Add**: Add a new experience (provide the text)
- **Delete <index>**: Remove experience at index
- **Modify <index>**: Update experience at index (provide new text)
- **Keep**: No changes needed

Provide your operations as a JSON list. Example:
```json
[
  {{"operation": "Add", "content": "Clear examples improve understanding"}},
  {{"operation": "Delete", "index": 2}},
  {{"operation": "Modify", "index": 1, "content": "Updated guidance..."}}
]
```

Operations:"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse operations
            response_text = response.content[0].text.strip()

            # Extract JSON from response
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                json_text = response_text

            operations = json.loads(json_text)

            # Apply operations
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
        """Generate optimized markdown variant using LLM with experience context."""

        prompt = f"""You are optimizing a skill's documentation (SKILL.md).

{experience_context}

**Current Best Version:**
{self.current_best_content}

**Task:** Generate an improved version that addresses the learned experiences above.

Focus on:
1. Clarity and structure
2. Completeness of instructions
3. Quality of examples
4. Technical accuracy

Provide the complete improved SKILL.md:"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"Warning: Failed to generate markdown variant: {e}")
            return self.current_best_content

    def generate_code_variant(self, experience_context: str, code_file: Path) -> str:
        """Generate optimized code variant using LLM with experience context."""

        with open(code_file, 'r') as f:
            current_code = f.read()

        prompt = f"""You are optimizing executable code for a skill.

{experience_context}

**Current Code ({code_file.name}):**
```python
{current_code}
```

**Task:** Generate an improved version that:
1. Fixes any bugs or issues
2. Improves error handling
3. Optimizes performance
4. Enhances code quality

Provide only the improved code (no explanations):"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            code_text = response.content[0].text.strip()

            # Extract code from markdown if present
            if "```python" in code_text:
                start = code_text.find("```python") + 9
                end = code_text.find("```", start)
                code_text = code_text[start:end].strip()
            elif "```" in code_text:
                start = code_text.find("```") + 3
                end = code_text.find("```", start)
                code_text = code_text[start:end].strip()

            return code_text
        except Exception as e:
            print(f"Warning: Failed to generate code variant: {e}")
            return current_code

    def optimize(self, training_tasks: List[Dict]) -> Dict:
        """
        Main optimization loop using Training-Free GRPO.

        Returns:
            Dictionary with optimization results
        """
        print("\n" + "="*60)
        print("Training-Free GRPO Optimization")
        print("="*60)

        # Detect skill type
        skill_type = self.detect_skill_type(self.original_skill_content)
        print(f"✓ Detected skill type: {skill_type}")

        # Select appropriate experience library
        if skill_type == "code":
            experience_lib = self.code_experiences
            domain = "code"
        else:
            experience_lib = self.markdown_experiences
            domain = "markdown"

        # Compute baseline
        print("\n=== Computing Baseline Score ===")
        baseline_score = self._compute_baseline(training_tasks)
        print(f"✓ Baseline: {baseline_score['total_score']}/{baseline_score['total_possible']} ({baseline_score['percentage']:.1f}%)")

        self.current_best_score = baseline_score['total_score']

        # Multi-epoch learning
        for epoch in range(1, self.num_epochs + 1):
            print(f"\n{'='*60}")
            print(f"EPOCH {epoch}/{self.num_epochs}")
            print("="*60)

            # Generate experience context
            experience_context = experience_lib.to_prompt_context(domain)

            # Generate group of rollouts
            print(f"✓ Generating {self.group_size} rollout variants...")
            rollouts = []

            for g in range(self.group_size):
                variant_id = f"e{epoch}-g{g+1}"

                # Generate variant based on skill type
                if skill_type == "code":
                    # For code skills, optimize both markdown and code
                    variant_content = self.generate_markdown_variant(experience_context, epoch)
                    # TODO: Also optimize code files
                else:
                    variant_content = self.generate_markdown_variant(experience_context, epoch)

                rollouts.append({
                    'variant_id': variant_id,
                    'content': variant_content
                })

            # Score each rollout
            print(f"✓ Scoring {len(rollouts)} variants...")
            rollout_summaries = []

            for rollout in rollouts:
                # Execute on training tasks
                scores = self._evaluate_variant(rollout['content'], training_tasks)
                total_score = sum(s['score'] for s in scores)
                total_possible = sum(s['total'] for s in scores)

                # Generate summary
                summary = self.generate_rollout_summary(
                    rollout['content'],
                    training_tasks[0],  # Use first task for context
                    total_score,
                    total_possible
                )

                rollout_summaries.append(RolloutSummary(
                    variant_id=rollout['variant_id'],
                    content=rollout['content'],
                    score=total_score,
                    total=total_possible,
                    summary=summary
                ))

                print(f"  {rollout['variant_id']}: {total_score}/{total_possible} ({total_score/total_possible*100:.1f}%)")

            # Extract semantic advantage
            print("✓ Extracting semantic advantage...")
            semantic_advantage = self.extract_semantic_advantage(
                rollout_summaries,
                experience_lib,
                domain
            )

            if semantic_advantage:
                print(f"  Insight: {semantic_advantage[:100]}...")

                # Update experience library
                print("✓ Updating experience library...")
                operations = self.update_experience_library(
                    [semantic_advantage],
                    experience_lib,
                    domain
                )
                for op in operations:
                    print(f"  - {op}")

            # Select best variant
            best_rollout = max(rollout_summaries, key=lambda r: r.score)
            if best_rollout.score > self.current_best_score:
                self.current_best_content = best_rollout.content
                self.current_best_score = best_rollout.score
                print(f"✓ New best: {best_rollout.variant_id} with {best_rollout.score}/{best_rollout.total}")
            else:
                print(f"  No improvement (best: {best_rollout.score}/{best_rollout.total})")

            # Save epoch results
            self.optimization_history.append({
                'epoch': epoch,
                'rollouts': [asdict(r) for r in rollout_summaries],
                'best_variant': best_rollout.variant_id,
                'best_score': best_rollout.score,
                'semantic_advantage': semantic_advantage,
                'experience_operations': operations if semantic_advantage else []
            })

        # Save final results
        print("\n" + "="*60)
        print("Optimization Complete")
        print("="*60)

        final_score = self.current_best_score
        improvement = final_score - baseline_score['total_score']
        print(f"Final Score: {final_score}/{baseline_score['total_possible']} ({final_score/baseline_score['total_possible']*100:.1f}%)")
        print(f"Improvement: +{improvement} points")

        # Save optimized skill
        optimized_path = self.output_dir / "SKILL.md"
        with open(optimized_path, 'w') as f:
            f.write(self.current_best_content)
        print(f"✓ Saved optimized skill to {optimized_path}")

        # Save experience library
        exp_path = self.output_dir / f"experience_library_{domain}.json"
        experience_lib.save(exp_path)
        print(f"✓ Saved experience library to {exp_path}")

        # Save optimization log
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
        scores = self._evaluate_variant(self.original_skill_content, training_tasks)
        total_score = sum(s['score'] for s in scores)
        total_possible = sum(s['total'] for s in scores)

        return {
            'total_score': total_score,
            'total_possible': total_possible,
            'percentage': (total_score / total_possible * 100) if total_possible > 0 else 0,
            'task_scores': scores
        }

    def _evaluate_variant(self, variant_content: str, training_tasks: List[Dict]) -> List[Dict]:
        """Evaluate a variant on training tasks (simplified scoring)."""
        # This is a placeholder - in real implementation, this would:
        # 1. Save variant to temp location
        # 2. Execute tasks using the variant
        # 3. Score results using speccheck criteria

        # For now, return mock scores
        scores = []
        for task in training_tasks:
            # Simple heuristic scoring based on content quality
            score = self._heuristic_score(variant_content, task)
            scores.append({
                'task_id': task['task_id'],
                'score': score,
                'total': 5
            })
        return scores

    def _heuristic_score(self, content: str, task: Dict) -> int:
        """Simple heuristic scoring (placeholder for real execution)."""
        # Check for key quality indicators
        score = 0

        # Has clear structure
        if "##" in content:
            score += 1

        # Has examples
        if "```" in content:
            score += 1

        # Has usage section
        if "usage" in content.lower() or "example" in content.lower():
            score += 1

        # Reasonable length
        if 500 < len(content) < 10000:
            score += 1

        # Has parameters/options
        if "parameter" in content.lower() or "option" in content.lower():
            score += 1

        return min(score, 5)

