from django.http import Http404
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        result = self.model.objects.prefetch_related(
            'genres', 
            'persons',
        ).values(
            'id', 
            'title', 
            'description', 
            'creation_date', 
            'rating',
            'type'
        ).annotate(
            genres=ArrayAgg("genres__name", distinct=True),
            actors=ArrayAgg("persons__full_name", filter=Q(personfilmwork__role='actor'), distinct=True),  
            directors=ArrayAgg("persons__full_name", filter=Q(personfilmwork__role='director'), distinct=True),  
            writers=ArrayAgg("persons__full_name", filter=Q(personfilmwork__role='writer'), distinct=True),  
        )
        return result

    def render_to_response(self, context, **response_kwargs):
        print(context, 111)
        return JsonResponse(context) 

class MoviesListApi(MoviesApiMixin, BaseListView):
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, 
            self.paginate_by,
        )
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": None if page.number == 1 else paginator.validate_number(page.number-1),
            "next": None if page.number == paginator.num_pages else paginator.validate_number(page.number+1),
            "results" : list(queryset)
        }

class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return self.object