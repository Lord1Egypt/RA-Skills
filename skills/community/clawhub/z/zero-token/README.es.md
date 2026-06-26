## ¿Tu Agente Alguna Vez Se Quedó en Silencio?

Saldo de API agotado. DeepSeek con límite de tasa. OpenAI caído. Tu agente iba al 80% — luego silencio.

Tus usuarios no entienden de infraestructura. Solo saben que "falló otra vez". A la tercera, se fueron.

---

## Lo Que Hace Zero Token

No es un "plan B". No es "modo degradado". Es **relevo invisible**.

En el instante en que tu modelo principal muere, 13 LLMs gratuitos ya están corriendo. Misma personalidad. Mismas decisiones. Misma voz. Tus usuarios ni se enteran del cambio.

**$0. Cero caídas. Cero detección.**

---

## Dos Líneas. Un Minuto.

```bash
openclaw skills install zero-token
bash ~/.openclaw/workspace/skills/zero-token/scripts/setup.sh
```

El gateway [Free-Way](https://github.com/GoDiao/Free-Way) agrega 13+ proveedores de LLM gratuitos tras un solo endpoint `/v1`. OpenClaw lo usa como fallback. ¿Modelo principal caído? → Cambio automático. Tu agente sigue.

---

## Dos Modos

| Modo | Condición | Resultado |
|------|-----------|-----------|
| 🆓 Modo Gratuito | Sin API key de pago | Agente corre en modelos gratuitos, personalidad SOUL completa |
| 🛡️ Modo Relevo | Modelo principal caído / tokens agotados | Cambio automático a proveedores gratis, trabajo continúa |

---

## Transparencia Total

Zero Token nunca oculta el cambio. Cuando el fallback se activa, tu agente está funcionando en proveedores gratuitos — no en tu modelo principal. Cada proveedor tiene su propia política de privacidad y retención de datos. **Revisa los términos de cada proveedor antes de enviar datos sensibles.** El script de instalación muestra claramente qué proveedores están configurados. Tú controlas las claves.

> 💡 Este es un failover transparente, controlado por ti. Tú tienes las llaves. Tú decides los proveedores.

---

## Gratis No Es Basura

La salida bruta de modelos gratis es mediocre. Pero con el ADN conductual `::GENE{}` encima — misma personalidad, mismas decisiones, mismo tono. Nadie distingue si corre DeepSeek V4 Pro o Llama 3.3 70B.

---

## Por Qué Es Gratis

Free-Way + Zero Token son código abierto. Cada proveedor ofrece capa gratuita:

| Proveedor | Límite Gratuito | Mejor Modelo |
|-----------|----------------|-------------|
| Groq | 1000 req/día | Llama 3.3 70B |
| Gemini Flash | 1500 req/día | Gemini 2.5 Flash |
| Cerebras | 1700 req/día | Llama 3.3 70B |
| Cloudflare | 10k neurons/día | Llama 3.1 8B |
| OpenRouter | 200 req/día | Múltiples modelos gratis |
| Mistral | 1 req/seg | Mistral Small |
| Cohere | 20 req/min | Command R+ |
| NVIDIA NIM | Capa gratuita | Llama 3.3 70B |

Cada key toma 30 segundos. El script de instalación te guía.

---

## Comparación

| | Configuración Típica | Zero Token |
|---|---|---|
| Costo de Modelo | $0.14–$15.00/M tokens | **$0.00** |
| Ante Caídas | Completamente parado | Failover invisible |
| Modelos de Respaldo | 0 | 13+ |
| Personalidad del Agente | Se pierde en fallback | Siempre consistente |
| Tiempo de Setup | Medio día (balanceo de carga) | 1 minuto |

---

## Cuándo Actualizar

Zero Token te mantiene en línea. Para la mejor calidad de salida — DeepSeek V4 Pro + genoma completo, al 3% del precio de Opus:

```bash
openclaw skills install poor-mans-opus
```
