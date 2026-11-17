from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

class CliV3Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.env={**os.environ,'QIANLIMA_API_KEY':'offline-cli-key','QIANLIMA_SKILL_STATE_DIR':self.tmp.name}
        self.query={'keywordGroups':[{'keywords':['空调','新风'],'matchScopes':[2]},{'keywords':['安装','改造'],'matchScopes':[8,10]}],'procurementCategories':[0,1],'procurementMethods':[0,2],'fundsSources':[1,5],'hasAnnex':0,'hasAgency':0,'registrationStatus':0,'beginTime':'2026-09-01 10:00:00','endTime':'2026-09-14 18:30:00','numPerPage':2}

    def call(self,command,*args):
        proc=subprocess.run([sys.executable,str(ROOT/'scripts/qianlima_skill.py'),'--mock-dir',str(ROOT/'tests/fixtures'),command,*args],env=self.env,capture_output=True,text=True)
        out=json.loads(proc.stdout)
        self.assertTrue(out.get('ok'),out)
        return out

    def context(self,result):
        return ['--session-id',result['follow_up']['session_id'],'--result-set-id',result['follow_up']['result_set_id']]

    def test_new_fields_survive_next_and_refine_with_independent_groups(self):
        first=self.call('search','--query-json',json.dumps(self.query))
        second=self.call('next',*self.context(first))
        refined=self.call('refine',*self.context(second),'--query-json',json.dumps({'beginAmount':5000000}))
        for out in [first,second,refined]:
            for field,value in self.query.items():self.assertEqual(out['request_query'][field],value)
        self.assertEqual(second['request_query']['currentPage'],2)
        self.assertEqual(refined['request_query']['currentPage'],1)
        self.assertEqual(refined['request_query']['beginAmount'],5000000)

    def test_resource_cli_timeline_and_details_use_selected_project(self):
        first=self.call('search','--query-json',json.dumps(self.query))
        context=self.context(first)
        body=self.call('full-text',*context,'--project-ref','第1条')
        self.assertEqual(body['full_text']['projectId'],101)
        annex=self.call('attachments',*context,'--project-ref','第1条')
        self.assertEqual(annex['attachments'][0]['fileSize'],125.5)
        empty=self.call('attachments',*context,'--project-ref','第2条')
        self.assertEqual(empty['attachments'],[])
        timeline=self.call('timeline',*context,'--project-ref','第1条')
        detail=self.call('detail',*self.context(timeline),'--project-ref','第2条','--fields','title')
        self.assertEqual(str(detail['selected_project_id']),'103')
        self.assertNotEqual(timeline['follow_up']['result_set_id'],first['follow_up']['result_set_id'])
        self.assertNotIn('next',timeline['follow_up']['allowed_actions'])

    def test_company_paging_remains_separate_from_project_and_wallet(self):
        project=self.call('search','--query-json',json.dumps(self.query))
        first=self.call('search-company','--query-json',json.dumps({'companyName':'测试企业','pageSize':1}))
        second=self.call('search-company','--next',*self.context(first))
        self.assertEqual(first['rows'][0]['companyId'],1)
        self.assertEqual(second['rows'][0]['companyId'],2)
        self.assertEqual(second['request_query']['pageSize'],1)
        self.assertNotIn('numPerPage',second['request_query'])
        self.assertEqual(first['rows'][0]['winningCount'],0)
        self.assertEqual(self.call('entitlement')['availablePoints'],1498)
        detail=self.call('detail',*self.context(project),'--project-ref','第1条','--fields','xmNumber,bidingEndTime,biddingEndTime,biddingCandidates')
        self.assertEqual(detail['detail']['xmNumber'],'LAB-2026-001')
        self.assertNotEqual(detail['detail']['bidingEndTime'],detail['detail']['biddingEndTime'])
        self.assertEqual(detail['detail']['biddingCandidates'],[])

if __name__=='__main__':unittest.main()
