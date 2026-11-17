---
name: sop-dev-003-docker-workaround-host-commands
description: "SOP Canónico: sop-dev-003-docker-workaround-host-commands"
userFacing: true
---

---
sop_id: SOP-DEV-003
title: Workaround para limitación Docker (host-commands.sh)
agent: dev
status: approved
version: 1.0
created: 2026-07-10
updated: 2026-08-07
reviewed_by: "skill-manager"
approved_by: "change-manager"
promoted_to_skill: "sop-dev-003-docker-workaround"
---

## Propósito
Define el procedimiento estándar para ejecutar comandos Docker (`docker exec`, `docker run`, `docker build`, etc.) cuando el agente `dev` no tiene acceso directo al daemon Docker del host. Usa el mecanismo de host-commands.sh como puente seguro.

## Disparador
Cuando una tarea asignada a `dev` requiere operaciones Docker que no se pueden ejecutar dentro del sandbox (ej: levantar contenedores, ejecutar en contenedores existentes, builds multi-stage, acceso a volúmenes host).

## Procedimiento
1. **Validar necesidad** — Confirmar que la operación NO puede hacerse en sandbox (ej: necesita daemon Docker real, red host, volúmenes host, GPU, puertos privilegiados). Documentar justificación en COMMS.
2. **Escribir comandos en host-commands.sh** — Crear/añadir a `/workspace/host-commands.sh`:
   ```bash
   #!/bin/bash
   # TASK: <card_id> — <descripción breve>
   # AGENT: dev
   # TIMESTAMP: $(date -Iseconds)
   
   # Comandos Docker a ejecutar en host (uno por línea, con set -e)
   docker exec <container> <comando>
   docker run --rm <imagen> <comando>
   # ... más comandos
   ```
   - Un comando por línea, con `set -e` implícito (fallo detiene ejecución)
   - Incluir solo comandos Docker; NO comandos arbitrarios de host
   - Comentar cada bloque con propósito
3. **Hacer ejecutable** — `chmod +x /workspace/host-commands.sh`
4. **Registrar en COMMS** — Escribir bloque `WORKBOARD_BLOCK` con:
   - REASON: "Docker operation required — host-commands.sh ready"
   - COMMANDS_FILE: `/workspace/host-commands.sh`
   - STATUS: WAITING_HOST_EXEC
   - CARD_ID: <card_id>
5. **Bloquear workboard card** — Ejecutar `workboard_block` en la card actual con reason: "Waiting for host Docker execution via host-commands.sh"
6. **Esperar ejecución host** — Main/operator ejecuta `/workspace/host-commands.sh` en host. Output se captura en `/workspace/host-commands-output.log`
7. **Verificar resultado** — Leer `/workspace/host-commands-output.log`. Confirmar éxito (exit code 0, output esperado).
8. **Limpiar** — Borrar `/workspace/host-commands.sh` y `/workspace/host-commands-output.log` tras confirmar.
9. **Desbloquear y continuar** — `workboard_unblock` card, continuar con SOP-DEV-001 validación en sandbox con resultado de host.

## Validación
- ✅ Justificación documentada en COMMS (por qué sandbox no basta)
- ✅ host-commands.sh solo contiene comandos Docker (auditable)
- ✅ WORKBOARD_BLOCK escrito con CARD_ID y COMMANDS_FILE
- ✅ Card bloqueada en workboard
- ✅ Output verificado tras ejecución host
- ✅ Archivos temporales limpiados tras confirmación
- ✅ Continuación en sandbox validada

## Escalado
- Si host-commands.sh falla (exit code ≠ 0) → STATUS: BLOCKED en COMMS → notificar a main con output log
- Si operación Docker requiere privilegios no permitidos → STATUS: DECISION_RECORDED → escalar a main para decisión de arquitectura
- Si timeout > 5 min en ejecución host → STATUS: BLOCKED → investigar hang
- Si main/operator no ejecuta en 30 min → STATUS: ESCALATED → notificar en COMMS_main.md

## Seguridad
- **NUNCA** escribir comandos no-Docker en host-commands.sh (rm -rf, chmod 777, curl | bash, etc.)
- **NUNCA** usar host-commands.sh para operaciones que sandbox puede hacer
- Auditoría: main/operator revisa host-commands.sh ANTES de ejecutar
- Log de ejecuciones se mantiene en COMMS_main.md con timestamp y resultado

---
*Ref: ~/.openclaw/workspace/gobierno/SOP_STANDARD.md*