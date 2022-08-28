from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from learning_logs.form import EntryForm
from learning_logs.form import TopicForm
from learning_logs.models import Entry
from learning_logs.models import Topic


def index(request):
    """学習ノートのホームページを表示する"""
    return render(request=request, template_name="learning_logs/index.html")


@login_required
def topics(request):
    """すべてのトピックを表示する"""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}
    return render(
        request=request, template_name="learning_logs/topics.html", context=context
    )


@login_required
def topic(request, topic_id):
    """1つのトピックとそれについてのすべての記事を表示する"""
    topic = get_object_or_404(Topic, id=topic_id)
    # トピックが現在のユーザーが所持するものであることを確認する
    check_topic_owner(topic, request)

    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(
        request=request, template_name="learning_logs/topic.html", context=context
    )


@login_required
def new_topic(request):
    """新規トピックを追加する"""
    if request.method != "POST":
        # データは送信されていないので空のフォームを生成する
        form = TopicForm()

    if request.method == "POST":
        # POSTで送信されたのでこれを処理する
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect(to="learning_logs:topics")

    context = {"form": form}
    return render(
        request=request, template_name="learning_logs/new_topic.html", context=context
    )


@login_required
def new_entry(request, topic_id):
    """特定のトピックに新規記事を追加する"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)

    if request.method != "POST":
        form = EntryForm()

    if request.method == "POST":
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect(to="learning_logs:topic", topic_id=topic.id)

    # 空または無効のフォームを表示する
    context = {"topic": topic, "form": form}
    return render(
        request=request, template_name="learning_logs/new_entry.html", context=context
    )


@login_required
def edit_entry(request, entry_id):
    """既存の記事の編集"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)

    if request.method != "POST":
        # 初回リクエスト時にはDBに保存されている記事の内容がフォームに埋め込まれている
        form = EntryForm(instance=entry)

    if request.method == "POST":
        # POSTでデータが送信されたのでこれを処理する
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="learning_logs:topic", topic_id=topic.id)

    # 空または無効のフォームを表示する
    context = {"entry": entry, "topic": topic, "form": form}
    return render(
        request=request, template_name="learning_logs/edit_entry.html", context=context
    )


def check_topic_owner(topic, request):
    """トピックと関連付けられたユーザーとログインユーザーの比較"""
    if topic.owner != request.user:
        raise Http404
