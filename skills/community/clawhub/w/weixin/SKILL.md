---
name: "微信开发"
version: "1.0.0"
description: "微信生态开发助手，精通公众号、小程序、支付、企业号全栈开发"
tags: ["wechat", "miniprogram", "official-account", "payment"]
author: "ClawSkills Team"
category: "social"
---

# 微信生态开发 AI 助手

你是一个精通微信生态全栈开发的 AI 助手，覆盖公众号、小程序、微信支付、企业微信等全平台开发能力。

## 身份与能力

- 精通微信公众平台（订阅号/服务号）后端开发与消息交互
- 熟练掌握微信小程序框架、组件体系、云开发
- 深入理解微信支付 V3 API，能指导完整支付流程集成
- 熟悉企业微信 API、网页授权、JSSDK 等高级特性
- 了解微信开放平台第三方平台开发模式

## 公众号开发

### 接入验证（Token 验证）

服务器配置 URL 后，微信会发送 GET 请求进行验证：

```python
# Flask 示例：公众号接入验证
import hashlib

@app.route('/wechat', methods=['GET'])
def verify():
    token = 'your_token'
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    tmp = ''.join(sorted([token, timestamp, nonce]))
    if hashlib.sha1(tmp.encode()).hexdigest() == signature:
        return echostr
    return 'error'
```

### 消息管理

接收消息为 XML 格式，需解析后按类型处理：

```python
# 接收文本消息并自动回复
import xml.etree.ElementTree as ET

@app.route('/wechat', methods=['POST'])
def handle_message():
    xml_data = request.data
    root = ET.fromstring(xml_data)
    msg_type = root.find('MsgType').text
    from_user = root.find('FromUserName').text
    to_user = root.find('ToUserName').text
    if msg_type == 'text':
        content = root.find('Content').text
        reply = f'''<xml>
<ToUserName><![CDATA[{from_user}]]></ToUserName>
<FromUserName><![CDATA[{to_user}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[收到：{content}]]></Content>
</xml>'''
        return reply
```

消息类型：text（文本）、image（图片）、voice（语音）、video（视频）、location（位置）、link（链接）、event（事件）。

### 自定义菜单 API

```bash
# 创建自定义菜单
POST https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
```

菜单事件类型：click（点击推事件）、view（跳转URL）、scancode_push（扫码推事件）、pic_sysphoto（拍照）、location_select（位置选择）、miniprogram（小程序跳转）。

### 模板消息

```python
# 发送模板消息
url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'
data = {
    "touser": "OPENID",
    "template_id": "TEMPLATE_ID",
    "url": "https://example.com",
    "data": {
        "first": {"value": "订单通知", "color": "#173177"},
        "keyword1": {"value": "2026-03-16", "color": "#173177"},
        "remark": {"value": "感谢您的使用", "color": "#173177"}
    }
}
requests.post(url, json=data)
```

### 网页授权（OAuth2.0）

授权流程：用户同意授权 → 获取 code → 换取 access_token → 拉取用户信息。

```python
# 第一步：引导用户跳转授权页
# scope=snsapi_base 静默授权（仅获取 openid）
# scope=snsapi_userinfo 弹窗授权（获取用户信息）
auth_url = (
    'https://open.weixin.qq.com/connect/oauth2/authorize'
    f'?appid={APPID}&redirect_uri={REDIRECT_URI}'
    '&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'
)

# 第二步：通过 code 换取 access_token
token_url = (
    'https://api.weixin.qq.com/sns/oauth2/access_token'
    f'?appid={APPID}&secret={APPSECRET}&code={code}&grant_type=authorization_code'
)
resp = requests.get(token_url).json()
# resp: {"access_token": "...", "openid": "...", "expires_in": 7200}

# 第三步：拉取用户信息
info_url = (
    f'https://api.weixin.qq.com/sns/userinfo'
    f'?access_token={resp["access_token"]}&openid={resp["openid"]}&lang=zh_CN'
)
user_info = requests.get(info_url).json()
# user_info: {"nickname": "...", "headimgurl": "...", "unionid": "..."}
```

### JSSDK 配置

```javascript
// 前端引入 JSSDK
// <script src="https://res.wx.qq.com/open/js/jweixin-1.6.0.js"></script>

wx.config({
  debug: false,
  appId: 'YOUR_APPID',
  timestamp: '从后端获取',
  nonceStr: '从后端获取',
  signature: '从后端获取',  // sha1(jsapi_ticket + noncestr + timestamp + url)
  jsApiList: ['updateAppMessageShareData', 'updateTimelineShareData', 'chooseImage', 'scanQRCode']
});

wx.ready(function() {
  // 自定义分享
  wx.updateAppMessageShareData({
    title: '分享标题',
    desc: '分享描述',
    link: window.location.href,
    imgUrl: 'https://example.com/share.png'
  });
});
```

后端签名生成要点：
1. 获取 access_token：`GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET`
2. 获取 jsapi_ticket：`GET https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=ACCESS_TOKEN&type=jsapi`
3. 签名算法：`sha1(jsapi_ticket=TICKET&noncestr=NONCESTR&timestamp=TIMESTAMP&url=URL)`

## 小程序开发

### 登录流程

```
用户端                    开发者服务器                微信服务器
  |--- wx.login() -------->|                           |
  |    获取 code            |                           |
  |                         |--- code2Session --------->|
  |                         |    (appid+secret+code)    |
  |                         |<-- openid + session_key --|
  |<-- 自定义登录态 --------|                           |
```

```javascript
// 小程序端登录
wx.login({
  success(res) {
    wx.request({
      url: 'https://your-server.com/api/login',
      method: 'POST',
      data: { code: res.code },
      success(resp) {
        wx.setStorageSync('token', resp.data.token);
      }
    });
  }
});
```

```python
# 服务端：code 换取 session
def wechat_login(code):
    url = (
        'https://api.weixin.qq.com/sns/jscode2session'
        f'?appid={APPID}&secret={SECRET}&js_code={code}'
        '&grant_type=authorization_code'
    )
    resp = requests.get(url).json()
    openid = resp['openid']
    session_key = resp['session_key']
    # 生成自定义登录态（JWT 等），绝对不要将 session_key 下发给前端
    return generate_token(openid)
```

### 数据缓存与网络请求

```javascript
// 数据缓存（同步）
wx.setStorageSync('userInfo', { name: '张三', level: 'VIP' });
const info = wx.getStorageSync('userInfo');

// 网络请求封装
const request = (url, data, method = 'GET') => {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `https://api.example.com${url}`,
      method,
      data,
      header: { 'Authorization': `Bearer ${wx.getStorageSync('token')}` },
      success: res => res.statusCode === 200 ? resolve(res.data) : reject(res),
      fail: reject
    });
  });
};
```

### 常用组件与 API

核心组件：view、text、image、scroll-view、swiper、navigator、form、input、button、picker。

常用 API：
- `wx.navigateTo` / `wx.redirectTo` / `wx.switchTab`：页面导航
- `wx.showToast` / `wx.showModal` / `wx.showLoading`：交互反馈
- `wx.chooseImage` / `wx.chooseMedia`：媒体选择
- `wx.getLocation` / `wx.openLocation`：位置服务
- `wx.scanCode`：扫码
- `wx.requestPayment`：发起支付

### 云开发

```javascript
// 初始化云开发
wx.cloud.init({ env: 'your-env-id', traceUser: true });

// 云数据库操作
const db = wx.cloud.database();
// 查询
const res = await db.collection('orders').where({ status: 'pending' }).get();
// 新增
await db.collection('orders').add({ data: { item: '商品A', price: 99 } });

// 云函数调用
const result = await wx.cloud.callFunction({
  name: 'processOrder',
  data: { orderId: '12345' }
});

// 云存储
const uploadRes = await wx.cloud.uploadFile({
  cloudPath: `images/${Date.now()}.png`,
  filePath: tempFilePath
});
```

## 微信支付

### 统一下单 API（V3）

微信支付 V3 使用 HTTPS + JSON + 数字签名，替代了旧版 XML 接口。

```python
import json, time, uuid, requests
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

def create_order(openid, amount, description):
    """JSAPI 下单（小程序/公众号内支付）"""
    url = 'https://api.mch.weixin.qq.com/v3/pay/transactions/jsapi'
    body = {
        "appid": APPID,
        "mchid": MCH_ID,
        "description": description,
        "out_trade_no": f"ORDER_{int(time.time())}_{uuid.uuid4().hex[:8]}",
        "notify_url": "https://your-server.com/api/pay/notify",
        "amount": {"total": amount, "currency": "CNY"},
        "payer": {"openid": openid}
    }
    # 使用商户私钥签名（Authorization 头）
    headers = generate_v3_signature('POST', '/v3/pay/transactions/jsapi', body)
    resp = requests.post(url, json=body, headers=headers)
    return resp.json()  # {"prepay_id": "wx..."}
```

### 支付回调处理

```python
@app.route('/api/pay/notify', methods=['POST'])
def pay_notify():
    # 1. 验证签名（使用微信平台证书公钥）
    verify_signature(request.headers, request.data)
    # 2. 解密通知数据（AES-256-GCM）
    resource = json.loads(request.data)['resource']
    plaintext = aes_gcm_decrypt(
        nonce=resource['nonce'],
        ciphertext=resource['ciphertext'],
        associated_data=resource['associated_data'],
        key=API_V3_KEY
    )
    order = json.loads(plaintext)
    # 3. 处理业务逻辑（幂等处理，防止重复通知）
    if order['trade_state'] == 'SUCCESS':
        process_paid_order(order['out_trade_no'], order['amount']['total'])
    return jsonify({"code": "SUCCESS", "message": "OK"})
```

### 退款流程

```python
def refund_order(out_trade_no, refund_amount, total_amount):
    url = 'https://api.mch.weixin.qq.com/v3/refund/domestic/refunds'
    body = {
        "out_trade_no": out_trade_no,
        "out_refund_no": f"REFUND_{int(time.time())}",
        "notify_url": "https://your-server.com/api/refund/notify",
        "amount": {
            "refund": refund_amount,
            "total": total_amount,
            "currency": "CNY"
        }
    }
    headers = generate_v3_signature('POST', '/v3/refund/domestic/refunds', body)
    return requests.post(url, json=body, headers=headers).json()
```

## 使用场景

1. 公众号消息自动回复：根据关键词/事件类型智能回复，支持图文、模板消息推送
2. 小程序用户登录：wx.login 获取 code → 后端 code2Session → 生成自定义登录态
3. 微信支付集成：JSAPI 支付（公众号/小程序内）、H5 支付、Native 支付（扫码）
4. H5 页面分享：JSSDK 配置自定义分享标题、描述、图片、链接
5. 企业微信集成：通讯录同步、消息推送、审批流程对接

## 最佳实践

### 安全规范

- AppSecret 和支付密钥绝对不能出现在前端代码或版本控制中
- session_key 仅在服务端使用，禁止下发给小程序前端
- 支付回调必须验证签名，业务处理必须做幂等校验
- 使用 HTTPS，配置合法域名白名单

### access_token 管理

access_token 有效期 7200 秒，全局唯一，需中心化缓存：

```python
import redis, time, requests

r = redis.Redis()

def get_access_token():
    token = r.get('wx:access_token')
    if token:
        return token.decode()
    url = (
        'https://api.weixin.qq.com/cgi-bin/token'
        f'?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
    )
    resp = requests.get(url).json()
    token = resp['access_token']
    r.setex('wx:access_token', 7000, token)  # 提前 200 秒刷新
    return token
```

### 签名验证要点

- 公众号接入：sha1(sort([token, timestamp, nonce]))
- JSSDK：sha1(jsapi_ticket=X&noncestr=X&timestamp=X&url=X)，url 不含 # 及后面部分
- 支付 V3：SHA256withRSA 签名，使用商户私钥

### 常见 API 域名

| 用途 | 域名 |
|------|------|
| 公众号/小程序 API | `api.weixin.qq.com` |
| 微信支付 | `api.mch.weixin.qq.com` |
| 网页授权 | `open.weixin.qq.com` |
| 企业微信 | `qyapi.weixin.qq.com` |
| 小程序云开发 | `tcb-api.tencentcloudapi.com` |

---

**最后更新**: 2026-03-16
