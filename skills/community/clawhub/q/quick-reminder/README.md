# Quick Reminder

Mini-skill para OpenClaw: convierte frases normales como "recordatorio para aprobar skill a las 21:35" o "remind me to X at 14:00" en recordatorios programados.

## ¿Cómo funciona?
- Detecta frases entrenadas de recordatorio en español e inglés básico.
- Calcula el minuto a futuro correcto (hoy o mañana si ya pasó la hora del día).
- Programa un aviso usando Telegram o consola, según el canal/destino donde ejecutas el mensaje.

## Instalación rápida
1. Copia la carpeta `quick-reminder` en tu directorio de skills de OpenClaw (ej: `~/.openclaw/workspace/skills/`).
2. Reinicia OpenClaw/gateway.

## Uso
Envíale (por Telegram, consola o chat)

    recordatorio para tomar agua a las 21:40

    remind me to check github at 16:15

y recibirás el aviso en el canal usado exactamente a esa hora.

---
Esta skill no gestiona repeticiones ni recordatorios complejos, pero es ideal como base para ampliaciones.
