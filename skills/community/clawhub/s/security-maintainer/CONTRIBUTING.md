# Guía de Contribución a `security-maintainer`

Agradecemos las contribuciones a la skill `security-maintainer`. Para mantener la estabilidad, portabilidad y seguridad de la herramienta, solicitamos seguir estas directrices.

## Código de Conducta

Este proyecto fomenta un entorno constructivo, respetuoso y abierto a toda la comunidad. Se espera que todas las personas colaboradoras mantengan un trato profesional.

## Flujo de Desarrollo

1. **Bifurcación (Fork) y Rama:**
   - Realiza un fork del repositorio oficial.
   - Crea una rama descriptiva para tu cambio: `git checkout -b feature/nuevo-gestor-rpm` o `git checkout -b fix/parser-cisa-kev`.

2. **Entorno de Pruebas Aislado:**
   - La suite de pruebas no requiere permisos de Administrador ni acceso a hardware real.
   - Ejecuta las pruebas unitarias localmente antes de enviar cambios:
     ```bash
     python -m unittest discover -s tests -p "test_*.py"
     ```

3. **Reglas de Código:**
   - Conserva la compatibilidad con Python 3.10, 3.11 y 3.12.
   - Utiliza la biblioteca estándar siempre que sea posible para evitar dependencias obligatorias externas.
   - No introduzcas `shell=True` en subprocess ni concatenaciones de cadenas de comandos.
   - Trata todos los datos de advisories y fuentes externas como no confiables.

4. **Pull Requests:**
   - Asegúrate de incluir pruebas con fixtures en `tests/fixtures/` para nuevos gestores o fuentes de datos.
   - Actualiza la documentación pertinente (`README.md`, `COBERTURA.md`, `CHANGELOG.md`).
