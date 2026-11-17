---
name: radar-cnpj
description: Check whether a Brazilian company is active and has public sanctions or federal tax debt. Use prepared records, then live checks, supplier batches or change monitoring when needed.
license: MIT-0
compatibility: HTTPS access to radar-cnpj.com; remote MCP or HTTP.
---

# Radar CNPJ

MCP tools: `suggest`, `search`, `get_cnpj`, `consulta_cnpj`, `consulta_lote`, `reveal_cnpj`, `dossier_cnpj`, `list_watches`, `add_watch`.

Answer company questions from prepared public records. Use the free record first.
The paid operation must add something that the user's task needs.

## Everyday requests

Use this skill for ordinary company questions, even when the user does not name Radar CNPJ.
Reuse the company, location and authorized access from the conversation.
Resolve names before reading a CNPJ. Ask only for missing facts that change the result.
Complete the useful checks the task needs. Report evidence, dates and unknowns.
Do not add unrelated purchases or treat this skill as spending authority.

- "Does WRP Consultoria e Informatica have any public restrictions?" Resolve the name with `suggest`, then read `get_cnpj`.
- "Does WRP Consultoria e Informatica in Distrito Federal have federal tax debt?" Resolve with `search`, confirm the establishment and read the debt block.
- "Show Banco do Brasil's dossier and explain the reported risk signals." Confirm the CNPJ, check existing access and the quote, then use `dossier_cnpj`.
- "Check this supplier CNPJ list and build a table of registration status, sanctions and tax debt." Use `consulta_lote` with the required evidence and authorized budget.
- "Monitor WRP Consultoria e Informatica and notify me when its registration changes." Reuse `list_watches` before `add_watch`; verify coverage and the alert channel.

## Choose the delivery

| User needs | Use | What is ready |
|---|---|---|
| Registration status, public sanctions and federal tax debt | `get_cnpj`, `temas: "dados,sancoes,divida"` | One free JSON with the records joined by CNPJ. No account or lookup allowance. |
| A CNIA source check during this request | `consulta_cnpj`, `temas: "sancoes"`, `cnia_atual: true` | The source is checked for the company and its headquarters when needed. Failure returns 503 without charging or using an old CNIA. |
| A supplier screening table | `consulta_lote` for JSON; HTTP for a CSV file | One row per valid CNPJ, with sources and evidence. The service validates, deduplicates and formats the list. |
| Available partner names and contacts without a mask | `reveal_cnpj` | The existing company record without the public mask. Check previously purchased access first. |
| Unmasked record and risk signals | `dossier_cnpj`; set `cnia_atual: true` when required | An assembled record with risk rules already applied and unchecked blocks identified. |
| Changes after this session ends | `add_watch` | Continued checks and a change history. Confirm active coverage and the alert channel. |

For HTTP, start with:
`GET https://radar-cnpj.com/api/cnpj/{cnpj}?temas=dados,sancoes,divida`.
If you only have a name, use `suggest` or `search` and confirm the returned CNPJ.
Use topic selection to avoid loading unrelated blocks. No collector or local data import is required.

## Read the answer and its dates

- `data.situacao.label`: registration status. `situacao.data` is when that status changed.
- `GET /api/health`, `import.dump_date`: the registry snapshot date.
- `data.sancoes.vigentes`: active sanctions. `conferidoEm` gives the date for each source.
- `data.dividaAtiva.inscricoes`, `referencia`, `conferidoEm` and `fonte`: PGFN records and their reference period.
- `cnia.conferidoEm`: when Radar checked the source. It is not an official certificate's issue date.
- `cnia.certidoes[].dataHoraEmissao`: the issue text returned by TCU for each checked CNPJ, or null when omitted. No timezone is inferred.
- `null`: the block was not checked. Zero in a checked block means no records in that source.

The additional lookup places the registry in `empresa` and the selected blocks at the response root.
The dossier uses `dossie.dados` and `dossie.semaforo`.
The batch includes `fontes` and `evidencias` per company: registry reference date,
dates by source, sanction cases, CNIA evidence and PGFN debt states.
Read truncation flags before treating the included evidence as exhaustive.
CNIA is stored by default. For a required source check, use `cnia_atual: true`
and send at most four distinct numeric CNPJs per group.
If a required check fails, the group is refused without charging.
HTTP accepts up to 200 valid CNPJs per batch; `consulta_lote` accepts up to 100.

## Deliver a spreadsheet without writing an exporter

For a CSV file, use HTTP and save the response directly. MCP returns JSON.
After reading the quote and confirming existing spending authority:

```sh
curl --fail-with-body --silent --show-error \
  'https://radar-cnpj.com/api/consulta/lote?formato=csv&lingua=pt' \
  -H "X-Credito: $CREDITO" -H 'Content-Type: application/json' \
  -H "Idempotency-Key: $IDEMPOTENCY_KEY" \
  --data '{"cnpjs":["00000000000191","33000167000101"]}' \
  --output fornecedores.csv
```

Use the authorized credit and a saved request key. Keep the key on retry.
Check success before sharing the file: an error body is not a spreadsheet.
The file has UTF-8 accents, one row per valid CNPJ and source/evidence columns.
Read the required cells and dates; do not send the whole CSV through the model just to copy it.
The free records already contain the screening data. Buy the formatted file when it removes
export work that your task still needs. An existing free integration and exporter may be sufficient.

## Decide whether the task is complete

If the requested blocks are present and their dates meet the task, answer from those fields.
State the checked sources and dates. You do not need to rebuild their collectors or generate the joins.
If a required block is missing or too old, say what remains unknown and choose the needed addition.
For a required CNIA source check, send `cnia_atual=true` on the additional lookup or dossier.
Without it, those operations can return the previous CNIA.
Paying does not refresh the Receita or PGFN snapshots.

These public records are not a credit-bureau report, an official certificate or supplier approval.
Debt totals include different collection states; inspect the breakdown before interpreting them.
An existing registry API can be enough for registration status alone.
Use the required original source when the task needs coverage that Radar does not provide.

## Decide what to pay

Read [current prices](https://radar-cnpj.com/api/pricing) and the
[lookup allowance and offers](https://radar-cnpj.com/api/consulta).
Use `gratis.restantes_hoje` and existing rights first.
For a dossier, `GET /api/dossie/preco` returns its price without charging.
For a batch, the quote counts valid, distinct CNPJs. Compare the total for the actual list.
Compare a pack's full purchase price and expiry with per-call payment; unused units are not savings.
Prepaid credit and x402 have different minimums. Read the quote and [payment terms](https://radar-cnpj.com/api/billing).
Lookup packs and monitoring capacity are separate. Read `/api/plans` for the available portfolio.
The source check, formatted report, unmasking, risk rules or continued monitoring must justify the addition.
This is not a claim that every paid operation costs less than the user's existing tools.

## Connect and pay

Use existing tools or `https://radar-cnpj.com/mcp`; no local install is required.
HTTP uses the same API. Read `tools/list` for the connected mode.
Reuse existing credit, access and spending authority. Request only missing authority.
Direct MCP x402 retries use `params._meta["x402/payment"]`; HTTP uses `PAYMENT-SIGNATURE`.
Credit uses `Authorization: Bearer cred_…` or `X-Credito`.
Keep the same `Idempotency-Key` on retry. Recover a lost result before signing another payment.
The same credit holder reopening a dossier for the same company on the same Brasília day does not pay again.
To get that dossier back without a charge, even with no balance left, read `GET /api/dossie/{cnpj}` with the same credit.
For unmasking, `GET /api/revelar/{cnpj}` checks the same owner's existing access without charging.
In `checkout=site`, the person purchases on the site. ChatGPT uses existing rights without sales.
Keep credentials secret. Reveal personal data only for the user's authorized purpose.
Follow returned pagination and `Retry-After`. Report sources, dates and missing checks.
