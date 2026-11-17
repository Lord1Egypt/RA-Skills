"""
Cliente async para API de Dados Abertos do Senado Federal.
Base: https://legis.senado.leg.br/dadosabertos

Uso:
    from senate_client import get_senado_client

    async def main():
        client = get_senado_client()
        try:
            # Listar senadores atuais
            senators = await client.lista_senadores_atuais()

            # Pesquisar matérias
            materias = await client.pesquisar_materia(sigla="PL", ano=2026)

            # Votações da semana
            from datetime import date, timedelta
            votacoes = await client.get_votacoes_periodo(
                date.today() - timedelta(days=7),
                date.today()
            )
        finally:
            await client.close()
"""

import asyncio
import logging
from datetime import date, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

import httpx

# Configurar logger
logger = logging.getLogger(__name__)


# Exceções customizadas
class SenadoAPIError(Exception):
    """Erro base para erros da API do Senado."""

    pass


class SenadoConnectionError(SenadoAPIError):
    """Erro de conexão com a API."""

    pass


class SenadoTimeoutError(SenadoAPIError):
    """Timeout ao conectar com a API."""

    pass


class SenadoNotFoundError(SenadoAPIError):
    """Recurso não encontrado."""

    pass


class SenadoValidationError(SenadoAPIError):
    """Erro de validação de parâmetros."""

    pass


BASE_URL = "https://legis.senado.leg.br/dadosabertos"

# Timeout padrão para requisições (45s)
DEFAULT_TIMEOUT = 45.0
BRASILIA_TZ = ZoneInfo("America/Sao_Paulo")


def _today_brasilia() -> date:
    return datetime.now(BRASILIA_TZ).date()


def _as_list(value: Any) -> list[dict]:
    """Normaliza o campo terminal objeto/lista usado pela API do Senado."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [value]
    raise SenadoAPIError(f"Esperava objeto ou lista, recebeu {type(value).__name__}")


def _at_path(data: Any, *keys: str) -> Any:
    """Obtém um caminho conhecido sem confundir listas de metadados."""
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


class SenadoClient:
    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        self.client: httpx.AsyncClient | None = None
        self.timeout = timeout

    async def _get_client(self) -> httpx.AsyncClient:
        if self.client is None or self.client.is_closed:
            self.client = httpx.AsyncClient(
                base_url=BASE_URL, timeout=httpx.Timeout(self.timeout), follow_redirects=True
            )
        return self.client

    async def close(self) -> None:
        if self.client and not self.client.is_closed:
            await self.client.aclose()

    async def _get(self, path: str, params: dict | None = None, retries: int = 3) -> Any:
        """
        Executa GET com retry logic e tratamento de erros.

        Args:
            path: Caminho do endpoint
            params: Parâmetros da query
            retries: Número de tentativas em caso de falha

        Raises:
            SenadoTimeoutError: Timeout na requisição
            SenadoNotFoundError: Recurso não encontrado (404)
            SenadoConnectionError: Erro de conexão
            SenadoAPIError: Outros erros da API
        """
        client = await self._get_client()
        last_error: SenadoAPIError | None = None

        for attempt in range(retries):
            try:
                logger.debug(f"Requisição para {path}, tentativa {attempt + 1}/{retries}")
                response = await client.get(path, params=params)
                response.raise_for_status()
                return response.json()

            except httpx.TimeoutException as e:
                last_error = SenadoTimeoutError(f"Timeout ao acessar {path}: {e}")
                logger.warning(f"Timeout na tentativa {attempt + 1}/{retries}")
                if attempt < retries - 1:
                    await asyncio.sleep(2**attempt)  # Backoff exponencial

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise SenadoNotFoundError(f"Recurso não encontrado: {path}") from e
                last_error = SenadoAPIError(f"Erro HTTP {e.response.status_code}: {e}")
                if e.response.status_code >= 500:
                    logger.warning(f"Erro {e.response.status_code} na tentativa {attempt + 1}/{retries}")
                    if attempt < retries - 1:
                        await asyncio.sleep(2**attempt)
                        continue
                logger.error(f"Erro HTTP: {e}")
                break

            except httpx.ConnectError as e:
                last_error = SenadoConnectionError(f"Erro de conexão: {e}")
                logger.warning(f"Erro de conexão na tentativa {attempt + 1}/{retries}")
                if attempt < retries - 1:
                    await asyncio.sleep(2**attempt)

            except Exception as e:
                last_error = SenadoAPIError(f"Erro inesperado: {e}")
                logger.error(f"Erro inesperado: {e}")
                break

        if last_error:
            raise last_error

        raise SenadoAPIError("Falha após todas as tentativas")

    async def _get_list(self, path: str, params: dict | None = None) -> list:
        """Executa GET e retorna lista, lidando com estrutura variável."""
        data = await self._get(path, params)

        candidates: list[list] = []

        def collect_lists(obj: Any) -> None:
            if isinstance(obj, list):
                candidates.append(obj)
            elif isinstance(obj, dict):
                for value in obj.values():
                    collect_lists(value)

        collect_lists(data)
        if not candidates:
            return []
        if len(candidates) > 1:
            raise SenadoAPIError(f"Resposta ambígua em {path}: informe um caminho de resultado explícito")
        return candidates[0]

    # ========== PLENÁRIO ==========

    async def get_agenda_plenario_dia(self, data: date | None = None) -> dict:
        """Agenda do plenário para um dia específico (YYYYMMDD)."""
        if data is None:
            data = _today_brasilia()
        data_str = data.strftime("%Y%m%d")
        return await self._get(f"/plenario/agenda/dia/{data_str}.json")

    async def get_agenda_plenario_mes(self, ano: int, mes: int) -> dict:
        """Agenda do plenário para um mês (YYYYMM)."""
        yyyymm = f"{ano}{mes:02d}"
        return await self._get(f"/plenario/agenda/mes/{yyyymm}.json")

    async def get_votacoes_periodo(self, data_inicio: date, data_fim: date) -> list[dict]:
        """Lista de votações em um período."""
        inicio = data_inicio.strftime("%Y%m%d")
        fim = data_fim.strftime("%Y%m%d")
        data = await self._get(f"/plenario/lista/votacao/{inicio}/{fim}.json")
        votacoes = data.get("ListaVotacoes", {}).get("Votacoes", {}).get("Votacao", [])
        return votacoes if isinstance(votacoes, list) else [votacoes] if votacoes else []

    # ========== COMISSÕES ==========

    async def get_agenda_comissao_dia(self, data: date | None = None) -> dict:
        """Agenda das comissões para um dia."""
        if data is None:
            data = date.today()
        data_str = data.strftime("%Y%m%d")
        return await self._get(f"/comissao/agenda/dia/{data_str}.json")

    async def get_agenda_comissao_periodo(self, data_inicio: date, data_fim: date) -> dict:
        """Agenda das comissões em um período."""
        inicio = data_inicio.strftime("%Y%m%d")
        fim = data_fim.strftime("%Y%m%d")
        return await self._get(f"/comissao/agenda/{inicio}/{fim}.json")

    async def get_lista_comissoes(self) -> list[dict]:
        """Lista de todas as comissões."""
        data = await self._get("/comissao/lista.json")
        comissoes = data.get("ListaComissoes", {}).get("Comissoes", {}).get("Comissao", [])
        return comissoes if isinstance(comissoes, list) else [comissoes] if comissoes else []

    # ========== SENADORES ==========

    async def lista_senadores_atuais(self) -> list[dict]:
        """Lista de senadores em exercício."""
        data = await self._get("/senador/lista/atual.json")
        return _as_list(_at_path(data, "ListaParlamentarEmExercicio", "Parlamentares", "Parlamentar"))

    async def lista_senadores_legislatura(self, legislatura: int, somente_exercicio: bool = True) -> list[dict]:
        """Lista a coorte de uma legislatura, incluindo quem exerceu o mandato."""
        params = {"exercicio": "S"} if somente_exercicio else None
        data = await self._get(f"/senador/lista/legislatura/{legislatura}/{legislatura}.json", params)
        return _as_list(_at_path(data, "ListaParlamentarLegislatura", "Parlamentares", "Parlamentar"))

    async def buscar_senador_por_nome(self, nome: str) -> list[dict]:
        """Busca senadores pelo nome (contém)."""
        todos = await self.lista_senadores_atuais()
        nome_lower = nome.lower()
        return [
            s for s in todos if nome_lower in s.get("IdentificacaoParlamentar", {}).get("NomeParlamentar", "").lower()
        ]

    async def get_senador_detalhe(self, codigo: str) -> dict | None:
        """Detalhe de um senador pelo código."""
        data = await self._get(f"/senador/{codigo}.json")
        return data.get("DetalheParlamentar", {}).get("Parlamentar")

    async def get_autorias_senador(self, codigo: str) -> list[dict]:
        """Lista de autorias de um senador."""
        data = await self._get(f"/senador/{codigo}/autorias.json")
        return _as_list(
            _at_path(
                data,
                "MateriasAutoriaParlamentar",
                "Parlamentar",
                "Autorias",
                "Autoria",
            )
        )

    async def get_discursos_senador(
        self, codigo: str, data_inicio: date | None = None, data_fim: date | None = None
    ) -> list[dict]:
        """Discursos de um senador em um período."""
        params = {}
        if data_inicio:
            params["dataInicio"] = data_inicio.strftime("%Y%m%d")
        if data_fim:
            params["dataFim"] = data_fim.strftime("%Y%m%d")
        data = await self._get(f"/senador/{codigo}/discursos.json", params)
        return _as_list(
            _at_path(
                data,
                "DiscursosParlamentar",
                "Parlamentar",
                "Pronunciamentos",
                "Pronunciamento",
            )
        )

    async def get_senador_filiacoes(self, codigo: str) -> list[dict]:
        """Filiações partidárias de um senador."""
        data = await self._get(f"/senador/{codigo}/filiacoes.json")
        filiacoes = data.get("FiliacaoParlamentar", {}).get("Parlamentar", {}).get("Filiacoes", {}).get("Filiacao", [])
        return filiacoes if isinstance(filiacoes, list) else [filiacoes] if filiacoes else []

    async def get_senador_cargos(self, codigo: str) -> list[dict]:
        """Cargos exercidos por um senador."""
        data = await self._get(f"/senador/{codigo}/cargos.json")
        cargos = data.get("CargoParlamentar", {}).get("Parlamentar", {}).get("Cargos", {}).get("Cargo", [])
        return cargos if isinstance(cargos, list) else [cargos] if cargos else []

    async def get_senador_liderancas(self, codigo: str) -> list[dict]:
        """Lideranças exercidas por um senador."""
        data = await self._get(f"/senador/{codigo}/liderancas.json")
        liderancas = (
            data.get("LiderancaParlamentar", {}).get("Parlamentar", {}).get("Liderancas", {}).get("Lideranca", [])
        )
        return liderancas if isinstance(liderancas, list) else [liderancas] if liderancas else []

    async def get_senador_apartes(self, codigo: str) -> list[dict]:
        """Apartes (intervenções) de um senador."""
        data = await self._get(f"/senador/{codigo}/apartes.json")
        apartes = data.get("ApartesParlamentar", {}).get("Parlamentar", {}).get("Apartes", {}).get("Aparte", [])
        return apartes if isinstance(apartes, list) else [apartes] if apartes else []

    async def get_senador_relatorias(self, codigo: str) -> list[dict]:
        """Relatorias de um senador."""
        data = await self._get(f"/senador/{codigo}/relatorias.json")
        return _as_list(
            _at_path(
                data,
                "MateriasRelatoriaParlamentar",
                "Parlamentar",
                "Relatorias",
                "Relatoria",
            )
        )

    async def get_senador_profissao(self, codigo: str) -> list[dict]:
        """Profissão de um senador."""
        return await self._get_list(f"/senador/{codigo}/profissao.json")

    async def get_senador_historico_academico(self, codigo: str) -> list[dict]:
        """Histórico acadêmico de um senador."""
        return await self._get_list(f"/senador/{codigo}/historicoAcademico.json")

    async def get_senador_licencas(self, codigo: str) -> list[dict]:
        """Licenças de um senador."""
        return await self._get_list(f"/senador/{codigo}/licencas.json")

    # ========== MATÉRIAS / PROPOSIÇÕES ==========

    async def pesquisar_materia(
        self, sigla: str | None = None, numero: str | None = None, ano: int | None = None, tramitando: bool = True
    ) -> list[dict]:
        """Pesquisa matérias por sigla, número e ano."""
        params: dict[str, Any] = {}
        if sigla:
            params["sigla"] = sigla
        if numero:
            params["numero"] = numero
        if ano:
            params["ano"] = str(ano)
        if tramitando:
            params["tramitando"] = "S"

        data = await self._get("/materia/pesquisa/lista.json", params)
        materias = data.get("PesquisaBasicaMateria", {}).get("Materias", {}).get("Materia", [])
        return materias if isinstance(materias, list) else [materias] if materias else []

    async def get_materia_detalhe(self, codigo: str) -> dict | None:
        """Detalhe de uma matéria pelo código."""
        data = await self._get(f"/materia/{codigo}.json")
        return data.get("DetalheMateria", {}).get("Materia")

    async def get_materia_movimentacoes(self, codigo: str) -> list[dict]:
        """Movimentações de uma matéria."""
        data = await self._get(f"/materia/movimentacoes/{codigo}.json")
        movimentacoes = data.get("MovimentacaoMateria", {}).get("Movimentacao", [])
        return movimentacoes if isinstance(movimentacoes, list) else [movimentacoes] if movimentacoes else []

    async def get_materia_tramitacao(self, codigo: str) -> list[dict]:
        """Tramitações de uma matéria."""
        data = await self._get(f"/materia/tramitacao/{codigo}.json")
        tramitacoes = data.get("TramitacaoMateria", {}).get("Tramitacao", [])
        return tramitacoes if isinstance(tramitacoes, list) else [tramitacoes] if tramitacoes else []

    # ========== NOVOS ENDPOINTS ==========

    async def get_senador_votacoes(self, codigo: str) -> list[dict]:
        """Histórico de votações de um senador."""
        data = await self._get(f"/senador/{codigo}/votacoes.json")
        return _as_list(_at_path(data, "VotacaoParlamentar", "Parlamentar", "Votacoes", "Votacao"))

    async def get_senador_comissoes(self, codigo: str) -> list[dict]:
        """Comissões de que um senador é membro."""
        data = await self._get(f"/senador/{codigo}/comissoes.json")
        return _as_list(
            _at_path(
                data,
                "MembroComissaoParlamentar",
                "Parlamentar",
                "MembroComissoes",
                "Comissao",
            )
        )

    async def get_senador_mandatos(self, codigo: str) -> list[dict]:
        """Mandatos de um senador."""
        data = await self._get(f"/senador/{codigo}/mandatos.json")
        return _as_list(_at_path(data, "MandatoParlamentar", "Parlamentar", "Mandatos", "Mandato"))

    async def get_materia_por_sigla(self, sigla: str, numero: str, ano: int) -> dict | None:
        """Busca matéria pela sigla completa (ex: PL 1234/2026)."""
        resultados = await self.pesquisar_materia(sigla=sigla, numero=numero, ano=ano, tramitando=False)
        return resultados[0] if resultados else None

    async def pesquisar_materia_por_assunto(self, assunto: str, tramitando: bool = True) -> list[dict]:
        """Pesquisa matérias por assunto/keyword."""
        params: dict[str, Any] = {"assunto": assunto}
        if tramitando:
            params["tramitando"] = "S"
        data = await self._get("/materia/pesquisa/lista.json", params)
        materias = data.get("PesquisaBasicaMateria", {}).get("Materias", {}).get("Materia", [])
        return materias if isinstance(materias, list) else [materias] if materias else []

    async def get_materia_situacao_atual(self, codigo: str) -> dict:
        """Situação atual de uma matéria."""
        return await self._get(f"/materia/situacaoatual/{codigo}.json")

    async def get_materia_textos(self, codigo: str) -> list[dict]:
        """Textos de uma matéria."""
        return await self._get_list(f"/materia/textos/{codigo}.json")

    async def get_materia_emendas(self, codigo: str) -> list[dict]:
        """Emendas de uma matéria."""
        return await self._get_list(f"/materia/emendas/{codigo}.json")

    async def get_materia_relatorias(self, codigo: str) -> list[dict]:
        """Relatorias de uma matéria."""
        return await self._get_list(f"/materia/relatorias/{codigo}.json")

    async def get_materia_autoria(self, codigo: str) -> list[dict]:
        """Autoria de uma matéria."""
        return await self._get_list(f"/materia/autoria/{codigo}.json")

    async def get_materias_tramitando(self) -> list[dict]:
        """Matérias atualmente em tramitação."""
        return await self._get_list("/materia/tramitando.json")

    async def get_materias_atualizadas(self, dias: int = 7) -> list[dict]:
        """Matérias atualizadas nos últimos N dias."""
        return await self._get_list("/materia/atualizadas.json", {"numdias": dias})

    # ========== PLENÁRIO (RESULTADOS E VOTAÇÕES) ==========

    async def get_resultado_plenario_dia(self, data: date) -> dict:
        """Resultado do plenário em um dia."""
        data_str = data.strftime("%Y%m%d")
        return await self._get(f"/plenario/resultado/{data_str}.json")

    async def get_resultado_plenario_mes(self, ano: int, mes: int) -> dict:
        """Resultado do plenário em um mês."""
        return await self._get(f"/plenario/resultado/mes/{ano}{mes:02d}.json")

    async def get_votacoes_nominais_ano(self, ano: int) -> list[dict]:
        """Todas as votações nominais de um ano."""
        return await self._get_list(f"/plenario/votacao/nominal/{ano}.json")

    async def get_discursos_plenario(self, data_inicio: date, data_fim: date) -> list[dict]:
        """Discursos em plenário em um período."""
        inicio = data_inicio.strftime("%Y%m%d")
        fim = data_fim.strftime("%Y%m%d")
        return await self._get_list(f"/plenario/lista/discursos/{inicio}/{fim}.json")

    async def get_encontro_plenario(self, codigo: str) -> dict:
        """Detalhes de uma sessão/encontro plenário."""
        return await self._get(f"/plenario/encontro/{codigo}.json")

    async def get_encontro_pauta(self, codigo: str) -> list[dict]:
        """Pauta de uma sessão/encontro plenário."""
        return await self._get_list(f"/plenario/encontro/{codigo}/pauta.json")

    # ========== COMISSÕES (DETALHE) ==========

    async def get_comissao_detalhe(self, codigo: str) -> dict:
        """Detalhes de uma comissão."""
        return await self._get(f"/comissao/{codigo}.json")

    async def get_comissao_reuniao(self, codigo_reuniao: str) -> dict:
        """Detalhes de uma reunião de comissão."""
        return await self._get(f"/comissao/reuniao/{codigo_reuniao}.json")

    async def get_composicao_comissao(self, codigo: str) -> list[dict]:
        """Composição (membros) de uma comissão."""
        return await self._get_list(f"/composicao/comissao/{codigo}.json")

    async def get_lista_comissoes_mistas(self) -> list[dict]:
        """Lista de comissões mistas (CN)."""
        return await self._get_list("/comissao/lista/mistas.json")

    # ========== VOTAÇÃO EM COMISSÕES ==========

    async def get_votacao_comissao(self, sigla_comissao: str) -> list[dict]:
        """Votações em uma comissão."""
        return await self._get_list(f"/votacaoComissao/comissao/{sigla_comissao}.json")

    async def get_votacao_comissao_materia(self, sigla: str, numero: str, ano: int) -> list[dict]:
        """Votações em comissão sobre uma matéria."""
        return await self._get_list(f"/votacaoComissao/materia/{sigla}/{numero}/{ano}.json")

    async def get_votacao_comissao_parlamentar(self, codigo: str) -> list[dict]:
        """Votações de um parlamentar em comissões."""
        return await self._get_list(f"/votacaoComissao/parlamentar/{codigo}.json")

    # ========== COMPOSIÇÃO E LIDERANÇAS ==========

    async def get_mesa_senado(self) -> dict:
        """Mesa diretora do Senado."""
        return await self._get("/composicao/mesaSF.json")

    async def get_mesa_congresso(self) -> dict:
        """Mesa do Congresso Nacional."""
        return await self._get("/composicao/mesaCN.json")

    async def get_liderancas(self) -> dict:
        """Lideranças partidárias."""
        return await self._get("/composicao/lideranca.json")

    async def get_blocos_parlamentares(self) -> list[dict]:
        """Blocos parlamentares."""
        return await self._get_list("/composicao/lista/blocos.json")

    # ========== VETOS ==========

    async def get_vetos_ano(self, ano: int) -> list[dict]:
        """Vetos presidenciais de um ano."""
        return await self._get_list(f"/materia/vetos/{ano}.json")

    async def get_vetos_apos_rcn(self) -> list[dict]:
        """Vetos posteriores à RCN 1/2013 em tramitação."""
        return await self._get_list("/materia/vetos/aposrcn.json")

    async def get_vetos_antes_rcn(self) -> list[dict]:
        """Vetos anteriores à RCN 1/2013 em tramitação."""
        return await self._get_list("/materia/vetos/antesrcn.json")

    async def get_vetos_encerrados(self) -> list[dict]:
        """Vetos com tramitação encerrada."""
        return await self._get_list("/materia/vetos/encerrados.json")

    # ========== ORIENTAÇÃO DE BANCADA ==========

    async def get_orientacao_bancada_data(self, data: date) -> dict:
        """Orientação de bancada para votações em uma data específica (YYYYMMDD)."""
        data_str = data.strftime("%Y%m%d")
        return await self._get(f"/plenario/votacao/orientacaoBancada/{data_str}.json")

    async def get_orientacao_bancada_periodo(self, data_inicio: date, data_fim: date) -> dict:
        """Orientação de bancada para votações em um período."""
        inicio = data_inicio.strftime("%Y%m%d")
        fim = data_fim.strftime("%Y%m%d")
        return await self._get(f"/plenario/votacao/orientacaoBancada/{inicio}/{fim}.json")

    # ========== RESULTADO PLENÁRIO CN E VETOS ==========

    async def get_resultado_plenario_cn(self, data: date) -> dict:
        """Resultado da sessão plenária do Congresso Nacional em uma data."""
        data_str = data.strftime("%Y%m%d")
        return await self._get(f"/plenario/resultado/cn/{data_str}.json")

    async def get_resultado_veto(self, codigo: str) -> dict:
        """Resultado da votação nominal de um veto."""
        return await self._get(f"/plenario/resultado/veto/{codigo}.json")

    async def get_resultado_veto_materia(self, codigo: str) -> dict:
        """Resultado da votação nominal do veto a um projeto de lei."""
        return await self._get(f"/plenario/resultado/veto/materia/{codigo}.json")

    # ========== ORÇAMENTO (EMENDAS PARLAMENTARES) ==========

    async def get_orcamento_lotes_emendas(self) -> list[dict]:
        """Lotes de emendas ao orçamento."""
        return await self._get_list("/orcamento/lista.json")

    async def get_orcamento_oficios(self) -> list[dict]:
        """Lista de ofícios de apoio às emendas de orçamento."""
        return await self._get_list("/orcamento/oficios.json")

    async def get_orcamento_oficio(self, numero_sedol: str) -> dict:
        """Detalhes de um ofício de apoio a emenda orçamentária."""
        return await self._get(f"/orcamento/oficios/{numero_sedol}.json")

    # ========== CPI ==========

    async def get_cpi_requerimentos(self, comissao: str, pagina: int = 1, tamanho: int = 20) -> list[dict]:
        """Lista de requerimentos de uma CPI."""
        params = {"pagina": pagina, "tamanho": tamanho}
        return await self._get_list(f"/comissao/cpi/{comissao}/requerimentos.json", params)

    # ========== COMPOSIÇÃO COMISSÃO MISTA ==========

    async def get_composicao_comissao_mista_atual(self, codigo: str) -> dict:
        """Composição atual de uma comissão mista."""
        return await self._get(f"/composicao/comissao/atual/mista/{codigo}.json")

    # ========== DISTRIBUIÇÃO DE AUTORIA/RELATORIA ==========

    async def get_distribuicao_autoria_comissao(
        self, sigla_comissao: str | None = None, cod_parlamentar: str | None = None
    ) -> list[dict]:
        """Distribuição de autoria de matérias por comissão e/ou parlamentar."""
        params: dict[str, Any] = {}
        if sigla_comissao:
            params["siglaComissao"] = sigla_comissao
        if cod_parlamentar:
            params["codParlamentar"] = cod_parlamentar
        return await self._get_list("/materia/distribuicao/autoria.json", params)

    async def get_distribuicao_relatoria_comissao(self, sigla: str) -> list[dict]:
        """Distribuição de relatoria de matérias em uma comissão."""
        return await self._get_list(f"/materia/distribuicao/relatoria/{sigla}.json")

    # ========== TRAMITAÇÃO CONSOLIDADA ==========

    async def get_materia_lista_tramitacao(self, sigla: str | None = None, comissao: str | None = None) -> dict:
        """Total de processos em tramitação por tipo ou colegiado."""
        params: dict[str, Any] = {}
        if sigla:
            params["sigla"] = sigla
        if comissao:
            params["comissao"] = comissao
        return await self._get("/materia/lista/tramitacao.json", params)

    # ========== PROCESSO ==========

    async def get_processo(self, codigo: str) -> dict:
        """Processo legislativo completo de uma matéria.
        Retorna autuações, situações, tramitação em estrutura rica.
        Endpoint preferido sobre /materia/{codigo} para status detalhado.
        """
        data = await self._get(f"/processo/{codigo}.json")
        if not isinstance(data, dict):
            raise SenadoAPIError(f"Resposta de processo inválida para {codigo}")
        return data

    async def pesquisar_processos(
        self,
        sigla: str | None = None,
        numero: str | None = None,
        ano: int | None = None,
        tramitando: bool | None = True,
        autor: str | None = None,
        assunto: str | None = None,
        data_inicio_apresentacao: str | None = None,
        data_fim_apresentacao: str | None = None,
    ) -> list[dict]:
        """Pesquisa avançada de processos legislativos (API /processo).

        Nota: este endpoint retorna JSON sem sufixo .json e aceita mais filtros
        do que /materia/pesquisa/lista.

        Parâmetros de data no formato YYYYMMDD.
        """
        params: dict[str, Any] = {}
        if sigla:
            params["sigla"] = sigla
        if numero:
            params["numero"] = numero
        if ano:
            params["ano"] = str(ano)
        if tramitando is not None:
            params["tramitando"] = "S" if tramitando else "N"
        if autor:
            params["autor"] = autor
        if assunto:
            params["termo"] = assunto
        if data_inicio_apresentacao:
            params["dataInicioApresentacao"] = data_inicio_apresentacao
        if data_fim_apresentacao:
            params["dataFimApresentacao"] = data_fim_apresentacao

        data = await self._get("/processo", params)
        if not isinstance(data, list):
            raise SenadoAPIError("A pesquisa /processo não retornou uma lista")
        return data

    # ========== AUTORES, LEGISLAÇÃO, DISCURSO ==========

    async def get_autores_atuais(self) -> list[dict]:
        """Lista de autores (senadores atuais como autores)."""
        return await self._get_list("/autor/lista/atual.json")

    async def pesquisar_legislacao(
        self, tipo: str | None = None, ano: int | None = None, numero: str | None = None
    ) -> list[dict]:
        """Pesquisa legislação/normas."""
        params: dict[str, Any] = {}
        if tipo:
            params["tipo"] = tipo
        if ano:
            params["ano"] = str(ano)
        if numero:
            params["numero"] = numero
        return await self._get_list("/legislacao/lista.json", params)

    async def get_discurso_texto_integral(self, codigo_pronunciamento: str) -> dict:
        """Texto integral de um discurso/pronunciamento."""
        return await self._get(f"/discurso/texto-integral/{codigo_pronunciamento}.json")

    # ========== UTILITÁRIOS ==========

    async def get_materias_recentes(self, dias: int = 7) -> list[dict]:
        """Busca matérias apresentadas nos últimos N dias."""
        hoje = _today_brasilia()
        inicio = hoje - timedelta(days=dias)
        data_str = inicio.strftime("%Y%m%d")

        data = await self._get(
            "/materia/pesquisa/lista.json", {"dataApresentacaoIni": data_str, "tramitando": "S", "itens": 50}
        )
        materias = data.get("PesquisaBasicaMateria", {}).get("Materias", {}).get("Materia", [])
        return materias if isinstance(materias, list) else [materias] if materias else []

    async def get_votacoes_semana(self) -> list[dict]:
        """Votações da última semana."""
        hoje = _today_brasilia()
        return await self.get_votacoes_periodo(hoje - timedelta(days=7), hoje)

    async def get_agenda_semana(self) -> list:
        """Agenda do plenário para a semana atual."""
        hoje = _today_brasilia()
        dia_semana = hoje.weekday()
        inicio = hoje - timedelta(days=dia_semana)
        fim = inicio + timedelta(days=6)

        # Baixa mês a mês
        meses: dict[str, dict] = {}
        cursor = date(inicio.year, inicio.month, 1)
        fim_mes = date(fim.year, fim.month, 1)

        all_events = []
        while cursor <= fim_mes:
            key = f"{cursor.year}{cursor.month:02d}"
            meses[key] = await self.get_agenda_plenario_mes(cursor.year, cursor.month)

            # Extrai eventos do mês
            mes_data = meses[key]

            def extract_events(obj: Any) -> list:
                if isinstance(obj, list):
                    return obj
                if isinstance(obj, dict):
                    for v in obj.values():
                        result = extract_events(v)
                        if result:
                            return result
                return []

            all_events.extend(extract_events(mes_data))
            cursor = date(cursor.year, cursor.month + 1, 1) if cursor.month < 12 else date(cursor.year + 1, 1, 1)

        return all_events


# ===========================================================================
# API ADM (adm.senado.gov.br/adm-dadosabertos) — Prestação de Contas
# ===========================================================================

ADM_BASE_URL = "https://adm.senado.gov.br/adm-dadosabertos"


class SenadoAdmClient:
    """Cliente para a API Administrativa do Senado Federal.

    Base URL: https://adm.senado.gov.br/adm-dadosabertos
    Sem autenticao. Swagger: /adm-dadosabertos/swagger-ui/index.html
    """

    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        self.client: httpx.AsyncClient | None = None
        self.timeout = timeout

    async def _get_client(self) -> httpx.AsyncClient:
        if self.client is None or self.client.is_closed:
            self.client = httpx.AsyncClient(
                base_url=ADM_BASE_URL, timeout=httpx.Timeout(self.timeout), follow_redirects=True
            )
        return self.client

    async def close(self) -> None:
        if self.client and not self.client.is_closed:
            await self.client.aclose()

    async def _get(self, path: str, params: dict | None = None, retries: int = 3) -> Any:
        """GET com retry limitado para a API administrativa."""
        client = await self._get_client()
        last_error: SenadoAPIError | None = None

        for attempt in range(retries):
            try:
                response = await client.get(path, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.TimeoutException as exc:
                last_error = SenadoTimeoutError(f"Timeout ao acessar {path}: {exc}")
            except httpx.ConnectError as exc:
                last_error = SenadoConnectionError(f"Erro de conexão em {path}: {exc}")
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    raise SenadoNotFoundError(f"Recurso não encontrado: {path}") from exc
                last_error = SenadoAPIError(f"Erro HTTP {exc.response.status_code} ao acessar {path}")
                if exc.response.status_code < 500 and exc.response.status_code != 429:
                    raise last_error from exc
            except ValueError as exc:
                raise SenadoAPIError(f"JSON inválido em {path}: {exc}") from exc

            if attempt < retries - 1:
                await asyncio.sleep(2**attempt)

        if last_error:
            raise last_error
        raise SenadoAPIError(f"Falha após {retries} tentativas em {path}")

    async def _get_records(self, path: str, params: dict | None = None) -> list[dict]:
        """Aceita lista bruta ou envelope ``data`` e rejeita formas ambíguas."""
        payload = await self._get(path, params)
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict) and isinstance(payload.get("data"), list):
            return payload["data"]
        raise SenadoAPIError(f"Resposta administrativa inválida em {path}")

    # ========== SENADORES ==========

    async def get_ceap(self, ano: int) -> list[dict]:
        """Despesas da CEAP (Cota para Exercício da Atividade Parlamentar) por ano.

        Retorna todas as despesas de todos os senadores no ano informado.
        Campos: id, tipoDocumento, ano, mes, codSenador, nomeSenador,
                tipoDespesa, cpfCnpj, fornecedor, valorReembolsado.
        """
        return await self._get_records(f"/api/v1/senadores/despesas_ceaps/{ano}")

    async def get_ceap_senador(self, nome_senador: str, ano: int) -> list[dict]:
        """Despesas CEAP filtradas por nome de senador (busca case-insensitive)."""
        todas = await self.get_ceap(ano)
        nome_lower = nome_senador.lower()
        return [d for d in todas if nome_lower in d.get("nomeSenador", "").lower()]

    async def get_auxilio_moradia(
        self, nome: str | None = None, estado: str | None = None, partido: str | None = None
    ) -> list[dict]:
        """Auxílio moradia e imóvel funcional por senador."""
        params: dict[str, Any] = {}
        if nome:
            params["nomeParlamentarContains"] = nome
        if estado:
            params["estadoEleitoEquals"] = estado
        if partido:
            params["partidoEleitoEquals"] = partido
        return await self._get_records("/api/v1/senadores/auxilio-moradia", params)

    async def get_escritorios_apoio(self) -> list[dict]:
        """Escritórios de apoio dos senadores (endereço, telefone)."""
        return await self._get_records("/api/v1/senadores/escritorios")

    async def get_senadores_aposentados(self) -> list[dict]:
        """Senadores aposentados e suas remunerações."""
        return await self._get_records("/api/v1/senadores/aposentados")

    # ========== SERVIDORES ==========

    async def get_remuneracao_servidores(self, ano: int, mes: int) -> list[dict]:
        """Remuneração de servidores por mês/ano.

        Campos: sequencial, nome, mes, ano, remuneracao_basica,
                vantagens_pessoais, funcao_comissionada, gratificacoes,
                diarias, auxilios, faltas, previdencia, tipo_folha.
        """
        return await self._get_records(f"/api/v1/servidores/remuneracoes/{ano}/{mes:02d}")

    async def get_servidores(
        self, tipo_vinculo: str | None = None, situacao: str | None = None, lotacao: str | None = None
    ) -> list[dict]:
        """Lista de servidores com filtros opcionais."""
        params: dict[str, Any] = {}
        if tipo_vinculo:
            params["tipoVinculoEquals"] = tipo_vinculo
        if situacao:
            params["situacaoEquals"] = situacao
        if lotacao:
            params["lotacaoEquals"] = lotacao
        return await self._get_records("/api/v1/servidores/servidores", params)

    async def get_servidores_ativos(self) -> list[dict]:
        """Lista de servidores ativos."""
        return await self._get_records("/api/v1/servidores/servidores/ativos")

    async def get_servidores_comissionados(self) -> list[dict]:
        """Servidores comissionados."""
        return await self._get_records("/api/v1/servidores/servidores/comissionados")

    async def get_horas_extras(self, ano: int, mes: int) -> list[dict]:
        """Horas extras de servidores por mês/ano."""
        return await self._get_records(f"/api/v1/servidores/horas-extras/{ano}/{mes:02d}")

    async def get_estagiarios(self) -> list[dict]:
        """Estagiários do Senado."""
        return await self._get_records("/api/v1/servidores/estagiarios")

    async def get_pensionistas(self) -> list[dict]:
        """Pensionistas do Senado."""
        return await self._get_records("/api/v1/servidores/pensionistas")

    async def get_remuneracao_pensionistas(self, ano: int, mes: int) -> list[dict]:
        """Remuneração de pensionistas por mês/ano."""
        return await self._get_records(f"/api/v1/servidores/pensionistas/remuneracoes/{ano}/{mes:02d}")

    # ========== SUPRIDOS (CARTÃO CORPORATIVO) ==========

    async def get_supridos(self, ano: int) -> list[dict]:
        """Lista de servidores supridos (cartão corporativo) no ano."""
        return await self._get_records(f"/api/v1/supridos/{ano}")

    async def get_supridos_transacoes(self, ano: int) -> list[dict]:
        """Transações do cartão corporativo no ano."""
        return await self._get_records(f"/api/v1/supridos/transacoes/{ano}")

    async def get_supridos_movimentacoes(self, ano: int) -> list[dict]:
        """Movimentações do cartão corporativo no ano."""
        return await self._get_records(f"/api/v1/supridos/movimentacoes/{ano}")

    async def get_supridos_empenhos(self, ano: int) -> list[dict]:
        """Empenhos do cartão corporativo no ano."""
        return await self._get_records(f"/api/v1/supridos/empenhos/{ano}")

    # ========== CONTRATAÇÕES ==========

    async def get_contratos(
        self, fornecedor: str | None = None, cnpj: str | None = None, ano: int | None = None, objeto: str | None = None
    ) -> list[dict]:
        """Contratos do Senado Federal."""
        params: dict[str, Any] = {}
        if fornecedor:
            params["nomeFornecedorContains"] = fornecedor
        if cnpj:
            params["cnpjCpfEquals"] = cnpj
        if ano:
            params["anoEquals"] = ano
        if objeto:
            params["objetoDescricaoContains"] = objeto
        return await self._get_records("/api/v1/contratacoes/contratos", params)

    async def get_licitacoes(self, numero: str | None = None, objeto: str | None = None) -> list[dict]:
        """Licitações do Senado."""
        params: dict[str, Any] = {}
        if numero:
            params["numeroEquals"] = numero
        if objeto:
            params["objetoContains"] = objeto
        return await self._get_records("/api/v1/contratacoes/licitacoes", params)

    async def get_notas_empenho(self, fornecedor: str | None = None, ano: int | None = None) -> list[dict]:
        """Notas de empenho."""
        params: dict[str, Any] = {}
        if fornecedor:
            params["nomeFornecedorContains"] = fornecedor
        if ano:
            params["anoEquals"] = ano
        return await self._get_records("/api/v1/contratacoes/notas_empenho", params)

    async def get_empresas_fornecedoras(self, nome: str | None = None, cnpj: str | None = None) -> list[dict]:
        """Empresas fornecedoras cadastradas."""
        params: dict[str, Any] = {}
        if nome:
            params["nomeContains"] = nome
        if cnpj:
            params["cnpjCpfEquals"] = cnpj
        return await self._get_records("/api/v1/contratacoes/empresas", params)

    async def get_terceirizados(self) -> list[dict]:
        """Terceirizados alocados no Senado."""
        return await self._get_records("/api/v1/contratacoes/terceirizados")


# Instância global do cliente ADM
_adm_client: SenadoAdmClient | None = None

# Instância global do cliente legislativo
_client: SenadoClient | None = None


def get_senado_adm_client() -> SenadoAdmClient:
    """Retorna instância singleton do cliente ADM."""
    global _adm_client
    if _adm_client is None:
        _adm_client = SenadoAdmClient()
    return _adm_client


async def close_senado_adm_client() -> None:
    """Fecha e remove a instância global do cliente ADM."""
    global _adm_client
    if _adm_client:
        await _adm_client.close()
        _adm_client = None


def get_senado_client() -> SenadoClient:
    """Retorna instância singleton do cliente."""
    global _client
    if _client is None:
        _client = SenadoClient()
    return _client


async def close_senado_client() -> None:
    """Fecha o cliente global."""
    global _client
    if _client:
        await _client.close()
        _client = None


# ========== FACADE FUNCTIONS (uso direto) ==========


async def lista_senadores_atuais() -> list[dict]:
    """Facade: lista de senadores atuais."""
    client = get_senado_client()
    return await client.lista_senadores_atuais()


async def buscar_senador(nome: str) -> list[dict]:
    """Facade: busca senador por nome."""
    client = get_senado_client()
    return await client.buscar_senador_por_nome(nome)


async def pesquisar_materia(sigla: str | None = None, numero: str | None = None, ano: int | None = None) -> list[dict]:
    """Facade: pesquisa matéria."""
    client = get_senado_client()
    return await client.pesquisar_materia(sigla, numero, ano)


async def get_votacoes_semana() -> list[dict]:
    """Facade: votações da semana."""
    client = get_senado_client()
    return await client.get_votacoes_semana()


async def get_materias_recentes(dias: int = 7) -> list[dict]:
    """Facade: matérias recentes."""
    client = get_senado_client()
    return await client.get_materias_recentes(dias)
