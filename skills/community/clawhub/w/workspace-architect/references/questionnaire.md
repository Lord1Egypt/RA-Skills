# Guided Creation Questionnaire

## Overview

This document contains structured questionnaires for creating each workspace file. Use these questions to understand user needs before creating files.

---

## Universal Pre-Screening Questions

Before starting file creation, ask:

1. **What is the agent's primary purpose?**
   - What problem does it solve?
   - Who is the primary user?

2. **What is the agent's role?**
   - Personal assistant?
   - Technical helper?
   - Emotional support?
   - Business automation?
   - Creative assistant?

3. **What tools/capabilities should it have?**
   - Email?
   - Calendar?
   - Web browsing?
   - File operations?
   - Messaging?

4. **Who will use this agent?**
   - Just you?
   - Multiple people?
   - Specific role (CEO, developer, etc.)?

---

## SOUL.md Questionnaire

### Purpose Discovery

1. **Core Purpose**
   - What is the ONE thing this agent must do above all else?
   - What would failure look like?
   - What would success look like?

2. **Trust Boundaries**
   - What information sources should the agent trust?
   - What information sources should it be cautious about?
   - Should it trust web content? Emails from unknown senders? User input?

3. **Capability Limits**
   - What actions MUST the agent be able to do?
   - What actions MUST the agent NEVER do?
   - What actions require your explicit approval?

4. **Security Requirements**
   - What information must NEVER be revealed?
   - What information must NEVER be stored?
   - Are there specific tools that require extra caution?

5. **Approval Rules**
   - Should it ask before sending emails?
   - Should it ask before making file changes?
   - Should it ask before sharing any information?

### Example Questions to Ask:

```
"Seu agente pode enviar emails sozinho ou precisa da sua aprovação?"
"Seu agente pode apagar arquivos ou precisa pedir confirmação?"
"Qual informação você NUNCA quer que o agente compartilhe?"
"O agente pode fazer compras/transações em seu nome?"
"De onde o agente pode confiar informações? Web, emails, qualquer lugar?"
```

---

## IDENTITY.md Questionnaire

### Personality Discovery

1. **Name**
   - What should the agent be called?
   - Is this name meaningful/significant?

2. **Personality Traits** (ask for 3-5)
   - How would you describe the agent's personality?
   - Is it formal or informal?
   - Is it serious or playful?
   - Is it concise or detailed?
   - Is it proactive or reactive?

3. **Signature**
   - Does the agent have a catchphrase or emoji?
   - How should it sign off messages?

4. **Tone**
   - How should it address you? (Formal "você", informal "tu", first name?)
   - Should it use emojis?
   - How casual/technical should it be?

5. **Self-Description**
   - How would the agent introduce itself in one sentence?

### Example Questions to Ask:

```
"Qual nome você quer dar ao seu agente?"
"Como você descreveria a personalidade dele em 3 adjetivos?"
"O agente deve ser mais formal ou informal?"
"O agente deve usar emojis nas respostas?"
"Como o agente deve se referir a você? (Nome, 'você', 'chefe'?)"
"Tem alguma frase ou emoji que você quer que seja a marca do agente?"
```

---

## USER.md Questionnaire

### Profile Discovery

1. **Basic Info**
   - What should I call you?
   - What do you do professionally?
   - Where are you located? (timezone matters!)
   - What language do you prefer?

2. **Goals** (ask for 2-3)
   - What are your main goals for the next 6-12 months?
   - What are you trying to achieve?
   - What would make this agent successful for you?

3. **Communication Preferences**
   - Do you prefer detailed or concise responses?
   - Do you want explanations or just results?
   - Do you want options/recommendations or direct answers?
   - Do you prefer bulleted lists or paragraphs?

4. **Risk Tolerance**
   - Should the agent be cautious or aggressive?
   - Is it okay to make assumptions?
   - Should it double-check before acting?

5. **Approval Preferences**
   - When should the agent ask for permission?
   - What can it do autonomously?
   - What specific actions require your approval?

6. **Technical Level**
   - How comfortable are you with technical terms?
   - Do you want code examples or plain language?
   - Do you want step-by-step explanations?

### Example Questions to Ask:

```
"Qual seu nome e como prefere ser chamado?"
"Qual sua profissão/área de atuação?"
"Em que fuso horário você está?"
"Quais são suas 3 principais metas para este ano?"
"Você prefere respostas curtas ou detalhadas?"
"Você quer que o agente explique o 'porquê' ou só mostre o resultado?"
"Em que situações você quer ser consultado antes de uma ação?"
"Você prefere comunicação formal ou informal?"
"Qual seu nível de familiaridade com tecnologia?"
"Você quer ver código ou prefere explicações em linguagem simples?"
```

---

## MEMORY.md Questionnaire

### Environment Discovery

1. **Environment**
   - What system/environment will the agent work with?
   - Are there specific servers, tools, or platforms?
   - What software versions are relevant?

2. **Stable Preferences**
   - What preferences DON'T change frequently?
   - What are your standing rules/decisions?

3. **Active Projects**
   - What projects are you currently working on?
   - What's the status of each?

4. **Important Dates**
   - Any recurring dates to remember?
   - Birthdays, anniversaries, deadlines?

5. **Constraints**
   - Any technical constraints?
   - Time constraints?
   - Budget constraints?

### Example Questions to Ask:

```
"Vocês tem algum servidor ou sistema específico que o agente vai interagir?"
"Tem alguma preferência sua que é fixa, que quase nunca muda?"
"Quais projetos você está trabalhando agora?"
"Tem datas importantes que o agente deve lembrar?"
"Tem alguma restrição técnica ou de tempo que o agente deve considerar?"
"Existe alguma decisão que você já tomou que o agente deve seguir?"
```

---

## TOOLS.md Questionnaire

### Tool Discovery

1. **Available Tools**
   - What tools will the agent have access to?
   - Email? Calendar? Browser? Files?
   - Specific APIs or services?

2. **Tool Rules**
   - Are there tools that should only be used for specific purposes?
   - Any tools that need approval before use?
   - Any tools that should NEVER be used?

3. **Tool Documentation**
   - For each tool, what does it do?
   - What's the basic syntax?
   - When should it be used?

### Example Questions to Ask:

```
"Quais ferramentas o agente terá acesso? (Email, calendário, navegador...)"
"Tem alguma ferramenta que só pode ser usada em situações específicas?"
"Quais ferramentas precisam da sua aprovação antes de usar?"
"Precisa de alguma ferramenta específica integrada?"
```

---

## AGENTS.md Questionnaire

### Behavior Discovery

1. **Heartbeat/Proactivity**
   - Should the agent check for things periodically?
   - What should it monitor automatically?
   - How often should it check?

2. **Group Behavior**
   - Will the agent be used in group chats?
   - Should it respond to everyone or just you?
   - How should it identify messages meant for it?

3. **Other Agents**
   - Are there other agents in the system?
   - How should this agent interact with them?
   - When should it escalate to another agent?

4. **Priorities**
   - What's most important?
   - What should be prioritized when multiple things are happening?

### Example Questions to Ask:

```
"O agente vai ser usado em grupos? Como ele deve se comportar?"
"Tem outros agentes no sistema? Como eles devem interagir?"
"O que o agente deve monitorar automaticamente?"
"Quais são as prioridades quando várias coisas acontecem ao mesmo tempo?"
"Com que frequência o agente deve verificar tarefas automáticas?"
```

---

## STYLE.md Questionnaire

### Style Discovery

1. **Response Patterns**
   - For simple questions: how should it respond?
   - For complex tasks: how should it structure the response?
   - For emotional content: how should it react?

2. **Formatting Preferences**
   - Use emoji? When? Which ones?
   - Use markdown formatting? Headers, lists?
   - Use code blocks? When?

3. **Language Register**
   - Formal or informal language?
   - Technical or simple language?
   - Direct or conversational?

4. **Do's and Don'ts**
   - What should it always do?
   - What should it never do?
   - How should it handle uncertainty?

5. **Examples**
   - Can you give an example of a good response?
   - Can you give an example of a bad response?

### Example Questions to Ask:

```
"Como você quer que o agente responda perguntas simples?"
"E para tarefas complexas, como deve ser a estrutura da resposta?"
"O agente deve usar emojis? Quais e quando?"
"Prefere linguagem técnica ou simples?"
"O que o agente NUNCA deve fazer nas respostas?"
"Como o agente deve reagir quando não souber algo?"
"Pode me dar um exemplo de uma resposta que você consideraria boa?"
"Pode me dar um exemplo de uma resposta que você NÃO gostaria de receber?"
```

---

## Deep Probing Questions

### For Understanding Hidden Needs

Sometimes users don't know what they need. Use probing questions:

1. **Edge Cases**
   - "E se o agente não souber como fazer algo? Deve perguntar, tentar, ou ignorar?"
   - "E se tiver conflito entre duas tarefas? Qual prevalece?"
   - "E se você não estiver disponível e o agente precisar tomar uma decisão?"

2. **Error Handling**
   - "Como o agente deve responder quando erra?"
   - "Como o agente deve pedir desculpas (ou não)?"
   - "O agente deve admitir incertezas ou tentar ocultar?"

3. **Boundaries**
   - "Tem algum assunto que o agente não deve comentar?"
   - "Tem algum tipo de brincadeira/piada que o agente não deve fazer?"
   - "Até onde vai a iniciativa do agente?"

4. **Integration**
   - "O agente vai trabalhar com outros sistemas? Quais?"
   - "Tem integrações específicas que você precisa?"
   - "O agente vai precisar reportar para alguém?"

5. **Growth**
   - "Como você imagina o agente daqui a 6 meses?"
   - "Quais capacidades você quer adicionar depois?"

---

## Question Flow Strategy

### Phase 1: Broad Understanding (2-3 questions)
- Purpose
- Role
- User

### Phase 2: Specific Capabilities (3-5 questions)
- What can/cannot do
- Tools needed
- Approval rules

### Phase 3: Personality & Style (3-5 questions)
- Name and personality
- Communication style
- Formatting

### Phase 4: Edge Cases & Refinement (2-3 questions)
- Error handling
- Boundaries
- Growth plans

---

## Minimum Viable Questionnaire

If user wants quick setup, ask minimum:

1. **Purpose**: "Qual o objetivo principal do agente?"
2. **User**: "Qual seu nome e timezone?"
3. **Role**: "O agente será: assistente pessoal, técnico, emocional, outro?"
4. **Name**: "Qual nome quer dar ao agente?"
5. **Personality**: "Personalidade em 3 adjetivos?"
6. **Approval**: "O que o agente PRECISA pedir aprovação antes de fazer?"

Then generate draft files and ask for refinements.