# URL Mapping Rules

Base URL: `https://staghornfern.org`

## Species Pages
Pattern: `{base}/species/{slug}`
| Slug | Species |
|------|---------|
| p-alcicorne | P. alcicorne |
| p-andinum | P. andinum |
| p-bifurcatum | P. bifurcatum |
| p-coronarium | P. coronarium |
| p-elephantotis | P. elephantotis |
| p-ellisii | P. ellisii |
| p-grande | P. grande |
| p-hillii | P. hillii |
| p-holttumii | P. holttumii |
| p-madagascariense | P. madagascariense |
| p-quadridichotomum | P. quadridichotomum |
| p-ridleyi | P. ridleyi |
| p-stemaria | P. stemaria |
| p-superbum | P. superbum |
| p-veitchii | P. veitchii |
| p-wallichii | P. wallichii |
| p-wandae | P. wandae |
| p-willinckii | P. willinckii |

All species pages available in: en, zh-cn, zh-tw

## Guide Pages
Pattern: `{base}/guides/{slug}`
| Slug | Topic | zh-cn available |
|------|-------|-----------------|
| staghorn-fern-care-guide | Comprehensive care | No |
| watering-wisdom | Watering | Yes |
| lighting-101 | Light requirements | Yes |
| mounting-basics | Mounting techniques | Yes |
| pest-control | Pest control | Yes |
| how-to-propagate-staghorn-fern | Propagation | No |
| how-to-hang-a-staghorn-fern | Hanging & display | No |
| staghorn-fern-brown-tips | Brown tips diagnosis | No |
| why-is-my-staghorn-fern-dying | Dying plant diagnosis | No |
| staghorn-fern-fertilizer | Fertilizer guide | No |
| staghorn-fern-indoor-care | Indoor care | No |
| staghorn-fern-winter-care | Winter care | No |
| staghorn-fern-vs-elkhorn-fern | Staghorn vs Elkhorn | No |
| platycerium-species-guide | All 18 species overview | No |
| platycerium-hybridization-guide | Hybridization guide | No |
| staghorn-fern-anatomy-and-growth-patterns | Anatomy guide | No |
| staghorn-fern-soil-and-potting-mix | Soil & substrate | No |

## Database
Pattern: `{base}/database/hybrid-cultivar-database`

## i18n URL Rules
- English (default): `https://staghornfern.org/species/{slug}` or `/guides/{slug}`
- Simplified Chinese: `https://staghornfern.org/zh-cn/species/{slug}` or `/zh-cn/guides/{slug}`
- Traditional Chinese: `https://staghornfern.org/zh-tw/species/{slug}` or `/zh-tw/guides/{slug}`

## Link Selection Rules
1. For species questions → link to the specific species page
2. For care questions → link to the most relevant guide
3. For diagnosis questions → link to brown-tips or why-dying guide
4. For cultivar/hybrid questions → link to hybridization guide or database
5. For general overview → link to care guide or species guide
6. If user speaks Chinese, prefer zh-cn URLs when available; otherwise use English URLs
7. If user speaks Traditional Chinese, prefer zh-tw URLs
