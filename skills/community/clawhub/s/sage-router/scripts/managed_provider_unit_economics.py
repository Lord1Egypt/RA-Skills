#!/usr/bin/env python3
"""Secret-safe managed-provider unit-economics preflight."""

import argparse
import json
import logging
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# This CLI only needs public plan math. Keep import-time provider discovery from
# touching external provider APIs while an operator is reviewing private costs.
os.environ['SAGE_ROUTER_OLLAMA_CLOUD_CATALOG_ENABLED'] = '0'
os.environ['SAGE_ROUTER_PROFILE_OVERLAYS'] = ''
_disabled = {
    item.strip()
    for item in os.environ.get('SAGE_ROUTER_DISABLED_PROVIDERS', '').split(',')
    if item.strip()
}
_disabled.update({
    'anthropic',
    'darkbloom',
    'dario',
    'google',
    'google-vertex',
    'nvidia-nim',
    'ollama',
    'ollama-cloud',
    'ollama-cyber',
    'openai',
    'openai-codex',
    'openrouter',
})
os.environ['SAGE_ROUTER_DISABLED_PROVIDERS'] = ','.join(sorted(_disabled))
logging.basicConfig(level=logging.ERROR)

import router  # noqa: E402


def parse_margin(raw):
    try:
        return max(0, int(float(str(raw or '').strip() or '35')))
    except (TypeError, ValueError):
        return 0


def public_safe_preflight(minimum_margin_percent):
    economics = router.managed_provider_unit_economics(
        router.parse_provider_resale_cost_cents_per_thousand_requests(),
        minimum_margin_percent,
    )
    rows = []
    for row in economics.get('evaluatedPlans') or []:
        rows.append({
            'plan': row.get('plan'),
            'monthlyRequests': row.get('monthlyRequests'),
            'monthlyPriceUsd': row.get('monthlyPriceUsd'),
            'revenueCentsPerThousandRequests': row.get('revenueCentsPerThousandRequests'),
            'minimumGrossMarginPercent': row.get('minimumGrossMarginPercent'),
            'maximumProviderCostCentsPerThousandRequests': row.get(
                'maximumProviderCostCentsPerThousandRequests'
            ),
            'meetsMinimumGrossMargin': bool(row.get('meetsMinimumGrossMargin')),
        })
    failed = [row['plan'] for row in rows if not row.get('meetsMinimumGrossMargin')]
    return {
        'kind': 'managed_provider_unit_economics_preflight',
        'costModel': economics.get('costModel'),
        'costModelConfigured': bool(economics.get('costModelConfigured')),
        'costModelEnv': economics.get('costModelEnv'),
        'candidateCostProvided': bool(economics.get('costModelConfigured')),
        'candidateCostPrinted': False,
        'actualProviderCostExposed': False,
        'grossMarginPercentExposed': False,
        'minimumGrossMarginPercent': minimum_margin_percent,
        'evaluatedPlans': rows,
        'failedPlans': failed,
        'satisfied': bool(economics.get('satisfied')),
        'privacy': {
            'containsSecrets': False,
            'containsProviderCredentials': False,
            'containsActualProviderCosts': False,
            'containsGrossMarginPercent': False,
            'containsPrompts': False,
            'containsRawProviderResponses': False,
        },
    }


def print_text(report):
    print('Managed provider unit-economics preflight')
    print(f"candidateCostProvided={'true' if report['candidateCostProvided'] else 'false'}")
    print('candidateCostPrinted=false')
    print('actualProviderCostExposed=false')
    print('grossMarginPercentExposed=false')
    print(f"minimumGrossMarginPercent={report['minimumGrossMarginPercent']}")
    print(f"satisfied={'true' if report['satisfied'] else 'false'}")
    print('plans:')
    for row in report['evaluatedPlans']:
        status = 'pass' if row['meetsMinimumGrossMargin'] else 'fail'
        print(
            f"- {row['plan']}: revenueCentsPer1k={row['revenueCentsPerThousandRequests']} "
            f"maxSafeProviderCostCentsPer1k={row['maximumProviderCostCentsPerThousandRequests']} "
            f"minimumGrossMarginPercent={row['minimumGrossMarginPercent']} "
            f"status={status}"
        )
    if report['failedPlans']:
        print('failedPlans=' + ','.join(report['failedPlans']))


def main():
    parser = argparse.ArgumentParser(
        description='Validate managed-provider resale unit economics without printing provider costs.'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Print a machine-readable secret-free report.',
    )
    parser.add_argument(
        '--min-margin',
        default=os.environ.get('SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT', '35'),
        help='Minimum gross margin percent. Defaults to SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT or 35.',
    )
    args = parser.parse_args()

    report = public_safe_preflight(parse_margin(args.min_margin))
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text(report)
    return 0 if report['satisfied'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
