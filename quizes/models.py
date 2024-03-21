from django.contrib.auth import get_user_model
from django.db import models

from datetime import datetime
import random


User = get_user_model()


class BaseModel(models.Model):

    code = models.CharField(
        max_length=256,
        verbose_name='Код',
        default=None,
        blank=True,
        null=True
    )
    name = models.CharField(
        max_length=256,
        default='',
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание',
        default=None,
        blank=True
    )
    created_at = models.DateTimeField(
        default=datetime.now(),
        verbose_name='Дата создания'
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
        verbose_name='Дата изменения'
    )

    class Meta:
        abstract = True


class Quiz(BaseModel):
    """Тест"""

    time = models.IntegerField(verbose_name='Продолжительность теста в минутах')
    pass_score = models.IntegerField(help_text='Проходной балл')
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Кто создал',
        related_name='user_created_quizes'
    )
    modified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Кто изменил',
        related_name='user_modified_quizes'
    )

    class Meta():
        verbose_name_plural = 'Quizes'

    def __str__(self):
        return self.name

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions


class Question(BaseModel):
    QUESTION_TYPES = [
        ('single_choice', 'Единственный выбор'),
        ('multiplie_choice', 'Множественный выбор'),
    ]
    question_type = models.CharField(
        max_length=30,
        choices=QUESTION_TYPES,
        default='single_choice'
    )
    quiz_id = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE
    )
    question_weight = models.IntegerField(
        help_text='Вес вопроса',
        default=1
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Кто создал',
        related_name='user_created_questions'
    )
    modified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Кто изменил',
        related_name='user_modified_questions'
    )

    def __str__(self) -> str:
        return self.name

    def get_answers(self):
        answers = list(self.answer_set.all())
        random.shuffle(answers)
        return answers


class Answer(BaseModel):
    is_correct = models.BooleanField(default=False)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Кто создал',
        related_name='user_created_answers'
    )
    modified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Кто изменил',
        related_name='user_modified_answers'
    )

    def __str__(self) -> str:
        return self.name


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    detail = models.TextField()

    def __str__(self) -> str:
        return f'{self.user.last_name} {self.user.first_name} - {self.quiz.name}'
