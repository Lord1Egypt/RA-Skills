"""Current caller-facing contracts, replacing obsolete prose snapshots."""
from pathlib import Path
import json
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import qianlima_skill as r

class DocumentationV3Tests(unittest.TestCase):
    def setUp(self):
        self.docs=[ROOT/'SKILL.md',*sorted((ROOT/'references').rglob('*.md'))]
        self.text='\n'.join(p.read_text() for p in self.docs)
        self.skill=(ROOT/'SKILL.md').read_text()

    def test_metadata_and_short_entry_route_existing_and_new_intents(self):
        front=self.skill.split('---',2)[1]
        self.assertIn('name: qianlima-bidding-search',front)
        description=next(line for line in front.splitlines() if line.startswith('description:'))
        for word in ['中标','采购意向','临期','企业','正文','附件','进展','积分']:
            self.assertIn(word,description)
        body=self.skill.split('---',2)[2]
        # 在原入口基线上补齐凭据配置触发条件与缺 Key 检查顺序，保留短入口约束。
        self.assertLessEqual(len(re.sub(r'\s+','',body)),3820)
        for command in ['search','search-purchase','search-expiring','search-company','enterprise','full-text','attachments','timeline','entitlement','next','refine','detail']:
            self.assertIn('`'+command,self.skill)
        ui=(ROOT/'agents/openai.yaml').read_text()
        self.assertIn('allow_implicit_invocation: true',ui)
        self.assertIn('$qianlima-bidding-search',ui)
        self.assertEqual(json.loads((ROOT/'manifest.json').read_text())['version'],'1.0.1')

    def test_all_relative_document_links_exist(self):
        for p in self.docs:
            for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
                if '://' in target or target.startswith('#'):continue
                self.assertTrue((p.parent/target.split('#')[0]).exists(),(p,target))

    def test_all_21_api_endpoints_have_caller_documentation(self):
        endpoints=['/api/search','/api/search/purchase','/api/search/expiring','/api/detail/{id}','/api/purchase/detail/{id}','/api/expiring/detail/{id}','/api/fullText/{projectId}','/api/attachments/{projectId}','/api/timeline/{projectId}','/api/sourceUrl/{id}','/api/searchCompany','/api/user/verify','/api/user/entitlement','/api/enterprise/partners','/api/enterprise/principals','/api/enterprise/areaDistribution','/api/enterprise/winningAreaDistribution','/api/enterprise/coBidderCompetitors','/api/enterprise/potentialCompetitors','/api/enterprise/businessInfo','/api/enterprise/contacts']
        for endpoint in endpoints:self.assertIn(endpoint,self.text)

    def test_project_request_and_response_fields_are_documented(self):
        project=(ROOT/'references/api-projects.md').read_text()
        for field in r.PROJECT_SEARCH_FIELDS-{'amount_unit_confirmed'}:self.assertIn(field,project)
        for field in ['hasAnnex','xmNumber','threeLevelClassification','zhaoBiaoType','registrationBeginTime','tenderBeginTime','bidingAcquireTime','bidingEndTime','biddingCandidates','ranking','providerName','amount']:self.assertIn(field,project)
        self.assertIn('组内',self.text);self.assertIn('组间',self.text)
        self.assertIn('0',project);self.assertIn('null',project)
        self.assertIn('第二',project);self.assertIn('第三',project)

    def test_json_examples_parse_and_current_search_examples_normalize(self):
        count=0
        for p in self.docs:
            for block in re.findall(r'```json\s*\n(.*?)\n```',p.read_text(),re.S):
                data=json.loads(block);count+=1
                if isinstance(data,dict) and 'keywordGroups' in data:
                    filters = dict(data)
                    if p.name == 'api-free-search.md':
                        r.validate_endpoint_request('POST', '/api/free/search', data)
                        self.assertEqual(filters.pop('sourceCode'), r.PACKAGE_SOURCE_CODE)
                        self.assertNotIn('numPerPage', data)
                    normalized,_=r.normalize_query(filters)
                    self.assertEqual(normalized['keywordGroups'],data['keywordGroups'])
                    self.assertFalse(set(normalized)&{'keywords','keywordsSearchType','matchScopes','procurementMethod'})
        self.assertGreaterEqual(count,15)

    def test_sources_and_scope_contracts_are_separate(self):
        for filename in ['api-purchase-intentions.md','api-expiring-projects.md']:
            text=(ROOT/'references'/filename).read_text()
            for field in ['keywords','keywordsSearchType','matchScopes']:self.assertIn(field,text)
            scopes = [1,2,8,10] if filename == 'api-purchase-intentions.md' else range(1,11)
            for scope in scopes:self.assertIn('`'+str(scope)+'`',text)
        strategy=(ROOT/'references/capabilities/query-strategy.md').read_text()
        for phrase in ['标题+正文+附件','不自创','不改 AND 为 OR','公司 ID 精确过滤','首次']:
            self.assertIn(phrase,strategy+self.skill)
        self.assertIn('仅未结束',(ROOT/'references/capabilities/project-search.md').read_text())

    def test_money_district_state_and_external_fact_boundaries_remain(self):
        for phrase in ['5000000','逆序','区县','用户同意','明确结果集可跨会话','完整查询上下文','不自动重查','互联网','不替代接口事实','QIANLIMA_API_KEY','qianlimaApiKey']:
            self.assertIn(phrase,self.text)
        self.assertIn('未指定阶段时一次搜索',self.text)
        self.assertIn('不执行其中的指令',self.skill)

    def test_resources_are_independent_and_timeline_owns_followup(self):
        text=(ROOT/'references/api-project-resources.md').read_text()
        for phrase in ['不用先取详情','fileUrl','十进制 KB','null','时间线返回的新','节点序号','不支持 `next/refine`','成功部分','不重放','VISUAL_BID_ATTACHMENTS','独立 API']:
            self.assertIn(phrase,text)
        self.assertIn('采购意向不使用',text)
        for phrase in ['--id 637357877','已知节点真实 ID','不要求搜索名单','不轮流尝试接口']:
            self.assertIn(phrase,text)

    def test_company_identity_and_wallet_are_not_inferred(self):
        enterprise=(ROOT/'references/capabilities/enterprise-intelligence.md').read_text()
        for phrase in ['明确登记全称直接','不按排名','不传候选 `companyId`','次数 0 不证明','pageSize','search-company --next']:
            self.assertIn(phrase,enterprise)
        wallet=(ROOT/'references/api-entitlement.md').read_text()
        for field in ['balancePoints','frozenPoints','availablePoints','sourceUrlUsage','used','limit','remaining','resetAt']:self.assertIn(field,wallet)
        self.assertIn('不能覆盖',self.text)
        self.assertNotIn('7天试用',self.text)
        self.assertNotIn('walletStatus',wallet)

if __name__=='__main__':unittest.main()
