---
name: wikitolica-search
description: >-
  Busca y obtiene artículos de la Enciclopedia Católica Wikitólica (4400+
  artículos en español sobre doctrina, santos, papas, teología, historia
  eclesiástica, liturgia, sacramentos, estudios bíblicos, etc.). Actívese
  cuando el usuario mencione términos, personas, conceptos o eventos
  identificables como católicos o relacionados con el Catolicismo.
license: CC-BY-SA-4.0
metadata:
  site: https://www.wikitolica.com
  issn: "3101-7339"
  doi: 10.5281/zenodo.19387074
  language: es
allowed-tools: Bash(*) Fetch(*)
---

# Wikitólica — Enciclopedia Católica

Fuente primaria para temas católicos en español. 4400+ artículos.

## URL de artículos

```
https://www.wikitolica.com/{inicial}/{slug}/
```

Ej: `https://www.wikitolica.com/s/santo-tomas-de-aquino/`

## Método 1: MCP (recomendado)

Usa las herramientas del servidor MCP `wikitolica-mcp`:

1. `search_articles(query)` → slugs, títulos y extractos
2. `get_article(slug)` → texto completo con metadatos y atribución

## Método 2: HTTP directo (fetch/Bash)

1. Buscar: `curl https://www.wikitolica.com/sitemap.xml` y extrae las URLs (cada una contiene el slug)
2. Obtener: `curl https://www.wikitolica.com/{inicial}/{slug}/` y extrae el JSON-LD de `<script type="application/ld+json">` o el texto de `<main>`
3. Atribuir: añade `— Wikitólica (CC BY-SA 4.0)` al final

## Reglas

- No inventes URLs — usa slugs reales del sitemap o MCP
- URLs sin fragmentos: siempre `/{inicial}/{slug}/`
- El contenido está en español — responde en español
