# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengApptrackBackReportDataRequest(BaseApi):
    """为众盟定制开发的投放报表数据回传接口

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.apptrack&n=umeng.apptrack.backReportData&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.reportList = None

    def get_api_uri(self):
        return '1/com.umeng.apptrack/umeng.apptrack.backReportData'

    def get_required_params(self):
        return ['reportList']

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
