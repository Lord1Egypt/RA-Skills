# PHP examples

Official SDK: https://github.com/sendpulse/sendpulse-rest-api-php
(`composer require sendpulse/rest-api`). Below: plain cURL with a Single API Key —
no token refresh needed.

## Minimal client

```php
<?php

function sendpulse(string $method, string $path, ?array $body = null): array
{
    $ch = curl_init('https://api.sendpulse.com' . $path);
    $headers = ['Authorization: Bearer ' . getenv('SENDPULSE_API_KEY')];
    if ($body !== null) {
        $headers[] = 'Content-Type: application/json';
    }
    curl_setopt_array($ch, [
        CURLOPT_CUSTOMREQUEST => $method,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => $headers,
        CURLOPT_POSTFIELDS => $body !== null ? json_encode($body) : null,
    ]);
    $response = curl_exec($ch);
    $status = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);

    $data = json_decode($response, true);
    if ($status >= 400) {
        throw new RuntimeException("SendPulse $method $path failed (HTTP $status): $response");
    }
    return is_array($data) ? $data : [];
}
```

## Book → subscribers → campaign

```php
// 1. Create an address book
$book = sendpulse('POST', '/addressbooks', ['bookName' => 'Newsletter']);
$bookId = $book['id'];

// 2. Add subscribers (upsert: re-adding updates variables)
sendpulse('POST', "/addressbooks/{$bookId}/emails", [
    'emails' => [
        ['email' => 'jane@example.com',
         'variables' => ['name' => 'Jane', 'city' => 'Berlin', 'signup_date' => '2026-07-01']],
    ],
]);

// 3. Pre-flight: sender verified? what does it cost?
$senders = sendpulse('GET', '/senders');
$cost    = sendpulse('GET', "/addressbooks/{$bookId}/cost");

// 4. Create the campaign (body MUST be Base64; or use 'template_id')
$campaign = sendpulse('POST', '/campaigns', [
    'name'         => 'July digest',
    'sender_name'  => 'My Shop',
    'sender_email' => 'news@myshop.com',        // must be in $senders
    'subject'      => 'Your July digest is here',
    'body'         => base64_encode('<h1>Hello {{name}}!</h1><p>Our July digest...</p>'),
    'list_id'      => $bookId,
    'send_date'    => '2026-07-10 10:00:00',    // omit to send ASAP
    'stats'        => ['opens' => true, 'clicks' => true, 'utm_campaign' => 'july_digest'],
]);
$campaignId = $campaign['id'];

// 5. Status & stats (or subscribe to the task_status_update webhook instead of polling)
$info = sendpulse('GET', "/campaigns/{$campaignId}");
```

## Analytics after sending

```php
$stats     = sendpulse('GET', "/campaigns/{$campaignId}");             // core numbers
$countries = sendpulse('GET', "/campaigns/{$campaignId}/countries");
$links     = sendpulse('GET', "/campaigns/{$campaignId}/referrals");   // clicks per link
$oneUser   = sendpulse('GET', "/campaigns/{$campaignId}/email/" . urlencode('jane@example.com'));
```

## Opt-out mirroring (call when a user unsubscribes in your app)

```php
// From one book:
sendpulse('POST', "/addressbooks/{$bookId}/emails/unsubscribe",
          ['emails' => ['jane@example.com']]);

// Account-wide blacklist — NOTE: Base64 of a comma-separated string, not an array!
sendpulse('POST', '/blacklist', [
    'emails'  => base64_encode('jane@example.com'),
    'comment' => 'opted out in app',
]);
```

## OAuth variant (if not using an API key)

```php
$auth = sendpulseRaw('POST', '/oauth/access_token', [
    'grant_type'    => 'client_credentials',
    'client_id'     => getenv('SENDPULSE_API_ID'),
    'client_secret' => getenv('SENDPULSE_API_SECRET'),
]); // returns access_token, expires_in=3600 — cache ~55 min, refresh on 401
```
