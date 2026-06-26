#!/usr/bin/env python3
"""
Documentation Generator

Generates documentation files from marketplace data using Jinja2 templates.
"""

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse

# Try to use real Jinja2 if available, otherwise use SimpleTemplate fallback
try:
    from jinja2 import Template as Jinja2Template
    USE_JINJA2 = True
except ImportError:
    USE_JINJA2 = False


class SimpleTemplate:
    """Minimal Jinja2-like template engine"""

    def __init__(self, template_str: str):
        self.template = template_str

    def apply_filter(self, value: Any, filter_name: str) -> Any:
        """Apply a filter to a value"""
        if filter_name == 'title':
            return str(value).replace('-', ' ').replace('_', ' ').title()
        elif filter_name == 'length':
            return len(value) if hasattr(value, '__len__') else 0
        elif filter_name.startswith('join'):
            # Extract separator from filter (e.g., "join(', ')")
            match = re.search(r"join\(['\"]([^'\"]*)['\"]\)", filter_name)
            if match and isinstance(value, list):
                separator = match.group(1)
                return separator.join(str(v) for v in value)
            return str(value)
        return value

    def resolve_value(self, expr: str, context: Dict[str, Any]) -> Any:
        """Resolve a variable expression with optional filters"""
        # Split expression and filters
        parts = expr.strip().split('|')
        var_expr = parts[0].strip()
        filters = [f.strip() for f in parts[1:]]

        # Resolve the base variable
        value = context
        for key in var_expr.split('.'):
            key = key.strip()
            if isinstance(value, dict):
                value = value.get(key, '')
            elif hasattr(value, key):
                value = getattr(value, key)
            else:
                value = ''
                break

        # Apply filters
        for filter_name in filters:
            value = self.apply_filter(value, filter_name)

        return value

    def render(self, context: Dict[str, Any]) -> str:
        """Render template with context"""
        result = self.template

        # Handle nested loops with .items(): {% for key, value in dict.items() %}...{% endfor %}
        items_pattern = r'{%\s*for\s+(\w+)\s*,\s*(\w+)\s+in\s+([\w.]+)\.items\(\)\s*%}(.*?){%\s*endfor\s*%}'

        def replace_items_loop(match):
            key_var = match.group(1)
            value_var = match.group(2)
            dict_name = match.group(3)
            loop_body = match.group(4)

            dict_obj = self.resolve_value(dict_name, context)
            if not isinstance(dict_obj, dict):
                return ""

            output = []
            for key, value in dict_obj.items():
                loop_context = context.copy()
                loop_context[key_var] = key
                loop_context[value_var] = value

                # Recursively render the loop body
                template = SimpleTemplate(loop_body)
                body_result = template.render(loop_context)
                output.append(body_result)

            return "".join(output)

        result = re.sub(items_pattern, replace_items_loop, result, flags=re.DOTALL)

        # Handle loops with .keys(): {% for key in dict.keys() %}...{% endfor %}
        keys_pattern = r'{%\s*for\s+(\w+)\s+in\s+([\w.]+)\.keys\(\)\s*%}(.*?){%\s*endfor\s*%}'

        def replace_keys_loop(match):
            var_name = match.group(1)
            dict_name = match.group(2)
            loop_body = match.group(3)

            dict_obj = self.resolve_value(dict_name, context)
            if not isinstance(dict_obj, dict):
                return ""

            output = []
            for key in dict_obj.keys():
                loop_context = context.copy()
                loop_context[var_name] = key

                # Recursively render the loop body
                template = SimpleTemplate(loop_body)
                body_result = template.render(loop_context)
                output.append(body_result)

            return "".join(output)

        result = re.sub(keys_pattern, replace_keys_loop, result, flags=re.DOTALL)

        # Handle regular loops: {% for item in items %}...{% endfor %}
        for_pattern = r'{%\s*for\s+(\w+)\s+in\s+([\w.]+)\s*%}(.*?){%\s*endfor\s*%}'

        def replace_for(match):
            var_name = match.group(1)
            list_name = match.group(2)
            loop_body = match.group(3)

            items = self.resolve_value(list_name, context)
            if not isinstance(items, (list, dict)):
                return ""

            # Handle both lists and dict values
            if isinstance(items, dict):
                items = list(items.values())

            output = []
            for item in items:
                loop_context = context.copy()
                loop_context[var_name] = item

                # If item is a dict, also add its keys directly to context for easier access
                if isinstance(item, dict):
                    for key, value in item.items():
                        loop_context[f"{var_name}.{key}"] = value

                # Recursively render the loop body
                template = SimpleTemplate(loop_body)
                body_result = template.render(loop_context)
                output.append(body_result)

            return "".join(output)

        result = re.sub(for_pattern, replace_for, result, flags=re.DOTALL)

        # Handle conditionals with comparison: {% if var1 == var2 %}...{% endif %}
        if_compare_pattern = r'{%\s*if\s+([\w.]+)\s*==\s*([\w.]+)\s*%}(.*?){%\s*endif\s*%}'

        def replace_if_compare(match):
            left_expr = match.group(1)
            right_expr = match.group(2)
            body = match.group(3)

            left_val = self.resolve_value(left_expr, context)
            right_val = self.resolve_value(right_expr, context)

            if left_val == right_val:
                template = SimpleTemplate(body)
                return template.render(context)
            return ""

        result = re.sub(if_compare_pattern, replace_if_compare, result, flags=re.DOTALL)

        # Handle conditionals with else: {% if condition %}...{% else %}...{% endif %}
        if_else_pattern = r'{%\s*if\s+([\w.]+)\s*%}(.*?){%\s*else\s*%}(.*?){%\s*endif\s*%}'

        def replace_if_else(match):
            condition = match.group(1)
            true_body = match.group(2)
            false_body = match.group(3)

            cond_val = self.resolve_value(condition, context)

            if cond_val:
                template = SimpleTemplate(true_body)
                return template.render(context)
            else:
                template = SimpleTemplate(false_body)
                return template.render(context)

        result = re.sub(if_else_pattern, replace_if_else, result, flags=re.DOTALL)

        # Handle simple conditionals: {% if condition %}...{% endif %}
        if_pattern = r'{%\s*if\s+([\w.]+)\s*%}(.*?){%\s*endif\s*%}'

        def replace_if(match):
            condition = match.group(1)
            body = match.group(2)

            cond_val = self.resolve_value(condition, context)

            if cond_val:
                template = SimpleTemplate(body)
                return template.render(context)
            return ""

        result = re.sub(if_pattern, replace_if, result, flags=re.DOTALL)

        # Replace variables with filters: {{ variable|filter }}
        var_pattern = r'{{\s*([\w.|()\'",\s]+)\s*}}'

        def replace_var(match):
            expr = match.group(1)
            value = self.resolve_value(expr, context)
            return str(value) if value is not None else ''

        result = re.sub(var_pattern, replace_var, result)

        # Clean up any remaining template syntax
        result = re.sub(r'{%.*?%}', '', result)
        result = re.sub(r'{{.*?}}', '', result)

        return result


class DocGenerator:
    """Generates documentation from marketplace data"""

    def __init__(
        self,
        marketplace_path: str = ".claude-plugin/marketplace.json",
        templates_dir: str = "plugins/claude-plugin/skills/documentation-update/assets",
        output_dir: str = "docs",
    ):
        self.marketplace_path = Path(marketplace_path)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.marketplace_data: Dict[str, Any] = {}

    def load_marketplace(self) -> None:
        """Load marketplace.json"""
        if not self.marketplace_path.exists():
            raise FileNotFoundError(f"Marketplace not found: {self.marketplace_path}")

        with open(self.marketplace_path, 'r') as f:
            self.marketplace_data = json.load(f)

    def extract_frontmatter(self, file_path: Path) -> Dict[str, str]:
        """Extract YAML frontmatter from a markdown file"""
        if not file_path.exists():
            return {}

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Match frontmatter between --- delimiters
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not match:
                return {}

            frontmatter_text = match.group(1)
            frontmatter = {}

            # Simple YAML parsing (key: value)
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')

            return frontmatter

        except Exception as e:
            print(f"Warning: Could not parse frontmatter in {file_path}: {e}")
            return {}

    def build_context(self) -> Dict[str, Any]:
        """Build template context from marketplace data"""
        context = {
            "marketplace": self.marketplace_data,
            "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "plugins_by_category": {},
            "all_agents": [],
            "all_skills": [],
            "all_commands": [],
            "stats": {
                "total_plugins": 0,
                "total_agents": 0,
                "total_commands": 0,
                "total_skills": 0,
            },
        }

        if "plugins" not in self.marketplace_data:
            return context

        plugins = self.marketplace_data["plugins"]
        context["stats"]["total_plugins"] = len(plugins)

        # Organize plugins by category
        for plugin in plugins:
            category = plugin.get("category", "general")
            if category not in context["plugins_by_category"]:
                context["plugins_by_category"][category] = []
            context["plugins_by_category"][category].append(plugin)

            plugin_name = plugin.get("name", "")
            plugin_dir = Path(f"plugins/{plugin_name}")

            # Extract agent information
            if "agents" in plugin:
                for agent_path in plugin["agents"]:
                    agent_file = agent_path.replace("./agents/", "")
                    full_path = plugin_dir / agent_path.lstrip('./')
                    frontmatter = self.extract_frontmatter(full_path)

                    context["all_agents"].append({
                        "plugin": plugin_name,
                        "name": frontmatter.get("name", agent_file.replace(".md", "")),
                        "file": agent_file,
                        "description": frontmatter.get("description", ""),
                        "model": frontmatter.get("model", ""),
                    })

                context["stats"]["total_agents"] += len(plugin["agents"])

            # Extract command information
            if "commands" in plugin:
                for cmd_path in plugin["commands"]:
                    cmd_file = cmd_path.replace("./commands/", "")
                    full_path = plugin_dir / cmd_path.lstrip('./')
                    frontmatter = self.extract_frontmatter(full_path)

                    context["all_commands"].append({
                        "plugin": plugin_name,
                        "name": frontmatter.get("name", cmd_file.replace(".md", "")),
                        "file": cmd_file,
                        "description": frontmatter.get("description", ""),
                    })

                context["stats"]["total_commands"] += len(plugin["commands"])

            # Extract skill information
            if "skills" in plugin:
                for skill_path in plugin["skills"]:
                    skill_name = skill_path.replace("./skills/", "")
                    full_path = plugin_dir / skill_path.lstrip('./') / "SKILL.md"
                    frontmatter = self.extract_frontmatter(full_path)

                    context["all_skills"].append({
                        "plugin": plugin_name,
                        "name": frontmatter.get("name", skill_name),
                        "path": skill_name,
                        "description": frontmatter.get("description", ""),
                    })

                context["stats"]["total_skills"] += len(plugin["skills"])

        return context

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with context"""
        template_path = self.templates_dir / f"{template_name}.md.j2"

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(template_path, 'r') as f:
            template_content = f.read()

        if USE_JINJA2:
            # Use real Jinja2 for full compatibility
            template = Jinja2Template(template_content)
            return template.render(**context)
        else:
            # Fallback to SimpleTemplate
            template = SimpleTemplate(template_content)
            return template.render(context)

    def generate_all(self, dry_run: bool = False, specific_file: Optional[str] = None) -> None:
        """Generate all documentation files"""
        self.load_marketplace()
        context = self.build_context()

        docs_to_generate = {
            "agents": "agents.md",
            "agent-skills": "agent-skills.md",
            "plugins": "plugins.md",
            "usage": "usage.md",
        }

        if specific_file:
            if specific_file not in docs_to_generate:
                raise ValueError(f"Unknown documentation file: {specific_file}")
            docs_to_generate = {specific_file: docs_to_generate[specific_file]}

        for template_name, output_file in docs_to_generate.items():
            try:
                print(f"Generating {output_file}...")
                content = self.render_template(template_name, context)

                if dry_run:
                    print(f"\n--- {output_file} ---")
                    print(content[:500] + "..." if len(content) > 500 else content)
                    print()
                else:
                    output_path = self.output_dir / output_file
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    with open(output_path, 'w') as f:
                        f.write(content)

                    print(f"✓ Generated {output_path}")

            except Exception as e:
                print(f"❌ Error generating {output_file}: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Generate documentation from marketplace")
    parser.add_argument(
        "--marketplace",
        default=".claude-plugin/marketplace.json",
        help="Path to marketplace.json",
    )
    parser.add_argument(
        "--templates",
        default="plugins/claude-plugin/skills/documentation-update/assets",
        help="Path to templates directory",
    )
    parser.add_argument(
        "--output",
        default="docs",
        help="Output directory for documentation",
    )
    parser.add_argument(
        "--file",
        choices=["agents", "agent-skills", "plugins", "usage"],
        help="Generate specific file only",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show output without writing files",
    )

    args = parser.parse_args()

    try:
        generator = DocGenerator(
            marketplace_path=args.marketplace,
            templates_dir=args.templates,
            output_dir=args.output,
        )

        generator.generate_all(dry_run=args.dry_run, specific_file=args.file)

        if not args.dry_run:
            print("\n✓ Documentation generation complete")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
