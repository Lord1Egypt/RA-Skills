# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUminiGetAllPropertyValueCountRequest(BaseApi):
    """获取某事件属性下全部属性值数据

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.umini&n=umeng.umini.getAllPropertyValueCount&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.timeUnit = None
        self.fromDate = None
        self.toDate = None
        self.propertyName = None
        self.pageIndex = None
        self.pageSize = None
        self.eventName = None
        self.dataSourceId = None

    def get_api_uri(self):
        return '1/com.umeng.umini/umeng.umini.getAllPropertyValueCount'

    def get_required_params(self):
        return ['timeUnit', 'fromDate', 'toDate', 'propertyName', 'eventName', 'dataSourceId']

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
