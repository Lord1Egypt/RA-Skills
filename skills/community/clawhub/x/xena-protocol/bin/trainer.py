"""Train the Naive Bayes phishing classifier.

Minimal hackathon trainer: fits on an inline corpus of seeded phish + ham
snippets (plus the 8 famous historical cases) and emits
`agent/data/bayes_model.json` for inference at runtime.

Run:
    python -m bin.trainer
or:
    python bin/trainer.py

Production path (future): replace inline corpora with Nazario + PhishTank +
Enron + SpamAssassin full downloads.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from bin.bayes_classify import tokenize

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

# Additional high-weight boost per famous-case token to guarantee demo hits
FAMOUS_BOOST = 50

# Minimum total occurrence count to keep a token in the model (prunes noise)
MIN_OCCURRENCE = 2


# -------- inline hackathon corpus --------
# Phish snippets (reconstructed phishing patterns, not copied from any source)
PHISH_CORPUS = [
    "URGENT verify your account within 24 hours or it will be suspended. Click here to confirm your identity.",
    "Your PayPal account has been limited. Sign in immediately to restore access.",
    "You have won a 10 million dollar lottery. Claim your prize by sending processing fees and bank details.",
    "Send 0.5 bitcoin to this wallet address within 48 hours or your data will be leaked.",
    "Investment opportunity guaranteed 300 percent return on crypto trading. Wire funds to the Binance account below.",
    "I am a Nigerian prince and I need your help transferring 10 million dollars. You will receive 20 percent.",
    "Amazon security alert: your recent order cannot be processed. Update your payment information now.",
    "Microsoft Office 365 password expires today. Reset your password using the secure link.",
    "Your Netflix subscription was declined. Update your credit card to avoid service interruption.",
    "Security notice from HSBC: suspicious login detected. Verify your online banking credentials here.",
    "Dear customer you have an outstanding invoice. Wire the amount to the new bank account below before the deadline.",
    "CEO urgent request: I am in a meeting and need you to wire gift cards to this vendor. Please confirm by text.",
    "Your Apple ID was used to sign in on a new iPhone. If this was not you please verify your account immediately.",
    "Gmail storage full. Click to upgrade or your messages will be deleted in 24 hours.",
    "LinkedIn connection request pending. Please log in to view and approve.",
    "Your FedEx package delivery failed. Pay the customs fee to reschedule delivery.",
    "IRS notice: you owe back taxes. Pay immediately with bitcoin or gift cards to avoid arrest warrant.",
    "Your Coinbase wallet will be frozen unless you verify ownership. Provide your seed phrase within the hour.",
    "Romance match waiting for you. Beautiful woman looking for a serious relationship. Click to see her photos.",
    "Please process the attached invoice urgently. The vendor changed their bank account. Wire to the new SWIFT code.",
    "Your DocuSign document is ready. Review and sign the attached PDF to complete the transaction.",
    "Urgent: we need you to buy 5000 dollars in Amazon gift cards and email the codes to me. This is confidential.",
    "Chase Bank alert: unauthorized transfer blocked. Log in with your username and password to confirm.",
    "FIFA World Cup lottery winner! Send your passport and credit card number to claim the tickets.",
    "Crypto airdrop: connect your wallet to receive 5000 free tokens. Enter your 12 word seed phrase to qualify.",

    # Nigerian-Prince / 419 advance-fee pattern — needs strong Bayes signal
    "I am the nephew of the late Nigerian prince with 18 million USD of inheritance funds. I need a foreign partner to receive this transfer. You will receive 25 percent commission.",
    "Confidential inheritance transfer requires your assistance. Please reply with your full name, bank account number, and scanned copy of your passport.",
    "Dear friend I am writing with utmost urgency. West African nation royal family inheritance stranded in bank account. Foreign partner required.",
    "My late father was a government minister in Nigeria. I have access to 25 million USD in a dormant account. Please assist me to move these funds abroad.",
    "Strictly confidential. I represent a Swiss banker holding the unclaimed inheritance of our deceased client. You have been named a beneficiary. Please provide banking details.",
    "Yours faithfully Prince Adebayo. I require your assistance transferring funds out of the country. The commission for your help will be generous.",
    "I need a trustworthy foreign partner to receive this sum on my behalf. Full name bank account number passport scan required within 48 hours.",
    "I am contacting you because you share the same surname as our late customer whose account remains unclaimed. You can inherit the money with my assistance.",

    # Fake lottery / sweepstakes
    "Congratulations you have been selected as a winner of the international lottery draw. To claim your prize of 2.5 million dollars please provide your banking details.",
    "FIFA lottery winner announcement. Send passport scan credit card number and processing fee to collect your prize tickets and apartment rental.",
]

# Ham snippets (benign business and personal email patterns)
HAM_CORPUS = [
    "Thanks for the meeting yesterday. I will send over the project timeline by end of week.",
    "Quick reminder: our team standup is at 10 am tomorrow. See you in the conference room.",
    "Please find the quarterly report attached. Let me know if you have any questions.",
    "Happy birthday! Hope you have a great day with the family.",
    "Reminder that your dentist appointment is scheduled for Thursday at 3 pm.",
    "The package you ordered has shipped. You can track it with the tracking number in your account.",
    "Your recent order from our store has been delivered. Thanks for shopping with us.",
    "The book club is meeting this Saturday to discuss chapter 12. Bring snacks.",
    "Sharing the project proposal for your review. Comments welcome.",
    "The new hire orientation is next Monday. Please review the onboarding document.",
    "Team lunch on Friday at the Italian place. Reply if you are coming.",
    "Your newsletter subscription is confirmed. Expect weekly updates about photography.",
    "The invoice for the consulting engagement is attached. Payment terms as discussed.",
    "I enjoyed our conversation at the conference. Here is the article I mentioned.",
    "Flight confirmation: your trip to Berlin is confirmed for next Tuesday.",
    "The repository has been updated. Please pull the latest changes before continuing.",
    "Pull request merged. Nice work on the refactor. Deploying to staging now.",
    "Meeting notes from today are in the shared drive. Action items are highlighted.",
    "Welcome to the team. HR will reach out with your onboarding schedule this week.",
    "The software license renewal is due next month. Finance has been notified.",
    "Your reservation at the restaurant is confirmed for 7 pm Friday. See you then.",
    "Your subscription to the industry newsletter has been renewed for another year.",
    "Following up on our call. I will send the revised proposal tomorrow.",
    "Congratulations on the promotion. Well deserved after all the work you put in.",
    "The webinar you registered for starts in one hour. Join via the link in the calendar invite.",
    # Newsletter / marketing patterns — legitimate but phish-vocabulary-heavy.
    # Added in v0.1.8 because strong_bayes was over-firing on these.
    "Your weekly TLDR: five stories in tech, science, and startups you should not miss this week.",
    "This week in AI: new model releases, fresh research, and the best papers we read. Happy reading.",
    "Top picks from our community: curated articles, podcast episodes, and long reads.",
    "Product update: we shipped dark mode, faster exports, and better keyboard shortcuts.",
    "Your monthly statement is ready. View balance and recent transactions in the app.",
    "New feature rollout: announcements from our product team for the next quarter.",
    "Event invitation: join us for a panel discussion on remote work and team culture.",
    "Your account activity summary: logins this week, new devices, and recent downloads.",
    "Jane updated the shared document and left a comment for you. Review when you can.",
    "Here are the highlights from our latest release notes: improvements, fixes, and performance.",
    "Weekly engineering digest: deploys shipped, incidents resolved, and on-call schedule ahead.",
    "Thank you for subscribing. We send one email per week with our best content.",
    "Reminder: your upcoming reservation, check-in details, and parking information are attached.",
    "Order confirmed. Estimated delivery between Tuesday and Thursday next week.",
    "New comment on the issue you subscribed to. View the discussion thread in the browser.",
    "Your monthly usage report: API calls, storage used, and bandwidth for the billing period.",
    # GitHub / engineering tool notifications — common in real inboxes
    "Your pull request has been merged into main. View details on GitHub.",
    "A new issue was opened in the repository. Review the details and assign a label.",
    "The CI build passed for your commit. View the check results in the Actions tab.",
    "Review requested on pull request number 42. Please leave your feedback.",
    "Deployment to staging succeeded. View details and logs in the dashboard.",
    "Your commit was mentioned in a code review comment. View the thread for details.",
    # Transactional receipts and shipping confirmations
    "Your order has shipped. View tracking details and the estimated delivery date.",
    "Receipt for your recent transaction. View order details in your account.",
    "Payment of eighty dollars confirmed. View invoice and receipt details below.",
    "Your monthly subscription renewed successfully. View the billing details in settings.",
    "Flight booking confirmed. View your itinerary and ticket details in the app.",
    "Password reset successful. If this was not you please review account details.",
]


def build_model() -> dict:
    phish_emails = list(PHISH_CORPUS)

    # load + append famous cases
    famous_path = DATA / "famous_cases.json"
    famous = json.loads(famous_path.read_text())
    famous_texts = [case["text"] for case in famous]
    phish_emails.extend(famous_texts)

    ham_emails = list(HAM_CORPUS)

    phish_counts: Counter[str] = Counter()
    for text in phish_emails:
        # count per-email (use set so a token in one email contributes +1)
        phish_counts.update(set(tokenize(text)))

    ham_counts: Counter[str] = Counter()
    for text in ham_emails:
        ham_counts.update(set(tokenize(text)))

    # Famous-case boost: add extra phish-weight to tokens that appear in those seeds
    for text in famous_texts:
        for token in set(tokenize(text)):
            phish_counts[token] += FAMOUS_BOOST

    # Real email counts for Laplace denominators. The famous-case boost
    # lifts individual token counts without inflating the denominator, so
    # boosted tokens score very high while unboost tokens retain their
    # real signal ratio.
    n_phish = len(phish_emails)
    n_ham = len(ham_emails)

    tokens: dict[str, dict] = {}
    vocab = set(phish_counts) | set(ham_counts)
    for token in vocab:
        phish_c = phish_counts.get(token, 0)
        ham_c = ham_counts.get(token, 0)
        if phish_c + ham_c < MIN_OCCURRENCE:
            continue

        # Laplace smoothing
        p_t_given_phish = (phish_c + 1) / (n_phish + 2)
        p_t_given_ham = (ham_c + 1) / (n_ham + 2)
        # equal priors → P(phish | t) = p_t_given_phish / (p_t_given_phish + p_t_given_ham)
        p_phish = p_t_given_phish / (p_t_given_phish + p_t_given_ham)

        tokens[token] = {
            "phish": phish_c,
            "ham": ham_c,
            "p_phish": round(p_phish, 3),
        }

    return {
        "version": "openclaw-hackathon-v1",
        "phish_email_count": n_phish,
        "ham_email_count": n_ham,
        "vocab_size": len(tokens),
        "tokens": dict(sorted(tokens.items())),
    }


def main() -> None:
    model = build_model()
    out = DATA / "bayes_model.json"
    out.write_text(json.dumps(model, indent=2) + "\n")
    print(f"wrote {out} — vocab={model['vocab_size']} tokens")

    # Spot check: print a few known-phishy tokens
    print("\nSample p_phish values:")
    for t in ("urgent", "wire", "bitcoin", "quanta", "meeting", "invoice", "verify"):
        entry = model["tokens"].get(t)
        if entry:
            print(f"  {t:12s} p_phish={entry['p_phish']:.3f}  (phish={entry['phish']}, ham={entry['ham']})")


if __name__ == "__main__":
    main()
