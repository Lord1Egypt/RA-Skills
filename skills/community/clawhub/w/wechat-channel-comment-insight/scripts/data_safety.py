"""Public fields safe for local evidence; credentials stay in process memory."""
from decimal import Decimal
import urllib.parse

DROP = {"cookie", "authorization", "decodekey", "urltoken", "playbackurl", "exportid", "dynamicexportid",
        "temporaryurl", "appmsg_token", "pass_ticket", "access_token", "secret", "upstreamsecret", "headers"}


def public_data(value):
    if isinstance(value, dict):
        return {k: public_data(v) for k, v in value.items() if k.lower() not in DROP}
    if isinstance(value, list):
        return [public_data(v) for v in value]
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, str) and value.startswith(("https://", "http://")):
        u = urllib.parse.urlsplit(value)
        if u.hostname == "mp.weixin.qq.com":
            query = urllib.parse.parse_qsl(u.query, keep_blank_values=True)
            return urllib.parse.urlunsplit(("https", u.netloc, u.path,
                urllib.parse.urlencode([(k, v) for k, v in query if k in {"__biz", "mid", "idx", "sn"}]), ""))
        if u.hostname == "channels.weixin.qq.com" and "finder-preview" in u.path:
            return "[临时视频链接仅在采集内存中使用]"
        # Do not persist signed CDN / object-storage links from media payloads.
        query = urllib.parse.parse_qsl(u.query)
        if any(k.lower() in {"token", "key", "signature", "sig", "auth_key", "x-amz-signature"} for k, _ in query):
            return "[临时资源地址未保存]"
    return value
