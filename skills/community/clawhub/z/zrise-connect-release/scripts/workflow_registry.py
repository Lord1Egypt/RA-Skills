#!/usr/bin/env python3
"""
workflow_registry.py — List available Lobster workflows for Zrise tasks.

Workflows can be:
1. Built-in Lobster workflows
2. Custom workflows in workspace/workflows/
3. Skill-specific workflows in skills/zrise-connect/workflows/

Usage:
    python3 workflow_registry.py --list
    python3 workflow_registry.py --search "requirement"
    python3 workflow_registry.py --info general
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPTS_DIR))

from zrise_utils import get_root

ROOT = get_root()

# Built-in Zrise workflows (defined as Lobster workflows)
BUILTIN_WORKFLOWS = {
    'general': {
        'name': 'general',
        'description': 'General task processing with OpenClaw Agent',
        'file': 'skills/zrise-connect/workflows/general.lobster',
        'category': 'general',
        'tags': ['general', 'default'],
        'agent_model': 'default',
    },
    'requirement-analysis': {
        'name': 'requirement-analysis',
        'description': 'Analyze requirements, create user stories, acceptance criteria',
        'file': 'skills/zrise-connect/workflows/requirement-analysis.lobster',
        'category': 'analysis',
        'tags': ['requirement', 'ba', 'analysis', 'user-story'],
        'agent_model': 'zrise-analyst',
    },
    'technical-design': {
        'name': 'technical-design',
        'description': 'Design technical architecture, APIs, data models',
        'file': 'skills/zrise-connect/workflows/technical-design.lobster',
        'category': 'design',
        'tags': ['technical', 'design', 'architecture', 'api'],
        'agent_model': 'zrise-dev',
    },
    'implementation': {
        'name': 'implementation',
        'description': 'Implement code, fix bugs, build features',
        'file': 'skills/zrise-connect/workflows/implementation.lobster',
        'category': 'development',
        'tags': ['implement', 'code', 'bug', 'feature'],
        'agent_model': 'zrise-dev',
    },
    'code-review': {
        'name': 'code-review',
        'description': 'Review code, identify issues, suggest improvements',
        'file': 'skills/zrise-connect/workflows/code-review.lobster',
        'category': 'review',
        'tags': ['review', 'code', 'pr'],
        'agent_model': 'zrise-dev',
    },
    'testing': {
        'name': 'testing',
        'description': 'Create test plans, test cases, QA scenarios',
        'file': 'skills/zrise-connect/workflows/testing.lobster',
        'category': 'qa',
        'tags': ['test', 'qa', 'testing'],
        'agent_model': 'zrise-qa',
    },
    'documentation': {
        'name': 'documentation',
        'description': 'Create documentation, knowledge articles',
        'file': 'skills/zrise-connect/workflows/documentation.lobster',
        'category': 'docs',
        'tags': ['document', 'docs', 'wiki'],
        'agent_model': 'zrise-analyst',
    },
    'pm-planning': {
        'name': 'pm-planning',
        'description': 'PM planning, coordination, task breakdown',
        'file': 'skills/zrise-connect/workflows/pm-planning.lobster',
        'category': 'pm',
        'tags': ['pm', 'planning', 'coordination'],
        'agent_model': 'zrise-pm',
    },
}


def discover_custom_workflows():
    """Discover custom Lobster workflows in workspace."""
    custom = {}
    
    # Check workspace/workflows/
    workflows_dir = ROOT / 'workflows'
    if workflows_dir.exists():
        for f in workflows_dir.glob('**/*.lobster'):
            # Parse workflow metadata
            try:
                content = f.read_text(encoding='utf-8')
                name = f.stem
                # Extract name from file if defined
                for line in content.split('\n'):
                    if line.startswith('name:'):
                        name = line.split(':', 1)[1].strip()
                        break
                
                custom[name] = {
                    'name': name,
                    'file': str(f.relative_to(ROOT)),
                    'source': 'custom',
                    'description': f'Custom workflow: {name}',
                }
            except Exception:
                pass
    
    return custom


def list_all_workflows():
    """List all available workflows (built-in + custom)."""
    workflows = {}
    
    # Add built-in workflows
    workflows.update(BUILTIN_WORKFLOWS)
    
    # Add custom workflows
    custom = discover_custom_workflows()
    workflows.update(custom)
    
    # Try to get Lobster's registered workflows
    try:
        result = subprocess.run(
            ['lobster', 'workflows.list', '--json'],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            timeout=10
        )
        if result.returncode == 0:
            lobster_workflows = json.loads(result.stdout)
            for wf in lobster_workflows:
                name = wf.get('name')
                if name and name not in workflows:
                    workflows[name] = {
                        'name': name,
                        'description': wf.get('description', ''),
                        'source': 'lobster',
                        'args_schema': wf.get('argsSchema', {}),
                    }
    except Exception as e:
        print(f"Warning: Could not list Lobster workflows: {e}", file=sys.stderr)
    
    return workflows


def search_workflows(query):
    """Search workflows by name, description, or tags."""
    workflows = list_all_workflows()
    query_lower = query.lower()
    
    results = []
    for name, wf in workflows.items():
        # Search in name, description, tags
        searchable = ' '.join([
            name,
            wf.get('description', ''),
            ' '.join(wf.get('tags', []))
        ]).lower()
        
        if query_lower in searchable:
            results.append(wf)
    
    return results


def get_workflow_info(name):
    """Get detailed info about a specific workflow."""
    workflows = list_all_workflows()
    return workflows.get(name)


def main():
    parser = argparse.ArgumentParser(description='Zrise Workflow Registry')
    parser.add_argument('--list', action='store_true', help='List all workflows')
    parser.add_argument('--search', type=str, help='Search workflows')
    parser.add_argument('--info', type=str, help='Get workflow info')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()
    
    if args.list:
        workflows = list_all_workflows()
        if args.json:
            print(json.dumps(workflows, indent=2, ensure_ascii=False))
        else:
            print(f"\n📋 Available Workflows ({len(workflows)} total)\n")
            for name, wf in sorted(workflows.items()):
                source = wf.get('source', 'builtin')
                desc = wf.get('description', '')[:60]
                print(f"  • {name} [{source}]: {desc}")
    
    elif args.search:
        results = search_workflows(args.search)
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(f"\n🔍 Search Results for '{args.search}' ({len(results)} found)\n")
            for wf in results:
                print(f"  • {wf['name']}: {wf.get('description', '')[:60]}")
    
    elif args.info:
        wf = get_workflow_info(args.info)
        if wf:
            print(json.dumps(wf, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Workflow '{args.info}' not found")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
