from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SubCategorySerializer
from django.shortcuts import render, redirect, get_object_or_404
from .models import Record, Status, Type, Category, SubCategory
from .forms import RecordForm
from .serializers import SubCategorySerializer, CategorySerializer


def record_list(request): 
    records = Record.objects.all() 
    date_from = request.GET.get("date_from")
    

    date_to = request.GET.get("date_to")
    status_id = request.GET.get("status")
    type_id = request.GET.get("type")
    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")
 
    date_error = None
    if date_from and date_to and date_from > date_to:
        date_error = "Дата «с» не может быть позже даты «по»."
        date_from = None
        date_to = None

    if date_from:
        records = records.filter(created__gte=date_from)
    if date_to:
        records = records.filter(created__lte=date_to)
    if status_id:
        records = records.filter(status_id=status_id)
    if type_id:
        records = records.filter(type_id=type_id)
    if category_id:
        records = records.filter(category_id=category_id)
    if subcategory_id:
        records = records.filter(subcategory_id=subcategory_id)

    context = {
        "records": records,
        "statuses": Status.objects.all(),
        "types": Type.objects.all(),
        "categories": Category.objects.all(),
        "subcategories": SubCategory.objects.all(),
        "date_error": date_error,
    }
    return render(request, "cashflow/record_list.html", context)
def record_create(request):
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("record_list") 
    else: 
        form = RecordForm()
 
    return render(request, "cashflow/record_form.html", {"form": form, "title": "Новая запись"})
 
def record_edit(request, pk): 
    record = get_object_or_404(Record, pk=pk)

    if request.method == "POST": 
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect("record_list")
    else: 
        form = RecordForm(instance=record)

    return render(request, "cashflow/record_form.html", {"form": form, "title": "Редактировать запись"})

def record_delete(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == "POST":
        record.delete()             
        return redirect("record_list")
    return render(request, "cashflow/record_confirm_delete.html", {"record": record})

@api_view(["GET"])
def subcategories_api(request):
    category_id = request.GET.get("category") 
    subcategories = SubCategory.objects.filter(category_id=category_id) 
    serializer = SubCategorySerializer(subcategories, many=True)         
    return Response(serializer.data)
@api_view(["GET"])
def categories_api(request):
    type_id = request.GET.get("type")                    # номер типа из адреса
    categories = Category.objects.filter(type_id=type_id)  # только его категории
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)