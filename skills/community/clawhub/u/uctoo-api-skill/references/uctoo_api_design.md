# API版本 v3.0.0 Beta  

1. 采用RESTFul风格API。  
2. 遵循全栈模型同构UMI设计理念。[UMI参考文章](https://mp.weixin.qq.com/s/ja0jfsfkyIK2hdW6bDg2Ow)  
3. 采用jwt进行接口权限验证。需要权限调用的接口需先通过登录 /api/uctoo/auth/login 接口获取动态token，再以Bearer 动态token拼接成的字符串作为header的Authorization进行需要权限的接口调用。动态token过期时间默认为172800秒，如需定制修改可编辑根目录.env文件中ACCESS_TOKEN_VALIDITY_SEC字段。  
4. 单表对应的CURD操作默认API应以id字段作为数据一致性传输的主标识，如有特殊API不存在id字段的，则以动态token作为主标识。  
5. API不应输出的模型字段，可以使用hideSelectedObjectKeys()方法过滤掉不应输出的字段。需注意接口数据的信息安全。

## 数据表CURD标准接口规范  
以uctoo数据库entity表为例，介绍数据表CURD标准接口规范。多数据库API规则，将/uctoo/entity部分替换为对应的数据库名和表名/database_name/table_name  

### 路由规则  
完整接口URL地址是由.env文件中配置的API_URL拼接路由地址而成。路由地址遵循以下规范。  
1. 新增接口路由地址 /api/uctoo/entity/add ，post请求，需认证权限，body数据以json格式提交，成功调用返回新增的entity全部信息。  
2. 更新接口路由地址 /api/uctoo/entity/edit ，post请求，需认证权限，以id作为主键，body数据以json格式提交，成功调用返回更新后的entity全部信息。恢复一条软删除数据，可以通过调用更新接口，并将deleted_at字段传值"0"，以将deleted_at字段设置为空。支持多条数据编辑，body中以ids参数传编辑数据的多条主键数组以及编辑数据，例如 {ids: JSON.stringify(rowSelectState.selectedRowKeys)，link: "value", privacy_level:2}     
3. 删除接口路由地址 /api/uctoo/entity/del ，post请求，需认证权限，以id作为主键，默认为软删除，如需真删除，body中增加force参数设置为1，成功调用不返回任何数据。支持多条数据删除，body中以ids参数传删除数据的多条主键数组，例如 {ids: JSON.stringify(rowSelectState.selectedRowKeys)}    
4. 单条数据查询接口地址 /api/uctoo/entity/:id ，get请求，根据需要设置认证权限，以id作为主键查询，成功调用返回完整单条数据。  
5. 多条数据查询接口地址 /api/uctoo/entity/:limit/:page，get请求，根据需要设置认证权限，limit参数为一页的数据条数，page参数为页数，起始页数为0，成功调用返回多条完整数据数组。  
6. 多条数据查询接口地址 /api/uctoo/entity/:limit/:page/:skip，get请求，根据需要设置认证权限，limit参数为一页的数据条数，page参数为页数，起始页数为0，skip参数为跳过几条数据，起始条数为0，成功调用返回多条完整数据数组。    
7. 多条数据查询接口可支持prisma orm的where条件查询和orderBy排序，路由地址格式为 /api/entity/:limit/:page?sort=-privacy_level,id&filter={"link":{"endsWith":"opencangjie.com"}}。filter为json格式的查询参数，与prisma官方规范一致(see the [official documentation](https://www.prisma.io/docs/concepts/components/prisma-client/filtering-and-sorting#filtering))。sort为排序参数，负号为降序，如无sort排序，默认按created_at数据创建时间降序。  

### 接口状态代码
与HTTP/HTTPS协议状态代码约定一致（RFC2616）。例如，200为请求成功，400为客户端请求语法错误服务器无法理解，500为服务器处理错误。  

### 错误码  
接口返回错误时，将返回如下结构的错误对象
{
    "errno": "42002", errmsg: "verify code is invalid"
}
errno 错误码一般为 5 位数，errmsg 为错误描述  

### 接口文档
完整接口文档网址  
https://apifox.com/apidoc/shared/9a22079c-a59f-4b65-a7f6-678f0643e7f6/api-170720939

## websocket接口  
websocket接口路由地址以 /ws 开头，大部分为定制接口路由，暂无固定规范。可参考websocket目录中实现。
