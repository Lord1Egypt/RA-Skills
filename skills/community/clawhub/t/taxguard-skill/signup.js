#!/usr/bin/env node
// TaxGuard Signup — get your API key in one command
// Usage: node signup.js your@email.com

const email = process.argv[2]
if (!email || !email.includes("@")) {
  console.log("Usage: node signup.js your@email.com")
  process.exit(1)
}

async function main() {
  console.log("Signing up", email, "...")
  const res = await fetch("https://api.rhetra.io/api/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email })
  })
  const data = await res.json()
  if (data.apiKey) {
    console.log("")
    console.log("=== SUCCESS ===")
    console.log("Your API key:", data.apiKey)
    console.log("")
    console.log("Set it in your environment:")
    console.log("  export TAXGUARD_API_KEY=" + data.apiKey)
    console.log("")
    console.log("Or add to your .env file:")
    console.log("  TAXGUARD_API_KEY=" + data.apiKey)
    console.log("")
    console.log("First 10 checks/month are free. $0.01 each after that.")
  } else if (data.error) {
    console.log("Error:", data.error)
    if (data.details) console.log("Details:", JSON.stringify(data.details))
  } else {
    console.log("Response:", JSON.stringify(data, null, 2))
  }
}

main().catch(e => { console.error("Failed:", e.message); process.exit(1) })
