from __future__ import annotations
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from test_api_v3 import r,project


def wallet():
    return {'balancePoints':1500,'frozenPoints':2,'availablePoints':1498,'sourceUrlUsage':{'used':3,'limit':30,'remaining':27,'resetAt':'2026-10-01 00:00:00'}}

class WalletV3Tests(unittest.TestCase):
    def test_wallet_retains_reported_values_without_subscription_claims(self):
        out=r.normalize_entitlement_data(wallet())
        self.assertEqual(out,wallet())
        self.assertFalse({'version','area','rights','walletStatus'} & out.keys())

    def test_wallet_preserves_fields_and_types(self):
        bads=[{}, {'version':{},'area':'全国','rights':[]}]
        for field in ['balancePoints','availablePoints','frozenPoints']:
            for value in [None,True,-1,'100']:
                item=wallet();item[field]=value;bads.append(item)
        for item in bads:
            with self.subTest(item=item): self.assertEqual(r.normalize_entitlement_data(item),item)

    def test_wallet_preserves_reported_balance(self):
        item=wallet();item['availablePoints']=1500
        self.assertEqual(r.normalize_entitlement_data(item),item)

    def test_source_usage_missing_or_unknown_is_not_zero(self):
        for usage in [None,{}, {'used':0,'limit':30,'remaining':None}]:
            item=wallet();item['sourceUrlUsage']=usage
            self.assertEqual(r.normalize_entitlement_data(item),item)

    def test_zero_wallet_is_a_valid_fact(self):
        item=wallet();item.update(balancePoints=0,frozenPoints=0,availablePoints=0)
        self.assertEqual(r.normalize_entitlement_data(item)['availablePoints'],0)
        self.assertIn('可用积分：0',r.user_entitlement_message(item))

    def test_reset_timestamp_is_not_invented(self):
        item=wallet();item['sourceUrlUsage']['resetAt']=None
        text=r.user_entitlement_message(item)
        self.assertNotIn('重置时间',text)
        self.assertIn('27',text)

    def test_wallet_output_is_remaining_first_and_chinese(self):
        text=r.user_entitlement_message(wallet())
        self.assertTrue(text.startswith('当前可用积分：1498'))
        for word in ['version','rights','availablePoints','会员','套餐','有效期','不限']:self.assertNotIn(word,text)
        self.assertIn('北京时间',text)

    def test_entitlement_read_only_no_search_state_mutation(self):
        with tempfile.TemporaryDirectory() as tmp,mock.patch.dict(os.environ,{'QIANLIMA_SKILL_STATE_DIR':tmp}):
            before=Path(tmp)/'unchanged.json';before.write_text('{"keep":true}')
            with mock.patch.object(r.ApiClient,'entitlement',return_value=wallet()) as call:
                out=r.cmd_entitlement(r.build_parser().parse_args(['entitlement']))
            call.assert_called_once()
            self.assertEqual(before.read_text(),'{"keep":true}')
            self.assertEqual(len(list(Path(tmp).iterdir())),1)
            self.assertEqual(out['sourceUrlUsage']['remaining'],27)

    def test_diagnosis_once_preserves_original_error_every_current_code(self):
        for code in r.ENTITLEMENT_DIAGNOSIS_ERROR_CODES:
            with self.subTest(code=code):
                err=r.SkillError(code,'不输出原始服务提示')
                original=r.failure_payload(stage='detail',error=err)
                before=copy.deepcopy(original)
                client=mock.Mock();client.entitlement.return_value=wallet()
                result=r.maybe_attach_entitlement_diagnosis(original,client,err,target_right='标讯详情')
                client.entitlement.assert_called_once_with()
                for field in ['error_code','message','warnings']:self.assertEqual(result[field],before[field])
                self.assertTrue(result['user_message'].startswith(before['user_message']))
                self.assertNotIn('额度正常',result['user_message'])
                self.assertNotIn('升级订阅',result['user_message'])

    def test_no_diagnosis_for_auth_rate_network_parameter_or_removed_codes(self):
        for code in ['MISSING_API_KEY','10001','401','429','NETWORK_ERROR','10004','10020','10009','10029']:
            client=mock.Mock();err=r.SkillError(code,'error')
            r.maybe_attach_entitlement_diagnosis({'ok':False},client,err,target_right='标讯查询')
            client.entitlement.assert_not_called()

    def test_failed_diagnosis_does_not_retry(self):
        client=mock.Mock();client.entitlement.side_effect=r.SkillError('NETWORK_ERROR','failed')
        out=r.maybe_attach_entitlement_diagnosis({'ok':False,'error_code':'10030','user_message':'积分余额不足'},client,r.SkillError('10030','余额不足'),target_right='标讯查询')
        client.entitlement.assert_called_once_with()
        self.assertEqual(out['error_code'],'10030')
        self.assertFalse(out['entitlement_diagnosis']['checked'])
        self.assertTrue(out['user_message'].startswith('积分余额不足'))

    def test_local_presentation_errors_never_trigger_wallet(self):
        client=mock.Mock();client.entitlement.return_value=wallet()
        err=r.SkillError('INVALID_RESPONSE','数据不完整')
        out=r.maybe_attach_entitlement_diagnosis(r.failure_payload(stage='search',error=err),client,err,target_right='标讯查询')
        self.assertFalse(out['ok']);self.assertEqual(out['error_code'],'INVALID_RESPONSE')
        self.assertNotIn('entitlement_diagnosis',out)
        client.entitlement.assert_not_called()

    def test_source_diagnosis_only_reports_source_usage(self):
        data=r.build_entitlement_diagnosis(wallet(),'源网址','access_block')
        text=r.entitlement_diagnosis_message(data)
        self.assertIn('27',text);self.assertNotIn('1498',text)
        self.assertIn('2026-10-01',text)

    def test_current_errors_are_distinct(self):
        expected={'10028':'地区权限','10030':'积分余额不足','10031':'积分扣除失败','10032':'积分账户','10036':'本月','10037':'超时','10038':'处理中','10039':'价格','10040':'冲突','10041':'正文'}
        for code,label in expected.items():
            self.assertIn(label,r.public_error_summary(r.SkillError(code,'raw')))

if __name__=='__main__':unittest.main()
