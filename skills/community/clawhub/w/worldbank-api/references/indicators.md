# Verified Indicator Codes by Topic

Every code below was verified against the live API (data query, not just
metadata). All are annual series in source 2 (World Development Indicators)
unless noted — no `source` parameter needed. Query pattern:

```
GET https://api.worldbank.org/v2/country/{codes}/indicator/{CODE}?format=json&mrnev=1
```

## Contents

- [Economy and growth](#economy-and-growth)
- [Prices, money, interest rates](#prices-money-interest-rates)
- [Government finance](#government-finance)
- [Trade and external sector](#trade-and-external-sector)
- [Population and demographics](#population-and-demographics)
- [Health](#health)
- [Education](#education)
- [Labor](#labor)
- [Poverty, inequality, gender](#poverty-inequality-gender)
- [Environment, energy, land](#environment-energy-land)
- [Technology and infrastructure](#technology-and-infrastructure)
- [Financial sector](#financial-sector)
- [Governance (WGI, source 3)](#governance-wgi-source-3)
- [Sub-annual series](#sub-annual-series)
- [Archived codes and their successors](#archived-codes-and-their-successors)

## Economy and growth

| Code | Indicator |
|---|---|
| `NY.GDP.MKTP.CD` | GDP (current US$) |
| `NY.GDP.MKTP.KD` | GDP (constant 2015 US$) |
| `NY.GDP.MKTP.KD.ZG` | GDP growth (annual %) |
| `NY.GDP.MKTP.PP.CD` | GDP, PPP (current international $) |
| `NY.GDP.PCAP.CD` | GDP per capita (current US$) |
| `NY.GDP.PCAP.KD` | GDP per capita (constant 2015 US$) |
| `NY.GDP.PCAP.PP.CD` | GDP per capita, PPP (current international $) |
| `NY.GNP.MKTP.CD` | GNI (current US$) |
| `NY.GNP.PCAP.CD` | GNI per capita, Atlas method (current US$) |
| `NY.GDP.DEFL.KD.ZG` | Inflation, GDP deflator (annual %) |
| `NV.AGR.TOTL.ZS` | Agriculture, forestry, fishing value added (% of GDP) |
| `NV.IND.MANF.ZS` | Manufacturing, value added (% of GDP) |
| `NV.SRV.TOTL.ZS` | Services, value added (% of GDP) |
| `NE.GDI.TOTL.ZS` | Gross capital formation (% of GDP) |
| `NY.GNS.ICTR.ZS` | Gross savings (% of GDP) |

## Prices, money, interest rates

| Code | Indicator |
|---|---|
| `FP.CPI.TOTL.ZG` | Inflation, consumer prices (annual %) |
| `FP.CPI.TOTL` | Consumer price index (2010 = 100) |
| `FR.INR.RINR` | Real interest rate (%) |
| `FR.INR.LEND` | Lending interest rate (%) |
| `FR.INR.DPST` | Deposit interest rate (%) |
| `FM.LBL.BMNY.GD.ZS` | Broad money (% of GDP) |
| `PA.NUS.FCRF` | Official exchange rate (LCU per US$, period average) |
| `PA.NUS.PPP` | PPP conversion factor, GDP (LCU per international $) |

## Government finance

| Code | Indicator |
|---|---|
| `GC.DOD.TOTL.GD.ZS` | Central government debt, total (% of GDP) |
| `GC.TAX.TOTL.GD.ZS` | Tax revenue (% of GDP) |
| `GC.XPN.TOTL.GD.ZS` | Expense (% of GDP) |
| `GC.REV.XGRT.GD.ZS` | Revenue, excluding grants (% of GDP) |
| `MS.MIL.XPND.GD.ZS` | Military expenditure (% of GDP) |

## Trade and external sector

| Code | Indicator |
|---|---|
| `NE.EXP.GNFS.ZS` | Exports of goods and services (% of GDP) |
| `NE.IMP.GNFS.ZS` | Imports of goods and services (% of GDP) |
| `TG.VAL.TOTL.GD.ZS` | Merchandise trade (% of GDP) |
| `BX.KLT.DINV.WD.GD.ZS` | FDI, net inflows (% of GDP) |
| `BX.KLT.DINV.CD.WD` | FDI, net inflows (BoP, current US$) |
| `BN.CAB.XOKA.GD.ZS` | Current account balance (% of GDP) |
| `BX.TRF.PWKR.DT.GD.ZS` | Personal remittances, received (% of GDP) |
| `DT.DOD.DECT.CD` | External debt stocks, total (current US$) |
| `FI.RES.TOTL.CD` | Total reserves incl. gold (current US$) |
| `DT.ODA.ODAT.CD` | Net official development assistance received (current US$) |

## Population and demographics

| Code | Indicator |
|---|---|
| `SP.POP.TOTL` | Population, total |
| `SP.POP.GROW` | Population growth (annual %) |
| `SP.POP.0014.TO.ZS` | Population ages 0–14 (% of total) |
| `SP.POP.65UP.TO.ZS` | Population ages 65+ (% of total) |
| `SP.DYN.TFRT.IN` | Fertility rate, total (births per woman) |
| `SP.DYN.CBRT.IN` | Birth rate, crude (per 1,000 people) |
| `SP.DYN.CDRT.IN` | Death rate, crude (per 1,000 people) |
| `SP.DYN.LE00.IN` | Life expectancy at birth, total (years) |
| `SP.DYN.LE00.FE.IN` / `SP.DYN.LE00.MA.IN` | Life expectancy, female / male |
| `SP.DYN.IMRT.IN` | Mortality rate, infant (per 1,000 live births) |
| `SP.URB.TOTL` | Urban population |
| `SP.URB.TOTL.IN.ZS` | Urban population (% of total) |
| `SP.RUR.TOTL.ZS` | Rural population (% of total) |
| `SM.POP.NETM` | Net migration |
| `EN.POP.DNST` | Population density (people per sq. km) |

## Health

| Code | Indicator |
|---|---|
| `SH.XPD.CHEX.GD.ZS` | Current health expenditure (% of GDP) |
| `SH.XPD.CHEX.PC.CD` | Current health expenditure per capita (current US$) |
| `SH.DYN.MORT` | Mortality rate, under-5 (per 1,000 live births) |
| `SH.STA.MMRT` | Maternal mortality ratio (per 100,000 live births) |
| `SH.MED.BEDS.ZS` | Hospital beds (per 1,000 people) |
| `SH.MED.PHYS.ZS` | Physicians (per 1,000 people) |
| `SN.ITK.DEFC.ZS` | Prevalence of undernourishment (% of population) |
| `SH.IMM.MEAS` | Immunization, measles (% of children 12–23 months) |

## Education

| Code | Indicator |
|---|---|
| `SE.ADT.LITR.ZS` | Literacy rate, adult total (% ages 15+) |
| `SE.XPD.TOTL.GD.ZS` | Government expenditure on education (% of GDP) |
| `SE.PRM.ENRR` | School enrollment, primary (% gross) |
| `SE.SEC.ENRR` | School enrollment, secondary (% gross) |
| `SE.TER.ENRR` | School enrollment, tertiary (% gross) |
| `SE.PRM.CMPT.ZS` | Primary completion rate (% of relevant age group) |
| `SE.COM.DURS` | Compulsory education, duration (years) |

## Labor

| Code | Indicator |
|---|---|
| `SL.UEM.TOTL.ZS` | Unemployment, total (% of labor force, ILO) |
| `SL.UEM.1524.ZS` | Unemployment, youth (% ages 15–24, ILO) |
| `SL.TLF.CACT.ZS` | Labor force participation rate, total (% ages 15+) |
| `SL.TLF.CACT.FE.ZS` | Labor force participation rate, female |
| `SL.TLF.TOTL.IN` | Labor force, total |
| `SL.EMP.TOTL.SP.ZS` | Employment to population ratio, 15+ (%) |

## Poverty, inequality, gender

| Code | Indicator |
|---|---|
| `SI.POV.DDAY` | Poverty headcount at $3.00/day, 2021 PPP (% of population) |
| `SI.POV.NAHC` | Poverty headcount at national poverty lines (%) |
| `SI.POV.GINI` | Gini index |
| `SI.DST.10TH.10` | Income share held by highest 10% |
| `SI.DST.FRST.20` | Income share held by lowest 20% |
| `SG.GEN.PARL.ZS` | Seats held by women in national parliament (%) |

## Environment, energy, land

| Code | Indicator |
|---|---|
| `EN.GHG.CO2.PC.CE.AR5` | CO2 emissions per capita, excl. LULUCF (t CO2e) |
| `EN.GHG.CO2.MT.CE.AR5` | CO2 emissions total, excl. LULUCF (Mt CO2e) |
| `EN.GHG.ALL.PC.CE.AR5` | Total GHG emissions per capita (t CO2e) |
| `EG.USE.ELEC.KH.PC` | Electric power consumption (kWh per capita) |
| `EG.USE.PCAP.KG.OE` | Energy use (kg of oil equivalent per capita) |
| `EG.ELC.ACCS.ZS` | Access to electricity (% of population) |
| `EG.ELC.RNEW.ZS` | Renewable electricity output (% of total) |
| `EG.FEC.RNEW.ZS` | Renewable energy consumption (% of final energy) |
| `AG.LND.FRST.ZS` | Forest area (% of land area) |
| `AG.LND.AGRI.ZS` | Agricultural land (% of land area) |
| `AG.LND.TOTL.K2` | Land area (sq. km) |
| `AG.SRF.TOTL.K2` | Surface area (sq. km) |

## Technology and infrastructure

| Code | Indicator |
|---|---|
| `IT.NET.USER.ZS` | Individuals using the Internet (% of population) |
| `IT.CEL.SETS.P2` | Mobile cellular subscriptions (per 100 people) |
| `IT.NET.BBND.P2` | Fixed broadband subscriptions (per 100 people) |
| `IS.AIR.PSGR` | Air transport, passengers carried |
| `TX.VAL.TECH.MF.ZS` | High-technology exports (% of manufactured exports) |
| `GB.XPD.RSDV.GD.ZS` | R&D expenditure (% of GDP) |
| `IP.PAT.RESD` | Patent applications, residents |

## Financial sector

| Code | Indicator |
|---|---|
| `FS.AST.PRVT.GD.ZS` | Domestic credit to private sector (% of GDP) |
| `CM.MKT.LCAP.GD.ZS` | Market capitalization of listed companies (% of GDP) |
| `FX.OWN.TOTL.ZS` | Account ownership, financial institution or mobile money (% ages 15+) |

## Governance (WGI, source 3)

Worldwide Governance Indicators live in **source 3** and were renamed from the
old `CC.EST`-style codes (now dead) to a `GOV_WGI_` prefix. Two quirks:
`source=3` is required, and **`mrv`/`mrnev` fail on this source** (transient
"Request Error" pages) — use an explicit `date=` range instead:

```
GET /v2/country/US/indicator/GOV_WGI_CC.EST?format=json&date=2020:2023&source=3
```

| Code | Indicator (all: estimate, approx. −2.5 to +2.5) |
|---|---|
| `GOV_WGI_CC.EST` | Control of Corruption |
| `GOV_WGI_GE.EST` | Government Effectiveness |
| `GOV_WGI_PV.EST` | Political Stability and Absence of Violence |
| `GOV_WGI_RL.EST` | Rule of Law |
| `GOV_WGI_RQ.EST` | Regulatory Quality |
| `GOV_WGI_VA.EST` | Voice and Accountability |

Each also has `.SC` variants (0–100 score), e.g. `GOV_WGI_CC.SC`.

## Sub-annual series

| Code | Indicator | Source |
|---|---|---|
| `DPANUSSPB` | Exchange rate, LCU per USD, monthly (`date=2025M01:2025M06`) | `source=15` (GEM) |
| `DP.DOD.DECD.CR.GG.CD` | Gross public sector debt, general gov., quarterly | `source=20` |

Browse more with `/v2/source/15/indicators?format=json` (Global Economic
Monitor) and sources 20/22/23 (quarterly debt).

## Archived codes and their successors

Data queries on archived codes fail with error id 175 even though the
metadata endpoint still describes them. Known cases:

| Dead code | Use instead |
|---|---|
| `EN.ATM.CO2E.PC`, `EN.ATM.CO2E.KT` (old CO2 series) | `EN.GHG.CO2.PC.CE.AR5`, `EN.GHG.CO2.MT.CE.AR5` |
| `CC.EST`, `GE.EST`, `RL.EST`, `RQ.EST`, `PV.EST`, `VA.EST` (old WGI) | `GOV_WGI_*.EST` with `source=3` |
| `IC.BUS.EASE.XQ` and all Doing Business (source 1) | Retired; use B-READY reports outside this API |

If a code that "should exist" fails, run
`wb_data.py --search "keyword"` or check the source's live catalog
(`/v2/source/{id}/indicators`) — membership there is the ground truth.
