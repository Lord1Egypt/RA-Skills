"""Text the people around the assistant read, in Portuguese and English.

Every string follows the platform's customer-copy standards: written from the reader's side, one
idea per sentence, no dashes as punctuation, no internal vocabulary. A test scans them all.
"""

from __future__ import annotations

from typing import Literal

Lang = Literal["pt", "en"]

STRINGS: dict[str, dict[str, str]] = {
    "connected_number_warning": {
        "pt": (
            "O número conectado é o do celular, ou do WhatsApp Web, de quem atende os clientes. "
            "Se ele for administrador, qualquer atendente com o aparelho passa a ensinar o "
            "assistente, apagar clientes, mudar o modo e cadastrar outros administradores. "
            "O mais seguro é cadastrar como administradores os números pessoais de quem decide "
            "pelo negócio (o seu, por exemplo) e deixar o número conectado só para os "
            "atendentes. A escolha é sua. Cadastrar o número conectado como administrador?"
        ),
        "en": (
            "The connected number is the one on the phone, or WhatsApp Web, of the people who "
            "answer customers. If it is an admin, any attendant holding the device can teach the "
            "assistant, erase customers, change the mode and add other admins. The safer setup "
            "is to register as admins the personal numbers of the people who decide for the "
            "business (yours, for example) and keep the connected number for attendants. It is "
            "your call. Register the connected number as an admin?"
        ),
    },
    "connected_number_refused_over_whatsapp": {
        "pt": (
            "Esse é o número conectado. Quem está com o celular passaria a ter todos os poderes "
            "de administrador, por isso só quem configurou o assistente pode cadastrá-lo. "
            "Peça a essa pessoa."
        ),
        "en": (
            "That is the connected number. Whoever holds the phone would get every admin power, "
            "so only the person who set up the assistant can register it. Ask that person."
        ),
    },
    "update_notice": {
        "pt": "Há uma versão nova do atendente virtual: {latest} (a instalada é {installed}). Para atualizar: {command}",
        "en": "There is a new version of the virtual attendant: {latest} (installed: {installed}). To update: {command}",
    },
    "update_hint_claude_code": {
        "pt": "claude plugin marketplace update turbo-notify && claude plugin update turbo-notify@turbo-notify (depois reinicie o Claude Code)",
        "en": "claude plugin marketplace update turbo-notify && claude plugin update turbo-notify@turbo-notify (then restart Claude Code)",
    },
    "update_hint_claude_desktop": {
        "pt": "no Claude Desktop ou no Cowork, o marketplace sincroniza pelo repositório; se a versão nova não aparecer, remova o marketplace turbo-notify em Plugins e adicione de novo",
        "en": "in Claude Desktop or Cowork, the marketplace syncs from the repository; if the new version does not show up, remove the turbo-notify marketplace under Plugins and add it again",
    },
    "update_hint_codex": {
        "pt": "codex plugin marketplace upgrade && codex plugin add turbo-notify@turbo-notify",
        "en": "codex plugin marketplace upgrade && codex plugin add turbo-notify@turbo-notify",
    },
    "update_hint_antigravity": {
        "pt": "agy plugin install https://github.com/turbo-notify/agent-skills",
        "en": "agy plugin install https://github.com/turbo-notify/agent-skills",
    },
    "draft_notice": {
        "pt": "Rascunho #{n} para {name} ({number}):\n{text}\nPara enviar: /enviar {n}. Para trocar o texto: /enviar {n} <novo texto>.",
        "en": "Draft #{n} for {name} ({number}):\n{text}\nTo send it: /send {n}. To change the text: /send {n} <new text>.",
    },
    "gap_notice": {
        "pt": "O assistente ficou fora do ar de {start} até {end}. Mensagens desse período podem ter se perdido: confira as conversas.",
        "en": "The assistant was offline from {start} to {end}. Messages from that period may be missing: check the conversations.",
    },
    "foreign_notice": {
        "pt": "Chegou um evento de outro número que não é o deste atendimento. Ignorei. Se isso se repetir, confira a configuração.",
        "en": "An event arrived from a number other than this service's. I ignored it. If it keeps happening, check the setup.",
    },
    "greeting_default": {
        "pt": "Olá! Sou o atendente virtual de {business}. Como posso ajudar?",
        "en": "Hi! I am the virtual attendant of {business}. How can I help?",
    },
    "handoff_default": {
        "pt": (
            "Vou pedir para uma pessoa da equipe continuar essa conversa com você. "
            "Ela responde assim que puder."
        ),
        "en": (
            "I will ask someone on the team to continue this conversation with you. "
            "They will reply as soon as they can."
        ),
    },
    "ai_disclosure": {
        "pt": "Sou o assistente virtual deste negócio, uma inteligência artificial.",
        "en": "I am this business's virtual assistant, an AI.",
    },
    "dnc_default": {
        "pt": "Tudo bem, não vou mais enviar mensagens por aqui.",
        "en": "Okay, I will not send you more messages here.",
    },
    "escalation_notice": {
        "pt": (
            "Uma pessoa precisa assumir o atendimento de {name} ({number}).\n"
            "Motivo: {reason}\nResumo: {summary}\nÚltima mensagem: {last}\n"
            "Para devolver ao assistente depois, envie /retomar."
        ),
        "en": (
            "A person needs to take over {name} ({number}).\n"
            "Reason: {reason}\nSummary: {summary}\nLast message: {last}\n"
            "To hand it back to the assistant later, send /resume."
        ),
    },
    "escalation_reminder": {
        "pt": "Lembrete: {name} ({number}) espera uma pessoa há {hours} horas.",
        "en": "Reminder: {name} ({number}) has been waiting for a person for {hours} hours.",
    },
    "auto_resumed": {
        "pt": "O atendimento de {name} ({number}) voltou para o atendente virtual: nenhuma pessoa escreveu há {minutes} minutos.",
        "en": "{name} ({number}) is back with the virtual attendant: no person has written for {minutes} minutes.",
    },
    "contact_paused": {
        "pt": (
            "Pausei o atendimento de {number}. Motivo: {reason}. "
            "Para voltar a responder, envie /retomar."
        ),
        "en": ("I paused {number}. Reason: {reason}. To start answering again, send /resume."),
    },
    "send_failure_notice": {
        "pt": "Não consegui enviar mensagens: {cause}. Tentar de novo agora não adianta.",
        "en": "I could not send messages: {cause}. Trying again now will not help.",
    },
    "cause_contact_quota_exceeded": {
        "pt": "o limite de contatos diferentes do plano neste ciclo foi atingido",
        "en": "the plan's limit of different contacts for this billing cycle was reached",
    },
    "cause_messages_quota_exceeded": {
        "pt": "o limite de mensagens do plano neste ciclo foi atingido",
        "en": "the plan's message limit for this billing cycle was reached",
    },
    "cause_payment_required": {
        "pt": "há um pagamento pendente na conta",
        "en": "the account has a payment pending",
    },
    "cause_feature_not_available": {
        "pt": "este recurso não está incluído no plano",
        "en": "this feature is not included in the plan",
    },
    "cause_insufficient_scope": {
        "pt": "a chave não tem permissão para enviar mensagens",
        "en": "the key does not have permission to send messages",
    },
    "reason_repeated_messages": {
        "pt": "as mensagens se repetem, como as de um robô",
        "en": "the messages repeat, like a bot's",
    },
    "reason_rate_cap": {
        "pt": "passou do limite de respostas por período",
        "en": "too many replies in a short period",
    },
    "reply_blocked_notice": {
        "pt": "Bloqueei uma resposta para {number} para proteger {why}. Nada foi enviado.",
        "en": "I blocked a reply to {number} to protect {why}. Nothing was sent.",
    },
    "reason_reply_blocked": {
        "pt": "uma resposta foi bloqueada para proteger {why}",
        "en": "a reply was blocked to protect {why}",
    },
    "egress_other_contact": {"pt": "dados de outro cliente", "en": "another customer's data"},
    "egress_non_public": {"pt": "informação interna", "en": "internal information"},
    "egress_personal_data": {"pt": "dados pessoais", "en": "personal data"},
    "egress_credential": {"pt": "uma credencial", "en": "a credential"},
    "blocked_draft": {"pt": "[bloqueado: {why}]", "en": "[blocked: {why}]"},
    "reason_decision_unreadable": {
        "pt": "a resposta do assistente não pôde ser lida duas vezes seguidas",
        "en": "the assistant's answer could not be read twice in a row",
    },
    "reason_empty_decision": {
        "pt": "o assistente não soube como responder",
        "en": "the assistant did not know how to answer",
    },
    "reason_silence_refused": {
        "pt": "a mensagem do cliente tem mais do que um agradecimento e o assistente não respondeu",
        "en": "the customer's message has more than a thank you, and the assistant did not answer",
    },
}


def t(key: str, lang: Lang, **fields: str) -> str:
    """The text for ``key`` in ``lang`` with ``fields`` filled in."""
    return STRINGS[key][lang].format(**fields)


from tn_assist.i18n_console import CONSOLE_STRINGS  # noqa: E402

STRINGS.update(CONSOLE_STRINGS)
