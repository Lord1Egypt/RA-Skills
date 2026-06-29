---
name: "taptap-godot-integration"
description: "Integrate TapSDK v4 into Godot 4 Android games: login, anti-addiction, cloud save, leaderboard, friends. Invoke when adding TapTap features to a Godot Android project."
---

# TapTap SDK v4 Godot 4 Android Integration Skill

Complete integration guide for TapTap SDK v4 into Godot 4 Android games, covering login, anti-addiction, cloud save, leaderboard, and friends modules.

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  Godot 4 (GDScript)              │
│  ┌──────────────────────────────────────────┐   │
│  │         TapTapManager (Autoload)         │   │
│  │  - SDK lifecycle management              │   │
│  │  - Signal bridging (plugin → game)       │   │
│  │  - Cross-platform abstraction            │   │
│  │    (Android / PC / Mock modes)           │   │
│  └──────────────┬───────────────────────────┘   │
│                 │ Godot Plugin API               │
│  ┌──────────────▼───────────────────────────┐   │
│  │      TapTapPlugin.kt (GodotPlugin)       │   │
│  │  - @UsedByGodot methods                  │   │
│  │  - Signal emission to GDScript           │   │
│  │  - TapSDK v4 API calls                   │   │
│  └──────────────┬───────────────────────────┘   │
│                 │ TapSDK v4                       │
│  ┌──────────────▼───────────────────────────┐   │
│  │            TapTap SDK v4                  │   │
│  │  Login | Compliance | CloudSave |         │   │
│  │  Leaderboard | RelationLite               │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

## Prerequisites

- Godot 4.x with Android export template
- TapTap Developer account (https://developer.taptap.cn/)
- TapSDK v4 credentials: Client ID, Client Token
- Android Studio for building the Godot Android plugin

## Step 1: Project Configuration

### 1.1 Android Plugin build.gradle

Add TapSDK v4 dependencies to your Godot Android plugin's `app/build.gradle`:

```gradle
dependencies {
    implementation 'com.taptap.sdk:tap-core:4.10.2'
    implementation 'com.taptap.sdk:tap-login:4.10.2'
    implementation 'com.taptap.sdk:tap-compliance:4.10.2'
    implementation 'com.taptap.sdk:tap-cloudsave:4.10.2'
    implementation 'com.taptap.sdk:tap-leaderboard-androidx:4.10.2'  // Note: -androidx suffix!
    implementation 'com.taptap.sdk:tap-relation-lite:4.10.2'

    compileOnly 'org.godotengine:godot:4.3.0.stable'
}
```

**Important**: The leaderboard module uses `-androidx` suffix (`tap-leaderboard-androidx`), not `tap-leaderboard`.

### 1.2 Godot Android Plugin descriptor (.gdap)

Create or update `android/plugins/TapTapPlugin.gdap`:

```ini
[config]

name="TapTapPlugin"
binary_type="local"
binary="res://android/plugins/TapTapPlugin.aar"

[dependencies]

local=["com.taptap.sdk:tap-core:4.10.2", "com.taptap.sdk:tap-login:4.10.2", "com.taptap.sdk:tap-compliance:4.10.2", "com.taptap.sdk:tap-cloudsave:4.10.2", "com.taptap.sdk:tap-leaderboard-androidx:4.10.2", "com.taptap.sdk:tap-relation-lite:4.10.2"]

remote=["com.google.code.gson:gson:2.10.1"]
```

### 1.3 AndroidManifest.xml

Add required activities and permissions:

```xml
<uses-permission android:name="android.permission.INTERNET" />

<!-- TapTap Login Activity -->
<activity
    android:name="com.taptap.sdk.login.TapTapLoginActivity"
    android:configChanges="orientation|keyboardHidden|screenSize"
    android:exported="false"
    android:theme="@android:style/Theme.Translucent.NoTitleBar" />
```

## Step 2: Kotlin Plugin Implementation

### 2.1 TapTapPlugin.kt - Full Implementation

```kotlin
package com.yourpackage.taptap

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.util.Log
import android.os.Handler
import android.os.Looper
import org.godotengine.godot.Godot
import org.godotengine.godot.plugin.GodotPlugin
import org.godotengine.godot.plugin.SignalInfo
import org.godotengine.godot.plugin.UsedByGodot
import org.json.JSONObject

// TapSDK v4 imports
import com.taptap.sdk.core.TapTapSdk
import com.taptap.sdk.core.TapTapSdkOptions
import com.taptap.sdk.core.TapTapRegion
import com.taptap.sdk.login.TapTapLogin
import com.taptap.sdk.login.TapTapAccount
import com.taptap.sdk.login.Scopes
import com.taptap.sdk.kit.internal.callback.TapTapCallback
import com.taptap.sdk.kit.internal.exception.TapTapException
import com.taptap.sdk.compliance.TapTapCompliance
import com.taptap.sdk.compliance.TapTapComplianceCallback
import com.taptap.sdk.compliance.constants.ComplianceMessage
import com.taptap.sdk.compliance.option.TapTapComplianceOptions
import com.taptap.sdk.cloudsave.TapTapCloudSave
import com.taptap.sdk.cloudsave.internal.TapCloudSaveRequestCallback
import com.taptap.sdk.cloudsave.internal.TapCloudSaveCallback
import com.taptap.sdk.cloudsave.ArchiveMetadata
import com.taptap.sdk.cloudsave.ArchiveData
import com.taptap.sdk.leaderboard.androidx.TapTapLeaderboard
import com.taptap.sdk.leaderboard.callback.TapTapLeaderboardCallback
import com.taptap.sdk.leaderboard.callback.ITapTapLeaderboardResponseCallback
import com.taptap.sdk.leaderboard.data.request.LeaderboardCollection
import com.taptap.sdk.leaderboard.data.request.SubmitScoresRequest
import com.taptap.sdk.leaderboard.data.response.LeaderboardScoresResponse
import com.taptap.sdk.leaderboard.data.response.UserScoreResponse
import com.taptap.sdk.leaderboard.data.response.SubmitScoresResponse
import com.taptap.sdk.leaderboard.data.response.common.Score
import com.taptap.sdk.relation.lite.TapTapRelationLite
import com.taptap.sdk.relation.lite.internal.TapTapRelationLiteCallback
import com.taptap.sdk.relation.lite.internal.TapTapRelationRequestCallback
import com.taptap.sdk.relation.lite.internal.model.RelationLiteUserItem

class TapTapPlugin(godot: Godot) : GodotPlugin(godot) {

    companion object {
        private const val TAG = "TapTapPlugin"
    }

    private var isInitialized = false
    private var complianceInitialized = false
    private val mainHandler = Handler(Looper.getMainLooper())
    private var currentArchiveId: String? = null

    override fun getPluginName(): String = "TapTapPlugin"

    override fun getPluginSignals(): MutableSet<SignalInfo> {
        return mutableSetOf(
            SignalInfo("on_login_success", String::class.java),
            SignalInfo("on_login_failed", String::class.java),
            SignalInfo("on_login_canceled"),
            SignalInfo("on_logout_finished"),
            SignalInfo("on_anti_addiction_callback", String::class.java, String::class.java),
            SignalInfo("on_cloud_save_result", String::class.java, String::class.java),
            SignalInfo("on_cloud_save_list", String::class.java),
            SignalInfo("on_cloud_save_data", String::class.java),
            SignalInfo("on_leaderboard_result", String::class.java, String::class.java),
            SignalInfo("on_leaderboard_scores", String::class.java),
            SignalInfo("on_leaderboard_user_score", String::class.java),
            SignalInfo("on_friends_list", String::class.java),
        )
    }

    // Thread-safe signal emission
    private fun safeEmit(signalName: String, vararg args: Any) {
        try {
            if (Looper.myLooper() == Looper.getMainLooper()) {
                emitSignal(signalName, *args)
            } else {
                mainHandler.post { emitSignal(signalName, *args) }
            }
        } catch (e: Exception) {
            Log.e(TAG, "safeEmit failed: $signalName", e)
        }
    }

    // ==================== SDK Initialization ====================

    @UsedByGodot
    fun initSDK(clientId: String, clientToken: String, serverUrl: String) {
        val activity = activity ?: return
        try {
            val sdkOptions = TapTapSdkOptions(
                clientId,
                clientToken,
                TapTapRegion.CN,  // Use TapTapRegion.IO for international
                "",
                true,
            )
            val complianceOptions = TapTapComplianceOptions(true, false)
            TapTapSdk.init(activity, sdkOptions, complianceOptions)
            isInitialized = true
        } catch (e: Exception) {
            Log.e(TAG, "Failed to initialize TapSDK v4", e)
        }
    }

    // ==================== Anti-Addiction ====================

    @UsedByGodot
    fun initAntiAddiction(clientId: String) {
        try {
            TapTapCompliance.registerComplianceCallback(
                object : TapTapComplianceCallback {
                    override fun onComplianceResult(code: Int, extra: Map<String, Any>?) {
                        val msg = extra?.entries?.joinToString("; ") { "${it.key}=${it.value}" } ?: ""
                        safeEmit("on_anti_addiction_callback", code.toString(), msg)
                    }
                }
            )
            complianceInitialized = true
        } catch (e: Exception) {
            Log.e(TAG, "Failed to register compliance callback", e)
            safeEmit("on_anti_addiction_callback", "500", "compliance_init_failed")
        }
    }

    @UsedByGodot
    fun checkAntiAddiction() {
        if (!isInitialized || !complianceInitialized) {
            safeEmit("on_anti_addiction_callback", "500", "not_initialized")
            return
        }
        val userId = TapTapLogin.getCurrentTapAccount()?.openId ?: ""
        if (userId.isEmpty()) {
            safeEmit("on_anti_addiction_callback", "500", "no_userid")
            return
        }
        TapTapCompliance.startup(activity!!, userId)
    }

    @UsedByGodot
    fun exitAntiAddiction() {
        if (complianceInitialized) TapTapCompliance.exit()
    }

    // ==================== Login ====================

    @UsedByGodot
    fun login() {
        if (!isInitialized) return
        val activity = activity ?: return
        val scopes = arrayOf(Scopes.SCOPE_PUBLIC_PROFILE, Scopes.SCOPE_USER_FRIENDS)
        TapTapLogin.loginWithScopes(activity, scopes, object : TapTapCallback<TapTapAccount> {
            override fun onSuccess(account: TapTapAccount) {
                val json = JSONObject().apply {
                    put("name", account.name ?: "")
                    put("avatar", account.avatar ?: "")
                    put("user_id", account.openId ?: "")
                    put("openid", account.openId ?: "")
                    put("unionid", account.unionId ?: "")
                }
                safeEmit("on_login_success", json.toString())
            }
            override fun onCancel() { safeEmit("on_login_canceled") }
            override fun onFail(exception: TapTapException) {
                safeEmit("on_login_failed", exception.message ?: "Unknown error")
            }
        })
    }

    @UsedByGodot
    fun logout() {
        TapTapLogin.logout()
        currentArchiveId = null
        safeEmit("on_logout_finished")
    }

    @UsedByGodot
    fun isUserLoggedIn(): Boolean {
        return try { TapTapLogin.getCurrentTapAccount() != null } catch (_: Exception) { false }
    }

    @UsedByGodot
    fun getCurrentUserInfo(): String {
        val account = TapTapLogin.getCurrentTapAccount() ?: return ""
        return JSONObject().apply {
            put("name", account.name ?: "")
            put("avatar", account.avatar ?: "")
            put("user_id", account.openId ?: "")
            put("openid", account.openId ?: "")
            put("unionid", account.unionId ?: "")
        }.toString()
    }

    @UsedByGodot
    fun getDisplayUserId(): String {
        // Generate 8-digit display ID from openId hash
        val openId = TapTapLogin.getCurrentTapAccount()?.openId ?: return ""
        val hash = openId.hashCode().toLong() and 0xFFFFFFFFL
        return String.format("%08d", hash % 100000000L)
    }

    // ==================== Cloud Save ====================

    @UsedByGodot
    fun initCloudSave() {
        TapTapCloudSave.registerCloudSaveCallback(object : TapCloudSaveCallback {
            override fun onResult(resultCode: Int) {
                when (resultCode) {
                    300001 -> safeEmit("on_cloud_save_result", "error", "need_login")
                    300002 -> safeEmit("on_cloud_save_result", "error", "init_failed")
                }
            }
        })
    }

    @UsedByGodot
    fun setCurrentArchiveId(archiveId: String) {
        currentArchiveId = if (archiveId.isEmpty()) null else archiveId
    }

    @UsedByGodot
    fun saveToCloud(saveData: String, summary: String) {
        val activity = this.activity ?: return
        try {
            val saveFile = File(activity.cacheDir, "cloud_save.json")
            saveFile.writeText(saveData)
            val metadata = ArchiveMetadata.Builder()
                .setName("game_save")
                .setSummary(summary)
                .setExtra("")
                .setPlaytime(0)
                .build()
            val callback = object : TapCloudSaveRequestCallback {
                override fun onRequestError(errorCode: Int, errorMessage: String) {
                    safeEmit("on_cloud_save_result", "error", "code=$errorCode msg=$errorMessage")
                }
                override fun onArchiveCreated(archive: ArchiveData) {
                    currentArchiveId = archive.uuid
                    safeEmit("on_cloud_save_result", "created", archive.uuid)
                }
                override fun onArchiveUpdated(archive: ArchiveData) {
                    currentArchiveId = archive.uuid
                    safeEmit("on_cloud_save_result", "updated", archive.uuid)
                }
                override fun onArchiveDeleted(archive: ArchiveData) {
                    if (currentArchiveId == archive.uuid) currentArchiveId = null
                    safeEmit("on_cloud_save_result", "deleted", archive.uuid)
                }
                override fun onArchiveListResult(archiveList: List<ArchiveData>) {}
                override fun onArchiveDataResult(archiveData: ByteArray) {}
                override fun onArchiveCoverResult(coverData: ByteArray) {}
            }
            if (currentArchiveId != null) {
                TapTapCloudSave.updateArchive(currentArchiveId!!, metadata, saveFile.absolutePath, null, callback)
            } else {
                // Query first to avoid duplicates
                TapTapCloudSave.getArchiveList(object : TapCloudSaveRequestCallback {
                    override fun onRequestError(errorCode: Int, errorMessage: String) {
                        TapTapCloudSave.createArchive(metadata, saveFile.absolutePath, null, callback)
                    }
                    override fun onArchiveCreated(archive: ArchiveData) {}
                    override fun onArchiveUpdated(archive: ArchiveData) {}
                    override fun onArchiveDeleted(archive: ArchiveData) {}
                    override fun onArchiveDataResult(archiveData: ByteArray) {}
                    override fun onArchiveCoverResult(coverData: ByteArray) {}
                    override fun onArchiveListResult(archiveList: List<ArchiveData>) {
                        if (archiveList.isNotEmpty()) {
                            currentArchiveId = archiveList[0].uuid
                            TapTapCloudSave.updateArchive(currentArchiveId!!, metadata, saveFile.absolutePath, null, callback)
                        } else {
                            TapTapCloudSave.createArchive(metadata, saveFile.absolutePath, null, callback)
                        }
                    }
                })
            }
        } catch (e: Exception) {
            safeEmit("on_cloud_save_result", "error", e.message ?: "unknown")
        }
    }

    @UsedByGodot
    fun loadCloudSaveList() {
        TapTapCloudSave.getArchiveList(object : TapCloudSaveRequestCallback {
            override fun onRequestError(errorCode: Int, errorMessage: String) {
                safeEmit("on_cloud_save_list", "")
            }
            override fun onArchiveCreated(archive: ArchiveData) {}
            override fun onArchiveUpdated(archive: ArchiveData) {}
            override fun onArchiveDeleted(archive: ArchiveData) {}
            override fun onArchiveDataResult(archiveData: ByteArray) {}
            override fun onArchiveCoverResult(coverData: ByteArray) {}
            override fun onArchiveListResult(archiveList: List<ArchiveData>) {
                if (archiveList.isNotEmpty()) currentArchiveId = archiveList[0].uuid
                val json = JSONObject()
                val arr = org.json.JSONArray()
                for (archive in archiveList) {
                    arr.put(JSONObject().apply {
                        put("archiveId", archive.uuid)
                        put("name", archive.name ?: "")
                        put("summary", archive.summary ?: "")
                        put("fileId", archive.fileId ?: "")
                        put("modifiedTime", archive.modifiedTime)
                    })
                }
                json.put("archives", arr)
                safeEmit("on_cloud_save_list", json.toString())
            }
        })
    }

    @UsedByGodot
    fun loadCloudSaveData(archiveId: String, fileId: String) {
        TapTapCloudSave.getArchiveData(archiveId, fileId, object : TapCloudSaveRequestCallback {
            override fun onRequestError(errorCode: Int, errorMessage: String) {
                safeEmit("on_cloud_save_data", "")
            }
            override fun onArchiveCreated(archive: ArchiveData) {}
            override fun onArchiveUpdated(archive: ArchiveData) {}
            override fun onArchiveDeleted(archive: ArchiveData) {}
            override fun onArchiveListResult(archiveList: List<ArchiveData>) {}
            override fun onArchiveCoverResult(coverData: ByteArray) {}
            override fun onArchiveDataResult(archiveData: ByteArray) {
                safeEmit("on_cloud_save_data", String(archiveData, Charsets.UTF_8))
            }
        })
    }

    // ==================== Leaderboard ====================

    @UsedByGodot
    fun initLeaderboard() {
        TapTapLeaderboard.registerLeaderboardCallback(object : TapTapLeaderboardCallback {
            override fun onLeaderboardResult(code: Int, message: String) {
                safeEmit("on_leaderboard_result", code.toString(), message)
            }
        })
    }

    @UsedByGodot
    fun submitLeaderboardScore(leaderboardId: String, score: Long) {
        val scoreItem = SubmitScoresRequest.ScoreItem(leaderboardId, score)
        val request = SubmitScoresRequest(listOf(scoreItem))
        TapTapLeaderboard.submitScores(request.scores, object : ITapTapLeaderboardResponseCallback<SubmitScoresResponse> {
            override fun onSuccess(result: SubmitScoresResponse) {
                safeEmit("on_leaderboard_result", "0", "submit_success")
            }
            override fun onFailure(code: Int, message: String) {
                safeEmit("on_leaderboard_result", code.toString(), message)
            }
        })
    }

    @UsedByGodot
    fun loadLeaderboardScores(leaderboardId: String, collection: String, page: String) {
        val col = if (collection == "FRIENDS") LeaderboardCollection.FRIENDS else LeaderboardCollection.PUBLIC
        TapTapLeaderboard.loadLeaderboardScores(leaderboardId, col, page, null,
            object : ITapTapLeaderboardResponseCallback<LeaderboardScoresResponse> {
                override fun onSuccess(result: LeaderboardScoresResponse) {
                    try {
                        val json = JSONObject()
                        json.put("leaderboard", JSONObject().apply {
                            put("id", result.leaderboard?.id ?: "")
                            put("name", result.leaderboard?.name ?: "")
                        })
                        val arr = org.json.JSONArray()
                        for (score in result.scores) arr.put(scoreToJson(score))
                        json.put("scores", arr)
                        json.put("nextPage", result.nextPage ?: "")
                        safeEmit("on_leaderboard_scores", json.toString())
                    } catch (e: Exception) {
                        safeEmit("on_leaderboard_scores", "")
                    }
                }
                override fun onFailure(code: Int, message: String) {
                    safeEmit("on_leaderboard_scores", "")
                }
            })
    }

    @UsedByGodot
    fun loadCurrentUserScore(leaderboardId: String, collection: String) {
        val col = if (collection == "FRIENDS") LeaderboardCollection.FRIENDS else LeaderboardCollection.PUBLIC
        TapTapLeaderboard.loadCurrentPlayerLeaderboardScore(leaderboardId, col, null,
            object : ITapTapLeaderboardResponseCallback<UserScoreResponse> {
                override fun onSuccess(result: UserScoreResponse) {
                    val json = scoreToJson(result.currentUserScore ?: return)
                    safeEmit("on_leaderboard_user_score", json.toString())
                }
                override fun onFailure(code: Int, message: String) {
                    safeEmit("on_leaderboard_user_score", "")
                }
            })
    }

    private fun scoreToJson(score: Score): JSONObject {
        val userObj = JSONObject().apply {
            put("name", score.user?.name ?: "")
            put("openid", score.user?.openid ?: "")
            put("avatar", score.user?.avatar?.url ?: "")
        }
        return JSONObject().apply {
            put("rank", score.rank?.toString() ?: "0")
            put("rankDisplay", score.rankDisplay ?: "")
            put("score", score.score?.toString() ?: "0")
            put("scoreDisplay", score.scoreDisplay ?: "")
            put("user", userObj)
        }
    }

    // ==================== Friends ====================

    @UsedByGodot
    fun initFriends() {
        TapTapRelationLite.registerRelationLiteCallback(object : TapTapRelationLiteCallback {
            override fun onRelationLiteResult(code: Int) {
                Log.i(TAG, "RelationLite callback: code=$code")
            }
        })
    }

    @UsedByGodot
    fun getFriendsList(nextPageToken: String) {
        TapTapRelationLite.getFriendsList(nextPageToken = nextPageToken,
            callback = object : TapTapRelationRequestCallback() {
                override fun onFriendsListResult(friendsList: List<RelationLiteUserItem>, nextPageToken: String) {
                    val json = JSONObject()
                    val arr = org.json.JSONArray()
                    for (friend in friendsList) {
                        arr.put(JSONObject().apply {
                            put("openid", friend.user?.openId ?: "")
                            put("name", friend.user?.name ?: "")
                            put("avatar", friend.user?.avatar ?: "")
                        })
                    }
                    json.put("friends", arr)
                    json.put("nextPageToken", nextPageToken)
                    safeEmit("on_friends_list", json.toString())
                }
            })
    }

    // ==================== Update Check ====================

    @UsedByGodot
    fun initUpdate(clientId: String, clientToken: String) {
        // Intent-based update check
    }

    @UsedByGodot
    fun checkUpdate() {
        val activity = this.activity ?: return
        try {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse("taptap://taptap.cn/app?source=outer|update"))
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
            activity.startActivity(intent)
        } catch (e: Exception) {
            val webIntent = Intent(Intent.ACTION_VIEW, Uri.parse("https://www.taptap.cn/"))
            webIntent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
            activity.startActivity(webIntent)
        }
    }
}
```

## Step 3: GDScript Autoload Manager

Create `scripts/autoload/tap_tap_manager.gd` and register it as an Autoload:

```gdscript
extends Node

# ==================== Signals ====================
signal login_success(user_info: Dictionary)
signal login_failed(error: String)
signal login_canceled
signal logout_finished
signal sdk_initialized
signal anti_addiction_callback(code: String, message: String)
signal cloud_save_result(action: String, data: String)
signal cloud_save_list(archives_json: String)
signal cloud_save_data(save_json: String)
signal leaderboard_result(code: String, message: String)
signal leaderboard_scores(scores_json: String)
signal leaderboard_user_score(score_json: String)
signal friends_list(friends_json: String)
signal sdk_api_ready

# ==================== Variables ====================
var _plugin: Object = null
var _is_logged_in: bool = false
var _is_sdk_initialized: bool = false
var _user_info: Dictionary = {}
var _current_archive_id: String = ""
var _login_time: float = 0.0
var _sdk_api_ready: bool = true
var _api_ready_timer: Timer = null
var _mock_mode: bool = false

const PLUGIN_NAME: String = "TapTapPlugin"

func _ready() -> void:
    if OS.get_name() == "Android" and Engine.has_singleton(PLUGIN_NAME):
        _plugin = Engine.get_singleton(PLUGIN_NAME)
        _connect_plugin_signals()
    else:
        _mock_mode = true
        print("TapTapManager: Running in mock mode")

func _connect_plugin_signals() -> void:
    if not _plugin: return
    _plugin.on_login_success.connect(_on_login_success)
    _plugin.on_login_failed.connect(_on_login_failed)
    _plugin.on_login_canceled.connect(_on_login_canceled)
    _plugin.on_logout_finished.connect(_on_logout_finished)
    _plugin.on_anti_addiction_callback.connect(_on_anti_addiction_callback)
    _plugin.on_cloud_save_result.connect(_on_cloud_save_result)
    _plugin.on_cloud_save_list.connect(_on_cloud_save_list)
    _plugin.on_cloud_save_data.connect(_on_cloud_save_data)
    _plugin.on_leaderboard_result.connect(_on_leaderboard_result)
    _plugin.on_leaderboard_scores.connect(_on_leaderboard_scores)
    _plugin.on_leaderboard_user_score.connect(_on_leaderboard_user_score)
    _plugin.on_friends_list.connect(_on_friends_list)

# ==================== Public API ====================

func is_available() -> bool:
    return _plugin != null or _mock_mode

func is_mock_mode() -> bool:
    return _mock_mode

func is_logged_in() -> bool:
    return _is_logged_in

func is_sdk_logged_in() -> bool:
    if _mock_mode: return _is_logged_in
    if not _plugin: return false
    return _plugin.isUserLoggedIn()

func init_sdk(client_id: String, client_token: String, server_url: String) -> void:
    if _mock_mode:
        _is_sdk_initialized = true
        sdk_initialized.emit()
        return
    if not _plugin: return
    _plugin.initSDK(client_id, client_token, server_url)
    _is_sdk_initialized = true
    sdk_initialized.emit()

func init_anti_addiction(client_id: String) -> void:
    if _mock_mode: return
    if not _plugin: return
    _plugin.initAntiAddiction(client_id)

func init_cloud_save() -> void:
    if _mock_mode: return
    if not _plugin: return
    _plugin.initCloudSave()
    if not _current_archive_id.is_empty() and _plugin.has_method("setCurrentArchiveId"):
        _plugin.setCurrentArchiveId(_current_archive_id)

func init_leaderboard() -> void:
    if _mock_mode: return
    if not _plugin: return
    _plugin.initLeaderboard()

func init_friends() -> void:
    if _mock_mode: return
    if not _plugin: return
    _plugin.initFriends()

func init_update(client_id: String, client_token: String) -> void:
    if _mock_mode: return
    if not _plugin: return
    _plugin.initUpdate(client_id, client_token)

func login() -> void:
    if _mock_mode:
        get_tree().create_timer(1.0).timeout.connect(_mock_login_success)
        return
    if not _plugin or not _is_sdk_initialized: return
    _plugin.login()

func logout() -> void:
    if _mock_mode:
        _is_logged_in = false
        _user_info = {}
        logout_finished.emit()
        return
    if not _plugin: return
    _plugin.logout()

func check_anti_addiction() -> void:
    if _mock_mode:
        get_tree().create_timer(1.0).timeout.connect(func():
            anti_addiction_callback.emit("500", "LOGIN_SUCCESS")
        )
        return
    if _plugin and _is_sdk_initialized:
        _plugin.checkAntiAddiction()

func check_update() -> void:
    if _mock_mode: return
    if _plugin: _plugin.checkUpdate()

func save_to_cloud(save_data: String, summary: String) -> void:
    if _mock_mode:
        get_tree().create_timer(1.0).timeout.connect(func():
            cloud_save_result.emit("created", "mock_archive_id")
        )
        return
    if not _plugin or not _sdk_api_ready: return
    _plugin.saveToCloud(save_data, summary)

func load_cloud_save_list() -> void:
    if _mock_mode:
        get_tree().create_timer(1.0).timeout.connect(func():
            cloud_save_list.emit('{"archives":[]}')
        )
        return
    if not _plugin or not _sdk_api_ready: return
    _plugin.loadCloudSaveList()

func load_cloud_save_data(archive_id: String, file_id: String) -> void:
    if _mock_mode:
        get_tree().create_timer(1.0).timeout.connect(func():
            cloud_save_data.emit("")
        )
        return
    if not _plugin: return
    _plugin.loadCloudSaveData(archive_id, file_id)

func submit_leaderboard_score(leaderboard_id: String, score: int) -> void:
    if _mock_mode:
        get_tree().create_timer(0.5).timeout.connect(func():
            leaderboard_result.emit("0", "submit_success")
        )
        return
    if not _plugin or not _sdk_api_ready: return
    _plugin.submitLeaderboardScore(leaderboard_id, score)

func load_leaderboard_scores(leaderboard_id: String, collection: String = "PUBLIC", page: String = "") -> void:
    if _mock_mode: return
    if not _plugin or not _sdk_api_ready: return
    _plugin.loadLeaderboardScores(leaderboard_id, collection, page)

func load_current_user_score(leaderboard_id: String, collection: String = "PUBLIC") -> void:
    if _mock_mode: return
    if not _plugin or not _sdk_api_ready: return
    _plugin.loadCurrentUserScore(leaderboard_id, collection)

func get_friends_list(next_page_token: String = "") -> void:
    if _mock_mode: return
    if not _plugin: return
    _plugin.getFriendsList(next_page_token)

func get_user_info() -> Dictionary:
    return _user_info

func get_user_name() -> String:
    return _user_info.get("name", "")

func get_user_id() -> String:
    return _user_info.get("user_id", "")

func get_display_user_id() -> String:
    if _mock_mode:
        return _user_info.get("openid", "mock_001") if _is_logged_in else ""
    if not _plugin: return ""
    return _plugin.getDisplayUserId()

func get_current_user_info() -> Dictionary:
    if _mock_mode:
        return _user_info if _is_logged_in else {}
    if not _plugin: return {}
    if not _plugin.has_method("getCurrentUserInfo"): return {}
    var json_str = _plugin.getCurrentUserInfo()
    if json_str.is_empty(): return {}
    var json = JSON.new()
    if json.parse(json_str) != OK: return {}
    return json.data if json.data is Dictionary else {}

# ==================== Signal Handlers ====================

func _on_login_success(user_json: String) -> void:
    var json = JSON.new()
    if json.parse(user_json) == OK and json.data is Dictionary:
        _user_info = json.data
    _is_logged_in = true
    _login_time = Time.get_ticks_msec() / 1000.0
    _sdk_api_ready = false
    if _api_ready_timer == null:
        _api_ready_timer = Timer.new()
        _api_ready_timer.one_shot = true
        _api_ready_timer.timeout.connect(_on_api_ready)
        add_child(_api_ready_timer)
    _api_ready_timer.start(1.0)  # Wait for SDK APIs to become available
    login_success.emit(_user_info)

func _on_api_ready() -> void:
    _sdk_api_ready = true
    sdk_api_ready.emit()

func _on_login_failed(error: String) -> void:
    login_failed.emit(error)

func _on_login_canceled() -> void:
    login_canceled.emit()

func _on_logout_finished() -> void:
    _is_logged_in = false
    _user_info = {}
    _login_time = 0.0
    logout_finished.emit()

func _on_anti_addiction_callback(code: String, message: String) -> void:
    anti_addiction_callback.emit(code, message)

func _on_cloud_save_result(action: String, data: String) -> void:
    match action:
        "created", "updated":
            _current_archive_id = data
        "deleted":
            if _current_archive_id == data:
                _current_archive_id = ""
    cloud_save_result.emit(action, data)

func _on_cloud_save_list(archives_json: String) -> void:
    if _current_archive_id.is_empty() and not archives_json.is_empty():
        var json = JSON.new()
        if json.parse(archives_json) == OK and json.data is Dictionary:
            var archives = json.data.get("archives", [])
            if archives is Array and not archives.is_empty():
                _current_archive_id = archives[0].get("archiveId", "")
    cloud_save_list.emit(archives_json)

func _on_cloud_save_data(save_json: String) -> void:
    cloud_save_data.emit(save_json)

func _on_leaderboard_result(code: String, message: String) -> void:
    leaderboard_result.emit(code, message)

func _on_leaderboard_scores(scores_json: String) -> void:
    leaderboard_scores.emit(scores_json)

func _on_leaderboard_user_score(score_json: String) -> void:
    leaderboard_user_score.emit(score_json)

func _on_friends_list(friends_json: String) -> void:
    friends_list.emit(friends_json)

func _mock_login_success() -> void:
    _user_info = {"name": "MockPlayer", "avatar": "", "user_id": "mock_001", "openid": "mock_001"}
    _is_logged_in = true
    _login_time = Time.get_ticks_msec() / 1000.0
    login_success.emit(_user_info)
```

## Step 4: Game Integration

### 4.1 Initialization Flow (main_menu.gd)

```gdscript
const TAPTAP_CLIENT_ID: String = "your_client_id"
const TAPTAP_CLIENT_TOKEN: String = "your_client_token"
const TAPTAP_SERVER_URL: String = ""

func _setup_taptap() -> void:
    if not TapTapManager.is_available():
        return
    TapTapManager.login_success.connect(_on_taptap_login_success)
    TapTapManager.login_failed.connect(_on_taptap_login_failed)
    TapTapManager.anti_addiction_callback.connect(_on_anti_addiction_callback)
    if not GameManager.privacy_agreed:
        # Show privacy popup first
        privacy_popup.show_popup()
    else:
        _init_taptap_sdk()

func _init_taptap_sdk() -> void:
    TapTapManager.init_sdk(TAPTAP_CLIENT_ID, TAPTAP_CLIENT_TOKEN, TAPTAP_SERVER_URL)
    TapTapManager.init_anti_addiction(TAPTAP_CLIENT_ID)
    TapTapManager.init_update(TAPTAP_CLIENT_ID, TAPTAP_CLIENT_TOKEN)
    TapTapManager.init_cloud_save()
    TapTapManager.init_leaderboard()
    TapTapManager.init_friends()
    # Handle cached login session
    if TapTapManager.is_sdk_logged_in():
        _handle_cached_login()

func _handle_cached_login() -> void:
    var user_info = TapTapManager.get_current_user_info()
    if user_info.is_empty(): return
    TapTapManager._is_logged_in = true
    TapTapManager._user_info = user_info
    TapTapManager._sdk_api_ready = false
    # Start API ready timer
    if TapTapManager._api_ready_timer == null:
        TapTapManager._api_ready_timer = Timer.new()
        TapTapManager._api_ready_timer.one_shot = true
        TapTapManager._api_ready_timer.timeout.connect(TapTapManager._on_api_ready)
        TapTapManager.add_child(TapTapManager._api_ready_timer)
    TapTapManager._api_ready_timer.start(2.0)
    TapTapManager.get_friends_list()
    _try_restore_cloud_save()
    TapTapManager.check_anti_addiction()
```

### 4.2 Anti-Addiction Callback Handling

```gdscript
func _on_anti_addiction_callback(code: String, message: String) -> void:
    match code:
        "500":   # LOGIN_SUCCESS - can play
            _try_restore_cloud_save()
            _enter_bookshelf()
        "1000", "1001":  # Need re-login
            ToastManager.show_toast(tr("请重新登录"))
        "1030":  # Time restricted
            ToastManager.show_toast(tr("当前时间无法游戏"))
        "1050":  # Time used up
            ToastManager.show_toast(tr("今日游戏时长已用完"))
        "1100":  # Age restricted
            ToastManager.show_toast(tr("年龄限制，无法进入游戏"))
        "1200":  # Network error
            ToastManager.show_toast(tr("网络错误，请检查网络"))
        _:
            _try_restore_cloud_save()
            _enter_bookshelf()
```

### 4.3 Cloud Save Sync with Loading Mask

```gdscript
var _cloud_save_restore_started: bool = false
var _cloud_sync_mask: CanvasLayer = null
var _cloud_sync_timeout: Timer = null
var _pending_enter_bookshelf: bool = false

# Spinner animation class
class _CloudSyncSpinner extends Control:
    var _angle: float = 0.0
    func _ready():
        custom_minimum_size = Vector2(56, 56)
    func _process(delta):
        _angle = fmod(_angle + delta * 3.5, TAU)
        queue_redraw()
    func _draw():
        var center = size / 2.0
        var radius = min(size.x, size.y) * 0.4
        if radius <= 0: return
        var arc_length = PI * 1.3
        var segments = 30
        var line_width = 4.0
        for i in range(segments):
            var t1 = float(i) / float(segments)
            var t2 = float(i + 1) / float(segments)
            var alpha = 1.0 - t1
            var a1 = _angle + t1 * arc_length
            var a2 = _angle + t2 * arc_length
            var p1 = center + Vector2(cos(a1), sin(a1)) * radius
            var p2 = center + Vector2(cos(a2), sin(a2)) * radius
            draw_line(p1, p2, Color(1, 1, 1, alpha), line_width, true)

func _try_restore_cloud_save() -> void:
    if _cloud_save_restore_started: return
    if not TapTapManager.is_available() or not TapTapManager.is_logged_in() or TapTapManager.is_mock_mode():
        return
    _cloud_save_restore_started = true
    GameManager.cloud_sync_in_progress = true
    var _finish_sync = func():
        GameManager.cloud_sync_in_progress = false
        GameManager.cloud_sync_completed.emit()
    var do_load_list = func():
        TapTapManager.cloud_save_list.connect(func(archives_json):
            if archives_json.is_empty():
                _finish_sync.call()
                return
            var json = JSON.new()
            if json.parse(archives_json) != OK:
                _finish_sync.call()
                return
            var archives = json.data.get("archives", [])
            if archives.is_empty():
                _finish_sync.call()
                return
            var latest = archives[0]
            var archive_id = latest.get("archiveId", "")
            var file_id = latest.get("fileId", "")
            if archive_id.is_empty() or file_id.is_empty():
                _finish_sync.call()
                return
            TapTapManager.cloud_save_data.connect(func(save_json):
                if save_json.is_empty():
                    _finish_sync.call()
                    return
                var comparison = GameManager.compare_with_cloud_save(save_json)
                if comparison["cloud_newer"]:
                    GameManager.load_from_cloud_save(save_json)
                _finish_sync.call()
            , CONNECT_ONE_SHOT)
            TapTapManager.load_cloud_save_data(archive_id, file_id)
        , CONNECT_ONE_SHOT)
        TapTapManager.load_cloud_save_list()
    if TapTapManager._sdk_api_ready:
        do_load_list.call()
    else:
        TapTapManager.sdk_api_ready.connect(do_load_list, CONNECT_ONE_SHOT)

func _enter_bookshelf() -> void:
    if GameManager.cloud_sync_in_progress:
        _pending_enter_bookshelf = true
        _show_cloud_sync_mask()
        if not GameManager.cloud_sync_completed.is_connected(_on_cloud_sync_completed):
            GameManager.cloud_sync_completed.connect(_on_cloud_sync_completed, CONNECT_ONE_SHOT)
        if _cloud_sync_timeout == null:
            _cloud_sync_timeout = Timer.new()
            _cloud_sync_timeout.one_shot = true
            _cloud_sync_timeout.timeout.connect(_on_cloud_sync_timeout)
            add_child(_cloud_sync_timeout)
            _cloud_sync_timeout.start(15.0)
        return
    _do_enter_bookshelf()

func _show_cloud_sync_mask() -> void:
    if _cloud_sync_mask != null:
        _cloud_sync_mask.visible = true
        return
    _cloud_sync_mask = CanvasLayer.new()
    _cloud_sync_mask.layer = 10
    add_child(_cloud_sync_mask)
    var mask = Control.new()
    mask.set_anchors_preset(Control.PRESET_FULL_RECT)
    mask.mouse_filter = Control.MOUSE_FILTER_STOP
    _cloud_sync_mask.add_child(mask)
    var bg = ColorRect.new()
    bg.set_anchors_preset(Control.PRESET_FULL_RECT)
    bg.color = Color(0, 0, 0, 0.6)
    mask.add_child(bg)
    var center_box = VBoxContainer.new()
    center_box.set_anchors_preset(Control.PRESET_CENTER)
    center_box.offset_left = -60
    center_box.offset_top = -50
    center_box.offset_right = 60
    center_box.offset_bottom = 50
    center_box.alignment = BoxContainer.ALIGNMENT_CENTER
    mask.add_child(center_box)
    var spinner = _CloudSyncSpinner.new()
    center_box.add_child(spinner)
    var label = Label.new()
    label.text = tr("正在同步云存档")
    label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    label.add_theme_color_override("font_color", Color(1, 1, 1, 1))
    label.add_theme_font_size_override("font_size", 22)
    center_box.add_child(label)

func _hide_cloud_sync_mask() -> void:
    if _cloud_sync_mask != null:
        _cloud_sync_mask.queue_free()
        _cloud_sync_mask = null
    if _cloud_sync_timeout != null:
        _cloud_sync_timeout.stop()
        _cloud_sync_timeout.queue_free()
        _cloud_sync_timeout = null

func _on_cloud_sync_completed() -> void:
    _hide_cloud_sync_mask()
    if _pending_enter_bookshelf:
        _pending_enter_bookshelf = false
        _do_enter_bookshelf()

func _on_cloud_sync_timeout() -> void:
    _hide_cloud_sync_mask()
    if _pending_enter_bookshelf:
        _pending_enter_bookshelf = false
        _do_enter_bookshelf()
```

### 4.4 Leaderboard Data Layer

```gdscript
# scripts/data/leaderboard_data.gd
static var _global_cache: Array = []
static var _friends_cache: Array = []
static var _cache_timestamp: Dictionary = {}
static var _dirty: bool = false
var _taptap_global_loading: bool = false
var _taptap_friends_loading: bool = false
var _pending_collection: String = ""

const LEADERBOARD_ID: String = "your_leaderboard_id"
const REFRESH_INTERVAL_GLOBAL: int = 60
const REFRESH_INTERVAL_FRIENDS: int = 60

enum TabType { GLOBAL, FRIENDS }

func get_leaderboard(tab: int, _region: String = "") -> Array:
    match tab:
        TabType.GLOBAL: return _get_global()
        TabType.FRIENDS: return _get_friends()
    return []

func _get_global() -> Array:
    var now = Time.get_unix_time_from_system()
    if not _dirty and not _global_cache.is_empty() and _cache_timestamp.has("global"):
        if now - _cache_timestamp["global"] < REFRESH_INTERVAL_GLOBAL:
            return _global_cache
    _dirty = false
    if TapTapManager.is_available() and TapTapManager.is_logged_in():
        if not _taptap_global_loading:
            _taptap_global_loading = true
            _pending_collection = "PUBLIC"
            if not TapTapManager.leaderboard_scores.is_connected(_on_taptap_global_scores):
                TapTapManager.leaderboard_scores.connect(_on_taptap_global_scores)
            TapTapManager.load_leaderboard_scores(LEADERBOARD_ID, "PUBLIC")
    return _global_cache

func _parse_taptap_scores(scores_json: String) -> Array:
    if scores_json.is_empty(): return []
    var json = JSON.new()
    if json.parse(scores_json) != OK: return []
    var data = json.data
    if not data is Dictionary: return []
    var scores = data.get("scores", [])
    if not scores is Array: return []
    var current_openid = ""
    if TapTapManager.is_logged_in():
        current_openid = TapTapManager.get_user_id()
    var entries = []
    for i in range(scores.size()):
        var s = scores[i]
        var user = s.get("user", {})
        var openid = user.get("openid", "")
        var is_me = openid == current_openid and not openid.is_empty()
        var score_val = int(s.get("score", "0"))
        var avatar_url = ""
        var avatar_data = user.get("avatar", "")
        if avatar_data is Dictionary:
            avatar_url = avatar_data.get("url", "")
        elif avatar_data is String:
            avatar_url = avatar_data
        entries.append({
            "user_id": openid,
            "nickname": user.get("name", ""),
            "avatar_url": avatar_url,
            "avatar_index": i % 12,
            "score": float(score_val),
            "score_display": str(score_val),
            "is_me": is_me,
        })
    return entries

func _on_taptap_global_scores(scores_json: String) -> void:
    _taptap_global_loading = false
    if _pending_collection != "PUBLIC": return
    _pending_collection = ""
    var entries = _parse_taptap_scores(scores_json)
    if not entries.is_empty():
        entries.sort_custom(func(a, b): return a.score > b.score)
        for i in range(entries.size()):
            entries[i]["rank"] = i + 1
    _global_cache = entries
    _cache_timestamp["global"] = Time.get_unix_time_from_system()

static func mark_dirty() -> void:
    _dirty = true

func invalidate_cache(tab: int = -1) -> void:
    if tab == -1:
        _global_cache.clear()
        _friends_cache.clear()
        _cache_timestamp.clear()
        return
    match tab:
        TabType.GLOBAL:
            _global_cache.clear()
            _cache_timestamp.erase("global")
        TabType.FRIENDS:
            _friends_cache.clear()
            _cache_timestamp.erase("friends")
```

### 4.5 Leaderboard Score Submission

```gdscript
# In game_manager.gd
var _leaderboard_submit_timer: Timer = null

func complete_puzzle(puzzle_id: String) -> void:
    # ... existing puzzle completion logic ...
    _submit_leaderboard_score()

func _submit_leaderboard_score() -> void:
    if not TapTapManager.is_available() or not TapTapManager.is_logged_in():
        return
    if _leaderboard_submit_timer == null:
        _leaderboard_submit_timer = Timer.new()
        _leaderboard_submit_timer.one_shot = true
        _leaderboard_submit_timer.timeout.connect(_do_leaderboard_submit)
        add_child(_leaderboard_submit_timer)
    if not _leaderboard_submit_timer.is_stopped():
        _leaderboard_submit_timer.stop()
    _leaderboard_submit_timer.start(5.0)  # 5-second debounce

func _do_leaderboard_submit() -> void:
    var score = completed_puzzles.size()
    TapTapManager.submit_leaderboard_score(LeaderboardDataScript.LEADERBOARD_ID, score)
```

### 4.6 Avatar Loading in Rank Rows

```gdscript
# In rank_row.gd
var _http_request: HTTPRequest = null
const AVATAR_SIZE := Vector2(56, 56)

func _load_avatar_from_url(url: String) -> void:
    if _http_request == null:
        _http_request = HTTPRequest.new()
        _http_request.request_completed.connect(_on_avatar_loaded)
        add_child(_http_request)
    _avatar.modulate.a = 0.0
    _http_request.request(url)

func _on_avatar_loaded(_result: int, _code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
    if body.is_empty():
        _setup_fallback_avatar(0)
        _avatar.modulate.a = 1.0
        return
    var img = Image.new()
    var err = img.load_png_from_buffer(body)
    if err != OK: err = img.load_jpg_from_buffer(body)
    if err != OK: err = img.load_webp_from_buffer(body)
    if err != OK:
        _setup_fallback_avatar(0)
        _avatar.modulate.a = 1.0
        return
    img.convert(Image.FORMAT_RGBA8)
    img = _make_circular(img)
    _avatar.texture = ImageTexture.create_from_image(img)
    _avatar.modulate.a = 1.0

func _make_circular(img: Image) -> Image:
    var size = Vector2(img.get_width(), img.get_height())
    var target = AVATAR_SIZE
    if size != target:
        img.resize(int(target.x), int(target.y), Image.INTERPOLATE_LANCZOS)
    var center = target * 0.5
    var radius = min(target.x, target.y) * 0.48
    for y in range(int(target.y)):
        for x in range(int(target.x)):
            if Vector2(x, y).distance_to(center) > radius:
                img.set_pixel(x, y, Color(0, 0, 0, 0))
    return img
```

## Key Technical Notes

### ScoreItem Limitations
`SubmitScoresRequest.ScoreItem` only has `leaderboardId` and `score` fields. It does **NOT** support extra metadata (country, region, etc.). If you need region-based leaderboards, you must create separate leaderboards on the TapTap developer console.

### API Ready Timing
After login, TapSDK APIs (cloud save, leaderboard) are not immediately available. Always wait for `sdk_api_ready` signal before calling these APIs. The recommended delay is 1-2 seconds after login callback.

### Cached Login Sessions
When the app restarts, `TapTapLogin.getCurrentTapAccount()` may return a cached session. You must:
1. Call `getCurrentUserInfo()` to verify the session
2. Set `_is_logged_in = true` and `_user_info` manually
3. Start the API ready timer before calling any API
4. Trigger cloud save restore after API is ready

### Cloud Save Unauthenticated Error
If you call cloud save APIs before the SDK is fully authenticated, you'll get `Unauthenticated: login required`. Always:
1. Check `_sdk_api_ready` before calling cloud save
2. For cached sessions, wait for `sdk_api_ready` signal
3. Use the loading mask pattern to prevent users from seeing stale data

### Leaderboard -androidx Suffix
The leaderboard module dependency must use `tap-leaderboard-androidx`, not `tap-leaderboard`. Using the wrong one will cause compilation errors.

### Thread Safety
All TapSDK callbacks run on background threads. Use `mainHandler.post {}` in Kotlin to emit signals on the main thread, or use the `safeEmit` helper pattern shown in the code.

### 8-Digit Display User ID
Generate a user-friendly 8-digit ID from openId:
```kotlin
val hash = openId.hashCode().toLong() and 0xFFFFFFFFL
val displayId = String.format("%08d", hash % 100000000L)
```

## Anti-Addiction Code Reference

| Code | Meaning | Action |
|------|---------|--------|
| 500 | LOGIN_SUCCESS | Allow entry |
| 1000/1001 | Need re-login | Prompt re-login |
| 1030 | Time restricted | Show time restriction message |
| 1050 | Time used up | Show time limit message |
| 1100 | Age restricted | Block entry |
| 1200 | Network error | Show network error |

## Cloud Save Data Flow

```
App Start → Check cached login → Restore session → Wait for API ready
    ↓
Load cloud save list → Get latest archive → Download save data
    ↓
Compare with local save → If cloud newer, apply cloud save
    ↓
Emit cloud_sync_completed → Enter game
```

## Leaderboard Data Flow

```
User opens leaderboard → Check cache (with TTL)
    ↓ (cache miss)
Call TapTapLeaderboard.loadLeaderboardScores()
    ↓
Receive on_leaderboard_scores signal → Parse JSON
    ↓
Extract: rank, score, user.name, user.openid, user.avatar.url
    ↓
Sort by score desc → Assign ranks → Update cache → Display
```
