#!/usr/bin/env python3
"""
Bundle Analyzer for Vite React Projects

Analyzes build output and provides optimization recommendations:
- Large dependencies
- Unused code
- Code splitting opportunities
- Import analysis
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from collections import defaultdict


def analyze_package_json():
    """Analyze package.json for optimization opportunities"""
    try:
        with open('package.json', 'r') as f:
            package = json.load(f)
    except FileNotFoundError:
        print("❌ package.json not found")
        return

    print("📦 Package Analysis")
    print("=" * 70)

    dependencies = package.get('dependencies', {})
    dev_dependencies = package.get('devDependencies', {})

    # Known large libraries
    large_libs = {
        'moment': {'size': '~290KB', 'alternative': 'date-fns or dayjs (~2-7KB)'},
        'lodash': {'size': '~70KB', 'alternative': 'lodash-es with tree-shaking or native JS'},
        'axios': {'size': '~13KB', 'alternative': 'native fetch API'},
        'jquery': {'size': '~90KB', 'alternative': 'native DOM APIs'},
        'material-ui': {'size': '~350KB', 'alternative': 'Consider lighter alternatives'},
    }

    print("\n🔍 Large Dependencies Found:")
    found_large = False
    for lib, info in large_libs.items():
        if lib in dependencies:
            found_large = True
            print(f"  ⚠️  {lib} ({info['size']})")
            print(f"      → Consider: {info['alternative']}")

    if not found_large:
        print("  ✅ No known large dependencies found")

    # Check for duplicate functionality
    print("\n🔄 Potential Duplicates:")
    duplicate_checks = [
        (['axios', 'node-fetch', 'got'], "HTTP clients"),
        (['moment', 'dayjs', 'date-fns'], "Date libraries"),
        (['lodash', 'underscore', 'ramda'], "Utility libraries"),
    ]

    found_duplicates = False
    for libs, category in duplicate_checks:
        found = [lib for lib in libs if lib in dependencies]
        if len(found) > 1:
            found_duplicates = True
            print(f"  ⚠️  Multiple {category}: {', '.join(found)}")
            print(f"      → Consider using only one")

    if not found_duplicates:
        print("  ✅ No duplicate functionality detected")


def analyze_imports(src_dir='src'):
    """Analyze import statements for optimization opportunities"""
    print("\n\n📥 Import Analysis")
    print("=" * 70)

    import_counts = defaultdict(int)
    default_imports = defaultdict(list)
    named_imports = defaultdict(list)

    # Scan all JS/TS files
    for ext in ['*.tsx', '*.ts', '*.jsx', '*.js']:
        for file in Path(src_dir).rglob(ext):
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    # Simple import parsing (not AST-based, but good enough)
                    for line in content.split('\n'):
                        line = line.strip()
                        if line.startswith('import ') and ' from ' in line:
                            # Extract library name
                            lib = line.split(' from ')[-1].strip().strip('";\'')
                            if not lib.startswith('.'):  # External import
                                import_counts[lib] += 1

                                # Check if it's a default import
                                if 'import {' not in line and '* as' not in line:
                                    default_imports[lib].append(str(file))
                                else:
                                    named_imports[lib].append(str(file))
            except:
                continue

    # Report most imported libraries
    print("\n📊 Most Imported Libraries:")
    sorted_imports = sorted(import_counts.items(), key=lambda x: x[1], reverse=True)
    for lib, count in sorted_imports[:10]:
        print(f"  {lib}: {count} imports")

    # Check for default imports that should be named
    print("\n⚠️  Optimization Opportunities:")

    # lodash default imports
    if 'lodash' in default_imports:
        print(f"  • lodash: Use named imports for better tree-shaking")
        print(f"    import {{ debounce }} from 'lodash-es'; // Instead of: import _ from 'lodash';")

    # Check for React imports in newer React versions
    if 'react' in import_counts:
        print(f"  • React 17+: JSX transform doesn't require React import")
        print(f"    Remove: import React from 'react'; (unless using React.xxx)")


def analyze_build_output():
    """Analyze Vite build output"""
    dist_dir = Path('dist/assets')

    if not dist_dir.exists():
        print("\n❌ No build output found. Run 'npm run build' first.")
        return

    print("\n\n📊 Build Output Analysis")
    print("=" * 70)

    # Analyze JS bundles
    js_files = list(dist_dir.glob('*.js'))

    if not js_files:
        print("❌ No JavaScript bundles found")
        return

    print("\n📦 JavaScript Bundles:")
    total_size = 0
    for js_file in sorted(js_files, key=lambda f: f.stat().st_size, reverse=True):
        size = js_file.stat().st_size
        total_size += size
        size_kb = size / 1024
        size_mb = size / (1024 * 1024)

        # Determine type
        if 'vendor' in js_file.name:
            file_type = "📚 Vendor"
        elif 'index' in js_file.name:
            file_type = "🏠 Main"
        else:
            file_type = "📄 Chunk"

        if size_mb >= 1:
            print(f"  {file_type}: {js_file.name} ({size_mb:.2f} MB)")
        else:
            print(f"  {file_type}: {js_file.name} ({size_kb:.2f} KB)")

        # Warnings for large files
        if size_kb > 500:
            print(f"    ⚠️  Large bundle! Consider code splitting")

    print(f"\n  Total JS size: {total_size / (1024 * 1024):.2f} MB")

    # Analyze CSS
    css_files = list(dist_dir.glob('*.css'))
    if css_files:
        print("\n🎨 CSS Files:")
        for css_file in css_files:
            size_kb = css_file.stat().st_size / 1024
            print(f"  {css_file.name} ({size_kb:.2f} KB)")


def provide_recommendations():
    """Provide general optimization recommendations"""
    print("\n\n💡 Optimization Recommendations")
    print("=" * 70)

    recommendations = [
        ("Code Splitting", [
            "Use React.lazy() for route-based code splitting",
            "Lazy load heavy components (modals, charts, editors)",
            "Split vendor bundle: splitChunks in vite.config.ts"
        ]),
        ("Tree Shaking", [
            "Use named imports: import { Button } from 'library'",
            "Avoid default exports for large libraries",
            "Use lodash-es instead of lodash",
            "Enable sideEffects: false in package.json"
        ]),
        ("Asset Optimization", [
            "Use WebP/AVIF for images",
            "Lazy load images with loading='lazy'",
            "Use SVG sprites for icons",
            "Enable image compression in Vite config"
        ]),
        ("Runtime Performance", [
            "Use React.memo() for expensive components",
            "Implement useMemo() and useCallback() for heavy computations",
            "Virtualize long lists (react-window, react-virtualized)",
            "Debounce expensive operations"
        ]),
        ("Build Configuration", [
            "Enable minification and compression",
            "Configure chunk size warnings",
            "Use build analyzer: rollup-plugin-visualizer",
            "Enable CSS code splitting"
        ])
    ]

    for category, items in recommendations:
        print(f"\n{category}:")
        for item in items:
            print(f"  • {item}")


def main():
    print("🔍 Vite React Bundle Analyzer")
    print("=" * 70)

    # Check if in a Vite project
    if not Path('vite.config.ts').exists() and not Path('vite.config.js').exists():
        print("❌ Not a Vite project (vite.config not found)")
        sys.exit(1)

    analyze_package_json()
    analyze_imports()
    analyze_build_output()
    provide_recommendations()

    print("\n" + "=" * 70)
    print("✅ Analysis complete!")
    print("\n💡 Next steps:")
    print("  1. Review large dependencies and consider alternatives")
    print("  2. Implement code splitting for routes and heavy components")
    print("  3. Run: npm run build -- --mode analyze (if configured)")
    print("  4. Use Chrome DevTools Coverage to find unused code")


if __name__ == "__main__":
    main()
