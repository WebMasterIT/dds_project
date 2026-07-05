from django import forms
from .models import Record

 
class RecordForm(forms.ModelForm):
    class Meta:
        model = Record              
        fields = [           
            "created",
            "status",
            "type",
            "category",
            "subcategory",
            "amount",
            "comment",
        ]

        widgets = {
            "created": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "subcategory": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        } 
    def clean(self):
        cleaned_data = super().clean()  
        type = cleaned_data.get("type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")
 
        if type and category and category.type != type:
            self.add_error("category", "Эта категория не относится к выбранному типу.")
 
        if category and subcategory and subcategory.category != category:
            self.add_error("subcategory", "Эта подкатегория не относится к выбранной категории.")

        return cleaned_data