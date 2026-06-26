#!/usr/bin/env python3
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import SupplierSyncManager, handle


def _skill_description() -> str:
    text = Path(__file__).resolve().parents[1].joinpath('SKILL.md').read_text(encoding='utf-8')
    frontmatter = text.split('---', 2)[1]
    for line in frontmatter.splitlines():
        if line.strip().startswith('description:'):
            return line.split(':', 1)[1].strip().strip("\"'")
    raise AssertionError('description not found in SKILL.md')


def test_objective_detection_inventory():
    manager = SupplierSyncManager('Need daily inventory sync between supplier feed and ERP to avoid stock lag.')
    assert manager.objective == 'Inventory synchronization'
    assert manager.cadence == 'Daily control cycle'


def test_objective_detection_order_handoff():
    manager = SupplierSyncManager('Review duplicate order retries and shipment tracking gaps in the OMS handoff.')
    assert manager.objective == 'Order and fulfillment handoff'
    assert 'Duplicate or missing order events' in manager.risks


def test_system_and_risk_detection():
    manager = SupplierSyncManager('Our ERP, WMS, and Shopify storefront show price mismatch and pack size mapping issues.')
    assert 'ERP' in manager.systems
    assert 'WMS' in manager.systems
    assert 'Marketplace / Storefront' in manager.systems
    assert 'Price or cost mismatch' in manager.risks
    assert 'Pack size or MOQ mismatch' in manager.risks


def test_render_contains_sections_and_skill_description():
    output = handle('Prepare a launch cutover plan for catalog mapping and supplier onboarding.')
    assert output.startswith('# Supplier Sync Management Brief')
    assert f'**Skill description:** {_skill_description()}' in output
    assert '## Recommended Control Table' in output
    assert '## Field Mapping Watchlist' in output
    assert '## Exception Queue Design' in output


def test_dict_input_supported():
    output = handle({
        'objective': 'price sync',
        'systems': ['ERP', 'supplier portal', 'marketplace'],
        'risks': ['currency mismatch', 'mapping'],
        'cadence': 'weekly',
    })
    assert '# Supplier Sync Management Brief' in output
    assert 'Catalog and pricing alignment' in output
    assert 'Weekly operating review' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
