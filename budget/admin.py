from django.contrib import admin

from .models import Category, Expense, Project

admin.site.register(Project)
admin.site.register(Expense)
admin.site.register(Category)
