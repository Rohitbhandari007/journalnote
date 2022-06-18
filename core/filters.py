from django.forms import DateInput, TextInput
import django_filters
from django_filters import DateFilter, CharFilter, DateRangeFilter
from .models import Post


class OrderFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name="date_created",
                            label="FROM", lookup_expr='gte', widget=DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name="date_created", label="BEFORE",
                          lookup_expr='lte', widget=DateInput(attrs={'type': 'date'}))

    title = CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ["start_date", "end_date", "title"]
