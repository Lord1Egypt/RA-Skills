import json, urllib.request, re

url = 'https://qt.gtimg.cn/q=hkHSI,hkHSTECH,hkHSCEI,hk00992,hk01088,hk06613,hk00981,hk00941,hk00005'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://gu.qq.com'})
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode('gbk')

# 获取MA20
ma20_url = 'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=hkHSI,day,,,20,qfq&r=0.1'
req2 = urllib.request.Request(ma20_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp2 = urllib.request.urlopen(req2, timeout=10)
    ma20data = resp2.read().decode()
    # 找close数组
    idx = ma20data.find('close')
    if idx >= 0:
        start = ma20data.find('[', idx)
        end = ma20data.find(']', start)
        closes_str = ma20data[start+1:end]
        closes = [float(x) for x in closes_str.split(',') if x.strip()]
        ma20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else None
        print(f'恒生MA20: {ma20:.2f}' if ma20 else 'MA20: N/A')
    else:
        print('MA20: N/A')
except Exception as e:
    print(f'MA20 Error: {e}')

# 解析行情
lines = [l for l in data.split(';') if l.strip()]
for line in lines:
    # 去掉 v_ 前缀
    idx = line.find('=')
    if idx < 0:
        continue
    code_part = line[:idx].strip()
    if code_part.startswith('v_'):
        code = code_part[2:]
    else:
        continue
    rest = line[idx+1].strip('"')
    fields = rest.split('~')
    if len(fields) > 35:
        name = fields[1]
        price = fields[3]
        yclose = fields[4]
        pct = fields[32]
        high = fields[33]
        low = fields[34]
        print(f'{code} | {name} | 现价:{price} | 昨收:{yclose} | 涨跌幅:{pct}% | 最高:{high} | 最低:{low}')
