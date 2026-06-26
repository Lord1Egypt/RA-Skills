# AI Health Assistant Schema

Data structure definition for AI health analysis and risk prediction.

## Analysis Types

| Operation | Description |
|-----------|-------------|
| analyze | Comprehensive health analysis |
| predict | Health risk prediction |
| chat | Intelligent health Q&A |
| report | Generate AI report |
| status | View feature status |

## Risk Prediction Types

| Type | Description | Model |
|-----|-------------|-------|
| hypertension | Hypertension risk (10-year) | Framingham |
| diabetes | Diabetes risk (10-year) | ADA |
| cardiovascular | Cardiovascular risk (10-year) | Framingham |
| nutritional_deficiency | Nutritional deficiency risk | Custom |
| sleep_disorder | Sleep disorder risk | Custom |

## Report Types

| Type | Description |
|-----|-------------|
| comprehensive | Comprehensive health report |
| quick_summary | Quick summary |
| risk_assessment | Risk assessment report |
| trend_analysis | Trend analysis report |

## Analysis Result Fields

| Field | Type | Description |
|-----|------|-------------|
| `overall_health_score.score` | number | 0-100 score |
| `overall_health_score.grade` | string | Excellent/Good/Fair/Needs Attention |
| `risk_predictions[]` | array | Risk prediction list |
| `trends[]` | array | Trend analysis |
| `correlations[]` | array | Correlation findings |
| `recommendations[]` | array | Personalized recommendations |

## Data Storage

- AI configuration: `data/ai-config.json`
- Analysis reports: `data/ai-reports/`
- Conversation records: `data/ai-conversations/`
