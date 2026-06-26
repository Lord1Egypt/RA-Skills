---
name: touch-the-grass
version: 1.0.0
description: Skill de reconexión personal para semanas agobiantes de trabajo. Úsala cuando el usuario mencione que está estresado, agotado, quemado, necesita descansar, quiere desconectarse del trabajo, o cuando diga frases como "touch the grass", "necesito descansar", "llevo semanas sin parar", "estoy quemado", "burnout". También se activa en el heartbeat diario para recordatorios proactivos de actividades. Gestiona un sistema de actividades para bajar la dopamina, las agrega al Google Calendar del usuario, lleva un score con verificación visual por foto, y mantiene una racha (streak) de días activos.
metadata: {"openclaw":{"emoji":"🌿"}}
---

# Touch the Grass 🌿

Skill de reconexión personal. Ayuda al usuario a planear y completar actividades que bajan la dopamina y reconectan con el mundo analógico después de semanas intensas de trabajo.

## Archivos de referencia
- `{baseDir}/activities.json` — catálogo completo de actividades con puntuación
- El estado del usuario (score, streak, actividades completadas) se guarda en la **memoria del agente**

---

## Flujos principales

### 1. Inicio / Activación manual

Cuando el usuario mencione estrés, agotamiento o quiera reconectarse:

1. Salúdalo con empatía, sin drama. Algo como: *"Llevas un buen rato dándole duro. Hora de tocar el pasto 🌿"*
2. Pregúntale su **estado de ánimo actual del 1 al 5** (1=agotado, 5=bien)
3. Lee `{baseDir}/activities.json` para cargar el catálogo
4. Sugiere **3 actividades concretas** según la hora del día:
   - **Mañana (6-12h)**: prioriza outdoor y mindful
   - **Tarde (12-18h)**: outdoor, analógico, social
   - **Noche (18-23h)**: analógico, pasivo con intención, mindful
5. Pregunta cuáles quiere agendar y para cuándo
6. Crea los eventos en **Google Calendar** con:
   - Título: emoji + nombre de la actividad (ej: `🌿 Caminar 15 min sin teléfono`)
   - Descripción: "Touch the Grass — tiempo para ti. Sin pantallas."
   - Recordatorio: 10 minutos antes
7. Confirma con el usuario y dile su **score actual + streak**

### 2. Heartbeat diario (recordatorio proactivo)

Este flujo corre **una vez al día en la mañana** (configurar en cron a las 9:00 AM hora local).

Revisa en memoria si el usuario tiene actividades Touch the Grass pendientes para hoy:

**Si tiene actividades agendadas hoy:**
> "Buenos días ☀️ Tienes [actividad] agendada para hoy a las [hora]. ¿Listo para tocar el pasto?"

**Si no tiene actividades agendadas:**
> "Hey 👋 ¿Ya planeaste tu momento Touch the Grass para hoy? Tu mente lo necesita. ¿Te ayudo a agendar algo rápido?"

**Si lleva 3+ días sin completar ninguna actividad:**
> "Llevás [N] días sin tocar el pasto 🥀 No te estoy juzgando, pero sí te recuerdo que existe. ¿Qué tal 15 minutos hoy?"

No seas insistente si el usuario ya respondió ese día.

### 3. Registro y verificación de actividad completada

Cuando el usuario diga que completó una actividad:

#### Paso 1 — Verificación
Pregunta cómo quiere confirmarla:
> "¡Genial! ¿Cómo lo confirmamos?"
> - 💬 Solo texto → **+1 punto**
> - 📸 Foto → **+2 puntos** (el agente analiza la imagen)
> - 🌐 Post en redes → **+3 puntos**

#### Paso 2 — Si envía FOTO (verificación con visión)
Analiza la imagen recibida. Verifica que sea plausible para la actividad declarada:

**Criterios de validación visual:**
- ¿La imagen muestra un contexto exterior, naturaleza, o entorno relacionado con la actividad?
- ¿Hay elementos consistentes con la actividad (libro, comida cocinada, parque, persona caminando)?
- ¿La imagen parece genuina (no stock photo, no captura de pantalla)?

Si la imagen **es válida**: otorga +2 puntos, confirma con entusiasmo moderado
Si la imagen **no es clara o no corresponde**: pide amablemente otra foto o acepta texto como respaldo (+1 punto)

**Nunca seas condescendiente si la foto no es perfecta.** El objetivo es motivar, no policiar.

#### Paso 3 — Si comparte POST de redes
Acepta la URL o captura de pantalla del post. Si hay URL, confirma que existe. Otorga +3 puntos.

#### Paso 4 — Actualiza estado en memoria
Guarda en memoria del agente:
```
touch_the_grass_state: {
  score: N,
  streak_days: N,
  last_activity_date: "YYYY-MM-DD",
  completed_today: ["activity_id"],
  mood_checkins: [{"date": "...", "before": N, "after": N}]
}
```

#### Paso 5 — Feedback post-actividad
Pregunta: *"Del 1 al 5, ¿cómo te sientes ahora vs antes?"*
Guarda el delta en memoria. Si el delta es positivo, menciónalo brevemente.

### 4. Ver progreso / score

Cuando el usuario pida ver su progreso:

Muestra un resumen:
```
🌿 Touch the Grass — Tu progreso

⭐ Score total: [N] puntos
🔥 Racha actual: [N] días
📅 Actividades esta semana: [N]
😊 Delta de ánimo promedio: +[N]

Bonos de racha:
  3 días → +5 pts [conseguido ✅ / falta N días]
  7 días → +15 pts
  14 días → +30 pts

Última actividad: [nombre] — hace [N] días
```

---

## Reglas generales

- **Tono**: cálido, directo, sin sermones. Ni coach de vida ni robot. Como un amigo que te conoce.
- **No insistir**: si el usuario dice que no puede hoy, acéptalo sin culpa. Registra que ya respondió.
- **Honestidad sobre el scoring**: si el usuario pregunta por qué se da más puntos por foto, explícalo naturalmente — la idea es que haya evidencia real del momento, no competencia.
- **Privacidad**: las fotos se analizan solo para verificar la actividad. No se describen en detalle ni se comentan aspectos personales de la imagen.
- **Google Calendar**: siempre confirma la zona horaria antes de crear eventos si hay duda. El usuario está en **Guadalajara / Ciudad de México (America/Mexico_City, UTC-6)**.

---

## Setup al instalar (una sola vez)

Cuando el usuario instale la skill o diga "configura touch the grass", ofrécele estas dos opciones:

### Opción A — Cron dedicado ✅ recomendado (hora exacta)
Ejecuta este comando y confirma que quedó registrado:
```
openclaw cron add \
  --name "touch-the-grass-daily" \
  --cron "0 9 * * *" \
  --tz "America/Mexico_City" \
  --session isolated \
  --message "Heartbeat Touch the Grass: revisa si el usuario tiene actividades TTG planeadas para hoy. Si no tiene, recuérdaselo con amabilidad. Si lleva 3+ días sin completar ninguna, menciónalo. Sigue las instrucciones del skill touch-the-grass para el tono correcto." \
  --announce
```
Verifica con `openclaw cron list` — si muestra `jobs: 0`, repite el comando.

### Opción B — Heartbeat (sin comandos extra)
Si el usuario prefiere no configurar un cron, dile que agregue esto a su `~/.openclaw/workspace/HEARTBEAT.md`:
```
- Touch the Grass: una vez al día en la mañana, revisa si el usuario tiene actividades planeadas.
  Si no las tiene y aún no le preguntaste hoy, hazlo con amabilidad.
  Si lleva 3+ días sin actividad completada, menciónalo brevemente.
```
Menos puntual en horario, pero cero comandos adicionales.

---

## Ejemplos de activación

- "llevo 3 semanas sin parar, estoy quemado"
- "touch the grass"
- "necesito desconectarme"
- "¿qué tengo de touch the grass hoy?"
- "ya fui a caminar" → iniciar flujo de verificación
- "muéstrame mi score"
