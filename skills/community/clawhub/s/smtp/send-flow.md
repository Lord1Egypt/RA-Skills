# Send Flow - SMTP

Use this workflow for every SMTP task so the agent does not skip safety gates.

## Step 1: Classify the job

Choose one path:
- Draft only: write the message and stop before network use
- Probe: test DNS, TLS, EHLO, or auth with no real send
- Canary: send one approved message to one controlled inbox
- Live send: send to real recipients after the canary is verified

## Step 2: Collect the minimum inputs

Need only:
- host and port
- TLS mode
- auth identity
- visible From address
- recipient scope
- success definition

If one of these is missing, say exactly what is blocked.

## Step 3: Preflight before sending

Run the checks in order:
1. host resolves and the port is reachable
2. TLS handshake matches the selected port mode
3. EHLO capabilities show the expected auth and STARTTLS support
4. auth works
5. sender identity is coherent

## Step 4: Canary before scale

For the first real send:
- one recipient only
- smallest useful body
- prefer plain text unless HTML is part of the bug
- capture queue ID or message ID immediately

## Step 5: Verify the result

Check the strongest evidence available:
- SMTP acceptance code
- provider activity log
- inbox or spam placement
- bounce or DSN

If final placement is unknown, report unknown rather than success.

## Step 6: Scale carefully

Only widen recipient scope when:
- the canary succeeded
- the auth and sender identity path is stable
- the user confirmed broader sending
