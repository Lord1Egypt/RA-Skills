"""
Task Generator for Skills-Coach v2.3.1

Generates diverse test tasks by analyzing a target skill's SKILL.md specification.
Creates 16 training tasks (6 standard + 4 advanced + 6 boundary) and 10 test tasks (4 standard + 3 advanced + 3 boundary).
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict

# Import boundary prober for v1.2.0
try:
    from boundary_prober import CapabilityBoundaryProber, integrate_boundary_tasks
    BOUNDARY_PROBING_AVAILABLE = True
except ImportError:
    BOUNDARY_PROBING_AVAILABLE = False
    print("⚠ Boundary probing not available - using legacy mode")


@dataclass
class Task:
    """Represents a single test task."""
    task_id: str
    task_type: str  # "standard", "advanced", or "boundary"
    title: str
    background: str
    objective: str
    input_description: str
    expected_behavior: str
    constraints: List[str]
    workspace_files: Dict[str, str]  # filename -> content


@dataclass
class SpecCheckCriterion:
    """Represents a single evaluation criterion."""
    description: str
    verification_method: str


@dataclass
class SpecCheck:
    """Represents the evaluation criteria for a task."""
    task_id: str
    criteria: List[SpecCheckCriterion]
    total_points: int
    pass_threshold: int
    evaluation_notes: str


class TaskGenerator:
    """Generates test tasks for a target skill."""

    def __init__(self, target_skill_path: str, output_dir: str = ".", config_path: str = None):
        self.target_skill_path = Path(target_skill_path)
        self.output_dir = Path(output_dir)
        self.skill_md_content = ""

        # Load config for v1.2.0 features
        self.config = self._load_config(config_path)
        self.probe_boundaries = self.config.get('task_generation', {}).get('probe_boundaries', False)

    def _load_config(self, config_path: str = None) -> dict:
        """Load configuration file."""
        if config_path is None:
            # Try to find config.yaml in parent directories
            current = Path(__file__).parent
            for _ in range(3):
                config_file = current / "config.yaml"
                if config_file.exists():
                    config_path = config_file
                    break
                current = current.parent

        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)

        # Default config
        return {
            'task_generation': {
                'probe_boundaries': False,
                'num_training_tasks': 16,
                'num_test_tasks': 10
            }
        }

    def load_skill_specification(self) -> bool:
        """Load and parse the target skill's SKILL.md."""
        skill_md_path = self.target_skill_path / "SKILL.md"

        if not skill_md_path.exists():
            print(f"ERROR: SKILL.md not found at {skill_md_path}")
            return False

        with open(skill_md_path, 'r', encoding='utf-8') as f:
            self.skill_md_content = f.read()

        print(f"✓ Loaded SKILL.md from {skill_md_path}")
        return True

    def generate_tasks(self) -> Tuple[List[Task], List[SpecCheck]]:
        """
        Generate training tasks by analyzing the skill specification.

        Returns:
            Tuple of (tasks, speccheck_definitions)
        """
        tasks = []
        specchecks = []

        # Standard Task 1: Basic feed fetching with single source
        tasks.append(Task(
            task_id="task_001",
            task_type="standard",
            title="Basic Single Feed Fetch",
            background="Tests the core functionality of fetching and parsing a single RSS feed.",
            objective="Fetch articles from a single RSS feed and generate a basic digest.",
            input_description="Feed configuration with one tech feed (Hacker News RSS).",
            expected_behavior="Successfully fetch articles, parse them, and generate a digest with proper formatting.",
            constraints=[
                "Must fetch at least 1 article",
                "Must generate valid Markdown output",
                "Must include article title, URL, and source name"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_001",
            criteria=[
                SpecCheckCriterion(
                    description="Output file exists at expected location",
                    verification_method="Check if digest-*.md file exists in output directory"
                ),
                SpecCheckCriterion(
                    description="Output contains valid Markdown header with date",
                    verification_method="Check for '# Daily Digest — YYYY-MM-DD' pattern"
                ),
                SpecCheckCriterion(
                    description="Output includes at least one article with title and URL",
                    verification_method="Check for '**[Title](url)**' pattern"
                ),
                SpecCheckCriterion(
                    description="Output includes source attribution",
                    verification_method="Check for '*(Source Name)*' pattern"
                ),
                SpecCheckCriterion(
                    description="No Python errors in execution log",
                    verification_method="Check run_log.md for ImportError or Exception"
                )
            ],
            total_points=5,
            pass_threshold=4,
            evaluation_notes="This tests basic functionality. All criteria should pass for a working implementation."
        ))

        # Standard Task 2: Multiple feeds across categories
        tasks.append(Task(
            task_id="task_002",
            task_type="standard",
            title="Multiple Feeds with Categories",
            background="Tests handling multiple feeds organized into different categories.",
            objective="Fetch from multiple feeds and organize articles by category in the digest.",
            input_description="Feed configuration with tech, business, and world categories.",
            expected_behavior="Generate digest with articles grouped by category, maintaining category structure.",
            constraints=[
                "Must preserve category organization",
                "Must handle multiple feeds per category",
                "Must include articles from all categories"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
  business:
    - url: "https://feeds.bloomberg.com/markets/news.rss"
      name: "Bloomberg"
  world:
    - url: "https://feeds.bbc.co.uk/news/rss.xml"
      name: "BBC News"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_002",
            criteria=[
                SpecCheckCriterion(
                    description="Output contains Tech category section",
                    verification_method="Check for '## Tech' header"
                ),
                SpecCheckCriterion(
                    description="Output contains Business category section",
                    verification_method="Check for '## Business' header"
                ),
                SpecCheckCriterion(
                    description="Output contains World category section",
                    verification_method="Check for '## World' header"
                ),
                SpecCheckCriterion(
                    description="Articles are grouped under correct categories",
                    verification_method="Verify articles appear under their category headers"
                ),
                SpecCheckCriterion(
                    description="Summary line shows correct feed count",
                    verification_method="Check for '> N articles from 3 sources' pattern"
                )
            ],
            total_points=5,
            pass_threshold=4,
            evaluation_notes="Tests category organization and multi-feed handling."
        ))

        # Standard Task 3: Time filtering (24 hours)
        tasks.append(Task(
            task_id="task_003",
            task_type="standard",
            title="Time-based Article Filtering",
            background="Tests the ability to filter articles by publication time.",
            objective="Fetch only articles published within the last 24 hours.",
            input_description="Feed configuration with --hours 24 parameter.",
            expected_behavior="Only include articles from the last 24 hours, exclude older articles.",
            constraints=[
                "Must respect time window parameter",
                "Must not include articles older than 24 hours",
                "Must handle timezone correctly"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_003",
            criteria=[
                SpecCheckCriterion(
                    description="Fetch command includes --hours 24 parameter",
                    verification_method="Check run_log.md for correct command invocation"
                ),
                SpecCheckCriterion(
                    description="Output includes timestamp information",
                    verification_method="Check for timestamp in footer or metadata"
                ),
                SpecCheckCriterion(
                    description="No errors related to time parsing",
                    verification_method="Check run_log.md for datetime errors"
                ),
                SpecCheckCriterion(
                    description="Articles have valid publication dates",
                    verification_method="Verify articles are within expected timeframe"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests time filtering functionality."
        ))

        # Standard Task 4: Output file naming and location
        tasks.append(Task(
            task_id="task_004",
            task_type="standard",
            title="Correct Output File Handling",
            background="Tests proper file naming and directory creation.",
            objective="Save digest with correct filename format and create output directory if needed.",
            input_description="Standard feed configuration.",
            expected_behavior="Create output directory and save file as digest-YYYY-MM-DD.md.",
            constraints=[
                "Must create directory if it doesn't exist",
                "Must use correct date format in filename",
                "Must save to ~/openclaw-output/digests/"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_004",
            criteria=[
                SpecCheckCriterion(
                    description="Output directory exists",
                    verification_method="Check if ~/openclaw-output/digests/ directory was created"
                ),
                SpecCheckCriterion(
                    description="Filename follows digest-YYYY-MM-DD.md pattern",
                    verification_method="Verify filename matches expected format"
                ),
                SpecCheckCriterion(
                    description="File is saved in correct location",
                    verification_method="Check file exists at ~/openclaw-output/digests/"
                ),
                SpecCheckCriterion(
                    description="File contains valid UTF-8 content",
                    verification_method="Verify file can be read as UTF-8"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests file handling and directory creation."
        ))

        # Standard Task 5: Error reporting for failed feeds
        tasks.append(Task(
            task_id="task_005",
            task_type="standard",
            title="Failed Feed Error Reporting",
            background="Tests error handling when a feed fails to fetch.",
            objective="Gracefully handle feed failures and report them to the user.",
            input_description="Feed configuration with one valid and one invalid feed URL.",
            expected_behavior="Skip failed feed, continue with successful ones, report errors clearly.",
            constraints=[
                "Must not crash on feed failure",
                "Must report which feeds failed",
                "Must continue processing other feeds"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
    - url: "https://invalid-feed-url-that-does-not-exist.com/rss"
      name: "Invalid Feed"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_005",
            criteria=[
                SpecCheckCriterion(
                    description="Execution completes without crashing",
                    verification_method="Check run_log.md shows successful completion"
                ),
                SpecCheckCriterion(
                    description="Error is logged for failed feed",
                    verification_method="Check run_log.md contains error message for Invalid Feed"
                ),
                SpecCheckCriterion(
                    description="Successful feed is processed",
                    verification_method="Check output contains articles from Hacker News"
                ),
                SpecCheckCriterion(
                    description="User is informed of partial results",
                    verification_method="Check output footer shows feed success/failure count"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests error handling and graceful degradation."
        ))

        # Standard Task 6: Summary generation
        tasks.append(Task(
            task_id="task_006",
            task_type="standard",
            title="Article Summary Generation",
            background="Tests the ability to generate concise summaries for articles.",
            objective="Generate one-sentence summaries for each article (max 30 words).",
            input_description="Standard feed configuration.",
            expected_behavior="Each article has a summary following the title.",
            constraints=[
                "Summaries must be concise (≤30 words)",
                "Must use AI service or fallback to first 30 words",
                "Must preserve factual accuracy"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_006",
            criteria=[
                SpecCheckCriterion(
                    description="Each article has a summary",
                    verification_method="Check that articles have text after title"
                ),
                SpecCheckCriterion(
                    description="Summaries are concise",
                    verification_method="Verify summaries are approximately 30 words or less"
                ),
                SpecCheckCriterion(
                    description="Summary follows proper format",
                    verification_method="Check for '— Summary text. *(Source)*' pattern"
                ),
                SpecCheckCriterion(
                    description="No placeholder or empty summaries",
                    verification_method="Verify no '[Summary]' or empty summary fields"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests summary generation functionality."
        ))

        # Standard Task 7: Relevance scoring
        tasks.append(Task(
            task_id="task_007",
            task_type="standard",
            title="Article Relevance Scoring",
            background="Tests the relevance scoring system for articles.",
            objective="Calculate and display relevance scores for articles.",
            input_description="Feed configuration with keyword matching enabled.",
            expected_behavior="Articles have relevance scores displayed, sorted by score.",
            constraints=[
                "Scores must be on 1-5 scale",
                "Must consider keyword match, source weight, and freshness",
                "Must display scores in output"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
      keywords:
        - "AI"
        - "Python"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_007",
            criteria=[
                SpecCheckCriterion(
                    description="Articles include relevance scores",
                    verification_method="Check for '[Score: X.X]' pattern in output"
                ),
                SpecCheckCriterion(
                    description="Scores are in valid range (1.0-5.0)",
                    verification_method="Verify all scores are between 1.0 and 5.0"
                ),
                SpecCheckCriterion(
                    description="Articles are sorted by relevance",
                    verification_method="Verify scores are in descending order within categories"
                ),
                SpecCheckCriterion(
                    description="Scoring algorithm is documented in log",
                    verification_method="Check run_log.md mentions scoring formula"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests relevance scoring and sorting."
        ))

        # Standard Task 8: Configuration via environment variables
        tasks.append(Task(
            task_id="task_008",
            task_type="standard",
            title="Environment Variable Configuration",
            background="Tests configuration through environment variables.",
            objective="Apply configuration from environment variables (RSS_MAX_ARTICLES, RSS_TIMEOUT).",
            input_description="Standard feed configuration with environment variables set.",
            expected_behavior="Respect environment variable settings for max articles and timeout.",
            constraints=[
                "Must read RSS_MAX_ARTICLES environment variable",
                "Must read RSS_TIMEOUT environment variable",
                "Must apply these settings correctly"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_008",
            criteria=[
                SpecCheckCriterion(
                    description="Environment variables are read",
                    verification_method="Check run_log.md shows config values from env vars"
                ),
                SpecCheckCriterion(
                    description="RSS_MAX_ARTICLES is respected",
                    verification_method="Verify output has ≤ max articles specified"
                ),
                SpecCheckCriterion(
                    description="RSS_TIMEOUT is applied",
                    verification_method="Check log shows timeout value being used"
                ),
                SpecCheckCriterion(
                    description="Configuration is logged at startup",
                    verification_method="Check run_log.md contains config summary"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests environment variable configuration."
        ))

        # Advanced Task 9: Empty results handling
        tasks.append(Task(
            task_id="task_009",
            task_type="advanced",
            title="Zero Articles Scenario",
            background="Tests handling when no articles are found in the time window.",
            objective="Gracefully handle scenario where no articles match the time filter.",
            input_description="Feed configuration with very short time window (--hours 0.01).",
            expected_behavior="Report zero articles found, suggest expanding timeframe, don't crash.",
            constraints=[
                "Must not crash or error out",
                "Must inform user of zero results",
                "Must suggest alternative timeframes"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_009",
            criteria=[
                SpecCheckCriterion(
                    description="Execution completes without error",
                    verification_method="Check run_log.md shows successful completion"
                ),
                SpecCheckCriterion(
                    description="Zero articles message is displayed",
                    verification_method="Check output or log contains 'No articles found' or '0 articles'"
                ),
                SpecCheckCriterion(
                    description="Suggestion to expand timeframe is provided",
                    verification_method="Check for suggestion like '--hours 72' or '--hours 168'"
                ),
                SpecCheckCriterion(
                    description="No empty digest file is created",
                    verification_method="Verify either no file created or file contains explanation"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests edge case of zero results."
        ))

        # Advanced Task 10: All feeds fail scenario
        tasks.append(Task(
            task_id="task_010",
            task_type="advanced",
            title="Complete Feed Failure",
            background="Tests handling when all configured feeds fail to fetch.",
            objective="Handle scenario where every feed fails, provide useful error report.",
            input_description="Feed configuration with only invalid URLs.",
            expected_behavior="Report all failures, suggest troubleshooting steps, exit with error code.",
            constraints=[
                "Must report each failed feed",
                "Must suggest network troubleshooting",
                "Must exit with non-zero code"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://invalid-url-1.com/rss"
      name: "Invalid Feed 1"
    - url: "https://invalid-url-2.com/rss"
      name: "Invalid Feed 2"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_010",
            criteria=[
                SpecCheckCriterion(
                    description="All feed failures are reported",
                    verification_method="Check run_log.md lists both failed feeds"
                ),
                SpecCheckCriterion(
                    description="Failure reasons are provided",
                    verification_method="Check log includes error details (timeout, 404, etc.)"
                ),
                SpecCheckCriterion(
                    description="Troubleshooting suggestions are provided",
                    verification_method="Check for suggestions like 'Check network connectivity'"
                ),
                SpecCheckCriterion(
                    description="Process exits with error status",
                    verification_method="Check run_log.md shows exit code 1 or error status"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests complete failure scenario."
        ))

        # Advanced Task 11: Multilingual content handling
        tasks.append(Task(
            task_id="task_011",
            task_type="advanced",
            title="Multilingual Digest Generation",
            background="Tests handling of non-English content and translation.",
            objective="Generate digest with Chinese language output and proper timezone handling.",
            input_description="Feed configuration with language='zh' and timezone='Asia/Shanghai'.",
            expected_behavior="Output in Chinese with correct timezone conversion.",
            constraints=[
                "Must detect or respect language setting",
                "Must handle timezone conversion",
                "Must preserve UTF-8 encoding"
            ],
            workspace_files={
                "feed-sources.md": """config:
  language: "zh"
  timezone: "Asia/Shanghai"
  enableTranslation: true

feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_011",
            criteria=[
                SpecCheckCriterion(
                    description="Language configuration is read",
                    verification_method="Check run_log.md shows language=zh"
                ),
                SpecCheckCriterion(
                    description="Timezone configuration is applied",
                    verification_method="Check log shows timezone=Asia/Shanghai"
                ),
                SpecCheckCriterion(
                    description="Output file is UTF-8 encoded",
                    verification_method="Verify file can be read as UTF-8 with Chinese characters"
                ),
                SpecCheckCriterion(
                    description="Timestamps reflect correct timezone",
                    verification_method="Check footer timestamp shows CST or +08:00"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests internationalization features."
        ))

        # Advanced Task 12: High-volume feed processing
        tasks.append(Task(
            task_id="task_012",
            task_type="advanced",
            title="High Article Volume Handling",
            background="Tests handling of feeds with many articles and max article limiting.",
            objective="Process high-volume feeds and respect RSS_MAX_ARTICLES limit.",
            input_description="Multiple feeds with RSS_MAX_ARTICLES=20 set.",
            expected_behavior="Limit output to 20 articles, prioritize by relevance score.",
            constraints=[
                "Must not exceed max articles limit",
                "Must prioritize highest-scoring articles",
                "Must handle large feed volumes efficiently"
            ],
            workspace_files={
                "feed-sources.md": """config:
  maxArticles: 20
  sortBy: "relevance"

feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
    - url: "https://www.theverge.com/rss/index.xml"
      name: "The Verge"
  business:
    - url: "https://feeds.bloomberg.com/markets/news.rss"
      name: "Bloomberg"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_012",
            criteria=[
                SpecCheckCriterion(
                    description="Output respects max articles limit",
                    verification_method="Count articles in output, verify ≤20"
                ),
                SpecCheckCriterion(
                    description="Articles are sorted by relevance",
                    verification_method="Verify scores are in descending order"
                ),
                SpecCheckCriterion(
                    description="Summary shows filtered count",
                    verification_method="Check for indication of how many articles were filtered"
                ),
                SpecCheckCriterion(
                    description="Processing completes in reasonable time",
                    verification_method="Check run_log.md shows completion time <2 minutes"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests high-volume processing and filtering."
        ))

        return tasks, specchecks

    def generate_test_tasks(self) -> Tuple[List[Task], List[SpecCheck]]:
        """
        Generate test tasks (distinct from training tasks).

        Returns:
            Tuple of (tasks, speccheck_definitions) for 8 test tasks
        """
        tasks = []
        specchecks = []

        # Test Task 1: Basic functionality with different feed
        tasks.append(Task(
            task_id="task_001",
            task_type="standard",
            title="Alternative Tech Feed Processing",
            background="Tests basic functionality with a different tech news source.",
            objective="Fetch and process articles from The Verge RSS feed.",
            input_description="Feed configuration with The Verge as the source.",
            expected_behavior="Generate properly formatted digest with articles from The Verge.",
            constraints=[
                "Must successfully fetch from The Verge",
                "Must generate valid Markdown",
                "Must include proper attribution"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://www.theverge.com/rss/index.xml"
      name: "The Verge"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_001",
            criteria=[
                SpecCheckCriterion(
                    description="Digest file is created",
                    verification_method="Check for digest-*.md in output directory"
                ),
                SpecCheckCriterion(
                    description="Output has proper Markdown structure",
                    verification_method="Verify header, category sections, and footer exist"
                ),
                SpecCheckCriterion(
                    description="Articles are from The Verge",
                    verification_method="Check source attribution shows 'The Verge'"
                ),
                SpecCheckCriterion(
                    description="No execution errors",
                    verification_method="Check run_log.md for successful completion"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests generalization to different feed sources."
        ))

        # Test Task 2: Different category mix
        tasks.append(Task(
            task_id="task_002",
            task_type="standard",
            title="Science and World News Categories",
            background="Tests category handling with different category names.",
            objective="Process feeds in science and world categories.",
            input_description="Feed configuration with science and world categories.",
            expected_behavior="Generate digest with science and world sections.",
            constraints=[
                "Must create sections for both categories",
                "Must handle category names correctly",
                "Must group articles appropriately"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  science:
    - url: "https://www.nature.com/nature.rss"
      name: "Nature"
  world:
    - url: "https://feeds.bbci.co.uk/news/world/rss.xml"
      name: "BBC World"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_002",
            criteria=[
                SpecCheckCriterion(
                    description="Science category section exists",
                    verification_method="Check for '## Science' or '## science' header"
                ),
                SpecCheckCriterion(
                    description="World category section exists",
                    verification_method="Check for '## World' or '## world' header"
                ),
                SpecCheckCriterion(
                    description="Articles are under correct categories",
                    verification_method="Verify Nature articles under science, BBC under world"
                ),
                SpecCheckCriterion(
                    description="Feed count is accurate",
                    verification_method="Check summary shows 2 sources"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests handling of different category names."
        ))

        # Test Task 3: Different time window (48 hours)
        tasks.append(Task(
            task_id="task_003",
            task_type="standard",
            title="Extended Time Window (48 hours)",
            background="Tests time filtering with a different time window.",
            objective="Fetch articles from the last 48 hours instead of 24.",
            input_description="Feed configuration with --hours 48 parameter.",
            expected_behavior="Include articles from last 48 hours, more articles than 24h window.",
            constraints=[
                "Must use 48-hour time window",
                "Must handle longer timeframe correctly",
                "Must not include articles older than 48 hours"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_003",
            criteria=[
                SpecCheckCriterion(
                    description="Command uses --hours 48",
                    verification_method="Check run_log.md for correct parameter"
                ),
                SpecCheckCriterion(
                    description="Articles span appropriate timeframe",
                    verification_method="Verify articles are within 48-hour window"
                ),
                SpecCheckCriterion(
                    description="Digest is generated successfully",
                    verification_method="Check output file exists and is valid"
                ),
                SpecCheckCriterion(
                    description="No time-related errors",
                    verification_method="Check log for datetime parsing errors"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests different time window parameter."
        ))

        # Test Task 4: Custom output directory
        tasks.append(Task(
            task_id="task_004",
            task_type="standard",
            title="Custom Output Directory",
            background="Tests using a custom output directory via environment variable.",
            objective="Save digest to a custom directory specified by RSS_OUTPUT_DIR.",
            input_description="Standard feed with RSS_OUTPUT_DIR set to custom path.",
            expected_behavior="Create custom directory and save digest there.",
            constraints=[
                "Must respect RSS_OUTPUT_DIR environment variable",
                "Must create custom directory if it doesn't exist",
                "Must save file to custom location"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_004",
            criteria=[
                SpecCheckCriterion(
                    description="Custom directory is created",
                    verification_method="Check if custom output directory exists"
                ),
                SpecCheckCriterion(
                    description="File is saved to custom location",
                    verification_method="Verify digest file exists in custom directory"
                ),
                SpecCheckCriterion(
                    description="Environment variable is logged",
                    verification_method="Check run_log.md shows RSS_OUTPUT_DIR value"
                ),
                SpecCheckCriterion(
                    description="File has correct name format",
                    verification_method="Verify filename is digest-YYYY-MM-DD.md"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests custom output directory configuration."
        ))

        # Test Task 5: Mixed success/failure with different feeds
        tasks.append(Task(
            task_id="task_005",
            task_type="advanced",
            title="Partial Feed Failure with Recovery",
            background="Tests error handling with a different mix of valid/invalid feeds.",
            objective="Handle mix of successful and failed feeds, generate partial digest.",
            input_description="Three feeds: two valid, one invalid.",
            expected_behavior="Process valid feeds, skip invalid one, report partial results.",
            constraints=[
                "Must process both valid feeds",
                "Must skip invalid feed gracefully",
                "Must report which feeds succeeded/failed"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://www.theverge.com/rss/index.xml"
      name: "The Verge"
  business:
    - url: "https://invalid-business-feed.com/rss"
      name: "Invalid Business"
  world:
    - url: "https://feeds.bbci.co.uk/news/rss.xml"
      name: "BBC News"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_005",
            criteria=[
                SpecCheckCriterion(
                    description="Valid feeds are processed",
                    verification_method="Check output contains articles from The Verge and BBC"
                ),
                SpecCheckCriterion(
                    description="Invalid feed error is logged",
                    verification_method="Check run_log.md for error about Invalid Business feed"
                ),
                SpecCheckCriterion(
                    description="Partial results indicator is shown",
                    verification_method="Check output shows 2/3 feeds or similar indicator"
                ),
                SpecCheckCriterion(
                    description="Execution completes successfully",
                    verification_method="Verify process doesn't crash"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests partial failure handling with different feeds."
        ))

        # Test Task 6: Feed with custom weight and keywords
        tasks.append(Task(
            task_id="task_006",
            task_type="advanced",
            title="Custom Feed Weights and Keywords",
            background="Tests relevance scoring with custom weights and different keywords.",
            objective="Apply custom feed weights and keyword matching for scoring.",
            input_description="Feed configuration with custom weights and keywords.",
            expected_behavior="Calculate scores using custom weights, prioritize keyword matches.",
            constraints=[
                "Must apply custom weight values",
                "Must match against specified keywords",
                "Must display scores in output"
            ],
            workspace_files={
                "feed-sources.md": """feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
      weight: 1.5
      keywords:
        - "Rust"
        - "WebAssembly"
        - "Cloud"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_006",
            criteria=[
                SpecCheckCriterion(
                    description="Custom weight is applied",
                    verification_method="Check log shows weight=1.5 for Hacker News"
                ),
                SpecCheckCriterion(
                    description="Keywords are used for scoring",
                    verification_method="Verify log mentions keyword matching"
                ),
                SpecCheckCriterion(
                    description="Scores reflect custom configuration",
                    verification_method="Check articles have relevance scores displayed"
                ),
                SpecCheckCriterion(
                    description="Articles are sorted by score",
                    verification_method="Verify scores are in descending order"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests custom scoring configuration."
        ))

        # Test Task 7: Minimum relevance threshold filtering
        tasks.append(Task(
            task_id="task_007",
            task_type="advanced",
            title="Relevance Threshold Filtering",
            background="Tests filtering articles below a minimum relevance score.",
            objective="Apply minRelevanceScore filter to exclude low-scoring articles.",
            input_description="Feed configuration with minRelevanceScore=3.0.",
            expected_behavior="Only include articles with score ≥3.0, show filtered count.",
            constraints=[
                "Must filter articles below threshold",
                "Must report how many were filtered",
                "Must only show high-relevance articles"
            ],
            workspace_files={
                "feed-sources.md": """config:
  minRelevanceScore: 3.0
  sortBy: "relevance"

feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
      keywords:
        - "AI"
        - "Machine Learning"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_007",
            criteria=[
                SpecCheckCriterion(
                    description="Minimum relevance threshold is applied",
                    verification_method="Check all displayed articles have score ≥3.0"
                ),
                SpecCheckCriterion(
                    description="Filtered count is reported",
                    verification_method="Check output shows how many articles were filtered"
                ),
                SpecCheckCriterion(
                    description="Configuration is logged",
                    verification_method="Check run_log.md shows minRelevance=3.0"
                ),
                SpecCheckCriterion(
                    description="Output indicates filtering was applied",
                    verification_method="Check for 'filtered' or 'threshold' mention in output"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests relevance filtering feature."
        ))

        # Test Task 8: Maximum articles with multiple categories
        tasks.append(Task(
            task_id="task_008",
            task_type="advanced",
            title="Article Limit Across Multiple Categories",
            background="Tests max article limiting with multiple categories and feeds.",
            objective="Limit total articles to 15 across all categories, prioritize by relevance.",
            input_description="Multiple categories with maxArticles=15.",
            expected_behavior="Output exactly 15 articles, highest-scoring across all categories.",
            constraints=[
                "Must not exceed 15 articles total",
                "Must select highest-scoring articles across categories",
                "Must maintain category organization"
            ],
            workspace_files={
                "feed-sources.md": """config:
  maxArticles: 15
  sortBy: "relevance"

feeds:
  tech:
    - url: "https://news.ycombinator.com/rss"
      name: "Hacker News"
  business:
    - url: "https://feeds.bloomberg.com/markets/news.rss"
      name: "Bloomberg"
  world:
    - url: "https://feeds.bbc.co.uk/news/rss.xml"
      name: "BBC News"
"""
            }
        ))
        specchecks.append(SpecCheck(
            task_id="task_008",
            criteria=[
                SpecCheckCriterion(
                    description="Total articles does not exceed 15",
                    verification_method="Count all articles in output, verify ≤15"
                ),
                SpecCheckCriterion(
                    description="Articles are highest-scoring",
                    verification_method="Verify scores are high and in descending order"
                ),
                SpecCheckCriterion(
                    description="Categories are preserved",
                    verification_method="Check articles are still grouped by category"
                ),
                SpecCheckCriterion(
                    description="Limit is documented in output",
                    verification_method="Check footer or summary mentions article limit"
                )
            ],
            total_points=4,
            pass_threshold=3,
            evaluation_notes="Tests article limiting across multiple categories."
        ))

        return tasks, specchecks

    def write_task_to_disk(self, task: Task, speccheck: SpecCheck, task_dir: Path):
        """Write a task and its speccheck to disk."""
        task_dir.mkdir(parents=True, exist_ok=True)

        # Write task.md
        task_md_content = f"""# Task: {task.title}

## Background
{task.background}

## Objective
{task.objective}

## Input
{task.input_description}

## Expected Behavior
{task.expected_behavior}

## Constraints
"""
        for constraint in task.constraints:
            task_md_content += f"- {constraint}\n"

        with open(task_dir / "task.md", 'w', encoding='utf-8') as f:
            f.write(task_md_content)

        # Write speccheck.md
        speccheck_md_content = f"""# SpecCheck: {task.title}

## Pass Criteria

Each criterion must be independently verifiable.

"""
        for i, criterion in enumerate(speccheck.criteria, 1):
            speccheck_md_content += f"- [ ] **Criterion {i}**: {criterion.description}\n"

        speccheck_md_content += f"""
## Scoring

- **Total Points**: {speccheck.total_points}
- **Pass Threshold**: {speccheck.pass_threshold}

## Evaluation Notes

{speccheck.evaluation_notes}

## Verification Methods

"""
        for i, criterion in enumerate(speccheck.criteria, 1):
            speccheck_md_content += f"**Criterion {i}**: {criterion.verification_method}\n\n"

        with open(task_dir / "speccheck.md", 'w', encoding='utf-8') as f:
            f.write(speccheck_md_content)

        # Create workspace directory and write files
        workspace_dir = task_dir / "workspace"
        workspace_dir.mkdir(exist_ok=True)

        # Check if files need preparation
        if '__needs_preparation__' in task.workspace_files:
            prep_info = task.workspace_files['__needs_preparation__']
            try:
                from test_file_manager import TestFileManager
                file_manager = TestFileManager(workspace_dir)
                prepared_files = file_manager.prepare_files_for_command(
                    prep_info['command'],
                    prep_info['script_path']
                )
                # Copy prepared files to workspace
                for filename, filepath in prepared_files.items():
                    if filepath.startswith('<') and filepath.endswith('>'):
                        # Placeholder, skip
                        continue
                    # If it's a path, copy the file
                    if Path(filepath).exists():
                        import shutil
                        dest = workspace_dir / filename
                        shutil.copy2(filepath, dest)
            except Exception as e:
                print(f"  ⚠ Warning: Could not prepare files for {task.task_id}: {e}")
        else:
            # Write regular workspace files
            for filename, content in task.workspace_files.items():
                with open(workspace_dir / filename, 'w', encoding='utf-8') as f:
                    f.write(content)

        print(f"✓ Written {task.task_id} ({task.task_type})")

    def save_tasks(self, tasks: List[Task], specchecks: List[SpecCheck], task_set: str):
        """Save a set of tasks (train or test) to disk."""
        base_dir = self.output_dir / "tasks" / task_set

        for task, speccheck in zip(tasks, specchecks):
            task_dir = base_dir / task.task_id
            self.write_task_to_disk(task, speccheck, task_dir)

    def generate_and_save_all(self):
        """Main entry point: generate and save all tasks."""
        if not self.load_skill_specification():
            return False

        print("\n=== Generating Training Tasks ===")
        train_tasks, train_specchecks = self.generate_tasks()

        print("\n=== Generating Test Tasks ===")
        test_tasks, test_specchecks = self.generate_test_tasks()

        # v1.2.0: Add boundary probing if enabled
        if self.probe_boundaries and BOUNDARY_PROBING_AVAILABLE:
            print("\n=== Generating Boundary Tasks (v1.2.0) ===")
            prober = CapabilityBoundaryProber(self.skill_md_content)
            prober.analyze_skill_boundaries()
            boundary_specs = prober.generate_boundary_tasks()

            # Convert boundary specs to Task objects
            boundary_tasks = []
            boundary_specchecks = []
            for i, spec in enumerate(boundary_specs, 1):
                task_id = f"boundary_{i:03d}"
                task = Task(
                    task_id=task_id,
                    task_type="boundary",
                    title=spec['title'],
                    background=f"Boundary test: {spec['task_type']}",
                    objective=spec['objective'],
                    input_description="Test input designed to probe capability boundaries",
                    expected_behavior=spec['expected_behavior'],
                    constraints=spec['constraints'],
                    workspace_files={}
                )
                boundary_tasks.append(task)

                # Create speccheck
                criteria = [SpecCheckCriterion(c, "Manual verification") for c in spec['constraints']]
                speccheck = SpecCheck(
                    task_id=task_id,
                    criteria=criteria,
                    total_points=len(criteria),
                    pass_threshold=int(len(criteria) * 0.7),
                    evaluation_notes=f"Boundary test: {spec['task_type']}"
                )
                boundary_specchecks.append(speccheck)

            print(f"✓ Generated {len(boundary_tasks)} boundary tasks")

            # Integrate boundary tasks into train/test split only if we have boundary tasks
            if len(boundary_tasks) > 0:
                # Training: 6 standard + 4 advanced + 6 boundary
                # Test: 4 standard + 3 advanced + 3 boundary
                train_standard = [t for t in train_tasks if t.task_type == "standard"][:6]
                train_advanced = [t for t in train_tasks if t.task_type == "advanced"][:4]
                train_boundary = boundary_tasks[:6]

                test_standard = [t for t in test_tasks if t.task_type == "standard"][:4]
                test_advanced = [t for t in test_tasks if t.task_type == "advanced"][:3]
                test_boundary = boundary_tasks[6:9]

                train_tasks = train_standard + train_advanced + train_boundary
                test_tasks = test_standard + test_advanced + test_boundary

                # Update specchecks accordingly
                train_ids = [t.task_id for t in train_tasks]
                test_ids = [t.task_id for t in test_tasks]

                all_specchecks = train_specchecks + test_specchecks + boundary_specchecks
                train_specchecks = [s for s in all_specchecks if s.task_id in train_ids]
                test_specchecks = [s for s in all_specchecks if s.task_id in test_ids]
            else:
                # No boundary tasks - use original distribution
                # Keep the original train/test split from generate_tasks() and generate_test_tasks()
                print("⚠ No boundary tasks generated - using standard distribution")

        self.save_tasks(train_tasks, train_specchecks, "train")
        print(f"✓ Saved {len(train_tasks)} training tasks")

        self.save_tasks(test_tasks, test_specchecks, "test")
        print(f"✓ Saved {len(test_tasks)} test tasks")

        # Save metadata
        metadata = {
            "target_skill": str(self.target_skill_path),
            "train_tasks": len(train_tasks),
            "test_tasks": len(test_tasks),
            "train_standard": len([t for t in train_tasks if t.task_type == "standard"]),
            "train_advanced": len([t for t in train_tasks if t.task_type == "advanced"]),
            "train_boundary": len([t for t in train_tasks if t.task_type == "boundary"]),
            "test_standard": len([t for t in test_tasks if t.task_type == "standard"]),
            "test_advanced": len([t for t in test_tasks if t.task_type == "advanced"]),
            "test_boundary": len([t for t in test_tasks if t.task_type == "boundary"]),
            "boundary_probing_enabled": self.probe_boundaries and BOUNDARY_PROBING_AVAILABLE,
        }

        with open(self.output_dir / "tasks" / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)

        print("\n✓ Task generation complete!")
        return True


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python task_generator.py <target-skill-path> [output-dir]")
        sys.exit(1)

    target_skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    generator = TaskGenerator(target_skill_path, output_dir)
    success = generator.generate_and_save_all()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
