---
name: senado-federal
description: Monitor and research the Brazilian Senate (Senado Federal) legislative activity. Use when: (1) searching for Senate bills/matérias by type, author, keyword or year, (2) checking today's or upcoming plenary/committee agenda, (3) looking up senators by name, party or state, (4) tracking voting results (votações) in plenary or committees, (5) checking committee (comissão) schedules and composition, (6) monitoring specific bill tramitação/status, (7) researching senator speeches (discursos/apartes), (8) checking senator mandates, affiliations, academic history, (9) any question about the Senado Federal, senators, or Senate legislative process, (10) tracking presidential vetoes (vetos presidenciais), (11) checking party/bancada voting orientation (orientação de bancada), (12) budget amendments/emendas parlamentares, (13) CPI requerimentos, (14) advanced processo legislativo search with multiple filters. Base URL: https://legis.senado.leg.br/dadosabertos — no auth required, supports .json and .xml suffixes.
version: "1.1.0"
author: "Daniel Marques"
license: "MIT"
---

# Senado Federal — API de Dados Abertos

Base URL: `https://legis.senado.leg.br/dadosabertos`
Swagger: `https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html`
No authentication required.
**Format**: append `.json` or `.xml` to endpoint paths.

---

## Key Endpoints

### Senators (Senadores)
```
GET /senador/lista/atual.json           # all senators currently in office
GET /senador/afastados.json             # senators on leave
GET /senador/lista/legislatura/{leg}.json  # by legislature number (e.g. 57)
GET /senador/partidos.json              # party list

GET /senador/{codigo}.json              # full senator profile
GET /senador/{codigo}/mandatos.json     # mandate history
GET /senador/{codigo}/filiacoes.json    # party affiliations
GET /senador/{codigo}/cargos.json       # positions held
GET /senador/{codigo}/comissoes.json    # committee memberships
GET /senador/{codigo}/liderancas.json   # leadership roles
GET /senador/{codigo}/discursos.json    # speeches
  ?dataInicio=YYYYMMDD&dataFim=YYYYMMDD&tipoPronunciamento=
GET /senador/{codigo}/apartes.json      # interjections
GET /senador/{codigo}/autorias.json     # authored bills
GET /senador/{codigo}/relatorias.json   # reports authored
GET /senador/{codigo}/votacoes.json     # voting history
GET /senador/{codigo}/profissao.json    # professional background
GET /senador/{codigo}/historicoAcademico.json
GET /senador/{codigo}/licencas.json     # leave periods
```

### Bills / Matérias (API v2 — recommended)
```
GET /materia/pesquisa/lista.json
  ?sigla=PL          # type: PL, PEC, PLS, MSF, INC, etc.
  ?numero=123
  ?ano=2026
  ?autor=            # author name
  ?assunto=          # subject/keyword
  ?tramitando=S      # S=currently in progress
  ?codigoSituacao=

GET /materia/{codigo}.json              # by internal code
GET /materia/{sigla}/{numero}/{ano}.json  # e.g. /materia/PL/1234/2026.json
GET /materia/situacaoatual/{codigo}.json  # current status
GET /materia/votacoes/{codigo}.json     # votes on this bill
GET /materia/textos/{codigo}.json       # bill texts
GET /materia/emendas/{codigo}.json      # amendments
GET /materia/relatorias/{codigo}.json   # rapporteurs
GET /materia/autoria/{codigo}.json      # authorship
GET /materia/movimentacoes/{codigo}.json # full tramitação history
GET /materia/tramitando.json            # all currently in progress
GET /materia/legislaturaatual.json      # current legislature bills
GET /materia/atualizadas.json           # recently updated
  ?numdias=7         # last N days
```

### Plenary Agenda & Results (Plenário)
```
GET /plenario/agenda/dia/{data}.json     # e.g. /plenario/agenda/dia/20260304.json
GET /plenario/agenda/mes/{data}.json     # e.g. /plenario/agenda/mes/202603.json
GET /plenario/agenda/cn/{data}.json      # Congresso Nacional joint session agenda
GET /plenario/agenda/atual/iCal          # iCal feed agenda atual

GET /plenario/resultado/{data}.json      # plenary results for a date (YYYYMMDD)
GET /plenario/resultado/mes/{data}.json  # monthly results (YYYYMM)
GET /plenario/resultado/cn/{data}.json   # resultado sessão CN (YYYYMMDD)
GET /plenario/resultado/veto/{codigo}.json              # resultado de veto
GET /plenario/resultado/veto/materia/{codigo}.json      # resultado veto sobre PL
GET /plenario/resultado/veto/dispositivo/{codigo}.json  # resultado dispositivo de veto parcial

GET /plenario/lista/votacao/{dataInicio}/{dataFim}.json  # votes in date range (YYYYMMDD)
GET /plenario/votacao/nominal/{ano}.json  # all nominal votes in a year
GET /plenario/votacao/orientacaoBancada/{dataSessao}.json           # orientação bancada por data
GET /plenario/votacao/orientacaoBancada/{dataInicio}/{dataFim}.json # orientação bancada por período

GET /plenario/lista/discursos/{dataInicio}/{dataFim}.json  # speeches
GET /plenario/lista/legislaturas.json
GET /plenario/lista/tiposComparecimento.json  # tipos de comparecimento
GET /plenario/legislatura/{data}.json
GET /plenario/tiposSessao.json               # tipos de sessão

GET /plenario/encontro/{codigo}.json       # session detail
GET /plenario/encontro/{codigo}/pauta.json # session agenda
GET /plenario/encontro/{codigo}/resultado.json
GET /plenario/encontro/{codigo}/resumo.json
```

### Committees (Comissões)
```
GET /comissao/lista/colegiados.json      # all standing committees
GET /comissao/lista/mistas.json          # joint CN/Congresso committees
GET /comissao/lista/{tipo}.json          # by type
GET /comissao/lista/tiposColegiado.json  # tipos de colegiado

GET /comissao/{codigo}.json              # committee detail
GET /comissao/agenda/{dataReferencia}.json   # YYYYMMDD
GET /comissao/agenda/{dataInicio}/{dataFim}.json
GET /comissao/agenda/mes/{mesReferencia}.json  # YYYYMM
GET /comissao/agenda/atual/iCal          # iCal feed

GET /comissao/reuniao/{codigoReuniao}.json
GET /comissao/reuniao/notas/{codigoReuniao}.json
GET /comissao/reuniao/{sigla}/documento/{tipoDocumento}.json  # doc da última reunião

GET /composicao/comissao/{codigo}.json                          # membership
GET /composicao/comissao/atual/mista/{codigo}.json             # composição atual comissão mista
GET /composicao/comissao/resumida/mista/{codigo}/{dataInicio}/{dataFim}.json

GET /comissao/cpi/{comissao}/requerimentos.json  # Requerimentos de CPI
  ?pagina=1&tamanho=20
```

### Voting in Committees (VotaçãoComissão)
```
GET /votacaoComissao/comissao/{siglaComissao}.json
GET /votacaoComissao/materia/{sigla}/{numero}/{ano}.json
GET /votacaoComissao/parlamentar/{codigo}.json
```

### Voting (Geral)
```
GET /votacao.json
  ?dataInicio=YYYYMMDD&dataFim=YYYYMMDD
  ?codigoSessao=
```

### Leadership & Composition
```
GET /composicao/mesaSF.json           # Senate presiding board
GET /composicao/mesaCN.json           # CN presiding board
GET /composicao/lideranca.json        # leadership
GET /composicao/lideranca/tipos.json  # tipos de lideranças
GET /composicao/lideranca/tipos-unidade.json  # tipos de unidades de lideranças
GET /composicao/lista/liderancaSF.json
GET /composicao/lista/liderancaCN.json
GET /composicao/lista/cn/{tipo}.json  # composição comissões CN por tipo
GET /composicao/lista/partidos.json
GET /composicao/lista/blocos.json
GET /composicao/lista/tiposCargo.json # tipos de cargo
GET /composicao/bloco/{codigo}.json
```

### Authors / Autores
```
GET /autor/lista/atual.json
GET /autor/tiposAutor.json
```

### Legislation / Normas
```
GET /legislacao/lista.json
  ?tipo=&ano=&numero=
GET /legislacao/{codigo}.json
GET /legislacao/urn.json?urn={urn}
```

### Taquigrafia (Transcripts)
```
GET /taquigrafia/notas/sessao/{idSessao}.json
GET /taquigrafia/notas/reuniao/{idReuniao}.json
GET /taquigrafia/videos/sessao/{idSessao}.json
GET /taquigrafia/videos/reuniao/{idReuniao}.json
```

### Speeches / Discursos
```
GET /discurso/texto-integral/{codigoPronunciamento}.json
GET /discurso/texto-binario/{codigoPronunciamento}.json
```

### Vetos Presidenciais
```
GET /materia/vetos/{ano}.json         # Vetos de um ano (ex: 2026)
GET /materia/vetos/aposrcn.json       # Vetos posteriores à RCN 1/2013 em tramitação
GET /materia/vetos/antesrcn.json      # Vetos anteriores à RCN 1/2013 em tramitação
GET /materia/vetos/encerrados.json    # Vetos com tramitação encerrada
```

### Orçamento e Emendas Parlamentares
```
GET /orcamento/lista.json              # Lotes de emendas ao orçamento
GET /orcamento/oficios.json            # Ofícios de apoio às emendas de orçamento
GET /orcamento/oficios/{numeroSedol}.json  # Detalhes de um ofício específico
```

### Processo Legislativo (API Avançada)
```
GET /processo                          # Pesquisa avançada (SEM sufixo .json, retorna array)
  ?sigla=PL          # tipo
  ?numero=123
  ?ano=2026
  ?tramitando=S
  ?autor=            # nome do autor
  ?codigoParlamentarAutor=
  ?termo=            # palavra-chave no assunto
  ?dataInicioApresentacao=YYYYMMDD
  ?dataFimApresentacao=YYYYMMDD
  ?numdias=          # últimos N dias
GET /processo/{id}                     # Processo pelo ID
GET /processo/assuntos.json            # Assuntos gerais e específicos
GET /processo/documento.json           # Documentos de processo
GET /processo/documento/tipos.json
GET /processo/documento/tipos-conteudo.json
GET /processo/emenda.json
GET /processo/entes.json
GET /processo/prazo.json
GET /processo/prazo/tipos.json
GET /processo/relatoria.json
GET /processo/siglas.json
GET /processo/tipos-atualizacao.json
GET /processo/tipos-autor.json
GET /processo/tipos-decisao.json
GET /processo/tipos-situacao.json
```

### Distribuição de Autoria e Relatoria
```
GET /materia/distribuicao/autoria.json
  ?siglaComissao=  # por comissão
  ?codParlamentar= # por parlamentar
GET /materia/distribuicao/relatoria/{sigla}.json
```

---

## Prestação de Contas & Transparência

Existem **duas APIs** distintas do Senado para transparência:

| API | Base URL | Foco |
|-----|----------|------|
| Dados Abertos Legislativos | `legis.senado.leg.br/dadosabertos` | Atividade legislativa |
| **Dados Abertos Administrativos** | `adm.senado.gov.br/adm-dadosabertos` | **CEAP, servidores, contratos** |

Swagger ADM: https://adm.senado.gov.br/adm-dadosabertos/swagger-ui/index.html

---

### API ADM — Senadores (Prestação de Contas)

Base URL: `https://adm.senado.gov.br/adm-dadosabertos`

```
GET /api/v1/senadores/despesas_ceaps/{ano}     # CEAP por ano (ex: 2026) - retorna JSON
GET /api/v1/senadores/despesas_ceaps/{ano}/csv # CEAP por ano em CSV
  Campos: id, tipoDocumento, ano, mes, codSenador, nomeSenador,
          tipoDespesa, cpfCnpj, fornecedor, valor, ...

GET /api/v1/senadores/auxilio-moradia          # Auxílio moradia por senador
GET /api/v1/senadores/auxilio-moradia/csv
  ?nomeParlamentarContains=
  ?estadoEleitoEquals=
  ?partidoEleitoEquals=

GET /api/v1/senadores/escritorios              # Escritórios de apoio
GET /api/v1/senadores/escritorios/csv

GET /api/v1/senadores/aposentados              # Senadores aposentados e remuneração
GET /api/v1/senadores/aposentados/csv

GET /api/v1/senadores/quantitativos/senadores  # Quantitativo de senadores
GET /api/v1/senadores/quantitativos/senadores/csv
```

### API ADM — Servidores
```
GET /api/v1/servidores/servidores              # Lista servidores
  ?tipoVinculoEquals=
  ?situacaoEquals=
  ?lotacaoEquals=
  ?cargoEquals=
GET /api/v1/servidores/servidores/ativos       # Apenas ativos
GET /api/v1/servidores/servidores/efetivos     # Apenas efetivos
GET /api/v1/servidores/servidores/comissionados
GET /api/v1/servidores/servidores/inativos
GET /api/v1/servidores/servidores/{formato}/csv  # Export CSV

GET /api/v1/servidores/remuneracoes/{ano}/{mes}  # Remuneração mensal
GET /api/v1/servidores/remuneracoes/{ano}/{mes}/csv
  Campos: sequencial, nome, mes, ano, remuneracao_basica, vantagens_pessoais,
          funcao_comissionada, gratificacoes, diarias, auxilios, ...

GET /api/v1/servidores/horas-extras/{ano}/{mes}  # Horas extras
GET /api/v1/servidores/horas-extras/{ano}/{mes}/csv

GET /api/v1/servidores/estagiarios             # Estagiários
GET /api/v1/servidores/pensionistas            # Pensionistas
GET /api/v1/servidores/pensionistas/remuneracoes/{ano}/{mes}
GET /api/v1/servidores/lotacoes                # Lotações
GET /api/v1/servidores/cargos                  # Cargos
GET /api/v1/servidores/previsao-aposentadoria  # Previsão de aposentadoria
GET /api/v1/servidores/quantitativos/pessoal   # Quantitativo de pessoal
GET /api/v1/servidores/quantitativos/cargos-funcoes
```

### API ADM — Supridos (Cartão Corporativo)
```
GET /api/v1/supridos/{ano}                     # Lista de supridos do ano
GET /api/v1/supridos/{ano}/csv
GET /api/v1/supridos/atosConcessao/{ano}       # Atos de concessão
GET /api/v1/supridos/empenhos/{ano}            # Empenhos
GET /api/v1/supridos/movimentacoes/{ano}       # Movimentações
GET /api/v1/supridos/transacoes/{ano}          # Transações
```

### API ADM — Contratações
```
GET /api/v1/contratacoes/contratos             # Contratos
  ?statusContratoParam=
  ?nomeFornecedorContains=
  ?cnpjCpfEquals=
  ?numeroContains=
  ?anoEquals=
  ?objetoDescricaoContains=
GET /api/v1/contratacoes/contratos/{id}/aditivos
GET /api/v1/contratacoes/contratos/{id}/pagamentos
GET /api/v1/contratacoes/licitacoes            # Licitações
  ?numeroEquals=
  ?objetoContains=
GET /api/v1/contratacoes/licitacoes/{id}/detalhamentos
GET /api/v1/contratacoes/notas_empenho         # Notas de empenho
GET /api/v1/contratacoes/atas_registro_preco   # Atas de registro de preço
GET /api/v1/contratacoes/empresas              # Empresas fornecedoras
GET /api/v1/contratacoes/terceirizados         # Terceirizados
GET /api/v1/contratacoes/{tipoContratacao}/{id}/itens
GET /api/v1/contratacoes/{tipoContratacao}/{id}/garantias
# Todos aceitam sufixo /csv para export
```

### API Ergon — Diretores/Coordenadores
```bash
curl "https://adm.senado.gov.br/ergon-ng-reports/api/v1/diretores-e-coordenadores"
# Retorna: diretores, coordenadores, setores, telefones e e-mails do SF
```

### Exemplo: CEAP de 2026
```bash
curl "https://adm.senado.gov.br/adm-dadosabertos/api/v1/senadores/despesas_ceaps/2026" | \
  python3 -c "
import json, sys
despesas = json.load(sys.stdin)
# Filtrar por senador
for d in despesas:
    if 'MARCOS PONTES' in d.get('nomeSenador', ''):
        print(f\"{d['mes']:02d}/{d['ano']} | {d['tipoDespesa'][:40]} | R$ {d.get('valor', 0)}\")
"
```

### Dados Disponíveis via API (accountability)
- ✅ **CEAP/Cota parlamentar**: `/api/v1/senadores/despesas_ceaps/{ano}` (ADM)
- ✅ **Auxílio moradia**: `/api/v1/senadores/auxilio-moradia` (ADM)
- ✅ **Escritórios de apoio**: `/api/v1/senadores/escritorios` (ADM)
- ✅ **Remuneração servidores**: `/api/v1/servidores/remuneracoes/{ano}/{mes}` (ADM)
- ✅ **Cartão corporativo**: `/api/v1/supridos/{ano}` (ADM)
- ✅ **Contratos/licitações**: `/api/v1/contratacoes/contratos` (ADM)
- ✅ **Emendas parlamentares**: `/orcamento/lista.json` (LEGIS)
- ✅ **Votações/Discursos/Autorias**: API LEGIS (`/senador/{cod}/...`)
- ❌ Declaração de bens: apenas portal de transparência (web)

### Today's plenary agenda
```bash
DATE=$(date +%Y%m%d)
curl "https://legis.senado.leg.br/dadosabertos/plenario/agenda/dia/$DATE.json"
```

### Find a senator (search in lista/atual)
```bash
curl "https://legis.senado.leg.br/dadosabertos/senador/lista/atual.json" | \
  python3 -c "
import json,sys
data = json.load(sys.stdin)
senators = data['ListaParlamentarEmExercicio']['Parlamentares']['Parlamentar']
for s in senators:
    name = s['IdentificacaoParlamentar']['NomeParlamentar']
    if 'Pontes' in name:
        print(json.dumps(s, ensure_ascii=False, indent=2))
"
```

### Search bills
```bash
curl "https://legis.senado.leg.br/dadosabertos/materia/pesquisa/lista.json?sigla=PL&ano=2026&tramitando=S&assunto=transporte"
```

### Recent plenary votes
```bash
START=$(date -d '7 days ago' +%Y%m%d)
END=$(date +%Y%m%d)
curl "https://legis.senado.leg.br/dadosabertos/plenario/lista/votacao/$START/$END.json"
```

### Committee agenda (current month)
```bash
MONTH=$(date +%Y%m)
curl "https://legis.senado.leg.br/dadosabertos/comissao/agenda/mes/$MONTH.json"
```

### Bill tramitação
```bash
# By sigla/number/year:
curl "https://legis.senado.leg.br/dadosabertos/materia/movimentacoes/{codigo}.json"
```

---

## Notes
- Date formats vary: plenary agenda uses `YYYYMMDD`; senator speeches use `YYYYMMDD`; materia pesquisa uses `YYYY`
- Current legislature: 57 (started Feb 2023)
- Senator codes (CodigoParlamentar) found in `/senador/lista/atual.json`
- Materia codes (codigo) found in `/materia/pesquisa/lista.json` results
- API v1 `/materia/{sigla}/{numero}/{ano}` is deprecated since 2025; prefer `/processo` or `/materia/pesquisa/lista`
- iCal feed available for committee agenda: `/comissao/agenda/atual/iCal`
- Full endpoint list: see `references/api-endpoints.md`

---

## API Quirks & Tips

- **Single-item responses**: When an endpoint returns only 1 item, the Senado API may return a dict instead of a list. Always use the pattern: `isinstance(x, list) else [x] if x else []`
- **Deeply nested JSON**: Responses are typically 3-4 levels deep (e.g., `data["ListaParlamentarEmExercicio"]["Parlamentares"]["Parlamentar"]`). The Python client's `_get_list()` uses DFS to find the first list.
- **Date format inconsistency**: Plenário endpoints use `YYYYMMDD`; some senator endpoints also use `YYYYMMDD`; matéria pesquisa uses just `YYYY` for year filters.
- **Processo vs Materia**: `/processo/{codigo}.json` returns richer data (autuações, situações, tramitação completa) than `/materia/{codigo}.json`. Prefer processo for detailed status tracking.
- **API v1 deprecation**: `/materia/{sigla}/{numero}/{ano}` is deprecated since 2025. Use `/materia/pesquisa/lista.json` with params instead.
- **Retry recommended**: The API can be slow or return 500s. The Python client implements exponential backoff (2^attempt seconds).
- **`/composicao/comissao/{codigo}`**: requires a valid committee code from `/comissao/lista/colegiados` — passing `1` returns 400.
- **`/plenario/agenda/mes/{data}` and `/plenario/resultado/mes/{data}`**: require format `YYYYMM` and must correspond to months with actual sessions; past months without sessions may return 400.
- **`/votacao.json`**: requires `codigoSessao` parameter (not a date range) to return results. Use `/plenario/lista/votacao/{inicio}/{fim}` for date-based queries.
- **ADM API base URL**: `https://adm.senado.gov.br/adm-dadosabertos` (separate from legis). No `.json` suffix needed. Returns arrays directly.
- **Processo search**: `/processo` (no `.json` suffix) returns a raw JSON array, not a nested object. Params accept 20+ filters including `dataInicioApresentacao`, `termo`, `codigoParlamentarAutor`.

---

## Python Client (async)

You can use the async Python client for programmatic access:

```python
import asyncio
from senado_client import get_senado_client

async def main():
    client = get_senado_client()
    
    # Listar senadores atuais
    senators = await client.lista_senadores_atuais()
    
    # Buscar por nome
    resultado = await client.buscar_senador_por_nome("Bolsonaro")
    
    # Pesquisar matérias
    materias = await client.pesquisar_materia(sigla="PL", ano=2026)
    
    # Votações da semana
    from datetime import date, timedelta
    votacoes = await client.get_votacoes_periodo(
        date.today() - timedelta(days=7),
        date.today()
    )
    
    await client.close()

asyncio.run(main())
```

Requires: `pip install httpx`

### Available Methods

**Senadores:**
- `lista_senadores_atuais()` — Senadores em exercício
- `buscar_senador_por_nome(nome)` — Busca por nome
- `get_senador_detalhe(codigo)` — Detalhes completos
- `get_autorias_senador(codigo)` — Matérias de autoria
- `get_discursos_senador(codigo, data_inicio?, data_fim?)` — Discursos
- `get_senador_votacoes(codigo)` — Histórico de votações
- `get_senador_comissoes(codigo)` — Comissões
- `get_senador_mandatos(codigo)` — Mandatos
- `get_senador_filiacoes(codigo)` — Filiações partidárias
- `get_senador_cargos(codigo)` — Cargos exercidos
- `get_senador_liderancas(codigo)` — Lideranças
- `get_senador_apartes(codigo)` — Apartes/intervenções
- `get_senador_relatorias(codigo)` — Relatorias
- `get_senador_profissao(codigo)` — Profissão
- `get_senador_historico_academico(codigo)` — Histórico acadêmico
- `get_senador_licencas(codigo)` — Licenças

**Matérias/Proposições:**
- `pesquisar_materia(sigla?, numero?, ano?, tramitando?)` — Pesquisa
- `pesquisar_materia_por_assunto(assunto, tramitando?)` — Por assunto
- `get_materia_detalhe(codigo)` — Detalhes
- `get_materia_movimentacoes(codigo)` — Movimentações
- `get_materia_tramitacao(codigo)` — Tramitação
- `get_materia_por_sigla(sigla, numero, ano)` — Por sigla completa
- `get_materia_situacao_atual(codigo)` — Situação atual
- `get_materia_textos(codigo)` — Textos
- `get_materia_emendas(codigo)` — Emendas
- `get_materia_relatorias(codigo)` — Relatorias
- `get_materia_autoria(codigo)` — Autoria
- `get_materias_tramitando()` — Em tramitação
- `get_materias_atualizadas(dias?)` — Atualizadas recentemente

**Plenário:**
- `get_agenda_plenario_dia(data?)` — Agenda diária
- `get_agenda_plenario_mes(ano, mes)` — Agenda mensal
- `get_votacoes_periodo(data_inicio, data_fim)` — Votações em período
- `get_resultado_plenario_dia(data)` — Resultado do dia
- `get_resultado_plenario_mes(ano, mes)` — Resultado do mês
- `get_votacoes_nominais_ano(ano)` — Votações nominais
- `get_discursos_plenario(data_inicio, data_fim)` — Discursos
- `get_encontro_plenario(codigo)` — Detalhes de sessão
- `get_encontro_pauta(codigo)` — Pauta de sessão

**Comissões:**
- `get_lista_comissoes()` — Lista de comissões
- `get_agenda_comissao_dia(data?)` — Agenda do dia
- `get_agenda_comissao_periodo(data_inicio, data_fim)` — Agenda de período
- `get_comissao_detalhe(codigo)` — Detalhes
- `get_comissao_reuniao(codigo_reuniao)` — Reunião
- `get_composicao_comissao(codigo)` — Membros
- `get_lista_comissoes_mistas()` — Comissões mistas

**Votação em Comissões:**
- `get_votacao_comissao(sigla_comissao)` — Votações
- `get_votacao_comissao_materia(sigla, numero, ano)` — Por matéria
- `get_votacao_comissao_parlamentar(codigo)` — Por parlamentar

**Composição e Lideranças:**
- `get_mesa_senado()` — Mesa diretora do Senado
- `get_mesa_congresso()` — Mesa do CN
- `get_liderancas()` — Lideranças partidárias
- `get_blocos_parlamentares()` — Blocos parlamentares

**Processo:**
- `get_processo(codigo)` — Processo legislativo completo

**Autores, Legislação, Discurso:**
- `get_autores_atuais()` — Autores atuais
- `pesquisar_legislacao(tipo?, ano?, numero?)` — Pesquisa legislação
- `get_discurso_texto_integral(codigo_pronunciamento)` — Texto integral

**Vetos Presidenciais:**
- `get_vetos_ano(ano)` — Vetos de um ano
- `get_vetos_apos_rcn()` — Vetos pós-RCN 1/2013 em tramitação
- `get_vetos_antes_rcn()` — Vetos pré-RCN 1/2013
- `get_vetos_encerrados()` — Vetos encerrados

**Orientação de Bancada:**
- `get_orientacao_bancada_data(data)` — Orientação por data
- `get_orientacao_bancada_periodo(data_inicio, data_fim)` — Por período

**Resultado Plenário CN e Vetos:**
- `get_resultado_plenario_cn(data)` — Resultado sessão CN
- `get_resultado_veto(codigo)` — Resultado voto de veto
- `get_resultado_veto_materia(codigo)` — Resultado veto sobre PL

**Orçamento/Emendas:**
- `get_orcamento_lotes_emendas()` — Lotes de emendas
- `get_orcamento_oficios()` — Ofícios de emendas
- `get_orcamento_oficio(numero_sedol)` — Ofício específico

**CPI:**
- `get_cpi_requerimentos(comissao, pagina?, tamanho?)` — Requerimentos de CPI

**Processo Legislativo (API Avançada):**
- `pesquisar_processos(sigla?, numero?, ano?, tramitando?, autor?, assunto?, data_inicio_apresentacao?, data_fim_apresentacao?)` — Pesquisa avançada

**Distribuição:**
- `get_distribuicao_autoria_comissao(sigla_comissao?, cod_parlamentar?)` — Distribuição de autoria
- `get_distribuicao_relatoria_comissao(sigla)` — Distribuição de relatoria
- `get_materia_lista_tramitacao(sigla?, comissao?)` — Total em tramitação

**Composição Mista:**
- `get_composicao_comissao_mista_atual(codigo)` — Composição atual de comissão mista

**Utilitários:**
- `get_materias_recentes(dias?)` — Matérias recentes
- `get_votacoes_semana()` — Votações da semana
- `get_agenda_semana()` — Agenda da semana

---

## Python Client — API ADM (Prestação de Contas)

```python
from senado_client import get_senado_adm_client

async def main():
    adm = get_senado_adm_client()
    
    # CEAP do ano
    ceap = await adm.get_ceap(2026)
    
    # CEAP de um senador específico
    ceap_pontes = await adm.get_ceap_senador("Marcos Pontes", 2026)
    
    # Remuneração de servidores
    remuneracao = await adm.get_remuneracao_servidores(2026, 1)
    
    # Contratos
    contratos = await adm.get_contratos(objeto="limpeza")
    
    await adm.close()
```

### Métodos Disponíveis (`SenadoAdmClient`)

**Senadores — CEAP e Benefícios:**
- `get_ceap(ano)` — Todas as despesas CEAP do ano
- `get_ceap_senador(nome, ano)` — CEAP filtrado por nome do senador
- `get_auxilio_moradia(nome?, estado?, partido?)` — Auxílio moradia / imóvel funcional
- `get_escritorios_apoio()` — Escritórios de apoio (endereço/telefone)
- `get_senadores_aposentados()` — Senadores aposentados e remuneração

**Servidores:**
- `get_servidores(tipo_vinculo?, situacao?, lotacao?)` — Lista com filtros
- `get_servidores_ativos()` — Ativos
- `get_servidores_comissionados()` — Comissionados
- `get_remuneracao_servidores(ano, mes)` — Remuneração mensal
- `get_horas_extras(ano, mes)` — Horas extras
- `get_estagiarios()` — Estagiários
- `get_pensionistas()` — Pensionistas
- `get_remuneracao_pensionistas(ano, mes)` — Remuneração de pensionistas

**Supridos (Cartão Corporativo):**
- `get_supridos(ano)` — Supridos do ano
- `get_supridos_transacoes(ano)` — Transações
- `get_supridos_movimentacoes(ano)` — Movimentações
- `get_supridos_empenhos(ano)` — Empenhos

**Contratações:**
- `get_contratos(fornecedor?, cnpj?, ano?, objeto?)` — Contratos
- `get_licitacoes(numero?, objeto?)` — Licitações
- `get_notas_empenho(fornecedor?, ano?)` — Notas de empenho
- `get_empresas_fornecedoras(nome?, cnpj?)` — Empresas cadastradas
- `get_terceirizados()` — Terceirizados
