# 🌿 Touch the Grass

**Skill de reconexión personal para cuando llevas semanas sin parar.**

Touch the Grass te ayuda a planear y completar actividades que bajan la dopamina y te reconectan con el mundo analógico. Se activa cuando mencionas estrés, agotamiento o burnout, y también te recuerda diariamente que el pasto sigue ahí esperándote.

---

## ✨ Qué hace

- **Detecta tu estado** — cuando dices que estás quemado, agotado o necesitas desconectarte, arranca automáticamente
- **Sugiere actividades** según la hora del día (outdoor por la mañana, analógicas por la noche)
- **Agenda en Google Calendar** — crea eventos con recordatorios para que no se te olvide tocar el pasto
- **Sistema de puntos y rachas** — confirma actividades por texto (+1), foto (+2) o post en redes (+3)
- **Verificación visual** — analiza fotos para validar que realmente saliste de la cueva
- **Recordatorio diario** — un heartbeat matutino que te pregunta si ya planeaste tu momento de reconexión

---

## 📂 Estructura

```
touch-the-grass/
├── SKILL.md           # Definición completa del skill (flujos, reglas, setup)
├── activities.json    # Catálogo de actividades con categorías y puntuación
└── README.md
```

---

## 🏷️ Categorías de actividades

| Categoría | Emoji | Ejemplos |
|-----------|-------|----------|
| **Al aire libre** | 🌿 | Caminar sin teléfono, grounding descalzo, bici, ir al parque |
| **Mindfulness** | 🧘 | Meditar, respiración 4-7-8, journaling a mano, estiramientos |
| **Analógico** | 📖 | Leer libro físico, dibujar, cocinar desde cero, rompecabezas |
| **Social real** | 👥 | Café con alguien en persona, llamar a familia, un abrazo largo |
| **Pasivo con intención** | 🎬 | Ver una película sin scroll, escuchar un álbum completo, siesta |

---

## ⭐ Sistema de puntos

| Confirmación | Puntos |
|-------------|--------|
| 💬 Solo texto | +1 |
| 📸 Foto verificada | +2 |
| 🌐 Post en redes | +3 |

### Bonos de racha

| Racha | Bonus |
|-------|-------|
| 🔥 3 días seguidos | +5 pts |
| 🔥 7 días seguidos | +15 pts |
| 🔥 14 días seguidos | +30 pts |

---

## 🚀 Setup

Hay dos formas de configurar el recordatorio diario:

### Opción A — Cron dedicado *(recomendada)*

```bash
openclaw cron add \
  --name "touch-the-grass-daily" \
  --cron "0 9 * * *" \
  --tz "America/Mexico_City" \
  --session isolated \
  --message "Heartbeat Touch the Grass: revisa si el usuario tiene actividades TTG planeadas para hoy." \
  --announce
```

Verifica con `openclaw cron list`.

### Opción B — Heartbeat

Agrega esto a `~/.openclaw/workspace/HEARTBEAT.md`:

```
- Touch the Grass: una vez al día en la mañana, revisa si el usuario tiene actividades planeadas.
  Si no las tiene y aún no le preguntaste hoy, hazlo con amabilidad.
  Si lleva 3+ días sin actividad completada, menciónalo brevemente.
```

---

## 💬 Frases que lo activan

- *"llevo 3 semanas sin parar, estoy quemado"*
- *"touch the grass"*
- *"necesito desconectarme"*
- *"¿qué tengo de touch the grass hoy?"*
- *"ya fui a caminar"* → inicia verificación
- *"muéstrame mi score"*

---

## 🧩 Requisitos

- OpenClaw con Google Calendar habilitado (`gcal.enabled`)
- Zona horaria: `America/Mexico_City` (UTC-6)

---

## 🌱 Filosofía

> Ni coach de vida ni robot. Como un amigo que te conoce.

- Tono cálido y directo, sin sermones
- Si no puedes hoy, está bien — sin culpa
- Las fotos se analizan solo para verificar, nunca se comentan aspectos personales
- El objetivo es motivar, no policiar
