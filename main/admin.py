from django.contrib import admin
from main.models import PollCategories, Polls, Questions, Answers, UsersAnswers, Results
from nested_admin.nested import *


class AnswerInline(NestedTabularInline):
    model = Answers
    extra = 0


class QuestionInline(NestedStackedInline):
    model = Questions
    extra = 0
    inlines = [AnswerInline]
    ordering = ("order",)


@admin.register(Polls)
class PollAdmin(NestedModelAdmin):
    inlines = [QuestionInline]


@admin.register(PollCategories, UsersAnswers, Results)
class DefaultAdmin(admin.ModelAdmin):
    pass
