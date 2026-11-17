---
name: roadmap-producto-f100k
description: "Construye el ROADMAP de un programa, curso, comunidad, servicio o producto físico con Backward Design (ingeniería inversa desde la promesa final). Diseña el viaje del cliente — punto A a punto B — en fases con objetivos y entregables medibles. Soporta 4 tipos: digital (curso), comunidad (Skool), servicio (consultoría/coaching 1:1) y producto físico. Activar SIEMPRE que se pida 'hazme un roadmap', 'arma el roadmap de mi curso', 'diseña el paso a paso de mi programa', 'metodología de mi formación', 'cómo estructuro mi curso', 'fases de mi comunidad', 'arquitectura de mi programa', 'ingeniería inversa de mi promesa', 'backward design', 'estructura mi mentoría/consultoría', 'onboarding de mi producto físico', o cualquier variación de estructurar el VIAJE/CONTENIDO del producto. NO usar para la OFERTA de venta (constructor-ofertas-f100k), copy de venta (vsl-expert-f100k) ni calendarios de contenido (calendarizador-contenido-formula100k). Es el paso PREVIO a constructor-ofertas-f100k."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Genera los `.md` del paquete en `entregables/roadmaps/`. El `.docx` y el `.html` solo si el servidor tiene cómo producirlos (python-docx); si no, entrega los `.md` y dilo.
> - El «espejo al segundo cerebro» aquí es copiar los `.md` a `cerebro/roadmaps/` y sumarlos a `cerebro/INDICE.md`.
> - Entrega por Telegram: resumen del roadmap en el chat y los archivos como documentos.

---

## Qué hace esta skill

Diseña la **arquitectura del viaje del cliente** dentro de un producto: desde su punto A (situación actual) hasta su punto B (promesa cumplida), dividido en fases con objetivos, actividades y entregables medibles.

**El output tiene 2 caras (ambas obligatorias) entregadas en 4 archivos:**

| Cara | Foco | A quién le sirve |
|---|---|---|
| **A. Roadmap del CLIENTE** | El viaje que el cliente recorre (fases, objetivos, actividades, entregables que el cliente produce) | Lo que se muestra en la landing / VSL / About Page |
| **B. Plan de PRODUCCIÓN del CREADOR** | El paso a paso para MONTAR el producto: qué grabar, qué construir, qué sistemas armar, qué materiales preparar, qué orden seguir | La hoja de ruta operativa del usuario para que el producto exista |

Las 2 caras se consolidan en **un Plan Maestro** que incluye además el **stack de oferta** (precio, bonos, garantía, valor declarado), una **proyección financiera** a 90 días, y un **mapa de riesgos**. El Plan Maestro se entrega en 3 formatos: `.md` (fuente), `.docx` (Word para compartir), y `.html` (presentación de impacto para pitch).

**Principio base:** todo roadmap nace de **ingeniería inversa desde la promesa final**. No se empieza pensando en módulos — se empieza pensando en el resultado final y se desanda el camino hasta el punto cero.

> "Un roadmap NO es una lista de tareas. Es la arquitectura del viaje de tu alumno desde su punto A hasta su punto B."

Después de entregar las 2 caras del roadmap, la skill **enlaza automáticamente** con la siguiente:
- → [[constructor-ofertas-f100k]] para construir el stack de oferta encima del roadmap
- → [[creadora-comunidades-skool]] cuando el producto es comunidad Skool (estructura completa: vehículo único, onboarding, posts fijados, leaderboard, About Page)

Trabaja en español neutro (NO argentino — [[feedback_espanol_neutro]]). Tono directo, estratégico, orientado a resultado medible.

---

## Cuándo usar esta skill vs. otras

| Caso | Skill correcta |
|---|---|
| "Cómo estructuro mi curso / qué módulos pongo" | **Esta skill** (roadmap-producto-f100k) |
| "Qué incluyo en mi oferta, qué bonos, qué precio" | [[constructor-ofertas-f100k]] |
| "Cómo escribo el copy de venta" | [[vsl-expert-f100k]] |
| "Cómo construyo la comunidad Skool entera" | [[creadora-comunidades-skool]] (incluye vehículo único + estructura completa) |
| "Cómo programo mis publicaciones de la semana" | [[calendarizador-contenido-formula100k]] |

**Flujo natural:** roadmap (esta skill) → oferta → VSL → audios de cierre.

---

## Los 4 elementos clave de todo roadmap

Sin estos 4 elementos, no es un roadmap — es una lista de tareas.

| # | Elemento | Qué debe definir |
|---|---|---|
| 1 | **Duración y dirección** | Cuánto dura todo el programa y cuánto dura cada fase. Da validez al recorrido. |
| 2 | **Progresividad** | Cada fase desbloquea la siguiente. No se puede saltar pasos. |
| 3 | **Ritmo de avance** | Tareas diarias/semanales claras según el tiempo que el cliente puede dedicar. |
| 4 | **Soporte** | Cómo el cliente recibe acompañamiento durante el recorrido. |

---

## Anatomía completa del roadmap (6 capas, en orden)

### 1. Punto A — Situación actual
Dónde está el cliente HOY antes de empezar. Estado externo + estado interno.

### 2. Punto B — Transformación / promesa
Resultado prometido en X tiempo. Debe ser específico, medible y emocional.

### 3. Fases
3-6 hitos macro que dividen el viaje. Cada fase es un capítulo con identidad propia (nombre + duración + propósito).

### 4. Objetivos por fase
Mínimo 1 objetivo principal por fase. Define QUÉ logra el cliente al terminar esa fase.

### 5. Actividades por objetivo
Las acciones concretas y medibles que el cliente realiza para cumplir cada objetivo.

### 6. Entregables por actividad
Lo que el cliente PRODUCE como evidencia tangible de haber completado la actividad (documento, plantilla rellena, audit, post publicado, primer cliente, etc.).

---

## Backward Design — la metodología base (3 pasos)

Esta skill aplica **diseño inverso** siempre, en este orden:

### Paso 1 — Identifica el resultado deseado
Empieza por el FINAL: ¿qué exactamente puede hacer / tener / ser el cliente al terminar?

### Paso 2 — Determina las evidencias aceptables
¿Qué tendría que producir / demostrar para que sepamos que SÍ logró ese resultado? Estas son las pistas para los entregables.

### Paso 3 — Planea la experiencia de aprendizaje
Solo AHORA — y nunca antes — diseña las actividades, módulos, sesiones, contenidos que llevan a esas evidencias.

**Regla absoluta:** nunca empezar por "qué módulos pongo". Siempre empezar por "qué resultado quiero al final".

---

## Adaptación según el tipo de producto

La skill detecta automáticamente el tipo según el brief y adapta la estructura del roadmap.

### A) Producto digital (curso / formación / mentoría grupal)
- **Unidad de avance:** módulo o lección
- **Duración típica:** 4-12 semanas
- **Entregables:** plantillas rellenas, ejercicios completados, casos de aplicación
- **Soporte:** sesiones en vivo grupales + foro
- **Fase final típica:** "implementación + primer resultado medible"

### B) Comunidad (Skool / membresía recurrente)
- **Unidad de avance:** hito desbloqueable (no módulo lineal — la comunidad permite re-entrada)
- **Duración típica:** ciclos de 30/60/90 días que se pueden repetir
- **Entregables:** posts en foro, casos publicados, retos cumplidos
- **Soporte:** sesiones semanales + comunidad activa + foro
- **Conexión:** SIEMPRE derivar a [[creadora-comunidades-skool]] después del roadmap para configurar onboarding, posts fijados, leaderboard
- **Fase final típica:** "graduación" o "siguiente nivel" (retención)

### C) Servicio (consultoría / coaching 1:1 / high ticket)
- **Unidad de avance:** sesión 1:1 o sprint
- **Duración típica:** 4-16 semanas
- **Entregables:** auditorías, planes personalizados, implementaciones acompañadas
- **Soporte:** sesiones 1:1 + WhatsApp/Slack directo
- **Fase final típica:** "autonomía / cierre con resultado validado"

### D) Producto físico (e-commerce / kit / device)
- **Unidad de avance:** etapa de uso del producto (no aprendizaje, sino experiencia)
- **Duración típica:** depende del producto (7 días para consumibles, 30-90 para devices)
- **Entregables:** uso correcto del producto, hábito instalado, resultado físico observable
- **Soporte:** guía de uso + onboarding por email/WhatsApp + comunidad opcional
- **Fase final típica:** "recompra / referido / siguiente producto en la escalera"

---

## Brief obligatorio (preguntas una por una)

**NO escribir ningún roadmap sin completar este brief.** Hacer las preguntas UNA por UNA. Esperar respuesta antes de pasar a la siguiente.

### Bloque 1 — Promesa (Backward Design paso 1)
1. ¿Qué resultado final exacto promete tu producto? (debe ser medible)
2. ¿En cuánto tiempo el cliente llega a ese resultado?
3. ¿Cuál es el tipo de producto? (digital · comunidad · servicio · producto físico)

### Bloque 2 — Cliente
4. ¿En qué punto exacto está el cliente HOY antes de empezar? (nivel cero — qué sabe / qué no sabe / qué ya intentó)
5. ¿Cuánto tiempo a la semana puede dedicarle realísticamente?

### Bloque 3 — Evidencias (Backward Design paso 2)
6. ¿Qué cosas concretas tendría que SABER HACER / TENER / DEMOSTRAR el cliente al final para que tú digas "lo logró"?

### Bloque 4 — Soporte
7. ¿Qué tipo de acompañamiento ofreces? (sesiones en vivo, 1:1, foro, comunidad, WhatsApp, ninguno)
8. ¿Tienes un equipo/asistente o eres tú sola atendiendo?

### Bloque 5 — Tono y energía
9. ¿Cómo quieres que se sienta el recorrido? (académico · vivencial · práctico · espiritual · aventurero · militar/disciplina · híbrido)

Después del brief, **confirmar con un resumen y preguntar "¿Continúo?"** antes de generar.

---

## Proceso de generación (orden obligatorio)

### CARA A — Roadmap del cliente
1. **Backward Design paso 1:** anclar el resultado final
2. **Backward Design paso 2:** listar las 5-10 evidencias finales
3. **Backward Design paso 3:** agrupar las evidencias en 3-6 fases lógicas
4. **Nombrar cada fase** con identidad (verbo + tema, ej: "Fundamentos del Pescador" o "Construye tu Oferta")
5. **Asignar duración** a cada fase (todas suman = duración total prometida)
6. **Definir 1 objetivo principal** por fase (medible)
7. **Listar actividades** que llevan al objetivo
8. **Definir entregable** por actividad
9. **Validar progresividad:** ¿la fase N depende de haber completado fase N-1?
10. **Validar promesa:** ¿al terminar todas las fases, el cliente CUMPLE el resultado prometido?

### CARA B — Plan de producción del creador
Para cada fase del roadmap del cliente, traducir a tareas de MONTAJE concretas:

11. **Materiales a producir** — qué módulos grabar, qué PDFs escribir, qué plantillas armar, qué workbooks construir
12. **Sesiones a planear** — qué sesiones en vivo dictar, agenda + duración + entregable
13. **Sistemas a montar** — qué automatizaciones, qué cuentas, qué plataformas, qué accesos preparar
14. **Recursos físicos** (si aplica) — qué productos fabricar/empaquetar, qué insumos comprar, qué proveedor contactar
15. **Métricas de avance** — cómo el CREADOR sabe que cada fase está lista para vender (no la métrica del cliente — la del producto montado)
16. **Orden de montaje** — qué se construye primero, qué se puede paralelizar, qué bloquea a qué
17. **Estimación de tiempo de montaje** — cuánto le toma al creador tener el producto listo (distinto de la duración que el cliente recorre)

### Construcción del Plan Maestro (paso obligatorio)

Después de tener las 2 caras del roadmap, **NO TERMINAR ahí**. Construir el Plan Maestro integrado:

18. **Stack de oferta** — construir directamente (no derivar a `constructor-ofertas-f100k` salvo que el usuario lo pida explícitamente). Incluir:
    - Estructura de planes (FREE/PRO/Premium, o tier único + variantes)
    - Valor stack visible (lista de componentes con precio individual sumando 5-10x el precio real)
    - Bonos de lanzamiento (3-5, con fecha límite o stock)
    - Garantía explícita (siempre — cerrar fricción)
    - Urgencia y escasez (founder lock, beta limitada, aumento programado)
    - Ladder con el portafolio del cliente
19. **Proyección financiera** — escenario conservador + optimista a 90 días con MRR/ARR + supuestos explícitos
20. **Mapa de riesgos + mitigaciones** — mínimo 5 riesgos con su mitigación concreta
21. **Próximos pasos accionables** — tabla con plazo + acción + responsable

### Entrega multi-formato

22. Generar `00-ROADMAP-ORIGINAL.md` (las 2 caras puras)
23. Generar `01-PLAN-MAESTRO.md` (consolidado: implementación + servicio + oferta + proyección + riesgos)
24. Correr `pandoc 01-PLAN-MAESTRO.md -o 01-PLAN-MAESTRO.docx --from markdown --to docx --toc --toc-depth=2 --metadata title="<Producto> — Plan Maestro"`
25. Generar `02-PRESENTACION-IMPACTO.html` autocontenido siguiendo la convención visual definida arriba (paleta oscura del producto, gradientes, números enormes, secciones con respiro)
26. Espejar `.md` + `.docx` a `cerebro/roadmaps/<carpeta>/`
27. Abrir el `.docx` y el `.html` con `open`

### Enlace con otras skills (al final)
- Si tipo = comunidad Skool → ofrecer pasar a [[creadora-comunidades-skool]] para vehículo único, onboarding, posts fijados, leaderboard, About Page
- Si el usuario quiere **profundizar** el stack de oferta (más allá del que ya generaste en el Plan Maestro) → [[constructor-ofertas-f100k]]
- Si quiere visualizarlo como artifact interactivo para alumnos → [[generador-artifact-educativo-formula100k]]
- Si quiere reescribir el VSL → [[vsl-expert-f100k]]

---

## Reglas absolutas

- **Siempre Backward Design** — nunca empezar por módulos
- **Siempre brief completo** antes de generar
- **Mínimo 3 fases, máximo 6** — menos es difuso, más es abrumador
- **Cada fase debe tener identidad propia** (nombre con personalidad, no "Módulo 1")
- **Cada actividad debe tener UN entregable** (sin entregable, no es actividad — es lectura)
- **Las fases deben ser progresivas** — no aleatorias
- **La suma de las duraciones de fases = duración total prometida** — sin excepción
- **El último entregable debe ser la prueba pública del resultado** (no solo aprendizaje interno)
- **Adaptar al tipo de producto** (digital/comunidad/servicio/físico) — no usar el mismo template para todo
- **Español neutro siempre** — ver [[feedback_espanol_neutro]]
- **Nunca inventar duraciones** — si el usuario dice 90 días, son 90 días, no 120

---

## Plantillas

Las plantillas completas por tipo de producto (digital, comunidad, servicio, físico) están en [templates.md](templates.md). Cada una incluye:
- Estructura de fases sugerida por tipo
- Ejemplos reales (F100K, comunidad de pesca, consultoría)
- Tabla maestra de entrega
- Variaciones de ritmo (intensivo / estándar / suave)

---

## Output

El output es un **paquete entregable de 4 archivos en una carpeta dedicada**, no un solo `.md`. Esto permite usar cada formato según el contexto: editar en Markdown, compartir en Word, presentar en navegador.

```
entregables/roadmaps/YYYY-MM-DD_<slug>-paquete-entregable/
├── 00-ROADMAP-ORIGINAL.md          ← Backward Design + Cara A + Cara B (técnico, fuente)
├── 01-PLAN-MAESTRO.md              ← Plan de implementación + Entrega de servicio + Stack de oferta (fuente .md del .docx)
├── 01-PLAN-MAESTRO.docx            ← Word generado con pandoc desde el .md anterior
└── 02-PRESENTACION-IMPACTO.html    ← Deck scrolleable autocontenido para venta/pitch
```

### Por qué 4 archivos y no 1

| Archivo | Uso | Audiencia |
|---|---|---|
| `00-ROADMAP-ORIGINAL.md` | Documento técnico de trabajo. Backward Design, fases, dependencias. | Equipo interno (el usuario + dev + equipo) |
| `01-PLAN-MAESTRO.md/.docx` | Plan ejecutivo consolidado. Implementación + servicio + oferta + proyección + riesgos. | Stakeholders, inversores, partners. Para mandar por mail o imprimir. |
| `02-PRESENTACION-IMPACTO.html` | Deck visual de pitch. Hero por sección, métricas grandes, paleta del producto, comparativa visual contra competencia. | Venta · presentación pública · landing previa |

### Reglas de generación

1. **Generar PRIMERO** `00-ROADMAP-ORIGINAL.md` con las 2 caras (Backward Design + cliente + creador) — es la fuente de verdad
2. **Expandir** a `01-PLAN-MAESTRO.md` consolidando:
   - Plan de implementación (Cara B expandida)
   - Entrega de servicio (Cara A expandida)
   - **Stack de oferta** (precio, bonos, garantía, urgencia, valor declarado) — pieza nueva, NO está en el roadmap original
   - Proyección financiera (conservador/optimista a 90 días)
   - Mapa de riesgos + mitigaciones
   - Próximos pasos accionables con plazos
3. **Convertir** `.md` → `.docx` con pandoc:
   ```bash
   pandoc 01-PLAN-MAESTRO.md -o 01-PLAN-MAESTRO.docx \
     --from markdown --to docx \
     --toc --toc-depth=2 \
     --metadata title="<Producto> — Plan Maestro"
   ```
4. **Diseñar** `02-PRESENTACION-IMPACTO.html` siguiendo la convención visual ↓
5. **Espejar** los `.md` + `.docx` (no el `.html`) a `cerebro/roadmaps/<carpeta>/`
6. **Abrir automáticamente** el `.docx` y el `.html` al terminar

### Convención visual del HTML de impacto

NO usar la paleta crema de F100K. El HTML de impacto debe tener la identidad visual del PRODUCTO NUEVO (no de F100K), porque presenta el producto al público externo.

Estructura del deck (9 secciones grandes, una por viewport):

1. **Hero** — nombre del producto enorme + tagline + chips de contexto · gradient + blobs de fondo
2. **Problema** — métricas dolor con números enormes (gradient text)
3. **Solución** — flow visual del producto (input → motor → output) + 4 features
4. **Por qué ganamos** — tabla comparativa contra competencia (✓/✗ marcados, producto destacado)
5. **Viaje del cliente** — timeline con dots, fases visuales
6. **Cómo se construye** — grid de fases del plan de producción con números grandes
7. **La oferta** — 3 cards de planes lado a lado · valor stack desglosado · bonos + garantía
8. **Proyección** — 2 cards (conservador vs optimista) con MRR a 90 días en números enormes
9. **Ladder** — cómo el producto alimenta el resto del portafolio (ej: FREE → PRO → F100K → high ticket)
10. **Timeline final** — cuenta regresiva al lanzamiento + decisiones pendientes esta semana
11. **Footer** — nombre producto + tagline + firma del creador

Convenciones técnicas del HTML:
- Single file autocontenido con Tailwind CDN + Google Fonts
- Fuentes: `Space Grotesk` (display/números) + `Inter` (body) + `Caveat` (acentos numerados de sección)
- Paleta oscura como base (`#0F0817` o similar), gradientes violet-magenta-yellow, blobs blur de color
- Glass cards (`backdrop-filter: blur`), `glow` shadows en elementos destacados
- Numbers huge (5xl-9xl) con gradient text para impactar
- Cero scroll lateral, mobile-friendly
- Cada sección "respira" en su propio viewport (`min-h-screen` o `py-32` mínimo)

### Siguiente paso (siempre ofrecer al final)

| Tipo de producto | Siguiente skill recomendada |
|---|---|
| Comunidad Skool | [[creadora-comunidades-skool]] (vehículo único, onboarding, posts fijados, leaderboard, About Page) **+** [[constructor-ofertas-f100k]] (oferta de venta) |
| Producto digital / curso | [[constructor-ofertas-f100k]] (stack + bonos + garantía + precio) |
| Servicio / coaching | [[constructor-ofertas-f100k]] (stack high ticket + garantía condicional) |
| Producto físico | [[constructor-ofertas-f100k]] (oferta de lanzamiento + upsell) |
| Cualquiera, si quiere visualizarlo para alumnos | [[generador-artifact-educativo-formula100k]] (artifact interactivo HTML) |

**Frase de cierre obligatoria** (adaptar al tipo):
> "Listo, ya tienes la arquitectura del producto en sus 2 caras. ¿Pasamos a `constructor-ofertas-f100k` para armar el stack de oferta (bonos, garantía, precio) encima de este roadmap? [Si es comunidad: añadir 'o a `creadora-comunidades-skool` para configurar la comunidad completa']"
