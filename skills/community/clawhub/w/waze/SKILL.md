---
name: waze
version: 1.0.0
author: eliolonghi
tags: [navigation, waze, maps, briefing, location, rota, endereco]
description: >
  Gera links de navegação do Waze para qualquer destino: endereços, nomes de
  estabelecimentos, locais de compromissos na agenda. Use sempre que o usuário
  mencionar um destino, pedir rota, querer saber como chegar a algum lugar, ou
  quando um evento da agenda tiver um local definido — nesse caso inclua o link
  automaticamente no briefing, sem precisar ser solicitado. Quando o destino for
  vago (nome de empresa, tipo de estabelecimento, "posto mais próximo"), busca
  o local mais próximo da cidade do usuário antes de gerar o link — nunca use
  um endereço de outra cidade.
---

# Waze Navigation Skill

## O que faz

Gera links de navegação do Waze que, ao serem tocados no celular, abrem o app
diretamente com a rota pronta. Funciona via deep links públicos do Waze — sem
necessidade de API key.

## Formato do link

```
https://waze.com/ul?q=ENDEREÇO_CODIFICADO&navigate=yes
```

O endereço deve estar URL-encoded. Use Python quando disponível:

```python
from urllib.parse import quote
address = "Av. Jerônimo Monteiro, 1000, Vitória, ES, Brasil"
link = f"https://waze.com/ul?q={quote(address)}&navigate=yes"
print(link)
```

---

## Fluxo de uso

### Passo 1 — Descobrir a localização do usuário

Antes de qualquer coisa, descubra em qual cidade o usuário está. Procure em:
- `USER.md` no workspace ativo
- `SOUL.md` ou qualquer arquivo de perfil do workspace

Se não encontrar, pergunte. A cidade é essencial para buscar estabelecimentos
próximos — nunca assuma uma localização genérica ou use a primeira cidade que
aparecer num resultado de busca.

### Passo 2 — Classificar o destino

**Destino específico** (endereço completo, CEP, coordenadas):
→ Pule direto para o Passo 4.

**Destino vago** (nome de empresa, categoria, "o mais próximo"):
→ Siga para o Passo 3 primeiro.

### Passo 3 — Buscar o local mais próximo (destinos vagos)

Use Tavily para buscar: `"NOME DO LOCAL" + CIDADE + ESTADO`

Extraia o **endereço completo** do resultado (rua, número, bairro, cidade, estado).
Se houver mais de uma opção, escolha a geograficamente mais próxima do usuário,
ou apresente as opções para ele escolher.

> Exemplo: usuário em Vitória/ES pede "Leroy Merlin" →
> busca `"Leroy Merlin" Vitória ES` →
> endereço encontrado: "Av. Fernando Ferrari, 2600, Goiabeiras, Vitória, ES" →
> segue para o Passo 4.

### Passo 4 — Gerar o link

URL-encode o endereço e monte o link. Sempre inclua o estado e país no endereço
para evitar ambiguidade (cidades com nomes comuns podem existir em outros países).

### Passo 5 — Apresentar o link

Sempre use o formato markdown `[texto](url)` para o link — nunca exponha a URL crua.
Isso faz o link aparecer como texto clicável no Telegram, muito mais limpo para o usuário.

**Em conversa normal:**
```
📍 Leroy Merlin — Av. Fernando Ferrari, 2600, Goiabeiras, Vitória, ES
🗺️ [Abrir no Waze](https://waze.com/ul?q=Av.+Fernando+Ferrari%2C+2600%2C+Vit%C3%B3ria%2C+ES%2C+Brasil&navigate=yes)
```

**No briefing matinal** (quando o evento tem um local):
```
📅 *AGENDA DE HOJE*
09:00 — Reunião com Fornecedor
📍 Leroy Merlin — Av. Fernando Ferrari, 2600, Vitória, ES
🗺️ [Abrir no Waze](https://waze.com/ul?q=Av.+Fernando+Ferrari%2C+2600%2C+Vit%C3%B3ria%2C+ES%2C+Brasil&navigate=yes)
```

O resultado no Telegram é um link azul clicável com o texto "Abrir no Waze" — sem URL visível.

---

## Integração com Briefing Matinal

Quando estiver gerando um briefing e um evento da agenda tiver um campo de
localização preenchido, inclua o link do Waze automaticamente logo abaixo do
evento — sem precisar ser solicitado pelo usuário. Isso é especialmente útil
para quem consulta o briefing no celular antes de sair de casa.

Se o local do evento for o nome de um estabelecimento (não um endereço completo),
aplique o Passo 3 para descobrir o endereço real antes de gerar o link.

---

## Observações

- O link funciona em qualquer dispositivo com Waze instalado. Sem o app, abre
  o Waze no navegador.
- Sempre inclua estado e país no endereço para evitar ambiguidade.
- Vitória, ES, Brasil ≠ Victoria, Austrália ≠ Victoria, Canadá — seja específico.
- Se o usuário pedir "posto mais próximo" ou similar sem fornecer contexto de
  rota, use a cidade base do perfil dele como ponto de partida da busca.
