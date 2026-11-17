# Matriz de Cobertura y Límites Operativos

Este documento detalla la cobertura técnica real de `security-maintainer` v1.0.0, especificando qué componentes son completamente gestionables, cuáles tienen soporte parcial y cuáles requieren intervención manual o están expresamente excluidos por diseño defensivo.

## 1. Matriz de Cobertura de Componentes

| Entorno / Ámbito | Componente o Gestor | Nivel de Soporte | Detección | Actualización | Verificación Post-Parche | Reversión (Rollback) |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Windows Host** | **WinGet Apps** | **Completo** | Nativa (`winget list`) | Determinista (`winget upgrade --id`) | Re-inspección de versión en lista | Manual (WinGet no ofrece rollback transaccional) |
| **Windows Host** | **Windows Update** | **Parcial** | Nativa (COM API / WMI) | Vía script PowerShell autorizado | Detección de KB en `Get-HotFix` | Desinstalación vía `wusa.exe /uninstall` |
| **Windows Host** | **Registro (Desinstaladores)** | **Informativo / Manual** | Lectura de claves HKLM/HKCU | **No automatizable** | N/A | Manual |
| **Windows Host** | **Microsoft Store (AppX)** | **Parcial** | Paquetes de usuario / Store | Delegado en WinGet si existe manifest | Comprobación de versión AppX | Manual vía Store |
| **WSL** | **Ubuntu / Debian (APT/dpkg)** | **Completo** | `apt list`, `dpkg-query` | `apt-get --only-upgrade install` | Validación de versión de paquete deb | Parcial (`apt-get install <pkg>=<versión_previa>`) |
| **WSL** | **Fedora / RHEL (DNF/RPM)** | **Parcial** | `rpm -qa`, `dnf check-update` | `dnf upgrade-minimal` | Validación con `rpm -q` | `dnf history undo` |
| **WSL** | **Alpine Linux (APK)** | **Parcial** | `apk info`, `apk list` | `apk upgrade <pkg>` | `apk info -v` | No garantizada |
| **WSL** | **Plataforma y Kernel WSL** | **Informativo** | `wsl.exe --status` | Requiere `wsl --update` manual | Inspección de versión de kernel | Manual vía instalador MSI de WSL |
| **WSL** | **Distribuciones Detenidas** | **Informativo** | `wsl.exe -l -v` | **Omitida por política** | N/A | N/A |
| **Entornos Dev** | **Proyectos Node.js** | **Completo** | `package.json`, `package-lock.json` | `npm update` / `npm audit fix` | Coherencia de lockfile y tests | Total (restauración de lockfile vía git) |
| **Entornos Dev** | **Proyectos Python** | **Completo** | `requirements.txt`, `pyproject.toml` | `pip install --upgrade` en venv | `pip show` y ejecución de tests | Total (`pip install <pkg>==<versión_previa>`) |
| **Herramientas** | **pipx (CLI Apps)** | **Parcial** | `pipx list --json` | `pipx upgrade <app>` | Comprobación en entorno virtual | Reinstalación de versión previa |
| **Herramientas** | **npm global** | **Parcial** | `npm list -g --depth=0` | `npm update -g <pkg>` | Re-inspección de lista global | Reinstalación de versión previa |
| **Herramientas** | **Scoop / Chocolatey** | **Parcial** | `scoop list`, `choco list` | `scoop update`, `choco upgrade` | Detección de versión en lista | Reinstalación previa |
| **Hardware** | **Firmware / BIOS** | **Excluido** | N/A | **No soportado en v1.0** | N/A | N/A |
| **Hardware** | **Drivers de Dispositivo** | **Excluido** | N/A | **No soportado en v1.0** | N/A | N/A |

---

## 2. Fuentes de Datos de Vulnerabilidades

| Fuente Oficial | Tipo de Consulta | Soporte | Manejo de Cuotas / Fallos |
| :--- | :--- | :---: | :--- |
| **OSV.dev (Open Source Vulnerabilities)** | API REST JSON (`api.osv.dev`) | **Completo** | Paginación, timeouts de 15s, 3 reintentos con backoff. Caché local de 12 horas. |
| **CISA KEV Catalog** | Catálogo oficial JSON | **Completo** | Descarga con caché local de 24 horas. Marcado de prioridad crítica y fecha límite de remediación. |
| **Ubuntu Security Notices / Debian Tracker** | Base de firmas retroportadas | **Completo** | Resolución de backports para evitar falsos positivos en versiones LTS. |
| **NVD (National Vulnerability Database)** | Cruce de identidades CVE | **Parcial** | Enlaces canónicos y deduplicación con OSV y KEV. |
| **MSRC (Microsoft Security Update Guide)** | KB Articles de Windows | **Parcial** | Relación de KBs acumulativos con parches de sistema operativo. |

---

## 3. Política ante Fuentes No Disponibles

Un principio fundamental de diseño es que **la falta de respuesta de una fuente remota nunca equivale a la ausencia de vulnerabilidades**:

- Si la conexión con OSV.dev o CISA KEV falla y no existen datos locales en caché:
  - El sistema marca `is_coverage_complete = false`.
  - El informe destaca una alerta visual en Markdown (`[!WARNING] Cobertura incompleta`).
  - Se detallan las fuentes no disponibles.
  - Los componentes afectados se señalan como *no evaluables*.

---

## 4. Clasificación Estricta de Hallazgos

El motor distingue siempre las siguientes categorías:

1. `vulnerability_patched`: Actualización que subsana formalmente un CVE/GHSA confirmado.
2. `general_update_available`: Nueva versión disponible sin vulnerabilidades conocidas registradas.
3. `config_mitigation`: Cambio en configuración o flags que mitiga el riesgo sin alterar binarios.
4. `unpatched_vulnerability`: Vulnerabilidad sin solución oficial emitida por el fabricante o mantenedor.
5. `unsupported_eol`: Producto cuyo ciclo de vida ha expirado y no recibirá más actualizaciones.
6. `functional_bug`: Incidencia de funcionalidad no catalogada como vulnerabilidad de seguridad.
