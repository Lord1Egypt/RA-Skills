# WA-Relay Examples

## Example 1: Simple Message Relay

**Third party sends:**
```
[WhatsApp +573128511052] Salo, ¿nos vemos mañana?
```

**Agent action:**
1. Respond with NO_REPLY (nothing sent to Martín)
2. Use message tool to notify owner:

```
📩 *Martín Vásquez*
¿Nos vemos mañana?
```

**Owner responds:**
```
Dile que sí, a las 10 en la oficina
```

**Agent action:**
1. Use message tool to send to +573128511052: "Sí, nos vemos mañana a las 10 en la oficina"
2. Confirm to owner: "✅ Enviado a Martín"
3. Log in wa-relay-log.md

---

## Example 2: Audio Message

**Third party sends:**
```
[WhatsApp +573156175555] <media:audio>
```

**Agent action:**
1. Respond with NO_REPLY
2. Transcribe the audio
3. Notify owner:

```
📩 *Banana* (audio)
"Oye Salo, te cuento que el viernes no puedo ir al evento. ¿Podemos reagendar?"
```

---

## Example 3: Unknown Number

**Third party sends:**
```
[WhatsApp +573001234567] Buenas, ¿usted es el de las automatizaciones?
```

**Agent action:**
1. Respond with NO_REPLY
2. Notify owner:

```
📩 *+573001234567* (desconocido)
Buenas, ¿usted es el de las automatizaciones?
```

---

## Example 4: Owner Checks Messages

**Owner asks:**
```
¿Qué me han escrito hoy?
```

**Agent action:**
1. Read wa-relay-log.md for today
2. Summarize:

```
Hoy te escribieron:
- *Martín* (14:30): Preguntó si se ven mañana → le respondiste que sí a las 10
- *Banana* (15:10): Audio diciendo que no puede ir el viernes, pregunta si reagendan → sin respuesta
- *+573001234567* (16:45): Preguntando por automatizaciones → sin respuesta
```

---

## Example 5: Batch Messages

**Third party sends 3 messages in 30 seconds:**
```
[WhatsApp +573128511052] Ey
[WhatsApp +573128511052] ¿Estás ahí?
[WhatsApp +573128511052] Necesito hablar contigo urgente
```

**Agent action (single notification):**

```
📩 *Martín Vásquez* (3 mensajes)
Ey
¿Estás ahí?
Necesito hablar contigo urgente
```

---

## Example 6: Group Chat

**Message in group:**
```
[WhatsApp Group "Aztec Lab Team" +573128511052] ¿Ya quedó lista la propuesta?
```

**Agent action:**
1. NO_REPLY in group
2. Notify owner:

```
📩 *Martín* en *Aztec Lab Team*
¿Ya quedó lista la propuesta?
```
