---
name: quick-reminder
summary: Recordatorios rápidos tomando frases naturales y avisando vía Telegram o consola.
description: |
  Detecta frases tipo "recordatorio para ... a las HH:MM" o "remind me to ... at HH:MM" en tus mensajes.
  Programa un aviso exacto usando el método disponible: Telegram o consola.
  Ideal para recordatorios simples y rápidos sin depender de skills externas complejas.
tags:
  - reminder
  - recordatorio
  - telegram
  - chat
  - cron
---

# Quick Reminder

Skill sencilla que toma frases naturales y programa un recordatorio en minutos.

## Ejemplos de uso
- "recordatorio para llamar a María a las 21:15"
- "remind me to send email at 13:00"

El aviso se enviará automáticamente al canal donde recibiste el mensaje (Telegram, consola, web, etc).

## Instalación
1. Copia la carpeta `quick-reminder` en tu ruta de skills de OpenClaw.
2. Reinicia el gateway de OpenClaw.

## Funciona con:
- Español e inglés (bases, puedes sumar otros patrones en index.js)
- Telegram (si el context.telegram existe)
- Consola/TTY (si no es chat)

## Límite/simplicidad
No soporta repeticiones, solo HH:MM (de hoy o si ya pasó, lo agenda al día siguiente).
Ideal para flujos personales básicos o como plantilla para skills más potentes.
