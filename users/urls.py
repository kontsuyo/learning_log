"""users用URLパターンの定義"""
from django.urls import include
from django.urls import path

from users import views

app_name = "users"
urlpatterns = [
    # デフォルトの認証用URLを取り込む
    # login,logoutといった名前付きのURLパターンが含まれる
    # デフォルトのlogin.view,logout.viewへルーティングする
    path("", include("django.contrib.auth.urls")),
    # ユーザー登録ページ
    path("register", views.register, name="register"),
]
