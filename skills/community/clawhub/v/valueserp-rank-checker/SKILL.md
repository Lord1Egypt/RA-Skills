---
name: valueserp-rank-checker
description: Verifica la posición de una palabra clave para un dominio específico en Google usando la API de ValueSERP. Úsalo cuando el usuario pregunte "¿en qué posición está [keyword] en [dominio]?", "¿cómo rankea [dominio] para [keyword]?", "revisa el ranking de [keyword]", o cualquier consulta sobre posicionamiento SEO de un dominio en Google. Por defecto busca en Google Colombia (español).
metadata:
  openclaw:
    primaryEnv: VALUESERP_API_KEY
    requires:
      env:
        - VALUESERP_API_KEY
    envVars:
      - name: VALUESERP_API_KEY
        required: true
        description: API key de ValueSERP. Obtén la tuya en https://app.valueserp.com
    emoji: "📊"
    homepage: https://www.valueserp.com/docs/search-api/overview
---

# ValueSERP Rank Checker

Consulta la posición de una palabra clave para un dominio en Google usando la API de ValueSERP.

## Flujo

1. Extraer `keyword` y `domain` del mensaje del usuario.
2. Ejecutar `scripts/check_rank.py`.
3. Presentar el resultado de forma clara en español.

## Ejecutar la consulta

```bash
python3 scripts/check_rank.py "<keyword>" <domain>
```

Opciones adicionales:
- `--gl co` — país (default: Colombia)
- `--hl es` — idioma (default: español)
- `--pages 10` — páginas a revisar (10 resultados/página, default: top 100)

Ejemplos:
```bash
python3 scripts/check_rank.py "noticias" eltiempo.com
```

## Interpretar el resultado

**Encontrado:**
```json
{
  "found": true,
  "keyword": "el tiempo",
  "domain": "eltiempo.com",
  "position": 3,
  "page": 1,
  "position_in_page": 3,
  "url": "https://eltiempo.com/...",
  "title": "El Tiempo - ..."
}
```

**No encontrado:**
```json
{
  "found": false,
  "keyword": "el tiempo",
  "domain": "eltiempo.com",
  "pages_checked": 10,
  "message": "No se encontró 'eltiempo.com' en las primeras 100 posiciones."
}
```

## Formato de respuesta al usuario

Cuando esté en posición:
> **eltiempo.com** está en la posición **#3** para "*El tiempo*" en Google Colombia.
> URL: https://...

Cuando no aparezca en top 100:
> **eltiempo.com** no aparece en las primeras 100 posiciones para "*El tiempo*" en Google Colombia.

Si el usuario pide otro país o idioma, ajusta `--gl` y `--hl` según corresponda.
