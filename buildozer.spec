[app]

# (str) Title of your application
title = Consulta Preco RMarket

# (str) Package name
package.name = precoregistil

# (str) Package domain (needed for android packaging)
package.domain = org.rmarket

# (list) Source files to include (let it empty to include all files)
source.dir = .

# (list) Source file extensions to include (let it empty to include all files)
source.exts = py,png,jpg,kv,atlas

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,requests,beautifulsoup4,pyjnius

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 30

# (str) Android NDK version to use (v25b is required for Pyjnius compatibility)
android.ndk = 25b

# (bool) Skip target API check
#android.skip_api_check = False

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
