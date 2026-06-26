"""Testes de integração (requerem conexão com a API real)."""
import pytest
from datetime import date, timedelta

from senado_client import get_senado_client


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
            assert 'IdentificacaoParlamentar' in senador
            assert 'NomeParlamentar' in senador['IdentificacaoParlamentar']
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
                assert 'Sigla' in materia or 'Codigo' in materia
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
