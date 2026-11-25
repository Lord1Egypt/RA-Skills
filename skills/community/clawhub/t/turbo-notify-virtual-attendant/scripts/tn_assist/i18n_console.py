"""Texts of the WhatsApp console (administrators and attendants). Same standards as i18n.py."""

from __future__ import annotations

CONSOLE_STRINGS: dict[str, dict[str, str]] = {
    "console_unreadable": {
        "pt": "Não consegui responder a essa mensagem. Tente de novo ou envie /ajuda para ver os comandos.",
        "en": "I could not answer that message. Try again, or send /help to see the commands.",
    },
    "help_header": {"pt": "Comandos que você pode usar:", "en": "Commands you can use:"},
    "help_help": {"pt": "/ajuda: mostra esta lista", "en": "/help: shows this list"},
    "help_status": {
        "pt": "/status: situação do atendimento",
        "en": "/status: how the service is doing",
    },
    "help_queue": {
        "pt": "/fila: quem espera uma pessoa e os rascunhos",
        "en": "/queue: who is waiting for a person, and the drafts",
    },
    "help_send": {
        "pt": "/enviar <n> [texto]: envia o rascunho n, ou o seu texto no lugar",
        "en": "/send <n> [text]: sends draft n, or your text instead",
    },
    "help_digest": {
        "pt": "/resumo: resumo das conversas",
        "en": "/digest: summary of the conversations",
    },
    "help_resume": {
        "pt": "/retomar [n ou número]: devolve a conversa ao assistente",
        "en": "/resume [n or number]: hands the conversation back to the assistant",
    },
    "help_takeover": {
        "pt": "/assumir <n ou número>: uma pessoa assume a conversa",
        "en": "/takeover <n or number>: a person takes the conversation",
    },
    "help_contact": {
        "pt": "/cliente <número ou nome>: ficha do cliente",
        "en": "/contact <number or name>: the customer's file",
    },
    "help_thread": {
        "pt": "/conversa <número> [n]: últimas mensagens",
        "en": "/thread <number> [n]: latest messages",
    },
    "help_note": {
        "pt": "/nota <número> <texto>: guarda uma anotação sobre o cliente",
        "en": "/note <number> <text>: saves a note about the customer",
    },
    "help_contacts": {
        "pt": "/clientes [filtro]: lista de clientes",
        "en": "/contacts [filter]: list of customers",
    },
    "help_admins": {"pt": "/admins: quem administra", "en": "/admins: who administers"},
    "help_admin_add": {
        "pt": "/admin add <número> [nome]: cadastra um administrador",
        "en": "/admin add <number> [name]: registers an admin",
    },
    "help_admin_remove": {
        "pt": "/admin remover <número>: remove um administrador",
        "en": "/admin remove <number>: removes an admin",
    },
    "help_teach": {
        "pt": "/ensinar <tema>: ensina algo sobre o negócio (depois /pronto, e /publico ou /interno)",
        "en": "/teach <topic>: teaches something about the business (then /done, and /public or /internal)",
    },
    "help_kb": {
        "pt": "/conhecimento [tema]: o que o assistente sabe (/conhecimento remover <tema> apaga)",
        "en": "/kb [topic]: what the assistant knows (/kb remove <topic> deletes)",
    },
    "help_sources": {
        "pt": "/fontes [nome classe]: outros sistemas que o assistente pode consultar",
        "en": "/sources [name class]: other systems the assistant may consult",
    },
    "help_pause": {
        "pt": "/pausar [número]: pausa o assistente",
        "en": "/pause [number]: pauses the assistant",
    },
    "help_forget": {
        "pt": "/esquecer <número>: apaga os dados do cliente",
        "en": "/forget <number>: erases the customer's data",
    },
    "help_mode": {
        "pt": "/modo assistido|automático: escolhe se o assistente espera aprovação",
        "en": "/mode assist|auto: chooses whether the assistant waits for approval",
    },
    "help_policy": {
        "pt": "/politica: números da memória do assistente",
        "en": "/policy: the assistant's memory numbers",
    },
    "help_lang": {
        "pt": "/idioma pt|en: idioma dos comandos",
        "en": "/lang pt|en: language of the commands",
    },
    "refused_admin_only": {
        "pt": "Esse comando é só para administradores. Você pode usar:\n{allowed}",
        "en": "That command is for admins only. You can use:\n{allowed}",
    },
    "mode_assist": {"pt": "assistido", "en": "assisted"},
    "mode_auto": {"pt": "automático", "en": "automatic"},
    "paused_suffix": {"pt": " (pausado)", "en": " (paused)"},
    "status_text": {
        "pt": (
            "Último ciclo: {last}\nNa fila: {backlog}\nEsperando uma pessoa: {waiting}\n"
            "Rascunhos: {drafts}\nModo: {mode}{paused}\nVersão: {version}"
        ),
        "en": (
            "Last cycle: {last}\nIn the queue: {backlog}\nWaiting for a person: {waiting}\n"
            "Drafts: {drafts}\nMode: {mode}{paused}\nVersion: {version}"
        ),
    },
    "status_never": {"pt": "ainda nenhum", "en": "none yet"},
    "status_connected_admin": {
        "pt": "O número conectado também é administrador.",
        "en": "The connected number is also an admin.",
    },
    "queue_empty": {
        "pt": "Ninguém espera uma pessoa agora.",
        "en": "Nobody is waiting for a person now.",
    },
    "queue_waiting": {"pt": "Esperando uma pessoa:", "en": "Waiting for a person:"},
    "queue_entry": {
        "pt": "{n}. {name} ({number}): {reason}",
        "en": "{n}. {name} ({number}): {reason}",
    },
    "queue_drafts": {"pt": "Rascunhos:", "en": "Drafts:"},
    "queue_draft": {"pt": "#{n} para {name}: {text}", "en": "#{n} for {name}: {text}"},
    "resume_done": {
        "pt": "Pronto, {name} volta a ser atendido pelo assistente.",
        "en": "Done, {name} is back with the assistant.",
    },
    "resume_all_done": {
        "pt": "O assistente voltou a responder a todos.",
        "en": "The assistant is answering everyone again.",
    },
    "resume_need_queue": {
        "pt": "Envie /fila para ver as posições e depois /retomar <posição>.",
        "en": "Send /queue to see the positions, then /resume <position>.",
    },
    "resume_nobody": {"pt": "Ninguém para retomar agora.", "en": "Nobody to resume now."},
    "takeover_done": {
        "pt": "{name} fica com uma pessoa. O assistente não responde mais a essa conversa até /retomar.",
        "en": "{name} stays with a person. The assistant stops answering this chat until /resume.",
    },
    "not_found": {
        "pt": "Não encontrei esse cliente. Use o número com DDD ou parte do nome.",
        "en": "I did not find that customer. Use the number with area code or part of the name.",
    },
    "ambiguous": {
        "pt": "Mais de um cliente combina: {names}. Use o número.",
        "en": "More than one customer matches: {names}. Use the number.",
    },
    "contact_header": {
        "pt": "{name} ({number}) | estado: {state} | idioma: {language}",
        "en": "{name} ({number}) | state: {state} | language: {language}",
    },
    "contact_no_facts": {"pt": "Nenhum fato guardado.", "en": "No facts saved."},
    "contact_recent": {"pt": "Últimas mensagens:", "en": "Latest messages:"},
    "who_contact": {"pt": "cliente", "en": "customer"},
    "who_assistant": {"pt": "assistente", "en": "assistant"},
    "who_attendant": {"pt": "atendente", "en": "attendant"},
    "who_other": {"pt": "sistema", "en": "system"},
    "thread_empty": {"pt": "Nenhuma mensagem guardada.", "en": "No messages saved."},
    "note_saved": {"pt": "Anotação guardada para {name}.", "en": "Note saved for {name}."},
    "contacts_empty": {"pt": "Nenhum cliente ainda.", "en": "No customers yet."},
    "contacts_line": {"pt": "{name} ({number}): {state}", "en": "{name} ({number}): {state}"},
    "admins_list": {"pt": "Administradores:\n{lines}", "en": "Admins:\n{lines}"},
    "admin_added": {"pt": "{number} agora é administrador.", "en": "{number} is now an admin."},
    "admin_exists": {"pt": "{number} já é administrador.", "en": "{number} is already an admin."},
    "admin_removed": {
        "pt": "{number} deixou de ser administrador.",
        "en": "{number} is no longer an admin.",
    },
    "admin_unknown": {"pt": "{number} não é administrador.", "en": "{number} is not an admin."},
    "admin_last": {
        "pt": "Esse é o último administrador. Cadastre outro antes de remover.",
        "en": "That is the last admin. Register another before removing.",
    },
    "invalid_number": {
        "pt": "Esse número não parece certo. Use o número com DDD, só dígitos.",
        "en": "That number does not look right. Use the number with area code, digits only.",
    },
    "confirm_ask": {
        "pt": "Isso não pode ser desfeito. Para confirmar, envie /confirmar {code} em até 10 minutos.",
        "en": "This cannot be undone. To confirm, send /confirm {code} within 10 minutes.",
    },
    "confirm_resume": {
        "pt": "{name} ({number}) pediu para não receber mensagens. Para devolver o cliente ao atendimento, envie /confirmar {code} em até 10 minutos.",
        "en": "{name} ({number}) asked to stop receiving messages. To put the customer back in service, send /confirm {code} within 10 minutes.",
    },
    "confirm_invalid": {
        "pt": "Esse código não vale. Envie o comando de novo para receber outro.",
        "en": "That code is not valid. Send the command again to get a new one.",
    },
    "teach_started": {
        "pt": "Pode contar sobre {topic}. Quando terminar, envie /pronto.",
        "en": "Go ahead and tell me about {topic}. When you finish, send /done.",
    },
    "teach_none": {
        "pt": "Nada em andamento. Comece com /ensinar <tema>.",
        "en": "Nothing in progress. Start with /teach <topic>.",
    },
    "teach_got": {"pt": "Anotado.", "en": "Noted."},
    "teach_filed": {
        "pt": "Guardei em {path}, por enquanto só para uso interno. É para os clientes? Envie /publico ou /interno.",
        "en": "Saved in {path}, internal for now. Is it for customers? Send /public or /internal.",
    },
    "teach_public": {
        "pt": "Agora {path} faz parte do que o assistente diz aos clientes.",
        "en": "{path} is now part of what the assistant tells customers.",
    },
    "teach_internal": {
        "pt": "{path} fica só para uso interno.",
        "en": "{path} stays internal.",
    },
    "kb_header": {"pt": "O que o assistente sabe:", "en": "What the assistant knows:"},
    "kb_line": {
        "pt": "{path} ({visibility}): {description}",
        "en": "{path} ({visibility}): {description}",
    },
    "kb_public": {"pt": "clientes", "en": "customers"},
    "kb_internal": {"pt": "interno", "en": "internal"},
    "kb_missing": {"pt": "Não achei esse assunto.", "en": "I did not find that topic."},
    "kb_removed": {"pt": "{path} foi apagado.", "en": "{path} was deleted."},
    "sources_empty": {
        "pt": "Nenhum outro sistema foi encontrado.",
        "en": "No other systems were found.",
    },
    "sources_line": {"pt": "{name}: {cls} ({mode})", "en": "{name}: {cls} ({mode})"},
    "sources_changed": {"pt": "{name} agora é {cls}.", "en": "{name} is now {cls}."},
    "sources_unknown": {
        "pt": "Não conheço o sistema {name}.",
        "en": "I do not know the system {name}.",
    },
    "sources_write": {
        "pt": "Essa ferramenta altera dados e não pode ser usada.",
        "en": "That tool changes data and cannot be used.",
    },
    "sources_class_help": {
        "pt": "Classes: publica, interna, admin, desligada.",
        "en": "Classes: public, internal, admin, off.",
    },
    "cls_public": {"pt": "pública", "en": "public"},
    "cls_internal": {"pt": "interna", "en": "internal"},
    "cls_admin_only": {"pt": "só administradores", "en": "admins only"},
    "cls_off": {"pt": "desligada", "en": "off"},
    "paused_all": {
        "pt": "O assistente parou de responder. Para voltar, envie /retomar todos.",
        "en": "The assistant stopped answering. To bring it back, send /resume all.",
    },
    "paused_one": {
        "pt": "{name} está pausado. Para voltar, envie /retomar.",
        "en": "{name} is paused. To bring it back, send /resume.",
    },
    "forgotten": {
        "pt": (
            "Apaguei os dados de {number} que o assistente guardava. "
            "O que a plataforma ainda mantém segue o prazo do seu plano."
        ),
        "en": (
            "I erased the data the assistant kept about {number}. "
            "Whatever the platform still holds follows your plan's retention."
        ),
    },
    "mode_set": {"pt": "Modo {mode}.", "en": "Mode: {mode}."},
    "mode_help": {
        "pt": "Use /modo assistido (espera aprovação) ou /modo automático (responde sozinho).",
        "en": "Use /mode assist (waits for approval) or /mode auto (answers by itself).",
    },
    "mode_auto_unavailable": {
        "pt": "Neste aplicativo o atendente só funciona no modo assistido: uma pessoa aprova cada resposta. O modo automático é do Claude Code e do Codex, com o executor.",
        "en": "In this app the attendant only works in assisted mode: a person approves every answer. Automatic mode is for Claude Code and Codex, with the runner.",
    },
    "lang_set": {"pt": "Idioma: português.", "en": "Language: English."},
    "lang_help": {"pt": "Use /idioma pt ou /idioma en.", "en": "Use /lang pt or /lang en."},
    "policy_text": {
        "pt": (
            "Orçamento do pacote do cliente: {contact} tokens\nOrçamento do pacote do administrador: {admin} tokens\n"
            "Mensagens guardadas por {days} dias\nRespostas por hora: {per_hour}, por dia: {per_day}\n"
            "Lembrete de transferência: {reminder} horas\nDevolver ao atendente virtual sozinho: {resume}\nPropostas de melhoria: {proposals}"
        ),
        "en": (
            "Customer pack budget: {contact} tokens\nAdmin pack budget: {admin} tokens\n"
            "Messages kept for {days} days\nReplies per hour: {per_hour}, per day: {per_day}\n"
            "Hand-off reminder: {reminder} hours\nGive a conversation back by itself: {resume}\nImprovement proposals: {proposals}"
        ),
    },
    "digest_text": {
        "pt": (
            "Clientes: {total}\nAtivos: {active}\nEsperando uma pessoa: {handoff}\nPausados: {paused}\n"
            "Pediram para não receber mensagens: {dnc}\nMensagens hoje: {today}\nRascunhos: {drafts}"
        ),
        "en": (
            "Customers: {total}\nActive: {active}\nWaiting for a person: {handoff}\nPaused: {paused}\n"
            "Asked not to be contacted: {dnc}\nMessages today: {today}\nDrafts: {drafts}"
        ),
    },
    "resume_all_admin_only": {
        "pt": "Só um administrador pode voltar a atender todos de uma vez.",
        "en": "Only an admin can bring the assistant back for everyone at once.",
    },
    "dnc_admin_only": {
        "pt": "{name} pediu para não receber mensagens. Só um administrador pode desfazer isso.",
        "en": "{name} asked not to receive messages. Only an admin can undo that.",
    },
    "dnc_blocked": {
        "pt": "{name} pediu para não receber mensagens. Nada foi enviado.",
        "en": "{name} asked not to receive messages. Nothing was sent.",
    },
    "paused_admin_only": {
        "pt": "O assistente está pausado. Só um administrador pode enviar agora.",
        "en": "The assistant is paused. Only an admin can send right now.",
    },
    "suggest_command": {
        "pt": "Para fazer isso, envie você mesmo: {command}",
        "en": "To do this, send it yourself: {command}",
    },
    "send_done": {"pt": "Enviando para {name}.", "en": "Sending to {name}."},
    "send_unknown": {
        "pt": "Não existe o rascunho {n}. Veja /fila.",
        "en": "There is no draft {n}. See /queue.",
    },
    "send_blocked": {
        "pt": "Esse rascunho foi bloqueado para proteger dados. Envie /enviar {n} com o seu texto no lugar.",
        "en": "That draft was blocked to protect data. Send /send {n} with your own text instead.",
    },
    "send_needs_number": {
        "pt": "Qual rascunho? Use /enviar <n>.",
        "en": "Which draft? Use /send <n>.",
    },
    "usage": {
        "pt": "Faltou algo nesse comando. Veja /ajuda.",
        "en": "Something is missing in that command. See /help.",
    },
}
