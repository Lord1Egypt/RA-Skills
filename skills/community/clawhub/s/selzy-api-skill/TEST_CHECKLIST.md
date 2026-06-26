# Selzy Skill — Test Checklist Before Use

## 🧪 Quick Test (5 minutes)

Before first use or after updates, run through this test.

---

### Test 1: API Access Check

```bash
curl "https://api.selzy.com/en/api/getLists?format=json&api_key=$SELZY_API_KEY"
```

**Expected Result:**
```json
{"result": [{"id": 12345, "title": "My first list", "count": 4}]}
```

✅ **PASS:** Got contact list  
❌ **FAIL:** API error → check `SELZY_API_KEY`

---

### Test 2: list_id Check (CRITICAL)

**Question:** Do you have `list_id` from `getLists`?

- [ ] Yes, called `getLists` and got `list_id=12345`
- [ ] No, trying to guess or using default → **STOP!**

**Rule:** Never create email without explicit `list_id`!

---

### Test 3: Contact Count Check

**Question:** How many contacts are in the list?

- [ ] Know exact number (e.g., 4)
- [ ] Don't know → **Call `getList(list_id=12345)` and check!**

**Rule:** If count = 0 or doesn't match expectations → STOP and ask user!

---

### Test 4: Create Email with list_id

```bash
curl "https://api.selzy.com/en/api/createEmailMessage?format=json&api_key=$KEY&sender_name=Test&sender_email=test@example.com&subject=Test&body=<h1>Test</h1>&list_id=12345"
```

**Expected Result:**
```json
{"result": {"message_id": 67890}}
```

✅ **PASS:** Email created with `list_id`  
❌ **FAIL:** Error → check parameters (especially `list_id`)

---

### Test 5: Confirmation Before Send

**Question:** Did you get explicit confirmation from user?

- [ ] Yes, user said "send" / "confirm" / "yes"
- [ ] No, sending myself → **STOP!**

**Rule:** Never send without explicit confirmation!

---

### Test 6: Final Check Before createCampaign

Before calling `createCampaign`, verify:

- [ ] `list_id` obtained from `getLists` ✅
- [ ] Contact count known and matches ✅
- [ ] Email created with `list_id` parameter ✅
- [ ] User confirmed sending ✅
- [ ] Send time confirmed (immediate or scheduled) ✅

**If all checked → can create campaign!**

---

## 🚨 Red Flags (Stop Immediately!)

If you see any of these → **DO NOT PROCEED**:

1. ❌ Didn't call `getLists` → no `list_id`
2. ❌ Don't know contact count in list
3. ❌ Trying to use `list_id` from old cache
4. ❌ User didn't explicitly confirm sending
5. ❌ Count = 0 or doesn't match expectations
6. ❌ `sender_email` not verified in Selzy

---

## ✅ Success Criteria

Test passed successfully if:

1. Can name your list's `list_id`
2. Know exact contact count
3. Understand that without `list_id`, send goes to only 1 person
4. Always get explicit confirmation before sending
5. Check count before creating campaign

---

## 📊 Example Correct Workflow

```
User: "Send campaign to my customers"

Assistant:
1. getLists() → [{"id": 12345, "title": "Customers", "count": 4}]
2. "Found list 'Customers' with 4 contacts. Send to all?"
3. User: "Yes"
4. createEmailMessage(..., list_id=12345) → message_id=67890
5. "Email ready. Send now?"
6. User: "Send it"
7. createCampaign(message_id=67890) → campaign_id=11111
8. "Done! Campaign #11111 sent to 4 contacts."
```

**All stages passed ✅**

---

## 🔧 Troubleshooting

### Problem: "Incorrect API key"
**Solution:** Check `SELZY_API_KEY` in config

### Problem: "Sender not verified"
**Solution:** Use `getSenderEmails`, select verified email

### Problem: "Not found" (list_id)
**Solution:** Call `getLists` again, get current `list_id`

### Problem: Campaign sent to 1 person
**Solution:** See "Real-World Bug Fix Example" in SKILL.md

---

## 📞 Support

If stuck on any step:

1. Check API error logs
2. Compare with checklist above
3. Read README.md
4. See examples in SKILL.md (section "Common Workflows")

---

**Remember:** 5 minutes of checking saves hours of fixing mistakes! 🛡️
