"""Testes unitários para senado_client."""
import pytest
from unittest.mock import AsyncMock, Mock, patch, PropertyMock
from datetime import date

from senado_client import (
    SenadoClient,
    get_senado_client,
    SenadoAPIError,
    SenadoTimeoutError,
    SenadoNotFoundError,
    SenadoConnectionError,
)


def _make_mock_client(responses):
    """Helper: cria mock httpx client com lista de respostas sequenciais."""
    mock_client = AsyncMock()
    type(mock_client).is_closed = PropertyMock(return_value=False)
    if isinstance(responses, list):
        mock_client.get.side_effect = responses
    else:
        mock_client.get.return_value = responses
    return mock_client


def _make_response(json_data, status_code=200):
    """Helper: cria mock de resposta HTTP."""
    resp = Mock()
    resp.json.return_value = json_data
    resp.raise_for_status = Mock()
    resp.status_code = status_code
    return resp


@pytest.mark.asyncio
class TestSenadoClient:
    """Testes do cliente do Senado."""

    async def test_client_initialization(self):
        """Testa inicialização do cliente."""
        client = SenadoClient()
        assert client.client is None
        assert client.timeout == 45.0

    async def test_custom_timeout(self):
        """Testa timeout customizado."""
        client = SenadoClient(timeout=10.0)
        assert client.timeout == 10.0

    async def test_get_singleton(self):
        """Testa padrão singleton."""
        import senado_client as mod
        mod._client = None
        client1 = get_senado_client()
        client2 = get_senado_client()
        assert client1 is client2
        mod._client = None

    @patch('senado_client.httpx.AsyncClient')
    async def test_lista_senadores_atuais_success(self, mock_httpx, mock_senado_response):
        """Testa listagem de senadores com sucesso."""
        mock_client = _make_mock_client(_make_response(mock_senado_response))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.lista_senadores_atuais()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['IdentificacaoParlamentar']['NomeParlamentar'] == "Renan Calheiros"

    @patch('senado_client.httpx.AsyncClient')
    async def test_buscar_senador_por_nome(self, mock_httpx, mock_senado_response):
        """Testa busca de senador por nome."""
        mock_client = _make_mock_client(_make_response(mock_senado_response))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.buscar_senador_por_nome("Renan")

        assert len(result) == 1
        assert "renan" in result[0]['IdentificacaoParlamentar']['NomeParlamentar'].lower()

    @patch('senado_client.httpx.AsyncClient')
    async def test_buscar_senador_nao_encontrado(self, mock_httpx, mock_senado_response):
        """Testa busca que não encontra nenhum senador."""
        mock_client = _make_mock_client(_make_response(mock_senado_response))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.buscar_senador_por_nome("NomeInexistente")

        assert len(result) == 0

    @patch('senado_client.httpx.AsyncClient')
    async def test_pesquisar_materia_success(self, mock_httpx, mock_materia_response):
        """Testa pesquisa de matérias."""
        mock_client = _make_mock_client(_make_response(mock_materia_response))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.pesquisar_materia(sigla="PL", ano=2026)

        assert isinstance(result, list)
        assert result[0]['SiglaSubtipoMateria'] == "PL"

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_with_timeout_and_retry(self, mock_httpx):
        """Testa retry após timeout."""
        import httpx
        success_resp = _make_response({"resultado": "ok"})
        mock_client = _make_mock_client([
            httpx.TimeoutException("Timeout"),
            success_resp,
        ])
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client._get("/test")
        assert result == {"resultado": "ok"}
        assert mock_client.get.call_count == 2

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_timeout_exhausts_retries(self, mock_httpx):
        """Testa que timeout esgota tentativas."""
        import httpx
        mock_client = AsyncMock()
        type(mock_client).is_closed = PropertyMock(return_value=False)
        mock_client.get.side_effect = httpx.TimeoutException("Timeout")
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        with pytest.raises(SenadoTimeoutError):
            await client._get("/test", retries=2)
        assert mock_client.get.call_count == 2

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_with_404_error(self, mock_httpx):
        """Testa tratamento de 404 (sem retry)."""
        import httpx
        mock_response = Mock()
        mock_response.status_code = 404
        mock_client = AsyncMock()
        type(mock_client).is_closed = PropertyMock(return_value=False)
        mock_client.get.side_effect = httpx.HTTPStatusError(
            "Not found", request=Mock(), response=mock_response
        )
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        with pytest.raises(SenadoNotFoundError):
            await client._get("/test")
        assert mock_client.get.call_count == 1

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_with_connection_error_and_retry(self, mock_httpx):
        """Testa retry após erro de conexão."""
        import httpx
        mock_client = AsyncMock()
        type(mock_client).is_closed = PropertyMock(return_value=False)
        mock_client.get.side_effect = httpx.ConnectError("Connection failed")
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        with pytest.raises(SenadoConnectionError):
            await client._get("/test", retries=2)
        assert mock_client.get.call_count == 2

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_list_finds_nested_list(self, mock_httpx):
        """Testa que _get_list navega JSON aninhado."""
        nested_data = {
            "ListaParlamentar": {
                "Parlamentares": {
                    "Parlamentar": [{"nome": "A"}, {"nome": "B"}]
                }
            }
        }
        mock_client = _make_mock_client(_make_response(nested_data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client._get_list("/test")

        assert len(result) == 2

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_list_empty_response(self, mock_httpx):
        """Testa _get_list com resposta vazia."""
        mock_client = _make_mock_client(_make_response({"Lista": {}}))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client._get_list("/test")

        assert result == []

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_agenda_plenario_dia(self, mock_httpx):
        """Testa busca de agenda do plenário."""
        mock_client = _make_mock_client(_make_response({"AgendaDia": {}}))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_agenda_plenario_dia(date(2026, 4, 2))

        assert isinstance(result, dict)
        mock_client.get.assert_called_once()

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_senador_votacoes(self, mock_httpx):
        """Testa novo endpoint: votações de senador."""
        data = {"VotacaoParlamentar": {"Votacoes": {"Votacao": [
            {"CodigoSessaoVotacao": "123", "DescricaoVotacao": "Aprovada"}
        ]}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_senador_votacoes("5012")

        assert isinstance(result, list)
        assert len(result) == 1

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_senador_comissoes(self, mock_httpx):
        """Testa novo endpoint: comissões de senador."""
        data = {"MembroComissaoParlamentar": {"Comissoes": {"Comissao": [
            {"SiglaComissao": "CAE"}
        ]}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_senador_comissoes("5012")

        assert isinstance(result, list)
        assert result[0]['SiglaComissao'] == "CAE"

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_materia_por_sigla(self, mock_httpx, mock_materia_response):
        """Testa busca de matéria por sigla completa."""
        mock_client = _make_mock_client(_make_response(mock_materia_response))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_materia_por_sigla("PL", "1234", 2026)

        assert result is not None
        assert result['SiglaSubtipoMateria'] == "PL"

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_materia_por_sigla_nao_encontrada(self, mock_httpx):
        """Testa busca de matéria inexistente."""
        empty_data = {"PesquisaBasicaMateria": {"Materias": {"Materia": []}}}
        mock_client = _make_mock_client(_make_response(empty_data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_materia_por_sigla("XY", "9999", 2099)

        assert result is None

    @patch('senado_client.httpx.AsyncClient')
    async def test_pesquisar_materia_por_assunto(self, mock_httpx, mock_materia_response):
        """Testa novo endpoint: pesquisa por assunto."""
        mock_client = _make_mock_client(_make_response(mock_materia_response))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.pesquisar_materia_por_assunto("educação")

        assert isinstance(result, list)

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_senador_filiacoes(self, mock_httpx):
        """Testa endpoint: filiações de senador."""
        data = {"FiliacaoParlamentar": {"Parlamentar": {"Filiacoes": {"Filiacao": [
            {"Partido": "MDB", "DataFiliacao": "2015-03-01"}
        ]}}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_senador_filiacoes("5012")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['Partido'] == "MDB"

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_senador_filiacoes_single_item(self, mock_httpx):
        """Testa filiações quando API retorna dict em vez de lista."""
        data = {"FiliacaoParlamentar": {"Parlamentar": {"Filiacoes": {"Filiacao": 
            {"Partido": "PT", "DataFiliacao": "2010-01-01"}
        }}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_senador_filiacoes("5012")

        assert isinstance(result, list)
        assert len(result) == 1

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_senador_cargos(self, mock_httpx):
        """Testa endpoint: cargos de senador."""
        data = {"CargoParlamentar": {"Parlamentar": {"Cargos": {"Cargo": [
            {"DescricaoCargo": "Presidente", "DataInicio": "2023-02-01"}
        ]}}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_senador_cargos("5012")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['DescricaoCargo'] == "Presidente"

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_materia_situacao_atual(self, mock_httpx):
        """Testa endpoint: situação atual de matéria."""
        data = {"SituacaoAtualMateria": {"IdentificacaoMateria": {"CodigoMateria": "123"}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_materia_situacao_atual("123")

        assert isinstance(result, dict)
        assert "SituacaoAtualMateria" in result

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_materia_emendas(self, mock_httpx):
        """Testa endpoint: emendas de matéria."""
        data = {"EmendasMateria": {"Materia": {"Emendas": {"Emenda": [
            {"CodigoEmenda": "1", "AutorEmenda": "Senador X"}
        ]}}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_materia_emendas("123")

        assert isinstance(result, list)
        assert len(result) == 1

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_materia_textos(self, mock_httpx):
        """Testa endpoint: textos de matéria."""
        data = {"TextosMateria": {"Materia": {"Textos": {"Texto": [
            {"UrlTexto": "http://example.com/texto.pdf", "TipoTexto": "Inicial"}
        ]}}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_materia_textos("123")

        assert isinstance(result, list)
        assert len(result) == 1

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_resultado_plenario_dia(self, mock_httpx):
        """Testa endpoint: resultado do plenário no dia."""
        data = {"ResultadoPlenario": {"Sessoes": {"Sessao": []}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_resultado_plenario_dia(date(2026, 4, 2))

        assert isinstance(result, dict)
        mock_client.get.assert_called_once()

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_votacoes_nominais_ano(self, mock_httpx):
        """Testa endpoint: votações nominais de um ano."""
        data = {"VotacoesNominais": {"Votacoes": {"Votacao": [
            {"CodigoSessao": "1", "Resultado": "Aprovado"},
            {"CodigoSessao": "2", "Resultado": "Rejeitado"}
        ]}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_votacoes_nominais_ano(2026)

        assert isinstance(result, list)
        assert len(result) == 2

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_discursos_plenario(self, mock_httpx):
        """Testa endpoint: discursos em plenário."""
        data = {"ListaDiscursosPlenario": {"Discursos": {"Discurso": [
            {"CodigoPronunciamento": "111", "NomeParlamentar": "Senador A"}
        ]}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_discursos_plenario(date(2026, 3, 1), date(2026, 3, 31))

        assert isinstance(result, list)
        assert len(result) == 1

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_comissao_detalhe(self, mock_httpx):
        """Testa endpoint: detalhe de comissão."""
        data = {"DetalheComissao": {"Comissao": {"SiglaComissao": "CAE", "NomeComissao": "Assuntos Econômicos"}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_comissao_detalhe("52")

        assert isinstance(result, dict)
        assert "DetalheComissao" in result

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_composicao_comissao(self, mock_httpx):
        """Testa endpoint: composição de comissão."""
        data = {"ComposicaoComissao": {"Comissao": {"Membros": {"Membro": [
            {"NomeParlamentar": "Senador A", "Cargo": "Titular"},
            {"NomeParlamentar": "Senador B", "Cargo": "Suplente"}
        ]}}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_composicao_comissao("52")

        assert isinstance(result, list)
        assert len(result) == 2

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_votacao_comissao(self, mock_httpx):
        """Testa endpoint: votações em comissão."""
        data = {"VotacaoComissao": {"Votacoes": {"Votacao": [
            {"CodigoVotacao": "1", "Resultado": "Aprovado"}
        ]}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_votacao_comissao("CAE")

        assert isinstance(result, list)
        assert len(result) == 1

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_mesa_senado(self, mock_httpx):
        """Testa endpoint: mesa diretora do Senado."""
        data = {"MesaSenado": {"Membros": {"Membro": [{"Cargo": "Presidente"}]}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_mesa_senado()

        assert isinstance(result, dict)
        assert "MesaSenado" in result

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_blocos_parlamentares(self, mock_httpx):
        """Testa endpoint: blocos parlamentares."""
        data = {"ListaBlocos": {"Blocos": {"Bloco": [
            {"NomeBloco": "Bloco A", "SiglaBloco": "BA"},
            {"NomeBloco": "Bloco B", "SiglaBloco": "BB"}
        ]}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_blocos_parlamentares()

        assert isinstance(result, list)
        assert len(result) == 2

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_processo(self, mock_httpx):
        """Testa endpoint: processo legislativo."""
        data = {"DetalheProcesso": {"Materia": {"Codigo": "123"}, "Autuacoes": {}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_processo("123")

        assert isinstance(result, dict)
        assert "DetalheProcesso" in result

    @patch('senado_client.httpx.AsyncClient')
    async def test_pesquisar_legislacao(self, mock_httpx):
        """Testa endpoint: pesquisa de legislação."""
        data = {"ListaLegislacao": {"Legislacoes": {"Legislacao": [
            {"Tipo": "LEI", "Numero": "14133", "Ano": "2021"}
        ]}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.pesquisar_legislacao(tipo="LEI", ano=2021)

        assert isinstance(result, list)
        assert len(result) == 1

    @patch('senado_client.httpx.AsyncClient')
    async def test_get_autores_atuais(self, mock_httpx):
        """Testa endpoint: lista de autores atuais."""
        data = {"ListaAutores": {"Autores": {"Autor": [
            {"CodigoAutor": "1", "NomeAutor": "Senador A"},
            {"CodigoAutor": "2", "NomeAutor": "Senador B"}
        ]}}}
        mock_client = _make_mock_client(_make_response(data))
        mock_httpx.return_value = mock_client

        client = SenadoClient()
        result = await client.get_autores_atuais()

        assert isinstance(result, list)
        assert len(result) == 2

    async def test_close_client(self):
        """Testa fechamento do cliente."""
        client = SenadoClient()
        client.client = AsyncMock()
        client.client.is_closed = False

        await client.close()

        client.client.aclose.assert_called_once()

    async def test_close_when_already_closed(self):
        """Testa close quando já fechado."""
        client = SenadoClient()
        client.client = AsyncMock()
        client.client.is_closed = True

        await client.close()
        client.client.aclose.assert_not_called()
