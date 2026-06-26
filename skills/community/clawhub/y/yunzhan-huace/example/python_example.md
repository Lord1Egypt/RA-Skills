# 云展网 API CURL请求示范

---

## 登录获取 Token

```python
import requests

url = "https://www.yunzhan365.com/api/user/get-token"
headers = {"Content-Type": "application/json"}
data = {"username": "您的用户名", "密码": "您的密码"}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    if result["code"] == "OK":
        token = result["data"]["token"]
        print(f"登录成功")
        ### 保存token供后续使用
    else:
        print(f"接口返回错误: {result['msg']}")
else:
    print(f"HTTP请求失败: {response.status_code}")
```

---

## 文件上传

```python
import requests

### 配置参数
cptoken = "*************"  # 替换为您的token
file_path = "C:/Users/test.pdf"

### 准备请求
url = "https://www.yunzhan365.com/api/common/upload-file"
files = {'file': open(file_path, 'rb')}
data = {'cptoken': cptoken}

### 发送请求
response = requests.post(url, files=files, data=data)

### 关闭文件
files['file'].close()

### 处理响应
if response.status_code == 200:
    result = response.json()
    if result['code'] == 'OK':
        file_info = result['data']
        print(f"上传成功！")
        
        ### 完整URL
        full_url = f"https:{file_info['fileSrc']}"
    else:
        print(f"上传失败: {result['msg']}")
else:
    print(f"请求失败: {response.status_code}")
```

---

## 创建电子书

```python
import requests
import json

### 配置参数
cptoken = "your_token_here"
title = "我的电子书"
description = "这是一本精彩的电子书"
keyword = "科技,教育,阅读"
file_path_link = "https://example.com/book.pdf"

### 构建请求数据
data = {
    "cptoken": cptoken,
    "title": title,
    "description": description,
    "keyword": keyword,
    "htmlTemplate": "Mobile",
    "phoneTemplate": "Mobile",
    "filePath": json.dumps([{"link": file_path_link}]),
    "bookConfig": json.dumps({
        "loadingCaption": "Loading",
        "loadingCaptionColor": "0xdddddd"
    }),
    "engineType": 2,
    "convertMode": -1,
    "seo_boost": 1
}

headers = {"Content-Type": "application/json"}

### 发送请求
response = requests.post(
    "https://www.yunzhan365.com/api/book/add-book",
    headers=headers,
    json=data
)

### 处理响应
if response.status_code == 200:
    result = response.json()
    if result['code'] == 'OK':
        book_info = result['data']
        print(f"创建成功！")
        bookId=book_info['bookId']
    else:
        print(f"创建失败: {result['msg']}")
else:
    print(f"请求失败: {response.status_code}")
```

---

## 获取电子书转换进度

```python
import requests
import time

def check_progress(cptoken, book_id):
    """简单版本：查询进度"""
    url = "https://www.yunzhan365.com/api/book/get-book-progress"
    data = {"bookId": book_id, "cptoken": cptoken}
    
    response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == "OK":
            status = int(result.get("convertStatus"))
            progress = int(result.get("convertProgress"))
            
            status_map = {-3:"配置生成中", -2:"上传失败", -1:"上传中", 
                         0:"未分配", 1:"已分配", 2:"确认中", 3:"超时", 
                         4:"异常", 5:"✅成功", 6:"❌失败"}
            
            print(f"状态: {status_map.get(status, '未知')} | 进度: {progress}%")
            return status == 5  # 返回是否成功
    return False

### 使用示例
cptoken = "*************"
book_id = "3439934"

### 轮询直到完成
while True:
    if check_progress(cptoken, book_id):
        print("电子书转换完成！")
        break
    time.sleep(3)  # 每3秒检查一次
```

---

## 获取指定书籍信息

```python
import requests

def get_book_info(cptoken, bookId):
    """获取指定书籍信息"""
    url = "https://www.yunzhan365.com/api/book/get-book"
    data = {"bookId": bookId, "cptoken": cptoken}
    
    response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == "OK":
            return result['data']
		        
    print("获取失败")
    return [];

# 使用示例
cptoken = "*************"
getbook = get_book_info(cptoken,bookId)
bookId=getbook['bookId']
book_url=getbook['book_url']
domain_url=getbook['domain_url']
thumbnailUrl=getbook['thumbnailUrl']
auditStatus=getbook['auditStatus']
```

---

## 获取用户信息

```python
import requests

def get_user_info(cptoken):
    """获取用户信息"""
    url = "https://www.yunzhan365.com/api/user/get-user"
    data = {"cptoken": cptoken}
    
    response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == "OK":
            return result['data']
		        
    print("获取失败")
    return []

# 使用示例
cptoken = "*************"
getuser = get_user_info(cptoken)
userId=getuser['userId']
uName=getuser['uName']
userImg=getuser['userImg']
uType=getuser['uType']
add_wechat=getuser['add_wechat']
```

---

## 获取客服企业微信二维码

```python
import requests

def get_qrcode(cptoken):
    """获取客服企业微信二维码"""
    url = "https://www.yunzhan365.com/api/scrm/get-qrcode"
    data = {"cptoken": cptoken}
    
    response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == "OK":
            return result['data']
    print("获取失败")
    return []

# 使用示例
cptoken = "*************"
getQrcode = get_qrcode(cptoken)
qrcode = getQrcode['qrcode']
```

---

## 删除电子书

```python
import requests

def delete_books(cptoken, books):
    """
    删除电子书（简洁版）
    
    Args:
        cptoken: 用户token
        books: 电子书编号，可以是字符串、整数或列表
    """
    url = "https://www.yunzhan365.com/api/folder/delete-folder-data"
    
    ### 处理books参数
    if isinstance(books, (list, tuple)):
        books_str = ",".join(str(b) for b in books)
    else:
        books_str = str(books)
    
    data = {
        "books": books_str,
        "cptoken": cptoken
    }
    
    response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == "OK":
            print(f"✅ 删除成功: {result['msg']}")
            return True
        else:
            print(f"❌ 删除失败: {result.get('msg', '未知错误')}")
            return False
    else:
        print(f"❌ 请求失败: {response.status_code}")
        return False

### 使用示例
cptoken = "*************"
bookId = ****
delete_books(cptoken, "bookId")

```

---

## 获取电子书列表

```python
import requests

def get_books_list(cptoken, operate_id="0"):
    """获取电子书列表"""
    url = "https://www.yunzhan365.com/api/folder/list-folder-data"
    data = {"operateId": operate_id, "cptoken": cptoken}
    
    response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == "OK":
            books = result.get("data", {}).get("books", [])
            print(f"共找到 {len(books)} 本电子书")
            return books
    
    print("获取失败")
    return []

# 使用示例
cptoken = "*************"
books = get_books_list(cptoken)

```

---