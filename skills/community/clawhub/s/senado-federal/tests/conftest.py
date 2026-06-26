"""Configuração do pytest para testes do senado_client."""
import pytest


@pytest.fixture
def mock_senado_response():
    """Mock de resposta típica da API do Senado."""
    return {
        "ListaParlamentarEmExercicio": {
            "Parlamentares": {
                "Parlamentar": [
                    {
                        "IdentificacaoParlamentar": {
                            "CodigoParlamentar": "5012",
                            "NomeParlamentar": "Renan Calheiros",
                            "SiglaPartidoParlamentar": "MDB",
                            "UfParlamentar": "AL"
                        }
                    }
                ]
            }
        }
    }


@pytest.fixture
def mock_materia_response():
    """Mock de resposta de pesquisa de matérias."""
    return {
        "PesquisaBasicaMateria": {
            "Materias": {
                "Materia": [
                    {
                        "CodigoMateria": "123456",
                        "SiglaSubtipoMateria": "PL",
                        "NumeroMateria": "1234",
                        "AnoMateria": "2026",
                        "EmentaMateria": "Dispõe sobre..."
                    }
                ]
            }
        }
    }
