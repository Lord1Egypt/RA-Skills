# Marketplace setup / 市场安装与费用说明

Register at https://mro-api.iwilley.com/ and create your own API key.
Configure MRO_API_KEY using the host agent's secret or environment settings.
This key authenticates API requests; never paste it into SKILL.md or inquiry outputs.
MRO_API_BASE_URL is optional and defaults to https://mro-api.iwilley.com.

Remote MCP endpoint: https://mro-api.iwilley.com/v1/mcp.
If remote MCP is unavailable, run the included Python 3 REST client from the skill directory.
The REST client sends structured search conditions to the service. It does not itself
read or export Excel workbooks; that requires the host agent's spreadsheet capabilities.

Online matching and product-detail calls may consume account credits. Source discovery
is free. Agent-provider charges may also apply. Check the service for current terms;
this package does not promise any fixed free allowance or number of processable rows.

请先在平台注册并获取 API Key。用户询价中的检索条件、型号和规格会发送给 API
进行匹配；文件读取和结果导出由宿主 Agent 完成。平台 API 凭据与市场发布 Token
是不同凭据。商品适用性、最终价格、库存与交期由原始资料和供应商确认。

来源发现：`python3 scripts/mro_api_client.py sources`。
其他调用和批处理说明见 [portability.md](portability.md)。
