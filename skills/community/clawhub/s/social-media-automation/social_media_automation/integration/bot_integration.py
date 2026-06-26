"""Bot integration for Discord and Telegram."""

from typing import Dict, Any, Optional, Callable
from datetime import datetime
from pydantic import BaseModel

from rich.console import Console

from .github_monitor import GitHubMonitor, CommitInfo
from .content_generator import GeneratedContent

console = Console()


class DiscordWebhook(BaseModel):
    """Discord webhook configuration."""

    url: str
    enabled: bool = True
    content_format: str = "markdown"  # plain, markdown


class TelegramBot(BaseModel):
    """Telegram bot configuration."""

    token: str
    chat_id: str
    enabled: bool = True
    parse_mode: str = "HTML"  # MarkdownV2, HTML


class BotIntegration:
    """Manage bot integrations for social media platforms."""

    def __init__(self, discord_config: DiscordWebhook = None, telegram_config: TelegramBot = None):
        """
        Initialize bot integration.

        Args:
            discord_config: Discord webhook configuration
            telegram_config: Telegram bot configuration
        """
        self.discord_config = discord_config
        self.telegram_config = telegram_config
        self.webhooks = {}  # Cache webhook URLs
        self.bots = {}  # Cache bot clients

    def send_discord(self, content: str) -> bool:
        """
        Send content to Discord webhook.

        Args:
            content: Content to send (Markdown)

        Returns:
            True if successful, False otherwise
        """
        if not self.discord_config or not self.discord_config.enabled:
            console.print("[yellow]⚠ Discord webhook not enabled[/yellow]")
            return False

        if not self.discord_config.url:
            console.print("[red]✗ Discord webhook URL not configured[/red]")
            return False

        try:
            import requests
            console.print(f"[cyan]Sending to Discord webhook: {content[:50]}...[/cyan]")

            payload = {
                "username": "Social Media Automation",
                "avatar_url": "https://via.placeholder.com/150",
                "embeds": [
                    {
                        "title": "📱 Social Media Update",
                        "description": content,
                        "color": 5814783,  # Blue
                        "timestamp": datetime.now().isoformat()
                    }
                ]
            }

            response = requests.post(
                self.discord_config.url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 204:
                console.print("[green]✓ Sent to Discord successfully[/green]")
                return True
            else:
                console.print(
                    f"[red]✗ Discord webhook error: {response.status_code}[/red]"
                )
                return False

        except Exception as e:
            console.print(f"[red]✗ Failed to send to Discord: {e}[/red]")
            return False

    def send_telegram(self, content: str, media: Optional[str] = None) -> bool:
        """
        Send content to Telegram bot.

        Args:
            content: Content to send
            media: Optional media file path

        Returns:
            True if successful, False otherwise
        """
        if not self.telegram_config or not self.telegram_config.enabled:
            console.print("[yellow]⚠ Telegram bot not enabled[/yellow]")
            return False

        if not self.telegram_config.token or not self.telegram_config.chat_id:
            console.print("[red]✗ Telegram bot not configured[/red]")
            return False

        try:
            import requests
            console.print(f"[cyan]Sending to Telegram: {content[:50]}...[/cyan]")

            # Prepare payload
            if self.telegram_config.parse_mode == "MarkdownV2":
                text = f"{'{'{'}'}{content}{'{'}'}"}"
            else:
                text = content

            payload = {
                "chat_id": self.telegram_config.chat_id,
                "text": text,
                "parse_mode": self.telegram_config.parse_mode,
                "disable_web_page_preview": True
            }

            # Add media if provided
            if media:
                import os
                if os.path.exists(media):
                    with open(media, 'rb') as f:
                        files = {'document': f}
                        response = requests.post(
                            f"https://api.telegram.org/bot{self.telegram_config.token}/sendDocument",
                            data=payload,
                            files=files
                        )
                else:
                    console.print(f"[yellow]⚠ Media file not found: {media}[/yellow]")
                    response = requests.post(
                        f"https://api.telegram.org/bot{self.telegram_config.token}/sendMessage",
                        json=payload
                    )
            else:
                response = requests.post(
                    f"https://api.telegram.org/bot{self.telegram_config.token}/sendMessage",
                    json=payload
                )

            if response.status_code == 200:
                console.print("[green]✓ Sent to Telegram successfully[/green]")
                return True
            else:
                console.print(
                    f"[red]✗ Telegram bot error: {response.status_code}[/red]"
                )
                return False

        except Exception as e:
            console.print(f"[red]✗ Failed to send to Telegram: {e}[/red]")
            return False

    def send_to_all(self, content: str, platform: str = None, media: Optional[str] = None) -> Dict[str, bool]:
        """
        Send content to all configured platforms.

        Args:
            content: Content to send
            platform: Optional platform filter
            media: Optional media file path

        Returns:
            Dictionary with platform names and success status
        """
        console.print(f"[cyan]Sending to all platforms...[/cyan]")

        results = {}

        # Send to Discord
        discord_success = self.send_discord(content)
        results["discord"] = discord_success

        # Send to Telegram
        telegram_success = self.send_telegram(content, media)
        results["telegram"] = telegram_success

        # Report summary
        console.print("[cyan]Send summary:[/cyan]")
        for platform, success in results.items():
            status = "[green]✓ Success[/green]" if success else "[red]✗ Failed[/red]"
            console.print(f"  {platform}: {status}")

        return results

    def auto_post(self, content: str, generated_content: GeneratedContent) -> bool:
        """
        Automatically post generated content.

        Args:
            content: Content to post
            generated_content: GeneratedContent object with metadata

        Returns:
            True if successful, False otherwise
        """
        console.print(f"[cyan]Auto-posting generated content...[/cyan]")
        console.print(f"  Platform: {generated_content.platform}")
        console.print(f"  Content: {content[:50]}...")

        # Add media if present (for Instagram)
        media = generated_content.media if generated_content.media else None

        # Send to appropriate platform
        if generated_content.platform == "instagram" and media:
            # Instagram requires media, use Telegram for now (webhook)
            return self.send_telegram(content, media)
        elif generated_content.platform == "x":
            # Send to Discord (notification) or Telegram (actual post)
            return self.send_telegram(content)
        elif generated_content.platform == "linkedin":
            return self.send_telegram(content)
        else:
            console.print(f"[yellow]⚠ Auto-posting not configured for {generated_content.platform}[/yellow]")
            return False

    def test_integration(self, platform: str) -> Dict[str, Any]:
        """
        Test bot integration.

        Args:
            platform: Platform to test (discord, telegram)

        Returns:
            Test results
        """
        console.print(f"[cyan]Testing {platform} integration...[/cyan]")

        test_message = "Test message from Social Media Automation"
        results = {
            "platform": platform,
            "timestamp": datetime.now().isoformat()
        }

        if platform == "discord":
            success = self.send_discord(test_message)
            results["success"] = success
            results["message"] = "Discord webhook test"

        elif platform == "telegram":
            success = self.send_telegram(test_message)
            results["success"] = success
            results["message"] = "Telegram bot test"

        else:
            results["success"] = False
            results["message"] = f"Unknown platform: {platform}"

        status = "[green]✓ Test passed[/green]" if success else "[red]✗ Test failed[/red]"
        console.print(f"{status}: {results['message']}")

        return results

    def get_status(self) -> Dict[str, Any]:
        """
        Get bot integration status.

        Returns:
            Dictionary with status information
        """
        console.print("[cyan]Bot Integration Status:[/cyan]")

        status = {
            "discord": {
                "enabled": bool(self.discord_config),
                "configured": bool(self.discord_config and self.discord_config.url)
            },
            "telegram": {
                "enabled": bool(self.telegram_config),
                "configured": bool(self.telegram_config and self.telegram_config.token)
            }
        }

        if status["discord"]["enabled"]:
            console.print("  Discord: [green]enabled[/green]")
            if status["discord"]["configured"]:
                console.print(f"    Webhook: {self.discord_config.url[:30]}...")
        else:
            console.print("    [red]Not configured[/red]")
        else:
            console.print("  Discord: [red]disabled[/red]")

        if status["telegram"]["enabled"]:
            console.print("  Telegram: [green]enabled[/green]")
            if status["telegram"]["configured"]:
                console.print(f"    Bot: {self.telegram_config.chat_id}")
        else:
            console.print("    [red]Not configured[/red]")
        else:
            console.print("  Telegram: [red]disabled[/red]")

        return status
