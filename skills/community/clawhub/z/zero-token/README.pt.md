## Seu Agente Já Ficou em Silêncio?

Saldo da API acabou. DeepSeek no limite de taxa. OpenAI caiu. Seu agente estava 80% pronto — então silêncio.

Seus usuários não entendem infraestrutura. Eles só sabem que "quebrou de novo". Três vezes e você os perdeu.

---

## O Que o Zero Token Faz

Não é um "plano B". Não é "modo degradado". É **tomada de controle invisível**.

No segundo em que seu modelo principal morre, 13 LLMs gratuitos já estão rodando. Mesma personalidade. Mesmas decisões. Mesma voz. Seus usuários nem notam a troca.

**R$0. Zero downtime. Zero detecção.**

---

## Duas Linhas. Um Minuto.

```bash
openclaw skills install zero-token
bash ~/.openclaw/workspace/skills/zero-token/scripts/setup.sh
```

O gateway [Free-Way](https://github.com/GoDiao/Free-Way) agrega 13+ provedores de LLM gratuitos em um único endpoint `/v1`. OpenClaw usa como fallback. Modelo principal caiu? → Troca automática. Seu agente continua.

---

## Dois Modos

| Modo | Condição | Resultado |
|------|----------|-----------|
| 🆓 Modo Grátis | Sem API key paga | Agente roda em modelos gratuitos, personalidade SOUL completa |
| 🛡️ Modo Revezamento | Modelo principal caiu / tokens esgotados | Troca automática para provedores grátis, trabalho continua |

---

## Transparência Total

Zero Token nunca esconde a troca. Quando o fallback ativa, seu agente está rodando em provedores gratuitos — não no seu modelo principal. Cada provedor tem sua própria política de privacidade e retenção de dados. **Revise os termos de cada provedor antes de enviar dados sensíveis.** O script de setup mostra claramente quais provedores estão configurados. Você controla as chaves.

> 💡 Este é um failover transparente, controlado por você. Você tem as chaves. Você decide os provedores.

---

## Grátis Não É Lixo

A saída bruta dos modelos grátis é mediana. Mas com o DNA comportamental `::GENE{}` por cima — mesma personalidade, mesmas decisões, mesmo tom. Ninguém distingue se está rodando DeepSeek V4 Pro ou Llama 3.3 70B.

---

## Por Que É Grátis

Free-Way + Zero Token são open source. Cada provedor oferece camada gratuita:

| Provedor | Limite Grátis | Melhor Modelo |
|----------|--------------|--------------|
| Groq | 1000 req/dia | Llama 3.3 70B |
| Gemini Flash | 1500 req/dia | Gemini 2.5 Flash |
| Cerebras | 1700 req/dia | Llama 3.3 70B |
| Cloudflare | 10k neurons/dia | Llama 3.1 8B |
| OpenRouter | 200 req/dia | Múltiplos modelos grátis |
| Mistral | 1 req/seg | Mistral Small |
| Cohere | 20 req/min | Command R+ |
| NVIDIA NIM | Camada gratuita | Llama 3.3 70B |

Cada chave leva 30 segundos. O script de setup te guia.

---

## Comparação

| | Configuração Típica | Zero Token |
|---|---|---|
| Custo do Modelo | $0.14–$15.00/M tokens | **$0.00** |
| Quedas | Totalmente parado | Failover invisível |
| Modelos de Reserva | 0 | 13+ |
| Personalidade do Agente | Perdida no fallback | Sempre consistente |
| Tempo de Setup | Meio dia (load balancing) | 1 minuto |

---

## Quando Fazer Upgrade

Zero Token mantém você online. Para a melhor qualidade de saída — DeepSeek V4 Pro + genoma completo, a 3% do preço do Opus:

```bash
openclaw skills install poor-mans-opus
```
