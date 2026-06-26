"""Content generator for social media posts from GitHub activity."""

import re
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

from rich.console import Console

from .github_monitor import CommitInfo
from ..config import get_config, OpenClawConfig

console = Console()


class GeneratedContent(BaseModel):
    """Generated social media content."""

    platform: str
    content: str
    media: Optional[str] = None
    hashtags: List[str] = []
    scheduled_for: Optional[datetime] = None


class ContentGenerator:
    """Generate social media content from GitHub activity."""

    def __init__(self):
        """Initialize content generator."""
        self.config = get_config()
        self.templates = self.config.openclaw.content_templates if self.config.openclaw else {}

    def generate_from_commit(self, commit: CommitInfo, platform: str) -> GeneratedContent:
        """
        Generate content from a commit.

        Args:
            commit: Commit information
            platform: Target platform (x, linkedin, instagram)

        Returns:
            GeneratedContent object
        """
        console.print(f"[cyan]Generating {platform} content from commit...[/cyan]")

        # Parse commit message
        message = commit.message
        feature = self._extract_feature(message)
        repo_name = self._extract_repo_name(commit.repository)
        branch = commit.branch or "main"

        # Get template
        if platform == "x" and "commit_tweet" in self.templates:
            template = self.templates["commit_tweet"]
            content = self._fill_template(template, {
                "feature": feature,
                "repo": repo_name,
                "branch": branch
            })

            # Truncate if too long
            char_limit = 280
            if len(content) > char_limit:
                content = content[:char_limit-3] + "..."

            # Extract hashtags
            hashtags = self._generate_hashtags(content, platform)

        elif platform == "linkedin" and "linkedin_post" in self.templates:
            template = self.templates["linkedin_post"]
            content = self._fill_template(template, {
                "feature": feature,
                "repo": repo_name,
                "branch": branch,
                "author": commit.author
            })

            # Truncate if too long
            char_limit = 3000
            if len(content) > char_limit:
                content = content[:char_limit-3] + "..."

            # Extract hashtags
            hashtags = self._generate_hashtags(content, platform)

        else:
            # Default template
            content = f"New commit to {repo_name}: {message[:100]}"
            hashtags = []

        console.print(f"[green]✓ Generated {platform} content[/green]")
        console.print(f"  Content: {content[:50]}...")

        return GeneratedContent(
            platform=platform,
            content=content,
            hashtags=hashtags
        )

    def generate_from_release(self, repo_name: str, version: str, changelog: str, platform: str) -> GeneratedContent:
        """
        Generate content from a release.

        Args:
            repo_name: Repository name
            version: Version number
            changelog: Changelog text
            platform: Target platform

        Returns:
            GeneratedContent object
        """
        console.print(f"[cyan]Generating {platform} content from release...[/cyan]")

        # Get template
        if platform == "x" and "release_tweet" in self.templates:
            template = self.templates["release_tweet"]
            content = self._fill_template(template, {
                "version": version,
                "repo": repo_name,
                "changelog": changelog[:100] if changelog else "Minor fixes and improvements"
            })

            # Truncate if too long
            char_limit = 280
            if len(content) > char_limit:
                content = content[:char_limit-3] + "..."

            # Extract hashtags
            hashtags = self._generate_hashtags(content, platform)

        elif platform == "linkedin" and "linkedin_article" in self.templates:
            template = self.templates["linkedin_article"]
            content = self._fill_template(template, {
                "version": version,
                "repo": repo_name,
                "changelog": changelog
            })

            # Extract hashtags
            hashtags = self._generate_hashtags(content, platform)

        else:
            # Default template
            content = f"New version {version} of {repo_name} is out! 🎉"
            hashtags = ["#opensource", "#release"]

        console.print(f"[green]✓ Generated {platform} content[/green]")
        console.print(f"  Content: {content[:50]}...")

        return GeneratedContent(
            platform=platform,
            content=content,
            hashtags=hashtags
        )

    def _extract_feature(self, message: str) -> str:
        """
        Extract feature name from commit message.

        Args:
            message: Commit message

        Returns:
            Feature name
        """
        # Try to extract "feature:" prefix
        if message.lower().startswith("feat:"):
            feature = message[5:].strip()
        elif message.lower().startswith("feature:"):
            feature = message[8:].strip()
        else:
            # Extract first line or sentence
            lines = message.split('\n')
            first_line = lines[0].strip()

            # Try to extract from common patterns
            patterns = [
                r'add (.+)',
                r'implement (.+)',
                r'update (.+)',
                r'fix (.+)',
                r'(.+) (?:functionality|feature|support)'
            ]

            for pattern in patterns:
                match = re.search(pattern, first_line, re.IGNORECASE)
                if match:
                    feature = match.group(1)
                    break
            else:
                feature = first_line[:50]

        return feature[:100]  # Limit feature name

    def _extract_repo_name(self, repo_name: str) -> str:
        """
        Extract clean repository name.

        Args:
            repo_name: Repository name (owner/repo)

        Returns:
            Clean repository name
        """
        parts = repo_name.split('/')
        return parts[-1] if len(parts) > 1 else repo_name

    def _fill_template(self, template: str, variables: Dict[str, str]) -> str:
        """
        Fill template with variables.

        Args:
            template: Template string
            variables: Variables to fill

        Returns:
            Filled template
        """
        content = template
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            content = content.replace(placeholder, value)

        return content

    def _generate_hashtags(self, content: str, platform: str) -> List[str]:
        """
        Generate relevant hashtags.

        Args:
            content: Content text
            platform: Target platform

        Returns:
            List of hashtags
        """
        hashtags = []

        # Platform-specific hashtags
        if platform == "x":
            hashtags.extend(["#coding", "#dev", "#opensource"])
        elif platform == "linkedin":
            hashtags.extend(["#development", "#opensource", "#tech"])
        elif platform == "instagram":
            hashtags.extend(["#dev", "#coding", "#programmer"])

        # Content-based hashtags
        words = content.split()
        for word in words:
            # Common tech keywords
            tech_keywords = [
                "python", "javascript", "java", "api", "web", "mobile",
                "react", "vue", "node", "docker", "kubernetes",
                "ci/cd", "testing", "deployment", "security"
            ]

            if word.lower() in tech_keywords:
                hashtags.append(f"#{word.lower()}")

        # Remove duplicates and limit
        hashtags = list(set(hashtags))
        if platform == "x":
            hashtags = hashtags[:3]  # Limit hashtags for Twitter
        else:
            hashtags = hashtags[:5]  # More hashtags for other platforms

        return hashtags

    def generate_batch(self, commits: List[CommitInfo], platform: str = "x") -> List[GeneratedContent]:
        """
        Generate content for multiple commits.

        Args:
            commits: List of CommitInfo objects
            platform: Target platform

        Returns:
            List of GeneratedContent objects
        """
        console.print(f"[cyan]Generating {platform} content for {len(commits)} commits...[/cyan]")

        contents = []
        for commit in commits:
            content = self.generate_from_commit(commit, platform)
            contents.append(content)

        console.print(f"[green]✓ Generated {len(contents)} contents[/green]")
        return contents

    def customize_template(self, name: str, template: str) -> bool:
        """
        Add a custom content template.

        Args:
            name: Template name
            template: Template string

        Returns:
            True if successful
        """
        console.print(f"[cyan]Adding custom template: {name}[/cyan]")

        if not template:
            console.print("[red]✗ Template cannot be empty[/red]")
            return False

        # Store in config (would need to update config)
        console.print(f"[yellow]⚠ Custom template storage not implemented yet[/yellow]")
        return False

    def list_templates(self) -> Dict[str, str]:
        """
        List all available content templates.

        Returns:
            Dictionary of template names and templates
        """
        console.print("[cyan]Available content templates:[/cyan]")

        # Add default templates if not present
        default_templates = {
            "commit_tweet": "Just pushed {feature} to {repo}! 🚀 #{repo} #coding",
            "release_tweet": "New version {version} of {repo} is out! 🎉 {changelog}",
            "linkedin_post": "I just released {feature} in {repo}. This update includes several improvements and bug fixes. Check it out! #opensource #development"
            "linkedin_article": "I'm excited to announce the release of {repo} version {version}!{changelog} This release represents a significant milestone for the project. I'd like to thank all contributors who helped make this possible."
        }

        templates = {**default_templates, **self.templates}

        for name, template in templates.items():
            console.print(f"  [cyan]{name}[/cyan]")
            console.print(f"    {template[:60]}...")

        return templates
