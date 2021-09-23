import re
from django.shortcuts import render, redirect
from django import forms
import markdown2
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
from random import randint

class CreateEntryForm(forms.Form):
    Title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    Entry = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
    'placeholder': 'Type markdown here...', 'margin':'20px'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Search for a specific page
def search(request):
    q = request.GET['q']
    matches = []
    entries = util.list_entries()
    for title in entries:
        if title.lower() == q.lower():
            return redirect(reverse('entry', kwargs={'title': title}))
        else:
            if q.lower() in title.lower():
                matches.append(title)
    if matches:
        return render(request, "encyclopedia/search.html", {
            'matches': matches
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": f"<h2>Your search '{q}' did not match any entries</h2>"
        })

# Render a specific wiki page
def entry(request, title):

    # Pull the entry
    mdown = util.get_entry(title)

    # Make sure the entry was found and convert it to HTML
    if mdown:
        html = markdown2.markdown(mdown)
        return render(request, "encyclopedia/entry.html", {
            "title": title, 
            "content": html
        })

    # Render an  error page if entry is not found
    else:
        return render(request, "encyclopedia/error.html", {
            "message": f"<h1>'{title}' page does not exist.</h1>"
        })

# Create a new entry and add it to the encyclopedia
def create(request):
    if request.method == "POST":
        form = CreateEntryForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data["Title"]
            entry = form.cleaned_data["Entry"]

            entries = util.list_entries()

            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    "message": f"<h1> '{title}' already exists."
                })
            
            else:
                util.save_entry(title, entry)
                return redirect(reverse('entry', kwargs={'title': title}))
                
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    else:       
        return render(request, "encyclopedia/create.html", {
            'form': CreateEntryForm()
        })

# Edit a page and save the changes
def edit(request):
    if request.method == 'POST':
        
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect(reverse('entry', kwargs={'title': title}))

    else:
        title = request.GET['title']
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'content': content
        })


# Pick a random page to show
def randompage(request):

    # Pull the list of entries
    entries = util.list_entries()
    length = len(entries)

    # Get a random int used to pick the random page
    rand_int = randint(1, length - 1)

    # Assign the title of the random page
    rand_title = entries[rand_int]

    # Redirect user to entry view with the random title
    return redirect(reverse('entry', kwargs={'title': rand_title}))
    
    



