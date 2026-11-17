"""Testes de integração (requerem conexão com a API real)."""

from datetime import date, timedelta

import pytest

from senado_client import SenadoAdmClient, get_senado_client


@pytest.mark.integration
@pytest.mark.asyncio
class TestSenadoIntegration:
    """Testes de integração com a API real."""

    async def test_lista_senadores_atuais_real(self):
        """Testa listagem real de senadores."""
        client = get_senado_client()
        try:
            senadores = await client.lista_senadores_atuais()

            assert isinstance(senadores, list)
            assert len(senadores) > 50  # Brasil tem 81 senadores

            # Verifica estrutura
            senador = senadores[0]
            assert "IdentificacaoParlamentar" in senador
            assert "NomeParlamentar" in senador["IdentificacaoParlamentar"]
        finally:
            await client.close()

    async def test_pesquisar_materia_real(self):
        """Testa pesquisa real de matérias."""
        client = get_senado_client()
        try:
            materias = await client.pesquisar_materia(sigla="PL", ano=2024, tramitando=True)

            assert isinstance(materias, list)
            if len(materias) > 0:
                materia = materias[0]
                # API retorna campos como Sigla, Ano, Codigo, Autor
                assert "Sigla" in materia or "Codigo" in materia
        finally:
            await client.close()

    async def test_get_agenda_plenario_real(self):
        """Testa busca real de agenda."""
        client = get_senado_client()
        try:
            agenda = await client.get_agenda_plenario_dia()

            assert isinstance(agenda, dict)
            # Agenda pode estar vazia em dias sem sessão
        finally:
            await client.close()

    async def test_get_votacoes_periodo_real(self):
        """Testa busca real de votações."""
        client = get_senado_client()
        try:
            fim = date.today()
            inicio = fim - timedelta(days=30)

            votacoes = await client.get_votacoes_periodo(inicio, fim)

            assert isinstance(votacoes, list)
            # Pode estar vazio se não houver votações no período
        finally:
            await client.close()

    async def test_senator_nested_contracts_real(self):
        """Garante que os caminhos aninhados atuais não virem listas vazias."""
        client = get_senado_client()
        try:
            autorias = await client.get_autorias_senador("6009")
            mandatos = await client.get_senador_mandatos("6009")

            assert autorias and "IdentificacaoProcesso" in autorias[0]["Materia"]
            assert mandatos and "CodigoMandato" in mandatos[0]
        finally:
            await client.close()

    async def test_historical_cohort_real(self):
        """Usa a rota de intervalo para obter a coorte completa da legislatura."""
        client = get_senado_client()
        try:
            coorte = await client.lista_senadores_legislatura(57)

            assert len(coorte) > 81
            assert "IdentificacaoParlamentar" in coorte[0]
        finally:
            await client.close()

    async def test_process_author_filter_real(self):
        """Valida a busca de autoria na API de processos."""
        client = get_senado_client()
        try:
            processos = await client.pesquisar_processos(autor="Astronauta Marcos Pontes", tramitando=True)

            assert processos
            assert all("Astronauta Marcos Pontes" in item["autoria"] for item in processos)
        finally:
            await client.close()

    async def test_ceap_contract_real(self):
        """Valida o campo monetário real da CEAP."""
        client = SenadoAdmClient(timeout=90)
        try:
            despesas = await client.get_ceap(date.today().year)

            assert despesas
            assert "valorReembolsado" in despesas[0]
        finally:
            await client.close()
