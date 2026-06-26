# Naming Conventions

## Principles
- Use blocos em colchetes separados por espaco.
- O nome precisa ser legivel por humano e filtravel por metadata.
- Omitir campos nao aplicaveis; nunca usar placeholders vazios.
- Todo build novo nasce com `PAUSED` quando o status fizer sentido no nome.

## Campaign
Formato:
`[Platform] [Objective] [Offer] [Funnel] [Geo] [Audience] [Status] [YYYY-MM-DD]`

Exemplo:
`[Meta] [Sales] [Consultoria] [BOFU] [BR] [Broad] [PAUSED] [2026-03-13]`

## Ad Set
Formato:
`[Index] [Audience] [Placement] [Optimization] [Window] [Budget]`

Exemplo:
`[01] [Lookalike 1% Compradores] [Advantage+ Placements] [Purchase] [30D] [R$300]`

## Ad
Formato:
`[Angle] [Format] [Hook] [CTA] [vN]`

Exemplo:
`[Dor Operacional] [Video] [Gancho 01] [Fale no WhatsApp] [v1]`

## Creative
Formato:
`[Offer] [Angle] [Format] [Asset] [rN]`

Exemplo:
`[Consultoria] [Case de Escala] [UGC] [Cliente A] [r2]`

## Tracking template
Use este padrao canonico:

```text
utm_source=MetaAds&utm_medium={{adset.name}}|{{adset.id}}&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_term={{placement}}&utm_content={{ad.name}}|{{ad.id}}
```

## Naming guardrails
- `Platform` deve ser `Meta`.
- `Status` padrao para ativos novos: `PAUSED`.
- `Index` deve seguir `01`, `02`, `03`...
- O mesmo conceito deve manter o mesmo vocabulario ao longo da conta.
