# 云展网 API CURL请求示范

---

## 登录获取 Token

```bash
curl -s -X POST "https://www.yunzhan365.com/api/user/get-token" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"用户名\",\"密码\":\"111111\"}"
```

---

## 文件上传

```bash
curl.exe -s -X POST "https://www.yunzhan365.com/api/common/upload-file" \
	-F "cptoken=*************" \
	-F "file=@C:/Users/test.pdf"
```

---

## 创建电子书

```bash
curl -s -X POST https://www.yunzhan365.com/api/book/add-book \
  -H "Content-Type: application/json" \
  -d "{
    \"cptoken\": \"your_token_here\",
    \"title\": \"我的电子书\",
    \"description\": \"这是一本精彩的电子书\",
    \"keyword\": \"科技,教育,阅读\",
    \"htmlTemplate\": \"Mobile\",
    \"phoneTemplate\": \"Mobile\",
    \"filePath\": \"[{\"link\": \"https://example.com/book.pdf\"}]\",
    \"bookConfig\": \"{\"loadingCaption\": \"Loading\", \"loadingCaptionColor\": \"0xdddddd"}\",
    \"engineType\": 2,
    \"convertMode\": -1,
    \"seo_boost\": 1
  }"
```

---

## 获取电子书转换进度

```bash
curl -s -X POST "https://www.yunzhan365.com/api/book/get-book-progress" \
  -H "Content-Type: application/json" \
  -d "{\"bookId\":\"电子书编号\",\"cptoken\":\"*************\"}"
```

---

## 获取指定书籍信息

```bash
curl -s -X POST "https://www.yunzhan365.com/api/book/get-book" \
  -H "Content-Type: application/json" \
  -d "{\"bookId\":\"电子书编号\",\"cptoken\":\"*************\"}"
```

---

## 获取用户信息

```bash
curl -s -X POST "https://www.yunzhan365.com/api/user/get-user" \
  -H "Content-Type: application/json" \
  -d "{\"cptoken\":\"*************\"}"
```

---

## 获取客服企业微信二维码

```bash
curl -s -X POST "https://www.yunzhan365.com/api/scrm/get-qrcode" \
  -H "Content-Type: application/json" \
  -d "{\"cptoken\":\"*************\"}"
```

---

## 删除电子书

```bash
curl -s -X POST "https://www.yunzhan365.com/api/folder/delete-folder-data" \
  -H "Content-Type: application/json" \
  -d "{\"books\":\"电子书编号\",\"cptoken\":\"*************\"}"
```

---

## 获取电子书列表

```bash
curl -s -X POST "https://www.yunzhan365.com/api/folder/list-folder-data" \
  -H "Content-Type: application/json" \
  -d "{\"operateId\":\"0\",\"cptoken\":\"*************\"}"
```

---