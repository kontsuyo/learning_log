from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render


def register(request):
    """新しいユーザーを登録する"""
    if request.method != "POST":
        # 空のユーザー登録フォームを生成する
        form = UserCreationForm()

    if request.method == "POST":
        # 入力済みのフォームを処理する
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # ユーザーをログインさせてホームページにリダイレクトする
            login(request=request, user=new_user)
            return redirect(to="learning_logs:index")

    context = {"form": form}
    return render(
        request=request, template_name="registration/register.html", context=context
    )
