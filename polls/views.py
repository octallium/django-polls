from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question

# --------------------------------------------------------------------------------------
# CLASS BASED VIEWS (CBV)
# --------------------------------------------------------------------------------------


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self) -> QuerySet[Question]:
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# --------------------------------------------------------------------------------------


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    question: Question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice: Choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select a choice"},
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(
            redirect_to=reverse("polls:results", args=(question.id,))
        )


# --------------------------------------------------------------------------------------
# FUNCTION BASED VIEWS (FBV)
# --------------------------------------------------------------------------------------


# def index(request: HttpRequest) -> HttpResponse:
#     """Index page for polls app."""

#     # SQL => SELECT * FROM polls_question ORDER BY pub_date DESC LIMIT 5;
#     latest_question_list: QuerySet[Question] = Question.objects.order_by("-pub_date")[
#         :5
#     ]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)


# def detail(request: HttpRequest, question_id: int) -> HttpResponse:
#     # SQL => SELECT * FROM polls_question WHERE id=1;
#     question: Question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


# def results(request: HttpRequest, question_id: int) -> HttpResponse:
#     question: Question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})
