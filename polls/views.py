from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from polls.models import Question, Choice
from django.db.models import F
from django.views import generic
from django.urls import reverse


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "question_text_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choices = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "error_msg": "You didn't select a choice.",
                "question": question,
            },
        )
    else:
        selected_choices.votes = F("votes") + 1
        selected_choices.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
