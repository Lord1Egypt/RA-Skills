# Tracking a process across the Senate and Chamber

A Senate process may include multiple autuações and house-specific identifiers. Keep `IdentificacaoProcesso`, Senate `CodigoMateria`, and Chamber proposition ID distinct.

## Senate to Chamber

1. Query `/processo/{IdentificacaoProcesso}.json`.
2. Inspect autuações and house identifiers for a Chamber designation.
3. Query the Chamber `/proposicoes` collection using `siglaTipo`, `numero`, and `ano`.
4. Retrieve Chamber detail and movements using its returned numeric ID.

## Chamber to Senate

1. Resolve the Chamber record and review its movements for transfer.
2. Search the Senate `/processo` collection by the corresponding designation or other authoritative identifier.
3. Confirm the relationship from process autuações rather than title similarity.

For an auditable answer, expose each official identifier and link each house's record separately.
