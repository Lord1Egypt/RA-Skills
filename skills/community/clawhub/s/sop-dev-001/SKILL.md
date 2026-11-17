---
name: sop-dev-001
description: "SOP Canónico: SOP-DEV-001-implementacion-sandbox"
userFacing: true
---

---
sop_id: SOP-DEV-001
title: Implementación en Sandbox
agent: dev
status: approved
version: 1.0
created: 2026-07-10
updated: 2026-08-07
reviewed_by: "skill-manager"
approved_by: "change-manager"
promoted_to_skill: "sop-dev-001"
---

## Propósito
Define el proceso obligatorio para implementar scripts, configuraciones y cambios en el entorno sandbox antes de cualquier ejecución en host.

## Disparador
Al recibir TASK_ASSIGNED con objetivo de implementar script, configuración, cambio de infraestructura o despliegue que requiera validación en sandbox.

## Procedimiento
1. Verificar sandbox disponible y limpio
2. Clonar/preparar entorno en sandbox
3. Escribir implementación exclusivamente en sandbox
4. Ejecutar validaciones (tests, linters, build) en sandbox
5. Verificar evidencia de funcionamiento
6. Documentar artifacts con rutas absolutas del sandbox
7. Registrar en COMMS con STATUS: SANDBOX_VALIDATED

## Validación
- Sandbox limpio al inicio
- Implementación completa en sandbox (cero archivos en host)
- Tests/validaciones pasan en sandbox
- ARTIFACTS documentados
- COMMS block con STATUS: SANDBOX_VALIDATED escrito
