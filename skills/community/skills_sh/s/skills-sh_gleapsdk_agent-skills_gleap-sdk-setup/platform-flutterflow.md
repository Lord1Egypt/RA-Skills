# FlutterFlow SDK

## Step 1: Add Dependency

In FlutterFlow, go to **Custom Code** > pubspec.yaml dependencies.
Add the latest `gleap_sdk` from [pub.dev/packages/gleap_sdk](https://pub.dev/packages/gleap_sdk).
Refresh the code editor to load pubspec dependencies.

## Step 2: Create Custom Action

Create a new Custom Action named `gleapInitialize`:

```dart
// Automatic FlutterFlow imports
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/custom_code/actions/index.dart';
import '/flutter_flow/custom_functions.dart';
import 'package:flutter/material.dart';
// Begin custom action code

import 'package:gleap_sdk/gleap_sdk.dart';

Future gleapInitialize() async {
  Gleap.initialize(token: 'API_KEY');
}
```

Keep the FlutterFlow boilerplate imports above the custom code.

## Step 3: Web CDN (for web deployment)

In **App Settings > Web Deployment > Custom Headers**, add:

```html
<script>
!function(Gleap,t,i){if(!(Gleap=window.Gleap=window.Gleap||[]).invoked){for(window.GleapActions=[],Gleap.invoked=!0,Gleap.methods=["identify","setEnvironment","setTags","attachCustomData","setCustomData","removeCustomData","clearCustomData","registerCustomAction","trackEvent","log","preFillForm","showSurvey","sendSilentCrashReport","startFeedbackFlow","startBot","setAppBuildNumber","setAppVersionCode","setApiUrl","setFrameUrl","isOpened","open","close","on","setLanguage","setOfflineMode","initialize","disableConsoleLogOverwrite","logEvent","hide","enableShortcuts","showFeedbackButton","destroy","getIdentity","isUserIdentified","clearIdentity","openConversations","openConversation","openHelpCenterCollection","openHelpCenterArticle","openHelpCenter","searchHelpCenter","openNewsArticle","openNews","openFeatureRequests","isLiveMode"],Gleap.f=function(e){return function(){var t=Array.prototype.slice.call(arguments);window.GleapActions.push({e:e,a:t})}},t=0;t<Gleap.methods.length;t++)Gleap[i=Gleap.methods[t]]=Gleap.f(i);Gleap.load=function(){var t=document.getElementsByTagName("head")[0],i=document.createElement("script");i.type="text/javascript",i.async=!0,i.src="https://sdk.gleap.io/latest/index.js",t.appendChild(i)},Gleap.load()}}();
</script>
```

## Step 4: Wire the Action

Go to **Custom Files > main.dart > Final Actions**.
Add `gleapInitialize` and save.

## Step 5: Build & Run

Deploy your app. Gleap will be active on iOS, Android, and Web.

## Additional API Usage

For advanced features (identify users, track events, custom data), create additional Custom Actions using the Flutter Gleap SDK methods. See `platform-flutter.md` for the full Dart API reference.
