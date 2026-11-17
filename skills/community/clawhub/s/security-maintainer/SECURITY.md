# Política de Seguridad y Divulgación Responsable

El proyecto `security-maintainer` toma la seguridad y la privacidad de la infraestructura del usuario con máxima prioridad.

## Reporte de Vulnerabilidades

Si descubres una posible vulnerabilidad de seguridad en esta skill, por favor **NO** abras una incidencia pública en GitHub.

Sigue este procedimiento:

1. Utiliza la funcionalidad de [Advisories privados de GitHub](https://github.com/openclaw/security-maintainer/security/advisories/new) para reportar el problema de forma confidencial.
2. Si no tienes acceso a GitHub Advisories, contacta directamente con el equipo de mantenedores a través del canal oficial de seguridad de OpenClaw: `security@openclaw.dev` con el asunto `[VULNERABILITY] security-maintainer`.
3. Incluye:
   - Descripción detallada del hallazgo.
   - Pasos deterministas para reproducir el comportamiento.
   - Versión de OpenClaw, versión de Windows y distribuciones WSL evaluadas.
   - Posible impacto o vectores de ataque identificados.

Nos comprometemos a acusar recibo en un plazo inferior a 48 horas laborables y coordinar un parche o mitigación antes de cualquier divulgación pública.

## Principios de Diseño Defensivo

Esta skill opera bajo directrices estrictas de contención:
- **Modo predeterminado `ask`:** Jamás se ejecutan cambios sin aprobación explícita vinculada a la huella criptográfica SHA-256 del plan.
- **Sin elevación silenciosa:** La falta de privilegios detiene la acción y la reporta como bloqueada.
- **Sin ejecución de código arbitrario:** Toda interacción con el sistema operativo y gestores de paquetes es estática y determinista.
- **Sin telemetría oculta:** No se recopilan ni transmiten datos privados, nombres de usuario ni credenciales.
