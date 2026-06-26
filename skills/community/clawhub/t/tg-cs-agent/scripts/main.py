"""Main entry point: wire everything together and run."""
import sys
import asyncio
from config import Config
from knowledge import KnowledgeBase
from agent import Agent
from telegram_client import TelegramClient


async def main():
    config = Config()

    # Validate config
    if not config.anthropic_api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)
    if not config.telegram_api_id or not config.telegram_api_hash:
        print("Error: TELEGRAM_API_ID / TELEGRAM_API_HASH not set")
        sys.exit(1)

    # Init components
    print("[INIT] Loading knowledge base...")
    kb = KnowledgeBase(config.knowledge_dir)
    kb.load()

    print("[INIT] Initializing agent...")
    agent = Agent(config, kb)

    print("[INIT] Connecting to Telegram...")
    tg = TelegramClient(config)
    await tg.connect()

    me = await tg.get_me()
    print(f"[INIT] Logged in as: {me.get('name', 'unknown')} ({me.get('id', '')})")

    async def on_message(chat_id: str, sender_id: str, text: str):
        # Skip own messages
        if sender_id == str(tg.my_id):
            return

        # Commands
        if text.strip().lower() == "/clear":
            agent.clear_history(chat_id)
            await tg.send(chat_id, "✅ Conversation history cleared.")
            return

        if text.strip().lower() == "/help":
            await tg.send(chat_id, (
                "🤖 Customer Service Bot\n\n"
                "Ask me anything about our project.\n"
                "/clear - Clear conversation history\n"
                "/human - Request human support\n"
                "/help - Show this message"
            ))
            return

        if text.strip().lower() == "/human":
            await _handoff(tg, config, chat_id, sender_id, text="User requested human support")
            await tg.send(chat_id, "🙋 已通知人工客服，稍后会有专人联系您。")
            return

        # Agent response
        print(f"[MSG] {sender_id} in {chat_id}: {text[:80]}")
        try:
            await tg.set_typing(chat_id, True)
            result = agent.chat(chat_id, text)
            await tg.set_typing(chat_id, False)
            await tg.send(chat_id, result["reply"])

            if result["handoff"]:
                await _handoff(tg, config, chat_id, sender_id, text)
                await tg.send(chat_id, "🙋 我已通知人工客服，稍后会有专人为您服务。")

        except Exception as e:
            print(f"[ERROR] {e}")
            await tg.send(chat_id, "⚠️ Sorry, something went wrong. Please try again or type /human for support.")

    print("[READY] Listening for messages...")
    await tg.listen(on_message)


async def _handoff(tg: TelegramClient, config: Config, chat_id: str, sender_id: str, text: str):
    """Notify human agent about escalation."""
    if not config.handoff_chat_id:
        print("[HANDOFF] No handoff_chat_id configured, skipping")
        return

    notice = (
        f"🚨 Human support requested\n"
        f"Chat: {chat_id}\n"
        f"User: {sender_id}\n"
        f"Message: {text[:200]}"
    )
    await tg.send(config.handoff_chat_id, notice)
    print(f"[HANDOFF] Notified {config.handoff_chat_id}")


if __name__ == "__main__":
    asyncio.run(main())
