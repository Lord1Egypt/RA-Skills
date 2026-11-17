"""Login to an account using credential vault + 2FA human action."""
import asyncio

from ceki_browser import Browser, HumanActionDeclined, HumanActionTimeout


async def main():
    async with Browser(token="YOUR_TOKEN") as br:
        async with await br.session(
            mode="persona",
            domain_hints=["app.example.com"],
        ) as s:
            await s.navigate("https://app.example.com/login")

            await s.inject_credentials(
                secret_id="secret-abc-123",
                target={
                    "username_selector": "#email",
                    "password_selector": "#password",
                    "submit_selector": "#login-btn",
                },
            )

            try:
                result = await s.request_human_action(
                    action_type="2fa",
                    message="Please enter the 2FA code from your authenticator app",
                    timeout_sec=120,
                )
                print(f"2FA completed: {result.status}")
            except HumanActionDeclined:
                print("Provider declined the 2FA request")
            except HumanActionTimeout:
                print("Provider did not respond in time")

            page = await s.query("h1")
            print(f"Logged in. Page title: {page.text}")


if __name__ == "__main__":
    asyncio.run(main())
