from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    


# directs user to the error page
def error(request):
    return render(request, "encyclopedia/error.html")


# directs user to a wiki entry page if it exists
def entry(request, entry):

    # check if entry exists
    if util.get_entry(entry):

        # if entry exists, convert markdown file to html
        html = markdown2.markdown(util.get_entry(entry))

        # render entry.html with info from markdown
        return render(request, "encyclopedia/wiki/entry.html", {
            "title": entry,
            "html" : html
        })   

    else:  
        # if entry is not found, redirect to error page
        return render(request, "encyclopedia/error.html")

def search(request):

    # define query on a variable for easier use
    query = request.GET.get('q')

    # check if query has an entry and return that page if true
    if util.get_entry(query):    
        return (entry(request,  query))

    else:
        # create list to store entries close to search term if no match is found
        possible_results = []

        # check if query is a substring of any entries
        for result in util.list_entries():

            # results are not case sensitive
            if query.lower() in result.lower():

                # if a match is found, record the entry in the possible results list
                possible_results.append(result)

        # pass the final possible results array to search.html if any are found
        if possible_results:

            return render(request, "encyclopedia/search.html", {
                "entries": possible_results
            })

        # otherwise, return an error page
        return render(request, "encyclopedia/error.html")
# TODO
