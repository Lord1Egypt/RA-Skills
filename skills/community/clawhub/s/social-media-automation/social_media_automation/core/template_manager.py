"""
Template manager for social media automation
"""

from typing import Any

from rich.console import Console
from rich.table import Table

from social_media_automation.storage.template_store import TemplateStore

console = Console()


class TemplateManager:
    """Manager for content templates"""

    def __init__(self, store: TemplateStore | None = None) -> None:
        """Initialize template manager"""
        self.store = store or TemplateStore()

    def create_template(
        self,
        name: str,
        content: str,
        platform: str,
        variables: list[str] | None = None,
    ) -> int:
        """Create a new template"""
        try:
            template_id = self.store.save_template(name, content, platform, variables)
            console.print(f"[green]✓ Template created[/green]")
            console.print(f"  ID: {template_id}")
            console.print(f"  Name: {name}")
            console.print(f"  Platform: {platform}")

            return template_id
        except Exception as e:
            console.print(f"[red]✗ Failed to create template: {e}[/red]")
            raise

    def list_templates(
        self,
        platform: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """List all templates"""
        return self.store.list_templates(platform, limit)

    def get_template(self, template_id: int) -> dict[str, Any] | None:
        """Get a template by ID"""
        return self.store.get_template(template_id)

    def get_template_by_name(self, name: str) -> dict[str, Any] | None:
        """Get a template by name"""
        return self.store.get_template_by_name(name)

    def update_template(
        self,
        template_id: int,
        name: str | None = None,
        content: str | None = None,
        platform: str | None = None,
        variables: list[str] | None = None,
    ) -> bool:
        """Update a template"""
        try:
            success = self.store.update_template(template_id, name, content, platform, variables)

            if success:
                console.print(f"[green]✓ Template updated[/green]")
            else:
                console.print(f"[red]✗ Template not found[/red]")

            return success
        except Exception as e:
            console.print(f"[red]✗ Failed to update template: {e}[/red]")
            raise

    def delete_template(self, template_id: int) -> bool:
        """Delete a template"""
        try:
            success = self.store.delete_template(template_id)

            if success:
                console.print(f"[green]✓ Template deleted[/green]")
            else:
                console.print(f"[red]✗ Template not found[/red]")

            return success
        except Exception as e:
            console.print(f"[red]✗ Failed to delete template: {e}[/red]")
            raise

    def use_template(
        self,
        template_id: int | str,
        variables: dict[str, str],
    ) -> str:
        """Use a template and apply variables"""
        try:
            # Support both ID and name
            if isinstance(template_id, int) or template_id.isdigit():
                template = self.store.get_template(int(template_id))
            else:
                template = self.store.get_template_by_name(template_id)

            if not template:
                raise ValueError(f"Template not found: {template_id}")

            # Check if all variables are provided
            required_vars = set(template["variables"])
            provided_vars = set(variables.keys())
            missing_vars = required_vars - provided_vars

            if missing_vars:
                console.print(f"[yellow]Missing variables: {', '.join(missing_vars)}[/yellow]")
                console.print(f"[yellow]Required variables: {', '.join(template['variables'])}[/yellow]")
                raise ValueError("Missing required variables")

            # Apply variables
            content = self.store.apply_template(template["id"], variables)

            console.print(f"[green]✓ Template applied[/green]")
            console.print(f"  Name: {template['name']}")
            console.print(f"  Platform: {template['platform']}")
            console.print(f"  Content length: {len(content)} characters")

            return content
        except Exception as e:
            console.print(f"[red]✗ Failed to use template: {e}[/red]")
            raise
