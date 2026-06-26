---
name: teamgram-bff-aggregation
description: Complete reference for the BFF aggregation layer in Teamgram Server with all 27 RPC modules and 268 handlers implementing Telegram-compatible API endpoints.
compatibility: Documentation/knowledge skill only. No executable code. Reference material for Teamgram Server developers.
metadata:
  author: zhihang9978
  version: "1.0.0"
  source: https://github.com/teamgram/teamgram-server
  homepage: https://github.com/teamgram/teamgram-server
  openclaw:
    requires:
      env: []
      bins: []
    securityNotes: |
      Documentation-only skill. Contains no executable code, no network calls, no credential handling.
      Handler names listed are Telegram TL API method names from the public TL schema.
      All content references the open-source teamgram-server project (Apache-2.0).
---

# BFF 聚合层：bff.bff（27 个 RPC 模块，268 个 handler）

## 概述

bff.bff 是 Telegram RPC 的主要实现层。它本质上是一个 go-zero zrpc gRPC server，注册了多个 `mtproto.RegisterRPCxxxServer`。

## 27 个模块总览与 handler 数量

| module | handlers | 说明 |
|---|---:|---|
| account | 8 | 账户TTL/换手机号/删除账户 |
| authorization | 29 | 登录/注册/二步验证/邮箱验证 |
| autodownload | 2 | 自动下载设置 |
| chatinvites | 14 | 聊天邀请链接/加群请求 |
| chats | 23 | 群组管理/创建/迁移/管理员 |
| configuration | 11 | 帮助/配置/国家列表/更新检查 |
| contacts | 23 | 联系人管理/搜索/屏蔽/导入 |
| dialogs | 15 | 对话列表/置顶/标记未读/输入状态 |
| drafts | 3 | 消息草稿 |
| files | 12 | 文件上传/下载/CDN |
| messages | 33 | 消息发送/编辑/删除/搜索/转发/置顶 |
| miscellaneous | 2 | 测试/日志 |
| notification | 7 | 通知设置/设备注册 |
| nsfw | 2 | 内容设置 |
| passkey | 6 | Passkey 认证 |
| passport | 11 | Telegram Passport |
| premium | 5 | Premium/支付 |
| privacysettings | 8 | 隐私设置/全局隐私 |
| qrcode | 3 | QR 码登录 |
| savedmessagedialogs | 9 | 保存的消息对话 |
| sponsoredmessages | 11 | 赞助消息 |
| tos | 2 | 服务条款 |
| updates | 3 | 获取状态/差异/频道差异 |
| userchannelprofiles | 18 | 用户资料/头像/频道资料 |
| usernames | 5 | 用户名管理 |
| users | 4 | 用户查询 |

## 全量 Handler 清单

### account (8)
- AccountSetAccountTTL
- AccountSendChangePhoneCode
- AccountResetAuthorization
- AccountGetAccountTTL
- AccountSendConfirmPhoneCode
- AccountConfirmPhone
- AccountChangePhone
- AccountDeleteAccount

### authorization (29)
- AuthToggleBan
- AuthSignIn
- AuthSendCode / authSendCode
- AuthResetLoginEmail
- AuthResetAuthorizations
- AuthResendCode
- AuthRequestPasswordRecovery
- AuthRequestFirebaseSms
- AuthReportMissingCode
- AuthRecoverPassword
- AuthImportWebTokenAuthorization
- AuthImportBotAuthorization
- AuthImportAuthorization
- AuthExportAuthorization
- AuthDropTempAuthKeys
- AuthCheckRecoveryPassword
- AuthCheckPassword
- AuthCheckPaidAuth
- AuthCancelCode
- AuthBindTempAuthKey
- AccountVerifyEmailECBA39DB
- AccountVerifyEmail32DA4CF
- AccountSetAuthorizationTTL
- AccountSendVerifyEmailCode
- AccountResetPassword
- AccountInvalidateSignInCodes
- AccountChangeAuthorizationSettings
- AuthSignUp
- onContactSignUp
- AuthLogOut

### autodownload (2)
- AccountSaveAutoDownloadSettings
- AccountGetAutoDownloadSettings

### chatinvites (14)
- MessagesImportChatInvite
- MessagesHideAllChatJoinRequests
- MessagesGetExportedChatInvites
- MessagesGetExportedChatInvite
- MessagesGetChatInviteImporters
- MessagesGetAdminsWithInvites
- MessagesExportChatInvite
- MessagesEditExportedChatInvite
- MessagesDeleteRevokedExportedChatInvites
- MessagesDeleteExportedChatInvite
- MessagesCheckChatInvite
- ChannelsToggleJoinRequest
- MessagesHideChatJoinRequest
- ChannelsToggleJoinToSend

### chats (23)
- MessagesMigrateChat
- MessagesGetMessageReadParticipants2C6F97B7
- MessagesGetFullChat
- MessagesGetCommonChats
- MessagesGetChats
- MessagesGetAllChats
- MessagesEditChatTitle
- MessagesEditChatPhoto
- MessagesEditChatDefaultBannedRights
- MessagesGetMessageReadParticipants31C1C44F
- MessagesEditChatAdmin
- MessagesDeleteChat
- MessagesDeleteChatUser
- MessagesEditChatAbout
- createChat
- MessagesCreateChat9CB126E
- MessagesCreateChat92CEDDD4
- addChatUser
- MessagesAddChatUserF24753E3
- MessagesAddChatUserCBC6D107
- ChannelsSetEmojiStickers
- ChannelsConvertToGigagroup
- MessagesCreateChat34A818

### configuration (11)
- HelpGetSupport
- HelpGetNearestDc
- HelpGetInviteText
- HelpGetCountriesList
- HelpGetAppUpdate
- HelpGetAppConfig98914110
- HelpGetAppConfig61E3F854
- HelpGetAppChangelog
- HelpDismissSuggestion
- HelpGetSupportName
- HelpGetConfig

### contacts (23)
- ContactsUpdateContactNote
- ContactsToggleTopPeers
- ContactsSetBlocked
- ContactsSearch
- ContactsResetTopPeerRating
- ContactsResetSaved
- ContactsImportContacts
- ContactsGetTopPeers
- ContactsGetStatuses
- ContactsGetSaved
- ContactsGetLocated
- ContactsGetContacts
- ContactsGetContactIDs
- ContactsGetBlocked
- ContactsEditCloseFriends
- ContactsDeleteByPhones
- ContactsBlock
- ContactsAddContact
- ContactsAcceptContact
- ContactsUnblock
- AccountSetContactSignUpNotification
- AccountGetContactSignUpNotification
- ContactsDeleteContacts

### dialogs (15)
- MessagesToggleDialogPin
- MessagesSetHistoryTTL
- MessagesSendScreenshotNotification
- MessagesReorderPinnedDialogs
- MessagesMarkDialogUnread
- MessagesHidePeerSettingsBar
- MessagesGetSavedHistory
- MessagesGetSavedDialogs
- MessagesGetPinnedDialogs
- MessagesGetPeerSettings
- MessagesGetPeerDialogs
- MessagesGetOnlines
- MessagesGetDialogs
- MessagesSetTyping
- MessagesGetDialogUnreadMarks

### drafts (3)
- MessagesSaveDraft
- MessagesClearAllDrafts
- MessagesGetAllDrafts

### files (12)
- UploadSaveFilePart
- UploadReuploadCdnFile
- UploadGetWebFile
- UploadGetFile
- UploadGetFileHashes
- UploadGetCdnFile
- UploadGetCdnFileHashes
- MessagesUploadMedia
- makeMediaByInputMedia
- MessagesUploadEncryptedFile
- MessagesGetDocumentByHash
- HelpGetCdnConfig
- UploadSaveBigFilePart

### messages (33)
- MessagesUpdatePinnedMessage
- MessagesToggleNoForwards
- MessagesSummarizeText
- MessagesSendMultiMedia
- MessagesSendMessage
- MessagesSendMedia
- MessagesSearch
- MessagesSearchGlobal
- MessagesUnpinAllMessages
- MessagesSaveDefaultSendAs
- MessagesReceivedMessages
- MessagesReadMentions
- MessagesReadMessageContents
- MessagesReadHistory
- MessagesGetUnreadMentions
- MessagesGetSearchResultsCalendar
- MessagesGetSearchCounters
- MessagesGetSearchResultsPositions
- MessagesGetRecentLocations
- MessagesGetMessages
- MessagesGetMessagesViews
- MessagesGetMessageEditData
- MessagesGetExtendedMedia
- MessagesSearchSentMedia
- MessagesGetHistory
- MessagesForwardMessages
- checkForwardPrivacy
- makeForwardMessages
- MessagesDeleteMessages
- MessagesDeleteHistory
- MessagesEditMessage
- ChannelsSearchPosts
- ChannelsGetSendAs
- ChannelsCheckSearchPostsFlood
- MessagesGetOutboxReadDate

### miscellaneous (2)
- HelpTest
- HelpSaveAppLog

### notification (7)
- AccountUpdateNotifySettings
- AccountUnregisterDevice
- AccountResetNotifySettings
- AccountGetNotifySettings
- AccountGetNotifyExceptions
- AccountUpdateDeviceLocked
- AccountRegisterDevice

### nsfw (2)
- AccountSetContentSettings
- AccountGetContentSettings

### passkey (6)
- AuthInitPasskeyLogin
- AccountRegisterPasskey
- AccountInitPasskeyRegistration
- AccountGetPasskeys
- AuthFinishPasskeyLogin
- AccountDeletePasskey

### passport (11)
- UsersSetSecureValueErrors
- AccountVerifyPhone
- AccountSendVerifyPhoneCode
- AccountSaveSecureValue
- AccountGetSecureValue
- AccountGetAuthorizations
- AccountGetAuthorizationForm
- AccountGetAllSecureValues
- AccountDeleteSecureValue
- AccountAcceptAuthorization
- HelpGetPassportConfig

### premium (5)
- PaymentsCanPurchaseStore
- PaymentsAssignPlayMarketTransaction
- PaymentsAssignAppStoreTransaction
- HelpGetPremiumPromo
- PaymentsCanPurchasePremium

### privacysettings (8)
- UsersGetRequirementsToContact
- MessagesSetDefaultHistoryTTL
- MessagesGetDefaultHistoryTTL
- AccountSetPrivacy
- AccountSetGlobalPrivacySettings
- AccountGetGlobalPrivacySettings
- UsersGetIsPremiumRequiredToContact
- AccountGetPrivacy

### qrcode (3)
- AuthImportLoginToken
- AuthAcceptLoginToken
- AuthExportLoginToken

### savedmessagedialogs (9)
- MessagesToggleSavedDialogPin
- MessagesReadSavedHistory
- MessagesGetSavedHistory
- MessagesGetSavedDialogs
- MessagesGetSavedDialogsByID
- MessagesGetPinnedSavedDialogs
- MessagesReorderPinnedSavedDialogs
- ChannelsGetMessageAuthor
- MessagesDeleteSavedHistory

### sponsoredmessages (11)
- MessagesViewSponsoredMessage
- MessagesGetSponsoredMessages
- MessagesClickSponsoredMessage
- ContactsGetSponsoredPeers
- ChannelsViewSponsoredMessage
- ChannelsRestrictSponsoredMessages
- ChannelsReportSponsoredMessage
- ChannelsGetSponsoredMessages
- ChannelsClickSponsoredMessage
- MessagesReportSponsoredMessage
- AccountToggleSponsoredMessages

### tos (2)
- HelpGetTermsOfServiceUpdate
- HelpAcceptTermsOfService

### updates (3)
- UpdatesGetState
- UpdatesGetDifference
- UpdatesGetChannelDifference

### userchannelprofiles (18)
- UsersSuggestBirthday
- UsersGetSavedMusicByID
- PhotosUploadProfilePhoto
- PhotosUpdateProfilePhoto
- PhotosGetUserPhotos
- PhotosDeletePhotos
- ContactsGetBirthdays
- ChannelsSetMainProfileTab
- UsersGetSavedMusic
- AccountUpdateVerified
- AccountUpdateProfile
- AccountUpdateStatus
- AccountUpdatePersonalChannel
- AccountSetMainProfileTab
- AccountUpdateBirthday
- AccountSaveMusic
- AccountGetSavedMusicIds
- PhotosUploadContactProfilePhoto

### usernames (5+1)
- ContactsResolveUsername
- ChannelsCheckUsername
- AccountUpdateUsername
- updateUsername
- AccountCheckUsername
- ChannelsUpdateUsername

### users (4)
- UsersGetUsers
- UsersGetMe
- UsersGetFullUser
- ContactsResolvePhone

## 典型请求模式：auth.sendCode

auth.sendCode 的 handler 展示 BFF 的典型模式：
1. 校验 api_id/api_hash
2. 解析/校验手机号
3. 调用 biz.user 查询用户是否存在
4. 调用 status 获取在线会话 → 决定是否走 app code
5. 调用 VerifyCodeInterface 下发短信

常见错误（TL/协议层）：
- PHONE_NUMBER_INVALID / PHONE_NUMBER_BANNED / PHONE_NUMBER_FLOOD
- SESSION_PASSWORD_NEEDED（两步验证）
- *_MIGRATE_*（跨 DC 重定向：Teamgram 社区版常保留 TODO）

## 关键代码路径

- BFF 模块目录：`app/bff/<module>/internal/core/*_handler.go`
- BFF 聚合注册：`app/bff/bff/internal/server/server.go`
- 配置文件：`teamgramd/etc/bff.yaml`


## Source Code References

- Repository: https://github.com/teamgram/teamgram-server (Apache-2.0)
