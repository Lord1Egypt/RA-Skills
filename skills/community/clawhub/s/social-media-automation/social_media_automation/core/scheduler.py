"""
Scheduler for automated posting
"""

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime

from social_media_automation.config import Config
from social_media_automation.storage.database import Database
from social_media_automation.platforms.x.client import TwitterClient
from social_media_automation.utils.logger import setup_logger

logger = setup_logger()


class PostScheduler:
    """Scheduler for automated social media posting"""

    def __init__(self, config: Config | None = None, db: Database | None = None) -> None:
        """Initialize scheduler"""
        self.config = config or Config.load()
        self.db = db or Database()

        # Initialize scheduler
        self.scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Tokyo"))
        self.scheduler.start()

        # Schedule recurring check for scheduled posts
        self.scheduler.add_job(
            self.process_scheduled_posts,
            "interval",
            minutes=1,
            id="check_scheduled_posts",
            replace_existing=True,
        )

        logger.info("Post scheduler initialized")

    def process_scheduled_posts(self) -> None:
        """Process all scheduled posts that are due"""
        try:
            now = datetime.now(pytz.utc)

            # Get all scheduled posts
            scheduled_posts = self.db.get_scheduled_posts(limit=100)

            for post in scheduled_posts:
                scheduled_at = datetime.fromisoformat(post["scheduled_at"])
                scheduled_at = scheduled_at.replace(tzinfo=pytz.utc)

                # Check if post is due
                if scheduled_at <= now:
                    logger.info(f"Processing scheduled post {post['id']}")
                    self._post_scheduled_item(post)

        except Exception as e:
            logger.error(f"Error processing scheduled posts: {e}")

    def _post_scheduled_item(self, post: dict[str, any]) -> None:
        """Post a scheduled item"""
        try:
            platform = post["platform"]
            content = post["content"]
            post_id = post["id"]

            # Post to platform
            if platform == "x" or platform == "twitter":
                client = TwitterClient(self.config)
                result = client.post_tweet(content)

                # Update post status
                self.db.update_post_status(post_id, "posted")

                # Update post_id if needed
                # Note: You might want to add a field to store the actual platform post ID

                logger.info(f"Successfully posted scheduled post {post_id}")
            else:
                logger.warning(f"Unsupported platform: {platform}")
                self.db.update_post_status(post_id, "failed")

        except Exception as e:
            logger.error(f"Failed to post scheduled item {post['id']}: {e}")
            self.db.update_post_status(post["id"], "failed")

    def schedule_post(self, post_id: int, scheduled_at: datetime) -> bool:
        """Schedule a post for a specific time"""
        try:
            # Store scheduled time in database
            # This is handled by the CLI command already
            # The scheduler will pick it up automatically
            logger.info(f"Post {post_id} scheduled for {scheduled_at}")
            return True
        except Exception as e:
            logger.error(f"Failed to schedule post {post_id}: {e}")
            return False

    def schedule_recurring_post(
        self,
        platform: str,
        content: str,
        cron_expression: str,
        timezone: str = "Asia/Tokyo",
    ) -> str:
        """Schedule a recurring post using cron expression"""
        try:
            # Parse cron expression
            parts = cron_expression.split()
            if len(parts) != 5:
                raise ValueError("Invalid cron expression. Expected format: 'minute hour day month weekday'")

            minute, hour, day, month, weekday = parts

            # Create job
            job_id = f"recurring_{datetime.now().strftime('%Y%m%d%H%M%S')}"

            self.scheduler.add_job(
                self._post_recurring,
                trigger=CronTrigger(
                    minute=minute,
                    hour=hour,
                    day=day,
                    month=month,
                    day_of_week=weekday,
                    timezone=timezone,
                ),
                args=[platform, content],
                id=job_id,
                replace_existing=True,
            )

            logger.info(f"Scheduled recurring post {job_id} with cron: {cron_expression}")
            return job_id
        except Exception as e:
            logger.error(f"Failed to schedule recurring post: {e}")
            raise

    def _post_recurring(self, platform: str, content: str) -> None:
        """Post a recurring item"""
        try:
            if platform == "x" or platform == "twitter":
                client = TwitterClient(self.config)
                result = client.post_tweet(content)

                # Save to database
                self.db.save_post(
                    platform=platform,
                    content=content,
                    post_id=result.data.id,
                    status="posted",
                )

                logger.info(f"Successfully posted recurring content")
            else:
                logger.warning(f"Unsupported platform: {platform}")

        except Exception as e:
            logger.error(f"Failed to post recurring content: {e}")

    def remove_scheduled_post(self, post_id: int) -> bool:
        """Remove a scheduled post"""
        try:
            # Update status to cancelled
            success = self.db.update_post_status(post_id, "cancelled")
            logger.info(f"Cancelled scheduled post {post_id}")
            return success
        except Exception as e:
            logger.error(f"Failed to remove scheduled post {post_id}: {e}")
            return False

    def remove_recurring_post(self, job_id: str) -> bool:
        """Remove a recurring post job"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Removed recurring post job {job_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove recurring post {job_id}: {e}")
            return False

    def list_scheduled_posts(self, limit: int = 20) -> list[dict[str, any]]:
        """List all scheduled posts"""
        return self.db.get_scheduled_posts(limit)

    def list_recurring_jobs(self) -> list[dict[str, any]]:
        """List all recurring jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            if job.id.startswith("recurring_"):
                jobs.append(
                    {
                        "id": job.id,
                        "trigger": str(job.trigger),
                        "next_run": str(job.next_run_time),
                    }
                )
        return jobs

    def shutdown(self) -> None:
        """Shutdown the scheduler"""
        logger.info("Shutting down scheduler")
        self.scheduler.shutdown()
