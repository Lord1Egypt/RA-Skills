# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Created on 2018-2-24

@author: Umeng Open Platform

"""

"""1. Import modules"""
import aop
import aop.api


#### Default settings, begin
"""2. Remote server

Remote server is the server domain or ip. e.g. 'gateway.open.umeng.com' for Umeng.

Set the default server by calling aop.set_default_server(remote_server).
You can also specify the server when newing an API request.
    e.g. req = aop.api.GetServerTimestampRequest(remote_server)

"""
aop.set_default_server('gateway.open.umeng.com')

"""3. ApiKey and secret

Set the default appinfo by calling aop.set_default_appinfo(apiKey, secret)
If you need to dynamically bind a different appinfo to the request, call req.set_appinfo(apiKey, secret)

"""
aop.set_default_appinfo(1000000, "aaaaaaaaaaaa") # default

"""4.Timestamp

Timestamp is milliseconds since midnight, January 1, 1970 UTC and needed by some APIs
due to security concerns.

Timestamp generator is a function taking three arguments: apiKey, secret, server domain.

Generally, there are three policy to generate the timestamp.
1) Use the local time every time.
    This is the default policy.
    Ensure that the time difference between your local machine and the server is tiny.
2) Use the server time every time. NOT RECOMMENDED!
    Just call aop.set_timestamp_generator(aop.get_server_timestamp).
    But remember that API '1/system/currentTimeMillis' will be called to get the server
    timestamp and there is a call limit for the API per 10-minutes.
3) Get the timestamp by the formula: timestamp = local_timestamp + timestamp_diff.
    "timestamp_diff" is the time difference between the server and the local that saved
    somewhere and periodically synchronized by calling aop.get_timestamp_diff(apiKey, secret, server).
    e.g.
        1> periodically synchronize timestamp_diff:
            timestamp_diff = aop.get_timestamp_diff(apiKey, secret, server)
        2> aop.set_timestamp_generator(lambda apiKey, secret, server: timestamp_diff + aop.get_local_timestamp())

"""
aop.set_timestamp_generator(custom_timestamp_generator)
#### Default settings, end

"""5. New an API request"""
req = aop.api.XxxRequest('gateway.open.umeng.com')
req = aop.api.XxxRequest() # Use the default server that set by aop.set_default_server(remote_server)
# req.set_need_https(False)

"""6. File upload (FileItem)

FileItem is used when the type of an API parameter is byte[].
And finally we will send a multipart request to the server.

Parameters
----------
filecontent: file-like-object(str/bytes/bytearray or an object that has read attribute)
    e.g. f = open('filepath', 'rb') ...  fileitem = aop.api.FileItem('filename', f)
    e.g. fileitem = aop.api.FileItem('filename', 'file_content_str')

"""
req.file_item_param = aop.api.FileItem(filename, filecontent)


"""7. Other parameters"""
req.other_param = param_json_value


"""8. Send the request

Raises
------
ApiError
    The remote server returned error and the error messages were successfully recognized.

AopError
    1) Failed before sending a request.
        e.g. Some of the required parameters missing.
    2) Failed to parse the returned results.

"""

try:
    resp = req.get_response()
    print(resp)
except aop.ApiError as e:
    print(e)
except aop.AopError as e:
    print(e)
except Exception as e:
    print(e)

"""9. Extend BaseApi for your own request

Raises
------
ApiError
    The remote server returned error and the error messages were successfully recognized.

AopError
    1) Failed before sending a request.
        e.g. Some of the required parameters missing.
    2) Failed to parse the returned results.

"""
from aop.api import BaseApi
class XXRequest(BaseApi):
    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)

    def get_api_uri(self):
        """
        Returns
        -------
        str
            version/namespace/name
        """
        return 'version/namespace/name'

    def need_sign(self):
        """True if _aop_signature is needed"""
        return False

    def need_timestamp(self):
        """True if _aop_timestamp is needed"""
        return False

    def need_auth(self):
        """True if access_token is needed"""
        return False

    def need_https(self):
        """True if to send https a request"""
        return False

    def is_inner_api(self):
        """True if not an open api. Usually false."""
        return False

    def get_multipart_params(self):
        """
        Returns
        -------
        list
            API parameters with type of byte[].
            A multipart request will be sent if not empty.
            e.g. returns ['image'] if the 'image' parameter's type is byte[].
                Then assign it as req.image = aop.api.FileItem('imagename.png', imagecontent)

        """
        return ['image']

    def get_required_params(self):
        """
        Names of required API parameters.
        System parameters(access_token/_aop_timestamp/_aop_signature) excluded.

        An AopError with message 'Required params missing: {"missing_param1_name", ...}'
        will be thrown out if some of the required API parameters are missing before a
        request sent to the remote server.

        """
        return []

req = XXRequest()
try:
    resp = req.get_response()
    print(resp)
except aop.ApiError as e:
    pass #log
except aop.AopError as e:
    pass #log
except Exception as e:
    pass #log