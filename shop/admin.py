from django.contrib import admin
from shop.models import Category, Product, Offer, Images
from mptt.admin import MPTTModelAdmin
from properties.models import CategoryProperty, ProductProperty
from filters.models import FilterCategory, ProductFilter, FilterSelect
from django.forms import TextInput, ModelForm, Textarea, Select


# Модель категории
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']



class CategoryPropertyInline(admin.TabularInline):
    model = CategoryProperty
    extra = 1
    verbose_name_plural = 'Params'
    suit_classes = 'suit-tab suit-tab-params'


class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1
    verbose_name_plural = 'Images'
    suit_classes = 'suit-tab suit-tab-images'


class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty
    extra = 1
    verbose_name_plural = 'Params'
    suit_classes = 'suit-tab suit-tab-params'


class OfferInline(admin.TabularInline):
    model = Offer
    extra = 1
    verbose_name_plural = 'Offers'
    suit_classes = 'suit-tab suit-tab-offers'


class ProductFilterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductFilterForm, self).__init__(*args, **kwargs)
        if self.instance:
            i = self.instance
            if i.filter_category:
                self.fields["values"].queryset = \
                    FilterSelect.objects.filter(filter_category=i.filter_category)

    class Meta:
        model = ProductFilter
        fields = '__all__'


class ProductFilterInline(admin.TabularInline):
    form = ProductFilterForm
    model = ProductFilter
    extra = 1
    verbose_name_plural = 'Filters'
    suit_classes = 'suit-tab suit-tab-filters'


class FilterCategoryInline(admin.TabularInline):
    model = FilterCategory
    extra = 1
    verbose_name_plural = 'Filters'
    suit_classes = 'suit-tab suit-tab-filters'




@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    inlines = [CategoryPropertyInline, FilterCategoryInline, ]
    suit_form_tabs = (('general', 'Основные'),
                      ('params', 'Параметры'),
                      ('filters', 'Фильтры'))
    fieldsets = [
        ('General', {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': [
                'name',
                'title',
                'description',
                'keywords',
                'image',
                'parent',
                'url',
            ]
        }),
    ]


# Модель товара
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
