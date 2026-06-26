# brijr/meta-mcp Tool Policy

## Scope lock
- Esta skill considera somente o MCP `brijr/meta-mcp`.
- Nenhum outro MCP de Ads e considerado parte da capacidade ativa.

## Confirmed tools from README
- `get_insights`
- `compare_performance`
- `export_insights`
- `create_campaign`
- `update_campaign`
- `pause_campaign`
- `resume_campaign`
- `create_ad_set`
- `list_ad_sets`
- `create_ad`
- `list_ads`
- `list_audiences`
- `create_custom_audience`
- `create_lookalike_audience`
- `get_audience_info`
- `list_ad_creatives`
- `create_ad_creative`
- `health_check`
- `get_ad_accounts`
- `get_campaigns`
- `get_token_info`
- `diagnose_campaign_readiness`
- `check_account_setup`

## Validation note
- O README do repositorio diz "25 comprehensive tools", mas a lista nomeada revisada em `2026-03-13` enumera 23 tools explicitas.
- Esta skill usa apenas as tools explicitamente nomeadas acima.
- A funcionalidade mencionando "delete campaigns" aparece na secao de features, mas nao existe tool nomeada de exclusao na lista oficial de tools. Portanto exclusao segue fora de escopo.

## Recommended use by intent
- Diagnostico: `health_check`, `get_ad_accounts`, `get_campaigns`, `get_insights`, `compare_performance`, `export_insights`, `list_ad_sets`, `list_ads`
- Estrutura: `create_campaign`, `create_ad_set`, `create_ad_creative`, `create_ad`
- Audiencia: `list_audiences`, `create_custom_audience`, `create_lookalike_audience`, `get_audience_info`
- Seguranca operacional: `diagnose_campaign_readiness`, `check_account_setup`, `get_token_info`
