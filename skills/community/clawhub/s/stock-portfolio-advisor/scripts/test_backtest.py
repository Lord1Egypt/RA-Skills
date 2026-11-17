"""Regression tests for time leakage, execution accounting and weight releases."""
import copy
import tempfile
import unittest
from pathlib import Path
from backtest import simulate, rank_ic
from build_backtest_dataset import forward_label, verify_dataset
from calibrate_weights import split_rows, candidates, configuration, calibrate
from weight_registry import normalize, resolve, digest, write_json, read_registry, activate, SCORING_RULES
from value_model import evaluate, compute_delta
from test_value_model import stock, data


def small_dataset():
    days=['2020-01-31','2020-02-03','2020-02-04','2020-02-28','2020-03-02','2020-03-31']
    bars={'A':{d:dict(open=10.,close=10.,split_factor=1.,cash_dividend=0.,buy_allowed=True,sell_allowed=True,delisted=False) for d in days}}
    ds=dict(schema_version=1,rules_version=SCORING_RULES,synthetic=True,label_months=1,sessions=days,
            benchmark={d:dict(open_tr=100.,close_tr=100.) for d in days},bars=bars,
            rows=[dict(date='2020-01-31',code='A',profile='default',industry='i',exposure_group='g',dims=dict(Q=80,G=80,V=80),eligible=True,label=None),
                  dict(date='2020-02-28',code='A',profile='default',industry='i',exposure_group='g',dims=dict(Q=80,G=80,V=80),eligible=False,label=None)])
    ds['dataset_hash']=digest(ds)
    return ds


W=dict(Q=40,G=30,V=30)
STRATEGY=dict(top_k=1,initial_cash=10000,lot_size=1,equity_budget=.8,buy_fee_bps=0,sell_fee_bps=0,slippage_bps=0)


def run(ds,**kwargs):
    return simulate(ds,W,'2020-01-31','2020-03-31',strategy=STRATEGY,**kwargs)


def release():
    return dict(version='test-release',calibration_id='test',rules_version=SCORING_RULES,
                synthetic=False,validation_passed=True,weights={'default':W},
                training_cutoff='2026-09-05',max_label_end='2026-09-04',effective_from='2026-09-06',expires_on='2027-09-05')


class BacktestTests(unittest.TestCase):
    def test_next_open_execution_and_sell(self):
        r=run(small_dataset())
        self.assertEqual([x['date'] for x in r['trades']],['2020-02-03','2020-03-02'])
        self.assertAlmostEqual(r['total_return'],0)

    def test_dividend_split_accounting(self):
        ds=small_dataset()
        for d in ds['sessions'][2:]:ds['bars']['A'][d].update(open=5.,close=5.)
        ds['bars']['A']['2020-02-04'].update(split_factor=2.,cash_dividend=1.)
        r=run(ds)
        self.assertAlmostEqual(r['total_return'],.015)
        self.assertEqual(r['trades'][-1]['shares'],300)

    def test_blocked_sell_remains_marked(self):
        ds=small_dataset();ds['bars']['A']['2020-03-02']['sell_allowed']=False
        ds['bars']['A']['2020-03-31']['close']=2
        r=run(ds)
        self.assertEqual(r['blocked_orders'],1)
        self.assertAlmostEqual(r['total_return'],-.12)
        self.assertAlmostEqual(r['max_drawdown'],.12)

    def test_blocked_buy_does_not_get_a_fake_fill(self):
        ds=small_dataset();ds['bars']['A']['2020-02-03']['buy_allowed']=False
        self.assertFalse(run(ds)['trades'])

    def test_delisting_zero_settlement_is_loss(self):
        ds=small_dataset();ds['bars']['A']['2020-03-02'].update(delisted=True,close=0,buy_allowed=False,sell_allowed=False)
        ds['bars']['A'].pop('2020-03-31')
        self.assertAlmostEqual(run(ds)['total_return'],-.15)

    def test_missing_held_data_fails_instead_of_dropping_loser(self):
        ds=small_dataset();ds['bars']['A'].pop('2020-02-04')
        with self.assertRaises(ValueError):run(ds)

    def test_empty_profile_month_liquidates(self):
        ds=small_dataset();ds['rows'][1]['profile']='bank'
        self.assertEqual(run(ds,profile='default')['trades'][-1]['side'],'sell')

    def test_costs_reduce_returns(self):
        ds=small_dataset();strategy=STRATEGY|dict(buy_fee_bps=10,sell_fee_bps=10,slippage_bps=10)
        r=simulate(ds,W,'2020-01-31','2020-03-31',strategy=strategy)
        self.assertLess(r['total_return'],0);self.assertGreater(r['total_cost'],0)

    def test_future_prices_do_not_change_earlier_order(self):
        ds=small_dataset();a=run(ds)['trades'][0]
        ds['bars']['A']['2020-03-31']['close']=1000
        self.assertEqual(a,run(ds)['trades'][0])

    def test_forward_label_maturity_and_terminal_loss(self):
        ds=small_dataset();label=forward_label(ds['bars']['A'],ds['benchmark'],ds['sessions'],1,1)
        self.assertEqual(label['label_end'],'2020-03-31')
        self.assertIsNone(forward_label(ds['bars']['A'],ds['benchmark'],ds['sessions'],1,12))
        ds['bars']['A']['2020-03-02'].update(delisted=True,close=0)
        ds['bars']['A'].pop('2020-03-31')
        self.assertEqual(forward_label(ds['bars']['A'],ds['benchmark'],ds['sessions'],1,1)['forward_return'],-1)

    def test_purge_forward_windows_crossing_boundary(self):
        rows=[dict(date='2020-01-31',label={'label_end':'2021-02-01'}),
              dict(date='2020-02-28',label={'label_end':'2020-12-31'}),
              dict(date='2020-03-31',label={'label_end':'2021-01-01'})]
        selected=split_rows(rows,'2020-01-01','2021-01-01','2021-01-01')
        self.assertEqual(selected,[rows[1]])

    def test_rank_ic_uses_date_groups_and_ties(self):
        rows=[dict(date='2020-01-31',eligible=True,dims=dict(Q=i,G=0,V=0),label={'excess_return':i}) for i in range(8)]
        self.assertEqual(rank_ic(rows,W)['mean'],1)
        self.assertIsNone(rank_ic(rows[:3],W)['mean'])

    def test_grid_is_smoothed_and_bounded_before_testing(self):
        base=normalize((25,20,20));c=configuration(None)
        for candidate in candidates(base,c):
            self.assertAlmostEqual(sum(candidate.values()),100)
            self.assertTrue(all(abs(candidate[k]-base[k])<=3.00001 for k in W))

    def test_checksum_rejects_modified_dataset(self):
        ds=small_dataset();verify_dataset(ds);ds['rows'][0]['dims']['Q']=99
        with self.assertRaises(ValueError):verify_dataset(ds)

    def test_small_dataset_keeps_incumbent(self):
        r=calibrate(small_dataset(),'2020-03-31',{'schema_version':1,'releases':[]},profiles=['default'])
        self.assertFalse(r['profiles']['default']['accepted'])

    def test_release_effective_date_and_expiry(self):
        r={'schema_version':1,'releases':[release()]}
        self.assertEqual(resolve(r,'default','2026-09-05',(25,20,20))[1],'builtin-v2.1')
        self.assertEqual(resolve(r,'default','2026-09-06',(25,20,20))[1],'test-release')
        self.assertEqual(resolve(r,'default','2028-01-01',(25,20,20))[1],'builtin-v2.1')

    def test_synthetic_future_and_invalid_releases_rejected(self):
        for update in ({'synthetic':True},{'max_label_end':'2026-10-01'},{'weights':{'default':dict(Q=90,G=90,V=90)}}):
            r=release()|update
            self.assertEqual(resolve({'releases':[r]},'default','2026-09-06',(25,20,20))[1],'builtin-v2.1')

    def test_no_synthetic_activation(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/'weights.json'
            with self.assertRaises(ValueError):activate({'synthetic':True},target)
            self.assertFalse(target.exists())

    def test_registry_atomic_write_and_read(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'weights.json';r={'schema_version':1,'releases':[]}
            write_json(path,r);self.assertEqual(read_registry(path),r)
            self.assertFalse(path.with_name('weights.json.tmp').exists())

    def test_real_release_activation_is_idempotent_and_preserves_audit(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'weights.json'
            registry={'schema_version':1,'releases':[]}
            report=dict(synthetic=False,profiles={'default':{'accepted':True,'proposed_weights':W}},
                        registry_hash=digest(registry),as_of='2026-09-05',max_label_end='2026-09-04',dataset_hash='test-fixture')
            report['calibration_id']=digest(report)
            first=activate(report,path);second=activate(report,path)
            self.assertEqual(first['status'],'activated');self.assertEqual(second['status'],'unchanged')
            self.assertEqual(len(read_registry(path)['releases']),1)
            self.assertEqual(len(list((path.parent/'weight_history').glob('*.json'))),1)
            tampered=copy.deepcopy(report);tampered['profiles']['default']['proposed_weights']={'Q':0,'G':100,'V':0}
            with self.assertRaises(ValueError):activate(tampered,path)

    def test_score_delta_separates_weight_and_data_effect(self):
        old=evaluate(data(),registry={'releases':[]})
        d=data();d['date']='2026-09-06'
        new=evaluate(d,registry={'releases':[release()]})
        delta=compute_delta(new,old)['deltas'][0]
        self.assertEqual(delta['data_effect'],0)
        self.assertNotEqual(delta['weight_effect'],0)
        self.assertAlmostEqual(delta['total_delta'],delta['data_effect']+delta['weight_effect']+delta['risk_and_rounding_effect'],places=2)

    def test_stale_asof_is_not_a_fresh_calibration(self):
        with self.assertRaises(ValueError):calibrate(small_dataset(),'2026-09-05',profiles=['default'])

    def test_scoring_reads_correct_weight_version(self):
        r={'schema_version':1,'releases':[release()]};s=stock()
        d=data([s]);d['date']='2026-09-06'
        scored=evaluate(d,registry=r)['stocks'][0]
        self.assertEqual(scored['weights_version'],'test-release')
        self.assertEqual({k:scored['weights'][k] for k in W},W)


if __name__=='__main__':unittest.main()
