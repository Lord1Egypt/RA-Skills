#!/usr/bin/env python3
"""
Skill Scaffolder

Creates new Agent Skills from templates with proper structure.

Usage:
    python scaffold_skill.py my-skill
    python scaffold_skill.py my-skill --template with-scripts
    python scaffold_skill.py my-skill --description "My awesome skill"
    python scaffold_skill.py --interactive
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Optional


TEMPLATES = ["basic", "with-scripts", "with-assets"]
DEFAULT_LICENSE = "MIT"
DEFAULT_AUTHOR = ""


def validate_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate skill name according to spec.

    Rules:
    - 1-64 characters
    - lowercase alphanumeric and hyphens only
    - must start with a letter
    - cannot end with hyphen
    - no consecutive hyphens
    """
    if not name or len(name) == 0:
        return False, "Name is required"

    if len(name) > 64:
        return False, f"Name exceeds 64 characters (got {len(name)})"

    if not re.match(r'^[a-z0-9-]+$', name):
        return False, "Name must be lowercase alphanumeric and hyphens only"

    if not re.match(r'^[a-z]', name):
        return False, "Name must start with a letter"

    if name.endswith("-"):
        return False, "Name cannot end with a hyphen"

    if "--" in name:
        return False, "Name cannot contain consecutive hyphens"

    return True, None


def generate_skill_md(
    name: str,
    description: str = "",
    version: str = "1.0.0",
    license_id: str = DEFAULT_LICENSE,
    author: str = DEFAULT_AUTHOR,
    tags: list[str] = None
) -> str:
    """Generate SKILL.md content with proper frontmatter."""
    if not description:
        description = f"A skill for {name.replace('-', ' ')}"

    if tags is None:
        tags = []

    # Build frontmatter
    frontmatter_lines = [
        "---",
        f"name: {name}",
        f"description: {description}",
        f"version: {version}",
        f"license: {license_id}",
    ]

    if author:
        frontmatter_lines.append(f'author: "{author}"')

    if tags:
        frontmatter_lines.append("tags:")
        for tag in tags:
            frontmatter_lines.append(f"  - {tag}")

    frontmatter_lines.append("---")

    frontmatter = "\n".join(frontmatter_lines)

    # Instructions template
    instructions = dedent(f'''
        ## Instructions

        Describe what this skill does and how an agent should use it.

        ### When to Use

        - Describe scenarios when this skill is helpful
        - List specific use cases

        ### How to Use

        Explain how to invoke the skill:

        ```
        Example prompt that triggers this skill
        ```

        ## Examples

        **Example 1:**
        ```
        User: [example user request]
        Agent: [example agent response]
        ```

        ## Limitations

        - List any limitations or constraints
        - Note required dependencies

        ## Dependencies

        - Python 3.9+ (if applicable)
        - List any external dependencies
    ''').strip()

    return f"{frontmatter}\n\n{instructions}\n"


def generate_readme(name: str, description: str = "") -> str:
    """Generate README.md content."""
    if not description:
        description = f"A skill for {name.replace('-', ' ')}"

    return dedent(f'''
        # {name}

        {description}

        ## Installation

        This skill can be installed in any agent harness that supports the Agent Skills Specification.

        ## Usage

        See `SKILL.md` for instructions.

        ## License

        MIT
    ''').strip() + "\n"


def generate_main_py(name: str) -> str:
    """Generate a template main.py script."""
    return dedent(f'''
        #!/usr/bin/env python3
        """
        {name}

        Main script for the {name} skill.
        """

        import argparse
        import sys
        from pathlib import Path


        def main():
            parser = argparse.ArgumentParser(
                description="{name.replace('-', ' ').title()}"
            )
            parser.add_argument(
                "input",
                type=str,
                help="Input to process"
            )
            parser.add_argument(
                "--verbose", "-v",
                action="store_true",
                help="Verbose output"
            )

            args = parser.parse_args()

            # TODO: Implement your skill logic here
            print(f"Processing: {{args.input}}")

            return 0


        if __name__ == "__main__":
            sys.exit(main())
    ''').strip() + "\n"


def create_skill(
    output_dir: Path,
    name: str,
    template: str = "basic",
    description: str = "",
    version: str = "1.0.0",
    license_id: str = DEFAULT_LICENSE,
    author: str = DEFAULT_AUTHOR,
    tags: list[str] = None
) -> list[str]:
    """
    Create a skill directory with the specified template.

    Returns list of created files.
    """
    skill_dir = output_dir / name
    created_files = []

    # Check if directory exists
    if skill_dir.exists():
        raise FileExistsError(f"Directory already exists: {skill_dir}")

    # Create base directory
    skill_dir.mkdir(parents=True)

    # Create SKILL.md
    skill_md_path = skill_dir / "SKILL.md"
    skill_md_content = generate_skill_md(
        name=name,
        description=description,
        version=version,
        license_id=license_id,
        author=author,
        tags=tags
    )
    skill_md_path.write_text(skill_md_content)
    created_files.append(str(skill_md_path.relative_to(output_dir)))

    # Create README.md
    readme_path = skill_dir / "README.md"
    readme_content = generate_readme(name, description)
    readme_path.write_text(readme_content)
    created_files.append(str(readme_path.relative_to(output_dir)))

    # Add scripts directory for with-scripts and with-assets templates
    if template in ["with-scripts", "with-assets"]:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir()

        main_py_path = scripts_dir / "main.py"
        main_py_content = generate_main_py(name)
        main_py_path.write_text(main_py_content)
        main_py_path.chmod(0o755)  # Make executable
        created_files.append(str(main_py_path.relative_to(output_dir)))

    # Add assets directory for with-assets template
    if template == "with-assets":
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir()

        gitkeep_path = assets_dir / ".gitkeep"
        gitkeep_path.write_text("")
        created_files.append(str(gitkeep_path.relative_to(output_dir)))

    return created_files


def interactive_mode(output_dir: Path) -> int:
    """Run in interactive mode, prompting for all inputs."""
    print("\n=== Skill Scaffolder ===\n")

    # Get name
    while True:
        try:
            name = input("Skill name: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return 1

        valid, error = validate_name(name)
        if valid:
            break
        print(f"  Invalid: {error}")

    # Get description
    description = input("Description (optional): ").strip()

    # Get template
    print(f"Templates: {', '.join(TEMPLATES)}")
    template_input = input(f"Template [{TEMPLATES[0]}]: ").strip().lower()
    template = template_input if template_input in TEMPLATES else TEMPLATES[0]

    # Get license
    license_id = input(f"License [{DEFAULT_LICENSE}]: ").strip() or DEFAULT_LICENSE

    # Get author
    author = input("Author (optional): ").strip()

    # Get tags
    tags_input = input("Tags (comma-separated, optional): ").strip()
    tags = [t.strip().lower() for t in tags_input.split(",") if t.strip()] if tags_input else []

    print()

    try:
        created = create_skill(
            output_dir=output_dir,
            name=name,
            template=template,
            description=description,
            license_id=license_id,
            author=author,
            tags=tags
        )

        print(f"Created skill: {name}/")
        for f in created:
            print(f"  {f}")
        print()
        print("Next steps:")
        print("  1. Edit SKILL.md with your skill's instructions")
        print("  2. Add any supporting files")
        print("  3. Run skill-validator to check compliance")
        print()
        return 0

    except FileExistsError as e:
        print(f"Error: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Create new Agent Skills from templates"
    )
    parser.add_argument(
        "name",
        type=str,
        nargs="?",
        help="Name of the skill to create"
    )
    parser.add_argument(
        "--template", "-t",
        type=str,
        choices=TEMPLATES,
        default="basic",
        help=f"Template to use (default: basic)"
    )
    parser.add_argument(
        "--description", "-d",
        type=str,
        default="",
        help="Skill description"
    )
    parser.add_argument(
        "--version", "-v",
        type=str,
        default="1.0.0",
        help="Skill version (default: 1.0.0)"
    )
    parser.add_argument(
        "--license", "-l",
        type=str,
        default=DEFAULT_LICENSE,
        help=f"License (default: {DEFAULT_LICENSE})"
    )
    parser.add_argument(
        "--author", "-a",
        type=str,
        default="",
        help="Author name"
    )
    parser.add_argument(
        "--tags",
        type=str,
        default="",
        help="Comma-separated tags"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path.cwd(),
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON"
    )

    args = parser.parse_args()

    # Interactive mode
    if args.interactive or not args.name:
        return interactive_mode(args.output)

    # Validate name
    valid, error = validate_name(args.name)
    if not valid:
        if args.json:
            import json
            print(json.dumps({"success": False, "error": error}))
        else:
            print(f"Error: {error}")
        return 1

    # Parse tags
    tags = [t.strip().lower() for t in args.tags.split(",") if t.strip()] if args.tags else []

    try:
        created = create_skill(
            output_dir=args.output,
            name=args.name,
            template=args.template,
            description=args.description,
            version=args.version,
            license_id=args.license,
            author=args.author,
            tags=tags
        )

        if args.json:
            import json
            print(json.dumps({
                "success": True,
                "skill": args.name,
                "template": args.template,
                "files": created
            }, indent=2))
        else:
            print(f"\nCreated skill: {args.name}/")
            for f in created:
                print(f"  {f}")
            print()
            print("Next steps:")
            print("  1. Edit SKILL.md with your skill's instructions")
            print("  2. Add any supporting files")
            print("  3. Run skill-validator to check compliance")
            print()

        return 0

    except FileExistsError as e:
        if args.json:
            import json
            print(json.dumps({"success": False, "error": str(e)}))
        else:
            print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
