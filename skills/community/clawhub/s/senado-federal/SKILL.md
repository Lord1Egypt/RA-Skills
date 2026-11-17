---
name: senado-federal
description: "Research Brazil's Federal Senate using its official legislative and administrative open-data APIs. Use for senators, Senate bills and processes, votes, agendas, committees, speeches, mandates, CEAP expenses, contracts, or transparency records; use camara-deputados for Chamber-only records."
license: MIT
metadata:
  author: Daniel Marques
  version: "1.1.0"
---

# Senado Federal

Use official Senate data for factual legislative research and reproducible integrations.

- Legislative API: `https://legis.senado.leg.br/dadosabertos`
- Legislative Swagger: `https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html`
- Administrative API: `https://adm.senado.gov.br/adm-dadosabertos`
- Authentication: none

## Route the task

- Read [references/api-endpoints.md](references/api-endpoints.md) for legislative endpoints.
- Read [references/response-shapes.md](references/response-shapes.md) for nested JSON, historical cohorts, dates, and process identifiers.
- Read [references/administrative-api.md](references/administrative-api.md) for CEAP, personnel, procurement, and upstream-failure safeguards.
- Read [references/cross-house.md](references/cross-house.md) when a proposal moved between the Senate and Chamber.
- For a quick inspection, run `python3 scripts/senado.py <command>`.
- For reusable Python code, import `SenadoClient` or `SenadoAdmClient` from `senado_client.py`.

## Core workflow

1. Resolve the senator, matter, or legislative process to its official identifier before requesting details.
2. Use `/senador/lista/atual.json` only for current officeholders. For a historical cohort, query `/senador/lista/legislatura/{legislatura}/{legislatura}.json?exercicio=S`; the single-legislature route has produced a single record instead of the cohort.
3. Prefer `/processo` for searches by author and for cross-house status. The `autor` parameter on `/materia/pesquisa/lista` is not reliable.
4. Parse the documented key path for the endpoint and normalize a terminal object or list with `as_list`. Never use the first arbitrary list found by a depth-first search as a business result.
5. Preserve the distinction between `IdentificacaoProcesso` and a Senate `CodigoMateria`; they are not interchangeable.
6. For current-day queries, interpret “today” in `America/Sao_Paulo` and state the retrieval date when freshness matters.
7. Cite or return the exact API URL used when the answer needs to be auditable.

## Important contracts

- Most legislative endpoints accept a `.json` suffix; `/processo` search is queried without it.
- Senator speeches use `dataIni` and `dataFim` in `YYYYMMDD`. Query one calendar year at a time because broad multi-year ranges can fail or time out.
- Senator detail resources wrap results under endpoint-specific roots such as `DiscursosParlamentar`, `MateriasAutoriaParlamentar`, `MateriasRelatoriaParlamentar`, `VotacaoParlamentar`, `MembroComissaoParlamentar`, and `MandatoParlamentar`.
- A single result may be an object while multiple results are a list. Normalize only the expected terminal field.
- Administrative endpoints may return a raw list or `{ "data": [...] }`; reject other success shapes instead of silently treating them as empty.
- CEAP monetary values use `valorReembolsado`, not `valor`.

## Python clients

```python
from senado_client import SenadoAdmClient, SenadoClient

client = SenadoClient()
try:
    senadores = await client.buscar_senador_por_nome("nome")
    processos = await client.pesquisar_processos(
        autor=senadores[0]["IdentificacaoParlamentar"]["NomeParlamentar"],
        tramitando=True,
    )
    autorias = await client.get_autorias_senador(senadores[0]["IdentificacaoParlamentar"]["CodigoParlamentar"])
finally:
    await client.close()

adm = SenadoAdmClient()
try:
    despesas = await adm.get_ceap(2026)
    total = sum(float(item["valorReembolsado"]) for item in despesas)
finally:
    await adm.close()
```

## Output discipline

- Separate Senate data from interpretation.
- Include the matter identification, process ID, current situation, responsible body, and latest relevant movement when available.
- Treat “no records” and “the administrative API failed” as different outcomes.
- For expenses, state the year, field aggregated, currency treatment, and filtering criteria.
