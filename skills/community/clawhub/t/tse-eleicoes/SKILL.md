---
name: tse-eleicoes
description: >
  Cliente Python assíncrono para as APIs do TSE (Tribunal Superior Eleitoral).
  Integra DivulgaCandContas REST (candidatos, eleições, prestação de contas em tempo real)
  e CKAN Dados Abertos (datasets para download em massa).
  30+ métodos cobrindo: eleições ordinárias e suplementares, candidatos (detalhe, bens,
  foto, redes sociais, filtros por partido e situação), prestação de contas, ranking de
  doadores, datasets CKAN e URLs de download.
  Sem autenticação. Python 3.11+, httpx, retry com backoff exponencial.
version: 1.0.0
author: olegantonov
license: MIT
homepage: https://clawhub.ai
repository: https://github.com/olegantonov/tse-eleicoes
tags:
  - tse
  - eleicoes
  - candidatos
  - brasil
  - dados-abertos
  - api
  - async
---

# SKILL: tse-eleicoes

Use esta skill para acessar dados eleitorais do TSE (Tribunal Superior Eleitoral) diretamente via Python assíncrono.

## Quando Usar

- Buscar informações sobre candidatos (bens, redes sociais, foto, partido, situação)
- Listar eleições ordinárias ou suplementares por estado/município
- Consultar prestação de contas e ranking de doadores de campanha
- Baixar datasets oficiais (candidatos, resultados, eleitorado) via CKAN

## Como Usar

```python
import asyncio
from tse_client import get_tse_client, ELEICOES_ORDINARIAS, nome_cargo

async def main():
    client = get_tse_client()
    try:
        # Eleições disponíveis
        anos = await client.get_anos_eleitorais()

        # Candidatos a prefeito em SP — Municipais 2024
        candidatos = await client.get_candidatos(
            ano=2024,
            municipio_cod="71072",
            eleicao_id=ELEICOES_ORDINARIAS["2024"],
            cargo_cod="11"
        )

        # Dados abertos
        datasets = await client.get_datasets_candidatos()
        url_zip = await client.get_url_download_candidatos(2024)
    finally:
        await client.close()

asyncio.run(main())
```

## Instalação

```bash
git clone https://github.com/olegantonov/tse-eleicoes.git
cd tse-eleicoes
pip install -r requirements.txt
```

## APIs Integradas

- **DivulgaCandContas**: `https://divulgacandcontas.tse.jus.br/divulga/rest/v1`
- **CKAN Dados Abertos**: `https://dadosabertos.tse.jus.br/api/3/action`

## Principais Métodos

### Eleições
- `get_eleicoes_ordinarias()` — lista eleições ordinárias
- `get_anos_eleitorais()` — anos disponíveis
- `get_cargos_municipio(eleicao_id, municipio_cod)` — cargos por município
- `get_eleicoes_suplementares(ano, uf)` — eleições suplementares

### Candidatos
- `get_candidatos(ano, municipio_cod, eleicao_id, cargo_cod)` — lista candidatos
- `get_candidato(ano, municipio_cod, eleicao_id, candidato_id)` — detalhe completo
- `buscar_candidato_por_nome(nome, ...)` — busca por nome
- `get_bens_candidato(...)` — bens declarados
- `get_candidatos_eleitos(...)` — só eleitos
- `get_candidatos_por_partido(sigla, ...)` — filtra por partido

### Prestação de Contas
- `get_prestacao_contas(eleicao_id, ano, municipio_cod, cargo_cod, candidato_id)`
- `get_ranking_doadores(...)` — top doadores ordenados por valor

### Dados Abertos (CKAN)
- `get_datasets()` — lista todos os datasets
- `buscar_datasets(termo)` — busca por palavra-chave
- `get_datasets_candidatos()` / `get_datasets_resultados()` / `get_datasets_eleitorado()`
- `get_url_download_candidatos(ano)` / `get_url_download_resultados(ano)` — URLs dos ZIPs

## Constantes Úteis

```python
from tse_client import ELEICOES_ORDINARIAS, CARGOS, nome_cargo, nome_eleicao

ELEICOES_ORDINARIAS  # {'2024': '2045202024', '2022': '2040602022', ...}
CARGOS               # {'11': 'Prefeito', '13': 'Vereador', ...}
nome_cargo("11")     # "Prefeito"
nome_eleicao("2045202024")  # "2024"
```
