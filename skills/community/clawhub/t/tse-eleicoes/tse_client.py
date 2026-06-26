"""
Cliente async para APIs do TSE (Tribunal Superior Eleitoral).

Fontes:
    - DivulgaCandContas REST: https://divulgacandcontas.tse.jus.br/divulga/rest/v1
    - CKAN Dados Abertos: https://dadosabertos.tse.jus.br/api/3/action

Uso:
    from tse_client import get_tse_client

    async def main():
        client = get_tse_client()
        try:
            # Listar eleições ordinárias
            eleicoes = await client.get_eleicoes_ordinarias()

            # Buscar candidatos
            candidatos = await client.get_candidatos(
                ano=2024,
                municipio_cod="71072",
                eleicao_id="2045202024",
                cargo_cod="11"
            )

            # Dados abertos
            datasets = await client.get_datasets_candidatos()
        finally:
            await client.close()
"""
import asyncio
import logging
from typing import Any

import httpx


# Configurar logger
logger = logging.getLogger(__name__)


# ==================== EXCEÇÕES ====================

class TSEAPIError(Exception):
    """Erro base para erros da API do TSE."""
    pass


class TSEConnectionError(TSEAPIError):
    """Erro de conexão com a API."""
    pass


class TSETimeoutError(TSEAPIError):
    """Timeout ao conectar com a API."""
    pass


class TSENotFoundError(TSEAPIError):
    """Recurso não encontrado."""
    pass


class TSEValidationError(TSEAPIError):
    """Erro de validação de parâmetros."""
    pass


# ==================== CONSTANTES ====================

BASE_URL_DIVULGA = "https://divulgacandcontas.tse.jus.br/divulga/rest/v1"
BASE_URL_CKAN = "https://dadosabertos.tse.jus.br/api/3/action"

# Timeout padrão para requisições (45s)
DEFAULT_TIMEOUT = 45.0

# IDs de eleições ordinárias conhecidos
ELEICOES_ORDINARIAS: dict[str, str] = {
    "2024": "2045202024",
    "2022": "2040602022",
    "2020": "2030402020",
    "2018": "2022802018",
    "2016": "2",
    "2014": "680",
}

# Códigos de cargos eleitorais
CARGOS: dict[str, str] = {
    "3": "Governador",
    "4": "Vice-Governador",
    "5": "Senador",
    "6": "Deputado Federal",
    "7": "Deputado Estadual",
    "9": "1º Suplente",
    "10": "2º Suplente",
    "11": "Prefeito",
    "12": "Vice-Prefeito",
    "13": "Vereador",
}


def nome_cargo(codigo: str | int) -> str:
    """
    Retorna o nome do cargo pelo código.

    Args:
        codigo: Código do cargo (ex: '11' ou 11)

    Returns:
        Nome do cargo ou 'Cargo desconhecido' se não encontrado.
    """
    return CARGOS.get(str(codigo), "Cargo desconhecido")


def nome_eleicao(eleicao_id: str | int) -> str:
    """
    Retorna o nome/ano da eleição pelo ID.

    Args:
        eleicao_id: ID da eleição (ex: '2045202024')

    Returns:
        String descritiva da eleição ou o próprio ID se não encontrado.
    """
    inv = {v: k for k, v in ELEICOES_ORDINARIAS.items()}
    return inv.get(str(eleicao_id), f"Eleição {eleicao_id}")


# ==================== CLIENTE ====================

class TSEClient:
    """Cliente assíncrono para as APIs do TSE."""

    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        self._divulga_client: httpx.AsyncClient | None = None
        self._ckan_client: httpx.AsyncClient | None = None
        self.timeout = timeout

    async def _get_divulga_client(self) -> httpx.AsyncClient:
        """Retorna (ou cria) o cliente HTTP para a API DivulgaCandContas."""
        if self._divulga_client is None or self._divulga_client.is_closed:
            self._divulga_client = httpx.AsyncClient(
                base_url=BASE_URL_DIVULGA,
                timeout=httpx.Timeout(self.timeout),
                follow_redirects=True,
            )
        return self._divulga_client

    async def _get_ckan_client(self) -> httpx.AsyncClient:
        """Retorna (ou cria) o cliente HTTP para a API CKAN."""
        if self._ckan_client is None or self._ckan_client.is_closed:
            self._ckan_client = httpx.AsyncClient(
                base_url=BASE_URL_CKAN,
                timeout=httpx.Timeout(self.timeout),
                follow_redirects=True,
            )
        return self._ckan_client

    async def close(self):
        """Fecha os clientes HTTP."""
        if self._divulga_client and not self._divulga_client.is_closed:
            await self._divulga_client.aclose()
        if self._ckan_client and not self._ckan_client.is_closed:
            await self._ckan_client.aclose()

    async def _get(
        self,
        path: str,
        params: dict | None = None,
        retries: int = 3,
        _client_type: str = "divulga",
    ) -> dict:
        """
        Executa GET com retry e backoff exponencial.

        Args:
            path: Caminho do endpoint
            params: Parâmetros de query
            retries: Número de tentativas
            _client_type: 'divulga' ou 'ckan'

        Raises:
            TSETimeoutError: Timeout na requisição
            TSENotFoundError: Recurso não encontrado (404)
            TSEConnectionError: Erro de conexão
            TSEAPIError: Outros erros da API
        """
        if _client_type == "ckan":
            client = await self._get_ckan_client()
        else:
            client = await self._get_divulga_client()

        last_error: Exception | None = None

        for attempt in range(retries):
            try:
                logger.debug(f"GET {path} — tentativa {attempt + 1}/{retries}")
                response = await client.get(path, params=params)
                response.raise_for_status()
                return response.json()

            except httpx.TimeoutException as e:
                last_error = TSETimeoutError(f"Timeout ao acessar {path}: {e}")
                logger.warning(f"Timeout na tentativa {attempt + 1}/{retries}")
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise TSENotFoundError(f"Recurso não encontrado: {path}")
                last_error = TSEAPIError(f"Erro HTTP {e.response.status_code}: {e}")
                if e.response.status_code >= 500:
                    logger.warning(f"Erro {e.response.status_code} na tentativa {attempt + 1}/{retries}")
                    if attempt < retries - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                logger.error(f"Erro HTTP: {e}")
                break

            except httpx.ConnectError as e:
                last_error = TSEConnectionError(f"Erro de conexão: {e}")
                logger.warning(f"Erro de conexão na tentativa {attempt + 1}/{retries}")
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)

            except Exception as e:
                last_error = TSEAPIError(f"Erro inesperado: {e}")
                logger.error(f"Erro inesperado: {e}")
                break

        if last_error:
            raise last_error

        raise TSEAPIError("Falha após todas as tentativas")

    async def _get_divulga(self, path: str, params: dict | None = None, retries: int = 3) -> Any:
        """Atalho para chamadas à API DivulgaCandContas."""
        return await self._get(path, params=params, retries=retries, _client_type="divulga")

    async def _get_ckan(self, path: str, params: dict | None = None, retries: int = 3) -> dict:
        """Atalho para chamadas à API CKAN."""
        return await self._get(path, params=params, retries=retries, _client_type="ckan")

    # ==================== ELEIÇÕES ====================

    async def get_eleicoes_ordinarias(self) -> list[dict]:
        """
        Lista todas as eleições ordinárias disponíveis.

        Returns:
            Lista de dicionários com dados das eleições ordinárias.
        """
        data = await self._get_divulga("/eleicao/ordinarias")
        return data if isinstance(data, list) else data.get("eleicoes", data.get("results", []))

    async def get_anos_eleitorais(self) -> list[int]:
        """
        Lista os anos eleitorais disponíveis na API.

        Returns:
            Lista de anos (inteiros).
        """
        data = await self._get_divulga("/eleicao/anos-eleitorais")
        if isinstance(data, list):
            return data
        return data.get("anos", [])

    async def get_cargos_municipio(self, eleicao_id: str, municipio_cod: str) -> list[dict]:
        """
        Lista os cargos disponíveis em um município para uma eleição.

        Args:
            eleicao_id: ID da eleição (ex: '2045202024')
            municipio_cod: Código TSE do município (ex: '71072' para SP)

        Returns:
            Lista de dicionários com dados dos cargos.
        """
        data = await self._get_divulga(f"/eleicao/listar/municipios/{eleicao_id}/{municipio_cod}/cargos")
        if isinstance(data, list):
            return data
        return data.get("cargos", [])

    async def get_eleicoes_suplementares_estados(self, ano: int) -> list[dict]:
        """
        Lista os estados que tiveram eleições suplementares em um ano.

        Args:
            ano: Ano eleitoral (ex: 2022)

        Returns:
            Lista de dicionários com dados dos estados.
        """
        data = await self._get_divulga(f"/eleicao/estados/{ano}/ano")
        if isinstance(data, list):
            return data
        return data.get("estados", [])

    async def get_eleicoes_suplementares(self, ano: int, uf: str) -> list[dict]:
        """
        Lista as eleições suplementares de um estado em um ano.

        Args:
            ano: Ano eleitoral (ex: 2022)
            uf: Sigla do estado (ex: 'SP', 'MG')

        Returns:
            Lista de dicionários com dados das eleições suplementares.
        """
        data = await self._get_divulga(f"/eleicao/suplementares/{ano}/{uf.upper()}")
        if isinstance(data, list):
            return data
        return data.get("eleicoes", [])

    # ==================== CANDIDATOS ====================

    async def get_candidatos(
        self,
        ano: int,
        municipio_cod: str,
        eleicao_id: str,
        cargo_cod: str,
    ) -> list[dict]:
        """
        Lista os candidatos de um cargo em um município/eleição.

        Args:
            ano: Ano eleitoral
            municipio_cod: Código TSE do município
            eleicao_id: ID da eleição
            cargo_cod: Código do cargo (ex: '11' para Prefeito)

        Returns:
            Lista de dicionários com dados dos candidatos.
        """
        data = await self._get_divulga(
            f"/candidatura/listar/{ano}/{municipio_cod}/{eleicao_id}/{cargo_cod}/candidatos"
        )
        if isinstance(data, list):
            return data
        return data.get("candidatos", [])

    async def get_candidato(
        self,
        ano: int,
        municipio_cod: str,
        eleicao_id: str,
        candidato_id: str,
    ) -> dict:
        """
        Retorna os dados completos de um candidato (bens, redes sociais, foto, arquivos).

        Args:
            ano: Ano eleitoral
            municipio_cod: Código TSE do município
            eleicao_id: ID da eleição
            candidato_id: ID do candidato

        Returns:
            Dicionário com todos os dados do candidato.
        """
        return await self._get_divulga(
            f"/candidatura/buscar/{ano}/{municipio_cod}/{eleicao_id}/candidato/{candidato_id}"
        )

    async def buscar_candidato_por_nome(
        self,
        nome: str,
        ano: int,
        municipio_cod: str,
        eleicao_id: str,
        cargo_cod: str,
    ) -> list[dict]:
        """
        Busca candidatos por nome (filtro local sobre a listagem completa).

        Args:
            nome: Nome ou parte do nome do candidato
            ano: Ano eleitoral
            municipio_cod: Código TSE do município
            eleicao_id: ID da eleição
            cargo_cod: Código do cargo

        Returns:
            Lista de candidatos cujo nome contém o termo buscado.
        """
        todos = await self.get_candidatos(ano, municipio_cod, eleicao_id, cargo_cod)
        nome_lower = nome.lower()
        return [
            c for c in todos
            if nome_lower in c.get("nomeUrna", "").lower()
            or nome_lower in c.get("nomeCompleto", "").lower()
            or nome_lower in c.get("nome", "").lower()
        ]

    async def get_bens_candidato(
        self,
        ano: int,
        municipio_cod: str,
        eleicao_id: str,
        candidato_id: str,
    ) -> list[dict]:
        """
        Retorna apenas os bens declarados de um candidato.

        Args:
            ano: Ano eleitoral
            municipio_cod: Código TSE do município
            eleicao_id: ID da eleição
            candidato_id: ID do candidato

        Returns:
            Lista de bens declarados.
        """
        data = await self.get_candidato(ano, municipio_cod, eleicao_id, candidato_id)
        return data.get("bens", [])

    async def get_foto_candidato_url(
        self,
        ano: int,
        municipio_cod: str,
        eleicao_id: str,
        candidato_id: str,
    ) -> str | None:
        """
        Retorna a URL da foto de um candidato.

        Args:
            ano: Ano eleitoral
            municipio_cod: Código TSE do município
            eleicao_id: ID da eleição
            candidato_id: ID do candidato

        Returns:
            URL da foto ou None se não disponível.
        """
        data = await self.get_candidato(ano, municipio_cod, eleicao_id, candidato_id)
        return data.get("fotoUrl") or data.get("foto") or data.get("fotoPath")

    async def get_redes_sociais_candidato(
        self,
        ano: int,
        municipio_cod: str,
        eleicao_id: str,
        candidato_id: str,
    ) -> list[dict]:
        """
        Retorna as redes sociais declaradas de um candidato.

        Args:
            ano: Ano eleitoral
            municipio_cod: Código TSE do município
            eleicao_id: ID da eleição
            candidato_id: ID do candidato

        Returns:
            Lista de redes sociais.
        """
        data = await self.get_candidato(ano, municipio_cod, eleicao_id, candidato_id)
        return data.get("sites", data.get("redesSociais", []))

    async def get_candidatos_eleitos(
        self,
        ano: int,
        municipio_cod: str,
        eleicao_id: str,
        cargo_cod: str,
    ) -> list[dict]:
        """
        Retorna apenas os candidatos eleitos em um cargo/município.

        Args:
            ano: Ano eleitoral
            municipio_cod: Código TSE do município
            eleicao_id: ID da eleição
            cargo_cod: Código do cargo

        Returns:
            Lista de candidatos com situação de eleito.
        """
        todos = await self.get_candidatos(ano, municipio_cod, eleicao_id, cargo_cod)

        def _is_eleito(candidato: dict) -> bool:
            campos = [
                str(candidato.get("situacao", "")).lower(),
                str(candidato.get("descricaoSituacao", "")).lower(),
                str(candidato.get("situacaoTotalizacao", "")).lower(),
            ]
            for campo in campos:
                # Aceita "eleito" ou "eleita", mas rejeita "não eleito"
                if campo in ("eleito", "eleita", "elected"):
                    return True
                if campo.startswith("eleito") or campo.startswith("eleita"):
                    return True
            return False

        return [c for c in todos if _is_eleito(c)]

    async def get_candidatos_por_partido(
        self,
        sigla_partido: str,
        ano: int,
        municipio_cod: str,
        eleicao_id: str,
        cargo_cod: str,
    ) -> list[dict]:
        """
        Filtra candidatos pelo partido.

        Args:
            sigla_partido: Sigla do partido (ex: 'PT', 'PL', 'MDB')
            ano: Ano eleitoral
            municipio_cod: Código TSE do município
            eleicao_id: ID da eleição
            cargo_cod: Código do cargo

        Returns:
            Lista de candidatos do partido.
        """
        todos = await self.get_candidatos(ano, municipio_cod, eleicao_id, cargo_cod)
        sigla_upper = sigla_partido.upper()
        return [
            c for c in todos
            if sigla_upper in str(c.get("partido", {}).get("sigla", "")).upper()
            or sigla_upper in str(c.get("siglaPartido", "")).upper()
        ]

    # ==================== PRESTAÇÃO DE CONTAS ====================

    async def get_prestacao_contas(
        self,
        eleicao_id: str,
        ano: int,
        municipio_cod: str,
        cargo_cod: str,
        candidato_id: str,
    ) -> dict:
        """
        Retorna a prestação de contas de um candidato.

        Args:
            eleicao_id: ID da eleição
            ano: Ano eleitoral
            municipio_cod: Código TSE do município
            cargo_cod: Código do cargo
            candidato_id: ID do candidato

        Returns:
            Dicionário com dados da prestação de contas.
        """
        return await self._get_divulga(
            f"/prestador/consulta/{eleicao_id}/{ano}/{municipio_cod}/{cargo_cod}/90/90/{candidato_id}"
        )

    async def get_ranking_doadores(
        self,
        eleicao_id: str,
        ano: int,
        municipio_cod: str,
        cargo_cod: str,
        candidato_id: str,
    ) -> list[dict]:
        """
        Retorna o ranking de doadores de um candidato.

        Args:
            eleicao_id: ID da eleição
            ano: Ano eleitoral
            municipio_cod: Código TSE do município
            cargo_cod: Código do cargo
            candidato_id: ID do candidato

        Returns:
            Lista de doadores ordenada por valor.
        """
        data = await self.get_prestacao_contas(eleicao_id, ano, municipio_cod, cargo_cod, candidato_id)
        doadores = data.get("doadores", data.get("receitas", data.get("doadoresRanking", [])))
        if isinstance(doadores, list):
            return sorted(doadores, key=lambda x: float(x.get("valor", 0)), reverse=True)
        return []

    # ==================== CKAN / DADOS ABERTOS ====================

    async def get_datasets(self) -> list[str]:
        """
        Lista todos os datasets disponíveis no portal de dados abertos do TSE.

        Returns:
            Lista de slugs/IDs dos datasets.
        """
        data = await self._get_ckan("/package_list")
        return data.get("result", [])

    async def buscar_datasets(self, termo: str) -> list[dict]:
        """
        Busca datasets por termo/palavra-chave.

        Args:
            termo: Termo de busca (ex: 'candidatos', 'resultados')

        Returns:
            Lista de dicionários com metadados dos datasets encontrados.
        """
        data = await self._get_ckan("/package_search", params={"q": termo, "rows": 20})
        return data.get("result", {}).get("results", [])

    async def get_dataset(self, slug: str) -> dict:
        """
        Retorna os metadados e URLs de arquivos de um dataset.

        Args:
            slug: Identificador do dataset (ex: 'candidatos-2024')

        Returns:
            Dicionário com metadados e recursos do dataset.
        """
        data = await self._get_ckan("/package_show", params={"id": slug})
        return data.get("result", {})

    async def get_datasets_candidatos(self) -> list[dict]:
        """
        Retorna apenas os datasets relacionados a candidatos.

        Returns:
            Lista de datasets de candidatos.
        """
        return await self.buscar_datasets("candidatos")

    async def get_datasets_resultados(self) -> list[dict]:
        """
        Retorna apenas os datasets de resultados eleitorais.

        Returns:
            Lista de datasets de resultados.
        """
        return await self.buscar_datasets("resultados")

    async def get_datasets_eleitorado(self) -> list[dict]:
        """
        Retorna apenas os datasets de eleitorado.

        Returns:
            Lista de datasets de eleitorado.
        """
        return await self.buscar_datasets("eleitorado")

    async def get_url_download_candidatos(self, ano: int) -> str | None:
        """
        Retorna a URL de download do arquivo ZIP de candidatos de um ano.

        Args:
            ano: Ano eleitoral (ex: 2024)

        Returns:
            URL do arquivo ZIP ou None se não encontrado.
        """
        resultados = await self.buscar_datasets(f"candidatos {ano}")
        for dataset in resultados:
            recursos = dataset.get("resources", [])
            for recurso in recursos:
                url = recurso.get("url", "")
                if str(ano) in url and url.endswith(".zip"):
                    return url
        return None

    async def get_url_download_resultados(self, ano: int) -> str | None:
        """
        Retorna a URL de download do arquivo ZIP de resultados de um ano.

        Args:
            ano: Ano eleitoral (ex: 2022)

        Returns:
            URL do arquivo ZIP ou None se não encontrado.
        """
        resultados = await self.buscar_datasets(f"resultados {ano}")
        for dataset in resultados:
            recursos = dataset.get("resources", [])
            for recurso in recursos:
                url = recurso.get("url", "")
                if str(ano) in url and url.endswith(".zip"):
                    return url
        return None


# ==================== SINGLETON ====================

_client: TSEClient | None = None


def get_tse_client() -> TSEClient:
    """
    Retorna a instância singleton do TSEClient.

    Returns:
        Instância global do TSEClient.
    """
    global _client
    if _client is None:
        _client = TSEClient()
    return _client


async def close_tse_client():
    """Fecha e reseta o cliente global."""
    global _client
    if _client:
        await _client.close()
        _client = None


# ==================== FACADE FUNCTIONS ====================

async def get_eleicoes_ordinarias() -> list[dict]:
    """Facade: lista eleições ordinárias."""
    return await get_tse_client().get_eleicoes_ordinarias()


async def get_candidatos(ano: int, municipio_cod: str, eleicao_id: str, cargo_cod: str) -> list[dict]:
    """Facade: lista candidatos."""
    return await get_tse_client().get_candidatos(ano, municipio_cod, eleicao_id, cargo_cod)


async def get_datasets() -> list[str]:
    """Facade: lista todos os datasets."""
    return await get_tse_client().get_datasets()


async def buscar_datasets(termo: str) -> list[dict]:
    """Facade: busca datasets por termo."""
    return await get_tse_client().buscar_datasets(termo)
