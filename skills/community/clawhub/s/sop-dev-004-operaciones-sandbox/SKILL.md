---
name: sop-dev-004-operaciones-sandbox
description: "SOP Canónico: sop-dev-004-operaciones-sandbox"
userFacing: true
---

---
sop_id: SOP-DEV-004
title: Operaciones de Sandbox (Activación y Desactivación)
agent: dev
status: approved
version: 1.0
created: 2026-08-10
reviewed_by: "main"
approved_by: "Sebastian (piloto Tier 1A)"
promoted_to_skill: ""
---

## Propósito
Definir cuándo y cómo activar/desactivar el sandbox Docker para coder, dev y security, y los modos válidos de aislamiento en OpenClaw.

## Disparador
- Test de docker-compose nuevo, deploy de prerequisitos Magento, scripts destructivos o auditoría de seguridad profunda
- Necesidad de volver a producción (sandbox off)

## Procedimiento
1. Identificar el caso de uso y el modo requerido:
   - coder/dev (pruebas): modo `non-main`
   - security (auditoría/pentest): modo `all`
   - operación normal: modo `off`
2. Activar para dev/coder con el comando jq que setea `sandbox.mode = "non-main"` en openclaw.json
3. Activar para security con el comando jq que setea `sandbox.mode = "all"`
4. Reiniciar el gateway: `systemctl --user restart openclaw-gateway.service`
5. Verificar que el modo quedó aplicado (config + status del gateway)
6. Al terminar la tarea → desactivar todo con el comando jq que setea `sandbox.mode = "off"` y reiniciar
7. Registrar en COMMS con STATUS: DONE

## Validación
- ✅ El archivo openclaw.json refleja el modo esperado tras el jq
- ✅ El gateway reinició sin errores
- ✅ Al finalizar, todos los agentes volvieron a `off` (producción)

## Escalado
- Si el gateway no reinicia o la config queda corrupta → restaurar backup de openclaw.json y escalar a main
- Si un agente necesita sandbox y no está en la tabla de casos de uso → preguntar a main antes de activar

---
*Fuente: ~/.openclaw/workspace/cumplimiento/politicas/SANDBOX_OPERATIONS.md*
