# Lens

Camera web app with live filters and effects, packaged as an Android APK with Capacitor.

## Get the APK

1. Create a new GitHub repo and upload everything in this folder, including the hidden `.github` folder.
2. Push to the `main` branch. The build starts on its own. You can also run it from the Actions tab with "Run workflow".
3. Open the Actions tab, click the latest "Build APK" run, and wait about 5 to 8 minutes.
4. Download the `lens-debug-apk` artifact at the bottom of the run, unzip it, and install `app-debug.apk` on your phone. Allow "install unknown apps" if Android asks.

## Notes

- The web app is `www/index.html`. Edit it, push, and a new APK builds.
- Photos and videos are saved through the Android share sheet. Pick Photos, Files or Drive there.
- The APK is signed with a debug key. It's fine for personal use, but not for the Play Store.
- To run it in a browser, serve `www/` over https or localhost. Cameras are blocked on plain http.
