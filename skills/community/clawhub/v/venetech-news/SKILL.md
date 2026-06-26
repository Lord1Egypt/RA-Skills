---
name: VeneTech News
description: >
  Usa este skill siempre que el usuario pida noticias, actualizaciones, resúmenes o
  briefings sobre tecnología, startups, inteligencia artificial, fintech, cripto,
  innovación o emprendimiento digital — especialmente en el contexto venezolano o
  latinoamericano. Activa este skill cuando el usuario diga frases como "qué hay de
  nuevo en tech Venezuela", "dame noticias de startups venezolanas", "resumen tech de
  hoy", "qué pasó en IA esta semana", "noticias VenTech", "briefing tecnológico
  venezolano", o cualquier variante. También activa cuando el usuario mencione el
  proyecto VenTech News y pida contenido editorial o scraping de fuentes.
---

# VeneTech News — Skill de Noticias Tech Venezolanas

## Visión General

Obtiene y resume noticias de tecnología, startups, IA, fintech y emprendimiento
digital desde el ecosistema venezolano y latinoamericano. Agrega contenido de
14 fuentes en español e inglés, priorizando el contexto venezolano.

---

## Fuentes RSS y HTTP

### 🇻🇪 Portales Venezolanos (scraping HTTP + BeautifulSoup)

```bash
# Banca y Negocios — fintech y economía digital
curl -sL -A "Mozilla/5.0" "https://bancaynegocios.com/tecnologia/"

# Con-Café — tech y vida digital en Caracas (tiene RSS WordPress)
curl -sL -A "Mozilla/5.0" "https://con-cafe.com/feed/"

# El Estímulo — análisis, economía y startups
curl -sL -A "Mozilla/5.0" "https://elestimulo.com/tecnologia/"

# El Nacional — política, economía y tech
curl -sL -A "Mozilla/5.0" "https://www.elnacional.com/tecnologia/"

# Noticias 24 — breaking news y tech Venezuela
curl -sL -A "Mozilla/5.0" "https://www.noticias24.com/tecnologia/"

# El Pitazo — periodismo independiente verificado
curl -sL -A "Mozilla/5.0" "https://elpitazo.net/tecnologia/"

# Globovisión — noticias 24h Venezuela y mundo
curl -sL -A "Mozilla/5.0" "https://globovision.com/tecnologia/"

# TeleSUR — Venezuela y Latinoamérica
curl -sL -A "Mozilla/5.0" "https://www.telesurtv.net/tecnologia/"
```

### 🌎 Tech en Español — RSS Feed (más limpio y estable)

```bash
# Xataka — gadgets, móviles, IA
curl -sL -A "Mozilla/5.0" "https://www.xataka.com/rss"

# Hipertextual — tecnología, ciencia, tendencias
curl -sL -A "Mozilla/5.0" "https://hipertextual.com/feed"

# FayerWayer — tech latinoamericano, startups
curl -sL -A "Mozilla/5.0" "https://www.fayerwayer.com/feed/"

# Bloomberg Línea — tech y mercados para LATAM
curl -sL -A "Mozilla/5.0" "https://bloomberglinea.com/arc/outboundfeeds/rss/category/tecnologia/"
```

### 🇺🇸 Tech Global en Inglés — RSS Feed oficial

```bash
# TechCrunch — startups, VC, innovación global
curl -sL "https://techcrunch.com/feed/"

# Ars Technica — hardware, software, ciberseguridad
curl -sL "https://feeds.arstechnica.com/arstechnica/index"
```

---

## Parseo de RSS

Extraer títulos y descripciones de un feed RSS:

```bash
curl -sL -A "Mozilla/5.0" "https://www.xataka.com/rss" | \
  python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.parse(sys.stdin).getroot()
items = root.findall('.//item')[:8]
for i in items:
    title = i.find('title')
    desc  = i.find('description')
    link  = i.find('link')
    pub   = i.find('pubDate')
    print('TÍTULO:', title.text.strip() if title is not None else '')
    print('DESC:',   (desc.text or '')[:120].strip() if desc is not None else '')
    print('URL:',    link.text.strip() if link is not None else '')
    print('FECHA:',  pub.text.strip() if pub is not None else '')
    print('---')
"
```

Parseo ligero para HTML de portales venezolanos (BeautifulSoup):

```bash
pip install beautifulsoup4 requests --break-system-packages -q

python3 - <<'EOF'
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

url = "https://con-cafe.com/feed/"
r = requests.get(url, headers=HEADERS, timeout=10)
soup = BeautifulSoup(r.content, "xml")
items = soup.find_all("item")[:6]
for item in items:
    print("TÍTULO:", item.find("title").text.strip()[:90])
    print("URL:", item.find("link").text.strip() if item.find("link") else "")
    print("---")
EOF
```

---

## Workflow Estándar

### 1. Resumen Rápido (texto, 5–8 noticias)

1. Obtener feed RSS de Con-Café (WordPress nativo, más confiable)
2. Complementar con Xataka y FayerWayer para contexto regional
3. Agregar 1–2 noticias de TechCrunch si hay algo relevante para Venezuela
4. Filtrar por categorías relevantes (ver abajo)
5. Deduplicar titulares similares entre fuentes
6. Sintetizar en formato editorial con contexto venezolano

### 2. Briefing Completo (semanal o por categoría)

1. Scraping/RSS de las 8 fuentes venezolanas
2. RSS de las 4 fuentes tech en español
3. RSS de TechCrunch y Ars Technica para contexto global
4. Agrupar por categoría editorial
5. Destacar noticias que afecten directamente a Venezuela
6. Generar resumen en formato newsletter

---

## Filtros de Relevancia para Venezuela

Al procesar noticias internacionales, priorizar si menciona:

- Empresas venezolanas o fundadores venezolanos
- Mercados latinoamericanos con impacto en Venezuela
- Criptomonedas / USDT (muy usadas en Venezuela como reserva de valor)
- Remesas digitales y transferencias internacionales
- Ecommerce o pagos digitales en LATAM
- Trabajos remotos y plataformas de freelance
- Regulación tech en Venezuela o países similares
- Acceso a internet, censura digital, VPNs
- Inteligencia Artificial accesible en mercados emergentes

---

## Categorías Editoriales

| Emoji | Categoría | Palabras clave |
|-------|-----------|----------------|
| 🚀 | Startups Venezuela | startup, emprendimiento, fundador, ronda, inversión, lanzamiento VE |
| 🤖 | Inteligencia Artificial | IA, AI, ChatGPT, LLM, modelo, automatización, machine learning |
| 💰 | Fintech & Cripto | fintech, crypto, bitcoin, USDT, blockchain, pago digital, remesa |
| 📱 | Gadgets & Apps | app, smartphone, dispositivo, lanzamiento, software, plataforma |
| 🌎 | Tech Latinoamérica | LATAM, Colombia, Brasil, México, startup regional, ecosistema |
| 📊 | Economía Digital | ecommerce, trabajo remoto, freelance, digitalización, plataforma |
| 🔒 | Ciberseguridad | ciberseguridad, privacidad, VPN, hackeo, datos, malware, Venezuela |
| 🎓 | Educación Tech | curso, beca, bootcamp, formación, oportunidad para venezolanos |

---

## Formato de Salida

```
📡 VenTech News — [Fecha]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 STARTUPS VENEZUELA
• [Titular adaptado al contexto venezolano]
  → [Fuente] | [URL]

🤖 INTELIGENCIA ARTIFICIAL
• [Titular + por qué importa para Venezuela]
  → [Fuente] | [URL]

💰 FINTECH & CRIPTO
• [Titular]
  → [Fuente] | [URL]

[... otras categorías con noticias disponibles ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🇻🇪 VenTech News — Construyendo el ecosistema digital venezolano
```

---

## Buenas Prácticas

- **Nunca reproducir artículos completos** — solo título, resumen (≤150 palabras) y URL
- **Respetar robots.txt** de cada portal antes de iniciar scraping
- **Rate limiting**: máximo 1 request por segundo por dominio
- **User-Agent real**: usar Mozilla/5.0 Chrome para evitar bloqueos en portales VE
- **Proxies rotativos**: recomendados para elpitazo.net (bloqueos frecuentes)
- **RSS primero**: preferir feed RSS sobre scraping directo cuando esté disponible
- **Contexto venezolano**: siempre agregar una frase sobre cómo la noticia impacta al ecosistema venezolano o la diáspora

---

## Notas Técnicas por Portal

| Portal | Método recomendado | Notas |
|--------|--------------------|-------|
| con-cafe.com | RSS `/feed/` | WordPress, muy confiable |
| xataka.com | RSS `/rss` | Feed oficial limpio |
| hipertextual.com | RSS `/feed` | Feed oficial disponible |
| fayerwayer.com | RSS `/feed/` | RSS público estable |
| techcrunch.com | RSS `/feed/` | NO scraping directo |
| arstechnica.com | RSS feed oficial | NO scraping directo |
| elpitazo.net | HTTP + BS4 | Usar proxies, bloqueos frecuentes |
| globovision.com | HTTP + BS4 | API interna detectable en DevTools |
| elnacional.com | HTTP + BS4 | Requiere User-Agent real |
| elestimulo.com | HTTP + BS4 | Puede requerir Selenium si hay JS |
| bancaynegocios.com | HTTP + BS4 | Sección `/tecnologia` separada |
| noticias24.com | HTTP + BS4 | Estructura limpia, fácil parseo |
| telesurtv.net | HTTP + BS4 | Verificar robots.txt, sección `/tecnologia` |
| bloomberglinea.com | HTTP + BS4 | Verificar rate limiting |
