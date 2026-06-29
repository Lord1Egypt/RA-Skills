#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'managed_provider_unit_economics.py'
CONFIGURE_SCRIPT = ROOT / 'scripts' / 'configure_managed_provider_resale_readiness.sh'


class ManagedProviderUnitEconomicsCliTests(unittest.TestCase):
    def env(self, cost='1.234567'):
        env = os.environ.copy()
        env.update({
            'SAGE_ROUTER_DARIO_AUTOSTART': '0',
            'SAGE_ROUTER_BUNDLED_OLLAMA_AUTOSTART': '0',
            'SAGE_ROUTER_EDGE_MONTHLY_QUOTAS': (
                'trial=1000,lite=10000,pro=50000,max=200000,paid=50000,active=50000,default=0'
            ),
            'SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS': cost,
            'SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT': '35',
        })
        return env

    def test_json_output_does_not_print_private_cost_or_exact_margin(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), '--json'],
            cwd=ROOT,
            env=self.env(),
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertNotIn('1.234567', result.stdout)
        self.assertNotIn('"grossMarginPercent":', result.stdout)
        report = json.loads(result.stdout)
        self.assertTrue(report['candidateCostProvided'])
        self.assertFalse(report['candidateCostPrinted'])
        self.assertFalse(report['actualProviderCostExposed'])
        self.assertFalse(report['grossMarginPercentExposed'])
        self.assertTrue(report['satisfied'])
        self.assertEqual([], report['failedPlans'])
        self.assertTrue(report['privacy']['containsActualProviderCosts'] is False)
        for row in report['evaluatedPlans']:
            self.assertIn('maximumProviderCostCentsPerThousandRequests', row)
            self.assertIn('meetsMinimumGrossMargin', row)
            self.assertNotIn('grossMarginPercent', row)

    def test_text_output_fails_closed_without_printing_failing_candidate_cost(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            env=self.env(cost='30.123456'),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(0, result.returncode)
        combined = result.stdout + result.stderr
        self.assertNotIn('30.123456', combined)
        self.assertNotIn('grossMarginPercent=', combined)
        self.assertIn('candidateCostProvided=true', combined)
        self.assertIn('satisfied=false', combined)
        self.assertIn('failedPlans=max', combined)

    def test_configure_helper_unit_economics_mode_delegates_safely(self):
        result = subprocess.run(
            [str(CONFIGURE_SCRIPT), '--unit-economics'],
            cwd=ROOT,
            env=self.env(),
            text=True,
            capture_output=True,
            check=True,
        )
        combined = result.stdout + result.stderr
        self.assertNotIn('1.234567', combined)
        self.assertIn('candidateCostPrinted=false', combined)
        self.assertIn('satisfied=true', combined)


if __name__ == '__main__':
    unittest.main()
