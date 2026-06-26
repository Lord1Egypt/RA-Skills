# Quark Drive 分享/转存 API

## 创建分享

```
POST /1/clouddrive/share
Body: {
  "fid_list": ["<fid>"],
  "title": "分享标题",
  "url_type": 2,        // 1=公开链接, 2=有密码
  "expired_type": 2,    // 1=1天, 2=7天, 3=30天, 4=永久
  "passcode": "1234",   // 可选，设置提取码
  "expired_at": 1778594075925  // 可选，精确过期时间(ms)
}
返回: { task_id, task_resp: { share_id } }

查询分享详情:
POST /1/clouddrive/share/password
Body: { "share_id": "<share_id>" }
返回: { share_url, pwd_id, passcode }
```

## 转存他人分享

```
1. 获取 token:
POST /1/clouddrive/share/sharepage/token
Body: { "pwd_id": "<share_id>", "passcode": "1234", "support_visit_limit_private_share": true }
返回: { stoken }

2. 获取分享文件列表:
GET /1/clouddrive/share/sharepage/detail?pwd_id=<id>&stoken=<token>&pdir_fid=0

3. 转存:
POST /1/clouddrive/share/sharepage/save
Body: {
  "fid_list": [],           // 空=全部转存
  "fid_token_list": [],
  "to_pdir_fid": "<目标目录fid>",
  "pwd_id": "<share_id>",
  "stoken": "<token>",
  "pdir_fid": "0",
  "pdir_save_all": true,
  "scene": "link"
}
```

## 分享链接解析

正则: `https?://pan\.quark\.cn/s/([a-zA-Z0-9]+)`
提取码正则: `(?:提取码|密码)[：:\s]*([a-zA-Z0-9]+)`
