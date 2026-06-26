#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import SubscriptionBoxPlanner, handle


def test_category_detection_pet():
    planner = SubscriptionBoxPlanner('We run a pet subscription with dog toys and treats')
    assert planner.category == 'pet'


def test_budget_extraction():
    planner = SubscriptionBoxPlanner('Need a May beauty box under $28 landed cost')
    assert planner.budget == 28


def test_goal_detection_retention():
    planner = SubscriptionBoxPlanner('Our subscription churn is rising, help with retention')
    assert planner.goal == 'retention'


def test_render_contains_three_concepts():
    output = handle('Plan a beauty subscription box for busy professionals under $28')
    assert output.startswith('# Subscription Box Curation Plan')
    assert output.count('### Concept ') >= 3
    assert '## Risks and Assumptions' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
