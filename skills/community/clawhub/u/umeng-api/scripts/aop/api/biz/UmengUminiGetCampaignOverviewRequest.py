# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUminiGetCampaignOverviewRequest(BaseApi):
    """获取某推广活动的统计数据

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.umini&n=umeng.umini.getCampaignOverview&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.timeUnit = None
        self.fromDate = None
        self.toDate = None
        self.campaign = None
        self.pageSize = None
        self.pageIndex = None
        self.dataSourceId = None
        self.indicators = None

    def get_api_uri(self):
        return '1/com.umeng.umini/umeng.umini.getCampaignOverview'

    def get_required_params(self):
        return ['timeUnit', 'fromDate', 'toDate', 'campaign', 'dataSourceId', 'indicators']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return True

    def is_inner_api(self):
        return False
