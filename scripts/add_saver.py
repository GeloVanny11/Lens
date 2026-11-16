"""Adds a native plugin that saves photos/videos straight into the gallery."""
import os, re

PKG_DIR = "android/app/src/main/java/com/lens/camera"
os.makedirs(PKG_DIR, exist_ok=True)

open(f"{PKG_DIR}/LensSaverPlugin.java", "w").write('''package com.lens.camera;

import android.content.ContentResolver;
import android.content.ContentValues;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.io.OutputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@CapacitorPlugin(name = "LensSaver")
public class LensSaverPlugin extends Plugin {

    private static class Entry {
        Uri uri;
        OutputStream out;
    }

    private final Map<String, Entry> entries = new HashMap<>();

    @PluginMethod
    public void begin(PluginCall call) {
        try {
            String name = call.getString("name", "lens.jpg");
            String mime = call.getString("mime", "image/jpeg");
            boolean video = mime.startsWith("video");
            ContentResolver r = getContext().getContentResolver();
            ContentValues v = new ContentValues();
            v.put(MediaStore.MediaColumns.DISPLAY_NAME, name);
            v.put(MediaStore.MediaColumns.MIME_TYPE, mime);
            v.put(MediaStore.MediaColumns.RELATIVE_PATH,
                (video ? Environment.DIRECTORY_MOVIES : Environment.DIRECTORY_PICTURES) + "/Lens");
            v.put(MediaStore.MediaColumns.IS_PENDING, 1);
            Uri base = video ? MediaStore.Video.Media.EXTERNAL_CONTENT_URI
                             : MediaStore.Images.Media.EXTERNAL_CONTENT_URI;
            Uri uri = r.insert(base, v);
            if (uri == null) { call.reject("Could not create file"); return; }
            Entry e = new Entry();
            e.uri = uri;
            e.out = r.openOutputStream(uri);
            String id = UUID.randomUUID().toString();
            entries.put(id, e);
            JSObject res = new JSObject();
            res.put("id", id);
            call.resolve(res);
        } catch (Exception ex) {
            call.reject(String.valueOf(ex.getMessage()));
        }
    }

    @PluginMethod
    public void write(PluginCall call) {
        try {
            Entry e = entries.get(call.getString("id"));
            if (e == null) { call.reject("Unknown save id"); return; }
            e.out.write(Base64.decode(call.getString("data", ""), Base64.DEFAULT));
            call.resolve();
        } catch (Exception ex) {
            call.reject(String.valueOf(ex.getMessage()));
        }
    }

    @PluginMethod
    public void finish(PluginCall call) {
        try {
            Entry e = entries.remove(call.getString("id"));
            if (e == null) { call.reject("Unknown save id"); return; }
            e.out.close();
            ContentValues v = new ContentValues();
            v.put(MediaStore.MediaColumns.IS_PENDING, 0);
            getContext().getContentResolver().update(e.uri, v, null, null);
            call.resolve();
        } catch (Exception ex) {
            call.reject(String.valueOf(ex.getMessage()));
        }
    }
}
''')

open(f"{PKG_DIR}/MainActivity.java", "w").write('''package com.lens.camera;

import android.os.Bundle;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(LensSaverPlugin.class);
        super.onCreate(savedInstanceState);
    }
}
''')

# Scoped storage (MediaStore RELATIVE_PATH) needs Android 10+
p = "android/variables.gradle"
s = open(p).read()
s = re.sub(r"minSdkVersion\s*=\s*\d+", "minSdkVersion = 29", s)
open(p, "w").write(s)
print("Saver plugin added")
