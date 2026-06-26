#!/usr/bin/env python3
"""
React Custom Hook Generator

Generates optimized custom hooks with TypeScript types and tests.
"""

import os
import sys
import argparse
from pathlib import Path


HOOK_TEMPLATE = """import {{ {imports} }} from 'react';
{additional_imports}

{types}

export const {hook_name} = ({params}){return_type} => {{
  {hook_body}

  return {return_value};
}};
"""

TEST_TEMPLATE = """import {{ renderHook, act }} from '@testing-library/react';
import {{ {hook_name} }} from './{hook_name}';

describe('{hook_name}', () => {{
  it('should initialize with default values', () => {{
    const {{ result }} = renderHook(() => {hook_name}());

    // Add assertions here
    expect(result.current).toBeDefined();
  }});

  // Add more tests here
}});
"""

HOOK_TEMPLATES = {
    'state': {
        'imports': 'useState',
        'params': 'initialValue: T',
        'return_type': ': [T, (value: T) => void]',
        'types': 'type T = any; // Replace with your type',
        'body': '''const [value, setValue] = useState<T>(initialValue);''',
        'return': '[value, setValue]'
    },
    'effect': {
        'imports': 'useState, useEffect',
        'params': '',
        'return_type': ': void',
        'types': '',
        'body': '''useEffect(() => {
    // Effect logic here

    return () => {
      // Cleanup logic here
    };
  }, []);''',
        'return': 'undefined'
    },
    'fetch': {
        'imports': 'useState, useEffect',
        'params': 'url: string',
        'return_type': ': { data: T | null; loading: boolean; error: Error | null }',
        'types': 'type T = any; // Replace with your data type',
        'body': '''const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch');
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);''',
        'return': '{ data, loading, error }'
    },
    'localStorage': {
        'imports': 'useState, useEffect',
        'params': 'key: string, initialValue: T',
        'return_type': ': [T, (value: T) => void]',
        'types': 'type T = any; // Replace with your type',
        'body': '''const [value, setValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(error);
    }
  }, [key, value]);''',
        'return': '[value, setValue]'
    },
    'debounce': {
        'imports': 'useState, useEffect',
        'params': 'value: T, delay: number = 500',
        'return_type': ': T',
        'types': 'type T = any; // Replace with your type',
        'body': '''const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);''',
        'return': 'debouncedValue'
    },
    'interval': {
        'imports': 'useEffect, useRef',
        'params': 'callback: () => void, delay: number | null',
        'return_type': ': void',
        'types': '',
        'body': '''const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay === null) return;

    const tick = () => savedCallback.current();
    const id = setInterval(tick, delay);

    return () => clearInterval(id);
  }, [delay]);''',
        'return': 'undefined'
    }
}


def create_hook(name: str, template_type: str = "custom", with_tests: bool = True):
    """
    Create a custom React hook

    Args:
        name: Hook name (should start with 'use')
        template_type: Type of hook template to use
        with_tests: Generate test file
    """
    # Ensure hook name starts with 'use'
    if not name.startswith('use'):
        name = 'use' + name[0].upper() + name[1:]

    hook_name = name
    hooks_dir = Path("src/hooks")
    hooks_dir.mkdir(parents=True, exist_ok=True)

    # Get template or use custom
    if template_type in HOOK_TEMPLATES:
        template = HOOK_TEMPLATES[template_type]
        imports = template['imports']
        params = template['params']
        return_type = template['return_type']
        types = template['types']
        hook_body = template['body']
        return_value = template['return']
    else:
        # Custom hook template
        imports = 'useState'
        params = ''
        return_type = ''
        types = '// Add your types here'
        hook_body = '''// Add your hook logic here
  const [state, setState] = useState();'''
        return_value = '{ state }'

    # Create hook file
    hook_content = HOOK_TEMPLATE.format(
        hook_name=hook_name,
        imports=imports,
        additional_imports='',
        types=types,
        params=params,
        return_type=return_type,
        hook_body=hook_body,
        return_value=return_value
    )
    hook_file = hooks_dir / f"{hook_name}.ts"
    hook_file.write_text(hook_content)

    print(f"✅ Created {hook_name} hook in {hook_file}")

    # Create test file
    if with_tests:
        test_content = TEST_TEMPLATE.format(hook_name=hook_name)
        test_file = hooks_dir / f"{hook_name}.test.ts"
        test_file.write_text(test_content)
        print(f"✅ Created test file: {test_file}")

    print(f"\nUsage:")
    print(f"  import {{ {hook_name} }} from '@/hooks/{hook_name}';")


def main():
    parser = argparse.ArgumentParser(description="Generate React custom hook")
    parser.add_argument("name", help="Hook name (will add 'use' prefix if missing)")
    parser.add_argument("--type", choices=list(HOOK_TEMPLATES.keys()) + ["custom"],
                       default="custom",
                       help="Hook template type")
    parser.add_argument("--no-tests", action="store_true", help="Don't generate test file")

    args = parser.parse_args()

    create_hook(
        name=args.name,
        template_type=args.type,
        with_tests=not args.no_tests
    )


if __name__ == "__main__":
    main()
