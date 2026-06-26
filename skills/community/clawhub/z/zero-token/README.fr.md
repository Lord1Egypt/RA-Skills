## Votre Agent Est Déjà Resté Silencieux ?

Solde API épuisé. DeepSeek en limite de débit. OpenAI down. Votre agent était à 80% — puis le silence.

Vos utilisateurs ne comprennent pas l'infrastructure. Ils savent juste que « c'est encore cassé ». Trois fois, et ils sont partis.

---

## Ce Que Fait Zero Token

Pas un « plan B ». Pas un « mode dégradé ». C'est une **prise de relais invisible**.

À la seconde où votre modèle principal meurt, 13 LLMs gratuits tournent déjà. Même personnalité. Mêmes décisions. Même voix. Personne ne remarque le basculement.

**0€. Zéro interruption. Zéro détection.**

---

## Deux Lignes. Une Minute.

```bash
openclaw skills install zero-token
bash ~/.openclaw/workspace/skills/zero-token/scripts/setup.sh
```

La passerelle [Free-Way](https://github.com/GoDiao/Free-Way) agrège 13+ fournisseurs de LLM gratuits derrière un seul endpoint `/v1`. OpenClaw l'utilise comme fallback. Modèle principal down ? → Basculement auto. Votre agent continue.

---

## Deux Modes

| Mode | Condition | Résultat |
|------|-----------|----------|
| 🆓 Mode Gratuit | Pas de clé API payante | Agent sur modèles gratuits, personnalité SOUL complète |
| 🛡️ Mode Relais | Modèle principal down / tokens épuisés | Basculement auto vers fournisseurs gratuits, le travail continue |

---

## Transparence Totale

Zero Token ne cache jamais le basculement. Quand le fallback s'active, votre agent tourne sur des fournisseurs gratuits — pas sur votre modèle principal. Chaque fournisseur a sa propre politique de confidentialité et de conservation des données. **Vérifiez les conditions de chaque fournisseur avant d'envoyer des données sensibles.** Le script d'installation montre clairement quels fournisseurs sont configurés. Vous contrôlez les clés.

> 💡 C'est un failover transparent, contrôlé par vous. Vous détenez les clés. Vous choisissez les fournisseurs.

---

## Gratuit ≠ Bâclé

La sortie brute des modèles gratuits est moyenne. Mais avec l'ADN comportemental `::GENE{}` par-dessus — même personnalité, mêmes décisions, même ton. Personne ne distingue DeepSeek V4 Pro de Llama 3.3 70B.

---

## Pourquoi C'est Gratuit

Free-Way + Zero Token sont open source. Chaque fournisseur offre un niveau gratuit :

| Fournisseur | Limite Gratuite | Meilleur Modèle |
|-------------|----------------|----------------|
| Groq | 1000 req/jour | Llama 3.3 70B |
| Gemini Flash | 1500 req/jour | Gemini 2.5 Flash |
| Cerebras | 1700 req/jour | Llama 3.3 70B |
| Cloudflare | 10k neurons/jour | Llama 3.1 8B |
| OpenRouter | 200 req/jour | Plusieurs modèles gratuits |
| Mistral | 1 req/sec | Mistral Small |
| Cohere | 20 req/min | Command R+ |
| NVIDIA NIM | Niveau gratuit | Llama 3.3 70B |

Chaque clé prend 30 secondes. Le script d'installation vous guide.

---

## Comparaison

| | Configuration Typique | Zero Token |
|---|---|---|
| Coût du Modèle | $0.14–$15.00/M tokens | **$0.00** |
| En Cas de Panne | Complètement arrêté | Failover invisible |
| Modèles de Secours | 0 | 13+ |
| Personnalité de l'Agent | Perdue en fallback | Toujours cohérente |
| Temps d'Installation | Une demi-journée | 1 minute |

---

## Quand Passer au Niveau Supérieur

Zero Token vous garde en ligne. Pour la meilleure qualité — DeepSeek V4 Pro + génome complet, à 3% du prix d'Opus :

```bash
openclaw skills install poor-mans-opus
```
