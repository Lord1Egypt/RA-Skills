"""Testes unitários para tse_client."""
import pytest
from unittest.mock import AsyncMock, Mock, patch, PropertyMock

from tse_client import (
    TSEClient,
    TSEAPIError,
    TSEConnectionError,
    TSETimeoutError,
    TSENotFoundError,
    get_tse_client,
    nome_cargo,
    nome_eleicao,
    ELEICOES_ORDINARIAS,
    CARGOS,
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


# ==================== TESTES DE CONSTANTES E HELPERS ====================

class TestConstantesHelpers:
    """Testes de constantes e funções auxiliares."""

    def test_eleicoes_ordinarias_dict(self):
        """Testa que o dicionário de eleições ordinárias contém entradas conhecidas."""
        assert "2024" in ELEICOES_ORDINARIAS
        assert ELEICOES_ORDINARIAS["2024"] == "2045202024"
        assert ELEICOES_ORDINARIAS["2022"] == "2040602022"

    def test_cargos_dict(self):
        """Testa que o dicionário de cargos contém entradas conhecidas."""
        assert "11" in CARGOS
        assert CARGOS["11"] == "Prefeito"
        assert CARGOS["13"] == "Vereador"

    def test_nome_cargo_conhecido(self):
        """Testa nome_cargo com código válido."""
        assert nome_cargo("11") == "Prefeito"
        assert nome_cargo(13) == "Vereador"
        assert nome_cargo("5") == "Senador"

    def test_nome_cargo_desconhecido(self):
        """Testa nome_cargo com código inválido."""
        assert nome_cargo("99") == "Cargo desconhecido"
        assert nome_cargo("0") == "Cargo desconhecido"

    def test_nome_eleicao_conhecida(self):
        """Testa nome_eleicao com ID válido."""
        resultado = nome_eleicao("2045202024")
        assert "2024" in resultado

    def test_nome_eleicao_desconhecida(self):
        """Testa nome_eleicao com ID desconhecido."""
        resultado = nome_eleicao("9999999999")
        assert "9999999999" in resultado


# ==================== TESTES DO CLIENTE ====================

@pytest.mark.asyncio
class TestTSEClient:
    """Testes do TSEClient."""

    async def test_client_initialization(self):
        """Testa inicialização do cliente."""
        client = TSEClient()
        assert client._divulga_client is None
        assert client._ckan_client is None
        assert client.timeout == 45.0

    async def test_custom_timeout(self):
        """Testa timeout customizado."""
        client = TSEClient(timeout=10.0)
        assert client.timeout == 10.0

    async def test_get_singleton(self):
        """Testa padrão singleton."""
        import tse_client as mod
        mod._client = None
        c1 = get_tse_client()
        c2 = get_tse_client()
        assert c1 is c2
        mod._client = None

    # ========== ELEIÇÕES ==========

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_eleicoes_ordinarias_lista(self, mock_httpx):
        """Testa get_eleicoes_ordinarias com resposta em lista."""
        payload = [{"id": "2045202024", "nome": "Eleições Municipais 2024"}]
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_eleicoes_ordinarias()

        assert isinstance(result, list)
        assert result[0]["id"] == "2045202024"

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_eleicoes_ordinarias_dict(self, mock_httpx):
        """Testa get_eleicoes_ordinarias com resposta em dicionário."""
        payload = {"eleicoes": [{"id": "2045202024"}]}
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_eleicoes_ordinarias()

        assert isinstance(result, list)
        assert result[0]["id"] == "2045202024"

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_anos_eleitorais(self, mock_httpx):
        """Testa get_anos_eleitorais."""
        payload = [2024, 2022, 2020, 2018]
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_anos_eleitorais()

        assert isinstance(result, list)
        assert 2024 in result

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_cargos_municipio(self, mock_httpx):
        """Testa get_cargos_municipio."""
        payload = {"cargos": [{"codigo": "11", "nome": "Prefeito"}]}
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_cargos_municipio("2045202024", "71072")

        assert isinstance(result, list)
        assert result[0]["codigo"] == "11"

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_eleicoes_suplementares_estados(self, mock_httpx):
        """Testa get_eleicoes_suplementares_estados."""
        payload = [{"sigla": "SP"}, {"sigla": "MG"}]
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_eleicoes_suplementares_estados(2022)

        assert isinstance(result, list)

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_eleicoes_suplementares(self, mock_httpx):
        """Testa get_eleicoes_suplementares."""
        payload = {"eleicoes": [{"id": "123", "nome": "Suplementar SP"}]}
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_eleicoes_suplementares(2022, "SP")

        assert isinstance(result, list)

    # ========== CANDIDATOS ==========

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_candidatos_success(self, mock_httpx):
        """Testa listagem de candidatos com sucesso."""
        payload = {"candidatos": [
            {"id": "123", "nomeUrna": "LULA", "siglaPartido": "PT"},
            {"id": "456", "nomeUrna": "BOLSONARO", "siglaPartido": "PL"},
        ]}
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_candidatos(2022, "71072", "2040602022", "1")

        assert isinstance(result, list)
        assert len(result) == 2

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_candidato_detalhe(self, mock_httpx):
        """Testa detalhe completo de candidato."""
        payload = {
            "id": "123",
            "nomeUrna": "LULA",
            "bens": [{"descricao": "Imóvel", "valor": "500000"}],
            "sites": [{"url": "https://lula.com.br", "tipo": "site"}],
        }
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_candidato(2022, "71072", "2040602022", "123")

        assert result["nomeUrna"] == "LULA"

    @patch("tse_client.httpx.AsyncClient")
    async def test_buscar_candidato_por_nome(self, mock_httpx):
        """Testa busca de candidato por nome."""
        payload = {"candidatos": [
            {"id": "1", "nomeUrna": "JOÃO SILVA", "nomeCompleto": "João da Silva"},
            {"id": "2", "nomeUrna": "MARIA SOUZA", "nomeCompleto": "Maria de Souza"},
        ]}
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.buscar_candidato_por_nome("joão", 2024, "71072", "2045202024", "11")

        assert len(result) == 1
        assert "JOÃO" in result[0]["nomeUrna"]

    @patch("tse_client.httpx.AsyncClient")
    async def test_buscar_candidato_nao_encontrado(self, mock_httpx):
        """Testa busca que não encontra candidato."""
        payload = {"candidatos": [{"id": "1", "nomeUrna": "JOÃO"}]}
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.buscar_candidato_por_nome("ZZZNAOEXISTE", 2024, "71072", "2045202024", "11")

        assert len(result) == 0

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_bens_candidato(self, mock_httpx):
        """Testa extração de bens do candidato."""
        payload = {
            "id": "123",
            "bens": [
                {"descricao": "Veículo", "valor": "80000"},
                {"descricao": "Imóvel", "valor": "300000"},
            ],
        }
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_bens_candidato(2024, "71072", "2045202024", "123")

        assert isinstance(result, list)
        assert len(result) == 2

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_foto_candidato_url(self, mock_httpx):
        """Testa extração de URL da foto do candidato."""
        payload = {
            "id": "123",
            "fotoUrl": "https://example.com/foto.jpg",
        }
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_foto_candidato_url(2024, "71072", "2045202024", "123")

        assert result == "https://example.com/foto.jpg"

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_redes_sociais_candidato(self, mock_httpx):
        """Testa extração de redes sociais do candidato."""
        payload = {
            "id": "123",
            "sites": [
                {"url": "https://instagram.com/candidato", "tipo": "instagram"},
            ],
        }
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_redes_sociais_candidato(2024, "71072", "2045202024", "123")

        assert isinstance(result, list)
        assert len(result) == 1

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_candidatos_eleitos(self, mock_httpx):
        """Testa filtro de candidatos eleitos."""
        payload = {"candidatos": [
            {"id": "1", "nomeUrna": "ELEITO", "situacao": "eleito"},
            {"id": "2", "nomeUrna": "NAO ELEITO", "situacao": "não eleito"},
        ]}
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_candidatos_eleitos(2024, "71072", "2045202024", "11")

        assert len(result) == 1
        assert result[0]["nomeUrna"] == "ELEITO"

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_candidatos_por_partido(self, mock_httpx):
        """Testa filtro de candidatos por partido."""
        payload = {"candidatos": [
            {"id": "1", "nomeUrna": "CANDIDATO PT", "siglaPartido": "PT"},
            {"id": "2", "nomeUrna": "CANDIDATO PL", "siglaPartido": "PL"},
        ]}
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_candidatos_por_partido("PT", 2022, "71072", "2040602022", "1")

        assert len(result) == 1
        assert result[0]["siglaPartido"] == "PT"

    # ========== PRESTAÇÃO DE CONTAS ==========

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_prestacao_contas(self, mock_httpx):
        """Testa prestação de contas."""
        payload = {
            "totalReceitas": 100000,
            "totalDespesas": 95000,
            "doadores": [{"nome": "Fulano", "valor": "10000"}],
        }
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_prestacao_contas("2045202024", 2024, "71072", "11", "123")

        assert result["totalReceitas"] == 100000

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_ranking_doadores(self, mock_httpx):
        """Testa ranking de doadores (ordenado por valor desc)."""
        payload = {
            "doadores": [
                {"nome": "B", "valor": "5000"},
                {"nome": "A", "valor": "20000"},
                {"nome": "C", "valor": "1000"},
            ],
        }
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_ranking_doadores("2045202024", 2024, "71072", "11", "123")

        assert isinstance(result, list)
        assert float(result[0]["valor"]) >= float(result[1]["valor"])

    # ========== CKAN / DADOS ABERTOS ==========

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_datasets(self, mock_httpx):
        """Testa listagem de datasets CKAN."""
        payload = {"result": ["candidatos-2024", "resultados-2022", "eleitorado-2024"]}
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_datasets()

        assert isinstance(result, list)
        assert "candidatos-2024" in result

    @patch("tse_client.httpx.AsyncClient")
    async def test_buscar_datasets(self, mock_httpx):
        """Testa busca de datasets por termo."""
        payload = {
            "result": {
                "results": [
                    {"id": "candidatos-2024", "title": "Candidatos 2024"},
                ]
            }
        }
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.buscar_datasets("candidatos")

        assert isinstance(result, list)
        assert result[0]["id"] == "candidatos-2024"

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_dataset(self, mock_httpx):
        """Testa busca de dataset por slug."""
        payload = {
            "result": {
                "id": "candidatos-2024",
                "title": "Candidatos 2024",
                "resources": [{"url": "https://example.com/file.zip"}],
            }
        }
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_dataset("candidatos-2024")

        assert result["id"] == "candidatos-2024"

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_url_download_candidatos(self, mock_httpx):
        """Testa URL de download de candidatos."""
        payload = {
            "result": {
                "results": [
                    {
                        "id": "candidatos-2024",
                        "resources": [
                            {"url": "https://cdn.tse.jus.br/candidatos_2024.zip"},
                        ],
                    }
                ]
            }
        }
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_url_download_candidatos(2024)

        assert result is not None
        assert "2024" in result
        assert result.endswith(".zip")

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_url_download_candidatos_nao_encontrado(self, mock_httpx):
        """Testa URL de download quando não encontrado."""
        payload = {"result": {"results": []}}
        mock_client = _make_mock_client(_make_response(payload))
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client.get_url_download_candidatos(2024)

        assert result is None

    # ========== TRATAMENTO DE ERROS ==========

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_timeout_retry(self, mock_httpx):
        """Testa retry após timeout."""
        import httpx
        success = _make_response({"ok": True})
        mock_client = _make_mock_client([
            httpx.TimeoutException("Timeout"),
            success,
        ])
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client._get_divulga("/test")

        assert result == {"ok": True}
        assert mock_client.get.call_count == 2

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_timeout_exhausts_retries(self, mock_httpx):
        """Testa que timeout esgota tentativas e lança TSETimeoutError."""
        import httpx
        mock_client = AsyncMock()
        type(mock_client).is_closed = PropertyMock(return_value=False)
        mock_client.get.side_effect = httpx.TimeoutException("Timeout")
        mock_httpx.return_value = mock_client

        client = TSEClient()
        with pytest.raises(TSETimeoutError):
            await client._get("/test", retries=2)

        assert mock_client.get.call_count == 2

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_404_raises_not_found(self, mock_httpx):
        """Testa que 404 lança TSENotFoundError."""
        import httpx
        mock_response = Mock()
        mock_response.status_code = 404
        mock_client = AsyncMock()
        type(mock_client).is_closed = PropertyMock(return_value=False)
        mock_client.get.side_effect = httpx.HTTPStatusError(
            "Not Found", request=Mock(), response=mock_response
        )
        mock_httpx.return_value = mock_client

        client = TSEClient()
        with pytest.raises(TSENotFoundError):
            await client._get("/test")

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_connection_error(self, mock_httpx):
        """Testa que erro de conexão lança TSEConnectionError."""
        import httpx
        mock_client = AsyncMock()
        type(mock_client).is_closed = PropertyMock(return_value=False)
        mock_client.get.side_effect = httpx.ConnectError("Connection refused")
        mock_httpx.return_value = mock_client

        client = TSEClient()
        with pytest.raises(TSEConnectionError):
            await client._get("/test", retries=1)

    @patch("tse_client.httpx.AsyncClient")
    async def test_get_500_retry(self, mock_httpx):
        """Testa retry em erro 500."""
        import httpx
        mock_response_500 = Mock()
        mock_response_500.status_code = 500
        success = _make_response({"data": "ok"})
        mock_client = AsyncMock()
        type(mock_client).is_closed = PropertyMock(return_value=False)
        mock_client.get.side_effect = [
            httpx.HTTPStatusError("Server Error", request=Mock(), response=mock_response_500),
            success,
        ]
        mock_httpx.return_value = mock_client

        client = TSEClient()
        result = await client._get("/test")

        assert result == {"data": "ok"}
