#!/usr/bin/env python3
"""
Technical Spec Generator - Automatically generate technical specification templates

Usage:
  python generate_spec.py --interactive
  python generate_spec.py --prd <prd_file> --output <output_file>
  python generate_spec.py --template
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Feature:
    requirement: str
    page: str
    changes: str


@dataclass
class SpecData:
    project_name: str
    version: str
    author: str
    date: str
    background: str
    goal: str
    business_value: str
    features: List[Feature]
    frontend_stack: str
    backend_stack: str
    database: str


class TechSpecGenerator:
    def __init__(self):
        self.template_dir = Path(__file__).parent.parent / 'resources'
        self.template = self._load_template()

    def _load_template(self) -> str:
        template_file = self.template_dir / 'spec_template.md'
        return template_file.read_text(encoding='utf-8')

    def generate_interactive(self) -> str:
        print('=' * 60)
        print('Technical Specification Generator - Interactive Mode')
        print('=' * 60)
        print()

        spec_data = SpecData(
            project_name=self._input('Project name'),
            version=self._input('Version', 'V1.0'),
            author=self._input('Author'),
            date=datetime.now().strftime('%Y-%m-%d'),
            background=self._input_multiline('Business background/Problem'),
            goal=self._input_multiline('Project goals'),
            business_value=self._input_multiline('Business value'),
            features=self._input_features(),
            frontend_stack=self._input('Frontend stack'),
            backend_stack=self._input('Backend stack'),
            database=self._input('Database'),
        )

        return self._render(spec_data)

    def generate_from_prd(self, prd_file: str) -> str:
        prd_content = Path(prd_file).read_text(encoding='utf-8')

        # Return guidance to analyze PRD manually
        return f"""# Please manually analyze the PRD and fill in the following content

## Requirements Overview
### Background/Goals
Extract business background and project goals from the PRD

### Business Value
Describe the business value

## Requirements Analysis
Break down requirements using the Trifecta structure:
1. Feature Breakdown
2. Use Case Analysis
3. Page Operation Details

---

**PRD Content Preview:**
{prd_content[:500]}...
"""

    def _input(self, prompt: str, default: str = '') -> str:
        full_prompt = f'{prompt} [{default}]: ' if default else f'{prompt}: '
        value = input(full_prompt).strip()
        return value or default

    def _input_multiline(self, prompt: str) -> str:
        print(f'{prompt} (enter empty line to finish):')
        lines = []

        while True:
            line = input('> ').strip()
            if not line:
                break
            lines.append(line)

        return '\n'.join(lines)

    def _input_features(self) -> List[Feature]:
        print()
        print('Feature Breakdown (enter empty line to finish):')
        features = []
        idx = 1

        while True:
            input_str = input(f'  Feature {idx} (format: requirement|page|changes): ').strip()
            if not input_str:
                break

            parts = [p.strip() for p in input_str.split('|')]
            if len(parts) == 3:
                features.append(Feature(
                    requirement=parts[0],
                    page=parts[1],
                    changes=parts[2],
                ))
            idx += 1

        return features

    def _render(self, data: SpecData) -> str:
        content = self.template

        # Simple template replacement
        replacements = {
            '{project_name}': data.project_name,
            '{version}': data.version,
            '{author}': data.author,
            '{date}': data.date,
            '{background}': data.background,
            '{goal}': data.goal,
            '{business_value}': data.business_value,
            '{frontend_stack}': data.frontend_stack,
            '{backend_stack}': data.backend_stack,
            '{database}': data.database,
        }

        for key, value in replacements.items():
            content = content.replace(key, value)

        # Handle features table
        if data.features:
            table_rows = [
                f'| {f.requirement} | {f.page} | {f.changes} |'
                for f in data.features
            ]
            content = content.replace(
                '{features_table}',
                '\n'.join(table_rows)
            )
        else:
            content = content.replace('{features_table}', '| TBD | TBD | TBD |')

        return content


def main():
    parser = argparse.ArgumentParser(
        description='Technical Specification Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_spec.py --interactive
  python generate_spec.py --prd prd.md --output spec.md
  python generate_spec.py --template
        """
    )

    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Interactive mode')
    parser.add_argument('--prd', type=str,
                        help='Generate from PRD file')
    parser.add_argument('-o', '--output', type=str,
                        help='Output file path')
    parser.add_argument('-t', '--template', action='store_true',
                        help='Output template only')

    args = parser.parse_args()
    generator = TechSpecGenerator()

    content = ''

    if args.interactive:
        content = generator.generate_interactive()
    elif args.prd:
        content = generator.generate_from_prd(args.prd)
    elif args.template:
        content = generator.template
    else:
        parser.print_help()
        sys.exit(1)

    if args.output:
        Path(args.output).write_text(content, encoding='utf-8')
        print(f'✓ Technical specification generated: {args.output}')
    else:
        print()
        print('=' * 60)
        print(content)
        print('=' * 60)


if __name__ == '__main__':
    main()
