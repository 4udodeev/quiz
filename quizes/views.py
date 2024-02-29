from django.shortcuts import render
import json

from .models import Quiz


def index(request):
    return render(
        request,
        'quizes/index.html'
    )


def quiz(request, test_id):
    quiz = Quiz.objects.get(pk=1)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.description)
        questions.append({str(q)+"/"+q.question_type: answers})
    data = json.loads(str(questions).replace("'", "\""))
    return render(
        request,
        'quizes/quiz.html',
        {'test_id': test_id, 'data': data}
    )
