[app]

title = Consulta Preco RMarket
package.name = precoregistil
package.domain = org.rmarket
source.dir = .
source.exts = py,png,jpg,kv,atlas
version = 0.1

# Forçar versões estáveis de compatibilidade no buildozer
requirements = python3,kivy,requests,beautifulsoup4

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.sdk = 30
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
