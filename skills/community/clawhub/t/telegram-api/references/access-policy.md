# Telegram access policy

An access policy limits which endpoints Telegram connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/telegram#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Telegram: its 66 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create telegram --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": ":token/getChatMenuButton"},
    {"method": "POST", "path": ":token/getChatMenuButton"},
    {"method": "GET", "path": ":token/getMe"},
    {"method": "POST", "path": ":token/getMe"},
    {"method": "GET", "path": ":token/getMyCommands"},
    {"method": "POST", "path": ":token/getMyCommands"},
    {"method": "GET", "path": ":token/getMyDefaultAdministratorRights"},
    {"method": "POST", "path": ":token/getMyDefaultAdministratorRights"},
    {"method": "GET", "path": ":token/getMyDescription"},
    {"method": "POST", "path": ":token/getMyDescription"},
    {"method": "GET", "path": ":token/getMyName"},
    {"method": "POST", "path": ":token/getMyName"},
    {"method": "GET", "path": ":token/getMyShortDescription"},
    {"method": "POST", "path": ":token/getMyShortDescription"},
    {"method": "GET", "path": ":token/getBusinessAccountGifts"},
    {"method": "POST", "path": ":token/getBusinessAccountGifts"},
    {"method": "GET", "path": ":token/getBusinessAccountStarBalance"},
    {"method": "POST", "path": ":token/getBusinessAccountStarBalance"},
    {"method": "GET", "path": ":token/getBusinessConnection"},
    {"method": "POST", "path": ":token/getBusinessConnection"},
    {"method": "GET", "path": ":token/getChat"},
    {"method": "POST", "path": ":token/getChat"},
    {"method": "GET", "path": ":token/getChatAdministrators"},
    {"method": "POST", "path": ":token/getChatAdministrators"},
    {"method": "GET", "path": ":token/getChatMember"},
    {"method": "POST", "path": ":token/getChatMember"},
    {"method": "GET", "path": ":token/getChatMemberCount"},
    {"method": "POST", "path": ":token/getChatMemberCount"},
    {"method": "GET", "path": ":token/getChatShareThemeBackdrops"},
    {"method": "POST", "path": ":token/getChatShareThemeBackdrops"},
    {"method": "GET", "path": ":token/getUserChatBoosts"},
    {"method": "POST", "path": ":token/getUserChatBoosts"},
    {"method": "GET", "path": ":token/getUserPersonalChatMessages"},
    {"method": "POST", "path": ":token/getUserPersonalChatMessages"},
    {"method": "GET", "path": ":token/getFile"},
    {"method": "POST", "path": ":token/getFile"},
    {"method": "GET", "path": ":token/getUserProfileAudios"},
    {"method": "POST", "path": ":token/getUserProfileAudios"},
    {"method": "GET", "path": ":token/getUserProfilePhotos"},
    {"method": "POST", "path": ":token/getUserProfilePhotos"},
    {"method": "GET", "path": ":token/getGameHighScores"},
    {"method": "POST", "path": ":token/getGameHighScores"},
    {"method": "GET", "path": ":token/getAvailableGifts"},
    {"method": "POST", "path": ":token/getAvailableGifts"},
    {"method": "GET", "path": ":token/getChatGifts"},
    {"method": "POST", "path": ":token/getChatGifts"},
    {"method": "GET", "path": ":token/getUniqueGift"},
    {"method": "POST", "path": ":token/getUniqueGift"},
    {"method": "GET", "path": ":token/getUserGifts"},
    {"method": "POST", "path": ":token/getUserGifts"},
    {"method": "GET", "path": ":token/getManagedBotAccessSettings"},
    {"method": "POST", "path": ":token/getManagedBotAccessSettings"},
    {"method": "GET", "path": ":token/getMyStarBalance"},
    {"method": "POST", "path": ":token/getMyStarBalance"},
    {"method": "GET", "path": ":token/getStarTransactions"},
    {"method": "POST", "path": ":token/getStarTransactions"},
    {"method": "GET", "path": ":token/getCustomEmojiStickers"},
    {"method": "POST", "path": ":token/getCustomEmojiStickers"},
    {"method": "GET", "path": ":token/getForumTopicIconStickers"},
    {"method": "POST", "path": ":token/getForumTopicIconStickers"},
    {"method": "GET", "path": ":token/getStickerSet"},
    {"method": "POST", "path": ":token/getStickerSet"},
    {"method": "GET", "path": ":token/getUpdates"},
    {"method": "POST", "path": ":token/getUpdates"},
    {"method": "GET", "path": ":token/getWebhookInfo"},
    {"method": "POST", "path": ":token/getWebhookInfo"}
  ],
  "deny": []
}
```

## Endpoints

The Telegram endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | :token/close | write | bot | Close the bot instance before moving it from one local server to another. |
| POST | :token/close | write | bot | Close the bot instance before moving it from one local server to another. |
| GET | :token/getChatMenuButton | read | bot | Get the current value of the bot's menu button in a private chat, or the default menu button. |
| POST | :token/getChatMenuButton | read | bot | Get the current value of the bot's menu button in a private chat, or the default menu button. |
| GET | :token/getMe | read | bot | A simple method for testing your bot's authentication token. |
| POST | :token/getMe | read | bot | A simple method for testing your bot's authentication token. |
| GET | :token/getMyCommands | read | bot | Get the current list of the bot's commands for the given scope and user language. |
| POST | :token/getMyCommands | read | bot | Get the current list of the bot's commands for the given scope and user language. |
| GET | :token/getMyDefaultAdministratorRights | read | bot | Get the current default administrator rights of the bot. |
| POST | :token/getMyDefaultAdministratorRights | read | bot | Get the current default administrator rights of the bot. |
| GET | :token/getMyDescription | read | bot | Get the current bot description for the given user language. |
| POST | :token/getMyDescription | read | bot | Get the current bot description for the given user language. |
| GET | :token/getMyName | read | bot | Get the current bot name for the given user language. |
| POST | :token/getMyName | read | bot | Get the current bot name for the given user language. |
| GET | :token/getMyShortDescription | read | bot | Get the current bot short description for the given user language. |
| POST | :token/getMyShortDescription | read | bot | Get the current bot short description for the given user language. |
| GET | :token/logOut | write | bot | Log out from the cloud Bot API server before launching the bot locally. |
| POST | :token/logOut | write | bot | Log out from the cloud Bot API server before launching the bot locally. |
| GET | :token/setChatMenuButton | write | bot | Change the bot's menu button in a private chat, or the default menu button. |
| POST | :token/setChatMenuButton | write | bot | Change the bot's menu button in a private chat, or the default menu button. |
| GET | :token/setMyCommands | write | bot | Change the list of the bot's commands. |
| POST | :token/setMyCommands | write | bot | Change the list of the bot's commands. |
| GET | :token/setMyDefaultAdministratorRights | write | bot | Change the default administrator rights requested by the bot when it's added as an administrator to groups or channels. |
| POST | :token/setMyDefaultAdministratorRights | write | bot | Change the default administrator rights requested by the bot when it's added as an administrator to groups or channels. |
| GET | :token/setMyDescription | write | bot | Change the bot's description, which is shown in the chat with the bot if the chat is empty. |
| POST | :token/setMyDescription | write | bot | Change the bot's description, which is shown in the chat with the bot if the chat is empty. |
| GET | :token/setMyName | write | bot | Change the bot's name. |
| POST | :token/setMyName | write | bot | Change the bot's name. |
| GET | :token/setMyProfilePhoto | write | bot | Changes the profile photo of the bot. |
| POST | :token/setMyProfilePhoto | write | bot | Changes the profile photo of the bot. |
| GET | :token/setMyShortDescription | write | bot | Change the bot's short description, which is shown on the bot's profile page and is sent together with the link when users share the bot. |
| POST | :token/setMyShortDescription | write | bot | Change the bot's short description, which is shown on the bot's profile page and is sent together with the link when users share the bot. |
| GET | :token/deleteBusinessAccountGift | write | business | Deletes a regular gift owned by a managed business account without receiving Telegram Stars for it. |
| POST | :token/deleteBusinessAccountGift | write | business | Deletes a regular gift owned by a managed business account without receiving Telegram Stars for it. |
| GET | :token/deleteBusinessMessages | write | business | Delete messages on behalf of a business account. |
| POST | :token/deleteBusinessMessages | write | business | Delete messages on behalf of a business account. |
| GET | :token/deleteStory | write | business | Deletes a story previously posted by the bot on behalf of a managed business account. |
| POST | :token/deleteStory | write | business | Deletes a story previously posted by the bot on behalf of a managed business account. |
| GET | :token/editStory | write | business | Edits a story previously posted by the bot on behalf of a managed business account. |
| POST | :token/editStory | write | business | Edits a story previously posted by the bot on behalf of a managed business account. |
| GET | :token/getBusinessAccountGifts | read | business | Returns the gifts received and owned by a managed business account. |
| POST | :token/getBusinessAccountGifts | read | business | Returns the gifts received and owned by a managed business account. |
| GET | :token/getBusinessAccountStarBalance | read | business | Returns the amount of Telegram Stars owned by a managed business account. |
| POST | :token/getBusinessAccountStarBalance | read | business | Returns the amount of Telegram Stars owned by a managed business account. |
| GET | :token/getBusinessConnection | read | business | Get information about the connection of the bot with a business account. |
| POST | :token/getBusinessConnection | read | business | Get information about the connection of the bot with a business account. |
| GET | :token/postStory | write | business | Posts a story on behalf of a managed business account. |
| POST | :token/postStory | write | business | Posts a story on behalf of a managed business account. |
| GET | :token/readBusinessMessage | write | business | Marks incoming message as read on behalf of a business account. |
| POST | :token/readBusinessMessage | write | business | Marks incoming message as read on behalf of a business account. |
| GET | :token/removeBusinessAccountProfilePhoto | write | business | Removes the current profile photo of a managed business account. |
| POST | :token/removeBusinessAccountProfilePhoto | write | business | Removes the current profile photo of a managed business account. |
| GET | :token/repostStory | write | business | Reposts a story on behalf of a business account from another business account. |
| POST | :token/repostStory | write | business | Reposts a story on behalf of a business account from another business account. |
| GET | :token/setBusinessAccountBio | write | business | Changes the bio of a managed business account. |
| POST | :token/setBusinessAccountBio | write | business | Changes the bio of a managed business account. |
| GET | :token/setBusinessAccountGiftSettings | write | business | Changes the privacy settings pertaining to incoming gifts in a managed business account. |
| POST | :token/setBusinessAccountGiftSettings | write | business | Changes the privacy settings pertaining to incoming gifts in a managed business account. |
| GET | :token/setBusinessAccountName | write | business | Changes the first and last name of a managed business account. |
| POST | :token/setBusinessAccountName | write | business | Changes the first and last name of a managed business account. |
| GET | :token/setBusinessAccountProfilePhoto | write | business | Changes the profile photo of a managed business account. |
| POST | :token/setBusinessAccountProfilePhoto | write | business | Changes the profile photo of a managed business account. |
| GET | :token/setBusinessAccountUsername | write | business | Changes the username of a managed business account. |
| POST | :token/setBusinessAccountUsername | write | business | Changes the username of a managed business account. |
| GET | :token/transferBusinessAccountStars | write | business | Transfers Telegram Stars from the business account balance to the bot's balance. |
| POST | :token/transferBusinessAccountStars | write | business | Transfers Telegram Stars from the business account balance to the bot's balance. |
| GET | :token/answerCallbackQuery | write | callbacks | Send answers to callback queries sent from inline keyboards. |
| POST | :token/answerCallbackQuery | write | callbacks | Send answers to callback queries sent from inline keyboards. |
| GET | :token/answerGuestQuery | write | callbacks | Reply to a received guest message. |
| POST | :token/answerGuestQuery | write | callbacks | Reply to a received guest message. |
| GET | :token/answerChatJoinRequestQuery | write | chats | Process a received chat join request query. |
| POST | :token/answerChatJoinRequestQuery | write | chats | Process a received chat join request query. |
| GET | :token/approveChatJoinRequest | write | chats | Approve a chat join request. |
| POST | :token/approveChatJoinRequest | write | chats | Approve a chat join request. |
| GET | :token/banChatMember | write | chats | Ban a user in a group, a supergroup or a channel. |
| POST | :token/banChatMember | write | chats | Ban a user in a group, a supergroup or a channel. |
| GET | :token/banChatSenderChat | write | chats | Ban a channel chat in a supergroup or a channel. |
| POST | :token/banChatSenderChat | write | chats | Ban a channel chat in a supergroup or a channel. |
| GET | :token/createChatInviteLink | write | chats | Create an additional invite link for a chat. |
| POST | :token/createChatInviteLink | write | chats | Create an additional invite link for a chat. |
| GET | :token/createChatSubscriptionInviteLink | write | chats | Create a subscription invite link for a channel chat. |
| POST | :token/createChatSubscriptionInviteLink | write | chats | Create a subscription invite link for a channel chat. |
| GET | :token/declineChatJoinRequest | write | chats | Decline a chat join request. |
| POST | :token/declineChatJoinRequest | write | chats | Decline a chat join request. |
| GET | :token/deleteChatPhoto | write | chats | Delete a chat photo. |
| POST | :token/deleteChatPhoto | write | chats | Delete a chat photo. |
| GET | :token/deleteChatStickerSet | write | chats | Delete a group sticker set from a supergroup. |
| POST | :token/deleteChatStickerSet | write | chats | Delete a group sticker set from a supergroup. |
| GET | :token/editChatInviteLink | write | chats | Edit a non-primary invite link created by the bot. |
| POST | :token/editChatInviteLink | write | chats | Edit a non-primary invite link created by the bot. |
| GET | :token/editChatSubscriptionInviteLink | write | chats | Edit a subscription invite link created by the bot. |
| POST | :token/editChatSubscriptionInviteLink | write | chats | Edit a subscription invite link created by the bot. |
| GET | :token/exportChatInviteLink | write | chats | Generate a new primary invite link for a chat; any previously generated primary link is revoked. |
| POST | :token/exportChatInviteLink | write | chats | Generate a new primary invite link for a chat; any previously generated primary link is revoked. |
| GET | :token/getChat | read | chats | Get up-to-date information about the chat. |
| POST | :token/getChat | read | chats | Get up-to-date information about the chat. |
| GET | :token/getChatAdministrators | read | chats | Get a list of administrators in a chat. |
| POST | :token/getChatAdministrators | read | chats | Get a list of administrators in a chat. |
| GET | :token/getChatMember | read | chats | Get information about a member of a chat. |
| POST | :token/getChatMember | read | chats | Get information about a member of a chat. |
| GET | :token/getChatMemberCount | read | chats | Get the number of members in a chat. |
| POST | :token/getChatMemberCount | read | chats | Get the number of members in a chat. |
| GET | :token/getChatShareThemeBackdrops | read | chats | Get the list of backdrops, which can be used as the background of a theme of the screen for sharing a link to a user or a chat. |
| POST | :token/getChatShareThemeBackdrops | read | chats | Get the list of backdrops, which can be used as the background of a theme of the screen for sharing a link to a user or a chat. |
| GET | :token/getUserChatBoosts | read | chats | Get the list of boosts added to a chat by a user. |
| POST | :token/getUserChatBoosts | read | chats | Get the list of boosts added to a chat by a user. |
| GET | :token/getUserPersonalChatMessages | read | chats | Get the last messages from the personal chat (i.e., the chat currently added to their profile) of a given user. |
| POST | :token/getUserPersonalChatMessages | read | chats | Get the last messages from the personal chat (i.e., the chat currently added to their profile) of a given user. |
| GET | :token/leaveChat | write | chats | Your bot to leave a group, supergroup or channel. |
| POST | :token/leaveChat | write | chats | Your bot to leave a group, supergroup or channel. |
| GET | :token/pinChatMessage | write | chats | Add a message to the list of pinned messages in a chat. |
| POST | :token/pinChatMessage | write | chats | Add a message to the list of pinned messages in a chat. |
| GET | :token/promoteChatMember | write | chats | Promote or demote a user in a supergroup or a channel. |
| POST | :token/promoteChatMember | write | chats | Promote or demote a user in a supergroup or a channel. |
| GET | :token/restrictChatMember | write | chats | Restrict a user in a supergroup. |
| POST | :token/restrictChatMember | write | chats | Restrict a user in a supergroup. |
| GET | :token/revokeChatInviteLink | write | chats | Revoke an invite link created by the bot. |
| POST | :token/revokeChatInviteLink | write | chats | Revoke an invite link created by the bot. |
| GET | :token/sendChatAction | write | chats | Tell the user that something is happening on the bot's side. |
| POST | :token/sendChatAction | write | chats | Tell the user that something is happening on the bot's side. |
| GET | :token/sendChatJoinRequestWebApp | write | chats | Process a received chat join request query by showing a Mini App to the user before deciding the outcome. |
| POST | :token/sendChatJoinRequestWebApp | write | chats | Process a received chat join request query by showing a Mini App to the user before deciding the outcome. |
| GET | :token/setChatAdministratorCustomTitle | write | chats | Set a custom title for an administrator in a supergroup promoted by the bot. |
| POST | :token/setChatAdministratorCustomTitle | write | chats | Set a custom title for an administrator in a supergroup promoted by the bot. |
| GET | :token/setChatDescription | write | chats | Change the description of a group, a supergroup or a channel. |
| POST | :token/setChatDescription | write | chats | Change the description of a group, a supergroup or a channel. |
| GET | :token/setChatMemberTag | write | chats | Set a tag for a regular member in a group or a supergroup. |
| POST | :token/setChatMemberTag | write | chats | Set a tag for a regular member in a group or a supergroup. |
| GET | :token/setChatPermissions | write | chats | Set default chat permissions for all members. |
| POST | :token/setChatPermissions | write | chats | Set default chat permissions for all members. |
| GET | :token/setChatPhoto | write | chats | Set a new profile photo for the chat. |
| POST | :token/setChatPhoto | write | chats | Set a new profile photo for the chat. |
| GET | :token/setChatStickerSet | write | chats | Set a new group sticker set for a supergroup. |
| POST | :token/setChatStickerSet | write | chats | Set a new group sticker set for a supergroup. |
| GET | :token/setChatTitle | write | chats | Change the title of a chat. |
| POST | :token/setChatTitle | write | chats | Change the title of a chat. |
| GET | :token/unbanChatMember | write | chats | Unban a previously banned user in a supergroup or channel. |
| POST | :token/unbanChatMember | write | chats | Unban a previously banned user in a supergroup or channel. |
| GET | :token/unbanChatSenderChat | write | chats | Unban a previously banned channel chat in a supergroup or channel. |
| POST | :token/unbanChatSenderChat | write | chats | Unban a previously banned channel chat in a supergroup or channel. |
| GET | :token/unpinAllChatMessages | write | chats | Clear the list of pinned messages in a chat. |
| POST | :token/unpinAllChatMessages | write | chats | Clear the list of pinned messages in a chat. |
| GET | :token/unpinChatMessage | write | chats | Remove a message from the list of pinned messages in a chat. |
| POST | :token/unpinChatMessage | write | chats | Remove a message from the list of pinned messages in a chat. |
| GET | :token/getFile | read | files | Get basic information about a file and prepare it for downloading. |
| POST | :token/getFile | read | files | Get basic information about a file and prepare it for downloading. |
| GET | :token/getUserProfileAudios | read | files | Get a list of profile audios for a user. |
| POST | :token/getUserProfileAudios | read | files | Get a list of profile audios for a user. |
| GET | :token/getUserProfilePhotos | read | files | Get a list of profile pictures for a user. |
| POST | :token/getUserProfilePhotos | read | files | Get a list of profile pictures for a user. |
| GET | :token/removeMyProfilePhoto | write | files | Removes the profile photo of the bot. |
| POST | :token/removeMyProfilePhoto | write | files | Removes the profile photo of the bot. |
| GET | :token/closeForumTopic | write | forum | Close an open topic in a forum supergroup chat. |
| POST | :token/closeForumTopic | write | forum | Close an open topic in a forum supergroup chat. |
| GET | :token/closeGeneralForumTopic | write | forum | Close an open 'General' topic in a forum supergroup chat. |
| POST | :token/closeGeneralForumTopic | write | forum | Close an open 'General' topic in a forum supergroup chat. |
| GET | :token/createForumTopic | write | forum | Create a topic in a forum supergroup chat or a private chat with a user. |
| POST | :token/createForumTopic | write | forum | Create a topic in a forum supergroup chat or a private chat with a user. |
| GET | :token/deleteForumTopic | write | forum | Delete a forum topic along with all its messages in a forum supergroup chat or a private chat with a user. |
| POST | :token/deleteForumTopic | write | forum | Delete a forum topic along with all its messages in a forum supergroup chat or a private chat with a user. |
| GET | :token/editForumTopic | write | forum | Edit name and icon of a topic in a forum supergroup chat or a private chat with a user. |
| POST | :token/editForumTopic | write | forum | Edit name and icon of a topic in a forum supergroup chat or a private chat with a user. |
| GET | :token/editGeneralForumTopic | write | forum | Edit the name of the 'General' topic in a forum supergroup chat. |
| POST | :token/editGeneralForumTopic | write | forum | Edit the name of the 'General' topic in a forum supergroup chat. |
| GET | :token/hideGeneralForumTopic | write | forum | Hide the 'General' topic in a forum supergroup chat. |
| POST | :token/hideGeneralForumTopic | write | forum | Hide the 'General' topic in a forum supergroup chat. |
| GET | :token/reopenForumTopic | write | forum | Reopen a closed topic in a forum supergroup chat. |
| POST | :token/reopenForumTopic | write | forum | Reopen a closed topic in a forum supergroup chat. |
| GET | :token/reopenGeneralForumTopic | write | forum | Reopen a closed 'General' topic in a forum supergroup chat. |
| POST | :token/reopenGeneralForumTopic | write | forum | Reopen a closed 'General' topic in a forum supergroup chat. |
| GET | :token/unhideGeneralForumTopic | write | forum | Unhide the 'General' topic in a forum supergroup chat. |
| POST | :token/unhideGeneralForumTopic | write | forum | Unhide the 'General' topic in a forum supergroup chat. |
| GET | :token/unpinAllForumTopicMessages | write | forum | Clear the list of pinned messages in a forum topic in a forum supergroup chat or a private chat with a user. |
| POST | :token/unpinAllForumTopicMessages | write | forum | Clear the list of pinned messages in a forum topic in a forum supergroup chat or a private chat with a user. |
| GET | :token/unpinAllGeneralForumTopicMessages | write | forum | Clear the list of pinned messages in a General forum topic. |
| POST | :token/unpinAllGeneralForumTopicMessages | write | forum | Clear the list of pinned messages in a General forum topic. |
| GET | :token/getGameHighScores | read | games | Get data for high score tables. |
| POST | :token/getGameHighScores | read | games | Get data for high score tables. |
| GET | :token/sendGame | write | games | Send a game. |
| POST | :token/sendGame | write | games | Send a game. |
| GET | :token/setGameScore | write | games | Set the score of the specified user in a game message. |
| POST | :token/setGameScore | write | games | Set the score of the specified user in a game message. |
| GET | :token/convertGiftToStars | write | gifts | Converts a given regular gift to Telegram Stars. |
| POST | :token/convertGiftToStars | write | gifts | Converts a given regular gift to Telegram Stars. |
| GET | :token/getAvailableGifts | read | gifts | Returns the list of gifts that can be sent by the bot to users and channel chats. |
| POST | :token/getAvailableGifts | read | gifts | Returns the list of gifts that can be sent by the bot to users and channel chats. |
| GET | :token/getChatGifts | read | gifts | Returns the gifts owned by a chat. |
| POST | :token/getChatGifts | read | gifts | Returns the gifts owned by a chat. |
| GET | :token/getUniqueGift | read | gifts | Get information about a unique gift by its name. |
| POST | :token/getUniqueGift | read | gifts | Get information about a unique gift by its name. |
| GET | :token/getUserGifts | read | gifts | Returns the gifts owned and hosted by a user. |
| POST | :token/getUserGifts | read | gifts | Returns the gifts owned and hosted by a user. |
| GET | :token/giftPremiumSubscription | write | gifts | Gifts a Telegram Premium subscription to the given user. |
| POST | :token/giftPremiumSubscription | write | gifts | Gifts a Telegram Premium subscription to the given user. |
| GET | :token/sendGift | write | gifts | Sends a gift to the given user or channel chat. |
| POST | :token/sendGift | write | gifts | Sends a gift to the given user or channel chat. |
| GET | :token/transferGift | write | gifts | Transfers an owned unique gift to another user. |
| POST | :token/transferGift | write | gifts | Transfers an owned unique gift to another user. |
| GET | :token/upgradeGift | write | gifts | Upgrades a given regular gift to a unique gift. |
| POST | :token/upgradeGift | write | gifts | Upgrades a given regular gift to a unique gift. |
| GET | :token/answerInlineQuery | write | inline | Send answers to an inline query. |
| POST | :token/answerInlineQuery | write | inline | Send answers to an inline query. |
| GET | :token/savePreparedInlineMessage | write | inline | Stores a message that can be sent by a user of a Mini App. |
| POST | :token/savePreparedInlineMessage | write | inline | Stores a message that can be sent by a user of a Mini App. |
| GET | :token/getManagedBotAccessSettings | read | managed-bots | Get the access settings of a managed bot. |
| POST | :token/getManagedBotAccessSettings | read | managed-bots | Get the access settings of a managed bot. |
| GET | :token/getManagedBotToken | write | managed-bots | Get the token of a managed bot. Kept out of read: response is the managed bot's token. |
| POST | :token/getManagedBotToken | write | managed-bots | Get the token of a managed bot. Kept out of read: response is the managed bot's token. |
| GET | :token/replaceManagedBotToken | write | managed-bots | Revoke the current token of a managed bot and generate a new one. |
| POST | :token/replaceManagedBotToken | write | managed-bots | Revoke the current token of a managed bot and generate a new one. |
| GET | :token/setManagedBotAccessSettings | write | managed-bots | Change the access settings of a managed bot. |
| POST | :token/setManagedBotAccessSettings | write | managed-bots | Change the access settings of a managed bot. |
| GET | :token/approveSuggestedPost | write | messages | Approve a suggested post in a direct messages chat. |
| POST | :token/approveSuggestedPost | write | messages | Approve a suggested post in a direct messages chat. |
| GET | :token/copyMessage | write | messages | Copy messages of any kind. |
| POST | :token/copyMessage | write | messages | Copy messages of any kind. |
| GET | :token/copyMessages | write | messages | Copy messages of any kind. |
| POST | :token/copyMessages | write | messages | Copy messages of any kind. |
| GET | :token/declineSuggestedPost | write | messages | Decline a suggested post in a direct messages chat. |
| POST | :token/declineSuggestedPost | write | messages | Decline a suggested post in a direct messages chat. |
| GET | :token/deleteAllMessageReactions | write | messages | Remove up to 10000 recent reactions in a group or a supergroup chat added by a given user or chat. |
| POST | :token/deleteAllMessageReactions | write | messages | Remove up to 10000 recent reactions in a group or a supergroup chat added by a given user or chat. |
| GET | :token/deleteEphemeralMessage | write | messages | Delete an ephemeral message. |
| POST | :token/deleteEphemeralMessage | write | messages | Delete an ephemeral message. |
| GET | :token/deleteMessage | write | messages | Delete a message, including service messages, with the following limitations:- A message can only be deleted if it was sent less than 48 hours. |
| POST | :token/deleteMessage | write | messages | Delete a message, including service messages, with the following limitations:- A message can only be deleted if it was sent less than 48 hours. |
| GET | :token/deleteMessageReaction | write | messages | Remove a reaction from a message in a group or a supergroup chat. |
| POST | :token/deleteMessageReaction | write | messages | Remove a reaction from a message in a group or a supergroup chat. |
| GET | :token/deleteMessages | write | messages | Delete multiple messages simultaneously. |
| POST | :token/deleteMessages | write | messages | Delete multiple messages simultaneously. |
| GET | :token/deleteMyCommands | write | messages | Delete the list of the bot's commands for the given scope and user language. |
| POST | :token/deleteMyCommands | write | messages | Delete the list of the bot's commands for the given scope and user language. |
| GET | :token/editEphemeralMessageCaption | write | messages | Edit the caption of an ephemeral message. |
| POST | :token/editEphemeralMessageCaption | write | messages | Edit the caption of an ephemeral message. |
| GET | :token/editEphemeralMessageMedia | write | messages | Edit the media of an ephemeral message. |
| POST | :token/editEphemeralMessageMedia | write | messages | Edit the media of an ephemeral message. |
| GET | :token/editEphemeralMessageReplyMarkup | write | messages | Edit only the reply markup of an ephemeral message. |
| POST | :token/editEphemeralMessageReplyMarkup | write | messages | Edit only the reply markup of an ephemeral message. |
| GET | :token/editEphemeralMessageText | write | messages | Edit an ephemeral text or rich message. |
| POST | :token/editEphemeralMessageText | write | messages | Edit an ephemeral text or rich message. |
| GET | :token/editMessageCaption | write | messages | Edit captions of messages. |
| POST | :token/editMessageCaption | write | messages | Edit captions of messages. |
| GET | :token/editMessageChecklist | write | messages | Edit a checklist on behalf of a connected business account. |
| POST | :token/editMessageChecklist | write | messages | Edit a checklist on behalf of a connected business account. |
| GET | :token/editMessageLiveLocation | write | messages | Edit live location messages. |
| POST | :token/editMessageLiveLocation | write | messages | Edit live location messages. |
| GET | :token/editMessageMedia | write | messages | Edit animation, audio, document, live photo, photo, or video messages, or to replace a text or a rich message with a media. |
| POST | :token/editMessageMedia | write | messages | Edit animation, audio, document, live photo, photo, or video messages, or to replace a text or a rich message with a media. |
| GET | :token/editMessageReplyMarkup | write | messages | Edit only the reply markup of messages. |
| POST | :token/editMessageReplyMarkup | write | messages | Edit only the reply markup of messages. |
| GET | :token/editMessageText | write | messages | Edit text, rich and game messages. |
| POST | :token/editMessageText | write | messages | Edit text, rich and game messages. |
| GET | :token/forwardMessage | write | messages | Forward messages of any kind. |
| POST | :token/forwardMessage | write | messages | Forward messages of any kind. |
| GET | :token/forwardMessages | write | messages | Forward multiple messages of any kind. |
| POST | :token/forwardMessages | write | messages | Forward multiple messages of any kind. |
| GET | :token/sendAnimation | write | messages | Send animation files (GIF or H.264/MPEG-4 AVC video without sound). |
| POST | :token/sendAnimation | write | messages | Send animation files (GIF or H.264/MPEG-4 AVC video without sound). |
| GET | :token/sendAudio | write | messages | Send audio files, if you want Telegram clients to display them in the music player. |
| POST | :token/sendAudio | write | messages | Send audio files, if you want Telegram clients to display them in the music player. |
| GET | :token/sendChecklist | write | messages | Send a checklist on behalf of a connected business account. |
| POST | :token/sendChecklist | write | messages | Send a checklist on behalf of a connected business account. |
| GET | :token/sendContact | write | messages | Send phone contacts. |
| POST | :token/sendContact | write | messages | Send phone contacts. |
| GET | :token/sendDice | write | messages | Send an animated emoji that will display a random value. |
| POST | :token/sendDice | write | messages | Send an animated emoji that will display a random value. |
| GET | :token/sendDocument | write | messages | Send general files. |
| POST | :token/sendDocument | write | messages | Send general files. |
| GET | :token/sendLivePhoto | write | messages | Send live photos. |
| POST | :token/sendLivePhoto | write | messages | Send live photos. |
| GET | :token/sendLocation | write | messages | Send point on the map. |
| POST | :token/sendLocation | write | messages | Send point on the map. |
| GET | :token/sendMediaGroup | write | messages | Send a group of photos, live photos, videos, documents or audios as an album. |
| POST | :token/sendMediaGroup | write | messages | Send a group of photos, live photos, videos, documents or audios as an album. |
| GET | :token/sendMessage | write | messages | Send text messages. |
| POST | :token/sendMessage | write | messages | Send text messages. |
| GET | :token/sendMessageDraft | write | messages | Stream a partial message to a user while the message is being generated. |
| POST | :token/sendMessageDraft | write | messages | Stream a partial message to a user while the message is being generated. |
| GET | :token/sendPaidMedia | write | messages | Send paid media. |
| POST | :token/sendPaidMedia | write | messages | Send paid media. |
| GET | :token/sendPhoto | write | messages | Send photos. |
| POST | :token/sendPhoto | write | messages | Send photos. |
| GET | :token/sendPoll | write | messages | Send a native poll. |
| POST | :token/sendPoll | write | messages | Send a native poll. |
| GET | :token/sendRichMessage | write | messages | Send rich messages. |
| POST | :token/sendRichMessage | write | messages | Send rich messages. |
| GET | :token/sendRichMessageDraft | write | messages | Stream a partial rich message to a user while the message is being generated. |
| POST | :token/sendRichMessageDraft | write | messages | Stream a partial rich message to a user while the message is being generated. |
| GET | :token/sendVenue | write | messages | Send information about a venue. |
| POST | :token/sendVenue | write | messages | Send information about a venue. |
| GET | :token/sendVideo | write | messages | Send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document). |
| POST | :token/sendVideo | write | messages | Send video files, Telegram clients support MPEG4 videos (other formats may be sent as Document). |
| GET | :token/sendVideoNote | write | messages | Send a rounded square MPEG4 video of up to 1 minute long. |
| POST | :token/sendVideoNote | write | messages | Send a rounded square MPEG4 video of up to 1 minute long. |
| GET | :token/sendVoice | write | messages | Send audio files, if you want Telegram clients to display the file as a playable voice message. |
| POST | :token/sendVoice | write | messages | Send audio files, if you want Telegram clients to display the file as a playable voice message. |
| GET | :token/setMessageReaction | write | messages | Change the chosen reactions on a message. |
| POST | :token/setMessageReaction | write | messages | Change the chosen reactions on a message. |
| GET | :token/setUserEmojiStatus | write | messages | Changes the emoji status for a given user that previously allowed the bot to manage their emoji status via the Mini App method. |
| POST | :token/setUserEmojiStatus | write | messages | Changes the emoji status for a given user that previously allowed the bot to manage their emoji status via the Mini App method. |
| GET | :token/stopMessageLiveLocation | write | messages | Stop updating a live location message before live_period expires. |
| POST | :token/stopMessageLiveLocation | write | messages | Stop updating a live location message before live_period expires. |
| GET | :token/stopPoll | write | messages | Stop a poll which was sent by the bot. |
| POST | :token/stopPoll | write | messages | Stop a poll which was sent by the bot. |
| GET | :token/setPassportDataErrors | write | passport | Informs a user that some of the Telegram Passport elements they provided contains errors. |
| POST | :token/setPassportDataErrors | write | passport | Informs a user that some of the Telegram Passport elements they provided contains errors. |
| GET | :token/answerPreCheckoutQuery | write | payments | Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an Update with the field. |
| POST | :token/answerPreCheckoutQuery | write | payments | Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an Update with the field. |
| GET | :token/answerShippingQuery | write | payments | If you sent an invoice requesting a shipping address and the parameter is_flexible was specified, the Bot API will send an Update with a. |
| POST | :token/answerShippingQuery | write | payments | If you sent an invoice requesting a shipping address and the parameter is_flexible was specified, the Bot API will send an Update with a. |
| GET | :token/createInvoiceLink | write | payments | Create a link for an invoice. |
| POST | :token/createInvoiceLink | write | payments | Create a link for an invoice. |
| GET | :token/editUserStarSubscription | write | payments | Allows the bot to cancel or re-enable extension of a subscription paid in Telegram Stars. |
| POST | :token/editUserStarSubscription | write | payments | Allows the bot to cancel or re-enable extension of a subscription paid in Telegram Stars. |
| GET | :token/getMyStarBalance | read | payments | A method to get the current Telegram Stars balance of the bot. |
| POST | :token/getMyStarBalance | read | payments | A method to get the current Telegram Stars balance of the bot. |
| GET | :token/getStarTransactions | read | payments | Returns the bot's Telegram Star transactions in chronological order. |
| POST | :token/getStarTransactions | read | payments | Returns the bot's Telegram Star transactions in chronological order. |
| GET | :token/refundStarPayment | write | payments | Refunds a successful payment in Telegram Stars. |
| POST | :token/refundStarPayment | write | payments | Refunds a successful payment in Telegram Stars. |
| GET | :token/sendInvoice | write | payments | Send invoices. |
| POST | :token/sendInvoice | write | payments | Send invoices. |
| GET | :token/addStickerToSet | write | stickers | Add a new sticker to a set created by the bot. |
| POST | :token/addStickerToSet | write | stickers | Add a new sticker to a set created by the bot. |
| GET | :token/createNewStickerSet | write | stickers | Create a new sticker set owned by a user. |
| POST | :token/createNewStickerSet | write | stickers | Create a new sticker set owned by a user. |
| GET | :token/deleteStickerFromSet | write | stickers | Delete a sticker from a set created by the bot. |
| POST | :token/deleteStickerFromSet | write | stickers | Delete a sticker from a set created by the bot. |
| GET | :token/deleteStickerSet | write | stickers | Delete a sticker set that was created by the bot. |
| POST | :token/deleteStickerSet | write | stickers | Delete a sticker set that was created by the bot. |
| GET | :token/getCustomEmojiStickers | read | stickers | Get information about custom emoji stickers by their identifiers. |
| POST | :token/getCustomEmojiStickers | read | stickers | Get information about custom emoji stickers by their identifiers. |
| GET | :token/getForumTopicIconStickers | read | stickers | Get custom emoji stickers, which can be used as a forum topic icon by any user. |
| POST | :token/getForumTopicIconStickers | read | stickers | Get custom emoji stickers, which can be used as a forum topic icon by any user. |
| GET | :token/getStickerSet | read | stickers | Get a sticker set. |
| POST | :token/getStickerSet | read | stickers | Get a sticker set. |
| GET | :token/replaceStickerInSet | write | stickers | Replace an existing sticker in a sticker set with a new one. |
| POST | :token/replaceStickerInSet | write | stickers | Replace an existing sticker in a sticker set with a new one. |
| GET | :token/sendSticker | write | stickers | Send static .WEBP, animated .TGS, or video .WEBM stickers. |
| POST | :token/sendSticker | write | stickers | Send static .WEBP, animated .TGS, or video .WEBM stickers. |
| GET | :token/setCustomEmojiStickerSetThumbnail | write | stickers | Set the thumbnail of a custom emoji sticker set. |
| POST | :token/setCustomEmojiStickerSetThumbnail | write | stickers | Set the thumbnail of a custom emoji sticker set. |
| GET | :token/setStickerEmojiList | write | stickers | Change the list of emoji assigned to a regular or custom emoji sticker. |
| POST | :token/setStickerEmojiList | write | stickers | Change the list of emoji assigned to a regular or custom emoji sticker. |
| GET | :token/setStickerKeywords | write | stickers | Change search keywords assigned to a regular or custom emoji sticker. |
| POST | :token/setStickerKeywords | write | stickers | Change search keywords assigned to a regular or custom emoji sticker. |
| GET | :token/setStickerMaskPosition | write | stickers | Change the mask position of a mask sticker. |
| POST | :token/setStickerMaskPosition | write | stickers | Change the mask position of a mask sticker. |
| GET | :token/setStickerPositionInSet | write | stickers | Move a sticker in a set created by the bot to a specific position. |
| POST | :token/setStickerPositionInSet | write | stickers | Move a sticker in a set created by the bot to a specific position. |
| GET | :token/setStickerSetThumbnail | write | stickers | Set the thumbnail of a regular or mask sticker set. |
| POST | :token/setStickerSetThumbnail | write | stickers | Set the thumbnail of a regular or mask sticker set. |
| GET | :token/setStickerSetTitle | write | stickers | Set the title of a created sticker set. |
| POST | :token/setStickerSetTitle | write | stickers | Set the title of a created sticker set. |
| GET | :token/uploadStickerFile | write | stickers | Upload a file with a sticker for later use in the createNewStickerSet, addStickerToSet, or replaceStickerInSet methods (the file can be used. |
| POST | :token/uploadStickerFile | write | stickers | Upload a file with a sticker for later use in the createNewStickerSet, addStickerToSet, or replaceStickerInSet methods (the file can be used. |
| GET | :token/deleteWebhook | write | updates | Remove webhook integration if you decide to switch back to getUpdates. |
| POST | :token/deleteWebhook | write | updates | Remove webhook integration if you decide to switch back to getUpdates. |
| GET | :token/getUpdates | read | updates | Receive incoming updates using long polling. |
| POST | :token/getUpdates | read | updates | Receive incoming updates using long polling. |
| GET | :token/getWebhookInfo | read | updates | Get current webhook status. |
| POST | :token/getWebhookInfo | read | updates | Get current webhook status. |
| GET | :token/setWebhook | write | updates | Specify a URL and receive incoming updates via an outgoing webhook. |
| POST | :token/setWebhook | write | updates | Specify a URL and receive incoming updates via an outgoing webhook. |
| GET | :token/removeChatVerification | write | verification | Removes verification from a chat that is currently verified on behalf of the organization represented by the bot. |
| POST | :token/removeChatVerification | write | verification | Removes verification from a chat that is currently verified on behalf of the organization represented by the bot. |
| GET | :token/removeUserVerification | write | verification | Removes verification from a user who is currently verified on behalf of the organization represented by the bot. |
| POST | :token/removeUserVerification | write | verification | Removes verification from a user who is currently verified on behalf of the organization represented by the bot. |
| GET | :token/verifyChat | write | verification | Verifies a chat on behalf of the organization which is represented by the bot. |
| POST | :token/verifyChat | write | verification | Verifies a chat on behalf of the organization which is represented by the bot. |
| GET | :token/verifyUser | write | verification | Verifies a user on behalf of the organization which is represented by the bot. |
| POST | :token/verifyUser | write | verification | Verifies a user on behalf of the organization which is represented by the bot. |
| GET | :token/answerWebAppQuery | write | widgets | Set the result of an interaction with a Web App and send a corresponding message on behalf of the user to the chat from which the query originated. |
| POST | :token/answerWebAppQuery | write | widgets | Set the result of an interaction with a Web App and send a corresponding message on behalf of the user to the chat from which the query originated. |
| GET | :token/answerWidgetQuery | write | widgets | Send an answer to a query from a widget. |
| POST | :token/answerWidgetQuery | write | widgets | Send an answer to a query from a widget. |
| GET | :token/editMessageWidgetData | write | widgets | Edit data of a widget in a message sent by the bot or via the bot (for inline bots). |
| POST | :token/editMessageWidgetData | write | widgets | Edit data of a widget in a message sent by the bot or via the bot (for inline bots). |
| GET | :token/editSharedWidgetData | write | widgets | Edit public data of a shared widget created by the bot. |
| POST | :token/editSharedWidgetData | write | widgets | Edit public data of a shared widget created by the bot. |
| GET | :token/savePreparedKeyboardButton | write | widgets | Stores a keyboard button that can be used by a user within a Mini App. |
| POST | :token/savePreparedKeyboardButton | write | widgets | Stores a keyboard button that can be used by a user within a Mini App. |
| GET | :token/sendSharedWidget | write | widgets | Send again a shared widget created by the bot. |
| POST | :token/sendSharedWidget | write | widgets | Send again a shared widget created by the bot. |
| GET | :token/sendWidget | write | widgets | Send a message with an HTML widget. |
| POST | :token/sendWidget | write | widgets | Send a message with an HTML widget. |
