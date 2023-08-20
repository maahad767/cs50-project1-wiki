import random as rnd

from django import forms
from django.shortcuts import redirect, render
from django.urls import reverse

from markdown2 import Markdown

from . import util

markdowner = Markdown()


class EntryCreateForm(forms.Form):
    title = forms.CharField(max_length=500)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":"3", "cols": 4}))

    def clean_title(self):
        title = self.cleaned_data["title"]
        
        if util.get_entry(title):
            raise forms.ValidationError(f"Page with title {title} already exists!")
        
        return title
    
class EntryUpdateForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def detail(request, *args, **kwargs):
    title = kwargs.get("title")
    wiki = util.get_entry(title=kwargs.get("title"))
    
    if not wiki:
        return render(request, "encyclopedia/404.html", {
            "title": title,
        })
    
    return render(request, "encyclopedia/detail.html", {
        "entry": markdowner.convert(wiki),
        "title": title,
    })


def add(request):
    form = EntryCreateForm()
    
    if request.method == "POST":
        form = EntryCreateForm(data=request.POST)
        
        if form.is_valid():
            util.save_entry(title=form.cleaned_data["title"], content=form.cleaned_data["content"])
            return redirect(reverse("detail", kwargs={"title": form.cleaned_data["title"]}))
        
        return render(request, "encyclopedia/create-form.html", {"form": form})
    
    return render(request, "encyclopedia/create-form.html", {"form": form})
    
def edit(request, *args, **kwargs):
    title = kwargs.get("title")
    content = util.get_entry(title)
    data = {
        "content": content
    }
    form = EntryUpdateForm(initial=data)
    
    if request.method == "POST":
        form = EntryUpdateForm(data=request.POST)
        
        if form.is_valid():
            util.save_entry(title=title, content=form.cleaned_data["content"])
            return redirect(reverse("detail", kwargs={"title": title}))
        
        return render(request, "encyclopedia/update-form.html", {"form": form, "title": title})
    
    return render(request, "encyclopedia/update-form.html", {"form": form, "title": title})
    
def search(request, *args, **kwargs):
    q = request.GET.get("q")
    entries = util.list_entries()
    exact_entry = util.get_entry(q)
    
    if exact_entry:
        return redirect(reverse('detail', kwargs={"title": q}))
    
    filtered_entries = filter(lambda title: q.lower() in title.lower(), entries)
    
    return render(request, "encyclopedia/search.html", {
        "entries": filtered_entries
    })


def random(request):
    entries = util.list_entries()
    return redirect(reverse("detail", kwargs={"title": rnd.choice(entries)}))
