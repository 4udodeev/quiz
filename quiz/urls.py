from django.contrib import admin
from django.urls import path

from quizes import views


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        '',
        views.index,
        name='index'
    ),
    path(
        'quiz/<int:quiz_id>/',
        views.quiz,
        name='quiz'
    ),
    path(
        'quiz/<int:quiz_id>/save_result/',
        views.save_result,
        name='save_result'
    ),
    path(
        'result/<int:result_id>/',
        views.result_detail,
        name='result_detail'
    ),
    path(
        'upload_quiz/',
        views.upload_quiz,
        name='upload_quiz'
    ),
]
