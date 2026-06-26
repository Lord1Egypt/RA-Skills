# ZoomEye 查询语法参考

## 目录
- [基础查询语法](#基础查询语法)
- [主机搜索语法](#主机搜索语法)
- [Web搜索语法](#web搜索语法)
- [高级查询技巧](#高级查询技巧)
- [常见查询示例](#常见查询示例)

## 基础查询语法

### 逻辑运算符
- `AND` - 与运算，两个条件同时满足
- `OR` - 或运算，满足其中一个条件
- `NOT` - 非运算，排除指定条件

### 通配符
- `*` - 匹配任意字符
- `?` - 匹配单个字符

### 模糊匹配
- `~` - 模糊匹配

## 主机搜索语法

### 端口查询
```
port:80          # 搜索开放80端口的主机
port:80,443      # 搜索开放80或443端口的主机
port:[80 TO 443] # 搜索端口范围在80-443之间的主机
```

### IP查询
```
ip:1.1.1.1                # 搜索指定IP
ip:1.1.1.0/24             # 搜索指定IP段
ip:1.1.1.1-2.2.2.2        # 搜索IP范围
```

### 应用/服务查询
```
app:nginx           # 搜索运行nginx服务的主机
app:"Apache httpd"  # 搜索运行Apache的主机
app:redis           # 搜索Redis服务
app:mysql           # 搜索MySQL服务
```

### 操作系统查询
```
os:linux            # 搜索Linux系统
os:windows          # 搜索Windows系统
os:ubuntu           # 搜索Ubuntu系统
os:centos           # 搜索CentOS系统
```

### 地理位置
```
country:cn          # 搜索中国的主机
country:us          # 搜索美国的主机
city:beijing        # 搜索北京的主机
city:"new york"     # 搜索纽约的主机
```

### ASN查询
```
asn:4134            # 搜索指定ASN的主机
```

### 服务标识
```
banner:ssh          # 搜索banner包含ssh的主机
banner:"SSH-2.0"    # 搜索特定SSH版本
```

## Web搜索语法

### 网站应用
```
app:wordpress       # 搜索WordPress站点
app:joomla          # 搜索Joomla站点
app:drupal          # 搜索Drupal站点
app:tomcat          # 搜索Tomcat服务
```

### 网站标题
```
title:"Index of"    # 搜索标题包含"Index of"的站点
title:login         # 搜索标题包含login的站点
```

### 网站关键词
```
keywords:admin      # 搜索关键词包含admin的站点
keywords:login      # 搜索关键词包含login的站点
```

### HTTP响应头
```
headers:server      # 搜索响应头包含server的站点
headers:"X-Frame-Options"  # 搜索特定响应头
```

### 网站内容
```
body:password       # 搜索页面内容包含password的站点
body:admin          # 搜索页面内容包含admin的站点
```

### SSL证书
```
ssl:google.com      # 搜索SSL证书包含google.com的站点
ssl:"Let's Encrypt" # 搜索特定CA颁发的证书
```

## 高级查询技巧

### 组合查询
```
port:80 AND app:nginx                    # 80端口且运行nginx
port:80 OR port:443                      # 80端口或443端口
app:redis AND port:6379                  # Redis服务且开放6379端口
country:cn AND port:80                   # 中国且开放80端口
os:linux NOT app:nginx                   # Linux系统但不运行nginx
```

### 精确匹配
```
app:"Apache httpd"                       # 精确匹配"Apache httpd"
title:"Welcome to nginx!"                # 精确匹配标题
```

### 模糊匹配
```
app:apache~                              # 模糊匹配apache
```

### 范围查询
```
port:[20 TO 25]                          # 端口范围20-25
```

## 常见查询示例

### 安全审计
```
# 搜索暴露的数据库服务
port:3306 AND app:mysql                  # MySQL暴露
port:5432 AND app:postgresql             # PostgreSQL暴露
port:27017 AND app:mongodb               # MongoDB暴露
port:6379 AND app:redis                  # Redis暴露

# 搜索暴露的管理后台
title:"admin login"                      # 管理员登录页面
app:phpmyadmin                           # phpMyAdmin
app:tomcat AND port:8080                 # Tomcat管理界面

# 搜索存在风险的配置
title:"Index of /"                       # 目录遍历
app:ftp AND port:21                      # FTP服务
```

### 资产测绘
```
# 搜索特定组织的资产
org:google                               # Google的资产

# 搜索特定CDN
headers:"Cloudflare"                     # 使用Cloudflare的站点

# 搜索特定技术栈
app:nginx AND app:mysql                  # Nginx + MySQL架构
app:tomcat AND os:linux                  # Linux上的Tomcat
```

### 漏洞资产发现
```
# Apache Struts2
app:"Apache Struts2"                     # Struts2框架

# Shiro反序列化
headers:"rememberMe"                     # Shiro特征

# Spring Boot
app:"Spring Boot"                        # Spring Boot应用

# WebLogic
app:weblogic                             # WebLogic服务
port:7001 AND app:weblogic              # WebLogic默认端口
```

### 物联网设备
```
# 摄像头
app:webcam                               # 网络摄像头
app:dvr                                  # DVR设备

# 路由器
app:router                               # 路由器设备

# 打印机
app:printer                              # 网络打印机
```

## 注意事项

1. **查询限制**：免费用户有查询次数限制，建议精确查询语法以减少消耗
2. **引号使用**：包含空格的查询词需要用引号包裹
3. **大小写敏感**：查询语法不区分大小写，但查询内容区分大小写
4. **特殊字符**：包含特殊字符的查询需要转义或使用引号
5. **分页查询**：每页默认返回20条结果，大量数据需要分页获取
