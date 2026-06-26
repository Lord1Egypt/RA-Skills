# 💬 whatsapp-business-latam

> Configuración WhatsApp Business API (oficial Meta) para PyMEs de Argentina y LATAM — OpenClaw skill

Skill gratuito para [OpenClaw](https://openclaw.ai) que cubre el setup end-to-end de la
**WhatsApp Business API oficial de Meta**, con templates HSM listos en español para los
casos de uso más comunes de PyMEs argentinas, guía de compliance y checklist anti-ban.

**Solo API oficial de Meta. Nunca librerías no oficiales.**

---

## ¿Qué hace?

- Guía de setup paso a paso: Meta Business Manager → número → token → webhook → OpenClaw
- 6 templates HSM listos para copiar y enviar a Meta para aprobación (en español argentino)
- Integración directa con `openclaw.json` para envíos automatizados desde el agente
- Reglas de compliance: opt-in, ventana de 24hs, rate limits y quality rating
- Checklist anti-ban con 10 puntos antes del primer envío en producción
- Estimación de costos para PyMEs argentinas (~USD 7-15/mes para 1,000 mensajes)
- Ejemplos de curl para enviar templates y mensajes de texto libres

## Instalación

```bash
clawhub install whatsapp-business-latam
```

## Uso

```
wa setup              # Guía completa desde cero
wa template <tipo>    # Template HSM listo (turno | recordatorio | pago | arca | pedido | bienvenida)
wa checklist          # 10 puntos antes del primer envío en producción
wa compliance         # Reglas de opt-in, ventana 24hs, rate limits
wa costos             # Estimación de costos para PyMEs argentinas
wa config             # Bloque de configuración para openclaw.json
wa test               # Comando curl para enviar mensaje de prueba
```

## Templates HSM incluidos

| Template | Categoría Meta | Uso |
|----------|---------------|-----|
| `confirmacion_turno_v1` | UTILITY | Confirmar turnos agendados |
| `recordatorio_turno_24hs_v1` | UTILITY | Recordatorio automático 24hs antes |
| `recordatorio_pago_pendiente_v1` | UTILITY | Cobros pendientes / facturas vencidas |
| `alerta_vencimiento_arca_v1` | UTILITY | Vencimientos AFIP para estudios contables |
| `pedido_listo_v1` | UTILITY | Notificación de pedido / trabajo listo |
| `bienvenida_v1` | MARKETING | Primer contacto con nuevo cliente |

## Requisitos

- Cuenta en Meta Business Suite (business.facebook.com)
- App creada en Meta for Developers (developers.facebook.com)
- Número de teléfono dedicado (no debe tener WhatsApp instalado)
- `curl` disponible en el sistema (para envíos desde el agente)

## ⚠️ Importante: Solo API oficial

Este skill cubre exclusivamente la [WhatsApp Business Platform](https://business.whatsapp.com/)
de Meta. Las siguientes librerías **no oficiales** están fuera del scope y no deben usarse
en producción ya que violan los Términos de Servicio y resultan en baneo permanente del número:

❌ Baileys · ❌ whatsapp-web.js · ❌ WPPConnect · ❌ venom-bot · ❌ Chat-API

## Skills relacionados

| Skill | Descripción |
|-------|-------------|
| [`argentina-fiscal-calendar`](https://clawhub.ai/centriqs/argentina-fiscal-calendar) | Datos de vencimientos ARCA para automatizar el template `alerta_vencimiento_arca_v1` |
| [`latam-timezone-briefing`](https://clawhub.ai/centriqs/latam-timezone-briefing) | Canal de entrega del briefing matutino vía WhatsApp |
| `whatsapp-business-latam-pro` *(paid — próximamente)* | Menú interactivo, botones, flows, integración Tiendanube + MercadoPago |

## Licencia

MIT — Libre uso, modificación y redistribución.

---

Desarrollado por **[Centriqs](https://centriqs.io)** — *Center of your operations*
Agentes IA para PyMEs en LATAM · Buenos Aires, Argentina
