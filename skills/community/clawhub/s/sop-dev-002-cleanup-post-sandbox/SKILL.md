---
name: sop-dev-002-cleanup-post-sandbox
description: "SOP Canónico: sop-dev-002-cleanup-post-sandbox"
userFacing: true
---

---
sop_id: SOP-DEV-002
title: Cleanup post-ejecución del sandbox
agent: dev
status: approved
version: 1.0
created: 2026-07-10
updated: 2026-08-07
reviewed_by: "skill-manager"
approved_by: "change-manager"
promoted_to_skill: "sop-dev-002-cleanup-sandbox"
---

## Propósito
Define el procedimiento obligatorio de limpieza y reset del entorno sandbox después de completar una tarea. Garantiza que el sandbox quede limpio para la siguiente tarea y no queden residuos que contaminen ejecuciones futuras.

## Disparador
Al completar TASK con STATUS: SANDBOX_VALIDATED (después de SOP-DEV-001) y antes de promover a host, o al cancelar/abortar una tarea en sandbox.

## Procedimiento
1. **Identificar artifacts a preservar** — Revisar ARTIFACTS listados en COMMS del bloque SANDBOX_VALIDATED. Estos NO se borran (se promueven a host si procede).
2. **Eliminar archivos temporales** — Borrar del sandbox:
   - Archivos `*.tmp`, `*.temp`, `*.bak`, `*~`
   - Directorios `__pycache__/`, `.pytest_cache/`, `node_modules/` (si no son artifacts)
   - Logs de ejecución temporal (`*.log`, `nohup.out`)
   - Cualquier archivo creado durante validación que no esté en ARTIFACTS
3. **Reset de estado de servicios** — Si se levantaron servicios en sandbox (DB, Redis, mocks):
   - Detener contenedores/servicios: `docker compose down` o equivalente
   - Limpiar volúmenes temporales si se crearon
   - Verificar que puertos quedan libres
4. **Reset de git (si aplica)** — Si se hizo `git clone` o trabajo en repo:
   - `git checkout -- .` para descartar cambios no committed
   - `git clean -fd` para eliminar untracked (excepto artifacts preservados)
   - Volver al commit/branch base documentado en SOP-DEV-001
5. **Verificar limpieza** — Ejecutar `ls -la` y `git status` en sandbox root. Confirmar que solo quedan artifacts listados y estructura base.
6. **Registrar en COMMS** — Escribir bloque `TASK_PROGRESS` con STATUS: SANDBOX_CLEANED, lista de archivos eliminados/limpiados, confirmación de sandbox listo para siguiente tarea.

## Validación
- ✅ Ningún archivo temporal residual en sandbox (tmp, cache, logs, build outputs no declarados)
- ✅ Servicios/containers detenidos y puertos libres
- ✅ Git status limpio (solo artifacts preservados)
- ✅ COMMS block con STATUS: SANDBOX_CLEANED escrito
- ✅ Sandbox listo para próxima tarea sin intervención manual

## Escalado
- Si limpieza falla (permisos, procesos zombie, volúmenes persistentes) → STATUS: BLOCKED → notificar a main
- Si artifacts no preservados correctamente → STATUS: BLOCKED → no proceder a promoción; recuperar de backup si existe
- Si sandbox corrupto irrecuperable → STATUS: DECISION_RECORDED → solicitar nuevo sandbox a main

---
*Ref: ~/.openclaw/workspace/gobierno/SOP_STANDARD.md*