import re, sys
p = "android/app/src/main/AndroidManifest.xml"
s = open(p, encoding="utf-8").read()
add = [
    '<uses-permission android:name="android.permission.CAMERA" />',
    '<uses-permission android:name="android.permission.RECORD_AUDIO" />',
    '<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />',
    '<uses-feature android:name="android.hardware.camera" android:required="false" />',
    '<uses-feature android:name="android.hardware.microphone" android:required="false" />',
]
add = [a for a in add if a not in s]
if add:
    block = "\n    ".join(add)
    s, n = re.subn(r"</manifest>", "    " + block + "\n</manifest>", s, count=1)
    if n != 1:
        sys.exit("Could not patch manifest")
open(p, "w", encoding="utf-8").write(s)
print(s)
