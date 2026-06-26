# Quark Drive 上传 API 技术笔记

## COS 上传域名问题

- `pds.quark.cn` 无公网 DNS 记录（NXDOMAIN）
- 实际上传需使用 `{bucket}.pds.quark.cn` 格式，如 `ul-sz.pds.quark.cn` → 解析到 `101.91.142.147`
- upload_pre 返回的 `upload_url` 是 `http://pds.quark.cn`，需去掉协议前缀后拼接 bucket

## 分片上传流程

```
1. POST /1/clouddrive/file/upload/pre
   - 必须字段: pdir_fid, file_name, format_type(MIME), size, md5, sha1, l_created_at, l_updated_at
   - 返回: task_id, upload_id, obj_key, bucket, auth_info, callback, metadata.part_size

2. POST /1/clouddrive/file/update/hash
   - 字段: md5, sha1, task_id
   - 若 finish=true → 秒传成功，无需上传

3. PUT https://{bucket}.pds.quark.cn/{obj_key}?partNumber=N&uploadId=X
   - 每个分片需先调 /1/clouddrive/file/upload/auth 获取 auth_key
   - auth_meta 格式（PUT）:
     PUT\n\n{mime}\n{date_gmt}\nx-oss-date:{date_gmt}\nx-oss-user-agent:aliyun-sdk-js/6.6.1\n/{bucket}/{obj_key}?partNumber={pn}&uploadId={uid}
   - Headers: Authorization=auth_key, Content-Type, Referer, x-oss-date, x-oss-user-agent

4. POST https://{bucket}.pds.quark.cn/{obj_key}?uploadId=X (CompleteMultipartUpload)
   - Body: XML <CompleteMultipartUpload><Part>...</Part></CompleteMultipartUpload>
   - auth_meta 格式（POST）:
     POST\n{content_md5_b64}\napplication/xml\n{date_gmt}\nx-oss-callback:{callback_b64}\nx-oss-date:{date_gmt}\nx-oss-user-agent:aliyun-sdk-js/6.6.1\n/{bucket}/{obj_key}?uploadId={uid}
   - Headers: Authorization, Content-MD5, Content-Type=application/xml, x-oss-callback, x-oss-date

5. Callback 由阿里云 PDS 自动触发 → 关联文件到网盘目录
```

## format_type 说明

format_type 字段必须是 MIME 类型字符串（如 `application/x-tar`、`text/plain`），不是数字。

## 参考实现

- `KKeygen/idv-login/tools/quark_upload.py` — Python 分片上传完整实现
- `Cp0204/quark-auto-save/quark_auto_save.py` — 分享/转存 API
