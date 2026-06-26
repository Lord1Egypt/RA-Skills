# TSE Eleições - Cliente Python

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/olegantonov/tse-eleicoes/actions/workflows/tests.yml/badge.svg)](https://github.com/olegantonov/tse-eleicoes/actions)

Cliente Python assíncrono para as APIs do [TSE (Tribunal Superior Eleitoral)](https://www.tse.jus.br/).

Integra dois serviços:
- **DivulgaCandContas REST** — dados em tempo real de candidatos, eleições e prestação de contas
- **CKAN Dados Abertos** — portal de datasets oficiais para download em massa

## 📋 Características

- ✅ Cliente assíncrono com `httpx`
- ✅ Tratamento robusto de erros com retry automático (backoff exponencial)
- ✅ Logging estruturado
- ✅ Type hints completos (Python 3.11+)
- ✅ Sem necessidade de autenticação
- ✅ 30+ métodos cobrindo eleições, candidatos, prestação de contas e dados abertos
- ✅ Constantes prontas: IDs de eleições e códigos de cargos

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/olegantonov/tse-eleicoes.git
cd tse-eleicoes

# Instale as dependências
pip install -r requirements.txt

# Para desenvolvimento
pip install -r requirements-dev.txt
```

## 📖 Uso Básico

### Listar Eleições e Anos Eleitorais

```python
import asyncio
from tse_client import get_tse_client

async def main():
    client = get_tse_client()
    try:
        # Listar eleições ordinárias
        eleicoes = await client.get_eleicoes_ordinarias()

        # Anos com eleições disponíveis
        anos = await client.get_anos_eleitorais()
        print(f"Anos disponíveis: {anos}")
    finally:
        await client.close()

asyncio.run(main())
```

### Buscar Candidatos

```python
import asyncio
from tse_client import get_tse_client, ELEICOES_ORDINARIAS

async def main():
    client = get_tse_client()
    try:
        # Candidatos a prefeito em São Paulo nas Municipais 2024
        candidatos = await client.get_candidatos(
            ano=2024,
            municipio_cod="71072",   # código TSE de São Paulo
            eleicao_id=ELEICOES_ORDINARIAS["2024"],
            cargo_cod="11"           # 11 = Prefeito
        )

        for c in candidatos:
            print(f"{c.get('nomeUrna')} — {c.get('siglaPartido')}")

        # Filtrar por partido
        pt = await client.get_candidatos_por_partido(
            "PT", 2024, "71072", ELEICOES_ORDINARIAS["2024"], "11"
        )

        # Buscar por nome
        results = await client.buscar_candidato_por_nome(
            "Boulos", 2024, "71072", ELEICOES_ORDINARIAS["2024"], "11"
        )
    finally:
        await client.close()

asyncio.run(main())
```

### Detalhe de Candidato (bens, redes sociais, foto)

```python
async def main():
    client = get_tse_client()
    try:
        candidato = await client.get_candidato(
            ano=2024,
            municipio_cod="71072",
            eleicao_id="2045202024",
            candidato_id="280001636560"
        )

        # Bens declarados
        bens = await client.get_bens_candidato(2024, "71072", "2045202024", "280001636560")
        print(f"Total de bens: {len(bens)}")

        # Redes sociais
        redes = await client.get_redes_sociais_candidato(2024, "71072", "2045202024", "280001636560")

        # URL da foto
        foto = await client.get_foto_candidato_url(2024, "71072", "2045202024", "280001636560")
    finally:
        await client.close()
```

### Prestação de Contas

```python
async def main():
    client = get_tse_client()
    try:
        prestacao = await client.get_prestacao_contas(
            eleicao_id="2045202024",
            ano=2024,
            municipio_cod="71072",
            cargo_cod="11",
            candidato_id="280001636560"
        )

        # Top doadores
        ranking = await client.get_ranking_doadores(
            "2045202024", 2024, "71072", "11", "280001636560"
        )
        for doador in ranking[:5]:
            print(f"{doador.get('nome')}: R$ {doador.get('valor')}")
    finally:
        await client.close()
```

### Dados Abertos (CKAN)

```python
async def main():
    client = get_tse_client()
    try:
        # Listar todos os datasets
        datasets = await client.get_datasets()

        # Buscar datasets de candidatos
        candidatos_ds = await client.get_datasets_candidatos()

        # URL de download do ZIP de candidatos 2024
        url = await client.get_url_download_candidatos(2024)
        print(f"Download candidatos 2024: {url}")

        # URL de download dos resultados 2022
        url = await client.get_url_download_resultados(2022)
    finally:
        await client.close()
```

### Usando Constantes Prontas

```python
from tse_client import ELEICOES_ORDINARIAS, CARGOS, nome_cargo, nome_eleicao

# IDs de eleições conhecidos
print(ELEICOES_ORDINARIAS)
# {'2024': '2045202024', '2022': '2040602022', ...}

# Códigos de cargos
print(CARGOS)
# {'11': 'Prefeito', '13': 'Vereador', '5': 'Senador', ...}

# Lookup helpers
print(nome_cargo("11"))          # "Prefeito"
print(nome_eleicao("2045202024")) # "2024"
```

## 📚 Métodos Disponíveis

### Eleições
| Método | Descrição |
|--------|-----------|
| `get_eleicoes_ordinarias()` | Lista todas as eleições ordinárias |
| `get_anos_eleitorais()` | Lista anos eleitorais disponíveis |
| `get_cargos_municipio(eleicao_id, municipio_cod)` | Cargos disponíveis em um município |
| `get_eleicoes_suplementares_estados(ano)` | Estados com eleições suplementares |
| `get_eleicoes_suplementares(ano, uf)` | Eleições suplementares de um estado |

### Candidatos
| Método | Descrição |
|--------|-----------|
| `get_candidatos(ano, municipio_cod, eleicao_id, cargo_cod)` | Lista candidatos |
| `get_candidato(ano, municipio_cod, eleicao_id, candidato_id)` | Detalhe completo |
| `buscar_candidato_por_nome(nome, ...)` | Busca por nome (filtro local) |
| `get_bens_candidato(...)` | Bens declarados |
| `get_foto_candidato_url(...)` | URL da foto oficial |
| `get_redes_sociais_candidato(...)` | Redes sociais declaradas |
| `get_candidatos_eleitos(...)` | Filtra apenas eleitos |
| `get_candidatos_por_partido(sigla, ...)` | Filtra por partido |

### Prestação de Contas
| Método | Descrição |
|--------|-----------|
| `get_prestacao_contas(eleicao_id, ano, municipio_cod, cargo_cod, candidato_id)` | Prestação de contas completa |
| `get_ranking_doadores(...)` | Top doadores ordenados por valor |

### CKAN / Dados Abertos
| Método | Descrição |
|--------|-----------|
| `get_datasets()` | Lista todos os datasets |
| `buscar_datasets(termo)` | Busca por palavra-chave |
| `get_dataset(slug)` | Metadados e arquivos de um dataset |
| `get_datasets_candidatos()` | Datasets de candidatos |
| `get_datasets_resultados()` | Datasets de resultados eleitorais |
| `get_datasets_eleitorado()` | Datasets de eleitorado |
| `get_url_download_candidatos(ano)` | URL do ZIP de candidatos |
| `get_url_download_resultados(ano)` | URL do ZIP de resultados |

### Helpers e Constantes
| Símbolo | Descrição |
|---------|-----------|
| `ELEICOES_ORDINARIAS` | Dict `{ano: eleicao_id}` com IDs conhecidos |
| `CARGOS` | Dict `{codigo: nome}` com cargos eleitorais |
| `nome_cargo(codigo)` | Retorna nome do cargo pelo código |
| `nome_eleicao(eleicao_id)` | Retorna nome/ano da eleição pelo ID |

## 🔧 IDs de Eleições Conhecidos

| Ano | ID da Eleição | Tipo |
|-----|---------------|------|
| 2024 | `2045202024` | Municipais |
| 2022 | `2040602022` | Gerais (Federal) |
| 2020 | `2030402020` | Municipais |
| 2018 | `2022802018` | Gerais (Federal) |
| 2016 | `2` | Municipais |
| 2014 | `680` | Gerais |

## 🗳️ Códigos de Cargos

| Código | Cargo |
|--------|-------|
| 3 | Governador |
| 4 | Vice-Governador |
| 5 | Senador |
| 6 | Deputado Federal |
| 7 | Deputado Estadual |
| 11 | Prefeito |
| 12 | Vice-Prefeito |
| 13 | Vereador |

## 🧪 Testes

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

## 📎 Referências

- [DivulgaCandContas REST API](https://divulgacandcontas.tse.jus.br/divulga/)
- [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/)
- [CKAN API Docs](https://docs.ckan.org/en/2.10/api/)
- [TSE - Tribunal Superior Eleitoral](https://www.tse.jus.br/)

## 📄 Licença

MIT — veja [LICENSE](LICENSE) para detalhes.
