from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django import forms
import markdown2


from . import util
import encyclopedia


class NewEntryForm(forms.Form):
    title = forms.CharField(label = "Title")
    text = forms.CharField(widget=forms.Textarea, label = "Markdown Text")



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# directs user to the error page
#def error(request):
#    return render(request, "encyclopedia/error.html")


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
        return render(request, "encyclopedia/error.html", {
            "message": "Page Not Found"
        })

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
        return render(request, "encyclopedia/error.html", {
            "message": "No Matching Entry Found"
        })


# create a new entry
def new(request):

    # for GET requests, display new entry form
    if request.method == "GET":

        # NewEntryForm defined above, has a field for a title and for markdown text
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
        })

    # if received as a POST method, attempt to create a new entry
    elif request.method == "POST":
        
        # store title and markdown text from NewEntryForm
        form = NewEntryForm(request.POST)

        # check if user inputs are valid
        if form.is_valid():

            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]

            # check if an entry with inputted title already exists
            if util.get_entry(title):

                # if entry already exists, redirect user to error page
                return render(request, "encyclopedia/error.html", {
                    "message": "Entry Already Exists"
                })

            # otherwise, create new entry from form data
            util.save_entry(title, text)

            # direct user to new entry page
            return entry(request, title) 

        # if inputs are not valid, return user to input page
        else: 
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

    # if method is neither GET nor POST, return an error page
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Page Not Found"
        })




# TODO
# edit page
# maybe can use title to match to the filename of a md file?
    # fundamentally they have to exist
