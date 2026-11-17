# Senate response shapes, identifiers, and dates

The legislative API uses endpoint-specific nested roots and may encode one item as an object and many items as a list.

## Safe normalization

Normalize only the expected terminal field:

```python
def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]
```

Verified senator paths include:

| Resource | Terminal path |
|---|---|
| speeches | `DiscursosParlamentar.Parlamentar.Pronunciamentos.Pronunciamento` |
| authorships | `MateriasAutoriaParlamentar.Parlamentar.Autorias.Autoria` |
| rapporteurships | `MateriasRelatoriaParlamentar.Parlamentar.Relatorias.Relatoria` |
| votes | `VotacaoParlamentar.Parlamentar.Votacoes.Votacao` |
| committees | `MembroComissaoParlamentar.Parlamentar.MembroComissoes.Comissao` |
| mandates | `MandatoParlamentar.Parlamentar.Mandatos.Mandato` |

Do not recursively return the first list in the document. Metadata or unrelated nested collections may appear before the desired business field.

## Current and historical cohorts

- Current officeholders: `/senador/lista/atual.json`.
- Cohort for a legislature: `/senador/lista/legislatura/{leg}/{leg}.json?exercicio=S`. The single-legislature route has returned only one `Parlamentar`, so do not use it as a complete cohort.
- Historical list responses can encode `Mandatos.Mandato` as a list while a current response can encode it as one object. Normalize at that field.
- Do not hardcode which legislature is current in reusable code.

## Process identifiers

`IdentificacaoProcesso` identifies the consolidated legislative process. `CodigoMateria` identifies a Senate matter. A process can include autuações from more than one house. Keep these values in separate variables and storage fields.

## Dates and timezone

- Most path dates use `YYYYMMDD`.
- Senator speech filters are documented as `dataInicio` and `dataFim` in `YYYYMMDD`.
- Query speeches and apartes one calendar year at a time; merge results after normalization.
- Interpret relative dates in `America/Sao_Paulo`.

## Failures versus empty results

Retry timeouts, connection failures, HTTP 429, and 5xx with bounded exponential backoff. Raise after the configured attempt limit. Only a successfully parsed expected field that is absent or null should become an empty list.
