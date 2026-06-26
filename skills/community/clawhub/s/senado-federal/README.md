# Senado Federal - Cliente Python

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Cliente Python assíncrono para a [API de Dados Abertos do Senado Federal](https://legis.senado.leg.br/dadosabertos).

## 📋 Características

- ✅ Cliente assíncrono com `httpx`
- ✅ Tratamento robusto de erros com retry automático
- ✅ Logging estruturado
- ✅ Type hints completos
- ✅ Sem necessidade de autenticação
- ✅ Suporte a todas as principais funcionalidades da API

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/olegantonov/senado-federal.git
cd senado-federal

# Instale as dependências
pip install -r requirements.txt

# Para desenvolvimento
pip install -r requirements-dev.txt
```

## 📖 Uso Básico

### Buscar Senadores

```python
import asyncio
from senado_client import get_senado_client

async def main():
    client = get_senado_client()
    try:
        # Listar todos os senadores em exercício
        senadores = await client.lista_senadores_atuais()
        
        # Buscar por nome
        resultado = await client.buscar_senador_por_nome("Bolsonaro")
        
        for senador in resultado:
            nome = senador['IdentificacaoParlamentar']['NomeParlamentar']
            partido = senador['IdentificacaoParlamentar']['SiglaPartidoParlamentar']
            uf = senador['IdentificacaoParlamentar']['UfParlamentar']
            print(f"{nome} ({partido}-{uf})")
    finally:
        await client.close()

asyncio.run(main())
```

### Pesquisar Matérias/Proposições

```python
# Buscar PLs de 2026 em tramitação
materias = await client.pesquisar_materia(
    sigla="PL",
    ano=2026,
    tramitando=True
)

for materia in materias:
    print(f"{materia['SiglaSubtipoMateria']} {materia['NumeroMateria']}/{materia['AnoMateria']}")
    print(f"Ementa: {materia['EmentaMateria']}")
```

### Agenda do Plenário

```python
from datetime import date

# Agenda de hoje
agenda = await client.get_agenda_plenario_dia()

# Agenda de uma data específica
agenda = await client.get_agenda_plenario_dia(date(2026, 4, 2))

# Agenda do mês
agenda_mes = await client.get_agenda_plenario_mes(2026, 4)
```

### Votações Recentes

```python
from datetime import date, timedelta

# Últimas 7 dias
inicio = date.today() - timedelta(days=7)
fim = date.today()

votacoes = await client.get_votacoes_periodo(inicio, fim)

for votacao in votacoes:
    print(f"Sessão: {votacao['DescricaoSessao']}")
    print(f"Data: {votacao['DataSessao']}")
```

### Discursos de um Senador

```python
# Buscar código do senador
senador = await client.buscar_senador_por_nome("Renan Calheiros")
codigo = senador[0]['IdentificacaoParlamentar']['CodigoParlamentar']

# Obter discursos
discursos = await client.get_discursos_senador(codigo)

for discurso in discursos:
    print(f"{discurso['DataDiscurso']}: {discurso['TipoDiscurso']}")
```

### Processo Legislativo Completo

```python
# Obter processo legislativo com dados detalhados
processo = await client.get_processo("123456")
# Inclui autuações, situações, tramitação completa
```

### Composição de Comissão

```python
# Membros de uma comissão
membros = await client.get_composicao_comissao("52")

for membro in membros:
    print(f"{membro.get('NomeParlamentar')} - {membro.get('DescricaoCargo')}")
```

### Votações Nominais do Ano

```python
# Todas as votações nominais de 2026
votacoes = await client.get_votacoes_nominais_ano(2026)

for v in votacoes:
    print(f"{v.get('DataSessao')}: {v.get('DescricaoResultado')}")
```

### Pesquisar Legislação

```python
# Buscar leis por tipo e ano
leis = await client.pesquisar_legislacao(tipo="LEI", ano=2024)

for lei in leis:
    print(f"{lei.get('Tipo')} {lei.get('Numero')}/{lei.get('Ano')}")
```

## 🔧 Funcionalidades Principais

### Senadores
- `lista_senadores_atuais()` - Senadores em exercício
- `buscar_senador_por_nome(nome)` - Busca por nome
- `get_senador_detalhe(codigo)` - Detalhes completos
- `get_autorias_senador(codigo)` - Matérias de autoria
- `get_discursos_senador(codigo)` - Discursos e pronunciamentos
- `get_senador_votacoes(codigo)` - Histórico de votações
- `get_senador_comissoes(codigo)` - Comissões de que é membro
- `get_senador_mandatos(codigo)` - Mandatos
- `get_senador_filiacoes(codigo)` - Filiações partidárias
- `get_senador_cargos(codigo)` - Cargos exercidos
- `get_senador_liderancas(codigo)` - Lideranças
- `get_senador_apartes(codigo)` - Apartes/intervenções
- `get_senador_relatorias(codigo)` - Relatorias
- `get_senador_profissao(codigo)` - Profissão
- `get_senador_historico_academico(codigo)` - Histórico acadêmico
- `get_senador_licencas(codigo)` - Licenças

### Matérias
- `pesquisar_materia(sigla, numero, ano, tramitando)` - Busca de proposições
- `pesquisar_materia_por_assunto(assunto)` - Busca por assunto
- `get_materia_detalhe(codigo)` - Detalhes da matéria
- `get_materia_movimentacoes(codigo)` - Tramitação completa
- `get_materia_situacao_atual(codigo)` - Situação atual
- `get_materia_textos(codigo)` - Textos da matéria
- `get_materia_emendas(codigo)` - Emendas
- `get_materia_relatorias(codigo)` - Relatorias
- `get_materia_autoria(codigo)` - Autoria
- `get_materias_tramitando()` - Em tramitação
- `get_materias_atualizadas(dias)` - Atualizadas recentemente
- `get_materias_recentes(dias)` - Matérias recentes

### Plenário
- `get_agenda_plenario_dia(data)` - Agenda diária
- `get_agenda_plenario_mes(ano, mes)` - Agenda mensal
- `get_votacoes_periodo(inicio, fim)` - Votações em período
- `get_votacoes_semana()` - Votações da semana
- `get_resultado_plenario_dia(data)` - Resultado do plenário no dia
- `get_resultado_plenario_mes(ano, mes)` - Resultado mensal
- `get_votacoes_nominais_ano(ano)` - Votações nominais de um ano
- `get_discursos_plenario(inicio, fim)` - Discursos em plenário
- `get_encontro_plenario(codigo)` - Detalhes de sessão
- `get_encontro_pauta(codigo)` - Pauta de sessão

### Comissões
- `get_lista_comissoes()` - Lista de comissões
- `get_agenda_comissao_dia(data)` - Agenda do dia
- `get_agenda_comissao_periodo(inicio, fim)` - Agenda de período
- `get_comissao_detalhe(codigo)` - Detalhes de comissão
- `get_comissao_reuniao(codigo_reuniao)` - Detalhes de reunião
- `get_composicao_comissao(codigo)` - Membros da comissão
- `get_lista_comissoes_mistas()` - Comissões mistas

### Votação em Comissões
- `get_votacao_comissao(sigla)` - Votações de uma comissão
- `get_votacao_comissao_materia(sigla, numero, ano)` - Votações sobre matéria
- `get_votacao_comissao_parlamentar(codigo)` - Votações de parlamentar

### Composição e Lideranças
- `get_mesa_senado()` - Mesa diretora do Senado
- `get_mesa_congresso()` - Mesa do Congresso Nacional
- `get_liderancas()` - Lideranças partidárias
- `get_blocos_parlamentares()` - Blocos parlamentares

### Processo Legislativo
- `get_processo(codigo)` - Processo legislativo completo

### Autores, Legislação, Discurso
- `get_autores_atuais()` - Lista de autores atuais
- `pesquisar_legislacao(tipo, ano, numero)` - Pesquisa legislação
- `get_discurso_texto_integral(codigo)` - Texto integral de discurso

## ⚠️ Tratamento de Erros

O cliente possui exceções específicas:

```python
from senado_client import (
    SenadoAPIError,         # Erro genérico
    SenadoTimeoutError,     # Timeout
    SenadoNotFoundError,    # 404
    SenadoConnectionError,  # Erro de conexão
    SenadoValidationError   # Validação de parâmetros
)

try:
    senadores = await client.lista_senadores_atuais()
except SenadoTimeoutError:
    print("A API está demorando para responder")
except SenadoNotFoundError:
    print("Recurso não encontrado")
except SenadoAPIError as e:
    print(f"Erro na API: {e}")
```

## 📝 Logging

Para habilitar logs:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🔗 Recursos

- [Documentação da API](https://legis.senado.leg.br/dadosabertos)
- [Swagger UI](https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html)
- [SKILL.md](SKILL.md) - Referência completa de endpoints

## 🧪 Testes

```bash
# Executar testes
pytest

# Com coverage
pytest --cov=senado_client --cov-report=html

# Apenas testes unitários
pytest tests/unit/

# Apenas testes de integração
pytest tests/integration/
```

## 📄 Licença

MIT License

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 👨💻 Autor

Daniel Marques - [@olegantonov](https://github.com/olegantonov)

## 🙏 Agradecimentos

- Senado Federal pela disponibilização da API de Dados Abertos
- Comunidade Python Brasil
