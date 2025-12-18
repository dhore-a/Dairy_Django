from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DiaryEntry
from .forms import DiaryEntryForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

@login_required
def entry_list(request):
    query = request.GET.get('q')
    entries = DiaryEntry.objects.filter(author=request.user)
    if query:
        entries = entries.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, 'diary_app/entry_list.html', {'entries': entries})

@login_required
def entry_detail(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, author=request.user)
    return render(request, 'diary_app/entry_detail.html', {'entry': entry})

@login_required
def entry_create(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            return redirect('entry_list')
    else:
        form = DiaryEntryForm()
    return render(request, 'diary_app/entry_form.html', {'form': form})

@login_required
def entry_update(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, author=request.user)
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('entry_list')
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, 'diary_app/entry_form.html', {'form': form})

@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, author=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('entry_list')
    return render(request, 'diary_app/entry_confirm_delete.html', {'entry': entry})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after register
            return redirect('/')  # redirect to homepage or dashboard
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
