---
name: send
description: >
  The last step that matters most. A complete sending intelligence system for anyone who
  communicates at scale or with stakes: emails, messages, files, proposals, campaigns, or
  any communication before it leaves your hands. Trigger when someone needs to send something
  important, wants to check something before sending, needs to automate sending workflows,
  or has to deliver difficult news, critical information, or high-value content to the right
  person at the right moment in the right way.
---

# Send

## The Moment Before You Hit Send

Every important communication has a moment — the pause before it goes. The proposal to the
client who could change your year. The message to the person who needs to hear something
difficult. The campaign to ten thousand people. The apology that could repair or ruin a
relationship.

In that moment, most people are asking: is this good enough?

The better question is: will this do what I need it to do?

This skill answers that question. Then it helps you send with confidence.

---

## The Send Readiness Framework
```
SEND_READINESS = {
  "purpose_check": {
    "question":  "What do I need to happen as a result of this communication",
    "answers":   ["Recipient takes a specific action",
                  "Recipient has specific information",
                  "Recipient feels a specific way",
                  "Relationship advances or repairs"],
    "test":      "Does every element of this message serve the stated purpose.
                  If not, it should not be there."
  },

  "recipient_check": {
    "questions": ["Who exactly is reading this",
                  "What do they already know",
                  "What do they care about",
                  "What objection will they have",
                  "What do I need them to do after reading"],
    "principle": "Write for the reader you have, not the reader you wish you had"
  },

  "clarity_check": {
    "test":      "Read only the first sentence. Is the purpose immediately clear?",
    "test_2":    "Read only the last sentence. Is the ask or next step unmistakable?",
    "test_3":    "Could this be misunderstood? If yes, how, and how do you prevent it?"
  }
}
```

---

## Communication Type Protocols
```
SEND_PROTOCOLS = {
  "high_stakes_email": {
    "before_sending": [
      "Reply-all check — is everyone on this thread meant to see this",
      "Attachment confirmed — never write 'see attached' without attaching",
      "Tone check — read aloud to hear how it sounds",
      "Subject line — does it accurately represent the content",
      "24-hour rule — for anything written in anger, wait 24 hours"
    ],
    "checklist": """
      def pre_send_audit(email):
          checks = {
              "correct_recipient":   verify_to_cc_bcc(email),
              "attachment_present":  "attached" not in email.body or email.has_attachment,
              "clear_subject":       len(email.subject) > 5 and is_descriptive(email.subject),
              "single_ask":          count_requests(email.body) <= 1,
              "appropriate_tone":    not contains_words(email.body, TONE_RED_FLAGS),
              "no_sensitive_data":   not contains_pii_or_confidential(email.body)
          }
          return all(checks.values()), checks
    """
  },

  "difficult_message": {
    "principles": ["Direct does not mean harsh — clarity is kindness",
                   "One difficult message per communication — do not stack",
                   "Private channel for personal or sensitive content",
                   "Written record for professional accountability"],
    "structure":  ["Context — what this is about",
                   "The specific situation or behavior",
                   "The impact",
                   "What you need going forward",
                   "Invitation to respond"],
    "not_this":   ["Email to avoid a conversation that needs to happen in person",
                   "Group message for individual feedback",
                   "Passive framing that obscures the actual message"]
  },

  "mass_send": {
    "before_sending_to_list": [
      "Test send to yourself first — always",
      "Check all merge fields resolve correctly",
      "Mobile preview — 60%+ of email is read on mobile",
      "Unsubscribe link present and functional",
      "Sending domain authenticated — SPF, DKIM, DMARC",
      "Send time optimized for recipient timezone"
    ],
    "send_time_intelligence": """
      OPTIMAL_SEND_TIMES = {
          "B2B_email":    "Tuesday-Thursday, 9-11am recipient local time",
          "B2C_email":    "Tuesday-Thursday, 7-9pm recipient local time",
          "newsletters":  "Tuesday or Thursday morning",
          "transactional": "Immediately — delay reduces conversion",
          "cold_outreach": "Tuesday-Thursday, 8-9am — before inbox fills"
      }
    """
  },

  "file_send": {
    "before_sending": [
      "File opens correctly — do not assume",
      "Permissions set correctly — not edit when view is appropriate",
      "Version is final — not draft_v3_FINAL_actual_final",
      "File size appropriate for channel — large files to cloud storage, not attachment",
      "Sensitive data redacted if going outside organization"
    ]
  }
}
```

---

## Automation and Workflows
```
SEND_AUTOMATION = {
  "when_to_automate": {
    "good_candidates":  ["Confirmation emails after form submission",
                          "Follow-up sequences with time delays",
                          "Recurring reports and digests",
                          "Payment reminders",
                          "Onboarding sequences"],
    "bad_candidates":   ["Responses requiring judgment",
                          "Sensitive communications",
                          "Anything where being wrong is costly"]
  },

  "sequence_design": """
    def design_send_sequence(goal, audience):
        sequence = []
        sequence.append(Email(
            timing="immediately",
            purpose="deliver_value_or_confirm_action",
            cta="single_clear_next_step"
        ))
        sequence.append(Email(
            timing="day_3",
            purpose="provide_additional_value",
            cta="softer_secondary_ask"
        ))
        sequence.append(Email(
            timing="day_7",
            purpose="last_touch_before_exit",
            cta="direct_ask_or_breakup_email"
        ))
        return sequence
    # 3 emails is enough for most sequences — more is diminishing returns
  """,

  "deliverability": {
    "warm_up":        "New domains need gradual volume increase over 4-6 weeks",
    "list_hygiene":   "Remove bounces and unengaged subscribers — protects sender reputation",
    "engagement":     "High open rates protect deliverability — send to engaged segments first"
  }
}
```

---

## Damage Control
```
SENT_THE_WRONG_THING = {
  "recall_reality":   "Email recall works rarely and only within same organization.
                        Assume it cannot be recalled.",
  "immediate_steps":  ["Assess who received it and what they saw",
                        "Send correction promptly — delay makes it worse",
                        "Own the error directly — do not bury the correction"],
  "correction_template": {
    "subject":  "Correction: [Original subject]",
    "opening":  "I sent an email earlier today that contained [error].
                  The correct information is [correction]. I apologize for any confusion."
  },
  "data_breach":  "If sensitive data was sent to wrong recipient — notify IT and privacy
                   officer immediately. Most jurisdictions have notification requirements."
}
```

---

## Quality Check Before Delivering

- [ ] Purpose of communication is explicit and single
- [ ] Recipient confirmed including reply-all risk
- [ ] Tone appropriate for relationship and content
- [ ] Single clear call to action
- [ ] Attachment present if referenced
- [ ] Sensitive data check completed
- [ ] Send time optimized for mass sends
- [ ] Test send completed before list send
