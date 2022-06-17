from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.generic.edit import CreateView
from django.shortcuts import redirect

from main.models import *


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class PollsMainView(LoginRequiredMixin, generic.ListView):
    model = Polls
    template_name = "poll/home.html"
    context_object_name = 'polls'


class QuestionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Questions
    template_name = "poll/question.html"
    context_object_name = 'question'
    queryset = Questions.objects.all()
    slug_url_kwarg = "pk"

    def post(self, *args, **kwargs):
        question = Questions.objects.filter(id=kwargs.get('pk')).first()
        if not question:
            return HttpResponse("Объект не найден")
        user_answers = list(map(int, self.request.POST.getlist("answer")))
        answers = question.answers_set.all()
        is_correct = True
        for answer in answers:
            if answer.is_correct and answer.id not in user_answers:
                is_correct = False
                break
            if not answer.is_correct and answer.id in user_answers:
                is_correct = False
                break

        UsersAnswers.objects.create(
            user=self.request.user,
            question=question,
            is_correct=is_correct,
        )

        next_question = Questions.objects.filter(poll=question.poll, order__gt=question.order).first()
        if not next_question:
            user_answers = UsersAnswers.objects.filter(user=self.request.user, question__poll=question.poll)
            points = 0
            for answer in user_answers:
                if answer.is_correct:
                    points += 1

            Results.objects.create(
                user=self.request.user,
                poll=question.poll,
                points=points,
                max_points=len(user_answers),
            )
            return redirect("poll_detail", pk=question.poll.id)

        return redirect('question_detail', pk=next_question.id)


class PollDetailView(generic.View):

    def get(self, *args, **kwargs):
        poll = Polls.objects.filter(id=kwargs.get("pk", None)).first()
        if not poll:
            return HttpResponse("Объект не найден")

        res = Results.objects.filter(user=self.request.user, poll=poll).first()
        if res:
            percent = round(res.points / res.max_points * 100, 2)
            return render(self.request, "Poll/poll_result.html", context={"result": res, 'percent': percent})
        questions = Questions.objects.filter(poll=poll)
        for question in questions:
            user_answer = UsersAnswers.objects.filter(user=self.request.user, question=question).first()
            if not user_answer:
                return redirect('question_detail', pk=question.id)
