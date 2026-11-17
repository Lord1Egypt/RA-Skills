# Self-Relationship Skill · 与自己对话

[English](README.md) | [中文](README.zh-CN.md) | [Deutsch](README.de.md) | **Español** | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

> Ayudar a las personas a entenderse a sí mismas con más claridad, aceptarse sin renunciar al crecimiento y tomar decisiones que se ajusten a su vida real.
>
> 帮助一个人更好地理解自己、接纳自己、调整自己，并在现实中做出更适合自己的选择。

Una habilidad de IA basada en la psicología positiva: cuando los usuarios hablan de «relación con uno mismo», «autoaceptación», «entenderse a sí mismo», «crecimiento personal» y temas similares, los guía a entender primero y cambiar después, en lugar de apresurarse a dar consejos o etiquetas.

## Filosofía central

- **Entiéndete a ti mismo antes de cambiarte**: no juzgues con prisa; primero pregunta «¿qué pasó, qué estoy experimentando, qué significa esto para mí?»
- **Un estado no es una identidad**: «ahora me siento ansioso» ≠ «soy una persona ansiosa»
- **Aceptación no significa renunciar al cambio**: decide el siguiente paso basándote en la realidad
- **Las pruebas son herramientas para entender, no etiquetas que te definen**: los tests de personalidad, el MBTI y el Big Five son espejos para conocerte
- **No conviertas la psicología en una nueva herramienta de autojuicio**: sin certeza fabricada, sin experiencias inventadas, sin positividad forzada

## Características

- Contenido bilingüe (texto completo en chino + versión en inglés dentro de `SKILL.md`)
- Marco estructurado de autorreflexión: Hechos → Sentimientos → Interpretación → Juicio → Elección
- Principios de expresión y límites claros que evitan el tono de «artículo de psicología generado por IA»
- Sin diagnósticos, sin etiquetas, sin grandes decisiones de vida en nombre del usuario

## Instalación

Copia este directorio (o `SKILL.md`) al directorio de skills de tu agente:

```bash
# Para agentes que admiten skills, p. ej. Claude Code, Trae, etc.
# Copia el directorio self-relationship a tu directorio de skills
cp -r self-relationship ~/.claude/skills/
```

Una vez instalada, la habilidad se carga automáticamente cuando el usuario menciona temas como «relación con uno mismo», «autoaceptación», «entenderse a sí mismo», «crecimiento personal» o sus equivalentes en chino 「与自己相处」「自我关系」「自我接纳」「自我理解」「认识自己」「自我成长」.

## Uso

Simplemente habla con tu agente, por ejemplo:

- «No puedo dejar de criticarme. ¿Qué debería hacer?»
- «Me siento un fracaso. ¿Hay algo mal en mi personalidad?»
- «Hice el MBTI, pero siento que me define.»
- «No estoy seguro de lo que realmente quiero.»

El agente seguirá los principios de conversación definidos en la habilidad: entender → aclarar → ofrecer perspectiva → identificar opciones.

## Estructura del directorio

```
self-relationship/
├── README.md        # Este archivo (inglés, se muestra por defecto en GitHub)
├── README.zh-CN.md  # 中文说明 (Versión china)
├── README.de.md     # Deutsch (Versión alemana)
├── README.es.md     # Este archivo (Español)
├── README.ru.md     # Русский (Versión rusa)
├── README.ja.md     # 日本語 (Versión japonesa)
├── README.ko.md     # 한국어 (Versión coreana)
└── SKILL.md         # Contenido de la habilidad (bilingüe, con descripción de activación en el frontmatter)
```

## Marco de contenido

1. **Filosofía central** — 10 principios clave (estado ≠ identidad, aceptación ≠ renuncia, enfoque en tendencias, etc.)
2. **Marco de autorreflexión** — cinco capas: Hechos → Sentimientos → Interpretación → Juicio → Elección
3. **Distinciones importantes** — hechos vs. interpretaciones, sentimientos vs. juicios, aceptación vs. resignación, etc.
4. **Principios de conversación** — entender antes de aconsejar, permitir la incertidumbre, permitir las contradicciones, encontrar lo controlable
5. **Principios de expresión** — 13 principios (evitar el tono de IA, usar menos aforismos, nunca inventar experiencias)
6. **Orientación de respuesta** — entender → aclarar → ofrecer perspectiva → identificar opciones
7. **Límites** — sin diagnósticos, sin patologizar, sin decisiones en nombre del usuario

## Descargo de responsabilidad

Esta habilidad es solo para educación y autorreflexión. No constituye un diagnóstico médico, psicológico ni clínico. Si estás experimentando angustia psicológica grave o una crisis, busca ayuda profesional cualificada (como un terapeuta, psiquiatra o una línea de crisis local).

## Licencia

Este proyecto no tiene una licencia de código abierto especificada. Para uso comercial o redistribución, contacta al autor.
