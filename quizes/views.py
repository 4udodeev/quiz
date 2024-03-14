from django.db.models import Subquery, OuterRef, Prefetch
from django.shortcuts import render
from django.views.generic import ListView

from .models import Question, Answer


def index(request):
    return render(
        request,
        'quizes/index.html'
    )


class QuestionListView(ListView):
    model = Question
    paginate_by = 1
    test_id = None

    def get_queryset(self):
        subquery = Answer.objects.filter(
            question_id=OuterRef('id')
        ).values('description')

        return Question.objects.filter(quiz_id=1).prefetch_related(
            Prefetch('answer_set', queryset=Answer.objects.only('description'), to_attr='answers')
        )
