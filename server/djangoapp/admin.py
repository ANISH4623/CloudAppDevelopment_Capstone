from django.contrib import admin
# from .models import related models
from .models import CarMake,CarModel

# # Register your models here.
# admin.site.register(CarMake)
# admin.site.register(CarModel)

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['car_make', 'name', 'dealer_id', 'type', 'year']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    inlines = [CarModelInline]    

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)