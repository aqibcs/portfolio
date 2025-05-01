from django.contrib import admin
from .models import Category, Technology, Project


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured', 'created_at')
    list_filter = ('category', 'technologies', 'featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ('technologies', )
