from django.shortcuts import render, redirect
import random
import markdown2
from django.urls import reverse
from . import util

def index(request):
    """Displays the list of all encyclopedia entries."""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    """Retrieves and displays a specific encyclopedia entry.
       Shows an alert if the entry does not exist.
    """
    content = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content) if content else None,
        "not_found": content is None  # Pass flag if page is missing
    })

def search(request):
    """Handles search queries and displays relevant results.
       If an exact match exists, redirects to that entry.
    """
    query = request.GET.get("q", "").strip().lower()
    entries = util.list_entries()
    results = [entry for entry in entries if query in entry.lower()]

    if query in map(str.lower, entries):
        return redirect(reverse("entry_page", args=[query]))

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })

def new_page(request):
    """Allows users to create a new encyclopedia entry."""
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()

        if title.lower() in map(str.lower, util.list_entries()):
            return render(request, "encyclopedia/error.html", {
                "message": "This page already exists."
            })

        util.save_entry(title, content)
        return redirect(reverse("entry_page", args=[title]))

    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    """Allows users to edit an existing entry."""
    content = util.get_entry(title)

    if request.method == "POST":
        new_content = request.POST.get("content").strip()
        util.save_entry(title, new_content)
        return redirect(reverse("entry_page", args=[title]))

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    """Redirects users to a randomly chosen entry."""
    entries = util.list_entries()
    if entries:
        return redirect(reverse("entry_page", args=[random.choice(entries)]))
    return render(request, "encyclopedia/error.html", {
        "message": "No entries available!"
    })
