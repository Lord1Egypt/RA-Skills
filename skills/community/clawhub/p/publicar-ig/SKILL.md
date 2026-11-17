---
name: publicar-ig
description: "Skill para publicar fotos, carruseles (1-10 slides) o reels en el Instagram profesional de la usuaria desde su agente, con la conexión de Instagram que ELLA conectó (Composio, o Zapier si lo tiene). Activar SIEMPRE que pida: \"publica esto en Instagram\", \"/publicar-ig\", \"sube este carrusel a IG\", \"publica este reel\", \"manda esto a Instagram\", \"haz el post en IG\", \"publica lo que acabamos de hacer\", o cualquier variación que combine un archivo/carpeta de imagen o video con la intención de publicarlo en Instagram. Usa URLs públicas (las de Higgsfield, una que ella dé, o su propio repo público de GitHub si lo conectó). Nunca publica sin mostrar el preview completo y recibir ✅ explícito por Telegram. NO maneja Stories."
argument-hint: "<ruta archivo|carpeta|URL> [--caption=\"...\"] [--ubicacion=\"...\"] [--tags=@u1,@u2]"
metadata: {"version": "1.0.0", "depends-on": [], "mcp-required": ["Zapier-MCP"], "external-deps": ["github CLI (gh) authenticated", "Instagram for Business connected in Zapier"], "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Publicas con la conexión de Instagram profesional de la USUARIA: Composio si está conectado (revisa en su lista de acciones que exista la de publicar foto/carrusel/reel), o Zapier MCP si ella lo conectó. Si ninguna existe, no publiques: manda los archivos y el caption por Telegram listos para subir a mano.
> - Instagram exige URLs públicas. En orden: 1) si el archivo salió de Higgsfield, usa su URL de resultado directo (no hace falta subir nada); 2) si ella dio una URL pública, esa; 3) el repo público de GitHub del Paso 2 SOLO con su propia cuenta de GitHub conectada y su ✅ para crearlo, avisándole que todo lo que se sube ahí queda visible para cualquiera. Nunca un repo o almacenamiento que no sea de ella.
> - Las rutas locales se resuelven contra el workspace: carruseles en `entregables/carruseles/<tema>/`, infografías en `entregables/infografias/`. Los slides que mandó por Telegram se guardan primero en `entregables/publicar/AAAA-MM-DD-<slug>/`.
> - El Paso 4 (preview + «¿Publico?») es obligatorio SIEMPRE, también dentro de una automatización: sin ✅ explícito de la usuaria en Telegram no se publica. Nunca publiques algo que no se le mostró completo (todas las slides + caption entero).
> - El `instagramPageId` se guarda en `cerebro/memoria/instagram_page_id.md` y se suma a `cerebro/INDICE.md`.
> - Stories siguen sin soporte. Reels de más de 50 MB no pasan por Telegram: pide el link público.

---

# Skill: publicar-ig — Publicar en Instagram desde Claude Code

Pipeline de un comando: archivo local → repo público GitHub → URL raw → Zapier publica en IG.

---

## ⚠️ Pre-flight (SIEMPRE antes de publicar)

1. **Verificar que Instagram for Business sigue habilitado en Zapier:**
   ```
   mcp__Zapier-MCP__list_enabled_zapier_actions(app="Instagram for Business")
   ```
   Debe incluir `publish_media_v2` (fotos) y/o `publish_video` (reels). Si falta alguna,
   abortar y pedirle al usuario que la habilite en https://mcp.zapier.com.

2. **Verificar que el asset repo existe localmente:**
   - Path esperado: `entregables/.ig-assets-repo/` (solo si la usuaria conectó SU GitHub y dio ✅)
   - Si no existe: `gh repo clone <TU-USUARIO-GITHUB>/ig-assets entregables/.ig-assets-repo`
   - Si el repo no existe en GitHub: crearlo con
     `gh repo create formula100k-ig-assets --public --add-readme` y luego clonar.

3. **Resolver `instagramPageId`:**
   - Buscar en `cerebro/memoria/instagram_page_id.md`
   - Si NO existe: NO pasar `instagramPageId` en la primera llamada — Zapier resolverá la cuenta
     automáticamente si el usuario solo tiene una conectada. Si la respuesta de Zapier indica que
     hay múltiples cuentas o que el campo es ambiguo, mostrar las opciones al usuario, pedirle
     que elija, y guardar la elegida en memoria con la siguiente plantilla:

     ```markdown
     ---
     name: Instagram Page ID del usuario (FÓRMULA 100K)
     description: ID de la cuenta Instagram for Business conectada a Zapier — usar siempre como instagramPageId al publicar
     type: reference
     ---

     instagramPageId: <valor>
     Cuenta: la que el usuario confirme (nunca asumir un @)
     Fecha de captura: <YYYY-MM-DD>
     ```

     Y agregar a `cerebro/INDICE.md` la línea correspondiente.

---

## Resolución de input

El usuario puede pasar:

| Input | Interpretación |
|---|---|
| `https://...` | URL pública directa, no se sube nada |
| Ruta absoluta a archivo (`.png`,`.jpg`,`.gif`,`.bmp`) | Foto única → publish_media_v2 |
| Ruta absoluta a archivo (`.mp4`,`.mov`,`.webm`,`.mkv`,...) | Video/Reel → publish_video |
| Ruta absoluta a carpeta | Carrusel: lee todos los `.png/.jpg/.gif/.bmp` ordenados alfabéticamente (slide-1, slide-2,...) y arma carrusel de 1-10 |
| Ruta relativa | Resolver contra `entregables/` |
| Mezcla foto + video en carpeta | ABORTAR — Instagram no soporta carruseles mixtos vía Zapier |

Más de 10 imágenes en una carpeta: ABORTAR y pedir al usuario que elija o divida.

---

## Pipeline de publicación

### Paso 1 — Validación local

- Confirmar que el archivo existe y tiene formato soportado.
- Para video: avisar si es horizontal (>aspect ratio 1.0) — IG lo aceptará pero el reel se ve mal.
- Para fotos en carrusel: si tienen tamaños drásticamente distintos, advertir (IG recortará al primero).

### Paso 2 — Push a GitHub assets repo

1. Crear carpeta destino: `.ig-assets-repo/posts/YYYY-MM-DD-<slug-corto>/`
   - `slug-corto` = primeros 4 palabras del caption pasadas a kebab-case, o `untitled` si no hay caption.
2. Copiar archivo(s) al destino. Renombrar a:
   - Foto única: `image.<ext>`
   - Video: `video.<ext>`
   - Carrusel: `slide-01.<ext>`, `slide-02.<ext>`, ... (con padding para mantener orden)
3. `cd` al repo y ejecutar:
   ```bash
   git add -A
   git commit -m "publish: <YYYY-MM-DD> <slug>"
   git push
   ```
4. Esperar ~3 segundos para que GitHub propague el commit en raw.githubusercontent.

### Paso 3 — Construir URLs raw

Patrón:
```
https://raw.githubusercontent.com/<TU-USUARIO-GITHUB>/ig-assets/main/posts/YYYY-MM-DD-<slug>/<archivo>
```

Verificar que al menos una URL responde 200 con `curl -I` antes de seguir. Si responde 404,
esperar 5s más y reintentar 1 vez. Si sigue fallando, abortar y reportar.

### Paso 4 — Confirmación con el usuario

Mostrar preview compacto:

```
📸 Listo para publicar en Instagram
─────────────────────────────────
Tipo: Carrusel (4 fotos) | Foto única | Reel
Caption (XXX/2200 chars):
   <caption truncado a 200 chars con "..." si es más largo>
Ubicación: <si la pasó>
Tags: <si los pasó>
Cuenta: <de memoria si existe, "default" si no>
URLs subidas a GitHub: ✅ <N> archivos accesibles
─────────────────────────────────
¿Publico? (sí / cancela)
```

NUNCA publicar sin un "sí", "publica", "ya", "dale" explícito.

### Paso 5 — Llamada a Zapier

**Para fotos / carrusel:**
```
mcp__Zapier-MCP__execute_zapier_write_action(
  app="Instagram for Business",
  action="publish_media_v2",
  instructions="Publicar las imágenes en mi cuenta de Instagram for Business default",
  output="post URL, post ID, and any error messages",
  params={
    "media": [<lista de 1-10 URLs raw.githubusercontent>],
    "caption": "<caption>",
    "instagramPageId": "<valor de memoria si existe, omitir si no>",
    # opcionales
    "location": "<ubicacion>",
    "tagged_users": ["<@usr1>", "<@usr2>"]
  })
```

**Para video / reel:**
```
mcp__Zapier-MCP__execute_zapier_write_action(
  app="Instagram for Business",
  action="publish_video",
  instructions="Publicar el video como reel en mi cuenta de Instagram for Business default",
  output="post URL, post ID, and any error messages",
  params={
    "video": "<URL raw>",
    "caption": "<caption>",
    "instagramPageId": "<...>",
    "location": "<...>",
    "tagged_users": [...]
  })
```

### Paso 6 — Reporte

Si éxito:
```
✅ Publicado en Instagram
URL: https://www.instagram.com/p/XXXX
Caption: <primeros 80 chars>...
Assets: https://github.com/<TU-USUARIO-GITHUB>/ig-assets/tree/main/posts/<fecha>-<slug>
```

Si falla:
- Mostrar el error textual de Zapier sin maquillar.
- Errores comunes y qué hacer:
  - "Account not Business" → el usuario debe convertir su cuenta y vincularla a Facebook Page.
  - "Media URL invalid" → revisar que las URLs sean accesibles (probar con `curl -I`).
  - "instagramPageId required and ambiguous" → pedirle al usuario que elija de la lista que devolvió Zapier y guardar en memoria.
  - "Caption too long" → mostrar conteo y pedir versión recortada.
- NO reintentar automáticamente. Reportar y esperar instrucciones.

---

## Reglas de caption

- **Idioma:** español neutro (NO argentino). Aplicar feedback registrado en memoria
  (tabla de tuteo): vos→tú, tenés→tienes, copiá→copia, acá→aquí, etc.
- **Máximo 2,200 caracteres.** Si excede, mostrar conteo y pedir versión recortada.
- **Si el usuario no pasó caption:** ofrecer 3 opciones:
  1. Generar uno basado en el contenido (si es output de otra skill como
     `carrusel-render-formula100k` o `infografia-reel-formula100k`, leer el caption
     sugerido del .md adjunto).
  2. Que el usuario escriba uno.
  3. Publicar sin caption (vacío).

---

## Casos compuestos comunes

### El usuario acaba de generar un carrusel con `carrusel-render-formula100k`

Esa skill deja los slides en `entregables/carruseles/<tema>/`. El usuario puede decir
"publícalo" y resolvemos:
- Carpeta: la última modificada en `entregables/carruseles/`
- Caption: leer `caption.md` o `README.md` dentro de esa carpeta si existe
- Si no existe caption.md, ofrecer las 3 opciones de arriba

### El usuario acaba de generar un reel con `infografia-reel-formula100k`

Esa skill deja un `.mp4` en `entregables/infografias/`. Mismo flujo, modo video.

### El usuario pasa una URL de YouTube o de algo descargable

NO descargamos automáticamente. Decirle: "Esto es una URL de YouTube, no de imagen.
Si quieres publicar el video, primero descárgalo o pásame la ruta local del .mp4".

---

## Reglas inquebrantables

1. **Confirmación explícita siempre.** Cero publicaciones automáticas.
2. **No tocar el repo formula100k-ig-assets si no es para publicar.** No es un dump general.
3. **El repo debe seguir público.** Si alguien lo cambia a privado, las URLs se rompen
   inmediatamente (las publicaciones ya hechas siguen vivas porque Instagram hace su propia
   copia, pero futuras llamadas fallarán).
4. **Nunca publicar contenido que esté en `cerebro/`, en una carpeta `PRIVADO/` o cualquier subcarpeta
   con `.private`** — abortar y avisar.
5. **Span de tiempo entre commit y publicación de Zapier:** mínimo 3s para que GitHub propague.
6. **Cuenta target:** usar siempre la cuenta guardada en memoria. Si el usuario quiere publicar
   en otra cuenta (ej: comunidad o cliente), debe pasarla explícitamente con `--cuenta=`.
