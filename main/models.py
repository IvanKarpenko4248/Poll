from django.conf import settings
from django.db import models


class PollCategories(models.Model):
    title = models.CharField(verbose_name="Название", max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Polls(models.Model):
    title = models.CharField(verbose_name="Название", max_length=30)
    category = models.ForeignKey(to=PollCategories, verbose_name="Категория", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "тест"
        verbose_name_plural = "тесты"


class Questions(models.Model):
    question = models.TextField(verbose_name="Вопрос")
    poll = models.ForeignKey(to=Polls, verbose_name="Тест", on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name="Номер вопроса")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"
        unique_together = (("poll", 'order'))
        ordering = ("order",)


class Answers(models.Model):
    answer = models.CharField(verbose_name='Ответ', max_length=50)
    question = models.ForeignKey(to=Questions, verbose_name="Вопрос", on_delete=models.CASCADE)
    is_correct = models.BooleanField(verbose_name='Верный ответ', default=False)

    def __str__(self):
        return f'{self.question}: {self.answer}'

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "ответы"


class UsersAnswers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Questions, verbose_name="Вопрос", on_delete=models.CASCADE)
    is_correct = models.BooleanField(verbose_name="Правильный ответ", default=False)

    def __str__(self):
        return f'{self.user},{self.question}:{self.is_correct}'

    class Meta:
        verbose_name = "ответ пользователя"
        verbose_name_plural = "ответы пользователя"


class Results(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    poll = models.ForeignKey(Polls, on_delete=models.CASCADE, verbose_name='Тест')
    points = models.IntegerField(verbose_name="Количество правильных ответов")
    max_points = models.IntegerField(verbose_name="Максимальное количество правильных ответов")

    def __str__(self):
        return f'{self.user}, {self.poll}:{self.points}'

    class Meta:
        verbose_name = "результат"
        verbose_name_plural = "результаты"
