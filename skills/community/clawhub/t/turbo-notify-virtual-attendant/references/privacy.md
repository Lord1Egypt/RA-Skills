# Privacy

The business that runs the assistant decides what is done with its customers' data, and the data stays on the machine where the workspace is. Turbo Notify does not receive a copy.

## Notice to give the person who sets it up

Portuguese:

> O atendente virtual guarda neste computador as conversas com os seus clientes, a ficha de cada um e o que você ensinar sobre o negócio, na pasta que escolhemos juntos. Quem tem acesso a essa pasta vê tudo isso. O texto das conversas com os clientes fica guardado por 90 dias e depois é apagado; o resumo das conversas e a ficha do cliente ficam até você usar `/esquecer`. Você pode apagar os dados de um cliente quando ele pedir, com `/esquecer`, e exportar o que há sobre ele. A política de privacidade da sua empresa deve dizer que você usa um atendimento automatizado, e o assistente se apresenta como atendente virtual sempre que perguntam. O que o Turbo Notify guarda do seu lado segue o prazo do seu plano.

English:

> The virtual attendant keeps your customers' conversations, each customer's file and what you teach it about the business on this computer, in the folder we chose together. Anyone with access to that folder sees all of it. The text of customer conversations is kept for 90 days and then deleted; the summary of the conversations and each customer's file stay until you use `/forget`. You can erase a customer's data when they ask, with `/forget`, and export what is held about them. Your company's privacy policy should say that you use an automated assistant, and the assistant says it is an AI in the first answer of every chat, and again whenever it is asked. What Turbo Notify keeps on its side follows your plan's retention.

## What the helper does

- Folders are private to the user (mode 700), files too (600). Nothing is written outside the workspace.
- No credential is stored in the workspace or in logs.
- Retention of the transcript: `raw_retention_days` in `memory-policy.json`, 90 by default. `tn_assist purge` applies it.
- Export: `tn_assist export --contact <number>`. Erase: `/esquecer <number>` or `tn_assist forget --contact <number>`. The erase leaves one line in the audit log (who, which number, when), and nothing else about the customer.
- The assistant never says it is a person. Asked, it says it is a virtual attendant.
- It does not write to customers who have not written first, and it stops for anyone who asks.

## What to tell the person

The workspace is as safe as the computer and the account that hold it. Recommend disk encryption, a lock screen, and ending the WhatsApp Web sessions of anyone who leaves the team.
