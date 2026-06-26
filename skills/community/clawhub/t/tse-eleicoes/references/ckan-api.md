# CKAN Dados Abertos TSE — Referência

Base URL: `https://dadosabertos.tse.jus.br/api/3/action`

Sem autenticação. API CKAN padrão.

## Endpoints

```
GET /package_list
→ Lista todos os slugs/IDs de datasets disponíveis

GET /package_search?q={termo}&rows=20
→ Busca datasets por palavra-chave

GET /package_show?id={slug}
→ Metadados completos + URLs dos arquivos de um dataset
```

## Exemplo de Resposta — package_show

```json
{
  "success": true,
  "result": {
    "id": "candidatos-2024",
    "title": "Candidatos 2024",
    "resources": [
      {
        "id": "abc123",
        "name": "candidatos_2024_SP.zip",
        "url": "https://cdn.tse.jus.br/candidatos_2024_SP.zip",
        "format": "ZIP"
      }
    ]
  }
}
```

## Datasets Relevantes (exemplos)

- `candidatos-2024` — Candidatos das Eleições 2024
- `resultados-2022` — Resultados Eleição 2022
- `eleitorado-2024` — Perfil do Eleitorado 2024
- `prestacao-de-contas-eleitorais-candidatos-2024` — Contas de campanha 2024

## Links Úteis

- Portal: https://dadosabertos.tse.jus.br/
- CKAN Docs: https://docs.ckan.org/en/2.10/api/
