// quick-reminder/index.js
// Skill básica: agenda recordatorios a partir de mensajes naturales
// Funciona en consola y Telegram (si detecta el contexto)

const fs = require('fs');

// Simple: HH:MM, soporta 24h y español/inglés básico
const REMINDER_REGEXES = [
    /recordatorio para (.+) a las (\d{1,2}):(\d{2})/i,
    /remind me to (.+) at (\d{1,2}):(\d{2})/i
];

module.exports = async function (input, context) {
    if (!input || typeof input !== 'string') return;
    let match, texto, hour, minute;
    for (const regex of REMINDER_REGEXES) {
        match = input.match(regex);
        if (match) {
            texto = match[1].trim();
            hour = parseInt(match[2]);
            minute = parseInt(match[3]);
            break;
        }
    }
    if (!match) return; // No es recordatorio

    // Construir fecha para hoy o mañana según la hora
    const now = new Date();
    let remindDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hour, minute);
    if (remindDate < now) remindDate.setDate(remindDate.getDate() + 1);
    const msUntil = remindDate - now;

    // El mensaje a enviar
    const mensaje = `[Recordatorio] ${texto} — ${remindDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;

    // Determinar mecanismo de aviso
    if (context && context.telegram) {
        setTimeout(() => {
            context.telegram.sendMessage(context.telegram.chat.id, mensaje);
        }, msUntil);
        context.reply && context.reply(`Recordatorio programado para las ${remindDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} (Telegram)`);
    } else {
        setTimeout(() => {
            console.log(mensaje);
        }, msUntil);
        context.reply && context.reply(`Recordatorio programado para las ${remindDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} (consola/test)`);
    }
};
