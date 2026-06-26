# Approval Matrix

## Classification

### read-only
- `health_check`
- `get_ad_accounts`
- `get_campaigns`
- `get_insights`
- `compare_performance`
- `export_insights`
- `list_ad_sets`
- `list_ads`
- `list_audiences`
- `get_audience_info`
- `list_ad_creatives`
- `get_token_info`
- `diagnose_campaign_readiness`
- `check_account_setup`

### safe-within-limits
- `pause_campaign`
- `resume_campaign` when used to restore a previously approved campaign or protect delivery
- `update_campaign` for metadata-only changes or budget reduction
- `create_campaign` only if the output is `PAUSED`
- `create_ad_set` only under an already approved structure and with a review plan
- `create_ad` and `create_ad_creative` only for approved tests or paused builds

### approval-required
- `create_campaign` intended to go live
- `update_campaign` changing objective, budget above `10%`, key scheduling logic or multiple critical variables
- `create_ad_set` introducing a new targeting thesis, remarketing window or tracking dependency
- `create_ad` or `create_ad_creative` with a new offer, promise or compliance-sensitive angle
- `create_custom_audience`
- `create_lookalike_audience`

### forbidden
- qualquer acao de exclusao, billing, permissions ou business settings
- qualquer mudanca apoiada em tool nao confirmada no `brijr/meta-mcp`

## Budget limits
- Aumento autonomo maximo: `10%`
- Frequencia maxima do aumento autonomo: `1x a cada 24h por ativo`
- Requisito minimo: ativo estavel, sem tracking suspeito e sem queda recente de qualidade

## Change thresholds that force approval
- mais de uma variavel critica mudando ao mesmo tempo
- troca de objetivo
- alteracao do evento de conversao
- mudanca de audiencia com impacto estrutural
- tentativa de sair do escopo de `PAUSED` para `ACTIVE`
