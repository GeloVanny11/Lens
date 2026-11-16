# Lens

Camera web app with live filters and effects, packaged as an Android APK with Capacitor.

## Get the APK

1. Create a new GitHub repo and upload everything in this folder, including the hidden `.github` folder (drag the folders in, not just the files).
2. Commit to the `main` branch. The build starts on its own. You can also run it from the Actions tab with "Run workflow".
3. Wait about 5 to 8 minutes. Then either:
   - open the repo's **Releases** section (right sidebar) and download `lens-debug.apk`, or
   - open the Actions run and download the `lens-debug-apk` artifact (a zip).
4. Install the APK on your phone. Allow "install unknown apps" if Android asks.

If the build fails, open the failed run in the Actions tab and send me the red error lines.

## Notes

- The web app is `www/index.html`. Edit it, push, and a new APK builds.
- Photos and videos save automatically when you capture. Photos go to Pictures/Lens and videos to Movies/Lens, so they show up in your Gallery. This needs Android 10 or newer.
- The APK is signed with a debug key. Fine for personal use, not for the Play Store.
- The app icon comes from `assets/icon-only.png`. Replace it with your own 1024x1024 PNG.
- To run it in a browser, serve `www/` over https or localhost. Cameras are blocked on plain http.
