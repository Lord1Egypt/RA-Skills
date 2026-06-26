#!/usr/bin/env python3
"""
agent_selector.py - Select appropriate agent for task execution

Usage:
    python3 agent_selector.py --task-id 42174
    python3 agent_selector.py --task-id 42174 --agent demo-be  # Manual override
    python3 agent_selector.py --list  # List available agents
"""
import argparse
import json
import sys
import re
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPTS_DIR))

from zrise_utils import get_root, get_config_path

ROOT = get_root()


def load_agent_routing():
    """Load agent routing config"""
    config_path = get_config_path('zrise/agent-routing.json')
    
    if not config_path.exists():
        # Default config
        return {
            'agents': {
                'demo-be': {
                    'name': 'Backend Developer',
                    'skills': ['python', 'api', 'database'],
                    'keywords': ['backend', 'api', 'server'],
                    'priority': 1,
                    'auto_select': True
                },
                'demo-fe': {
                    'name': 'Frontend Developer',
                    'skills': ['html', 'css', 'javascript'],
                    'keywords': ['frontend', 'ui', 'web'],
                    'priority': 1,
                    'auto_select': True
                }
            },
            'default_agent': 'demo-be'
        }
    
    try:
        return json.loads(config_path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"⚠️ Failed to load agent routing config: {e}", file=sys.stderr)
        return {'agents': {}, 'default_agent': 'demo-be'}


def match_task_to_agent(task_description, task_name, routing):
    """Match task to best agent based on keywords"""
    if not routing.get('agents'):
        return routing.get('default_agent', 'demo-be')
    
    # Combine task text
    task_text = f"{task_name} {task_description}".lower()
    
    # Score each agent
    scores = {}
    for agent_id, agent_config in routing['agents'].items():
        if not agent_config.get('auto_select', True):
            continue
        
        score = 0
        keywords = agent_config.get('keywords', [])
        skills = agent_config.get('skills', [])
        priority = agent_config.get('priority', 1)
        
        # Count keyword matches
        for keyword in keywords:
            if keyword.lower() in task_text:
                score += 10
        
        # Count skill matches
        for skill in skills:
            if skill.lower() in task_text:
                score += 5
        
        # Adjust by priority (lower priority = higher score)
        score = score / priority
        
        if score > 0:
            scores[agent_id] = score
    
    # Return best match
    if scores:
        best_agent = max(scores, key=scores.get)
        return best_agent
    
    # Fallback to default
    return routing.get('default_agent', 'demo-be')


def select_agent(task_id, task_description, task_name, manual_agent=None):
    """Select agent for task execution"""
    routing = load_agent_routing()
    
    # Manual override
    if manual_agent:
        if manual_agent in routing.get('agents', {}):
            return {
                'agent_id': manual_agent,
                'agent_name': routing['agents'][manual_agent].get('name', manual_agent),
                'selection_type': 'manual',
                'confidence': 1.0
            }
        else:
            print(f"⚠️ Agent '{manual_agent}' not found in routing config", file=sys.stderr)
    
    # Auto selection
    selected_agent = match_task_to_agent(task_description, task_name, routing)
    
    agent_config = routing.get('agents', {}).get(selected_agent, {})
    
    return {
        'agent_id': selected_agent,
        'agent_name': agent_config.get('name', selected_agent),
        'selection_type': 'auto',
        'confidence': 0.8,  # Placeholder
        'skills': agent_config.get('skills', []),
        'estimated_time': agent_config.get('estimated_time', '30m')
    }


def list_available_agents():
    """List all available agents"""
    routing = load_agent_routing()
    
    agents = []
    for agent_id, config in routing.get('agents', {}).items():
        agents.append({
            'id': agent_id,
            'name': config.get('name', agent_id),
            'skills': config.get('skills', []),
            'auto_select': config.get('auto_select', True),
            'priority': config.get('priority', 1)
        })
    
    return {
        'agents': agents,
        'default': routing.get('default_agent', 'demo-be')
    }


def main():
    parser = argparse.ArgumentParser(description='Select agent for task execution')
    parser.add_argument('--task-id', type=int)
    parser.add_argument('--task-name', default='')
    parser.add_argument('--task-description', default='')
    parser.add_argument('--agent', help='Manual agent selection')
    parser.add_argument('--list', action='store_true', help='List available agents')
    args = parser.parse_args()
    
    # List agents
    if args.list:
        agents = list_available_agents()
        print(json.dumps(agents, indent=2, ensure_ascii=False))
        return 0
    
    # Select agent
    if not args.task_id:
        print("❌ --task-id required", file=sys.stderr)
        return 1
    
    result = select_agent(
        args.task_id,
        args.task_description,
        args.task_name,
        args.agent
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
