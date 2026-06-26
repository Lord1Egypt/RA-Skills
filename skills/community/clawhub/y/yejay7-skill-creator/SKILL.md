---
name: openclaw-skill-creator
description: Crea skills para OpenClaw con el formato correcto. YAML frontmatter, _meta.json, estructura de archivos. Publicar en ClawHub es opcional.
---

# OpenClaw Skill Creator

Este skill proporciona instrucciones completas para **crear skills en OpenClaw** con el formato correcto desde el primer intento. Los skills se guardan localmente en tu workspace.

**Publicar en ClawHub es opcional.**

---

## 🎯 **Cuándo Usar Este Skill**

Usa este skill cuando el usuario quiera:

- **Crear un skill nuevo para OpenClaw** (función principal)
- Guardar un skill en el panel local de skills
- Corregir el formato de un skill mal estructurado
- Aprender la estructura correcta de un skill
- Publicar un skill en ClawHub (opcional)

---

## 📁 **Estructura de Archivos Requerida**

Un skill de ClawHub debe tener esta estructura mínima:

```
nombre-del-skill/
├── SKILL.md          # Obligatorio - Documentación del skill
└── _meta.json        # Obligatorio - Metadatos del skill
```

**Archivos opcionales:**
```
nombre-del-skill/
├── README.md         # Documentación adicional
├── scripts/          # Scripts ejecutables
├── references/       # Referencias y ejemplos
└── assets/           # Recursos adicionales
```

---

## 📝 **Formato Correcto de SKILL.md**

### **YAML Frontmatter (OBLIGATORIO)**

El archivo `SKILL.md` **DEBE** comenzar con YAML frontmatter en este formato exacto:

```yaml
---
name: nombre-del-skill
description: Descripción clara y concisa del skill (máx 160 caracteres)
---
```

**Campos requeridos:**
- `name`: Nombre del skill (kebab-case, sin espacios, minúsculas)
- `description`: Descripción breve (aparece en ClawHub search)

**Ejemplo real:**
```yaml
---
name: lossless-claw-skill
description: Wrapper seguro para el plugin lossless-claw (LCM). Proporciona interfaz para lcm_grep, lcm_describe, lcm_expand_query.
---
```

### **Contenido del SKILL.md**

Después del frontmatter, incluye:

```markdown
# Nombre del Skill

Descripción extendida del propósito del skill.

---

## Descripción

Explicación detallada de qué hace el skill y por qué es útil.

## Cuándo Usar Este Skill

Lista de casos de uso específicos:

- Cuando el usuario necesita X
- Cuando ocurre Y
- Para resolver Z

## Cómo Usar

Instrucciones paso a paso o ejemplos de comandos.

## Ejemplos

```bash
npx clawhub install nombre-del-skill
```

## Notas Adicionales

Información extra, advertencias, o referencias.
```

---

## 📋 **Formato de _meta.json**

El archivo `_meta.json` debe tener esta estructura:

```json
{
  "name": "nombre-del-skill",
  "description": "Descripción clara y concisa del skill",
  "version": "1.0.0",
  "tags": ["categoria", "utilidad", "feature"]
}
```

**Campos requeridos:**
- `name`: Mismo nombre que en el YAML frontmatter
- `description`: Misma descripción que en el YAML frontmatter
- `version`: Versión semántica (recomendado: "1.0.0" para inicio)
- `tags`: Array de tags para búsqueda (mínimo 1, máximo 5)

**Ejemplo real:**
```json
{
  "name": "lossless-claw-skill",
  "description": "Wrapper seguro para el plugin lossless-claw (LCM). Proporciona interfaz para lcm_grep, lcm_describe, lcm_expand_query.",
  "version": "1.0.0",
  "tags": ["latest", "lcm", "memory", "context"]
}
```

---

## 🚀 **Proceso de Creación de Skills (LOCAL)**

### **Paso 1: Crear el Skill**

El skill se creará automáticamente en:
```
/mnt/data/openclaw/workspace/.openclaw/workspace/skills/nombre-del-skill/
```

**Estructura:**
```
nombre-del-skill/
├── SKILL.md       # Con YAML frontmatter correcto
└── _meta.json     # Metadatos del skill
```

### **Paso 2: Verificar Formato**

Antes de usar el skill, verifica:

- [ ] `SKILL.md` tiene YAML frontmatter (`---` al inicio y fin)
- [ ] `name` en YAML coincide con `name` en `_meta.json`
- [ ] `description` en YAML coincide con `description` en `_meta.json`
- [ ] El nombre usa kebab-case (guiones, sin espacios)
- [ ] `_meta.json` es JSON válido

### **Paso 3: Reiniciar Gateway (si es necesario)**

Para que OpenClaw cargue el nuevo skill:

```bash
openclaw gateway restart
```

O usa el comando desde OpenClaw:
```
/gateway restart
```

### **Paso 4: ¡Listo! El skill está disponible**

El skill ahora está en tu panel local y puede ser usado por tu agente.

---

## 🌐 **Publicar en ClawHub (OPCIONAL)**

Si quieres compartir tu skill con la comunidad:

### **Paso A: Autenticar CLI de ClawHub**

```bash
npx clawhub login
# Navegar a la URL que aparece en el output
```

**Nota:** Cuenta de GitHub debe tener **más de 14 días de antigüedad**.

### **Paso B: Publicar**

```bash
npx clawhub publish /mnt/data/openclaw/workspace/.openclaw/workspace/skills/nombre-del-skill \
  --slug nombre-del-skill \
  --name "Nombre del Skill" \
  --version 1.0.0 \
  --tags "tag1,tag2,tag3"
```

### **Paso C: Verificar**

```
✔ OK. Published nombre-del-skill@1.0.0 (ID)
URL: https://clawhub.ai/{ID}/{slug}
```

---

## ⚠️ **Errores Comunes y Soluciones**

### **Error 1: "Path must be a folder"**

**Causa:** La ruta no es absoluta o la carpeta no existe.

**Solución:**
```bash
# Usar ruta absoluta completa
npx clawhub publish /mnt/data/openclaw/workspace/.openclaw/workspace/skills/nombre-del-skill
```

### **Error 2: "Not logged in. Run: clawhub login"**

**Causa:** La CLI no está autenticada.

**Solución:**
```bash
npx clawhub login
# Navegar a la URL que aparece en el output
```

### **Error 3: "GitHub API rate limit exceeded"**

**Causa:** Límite temporal de API de GitHub.

**Solución:** Esperar 30-60 segundos y reintentar.

### **Error 4: "GitHub account must be at least 14 days old"**

**Causa:** La cuenta de GitHub fue creada recientemente.

**Solución:** Usar una cuenta de GitHub con más de 14 días de antigüedad.

### **Error 5: Skill no aparece en ClawHub panel después de instalar**

**Causa:** Formato incorrecto de YAML frontmatter.

**Solución:** Verificar que el frontmatter sea exactamente:
```yaml
---
name: nombre-del-skill
description: Descripción del skill
---
```

**NO usar este formato incorrecto:**
```yaml
# ❌ INCORRECTO - Muy complejo
name: skill-name
description: ...
author: ...
version: ...
```

---

## 📚 **Ejemplos de Skills Reales**

### **Ejemplo 1: Skill Simple (Wrapper)**

**SKILL.md:**
```yaml
---
name: lossless-claw-skill
description: Wrapper seguro para el plugin lossless-claw (LCM).
---

# Lossless Claw Skill

Skill wrapper para el plugin lossless-claw de OpenClaw.

## Descripción

Proporciona una interfaz segura para las herramientas LCM.

## Cuándo Usar

- Cuando necesitas buscar en el historial de conversación
- Cuando necesitas expandir resúmenes compactados
- Para queries complejas de memoria
```

**_meta.json:**
```json
{
  "name": "lossless-claw-skill",
  "description": "Wrapper seguro para el plugin lossless-claw (LCM).",
  "version": "1.0.0",
  "tags": ["latest", "lcm", "memory"]
}
```

### **Ejemplo 2: Skill con Scripts**

**SKILL.md:**
```yaml
---
name: weather-skill
description: Obtén el clima actual y pronósticos vía wttr.in o Open-Meteo.
---

# Weather Skill

Obtén información meteorológica para cualquier ubicación.

## Cuándo Usar

- Cuando el usuario pregunta sobre el clima
- Para pronósticos de 1-7 días
- Para temperaturas actuales

## Comandos

```bash
curl wttr.in/Ciudad
```
```

**_meta.json:**
```json
{
  "name": "weather-skill",
  "description": "Obtén el clima actual y pronósticos vía wttr.in o Open-Meteo.",
  "version": "1.0.0",
  "tags": ["weather", "forecast", "utility"]
}
```

---

## 🎓 **Checklist de Creación de Skill (LOCAL)**

Antes de usar el skill, verifica:

- [ ] **Estructura de archivos**
  - [ ] `SKILL.md` existe
  - [ ] `_meta.json` existe
  - [ ] Ambos están en la misma carpeta: `skills/nombre-del-skill/`

- [ ] **YAML Frontmatter**
  - [ ] Comienza con `---`
  - [ ] Tiene campo `name`
  - [ ] Tiene campo `description`
  - [ ] Termina con `---`
  - [ ] No hay campos innecesarios

- [ ] **_meta.json**
  - [ ] Es JSON válido
  - [ ] Tiene campo `name` (mismo que YAML)
  - [ ] Tiene campo `description` (mismo que YAML)
  - [ ] Tiene campo `version`
  - [ ] Tiene campo `tags` (array)

- [ ] **Gateway Reiniciado** (si OpenClaw no detecta el skill)
  - [ ] `openclaw gateway restart` ejecutado
  - [ ] Skill aparece en el panel después del restart

---

## 🌐 **Checklist Adicional para Publicar en ClawHub (OPCIONAL)**

Solo si quieres publicar en ClawHub:

- [ ] **CLI Autenticada**
  - [ ] `npx clawhub login` ejecutado
  - [ ] URL de auth navegada en browser
  - [ ] Mensaje "OK. Logged in as @usuario" apareció

- [ ] **Cuenta GitHub**
  - [ ] Cuenta tiene más de 14 días de antigüedad
  - [ ] No hay rate limit activo (esperar 60s si hay error)

- [ ] **Slug Disponible**
  - [ ] El slug no está tomado por otro skill
  - [ ] Si está tomado, usa una variación única

---

## 🔗 **Recursos Adicionales**

- **ClawHub:** https://clawhub.ai
- **Documentación OpenClaw:** https://docs.openclaw.ai
- **Skills existentes:** https://clawhub.ai/skills
- **GitHub:** https://github.com/openclaw/openclaw

---

## 💡 **Consejos Profesionales**

### **Para Creación Local:**

1. **Mantén el frontmatter simple** - Solo `name` y `description` son requeridos
2. **Usa kebab-case** - `nombre-del-skill`, no `NombreDelSkill` ni `nombre_del_skill`
3. **Descripciones claras** - Máximo 160 caracteres, explica qué hace el skill
4. **Tags relevantes** - Usa 3-5 tags que describan la funcionalidad
5. **Versiona correctamente** - Empieza en 1.0.0, usa semver para updates
6. **Prueba localmente** - Verifica que el skill funcione antes de usarlo
7. **Documenta bien** - Un SKILL.md claro ayuda a tu agente a usar el skill
8. **Reinicia el gateway** - Después de crear un skill, reinicia para que OpenClaw lo detecte

### **Para Publicación en ClawHub (Opcional):**

9. **Verifica slug disponible** - Busca en ClawHub antes de publicar
10. **Cuenta con 14+ días** - GitHub requiere antigüedad mínima
11. **Espera rate limits** - Si hay error, espera 60s y reintenta

---

## 📌 **Nota Importante**

**Este skill está diseñado para:**
1. ✅ **Crear skills localmente** (función principal)
2. ✅ **Guardar en tu panel de skills** de OpenClaw
3. ⭐ **Publicar en ClawHub** (opcional, para compartir con la comunidad)

**No necesitas publicar en ClawHub** para que tu skill funcione. Los skills locales son completamente funcionales y tu agente puede usarlos inmediatamente después de crearlos y reiniciar el gateway.

---

**Creado con ❤️ para la comunidad OpenClaw**
