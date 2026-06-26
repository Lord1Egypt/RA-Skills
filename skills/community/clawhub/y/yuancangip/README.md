需要配置mcpServers中的ip-data项，示例如下：
{
  "mcpServers": {
    "ip-data": {
      "type": "http",
      "url": "http://39.108.187.200:5210/yc_data/get_ip_data",
      "headers": {
        "Authorization": "Bearer sk-token"
      }
    }
  }
}

token需要求用户自行替换为实际的访问令牌，确保请求能够成功认证并获取数据。
token需要进行充值才能使用，查询一次扣一次，充值方式请参考：https://www.yuancangip.com/