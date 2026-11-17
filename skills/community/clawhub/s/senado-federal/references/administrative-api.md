# Senate administrative and transparency API

Base: `https://adm.senado.gov.br/adm-dadosabertos`

Swagger: `https://adm.senado.gov.br/adm-dadosabertos/swagger-ui/index.html`

This API covers CEAP expenses, housing assistance, offices, personnel, corporate-card transactions, procurement, and contractors.

## Response contract

Endpoints can return either a raw list or an envelope:

```json
{"statusCode": 200, "msg": "...", "data": []}
```

Accept the raw list or a list in `data`. For any other successful JSON shape, raise an API error. An invalid response must not become `[]`, because downstream sums would incorrectly report zero.

## Reliability

- Use a longer timeout than ordinary legislative calls when requesting large annual datasets.
- Retry timeouts, connection errors, HTTP 429, and 5xx with bounded exponential backoff.
- Validate the shape before caching.
- Cache a successful response only; retain the retrieval timestamp.

## CEAP

```text
GET /api/v1/senadores/despesas_ceaps/{ano}
```

Important fields include `codSenador`, `nomeSenador`, `tipoDespesa`, `fornecedor`, and `valorReembolsado`. Convert the monetary string or number deliberately, retain cent precision for financial totals, and state filters and treatment of refunds or cancellations.

## Other core routes

```text
GET /api/v1/senadores/auxilio-moradia
GET /api/v1/senadores/escritorios
GET /api/v1/servidores/remuneracoes/{ano}/{mes}
GET /api/v1/servidores/servidores
GET /api/v1/servidores/horas-extras/{ano}/{mes}
GET /api/v1/supridos/{ano}
GET /api/v1/supridos/transacoes/{ano}
GET /api/v1/contratacoes/contratos
GET /api/v1/contratacoes/licitacoes
GET /api/v1/contratacoes/notas_empenho
GET /api/v1/contratacoes/empresas
```

Check Swagger before relying on optional filter names because administrative query contracts can change independently of the legislative API.
