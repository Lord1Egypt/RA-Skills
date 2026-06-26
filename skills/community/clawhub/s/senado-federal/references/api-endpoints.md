# Senado Federal — Referência Completa de Endpoints

Base: `https://legis.senado.leg.br/dadosabertos`
Swagger: `https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html`
Formato: adicionar `.json` ou `.xml` ao final dos paths.

## Senadores

| Endpoint | Descrição |
|---|---|
| `GET /senador/lista/atual.json` | Todos em exercício |
| `GET /senador/afastados.json` | Afastados |
| `GET /senador/lista/legislatura/{leg}.json` | Por legislatura (ex: 57) |
| `GET /senador/lista/legislatura/{ini}/{fim}.json` | Intervalo de legislaturas |
| `GET /senador/partidos.json` | Partidos com representação |
| `GET /senador/{codigo}.json` | Perfil completo |
| `GET /senador/{codigo}/mandatos.json` | Mandatos |
| `GET /senador/{codigo}/filiacoes.json` | Filiações partidárias |
| `GET /senador/{codigo}/cargos.json` | Cargos exercidos |
| `GET /senador/{codigo}/comissoes.json` | Comissões |
| `GET /senador/{codigo}/liderancas.json` | Lideranças |
| `GET /senador/{codigo}/discursos.json` | Discursos (params: dataInicio, dataFim em YYYYMMDD) |
| `GET /senador/{codigo}/apartes.json` | Apartes |
| `GET /senador/{codigo}/autorias.json` | Autorias de matérias |
| `GET /senador/{codigo}/relatorias.json` | Relatorias exercidas |
| `GET /senador/{codigo}/votacoes.json` | Histórico de votações |
| `GET /senador/{codigo}/profissao.json` | Background profissional |
| `GET /senador/{codigo}/historicoAcademico.json` | Histórico acadêmico |
| `GET /senador/{codigo}/licencas.json` | Licenças |

## Matérias (Bills)

> ⚠️ O endpoint `/materia/{sigla}/{numero}/{ano}` foi depreciado em 2025. Use `/materia/pesquisa/lista` ou `/processo`.

| Endpoint | Params |
|---|---|
| `GET /materia/pesquisa/lista.json` | sigla, numero, ano, autor, assunto, tramitando (S/N), codigoSituacao |
| `GET /materia/{codigo}.json` | — |
| `GET /materia/situacaoatual/{codigo}.json` | Situação atual |
| `GET /materia/votacoes/{codigo}.json` | Votações sobre a matéria |
| `GET /materia/textos/{codigo}.json` | Textos/versões da matéria |
| `GET /materia/emendas/{codigo}.json` | Emendas |
| `GET /materia/relatorias/{codigo}.json` | Relatores |
| `GET /materia/autoria/{codigo}.json` | Autoria |
| `GET /materia/movimentacoes/{codigo}.json` | Tramitação completa |
| `GET /materia/atualizacoes/{codigo}.json` | Atualizações recentes |
| `GET /materia/tramitando.json` | Todas em tramitação |
| `GET /materia/legislaturaatual.json` | Matérias da legislatura atual |
| `GET /materia/atualizadas.json` | Recentemente atualizadas (param: numdias) |
| `GET /materia/lista/tramitacao.json` | Lista por tramitação |
| `GET /materia/lista/comissao.json` | Por comissão |
| `GET /materia/lista/prazo/{codPrazo}.json` | Por prazo |
| `GET /materia/vetos/{ano}.json` | Vetos presidenciais |
| `GET /materia/ordia/{codigo}.json` | Ordem do dia |

### Tipos de matéria (sigla)
PL, PLC, PLP, PEC, MPV, PDL, RQS, REQ, RDG, PDS, MSF, SCD, MSC, PCE, VET, INA, TPS, REC, EMS, EMC, EMP, SBT, PCR, REF, PFC, PRS

## Plenário

| Endpoint | Formato data | Descrição |
|---|---|---|
| `GET /plenario/agenda/dia/{data}.json` | YYYYMMDD | Agenda do dia |
| `GET /plenario/agenda/mes/{data}.json` | YYYYMM | Agenda do mês |
| `GET /plenario/agenda/cn/{data}.json` | YYYYMMDD | Sessão do CN |
| `GET /plenario/agenda/cn/{inicio}/{fim}.json` | YYYYMMDD | Intervalo CN |
| `GET /plenario/resultado/{data}.json` | YYYYMMDD | Resultado do dia |
| `GET /plenario/resultado/mes/{data}.json` | YYYYMM | Resultado mensal |
| `GET /plenario/lista/votacao/{dataInicio}/{dataFim}.json` | YYYYMMDD | Votações |
| `GET /plenario/votacao/nominal/{ano}.json` | YYYY | Votações nominais do ano |
| `GET /plenario/lista/discursos/{dataInicio}/{dataFim}.json` | YYYYMMDD | Discursos |
| `GET /plenario/encontro/{codigo}.json` | — | Detalhe da sessão |
| `GET /plenario/encontro/{codigo}/pauta.json` | — | Pauta da sessão |
| `GET /plenario/encontro/{codigo}/resultado.json` | — | Resultado |
| `GET /plenario/encontro/{codigo}/resumo.json` | — | Resumo |
| `GET /plenario/lista/legislaturas.json` | — | Legislaturas |
| `GET /plenario/tiposSessao.json` | — | Tipos de sessão |

## Comissões

| Endpoint | Descrição |
|---|---|
| `GET /comissao/lista/colegiados.json` | Comissões permanentes |
| `GET /comissao/lista/mistas.json` | Comissões mistas (CN) |
| `GET /comissao/lista/{tipo}.json` | Por tipo |
| `GET /comissao/{codigo}.json` | Detalhe |
| `GET /comissao/agenda/{dataReferencia}.json` | Agenda do dia (YYYYMMDD) |
| `GET /comissao/agenda/{dataInicio}/{dataFim}.json` | Intervalo |
| `GET /comissao/agenda/mes/{mesReferencia}.json` | Mês (YYYYMM) |
| `GET /comissao/agenda/atual/iCal` | Feed iCal |
| `GET /comissao/reuniao/{codigoReuniao}.json` | Reunião |
| `GET /comissao/reuniao/notas/{codigoReuniao}.json` | Notas taquigráficas |
| `GET /composicao/comissao/{codigo}.json` | Composição atual |

## Votações em Comissões

| Endpoint | Descrição |
|---|---|
| `GET /votacaoComissao/comissao/{sigla}.json` | Por comissão |
| `GET /votacaoComissao/materia/{sigla}/{numero}/{ano}.json` | Por matéria |
| `GET /votacaoComissao/parlamentar/{codigo}.json` | Por senador |

## Composição

| Endpoint | Descrição |
|---|---|
| `GET /composicao/mesaSF.json` | Mesa do Senado |
| `GET /composicao/mesaCN.json` | Mesa do CN |
| `GET /composicao/lideranca.json` | Lideranças |
| `GET /composicao/lista/liderancaSF.json` | Lideranças SF |
| `GET /composicao/lista/liderancaCN.json` | Lideranças CN |
| `GET /composicao/lista/partidos.json` | Partidos |
| `GET /composicao/lista/blocos.json` | Blocos |
| `GET /composicao/bloco/{codigo}.json` | Bloco detail |

## Taquigrafia

| Endpoint | Descrição |
|---|---|
| `GET /taquigrafia/notas/sessao/{idSessao}.json` | Notas da sessão |
| `GET /taquigrafia/notas/reuniao/{idReuniao}.json` | Notas da reunião |
| `GET /taquigrafia/videos/sessao/{idSessao}.json` | Vídeos da sessão |
| `GET /taquigrafia/videos/reuniao/{idReuniao}.json` | Vídeos da reunião |

## Discursos

| Endpoint | Descrição |
|---|---|
| `GET /discurso/texto-integral/{codigo}.json` | Texto completo |
| `GET /discurso/texto-binario/{codigo}.json` | Binário |

## Autores

| Endpoint |
|---|
| `GET /autor/lista/atual.json` |
| `GET /autor/tiposAutor.json` |

## Legislação

| Endpoint | Params |
|---|---|
| `GET /legislacao/lista.json` | tipo, ano, numero |
| `GET /legislacao/{codigo}.json` | — |
| `GET /legislacao/urn.json` | urn |
| `GET /legislacao/classes.json` | — |

## Comissões Permanentes do Senado (siglas principais)
CAE, CAS, CCJ, CCAI, CCT, CDR, CE, CI, CMA, CMMC, CMO, CPDesp, CRA, CRE, CTFC, CTINFRA, CVS, CSPCCO

## Notas de uso
- Legislatura atual: **57** (iniciada 01/02/2023)
- Codes dos senadores: obtidos via `/senador/lista/atual.json`
- Codes de matérias: obtidos via `/materia/pesquisa/lista.json`
- Datas em discursos/agenda: formato `YYYYMMDD` (sem hífens)
- `/materia/pesquisa/lista` sem filtro de assunto retorna todas em tramitação
