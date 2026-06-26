#!/usr/bin/env python3
"""
React Component Generator

Generates optimized React components following best practices:
- Proper file structure (component, styles, tests, types)
- TypeScript types
- CSS Modules or Styled Components
- Test boilerplate
- Storybook stories (optional)
"""

import os
import sys
import argparse
from pathlib import Path


COMPONENT_TEMPLATE = """import { FC } from 'react';
import styles from './{component_name}.module.css';
{type_import}

export const {component_name}: FC<{component_name}Props> = ({props_destructure}) => {{
  return (
    <div className={{styles.{component_name_lower}}}>
      <h2>{component_name}</h2>
      {children_usage}
    </div>
  );
}};
"""

TYPES_TEMPLATE = """export interface {component_name}Props {{
  {props_definition}
}}
"""

CSS_MODULE_TEMPLATE = """.{component_name_lower} {{
  /* Add your styles here */
  padding: 1rem;
}}
"""

TEST_TEMPLATE = """import {{ render, screen }} from '@testing-library/react';
import {{ {component_name} }} from './{component_name}';

describe('{component_name}', () => {{
  it('renders without crashing', () => {{
    render(<{component_name}{test_props} />);
    expect(screen.getByText('{component_name}')).toBeInTheDocument();
  }});

  // Add more tests here
}});
"""

STORY_TEMPLATE = """import type {{ Meta, StoryObj }} from '@storybook/react';
import {{ {component_name} }} from './{component_name}';

const meta: Meta<typeof {component_name}> = {{
  title: 'Components/{component_name}',
  component: {component_name},
  tags: ['autodocs'],
}};

export default meta;
type Story = StoryObj<typeof {component_name}>;

export const Default: Story = {{
  args: {{{story_args}
  }},
}};
"""

INDEX_TEMPLATE = """export {{ {component_name} }} from './{component_name}';
export type {{ {component_name}Props }} from './{component_name}.types';
"""


def create_component(
    name: str,
    path: str = "src/components",
    with_props: bool = True,
    with_children: bool = False,
    with_tests: bool = True,
    with_story: bool = False,
    component_type: str = "component"
):
    """
    Create a new React component with all necessary files

    Args:
        name: Component name (PascalCase)
        path: Base path for component
        with_props: Include props interface
        with_children: Include children prop
        with_tests: Generate test file
        with_story: Generate Storybook story
        component_type: Type (component, page, layout, feature)
    """
    # Ensure PascalCase
    component_name = ''.join(word.capitalize() for word in name.replace('-', '_').split('_'))
    component_name_lower = component_name[0].lower() + component_name[1:]

    # Determine base path based on type
    type_paths = {
        'component': 'src/components',
        'page': 'src/pages',
        'layout': 'src/layouts',
        'feature': 'src/features'
    }
    base_path = type_paths.get(component_type, path)

    # Create component directory
    component_dir = Path(base_path) / component_name
    component_dir.mkdir(parents=True, exist_ok=True)

    # Prepare template variables
    props_definition = "children?: React.ReactNode;" if with_children else "// Add your props here"
    props_destructure = "children" if with_children else ""
    children_usage = "{children}" if with_children else ""
    type_import = f"import {{ {component_name}Props }} from './{component_name}.types';" if with_props else ""
    test_props = " children={<>Test</>}" if with_children else ""
    story_args = "\n    children: 'Story content'," if with_children else "\n    // Add story args here"

    # Create component file
    component_content = COMPONENT_TEMPLATE.format(
        component_name=component_name,
        component_name_lower=component_name_lower,
        props_destructure=props_destructure,
        children_usage=children_usage,
        type_import=type_import
    )
    (component_dir / f"{component_name}.tsx").write_text(component_content)

    # Create types file
    if with_props:
        types_content = TYPES_TEMPLATE.format(
            component_name=component_name,
            props_definition=props_definition
        )
        (component_dir / f"{component_name}.types.ts").write_text(types_content)

    # Create CSS module
    css_content = CSS_MODULE_TEMPLATE.format(
        component_name_lower=component_name_lower
    )
    (component_dir / f"{component_name}.module.css").write_text(css_content)

    # Create test file
    if with_tests:
        test_content = TEST_TEMPLATE.format(
            component_name=component_name,
            test_props=test_props
        )
        (component_dir / f"{component_name}.test.tsx").write_text(test_content)

    # Create Storybook story
    if with_story:
        story_content = STORY_TEMPLATE.format(
            component_name=component_name,
            story_args=story_args
        )
        (component_dir / f"{component_name}.stories.tsx").write_text(story_content)

    # Create index file for clean imports
    index_content = INDEX_TEMPLATE.format(component_name=component_name)
    (component_dir / "index.ts").write_text(index_content)

    print(f"✅ Created {component_name} component in {component_dir}")
    print(f"\nFiles created:")
    print(f"  - {component_name}.tsx")
    if with_props:
        print(f"  - {component_name}.types.ts")
    print(f"  - {component_name}.module.css")
    if with_tests:
        print(f"  - {component_name}.test.tsx")
    if with_story:
        print(f"  - {component_name}.stories.tsx")
    print(f"  - index.ts")
    print(f"\nUsage:")
    print(f"  import {{ {component_name} }} from '@/{base_path.replace('src/', '')}/{component_name}';")


def main():
    parser = argparse.ArgumentParser(description="Generate React component with best practices")
    parser.add_argument("name", help="Component name (PascalCase)")
    parser.add_argument("--path", default="src/components", help="Base path for component")
    parser.add_argument("--type", choices=["component", "page", "layout", "feature"],
                       default="component", help="Component type")
    parser.add_argument("--no-props", action="store_true", help="Don't generate props file")
    parser.add_argument("--children", action="store_true", help="Include children prop")
    parser.add_argument("--no-tests", action="store_true", help="Don't generate test file")
    parser.add_argument("--story", action="store_true", help="Generate Storybook story")

    args = parser.parse_args()

    create_component(
        name=args.name,
        path=args.path,
        with_props=not args.no_props,
        with_children=args.children,
        with_tests=not args.no_tests,
        with_story=args.story,
        component_type=args.type
    )


if __name__ == "__main__":
    main()
