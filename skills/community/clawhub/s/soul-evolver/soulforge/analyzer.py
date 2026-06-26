"""
SoulForge Pattern Analyzer
Uses MiniMax API to analyze memory entries and discover patterns.
"""

import json
import logging
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from soulforge.memory_reader import MemoryEntry

logger = logging.getLogger(__name__)


@dataclass
class DiscoveredPattern:
    """A pattern discovered from memory analysis."""
    pattern_id: str
    target_file: str          # Which file to update
    update_type: str          # "SOUL" | "USER" | "IDENTITY" | "MEMORY" | "AGENTS" | "TOOLS"
    category: str             # "behavior" | "preference" | "decision" | "error" | etc.
    summary: str              # One-line summary
    content: str              # The content to add
    confidence: float         # 0.0 - 1.0
    evidence_count: int        # How many times this pattern was observed
    source_entries: List[str] # Source file references
    suggested_section: Optional[str] = None  # Where in the target file

    def to_markdown_block(self) -> str:
        """Format as a SoulForge update block for insertion."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        sources = ", ".join(self.source_entries[:3])  # Limit to 3 for readability
        if len(self.source_entries) > 3:
            sources += f" (+{len(self.source_entries) - 3} more)"

        return f"""
<!-- SoulForge Update | {timestamp} -->
## {self.summary}

**Source**: {sources}
**Pattern Type**: {self.category}
**Confidence**: {"High" if self.confidence > 0.7 else "Medium" if self.confidence > 0.4 else "Low"} (observed {self.evidence_count} times)

**Content**:
{self.content}

<!-- /SoulForge Update -->"""


class PatternAnalyzer:
    """
    Analyzes memory entries to discover patterns and generate updates.

    Uses MiniMax API to:
    1. Analyze memory entries for recurring patterns
    2. Map patterns to appropriate target files
    3. Generate update content in the correct format
    """

    SYSTEM_PROMPT = """You are SoulForge, an AI agent memory evolution analyzer.
Your task is to analyze memory entries and identify patterns that should be promoted to identity files.

You examine:
- Daily conversation logs (what the user said, how they reacted)
- Learning records (corrections, insights, knowledge gaps)
- Error records (what went wrong)
- Feature requests (what the user wanted)

For each pattern you find, you determine:
1. WHICH file to update (SOUL.md, USER.md, IDENTITY.md, MEMORY.md, AGENTS.md, TOOLS.md)
2. WHAT content to add
3. WHERE in the file it should go (which section)
4. HOW confident you are (based on evidence count)

Update target guidelines:
- SOUL.md: Behavioral patterns, communication style, principles, boundaries
- USER.md: User preferences, projects, habits, working style
- IDENTITY.md: Role changes, team structure, responsibilities
- MEMORY.md: Important decisions, milestones, lessons learned
- AGENTS.md: Team workflow patterns, delegation rules
- TOOLS.md: Tool usage心得, integration patterns, workarounds

Rules:
- Only report patterns with 2+ occurrences (high confidence)
- Report in JSON format (one "proposed_updates" array)
- If no significant patterns found, return empty updates array
- Always write in the language that matches existing content (detect from target file)
- Content should be concise, actionable, and specific
"""

    USER_PROMPT_TEMPLATE = """Analyze these memory entries and find patterns worth promoting to identity files.

## Memory Entries (last 7 days)

{memory_entries_text}

## Existing Content in Target Files

Check what already exists to avoid duplication:

{existing_content}

## Instructions

1. Find patterns that appear 2+ times
2. Check if similar content already exists in target files
3. Generate concise, specific updates (not generic statements)
4. Format output as JSON

## Output Format

Return a JSON object with this structure:
{{
  "proposed_updates": [
    {{
      "target_file": "SOUL.md",
      "update_type": "SOUL",
      "category": "behavior",
      "summary": "Brief one-line description",
      "content": "The content to add (2-4 sentences in Chinese if target is Chinese)",
      "confidence": 0.8,
      "evidence_count": 4,
      "source_entries": ["memory/2026-04-04.md", ".learnings/LEARNINGS.md"],
      "suggested_section": "沟通方式"
    }}
  ],
  "analysis_summary": "Brief explanation of what you found",
  "patterns_declined": [
    {{"reason": "already exists in SOUL.md as...", "entries": [...]}}
  ]
}}

Return ONLY JSON, no other text."""

    def __init__(self, config):
        """
        Initialize the pattern analyzer.

        Args:
            config: SoulForgeConfig instance with API key and settings
        """
        self.config = config
        self._api_key = config.minimax_api_key
        self._base_url = config.minimax_base_url
        self._model = config.get("model", "MiniMax-M2.7")

    def analyze(
        self,
        entries: List[MemoryEntry],
        existing_content: Dict[str, str]
    ) -> List[DiscoveredPattern]:
        """
        Analyze memory entries and return patterns to update.

        Args:
            entries: List of MemoryEntry objects
            existing_content: Dict mapping target file names to their current content

        Returns:
            List of DiscoveredPattern objects to apply
        """
        if not entries:
            logger.info("No entries to analyze")
            return []

        if not self._api_key:
            logger.error("MiniMax API key not configured")
            return []

        # Prepare memory entries text
        memory_text = self._prepare_entries_text(entries)

        # Build user prompt
        user_prompt = self.USER_PROMPT_TEMPLATE.format(
            memory_entries_text=memory_text,
            existing_content=self._format_existing_content(existing_content)
        )

        # Call MiniMax API
        response = self._call_minimax(self.SYSTEM_PROMPT, user_prompt)

        # Parse response
        patterns = self._parse_response(response)

        logger.info(f"Analysis complete: {len(patterns)} patterns discovered")
        return patterns

    def _prepare_entries_text(self, entries: List[MemoryEntry]) -> str:
        """Prepare memory entries as text for the prompt."""
        lines = []
        for i, entry in enumerate(entries[:100]):  # Limit to 100 entries
            lines.append(f"[{i+1}] Source: {entry.source} | Type: {entry.source_type} | Category: {entry.category}")
            lines.append(f"    Content: {entry.content[:300]}")
            if entry.timestamp:
                lines.append(f"    Time: {entry.timestamp}")
            lines.append("")
        return "\n".join(lines)

    def _format_existing_content(self, existing_content: Dict[str, str]) -> str:
        """Format existing content for the prompt."""
        if not existing_content:
            return "No existing content found."

        lines = []
        for filename, content in existing_content.items():
            lines.append(f"\n### {filename}")
            # Show first 1500 chars of each file
            lines.append(content[:1500])
            if len(content) > 1500:
                lines.append("...(truncated)...")
        return "\n".join(lines)

    def _call_minimax(self, system_prompt: str, user_prompt: str) -> str:
        """
        Call MiniMax API for chat completion.

        Args:
            system_prompt: System prompt
            user_prompt: User prompt

        Returns:
            Response text from the API
        """
        import urllib.request
        import urllib.error

        url = f"{self._base_url}/text/chatcompletion_v2"

        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,  # Low temperature for structured output
            "max_tokens": 4096,
        }

        data = json.dumps(payload).encode("utf-8")

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                response_data = json.loads(resp.read().decode("utf-8"))
                return response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            logger.error(f"MiniMax API error: {e.code} - {error_body}")
            return '{"proposed_updates": [], "analysis_summary": "API error"}'
        except Exception as e:
            logger.error(f"MiniMax API call failed: {e}")
            return '{"proposed_updates": [], "analysis_summary": "Request failed"}'

    def _parse_response(self, response_text: str) -> List[DiscoveredPattern]:
        """
        Parse the MiniMax response and extract DiscoveredPattern objects.

        Args:
            response_text: Raw response from MiniMax

        Returns:
            List of DiscoveredPattern objects
        """
        patterns = []

        try:
            # Try to extract JSON from the response
            # The response might have markdown code blocks
            json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find JSON directly
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                if start != -1 and end > start:
                    json_str = response_text[start:end]
                else:
                    json_str = response_text

            data = json.loads(json_str)

            proposed = data.get("proposed_updates", [])
            for item in proposed:
                pattern = DiscoveredPattern(
                    pattern_id=self._generate_pattern_id(),
                    target_file=item.get("target_file", ""),
                    update_type=item.get("update_type", ""),
                    category=item.get("category", "general"),
                    summary=item.get("summary", "Untitled pattern"),
                    content=item.get("content", ""),
                    confidence=item.get("confidence", 0.5),
                    evidence_count=item.get("evidence_count", 1),
                    source_entries=item.get("source_entries", []),
                    suggested_section=item.get("suggested_section"),
                )
                patterns.append(pattern)

            # Log analysis summary
            summary = data.get("analysis_summary", "")
            if summary:
                logger.info(f"Analysis summary: {summary}")

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response was: {response_text[:500]}")
        except Exception as e:
            logger.warning(f"Failed to process response: {e}")

        return patterns

    def _generate_pattern_id(self) -> str:
        """Generate a unique pattern ID."""
        import uuid
        return f"pattern_{uuid.uuid4().hex[:8]}"

    def filter_by_threshold(
        self,
        patterns: List[DiscoveredPattern],
        threshold: Optional[int] = None
    ) -> List[DiscoveredPattern]:
        """
        Filter patterns by evidence count threshold.

        Args:
            patterns: List of DiscoveredPattern objects
            threshold: Minimum evidence count (defaults to config value)

        Returns:
            Filtered list of patterns
        """
        if threshold is None:
            threshold = self.config.trigger_threshold

        return [p for p in patterns if p.evidence_count >= threshold]
