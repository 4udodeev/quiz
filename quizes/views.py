from django.shortcuts import render, redirect
import pandas as pd

from .models import Quiz, Result, Question, Answer


def index(request):
    return render(
        request,
        'quizes/index.html'
    )


def quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.get_questions()
    context = {'quiz': quiz, 'questions': questions}
    return render(request, 'quizes/quiz.html', context)


def save_result(request, quiz_id):
    if request.method == 'POST':
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.question_set.all()
        score = 0
        total_questions = 0
        detail = ""
        
        for question in questions:
            total_questions += 1
            selected_answer_ids = request.POST.getlist('question_' + str(question.id))
            correct_answer_ids = [str(answer.id) for answer in question.answer_set.filter(is_correct=True)]
            selected_answer_names = [Answer.objects.get(id=answer_id).name for answer_id in selected_answer_ids]
            correct_answer_names = [Answer.objects.get(id=answer_id).name for answer_id in correct_answer_ids]
            
            selected_answer_names.sort()
            correct_answer_names.sort()

            if set(selected_answer_ids) == set(correct_answer_ids) and set(selected_answer_ids) <= set(correct_answer_ids):
                score += question.question_weight
                detail += f"Вопрос: {question.name} - Ответы: {'#'.join(selected_answer_names)} - Правильные ответы: {'#'.join(correct_answer_names)} - Результат: Верно\n"
            else:
                detail += f"Вопрос: {question.name} - Ответы: {'#'.join(selected_answer_names)} - Правильные ответы: {'#'.join(correct_answer_names)} - Результат: Неверно\n"
                
        user = request.user
        result = Result.objects.create(quiz=quiz, user=user, score=score, detail=detail)
        return redirect('result_detail', result_id=result.id)
    
    return redirect('index')


def result_detail(request, result_id):
    result = Result.objects.get(id=result_id)
    return render(request, 'quizes/result_detail.html', {'result': result})


def upload_quiz(request):
    if request.method == 'POST' and request.FILES['quiz_file']:
        quiz_file = request.FILES['quiz_file']
        df = pd.read_excel(quiz_file)
        user = request.user

        for index, row in df.iterrows():
            question_text = row['Вопрос']
            question_type = 'multiplie_choice' if '#' in str(row['Правильные ответы']) else 'single_choice'
            question_weight = row['Уровень сложности']
            quiz_id = Quiz.objects.get(pk=2)

            if 'Расставьте в правильном порядке' in question_text:
                question_type = 'ranged'
        
            question = Question.objects.create(
                name=question_text,
                description=question_text,
                question_type=question_type,
                question_weight=question_weight,
                created_by=user,
                quiz_id=quiz_id,
            )
            answers = str(row['Варианты ответов']).split('#')
            correct_answers = str(row['Правильные ответы']).split('#')
        
            for answer_text in answers:
                is_correct = answer_text in correct_answers
                Answer.objects.create(
                    name=answer_text,
                    description=answer_text,
                    is_correct=is_correct,
                    question_id=question,
                    created_by=user,
                )
    
        return render(request, 'quizes/index.html')
    
    return render(request, 'quizes/upload_quiz.html')
