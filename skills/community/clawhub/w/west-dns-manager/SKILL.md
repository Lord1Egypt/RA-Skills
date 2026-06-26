# 西部数码域名解析管理

## 基本信息
- 技能名称：西部数码域名解析管理
- 技能 ID：west-dns-manager
- 版本：1.0.0
- 入口函数：skill.handler
- 运行环境：Python3
- 作者：OpenClaw

## 功能描述
通过西部数码 API 实现域名解析记录的添加、修改、删除。

## 输入参数
{
  "action": "add/modify/delete",
  "config": {
    "username": "西部数码用户名",
    "api_password": "API密码"
  },
  "dns_params": {
    "domain": "域名",
    "host": "主机头",
    "type": "A/CNAME/MX/TXT/AAAA",
    "value": "解析值",
    "old_value": "旧值(修改时必填)",
    "record_id": "解析ID(可选)"
  }
}

## 输出结果
{
  "success": true/false,
  "message": "提示信息",
  "data": {},
  "error": ""
}