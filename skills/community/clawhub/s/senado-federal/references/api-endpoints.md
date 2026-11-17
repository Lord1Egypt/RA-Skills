# Senate legislative API endpoint reference

Base: `https://legis.senado.leg.br/dadosabertos`

This is a task-oriented map of verified core endpoints. Consult the [official Swagger](https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html) for the complete current catalog. Contracts were checked on 2026-08-23.

## Senators

| Endpoint | Result or purpose |
|---|---|
| `GET /senador/lista/atual.json` | Current officeholders |
| `GET /senador/afastados.json` | Senators on leave |
| `GET /senador/lista/legislatura/{leg}/{leg}.json?exercicio=S` | Historical cohort that exercised the mandate |
| `GET /senador/{codigo}.json` | Profile |
| `GET /senador/{codigo}/mandatos.json` | Mandates |
| `GET /senador/{codigo}/filiacoes.json` | Party affiliations |
| `GET /senador/{codigo}/cargos.json` | Positions |
| `GET /senador/{codigo}/comissoes.json` | Committee memberships |
| `GET /senador/{codigo}/liderancas.json` | Leadership roles |
| `GET /senador/{codigo}/discursos.json` | Speeches; `dataInicio` and `dataFim` use `YYYYMMDD` |
| `GET /senador/{codigo}/apartes.json` | Interjections |
| `GET /senador/{codigo}/autorias.json` | Authored matters |
| `GET /senador/{codigo}/relatorias.json` | Rapporteur assignments |
| `GET /senador/{codigo}/votacoes.json` | Voting history |
| `GET /senador/{codigo}/licencas.json` | Leave records |

Use the `CodigoParlamentar` returned by a senator list or search, not a name embedded in a URL.

## Legislative process and matters

Use `/processo` for author searches and consolidated cross-house status:

```text
GET /processo?autor={nome}&tramitando=S
GET /processo?codigoParlamentarAutor={codigo}&tramitouLegislaturaAtual=S
GET /processo/{identificacaoProcesso}.json
```

The process collection returns a top-level JSON list. Its identifier is not necessarily a `CodigoMateria`.

Core matter resources:

| Endpoint | Purpose |
|---|---|
| `GET /materia/pesquisa/lista.json` | Search by `sigla`, `numero`, `ano`, `assunto`, `tramitando` |
| `GET /materia/{codigo}.json` | Matter detail by Senate code |
| `GET /materia/situacaoatual/{codigo}.json` | Current situation |
| `GET /materia/movimentacoes/{codigo}.json` | Movements |
| `GET /materia/textos/{codigo}.json` | Text versions |
| `GET /materia/emendas/{codigo}.json` | Amendments |
| `GET /materia/relatorias/{codigo}.json` | Rapporteurs |
| `GET /materia/autoria/{codigo}.json` | Authors |
| `GET /materia/tramitando.json` | Matters in progress |
| `GET /materia/atualizadas.json?numdias={n}` | Recently updated matters |
| `GET /materia/vetos/{ano}.json` | Presidential vetoes |

Do not use `autor` on `/materia/pesquisa/lista` for authoritative author filtering; observed responses can ignore that parameter.

## Plenary and committees

| Endpoint | Date format or purpose |
|---|---|
| `GET /plenario/agenda/dia/{data}.json` | `YYYYMMDD` |
| `GET /plenario/agenda/mes/{mes}.json` | `YYYYMM` |
| `GET /plenario/resultado/{data}.json` | `YYYYMMDD` |
| `GET /plenario/lista/votacao/{inicio}/{fim}.json` | `YYYYMMDD` |
| `GET /plenario/votacao/nominal/{ano}.json` | Nominal votes |
| `GET /plenario/lista/discursos/{inicio}/{fim}.json` | Plenary speeches |
| `GET /comissao/lista/colegiados.json` | Committees |
| `GET /comissao/agenda/{inicio}/{fim}.json` | Meetings |
| `GET /comissao/reuniao/{codigo}.json` | Meeting detail |
| `GET /composicao/comissao/{codigo}.json` | Membership |

Query speech ranges one calendar year at a time and combine the normalized results locally.

## Other domains

The API also exposes votes in committees, leadership composition, veto outcomes, budget amendments, shorthand records, and legislation. Verify the precise route and response schema in Swagger before adding a new long-lived client method or presenting a field as authoritative.
