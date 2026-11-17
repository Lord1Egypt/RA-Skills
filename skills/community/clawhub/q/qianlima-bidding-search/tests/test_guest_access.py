"""Guest routing, wire contracts and cross-mode continuations; no external network."""
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import qianlima_skill as r

QUERY = {'keywordGroups': [{'keywords': ['服务器'], 'matchScopes': [2]}]}
OFFICIAL = 'https://ai.qianlima.com/?source=bb3b4102f584028c3830df37'

class GuestAccessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.env = patch.dict(os.environ, {'QIANLIMA_API_KEY': '', 'QIANLIMA_MOCK_DIR': '',
                                          'QIANLIMA_SKILL_STATE_DIR': self.temp.name})
        self.env.start(); self.addCleanup(self.env.stop)
        self.calls = []
        self.transform = lambda data: data
        self.network = patch.object(r.urllib.request, 'urlopen', side_effect=self.respond)
        self.network.start(); self.addCleanup(self.network.stop)

    def respond(self, req, timeout):
        body = json.loads(req.data) if req.data else None
        self.calls.append((req.full_url.split('.com')[-1], body, dict(req.header_items())))
        free = req.full_url.endswith('/api/free/search')
        if body is None:
            data = {'id': '1', 'title': '详情'}
        else:
            page, size = body['currentPage'], 30 if free else body['numPerPage']
            has_key = bool(req.get_header('Qianlimaapikey'))
            data = {'rowCount': 900, 'pageCount': (900 + size - 1) // size,
                    'currentPage': page, 'numPerPage': size,
                    'list': [{'id': str(i), 'title': f'公告{i}', 'budgetAmount': 0,
                              'hasAnnex': False, 'secretField': 'excluded',
                              'url': f'https://www.qianlima.com/bid/{i}.html' if has_key else OFFICIAL}
                             for i in range((page - 1)*size + 1, page*size + 1)]}
            if free:
                data.update(accessMode='GUEST', viewablePageCount=10, maxViewableRows=300)
        data = self.transform(data)
        return contextlib.closing(io.BytesIO(json.dumps({'code': 200, 'data': data}).encode()))

    def call(self, command, *, query=None, mode='auto', context=None, ref=None, extra=()):
        args = [command, '--access-mode', mode]
        if query is not None: args += ['--query-json', json.dumps(query)]
        if context is not None: args += ['--context-json', json.dumps(context)]
        if ref is not None: args += ['--result-set-id', ref['follow_up']['result_set_id']]
        args += list(extra)
        out = io.StringIO()
        with contextlib.redirect_stdout(out): r.main(args)
        return json.loads(out.getvalue())

    def test_anonymous_default_strips_page_size_and_excess_fields(self):
        for size in [None, 30, 100, 999]:
            with self.subTest(size=size):
                out = self.call('search', query={**QUERY, 'numPerPage': size, 'hasAnnex': 0})
                self.assertTrue(out['ok'], out)
                self.assertEqual(self.calls[-1][0], '/api/free/search')
                self.assertNotIn('numPerPage', self.calls[-1][1])
                self.assertNotIn('Qianlimaapikey', self.calls[-1][2])
                self.assertEqual(out['effective_query']['numPerPage'], 30)
                self.assertEqual(out['cards'][0]['budgetAmount'], 0)
                self.assertNotIn('hasAnnex', out['cards'][0])
                self.assertNotIn('secretField', out['cards'][0])
                for card in out['cards']:
                    self.assertIn(f"[{card['title']}]({card['url']})", out['user_message'])
                self.assertEqual(out['total_count'], 900)
                self.assertEqual(out['viewable_page_count'], 10)

    def test_announcement_title_link_handles_brackets_without_changing_url(self):
        title = '[采购公告]服务器（一期）'
        url = 'https://ai.qianlima.com/?source=bb3b4102f584028c3830df37&ref=(notice)'
        self.transform = lambda data: {**data, 'list': [{**data['list'][0], 'title': title, 'url': url}]}
        out = self.call('search', query=QUERY)
        self.assertEqual(out['cards'][0]['url'], url)
        self.assertEqual(len(self.calls), 1)
        self.assertIn(r'1. [\[采购公告\]服务器（一期）](<' + url + '>)', out['user_message'])
        self.assertNotIn('[查看详情]', out['user_message'])

    def test_key_defaults_paid_and_explicit_free_keeps_key(self):
        os.environ['QIANLIMA_API_KEY'] = 'offline-guest-key'
        paid = self.call('search', query={**QUERY,'numPerPage':100})
        self.assertEqual(self.calls[-1][0], '/api/search')
        self.assertEqual(paid['returned_count'], 100)
        free = self.call('search', query=QUERY, mode='guest')
        self.assertEqual(self.calls[-1][0], '/api/free/search')
        self.assertEqual(self.calls[-1][2]['Qianlimaapikey'], 'offline-guest-key')
        self.assertIn('消耗账号积分', free['link_notice'])
        for path in Path(self.temp.name).rglob('*.json'):
            self.assertNotIn('offline-guest-key', path.read_text())

    def test_default_guest_becomes_paid_after_login_but_explicit_guest_remains(self):
        default = self.call('search', query=QUERY)
        explicit = self.call('search', query=QUERY, mode='guest')
        os.environ['QIANLIMA_API_KEY'] = 'offline-guest-key'
        out = self.call('next', ref=default)
        self.assertEqual(self.calls[-1][0], '/api/search')
        self.assertEqual(self.calls[-1][1]['numPerPage'], 30)
        self.assertEqual(out['cards'][0]['id'], '31')
        self.call('next', ref=explicit)
        self.assertEqual(self.calls[-1][0], '/api/free/search')
        self.call('search', query=QUERY)
        self.assertEqual(self.calls[-1][0], '/api/search')  # no global preference file

    def test_explicit_paid_overrides_old_guest_for_next_refine_and_restore(self):
        os.environ['QIANLIMA_API_KEY'] = 'offline-guest-key'
        for action in ['next', 'refine']:
            first = self.call('search', query=QUERY, mode='guest')
            out = self.call(action, ref=first, mode='authenticated', query={} if action == 'refine' else None)
            self.assertEqual(out['access_mode'], 'authenticated')
            self.assertEqual(self.calls[-1][0], '/api/search')
            again = self.call('next', ref=first)
            self.assertEqual(again['access_mode'], 'authenticated')
        ctx = {'result_type': 'project', 'effective_query': first['effective_query'], **first['follow_up']}
        self.call('next', context=ctx, mode='authenticated')
        self.assertEqual(self.calls[-1][0], '/api/search')

    def test_paid_100_to_free_page4_skips_ten_and_deduplicates(self):
        os.environ['QIANLIMA_API_KEY'] = 'offline-guest-key'
        first = self.call('search', query={**QUERY,'numPerPage':100})
        out = self.call('next', ref=first, mode='guest')
        self.assertEqual(self.calls[-1][1]['currentPage'], 4)
        self.assertNotIn('numPerPage', self.calls[-1][1])
        self.assertEqual([c['id'] for c in out['cards']], [str(i) for i in range(101,121)])
        self.assertEqual(out['follow_up']['delivered_position'], 120)
        out2 = self.call('next', ref=out)
        self.assertEqual(out2['cards'][0]['id'], '121')
        self.assertEqual(out2['access_mode'], 'guest')

    def test_guest_page_cap_and_switch_do_not_reset_position(self):
        os.environ['QIANLIMA_API_KEY'] = 'offline-guest-key'
        first = self.call('search', query={**QUERY, 'currentPage': 10}, mode='guest')
        n = len(self.calls)
        blocked = self.call('next', ref=first)
        self.assertEqual(blocked['error_code'], 'FREE_PAGE_LIMIT')
        self.assertEqual(len(self.calls), n)
        paid = self.call('next', ref=first, mode='authenticated')
        self.assertEqual(paid['cards'][0]['id'], '301')
        n = len(self.calls)
        self.assertEqual(self.call('next', ref=paid, mode='guest')['error_code'], 'FREE_PAGE_LIMIT')
        self.assertEqual(len(self.calls), n)

    def test_protocol_anomalies_preserve_success_but_disable_continuation(self):
        for patch_data in [{'accessMode':'UNKNOWN'}, {'numPerPage':100}, {'currentPage':2},
                           {'viewablePageCount':11}, {'maxViewableRows':301}, {'maxViewableRows':'invalid'}, {'viewablePageCount':'invalid'}, {'list':None}]:
            with self.subTest(patch_data=patch_data):
                self.transform = lambda data: {**data, **patch_data}
                out = self.call('search', query=QUERY)
                self.assertTrue(out['ok'])
                self.assertEqual(out['api_responses'][0]['response']['code'],200)
                self.assertTrue(out['continuation_blocked'])
                self.assertNotIn('follow_up', out)
                self.assertEqual(out['request_query']['sourceCode'],r.PACKAGE_SOURCE_CODE)

    def test_compact_free_response_supports_normal_continuation_without_fabricating_api_fields(self):
        self.transform = lambda data: {"list":data["list"],"rowCount":data["rowCount"],"pageCount":10}
        first = self.call('search',query=QUERY)
        self.assertTrue(first['ok'])
        self.assertNotIn('continuation_blocked',first)
        self.assertEqual(first['page_count'],30)
        self.assertEqual(first['api_page_count'],10)
        self.assertEqual(first['viewable_page_count'],10)
        self.assertNotIn('accessMode',first['api_responses'][0]['response']['data'])
        second = self.call('next',ref=first)
        self.assertEqual(second['cards'][0]['id'],'31')
        refined = self.call('refine',ref=second,query={'hasAnnex':0})
        self.assertEqual(refined['request_query']['currentPage'],1)
        context = {'result_type':'project','effective_query':second['effective_query'],**second['follow_up']}
        for path in Path(self.temp.name).rglob('*.json'): path.unlink()
        restored = self.call('next',context=context)
        self.assertEqual(restored['cards'][0]['id'],'61')
        for out in [first,second,refined,restored]:
            self.assertEqual(out['request_query']['sourceCode'],r.PACKAGE_SOURCE_CODE)
            self.assertNotIn('protocol_issues',out)

    def test_compact_free_response_zero_last_page_and_limit_remain_distinct(self):
        for total,page,expected in [(0,1,'NO_MORE_PAGES'),(45,2,'NO_MORE_PAGES'),(900,10,'FREE_PAGE_LIMIT')]:
            self.transform = lambda data, total=total: {"list":[c for c in data['list'] if int(c['id'])<=total],
                "rowCount":total,"pageCount":min(10,(total+29)//30)}
            out=self.call('search',query={**QUERY,'currentPage':page})
            self.assertNotIn('protocol_issues',out)
            n=len(self.calls)
            self.assertEqual(self.call('next',ref=out)['error_code'],expected)
            self.assertEqual(len(self.calls),n)

    def test_free_response_rejects_inconsistent_totals_and_explicit_null_metadata(self):
        for fields in [{'pageCount':4},{'rowCount':None},{'numPerPage':None},{'accessMode':None},
                       {'rowCount':20,'pageCount':1,'viewablePageCount':10}]:
            self.transform=lambda data,fields=fields:{**data,**fields}
            out=self.call('search',query=QUERY)
            self.assertTrue(out['ok'])
            self.assertTrue(out.get('continuation_blocked'),(fields,list(out)))
            self.assertNotIn('follow_up',out)


    def test_empty_list_is_success_not_limit(self):
        self.transform = lambda data: {**data, 'list':[], 'rowCount':0, 'pageCount':0, 'viewablePageCount':0}
        out = self.call('search', query=QUERY)
        self.assertTrue(out['ok']); self.assertEqual(out['cards'],[])
        self.assertNotIn('error_code',out)

    def test_http_json_errors_keep_cause_without_retry_wallet_or_fallback(self):
        os.environ['QIANLIMA_API_KEY'] = 'offline-guest-key'
        for http, code, message in [(401,10001,'Key 无效'),(429,429,'每日免费额度已用完'),(503,503,'免费查询暂时繁忙，请稍后再试。')]:
            body = {'code':code,'msg':message,'data':{'retryAfter':60}}
            error = urllib.error.HTTPError('https://test.invalid', http, 'error', {}, io.BytesIO(json.dumps(body).encode()))
            with patch.object(r.urllib.request,'urlopen',side_effect=error) as network:
                out = self.call('search',query=QUERY,mode='guest')
                self.assertFalse(out['ok']);self.assertEqual(out['error_code'],str(code))
                self.assertEqual(out['user_message'],message)
                self.assertEqual(out['limit_response'],{'retryAfter':60})
                self.assertEqual(network.call_count,1)

    def test_guest_unsupported_resources_never_request(self):
        for command, extra, query in [('detail', ['--id','1234567'],None), ('full-text',['--id','1234567'],None),
                                      ('search-purchase',[],{'keywords':['服务器']}),
                                      ('enterprise',['--kind','contacts'],{'companyName':'示例公司'})]:
            with self.subTest(command=command):
                out = self.call(command,query=query,mode='guest',extra=extra)
                self.assertFalse(out['ok']);self.assertEqual(out['error_code'],'FREE_CAPABILITY_UNAVAILABLE')
        self.assertEqual(self.calls,[])

    def test_paid_without_key_never_calls_backend(self):
        out = self.call('search',query=QUERY,mode='authenticated')
        self.assertEqual(out['error_code'],'MISSING_API_KEY');self.assertEqual(self.calls,[])

    def test_pending_cache_respects_target_fields_and_progress_without_request(self):
        os.environ['QIANLIMA_API_KEY']='offline-guest-key'
        first=self.call('search',query={**QUERY,'numPerPage':100})
        ctx={'result_type':'project','effective_query':first['effective_query'],
             **first['follow_up'],'delivered_position':20,'seen_ids':[str(i) for i in range(1,21)],
             'pending_cards':first['cards'][20:]}
        n=len(self.calls)
        out=self.call('next',context=ctx,mode='guest')
        self.assertEqual(len(self.calls),n)
        self.assertEqual(out['follow_up']['delivered_position'],50)
        self.assertEqual(out['cards'][0]['id'],'21')
        self.assertNotIn('secretField',out['cards'][0])
        self.assertNotIn('secretField',out['follow_up']['pending_cards'][0])
        out=self.call('next',ref=out)
        out=self.call('next',ref=out)
        self.assertEqual(out['follow_up']['delivered_position'],100)
        out=self.call('next',ref=out)
        self.assertEqual(self.calls[-1][1]['currentPage'],4)
        self.assertEqual(out['cards'][0]['id'],'101')

    def test_free_refine_preserves_mode_filters_and_resets_page(self):
        out=self.call('search',query={**QUERY,'hasAnnex':0,'currentPage':3},mode='guest')
        os.environ['QIANLIMA_API_KEY']='offline-guest-key'
        out=self.call('refine',ref=out,query={'numPerPage':None,'hasAgency':0})
        self.assertEqual(out['access_mode'],'guest')
        self.assertEqual(self.calls[-1][1]['currentPage'],1)
        self.assertEqual(self.calls[-1][1]['hasAnnex'],0)
        self.assertEqual(self.calls[-1][1]['hasAgency'],0)
        self.assertNotIn('numPerPage',self.calls[-1][1])


    def test_corrupt_access_metadata_never_guesses_paid_mode(self):
        os.environ['QIANLIMA_API_KEY']='offline-guest-key'
        for metadata in [{'access_mode':'unknown','access_mode_source':'explicit'},
                         {'access_mode':'guest'}, {'delivered_position':-1},
                         {'max_viewable_rows':900}, {'seen_ids':'1,2'}]:
            ctx={'result_type':'project','effective_query':{**QUERY,'currentPage':1,'numPerPage':30},**metadata}
            out=self.call('next',context=ctx)
            self.assertEqual(out['error_code'],'FOLLOW_UP_UNAVAILABLE',out)
        self.assertEqual(self.calls,[])

    def test_direct_page_eleven_never_requests(self):
        out=self.call('search',query={**QUERY,'currentPage':11})
        self.assertEqual(out['error_code'],'FREE_PAGE_LIMIT')
        self.assertEqual(self.calls,[])

    def test_reading_detail_does_not_change_explicit_free_list(self):
        os.environ['QIANLIMA_API_KEY']='offline-guest-key'
        first=self.call('search',query=QUERY,mode='guest')
        self.call('detail',extra=['--id','1234567'])
        out=self.call('next',ref=first)
        self.assertEqual(out['access_mode'],'guest')
        self.assertEqual(self.calls[-1][0],'/api/free/search')

    def test_one_time_paid_consent_is_followed_by_agent_restoring_free(self):
        os.environ['QIANLIMA_API_KEY']='offline-guest-key'
        first=self.call('search',query=QUERY,mode='guest')
        paid=self.call('next',ref=first,mode='authenticated')
        free=self.call('next',ref=paid,mode='guest')
        self.assertEqual(free['access_mode'],'guest')
        self.assertEqual(free['cards'][0]['id'],'61')

    def test_current_mode_overrides_old_complex_plan_and_never_enters_query(self):
        plan={'conditions':[{'id':'a','type':'keyword_group','value':QUERY['keywordGroups'][0]}],
              'logic_groups':[{'id':'root','operator':'AND','condition_ids':['a']}],
              'root_group_id':'root',
              'operations':[{'id':'op1','action':'search','data_source':'project','access_mode':'guest'}]}
        out=self.call('preflight-complex',mode='authenticated',extra=['--plan-json',json.dumps(plan)])
        self.assertTrue(out['ok'],out)
        self.assertEqual(out['approved_operations'][0]['access_mode'],'authenticated')
        self.assertNotIn('access_mode',out['approved_operations'][0]['query'])
        self.assertEqual(self.calls,[])

    def test_guest_seen_ids_filter_duplicate_rows_without_replaying(self):
        first=self.call('search',query=QUERY)
        self.transform=lambda data: {**data,'list':[{**data['list'][0],'id':'1'},*data['list'][1:]]}
        out=self.call('next',ref=first)
        self.assertEqual(out['returned_count'],29)
        self.assertNotIn('1',[c['id'] for c in out['cards']])
        self.assertEqual(out['follow_up']['delivered_position'],60)
        self.assertEqual(len(self.calls),2)

    def test_key_free_account_home_is_not_labeled_paid_detail(self):
        os.environ['QIANLIMA_API_KEY']='offline-guest-key'
        self.transform=lambda data: {**data,'list':[{**card,'url':'https://ai.atest.qianlima.com/'} for card in data['list']]}
        out=self.call('search',query=QUERY,mode='guest')
        self.assertTrue(out['ok'])
        self.assertNotIn('[查看详情]',out['user_message'])
        self.assertIn(f"[{out['cards'][0]['title']}]({out['cards'][0]['url']})",out['user_message'])
        self.assertNotIn('link_notice',out)
        self.assertEqual(out['link_contract_issues'],['官网入口缺少或不符合约定的 source 参数'])
        self.assertEqual(out['cards'][0]['url'],'https://ai.atest.qianlima.com/')
        self.assertEqual(out['api_responses'][0]['response']['data']['list'][0]['url'],'https://ai.atest.qianlima.com/')

    def test_invalid_key_anonymous_success_is_expected_without_retry_or_warning(self):
        os.environ['QIANLIMA_API_KEY']='offline-invalid-key'
        self.transform=lambda data:{**data,'list':[{**c,'url':OFFICIAL} for c in data['list']]}
        first=self.call('search',query=QUERY,mode='guest')
        second=self.call('next',ref=first)
        self.assertEqual(len(self.calls),2)
        for out in [first,second]:
            self.assertTrue(out['ok'])
            self.assertNotIn('link_contract_issues',out)
            self.assertNotIn('link_notice',out)
            self.assertNotIn('error_code',out)
            for card in out['cards']:
                self.assertIn(f"[{card['title']}]({card['url']})",out['user_message'])
        for path,body,headers in self.calls:
            self.assertEqual(path,'/api/free/search')
            self.assertEqual(headers['Qianlimaapikey'],'offline-invalid-key')

    def test_cached_anonymous_home_remains_home_after_login(self):
        first=self.call('search',query=QUERY)
        os.environ['QIANLIMA_API_KEY']='offline-guest-key'
        ctx={'result_type':'project','effective_query':first['effective_query'],**first['follow_up'],
             'delivered_position':10,'seen_ids':[str(i) for i in range(1,11)],'pending_cards':first['cards'][10:]}
        n=len(self.calls)
        out=self.call('next',context=ctx,mode='guest')
        self.assertEqual(len(self.calls),n)
        self.assertNotIn('link_notice',out)
        for card in out['cards']:
            self.assertIn(f"[{card['title']}]({card['url']})",out['user_message'])
        self.assertTrue(all(c['url']==OFFICIAL for c in out['cards']))
        self.assertNotIn('link_contract_issues',out)

    def test_source_is_sent_in_all_free_workflows_and_not_saved_as_filter(self):
        import qianlima_account
        self.assertEqual(r.PACKAGE_SOURCE_CODE, qianlima_account.PACKAGE_SOURCE_CODE)
        for key in ['', 'offline-source-key']:
            os.environ['QIANLIMA_API_KEY'] = key
            first = self.call('search', query=QUERY, mode='guest')
            second = self.call('next', ref=first)
            refined = self.call('refine', ref=second, query={'hasAnnex':0})
            context = {'result_type':'project', 'effective_query':second['effective_query'], **second['follow_up']}
            restored = self.call('next', context=context)
            for out in [first,second,refined,restored]:
                self.assertTrue(out['ok'],out)
                self.assertEqual(out['request_query']['sourceCode'],r.PACKAGE_SOURCE_CODE)
                self.assertNotIn('sourceCode',out['effective_query'])
                self.assertNotIn('numPerPage',out['request_query'])
            for path,body,headers in self.calls:
                if path == '/api/free/search':
                    self.assertEqual(body['sourceCode'],r.PACKAGE_SOURCE_CODE)
                    self.assertNotIn('Sourcecode',headers)
            for path in Path(self.temp.name).rglob('*.json'):
                self.assertNotIn('sourceCode',json.loads(path.read_text())['effective_query'])

    def test_caller_cannot_override_package_source(self):
        for field in ['sourceCode','source']:
            n=len(self.calls)
            out=self.call('search',query={**QUERY,field:'foreign'},mode='guest')
            self.assertFalse(out['ok'])
            self.assertEqual(len(self.calls),n)
        client=r.ApiClient(r.DEFAULT_BASE_URL,None)
        original={**QUERY,'currentPage':1,'sourceCode':'foreign'}
        client._request('POST','/api/free/search',original)
        self.assertEqual(self.calls[-1][1]['sourceCode'],r.PACKAGE_SOURCE_CODE)
        self.assertEqual(original['sourceCode'],'foreign')

    def test_source_is_not_added_to_authenticated_search(self):
        os.environ['QIANLIMA_API_KEY']='offline-source-key'
        out=self.call('search',query=QUERY)
        self.assertNotIn('sourceCode',out['request_query'])
        free=self.call('next',ref=out,mode='guest')
        self.assertEqual(free['request_query']['sourceCode'],r.PACKAGE_SOURCE_CODE)
        paid=self.call('next',ref=free,mode='authenticated')
        self.assertNotIn('sourceCode',paid['request_query'])

    def test_source_link_is_preserved_from_response_through_display_and_state(self):
        url=OFFICIAL+'&flow=free'
        self.transform=lambda data:{**data,'list':[{**c,'url':url} for c in data['list']]}
        out=self.call('search',query=QUERY)
        self.assertEqual(out['cards'][0]['url'],url)
        self.assertIn('('+url+')',out['user_message'])
        self.assertEqual(out['api_responses'][0]['response']['data']['list'][0]['url'],url)
        state=r.load_snapshot(None,out['follow_up']['result_set_id'])
        self.assertEqual(state['cards'][0]['url'],url)
        self.assertNotIn('link_contract_issues',out)

    def test_review_f1_anonymous_pending_preserves_original_url(self):
        url='https://ai.atest.qianlima.com/?source='+r.PACKAGE_SOURCE_CODE+'&flow=free'
        self.transform=lambda data:{**data,'list':[{**c,'url':url} for c in data['list']]}
        first=self.call('search',query=QUERY)
        ctx={'result_type':'project','effective_query':first['effective_query'],**first['follow_up'],
             'delivered_position':10,'seen_ids':[str(i) for i in range(1,11)],'pending_cards':first['cards'][10:]}
        count=len(self.calls)
        out=self.call('next',context=ctx)
        self.assertTrue(out['ok'],out)
        self.assertEqual(len(self.calls),count)
        self.assertTrue(all(c['url']==url for c in out['cards']))
        self.assertIn('('+url+')',out['user_message'])

    def test_review_f2_missing_pending_does_not_skip_undelivered_rows(self):
        first=self.call('search',query=QUERY)
        ctx={'result_type':'project','effective_query':first['effective_query'],**first['follow_up'],
             'delivered_position':10,'seen_ids':[str(i) for i in range(1,11)],'pending_cards':[]}
        count=len(self.calls)
        out=self.call('next',context=ctx)
        self.assertFalse(out['ok'],out)
        self.assertEqual(out['error_code'],'FOLLOW_UP_UNAVAILABLE')
        self.assertEqual(len(self.calls),count)

    def test_review_f3_explicit_choice_overrides_only_old_mode_metadata(self):
        os.environ['QIANLIMA_API_KEY']='offline-guest-key'
        first=self.call('search',query=QUERY,mode='guest')
        for mode in ['guest','authenticated']:
            for old in [{'access_mode':'UNKNOWN'}, {'access_mode_source':None}]:
                with self.subTest(mode=mode,old=old):
                    ctx={'result_type':'project','effective_query':first['effective_query'],**first['follow_up'],**old}
                    out=self.call('next',context=ctx,mode=mode)
                    self.assertTrue(out['ok'],out)
                    self.assertEqual(out['access_mode'],mode)
                    self.assertEqual(out['cards'][0]['id'],'31')
                    ctx['delivered_position']=-1
                    count=len(self.calls)
                    bad=self.call('next',context=ctx,mode=mode)
                    self.assertFalse(bad['ok'])
                    self.assertEqual(len(self.calls),count)

    def test_review_f4_free_error_fields_share_actual_reason(self):
        message='已达到免费可访问范围，匹配结果可能仍有更多。'
        body={'code':10004,'msg':message,'data':{}}
        error=urllib.error.HTTPError('https://test.invalid',400,'error',{},io.BytesIO(json.dumps(body).encode()))
        with patch.object(r.urllib.request,'urlopen',side_effect=error) as network:
            out=self.call('search',query=QUERY)
        self.assertFalse(out['ok'])
        self.assertEqual(out['message'],message)
        self.assertEqual(out['user_message'],message)
        self.assertIn(message,out['warnings'])
        self.assertFalse(any('查询条件没有通过' in w for w in out['warnings']))
        self.assertIn('未传时间参数，接口默认按近一个月查询。',out['warnings'])
        self.assertEqual(network.call_count,1)

    def test_review_f5_page_ten_explains_boundary_without_next_recommendation(self):
        out=self.call('search',query={**QUERY,'currentPage':10})
        self.assertTrue(out['ok'],out)
        self.assertNotIn('继续看下一批',out['user_message'])
        self.assertIn('免费',out['user_message'])
        self.assertIn('上限',out['user_message'])
        self.assertNotIn('next',out['follow_up']['allowed_actions'])
        self.assertEqual(out['total_count'],900)

    def test_review_progress_short_last_page_and_pending_at_free_cap(self):
        self.transform=lambda data:{**data,'rowCount':45,'pageCount':2,'viewablePageCount':2,
            'list':[c for c in data['list'] if int(c['id'])<=45]}
        last=self.call('search',query={**QUERY,'currentPage':2})
        ctx={'result_type':'project','effective_query':last['effective_query'],**last['follow_up']}
        count=len(self.calls)
        stopped=self.call('next',context=ctx)
        self.assertEqual(stopped['error_code'],'NO_MORE_PAGES')
        self.assertEqual(len(self.calls),count)
        self.transform=lambda data:data
        last=self.call('search',query={**QUERY,'currentPage':10})
        ctx={'result_type':'project','effective_query':last['effective_query'],**last['follow_up'],
             'delivered_position':280,'seen_ids':[str(i) for i in range(271,281)],
             'pending_cards':last['cards'][10:]}
        count=len(self.calls)
        out=self.call('next',context=ctx)
        self.assertTrue(out['ok'],out)
        self.assertEqual(out['follow_up']['delivered_position'],300)
        self.assertNotIn('next',out['follow_up']['allowed_actions'])
        self.assertIn('免费访问上限',out['user_message'])
        self.assertEqual(len(self.calls),count)

    def insufficient_responder(self, req, timeout):
        if req.full_url.endswith('/api/search'):
            self.calls.append(('/api/search', json.loads(req.data), dict(req.header_items())))
            return contextlib.closing(io.BytesIO(json.dumps({'code':10030,'msg':'积分余额不足','data':{}}).encode()))
        return self.respond(req, timeout)

    def test_insufficient_first_search_then_explicit_free_keeps_query_and_key(self):
        os.environ['QIANLIMA_API_KEY']='offline-insufficient-key'
        with patch.object(r.urllib.request, 'urlopen', side_effect=self.insufficient_responder):
            failed=self.call('search',query=QUERY)
        self.assertFalse(failed['ok']);self.assertEqual(failed['error_code'],'10030')
        self.assertEqual(sum(path=='/api/search' for path,_,_ in self.calls),1)
        self.assertFalse(any(path=='/api/free/search' for path,_,_ in self.calls))
        free=self.call('search',query=QUERY,mode='guest')
        self.assertTrue(free['ok'],free)
        self.assertEqual(self.calls[-1][1]['keywordGroups'],QUERY['keywordGroups'])
        self.assertNotIn('numPerPage',self.calls[-1][1])
        self.assertEqual(self.calls[-1][2]['Qianlimaapikey'],'offline-insufficient-key')
        following=self.call('next',ref=free)
        self.assertEqual(following['cards'][0]['id'],'31')
        self.assertEqual(following['access_mode'],'guest')

    def test_insufficient_next_does_not_advance_paid100_then_free_page4(self):
        os.environ['QIANLIMA_API_KEY']='offline-insufficient-key'
        first=self.call('search',query={**QUERY,'numPerPage':100})
        before={str(p):p.read_bytes() for p in Path(self.temp.name).rglob('*.json')}
        with patch.object(r.urllib.request, 'urlopen', side_effect=self.insufficient_responder):
            failed=self.call('next',ref=first)
        self.assertFalse(failed['ok']);self.assertEqual(failed['error_code'],'10030')
        self.assertEqual(before,{str(p):p.read_bytes() for p in Path(self.temp.name).rglob('*.json')})
        free=self.call('next',ref=first,mode='guest')
        self.assertTrue(free['ok'],free)
        self.assertEqual(self.calls[-1][1]['currentPage'],4)
        self.assertEqual(free['cards'][0]['id'],'101')
        self.assertEqual(free['follow_up']['delivered_position'],120)
        following=self.call('next',ref=free)
        self.assertEqual(following['cards'][0]['id'],'121')
        self.assertEqual(following['access_mode'],'guest')
        self.assertEqual(sum(path=='/api/search' for path,_,_ in self.calls),2)

    def test_mixed_plan_guest_keeps_executable_project_and_depth_pending(self):
        plan={'conditions':[{'id':'a','type':'keyword','value':['服务器']}],
              'logic_groups':[{'id':'root','operator':'AND','condition_ids':['a']}],
              'root_group_id':'root',
              'operations':[{'id':'free','action':'search','data_source':'project'},
                            {'id':'depth','action':'search','data_source':'purchase_intention'}]}
        valid=self.call('preflight-complex',mode='authenticated',extra=['--plan-json',json.dumps(plan)])
        self.assertEqual(len(valid['approved_operations']),2,valid)
        out=self.call('preflight-complex',mode='guest',extra=['--plan-json',json.dumps(plan)])
        self.assertTrue(out['ok'],out)
        self.assertEqual([op['id'] for op in out['approved_operations']],['free'])
        self.assertEqual(out['approved_operations'][0]['access_mode'],'guest')
        self.assertEqual(out['approved_business_calls'],1)
        self.assertTrue(any(item.get('operation_id')=='depth' for item in out['unresolved_conditions']))
        self.assertEqual(self.calls,[])
        delivered=self.call('search',query=out['approved_operations'][0]['query'],mode='guest')
        self.assertTrue(delivered['ok'],delivered)
        self.assertEqual(self.calls[-1][0],'/api/free/search')
        self.assertNotIn('Qianlimaapikey',self.calls[-1][2])
        plan['operations']=plan['operations'][1:]
        count=len(self.calls)
        blocked=self.call('preflight-complex',mode='guest',extra=['--plan-json',json.dumps(plan)])
        self.assertFalse(blocked['ok'],blocked)
        self.assertEqual(blocked['error_code'],'FREE_CAPABILITY_UNAVAILABLE')
        self.assertEqual(blocked['approved_operations'],[])
        self.assertEqual(blocked['approved_business_calls'],0)
        self.assertEqual(len(self.calls),count)

if __name__=='__main__': unittest.main()

