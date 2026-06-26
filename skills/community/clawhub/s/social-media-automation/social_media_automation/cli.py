"""
CLI interface for Social Media Automation
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from social_media_automation.config import Config
from social_media_automation.core.content_manager import ContentManager
from social_media_automation.core.scheduler import PostScheduler
from social_media_automation.core.template_manager import TemplateManager
from social_media_automation.storage.database import Database

app = typer.Typer(
    name="social-media-automation",
    help="Multi-platform social media automation tool",
    no_args_is_help=True,
)
console = Console()


def _parse_variables(variables_str: str) -> dict[str, str]:
    """
    Parse variables from JSON format or key=value pairs.

    Args:
        variables_str: Variables in JSON format (e.g., '{"name":"John"}')
                       or key=value format (e.g., 'name=John age=30')

    Returns:
        Dictionary of variables

    Raises:
        ValueError: If variables cannot be parsed
    """
    import json
    import shlex

    # Try JSON format first
    try:
        if variables_str.startswith("{"):
            return json.loads(variables_str)
    except json.JSONDecodeError:
        pass

    # Try key=value format (using shlex to handle quoted values)
    variables_dict = {}
    try:
        parts = shlex.split(variables_str)
        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                variables_dict[key] = value
            else:
                console.print(f"[yellow]Warning: Ignoring invalid variable format: {part}[/yellow]")
    except ValueError as e:
        raise ValueError(
            f"Failed to parse variables: {e}. "
            "Use JSON format (e.g., '{\"name\":\"John\"}') "
            "or key=value format (e.g., 'name=John age=30')"
        )

    if not variables_dict:
        raise ValueError(
            "Variables must be in JSON format (e.g., '{\"name\":\"John\"}') "
            "or key=value format (e.g., 'name=John age=30')"
        )

    return variables_dict


@app.command()
def init(
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing config"),
) -> None:
    """
    Initialize configuration for social media automation
    """
    config_path = Path(".env")

    if config_path.exists() and not force:
        console.print("[yellow]Configuration already exists.[/yellow]")
        if not typer.confirm("Do you want to overwrite?"):
            return

    # Create .env from example
    example_path = Path(__file__).parent.parent / ".env.example"
    if example_path.exists():
        import shutil

        shutil.copy(example_path, config_path)
        console.print("[green]✓ Configuration file created: .env[/green]")
        console.print("\n[yellow]Please edit .env with your API credentials.[/yellow]")
    else:
        console.print("[red]✗ .env.example not found[/red]")
        raise typer.Exit(1)


@app.command()
def post(
    text: str = typer.Argument(..., help="Text content to post"),
    platform: str = typer.Option("x", "--platform", "-p", help="Platform to post to"),
) -> None:
    """
    Post content to social media platform
    """
    try:
        config = Config.load()
        db = Database()

        # Get platform client
        if platform == "x" or platform == "twitter":
            from social_media_automation.platforms.x.client import TwitterClient

            client = TwitterClient(config)
            console.print(f"[cyan]Posting to X (Twitter):[/cyan] {text[:50]}...")
            result = client.post_tweet(text)
            console.print(f"[green]✓ Posted successfully[/green]")
            console.print(f"  URL: https://x.com/user/status/{result.data.id}")

            # Save to database
            db.save_post(
                platform=platform,
                content=text,
                post_id=result.data.id,
                status="posted",
            )
        else:
            console.print(f"[red]✗ Unsupported platform: {platform}[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def schedule(
    text: str = typer.Argument(..., help="Text content to post"),
    platform: str = typer.Option("x", "--platform", "-p", help="Platform to post to"),
    when: str = typer.Option(..., "--when", "-w", help="When to post (ISO 8601 format)"),
) -> None:
    """
    Schedule a post for future publication
    """
    try:
        config = Config.load()
        db = Database()

        # Parse datetime
        from datetime import datetime

        scheduled_time = datetime.fromisoformat(when)

        # Save to database
        db.save_post(
            platform=platform,
            content=text,
            scheduled_at=scheduled_time,
            status="scheduled",
        )

        console.print(f"[green]✓ Post scheduled[/green]")
        console.print(f"  Platform: {platform}")
        console.print(f"  Time: {scheduled_time}")
        console.print(f"  Content: {text[:50]}...")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


# Schedule commands
schedule_app = typer.Typer(name="schedule", help="Schedule management")
app.add_typer(schedule_app, name="schedule")


@schedule_app.command("list")
def schedule_list() -> None:
    """
    List all scheduled posts
    """
    try:
        db = Database()
        posts = db.get_scheduled_posts()

        if not posts:
            console.print("[yellow]No scheduled posts found[/yellow]")
            return

        table = Table(title="Scheduled Posts")
        table.add_column("ID", style="cyan")
        table.add_column("Platform", style="magenta")
        table.add_column("Content", style="white")
        table.add_column("Scheduled At", style="yellow")
        table.add_column("Status", style="green")

        for post in posts:
            table.add_row(
                str(post["id"]),
                post["platform"],
                post["content"][:50] + "...",
                post["scheduled_at"],
                post["status"],
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@schedule_app.command("cancel")
def schedule_cancel(post_id: int = typer.Argument(..., help="Post ID to cancel")) -> None:
    """
    Cancel a scheduled post
    """
    try:
        db = Database()
        scheduler = PostScheduler()

        # Confirm
        post = db.get_post(post_id)
        if not post:
            console.print(f"[red]✗ Post not found: {post_id}[/red]")
            raise typer.Exit(1)

        console.print(f"[yellow]Cancelling scheduled post:[/yellow]")
        console.print(f"  ID: {post['id']}")
        console.print(f"  Platform: {post['platform']}")
        console.print(f"  Content: {post['content'][:50]}...")
        console.print(f"  Scheduled: {post['scheduled_at']}")

        if not typer.confirm("Are you sure?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

        success = scheduler.remove_scheduled_post(post_id)

        if success:
            console.print(f"[green]✓ Post cancelled[/green]")
        else:
            console.print(f"[red]✗ Failed to cancel post[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@schedule_app.command("recurring:add")
def schedule_recurring_add(
    content: str = typer.Option(..., "--content", "-c", help="Content to post"),
    cron: str = typer.Option(..., "--cron", help="Cron expression (minute hour day month weekday)"),
    platform: str = typer.Option("x", "--platform", "-p", help="Platform to post to"),
    timezone: str = typer.Option("Asia/Tokyo", "--timezone", "-t", help="Timezone"),
) -> None:
    """
    Add a recurring post using cron expression
    """
    try:
        config = Config.load()
        scheduler = PostScheduler(config)

        job_id = scheduler.schedule_recurring_post(platform, content, cron, timezone)

        console.print(f"[green]✓ Recurring post scheduled[/green]")
        console.print(f"  Job ID: {job_id}")
        console.print(f"  Platform: {platform}")
        console.print(f"  Content: {content[:50]}...")
        console.print(f"  Cron: {cron}")
        console.print(f"  Timezone: {timezone}")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@schedule_app.command("recurring:list")
def schedule_recurring_list() -> None:
    """
    List all recurring posts
    """
    try:
        scheduler = PostScheduler()
        jobs = scheduler.list_recurring_jobs()

        if not jobs:
            console.print("[yellow]No recurring posts found[/yellow]")
            return

        table = Table(title="Recurring Posts")
        table.add_column("Job ID", style="cyan")
        table.add_column("Trigger", style="magenta")
        table.add_column("Next Run", style="yellow")

        for job in jobs:
            table.add_row(
                job["id"],
                job["trigger"],
                job["next_run"][:19].replace("T", " ") if job["next_run"] else "N/A",
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@schedule_app.command("recurring:remove")
def schedule_recurring_remove(
    job_id: str = typer.Argument(..., help="Job ID to remove"),
) -> None:
    """
    Remove a recurring post
    """
    try:
        scheduler = PostScheduler()

        if not typer.confirm(f"Are you sure you want to remove job {job_id}?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

        success = scheduler.remove_recurring_post(job_id)

        if success:
            console.print(f"[green]✓ Recurring post removed[/green]")
        else:
            console.print(f"[red]✗ Failed to remove recurring post[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("config:show")
def config_show() -> None:
    """
    Show current configuration (without sensitive data)
    """
    try:
        config = Config.load()

        console.print("[cyan]Current Configuration:[/cyan]")
        console.print(f"  Twitter API Key: {config.twitter_api_key[:10]}..." if config.twitter_api_key else "  Twitter API Key: [red]Not configured[/red]")
        console.print(f"  Bluesky Handle: {config.bluesky_handle}" if config.bluesky_handle else "  Bluesky Handle: [red]Not configured[/red]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("draft:create")
def draft_create(
    platform: str = typer.Option(..., "--platform", "-p", help="Target platform"),
    content: str = typer.Option(..., "--content", "-c", help="Draft content"),
    media: list[str] = typer.Option([], "--media", "-m", help="Media file paths"),
    schedule: str | None = typer.Option(None, "--schedule", "-s", help="Schedule time (ISO 8601)"),
) -> None:
    """
    Create a new draft
    """
    try:
        config = Config.load()
        db = Database()
        content_manager = ContentManager(db)

        # Create draft
        draft_id = content_manager.create_draft(
            platform=platform,
            content=content,
            media_paths=media if media else None,
            scheduled_at=schedule,
        )

        console.print(f"[green]✓ Draft created[/green]")
        console.print(f"  ID: {draft_id}")
        console.print(f"  Platform: {platform}")
        console.print(f"  Content: {content[:50]}...")

        if schedule:
            console.print(f"  Scheduled: {schedule}")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("draft:list")
def draft_list(
    platform: str | None = typer.Option(None, "--platform", "-p", help="Filter by platform"),
    limit: int = typer.Option(20, "--limit", "-l", help="Number of drafts to show"),
) -> None:
    """
    List all drafts
    """
    try:
        db = Database()
        content_manager = ContentManager(db)

        drafts = content_manager.list_drafts(platform=platform, limit=limit)

        if not drafts:
            console.print("[yellow]No drafts found[/yellow]")
            return

        table = Table(title="Drafts")
        table.add_column("ID", style="cyan")
        table.add_column("Platform", style="magenta")
        table.add_column("Content", style="white")
        table.add_column("Status", style="yellow")
        table.add_column("Created", style="green")

        for draft in drafts:
            table.add_row(
                str(draft["id"]),
                draft["platform"],
                draft["content"][:50] + "...",
                draft["status"],
                draft["created_at"][:19].replace("T", " "),
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("draft:show")
def draft_show(draft_id: int = typer.Argument(..., help="Draft ID")) -> None:
    """
    Show details of a specific draft
    """
    try:
        db = Database()
        content_manager = ContentManager(db)

        draft = content_manager.get_draft(draft_id)

        if not draft:
            console.print(f"[red]✗ Draft not found: {draft_id}[/red]")
            raise typer.Exit(1)

        console.print(f"[cyan]Draft ID:[/cyan] {draft['id']}")
        console.print(f"[cyan]Platform:[/cyan] {draft['platform']}")
        console.print(f"[cyan]Status:[/cyan] {draft['status']}")
        console.print(f"[cyan]Content:[/cyan] {draft['content']}")
        console.print(f"[cyan]Character count:[/cyan] {len(draft['content'])}")

        # Show platform limits
        limits = content_manager.PLATFORM_LIMITS.get(draft['platform'])
        if limits:
            console.print(f"[cyan]Limit:[/cyan] {len(draft['content'])}/{limits.max_characters}")

        if draft['media_attachments']:
            console.print(f"[cyan]Media attachments:[/cyan] {len(draft['media_attachments'])}")
            for i, media in enumerate(draft['media_attachments'], 1):
                console.print(f"  {i}. {media['media_type']}: {media['path']}")
        else:
            console.print("[cyan]Media attachments:[/cyan] None")

        console.print(f"[cyan]Created:[/cyan] {draft['created_at'][:19].replace('T', ' ')}")
        if draft['scheduled_at']:
            console.print(f"[cyan]Scheduled:[/cyan] {draft['scheduled_at'][:19].replace('T', ' ')}")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("draft:edit")
def draft_edit(
    draft_id: int = typer.Argument(..., help="Draft ID"),
    content: str | None = typer.Option(None, "--content", "-c", help="New content"),
    media: list[str] | None = typer.Option(None, "--media", "-m", help="New media files (replaces existing)"),
) -> None:
    """
    Edit a draft
    """
    try:
        db = Database()
        content_manager = ContentManager(db)

        # Get current draft
        current = content_manager.get_draft(draft_id)
        if not current:
            console.print(f"[red]✗ Draft not found: {draft_id}[/red]")
            raise typer.Exit(1)

        # Update draft
        if not content and not media:
            console.print("[yellow]No changes specified[/yellow]")
            return

        success = content_manager.update_draft(
            draft_id=draft_id,
            content=content,
            media_paths=media if media is not None else None,
        )

        if success:
            console.print(f"[green]✓ Draft updated[/green]")
            console.print(f"  ID: {draft_id}")
        else:
            console.print(f"[red]✗ Failed to update draft[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


# Template commands
template_app = typer.Typer(name="template", help="Template management")
app.add_typer(template_app, name="template")


@template_app.command("create")
def template_create(
    name: str = typer.Option(..., "--name", "-n", help="Template name"),
    platform: str = typer.Option(..., "--platform", "-p", help="Platform for the template"),
    content: str = typer.Option(..., "--content", "-c", help="Template content"),
    file: str | None = typer.Option(None, "--file", "-f", help="Read content from file"),
) -> None:
    """
    Create a new template
    """
    try:
        # Read from file if specified
        if file:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()

        # Extract variables from content
        import re

        pattern = r"\{\{([^}]+)\}\}"
        variables = list(set([m.strip() for m in re.findall(pattern, content)]))

        template_manager = TemplateManager()
        template_id = template_manager.create_template(name, content, platform, variables)

        if variables:
            console.print(f"[cyan]Variables detected:[/cyan] {', '.join(variables)}")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@template_app.command("list")
def template_list(
    platform: str | None = typer.Option(None, "--platform", "-p", help="Filter by platform"),
    limit: int = typer.Option(20, "--limit", "-l", help="Number of templates to show"),
) -> None:
    """
    List all templates
    """
    try:
        template_manager = TemplateManager()
        templates = template_manager.list_templates(platform, limit)

        if not templates:
            console.print("[yellow]No templates found[/yellow]")
            return

        table = Table(title="Templates")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Platform", style="white")
        table.add_column("Variables", style="yellow")
        table.add_column("Content", style="green")

        for template in templates:
            vars_str = ", ".join(template["variables"]) if template["variables"] else "None"
            content_preview = template["content"][:50] + "..." if len(template["content"]) > 50 else template["content"]

            table.add_row(
                str(template["id"]),
                template["name"],
                template["platform"],
                vars_str,
                content_preview,
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@template_app.command("show")
def template_show(
    template_id: str = typer.Argument(..., help="Template ID or name"),
) -> None:
    """
    Show details of a specific template
    """
    try:
        template_manager = TemplateManager()

        # Support both ID and name
        if template_id.isdigit():
            template = template_manager.get_template(int(template_id))
        else:
            template = template_manager.get_template_by_name(template_id)

        if not template:
            console.print(f"[red]✗ Template not found: {template_id}[/red]")
            raise typer.Exit(1)

        console.print(f"[cyan]Template ID:[/cyan] {template['id']}")
        console.print(f"[cyan]Name:[/cyan] {template['name']}")
        console.print(f"[cyan]Platform:[/cyan] {template['platform']}")
        console.print(f"[cyan]Variables:[/cyan] {', '.join(template['variables']) if template['variables'] else 'None'}")
        console.print(f"[cyan]Content:[/cyan]")
        console.print(f"  {template['content']}")
        console.print(f"[cyan]Character count:[/cyan] {len(template['content'])}")
        console.print(f"[cyan]Created:[/cyan] {template['created_at'][:19].replace('T', ' ')}")
        console.print(f"[cyan]Updated:[/cyan] {template['updated_at'][:19].replace('T', ' ')}")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@template_app.command("use")
def template_use(
    template_id: str = typer.Argument(..., help="Template ID or name"),
    variables: str = typer.Argument(..., help="Variables in JSON format (e.g., '{\"name\":\"John\"}') or key=value format"),
    output: bool = typer.Option(False, "--output", "-o", help="Output content to console"),
    save: bool = typer.Option(False, "--save", "-s", help="Save as draft"),
    platform: str | None = typer.Option(None, "--platform", "-p", help="Platform for draft"),
    schedule: str | None = typer.Option(None, "--schedule", help="Schedule time (ISO 8601)"),
) -> None:
    """
    Use a template and apply variables

    Variables can be provided in JSON format or as key=value pairs.
    JSON format: '{"name":"John","age":"30"}'
    Key=value format: 'name=John age=30'
    """
    try:
        template_manager = TemplateManager()

        # Parse variables
        variables_dict = _parse_variables(variables)

        # Apply template
        content = template_manager.use_template(template_id, variables_dict)

        if output:
            console.print(f"\n[cyan]Generated content:[/cyan]")
            console.print(content)

        if save:
            config = Config.load()
            db = Database()
            content_manager = ContentManager(db)

            # Get platform from template if not specified
            if not platform:
                if template_id.isdigit():
                    template = template_manager.get_template(int(template_id))
                else:
                    template = template_manager.get_template_by_name(template_id)
                platform = template["platform"] if template else "x"

            # Create draft
            draft_id = content_manager.create_draft(
                platform=platform,
                content=content,
                scheduled_at=schedule,
            )

            console.print(f"\n[green]✓ Draft created from template[/green]")
            console.print(f"  Draft ID: {draft_id}")

        if not output and not save:
            console.print(f"\n[cyan]Generated content:[/cyan]")
            console.print(content)
            console.print("\n[yellow]Use --output to display or --save to create a draft[/yellow]")

    except ValueError as e:
        console.print(f"[red]✗ Validation error: {e}[/red]")
        console.print("\n[yellow]Tips:[/yellow]")
        console.print("  - Use JSON format: '{\"name\":\"John\"}'")
        console.print("  - Use key=value format: 'name=John age=30'")
        console.print("  - Check template variables with: template show <template_id>")
        raise typer.Exit(1)
    except KeyError as e:
        console.print(f"[red]✗ Missing variable: {e}[/red]")
        console.print("\n[yellow]Check required variables with:[/yellow]")
        console.print(f"  template show {template_id}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        console.print("\n[yellow]For more information, use:[/yellow]")
        console.print(f"  template show {template_id}")
        raise typer.Exit(1)


@template_app.command("delete")
def template_delete(
    template_id: str = typer.Argument(..., help="Template ID or name"),
) -> None:
    """
    Delete a template
    """
    try:
        template_manager = TemplateManager()

        # Get template
        if template_id.isdigit():
            template = template_manager.get_template(int(template_id))
        else:
            template = template_manager.get_template_by_name(template_id)

        if not template:
            console.print(f"[red]✗ Template not found: {template_id}[/red]")
            raise typer.Exit(1)

        # Confirm
        console.print(f"[yellow]Deleting template:[/yellow]")
        console.print(f"  Name: {template['name']}")
        console.print(f"  Platform: {template['platform']}")
        console.print(f"  Content: {template['content'][:50]}...")

        if not typer.confirm("Are you sure?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

        template_manager.delete_template(template["id"])

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("draft:delete")
def draft_delete(draft_id: int = typer.Argument(..., help="Draft ID")) -> None:
    """
    Delete a draft
    """
    try:
        db = Database()
        content_manager = ContentManager(db)

        # Confirm
        draft = content_manager.get_draft(draft_id)
        if not draft:
            console.print(f"[red]✗ Draft not found: {draft_id}[/red]")
            raise typer.Exit(1)

        console.print(f"[yellow]Deleting draft:[/yellow]")
        console.print(f"  Platform: {draft['platform']}")
        console.print(f"  Content: {draft['content'][:50]}...")

        if not typer.confirm("Are you sure?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

        success = content_manager.delete_draft(draft_id)

        if success:
            console.print(f"[green]✓ Draft deleted[/green]")
        else:
            console.print(f"[red]✗ Failed to delete draft[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


# Timeline commands
timeline_app = typer.Typer(name="timeline", help="Timeline management")
app.add_typer(timeline_app, name="timeline")


@timeline_app.command("home")
def timeline_home(
    limit: int = typer.Option(20, "--limit", "-l", help="Number of tweets to fetch"),
) -> None:
    """Get home timeline"""
    try:
        config = Config.load()

        if config.twitter_api_key:
            from social_media_automation.platforms.x.client import TwitterClient

            client = TwitterClient(config)
            tweets = client.get_home_timeline(limit)

            if not tweets:
                console.print("[yellow]No tweets found[/yellow]")
                return

            table = Table(title="Home Timeline")
            table.add_column("ID", style="cyan")
            table.add_column("Author", style="magenta")
            table.add_column("Content", style="white")
            table.add_column("Date", style="yellow")

            for tweet in tweets:
                table.add_row(
                    str(tweet.id),
                    str(tweet.author_id),
                    tweet.text[:80] + "..." if len(tweet.text) > 80 else tweet.text,
                    str(tweet.created_at) if tweet.created_at else "N/A",
                )

            console.print(table)
        else:
            console.print("[red]✗ Twitter API not configured[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@timeline_app.command("user")
def timeline_user(
    username: str = typer.Argument(..., help="Twitter username"),
    limit: int = typer.Option(20, "--limit", "-l", help="Number of tweets to fetch"),
) -> None:
    """Get user timeline"""
    try:
        config = Config.load()

        if config.twitter_api_key:
            from social_media_automation.platforms.x.client import TwitterClient

            client = TwitterClient(config)
            tweets = client.get_user_timeline(username, limit)

            if not tweets:
                console.print(f"[yellow]No tweets found for @{username}[/yellow]")
                return

            table = Table(title=f"@{username} Timeline")
            table.add_column("ID", style="cyan")
            table.add_column("Content", style="white")
            table.add_column("Date", style="yellow")

            for tweet in tweets:
                table.add_row(
                    str(tweet.id),
                    tweet.text[:80] + "..." if len(tweet.text) > 80 else tweet.text,
                    str(tweet.created_at) if tweet.created_at else "N/A",
                )

            console.print(table)
        else:
            console.print("[red]✗ Twitter API not configured[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


# Interaction commands
@app.command("reply")
def reply(
    tweet_id: str = typer.Argument(..., help="Tweet ID to reply to"),
    text: str = typer.Argument(..., help="Reply text"),
) -> None:
    """Reply to a tweet"""
    try:
        config = Config.load()

        if config.twitter_api_key:
            from social_media_automation.platforms.x.client import TwitterClient

            client = TwitterClient(config)
            console.print(f"[cyan]Replying to tweet {tweet_id}[/cyan]")
            result = client.post_reply(tweet_id, text)
            console.print(f"[green]✓ Reply posted successfully[/green]")
            console.print(f"  URL: https://x.com/user/status/{result.data.id}")
        else:
            console.print("[red]✗ Twitter API not configured[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("retweet")
def retweet(
    tweet_id: str = typer.Argument(..., help="Tweet ID to retweet"),
) -> None:
    """Retweet a tweet"""
    try:
        config = Config.load()

        if config.twitter_api_key:
            from social_media_automation.platforms.x.client import TwitterClient

            client = TwitterClient(config)
            console.print(f"[cyan]Retweeting tweet {tweet_id}[/cyan]")
            client.retweet(tweet_id)
            console.print("[green]✓ Retweeted successfully[/green]")
        else:
            console.print("[red]✗ Twitter API not configured[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("like")
def like(
    tweet_id: str = typer.Argument(..., help="Tweet ID to like"),
) -> None:
    """Like a tweet"""
    try:
        config = Config.load()

        if config.twitter_api_key:
            from social_media_automation.platforms.x.client import TwitterClient

            client = TwitterClient(config)
            console.print(f"[cyan]Liking tweet {tweet_id}[/cyan]")
            client.like_tweet(tweet_id)
            console.print("[green]✓ Liked successfully[/green]")
        else:
            console.print("[red]✗ Twitter API not configured[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("mentions")
def mentions(
    limit: int = typer.Option(20, "--limit", "-l", help="Number of mentions to fetch"),
) -> None:
    """Get mentions timeline"""
    try:
        config = Config.load()

        if config.twitter_api_key:
            from social_media_automation.platforms.x.client import TwitterClient

            client = TwitterClient(config)
            tweets = client.get_mentions(limit)

            if not tweets:
                console.print("[yellow]No mentions found[/yellow]")
                return

            table = Table(title="Mentions")
            table.add_column("ID", style="cyan")
            table.add_column("Author", style="magenta")
            table.add_column("Content", style="white")
            table.add_column("Date", style="yellow")

            for tweet in tweets:
                table.add_row(
                    str(tweet.id),
                    str(tweet.author_id),
                    tweet.text[:80] + "..." if len(tweet.text) > 80 else tweet.text,
                    str(tweet.created_at) if tweet.created_at else "N/A",
                )

            console.print(table)
        else:
            console.print("[red]✗ Twitter API not configured[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


# Auth commands
auth_app = typer.Typer(name="auth", help="Authentication management")
app.add_typer(auth_app, name="auth")


@auth_app.command("login")
def auth_login() -> None:
    """Start interactive OAuth login flow"""
    try:
        config = Config.load()

        if not config.twitter_api_key or not config.twitter_api_secret:
            console.print("[red]✗ Twitter API keys not configured[/red]")
            console.print("[yellow]Please set TWITTER_API_KEY and TWITTER_API_SECRET in .env[/yellow]")
            raise typer.Exit(1)

        from social_media_automation.core.oauth import OAuthFlow, save_tokens

        oauth = OAuthFlow(config)
        access_token, access_token_secret = oauth.interactive_auth()

        # Save tokens
        save_tokens(access_token, access_token_secret)

        console.print("[green]✓ Authentication successful[/green]")
        console.print("[yellow]Please restart your application to use the new credentials[/yellow]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


# Rate limit commands
@app.command("rate-limit")
def rate_limit() -> None:
    """Show rate limit status"""
    try:
        config = Config.load()

        if config.twitter_api_key:
            from social_media_automation.platforms.x.client import TwitterClient

            client = TwitterClient(config)
            status = client.get_rate_limit_status()

            if not status:
                console.print("[yellow]No rate limit information available[/yellow]")
                return

            table = Table(title="Rate Limit Status")
            table.add_column("Endpoint", style="cyan")
            table.add_column("Remaining", style="green")
            table.add_column("Limit", style="magenta")
            table.add_column("Resets At", style="yellow")

            for endpoint, info in status.items():
                table.add_row(
                    endpoint,
                    str(info["remaining"]),
                    str(info["limit"]),
                    info["reset_at"][:19] if "reset_at" in info else "N/A",
                )

            console.print(table)
        else:
            console.print("[red]✗ Twitter API not configured[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
