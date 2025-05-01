from django.shortcuts import render, get_object_or_404
from .models import Project, Category


def project_list(request):
    projects = Project.objects.all()
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        projects = projects.filter(category=category)

    context = {
        'projects': projects,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'projects/project_list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.filter(
        category=project.category).exclude(id=project.id)[:3]

    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'projects/project_detail.html', context)
