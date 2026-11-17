from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('runtime_v3', ROOT/'scripts/qianlima_skill.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

def project(**kw):
    return {'keywordGroups':[{'keywords':['空调'], 'matchScopes':[2,8]}], **kw}

class ApiV3Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.env = patch.dict(os.environ, {'QIANLIMA_API_KEY':'offline-regression-key', 'QIANLIMA_SKILL_STATE_DIR':self.tmp.name})
        self.env.start(); self.addCleanup(self.env.stop)

    def test_group_query_preserves_independent_scopes_and_filters(self):
        q=project(procurementCategories=[0,1],procurementMethods=[0,2],fundsSources=[1,5],hasAnnex=0)
        q['keywordGroups'].append({'keywords':['安装','改造'],'matchScopes':[8]})
        actual,_=r.normalize_query(q)
        for k,v in q.items(): self.assertEqual(actual[k],v)
        self.assertFalse({'keywords','keywordsSearchType','matchScopes','procurementMethod'} & actual.keys())

    def test_legacy_search_fields_rejected(self):
        for field,value in [('keywords',['空调']),('keywordsSearchType',2),('matchScopes',[2]),('procurementMethod',0)]:
            with self.subTest(field=field), self.assertRaises(r.SkillError): r.normalize_query(project(**{field:value}))

    def test_groups_no_silent_truncation_or_missing_scope(self):
        words=[str(i) for i in range(12)]
        q,_=r.normalize_query({'keywordGroups':[{'keywords':words,'matchScopes':[1]}]})
        self.assertEqual(q['keywordGroups'][0]['keywords'],words)
        for groups in [[],[{'keywords':['x']}],[{'keywords':[],'matchScopes':[2]}],[{'keywords':['x'],'matchScopes':[]}],[{'keywords':['x'],'matchScopes':[11]}],[{'keywords':['x'],'matchScopes':[2],'extra':1}]]:
            with self.subTest(groups=groups), self.assertRaises(r.SkillError): r.normalize_query({'keywordGroups':groups})

    def test_project_datetime_and_single_endpoint(self):
        q,_=r.normalize_query(project(beginTime='2026-08-31 12:30:00'))
        self.assertEqual(q['beginTime'],'2026-08-31 12:30:00')
        self.assertEqual(q['endTime'],'2026-09-30 12:30:00')
        q,_=r.normalize_query(project(endTime='2026-03-31'))
        self.assertEqual(q['beginTime'],'2026-02-28 00:00:00')
        self.assertEqual(q['endTime'],'2026-03-31 23:59:59')
        for begin,end in [('2026-02-30','2026-03-01'),('2026-09-01 25:00:00','2026-09-02'),('2026-09-01 10:00:00','2026-09-01 09:59:59')]:
            with self.subTest(begin=begin), self.assertRaises(r.SkillError): r.normalize_query(project(beginTime=begin,endTime=end))

    def test_purchase_and_expiring_have_separate_scopes(self):
        for fn, scopes in [(r.normalize_purchase_search_query,[1,2,8,10]),(r.normalize_expiring_search_query,list(range(1,11)))]:
            q,_=fn({'keywords':['设备'],'matchScopes':scopes})
            self.assertEqual(q['matchScopes'],scopes)

    def test_new_commands_exist(self):
        parser=r.build_parser()
        choices=next(a for a in parser._actions if hasattr(a,'choices') and isinstance(a.choices,dict)).choices
        self.assertTrue({'full-text','attachments','timeline','search-company'} <= choices.keys())

    def test_new_detail_fields_and_attachment_state(self):
        fields='xmNumber,threeLevelClassification,zhaoBiaoType,registrationBeginTime,tenderBeginTime,bidingAcquireTime,bidingEndTime,biddingCandidates'
        self.assertEqual(r.parse_fields(fields,'project'),fields.split(','))
        for value in [True,False,None]:
            card=r.card_view({'id':101,'hasAnnex':value})
            self.assertIn('hasAnnex',card)
            self.assertIs(card['hasAnnex'],value)

    def test_wallet_command_uses_new_contract_only(self):
        data={'balancePoints':1500,'frozenPoints':2,'availablePoints':1498,'sourceUrlUsage':{'used':3,'limit':30,'remaining':27,'resetAt':'2026-10-01 00:00:00'}}
        with patch.object(r.ApiClient,'entitlement',return_value=data):
            args=r.build_parser().parse_args(['entitlement'])
            payload=args.func(args)
        self.assertTrue(payload['ok'])
        self.assertEqual(payload['availablePoints'],1498)
        self.assertEqual(payload['sourceUrlUsage']['remaining'],27)
        self.assertFalse({'rights','version','area','walletStatus'} & payload.keys())
        self.assertIn('1498',payload['user_message'])

    def test_empty_array_transport_is_not_coerced_to_object(self):
        p=Path(self.tmp.name)/'attachments_101.json'
        p.write_text(json.dumps({'code':200,'data':[]}))
        client=r.ApiClient('https://example.invalid',None,self.tmp.name)
        actual=client._request('GET','/api/attachments/101')
        self.assertEqual(actual,[])

    def command(self, argv, response):
        calls=[]
        def request(client, method, path, query=None):
            calls.append((method,path,query))
            client.last_request_path=path; client.last_request_query=query
            return response
        with patch.object(r.ApiClient,'_request',request):
            args=r.build_parser().parse_args(argv)
            payload=args.func(args)
        return payload,calls

    def snapshot(self, source='project'):
        import uuid
        return r.save_search_snapshot(session_id=str(uuid.uuid4()),result_type=source,effective_query=project(),viewed_cards=[{'id':101,'title':'空调采购'}],total_count=1,page_count=1)

    def test_resource_direct_call_and_timeline_node_followup(self):
        snap=self.snapshot()
        context=['--session-id',snap['session_id'],'--result-set-id',snap['result_set_id'],'--project-ref','第1条']
        data={'projectId':101,'title':'空调采购','publishTime':'2026-09-01','content':'完整正文'}
        out,calls=self.command(['full-text',*context],data)
        self.assertEqual([(x[0],x[1]) for x in calls],[('GET','/api/fullText/101')])
        self.assertEqual(out['full_text']['content'],'完整正文')
        nodes=[{'id':202,'title':'空调中标','publishTime':'2026-09-02'}]
        out,calls=self.command(['timeline',*context],nodes)
        follow=out['follow_up']
        out,calls=self.command(['detail','--session-id',follow['session_id'],'--result-set-id',follow['result_set_id'],'--project-ref','第1条','--fields','title'],{'id':202,'title':'空调中标'})
        self.assertEqual(calls[0][1],'/api/detail/202')

    def test_resources_reject_wrong_source_before_request(self):
        snap=self.snapshot('purchase_intention')
        args=r.build_parser().parse_args(['attachments','--session-id',snap['session_id'],'--result-set-id',snap['result_set_id'],'--project-ref','第1条'])
        with patch.object(r.ApiClient,'_request') as request:
            try: out=args.func(args)
            except r.SkillError: pass
            else: self.assertFalse(out['ok'])
            request.assert_not_called()

    def test_company_query_and_candidates_have_distinct_pagination(self):
        data={'total':2,'currentPage':1,'pageSize':10,'list':[{'companyId':8,'companyName':'甲有限公司','registeredAddress':'北京','winningCount':0,'tenderingCount':4}]}
        out,calls=self.command(['search-company','--query-json',json.dumps({'companyName':' 甲 '})],data)
        self.assertEqual(calls,[('POST','/api/searchCompany',{'companyName':'甲','currentPage':1,'pageSize':10})])
        self.assertEqual(out['rows'][0]['companyName'],'甲有限公司')
        self.assertEqual(out['total_count'],2)

    def test_resource_response_wrong_id_is_preserved(self):
        snap=self.snapshot()
        args=['full-text','--session-id',snap['session_id'],'--result-set-id',snap['result_set_id'],'--project-ref','第1条']
        out,_=self.command(args,{'projectId':999,'content':'不属于该项目'})
        self.assertTrue(out['ok'])
        self.assertEqual(out['full_text']['projectId'],999)
        self.assertTrue(out['warnings'])

    def test_wallet_diagnosis_does_not_override_permission_error(self):
        wallet={'balancePoints':100,'frozenPoints':0,'availablePoints':100,'sourceUrlUsage':{'used':0,'limit':30,'remaining':30,'resetAt':None}}
        error=r.SkillError('10028','地区权限不足')
        base=r.failure_payload(stage='search',error=error)
        original=base['message']
        with patch.object(r.ApiClient,'entitlement',return_value=wallet):
            out=r.maybe_attach_entitlement_diagnosis(base,r.ApiClient('x',None),error,target_right='标讯查询')
        self.assertEqual(out['message'],original)
        self.assertEqual(out['error_code'],'10028')
        self.assertIn('100',out['user_message'])
        self.assertNotIn('额度正常',out['user_message'])

    def test_business_number_is_not_announcement_id(self):
        cards=[{"id":20260001,"title":"无关公告"}]
        self.assertEqual(r.resolve_project("项目编号 ABC-20260001",cards)["status"],"not_found")
        self.assertEqual(r.resolve_project("公告ID 20260001",cards)["status"],"matched")

    def test_detail_wrong_id_is_preserved_with_difference_notice(self):
        snap=self.snapshot()
        args=['detail','--session-id',snap['session_id'],'--result-set-id',snap['result_set_id'],'--project-ref','第1条','--fields','title']
        with patch.object(r.ApiClient,'entitlement',side_effect=r.SkillError('NETWORK_ERROR','offline')):
            out,calls=self.command(args,{'id':999,'title':'其他项目'})
        self.assertTrue(out['ok'])
        self.assertEqual(out['detail']['id'],999)
        self.assertIn('项目编号与所选项目不同',out['user_message'])

    def test_detail_survives_source_url_failure_without_replay(self):
        snap=self.snapshot()
        args=r.build_parser().parse_args(['detail','--session-id',snap['session_id'],'--result-set-id',snap['result_set_id'],'--project-ref','第1条','--fields','purchasingUnitLinkPhone,sourceUrl'])
        calls=[]
        def request(client, method, path, query=None):
            calls.append(path)
            if path.startswith('/api/detail/'):
                return {'id':101,'title':'空调采购','purchasingUnitLinkPhone':'010-12345678'}
            raise r.SkillError('10011','missing')
        with patch.object(r.ApiClient,'_request',request):
            out=args.func(args)
        self.assertFalse(out['ok'])
        self.assertTrue(out['partial_success'])
        self.assertEqual(out['detail']['purchasingUnitLinkPhone'],'010-12345678')
        self.assertIn('010-12345678',out['user_message'])
        self.assertEqual(calls,['/api/detail/101','/api/sourceUrl/101'])
        self.assertEqual(out['retry_fields'],['sourceUrl'])

    def test_new_response_types_preserve_api_facts(self):
        invalid=[{'biddingCandidates':[{'ranking':1,'providerName':'甲','amount':1}]},{'biddingCandidates':[{'ranking':2,'providerName':'甲','amount':False}]},{'threeLevelClassification':'货物'},{'xmNumber':123},{'registrationBeginTime':0}]
        for fields in invalid:
            with self.subTest(fields=fields): self.assertEqual(r.validate_detail_response({'id':101,**fields}),{'id':101,**fields})
        good={'id':101,'biddingCandidates':[{'ranking':2,'providerName':'甲','amount':0},{'ranking':3,'providerName':'乙','amount':None}],'threeLevelClassification':['货物']}
        self.assertEqual(r.validate_detail_response(good),good)
        resource=[{'projectId':101,'filepathId':1,'fileName':'a','fileUrl':123}]
        self.assertEqual(r.validate_resource_data('attachments',resource,'101'),resource)
        self.assertNotIn('hasAnnex',r.card_view({'id':101}))

    def test_old_state_migration_is_equivalent_and_invalid_groups_stop(self):
        snap=self.snapshot()
        snap['effective_query']={'keywords':['空调','安装'],'keywordsSearchType':2,'matchScopes':[2,8],'procurementMethod':0,'currentPage':1}
        r.save_snapshot(snap)
        loaded=r.load_snapshot(snap['session_id'],snap['result_set_id'])
        self.assertEqual(loaded['effective_query']['keywordGroups'],[{'keywords':['空调'],'matchScopes':[2,8]},{'keywords':['安装'],'matchScopes':[2,8]}])
        self.assertEqual(loaded['effective_query']['procurementMethods'],[0])
        snap['effective_query']={'keywordGroups':[{'keywords':['空调'],'matchScopes':[]}],'currentPage':1}
        r.save_snapshot(snap)
        with self.assertRaises(r.SkillError) as caught:r.load_snapshot(snap['session_id'],snap['result_set_id'])
        self.assertEqual(caught.exception.code,'RESULT_SET_CORRUPT')

    def test_normal_zero_results_never_call_wallet_for_any_search_source(self):
        for command,query,path in [('search',project(),'/api/search'),('search-purchase',{'keywords':['空调']},'/api/search/purchase'),('search-expiring',{'keywords':['空调']},'/api/search/expiring')]:
            with self.subTest(command=command):
                out,calls=self.command([command,'--query-json',json.dumps(query)],{'rowCount':0,'pageCount':0,'list':[]})
                self.assertTrue(out['ok'])
                self.assertEqual(out['total_count'],0)
                self.assertEqual(out['cards'],[])
                self.assertNotIn('entitlement_diagnosis',out)
                self.assertEqual([entry[1] for entry in calls],[path])

if __name__=='__main__': unittest.main()
