"""Scheduler for Social Media Automation."""

import time
import threading
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from pytz import timezone as pytz

from rich.console import Console

from .storage.database import Database, Post

console = Console()


class Scheduler:
    """Manage post scheduling and queue processing."""

    def __init__(self, db_path: str = None, batch_size: int = 5, timezone: str = "Asia/Tokyo"):
        """
        Initialize scheduler.

        Args:
            db_path: Path to database file
            batch_size: Number of posts to process in each batch
            timezone: Timezone for scheduling
        """
        self.db = Database(db_path)
        self.batch_size = batch_size
        self.timezone = pytz.timezone(timezone)
        self.running = False
        self.thread = None
        self.retry_delays = {1: 60, 2: 120, 3: 300}  # minutes per attempt
        self.rate_limits = {
            "x": {"posts_per_hour": 50},
            "linkedin": {"posts_per_hour": 30},
            "instagram": {"posts_per_hour": 20}
        }

    def start(self):
        """Start the scheduler daemon."""
        if self.running:
            console.print("[yellow]⚠ Scheduler is already running[/yellow]")
            return

        console.print("[green]✓ Starting scheduler daemon[/green]")
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the scheduler daemon."""
        console.print("[yellow]⚠ Stopping scheduler daemon...[/yellow]")
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
            console.print("[green]✓ Scheduler stopped[/green]")

    def _run_scheduler_loop(self):
        """Main scheduler loop."""
        while self.running:
            try:
                # Process scheduled posts
                self._process_scheduled_posts()

                # Process failed posts with retry
                self._process_retry_queue()

                # Wait before next iteration (check every minute)
                time.sleep(60)
            except Exception as e:
                console.print(f"[red]✗ Scheduler error: {e}[/red]")
                time.sleep(60)

    def _process_scheduled_posts(self):
        """Process all scheduled posts."""
        posts = self.db.get_pending_posts()

        # Group by scheduled time (within the same minute)
        time_groups = {}
        for post in posts:
            if not post.scheduled_for:
                continue

            # Truncate to minute for grouping
            dt = datetime.fromisoformat(post.scheduled_for)
            dt_key = dt.replace(second=0, microsecond=0)
            if dt_key not in time_groups:
                time_groups[dt_key] = []
            time_groups[dt_key].append(post)

        # Process each time group
        for dt, posts_in_group in time_groups.items():
            # Check if it's time to post
            now = datetime.now(self.timezone)

            if dt <= now:
                # Post immediately
                for post in posts_in_group:
                    self._post_single(post)
            else:
                # Wait until next scheduled time
                return

    def _post_single(self, post: Post) -> bool:
        """
        Post a single post to the platform.

        Args:
            post: Post object

        Returns:
            True if successful, False otherwise
        """
        platform = post.platform

        # Check rate limit
        if self._is_rate_limited(platform):
            console.print(
                f"[yellow]⚠ Rate limited for {platform}, "
                f"postponing post #{post.id}[/yellow]"
            )
            return False

        try:
            console.print(f"[cyan]Posting to {platform}: {post.content[:50]}...[/cyan]")

            # TODO: Implement actual platform posting
            # This would call the platform client to post
            # platform_client.post(post.content, post.media_paths)
            # platform_post_id = platform_response.id

            # For now, simulate successful post
            platform_post_id = f"post_{post.id}_{int(datetime.now().timestamp())}"

            # Update post status
            self.db.update_post_status(
                post.id,
                "posted",
                platform_post_id=platform_post_id
            )

            # Update database
            self.db.conn.commit()

            console.print(f"[green]✓ Post #{post.id} posted to {platform}[/green]")
            return True

        except Exception as e:
            console.print(f"[red]✗ Failed to post post #{post.id}: {e}[/red]")

            # Update post status to failed
            self.db.update_post_status(post.id, "failed")
            self.db.conn.commit()

            return False

    def _process_retry_queue(self):
        """Process failed posts for retry."""
        # Get posts that failed (simulated - in real implementation, check for retry_count)
        # TODO: Implement retry queue logic
        pass

    def _is_rate_limited(self, platform: str) -> bool:
        """Check if platform is rate limited.

        Args:
            platform: Platform name

        Returns:
            True if rate limited, False otherwise
        """
        # Get recent posts for this platform (last hour)
        cutoff = datetime.now(self.timezone) - timedelta(hours=1)

        # Count posts in the last hour
        # TODO: Implement actual rate limit checking
        # For now, return False (no rate limit)
        return False

    def schedule_post(
        self,
        post_id: int,
        dt: datetime
    ) -> bool:
        """Schedule a post.

        Args:
            post_id: Post ID
            dt: Scheduled datetime

        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert to timezone-aware datetime
            if dt.tzinfo is None:
                dt = self.timezone.localize(dt)

            # Schedule post
            self.db.schedule_post(post_id, dt)
            console.print(
                f"[green]✓ Post #{post_id} scheduled for "
                f"{dt.strftime('%Y-%m-%d %H:%M')}[/green]"
            )
            return True
        except Exception as e:
            console.print(f"[red]✗ Failed to schedule post {post_id}: {e}[/red]")
            return False

    def list_scheduled(self, platform: str = None) -> List[Post]:
        """List all scheduled posts.

        Args:
            platform: Platform filter (optional)

        Returns:
            List of scheduled Post objects
        """
        posts = self.db.get_pending_posts()
        scheduled = [p for p in posts if p.scheduled_for and p.status == "scheduled"]

        if platform:
            scheduled = [p for p in scheduled if p.platform == platform]

        return scheduled

    def cancel_scheduled(self, post_id: int) -> bool:
        """Cancel a scheduled post.

        Args:
            post_id: Post ID

        Returns:
            True if successful, False otherwise
        """
        try:
            # Reset scheduled_for and status to pending
            self.db.schedule_post(post_id, None)
            console.print(f"[green]✓ Scheduled post #{post_id} cancelled[/green]")
            return True
        except Exception as e:
            console.print(f"[red]✗ Failed to cancel post {post_id}: {e}[/red]")
            return False

    def update_schedule(self, post_id: int, dt: datetime) -> bool:
        """Update scheduled time for a post.

        Args:
            post_id: Post ID
            dt: New scheduled datetime

        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert to timezone-aware datetime
            if dt.tzinfo is None:
                dt = self.timezone.localize(dt)

            # Update schedule
            self.db.schedule_post(post_id, dt)
            console.print(
                f"[green]✓ Post #{post_id} rescheduled for "
                f"{dt.strftime('%Y-%m-%d %H:%M')}[/green]"
            )
            return True
        except Exception as e:
            console.print(f"[red]✗ Failed to update schedule {post_id}: {e}[/red]")
            return False

    def get_schedule_status(self) -> Dict[str, Any]:
        """Get scheduler status.

        Returns:
            Dictionary with scheduler status
        """
        pending_posts = self.db.get_pending_posts()
        scheduled_posts = [p for p in pending_posts if p.status == "scheduled"]

        return {
            "running": self.running,
            "pending_count": len(pending_posts),
            "scheduled_count": len(scheduled_posts),
            "batch_size": self.batch_size,
            "timezone": str(self.timezone)
        }

    def process_batch(self, platform: str = None, count: int = 5):
        """Manually trigger batch processing.

        Args:
            platform: Platform filter (optional)
            count: Number of posts to process
        """
        console.print(f"[cyan]Processing batch of {count} posts")
        if platform:
            console.print(f"for {platform}")

        posts = self.db.get_pending_posts()
        if platform:
            posts = [p for p in posts if p.platform == platform]

        # Process first N posts
        count = min(count, len(posts))
        for i in range(count):
            self._post_single(posts[i])
            # Add small delay between posts
            time.sleep(0.5)

        console.print(f"[green]✓ Batch processing complete[/green]")
