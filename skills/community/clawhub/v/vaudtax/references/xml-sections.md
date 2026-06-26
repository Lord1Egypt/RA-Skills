# VaudTax XML Sections

Proprietary format maintained by the Canton Vaud tax authority — no public XSD. Element names follow French naming conventions and may change across fiscal years. ✅ = parsed by `parse_vaudtax.py`.

## Metadata & Taxpayer Info
| Section | Description |
|---|---|
| `fiscalPeriod` | ✅ Tax year (e.g. `2025`) |
| `lastGesdemReference` | ✅ Gesdem submission reference |
| `identification` | ✅ Address, municipality, phone, email, IBAN |
| `taxpayerPersonalData1` | ✅ Name, birthdate, NAVS13, profession, marital status |
| `taxpayerPersonalData2` | ✅ Second taxpayer (joint filers only) |
| `representative` | Tax representative details (not yet parsed) |

## Income
| Section | Description |
|---|---|
| `activiteSalarieeRevenus` | ✅ Employed income: employer, net salary, pension contributions, dates, activity rate |
| `complementRentePension` | ✅ Pension/rente income: type, annual amount |
| `activitesIndependantes` | ✅ Self-employment income: activity name, net revenue |
| `autresRevenusExoneresImposesSource` | Other income (not yet parsed) |
| `revenuImposeAutreEtat` | Income taxed in other states (not yet parsed) |

## Deductions & Expenses
| Section | Description |
|---|---|
| `autresFraisEtFraisActiviteSalarialeAccessoire` | ✅ Professional expense deduction method (flat-rate or actual) |
| `fraisTransport` | ✅ Transport costs: type, km, number of days, route |
| `fraisRepas` | ✅ Meal costs: type, number of days |
| `primesEtCotisationsAssurance` | ✅ Insurance premiums, subsidies, 3rd pillar (3a) contributions |
| `deductionSocialeLogement` | ✅ Rent/housing deduction |
| `fraisMedicauxDentaires` | ✅ Medical and dental expenses |
| `interetsDettes` | ✅ Debt interest deductions (code 520) |
| `fraisFormation` | ✅ Training/education costs |
| `donationsAvancesHoiries` | ✅ Donations and inheritance advances |
| `successionHoirieDonation` | Inheritances flag (skipped when `isInitialized=false`) |

## Assets & Securities
| Section | Description |
|---|---|
| `etatTitres` | ✅ Bank accounts: IBAN, balance, yield |
| `relevesFiscauxBancaires` | ✅ Investment portfolios: fiscal value, gross income, IES |
| `numerairesList` | ✅ Cash and liquid assets |
| `objetsMobiliers` | ✅ Movable property / crypto |
| `biensImmobiliers` (2025) / `immeubles` (older) | ✅ Real estate: commune, parcelle, fiscal value, rental income |
| `autoMoto` | ✅ Vehicles |
| `fraisAdministrationTitres` | ✅ Management fees for securities (code 490) |

## Supporting Documents & Navigation
| Section | Description |
|---|---|
| `piecesJustificativesObligatoires` | Mandatory supporting document metadata |
| `piecesJustificativesFacultatives` | Optional supporting document metadata |
| `infosComplementairesIes` | Additional investment income (IES) information |
| `prestationsEnCapital` | Capital benefit payments (not yet parsed) |
| `guidedNav` / `userProfil` / `piecesJustificativesSubFormInitialized` | UI/navigation state — intentionally skipped |

## Known differences between fiscal years

| Section | 2023–2024 | 2025 |
|---|---|---|
| Medical expenses | `fraisMedicaux` | `fraisMedicauxDentaires` |
| Medical net amount | `montantACharge` | `montantFrais` |
| Real estate section | `immeubles` | `biensImmobiliers` |
| Real estate fiscal value | `valeurFiscale` | `estimationFiscale` |

`parse_vaudtax.py` handles both variants transparently.

## Inspecting raw XML

If a parsed field returns `None` unexpectedly, inspect actual child element names:

```python
import zipfile, xml.etree.ElementTree as ET
NS = "http://www.vd.ch/fiscalite/vaudtax"
with zipfile.ZipFile("file.vaudtax") as z:
    xml_name = next(n for n in z.namelist() if n.endswith(".xml"))
    root = ET.parse(z.open(xml_name)).getroot()
for el in root.findall(f"{{{NS}}}sectionName"):
    print({c.tag.split("}")[1]: c.text for c in el})
```
