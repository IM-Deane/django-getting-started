from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone


from .models import Choice, Question


# Abstraction of the typical list/gallery view found in websites
class IndexView(generic.ListView):
    # Specifies a custom page template
    template_name = "polls/index.html"
    # Override the auto-generated context object
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions. Questions set in 
        the future should be excluded."""

        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


# Abstraction of the typical detail view found in websites
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# /vote
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always redirect after succesful post. This avoids duplicate submissions
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))