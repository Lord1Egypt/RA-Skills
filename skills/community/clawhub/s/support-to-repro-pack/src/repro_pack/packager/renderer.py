"""Template renderer using Jinja2."""

from __future__ import annotations

import os

from jinja2 import Environment, FileSystemLoader, select_autoescape


def create_jinja_env(template_dir: str) -> Environment:
    """Create a Jinja2 environment for rendering templates."""
    return Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape([]),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


def render_template(template_dir: str, template_name: str, context: dict) -> str:
    """Render a single template with the given context."""
    env = create_jinja_env(template_dir)
    template = env.get_template(template_name)
    return template.render(**context)


def get_default_template_dir() -> str:
    """Get the path to the built-in templates directory."""
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        ".claude",
        "skills",
        "support-to-repro-pack",
        "templates",
    )
