---
_manifest:
  urn: urn:salud:skill:salubrista-hah-clarifier:1.0.0
  type: lazy_load_endofunctor
---

# CM-CLARIFIER

## Proposito
Solicitar la aclaracion minima necesaria para que el dispatcher pueda clasificar la consulta. Identifica que dato falta (escala, modalidad, intencion, producto esperado o contexto local) y formula la pregunta mas parsimoniosa posible.

## Input/Output
- **Input:** consulta: string, intent_parcial: IntentResult?
- **Output:** ClarificationRequest { dato_faltante: string, motivo: string, pregunta: string, permite_supuestos: bool }

## Procedimiento
1. RECIBIR la consulta original y, si existe, el resultado parcial de CM-INTENT-HOSPITALIZATION.
2. IDENTIFICAR el dato minimo faltante para desambiguar:
   - escala (unidad / establecimiento / red / territorio / nacional)
   - modalidad dominante (hospital / domicilio / transicion / integrada)
   - intencion principal (analisis / diseno / HD / implementacion / evaluacion / vigilancia / producto / informe)
   - tipo de producto esperado (si la intencion apunta a producto)
   - grado de aterrizaje local requerido
3. EXPLICITAR por que falta ese dato y que implicancias tiene para la respuesta.
4. FORMULAR una pregunta directa y parsimoniosa.
5. OFRECER la opcion de avanzar con supuestos explicitos si el usuario lo autoriza.
6. OUTPUT: dato faltante, motivo, pregunta y flag de supuestos.

## Signature Output
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| dato_faltante | string | Escala / modalidad / intencion / producto / contexto_local |
| motivo | string | Por que ese dato es necesario para continuar |
| pregunta | string | Pregunta minima para el usuario |
| permite_supuestos | bool | True si es viable avanzar con supuestos explicitos |
